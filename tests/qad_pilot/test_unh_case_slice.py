"""UNH pilot registered on the existing canonical case, evidence, and stage records.

Offline. The committed cache is reused. No provider run and no schema change.
"""
import os
from pathlib import Path

os.environ.setdefault("IIP_AUTH_USER", "founder")
os.environ.setdefault("IIP_AUTH_PASSWORD", "test-password-123")
os.environ.setdefault("IIP_AUTH_SECRET", "y" * 40)

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402
from discovery.quality_asymmetry.fixture_evidence import evidence_from_fixture, load_fixture
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    FactRecord,
    FactRecordVerification_status,
)
from qad.persistence.errors import MissingForeignKey
from research.qad_pilot.unh.case_slice import (
    CASE_ID,
    CASE_VERSION,
    FINANCIAL_ANALYST,
    RED_TEAM,
    REPORT_SLUG,
    RESEARCH_DIRECTOR,
    FounderReadyRejected,
    VerificationRejected,
    annotate_stage,
    build_unh_case,
    case_view,
    finalize_partial_stage,
    record_verified_fact,
    recover_case,
    request_case_transition,
)
from scripts.qad_pilot.unh_reconcile import reconcile

ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app)


def _login() -> None:
    response = client.post(
        "/api/auth/login",
        json={"username": "founder", "password": "test-password-123"},
    )
    assert response.status_code == 200, response.text


def test_wp1_and_unh_reconcile_still_run_offline():
    payload = load_fixture(ROOT / "tests/fixtures/quality_asymmetry/synth_compounder.json")
    evidence = evidence_from_fixture(payload)
    assert evidence["network_used"] is False
    assert evidence["score"] is None
    assert evidence["invented_values"] is False
    assert evidence["recommendation"] is None

    result = reconcile()
    assert result["mismatches"] == []
    assert result["ticker"] == "UNH"


def test_case_is_recoverable_by_stable_case_ref():
    first = recover_case(CASE_ID)
    second = recover_case(CASE_ID)
    assert first.case_id == second.case_id == CASE_ID
    assert first.case_version == second.case_version == CASE_VERSION
    assert first.stage_ids == second.stage_ids
    loaded = second.registry.load("CASE-01", CASE_ID)
    assert loaded.case_version == CASE_VERSION
    assert loaded.as_of_date == "2026-10-17"
    assert loaded.case_state.value == "CASE_OPEN"
    assert loaded.research_director == RESEARCH_DIRECTOR
    with __import__("pytest").raises(KeyError):
        recover_case("CASE-DOES-NOT-EXIST")


def test_draft_report_and_case_are_readable_on_the_authenticated_mobile_route():
    _login()
    article = client.get(f"/api/reports/{REPORT_SLUG}")
    assert article.status_code == 200
    report = article.json()["report"]
    assert report["status"] == "draft"
    assert "## Independent Skeptic" in report["content"]

    case = client.get(f"/api/qad/cases/by-report/{REPORT_SLUG}")
    assert case.status_code == 200
    body = case.json()
    assert body["case_id"] == CASE_ID
    assert body["report_status"] == "draft"
    assert body["founder_decision_present"] is False

    page = (ROOT / "frontend/src/pages/ReportArticlePage.tsx").read_text(encoding="utf-8")
    route = (ROOT / "frontend/src/App.tsx").read_text(encoding="utf-8")
    assert 'path="library/:slug"' in route
    assert 'data-testid="qad-case-strip"' in page
    assert 'data-testid="qad-skeptic-outcome"' in page
    strip = page.split("function CaseStrip", 1)[1].split("function TitleBlock", 1)[0]
    assert "hidden" not in strip
    assert "md:" not in strip


def test_incomplete_stages_cannot_be_reported_founder_ready():
    bundle = recover_case(CASE_ID)
    view = case_view(bundle)
    by_name = {row["stage_name"]: row["stage_state"] for row in view["stages"]}
    for name in (
        "VALUATION",
        "UNDERWRITING",
        "AUDIT",
        "PUBLICATION",
        "FOUNDER_REVIEW",
        "SCUTTLEBUTT",
        "CHARTER",
    ):
        assert by_name[name] == "NOT_STARTED"
    assert by_name["CASE_OPEN"] == "COMPLETE"
    assert by_name["RED_TEAM"] == "INCOMPLETE"
    assert view["case_state"] == "CASE_OPEN"

    try:
        request_case_transition(bundle, case_state="FOUNDER_READY")
    except FounderReadyRejected as exc:
        assert exc.blocking_stages
        assert any(item.startswith("VALUATION=") for item in exc.blocking_stages)
    else:
        raise AssertionError("FOUNDER_READY was accepted")
    assert bundle.registry.load("CASE-01", CASE_ID).case_state.value == "CASE_OPEN"
    assert bundle.registry.list_all("FDR-01") == []

    _login()
    response = client.post(
        f"/api/qad/cases/{CASE_ID}/state",
        json={"case_state": "FOUNDER_READY"},
    )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["rejected"] is True
    assert detail["blocking_stages"]
    again = client.get(f"/api/qad/cases/{CASE_ID}")
    assert again.status_code == 200
    assert again.json()["case_state"] == "CASE_OPEN"


