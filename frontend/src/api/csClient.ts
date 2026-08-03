// Close System API client (Phase 7)
const BASE = "/api";

export interface CSQCondition {
  name: string;
  met: boolean;
  value: string;
}

export interface CSAsset {
  ticker: string;
  name: string;
  sector: string;
  q_conditions_met: number;
  q_conditions_total: number;
  q_details: CSQCondition[];
  dimensions: {
    suitability: number;
    opportunity: number;
    regime: string;
    decay: string;
    data_confidence: number;
  };
  rule_pack: string[];
  instrument: string;
  liquidity: string;
  capital_lockup: string;
}

export interface CSRadarResponse {
  data_source: string;
  assets: CSAsset[];
}

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export function getCSRadar(): Promise<CSRadarResponse> {
  return fetchJSON<CSRadarResponse>("/cs-radar");
}
