"""End-to-end ingest of the three committed UNH specialist result files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from qad.models.family_b import FactRecordVerification_status
from qad.models.family_c import InvestigationReportDisposition, InvestigationReportStop_rule
from qad.specialists.ingestion import attach_role_from_task, ingest_result, load_charter_file
from qad.specialists.routing import reload_case_records
from qad.specialists.separation import INDEPENDENCE_ROLES
from qad.specialists.stages import find_stage, transition_stage
from research.qad_pilot.unh.case_slice import (
    FounderReadyRejected,
    assert_founder_ready_allowed,
    build_unh_case,
    case_view,
)


ROOT = Path("research/qad-cases/CASE-2026-001")
RESULT_IDS = (
    "01a14a2d-3880-7792-80f6-34b43bab1141",
    "01a14a2d-3880-73d1-8542-68158b04b1fc",
    "01a14a2d-3880-7315-8a00-ca275c24ee13",
)
INDEPENDENCE_ACTORS = frozenset(
    {
        "Structural Red Team",
        "Independent Research Auditor",
        "Chief Underwriter",
        "Founder",
    }
)


def _enum(value: object) -> str:
    return getattr(value, "value", value)  # type: ignore[return-value]


def test_committed_unh_results_ingest_offline():
    bundle = build_unh_case()
    charter_dir = ROOT / "charters"
    reload_case_records(bundle, charter_dir)
    transition_stage(
        bundle.registry,
        bundle.case_id,
        "SCUTTLEBUTT",
        "IN_PROGRESS",
        "Replay the ingest open before the committed results.",
        [],
    )
    manifest = json.loads((charter_dir / "route-manifest.json").read_text(encoding="utf-8"))
    issued = [row["gap_id"] for row in manifest["selected"]]
    prior_fact_ids = {row.fact_id for row in bundle.registry.list_all("FACT-01")}
    ledger: list[tuple[str, str]] = []
    reported: set[str] = set()
    outcomes = []
    payloads = []
    for gap_id in RESULT_IDS:
        payload = json.loads((ROOT / "results" / f"{gap_id}.json").read_text(encoding="utf-8"))
        charter = attach_role_from_task(
            load_charter_file(charter_dir / f"{gap_id}.charter.json"),
            charter_dir / f"{gap_id}.task.json",
        )
        outcome = ingest_result(
            bundle,
            payload,
            charter,
            ledger,
            issued_ids=issued,
            reported_ids=reported,
        )
        reported.add(outcome.gap_id)
        outcomes.append(outcome)
        payloads.append(payload)

    assert [item.gap_id for item in outcomes] == list(RESULT_IDS)
    assert [item.investigation_disposition for item in outcomes] == ["PARTIALLY_ANSWERED"] * 3
    assert outcomes[0].ir_disposition == "PARTIALLY_ANSWERED"
    assert outcomes[1].ir_disposition == "PARTIALLY_ANSWERED"
    assert outcomes[2].ir_disposition is None
    assert outcomes[2].investigation_id is None
    assert all(item.quarantined == [] for item in outcomes)

    industry = bundle.registry.load("IR-01", outcomes[0].investigation_id)
    customer = bundle.registry.load("IR-01", outcomes[1].investigation_id)
    assert industry.disposition == InvestigationReportDisposition.PARTIALLY_ANSWERED
    assert customer.disposition == InvestigationReportDisposition.PARTIALLY_ANSWERED
    assert industry.stop_rule_triggered == InvestigationReportStop_rule.EVIDENCE_SUFFICIENT
    assert customer.stop_rule_triggered == InvestigationReportStop_rule.COUNTER_EVIDENCE_FOUND
    assert "specialist_disposition=PARTIALLY_ANSWERED" in industry.findings
    assert "specialist_disposition=PARTIALLY_ANSWERED" in customer.findings

    actors = [item.actor_id for item in outcomes]
    assert len(set(actors)) == 3
    challenge = bundle.registry.load("RTC-01", bundle.challenge_id)
    assert challenge.reviewer == "Structural Red Team"
    for outcome in outcomes:
        assert outcome.actor_id != challenge.reviewer
        assert outcome.actor_id not in INDEPENDENCE_ACTORS
        assert outcome.canonical_role not in INDEPENDENCE_ROLES
    for actor, role in ledger:
        assert actor in actors
        assert role not in INDEPENDENCE_ROLES
        assert role not in INDEPENDENCE_ACTORS

    for payload, outcome in zip(payloads, outcomes):
        assert len(outcome.admitted_evidence_ids) == len(payload["claims"])
        for claim, evidence_id, source_id in zip(
            payload["claims"],
            outcome.admitted_evidence_ids,
            outcome.admitted_source_ids,
        ):
            source = claim["source"]
            stored = bundle.archive.load("SRC-01", source_id)
            raw = bundle.archive.load_raw_blob(source_id)
            assert stored.url_or_identifier == source["url"]
            assert stored.retrieval_date == source["retrieval_timestamp"]
            assert stored.publication_date == source["source_date"]
            assert stored.author == source["publisher"]
            assert raw == source["quotation"].encode("utf-8")
            assert stored.content_hash == hashlib.sha256(raw).hexdigest()
            evidence = bundle.registry.load("EV-01", evidence_id)
            assert evidence.source_id == source_id
            assert evidence.content == source["quotation"]
            facts = [
                row
                for row in bundle.registry.list_all("FACT-01")
                if row.evidence_id == evidence_id and row.fact_id not in prior_fact_ids
            ]
            if claim["evidence_type"] == "FACT":
                assert len(facts) == 1
                assert facts[0].verification_status == FactRecordVerification_status.VERIFIED
            else:
                assert facts == []

    admitted_ids = {
        evidence_id
        for outcome in outcomes
        for evidence_id in outcome.admitted_evidence_ids
    }
    new_verified = [
        fact
        for fact in bundle.registry.list_all("FACT-01")
        if fact.fact_id not in prior_fact_ids
        and fact.verification_status == FactRecordVerification_status.VERIFIED
    ]
    assert new_verified
    for fact in new_verified:
        assert fact.evidence_id in admitted_ids
        evidence = bundle.registry.load("EV-01", fact.evidence_id)
        source = bundle.archive.load("SRC-01", evidence.source_id)
        assert str(source.url_or_identifier).startswith("http")
        assert source.publication_date
        assert source.retrieval_date
        assert source.author
        assert bundle.archive.load_raw_blob(source.source_id)

    for gap_id in RESULT_IDS:
        gap = bundle.registry.load("EG-01", gap_id)
        assert _enum(gap.operational_status) == "UNRESOLVED"

    view = case_view(bundle)
    stages = {row["stage_name"]: row["stage_state"] for row in view["stages"]}
    assert view["case_state"] == "CASE_OPEN"
    assert view["case_state"] != "FOUNDER_READY"
    assert stages["SCUTTLEBUTT"] == "INCOMPLETE"
    assert stages["SCUTTLEBUTT"] != "COMPLETE"
    for name in ("VALUATION", "UNDERWRITING", "AUDIT", "FOUNDER_REVIEW"):
        assert stages[name] == "NOT_STARTED"
    assert _enum(find_stage(bundle.registry, bundle.case_id, "SCUTTLEBUTT").stage_state) == "INCOMPLETE"
    with pytest.raises(FounderReadyRejected):
        assert_founder_ready_allowed(bundle.registry, bundle.case_id)
