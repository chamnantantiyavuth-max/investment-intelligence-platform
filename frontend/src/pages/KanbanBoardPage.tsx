import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getOrgQueue, getResearchArtifacts, type OrgCard, type ResearchArtifact } from "@/api/orgClient";
import { linkArtifact, latestCardUpdate } from "@/lib/researchWorkflow";
import { Skeleton } from "@/components/ui/skeleton";

/** Read-only kanban VISUAL board (FD #59) — Hermes Capital Intelligence board
 *  native columns (Stage 7.5, FD #106; C6 — triage/todo/scheduled/ready/running/
 *  blocked/review/done/archived) rendered as column stacks from GET /org-queue.
 *
 *  Operational tracking only — card state never equals domain state
 *  (KANBAN-CONTRACT §1). Read-only by design: movement rights belong to
 *  the CoS/IC Secretary and Founder (KANBAN-CONTRACT §6), never the UI —
 *  no drag, no move, no writes. Counts are display derivations from
 *  `workflow_column`; no composite scores (Constitution §10).
 */

function BoardCard({ card, artifacts }: { card: OrgCard; artifacts: ResearchArtifact[] }) {
  const target = linkArtifact(card, artifacts);
  const body = (
    <>
      <p className="font-mono text-[10px] uppercase tracking-[0.1em] text-ink-3">{card.card_id}</p>
      <p className="mt-1 font-display text-[13px] font-semibold leading-snug tracking-tight text-foreground">
        {card.title}
      </p>
      <p className="mt-1 flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-[10px]">
        <span className="uppercase tracking-[0.08em] text-primary">{card.domain}</span>
        <span className="font-mono text-ink-3">{card.materiality}</span>
        <span className="text-ink-2">{card.priority}</span>
      </p>
      <p className="mt-1 truncate text-[10px] text-ink-2">{card.principal_owner}</p>
      {card.active_holds.length > 0 && (
        <p className="mt-1 text-[10px] font-semibold uppercase tracking-[0.08em] text-warning">
          {card.active_holds.map((h) => h.hold_id).join(" · ")}
        </p>
      )}
      {card.blocked_reason && (
        <p className="mt-1 truncate text-[10px] text-warning" title={card.blocked_reason}>
          blocked: {card.blocked_reason}
        </p>
      )}
      <p className="mt-1.5 flex items-baseline justify-between gap-2 text-[10px] text-ink-3">
        <span className="font-mono">{card.last_updated}</span>
        {target ? (
          <span className="font-semibold uppercase tracking-[0.1em] text-primary">open →</span>
        ) : (
          <span>no artifact</span>
        )}
      </p>
    </>
  );
  return (
    <div className="rounded-md bg-bg-panel px-3 py-2">
      {target ? (
        <Link
          to={`/research/${target.artifact_id}`}
          className="block focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
        >
          {body}
        </Link>
      ) : (
        <div>{body}</div>
      )}
    </div>
  );
}

export default function KanbanBoardPage() {
  const queue = useQuery({ queryKey: ["org-queue"], queryFn: getOrgQueue, staleTime: 60_000 });
  const registry = useQuery({ queryKey: ["research-artifacts"], queryFn: getResearchArtifacts, staleTime: 60_000 });

  const columns = useMemo(() => queue.data?.columns ?? [], [queue.data]);
  const cards = useMemo(() => queue.data?.cards ?? [], [queue.data]);
  const artifacts = useMemo(() => registry.data?.artifacts ?? [], [registry.data]);

  const byColumn = useMemo(
    () => columns.map((col) => ({ column: col, cards: cards.filter((c) => c.workflow_column === col) })),
    [columns, cards]
  );

  if (queue.isLoading || registry.isLoading) return <Skeleton className="h-64 w-full" />;
  if (queue.isError || registry.isError)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Kanban board unavailable — API error.</p>
        <p className="mt-1 text-xs text-ink-2">What failed: the org-workflow queue endpoint.</p>
        <button
          type="button"
          onClick={() => {
            queue.refetch();
            registry.refetch();
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
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Research workflow</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">Kanban Board</h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">
          Kanban board · operational tracking · latest card update {latest}
        </p>
        <p className="mt-1 max-w-2xl text-xs text-ink-2">
          Read-only view of the research kanban. Operational tracking only — card state never equals
          the actual research state. Cards move only through the research workflow, never from this screen.
        </p>
      </div>

      <div className="overflow-x-auto pb-2">
        <div className="flex min-w-max gap-3">
          {byColumn.map(({ column, cards: colCards }, i) => (
            <div key={column} className={`w-[192px] shrink-0 ${i > 0 ? "border-l border-rule pl-3" : ""}`}>
              <p className="flex items-baseline gap-2 whitespace-nowrap text-[10px] font-bold uppercase tracking-[0.14em] text-foreground">
                {column}
                <span className="font-mono font-normal text-ink-3">{colCards.length}</span>
              </p>
              {colCards.length === 0 ? (
                <p className="mt-2 text-[10px] leading-relaxed text-ink-3">
                  No cards
                  <br />
                  intake: CoS / IC Secretary
                </p>
              ) : (
                <div className="mt-2 space-y-2">
                  {colCards.map((c) => (
                    <BoardCard key={c.card_id} card={c} artifacts={artifacts} />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
