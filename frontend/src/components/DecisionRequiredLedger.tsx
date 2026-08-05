import { Link } from "react-router-dom";
import type { OrgCard, ResearchArtifact } from "@/api/orgClient";
import { linkArtifact, readinessOf } from "@/lib/researchWorkflow";

/** Briefing "Decisions Required" ledger — states WHAT decision, not just
 *  "review needed" (fit-gap §4.3). Readiness is a display derivation. */
export function DecisionRequiredLedger({
  cards,
  artifacts,
}: {
  cards: OrgCard[];
  artifacts: ResearchArtifact[];
}) {
  const decisions = cards.filter(
    (c) => c.workflow_column === "Founder Review" || (c.open_decision_slots?.length ?? 0) > 0
  );
  if (decisions.length === 0) {
    return (
      <p className="text-xs text-ink-2">
        No items require your decision — new decisions appear here when the IC Secretary moves a
        complete packet into Founder Review.
      </p>
    );
  }
  return (
    <div className="divide-y divide-rule">
      {decisions.map((c) => {
        const target = linkArtifact(c, artifacts);
        const readiness = readinessOf(c);
        const inner = (
          <div className="py-2">
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
              <span className="font-mono text-[11px] text-ink-3">{c.card_id}</span>
              <span className="font-display text-[15px] font-semibold tracking-tight text-foreground">
                {c.title}
              </span>
              <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{readiness}</span>
            </div>
            <p className="mt-0.5 text-xs text-ink-2">
              Decide: {c.next_action || c.research_question}
            </p>
            <p className="mt-0.5 text-[11px] text-ink-3">
              {c.domain} · {c.materiality} · as-of {c.last_updated}
              {c.active_holds.length > 0 && ` · ${c.active_holds.length} active hold(s)`}
            </p>
          </div>
        );
        return target ? (
          <Link key={c.card_id} to={`/research/${target.artifact_id}`} className="block focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">
            {inner}
          </Link>
        ) : (
          <div key={c.card_id}>{inner}</div>
        );
      })}
    </div>
  );
}
