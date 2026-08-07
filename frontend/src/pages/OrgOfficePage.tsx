import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getOrgQueue, getResearchArtifacts, type OrgCard, type ResearchArtifact } from "@/api/orgClient";
import { getReports, type ReportMeta } from "@/api/reportClient";
import { linkArtifact, latestCardUpdate } from "@/lib/researchWorkflow";
import { Skeleton } from "@/components/ui/skeleton";

/**
 * Org Office — War Room (FD #75-adjacent; role-centric view, approved mockup
 * design/mockups/org-office-war-room.html, Founder pick A).
 *
 * Read-only role desks over the SAME D1 endpoints as /kanban + /research:
 *   - /org-queue          → cards grouped by principal_owner → 11 role desks
 *   - /research-artifacts → card→artifact links (linkArtifact)
 *   - /reports            → published notes per role (author match, display only)
 *
 * Operational tracking only — card state never equals domain state. No writes,
 * no drag, no movement rights (KANBAN-CONTRACT §6). Counts are display
 * derivations, never scores (Constitution §10).
 */

type DeskCode =
  | "org-cos"
  | "org-ic-secretary"
  | "org-commodity-analyst"
  | "org-macro-strategist"
  | "org-equity-analyst"
  | "org-options-strategist"
  | "org-cro"
  | "org-quant-validator"
  | "org-data-steward"
  | "org-auditor"
  | "org-radar-scout";

interface RoleDesk {
  code: DeskCode;
  name: string;
  duty: string;
  /** author-keyword → desk (for published-report grouping; display only). */
  authorMatch: RegExp;
}

// ROLE-REGISTRY-v0.1 row 1–11 — canonical 11 principals (display names in user language).
const DESKS: RoleDesk[] = [
  { code: "org-cos", name: "Chief of Staff", duty: "Triage, routing, capacity", authorMatch: /Chief of Staff/i },
  { code: "org-ic-secretary", name: "IC Secretary", duty: "Records, synthesis, founder pack", authorMatch: /^IC Secretary/i },
  { code: "org-commodity-analyst", name: "Commodity Analyst", duty: "Products & physical markets", authorMatch: /Commodity/i },
  { code: "org-macro-strategist", name: "Macro Strategist", duty: "Regime & transmission", authorMatch: /Macro Strategy/i },
  { code: "org-equity-analyst", name: "Equity Alpha Analyst", duty: "Companies, moats, earnings", authorMatch: /Equity/i },
  { code: "org-options-strategist", name: "Options Strategist", duty: "Structure & volatility", authorMatch: /Options/i },
  { code: "org-cro", name: "Chief Risk Officer", duty: "Independent challenge", authorMatch: /Chief Risk Officer|CRO|Chief Research Risk Officer/i },
  { code: "org-quant-validator", name: "Quant Validator", duty: "Reproduction & validation", authorMatch: /Quant/i },
  { code: "org-data-steward", name: "Data Steward", duty: "Provenance & freshness", authorMatch: /Data Steward/i },
  { code: "org-auditor", name: "Internal Auditor", duty: "Evidence integrity", authorMatch: /Internal Auditor/i },
  { code: "org-radar-scout", name: "Radar Scout", duty: "Discovery & monitoring", authorMatch: /Radar Scout|Radar/i },
];

// Terminal columns (a card there is done, not "active work").
const AWAITING_COLUMNS = new Set(["Founder Review", "Blocked"]);
const INFLIGHT_COLUMNS = new Set([
  "Inbox", "Triage", "Scoped", "Data Ready", "In Research", "Cross-Review", "Validation",
]);

function deskOfOwner(owner: string | null | undefined): DeskCode | null {
  if (!owner) return null;
  for (const d of DESKS) {
    if (owner.includes(d.code) || owner.includes(d.name)) return d.code;
  }
  return null;
}

