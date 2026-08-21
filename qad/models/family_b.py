"""Family B — Source & Evidence
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ClaimRecordClaimant_type(str, Enum):
    MANAGEMENT = "MANAGEMENT"
    ANALYST = "ANALYST"
    REGULATOR = "REGULATOR"
    CUSTOMER = "CUSTOMER"
    COMPETITOR = "COMPETITOR"
    OTHER = "OTHER"

class ContradictionRecordContradiction_type(str, Enum):
    DIRECT = "DIRECT"
    CIRCUMSTANTIAL = "CIRCUMSTANTIAL"
    NUMERICAL = "NUMERICAL"
    TEMPORAL = "TEMPORAL"

class EvidenceAdmissionRecordAdmission_method(str, Enum):
    DIRECT_SOURCE = "DIRECT_SOURCE"
    AI_EXTRACTION = "AI_EXTRACTION"
    AI_SYNTHESIS = "AI_SYNTHESIS"
    HUMAN_ANALYSIS = "HUMAN_ANALYSIS"
    SCUTTLEBUTT = "SCUTTLEBUTT"

class EvidenceRecordEvidence_type(str, Enum):
    FACT = "FACT"
    CLAIM = "CLAIM"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"

class FactRecordVerification_status(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    DISPUTED = "DISPUTED"

class HypothesisRecordHypothesis_label(str, Enum):
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"
    H4 = "H4"
    H5 = "H5"

class InferenceRecordConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    SPECULATIVE = "SPECULATIVE"

class SourceRecordSource_tier(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"
    L7 = "L7"
    L8 = "L8"
    L9 = "L9"
    L10 = "L10"

class SourceVersionChange_reason(str, Enum):
    INITIAL_RETRIEVAL = "INITIAL_RETRIEVAL"
    RE_RETRIEVAL = "RE_RETRIEVAL"
    CORRECTION = "CORRECTION"
    REMOVAL_TOMBSTONE = "REMOVAL_TOMBSTONE"


class ClaimRecord(BaseModel):
    """CLM-01: ClaimRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CLM-01", frozen=True)
    claim_date: str = Field(frozen=True)
    claim_id: str
    claimant: str
    evidence_id: str = Field(frozen=True)
    statement: str
    extractor: Optional[str] = Field(default=None)
    outcome: Optional[str] = Field(default=None)
    outcome_date: Optional[str] = Field(default=None, frozen=True)
    resolution: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    variance: Optional[str] = Field(default=None)

    # FK: evidence_id -> EV-01.evidence_id


class ContradictionRecord(BaseModel):
    """CTR-01: ContradictionRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CTR-01", frozen=True)
    contradiction_id: str
    contradiction_type: ContradictionRecordContradiction_type
    discovered_by: str
    evidence_ids: list[str]
    resolution_status: str
    discovered_at: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    resolution_evidence_id: Optional[str] = Field(default=None)
    resolution_timestamp: Optional[str] = Field(default=None, frozen=True)
    resolver: Optional[str] = Field(default=None)

    # FK: evidence_ids[] -> EV-01.evidence_id


class EvidenceAdmissionRecord(BaseModel):
    """EAR-01: EvidenceAdmissionRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="EAR-01", frozen=True)
    admission_id: str
    admission_timestamp: str = Field(frozen=True)
    admitting_role: str
    evidence_id: str = Field(frozen=True)
    source_tier_check: str
    validation_method: str
    contradiction_check: Optional[str] = Field(default=None)
    original_source_verified: Optional[str] = Field(default=None)
    pit_verified: Optional[str] = Field(default=None)
    source_as_of: Optional[str] = Field(default=None)
    validation_notes: Optional[str] = Field(default=None)

    # FK: evidence_id -> EV-01.evidence_id


