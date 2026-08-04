// Institutional Intelligence — TypeScript types (NEW surface, FD #46)
import type { Provenance } from "./am";

export interface IISignalSummary {
  filer_name: string;
  filer_cik: string;
  filer_category: string;
  ticker: string;
  filing_quarter: string;
  report_date: string;
  pct_of_portfolio: number;
  conviction: string;
  action: string;
  change_pct: number;
  value_usd: number;
}

export interface IISignalsResponse {
  signals: IISignalSummary[];
  summary: Record<string, unknown>;
  meta: Record<string, unknown>;
  provenance: Provenance;
  total?: number;
}
