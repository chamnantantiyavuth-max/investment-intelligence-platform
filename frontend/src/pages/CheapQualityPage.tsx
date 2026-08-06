import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { getFOCheapQuality } from "@/api/foClient";
import type { ResearchPackageSummary } from "@/types/fo";
import { Skeleton } from "@/components/ui/skeleton";
import { ProvenanceChip } from "@/components/ProvenanceChip";
import { cn } from "@/lib/utils";

/** Cheap & Quality watchlist (P2 — institutional standard, FD #60).
 *  Honest empty state: the trigger needs 5-year volatility data the current
 *  dataset does not carry — an empty watchlist is the correct, honest result. */

export default function CheapQualityPage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-cheap-quality"],
    queryFn: getFOCheapQuality,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-64 w-full" />;
  if (error)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Could not load the watchlist.</p>
        <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );

  const provenance = data?.[0]?.provenance;

  return (
    <div className="mx-auto max-w-[960px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Fundamental research</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">Cheap & Quality</h1>
        <p className="mt-1 flex flex-wrap items-center gap-2 text-[12px] text-ink-2">
          Companies unusually cheap against their own history AND clear of the value-trap screen
          {provenance?.mode && <ProvenanceChip mode={provenance.mode} source={provenance.source} asOf={provenance.as_of} />}
        </p>
      </header>

      {!data?.length ? (
        <div className="mt-8 rounded-md bg-bg-panel px-5 py-10">
          <p className="text-sm font-medium text-foreground">No companies pass the screen yet.</p>
          <p className="mt-1 max-w-[680px] text-[12.5px] leading-relaxed text-ink-2">
            The cheap-and-quality trigger compares a company's P/E to its own five-year average and requires
            five-year earnings volatility data. That volatility data is not yet carried by the current dataset,
            so the screen correctly returns nothing — it will light up when the data exists.
          </p>
        </div>
      ) : (
        <section className="mt-6">
          <div className="grid grid-cols-[minmax(220px,1.6fr)_0.8fr_0.9fr] gap-x-4 border-b border-rule pb-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">
            <span>Company</span>
            <span>Moat</span>
            <span>Conviction</span>
          </div>
          {data.map((pkg: ResearchPackageSummary) => (
            <Link
              key={pkg.id}
              to={`/fundamental/${pkg.id}`}
              className="group grid grid-cols-[minmax(220px,1.6fr)_0.8fr_0.9fr] items-baseline gap-x-4 border-b border-rule/60 py-2.5 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
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
              <span className={cn("font-mono text-[12.5px]", pkg.moat_width === "Wide" ? "text-positive" : pkg.moat_width === "None" ? "text-ink-3" : undefined)}>
                {pkg.moat_width || "—"}
              </span>
              <span className={cn("font-mono text-[12.5px]", pkg.conviction === "Maximum" || pkg.conviction === "High" ? "text-positive" : undefined)}>
                {pkg.conviction || "—"}
              </span>
            </Link>
          ))}
        </section>
      )}
    </div>
  );
}
