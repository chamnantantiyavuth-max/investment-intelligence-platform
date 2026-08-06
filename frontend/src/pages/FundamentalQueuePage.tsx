import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { getFOQueue } from "@/api/foClient";
import type { ResearchPackageSummary } from "@/types/fo";
import { Skeleton } from "@/components/ui/skeleton";
import { ProvenanceChip } from "@/components/ProvenanceChip";
import { cn } from "@/lib/utils";

/** Fundamental research queue (P2 — institutional standard, FD #60).
 *  Dense ledger; states as compact text with color, never pills-on-everything. */

function stateTone(kind: string, value: string): string | undefined {
  if (kind === "moat") return value === "Wide" ? "text-positive" : value === "None" ? "text-ink-3" : undefined;
  if (kind === "earnings") return value === "HIGH" ? "text-positive" : value === "LOW" ? "text-negative" : undefined;
  if (kind === "conviction") return value === "Maximum" || value === "High" ? "text-positive" : value === "Low" ? "text-negative" : undefined;
  if (kind === "trap")
    return value.includes("TRAP") ? "text-negative" : value === "MIXED" ? "text-warning" : "text-positive";
  return undefined;
}

export default function FundamentalQueuePage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-queue"],
    queryFn: getFOQueue,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Could not load the fundamental queue.</p>
        <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );
  if (!data?.length)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-10 text-center">
        <p className="text-sm font-medium text-foreground">No companies in the fundamental queue.</p>
        <p className="mt-1 text-xs text-ink-2">Research packages appear here once the pipeline admits a run.</p>
      </div>
    );

  const allMoatLimited = data.every((p) => !p.moat_width || p.moat_width === "None");

  return (
    <div className="mx-auto max-w-[960px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Fundamental research</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">The queue</h1>
        <p className="mt-1 flex flex-wrap items-center gap-2 text-[12px] text-ink-2">
          {data.length} companies under fundamental investigation
          <ProvenanceChip mode={data[0]?.provenance.mode} source={data[0]?.provenance.source} asOf={data[0]?.provenance.as_of} />
        </p>
      </header>

      <section className="mt-6">
        <h2 className="font-display text-[20px] font-semibold tracking-tight">Which companies deserve a closer look?</h2>
        <div className="mt-3">
          <div className="grid grid-cols-[minmax(220px,1.6fr)_0.8fr_0.7fr_0.9fr_1fr] gap-x-4 border-b border-rule pb-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">
            <span>Company</span>
            <span>Moat</span>
            <span>Earnings</span>
            <span>Conviction</span>
            <span>Value trap</span>
          </div>
          {data.map((pkg: ResearchPackageSummary) => (
            <Link
              key={pkg.id}
              to={`/fundamental/${pkg.id}`}
              className="group grid grid-cols-[minmax(220px,1.6fr)_0.8fr_0.7fr_0.9fr_1fr] items-baseline gap-x-4 border-b border-rule/60 py-2.5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              <span>
                <span className="font-display text-[14.5px] font-semibold tracking-tight text-foreground group-hover:text-primary">
                  {pkg.name}
                </span>
                <span className="ml-1.5 font-mono text-[11px] text-ink-3">{pkg.id}</span>
                <span className="block text-[11px] text-ink-2">
                  {pkg.sector} · {pkg.industry}
                </span>
              </span>
              <span className={cn("font-mono text-[12.5px]", stateTone("moat", pkg.moat_width))}>
                {pkg.moat_width || "—"} {pkg.moat_depth ? `· ${pkg.moat_depth.toLowerCase()}` : ""}
              </span>
              <span className={cn("font-mono text-[12.5px]", stateTone("earnings", pkg.earnings_quality))}>
                {pkg.earnings_quality || "—"}
              </span>
              <span className={cn("font-mono text-[12.5px]", stateTone("conviction", pkg.conviction))}>
                {pkg.conviction || "—"}
              </span>
              <span className={cn("font-mono text-[12.5px]", stateTone("trap", pkg.value_trap_verdict))}>
                {pkg.value_trap_verdict || "—"}
              </span>
            </Link>
          ))}
        </div>
        {allMoatLimited && (
          <p className="mt-4 max-w-[720px] text-[12px] leading-relaxed text-ink-2">
            Moat classification is currently limited for all companies in this queue — open a note to see the
            quantitative foundation and what the analysis cannot yet tell you.
          </p>
        )}
      </section>
    </div>
  );
}
