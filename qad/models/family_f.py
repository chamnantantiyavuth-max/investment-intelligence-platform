"""Family F — Financial & Economic Underwriting
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class FinancialFactMetric_family(str, Enum):
    REVENUE = "REVENUE"
    COGS = "COGS"
    SGA = "SG&A"
    RD = "R&D"
    DA = "D&A"
    OPERATING_INCOME = "OPERATING_INCOME"
    NET_INCOME = "NET_INCOME"
    EPS = "EPS"
    FCF = "FCF"
    CAPEX = "CAPEX"
    WORKING_CAPITAL = "WORKING_CAPITAL"
    DEBT = "DEBT"
    EQUITY = "EQUITY"
    ROIC = "ROIC"
    MARGIN = "MARGIN"
    SHARE_COUNT = "SHARE_COUNT"
    OTHER = "OTHER"

class NormalizedFinancialFactAdjustment_type(str, Enum):
    NON_RECURRING = "NON_RECURRING"
    CYCLICAL = "CYCLICAL"
    ACQUISITION_ACCOUNTING = "ACQUISITION_ACCOUNTING"
    PENSION = "PENSION"
    STOCK_COMPENSATION = "STOCK_COMPENSATION"
    DEFERRED_TAX = "DEFERRED_TAX"
    EXTRAORDINARY = "EXTRAORDINARY"
    OTHER = "OTHER"

class NormalizedFinancialFactIs_permanent(str, Enum):
    PERMANENT = "PERMANENT"
    TEMPORARY = "TEMPORARY"
    UNCERTAIN = "UNCERTAIN"

class PermanentLossAssessmentRisk_level(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ScenarioRecordScenario_type(str, Enum):
    CURRENT = "CURRENT"
    NO_RECOVERY = "NO_RECOVERY"
    PARTIAL_RECOVERY = "PARTIAL_RECOVERY"
    NORMALIZATION = "NORMALIZATION"
    QUALITY_COMPOUNDING = "QUALITY_COMPOUNDING"


class CalculationRecord(BaseModel):
    """CALC-01: CalculationRecord. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CALC-01", frozen=True)
    calculated_by: str = Field(frozen=True)
    calculation_id: str = Field(frozen=True)
    case_id: str = Field(frozen=True)
    formula: str = Field(frozen=True)
    inputs: list[str] = Field(frozen=True)
    result: str = Field(frozen=True)
    timestamp: str = Field(frozen=True)
    as_of: Optional[str] = Field(default=None, frozen=True)
    error_margin: Optional[str] = Field(default=None, frozen=True)
    formula_version: Optional[str] = Field(default=None, frozen=True)
    input_fact_ids: Optional[list[str]] = Field(default=None, frozen=True)
    notes: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class FinancialFact(BaseModel):
    """FF-01: FinancialFact. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="FF-01", frozen=True)
    case_id: str
    financial_fact_id: str
    fiscal_year: str = Field(frozen=True)
    metric_name: FinancialFactMetric_family
    period: str = Field(frozen=True)
    source_id: str
    unit: str
    value: str
    as_of: Optional[str] = Field(default=None, frozen=True)
    currency: Optional[str] = Field(default=None)
    extractor: Optional[str] = Field(default=None)
    footnote: Optional[str] = Field(default=None)
    is_gaap: Optional[str] = Field(default=None)
    restatement_flag: Optional[str] = Field(default=None)
    segment: Optional[str] = Field(default=None)
    source_location: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: source_id -> SRC-01.source_id


class NormalizedFinancialFact(BaseModel):
    """NFF-01: NormalizedFinancialFact. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="NFF-01", frozen=True)
    adjusted_value: str
    adjuster: str
    adjustment_rationale: str
    adjustment_type: NormalizedFinancialFactAdjustment_type
    financial_fact_id: str
    normalized_fact_id: str
    adjustment_amount: Optional[float] = Field(default=None)
    adjustment_date: Optional[str] = Field(default=None, frozen=True)
    is_permanent: Optional[NormalizedFinancialFactIs_permanent] = Field(default=None)
    methodology: Optional[str] = Field(default=None)
    source_id: Optional[str] = Field(default=None)

    # FK: financial_fact_id -> FF-01.financial_fact_id


