// Phase 8 + FD #46: Fundamental & Opportunity — TypeScript types
// Mirrors Pydantic schemas in backend/schemas/responses.py (real-artifact contracts + provenance)
import type { Provenance } from "./am";

export interface MoatType {
  type: string;
  strength: string;
  evidence: string;
}

export interface ResearchPackageSummary {
  id: string;
  name: string;
  sector: string;
  industry: string;
  moat_width: string;
  moat_depth: string;
  moat_trend: string;
  earnings_quality: string;
  conviction: string;
  value_trap_verdict: string;
  provenance: Provenance;
}

export interface EarningsQuality {
  rating: string;
  conviction_impact: string;
  surprise_direction: string;
  surprise_magnitude_pct: number;
  revenue_quality: string;
  margin_quality: string;
  fcf_conversion: number;
  one_time_items: boolean;
  guidance_direction: string;
  guidance_reason: string;
  narrative: string;
}

export interface MoatAssessment {
  types: MoatType[];
  active_count: number;
  total_types: number;
  width: string;
  depth: string;
  trend: string;
  types_summary: string;
  moat_narrative: string;
  moat_score: number;
  conviction_cap: string;
}

export interface ValueTrapResult {
  triggered: boolean;
  score: number;
  max_score: number;
  verdict: string;
  action: string;
}

export interface ConvictionDetail {
  level: string;
  cap: string;
  rationale: string;
}

export interface ResearchPackageDetail {
  id: string;
  name: string;
  sector: string;
  industry: string;
  moat_width: string;
  moat_depth: string;
  moat_trend: string;
  earnings_quality: string;
  conviction: ConvictionDetail;
  value_trap_verdict: string;
  provenance: Provenance;
  generated_at: string;
  spec_ref: string;
  thesis_summary: string;
  thesis_lifecycle: string;
  macro_context: Record<string, unknown>;
  industry_assessment: Record<string, unknown>;
  company_assessment: Record<string, unknown>;
  earnings_trajectory: EarningsQuality;
  valuation_context: Record<string, unknown>;
  key_risks: string[];
  independent_challenge: string[];
  supporting_evidence: string[];
  contradicting_evidence: string[];
  open_questions: string[];
}
