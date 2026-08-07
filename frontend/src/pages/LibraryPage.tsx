import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getReports, type ReportMeta } from "@/api/reportClient";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

/**
 * Research library — Modern Digital Magazine index (FD #84, direction B).
 * Text/typography-driven editorial: minimal masthead, hero feature, asymmetric
 * feature grid, latest stream, series chips. No imagery (FD #84 — AI art rejected).
 */

const TYPE_LABEL: Record<string, string> = {
  company: "Company",
  product: "Product",
  weekly: "Weekly",
  quarterly: "Quarterly",
  theme: "Theme",
};

const TYPE_KICKER: Record<string, string> = {
  company: "Company Research",
  product: "Commodities",
  weekly: "Weekly Intelligence",
  quarterly: "Quarterly",
  theme: "Theme",
};

function statusTone(status: string): string | undefined {
  if (status === "published") return "text-positive";
  if (status === "review") return "text-warning";
  return "text-ink-3";
}

/** Series grouping — display-level only: primary subject token → series name. */
function seriesKey(r: ReportMeta): string {
  const s = r.subject ?? "";
  if (s.includes("AAPL")) return "Apple";
  if (s.includes("Silver")) return "Silver";
  if (s.includes("Gold")) return "Gold";
  if (s.includes("JNJ")) return "JNJ";
  if (r.type === "weekly" || s.includes("weekly")) return "Weekly";
  return s.trim() || "Other";
}

