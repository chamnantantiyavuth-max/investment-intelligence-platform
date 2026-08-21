"""Family D — Business & Industry Quality
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class CapitalAllocationEvent(ProvenanceMixin, PITMixin, BaseModel):
    """CAE-01: CapitalAllocationEvent. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CAE-01", frozen=True)
    amount: str
    case_id: str
    decision_date: str = Field(frozen=True)
    decision_type: str
    event_id: str
    evidence_ids: Optional[list[str]]
    outcome: str
    per_share_impact: Optional[str] = Field(default=None)
    rationale: Optional[str] = Field(default=None)
    source_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class IndustryEconomicsRecord(ProvenanceMixin, PITMixin, BaseModel):
    """IE-01: IndustryEconomicsRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IE-01", frozen=True)
    capacity_utilization: str
    capital_entry_barriers: Optional[str] = Field(default=None)
    case_id: str
    demand_driver: str
    evidence_ids: Optional[list[str]]
    future_capacity_pipeline: Optional[str] = Field(default=None)
    industry_economics_id: str
    margins_normal: Optional[str] = Field(default=None)
    porter_forces: Optional[dict] = Field(default=None)
    pricing_dynamics: str
    roic_industry: Optional[str] = Field(default=None)
    supply_structure: str

    # FK: case_id -> CASE-01.case_id

class MoatAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """MA-01: MoatAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MA-01", frozen=True)
    case_id: str
    evidence_ids: Optional[list[str]]
    false_quality_concerns: Optional[list[str]] = Field(default=None)
    mechanism_evidence: Optional[dict] = Field(default=None)
    moat_assessment_id: str
    moat_depth: Optional[str]
    moat_durability: Optional[str]
    moat_trend: str
    moat_types: str
    moat_width: str

    # FK: case_id -> CASE-01.case_id

class ManagementClaim(ProvenanceMixin, PITMixin, BaseModel):
    """MC-01: ManagementClaim. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MC-01", frozen=True)
    case_id: str
    claim_date: str = Field(frozen=True)
    claim_id: str
    claimant: str
    outcome: Optional[str] = Field(default=None)
    outcome_date: Optional[str] = Field(default=None, frozen=True)
    source_id: str
    statement: str
    variance: Optional[str] = Field(default=None)
    variance_explanation: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: source_id -> SRC-01.source_id

class ManagementDecisionLedger(ProvenanceMixin, PITMixin, BaseModel):
    """MDL-01: ManagementDecisionLedger. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MDL-01", frozen=True)
    capital_allocation_quality: str
    case_id: str
    concerns: Optional[str] = Field(default=None)
    evidence_ids: Optional[list[str]]
    incentive_alignment: Optional[str] = Field(default=None)
    ledger_id: str
    ma_history_summary: Optional[str] = Field(default=None)
    management_quality: Optional[str]
    per_share_trend: Optional[str] = Field(default=None)
    promise_ratio: str

    # FK: case_id -> CASE-01.case_id

class ManagementOutcome(ProvenanceMixin, PITMixin, BaseModel):
    """MO-02: ManagementOutcome. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MO-02", frozen=True)
    case_id: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    is_resolved: Optional[str] = Field(default=None)
    management_claim_id: str
    measured_outcome: str
    outcome_date: str = Field(frozen=True)
    outcome_id: str
    variance: str
    variance_explanation: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: management_claim_id -> MC-01.claim_id

class QualityAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """QA-01: QualityAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="QA-01", frozen=True)
    assessment_id: str
    assessor: str
    case_id: str
    evidence_ids: Optional[list[str]]
    false_quality_test_completed: str
    industry_economics_id: Optional[str] = Field(default=None)
    moat_assessment_id: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    quality_state: str

    # FK: case_id -> CASE-01.case_id
    # FK: evidence_ids -> EV-01.evidence_id