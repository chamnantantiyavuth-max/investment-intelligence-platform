"""UNH pilot case registered on the canonical QAD records.

This module does not define a schema, a status vocabulary, or a second
evidence registry. It loads the already committed UNH cache, admits those
bytes through the M5.2 source and evidence gates, and records the pilot's
actual stage states on RSR-01.

Origin: ``CandidateRecord.entry_route = FOUNDER_DIRECTED``. The canonical
entry-route enum has no ``MANUAL_PILOT`` value. That gap is reported; it is
not added to a schema.

Role names are the M3 registry tokens. The draft's byline "QAD Research
Lead / Financial Evidence Analyst" is recorded as Financial & Management
Analyst output under Research Director. The draft's "Independent Skeptic"
section is a Structural Red Team challenge. Those two labels are not
canonical role tokens.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

from qad.ids import deterministic_uuid7
from qad.models.family_a import (
    CandidateRecord,
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecord,
    CaseRecordCase_state,
    SecurityMaster,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
    SignalRecord,
    SignalRecordEntry_route,
    SignalRecordSignal_family,
    SignalRecordSignal_type,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceGap,
    EvidenceGapOperational_status,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    FactRecord,
    FactRecordVerification_status,
    InferenceRecord,
    InferenceRecordConfidence,
)
from qad.models.family_c import (
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_d import (
    QualityAssessment,
    QualityAssessmentQuality_state,
)
from qad.models.family_e import (
    ImpairmentAssessment,
    ImpairmentAssessmentDiagnosis,
)
from qad.models.family_g import (
    RedTeamChallenge,
    RedTeamChallengeOutcome,
)
from qad.models.family_b import SourceRecord, SourceRecordSource_tier, SourceRecordSource_type
from qad.persistence.errors import MissingForeignKey
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryRawSourceArchive,
)
from scripts.qad_pilot.unh_reconcile import (
    ANCHORS_PATH,
    QUOTES_PATH,
    SUBSET_PATH,
    reconcile,
)

CASE_ID = "CASE-2026-001"
CASE_VERSION = "2026-10-17.1"
AS_OF_DATE = "2026-10-17"
OPENED_AT = "2026-10-17T14:04:00Z"
REPORT_SLUG = "unh-qad-pilot-2026-10-17"
REPORT_PATH = "reports/unh-qad-pilot-2026-10-17.md"
ANCHOR_TS_MS = int(datetime(2026, 10, 17, 14, 4, tzinfo=timezone.utc).timestamp() * 1000)

RESEARCH_DIRECTOR = "Research Director"
FINANCIAL_ANALYST = "Financial & Management Analyst"
RED_TEAM = "Structural Red Team"

# SM-2 stages that must already be COMPLETE before a case can be reported
# FOUNDER_READY. FOUNDER_REVIEW is the Founder's own later stage and is not
# a precondition. Persistence does not enforce this CASE-01 transition.
REQUIRED_COMPLETE_BEFORE_FOUNDER_READY: tuple[str, ...] = (
    "CHARTER",
    "SOURCE_FOUNDATION",
    "INITIAL_ANALYSIS",
    "DEEP_RESEARCH",
    "SCUTTLEBUTT",
    "CANONICAL_ADMISSION",
    "QUALITY_ANALYSIS",
    "ANALYTICAL_WORK",
    "IMPAIRMENT",
    "VALUATION",
    "RED_TEAM",
    "AUDIT",
    "UNDERWRITING",
    "PUBLICATION",
)

PARTIAL_STAGES: tuple[str, ...] = (
    "SOURCE_FOUNDATION",
    "INITIAL_ANALYSIS",
    "DEEP_RESEARCH",
    "CANONICAL_ADMISSION",
    "QUALITY_ANALYSIS",
    "ANALYTICAL_WORK",
    "IMPAIRMENT",
    "RED_TEAM",
)

NOT_STARTED_STAGES: dict[str, str] = {
    "CHARTER": RESEARCH_DIRECTOR,
    "SCUTTLEBUTT": RESEARCH_DIRECTOR,
    "VALUATION": "Valuation & Expectations Specialist",
    "AUDIT": "Independent Research Auditor",
    "UNDERWRITING": "Chief Underwriter",
    "PUBLICATION": "Thai Long-Form Research Editor",
    "FOUNDER_REVIEW": "Founder",
    "MONITORING": "Thesis / Knowledge Steward",
    "KNOWLEDGE": "Thesis / Knowledge Steward",
}

COMPANYFACTS_CALCS: tuple[tuple[str, str], ...] = (
    ("operating_margin_percent", "FY2023"),
    ("operating_margin_percent", "FY2024"),
    ("operating_margin_percent", "FY2025"),
    ("medical_care_ratio_percent", "FY2023"),
    ("medical_care_ratio_percent", "FY2025"),
    ("free_cash_flow_millions", "FY2025"),
)
RELEASE_CALCS: tuple[tuple[str, str], ...] = (
    ("operating_margin_percent", "Q3 2026"),
    ("medical_care_ratio_percent", "Q3 2026"),
)

MISSING_CAPABILITIES: tuple[str, ...] = (
    "CASE-01 SM-2 case_state transitions are not enforced by qad.persistence.immutability "
    "(RSR-01 SM-3 is enforced). research.qad_pilot.unh.case_slice.assert_founder_ready_allowed "
    "is an integration guard, not that missing persistence transition.",
    "No DeepResearchRunLedger row. The pilot did not execute an M6 provider run. "
    "The stable ref is CASE-01.case_id plus case_version.",
    "No executable role-compatibility matrix. The matrix is design/qad-pivot/"
    "QAD-M3-ROLE-AND-SERVICE-REGISTRY.md sections 4 and 6. This slice only refuses "
    "Research Director == Structural Red Team on the UNH records.",
    "EvidenceGap (EG-01) exists. There is no Evidence Gap Map service.",
    "InvestigatorCharter (IC-01) exists. No charter was created: scuttlebutt was not opened. "
    "There is no Investigation Charter service.",
    "Research Director is CaseRecord.research_director, not a routing service.",
    "qad.m53.retry_kernel is the stage-execution retry path. It was not used: this slice "
    "is an offline registration of committed evidence, not a research execution.",
)


class FounderReadyRejected(Exception):
    """An incomplete case was asked to become FOUNDER_READY."""

    def __init__(self, reason: str, blocking_stages: list[str]) -> None:
        self.reason = reason
        self.blocking_stages = blocking_stages
        super().__init__(reason)


class VerificationRejected(Exception):
    """A VERIFIED fact was refused because its evidence ref does not resolve."""


@dataclass
class UnhCaseBundle:
    archive: InMemoryRawSourceArchive
    registry: InMemoryEvidenceRegistry
    case_id: str
    case_version: str
    as_of_date: str
    report_slug: str
    source_ids: dict[str, str]
    stage_ids: dict[str, str]
    challenge_id: str
    evidence_ids: dict[str, str] = field(default_factory=dict)
    ingest_replay: dict = field(default_factory=dict)


def _uid(seed: str) -> str:
    return str(deterministic_uuid7(seed, ts_ms=ANCHOR_TS_MS))


def _enum(value: object) -> str:
    return str(getattr(value, "value", value))


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _admit_file(
    archive: InMemoryRawSourceArchive,
    *,
    seed: str,
    path,
    tier: SourceRecordSource_tier,
    source_type: SourceRecordSource_type,
    url: str,
    title: str,
) -> str:
    raw = path.read_bytes()
    source_id = _uid(seed)
    archive.admit_source(
        SourceRecord(
            source_id=source_id,
            source_tier=tier,
            source_type=source_type,
            url_or_identifier=url,
            content_hash=_sha256(raw),
            retrieval_date=AS_OF_DATE,
            title=title,
            file_size=str(len(raw)),
            retrieval_method="committed_cache",
            retriever=FINANCIAL_ANALYST,
        ),
        raw,
    )
    return source_id


def _admit_evidence(
    registry: InMemoryEvidenceRegistry,
    *,
    seed: str,
    source_id: str,
    evidence_type: EvidenceRecordEvidence_type,
    validation_status: EvidenceRecordValidation_status,
    content: str,
    source_tier: str,
    validation_method: str,
) -> str:
    evidence_id = _uid(f"ev:{seed}")
    evidence = EvidenceRecord(
        evidence_id=evidence_id,
        source_id=source_id,
        evidence_type=evidence_type,
        validation_status=validation_status,
        content=content,
        admitting_role=FINANCIAL_ANALYST,
        as_of=AS_OF_DATE,
        extractor=FINANCIAL_ANALYST,
        source_tier=source_tier,
        context=(
            "canonical_role=Financial & Management Analyst; "
            "pilot_byline=QAD Research Lead / Financial Evidence Analyst; "
            "alias_gap=Research Lead and Research Producer are not canonical role tokens"
        ),
        extraction_method="scripts/qad_pilot/unh_reconcile.py",
        validation_method=validation_method,
    )
    admission = EvidenceAdmissionRecord(
        admission_id=_uid(f"ear:{seed}"),
        evidence_id=evidence_id,
        admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
        admission_timestamp=OPENED_AT,
        admitting_role=FINANCIAL_ANALYST,
        source_tier_check=source_tier,
        validation_method=validation_method,
    )
    registry.admit_evidence(evidence, admission)
    return evidence_id


def record_verified_fact(
    registry: InMemoryEvidenceRegistry,
    archive: InMemoryRawSourceArchive,
    fact: FactRecord,
) -> None:
    """Store a fact. VERIFIED is refused unless the evidence and source resolve."""
    if fact.verification_status == FactRecordVerification_status.VERIFIED:
        if not registry.contains("EV-01", fact.evidence_id):
            raise VerificationRejected(
                f"{fact.fact_id}: missing evidence ref {fact.evidence_id}; not VERIFIED"
            )
        evidence = registry.load("EV-01", fact.evidence_id)
        if not archive.contains("SRC-01", evidence.source_id):
            raise VerificationRejected(
                f"{fact.fact_id}: invalid source ref {evidence.source_id}; not VERIFIED"
            )
    registry.store(fact)


def assert_founder_ready_allowed(registry: InMemoryEvidenceRegistry, case_id: str) -> None:
    """Reject FOUNDER_READY while any precondition stage is not COMPLETE.

    ``qad.persistence.immutability`` enforces RSR-01 / SM-3 only. It does not
    enforce CASE-01 / SM-2. This guard is the slice's rejection path.
    """
    stages = [
        row for row in registry.list_all("RSR-01")
        if row.case_id == case_id
    ]
    by_name = {_enum(row.stage_name): row for row in stages}
    blocking: list[str] = []
    for name in REQUIRED_COMPLETE_BEFORE_FOUNDER_READY:
        row = by_name.get(name)
        state = _enum(row.stage_state) if row is not None else "ABSENT"
        if state != ResearchStageRecordStage_state.COMPLETE.value:
            blocking.append(f"{name}={state}")
    if blocking:
        raise FounderReadyRejected(
            "FOUNDER_READY rejected: precondition stages are not COMPLETE",
            blocking,
        )


def request_case_transition(
    bundle: UnhCaseBundle,
    *,
    case_state: str | None = None,
    publication_state: str | None = None,
) -> None:
    """Attempt a state write. Incomplete UNH stages cannot become FOUNDER_READY.

    The function does not write ``case_state``. Founder decision records are
    not created here.
    """
    requested = case_state or publication_state or ""
    if requested in {
        "FOUNDER_ENDORSED",
        "FOUNDER_DISAGREES",
        "FOUNDER_REJECTS",
        "FOUNDER_DECIDED",
    }:
        raise FounderReadyRejected(
            "Founder approval is a separate FDR-01 decision and is absent",
            ["FOUNDER_REVIEW=NOT_STARTED", "FDR-01=ABSENT"],
        )
    if requested == "FOUNDER_READY" or requested == CaseRecordCase_state.FOUNDER_READY.value:
        assert_founder_ready_allowed(bundle.registry, bundle.case_id)
        raise FounderReadyRejected(
            "CASE-01 SM-2 writer is not implemented; FOUNDER_READY was not stored",
            [],
        )
    raise FounderReadyRejected(
        f"state write {requested!r} is not applied; CASE-01 SM-2 is not enforced by persistence",
        [],
    )


def annotate_stage(
    registry: InMemoryEvidenceRegistry,
    stage_id: str,
    issue: str,
) -> ResearchStageRecord:
    """Append an issue on an IN_PROGRESS stage. Identity and provenance stay."""
    current = registry.load("RSR-01", stage_id)
    if _enum(current.stage_state) != ResearchStageRecordStage_state.IN_PROGRESS.value:
        raise FounderReadyRejected(
            f"{current.stage_name} is {_enum(current.stage_state)}; annotation requires IN_PROGRESS",
            [f"{_enum(current.stage_name)}={_enum(current.stage_state)}"],
        )
    updated = current.model_copy(update={"issues": [*(current.issues or []), issue]})
    registry.store(updated)
    loaded = registry.load("RSR-01", stage_id)
    if (
        loaded.stage_id != current.stage_id
        or loaded.case_id != current.case_id
        or loaded.responsible_role != current.responsible_role
        or loaded.started_at != current.started_at
        or loaded.checkpoint_ref != current.checkpoint_ref
        or _enum(loaded.stage_name) != _enum(current.stage_name)
    ):
        raise RuntimeError("stage identity or provenance changed on update")
    return loaded


def finalize_partial_stage(registry: InMemoryEvidenceRegistry, stage_id: str) -> ResearchStageRecord:
    """Move one IN_PROGRESS stage to INCOMPLETE. SM-3 allows that edge."""
    current = registry.load("RSR-01", stage_id)
    updated = current.model_copy(
        update={"stage_state": ResearchStageRecordStage_state.INCOMPLETE}
    )
    registry.store(updated)
    loaded = registry.load("RSR-01", stage_id)
    if loaded.stage_id != current.stage_id or loaded.responsible_role != current.responsible_role:
        raise RuntimeError("stage identity changed while closing partial work")
    if loaded.started_at != current.started_at or loaded.checkpoint_ref != current.checkpoint_ref:
        raise RuntimeError("stage provenance changed while closing partial work")
    return loaded


def _open_stage(
    registry: InMemoryEvidenceRegistry,
    *,
    case_id: str,
    name: str,
    role: str,
    state: ResearchStageRecordStage_state,
    issues: list[str],
    output_ids: list[str] | None = None,
) -> str:
    stage_id = _uid(f"stage:{name}")
    registry.store(
        ResearchStageRecord(
            case_id=case_id,
            responsible_role=role,
            stage_id=stage_id,
            stage_name=ResearchStageRecordStage_name(name),
            stage_state=state,
            started_at=OPENED_AT,
            checkpoint_ref=f"case_version:{CASE_VERSION}",
            issues=issues,
            output_ids=output_ids or [],
        )
    )
    return stage_id


def _calc_map(result: dict) -> dict[tuple[str, str], dict]:
    return {(row["name"], row["period"]): row for row in result["calculations"]}


def build_unh_case(*, finalize_partial: bool = True) -> UnhCaseBundle:
    """Register the committed UNH pilot. Rebuilds are deterministic."""
    result = reconcile()
    if result["mismatches"]:
        raise RuntimeError(f"UNH reconcile mismatches: {result['mismatches']}")
    if result["ticker"] != "UNH":
        raise RuntimeError(f"unexpected ticker {result['ticker']}")

    archive = InMemoryRawSourceArchive()
    registry = InMemoryEvidenceRegistry(source_archive=archive)
    source_ids = {
        "companyfacts": _admit_file(
            archive,
            seed="src:companyfacts",
            path=SUBSET_PATH,
            tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url=result["companyfacts_url"],
            title="SEC companyfacts subset committed for the UNH pilot. Not the full filing archive.",
        ),
        "anchors": _admit_file(
            archive,
            seed="src:anchors",
            path=ANCHORS_PATH,
            tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.OTHER,
            url="research/qad_pilot/unh/filing_anchors.json",
            title=(
                "Filing-text anchors transcribed from named SEC documents. "
                "Not the filing HTML. Q3 2026 figures are from the earnings release transcription."
            ),
        ),
        "quotes": _admit_file(
            archive,
            seed="src:quotes",
            path=QUOTES_PATH,
            tier=SourceRecordSource_tier.L7,
            source_type=SourceRecordSource_type.OTHER,
            url=result["market_quote"]["source_url"],
            title="Weekly market closes from the committed Yahoo chart payload. Not an SEC filing.",
        ),
    }

    entity_id = "ENT-UNH-0000731766"
    signal_id = _uid("signal:unh-margin")
    candidate_id = "CR-2026-001"
    registry.store(
        SecurityMaster(
            entity_id=entity_id,
            cik=str(result["cik"]),
            exchange="NYSE",
            name=str(result["issuer"]),
            primary_ticker="UNH",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
            as_of_date=AS_OF_DATE,
            source=result["companyfacts_url"],
            retrieval_timestamp=OPENED_AT,
        )
    )
    registry.store(
        SignalRecord(
            signal_id=signal_id,
            entity_id=entity_id,
            signal_type=SignalRecordSignal_type.FOUNDER_DIRECTED,
            signal_family=SignalRecordSignal_family.MARGIN_ANOMALY,
            entry_route=SignalRecordEntry_route.FOUNDER_DIRECTED,
            detection_timestamp=OPENED_AT,
            as_of_date=AS_OF_DATE,
            detector="Founder",
            signal_description=(
                "Founder-directed pilot on the 2025 operating-margin break. "
                "MANUAL_PILOT is not a canonical signal_type."
            ),
            signal_evidence=REPORT_PATH,
        )
    )
    registry.store(
        CandidateRecord(
            candidate_id=candidate_id,
            entity_id=entity_id,
            entry_route=CandidateRecordEntry_route.FOUNDER_DIRECTED,
            entry_timestamp=OPENED_AT,
            evidence_freshness=AS_OF_DATE,
            selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
            signal_ids=[signal_id],
            selector="Founder",
            dislocation_flag=True,
        )
    )
    registry.store(
        CaseRecord(
            case_id=CASE_ID,
            entity_id=entity_id,
            candidate_id=candidate_id,
            case_state=CaseRecordCase_state.CASE_OPEN,
            as_of_date=AS_OF_DATE,
            opened_at=OPENED_AT,
            research_director=RESEARCH_DIRECTOR,
            case_version=CASE_VERSION,
            opening_note=(
                "Founder-directed manual pilot. entry_route=FOUNDER_DIRECTED. "
                "MANUAL_PILOT is not a canonical enum. selection_state=AUTO_RESEARCH_NOW "
                "opens research; it is not autonomous discovery recall. "
                f"Draft remains {REPORT_SLUG} status=draft. No FDR-01."
            ),
        )
    )

    calcs = _calc_map(result)
    evidence_ids: dict[str, str] = {}
    fact_ids: dict[str, str] = {}

    def add_fact(seed: str, source_key: str, tier: str, content: str, validation: str) -> str:
        evidence_id = _admit_evidence(
            registry,
            seed=seed,
            source_id=source_ids[source_key],
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=(
                EvidenceRecordValidation_status.VALIDATED
                if validation == "VALIDATED"
                else EvidenceRecordValidation_status.RAW
            ),
            content=content,
            source_tier=tier,
            validation_method=(
                "reconcile() mismatches empty; value read from the admitted file"
                if validation == "VALIDATED"
                else "value read from the admitted anchors transcription; original 8-K HTML is not in the archive"
            ),
        )
        fact_id = _uid(f"fact:{seed}")
        record_verified_fact(
            registry,
            archive,
            FactRecord(
                fact_id=fact_id,
                evidence_id=evidence_id,
                statement=content,
                source_location=source_key,
                verification_status=FactRecordVerification_status.VERIFIED,
                as_of=AS_OF_DATE,
                extractor=FINANCIAL_ANALYST,
                unit="USD millions unless the statement says otherwise",
            ),
        )
        evidence_ids[seed] = evidence_id
        fact_ids[seed] = fact_id
        return evidence_id

    input_evidence: dict[tuple[str, str, str], str] = {}
    for (name, period), source_key, tier, validation in (
        *((item, "companyfacts", "L1", "VALIDATED") for item in COMPANYFACTS_CALCS),
        *((item, "anchors", "L1", "RAW") for item in RELEASE_CALCS),
    ):
        row = calcs[(name, period)]
        if row["label"] != "INFERRED":
            raise RuntimeError(f"{name} {period} label {row['label']} is not INFERRED")
        linked: list[str] = []
        for input_name, input_value in row["inputs_millions"].items():
            key = (source_key, period, input_name)
            if key not in input_evidence:
                input_evidence[key] = add_fact(
                    f"{source_key}:{period}:{input_name}",
                    source_key,
                    tier,
                    (
                        f"{input_name} {period} = {input_value}. "
                        f"Read from the admitted {source_key} file by reconcile(). "
                        "VERIFIED against that file only."
                    ),
                    validation,
                )
            linked.append(input_evidence[key])
        inference_seed = f"inf:{name}:{period}"
        inference_evidence = _admit_evidence(
            registry,
            seed=inference_seed,
            source_id=source_ids[source_key],
            evidence_type=EvidenceRecordEvidence_type.INFERENCE,
            validation_status=EvidenceRecordValidation_status.VALIDATED,
            content=(
                f"{name} {period} = {row['value']}. Formula: {row['formula']}. "
                "Label INFERRED. This is not a VERIFIED fact and not an impairment verdict."
            ),
            source_tier=tier,
            validation_method="scripts/qad_pilot/unh_reconcile.py reconcile()",
        )
        registry.store(
            InferenceRecord(
                inference_id=_uid(inference_seed),
                conclusion=(
                    f"{name} {period} = {row['value']} by {row['formula']}. "
                    "Arithmetic from admitted inputs. Not a temporary-versus-structural conclusion."
                ),
                confidence=InferenceRecordConfidence.MEDIUM,
                evidence_ids=linked,
                inference_chain=row["formula"],
                inferrer=FINANCIAL_ANALYST,
                as_of=AS_OF_DATE,
                inference_method="scripts/qad_pilot/unh_reconcile.py",
                alternative_conclusions=["The ratio is not an impairment diagnosis."],
            )
        )
        evidence_ids[inference_seed] = inference_evidence

    anchors = json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))
    figures = anchors["earnings_release_q3_2026_not_in_companyfacts"]["figures_millions"]
    for key in (
        "unitedhealthcare_revenues_q3_2026",
        "unitedhealthcare_earnings_from_operations_q3_2026",
        "optum_revenues_q3_2026",
        "optum_earnings_from_operations_q3_2026",
    ):
        add_fact(
            f"anchors:{key}",
            "anchors",
            "L1",
            (
                f"{key} = {figures[key]}. Q3 2026 earnings-release transcription in filing_anchors. "
                "Absent from the companyfacts subset. VERIFIED against the anchors file only. "
                "The 8-K HTML bytes are not in the archive."
            ),
            "RAW",
        )

    quote = result["market_quote"]
    price_evidence = []
    for label, value in (
        ("peak_close", quote["peak_close"]),
        ("trough_close", quote["trough_close"]),
        ("latest_close", quote["latest_close"]),
    ):
        price_evidence.append(
            add_fact(
                f"quotes:{label}",
                "quotes",
                "L7",
                (
                    f"{label} = {value} USD. Weekly close in the committed chart payload. "
                    "MARKET_QUOTE. Not an SEC filing and not an official auction print."
                ),
                "VALIDATED",
            )
        )
    market_seed = "inf:market_drawdown"
    evidence_ids[market_seed] = _admit_evidence(
        registry,
        seed=market_seed,
        source_id=source_ids["quotes"],
        evidence_type=EvidenceRecordEvidence_type.INFERENCE,
        validation_status=EvidenceRecordValidation_status.VALIDATED,
        content=(
            f"peak-to-trough {quote['drawdown_peak_to_trough_percent']} percent; "
            f"peak-to-latest {quote['change_peak_to_latest_percent']} percent. "
            "INFERRED from the three admitted weekly closes. Not evidence that the impairment is temporary."
        ),
        source_tier="L7",
        validation_method="scripts/qad_pilot/unh_reconcile.py market_quote",
    )
    registry.store(
        InferenceRecord(
            inference_id=_uid(market_seed),
            conclusion=(
                f"Weekly-close drawdown peak to trough {quote['drawdown_peak_to_trough_percent']} percent; "
                f"peak to latest {quote['change_peak_to_latest_percent']} percent."
            ),
            confidence=InferenceRecordConfidence.MEDIUM,
            evidence_ids=price_evidence,
            inference_chain="(later / peak - 1) * 100, half-up to 0.1",
            inferrer=FINANCIAL_ANALYST,
            as_of=AS_OF_DATE,
            inference_method="scripts/qad_pilot/unh_reconcile.py",
            alternative_conclusions=["The price path does not decide temporary versus structural damage."],
        )
    )

    gap_specs = (
        (
            "q3-10q-absent",
            "CRITICAL",
            "RESOLVABLE_WITH_EXISTING_SOURCES",
            "Does a filed Q3 2026 Form 10-Q report the same revenue and earnings from operations as the 13 Oct 2026 earnings-release transcription?",
            "The companyfacts subset retrieved 2026-10-17 has no 2026-09-30 fact.",
        ),
        (
            "reserve-bridge",
            "HIGH",
            "CURRENTLY_UNRESOLVABLE",
            "What is Q3 2026 operating margin after removing the reserve development the company described, using a bridge the company itself prints?",
            "The release transcription does not provide that bridge. The skeptic's own subtraction is not admitted as a fact.",
        ),
        (
            "outlook-path-2025",
            "HIGH",
            "RESOLVABLE_WITH_EXISTING_SOURCES",
            "Did UnitedHealth publish a numeric 2025 outlook between the May 2025 withdrawal and year-end, and was that outlook missed?",
            "The committed cache does not contain those interim outlook exhibits. Status in the draft: UNKNOWN.",
        ),
        (
            "skeptic-cache-gap",
            "HIGH",
            "RESOLVABLE_WITH_EXISTING_SOURCES",
            "Do the Independent Skeptic numerical challenges that are absent from research/qad_pilot/unh/ appear in an admitted source byte?",
            "Those challenges stay UNVERIFIED. They are visible on RTC-01 and are not FactRecord VERIFIED.",
        ),
        (
            "scuttlebutt-unopened",
            "HIGH",
            "RESOLVABLE_WITH_SCUTTLEBUTT",
            "Can a chartered investigator, with one falsifiable question and an allowed source class, test whether Medicare Advantage membership shrinkage is the mechanism of the margin change?",
            "No IC-01 investigation charter exists.",
        ),
    )
    gap_ids = []
    for seed, importance, resolvability, question, falsifiable in gap_specs:
        gap_id = _uid(f"gap:{seed}")
        registry.store(
            EvidenceGap(
                gap_id=gap_id,
                case_id=CASE_ID,
                created_by=RESEARCH_DIRECTOR,
                importance=importance,
                operational_status=EvidenceGapOperational_status.UNRESOLVED,
                question=question,
                resolvability_class=resolvability,
                created_at=OPENED_AT,
                falsifiable_question=falsifiable,
            )
        )
        gap_ids.append(gap_id)

    quality_evidence = [
        evidence_ids["companyfacts:FY2025:revenues"],
        evidence_ids["companyfacts:FY2025:earnings_from_operations"],
        evidence_ids["anchors:optum_earnings_from_operations_q3_2026"],
        evidence_ids["anchors:unitedhealthcare_earnings_from_operations_q3_2026"],
    ]
    assessment_id = _uid("qa:unh")
    registry.store(
        QualityAssessment(
            assessment_id=assessment_id,
            assessor=FINANCIAL_ANALYST,
            case_id=CASE_ID,
            evidence_ids=quality_evidence,
            false_quality_test_completed="false",
            quality_state=QualityAssessmentQuality_state.UNRESOLVED,
            as_of=AS_OF_DATE,
            assessment_date=AS_OF_DATE,
            notes=(
                "Premium scale and two reported segment earnings were admitted. "
                "Six-type moat classification, moat dimensions, customer unit economics, "
                "and the false-quality test were not done."
            ),
        )
    )
    impairment_id = _uid("ia:unh")
    registry.store(
        ImpairmentAssessment(
            impairment_id=impairment_id,
            case_id=CASE_ID,
            diagnosis=ImpairmentAssessmentDiagnosis.UNRESOLVED,
            evidence_ids=[
                evidence_ids["inf:operating_margin_percent:FY2025"],
                evidence_ids["inf:operating_margin_percent:FY2023"],
                evidence_ids["inf:operating_margin_percent:Q3 2026"],
                evidence_ids["inf:medical_care_ratio_percent:Q3 2026"],
            ],
            flip_evidence=(
                "A filed Q3 2026 10-Q that disagrees with the 13 Oct 2026 release, "
                "or a full-year 2026 medical care ratio near the 2023 base without further membership shrinkage."
            ),
            primary_diagnosis="UNRESOLVED",
            strongest_competing_explanation=(
                "Structural book shrinkage: 2026 margin repair alongside a smaller Medicare Advantage "
                "and Optum Health book, with the medical care ratio still far above 2023. "
                "Recorded by Structural Red Team as an unresolved challenge, not as a verdict."
            ),
            weakest_link="Q3 2026 Form 10-Q is not in the companyfacts snapshot.",
            why_primary_dominates=(
                "No diagnosis dominates. The producer recorded partial 2026 repair and simultaneous "
                "book shrinkage and did not conclude temporary or structural."
            ),
            assessment_date=AS_OF_DATE,
            assessor=FINANCIAL_ANALYST,
        )
    )

    challenge_id = _uid("rtc:unh")
    registry.store(
        RedTeamChallenge(
            challenge_id=challenge_id,
            case_id=CASE_ID,
            reviewer=RED_TEAM,
            outcome=RedTeamChallengeOutcome.UNRESOLVED,
            challenge_date="2026-10-17T14:33:01Z",
            cost_of_being_wrong=(
                "Calling the 2025 margin break temporary, or calling the franchise structurally impaired, "
                "would change whether this is a QAD candidate. This pilot does not make either call."
            ),
            risk_assessment=(
                "The challenge is visible and unresolved. There is no ChallengeResponse, "
                "no underwriting verdict, and no audit."
            ),
            strongest_opposing_case=(
                "The 2025 operating-margin break is structural book change rather than a price delay: "
                "membership and value-based exposure were reduced to buy margin back, and 2026 has not "
                "returned to the 2023 margin base."
            ),
            findings=[
                "canonical_role=Structural Red Team; pilot_section=Independent Skeptic; "
                "alias_gap=Independent Skeptic is not a canonical role token.",
                "UNRESOLVED. The skeptic section says the company's own filings already weight "
                "Medicare Advantage and value-based shrinkage more heavily than a pure delay story. Not adjudicated.",
                "UNVERIFIED. The skeptic section computes a Q3 margin after removing reserve development "
                "and does not call that computation VERIFIED. It is not a FactRecord.",
                "UNVERIFIED. The skeptic section cites a printed first-half medical care ratio, Optum Health "
                "intercompany mix, parent general-purpose cash, regulated-subsidiary funding, a medical-costs-payable "
                "contribution to operating cash flow, and a CMS star effect. Those bytes were not added to the committed cache.",
                "UNRESOLVED. Days-claims-payable stability and a first-half reserve release are different layers "
                "in the skeptic section. The release amount is not in the committed cache.",
                "The producer's admitted margin, cash-flow, and price arithmetic was not rewritten by this challenge.",
            ],
            temporary_challenge="2026 quarterly margin is above the 2025 trough and still below the 2023 full-year margin.",
            quality_challenge="Segment earnings do not establish a moat. Moat classification was not done.",
            recovery_challenge="No recovery model was built. Partial repair is not a completed recovery.",
        )
    )
    if registry.load("CASE-01", CASE_ID).research_director == RED_TEAM:
        raise RuntimeError("Research Director and Structural Red Team collapsed")
    if registry.load("RTC-01", challenge_id).reviewer == FINANCIAL_ANALYST:
        raise RuntimeError("producer and skeptic collapsed onto one role")

    stage_ids = {
        "CASE_OPEN": _open_stage(
            registry,
            case_id=CASE_ID,
            name="CASE_OPEN",
            role=RESEARCH_DIRECTOR,
            state=ResearchStageRecordStage_state.COMPLETE,
            issues=["Case opened from the committed pilot. Research Director assigned."],
            output_ids=[CASE_ID],
        )
    }
    partial_notes = {
        "SOURCE_FOUNDATION": "Committed cache is a companyfacts subset, anchor transcription, and three weekly closes. Not a 7-10 year filing archive.",
        "INITIAL_ANALYSIS": "Bounded evidence gaps were recorded. There is no full dimension-by-dimension gap map.",
        "DEEP_RESEARCH": "No further primary documents were retrieved for this registration.",
        "CANONICAL_ADMISSION": "Only the committed-cache facts and reconcile() ratios were admitted.",
        "QUALITY_ANALYSIS": "quality_state=UNRESOLVED. Moat classification was not done.",
        "ANALYTICAL_WORK": "Selected margins, one medical care ratio pair, FY2025 free cash flow, and the weekly-close drawdown. Not a 7-10 year reconstruction.",
        "IMPAIRMENT": "diagnosis=UNRESOLVED. No recovery model.",
        "RED_TEAM": "RTC-01 outcome=UNRESOLVED. No ChallengeResponse and no adjudication.",
    }
    partial_outputs = {
        "SOURCE_FOUNDATION": list(source_ids.values()),
        "INITIAL_ANALYSIS": gap_ids,
        "CANONICAL_ADMISSION": list(evidence_ids.values()),
        "QUALITY_ANALYSIS": [assessment_id],
        "ANALYTICAL_WORK": [fact_id for fact_id in fact_ids.values()],
        "IMPAIRMENT": [impairment_id],
        "RED_TEAM": [challenge_id],
    }
    partial_roles = {
        "RED_TEAM": RED_TEAM,
    }
    for name in PARTIAL_STAGES:
        stage_ids[name] = _open_stage(
            registry,
            case_id=CASE_ID,
            name=name,
            role=partial_roles.get(name, FINANCIAL_ANALYST),
            state=ResearchStageRecordStage_state.IN_PROGRESS,
            issues=[partial_notes[name]],
            output_ids=partial_outputs.get(name, []),
        )
    for name, role in NOT_STARTED_STAGES.items():
        stage_ids[name] = _open_stage(
            registry,
            case_id=CASE_ID,
            name=name,
            role=role,
            state=ResearchStageRecordStage_state.NOT_STARTED,
            issues=["Not worked in the UNH pilot. started_at is the case anchor required by RSR-01, not a work start."],
        )

    bundle = UnhCaseBundle(
        archive=archive,
        registry=registry,
        case_id=CASE_ID,
        case_version=CASE_VERSION,
        as_of_date=AS_OF_DATE,
        report_slug=REPORT_SLUG,
        source_ids=source_ids,
        stage_ids=stage_ids,
        challenge_id=challenge_id,
        evidence_ids=evidence_ids,
    )
    if finalize_partial:
        for name in PARTIAL_STAGES:
            finalize_partial_stage(registry, stage_ids[name])
    return bundle


def recover_case(case_id: str = CASE_ID, *, replay: bool = True) -> UnhCaseBundle:
    """Rebuild the case from the committed cache and load it by case id.

    ``replay=True`` re-admits committed specialist ingest journals into a new
    in-memory bundle. That is file replay for this pilot case. It is not a
    hosted durable database and it is not, by itself, process-restart proof.
    The CLI passes ``replay=False`` and writes the journal after its own ingest.
    """
    bundle = build_unh_case()
    if case_id != bundle.case_id:
        raise KeyError(case_id)
    loaded = bundle.registry.load("CASE-01", case_id)
    if loaded.case_version != CASE_VERSION or loaded.as_of_date != AS_OF_DATE:
        raise KeyError(case_id)
    if replay:
        from qad.specialists.ingestion import replay_committed_ingests

        replay_committed_ingests(bundle)
    return bundle


def _coverage(bundle: UnhCaseBundle) -> list[dict]:
    demonstrated = {
        "FY2023/FY2024/FY2025 operating margin and FY2025 free cash flow": [
            bundle.evidence_ids["inf:operating_margin_percent:FY2023"],
            bundle.evidence_ids["inf:operating_margin_percent:FY2024"],
            bundle.evidence_ids["inf:operating_margin_percent:FY2025"],
            bundle.evidence_ids["inf:free_cash_flow_millions:FY2025"],
        ],
        "FY2023 and FY2025 medical care ratio": [
            bundle.evidence_ids["inf:medical_care_ratio_percent:FY2023"],
            bundle.evidence_ids["inf:medical_care_ratio_percent:FY2025"],
        ],
        "Q3 2026 release margin and medical care ratio, anchors file only": [
            bundle.evidence_ids["inf:operating_margin_percent:Q3 2026"],
            bundle.evidence_ids["inf:medical_care_ratio_percent:Q3 2026"],
        ],
        "Q3 2026 UnitedHealthcare and Optum operating earnings, anchors file only": [
            bundle.evidence_ids["anchors:unitedhealthcare_earnings_from_operations_q3_2026"],
            bundle.evidence_ids["anchors:optum_earnings_from_operations_q3_2026"],
        ],
        "Weekly-close drawdown, market quote file": [
            bundle.evidence_ids["inf:market_drawdown"],
        ],
        "Quality state recorded as UNRESOLVED": [_uid("qa:unh")],
        "Impairment diagnosis recorded as UNRESOLVED": [_uid("ia:unh")],
        "Structural Red Team challenge visible and UNRESOLVED": [bundle.challenge_id],
    }
    rows = []
    for dimension, refs in demonstrated.items():
        rows.append({
            "contract": "QAD-FULL-RESEARCH-PROTOCOL / QAD-BUSINESS-INDUSTRY-MANAGEMENT",
            "dimension": dimension,
            "status": "DEMONSTRATED",
            "evidence_refs": refs,
        })
    incomplete = (
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 2 Research Charter H1-H5", "No RC-01. Competing hypotheses were not chartered."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 3 seven-to-ten-year primary source foundation", "Cache is a subset plus a transcription."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 4 full evidence gap map", "Five gaps only. Not a map a scuttlebutt investigator can execute across every dimension."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 5 deep research", "No additional sources were collected for this registration."),
        ("QAD-MODERN-SCUTTLEBUTT-PROTOCOL", "Investigation charter and every investigator type", "Replayed specialist charters do not cover every investigator type. SCUTTLEBUTT is not COMPLETE."),
        ("QAD-BUSINESS-INDUSTRY-MANAGEMENT", "Customer economics", "CAC, LTV, churn, and revenue per customer were not measured."),
        ("QAD-BUSINESS-INDUSTRY-MANAGEMENT", "Moat types and moat dimensions", "No MoatAssessment. Six-type classification was not done."),
        ("QAD-BUSINESS-INDUSTRY-MANAGEMENT", "False-quality test and reinvestment runway", "false_quality_test_completed=false."),
        ("QAD-BUSINESS-INDUSTRY-MANAGEMENT", "Industry chain, five forces, industry playbook", "Not done."),
        ("QAD-BUSINESS-INDUSTRY-MANAGEMENT", "Management claim ledger, capital allocation, promise versus outcome", "Not done. CEO-change and outlook exhibits are not in the raw archive."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 11 valuation", "No normalized economics, reverse DCF, or permanent-loss analysis."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 12 red-team adjudication", "Challenge exists. ChallengeResponse does not."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 13 independent audit", "NOT_STARTED."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 14 chief underwriting", "NOT_STARTED. No UV-01."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 15 Thai editorial publication", "The research draft is not a Thai Editorial stage output. PUBLICATION is NOT_STARTED."),
        ("QAD-FULL-RESEARCH-PROTOCOL", "Stage 16 Founder review", "No FDR-01. FOUNDER_REVIEW is NOT_STARTED."),
    )
    for contract, dimension, note in incomplete:
        rows.append({
            "contract": contract,
            "dimension": dimension,
            "status": "INCOMPLETE",
            "evidence_refs": [],
            "note": note,
        })
    return rows


def case_view(bundle: UnhCaseBundle) -> dict:
    """Read model for the authenticated case endpoint. Not a new schema."""
    case = bundle.registry.load("CASE-01", bundle.case_id)
    challenge = bundle.registry.load("RTC-01", bundle.challenge_id)
    stages = []
    for name, stage_id in bundle.stage_ids.items():
        row = bundle.registry.load("RSR-01", stage_id)
        stages.append({
            "stage_name": _enum(row.stage_name),
            "stage_state": _enum(row.stage_state),
            "stage_id": row.stage_id,
            "responsible_role": row.responsible_role,
            "started_at": row.started_at,
            "checkpoint_ref": row.checkpoint_ref,
            "output_ids": list(row.output_ids or []),
        })
    stages.sort(key=lambda item: item["stage_name"])
    founder = [
        row for row in bundle.registry.list_all("FDR-01")
        if row.case_id == bundle.case_id
    ]
    return {
        "data_source": "qad_canonical_case_slice",
        "case_id": case.case_id,
        "case_version": case.case_version,
        "as_of_date": case.as_of_date,
        "case_state": _enum(case.case_state),
        "entry_route": "FOUNDER_DIRECTED",
        "entry_route_gap": "MANUAL_PILOT is not a canonical entry_route. FOUNDER_DIRECTED is the canonical value.",
        "research_director": case.research_director,
        "report_slug": bundle.report_slug,
        "report_path": REPORT_PATH,
        "report_status": "draft",
        "founder_decision_present": bool(founder),
        "stages": stages,
        "skeptic": {
            "challenge_id": challenge.challenge_id,
            "reviewer": challenge.reviewer,
            "outcome": _enum(challenge.outcome),
            "findings": list(challenge.findings),
        },
        "coverage": _coverage(bundle),
        "missing_capabilities": list(MISSING_CAPABILITIES),
        "specialist_recovery": _specialist_recovery(bundle, stages),
        "reused_modules": [
            "qad.persistence.reference.InMemoryRawSourceArchive.admit_source",
            "qad.persistence.reference.InMemoryEvidenceRegistry.admit_evidence",
            "qad.persistence.reference.InMemoryCanonicalRecordStore.store",
            "qad.persistence.reference.InMemoryCanonicalRecordStore.load",
            "qad.persistence.immutability._check_rsr01_sm3_transition",
            "qad.ids.deterministic_uuid7",
            "scripts.qad_pilot.unh_reconcile.reconcile",
        ],
    }


def _specialist_recovery(bundle: UnhCaseBundle, stages: list[dict]) -> dict:
    recovery = dict(bundle.ingest_replay or {})
    if recovery:
        return recovery
    scuttlebutt = next(
        (row["stage_state"] for row in stages if row["stage_name"] == "SCUTTLEBUTT"),
        "",
    )
    return {
        "accepted_evidence": [],
        "quarantined": [],
        "preserved": [],
        "investigations": [],
        "scuttlebutt_stage_state": scuttlebutt,
        "verified_fact_count": 0,
    }


def case_view_for_slug(slug: str) -> dict:
    if slug != REPORT_SLUG:
        raise KeyError(slug)
    return case_view(recover_case(CASE_ID))
