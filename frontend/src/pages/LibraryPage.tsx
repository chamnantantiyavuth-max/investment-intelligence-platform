import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getReports, type ReportMeta } from "@/api/reportClient";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";
import { LangToggle } from "@/components/LangToggle";
import { useLang } from "@/i18n/LanguageContext";
import { translate } from "@/i18n/translations";

/**
 * Research library — Feature Magazine index (FD #85, Direction B).
 * Hallmark-graded treatment of FD #84/B: single-rule masthead + hero feature +
 * asymmetric feature grid (01/02/03) + latest stream + series chips + Ft1 footer.
 * Text/typography-driven editorial; no imagery (FD #84 — AI art rejected).
 * Bilingual: Thai default / English toggle (10 Aug 2026).
 */

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
  const { lang } = useLang();
  const [status, setStatus] = useState("all");
  const [type, setType] = useState("all");
  const [series, setSeries] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState("date_desc");

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

  /** Localized display helpers — Thai title/summary when present (10 Aug 2026). */
  const tTitle = (r: ReportMeta) => (lang === "th" && r.title_th ? r.title_th : r.title);
  const tSummary = (r: ReportMeta) => (lang === "th" && r.summary_th ? r.summary_th : r.summary);

  const hero = mains[0] ?? published[0];
  const features = mains.filter((r) => r.slug !== hero?.slug).slice(0, 3);
  const rest = published.filter((r) => r.slug !== hero?.slug && !features.some((f) => f.slug === r.slug));

  const visible = useMemo(() => {
    let list = rest;
    if (status !== "all") list = list.filter((r) => r.status === status);
    if (type !== "all") list = list.filter((r) => r.type === type);
    if (series) list = list.filter((r) => seriesKey(r) === series);
    const q = search.trim().toLowerCase();
    if (q) {
      list = list.filter(
        (r) =>
          r.title.toLowerCase().includes(q) ||
          (r.subject ?? "").toLowerCase().includes(q) ||
          (r.author ?? "").toLowerCase().includes(q) ||
          r.date.includes(q)
      );
    }
    const sorted = [...list];
    switch (sortBy) {
      case "date_asc":
        sorted.sort((a, b) => a.date.localeCompare(b.date));
        break;
      case "title":
        sorted.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case "series":
        sorted.sort((a, b) => seriesKey(a).localeCompare(seriesKey(b)) || b.date.localeCompare(a.date));
        break;
      default: // date_desc
        sorted.sort((a, b) => b.date.localeCompare(a.date));
    }
    return sorted;
  }, [rest, status, type, series, search, sortBy]);

  /** True companion: the other half of a main/opposing pair (base-slug match, same subject). */
  const companionOf = (r: ReportMeta) => {
    const base = r.slug.replace(/-opposing$/, "");
    const pairSlug = r.slug.endsWith("-opposing") ? base : `${base}-opposing`;
    return published.find((o) => o.slug === pairSlug && o.subject === r.subject && o.slug !== r.slug);
  };

  const today = useMemo(
    () =>
      new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }),
    []
  );

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error)
    return (
      <div className="flex min-h-screen flex-col bg-bg-page">
        <div className="mx-auto w-full max-w-[1120px] flex-1 px-6 py-8">
          <p className="text-sm font-medium text-negative">
            {lang === "th" ? "ไม่สามารถโหลดคลังบทวิเคราะห์ได้" : "Could not load the research library."}
          </p>
          <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
            {lang === "th" ? "ลองอีกครั้ง →" : "Retry →"}
          </button>
        </div>
      </div>
    );

  return (
    <div className="flex min-h-screen flex-col bg-bg-page">
      <div className="mx-auto w-full max-w-[1120px] flex-1 px-6 py-6">
        {/* ── Masthead (single-rule, FD #85/B) ── */}
        <header className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-b border-ink py-4">
          <span className="font-display text-[clamp(20px,3vw,26px)] font-bold tracking-tight">
            {translate("library.brand", lang)}<span className="text-primary">.</span>
          </span>
          <span className="flex items-baseline gap-3">
            <span className="font-mono text-[11px] text-ink-3" data-testid="library-count">
              {translate("library.published", lang, { n: published.length, date: today })}
            </span>
            <LangToggle />
          </span>
          <nav className="flex flex-wrap gap-x-5 gap-y-1 text-[11px] font-semibold uppercase tracking-[0.1em] text-ink-2" aria-label="Series">
            {["Apple", "Silver", "Gold", "JNJ", "Weekly"].map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => {
                  setSeries(series === s ? null : s);
                  setStatus("all");
                  setType("all");
                }}
                className={cn("whitespace-nowrap hover:text-primary", series === s && "text-primary")}
              >
                {s}
              </button>
            ))}
          </nav>
        </header>

        {/* ── Hero feature ── */}
        {hero && (
          <section className="py-10">
            <div className="flex flex-wrap items-center gap-3">
              <span className="rounded-[2px] bg-primary px-2 py-0.5 text-[9.5px] font-bold uppercase tracking-[0.12em] text-white">
                {translate("library.featured", lang)}
              </span>
              <span className="font-mono text-[10.5px] uppercase tracking-[0.14em] text-primary">
                {translate(`library.typeKicker.${hero.type}` as const, lang) ?? hero.type} · {hero.subject || ""}
              </span>
            </div>
            <h1 className="mt-4 max-w-[900px] font-display text-[clamp(30px,5.5vw,52px)] font-bold leading-[1.06] tracking-[-0.015em]">
              <Link to={`/library/${hero.slug}`} className="hover:text-primary">{tTitle(hero)}</Link>
            </h1>
            {tSummary(hero) && <p className="mt-4 max-w-[760px] text-[16.5px] leading-[1.6] text-ink-2">{tSummary(hero)}</p>}
            <div className="mt-5 flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-[11px] text-ink-3">
              <span className="text-[10.5px] font-semibold uppercase tracking-[0.1em] text-ink-2">{hero.author}</span>
              <span className="text-rule">|</span>
              <span>{hero.date}</span>
              <span className="text-rule">|</span>
              <span className={cn("font-semibold", statusTone(hero.status))}>● {hero.status}</span>
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link to={`/library/${hero.slug}`} className="bg-ink px-4 py-2 text-[12.5px] font-semibold text-white hover:bg-primary">
                {translate("library.readReport", lang)}
              </Link>
              {companionOf(hero) && (
                <Link to={`/library/${companionOf(hero)!.slug}`} className="border border-ink-3 px-4 py-2 text-[12.5px] font-semibold text-ink-2 hover:border-primary hover:text-primary">
                  {translate("library.opposing", lang)}
                </Link>
              )}
            </div>
          </section>
        )}

        {/* ── Feature grid (asymmetric 01/02/03) ── */}
        {features.length > 0 && (
          <section>
            <div className="border-t-2 border-ink pt-2">
              <h2 className="font-display text-[20px] font-bold">{translate("library.weekNotes", lang)}</h2>
            </div>
            <div className="mt-4 grid grid-cols-1 gap-x-7 gap-y-8 md:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)_minmax(0,1fr)]">
              {features.map((r, i) => (
                <article key={r.slug} className="border-t border-rule pt-2">
                  <span className="font-mono text-[11px] text-ink-3">{String(i + 1).padStart(2, "0")}</span>
                  <span className="mt-2 block font-mono text-[9.5px] uppercase tracking-[0.14em] text-primary">
                    {translate(`library.typeKicker.${r.type}` as const, lang)} · {r.subject || ""}
                  </span>
                  <h3 className="mt-2 font-display text-[18px] font-bold leading-[1.25] tracking-tight">
                    <Link to={`/library/${r.slug}`} className="hover:text-primary">{tTitle(r)}</Link>
                  </h3>
                  {tSummary(r) && <p className="mt-2 text-[13.5px] leading-[1.55] text-ink-2">{tSummary(r)}</p>}
                  <p className="mt-2 font-mono text-[10.5px] text-ink-3">
                    {r.date}
                    {companionOf(r) ? ` · ${translate("library.opposingShort", lang)}` : ""}
                  </p>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* ── Latest stream ── */}
        <section className="mt-10">
          <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2 border-t border-ink py-3">
            <h2 className="font-display text-[20px] font-bold">{translate("library.latest", lang)}</h2>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-[11px] text-ink-2">
              <label className="flex items-center gap-1.5">
                <span className="uppercase tracking-[0.08em]">{translate("library.search", lang)}</span>
                <input
                  type="search"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder={lang === "th" ? "ชื่อเรื่อง, หัวข้อ, ผู้เขียน…" : "title, subject, author…"}
                  className="w-44 rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2 placeholder:text-ink-3"
                />
              </label>
              <label className="flex items-center gap-1.5">
                <span className="uppercase tracking-[0.08em]">{translate("library.status", lang)}</span>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2"
                >
                  <option value="all">{translate("library.statusAll", lang)}</option>
                  <option value="published">{translate("library.statusPublished", lang)}</option>
                  <option value="review">{translate("library.statusReview", lang)}</option>
                  <option value="draft">{translate("library.statusDraft", lang)}</option>
                </select>
              </label>
              <label className="flex items-center gap-1.5">
                <span className="uppercase tracking-[0.08em]">{translate("library.type", lang)}</span>
                <select
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  className="rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2"
                >
                  <option value="all">{translate("library.statusAll", lang)}</option>
                  {types.map((t) => (
                    <option key={t} value={t}>{translate(`library.typeLabel.${t}` as const, lang)}</option>
                  ))}
                </select>
              </label>
              <label className="flex items-center gap-1.5">
                <span className="uppercase tracking-[0.08em]">{translate("library.sort", lang)}</span>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2"
                >
                  <option value="date_desc">{translate("library.sortNewest", lang)}</option>
                  <option value="date_asc">{translate("library.sortOldest", lang)}</option>
                  <option value="title">{translate("library.sortTitle", lang)}</option>
                  <option value="series">{translate("library.sortSeries", lang)}</option>
                </select>
              </label>
            </div>
          </div>

          {visible.length === 0 ? (
            <div className="mt-4 border-t border-rule py-8">
              <p className="text-sm font-medium text-foreground">{translate("library.emptyTitle", lang)}</p>
              <p className="mt-1 text-[12.5px] text-ink-2">
                {translate("library.emptyBody", lang)}
              </p>
              <button
                type="button"
                onClick={() => { setSearch(""); setStatus("all"); setType("all"); setSeries(null); }}
                className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary hover:text-foreground"
              >
                {translate("library.clearFilters", lang)}
              </button>
            </div>
          ) : (
            <div>
              {visible.map((r) => (
                <Link
                  key={r.slug}
                  to={`/library/${r.slug}`}
                  className="group grid grid-cols-1 items-baseline gap-1 border-b border-rule px-1 py-3 hover:bg-bg-panel sm:grid-cols-[92px_minmax(0,1fr)_auto] sm:gap-4"
                >
                  <span className="font-mono text-[11px] text-ink-3">{r.date}</span>
                  <span className="font-display text-[15.5px] font-semibold tracking-tight group-hover:text-primary">{tTitle(r)}</span>
                  <span className="hidden whitespace-nowrap font-mono text-[10px] uppercase tracking-[0.1em] text-ink-3 sm:block">
                    {seriesKey(r)}
                    {companionOf(r) ? <span className="text-negative"> {translate("library.opposingShort", lang)}</span> : ""}
                  </span>
                </Link>
              ))}
            </div>
          )}
        </section>

        {/* ── Series chips (tonal) ── */}
        <section className="mt-10 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setSeries(null)}
            className={cn(
              "px-3.5 py-1.5 text-[12.5px] font-medium transition-colors",
              series === null ? "bg-ink text-white" : "bg-bg-panel text-ink hover:bg-ink hover:text-white"
            )}
          >
            {translate("library.all", lang)} <span className="font-mono text-[10.5px] opacity-70">{published.length}</span>
          </button>
          {seriesList.map((s) => (
            <button
              key={s.name}
              type="button"
              onClick={() => setSeries(series === s.name ? null : s.name)}
              className={cn(
                "px-3.5 py-1.5 text-[12.5px] font-medium transition-colors",
                series === s.name ? "bg-ink text-white" : "bg-bg-panel text-ink hover:bg-ink hover:text-white"
              )}
            >
              {s.name} <span className="font-mono text-[10.5px] opacity-70">{s.count} {translate("library.notes", lang)}</span>
            </button>
          ))}
        </section>

        {/* ── Ft1 Mast-headed footer ── */}
        <footer className="mt-14 border-t-2 border-ink pt-6">
          <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-2">
            <span className="font-display text-[20px] font-bold tracking-tight">
              {translate("library.brand", lang)}<span className="text-primary">.</span>
            </span>
            <span className="font-display text-[15px] text-ink-2">{translate("library.tagline", lang)}</span>
          </div>
          <nav className="mt-3 flex flex-wrap gap-x-6 gap-y-1 text-[11px] font-semibold uppercase tracking-[0.1em] text-ink-2" aria-label="Footer">
            <Link to="/library" className="whitespace-nowrap hover:text-primary">{translate("library.brand", lang)}</Link>
            <Link to="/org-office" className="whitespace-nowrap hover:text-primary">{translate("org.title", lang)}</Link>
            <Link to="/kanban" className="whitespace-nowrap hover:text-primary">{translate("kanban.title", lang)}</Link>
            <Link to="/library" className="whitespace-nowrap hover:text-primary">{translate("library.typeLabel.weekly", lang)}</Link>
          </nav>
          <p className="mt-3 font-mono text-[10.5px] text-ink-3">
            {translate("library.footerLine", lang, { n: published.length })}
          </p>
        </footer>
      </div>
    </div>
  );
}
