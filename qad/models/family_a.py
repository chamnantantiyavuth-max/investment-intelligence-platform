"""Family A — Identity & Coverage
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class CaseRecord(ProvenanceMixin, PITMixin, BaseModel):
    """CASE-01: CaseRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CASE-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    budget_id: Optional[str] = Field(default=None)
    candidate_id: str
    case_id: str
    case_state: str
    case_version: Optional[str] = Field(default=None)
    charter_id: Optional[str] = Field(default=None)
    closed_at: Optional[str] = Field(default=None, frozen=True)
    closing_reason: Optional[str] = Field(default=None)
    entity_id: str = Field(frozen=True)
    manifest_id: Optional[str] = Field(default=None)
    opened_at: str = Field(frozen=True)
    research_director: str

    # FK: entity_id -> SM-01.entity_id
    # FK: candidate_id -> CR-01.candidate_id

class CandidateRecord(ProvenanceMixin, PITMixin, BaseModel):
    """CR-01: CandidateRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CR-01", frozen=True)
    candidate_id: str
    dislocation_flag: Optional[bool] = Field(default=None)
    entity_id: str = Field(frozen=True)
    entry_route: str
    entry_timestamp: str = Field(frozen=True)
    evidence_freshness: str
    quality_flag: Optional[bool] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None)
    selection_state: str
    signal_ids: str
    watch_conditions: Optional[str] = Field(default=None)
    watch_price: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id
    # FK: signal_ids -> SR-01.signal_id

class QualityUniverseRecord(ProvenanceMixin, PITMixin, BaseModel):
    """QU-01: QualityUniverseRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="QU-01", frozen=True)
    assessment_date: str = Field(frozen=True)
    entity_id: str = Field(frozen=True)
    evidence_ids: Optional[list[str]]
    moat_depth: Optional[str] = Field(default=None)
    moat_durability: Optional[str] = Field(default=None)
    moat_trend: Optional[str] = Field(default=None)
    moat_types: Optional[str] = Field(default=None)
    moat_width: Optional[str] = Field(default=None)
    quality_state: str

    # FK: entity_id -> SM-01.entity_id
    # FK: evidence_ids -> EV-01.evidence_id

class ResearchableUniverseRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RU-01: ResearchableUniverseRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RU-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    dislocation_flag: Optional[bool] = Field(default=None)
    entity_id: str = Field(frozen=True)
    exclusion_category: Optional[str] = Field(default=None)
    exclusion_detail: Optional[str] = Field(default=None)
    inclusion_reason: str
    inclusion_state: str
    last_reviewed: Optional[str] = Field(default=None, frozen=True)
    quality_flag: Optional[bool] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id

class SecurityMaster(ProvenanceMixin, PITMixin, BaseModel):
    """SM-01: SecurityMaster. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SM-01", frozen=True)
    adr_flag: Optional[bool] = Field(default=None)
    cik: str
    corporate_actions: Optional[list[str]] = Field(default=None)
    dual_listings: Optional[list[str]] = Field(default=None)
    entity_id: str = Field(frozen=True)
    exchange: str
    industry: Optional[str] = Field(default=None)
    isin: Optional[str] = Field(default=None)
    name: str
    primary_ticker: str
    sector: Optional[str] = Field(default=None)
    security_type: str
    sedol: Optional[str] = Field(default=None)
    status: str
    ticker_history: Optional[list[str]] = Field(default=None)

class SignalRecord(ProvenanceMixin, PITMixin, BaseModel):
    """SR-01: SignalRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SR-01", frozen=True)
    data_version: Optional[str] = Field(default=None)
    detection_timestamp: str = Field(frozen=True)
    entity_id: str = Field(frozen=True)
    entry_route: str
    model_version: Optional[str] = Field(default=None)
    rule_version: Optional[str] = Field(default=None)
    signal_description: Optional[str] = Field(default=None)
    signal_evidence: Optional[str] = Field(default=None)
    signal_family: str
    signal_id: str
    signal_threshold: Optional[str] = Field(default=None)
    signal_type: str
    signal_value: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id