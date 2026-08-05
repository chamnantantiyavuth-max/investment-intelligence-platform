// Close System API client — v0.1 pipeline artifact surface (FD #57)
const BASE = "/api";

export interface CSLayer {
  signal: "supporting" | "neutral" | "contradicting" | string;
  note: string;
}

export interface CSAsset {
  id: string;
  ticker: string;
  name: string;
  category: string;
  currency: string;
  current_price: number;
  eligible: boolean;
  status: string;
  p1_pass: boolean;
  p2_pass: boolean;
  p3_pass: boolean;
  p1_rationale: string;
  discount_type: string;
  discount_depth: string;
  target_discount_entry: string;
  discount_detail: Record<string, unknown>;
  demand_type: string;
  demand_detail: Record<string, unknown>;
  layers: Record<string, CSLayer>;
  layers_aligned: number;
  layers_contradicting: number;
  conviction: string;
  key_risks: string[];
  recommendation: string;
  recommendation_rationale: string;
}

export interface CSRadarResponse {
  data_source: string;
  assets: CSAsset[];
}

export interface CSProductResponse {
  data_source: string;
  asset: CSAsset;
}

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: "include" });
  if (!res.ok) {
    const err = new Error(`API ${res.status}: ${res.statusText}`) as Error & { status?: number };
    err.status = res.status;
    throw err;
  }
  return res.json();
}

export function getCSRadar(): Promise<CSRadarResponse> {
  return fetchJSON<CSRadarResponse>("/cs-radar");
}

export function getCSProduct(productId: string): Promise<CSProductResponse> {
  return fetchJSON<CSProductResponse>(`/cs-radar/${productId}`);
}
