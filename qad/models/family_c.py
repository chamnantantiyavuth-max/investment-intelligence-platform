"""Family C — Research Governance
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class InvestigatorCharterInvestigator_type(str, Enum):
    CUSTOMER = "CUSTOMER"
    COMPETITOR = "COMPETITOR"
    SUPPLIER = "SUPPLIER"
    DISTRIBUTOR = "DISTRIBUTOR"
    EMPLOYEE = "EMPLOYEE"
    DIGITAL = "DIGITAL"
    REGULATORY = "REGULATORY"
    TECHNOLOGY = "TECHNOLOGY"
    SCIENTIFIC = "SCIENTIFIC"
    GEOGRAPHIC = "GEOGRAPHIC"
    INDUSTRY_SPECIALIST = "INDUSTRY_SPECIALIST"

class InvestigatorCharterExpected_information_value(str, Enum):
    PLAUSIBLE_HIGH = "PLAUSIBLE_HIGH"
    PLAUSIBLE_MEDIUM = "PLAUSIBLE_MEDIUM"
    PLAUSIBLE_LOW = "PLAUSIBLE_LOW"

class InvestigationReportDisposition(str, Enum):
    ANSWERED = "ANSWERED"
    NOT_ANSWERED = "NOT_ANSWERED"
    PARTIALLY_ANSWERED = "PARTIALLY_ANSWERED"

class InvestigationReportStop_rule(str, Enum):
    EVIDENCE_SUFFICIENT = "EVIDENCE_SUFFICIENT"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    COUNTER_EVIDENCE_FOUND = "COUNTER_EVIDENCE_FOUND"
    TIME_EXPIRED = "TIME_EXPIRED"

class ResearchBudgetRecordBudget_state(str, Enum):
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    EXHAUSTED = "EXHAUSTED"
    CLOSED = "CLOSED"

class ResearchCharterCharter_state(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    BUDGET_APPROVED = "BUDGET_APPROVED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"

class ResearchFailureRecordFailure_type(str, Enum):
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    RETRY_LIMIT = "RETRY_LIMIT"
    MODEL_FAILURE = "MODEL_FAILURE"
    AUDITOR_BLOCK = "AUDITOR_BLOCK"
    PIT_VIOLATION = "PIT_VIOLATION"
    SELECTION_ERROR = "SELECTION_ERROR"
    EVALUATION_INCOMPLETE = "EVALUATION_INCOMPLETE"

class ResearchFailureRecordResolution(str, Enum):
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    UNRESOLVED = "UNRESOLVED"
    WORKAROUND = "WORKAROUND"

class ResearchStageRecordStage_name(str, Enum):
    CASE_OPEN = "CASE_OPEN"
    CHARTER = "CHARTER"
    SOURCE_FOUNDATION = "SOURCE_FOUNDATION"
    INITIAL_ANALYSIS = "INITIAL_ANALYSIS"
    DEEP_RESEARCH = "DEEP_RESEARCH"
    SCUTTLEBUTT = "SCUTTLEBUTT"
    CANONICAL_ADMISSION = "CANONICAL_ADMISSION"
    QUALITY_ANALYSIS = "QUALITY_ANALYSIS"
    ANALYTICAL_WORK = "ANALYTICAL_WORK"
    IMPAIRMENT = "IMPAIRMENT"
    VALUATION = "VALUATION"
    RED_TEAM = "RED_TEAM"
    AUDIT = "AUDIT"
    UNDERWRITING = "UNDERWRITING"
    PUBLICATION = "PUBLICATION"
    FOUNDER_REVIEW = "FOUNDER_REVIEW"
    MONITORING = "MONITORING"
    KNOWLEDGE = "KNOWLEDGE"

class ResearchStageRecordStage_state(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    INCOMPLETE = "INCOMPLETE"
    SKIPPED = "SKIPPED"

class ResearchStopRecordStop_reason(str, Enum):
    HYPOTHESIS_FALSIFIED = "HYPOTHESIS_FALSIFIED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"
    FOUNDER_DIRECTED = "FOUNDER_DIRECTED"
    AUDITOR_BLOCKED = "AUDITOR_BLOCKED"
    THESIS_KILLER_TRIGGERED = "THESIS_KILLER_TRIGGERED"


class HypothesisSet(BaseModel):
    """HS-01: HypothesisSet. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="HS-01", frozen=True)
    case_id: str
    charter_id: str
    hypothesis_ids: list[str]
    hypothesis_set_id: str
    created_at: Optional[str] = Field(default=None, frozen=True)
    creator: Optional[str] = Field(default=None)
    dominant_hypothesis: Optional[str] = Field(default=None)
    last_shift_at: Optional[str] = Field(default=None, frozen=True)
    shift_history: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: hypothesis_ids[] -> HYP-01.hypothesis_id


