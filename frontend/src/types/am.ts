// Alpha Momentum — TypeScript types (mirrors backend/schemas/responses.py)
export interface ThemeSummary {
  id: string;
  name: string;
  approval_status: string;
  lifecycle: string;
  driver_count: number;
  candidate_count: number;
  evidence_supporting: number;
  evidence_contradicting: number;
  evidence_missing: number;
  theme_quality: number;
  candidate_quality: number;
  entry_readiness: number;
  data_confidence: number;
  data_source: string;
}
