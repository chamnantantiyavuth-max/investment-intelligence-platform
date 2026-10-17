"""Offline tests for specialist routing and result ingestion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from qad.ids import deterministic_uuid7
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    FactRecord,
    FactRecordVerification_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.specialists.budget import (
    PER_CHARTER_CEILING,
    Budget,
    BudgetBoundError,
    assert_within_charter_ceiling,
)
from qad.specialists.catalog import (
    EXPECTED_DISPLAY_NAMES,
    EXPECTED_ROLE,
    CatalogError,
    _validate,
    load_catalog,
)
from qad.specialists.contract import RESULT_CONTRACT_ID
from qad.specialists.ingestion import (
    decide_scuttlebutt_state,
    ingest_result,
    scuttlebutt_contract_complete,
)
from qad.specialists.routing import route_case
from qad.specialists.separation import SeparationViolation
from qad.specialists.stages import StageCompletionRejected, find_stage, transition_stage
from research.qad_pilot.unh.case_slice import ANCHOR_TS_MS, build_unh_case


ROOT = Path("research/qad-cases/CASE-2026-001/founder-priority.json")


def _priority() -> dict:
    return json.loads(ROOT.read_text(encoding="utf-8"))


def _routed(priority: dict | None = None):
    bundle = build_unh_case()
    result = route_case(bundle, max_n=3, founder_priority=priority)
    return bundle, result


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


def _result(item, **overrides) -> dict:
    payload = {
        "contract": RESULT_CONTRACT_ID,
        "case_id": "CASE-2026-001",
        "gap_id": item.gap_id,
        "investigator_charter_id": item.investigator_charter_id,
        "specialist_id": item.specialist_id,
        "actor_id": "agent-a",
        "canonical_role": item.canonical_role,
        "desk_research_only": True,
        "disposition": "UNRESOLVED",
        "falsifiable_question": item.falsifiable_question,
        "stop_rule_triggered": None,
        "usage": {"tool_calls": 1, "sources": 1, "minutes": 5},
        "sampling_limitations": "Public documents only.",
        "claims": [],
        "findings": [],
    }
    payload.update(overrides)
    return payload


def _claim(**source_overrides) -> dict:
    source = {
        "url": "https://www.cms.gov/newsroom/fact-sheets/2027-medicare-advantage-part-d-rate-announcement",
        "retrieval_timestamp": "2026-10-17T14:30:16Z",
        "source_date": "2026-04-06",
        "publisher": "CMS",
        "source_tier": "L3",
        "source_type": "GOVERNMENT_DATA",
        "title": "2027 Medicare Advantage Rate Announcement",
        "quotation": "expected net 2.48 percent",
    }
    source.update(source_overrides)
    return {
        "statement": "CMS printed an industry rate bridge with expected net 2.48 percent.",
        "evidence_type": "FACT",
        "source": source,
    }


def test_catalog_covers_exact_canonical_names():
    catalog = load_catalog()
    names = {row["display_name"] for row in catalog.values()}
    assert names == EXPECTED_DISPLAY_NAMES
    assert len(catalog) == 17
    core = [row for row in catalog.values() if row["kind"] == "core"]
    investigators = [row for row in catalog.values() if row["kind"] == "investigator"]
    assert len(core) == 6
    assert len(investigators) == 11
    for specialist_id, row in catalog.items():
        assert row["canonical_role"] == EXPECTED_ROLE[specialist_id]
        assert row["desk_research_only"] is True
        assert row["overrides_canonical_authority"] is False
    broken = json.loads(Path("qad/specialists/configs/dimensions.json").read_text(encoding="utf-8"))
    broken["specialists"][0]["canonical_role"] = "Chief Underwriter"
    with pytest.raises(CatalogError):
        _validate(broken["specialists"])


def test_dimension_selection_and_founder_override():
    bundle, natural = _routed(None)
    assert [item.specialist_id for item in natural.selected] == [
        "management_capital_allocation",
        "customer_product_investigator",
        "financial_reconstruction_accounting_quality",
    ]
    assert natural.override["applied"] is False
    _bundle, routed = _routed(_priority())
    assert [item.specialist_id for item in routed.selected] == [
        "industry_economics_capital_cycle",
        "customer_product_investigator",
        "management_capital_allocation",
    ]
    assert routed.override["applied"] is True
    assert "industry_economics_capital_cycle" in routed.override["reason"]
    assert routed.override["founder_approved"] is False
    charter = bundle.registry.load("RC-01", natural.charter_id)
    assert charter.charter_state.value == "DRAFT"
    labels = sorted(
        row.hypothesis_label.value
        for row in bundle.registry.list_all("HYP-01")
        if row.case_id == bundle.case_id
    )
    assert labels == ["H1", "H2", "H3", "H4", "H5"]
    assert "Not Founder-approved" in bundle.registry.list_all("HYP-01")[0].statement


def test_charter_gap_binding_and_budget_string():
    bundle, routed = _routed(_priority())
    for item in routed.selected:
        assert item.task_packet["gap_id"] == item.gap_id
        assert item.charter_record["gap_id"] == item.gap_id
        assert item.budget == "max_tool_calls=8;max_sources=6;max_minutes=90"
        assert item.task_packet["result_path"].endswith(f"/results/{item.gap_id}.json")
        if item.investigator_charter_id:
            stored = bundle.registry.load("IC-01", item.investigator_charter_id)
            assert stored.gap_id == item.gap_id
            assert stored.budget == item.budget
        else:
            assert item.charter_record["record_kind"] == "DESK_ASSIGNMENT"
            assert item.canonical_role == "Financial & Management Analyst"
    stage = find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT")
    assert stage.stage_state.value == "IN_PROGRESS"
    charter_stage = find_stage(bundle.registry, bundle.case_id, "CHARTER")
    assert charter_stage.stage_state.value == "IN_PROGRESS"


def test_budget_bounds_enforced():
    with pytest.raises(BudgetBoundError):
        assert_within_charter_ceiling(
            Budget(
                max_tool_calls=PER_CHARTER_CEILING.max_tool_calls + 1,
                max_sources=1,
                max_minutes=1,
            )
        )
    bundle = build_unh_case()
    with pytest.raises(ValueError):
        route_case(
            bundle,
            max_n=3,
            charter_budget=Budget(max_tool_calls=9, max_sources=6, max_minutes=90),
        )
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    ledger: list[tuple[str, str]] = []
    with pytest.raises(BudgetBoundError):
        ingest_result(
            bundle,
            _result(item, usage={"tool_calls": 99, "sources": 1, "minutes": 5}, claims=[_claim()]),
            _charter(item),
            ledger,
            issued_ids=[row.gap_id for row in routed.selected],
            reported_ids=set(),
        )
    assert ledger == []
    assert bundle.registry.list_all("FACT-01") == [] or all(
        row.statement != _claim()["statement"] for row in bundle.registry.list_all("FACT-01")
    )


def _snapshot_for(claim: dict, document: bytes | None = None) -> dict[str, bytes]:
    source = claim["source"]
    if document is None:
        document = (
            "CMS rate announcement fixture.\n"
            + source["quotation"]
            + "\nEnd of independently loaded snapshot.\n"
        ).encode("utf-8")
    return {source["url"]: document}


def _admit_trusted_source(bundle, claim: dict, document: bytes, *, retriever: str = "companyfacts-archive"):
    digest = hashlib.sha256(document).hexdigest()
    source_id = str(
        deterministic_uuid7(f"trusted-src:{claim['source']['url']}:{digest}", ts_ms=ANCHOR_TS_MS)
    )
    bundle.archive.admit_source(
        SourceRecord(
            content_hash=digest,
            retrieval_date=claim["source"]["retrieval_timestamp"],
            source_id=source_id,
            source_tier=SourceRecordSource_tier(claim["source"]["source_tier"]),
            source_type=SourceRecordSource_type(claim["source"].get("source_type") or "OTHER"),
            url_or_identifier=claim["source"]["url"],
            author=claim["source"]["publisher"],
            publication_date=claim["source"]["source_date"],
            retrieval_method="committed_cache",
            retriever=retriever,
            title=claim["source"].get("title") or "trusted archive",
        ),
        document,
    )
    return source_id


def test_provenance_survives_ingest_and_later_update():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    claim = _claim()
    claim["statement"] = claim["source"]["quotation"]
    document = _snapshot_for(claim)[claim["source"]["url"]]
    _admit_trusted_source(bundle, claim, document)
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[claim]),
        _charter(item),
        [],
        issued_ids=[row.gap_id for row in routed.selected],
        reported_ids=set(),
    )
    assert outcome.admitted_evidence_ids
    evidence_id = outcome.admitted_evidence_ids[0]
    source_id = outcome.admitted_source_ids[0]
    evidence = bundle.registry.load("EV-01", evidence_id)
    source = bundle.archive.load("SRC-01", source_id)
    assert evidence.validation_status.value == "RAW"
    assert source.url_or_identifier.startswith("https://www.cms.gov/")
    assert source.retrieval_date == "2026-10-17T14:30:16Z"
    assert source.publication_date == "2026-04-06"
    assert source.author == "CMS"
    facts = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.evidence_id == evidence_id
    ]
    assert len(facts) == 1
    assert facts[0].verification_status == FactRecordVerification_status.VERIFIED
    assert facts[0].source_location == source.url_or_identifier
    raw = bundle.archive.load_raw_blob(source_id)
    assert claim["source"]["quotation"].encode("utf-8") in raw
    assert raw != claim["source"]["quotation"].encode("utf-8")
    assert source.content_hash != hashlib.sha256(
        claim["source"]["quotation"].encode("utf-8")
    ).hexdigest()
    assert source.retrieval_method == "committed_cache"
    assert source.retriever == "companyfacts-archive"
    assert source.retriever != "agent-a"
    updated = evidence.model_copy(
        update={"validation_status": EvidenceRecordValidation_status.DISPUTED}
    )
    bundle.registry.store(updated)
    reloaded = bundle.registry.load("EV-01", evidence_id)
    reloaded_source = bundle.archive.load("SRC-01", reloaded.source_id)
    assert reloaded.validation_status.value == "DISPUTED"
    assert reloaded.source_id == source_id
    assert reloaded.as_of == evidence.as_of
    assert reloaded.content == evidence.content
    assert reloaded_source.url_or_identifier == source.url_or_identifier
    assert reloaded_source.retrieval_date == source.retrieval_date
    assert reloaded_source.publication_date == source.publication_date
    assert reloaded_source.author == source.author
    fact = bundle.registry.load("FACT-01", facts[0].fact_id)
    assert fact.verification_status == FactRecordVerification_status.VERIFIED
    assert fact.source_location == source.url_or_identifier
    gap = bundle.registry.load("EG-01", item.gap_id)
    assert gap.operational_status.value == "UNRESOLVED"
    assert outcome.gap_status["written"] is False
    assert outcome.gap_status["canonical_status"] == "UNRESOLVED"


def test_fabricated_quote_at_a_real_snapshot_is_not_verified():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    genuine = _claim()
    document = _snapshot_for(genuine)[genuine["source"]["url"]]
    fabricated = _claim(
        quotation="expected net 99.99 percent and an invented special dividend",
    )
    fabricated["statement"] = "CMS printed an invented 99.99 percent special dividend."
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[fabricated, genuine]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
        independent_snapshots={genuine["source"]["url"]: document},
    )
    assert outcome.verified_fact_ids == []
    assert len(outcome.quarantined) == 2
    assert all(row["verification_status"] == "UNVERIFIED" for row in outcome.quarantined)
    reasons = [row["reason"] for row in outcome.quarantined]
    assert any("local snapshot is not bound" in reason for reason in reasons)
    assert any("independently loaded" in reason for reason in reasons)
    verified = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.verification_status == FactRecordVerification_status.VERIFIED
        and row.statement in {fabricated["statement"], genuine["statement"]}
    ]
    assert verified == []


def test_forged_local_snapshot_under_a_real_url_cannot_promote_a_fact(tmp_path):
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    sec_url = "https://www.sec.gov/Archives/edgar/data/731766/000073176626000042/unh-20251231.htm"
    cms_url = "https://www.cms.gov/newsroom/fact-sheets/2027-medicare-advantage-part-d-rate-announcement"
    sec_quote = "fabricated special dividend of 99.99 percent"
    cms_quote = "fabricated expected net 88.00 percent"
    snap = tmp_path / "snapshots"
    snap.mkdir()
    (snap / "filing.bin").write_bytes(f"SEC lookalike.\n{sec_quote}\n".encode("utf-8"))
    (snap / "filing.url").write_text(sec_url + "\n", encoding="utf-8")
    (snap / "rates.bin").write_bytes(f"CMS lookalike.\n{cms_quote}\n".encode("utf-8"))
    (snap / "manifest.json").write_text(
        json.dumps({"urls": {cms_url: "rates.bin"}}),
        encoding="utf-8",
    )
    sec_claim = _claim(url=sec_url, quotation=sec_quote, publisher="SEC")
    sec_claim["statement"] = sec_quote
    cms_claim = _claim(url=cms_url, quotation=cms_quote)
    cms_claim["statement"] = cms_quote
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[sec_claim, cms_claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
        snapshot_dir=snap,
    )
    assert outcome.verified_fact_ids == []
    assert outcome.admitted_evidence_ids == []
    assert len(outcome.quarantined) == 2
    assert all(row["verification_status"] == "UNVERIFIED" for row in outcome.quarantined)
    assert all("local snapshot is not bound" in row["reason"] for row in outcome.quarantined)
    promoted = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.verification_status == FactRecordVerification_status.VERIFIED
        and row.statement in {sec_quote, cms_quote}
    ]
    assert promoted == []


def test_statement_numeric_mismatch_is_not_verified():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    passage = "expected net 2.48 percent"
    genuine = _claim(quotation=passage)
    genuine["statement"] = passage
    mismatched = _claim(quotation=passage)
    mismatched["statement"] = "expected net 24.8 percent"
    document = (
        "CMS rate announcement fixture.\n" + passage + "\nEnd of archived source.\n"
    ).encode("utf-8")
    _admit_trusted_source(bundle, genuine, document)
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[mismatched, genuine]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
    )
    assert len(outcome.quarantined) == 1
    assert outcome.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert "numeric values or core proposition" in outcome.quarantined[0]["reason"]
    assert outcome.verified_fact_ids
    kept = bundle.registry.load("FACT-01", outcome.verified_fact_ids[0])
    assert kept.statement == passage
    assert kept.verification_status == FactRecordVerification_status.VERIFIED
    rejected = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.statement == mismatched["statement"]
        and row.verification_status == FactRecordVerification_status.VERIFIED
    ]
    assert rejected == []


def test_replay_does_not_overwrite_an_adverse_fact():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    claim = _claim()
    claim["statement"] = claim["source"]["quotation"]
    document = _snapshot_for(claim)[claim["source"]["url"]]
    url = claim["source"]["url"]
    digest = hashlib.sha256(document).hexdigest()
    passage_digest = hashlib.sha256(claim["source"]["quotation"].encode("utf-8")).hexdigest()
    seed = f"{item.gap_id}:0:{digest}:{passage_digest}"
    fact_id = str(deterministic_uuid7(f"fact:{seed}", ts_ms=ANCHOR_TS_MS))
    evidence_id = str(deterministic_uuid7(f"ev:{seed}", ts_ms=ANCHOR_TS_MS))
    source_id = _admit_trusted_source(bundle, claim, document)
    bundle.registry.admit_evidence(
        EvidenceRecord(
            admitting_role="Evidence Intelligence Lead",
            as_of="2026-04-06",
            content="ADVERSE PRIOR PASSAGE",
            evidence_id=evidence_id,
            evidence_type=EvidenceRecordEvidence_type.FACT,
            extractor="prior-review",
            source_id=source_id,
            source_tier="L3",
            validation_status=EvidenceRecordValidation_status.DISPUTED,
        ),
        EvidenceAdmissionRecord(
            admission_id=str(deterministic_uuid7(f"ear:{seed}", ts_ms=ANCHOR_TS_MS)),
            admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
            admission_timestamp=claim["source"]["retrieval_timestamp"],
            admitting_role="Evidence Intelligence Lead",
            evidence_id=evidence_id,
            source_tier_check="L3",
            validation_method="prior adverse admission",
        ),
    )
    bundle.registry.store(
        FactRecord(
            evidence_id=evidence_id,
            fact_id=fact_id,
            source_location=url,
            statement="Adverse prior reading of the same passage.",
            verification_status=FactRecordVerification_status.DISPUTED,
            as_of="2026-04-06",
            extractor="prior-review",
        )
    )
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
    )
    kept = bundle.registry.load("FACT-01", fact_id)
    assert kept.verification_status == FactRecordVerification_status.DISPUTED
    assert kept.statement == "Adverse prior reading of the same passage."
    evidence = bundle.registry.load("EV-01", evidence_id)
    assert evidence.content == "ADVERSE PRIOR PASSAGE"
    assert evidence.validation_status == EvidenceRecordValidation_status.DISPUTED
    assert outcome.verified_fact_ids == []
    assert outcome.admitted_evidence_ids == []
    assert outcome.preserved
    assert "not overwritten" in outcome.preserved[0]["reason"]


def test_self_supplied_quote_without_snapshot_is_not_verified():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    claim = _claim()
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[claim]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
    )
    assert outcome.admitted_evidence_ids == []
    assert outcome.verified_fact_ids == []
    assert outcome.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert outcome.investigation_disposition == "UNRESOLVED"
    verified = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.statement == claim["statement"]
        and row.verification_status == FactRecordVerification_status.VERIFIED
    ]
    assert verified == []


def test_unsupported_claim_is_quarantined_unverified():
    bundle, routed = _routed(_priority())
    item = routed.selected[1]
    bad = _claim(url="", publisher="")
    outcome = ingest_result(
        bundle,
        _result(item, disposition="ANSWERED", claims=[bad]),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
    )
    assert outcome.admitted_evidence_ids == []
    assert outcome.quarantined[0]["status"] == "QUARANTINED"
    assert outcome.quarantined[0]["verification_status"] == "UNVERIFIED"
    assert outcome.investigation_disposition == "UNRESOLVED"
    verified = [
        row
        for row in bundle.registry.list_all("FACT-01")
        if row.verification_status == FactRecordVerification_status.VERIFIED
        and row.statement == bad["statement"]
    ]
    assert verified == []


def test_unresolved_investigation_stays_unresolved():
    bundle, routed = _routed(_priority())
    item = next(row for row in routed.selected if row.investigator_charter_id)
    outcome = ingest_result(
        bundle,
        _result(item, disposition="UNRESOLVED"),
        _charter(item),
        [],
        issued_ids=[row.gap_id for row in routed.selected],
        reported_ids=set(),
    )
    report = bundle.registry.load("IR-01", outcome.investigation_id)
    assert report.disposition.value == "NOT_ANSWERED"
    assert "specialist_disposition=UNRESOLVED" in report.findings
    assert report.evidence_gap_id == item.gap_id
    gap = bundle.registry.load("EG-01", item.gap_id)
    assert gap.operational_status.value == "UNRESOLVED"
    assert outcome.investigation_disposition == "UNRESOLVED"
    assert outcome.stage_state == "IN_PROGRESS"
    stage = find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT")
    assert stage.stage_state.value != "COMPLETE"


def test_separation_of_duties_violation_rejected():
    bundle, routed = _routed(_priority())
    item = next(row for row in routed.selected if row.canonical_role == "Elastic Investigator")
    ledger: list[tuple[str, str]] = []
    ingest_result(
        bundle,
        _result(item),
        _charter(item),
        ledger,
        issued_ids=[row.gap_id for row in routed.selected],
        reported_ids=set(),
    )
    before = len(bundle.registry.list_all("EV-01"))
    with pytest.raises(SeparationViolation):
        ingest_result(
            bundle,
            _result(item, additional_roles=["Independent Research Auditor"]),
            _charter(item),
            ledger,
            issued_ids=[row.gap_id for row in routed.selected],
            reported_ids={item.gap_id},
        )
    assert len(bundle.registry.list_all("EV-01")) == before


def test_scuttlebutt_complete_only_when_contract_allows():
    assert decide_scuttlebutt_state(
        ["g1"], {"g1"}, desk_research_only=True, contract_complete=True
    ) == "INCOMPLETE"
    assert decide_scuttlebutt_state(
        ["g1", "g2"], {"g1"}, desk_research_only=False, contract_complete=True
    ) == "IN_PROGRESS"
    assert (
        decide_scuttlebutt_state(
            ["g1"],
            {"g1"},
            desk_research_only=False,
            contract_complete=scuttlebutt_contract_complete(
                [
                    {
                        "disposition": "ANSWERED",
                        "stop_rule_triggered": "EVIDENCE_SUFFICIENT",
                        "admitted_evidence_ids": ["ev"],
                    }
                ]
            ),
        )
        == "COMPLETE"
    )
    bundle, routed = _routed(_priority())
    with pytest.raises(StageCompletionRejected):
        transition_stage(
            bundle.registry,
            bundle.case_id,
            "SCUTTLEBUTT",
            "COMPLETE",
            "not allowed",
            [],
            complete_allowed=False,
        )
    item = routed.selected[0]
    outcome = ingest_result(
        bundle,
        _result(item, disposition="UNRESOLVED"),
        _charter(item),
        [],
        issued_ids=[item.gap_id],
        reported_ids=set(),
    )
    assert outcome.stage_state == "INCOMPLETE"
    assert find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT").stage_state.value == "INCOMPLETE"