class InvestigatorCharter(BaseModel):
    """IC-01: InvestigatorCharter. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IC-01", frozen=True)
    allowed_source_classes: list[str]
    budget: str
    falsifiable_question: str
    gap_id: str
    investigator_charter_id: str
    investigator_type: InvestigatorCharterInvestigator_type
    stop_rule: str
    authorizing_role: Optional[str] = Field(default=None)
    budget_controller: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    created_at: Optional[str] = Field(default=None, frozen=True)
    expected_information_value: Optional[InvestigatorCharterExpected_information_value] = Field(default=None)
    geography: Optional[str] = Field(default=None)
    independence_check: Optional[str] = Field(default=None)
    output_evidence_ids: Optional[list[str]] = Field(default=None)
    population_represented: Optional[str] = Field(default=None)
    sampling_limitations: Optional[str] = Field(default=None)
    time_window: Optional[str] = Field(default=None)

    # FK: gap_id -> EG-01.gap_id


class InvestigationReport(BaseModel):
    """IR-01: InvestigationReport. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IR-01", frozen=True)
    disposition: InvestigationReportDisposition
    evidence_gap_id: str
    falsifiable_question: str
    findings: list[str]
    investigation_id: str
    investigator: str
    investigator_charter_id: str
    charter_version: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    proposed_evidence_ids: Optional[list[str]] = Field(default=None)
    sampling_limitations: Optional[str] = Field(default=None)
    sources: Optional[list[str]] = Field(default=None)
    started_at: Optional[str] = Field(default=None, frozen=True)
    stop_rule_triggered: Optional[InvestigationReportStop_rule] = Field(default=None)

    # FK: investigator_charter_id -> IC-01.investigator_charter_id
    # FK: evidence_gap_id -> EG-01.gap_id


class ResearchBudgetRecord(BaseModel):
    """RB-01: ResearchBudgetRecord. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RB-01", frozen=True)
    allocated_amount: str
    approved_by: str
    budget_id: str
    case_id: str = Field(frozen=True)
    policy_version: str
    approved_at: Optional[str] = Field(default=None, frozen=True)
    budget_exhausted: Optional[str] = Field(default=None)
    cumulative_spend: Optional[str] = Field(default=None)
    last_updated: Optional[str] = Field(default=None, frozen=True)
    remaining_budget: Optional[str] = Field(default=None)
    spend_breakdown: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ResearchCharter(BaseModel):
    """RC-01: ResearchCharter. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RC-01", frozen=True)
    budget_estimate: str
    case_id: str
    charter_id: str
    director: str
    evidence_lead_validation: str
    evidence_scope: str
    hypothesis_ids: list[str]
    key_questions: list[str]
    approved_at: Optional[str] = Field(default=None, frozen=True)
    budget_approved: Optional[str] = Field(default=None)
    budget_controller: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None, frozen=True)
    evidence_lead: Optional[str] = Field(default=None)
    material_blind_spots: Optional[list[str]] = Field(default=None)
    source_plan: Optional[str] = Field(default=None)
    timeline: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: hypothesis_ids[] -> HYP-01.hypothesis_id


class ResearchFailureRecord(BaseModel):
    """RFR-01: ResearchFailureRecord. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RFR-01", frozen=True)
    case_id: str = Field(frozen=True)
    failure_id: str = Field(frozen=True)
    failure_reason: str = Field(frozen=True)
    failure_type: ResearchFailureRecordFailure_type = Field(frozen=True)
    resolution: ResearchFailureRecordResolution = Field(frozen=True)
    retry_count: int = Field(frozen=True)
    stage_name: str = Field(frozen=True)
    error_details: Optional[str] = Field(default=None, frozen=True)
    escalated_to: Optional[str] = Field(default=None, frozen=True)
    escalation_target: Optional[str] = Field(default=None, frozen=True)
    failure_timestamp: Optional[str] = Field(default=None, frozen=True)
    recorder: Optional[str] = Field(default=None, frozen=True)
    recovery_action: Optional[str] = Field(default=None, frozen=True)
    resolution_timestamp: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class ResearchStageRecord(BaseModel):
    """RSR-01: ResearchStageRecord. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RSR-01", frozen=True)
    case_id: str
    responsible_role: str
    stage_id: str
    stage_name: ResearchStageRecordStage_name
    stage_state: ResearchStageRecordStage_state
    started_at: str = Field(frozen=True)
    checkpoint_ref: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    decisions: Optional[list[str]] = Field(default=None)
    failure_reason: Optional[str] = Field(default=None)
    issues: Optional[list[str]] = Field(default=None)
    output_ids: Optional[list[str]] = Field(default=None)
    retry_count: Optional[int] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ResearchStopRecord(BaseModel):
    """RSR-02: ResearchStopRecord. Frozen M4A canonical schema. Family C. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RSR-02", frozen=True)
    authorized_by: str = Field(frozen=True)
    case_id: str = Field(frozen=True)
    stage_name: str = Field(frozen=True)
    stop_id: str = Field(frozen=True)
    stop_reason: ResearchStopRecordStop_reason = Field(frozen=True)
    alternative_path: Optional[str] = Field(default=None, frozen=True)
    evidence_trigger: Optional[str] = Field(default=None, frozen=True)
    resume_condition: Optional[str] = Field(default=None, frozen=True)
    stop_timestamp: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id