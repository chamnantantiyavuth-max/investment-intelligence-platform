"""Family A — Identity & Coverage
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CaseRecordCase_state(str, Enum):
    CASE_OPEN = "CASE_OPEN"
    CHARTER_APPROVED = "CHARTER_APPROVED"
    SOURCE_FOUNDATION_COMPLETE = "SOURCE_FOUNDATION_COMPLETE"
    INITIAL_ANALYSIS_COMPLETE = "INITIAL_ANALYSIS_COMPLETE"
    DEEP_RESEARCH_COMPLETE = "DEEP_RESEARCH_COMPLETE"
    SCUTTLEBUTT_COMPLETE = "SCUTTLEBUTT_COMPLETE"
    EVIDENCE_CANONICAL = "EVIDENCE_CANONICAL"
    QUALITY_ANALYSIS_COMPLETE = "QUALITY_ANALYSIS_COMPLETE"
    ANALYTICAL_WORK_COMPLETE = "ANALYTICAL_WORK_COMPLETE"
    IMPAIRMENT_DIAGNOSIS_COMPLETE = "IMPAIRMENT_DIAGNOSIS_COMPLETE"
    VALUATION_COMPLETE = "VALUATION_COMPLETE"
    RED_TEAM_COMPLETE = "RED_TEAM_COMPLETE"
    AUDIT_COMPLETE = "AUDIT_COMPLETE"
    UNDERWRITING_COMPLETE = "UNDERWRITING_COMPLETE"
    FOUNDER_READY = "FOUNDER_READY"
    FOUNDER_DECIDED = "FOUNDER_DECIDED"
    MONITORING = "MONITORING"
    CLOSED = "CLOSED"

class CandidateRecordSelection_state(str, Enum):
    AUTO_RESEARCH_NOW = "AUTO_RESEARCH_NOW"
    WATCH_PRICE = "WATCH_PRICE"
    WATCH_EVIDENCE = "WATCH_EVIDENCE"
    DATA_LIMITED_WATCH = "DATA_LIMITED_WATCH"
    REJECT = "REJECT"
    SELECTION_ERROR = "SELECTION_ERROR"

class CandidateRecordEntry_route(str, Enum):
    QUALITY_FIRST = "QUALITY_FIRST"
    DISLOCATION_FIRST = "DISLOCATION_FIRST"
    EXTERNAL = "EXTERNAL"
    FOUNDER_DIRECTED = "FOUNDER_DIRECTED"

class QualityUniverseRecordQuality_state(str, Enum):
    VERIFIED = "VERIFIED"
    PROBABLE = "PROBABLE"
    UNRESOLVED = "UNRESOLVED"
    FAILED = "FAILED"

class ResearchableUniverseRecordInclusion_state(str, Enum):
    INCLUDED = "INCLUDED"
    EXCLUDED = "EXCLUDED"
    PENDING_REVIEW = "PENDING_REVIEW"
    DATA_LIMITED = "DATA_LIMITED"

class ResearchableUniverseRecordExclusion_category(str, Enum):
    NON_OPERATING = "NON_OPERATING"
    SHELL = "SHELL"
    DUPLICATE = "DUPLICATE"
    UNRESOLVED_IDENTITY = "UNRESOLVED_IDENTITY"
    NO_FINANCIAL_HISTORY = "NO_FINANCIAL_HISTORY"
    OTHER_APPROVED = "OTHER_APPROVED"

class SecurityMasterSecurity_type(str, Enum):
    COMMON_EQUITY = "COMMON_EQUITY"
    ADR = "ADR"
    PREFERRED = "PREFERRED"
    WARRANT = "WARRANT"
    ETF = "ETF"
    FUND = "FUND"
    OTHER = "OTHER"

class SecurityMasterStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DELISTED = "DELISTED"
    MERGED = "MERGED"
    ACQUIRED = "ACQUIRED"
    SPINOFF = "SPINOFF"
    UNKNOWN = "UNKNOWN"

class SignalRecordSignal_type(str, Enum):
    QUALITY = "QUALITY"
    DISLOCATION = "DISLOCATION"
    EXTERNAL = "EXTERNAL"
    FOUNDER_DIRECTED = "FOUNDER_DIRECTED"

class SignalRecordSignal_family(str, Enum):
    PRICE_DISLOCATION = "PRICE_DISLOCATION"
    MULTIPLE_COMPRESSION = "MULTIPLE_COMPRESSION"
    EARNINGS_REVISION = "EARNINGS_REVISION"
    REVENUE_DETERIORATION = "REVENUE_DETERIORATION"
    MARGIN_ANOMALY = "MARGIN_ANOMALY"
    WORKING_CAPITAL = "WORKING_CAPITAL"
    GOVERNANCE = "GOVERNANCE"
    REGULATORY = "REGULATORY"
    INDUSTRY_SHOCK = "INDUSTRY_SHOCK"
    COMPETITOR_DIVERGENCE = "COMPETITOR_DIVERGENCE"
    NARRATIVE_GAP = "NARRATIVE_GAP"
    EXTERNAL = "EXTERNAL"

class SignalRecordEntry_route(str, Enum):
    QUALITY_FIRST = "QUALITY_FIRST"
    DISLOCATION_FIRST = "DISLOCATION_FIRST"
    EXTERNAL = "EXTERNAL"
    FOUNDER_DIRECTED = "FOUNDER_DIRECTED"


class CaseRecord(BaseModel):
    """CASE-01: CaseRecord. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CASE-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    candidate_id: str
    case_id: str
    case_state: CaseRecordCase_state
    entity_id: str
    opened_at: str = Field(frozen=True)
    research_director: str
    budget_id: Optional[str] = Field(default=None)
    case_version: Optional[str] = Field(default=None)
    charter_id: Optional[str] = Field(default=None)
    closed_at: Optional[str] = Field(default=None, frozen=True)
    closing_reason: Optional[str] = Field(default=None)
    manifest_id: Optional[str] = Field(default=None)
    opening_note: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id
    # FK: candidate_id -> CR-01.candidate_id


