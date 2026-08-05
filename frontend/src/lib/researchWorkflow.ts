// Research-workflow presentation helpers (FD #55 — display derivations only,
// never domain state; KANBAN-CONTRACT §1)
import type { OrgCard, ResearchArtifact } from "@/api/orgClient";

// View ↔ kanban column mapping (KANBAN-CONTRACT §2) — single source.
export const VIEW_COLUMNS: Record<string, string[]> = {
  Inbox: ["Inbox", "Triage"],
  "Active Research": ["Scoped", "Data Ready", "In Research"],
  "Review Queue": ["Cross-Review", "Validation"],
  "Founder Review": ["Founder Review", "Blocked"],
  Archive: ["Monitoring", "Closed"],
};

export const VIEW_ORDER = ["Inbox", "Active Research", "Review Queue", "Founder Review", "Archive"];

export function cardsInView(cards: OrgCard[], view: string): OrgCard[] {
  const cols = VIEW_COLUMNS[view] ?? [];
  return cards.filter((c) => cols.includes(c.workflow_column));
}

export function isHeldOrBlocked(c: OrgCard): boolean {
  return c.active_holds.length > 0 || Boolean(c.blocked_reason);
}

// Readiness is a display derivation from admitted statuses — never a score.
export function readinessOf(c: OrgCard): "held" | "ready" | "in-progress" {
  if (c.active_holds.length > 0) return "held";
  if (c.data_status === "DATA HOLD" || c.validation_status === "VALIDATION HOLD" || c.risk_status === "RISK HOLD") return "held";
  const pending = [c.data_status, c.validation_status, c.risk_status].some(
    (s) => /PENDING|NOT (ASSESSED|REVIEWED|REQUIRED)/i.test(s ?? "")
  );
  return pending ? "in-progress" : "ready";
}

// Card → artifact link by expected_artifact path (registry match on path or basename).
// Normalizes annotated values (e.g. "evidence/organization/pilot/PILOT-REPORT.md (pass/fail)")
// by extracting the .md path before matching.
const MD_PATH = /([\w/.-]+\.md)/;

export function linkArtifact(card: OrgCard, artifacts: ResearchArtifact[]): ResearchArtifact | undefined {
  if (!card.expected_artifact) return undefined;
  const m = card.expected_artifact.replace(/\\/g, "/").match(MD_PATH);
  const needle = m ? m[1] : card.expected_artifact;
  const base = needle.split("/").pop();
  return artifacts.find(
    (a) => a.path === needle || a.path.endsWith(`/${base}`) || a.artifact_id.endsWith(`/${base}`)
  );
}

// Latest admitted card update — an explicit label, never client wall-clock.
export function latestCardUpdate(cards: OrgCard[]): string {
  const dates = cards.map((c) => c.last_updated).filter(Boolean).sort();
  return dates.length > 0 ? dates[dates.length - 1] : "unknown";
}

// Artifact family: same root (ciw-pilot-msft / org-pilot), then slice-2 vs
// first-slice for CIW files. Used for related artifacts + challenge/records joins.
export function familyOf(artifactId: string, all: ResearchArtifact[]): ResearchArtifact[] {
  const root = artifactId.split("/")[0];
  const slice2 = artifactId.includes("-2");
  return all.filter(
    (a) =>
      a.artifact_id !== artifactId &&
      a.artifact_id.startsWith(`${root}/`) &&
      a.artifact_id.includes("-2") === slice2
  );
}