class PriceImpliedExpectation(BaseModel):
    """PIE-01: PriceImpliedExpectation. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="PIE-01", frozen=True)
    case_id: str = Field(frozen=True)
    current_price: float = Field(frozen=True)
    expectation_id: str = Field(frozen=True)
    implied_growth_rate: float = Field(frozen=True)
    implied_terminal_value: float = Field(frozen=True)
    recovery_rate_implied: float = Field(frozen=True)
    scenario_comparison: dict = Field(frozen=True)
    analysis_date: Optional[str] = Field(default=None, frozen=True)
    analyst: Optional[str] = Field(default=None, frozen=True)
    implied_terminal_multiple: Optional[str] = Field(default=None, frozen=True)
    method_version: Optional[str] = Field(default=None, frozen=True)
    price_as_of: Optional[str] = Field(default=None, frozen=True)
    sensitivity_range: Optional[dict] = Field(default=None, frozen=True)
    years_of_no_recovery_priced_in: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class PermanentLossAssessment(BaseModel):
    """PLA-01: PermanentLossAssessment. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="PLA-01", frozen=True)
    assessment_id: str
    asset_impairment_risk: PermanentLossAssessmentRisk_level
    balance_sheet_runway: PermanentLossAssessmentRisk_level
    case_id: str
    competitive_damage: PermanentLossAssessmentRisk_level
    covenant_risk: PermanentLossAssessmentRisk_level
    dilution_risk: PermanentLossAssessmentRisk_level
    refinancing_risk: PermanentLossAssessmentRisk_level
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    evidence_ids: Optional[list[str]] = Field(default=None)
    permanent_loss_range: Optional[dict] = Field(default=None)
    recovery_capital_needed: Optional[float] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ReverseDCFRecord(BaseModel):
    """RDCF-01: ReverseDCFRecord. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RDCF-01", frozen=True)
    analyst: str = Field(frozen=True)
    case_id: str = Field(frozen=True)
    current_price: float = Field(frozen=True)
    implied_growth_rate: float = Field(frozen=True)
    implied_terminal_value: float = Field(frozen=True)
    r_dcf_id: str = Field(frozen=True)
    scenario_comparison: dict = Field(frozen=True)
    analysis_date: Optional[str] = Field(default=None, frozen=True)
    method_version: Optional[str] = Field(default=None, frozen=True)
    price_as_of: Optional[str] = Field(default=None, frozen=True)
    recovery_rate_implied: Optional[float] = Field(default=None, frozen=True)
    sensitivity_range: Optional[dict] = Field(default=None, frozen=True)
    years_of_no_recovery_priced_in: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class ScenarioRecord(BaseModel):
    """SCEN-01: ScenarioRecord. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SCEN-01", frozen=True)
    assumptions: dict = Field(frozen=True)
    case_id: str = Field(frozen=True)
    creator: str = Field(frozen=True)
    intrinsic_value_estimate: float = Field(frozen=True)
    scenario_id: str = Field(frozen=True)
    scenario_type: ScenarioRecordScenario_type = Field(frozen=True)
    as_of: Optional[str] = Field(default=None, frozen=True)
    created_at: Optional[str] = Field(default=None, frozen=True)
    evidence_ids: Optional[list[str]] = Field(default=None, frozen=True)
    probability_weight: Optional[float] = Field(default=None, frozen=True)
    sensitivity_analysis: Optional[dict] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class ValuationAssessment(BaseModel):
    """VA-01: ValuationAssessment. Frozen M4A canonical schema. Family F. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="VA-01", frozen=True)
    asymmetry_estimate: float
    case_id: str
    damage_gap: float
    economic_damage: float
    permanent_loss_id: str
    price_damage: float
    r_dcf_id: str
    scenario_values: dict
    valuation_id: str
    assessment_date: Optional[str] = Field(default=None, frozen=True)
    assessor: Optional[str] = Field(default=None)
    evidence_ids: Optional[list[str]] = Field(default=None)
    price_as_of: Optional[str] = Field(default=None, frozen=True)
    thesis_killers_financial: Optional[list[str]] = Field(default=None)
    valuation_range: Optional[dict] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: r_dcf_id -> RDCF-01.r_dcf_id
    # FK: permanent_loss_id -> PLA-01.assessment_id