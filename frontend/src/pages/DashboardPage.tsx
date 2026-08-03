import { useEffect, useMemo, useState } from "react"
import { HeroInsight } from "@/components/HeroInsight"
import { FindingCard } from "@/components/FindingCard"
import { ProvenanceChip } from "@/components/ProvenanceChip"
import { StalenessBanner } from "@/components/StalenessBanner"
import { AdvisoryFooter } from "@/components/AdvisoryFooter"
import { ExplainPanel } from "@/components/ExplainPanel"
import { TrendingUp, Shield, Building2, Landmark } from "lucide-react"
import {
  getDashboardSummary,
  type DashboardSummary,
  type ComponentProvenance,
} from "@/api/dashboardClient"
import { getAMQueue } from "@/api/amClient"
import { rankCandidates, lifecycleCounts, leadershipCount } from "@/lib/insights"

// Operational staleness bounds (FD #47 D3 — not investment rules)
const STALE_BOUNDS: Record<string, number> = { am: 7, fo: 30, ii: 120 }

function daysSince(iso?: string | null): number | null {
  if (!iso) return null
  const t = new Date(iso).getTime()
  if (Number.isNaN(t)) return null
  return Math.floor((Date.now() - t) / 86_400_000)
}

function modeFor(comp: ComponentProvenance): "real" | "synthetic" | null {
  if (comp.state === "unavailable") return null
  const ds = (comp.data_source ?? comp.source ?? "").toLowerCase()
  return ds.startsWith("real") ? "real" : "synthetic"
}

const lifecycleBarTone: Record<string, string> = {
  "Weak Signal": "bg-info",
  Formation: "bg-info",
  "Emerging Leadership": "bg-positive",
  Expansion: "bg-positive",
  "Crowded / Late Stage": "bg-warning",
  Deterioration: "bg-negative",
}