class EvidenceGap(BaseModel):
    """EG-01: EvidenceGap.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="EG-01", frozen=True)
    case_id: str
    created_by: str
    gap_id: str
    importance: str
    operational_status: str
    question: str
    resolvability_class: str
    created_at: Optional[str] = Field(default=None)
    falsifiable_question: Optional[str] = Field(default=None)
    investigator_charter_id: Optional[str] = Field(default=None)
    resolution_evidence_id: Optional[str] = Field(default=None)
    resolved_at: Optional[str] = Field(default=None, frozen=True)
    resolver: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class EvidenceRecord(BaseModel):
    """EV-01: EvidenceRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="EV-01", frozen=True)
    admitting_role: str
    as_of: str = Field(frozen=True)
    content: str = Field(frozen=True)
    evidence_id: str = Field(frozen=True)
    evidence_type: EvidenceRecordEvidence_type
    extractor: str
    source_id: str
    source_tier: str
    validation_status: str
    confidence: Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    contradicts_ids: Optional[list[str]] = Field(default=None)
    extraction_method: Optional[str] = Field(default=None)
    source_version: Optional[str] = Field(default=None)
    superseded_by_id: Optional[str] = Field(default=None)
    validation_method: Optional[str] = Field(default=None)
    validation_timestamp: Optional[str] = Field(default=None)

    # FK: source_id -> SRC-01.source_id
    # FK: contradicts_ids[] -> EV-01.evidence_id


class FactRecord(BaseModel):
    """FACT-01: FactRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="FACT-01", frozen=True)
    evidence_id: str = Field(frozen=True)
    fact_id: str = Field(frozen=True)
    source_location: str
    statement: str
    verification_status: FactRecordVerification_status
    as_of: Optional[str] = Field(default=None)
    extractor: Optional[str] = Field(default=None)
    numerical_value: Optional[str] = Field(default=None)
    page_number: Optional[str] = Field(default=None)
    paragraph: Optional[str] = Field(default=None)
    precision: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)

    # FK: evidence_id -> EV-01.evidence_id


class HypothesisRecord(BaseModel):
    """HYP-01: HypothesisRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="HYP-01", frozen=True)
    case_id: str
    falsification_criteria: str
    hypothesis_id: str
    hypothesis_label: HypothesisRecordHypothesis_label
    initial_plausibility: str
    originator: str
    statement: str
    created_at: Optional[str] = Field(default=None)
    current_plausibility: Optional[str] = Field(default=None)
    evidence_against: Optional[list[str]] = Field(default=None)
    evidence_for: Optional[list[str]] = Field(default=None)
    last_updated: Optional[str] = Field(default=None)
    research_charter: Optional[str] = Field(default=None)
    status_history: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class InferenceRecord(BaseModel):
    """INF-01: InferenceRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="INF-01", frozen=True)
    conclusion: str
    confidence: InferenceRecordConfidence
    evidence_ids: list[str]
    inference_chain: str
    inference_id: str
    inferrer: str
    alternative_conclusions: Optional[list[str]] = Field(default=None)
    as_of: Optional[str] = Field(default=None)
    contradicting_evidence: Optional[list[str]] = Field(default=None)
    inference_method: Optional[str] = Field(default=None)
    inference_timestamp: Optional[str] = Field(default=None)
    supporting_evidence: Optional[list[str]] = Field(default=None)

    # FK: evidence_ids[] -> EV-01.evidence_id


class SourceRecord(BaseModel):
    """SRC-01: SourceRecord.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SRC-01", frozen=True)
    content_hash: str
    retrieval_date: str = Field(frozen=True)
    source_id: str
    source_tier: SourceRecordSource_tier
    source_type: str
    url_or_identifier: str
    author: Optional[str] = Field(default=None)
    file_size: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    pages_referenced: Optional[list[str]] = Field(default=None)
    publication_date: Optional[str] = Field(default=None, frozen=True)
    retrieval_method: Optional[str] = Field(default=None)
    retriever: Optional[str] = Field(default=None)
    source_url_hash: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)


class SourceVersion(BaseModel):
    """SRCV-01: SourceVersion.
    Frozen M4A canonical schema. Family B.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SRCV-01", frozen=True)
    content_hash: str
    retrieval_date: str = Field(frozen=True)
    source_id: str
    version_id: str
    version_number: str
    change_reason: Optional[SourceVersionChange_reason] = Field(default=None)
    file_size: Optional[str] = Field(default=None)
    format: Optional[str] = Field(default=None)
    previous_version_id: Optional[str] = Field(default=None)
    retrieval_method: Optional[str] = Field(default=None)
    retriever: Optional[str] = Field(default=None)

    # FK: source_id -> SRC-01.source_id