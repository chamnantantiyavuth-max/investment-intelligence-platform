// Audit API client (FD #86, WS-3 — UI-4 Decision Register / Audit Center)
export interface DecisionItem {
  num: number;
  title: string;
  preview: string;
  date: string;
}

export interface CommitEntry {
  hash: string;
  date: string;
  subject: string;
}

export interface CorrectionRecord {
  path: string;
  modified: number;
}

export interface GitLogResponse {
  data_source: string;
  commits: CommitEntry[];
  corrections: CorrectionRecord[];
}

export interface ModelRegistryResponse {
  data_source: string;
  current_version: string;
  versions: Record<string, string>;
}

const BASE = "/api";

async function getJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: "include" });
  if (!res.ok) {
    const err = new Error(`API ${res.status}: ${res.statusText}`) as Error & { status?: number };
    err.status = res.status;
    throw err;
  }
  return res.json();
}

export async function getDecisions(): Promise<{ data_source: string; decisions: DecisionItem[] }> {
  return getJSON<{ data_source: string; decisions: DecisionItem[] }>("/decisions");
}

export async function getGitLog(): Promise<GitLogResponse> {
  return getJSON<GitLogResponse>("/audit/git-log");
}

export async function getModelRegistry(): Promise<ModelRegistryResponse> {
  return getJSON<ModelRegistryResponse>("/audit/model-registry");
}
