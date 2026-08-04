import { useMemo } from "react"
import { useQuery } from "@tanstack/react-query"
import { HeroInsight } from "@/components/HeroInsight"
import { FindingCard } from "@/components/FindingCard"
import { ProvenanceChip } from "@/components/ProvenanceChip"
import { StatusBadge } from "@/components/StatusBadge"
import { ExplainPanel } from "@/components/ExplainPanel"
import { EmptyState } from "@/components/EmptyState"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMQueue } from "@/api/amClient"
import { rankCandidates, lifecycleCounts, leadershipCount } from "@/lib/insights"
import type { ThemeWithCandidates } from "@/types/am"

/** Deep-dive tier: one theme as a tonal panel (theme-first — Constitution §14). */
function ThemeCardView({ tc }: { tc: ThemeWithCandidates }) {
  const t = tc.theme
  const candidates = tc.candidates ?? []
  return (
    <div className="rounded-md bg-bg-panel px-5 py-4">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="font-mono text-[11px] text-ink-2">{t.id}</span>
            <StatusBadge value={t.lifecycle} />
            <StatusBadge value={t.approval_status} />
            <StatusBadge value={t.monitoring_status} />
            <StatusBadge value={t.confidence} />
          </div>
          <h3 className="mt-1.5 text-base font-semibold leading-snug text-foreground">{t.name}</h3>
        </div>
        <Button variant="ghost" size="icon-sm" aria-label={`Open theme ${t.id}`} render={<Link to={`/am-theme/${t.id}`} />}>
          <ArrowRight className="size-4" />
        </Button>
      </div>
      <p className="mt-2 text-[13px] leading-relaxed text-ink-2">{t.why_now}</p>
      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[11px] text-ink-2">
        <span>
          <span className="font-mono text-foreground">{t.stocks_in_industry}</span> stocks in industry
        </span>
        <span>
          <span className="font-mono text-foreground">{t.key_tickers.join(", ")}</span> key tickers
        </span>
        <span>
          <span className="font-mono text-foreground">{candidates.length}</span> candidate{candidates.length === 1 ? "" : "s"}
        </span>
      </div>
      {candidates.length > 0 && (
        <div className="mt-2 space-y-1.5 border-t border-rule pt-2">
          {candidates.map((c) => (
            <div key={c.id} className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-[11px] lg:grid-cols-3">
              <div className="flex items-center gap-1.5">
                <span className="font-mono text-xs font-semibold text-foreground">{c.ticker}</span>
                <StatusBadge value={c.conviction_level} />
              </div>
              <span className="text-ink-2">
                RS <span className="font-mono text-foreground">{c.candidate_quality.relative_strength}</span>
                {" · "}Trend <span className="font-mono text-foreground">{c.candidate_quality.trend_quality}</span>
              </span>
              <span className="text-ink-2">
                Base <span className="font-mono text-foreground">{c.entry_readiness.base_quality}</span>
                {" · "}Breakout <span className="font-mono text-foreground">{c.entry_readiness.breakout_proximity}</span>
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function AMQueuePage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["am-queue"],
    queryFn: getAMQueue,
    staleTime: 5 * 60 * 1000,
  })

  const top = useMemo(() => (data ? rankCandidates(data.themes)[0] : undefined), [data])
  // C4 fix: provenance from the RANKED theme, not themes[0]
  const topTheme = useMemo(() => data?.themes.find((t) => t.theme.id === top?.themeId), [data, top])
  const topProv = topTheme?.theme.provenance
  const lifecycle = useMemo(() => (data ? lifecycleCounts(data.themes) : []), [data])
  const leaders = useMemo(() => (data ? leadershipCount(data.themes) : 0), [data])

  if (isLoading) return <Skeleton className="h-96 w-full" />
  if (error)
    return (
      <div>
        <h1 className="font-display text-h2 font-bold">Alpha Momentum Queue</h1>
        <div className="mt-3 rounded-md bg-bg-panel px-5 py-6 text-center">
          <p className="text-sm font-medium text-negative">Failed to load Alpha Momentum Queue</p>
          <p className="mt-1 text-xs text-ink-2">What failed: the AM queue endpoint (fail-closed 503). Nothing else is affected.</p>
          <button onClick={() => refetch()} className="mt-2 text-sm text-primary underline">
            Retry
          </button>
        </div>
      </div>
    )

  const themes = data?.themes ?? []
  const candidatesTotal = themes.reduce((n, t) => n + (t.candidates?.length ?? 0), 0)
  const prov = themes[0]?.theme.provenance
  const topStage = lifecycle[0]
  const runId = data?.run_id

  return (
    <div>
      {top ? (
        <HeroInsight
          kicker="Alpha Momentum · Queue"
          headline="Closest to a breakout in the current run"
          display={top.ticker}
          tone="positive"
          sub={`${top.conviction} conviction · ${top.themeName} (${top.lifecycle}) · RS ${top.rs} · Base ${top.base} · Breakout ${top.breakout}. ${top.whyNow}`}
          evidenceRef={`${runId} · ${top.themeId}`}
          chips={
            <ProvenanceChip
              mode={topProv?.hybrid ? "hybrid" : topProv?.mode}
              source={topProv?.source}
              asOf={data?.point_in_time}
            />
          }
        />
      ) : (
        <HeroInsight
          kicker="Alpha Momentum · Queue"
          headline="No admitted run to rank"
          display="—"
          tone="info"
          sub="Run the pipeline to populate the queue."
        />
      )}

      <section className="grid grid-cols-1 gap-x-10 gap-y-1 md:grid-cols-2">
        <FindingCard
          featured
          kicker="Finding 01 · Momentum"
          headline="Leadership is concentrated"
          value={`${leaders}/${themes.length} themes`}
          tone="positive"
          why={`${leaders} of ${themes.length} themes sit in Emerging Leadership or Expansion — the stages where the strongest candidates concentrate.`}
          evidenceRef={runId}
        />
        <FindingCard
          kicker="Finding 02 · Data"
          headline="Coverage on this run"
          value={prov?.coverage ?? "—"}
          tone="info"
          why={`Source: ${prov?.source ?? "—"} · point-in-time ${data?.point_in_time ?? "—"}. Data confidence is per-candidate and always visible.`}
          evidenceRef={runId}
        />
        <FindingCard
          kicker="Finding 03 · Queue"
          headline="Candidates under investigation"
          value={`${candidatesTotal} across ${themes.length} themes`}
          tone="neutral"
          why={
            topStage
              ? `Most common lifecycle stage: ${topStage[0]} (${topStage[1]} theme${topStage[1] === 1 ? "" : "s"}).`
              : "Theme-first queue with adaptive capacity (Constitution §14)."
          }
          evidenceRef={runId}
        />
      </section>

      {themes.length === 0 ? (
        <EmptyState
          message="No themes in the queue."
          sub="Queue capacity is adaptive — it may return zero high-priority candidates (Constitution §14)."
        />
      ) : (
        <section className="mt-8">
          <h2 className="mb-2 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
            Reference · Themes
          </h2>
          <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
            {themes.map((tc) => (
              <ThemeCardView key={tc.theme.id} tc={tc} />
            ))}
          </div>
        </section>
      )}

      <ExplainPanel title="How Alpha Momentum screens">
        Six pipeline stages (spec §4.1, v0.1): Universe Definition → Theme-linked Selection → Candidate
        Quality → Entry Readiness → Data Confidence → Research Queue Assembly. Every candidate is
        assessed on 7 quality, 6 entry-readiness, and 5 data-confidence dimensions — all qualitative
        badges, never a composite score (Constitution §10, CANDIDATE §2.5). The queue is Theme-first
        (§14). Exact formulas and thresholds are deferred (spec §4.3). See the{" "}
        <Link to="/am-screener" className="text-primary underline">
          criteria screener
        </Link>
        .
      </ExplainPanel>
    </div>
  )
}
