"""Family G — Challenge / Underwriting / Publication
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AuditFindingCheck_name(str, Enum):
    SOURCE_EXISTENCE = "SOURCE_EXISTENCE"
    ORIGINAL_SOURCE_INSPECTION = "ORIGINAL_SOURCE_INSPECTION"
    CITATION_CORRECTNESS = "CITATION_CORRECTNESS"
    PIT_INTEGRITY = "PIT_INTEGRITY"
    CALCULATION_REPRODUCIBILITY = "CALCULATION_REPRODUCIBILITY"
    CONTRADICTION_PRESERVATION = "CONTRADICTION_PRESERVATION"
    MODEL_PROVENANCE = "MODEL_PROVENANCE"
    SELF_REVIEW_SEPARATION = "SELF_REVIEW_SEPARATION"
    PUBLICATION_GATES = "PUBLICATION_GATES"

class AuditFindingPass_fail(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class AuditGateOutcome(str, Enum):
    PASS = "PASS"
    PASS_WITH_FINDINGS = "PASS_WITH_FINDINGS"
    FAIL = "FAIL"

class FounderDecisionReferenceDecision_type(str, Enum):
    ENDORSED = "ENDORSED"
    DISAGREES = "DISAGREES"
    REJECTS = "REJECTS"
    POLICY_OVERRIDE = "POLICY_OVERRIDE"

class PublicationRecordPublication_state(str, Enum):
    RESEARCH_COMPLETE = "RESEARCH_COMPLETE"
    FOUNDER_READY = "FOUNDER_READY"
    FOUNDER_ENDORSED = "FOUNDER_ENDORSED"
    FOUNDER_DISAGREES = "FOUNDER_DISAGREES"
    FOUNDER_REJECTS = "FOUNDER_REJECTS"

class PublicationRecordCategory(str, Enum):
    STOCK_FROM_ANOMALY = "STOCK_FROM_ANOMALY"
    STOCK_FROM_REQUEST = "STOCK_FROM_REQUEST"
    CLOSE_SYSTEM_PRODUCT = "CLOSE_SYSTEM_PRODUCT"
    WEEKLY_INTELLIGENCE = "WEEKLY_INTELLIGENCE"

class RedTeamChallengeOutcome(str, Enum):
    ACCEPTED = "ACCEPTED"
    PARTIALLY_ACCEPTED = "PARTIALLY_ACCEPTED"
    REJECTED_WITH_EVIDENCE = "REJECTED_WITH_EVIDENCE"
    UNRESOLVED = "UNRESOLVED"

class UnderwritingVerdictVerdict(str, Enum):
    QAD_CONFIRMED = "QAD_CONFIRMED"
    QAD_PROBABLE = "QAD_PROBABLE"
    QAD_UNRESOLVED = "QAD_UNRESOLVED"
    NOT_QAD_STRUCTURAL = "NOT_QAD_STRUCTURAL"
    NOT_QAD_QUALITY = "NOT_QAD_QUALITY"
    NOT_QAD_VALUATION = "NOT_QAD_VALUATION"


class AuditFinding(BaseModel):
    """AF-01: AuditFinding. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="AF-01", frozen=True)
    audit_id: str
    check_name: AuditFindingCheck_name
    evidence: str
    finding_id: str
    pass_fail: AuditFindingPass_fail
    required_correction: str
    auditor: Optional[str] = Field(default=None)
    check_timestamp: Optional[str] = Field(default=None, frozen=True)
    resolution_timestamp: Optional[str] = Field(default=None)
    resolved: Optional[bool] = Field(default=None)
    resolver: Optional[str] = Field(default=None)
    severity: Optional[str] = Field(default=None)

    # FK: audit_id -> AG-01.audit_id


class AuditGate(BaseModel):
    """AG-01: AuditGate (AuditReport). Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="AG-01", frozen=True)
    audit_id: str
    auditor: str
    case_id: str
    completed_at: str = Field(frozen=True)
    findings: list[str]
    outcome: AuditGateOutcome
    blocker: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: findings[] -> AF-01.finding_id


class ChallengeResponse(BaseModel):
    """CRESP-01: ChallengeResponse. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CRESP-01", frozen=True)
    adopted_findings: list[str]
    case_id: str
    challenge_id: str
    rejected_findings: list[str]
    response_id: str
    responses: list[str]
    underwriter: str
    notes: Optional[str] = Field(default=None)
    rejection_evidence: Optional[list[str]] = Field(default=None)
    response_date: Optional[str] = Field(default=None, frozen=True)

    # FK: challenge_id -> RTC-01.challenge_id
    # FK: case_id -> CASE-01.case_id


class FounderDecisionReference(BaseModel):
    """FDR-01: FounderDecisionReference. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="FDR-01", frozen=True)
    case_id: str
    decision_date: str = Field(frozen=True)
    decision_type: FounderDecisionReferenceDecision_type
    fd_number: str
    founder_decision_id: str
    founder: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    publication_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: publication_id -> PUB-01.publication_id


class PublicationRecord(BaseModel):
    """PUB-01: PublicationRecord. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="PUB-01", frozen=True)
    case_id: str
    category: PublicationRecordCategory
    editor: str
    publication_id: str
    publication_state: PublicationRecordPublication_state
    published_date: str = Field(frozen=True)
    slug: str
    title: str
    body_english: Optional[str] = Field(default=None)
    body_thai: Optional[str] = Field(default=None)
    companion_slug: Optional[str] = Field(default=None)
    research_complete_date: Optional[str] = Field(default=None)
    research_verdict: Optional[str] = Field(default=None)
    verdict_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: verdict_id -> UV-01.verdict_id


class RedTeamChallenge(BaseModel):
    """RTC-01: RedTeamChallenge. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RTC-01", frozen=True)
    case_id: str
    challenge_id: str
    cost_of_being_wrong: str
    findings: list[str]
    outcome: RedTeamChallengeOutcome
    risk_assessment: str
    strongest_opposing_case: str
    challenge_date: Optional[str] = Field(default=None, frozen=True)
    hidden_risks: Optional[list[str]] = Field(default=None)
    management_challenge: Optional[str] = Field(default=None)
    market_correctness_case: Optional[str] = Field(default=None)
    quality_challenge: Optional[str] = Field(default=None)
    recovery_challenge: Optional[str] = Field(default=None)
    reviewer: Optional[str] = Field(default=None)
    temporary_challenge: Optional[str] = Field(default=None)
    valuation_challenge: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class UnderwritingVerdict(BaseModel):
    """UV-01: UnderwritingVerdict. Frozen M4A canonical schema. Family G. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="UV-01", frozen=True)
    case_id: str
    key_uncertainties: list[str]
    monitoring_indicators: list[str]
    recommendation_to_founder: str
    scenario_weights: dict
    synthesis_narrative: str
    underwriter: str
    verdict: UnderwritingVerdictVerdict
    verdict_id: str
    additional_evidence_ids: Optional[list[str]] = Field(default=None)
    audit_report_id: Optional[str] = Field(default=None)
    dissent_notes: Optional[str] = Field(default=None)
    red_team_challenge_id: Optional[str] = Field(default=None)
    verdict_date: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id
    # FK: red_team_challenge_id -> RTC-01.challenge_id
    # FK: audit_report_id -> AG-01.audit_id