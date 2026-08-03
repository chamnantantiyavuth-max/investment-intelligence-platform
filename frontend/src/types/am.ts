// Alpha Momentum — TypeScript types (mirrors backend/schemas/responses.py — locked to REAL artifact fields, FD #46)
export interface Provenance {
  source: string;
  mode: string;
  as_of: string | null;
  coverage: string | null;
  completeness: string | null;
  hybrid: boolean;
  component_map?: Record<string, string>;
}

export interface EvidenceProvenance {
  source_id: string;
  source_type: "real" | "synthetic" | "human_sourced";
}

export interface EvidenceRecord {
  id: string;
  type: string;
  content: string;
  source: string | null;
}

export interface ThemeSummary {
  id: string;
  name: string;
  sector: string;
  industry: string;
  lifecycle: string;
  approval_status: string;
  monitoring_status: string;
  confidence: string;
  key_tickers: string[];
  stocks_in_industry: number;
  why_now: string;
  provenance: Provenance;
  evidence_provenance: EvidenceProvenance[];
  // Falsification read-only extension (mini-FD 4 Aug 2026, Constitution §11)
  alternative_explanations: Record<string, string> | null;
  evidence: EvidenceRecord[] | null;
  unresolved_counter_evidence: string[] | null;
}

export interface CandidateSummary {
  id: string;
  ticker: string;
  research_state: string;
  conviction_level: string;
  candidate_quality: {
    fundamentals: string;
    growth: string;
    liquidity: string;
    relative_strength: string;
    trend_quality: string;
    accumulation: string;
    industry_leadership: string;
  };
  entry_readiness: {
    price_structure: string;
    base_quality: string;
    breakout_proximity: string;
    volume_behavior: string;
    volatility_contraction: string;
    extension_risk: string;
  };
  data_confidence: {
    freshness: string;
    completeness: string;
    reliability: string;
    conflicts: string;
    missing_data: string;
  };
  provenance: Provenance;
}

export interface ThemeWithCandidates {
  theme: ThemeSummary;
  candidates: CandidateSummary[];
}

export interface AMQueueResponse {
  run_id: string;
  point_in_time: string | null;
  themes: ThemeWithCandidates[];
}
