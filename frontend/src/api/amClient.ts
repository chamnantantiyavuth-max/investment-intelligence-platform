// Alpha Momentum API client (Phase 7)
import type { ThemeSummary } from "@/types/am";

const BASE = "/api";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    if (res.status === 404) throw new Error("NOT_FOUND");
    throw new Error(`API ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

export async function getAMQueue(): Promise<ThemeSummary[]> {
  const data = await fetchJSON<{ themes: ThemeSummary[] }>("/am-queue");
  return data.themes;
}

export function getAMTheme(id: string): Promise<ThemeSummary> {
  return fetchJSON<ThemeSummary>(`/am-theme/${id}`);
}
