"""Family C — Research Case & Execution
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class HypothesisSet(ProvenanceMixin, PITMixin, BaseModel):
    """HS-01: HypothesisSet. Frozen M4A canonical schema."""
    schema_id: str = Field(default="HS-01", frozen=True)
    case_id: str
    charter_id: str
    dominant_hypothesis: Optional[str] = Field(default=None)
    hypothesis_ids: str
    hypothesis_set_id: str
    shift_history: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: hypothesis_ids -> HYP-01.hypothesis_id

class InvestigatorCharter(ProvenanceMixin, PITMixin, BaseModel):
    """IC-01: InvestigatorCharter. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IC-01", frozen=True)
    allowed_source_classes: str
    budget: str
    expected_information_value: Optional[str] = Field(default=None)
    falsifiable_question: str
    gap_id: str
    geography: Optional[str] = Field(default=None)
    independence_check: Optional[str] = Field(default=None)
    investigator_charter_id: str
    investigator_type: str
    output_evidence_ids: Optional[str] = Field(default=None)
    population_represented: Optional[str] = Field(default=None)
    sampling_limitations: Optional[str] = Field(default=None)
    stop_rule: str
    time_window: Optional[str] = Field(default=None)

    # FK: gap_id -> EG-01.gap_id

class InvestigationReport(ProvenanceMixin, PITMixin, BaseModel):
    """IR-01: InvestigationReport. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IR-01", frozen=True)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    disposition: str
    evidence_gap_id: str
    falsifiable_question: str
    findings: str
    investigation_id: str
    investigator: str
    investigator_charter_id: str
    proposed_evidence_ids: Optional[str] = Field(default=None)
    sampling_limitations: Optional[str] = Field(default=None)
    sources: Optional[str] = Field(default=None)
    stop_rule_triggered: Optional[str] = Field(default=None)

    # FK: investigator_charter_id -> IC-01.investigator_charter_id
    # FK: evidence_gap_id -> EG-01.gap_id

class ResearchBudgetRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RB-01: ResearchBudgetRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RB-01", frozen=True)
    allocated_amount: str
    approved_by: str
    budget_exhausted: Optional[str] = Field(default=None)
    budget_id: str
    case_id: str
    cumulative_spend: Optional[str] = Field(default=None)
    policy_version: str
    remaining_budget: Optional[str] = Field(default=None)
    spend_breakdown: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class ResearchCharter(ProvenanceMixin, PITMixin, BaseModel):
    """RC-01: ResearchCharter. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RC-01", frozen=True)
    budget_approved: Optional[str] = Field(default=None)
    budget_controller: Optional[str] = Field(default=None)
    budget_estimate: str
    case_id: str
    charter_id: str
    director: str
    evidence_lead_validation: str
    evidence_scope: str
    hypothesis_ids: str
    key_questions: str
    material_blind_spots: Optional[str] = Field(default=None)
    source_plan: Optional[str] = Field(default=None)
    timeline: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: hypothesis_ids -> HYP-01.hypothesis_id

class ResearchFailureRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RFR-01: ResearchFailureRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RFR-01", frozen=True)
    case_id: str
    error_details: Optional[str] = Field(default=None)
    escalated_to: Optional[str] = Field(default=None)
    failure_id: str
    failure_reason: str
    failure_type: str
    recovery_action: Optional[str] = Field(default=None)
    resolution: str
    retry_count: int
    stage_name: str

    # FK: case_id -> CASE-01.case_id

class ResearchStageRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RSR-01: ResearchStageRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RSR-01", frozen=True)
    case_id: str
    checkpoint_ref: Optional[str] = Field(default=None)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    decisions: Optional[str] = Field(default=None)
    failure_reason: Optional[str] = Field(default=None)
    issues: Optional[str] = Field(default=None)
    output_ids: Optional[str] = Field(default=None)
    responsible_role: str
    retry_count: Optional[int] = Field(default=None)
    stage_id: str
    stage_name: str
    stage_state: str
    started_at: str = Field(frozen=True)

    # FK: case_id -> CASE-01.case_id

class ResearchStopRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RSR-02: ResearchStopRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RSR-02", frozen=True)
    alternative_path: Optional[str] = Field(default=None)
    authorized_by: str
    case_id: str
    evidence_trigger: Optional[str] = Field(default=None)
    resume_condition: Optional[str] = Field(default=None)
    stage_name: str
    stop_id: str
    stop_reason: str

    # FK: case_id -> CASE-01.case_id