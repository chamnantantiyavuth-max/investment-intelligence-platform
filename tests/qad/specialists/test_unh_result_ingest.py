"""End-to-end ingest of the three committed UNH specialist result files."""

from __future__ import annotations

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
    assert [len(item.quarantined) for item in outcomes] == [len(payload["claims"]) for payload in payloads]
    assert all(item.admitted_evidence_ids == [] for item in outcomes)
    assert all(item.verified_fact_ids == [] for item in outcomes)
    for outcome in outcomes:
        assert all(row["status"] == "QUARANTINED" for row in outcome.quarantined)
        assert all(row["verification_status"] == "UNVERIFIED" for row in outcome.quarantined)
        assert all("independently loaded" in row["reason"] for row in outcome.quarantined)

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

    new_verified = [
        fact
        for fact in bundle.registry.list_all("FACT-01")
        if fact.fact_id not in prior_fact_ids
        and fact.verification_status == FactRecordVerification_status.VERIFIED
    ]
    assert new_verified == []
    for payload in payloads:
        for claim in payload["claims"]:
            matched = [
                fact
                for fact in bundle.registry.list_all("FACT-01")
                if fact.statement == claim["statement"]
                and fact.verification_status == FactRecordVerification_status.VERIFIED
            ]
            assert matched == []

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
