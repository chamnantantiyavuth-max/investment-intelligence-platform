"""Family E — Dislocation & Impairment
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class CompetingExplanation(ProvenanceMixin, PITMixin, BaseModel):
    """CE-01: CompetingExplanation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CE-01", frozen=True)
    alternative_diagnosis: str
    evidence_that_would_change_priority: Optional[str] = Field(default=None)
    explanation_id: str
    impairment_id: str
    supporting_evidence_ids: str
    why_not_primary: str

    # FK: impairment_id -> IA-01.impairment_id

class DislocationRecord(ProvenanceMixin, PITMixin, BaseModel):
    """DR-01: DislocationRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="DR-01", frozen=True)
    balance_sheet_runway: Optional[str] = Field(default=None)
    broken_variables: str
    case_id: str
    cause_classification: str
    dislocation_id: str
    external_evidence_ids: Optional[str] = Field(default=None)
    moat_test_result: str
    peer_test_result: str
    price_test_result: Optional[str] = Field(default=None)
    reversibility_assessment: Optional[str] = Field(default=None)
    root_cause: str
    thesis_killers: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class FlipEvidence(ProvenanceMixin, PITMixin, BaseModel):
    """FE-01: FlipEvidence. Frozen M4A canonical schema."""
    schema_id: str = Field(default="FE-01", frozen=True)
    condition: Optional[list[str]]
    evidence_source: Optional[str] = Field(default=None)
    flip_evidence_id: str
    impairment_id: str
    observability: str
    probability_if_observed: Optional[str] = Field(default=None)
    timeframe: Optional[str] = Field(default=None)
    would_flip_to: str

    # FK: impairment_id -> IA-01.impairment_id

class ImpairmentAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """IA-01: ImpairmentAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="IA-01", frozen=True)
    case_id: str
    competing_hypothesis_evidence: Optional[str] = Field(default=None)
    diagnosis: str
    evidence_ids: Optional[list[str]]
    flip_evidence: str
    impairment_dimensions: Optional[str] = Field(default=None)
    impairment_id: str
    primary_diagnosis: str
    strongest_competing_explanation: str
    weakest_link: str
    why_primary_dominates: str

    # FK: case_id -> CASE-01.case_id

class RecoveryModel(ProvenanceMixin, PITMixin, BaseModel):
    """RM-01: RecoveryModel. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RM-01", frozen=True)
    case_id: str
    cause: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    expected_sequence: str
    invalidation: str
    leading_evidence: str
    recovery_id: str
    recovery_mechanism: str
    recovery_scenario: Optional[str] = Field(default=None)
    thesis_killers: Optional[str] = Field(default=None)
    time_horizon: str = Field(frozen=True)

    # FK: case_id -> CASE-01.case_id

class ThesisKiller(ProvenanceMixin, PITMixin, BaseModel):
    """TK-01: ThesisKiller. Frozen M4A canonical schema."""
    schema_id: str = Field(default="TK-01", frozen=True)
    case_id: str
    condition: Optional[list[str]]
    evidence_id: Optional[str] = Field(default=None)
    evidence_type: str
    resolution: Optional[str] = Field(default=None)
    severity: str
    thesis_killer_id: str
    trigger_status: str
    trigger_timestamp: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id