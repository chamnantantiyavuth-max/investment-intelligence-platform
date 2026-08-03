import { useQuery } from "@tanstack/react-query"
import { HeroInsight } from "@/components/HeroInsight"
import { ProvenanceChip } from "@/components/ProvenanceChip"
import { StatusBadge } from "@/components/StatusBadge"
import { ExplainPanel } from "@/components/ExplainPanel"
import { EmptyState } from "@/components/EmptyState"
import { AdvisoryFooter } from "@/components/AdvisoryFooter"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMQueue } from "@/api/amClient"
import type { CandidateSummary } from "@/types/am"

/** Approved spec §4.2 stage table (version-stamped — display only, never a rule source). */
const STAGES: { stage: string; desc: string; owner: string }[] = [
  { stage: "Universe Definition", desc: "Select the controlled US-listed universe for the pipeline run", owner: "Alpha Momentum" },
  { stage: "Theme-linked Selection", desc: "Candidates linked to active Approved Themes via Candidate–Theme relationships; Shared Core supplies roles", owner: "Alpha Momentum" },
  { stage: "Candidate Quality Assessment", desc: "Fundamentals, growth, liquidity, relative strength, trend quality, accumulation, industry leadership", owner: "Alpha Momentum" },
  { stage: "Entry Readiness Assessment", desc: "Price structure, base quality, breakout proximity, volume behavior, volatility contraction, extension risk", owner: "Alpha Momentum" },
  { stage: "Data Confidence Assessment", desc: "Freshness, completeness, reliability, conflicts, missing data", owner: "Shared Core" },
  { stage: "Research Queue Assembly", desc: "Order by Theme, then strategy-owned prioritization within each Theme", owner: "Alpha Momentum" },
]

type Dim = [string, keyof CandidateSummary["candidate_quality"] | keyof CandidateSummary["entry_readiness"] | keyof CandidateSummary["data_confidence"]]

const DIMENSIONS: { title: string; note: string; rows: Dim[] }[] = [
  {
    title: "Candidate Quality",
    note: "Spec §4.2 — qualitative strings, no composite score (CANDIDATE §2.5)",
    rows: [
      ["Fundamentals", "fundamentals"],
      ["Growth", "growth"],
      ["Liquidity", "liquidity"],
      ["Relative Strength", "relative_strength"],
      ["Trend Quality", "trend_quality"],
      ["Accumulation", "accumulation"],
      ["Industry Leadership", "industry_leadership"],
    ],
  },
  {
    title: "Entry Readiness",
    note: "Price structure / base / breakout — readiness, not a buy signal",
    rows: [
      ["Price Structure", "price_structure"],
      ["Base Quality", "base_quality"],
      ["Breakout Proximity", "breakout_proximity"],
      ["Volume Behavior", "volume_behavior"],
      ["Volatility Contraction", "volatility_contraction"],
      ["Extension Risk", "extension_risk"],
    ],
  },
  {
    title: "Data Confidence",
    note: "Freshness / completeness / reliability of underlying data",
    rows: [
      ["Freshness", "freshness"],
      ["Completeness", "completeness"],
      ["Reliability", "reliability"],
      ["Conflicts", "conflicts"],
      ["Missing Data", "missing_data"],
    ],
  },
]

