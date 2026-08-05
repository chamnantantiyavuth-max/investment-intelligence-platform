import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getOrgQueue, getResearchArtifacts, type OrgCard } from "@/api/orgClient";
import { ResearchArtifactRow } from "@/components/ResearchArtifactRow";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { VIEW_ORDER, cardsInView, isHeldOrBlocked, latestCardUpdate } from "@/lib/researchWorkflow";

const VIEW_EMPTY: Record<string, [string, string]> = {
  Inbox: ["No new research requests", "Intake happens via template 01 / the CRR contract — cards land here from Triage."],
  "Active Research": ["No active research", "Scoped / Data Ready / In Research cards appear here while a principal works them."],
  "Review Queue": ["Nothing in review", "Cards enter Cross-Review or Validation when independent review starts."],
  "Founder Review": ["Nothing awaits your decision", "The IC Secretary moves a complete packet here; blocked cards also surface."],
  Archive: ["Archive is empty", "Closed, rejected, superseded, or archived cards land here."],
};

export default function ResearchDeskPage() {
  const [view, setView] = useState(VIEW_ORDER[0]);
  const [domain, setDomain] = useState("all");
  const [heldOnly, setHeldOnly] = useState(false);
  const [sort, setSort] = useState<"materiality" | "recent">("materiality");

  const queue = useQuery({ queryKey: ["org-queue"], queryFn: getOrgQueue, staleTime: 60_000 });
  const registry = useQuery({ queryKey: ["research-artifacts"], queryFn: getResearchArtifacts, staleTime: 60_000 });

  const cards = useMemo(() => queue.data?.cards ?? [], [queue.data]);
  const artifacts = useMemo(() => registry.data?.artifacts ?? [], [registry.data]);

  const domains = useMemo(() => Array.from(new Set(cards.map((c) => c.domain))).sort(), [cards]);

  const viewCards = useMemo(() => {
    let list = cardsInView(cards, view);
    if (domain !== "all") list = list.filter((c) => c.domain === domain);
    if (heldOnly) list = list.filter(isHeldOrBlocked);
    list = [...list];
    list.sort((a, b) => {
      if (sort === "recent") return b.last_updated.localeCompare(a.last_updated);
      const m = (x: OrgCard) => Number(x.materiality?.replace(/\D/g, "") || 0);
      return m(b) - m(a) || b.last_updated.localeCompare(a.last_updated);
    });
    return list;
  }, [cards, view, domain, heldOnly, sort]);

  if (queue.isLoading || registry.isLoading)
    return <Skeleton className="h-64 w-full" />;
  if (queue.isError || registry.isError)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Research Desk unavailable — API error.</p>
        <p className="mt-1 text-xs text-ink-2">What failed: the org-workflow queue or artifact registry endpoint.</p>
        <button type="button" onClick={() => { queue.refetch(); registry.refetch(); }} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );

  const counts = Object.fromEntries(VIEW_ORDER.map((v) => [v, cardsInView(cards, v).length]));
  const latest = latestCardUpdate(cards);

  return (
    <div className="space-y-6">
      <div className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Research workflow</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">Research Desk</h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">
          {queue.data?.data_source ?? "org_workflow_kanban"} · operational tracking · latest card update {latest}
        </p>
        <p className="mt-1 max-w-2xl text-xs text-ink-2">
          Operational tracking only — card state never equals domain state (KANBAN-CONTRACT §1).
        </p>
      </div>

      <div className="flex flex-wrap gap-1 border-b border-rule pb-3" role="tablist" aria-label="Research views">
        {VIEW_ORDER.map((v) => (
          <button
            key={v}
            type="button"
            role="tab"
            aria-selected={view === v}
            onClick={() => setView(v)}
            className={`rounded-sm px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.1em] ${
              view === v ? "bg-bg-panel text-foreground" : "text-ink-3 hover:text-foreground"
            }`}
          >
            {v} <span className="font-mono text-ink-3">{counts[v]}</span>
          </button>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-[11px] text-ink-2">
        <label className="flex items-center gap-1.5">
          <span className="uppercase tracking-[0.08em]">Domain</span>
          <select value={domain} onChange={(e) => setDomain(e.target.value)} className="rounded-sm border border-input bg-background px-2 py-0.5 font-mono text-ink-2">
            <option value="all">all</option>
            {domains.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </label>
        <label className="flex items-center gap-1.5">
          <span className="uppercase tracking-[0.08em]">Sort</span>
          <select value={sort} onChange={(e) => setSort(e.target.value as "materiality" | "recent")} className="rounded-sm border border-input bg-background px-2 py-0.5 font-mono text-ink-2">
            <option value="materiality">materiality</option>
            <option value="recent">recent</option>
          </select>
        </label>
        <label className="flex items-center gap-1.5">
          <input type="checkbox" checked={heldOnly} onChange={(e) => setHeldOnly(e.target.checked)} className="accent-primary" />
          <span className="uppercase tracking-[0.08em]">Held / blocked only</span>
        </label>
      </div>

      {viewCards.length === 0 ? (
        <EmptyState message={VIEW_EMPTY[view][0]} sub={VIEW_EMPTY[view][1]} action="Operational tracking — git is the audit trail" />
      ) : (
        <div>
          {viewCards.map((c) => (
            <ResearchArtifactRow key={c.card_id} card={c} artifacts={artifacts} />
          ))}
        </div>
      )}
    </div>
  );
}
