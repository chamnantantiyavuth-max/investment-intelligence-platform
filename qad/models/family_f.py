"""Family F — Financial & Valuation
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class CalculationRecord(ProvenanceMixin, PITMixin, BaseModel):
    """CALC-01: CalculationRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CALC-01", frozen=True)
    calculated_by: str
    calculation_id: str
    case_id: str
    error_margin: Optional[str] = Field(default=None)
    formula: str
    input_fact_ids: Optional[str] = Field(default=None)
    inputs: str
    notes: Optional[str] = Field(default=None)
    result: str
    timestamp: str = Field(frozen=True)

    # FK: case_id -> CASE-01.case_id

class FinancialFact(ProvenanceMixin, PITMixin, BaseModel):
    """FF-01: FinancialFact. Frozen M4A canonical schema."""
    schema_id: str = Field(default="FF-01", frozen=True)
    case_id: str
    currency: Optional[str] = Field(default=None)
    financial_fact_id: str
    fiscal_year: str = Field(frozen=True)
    footnote: Optional[str] = Field(default=None)
    is_gaap: Optional[str] = Field(default=None)
    metric_name: str
    period: str = Field(frozen=True)
    restatement_flag: Optional[str] = Field(default=None)
    segment: Optional[str] = Field(default=None)
    source_id: str
    unit: str
    value: str

    # FK: case_id -> CASE-01.case_id
    # FK: source_id -> SRC-01.source_id

class NormalizedFinancialFact(ProvenanceMixin, PITMixin, BaseModel):
    """NFF-01: NormalizedFinancialFact. Frozen M4A canonical schema."""
    schema_id: str = Field(default="NFF-01", frozen=True)
    adjusted_value: str
    adjuster: str
    adjustment_amount: Optional[float] = Field(default=None)
    adjustment_rationale: str
    adjustment_type: str
    financial_fact_id: str
    is_permanent: Optional[str] = Field(default=None)
    normalized_fact_id: str
    source_id: Optional[str] = Field(default=None)

    # FK: financial_fact_id -> FF-01.financial_fact_id

class PriceImpliedExpectation(ProvenanceMixin, PITMixin, BaseModel):
    """PIE-01: PriceImpliedExpectation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="PIE-01", frozen=True)
    case_id: str
    current_price: str
    expectation_id: str
    implied_growth_rate: str
    implied_terminal_multiple: Optional[str] = Field(default=None)
    implied_terminal_value: str
    recovery_rate_implied: str
    scenario_comparison: str
    sensitivity_range: Optional[str] = Field(default=None)
    years_of_no_recovery_priced_in: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class PermanentLossAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """PLA-01: PermanentLossAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="PLA-01", frozen=True)
    assessment_id: str
    asset_impairment_risk: str
    balance_sheet_runway: str
    case_id: str
    competitive_damage: str
    covenant_risk: str
    dilution_risk: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    permanent_loss_range: Optional[str] = Field(default=None)
    recovery_capital_needed: Optional[str] = Field(default=None)
    refinancing_risk: str

    # FK: case_id -> CASE-01.case_id

class ReverseDCFRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RDCF-01: ReverseDCFRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RDCF-01", frozen=True)
    analyst: str
    case_id: str
    current_price: str
    implied_growth_rate: str
    implied_terminal_value: str
    r_dcf_id: str
    recovery_rate_implied: Optional[str] = Field(default=None)
    scenario_comparison: str
    sensitivity_range: Optional[str] = Field(default=None)
    years_of_no_recovery_priced_in: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class ScenarioRecord(ProvenanceMixin, PITMixin, BaseModel):
    """SCEN-01: ScenarioRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SCEN-01", frozen=True)
    assumptions: str
    case_id: str
    creator: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    intrinsic_value_estimate: str
    probability_weight: Optional[str] = Field(default=None)
    scenario_id: str
    scenario_type: str
    sensitivity_analysis: Optional[dict] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class ValuationAssessment(ProvenanceMixin, PITMixin, BaseModel):
    """VA-01: ValuationAssessment. Frozen M4A canonical schema."""
    schema_id: str = Field(default="VA-01", frozen=True)
    asymmetry_estimate: str
    case_id: str
    damage_gap: str
    economic_damage: str
    evidence_ids: Optional[list[str]] = Field(default=None)
    permanent_loss_id: str
    price_damage: str
    r_dcf_id: str
    scenario_values: str
    thesis_killers_financial: Optional[str] = Field(default=None)
    valuation_id: str
    valuation_range: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: r_dcf_id -> RDCF-01.r_dcf_id
    # FK: permanent_loss_id -> PLA-01.assessment_id