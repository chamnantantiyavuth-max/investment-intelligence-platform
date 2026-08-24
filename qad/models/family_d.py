"""Family D — Business / Industry / Management
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CapitalAllocationEventDecision_type(str, Enum):
    ACQUISITION = "ACQUISITION"
    BUYBACK = "BUYBACK"
    DIVIDEND = "DIVIDEND"
    DEBT_ISSUANCE = "DEBT_ISSUANCE"
    EQUITY_ISSUANCE = "EQUITY_ISSUANCE"
    CAPEX = "CAPEX"
    RD = "R&D"
    DIVESTITURE = "DIVESTITURE"
    OTHER = "OTHER"

class MoatAssessmentMoat_type(str, Enum):
    SHARE_OF_MIND = "SHARE_OF_MIND"
    NETWORK_EFFECT = "NETWORK_EFFECT"
    HIGH_SWITCHING_COST = "HIGH_SWITCHING_COST"
    COST_ADVANTAGE = "COST_ADVANTAGE"
    INTANGIBLE_ASSETS = "INTANGIBLE_ASSETS"
    EFFICIENT_SCALE = "EFFICIENT_SCALE"

class MoatAssessmentMoat_width(str, Enum):
    NARROW = "NARROW"
    MODERATE = "MODERATE"
    WIDE = "WIDE"

class MoatAssessmentMoat_depth(str, Enum):
    SHALLOW = "SHALLOW"
    MODERATE = "MODERATE"
    DEEP = "DEEP"

class MoatAssessmentMoat_trend(str, Enum):
    STRENGTHENING = "STRENGTHENING"
    STABLE = "STABLE"
    WEAKENING = "WEAKENING"
    AT_RISK = "AT_RISK"

class MoatAssessmentMoat_durability(str, Enum):
    YEARS = "YEARS"
    DECADE_PLUS = "DECADE_PLUS"
    UNCERTAIN = "UNCERTAIN"

class ManagementDecisionLedgerManagement_quality(str, Enum):
    STRONG = "STRONG"
    ADEQUATE = "ADEQUATE"
    WEAK = "WEAK"
    UNPROVEN = "UNPROVEN"

class ManagementDecisionLedgerCapital_allocation_quality(str, Enum):
    VALUE_CREATING = "VALUE_CREATING"
    NEUTRAL = "NEUTRAL"
    VALUE_DESTROYING = "VALUE_DESTROYING"
    UNCLEAR = "UNCLEAR"

class ManagementOutcomeVariance_type(str, Enum):
    MET = "MET"
    EXCEEDED = "EXCEEDED"
    MISSED = "MISSED"
    UNCLEAR = "UNCLEAR"
    PENDING = "PENDING"

class QualityAssessmentQuality_state(str, Enum):
    VERIFIED = "VERIFIED"
    PROBABLE = "PROBABLE"
    UNRESOLVED = "UNRESOLVED"
    FAILED = "FAILED"


class CapitalAllocationEvent(BaseModel):
    """CAE-01: CapitalAllocationEvent. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CAE-01", frozen=True)
    amount: str
    case_id: str
    decision_date: str = Field(frozen=True)
    decision_type: CapitalAllocationEventDecision_type
    event_id: str
    evidence_ids: list[str]
    outcome: str
    extractor: Optional[str] = Field(default=None)
    outcome_date: Optional[str] = Field(default=None, frozen=True)
    per_share_impact: Optional[str] = Field(default=None)
    rationale: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    source_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class IndustryEconomicsRecord(BaseModel):
    """IE-01: IndustryEconomicsRecord. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IE-01", frozen=True)
    capacity_utilization: str
    case_id: str
    demand_driver: str
    evidence_ids: list[str]
    industry_economics_id: str
    pricing_dynamics: str
    supply_structure: str
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    capital_entry_barriers: Optional[str] = Field(default=None)
    future_capacity_pipeline: Optional[str] = Field(default=None)
    margins_normal: Optional[str] = Field(default=None)
    porter_forces: Optional[dict] = Field(default=None)
    roic_industry: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class MoatAssessment(BaseModel):
    """MA-01: MoatAssessment. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MA-01", frozen=True)
    case_id: str
    evidence_ids: list[str]
    moat_assessment_id: str
    moat_depth: MoatAssessmentMoat_depth
    moat_durability: MoatAssessmentMoat_durability
    moat_trend: MoatAssessmentMoat_trend
    moat_types: list[MoatAssessmentMoat_type]
    moat_width: MoatAssessmentMoat_width
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    false_quality_concerns: Optional[list[str]] = Field(default=None)
    mechanism_evidence: Optional[dict] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ManagementClaim(BaseModel):
    """MC-01: ManagementClaim. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MC-01", frozen=True)
    case_id: str
    claim_date: str = Field(frozen=True)
    claim_id: str
    claimant: str
    source_id: str
    statement: str
    extractor: Optional[str] = Field(default=None)
    outcome: Optional[str] = Field(default=None)
    outcome_date: Optional[str] = Field(default=None, frozen=True)
    source: Optional[str] = Field(default=None)
    variance: Optional[str] = Field(default=None)
    variance_explanation: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: source_id -> SRC-01.source_id


class ManagementDecisionLedger(BaseModel):
    """MDL-01: ManagementDecisionLedger. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MDL-01", frozen=True)
    capital_allocation_quality: ManagementDecisionLedgerCapital_allocation_quality
    case_id: str
    evidence_ids: list[str]
    ledger_id: str
    management_quality: ManagementDecisionLedgerManagement_quality
    promise_ratio: str
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    concerns: Optional[list[str]] = Field(default=None)
    incentive_alignment: Optional[str] = Field(default=None)
    ma_history_summary: Optional[str] = Field(default=None)
    per_share_trend: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ManagementOutcome(BaseModel):
    """MO-02: ManagementOutcome. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MO-02", frozen=True)
    case_id: str = Field(frozen=True)
    management_claim_id: str = Field(frozen=True)
    measured_outcome: str = Field(frozen=True)
    outcome_date: str = Field(frozen=True)
    outcome_id: str = Field(frozen=True)
    variance: ManagementOutcomeVariance_type = Field(frozen=True)
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None, frozen=True)
    evidence_ids: Optional[list[str]] = Field(default=None, frozen=True)
    is_resolved: Optional[bool] = Field(default=None, frozen=True)
    variance_explanation: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id
    # FK: management_claim_id -> MC-01.claim_id


class QualityAssessment(BaseModel):
    """QA-01: QualityAssessment. Frozen M4A canonical schema. Family D. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="QA-01", frozen=True)
    assessment_id: str
    assessor: str
    case_id: str
    evidence_ids: list[str]
    false_quality_test_completed: str
    quality_state: QualityAssessmentQuality_state
    as_of: Optional[str] = Field(default=None, frozen=True)
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    industry_economics_id: Optional[str] = Field(default=None)
    method_version: Optional[str] = Field(default=None)
    moat_assessment_id: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: evidence_ids[] -> EV-01.evidence_id