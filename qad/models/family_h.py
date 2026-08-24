"""Family H — Monitoring & Knowledge
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CrossCaseValidationValidation_result(str, Enum):
    CONFIRMED = "CONFIRMED"
    PARTIALLY_CONFIRMED = "PARTIALLY_CONFIRMED"
    INCONCLUSIVE = "INCONCLUSIVE"
    REJECTED = "REJECTED"

class CandidateLessonValidation_status(str, Enum):
    RESEARCH_FINDING = "RESEARCH_FINDING"
    CANDIDATE_LESSON = "CANDIDATE_LESSON"
    CROSS_CASE_VALIDATED = "CROSS_CASE_VALIDATED"
    INDEPENDENTLY_REVIEWED = "INDEPENDENTLY_REVIEWED"
    APPROVED_KNOWLEDGE = "APPROVED_KNOWLEDGE"

class MonitoringAssessmentMonitoring_state(str, Enum):
    RECOVERY_CONFIRMING = "RECOVERY_CONFIRMING"
    ON_TRACK = "ON_TRACK"
    UNCERTAIN = "UNCERTAIN"
    WEAKENING = "WEAKENING"
    BROKEN = "BROKEN"

class MonitoringIndicatorIndicator_type(str, Enum):
    RECOVERY = "RECOVERY"
    WARNING = "WARNING"
    THESIS_KILLER = "THESIS_KILLER"


class CrossCaseValidation(BaseModel):
    """CCV-01: CrossCaseValidation. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CCV-01", frozen=True)
    lesson_id: str = Field(frozen=True)
    pattern_consistent: str = Field(frozen=True)
    validating_case_ids: list[str] = Field(frozen=True)
    validation_date: str = Field(frozen=True)
    validation_id: str = Field(frozen=True)
    validation_result: CrossCaseValidationValidation_result = Field(frozen=True)
    validator: str = Field(frozen=True)
    inconsistent_case_ids: Optional[list[str]] = Field(default=None, frozen=True)
    industry_playbook_id: Optional[str] = Field(default=None, frozen=True)
    method: Optional[str] = Field(default=None, frozen=True)
    notes: Optional[str] = Field(default=None, frozen=True)

    # FK: lesson_id -> CL-01.lesson_id
    # FK: validating_case_ids[] -> CASE-01.case_id


class CandidateLesson(BaseModel):
    """CL-01: CandidateLesson. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CL-01", frozen=True)
    lesson_id: str = Field(frozen=True)
    pattern: str = Field(frozen=True)
    proposer: str = Field(frozen=True)
    source_case_ids: list[str] = Field(frozen=True)
    validation_status: CandidateLessonValidation_status = Field(frozen=True)
    cross_validation_ids: Optional[list[str]] = Field(default=None, frozen=True)
    industry_playbook_id: Optional[str] = Field(default=None, frozen=True)
    proposed_date: Optional[str] = Field(default=None, frozen=True)
    review_date: Optional[str] = Field(default=None, frozen=True)
    reviewer: Optional[str] = Field(default=None, frozen=True)

    # FK: source_case_ids[] -> CASE-01.case_id


class InstitutionalKnowledgeRecord(BaseModel):
    """IKR-01: InstitutionalKnowledgeRecord. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IKR-01", frozen=True)
    approval_date: str = Field(frozen=True)
    approved_by: str
    knowledge_id: str
    knowledge_statement: str
    lesson_id: str
    contradicting_evidence_ids: Optional[list[str]] = Field(default=None)
    industry_playbook_id: Optional[str] = Field(default=None)
    review_chain: Optional[str] = Field(default=None)
    supporting_evidence_ids: Optional[list[str]] = Field(default=None)

    # FK: lesson_id -> CL-01.lesson_id


class IndustryPlaybookRecord(BaseModel):
    """IPR-01: IndustryPlaybookRecord. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IPR-01", frozen=True)
    approval_date: str = Field(frozen=True)
    industry: str
    key_metrics: list[str]
    knowledge_ids: list[str]
    playbook_id: str
    warning_signs: list[str]
    approver: Optional[str] = Field(default=None)
    capital_cycle_patterns: Optional[str] = Field(default=None)
    competitive_dynamics: Optional[str] = Field(default=None)
    creator: Optional[str] = Field(default=None)
    last_updated: Optional[str] = Field(default=None, frozen=True)
    supply_chain_structure: Optional[str] = Field(default=None)
    what_to_measure: Optional[str] = Field(default=None)

    # FK: knowledge_ids[] -> IKR-01.knowledge_id


class MonitoringAssessment(BaseModel):
    """MASS-01: MonitoringAssessment. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MASS-01", frozen=True)
    assessment_date: str = Field(frozen=True)
    assessment_id: str
    assessor: str
    case_id: str
    indicator_ids: list[str]
    monitoring_state: MonitoringAssessmentMonitoring_state
    evidence_ids: Optional[list[str]] = Field(default=None)
    narrative: Optional[str] = Field(default=None)
    trigger_events: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: indicator_ids[] -> MI-01.indicator_id


class MonitoringIndicator(BaseModel):
    """MI-01: MonitoringIndicator. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MI-01", frozen=True)
    baseline_value: str
    case_id: str
    current_value: str
    frequency: str
    indicator_id: str
    indicator_name: str
    indicator_type: MonitoringIndicatorIndicator_type
    owner: str
    as_of: Optional[str] = Field(default=None, frozen=True)
    definition_source: Optional[str] = Field(default=None)
    last_observed: Optional[str] = Field(default=None, frozen=True)
    notes: Optional[str] = Field(default=None)
    threshold_alert: Optional[str] = Field(default=None)
    trend: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class MonitoringObservation(BaseModel):
    """MO-01: MonitoringObservation. Frozen M4A canonical schema. Family H. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MO-01", frozen=True)
    indicator_id: str
    observation_date: str = Field(frozen=True)
    observation_id: str
    observed_value: str
    observer: str
    evidence_id: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    trigger_event: Optional[str] = Field(default=None)

    # FK: indicator_id -> MI-01.indicator_id