import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getIISignals } from "@/api/iiClient";
import type { IISignalsResponse } from "@/types/ii";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

/** Institutional intelligence ledger (P2 — institutional standard, FD #60).
 *  Dense 13F signal table; action labels in plain language; raw CUSIPs stay
 *  as tooltips behind the ticker — background data, not page furniture. */

const PAGE_SIZE = 50;

const ACTION_LABEL: Record<string, string> = {
  BASELINE: "Held",
  INCREASED: "Added",
  NEW: "New",
  REDUCED: "Reduced",
  EXITED: "Exited",
};

function fmtUSD(v: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 1 }).format(v);
}

function actionTone(a: string): string | undefined {
  if (a === "INCREASED" || a === "NEW") return "text-positive";
  if (a === "REDUCED" || a === "EXITED") return "text-negative";
  return undefined;
}

export default function InstitutionalPage() {
  const [page, setPage] = useState(0);

  const { data, isLoading, isError } = useQuery<IISignalsResponse>({
    queryKey: ["ii-signals", page],
    queryFn: () => getIISignals(PAGE_SIZE, page * PAGE_SIZE),
  });

  const total = data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const meta = data?.meta ?? {};
  const provenance = data?.provenance;
  const completeness = provenance?.completeness?.replace("partial_21_51", "21 of 51 funds tracked");

  return (
    <div className="mx-auto max-w-[1080px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Institutional intelligence</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">13F signal ledger</h1>
        <p className="mt-1 text-[12px] text-ink-2">
          {total.toLocaleString()} signals from SEC 13F filings
          {completeness ? ` · ${completeness}` : ""}
          {meta.as_of ? ` · as of ${meta.as_of}` : ""}
          {provenance?.mode === "synthetic" ? " · synthetic demo data" : ""}
        </p>
      </header>

      <section className="mt-6">
        <h2 className="font-display text-[20px] font-semibold tracking-tight">
          Where are the funds we track concentrating capital?
        </h2>
        <p className="mt-1 text-[12px] text-ink-2">
          {String(data?.summary?.total_funds_tracked ?? "—")} funds · largest positions and conviction changes
        </p>
      </section>

      {isLoading ? (
        <Skeleton className="mt-4 h-96 w-full" />
      ) : isError ? (
        <div className="mt-4 rounded-md bg-bg-panel px-4 py-8">
          <p className="text-sm font-medium text-negative">Could not load 13F signals.</p>
        </div>
      ) : (
        <section className="mt-4">
          <div className="grid grid-cols-[1.5fr_0.55fr_0.55fr_0.7fr_0.75fr_0.7fr_0.7fr_0.8fr] gap-x-4 border-b border-rule pb-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">
            <span>Filer</span>
            <span>Position</span>
            <span>Quarter</span>
            <span>Portfolio</span>
            <span>Conviction</span>
            <span>Action</span>
            <span>Change</span>
            <span className="text-right">Value</span>
          </div>
          {(data?.signals ?? []).map((s, i) => (
            <div
              key={`${s.filer_cik}-${s.ticker}-${i}`}
              className="grid grid-cols-[1.5fr_0.55fr_0.55fr_0.7fr_0.75fr_0.7fr_0.7fr_0.8fr] items-baseline gap-x-4 border-b border-rule/60 py-2 text-[12.5px]"
            >
              <span>
                <span className="font-medium text-foreground">{s.filer_name}</span>
                <span className="ml-1.5 text-[10.5px] uppercase tracking-[0.06em] text-ink-3">{s.filer_category}</span>
              </span>
              <span className="font-mono text-[12px] text-foreground" title={/^\d/.test(s.ticker) ? `CUSIP ${s.ticker}` : undefined}>
                {/^\d/.test(s.ticker) ? "—" : s.ticker}
              </span>
              <span className="font-mono text-[11.5px] text-ink-2">{s.filing_quarter}</span>
              <span className="font-mono tabular-nums text-ink-2">{s.pct_of_portfolio.toFixed(2)}%</span>
              <span className={cn("font-mono", s.conviction === "Maximum" ? "text-positive" : s.conviction === "High" ? "text-foreground" : "text-ink-2")}>
                {s.conviction}
              </span>
              <span className={cn("font-mono", actionTone(s.action))}>{ACTION_LABEL[s.action] ?? s.action}</span>
              <span className={cn("font-mono tabular-nums", s.change_pct > 0 ? "text-positive" : s.change_pct < 0 ? "text-negative" : "text-ink-3")}>
                {s.change_pct === 0 ? "—" : `${s.change_pct > 0 ? "+" : ""}${s.change_pct.toFixed(1)}%`}
              </span>
              <span className="text-right font-mono tabular-nums text-ink-2">{fmtUSD(s.value_usd)}</span>
            </div>
          ))}
          {(data?.signals?.length ?? 0) === 0 && (
            <p className="py-8 text-center text-[12.5px] text-ink-3">No signals in this range.</p>
          )}

          <div className="mt-4 flex items-center justify-between text-[11.5px] text-ink-2">
            <span>
              Page {page + 1} of {pages} · {total.toLocaleString()} signals
            </span>
            <div className="flex gap-4">
              <button
                type="button"
                disabled={page === 0}
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                className="font-semibold uppercase tracking-[0.1em] text-primary disabled:text-ink-3"
              >
                ← Previous
              </button>
              <button
                type="button"
                disabled={page >= pages - 1}
                onClick={() => setPage((p) => p + 1)}
                className="font-semibold uppercase tracking-[0.1em] text-primary disabled:text-ink-3"
              >
                Next →
              </button>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
