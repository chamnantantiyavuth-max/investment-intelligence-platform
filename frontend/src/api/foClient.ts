// Fundamental & Opportunity API client (FD #46 — credentialed fetch)
import type { ResearchPackageSummary, ResearchPackageDetail } from "@/types/fo";

const BASE = "/api";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: "include" });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

export function getFOQueue(): Promise<ResearchPackageSummary[]> {
  return fetchJSON<ResearchPackageSummary[]>("/fo-queue");
}

export function getFOPackage(id: string): Promise<ResearchPackageDetail> {
  return fetchJSON<ResearchPackageDetail>(`/fo-package/${id}`);
}

export function getFOCheapQuality(): Promise<ResearchPackageSummary[]> {
  return fetchJSON<ResearchPackageSummary[]>("/fo-cheap-quality");
}
