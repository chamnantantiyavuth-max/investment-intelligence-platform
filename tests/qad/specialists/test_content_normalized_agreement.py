"""Cross-retrieval agreement ignores per-request script tokens only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qad.m6.content_norm import (
    content_normalized_sha256,
    strip_script_elements,
)
from qad.m6.receipt_file import load_persisted_receipts, persist_receipts
from qad.models.family_b import FactRecordVerification_status
from qad.specialists.contract import RESULT_CONTRACT_ID
from qad.specialists.ingestion import ingest_result
from qad.specialists.routing import route_case
from research.qad_pilot.unh.case_slice import build_unh_case

PASSAGE = "expected net 2.48 percent"
URL = "https://www.cms.gov/newsroom/fact-sheets/2027-medicare-advantage-part-d-rate-announcement"


def _routed():
    priority = json.loads(
        Path("research/qad-cases/CASE-2026-001/founder-priority.json").read_text(
            encoding="utf-8"
        )
    )
    bundle = build_unh_case()
    routed = route_case(bundle, max_n=3, founder_priority=priority)
    return bundle, routed


def _charter(item) -> dict:
    return {
        "gap_id": item.gap_id,
        "specialist_id": item.specialist_id,
        "canonical_role": item.canonical_role,
        "investigator_charter_id": item.investigator_charter_id,
        "allowed_source_classes": item.charter_record["allowed_source_classes"],
        "budget": item.budget,
        "desk_research_only": True,
    }


def _result(item, claims: list[dict]) -> dict:
    return {
        "contract": RESULT_CONTRACT_ID,
        "case_id": "CASE-2026-001",
        "gap_id": item.gap_id,
        "investigator_charter_id": item.investigator_charter_id,
        "specialist_id": item.specialist_id,
        "actor_id": "agent-a",
        "canonical_role": item.canonical_role,
        "desk_research_only": True,
        "disposition": "ANSWERED",
        "falsifiable_question": item.falsifiable_question,
        "stop_rule_triggered": None,
        "usage": {"tool_calls": 1, "sources": 1, "minutes": 5},
        "sampling_limitations": "Public documents only.",
        "claims": claims,
        "findings": [],
    }


def _claim(document_quotation: str, expected: str) -> dict:
    return {
        "statement": document_quotation,
        "evidence_type": "FACT",
        "source": {
            "url": URL,
            "retrieval_timestamp": "2026-10-17T14:30:16Z",
            "source_date": "2026-04-06",
            "publisher": "CMS",
            "source_tier": "L3",
            "source_type": "GOVERNMENT_DATA",
            "title": "2027 Medicare Advantage Rate Announcement",
            "quotation": document_quotation,
            "expected_sha256": expected,
        },
    }


def _mint(document: bytes):
    from qad.m6.original_fetch import mint_http_source

    def opener(got, _user_agent, _timeout):
        assert got == URL
        return document

    verification, error = mint_http_source(
        URL,
        opener=opener,
        source_tier="L3",
        source_type="GOVERNMENT_DATA",
        title="fixture",
        publication_date="2026-04-06",
    )
    assert verification is not None, error
    return verification


def _html(body: str, script: str) -> bytes:
    return (
        f"<html><body><p>{body}</p>"
        f'<script type="text/javascript" src="/{script}"></script>'
        "</body></html>"
    ).encode("utf-8")


def _ingest(document: bytes, lead: bytes, quotation: str):
    bundle, routed = _routed()
    item = routed.selected[1]
    expected = hashlib.sha256(lead).hexdigest()
    claim = _claim(quotation, expected)
    receipt = _mint(document)
    outcome = ingest_result(
        bundle,
        _result(item, [claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
        source_verifications=[receipt],
        evidence_lead_bytes={expected: lead},
    )
    return bundle, outcome


def test_script_stripping_removes_script_elements_and_nothing_else():
    raw = b"<p>Keep 1</p><style>color:1</style><!-- note --><ScRiPt src='a'>tok</sCrIpT>"
    stripped = strip_script_elements(raw)
    assert stripped == b"<p>Keep 1</p><style>color:1</style><!-- note -->"
    unclosed = b"<p>stay</p><script>no end"
    assert strip_script_elements(unclosed) == unclosed
    same = _html(PASSAGE, "token-a")
    other = _html(PASSAGE, "token-b")
    assert hashlib.sha256(same).hexdigest() != hashlib.sha256(other).hexdigest()
    assert content_normalized_sha256(same) == content_normalized_sha256(other)
    changed = _html(PASSAGE.replace("2.48", "2.49"), "token-a")
    assert content_normalized_sha256(same) != content_normalized_sha256(changed)


def test_script_only_difference_agrees_and_promotes():
    lead = _html(f"{PASSAGE} count 7", "token-aaa")
    fetched = _html(f"{PASSAGE} count 7", "token-bbb")
    assert content_normalized_sha256(lead) == content_normalized_sha256(fetched)
    bundle, outcome = _ingest(fetched, lead, f"{PASSAGE} count 7")
    assert outcome.verified_fact_ids
    assert outcome.quarantined == []
    fact = bundle.registry.load("FACT-01", outcome.verified_fact_ids[0])
    assert fact.verification_status == FactRecordVerification_status.VERIFIED
    assert outcome.cross_retrieval[0]["agreement"] == "normalized"
    assert (
        outcome.cross_retrieval[0]["normalized_sha256"]
        == outcome.cross_retrieval[0]["evidence_lead_normalized_sha256"]
    )
    assert outcome.cross_retrieval[0]["raw_sha256"] != hashlib.sha256(lead).hexdigest()


def test_body_or_passage_digit_outside_script_stays_unverified():
    lead = _html(f"{PASSAGE}</p><p>count 7", "token-aaa")
    fetched = _html(f"{PASSAGE}</p><p>count 8", "token-bbb")
    assert content_normalized_sha256(lead) != content_normalized_sha256(fetched)
    _bundle, outcome = _ingest(fetched, lead, PASSAGE)
    assert outcome.verified_fact_ids == []
    assert len(outcome.quarantined) == 1
    assert outcome.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert "normalized sha256" in outcome.quarantined[0]["reason"]
    assert "!=" in outcome.quarantined[0]["reason"]

    lead_passage = _html(PASSAGE, "token-aaa")
    fetched_passage = _html(PASSAGE.replace("2.48", "2.49"), "token-aaa")
    _bundle, shifted = _ingest(
        fetched_passage,
        lead_passage,
        PASSAGE.replace("2.48", "2.49"),
    )
    assert shifted.verified_fact_ids == []
    assert shifted.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert "normalized sha256" in shifted.quarantined[0]["reason"]


def test_quotation_only_inside_script_does_not_count():
    document = (
        b"<html><body><p>no rate in the body</p><script>expected net 2.48 percent</script></body></html>"
    )
    bundle, routed = _routed()
    item = routed.selected[1]
    claim = _claim(PASSAGE, "")
    claim["source"].pop("expected_sha256")
    receipt = _mint(document)
    outcome = ingest_result(
        bundle,
        _result(item, [claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
        source_verifications=[receipt],
    )
    assert outcome.verified_fact_ids == []
    assert outcome.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert "script" in outcome.quarantined[0]["reason"]
    verified = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.verification_status == FactRecordVerification_status.VERIFIED
        and row.statement == PASSAGE
    ]
    assert verified == []


def test_recorded_normalized_agreement_promotes_without_the_lead_file(tmp_path):
    lead = _html(f"{PASSAGE} count 7", "token-aaa")
    fetched = _html(f"{PASSAGE} count 7", "token-bbb")
    expected = hashlib.sha256(lead).hexdigest()
    receipt = _mint(fetched)
    bundle, routed = _routed()
    item = routed.selected[1]
    claim = _claim(f"{PASSAGE} count 7", expected)
    preview = ingest_result(
        bundle,
        _result(item, [claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
        source_verifications=[receipt],
        evidence_lead_bytes={expected: lead},
    )
    assert preview.cross_retrieval[0]["agreement"] == "normalized"
    from qad.m6.content_norm import judge_cross_retrieval

    agreement = judge_cross_retrieval(
        fetched,
        expected_raw_sha256=expected,
        quotation=f"{PASSAGE} count 7",
        lead_bytes=lead,
        notes="",
        looked_for_lead=True,
    )
    persist_receipts(tmp_path, [receipt], notes_by_source_id={receipt.source_id: agreement.notes})
    loaded = load_persisted_receipts(tmp_path)
    assert len(loaded) == 1
    assert loaded[0].notes
    assert "normalized_sha256=" in loaded[0].notes
    replay_bundle, replay_routed = _routed()
    replay_item = replay_routed.selected[1]
    outcome = ingest_result(
        replay_bundle,
        _result(replay_item, [claim]),
        _charter(replay_item),
        [],
        issued_ids=[replay_item.gap_id],
        reported_ids=set(),
        source_verifications=loaded,
    )
    assert outcome.verified_fact_ids
    assert outcome.cross_retrieval[0]["agreement"] == "normalized"
    assert outcome.cross_retrieval[0]["evidence_lead_raw_sha256"] == expected
