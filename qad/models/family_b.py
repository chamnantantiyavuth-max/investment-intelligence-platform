"""Family B — Evidence & Sources
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class ClaimRecord(ProvenanceMixin, PITMixin, BaseModel):
    """CLM-01: ClaimRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CLM-01", frozen=True)
    claim_date: str = Field(frozen=True)
    claim_id: str
    claimant: str
    evidence_id: str
    outcome: Optional[str] = Field(default=None)
    outcome_date: Optional[str] = Field(default=None, frozen=True)
    resolution: Optional[str] = Field(default=None)
    statement: str
    variance: Optional[str] = Field(default=None)

    # FK: evidence_id -> EV-01.evidence_id

class ContradictionRecord(ProvenanceMixin, PITMixin, BaseModel):
    """CTR-01: ContradictionRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CTR-01", frozen=True)
    contradiction_id: str
    contradiction_type: str
    discovered_by: str
    evidence_ids: Optional[list[str]]
    notes: Optional[str] = Field(default=None)
    resolution_evidence_id: Optional[str] = Field(default=None)
    resolution_status: str
    resolution_timestamp: Optional[str] = Field(default=None, frozen=True)

    # FK: evidence_ids -> EV-01.evidence_id

class EvidenceAdmissionRecord(ProvenanceMixin, PITMixin, BaseModel):
    """EAR-01: EvidenceAdmissionRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="EAR-01", frozen=True)
    admission_id: str
    admission_timestamp: str = Field(frozen=True)
    admitting_role: str
    contradiction_check: Optional[str] = Field(default=None)
    evidence_id: str
    original_source_verified: Optional[str] = Field(default=None)
    pit_verified: Optional[str] = Field(default=None)
    source_tier_check: str
    validation_method: str
    validation_notes: Optional[str] = Field(default=None)

    # FK: evidence_id -> EV-01.evidence_id

class EvidenceGap(ProvenanceMixin, PITMixin, BaseModel):
    """EG-01: EvidenceGap. Frozen M4A canonical schema."""
    schema_id: str = Field(default="EG-01", frozen=True)
    case_id: str
    created_by: str
    falsifiable_question: Optional[str] = Field(default=None)
    gap_id: str
    importance: str
    investigator_charter_id: Optional[str] = Field(default=None)
    operational_status: str
    question: str
    resolution_evidence_id: Optional[str] = Field(default=None)
    resolvability_class: str
    resolved_at: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id

class EvidenceRecord(ProvenanceMixin, PITMixin, BaseModel):
    """EV-01: EvidenceRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="EV-01", frozen=True)
    admitting_role: str
    as_of: str = Field(frozen=True)
    confidence: Optional[str] = Field(default=None)
    content: str
    context: Optional[str] = Field(default=None)
    contradicts_ids: Optional[str] = Field(default=None)
    evidence_id: str
    evidence_type: str
    extraction_method: Optional[str] = Field(default=None)
    extractor: str
    source_id: str
    source_tier: str
    superseded_by_id: Optional[str] = Field(default=None)
    validation_status: str

    # FK: source_id -> SRC-01.source_id
    # FK: contradicts_ids -> EV-01.evidence_id

class FactRecord(ProvenanceMixin, PITMixin, BaseModel):
    """FACT-01: FactRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="FACT-01", frozen=True)
    evidence_id: str
    fact_id: str
    numerical_value: Optional[str] = Field(default=None)
    page_number: Optional[str] = Field(default=None)
    paragraph: Optional[str] = Field(default=None)
    precision: Optional[str] = Field(default=None)
    source_location: str
    statement: str
    unit: Optional[str] = Field(default=None)
    verification_status: str

    # FK: evidence_id -> EV-01.evidence_id

class HypothesisRecord(ProvenanceMixin, PITMixin, BaseModel):
    """HYP-01: HypothesisRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="HYP-01", frozen=True)
    case_id: str
    current_plausibility: Optional[str] = Field(default=None)
    evidence_against: Optional[str] = Field(default=None)
    evidence_for: Optional[str] = Field(default=None)
    falsification_criteria: str
    hypothesis_id: str
    hypothesis_label: str
    initial_plausibility: str
    originator: str
    statement: str
    status_history: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class InferenceRecord(ProvenanceMixin, PITMixin, BaseModel):
    """INF-01: InferenceRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="INF-01", frozen=True)
    alternative_conclusions: Optional[str] = Field(default=None)
    conclusion: str
    confidence: Optional[str]
    contradicting_evidence: Optional[str] = Field(default=None)
    evidence_ids: Optional[list[str]]
    inference_chain: str
    inference_id: str
    inferrer: str
    supporting_evidence: Optional[list[str]] = Field(default=None)

    # FK: evidence_ids -> EV-01.evidence_id

class SourceRecord(ProvenanceMixin, PITMixin, BaseModel):
    """SRC-01: SourceRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SRC-01", frozen=True)
    author: Optional[str] = Field(default=None)
    content_hash: str
    file_size: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    pages_referenced: Optional[str] = Field(default=None)
    publication_date: Optional[str] = Field(default=None, frozen=True)
    retrieval_date: str = Field(frozen=True)
    source_id: str
    source_tier: str
    source_type: str
    title: Optional[str] = Field(default=None)
    url_or_identifier: str

class SourceVersion(ProvenanceMixin, PITMixin, BaseModel):
    """SRCV-01: SourceVersion. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SRCV-01", frozen=True)
    change_reason: Optional[str] = Field(default=None)
    content_hash: str
    file_size: Optional[str] = Field(default=None)
    format: Optional[str] = Field(default=None)
    previous_version_id: Optional[str] = Field(default=None)
    retrieval_date: str = Field(frozen=True)
    source_id: str
    version_id: str
    version_number: str

    # FK: source_id -> SRC-01.source_id