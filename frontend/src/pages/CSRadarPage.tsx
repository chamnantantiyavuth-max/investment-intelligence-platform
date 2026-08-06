import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { getCSRadar, type CSAsset } from "@/api/csClient";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

/** Close System radar (P2 — institutional standard, FD #60).
 *  Dense ledger; lead judgment = display ordering from admitted fields only. */

const CONVICTION_ORDER = ["Low", "Moderate", "High", "Maximum"];

function convictionRank(a: CSAsset): number {
  return CONVICTION_ORDER.indexOf(a.conviction);
}

export default function CSRadarPage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cs-radar"],
    queryFn: getCSRadar,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-64 w-full" />;
  if (error)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Could not load the Close System radar.</p>
        <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );

  const assets: CSAsset[] = data?.assets ?? [];
  const lead = [...assets].sort(
    (a, b) => convictionRank(b) - convictionRank(a) || b.layers_aligned - a.layers_aligned
  )[0];

  return (
    <div className="mx-auto max-w-[960px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Close System</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">Product radar</h1>
        <p className="mt-1 text-[12px] text-ink-2">
          Physical and commodity-linked products screened for discount, structural demand, and risk alignment ·{" "}
          <span className="text-warning">synthetic demo data — labeled, never disguised</span>
        </p>
      </header>

      {lead && (
        <section className="mt-6 border-b border-rule pb-6">
          <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-primary">Lead judgment</p>
          <h2 className="mt-2 max-w-[760px] font-display text-[22px] font-semibold leading-snug tracking-tight">
            Most interesting product to watch: {lead.ticker} — {lead.name}
          </h2>
          <p className="mt-2 font-mono text-[14px] text-foreground">
            {lead.conviction} conviction · {lead.layers_aligned}/{Object.keys(lead.layers).length} layers aligned
          </p>
          <p className="mt-1 max-w-[680px] text-[13px] leading-relaxed text-ink-2">{lead.recommendation}</p>
          <Link to={`/cs-radar/${lead.ticker}`} className="mt-2 inline-block text-[11px] font-semibold uppercase tracking-[0.12em] text-primary">
            Open the note →
          </Link>
        </section>
      )}

      <section className="mt-6">
        <div className="grid grid-cols-[70px_1.4fr_0.9fr_0.7fr_0.8fr_1.3fr] gap-x-4 border-b border-rule pb-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">
          <span>Ticker</span>
          <span>Product</span>
          <span>Eligibility</span>
          <span>Layers</span>
          <span>Conviction</span>
          <span>Recommendation</span>
        </div>
        {assets.map((a) => {
          const allPass = a.p1_pass && a.p2_pass && a.p3_pass;
          return (
            <Link
              key={a.id ?? a.ticker}
              to={`/cs-radar/${a.ticker}`}
              className="group grid grid-cols-[70px_1.4fr_0.9fr_0.7fr_0.8fr_1.3fr] items-baseline gap-x-4 border-b border-rule/60 py-2.5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              <span className="font-mono text-[12.5px] font-semibold text-primary">{a.ticker}</span>
              <span>
                <span className="font-display text-[14px] font-semibold tracking-tight text-foreground group-hover:text-primary">{a.name}</span>
                <span className="block text-[11px] text-ink-2">{a.category}</span>
              </span>
              <span className={cn("font-mono text-[12px]", allPass ? "text-positive" : "text-warning")}>
                {allPass ? "P1·P2·P3" : [a.p1_pass && "P1", a.p2_pass && "P2", a.p3_pass && "P3"].filter(Boolean).join("·") || "—"}
              </span>
              <span className="font-mono text-[12px] text-ink-2">
                {a.layers_aligned}/{Object.keys(a.layers).length}
              </span>
              <span className={cn("font-mono text-[12px]", a.conviction === "Maximum" || a.conviction === "High" ? "text-positive" : undefined)}>
                {a.conviction}
              </span>
              <span className="text-[12px] leading-snug text-ink-2">{a.recommendation}</span>
            </Link>
          );
        })}
      </section>
    </div>
  );
}