function MatrixCard({ title, note, rows, candidates }: { title: string; note: string; rows: Dim[]; candidates: (CandidateSummary & { _theme: string })[] }) {
  return (
    <Card>
      <CardHeader className="space-y-0 pb-2">
        <CardTitle className="text-sm">{title}</CardTitle>
        <p className="text-[11px] text-muted-foreground">{note}</p>
      </CardHeader>
      <CardContent className="overflow-x-auto p-0">
        <table className="w-full min-w-[560px] border-collapse text-xs">
          <thead>
            <tr className="border-b border-border">
              <th className="sticky left-0 bg-card px-3 py-2 text-left font-medium text-muted-foreground">Criteria</th>
              {candidates.map((c) => (
                <th key={c.id} className="px-2 py-2 text-center font-mono font-semibold text-foreground">
                  {c.ticker}
                  <span className="block text-[10px] font-normal text-muted-foreground">{c._theme}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map(([label, key]) => (
              <tr key={label} className="border-b border-border/60 last:border-0">
                <td className="sticky left-0 bg-card px-3 py-1.5 text-muted-foreground">{label}</td>
                {candidates.map((c) => {
                  const bucket = key in c.candidate_quality ? c.candidate_quality : key in c.entry_readiness ? c.entry_readiness : c.data_confidence
                  const v = String((bucket as Record<string, unknown>)[key] ?? "—")
                  return (
                    <td key={c.id} className="px-2 py-1.5 text-center">
                      <StatusBadge value={v} className="max-w-[110px] truncate" />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  )
}

export default function AMScreenerPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["am-screener"],
    queryFn: getAMQueue,
    staleTime: 5 * 60 * 1000,
  })

  if (isLoading) return <Skeleton className="h-96 w-full" />
  if (error)
    return (
      <div>
        <h1 className="font-mono text-lg font-semibold">AM Criteria Screener</h1>
        <div className="mt-3 rounded-2xl bg-negative/[0.06] px-5 py-6 text-center">
          <p className="text-sm text-negative">Failed to load screener data.</p>
        </div>
      </div>
    )

  const candidates = (data?.themes ?? []).flatMap((t) =>
    (t.candidates ?? []).map((c) => ({ ...c, _theme: t.theme.id }))
  ) as (CandidateSummary & { _theme: string })[]
  const provenance = data?.themes[0]?.theme.provenance

  // Data stories from real fields — display only, no invented pass/fail verdicts.
  const dataStories: { kicker: string; headline: string; value: string; tone: "warning" | "negative" | "info" }[] = []
  const incomplete = candidates.find((c) => /incomplete/i.test(c.data_confidence.completeness))
  if (incomplete) {
    dataStories.push({
      kicker: "Data story",
      headline: `${incomplete.ticker} runs the thinnest data set`,
      value: incomplete.data_confidence.completeness,
      tone: "warning",
    })
  }
  const stage4 = candidates.find((c) => /stage 4/i.test(c.entry_readiness.price_structure))
  if (stage4) {
    dataStories.push({
      kicker: "Structure story",
      headline: `${stage4.ticker} is in Stage 4 — declining`,
      value: stage4.entry_readiness.price_structure,
      tone: "negative",
    })
  }
  const extended = candidates.find((c) => /high/i.test(c.entry_readiness.extension_risk) && !/below/.test(c.entry_readiness.extension_risk))
  if (extended) {
    dataStories.push({
      kicker: "Risk story",
      headline: `${extended.ticker} is extended from its base`,
      value: extended.entry_readiness.extension_risk,
      tone: "warning",
    })
  }

  return (
    <div>
      <HeroInsight
        kicker="AM Criteria Screener"
        headline="The full rule pack, rendered against every candidate"
        display={`${candidates.length} × 18`}
        tone="info"
        sub={`${candidates.length} candidates assessed on 18 approved criteria — 7 candidate-quality, 6 entry-readiness, 5 data-confidence (spec §4.2). Every cell is the pipeline's qualitative string; nothing is summed into a score.`}
        chips={<ProvenanceChip mode={provenance?.mode} source={provenance?.source} asOf={data?.point_in_time} />}
      />

      <div className="mb-4 rounded-2xl bg-warning/[0.06] px-5 py-3 text-xs text-warning">
        Criteria source: ALPHA-MOMENTUM-V0-SPEC.md v0.1 (approved, FD #19/#20) — rendered as-is. Exact
        formulas, weights, and thresholds remain deferred (spec §4.3). No invented rules.
      </div>

      {dataStories.length > 0 && (
        <section className="mb-4 grid grid-cols-1 gap-3 sm:grid-cols-3">
          {dataStories.map((s) => (
            <div key={s.headline} className="rounded-2xl bg-elevated/50 px-4 py-3">
              <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
                {s.kicker}
              </span>
              <p className="mt-1 text-sm font-semibold text-foreground">{s.headline}</p>
              <p className="mt-0.5 font-mono text-xs text-warning">{s.value}</p>
            </div>
          ))}
        </section>
      )}

      <Card className="mb-3">
        <CardHeader className="space-y-0 pb-2">
          <CardTitle className="text-sm">Pipeline Stages (spec §4.1)</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-1.5">
            {STAGES.map((s, i) => (
              <span key={s.stage} className="flex items-center gap-1.5">
                <span
                  className="rounded-md border border-border bg-card px-2 py-1 text-[11px] font-medium text-foreground"
                  title={`${s.desc} — owner: ${s.owner}`}
                >
                  {s.stage}
                </span>
                {i < STAGES.length - 1 && <span className="text-muted-foreground">→</span>}
              </span>
            ))}
          </div>
          <p className="mt-2 text-[11px] text-muted-foreground">
            Theme-linked demonstration boundary only — future versions preserve stock-first discovery
            (spec §4.4). Feature computations are deterministic and reproducible (Constitution §20).
          </p>
        </CardContent>
      </Card>

      {candidates.length === 0 ? (
        <EmptyState message="No candidates to screen." sub="The controlled set currently has no admitted candidates." />
      ) : (
        <div className="space-y-3">
          {DIMENSIONS.map((d) => (
            <MatrixCard key={d.title} title={d.title} note={d.note} rows={d.rows} candidates={candidates} />
          ))}
        </div>
      )}

      <ExplainPanel title="How to read the matrix">
        Rows are the approved screening criteria (spec §4.2); columns are candidates from the admitted
        run. Every cell is the qualitative assessment string produced by the deterministic pipeline —
        rendered as a badge, never summed. The four quality dimensions stay separate (Constitution §10):
        Candidate Quality, Entry Readiness, Data Confidence here, Theme Quality on the Theme Card. A
        "pass" is not a recommendation — entry readiness is not a buy signal (Constitution §1).
      </ExplainPanel>

      <AdvisoryFooter provenance={`${data?.run_id ?? "—"} · REAL EOD — YAHOO FINANCE — V0.5 development only`} />
    </div>
  )
}
