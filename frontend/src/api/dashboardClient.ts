// Dashboard API client (FD #46 — per-component provenance, credentialed fetch)
import type { Provenance } from "@/types/am";

export interface ComponentProvenance {
  run_id: string | null;
  point_in_time: string | null;
  data_source: string | null;
  source?: string | null;
  state: "available" | "unavailable";
}

export interface DashboardSummary {
  total_themes: number;
  approved_themes: number;
  active_signals: number;
  queue_size: number;
  am_last_run: string | null;
  cs_radar_items: number;
  cs_qc_met: number;
  cs_regime: string;
  components: Record<"am" | "fo" | "ii" | "cs", ComponentProvenance>;
}

const BASE = "/api";

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${BASE}/dashboard/summary`, { credentials: "include" });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export type { Provenance };
