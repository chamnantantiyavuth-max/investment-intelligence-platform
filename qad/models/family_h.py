"""Family H — Monitoring & Knowledge
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class CrossCaseValidation(ProvenanceMixin, PITMixin, BaseModel):
    """CCV-01: CrossCaseValidation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CCV-01", frozen=True)
    inconsistent_case_ids: Optional[str] = Field(default=None)
    industry_playbook_id: Optional[str] = Field(default=None)
    lesson_id: str
    notes: Optional[str] = Field(default=None)
    pattern_consistent: str
    validating_case_ids: str
    validation_date: str = Field(frozen=True)
    validation_id: str
    validator: str

    # FK: lesson_id -> CL-01.lesson_id
    # FK: validating_case_ids -> CASE-01.case_id

class CandidateLesson(ProvenanceMixin, PITMixin, BaseModel):
    """CL-01: CandidateLesson. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CL-01", frozen=True)
    cross_validation_ids: Optional[str] = Field(default=None)
    industry_playbook_id: Optional[str] = Field(default=None)
    lesson_id: str
    pattern: str
    proposer: str
    review_date: Optional[str] = Field(default=None, frozen=True)
    reviewer: Optional[str] = Field(default=None)
    source_case_ids: str
    validation_status: str

    # FK: source_case_ids -> CASE-01.case_id

class InstitutionalKnowledgeRecord(ProvenanceMixin, PITMixin, BaseModel):
    """IKR-01: InstitutionalKnowledgeRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IKR-01", frozen=True)
    approval_date: str = Field(frozen=True)
    approved_by: str
    contradicting_evidence_ids: Optional[str] = Field(default=None)
    industry_playbook_id: Optional[str] = Field(default=None)
    knowledge_id: str
    knowledge_statement: str
    lesson_id: str
    supporting_evidence_ids: Optional[str] = Field(default=None)

    # FK: lesson_id -> CL-01.lesson_id

class IndustryPlaybookRecord(ProvenanceMixin, PITMixin, BaseModel):
    """IPR-01: IndustryPlaybookRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IPR-01", frozen=True)
    approval_date: str = Field(frozen=True)
    capital_cycle_patterns: Optional[str] = Field(default=None)
    competitive_dynamics: Optional[str] = Field(default=None)
    industry: Optional[str]
    key_metrics: str
    knowledge_ids: str
    playbook_id: str
    supply_chain_structure: Optional[str] = Field(default=None)
    warning_signs: str
    what_to_measure: Optional[str] = Field(default=None)

    # FK: knowledge_ids -> IKR-01.knowledge_id

class MonitoringAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """MASS-01: MonitoringAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MASS-01", frozen=True)
    assessment_date: str = Field(frozen=True)
    assessment_id: str
    assessor: str
    case_id: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    indicator_ids: str
    monitoring_state: str
    narrative: Optional[str] = Field(default=None)
    trigger_events: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: indicator_ids -> MI-01.indicator_id

class MonitoringIndicator(ProvenanceMixin, PITMixin, BaseModel):
    """MI-01: MonitoringIndicator. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MI-01", frozen=True)
    baseline_value: str
    case_id: str
    current_value: str
    frequency: str
    indicator_id: str
    indicator_name: str
    indicator_type: str
    last_observed: Optional[str] = Field(default=None, frozen=True)
    notes: Optional[str] = Field(default=None)
    owner: str
    threshold_alert: Optional[str] = Field(default=None)
    trend: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class MonitoringObservation(ProvenanceMixin, PITMixin, BaseModel):
    """MO-01: MonitoringObservation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MO-01", frozen=True)
    evidence_id: Optional[str] = Field(default=None)
    indicator_id: str
    notes: Optional[str] = Field(default=None)
    observation_date: str = Field(frozen=True)
    observation_id: str
    observed_value: str
    observer: str
    trigger_event: Optional[str] = Field(default=None)

    # FK: indicator_id -> MI-01.indicator_id