export default function LibraryPage() {
  const [status, setStatus] = useState("all");
  const [type, setType] = useState("all");
  const [series, setSeries] = useState<string | null>(null);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["reports"],
    queryFn: getReports,
    staleTime: 30_000,
  });

  const reports = useMemo(() => data?.reports ?? [], [data]);
  const published = useMemo(
    () => reports.filter((r) => r.status === "published").sort((a, b) => b.date.localeCompare(a.date)),
    [reports]
  );

  /** Cover = latest main research note (not the weekly cadence letter, not an opposing companion). */
  const mains = useMemo(
    () => published.filter((r) => r.type !== "weekly" && !r.slug.includes("opposing")),
    [published]
  );

  const types = useMemo(() => Array.from(new Set(reports.map((r) => r.type))).sort(), [reports]);

  const seriesList = useMemo(() => {
    const byKey = new Map<string, ReportMeta[]>();
    for (const r of reports) {
      const k = seriesKey(r);
      byKey.set(k, [...(byKey.get(k) ?? []), r]);
    }
    return Array.from(byKey.entries())
      .map(([name, items]) => ({
        name,
        count: items.length,
        latest: items.map((i) => i.date).sort().at(-1) ?? "",
      }))
      .sort((a, b) => b.count - a.count);
  }, [reports]);

  const hero = mains[0] ?? published[0];
  const features = mains.filter((r) => r.slug !== hero?.slug).slice(0, 3);
  const rest = published.filter((r) => r.slug !== hero?.slug && !features.some((f) => f.slug === r.slug));

  const visible = useMemo(() => {
    let list = rest;
    if (status !== "all") list = list.filter((r) => r.status === status);
    if (type !== "all") list = list.filter((r) => r.type === type);
    if (series) list = list.filter((r) => seriesKey(r) === series);
    return list;
  }, [rest, status, type, series]);

  /** True companion: the other half of a main/opposing pair (base-slug match, same subject). */
  const companionOf = (r: ReportMeta) => {
    const base = r.slug.replace(/-opposing$/, "");
    const pairSlug = r.slug.endsWith("-opposing") ? base : `${base}-opposing`;
    return published.find((o) => o.slug === pairSlug && o.subject === r.subject && o.slug !== r.slug);
  };

  if (isLoading) return <Skeleton className="h-96 w-full" />;
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
    <div className="mx-auto max-w-[1120px]">
      {/* ── Minimal masthead ── */}
      <header className="flex flex-wrap items-baseline justify-between gap-2 border-b border-ink py-4">
        <span className="font-display text-2xl font-bold tracking-tight">
          Research Intelligence<span className="text-primary">.</span>
        </span>
        <span className="font-mono text-[11px] text-ink-3" data-testid="library-count">
          {published.length} published
        </span>
      </header>

      {/* ── Hero feature ── */}
      {hero && (
        <section className="py-10">
          <span className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.2em] text-primary">
            <span className="rounded-[2px] bg-primary px-1.5 py-0.5 text-[9px] font-bold text-white">Featured</span>
            {TYPE_KICKER[hero.type] ?? hero.type} · {hero.subject || ""}
          </span>
          <h1 className="mt-4 max-w-[900px] font-display text-[clamp(34px,5vw,56px)] font-bold leading-[1.06] tracking-[-0.015em]">
            <Link to={`/library/${hero.slug}`} className="hover:text-primary">{hero.title}</Link>
          </h1>
          {hero.summary && <p className="mt-4 max-w-[760px] text-[17px] leading-[1.65] text-ink-2">{hero.summary}</p>}
          <div className="mt-5 flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-[11px] text-ink-3">
            <span className="text-[10px] font-semibold uppercase tracking-[0.1em] text-ink-2">{hero.author}</span>
            <span className="text-rule">|</span>
            <span>{hero.date}</span>
            <span className="text-rule">|</span>
            <span>{hero.subject}</span>
            <span className="text-rule">|</span>
            <span className={cn("font-semibold", statusTone(hero.status))}>● {hero.status}</span>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <Link to={`/library/${hero.slug}`} className="rounded-[4px] bg-ink px-4 py-2 text-[12px] font-semibold text-white hover:bg-ink-2">
              Read the report →
            </Link>
            {companionOf(hero) && (
              <Link to={`/library/${companionOf(hero)!.slug}`} className="rounded-[4px] border border-negative px-4 py-2 text-[12px] font-semibold text-negative hover:bg-bg-panel">
                The opposing essay (CRO)
              </Link>
            )}
          </div>
        </section>
      )}

      {/* ── Feature grid (asymmetric) ── */}
      {features.length > 0 && (
        <section className="grid grid-cols-1 border-y border-ink md:grid-cols-[1.15fr_1fr_1fr]">
          {features.map((r, i) => (
            <article key={r.slug} className={cn("py-7 md:py-8", i > 0 && "md:border-l md:border-rule md:pl-7")}>
              <span className="font-mono text-[11px] text-ink-3">{String(i + 1).padStart(2, "0")}</span>
              <span className="mt-3 block text-[9.5px] font-bold uppercase tracking-[0.18em] text-primary">
                {TYPE_KICKER[r.type] ?? r.type} · {r.subject || ""}
              </span>
              <h2 className="mt-2 font-display text-[20px] font-bold leading-[1.25] tracking-tight">
                <Link to={`/library/${r.slug}`} className="hover:text-primary">{r.title}</Link>
              </h2>
              {r.summary && <p className="mt-2 text-[12.5px] leading-[1.55] text-ink-2">{r.summary}</p>}
              <p className="mt-3 font-mono text-[10.5px] text-ink-3">
                {r.date}
                {companionOf(r) ? " · + opposing" : ""}
              </p>
            </article>
          ))}
        </section>
      )}

      {/* ── Latest stream ── */}
      <section className="mt-9">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h2 className="font-display text-[18px] font-bold">Latest intelligence</h2>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-ink-2">
            <label className="flex items-center gap-1.5">
              <span className="uppercase tracking-[0.08em]">Status</span>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2"
              >
                <option value="all">all</option>
                <option value="published">published</option>
                <option value="review">in review</option>
                <option value="draft">draft</option>
              </select>
            </label>
            <label className="flex items-center gap-1.5">
              <span className="uppercase tracking-[0.08em]">Type</span>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2"
              >
                <option value="all">all</option>
                {types.map((t) => (
                  <option key={t} value={t}>{TYPE_LABEL[t] ?? t}</option>
                ))}
              </select>
            </label>
          </div>
        </div>

        {visible.length === 0 ? (
          <div className="mt-4 rounded-md bg-bg-panel px-5 py-8">
            <p className="text-sm font-medium text-foreground">No reports here yet.</p>
            <p className="mt-1 text-[12.5px] text-ink-2">The research team's reports will appear as they pass review.</p>
          </div>
        ) : (
          <div className="mt-2">
            {visible.map((r) => (
              <Link
                key={r.slug}
                to={`/library/${r.slug}`}
                className="group grid grid-cols-[72px_1fr_auto] items-baseline gap-4 border-b border-rule px-1 py-3 hover:bg-bg-panel"
              >
                <span className="font-mono text-[11px] text-ink-3">{r.date}</span>
                <span className="font-display text-[15.5px] font-semibold tracking-tight group-hover:text-primary">{r.title}</span>
                <span className="hidden whitespace-nowrap text-[10px] uppercase tracking-[0.1em] text-ink-3 sm:block">
                  {seriesKey(r)}
                  {companionOf(r) ? <span className="text-negative"> + opposing</span> : ""}
                </span>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* ── Series chips ── */}
      <section className="mt-9 flex flex-wrap gap-2.5">
        <button
          type="button"
          onClick={() => setSeries(null)}
          className={cn(
            "rounded-full border px-3.5 py-1.5 text-[12px] transition-colors",
            series === null ? "border-ink bg-ink text-white" : "border-rule bg-bg-panel text-ink hover:border-ink"
          )}
        >
          All <span className="font-mono text-[10.5px] opacity-70">{published.length}</span>
        </button>
        {seriesList.map((s) => (
          <button
            key={s.name}
            type="button"
            onClick={() => setSeries(series === s.name ? null : s.name)}
            className={cn(
              "rounded-full border px-3.5 py-1.5 text-[12px] transition-colors",
              series === s.name ? "border-ink bg-ink text-white" : "border-rule bg-bg-panel text-ink hover:border-ink"
            )}
          >
            {s.name} <span className="font-mono text-[10.5px] opacity-70">{s.count} notes</span>
          </button>
        ))}
      </section>
    </div>
  );
}
