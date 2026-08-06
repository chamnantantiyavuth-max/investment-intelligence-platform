import { cn } from "@/lib/utils";

/** Weak signal inbox (P2 — institutional standard, FD #60).
 *  Demonstration items shown as a plain ledger — no dead buttons; actions
 *  arrive with the experimental pipeline. */

const ANOMALIES = [
  { id: 1, title: "Sector rotation into Utilities", age: "New", desc: "Defensive sector volume 3σ above 20-day average. No credible explanation yet." },
  { id: 2, title: "Small-cap breadth divergence", age: "2d", desc: "Russell 2000 advance/decline line diverging from price. Liquidity signal?" },
  { id: 3, title: "Treasury yield curve steepening", age: "New", desc: "2s10s spread widening rapidly. End-of-cycle or reflation?" },
];

const HYPOTHESES = [
  { id: 1, title: "Grid Modernization Supercycle", status: "Experimental", confidence: 62, evidence: 8, entities: ["GE", "VRT", "ETN", "HUBB"] },
  { id: 2, title: "Nuclear Renaissance for AI Power", status: "Experimental", confidence: 45, evidence: 5, entities: ["CEG", "BWXT", "LEU"] },
  { id: 3, title: "Insurance Hard Market Cycle", status: "Under Review", confidence: 71, evidence: 12, entities: ["BRK.B", "TRV", "CB"] },
  { id: 4, title: "Reshoring Capex Cycle", status: "Experimental", confidence: 55, evidence: 7, entities: ["CAT", "URI", "PWR"] },
];

function SectionKicker({ n: num, title }: { n: string; title: string }) {
  return (
    <div className="mt-8 border-b border-rule pb-2">
      <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink-3">
        {num} · {title}
      </p>
    </div>
  );
}

export default function WeakSignalInboxPage() {
  return (
    <div className="mx-auto max-w-[880px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Theme intelligence</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">Weak signal inbox</h1>
        <p className="mt-1 max-w-[680px] text-[12px] leading-relaxed text-ink-2">
          Early, unexplained moves and emerging hypotheses worth watching. These are demonstration items — the
          experimental pipeline is not yet connected, and actions (propose, dismiss, review) will arrive with it.
        </p>
      </header>

      <section>
        <SectionKicker n="01" title="Unexplained anomalies" />
        <div className="mt-3">
          {ANOMALIES.map((a) => (
            <div key={a.id} className="border-b border-rule/60 py-2.5">
              <p className="flex items-baseline gap-2">
                <span className="font-display text-[14px] font-semibold tracking-tight text-foreground">{a.title}</span>
                <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.08em] text-ink-2">{a.age}</span>
              </p>
              <p className="mt-0.5 text-[12.5px] leading-relaxed text-ink-2">{a.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <SectionKicker n="02" title="Theme hypotheses" />
        <div className="mt-3">
          {HYPOTHESES.map((h) => (
            <div key={h.id} className="border-b border-rule/60 py-2.5">
              <p className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
                <span className="font-display text-[14px] font-semibold tracking-tight text-foreground">{h.title}</span>
                <span
                  className={cn(
                    "text-[10.5px] font-semibold uppercase tracking-[0.1em]",
                    h.status === "Under Review" ? "text-warning" : "text-ink-3"
                  )}
                >
                  {h.status}
                </span>
                <span className="font-mono text-[11.5px] text-ink-2">confidence {h.confidence}%</span>
                <span className="font-mono text-[11.5px] text-ink-2">evidence {h.evidence} items</span>
              </p>
              <p className="mt-1 font-mono text-[11.5px] text-ink-2">{h.entities.join(" · ")}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