function EngineChip({
  name,
  icon,
  comp,
  bound,
}: {
  name: string
  icon: React.ReactNode
  comp: ComponentProvenance
  bound?: number
}) {
  const mode = modeFor(comp)
  const stale = daysSince(comp.point_in_time)
  const staleOver = bound !== undefined && stale !== null && stale > bound
  return (
    <div className="rounded-xl bg-elevated/50 px-4 py-3">
      <div className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-2 text-sm font-medium text-foreground">
          <span className="text-muted-foreground">{icon}</span>
          {name}
        </span>
        <ProvenanceChip mode={mode} source={comp.data_source ?? comp.source} asOf={comp.point_in_time} />
      </div>
      <div className="mt-1.5 flex items-center justify-between gap-2 text-[11px]">
        <span className="font-mono text-muted-foreground">
          {comp.state === "unavailable" ? "UNAVAILABLE — no admitted artifact" : comp.run_id ?? "—"}
        </span>
        {stale !== null && comp.state === "available" && (
          <span className={staleOver ? "font-mono text-warning" : "font-mono text-muted-foreground"}>
            {stale}d{bound !== undefined ? ` ≤ ${bound}d` : ""}
          </span>
        )}
      </div>
    </div>
  )
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [am, setAm] = useState<Awaited<ReturnType<typeof getAMQueue>> | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    getDashboardSummary().then(setData).catch(() => setError(true))
    getAMQueue().then(setAm).catch(() => setAm(null))
  }, [])

  const top = useMemo(() => (am ? rankCandidates(am.themes)[0] : undefined), [am])
  const lifecycle = useMemo(() => (am ? lifecycleCounts(am.themes) : []), [am])
  const leaders = useMemo(() => (am ? leadershipCount(am.themes) : 0), [am])

  if (error) return <p className="text-sm text-negative">Dashboard unavailable — API error</p>
  if (!data) return <p className="text-sm text-muted-foreground">Loading dashboard…</p>

  const staleWarnings: string[] = []
  for (const key of ["am", "fo", "ii"] as const) {
    const c = data.components[key]
    const d = daysSince(c.point_in_time)
    const bound = STALE_BOUNDS[key]
    if (c.state === "available" && d !== null && d > bound) {
      staleWarnings.push(`${key.toUpperCase()} data is ${d}d old (bound ${bound}d, FD #47 D3)`)
    }
  }
  const maxLifecycle = Math.max(1, ...lifecycle.map(([, n]) => n))
  const candidatesTotal = (am?.themes ?? []).reduce((n, t) => n + (t.candidates?.length ?? 0), 0)

  return (
    <div>
      {staleWarnings.length > 0 && <StalenessBanner message={staleWarnings.join(" · ")} />}

      {top ? (
        <HeroInsight
          kicker="Top setup · Alpha Momentum"
          headline="The most interesting setup right now"
          display={top.ticker}
          tone="positive"
          sub={`${top.conviction} conviction · ${top.themeName} (${top.lifecycle}) · RS ${top.rs} · Base ${top.base} · Breakout ${top.breakout}. ${top.whyNow}`}
          chips={
            <ProvenanceChip
              mode={am?.themes[0]?.theme.provenance.mode}
              source={am?.themes[0]?.theme.provenance.source}
              asOf={am?.themes[0]?.theme.provenance.as_of}
            />
          }
        />
      ) : (
        <HeroInsight
          kicker="Strategy Control Center"
          headline="The engine is up — awaiting an admitted Alpha Momentum run"
          display="—"
          tone="info"
          sub="Engine provenance below shows each strategy's artifact state."
        />
      )}

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <FindingCard
          featured
          kicker="Finding 01 · Momentum"
          headline="Leadership lives in the pipeline right now"
          value={am ? `${leaders}/${am.themes.length} themes` : "—"}
          tone="positive"
          why={`${leaders} of ${am?.themes.length ?? "—"} themes sit in Emerging Leadership or Expansion — the stages where the strongest candidates concentrate.`}
        />
        <FindingCard
          kicker="Finding 02 · Data"
          headline="Coverage on the admitted run"
          value={am?.themes[0]?.theme.provenance.coverage ?? "—"}
          tone="info"
          why="Real EOD from Yahoo Finance, point-in-time 2026-08-03. Staleness bounds: AM ≤7d, FO ≤30d, II ≤120d (FD #47 D3)."
        />
        <FindingCard
          kicker="Finding 03 · Close System"
          headline="Regime reads risk-on"
          value={data.cs_regime}
          tone="warning"
          why={`${data.cs_qc_met}/${data.cs_radar_items} radar items meet Q-conditions. Synthetic demo — labeled, never disguised (FD #46).`}
        />
        <FindingCard
          kicker="Finding 04 · Queue"
          headline="Candidates under investigation"
          value={`${candidatesTotal} across ${data.queue_size} themes`}
          tone="neutral"
          why="Theme-first queue with adaptive capacity — it may return zero high-priority candidates (Constitution §14)."
        />
      </section>

      <section className="mt-6">
        <h2 className="mb-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          Reference · Engine provenance
        </h2>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-4">
          <EngineChip name="Alpha Momentum" icon={<TrendingUp className="size-4" />} comp={data.components.am} bound={STALE_BOUNDS.am} />
          <EngineChip name="Close System" icon={<Shield className="size-4" />} comp={data.components.cs} />
          <EngineChip name="Fundamental & Opportunity" icon={<Building2 className="size-4" />} comp={data.components.fo} bound={STALE_BOUNDS.fo} />
          <EngineChip name="Institutional" icon={<Landmark className="size-4" />} comp={data.components.ii} bound={STALE_BOUNDS.ii} />
        </div>
      </section>

      {lifecycle.length > 0 && (
        <section className="mt-3 rounded-xl bg-elevated/50 px-4 py-3">
          <h2 className="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
            Theme lifecycle breadth
          </h2>
          <div className="mt-2 space-y-2">
            {lifecycle.map(([stage, n]) => (
              <div key={stage} className="space-y-0.5">
                <div className="flex justify-between text-[11px] text-muted-foreground">
                  <span>{stage}</span>
                  <span className="font-mono">{n}</span>
                </div>
                <div className="h-1.5 w-full rounded-full bg-muted">
                  <div
                    className={`h-1.5 rounded-full ${lifecycleBarTone[stage] ?? "bg-info"}`}
                    style={{ width: `${(n / maxLifecycle) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      <ExplainPanel title="What is this app">
        IIP reduces the global investment search space while preserving evidence, uncertainty, and
        dissent (Constitution §1). It answers “what deserves further investigation?” — not what to
        buy. Three strategy worlds: Alpha Momentum (momentum &amp; market leadership), Close System
        (product radar), Fundamental &amp; Opportunity. Experimental surfaces never touch official
        rankings, filters, or scores (§6). The hero and findings above are display derivations of
        approved pipeline outputs — never composite scores (Constitution §10).
      </ExplainPanel>

      <AdvisoryFooter provenance="Advisory discovery app — no broker connectivity, no execution, no allocation (Constitution §18)." />
    </div>
  )
}