function RoleDeskPanel({
  desk,
  cards,
  artifacts,
  reports,
  radarCards,
}: {
  desk: RoleDesk;
  cards: OrgCard[];
  artifacts: ResearchArtifact[];
  reports: ReportMeta[];
  radarCards?: OrgCard[];
}) {
  const inflight = cards.filter((c) => INFLIGHT_COLUMNS.has(c.workflow_column));
  const awaiting = cards.filter((c) => AWAITING_COLUMNS.has(c.workflow_column));
  const publishedCards = cards.filter((c) => c.workflow_column === "Published");
  const publishedReports = reports
    .filter((r) => r.status === "published" && desk.authorMatch.test(r.author))
    .slice(0, 4);

  const active = inflight.length + awaiting.length;
  const hasProduced = (radarCards?.length ?? 0) > 0;
  const loadLabel =
    desk.code === "org-radar-scout" && hasProduced
      ? "produced"
      : active > 0
        ? "active"
        : cards.length > 0
          ? "wip ok"
          : "standby";

  return (
    <div className="border-b border-r border-rule bg-background p-4">
      <div className="flex items-baseline justify-between gap-3 border-b border-rule pb-2">
        <div>
          <p className="font-display text-[15px] font-bold leading-tight tracking-tight">{desk.name}</p>
          <p className="font-mono text-[10px] uppercase tracking-[0.08em] text-ink-3">{desk.code}</p>
        </div>
        <p className="font-mono text-[10px] text-ink-3">
          <span className="text-[12px] font-semibold text-primary">{cards.length}</span> cards
        </p>
      </div>

      <p className="mt-2 flex flex-wrap items-center gap-2">
        <span
          className={
            loadLabel === "active"
              ? "rounded-sm bg-amber-500/10 px-1.5 py-0.5 font-mono text-[9.5px] uppercase tracking-[0.08em] text-warning"
              : loadLabel === "wip ok"
                ? "rounded-sm bg-emerald-500/10 px-1.5 py-0.5 font-mono text-[9.5px] uppercase tracking-[0.08em] text-positive"
                : loadLabel === "produced"
                  ? "rounded-sm bg-primary/10 px-1.5 py-0.5 font-mono text-[9.5px] uppercase tracking-[0.08em] text-primary"
                  : "rounded-sm bg-bg-panel px-1.5 py-0.5 font-mono text-[9.5px] uppercase tracking-[0.08em] text-ink-3"
          }
        >
          {loadLabel}
        </span>
        <span className="text-[10px] text-ink-3">{desk.duty}</span>
      </p>

      {cards.length === 0 ? (
        <p className="mt-3 text-[11.5px] leading-relaxed text-ink-3">
          No active mandate.
          <span className="mt-0.5 block text-[10.5px] text-ink-2">{desk.duty} work begins on demand.</span>
        </p>
      ) : (
        <div className="mt-2 flex flex-col">
          {cards.map((c) => {
            const target = linkArtifact(c, artifacts);
            const body = (
              <div className="border-b border-rule py-1.5 last:border-b-0">
                <p className="text-[12px] font-medium leading-snug text-foreground">{c.title}</p>
                <p className="mt-0.5 flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-[9.5px]">
                  <span className="font-mono uppercase tracking-[0.08em] text-primary">{c.workflow_column}</span>
                  <span className="font-mono text-ink-3">{c.materiality}</span>
                  <span className="text-ink-2">{c.priority}</span>
                  <span className="font-mono text-ink-3">{c.last_updated}</span>
                </p>
                {c.active_holds.length > 0 && (
                  <p className="mt-0.5 text-[9.5px] font-semibold uppercase tracking-[0.08em] text-warning">
                    {c.active_holds.map((h) => h.hold_id).join(" · ")}
                  </p>
                )}
              </div>
            );
            return target ? (
              <Link
                key={c.card_id}
                to={`/research/${target.artifact_id}`}
                className="focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
              >
                {body}
              </Link>
            ) : (
              <div key={c.card_id}>{body}</div>
            );
          })}
        </div>
      )}

      {(publishedCards.length > 0 || publishedReports.length > 0 || (radarCards && radarCards.length > 0)) && (
        <div className="mt-3 border-t border-rule pt-2">
          <p className="text-[9.5px] font-semibold uppercase tracking-[0.12em] text-ink-3">Recent output</p>
          <div className="mt-1 flex flex-col">
            {radarCards &&
              radarCards.map((c) => (
                <p key={c.card_id} className="py-0.5 text-[11.5px] text-ink-2">
                  <span className="mr-1.5 font-mono text-[9.5px] uppercase text-primary">{c.card_id}</span>
                  {c.title}
                </p>
              ))}
            {publishedReports.map((r) => (
              <Link
                key={r.slug}
                to={`/library/${r.slug}`}
                className="py-0.5 text-[11.5px] text-foreground hover:text-primary"
              >
                <span className="mr-1.5 font-mono text-[9.5px] uppercase text-primary">{r.type}</span>
                {r.title}
              </Link>
            ))}
            {publishedCards.map((c) => (
              <p key={c.card_id} className="py-0.5 text-[11.5px] text-ink-2">
                <span className="mr-1.5 font-mono text-[9.5px] uppercase text-ink-3">{c.card_id}</span>
                {c.title}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function OrgOfficePage() {
  const queue = useQuery({ queryKey: ["org-queue"], queryFn: getOrgQueue, staleTime: 60_000 });
  const registry = useQuery({ queryKey: ["research-artifacts"], queryFn: getResearchArtifacts, staleTime: 60_000 });
  const reports = useQuery({ queryKey: ["reports"], queryFn: getReports, staleTime: 60_000 });

  const cards = useMemo(() => queue.data?.cards ?? [], [queue.data]);
  const artifacts = useMemo(() => registry.data?.artifacts ?? [], [registry.data]);
  const reportList = useMemo(() => reports.data?.reports ?? [], [reports.data]);
  const holds = useMemo(() => queue.data?.holds ?? [], [queue.data]);

  const radarProduced = useMemo(
    () => cards.filter((c) => Boolean(c.radar_observation)),
    [cards]
  );

  const byDesk = useMemo(() => {
    const map = new Map<DeskCode, OrgCard[]>();
    for (const d of DESKS) map.set(d.code, []);
    for (const c of cards) {
      const code = deskOfOwner(c.principal_owner);
      if (code) map.get(code)!.push(c);
    }
    return map;
  }, [cards]);

  const inflight = useMemo(() => cards.filter((c) => INFLIGHT_COLUMNS.has(c.workflow_column)).length, [cards]);
  const awaiting = useMemo(() => cards.filter((c) => AWAITING_COLUMNS.has(c.workflow_column)).length, [cards]);
  const publishedReports = useMemo(
    () => reportList.filter((r) => r.status === "published").length,
    [reportList]
  );
  const activeHolds = useMemo(
    () => holds.filter((h) => String(h.status || "").toUpperCase() !== "CLEARED").length,
    [holds]
  );
  const blocked = useMemo(() => cards.filter((c) => c.blocked_reason).length, [cards]);
  const desksActive = useMemo(
    () => [...byDesk.values()].filter((cs) => cs.length > 0).length,
    [byDesk]
  );

  const pulseHealthy = activeHolds === 0 && blocked === 0;

  if (queue.isLoading || registry.isLoading || reports.isLoading)
    return <Skeleton className="h-64 w-full" />;
  if (queue.isError || registry.isError || reports.isError)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Org Office unavailable — API error.</p>
        <p className="mt-1 text-xs text-ink-2">What failed: the org-workflow or report endpoint.</p>
        <button
          type="button"
          onClick={() => {
            queue.refetch();
            registry.refetch();
            reports.refetch();
          }}
          className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary"
        >
          Retry →
        </button>
      </div>
    );

  const latest = latestCardUpdate(cards);

  return (
    <div className="space-y-6">
      <div className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Org office · war room</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">The research organization, at a glance</h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">
          Org workflow · operational tracking · latest card update {latest}
        </p>
        <p className="mt-1 max-w-2xl text-xs text-ink-2">
          Who is working on what, where each item stands, and what needs your attention — every role in one room.
          Read-only: cards move only through the research workflow, never from this screen.
        </p>
      </div>

      {/* Org pulse — display derivations from admitted data, never scores */}
      <div className="grid grid-cols-2 border-b border-t border-rule md:grid-cols-6">
        {[
          { label: "Cards in flight", value: String(inflight), note: "inbox → validation" },
          { label: "Awaiting you", value: String(awaiting), note: "founder review · blocked" },
          { label: "Published notes", value: String(publishedReports), note: "library · + companions" },
          { label: "Active holds", value: String(activeHolds), note: "none is silent" },
          { label: "Desks active", value: `${desksActive}/11`, note: "roles holding cards" },
          {
            label: "Org pulse",
            value: pulseHealthy ? "Healthy" : "Attention",
            note: pulseHealthy ? "no holds · no blockers" : `${activeHolds} holds · ${blocked} blocked`,
          },
        ].map((cell, i) => (
          <div
            key={cell.label}
            className={
              i > 0
                ? "border-l border-rule px-4 py-3 first:border-l-0 md:border-l md:px-4"
                : "px-4 py-3 md:px-4"
            }
          >
            <p className="text-[9.5px] font-semibold uppercase tracking-[0.12em] text-ink-3">{cell.label}</p>
            <p
              className={
                cell.label === "Org pulse"
                  ? pulseHealthy
                    ? "mt-1 font-mono text-[17px] leading-none text-positive"
                    : "mt-1 font-mono text-[17px] leading-none text-warning"
                  : "mt-1 font-mono text-[17px] leading-none text-foreground"
              }
            >
              {cell.value}
            </p>
            <p className="mt-1 text-[10px] text-ink-2">{cell.note}</p>
          </div>
        ))}
      </div>

      {/* Role desks — 3-col hairline grid (mockup-approved) */}
      <div className="grid grid-cols-1 border-t border-l border-rule md:grid-cols-2 lg:grid-cols-3">
        {DESKS.map((d) => (
          <RoleDeskPanel
            key={d.code}
            desk={d}
            cards={byDesk.get(d.code) ?? []}
            artifacts={artifacts}
            reports={reportList}
            radarCards={d.code === "org-radar-scout" ? radarProduced : undefined}
          />
        ))}
      </div>

      {/* Holds — active only, honest empty */}
      <div className="border-b border-rule pb-2">
        <p className="text-[9.5px] font-semibold uppercase tracking-[0.12em] text-ink-3">Holds &amp; exceptions</p>
        {activeHolds === 0 ? (
          <p className="mt-1 text-xs text-ink-2">No active holds.</p>
        ) : (
          <div className="mt-1 flex flex-wrap gap-2">
            {holds
              .filter((h) => String(h.status || "").toUpperCase() !== "CLEARED")
              .map((h) => (
                <span
                  key={h.hold_id}
                  className="rounded-sm bg-rose-500/10 px-2 py-1 font-mono text-[10px] uppercase tracking-[0.06em] text-negative"
                >
                  {h.hold_id} · {h.type}
                </span>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
