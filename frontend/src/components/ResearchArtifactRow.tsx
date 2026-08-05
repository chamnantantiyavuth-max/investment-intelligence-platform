import { Link } from "react-router-dom";
import type { OrgCard, ResearchArtifact } from "@/api/orgClient";
import { linkArtifact, readinessOf } from "@/lib/researchWorkflow";
import { HoldBanner } from "@/components/HoldBanner";
import { ReviewGatePanel } from "@/components/ReviewGatePanel";

/** Research Desk ledger row — the org-workflow card as a borderless hairline row.
 *  Active holds render a full banner above the row; never a badge. */
export function ResearchArtifactRow({
  card,
  artifacts,
}: {
  card: OrgCard;
  artifacts: ResearchArtifact[];
}) {
  const target = linkArtifact(card, artifacts);
  const readiness = readinessOf(card);
  const body = (
    <>
      {card.active_holds.length > 0 && (
        <div className="mb-3">
          {card.active_holds.map((h) => (
            <HoldBanner key={h.hold_id} hold={h} />
          ))}
        </div>
      )}
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
        <span className="font-mono text-[11px] text-ink-3">{card.card_id}</span>
        <span className="font-display text-[15px] font-semibold tracking-tight text-foreground">
          {card.title}
        </span>
        <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">
          {readiness}
        </span>
      </div>
      {card.research_question && (
        <p className="mt-0.5 text-xs text-ink-2">{card.research_question}</p>
      )}
      <div className="mt-1 flex flex-wrap items-baseline gap-x-4 gap-y-0.5 text-[11px] text-ink-2">
        <span className="uppercase tracking-[0.08em] text-primary">{card.domain}</span>
        <span className="font-mono">{card.materiality}</span>
        <span>{card.principal_owner}</span>
        <span className="font-mono text-ink-3">{card.workflow_column}</span>
        {card.blocked_reason && <span className="text-warning">blocked: {card.blocked_reason}</span>}
      </div>
      <div className="mt-1.5 flex flex-wrap items-baseline justify-between gap-2 text-[11px]">
        <span className="text-ink-3">
          changed {card.last_updated} · next: <span className="text-foreground">{card.next_action || "—"}</span>
        </span>
        {target ? (
          <span className="font-semibold uppercase tracking-[0.1em] text-primary">open →</span>
        ) : (
          <span className="text-ink-3">no artifact yet</span>
        )}
      </div>
    </>
  );
  return (
    <div className="border-b border-rule py-3">
      {target ? (
        <Link to={`/research/${target.artifact_id}`} className="block focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">
          {body}
        </Link>
      ) : (
        <div>{body}</div>
      )}
      <div className="mt-2">
        <ReviewGatePanel card={card} />
      </div>
    </div>
  );
}
