// Org-workflow API client (FD #55 — read-only operational tracking endpoints)
export interface OrgHold {
  hold_id: string
  type: string
  issuer: string
  artifact: string
  scope: string
  triggering_condition: string
  evidence: string
  remediation_required: string
  owner: string
  review_condition: string
  partial_work_allowed: unknown
  status: string
  clear_record: { cleared_by: string; date: string; basis: string } | null
  override_record: unknown
  _path: string
}

export interface OrgCard {
  card_id: string
  title: string
  research_question: string
  decision_user: string
  workflow_column: string
  approval_status: string | null
  monitoring_status: string | null
  thesis_status: string | null
  research_state: string | null
  artifact_state: string | null
  domain: string
  principal_owner: string
  assistant_owner: string
  priority: string
  materiality: string
  created_at: string
  required_by: string
  expected_artifact: string | null
  evidence_standard: string
  data_status: string
  validation_status: string
  risk_status: string
  audit_status: string
  open_decision_slots: string[]
  dependencies: string[]
  blocked_reason: string | null
  next_action: string
  last_updated: string
  /** Radar-produced cards carry the scout's observation (RADAR-#### pattern). */
  radar_observation?: string
  radar_source?: string
  active_holds: OrgHold[]
  holds: OrgHold[]
  _path: string
}

export interface OrgQueue {
  data_source: string
  columns: string[]
  cards: OrgCard[]
  holds: OrgHold[]
}

export interface ResearchArtifact {
  artifact_id: string
  title: string
  artifact_type: string
  path: string
  modified: string
  research_id?: string
  research_version?: string
  research_status?: string
}

export interface ResearchArtifactDetail extends ResearchArtifact {
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

export async function getOrgQueue(): Promise<OrgQueue> {
  return getJSON<OrgQueue>("/org-queue");
}

export async function getOrgHolds(): Promise<{ data_source: string; holds: OrgHold[] }> {
  return getJSON<{ data_source: string; holds: OrgHold[] }>("/org-holds");
}

export async function getResearchArtifacts(): Promise<{ data_source: string; artifacts: ResearchArtifact[] }> {
  return getJSON<{ data_source: string; artifacts: ResearchArtifact[] }>("/research-artifacts");
}

export async function getResearchArtifact(artifactId: string): Promise<{ data_source: string; artifact: ResearchArtifactDetail }> {
  return getJSON<{ data_source: string; artifact: ResearchArtifactDetail }>(`/research-artifacts/${artifactId}`);
}
