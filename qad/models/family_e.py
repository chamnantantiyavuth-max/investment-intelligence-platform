"""Family E — Impairment & Recovery
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class CompetingExplanationAlternative_diagnosis(str, Enum):
    TEMPORARY = "TEMPORARY"
    MOSTLY_TEMPORARY = "MOSTLY_TEMPORARY"
    MIXED = "MIXED"
    STRUCTURAL = "STRUCTURAL"
    UNRESOLVED = "UNRESOLVED"

class DislocationRecordCause_classification(str, Enum):
    CYCLICAL = "CYCLICAL"
    COMPETITIVE = "COMPETITIVE"
    TECHNOLOGICAL = "TECHNOLOGICAL"
    REGULATORY = "REGULATORY"
    COMPANY_SPECIFIC = "COMPANY_SPECIFIC"
    MACRO = "MACRO"
    MIXED = "MIXED"

class FlipEvidenceWould_flip_to(str, Enum):
    TEMPORARY = "TEMPORARY"
    MOSTLY_TEMPORARY = "MOSTLY_TEMPORARY"
    MIXED = "MIXED"
    STRUCTURAL = "STRUCTURAL"
    UNRESOLVED = "UNRESOLVED"

class ImpairmentAssessmentDiagnosis(str, Enum):
    TEMPORARY = "TEMPORARY"
    MOSTLY_TEMPORARY = "MOSTLY_TEMPORARY"
    MIXED = "MIXED"
    STRUCTURAL = "STRUCTURAL"
    UNRESOLVED = "UNRESOLVED"

class RecoveryModelRecovery_scenario(str, Enum):
    V_SHAPED = "V_SHAPED"
    U_SHAPED = "U_SHAPED"
    L_SHAPED = "L_SHAPED"
    W_SHAPED = "W_SHAPED"

class ThesisKillerSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CompetingExplanation(BaseModel):
    """CE-01: CompetingExplanation.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CE-01", frozen=True)
    alternative_diagnosis: CompetingExplanationAlternative_diagnosis
    explanation_id: str
    impairment_id: str
    supporting_evidence_ids: list[str]
    why_not_primary: str
    assessment_date: Optional[str] = Field(default=None)
    assessor: Optional[str] = Field(default=None)
    evidence_that_would_change_priority: Optional[list[str]] = Field(default=None)

    # FK: impairment_id -> IA-01.impairment_id


class DislocationRecord(BaseModel):
    """DR-01: DislocationRecord.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="DR-01", frozen=True)
    broken_variables: list[str]
    case_id: str
    cause_classification: DislocationRecordCause_classification
    dislocation_id: str
    moat_test_result: str
    peer_test_result: str
    root_cause: str
    assessment_date: Optional[str] = Field(default=None)
    assessor: Optional[str] = Field(default=None)
    balance_sheet_runway: Optional[str] = Field(default=None)
    external_evidence_ids: Optional[list[str]] = Field(default=None)
    price_test_result: Optional[str] = Field(default=None)
    reversibility_assessment: Optional[str] = Field(default=None)
    thesis_killers: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class FlipEvidence(BaseModel):
    """FE-01: FlipEvidence.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="FE-01", frozen=True)
    condition: str
    flip_evidence_id: str
    impairment_id: str
    observability: str
    would_flip_to: FlipEvidenceWould_flip_to
    defined_at: Optional[str] = Field(default=None)
    definer: Optional[str] = Field(default=None)
    evidence_source: Optional[str] = Field(default=None)
    probability_if_observed: Optional[str] = Field(default=None)
    timeframe: Optional[str] = Field(default=None)

    # FK: impairment_id -> IA-01.impairment_id


class ImpairmentAssessment(BaseModel):
    """IA-01: ImpairmentAssessment.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="IA-01", frozen=True)
    case_id: str
    diagnosis: ImpairmentAssessmentDiagnosis
    evidence_ids: list[str]
    flip_evidence: str
    impairment_id: str
    primary_diagnosis: str
    strongest_competing_explanation: str
    weakest_link: str
    why_primary_dominates: str
    assessment_date: Optional[str] = Field(default=None)
    assessor: Optional[str] = Field(default=None)
    competing_hypothesis_evidence: Optional[list[str]] = Field(default=None)
    impairment_dimensions: Optional[dict] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class RecoveryModel(BaseModel):
    """RM-01: RecoveryModel.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RM-01", frozen=True)
    case_id: str
    cause: str
    expected_sequence: str
    invalidation: str
    leading_evidence: str
    recovery_id: str
    recovery_mechanism: str
    time_horizon: str = Field(frozen=True)
    assessment_date: Optional[str] = Field(default=None)
    assessor: Optional[str] = Field(default=None)
    evidence_ids: Optional[list[str]] = Field(default=None)
    recovery_scenario: Optional[RecoveryModelRecovery_scenario] = Field(default=None)
    thesis_killers: Optional[list[str]] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ThesisKiller(BaseModel):
    """TK-01: ThesisKiller.
    Frozen M4A canonical schema. Family E.
    """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="TK-01", frozen=True)
    case_id: str
    condition: str
    evidence_type: str
    severity: ThesisKillerSeverity
    thesis_killer_id: str
    trigger_status: str
    defined_at: Optional[str] = Field(default=None)
    definer: Optional[str] = Field(default=None)
    evidence_id: Optional[str] = Field(default=None, frozen=True)
    resolution: Optional[str] = Field(default=None)
    trigger_timestamp: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id