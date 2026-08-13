import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getOrgQueue, getResearchArtifacts, type OrgCard, type ResearchArtifact } from "@/api/orgClient";
import { getReports, type ReportMeta } from "@/api/reportClient";
import { linkArtifact, latestCardUpdate } from "@/lib/researchWorkflow";
import { Skeleton } from "@/components/ui/skeleton";

// Maple-Story-style chibi sprites (generated via imagegen, chroma-keyed cutouts)
import cosSprite from "@/assets/agents/org-cos.png";
import icSecretarySprite from "@/assets/agents/org-ic-secretary.png";
import commoditySprite from "@/assets/agents/org-commodity-analyst.png";
import macroSprite from "@/assets/agents/org-macro-strategist.png";
import equitySprite from "@/assets/agents/org-equity-analyst.png";
import optionsSprite from "@/assets/agents/org-options-strategist.png";
import croSprite from "@/assets/agents/org-cro.png";
import quantSprite from "@/assets/agents/org-quant-validator.png";
import dataStewardSprite from "@/assets/agents/org-data-steward.png";
import auditorSprite from "@/assets/agents/org-auditor.png";
import radarScoutSprite from "@/assets/agents/org-radar-scout.png";

/**
 * Org Office — Virtual Office (Maple Story style sprites), drill-down layout.
 * Compact by default: sprite + role name only → all 11 roles fit one page.
 * Click a character to expand its desk (cards, status, recent output).
 * Data: /org-queue + /research-artifacts + /reports (read-only, real).
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
  sprite: string;
  authorMatch: RegExp;
}

const DESKS: RoleDesk[] = [
  { code: "org-cos", name: "Chief of Staff", duty: "Triage, routing, capacity", sprite: cosSprite, authorMatch: /Chief of Staff/i },
  { code: "org-ic-secretary", name: "IC Secretary", duty: "Records, synthesis, founder pack", sprite: icSecretarySprite, authorMatch: /^IC Secretary/i },
  { code: "org-commodity-analyst", name: "Commodity Analyst", duty: "Products & physical markets", sprite: commoditySprite, authorMatch: /Commodity/i },
  { code: "org-macro-strategist", name: "Macro Strategist", duty: "Regime & transmission", sprite: macroSprite, authorMatch: /Macro Strategy/i },
  { code: "org-equity-analyst", name: "Equity Alpha Analyst", duty: "Companies, moats, earnings", sprite: equitySprite, authorMatch: /Equity/i },
  { code: "org-options-strategist", name: "Options Strategist", duty: "Structure & volatility", sprite: optionsSprite, authorMatch: /Options/i },
  { code: "org-cro", name: "Chief Risk Officer", duty: "Independent challenge", sprite: croSprite, authorMatch: /Chief Risk Officer|CRO|Chief Research Risk Officer/i },
  { code: "org-quant-validator", name: "Quant Validator", duty: "Reproduction & validation", sprite: quantSprite, authorMatch: /Quant/i },
  { code: "org-data-steward", name: "Data Steward", duty: "Provenance & freshness", sprite: dataStewardSprite, authorMatch: /Data Steward/i },
  { code: "org-auditor", name: "Internal Auditor", duty: "Evidence integrity", sprite: auditorSprite, authorMatch: /Internal Auditor/i },
  { code: "org-radar-scout", name: "Radar Scout", duty: "Discovery & monitoring", sprite: radarScoutSprite, authorMatch: /Radar Scout|Radar/i },
];

// Hermes-native work-state buckets (C6, 2026-08-13): awaiting = human/review
// gates (blocked, review, triage); inflight = queued or actively running
// (todo, scheduled, ready, running). Legacy 11-column names retired.
const AWAITING_COLUMNS = new Set(["Blocked", "Review", "Triage"]);
const INFLIGHT_COLUMNS = new Set(["Todo", "Scheduled", "Ready", "Running"]);

function deskOfOwner(owner: string | null | undefined): DeskCode | null {
  if (!owner) return null;
  for (const d of DESKS) {
    if (owner.includes(d.code) || owner.includes(d.name)) return d.code;
  }
  return null;
}

function loadLabelOf(cards: OrgCard[], radarCards: OrgCard[] | undefined): string {
  const inflight = cards.filter((c) => INFLIGHT_COLUMNS.has(c.workflow_column));
  const awaiting = cards.filter((c) => AWAITING_COLUMNS.has(c.workflow_column));
  const active = inflight.length + awaiting.length;
  const hasProduced = (radarCards?.length ?? 0) > 0;
  if (hasProduced) return "produced";
  if (active > 0) return "active";
  if (cards.length > 0) return "wip ok";
  return "standby";
}

function loadChipClass(label: string): string {
  switch (label) {
    case "active":
      return "bg-amber-500/10 text-warning";
    case "wip ok":
      return "bg-emerald-500/10 text-positive";
    case "produced":
      return "bg-primary/10 text-primary";
    default:
      return "bg-bg-panel text-ink-3";
  }
}

function DeskHeader({
  desk,
  expanded,
  count,
  label,
  onToggle,
}: {
  desk: RoleDesk;
  expanded: boolean;
  count: number;
  label: string;
  onToggle: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-expanded={expanded}
      aria-controls={`desk-${desk.code}`}
      className="group flex w-full flex-col items-center gap-1 rounded-md px-2 py-3 text-center focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
    >
      <div className="relative">
        <img
          src={desk.sprite}
          alt={desk.name}
          className="h-[86px] w-auto max-w-[84px] object-contain drop-shadow-sm transition-transform duration-200 group-hover:scale-[1.04]"
          draggable={false}
        />
        <div aria-hidden="true" className="absolute bottom-0 left-1/2 h-2 w-14 -translate-x-1/2 rounded-[50%] bg-ink/15" />
        {count > 0 && (
          <span className="absolute -right-2 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-foreground px-1 font-mono text-[10px] font-semibold text-background">
            {count}
          </span>
        )}
      </div>
      <span className="font-display text-[13px] font-bold leading-tight tracking-tight">{desk.name}</span>
      <span className={`inline-flex items-center gap-1 rounded-sm px-1.5 py-0.5 font-mono text-[9px] uppercase tracking-[0.08em] ${loadChipClass(label)}`}>
        {label}
        <svg
          viewBox="0 0 12 12"
          className={`h-2.5 w-2.5 transition-transform duration-200 ${expanded ? "rotate-180" : ""}`}
          aria-hidden="true"
        >
          <path d="M2 4 L6 8 L10 4" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </span>
    </button>
  );
}

function DeskDetail({
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
  const publishedCards = cards.filter((c) => c.workflow_column === "Done");
  const publishedReports = reports
    .filter((r) => r.status === "published" && desk.authorMatch.test(r.author))
    .slice(0, 4);

  return (
    <div id={`desk-${desk.code}`} className="border-t border-rule px-3 pb-3 pt-2">
      <p className="text-[10px] text-ink-3">{desk.duty}</p>

      {cards.length === 0 && !(radarCards && radarCards.length > 0) ? (
        <p className="mt-1.5 text-[11px] leading-relaxed text-ink-3">
          No active mandate — work begins on demand.
        </p>
      ) : (
        <div className="mt-1.5 flex flex-col">
          {cards.map((c) => {
            const target = linkArtifact(c, artifacts);
            const body = (
              <div className="border-b border-rule py-1.5 last:border-b-0">
                <p className="text-[11.5px] font-medium leading-snug text-foreground">{c.title}</p>
                <p className="mt-0.5 flex flex-wrap items-baseline gap-x-2 text-[9px]">
                  <span className="font-mono uppercase tracking-[0.07em] text-primary">{c.workflow_column}</span>
                  <span className="font-mono text-ink-3">{c.materiality}</span>
                  <span className="text-ink-2">{c.priority}</span>
                  <span className="font-mono text-ink-3">{c.last_updated}</span>
                </p>
                {c.active_holds.length > 0 && (
                  <p className="mt-0.5 text-[9px] font-semibold uppercase tracking-[0.07em] text-warning">
                    {c.active_holds.map((h) => h.hold_id).join(" · ")}
                  </p>
                )}
              </div>
            );
            return target ? (
              <Link key={c.card_id} to={`/research/${target.artifact_id}`} className="focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">
                {body}
              </Link>
            ) : (
              <div key={c.card_id}>{body}</div>
            );
          })}
        </div>
      )}

      {(publishedCards.length > 0 || publishedReports.length > 0 || (radarCards && radarCards.length > 0)) && (
        <div className="mt-2 border-t border-rule pt-2">
          <p className="text-[9px] font-semibold uppercase tracking-[0.12em] text-ink-3">Recent output</p>
          <div className="mt-1 flex flex-col">
            {radarCards &&
              radarCards.map((c) => (
                <p key={c.card_id} className="py-0.5 text-[11px] text-ink-2">
                  <span className="mr-1.5 font-mono text-[9px] uppercase text-primary">{c.card_id}</span>
                  {c.title}
                </p>
              ))}
            {publishedReports.map((r) => (
              <Link key={r.slug} to={`/library/${r.slug}`} className="py-0.5 text-[11px] text-foreground hover:text-primary">
                <span className="mr-1.5 font-mono text-[9px] uppercase text-primary">{r.type}</span>
                {r.title}
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function OrgOfficePage() {
  const [expanded, setExpanded] = useState<DeskCode | null>(null);
  const queue = useQuery({ queryKey: ["org-queue"], queryFn: getOrgQueue, staleTime: 60_000 });
  const registry = useQuery({ queryKey: ["research-artifacts"], queryFn: getResearchArtifacts, staleTime: 60_000 });
  const reports = useQuery({ queryKey: ["reports"], queryFn: getReports, staleTime: 60_000 });

  const cards = useMemo(() => queue.data?.cards ?? [], [queue.data]);
  const artifacts = useMemo(() => registry.data?.artifacts ?? [], [registry.data]);
  const reportList = useMemo(() => reports.data?.reports ?? [], [reports.data]);
  const holds = useMemo(() => queue.data?.holds ?? [], [queue.data]);

  const radarProduced = useMemo(() => cards.filter((c) => Boolean(c.radar_observation)), [cards]);

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
  const publishedReports = useMemo(() => reportList.filter((r) => r.status === "published").length, [reportList]);
  const activeHolds = useMemo(() => holds.filter((h) => String(h.status || "").toUpperCase() !== "CLEARED").length, [holds]);
  const blocked = useMemo(() => cards.filter((c) => c.blocked_reason).length, [cards]);
  const desksActive = useMemo(() => [...byDesk.values()].filter((cs) => cs.length > 0).length, [byDesk]);

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
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Org office · virtual office</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">The research floor</h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">
          Org workflow · operational tracking · latest card update {latest}
        </p>
        <p className="mt-1 max-w-2xl text-xs text-ink-2">
          Every role in one room. Click a character to see what they are working on — read-only, cards move only
          through the research workflow, never from this screen.
        </p>
      </div>

      {/* Org pulse — display derivations from admitted data, never scores */}
      <div className="grid grid-cols-2 border-b border-t border-rule md:grid-cols-6">
        {[
          { label: "Cards in flight", value: String(inflight), note: "todo → running" },
          { label: "Awaiting you", value: String(awaiting), note: "blocked · review · triage" },
          { label: "Published notes", value: String(publishedReports), note: "library · + companions" },
          { label: "Active holds", value: String(activeHolds), note: "none is silent" },
          { label: "Desks active", value: `${desksActive}/11`, note: "roles holding cards" },
          {
            label: "Org pulse",
            value: pulseHealthy ? "Healthy" : "Attention",
            note: pulseHealthy ? "no holds · no blockers" : `${activeHolds} holds · ${blocked} blocked`,
          },
        ].map((cell, i) => (
          <div key={cell.label} className={i > 0 ? "border-l border-rule px-4 py-3" : "px-4 py-3"}>
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

      {/* Role desks — compact by default, click to drill down */}
      <div className="grid grid-cols-2 border-t border-l border-rule sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6">
        {DESKS.map((d) => {
          const deskCards = byDesk.get(d.code) ?? [];
          const label = loadLabelOf(deskCards, d.code === "org-radar-scout" ? radarProduced : undefined);
          const isOpen = expanded === d.code;
          return (
            <div key={d.code} className={`border-b border-r border-rule bg-background ${isOpen ? "bg-bg-panel/40" : ""}`}>
              <DeskHeader
                desk={d}
                expanded={isOpen}
                count={deskCards.length}
                label={label}
                onToggle={() => setExpanded(isOpen ? null : d.code)}
              />
              {isOpen && (
                <DeskDetail
                  desk={d}
                  cards={deskCards}
                  artifacts={artifacts}
                  reports={reportList}
                  radarCards={d.code === "org-radar-scout" ? radarProduced : undefined}
                />
              )}
            </div>
          );
        })}
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