def test_skeptic_findings_remain_visible_and_separate_from_the_producer():
    view = case_view(recover_case(CASE_ID))
    skeptic = view["skeptic"]
    assert skeptic["reviewer"] == RED_TEAM
    assert skeptic["reviewer"] != FINANCIAL_ANALYST
    assert view["research_director"] == RESEARCH_DIRECTOR
    assert skeptic["reviewer"] != view["research_director"]
    assert skeptic["outcome"] == "UNRESOLVED"
    assert any("UNVERIFIED" in item for item in skeptic["findings"])
    assert any("UNRESOLVED" in item for item in skeptic["findings"])
    _login()
    body = client.get(f"/api/qad/cases/{CASE_ID}").json()
    assert body["skeptic"]["findings"] == skeptic["findings"]
    assert body["skeptic"]["outcome"] == "UNRESOLVED"


def test_stage_identity_and_provenance_survive_an_update():
    bundle = build_unh_case(finalize_partial=False)
    stage_id = bundle.stage_ids["SOURCE_FOUNDATION"]
    before = bundle.registry.load("RSR-01", stage_id)
    assert before.stage_state.value == "IN_PROGRESS"
    updated = annotate_stage(bundle.registry, stage_id, "cache remains a subset")
    assert updated.stage_id == before.stage_id
    assert updated.case_id == before.case_id
    assert updated.responsible_role == before.responsible_role == FINANCIAL_ANALYST
    assert updated.started_at == before.started_at
    assert updated.checkpoint_ref == before.checkpoint_ref == f"case_version:{CASE_VERSION}"
    assert updated.stage_name == before.stage_name
    assert "v0001" in bundle.registry.list_versions("RSR-01", stage_id)
    prior = bundle.registry.load_version("RSR-01", stage_id, "v0001")
    assert prior.stage_id == before.stage_id
    assert prior.responsible_role == before.responsible_role
    assert prior.started_at == before.started_at
    assert prior.checkpoint_ref == before.checkpoint_ref
    closed = finalize_partial_stage(bundle.registry, stage_id)
    assert closed.stage_state.value == "INCOMPLETE"
    assert closed.stage_id == before.stage_id
    assert closed.responsible_role == before.responsible_role
    assert closed.started_at == before.started_at
    assert closed.checkpoint_ref == before.checkpoint_ref
    try:
        annotate_stage(bundle.registry, stage_id, "too late")
    except FounderReadyRejected:
        pass
    else:
        raise AssertionError("terminal stage accepted another annotation")


def test_missing_or_invalid_evidence_ref_does_not_become_verified():
    bundle = build_unh_case()
    fact = FactRecord(
        fact_id="01932f6a-7c00-7000-8000-000000000001",
        evidence_id="EV-NOT-ADMITTED",
        statement="A figure with no admitted evidence.",
        source_location="missing",
        verification_status=FactRecordVerification_status.VERIFIED,
    )
    try:
        record_verified_fact(bundle.registry, bundle.archive, fact)
    except VerificationRejected as exc:
        assert "not VERIFIED" in str(exc)
    else:
        raise AssertionError("missing evidence became VERIFIED")
    assert bundle.registry.contains("FACT-01", fact.fact_id) is False

    bogus = EvidenceRecord(
        evidence_id="01932f6a-7c00-7000-8000-000000000002",
        source_id="SRC-NOT-ADMITTED",
        evidence_type=EvidenceRecordEvidence_type.FACT,
        validation_status=EvidenceRecordValidation_status.VALIDATED,
        content="This source was never admitted.",
        admitting_role=FINANCIAL_ANALYST,
        as_of="2026-10-17",
        extractor=FINANCIAL_ANALYST,
        source_tier="L1",
    )
    admission = EvidenceAdmissionRecord(
        admission_id="01932f6a-7c00-7000-8000-000000000003",
        evidence_id=bogus.evidence_id,
        admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
        admission_timestamp="2026-10-17T14:04:00Z",
        admitting_role=FINANCIAL_ANALYST,
        source_tier_check="L1",
        validation_method="none",
    )
    try:
        bundle.registry.admit_evidence(bogus, admission)
    except MissingForeignKey:
        pass
    else:
        raise AssertionError("invalid source was admitted")
    assert bundle.registry.contains("EV-01", bogus.evidence_id) is False


def test_coverage_map_marks_only_admitted_dimensions_demonstrated():
    view = case_view(recover_case(CASE_ID))
    demonstrated = [row for row in view["coverage"] if row["status"] == "DEMONSTRATED"]
    incomplete = [row for row in view["coverage"] if row["status"] == "INCOMPLETE"]
    assert demonstrated
    assert all(row["evidence_refs"] for row in demonstrated)
    assert incomplete
    assert all(row["evidence_refs"] == [] for row in incomplete)
    names = {row["dimension"] for row in incomplete}
    assert any("valuation" in name for name in names)
    assert any("Investigation charter" in name for name in names)
    assert any("Founder review" in name for name in names)
    assert any("Thai editorial" in name for name in names)
    assert any("chief underwriting" in name for name in names)
    facts = bundle_facts(view)
    joined = " ".join(facts)
    assert "85.3" not in joined
    assert "intercompany" not in joined.lower()


def bundle_facts(view: dict) -> list[str]:
    bundle = recover_case(view["case_id"])
    return [row.statement for row in bundle.registry.list_all("FACT-01")]
