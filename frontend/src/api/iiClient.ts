// Institutional Intelligence API client (NEW surface, FD #46 — credentialed fetch)
import type { IISignalsResponse } from "@/types/ii";

const BASE = "/api";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: "include" });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export function getIISignals(limit = 0, offset = 0): Promise<IISignalsResponse> {
  const q = limit > 0 ? `?limit=${limit}&offset=${offset}` : "";
  return fetchJSON<IISignalsResponse>(`/ii-signals${q}`);
}
