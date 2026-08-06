import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getReports } from "@/api/reportClient";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

const TYPE_LABEL: Record<string, string> = {
  company: "Company",
  product: "Product",
  weekly: "Weekly Brief",
  quarterly: "Quarterly",
  theme: "Theme",
};

function statusTone(status: string): string | undefined {
  if (status === "published") return "text-positive";
  if (status === "review") return "text-warning";
  return "text-ink-3";
}

export default function LibraryPage() {
  const [status, setStatus] = useState("all");
  const [type, setType] = useState("all");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["reports"],
    queryFn: getReports,
    staleTime: 30_000,
  });

  const reports = useMemo(() => data?.reports ?? [], [data]);
  const types = useMemo(() => Array.from(new Set(reports.map((r) => r.type))).sort(), [reports]);

  const visible = useMemo(
    () =>
      reports.filter(
        (r) => (status === "all" || r.status === status) && (type === "all" || r.type === type)
      ),
    [reports, status, type]
  );

  if (isLoading) return <Skeleton className="h-64 w-full" />;
  if (error)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Could not load the research library.</p>
        <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );

  return (
    <div className="mx-auto max-w-[960px]">
      <header className="border-b border-rule pb-5">
        <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Research library</p>
        <h1 className="mt-1 font-display text-h2 font-bold tracking-tight">The library</h1>
        <p className="mt-1 text-[12px] text-ink-2">
          {reports.filter((r) => r.status === "published").length} published reports · every report carries its
          evidence, its date, and its status
        </p>
      </header>

      <div className="mt-5 flex flex-wrap items-center gap-x-5 gap-y-2 text-[11px] text-ink-2">
        <label className="flex items-center gap-1.5">
          <span className="uppercase tracking-[0.08em]">Status</span>
          <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded-sm border border-input bg-background px-2 py-0.5 font-mono text-ink-2">
            <option value="all">all</option>
            <option value="published">published</option>
            <option value="review">in review</option>
            <option value="draft">draft</option>
          </select>
        </label>
        <label className="flex items-center gap-1.5">
          <span className="uppercase tracking-[0.08em]">Type</span>
          <select value={type} onChange={(e) => setType(e.target.value)} className="rounded-sm border border-input bg-background px-2 py-0.5 font-mono text-ink-2">
            <option value="all">all</option>
            {types.map((t) => (
              <option key={t} value={t}>{TYPE_LABEL[t] ?? t}</option>
            ))}
          </select>
        </label>
      </div>

      {visible.length === 0 ? (
        <div className="mt-8 rounded-md bg-bg-panel px-5 py-10">
          <p className="text-sm font-medium text-foreground">No reports here yet.</p>
          <p className="mt-1 text-[12.5px] text-ink-2">The research team's reports will appear as they pass review.</p>
        </div>
      ) : (
        <section className="mt-4">
          {visible.map((r) => (
            <Link
              key={r.slug}
              to={`/library/${r.slug}`}
              className="group block border-b border-rule/60 py-3 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
            >
              <p className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
                <span className="font-display text-[16px] font-semibold tracking-tight text-foreground group-hover:text-primary">
                  {r.title}
                </span>
                <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.08em] text-ink-2">
                  {TYPE_LABEL[r.type] ?? r.type}
                </span>
                <span className={cn("text-[10.5px] font-semibold uppercase tracking-[0.12em]", statusTone(r.status))}>
                  {r.status}
                </span>
              </p>
              {r.summary && <p className="mt-0.5 max-w-[720px] text-[12.5px] leading-relaxed text-ink-2">{r.summary}</p>}
              <p className="mt-1 font-mono text-[11px] text-ink-3">
                {r.date}
                {r.subject ? ` · ${r.subject}` : ""}
                {r.author ? ` · ${r.author}` : ""}
              </p>
            </Link>
          ))}
        </section>
      )}
    </div>
  );
}
