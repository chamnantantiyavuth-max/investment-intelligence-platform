// Research blog API client (FD #62 — read-only report library)
export interface ReportMeta {
  slug: string
  title: string
  type: string
  subject: string
  date: string
  author: string
  status: string
  updated: string
  summary: string
  path: string
}

export interface ReportDetail extends ReportMeta {
  content: string
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

export async function getReports(): Promise<{ data_source: string; reports: ReportMeta[] }> {
  return getJSON<{ data_source: string; reports: ReportMeta[] }>("/reports");
}

export async function getReport(slug: string): Promise<{ data_source: string; report: ReportDetail }> {
  return getJSON<{ data_source: string; report: ReportDetail }>(`/reports/${slug}`);
}
