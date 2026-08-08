// Alpha Momentum API client (FD #46 — credentialed fetch, real artifact-backed contracts)
import type { AMQueueResponse, ThemeWithCandidates } from "@/types/am";

const BASE = "/api";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: "include" });
  if (!res.ok) {
    if (res.status === 404) throw new Error("NOT_FOUND");
    if (res.status === 401) throw new Error("UNAUTHORIZED");
    if (res.status === 503) throw new Error("UNAVAILABLE");
    throw new Error(`API ${res.status}: ${res.statusText}`);
  }
  return res.json();
}

export async function getAMQueue(): Promise<AMQueueResponse> {
  return fetchJSON<AMQueueResponse>("/am-queue");
}

export function getAMTheme(id: string): Promise<ThemeWithCandidates> {
  return fetchJSON<ThemeWithCandidates>(`/am-theme/${id}`);
}