class CandidateRecord(BaseModel):
    """CR-01: CandidateRecord. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CR-01", frozen=True)
    candidate_id: str
    entity_id: str
    entry_route: CandidateRecordEntry_route
    entry_timestamp: str = Field(frozen=True)
    evidence_freshness: str
    selection_state: CandidateRecordSelection_state
    signal_ids: list[str]
    data_version: Optional[str] = Field(default=None)
    dislocation_flag: Optional[bool] = Field(default=None)
    last_evaluated: Optional[str] = Field(default=None, frozen=True)
    policy_version: Optional[str] = Field(default=None)
    quality_flag: Optional[bool] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None)
    selector: Optional[str] = Field(default=None)
    watch_conditions: Optional[str] = Field(default=None)
    watch_price: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id
    # FK: signal_ids[] -> SR-01.signal_id


class QualityUniverseRecord(BaseModel):
    """QU-01: QualityUniverseRecord. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="QU-01", frozen=True)
    assessment_date: str = Field(frozen=True)
    entity_id: str = Field(frozen=True)
    evidence_ids: list[str]
    quality_state: QualityUniverseRecordQuality_state
    as_of_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    data_version: Optional[str] = Field(default=None)
    moat_depth: Optional[str] = Field(default=None)
    moat_durability: Optional[str] = Field(default=None)
    moat_trend: Optional[str] = Field(default=None)
    moat_types: Optional[list[str]] = Field(default=None)
    moat_width: Optional[str] = Field(default=None)
    rule_version: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id
    # FK: evidence_ids[] -> EV-01.evidence_id


class ResearchableUniverseRecord(BaseModel):
    """RU-01: ResearchableUniverseRecord. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RU-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    entity_id: str
    inclusion_reason: str
    inclusion_state: ResearchableUniverseRecordInclusion_state
    data_version: Optional[str] = Field(default=None)
    dislocation_flag: Optional[bool] = Field(default=None)
    exclusion_category: Optional[ResearchableUniverseRecordExclusion_category] = Field(default=None)
    exclusion_detail: Optional[str] = Field(default=None)
    last_reviewed: Optional[str] = Field(default=None, frozen=True)
    quality_flag: Optional[bool] = Field(default=None)
    reviewer: Optional[str] = Field(default=None)
    rule_version: Optional[str] = Field(default=None)

    # FK: entity_id -> SM-01.entity_id


class SecurityMaster(BaseModel):
    """SM-01: SecurityMaster. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SM-01", frozen=True)
    cik: str
    entity_id: str = Field(frozen=True)
    exchange: str
    name: str
    primary_ticker: str
    security_type: SecurityMasterSecurity_type
    status: SecurityMasterStatus
    adr_flag: Optional[bool] = Field(default=None)
    as_of_date: Optional[str] = Field(default=None, frozen=True)
    corporate_actions: Optional[list[str]] = Field(default=None)
    data_version: Optional[str] = Field(default=None)
    dual_listings: Optional[list[str]] = Field(default=None)
    effective_date: Optional[str] = Field(default=None, frozen=True)
    industry: Optional[str] = Field(default=None)
    isin: Optional[str] = Field(default=None)
    resolver: Optional[str] = Field(default=None)
    retrieval_timestamp: Optional[str] = Field(default=None)
    sector: Optional[str] = Field(default=None)
    sedol: Optional[str] = Field(default=None)
    source: Optional[str] = Field(default=None)
    termination_date: Optional[str] = Field(default=None, frozen=True)
    ticker_history: Optional[list[str]] = Field(default=None)


class SignalRecord(BaseModel):
    """SR-01: SignalRecord. Frozen M4A canonical schema. Family A. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SR-01", frozen=True)
    detection_timestamp: str = Field(frozen=True)
    entity_id: str = Field(frozen=True)
    entry_route: SignalRecordEntry_route = Field(frozen=True)
    signal_family: SignalRecordSignal_family = Field(frozen=True)
    signal_id: str = Field(frozen=True)
    signal_type: SignalRecordSignal_type = Field(frozen=True)
    as_of_date: Optional[str] = Field(default=None, frozen=True)
    data_version: Optional[str] = Field(default=None, frozen=True)
    detector: Optional[str] = Field(default=None, frozen=True)
    model_version: Optional[str] = Field(default=None, frozen=True)
    rule_version: Optional[str] = Field(default=None, frozen=True)
    signal_description: Optional[str] = Field(default=None, frozen=True)
    signal_evidence: Optional[str] = Field(default=None, frozen=True)
    signal_threshold: Optional[str] = Field(default=None, frozen=True)
    signal_value: Optional[str] = Field(default=None, frozen=True)
    source: Optional[str] = Field(default=None, frozen=True)

    # FK: entity_id -> SM-01.entity_id