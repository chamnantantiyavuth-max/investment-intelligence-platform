import { useEffect, useMemo, useState } from "react"
import { HeroInsight } from "@/components/HeroInsight"
import { FindingCard } from "@/components/FindingCard"
import { ProvenanceChip } from "@/components/ProvenanceChip"
import { StalenessBanner } from "@/components/StalenessBanner"
import { ExplainPanel } from "@/components/ExplainPanel"
import { DecisionRequiredLedger } from "@/components/DecisionRequiredLedger"
import { MaterialChangePanel } from "@/components/MaterialChangePanel"
import { HoldBanner } from "@/components/HoldBanner"
import { TrendingUp, Shield, Building2, Landmark } from "lucide-react"
import {
  getDashboardSummary,
  type DashboardSummary,
  type ComponentProvenance,
} from "@/api/dashboardClient"
import { getAMQueue } from "@/api/amClient"
import { getOrgQueue, getResearchArtifacts, type OrgQueue, type ResearchArtifact } from "@/api/orgClient"
import { rankCandidates, lifecycleCounts, leadershipCount } from "@/lib/insights"
import { cardsInView, isHeldOrBlocked, latestCardUpdate } from "@/lib/researchWorkflow"

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

/** Mono provenance stamp for a data section (design-system mandate — every
 *  surface carries source + as-of; derived from admitted fields only). */
function SectionStamp({ text }: { text: string }) {
  return <p className="mb-1 font-mono text-[10px] uppercase tracking-[0.08em] text-ink-3">{text}</p>
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
    <div className="rounded-md bg-bg-panel px-4 py-3">
      <div className="flex items-center justify-between gap-2">
        <span className="flex items-center gap-2 text-sm font-medium text-foreground">
          <span className="text-ink-2">{icon}</span>
          {name}
        </span>
        <ProvenanceChip mode={mode} source={comp.data_source ?? comp.source} asOf={comp.point_in_time} />
      </div>
      <div className="mt-1.5 flex items-center justify-between gap-2 text-[11px]">
        <span className="font-mono text-ink-2">
          {comp.state === "unavailable" ? "UNAVAILABLE — no admitted artifact" : comp.run_id ?? "—"}
        </span>
        {stale !== null && comp.state === "available" && (
          <span className={staleOver ? "font-mono text-warning" : "font-mono text-ink-2"}>
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
  const [amError, setAmError] = useState(false)
  const [error, setError] = useState(false)
  const [org, setOrg] = useState<OrgQueue | null>(null)
  const [orgError, setOrgError] = useState(false)
  const [artifacts, setArtifacts] = useState<ResearchArtifact[]>([])
  const [artifactsError, setArtifactsError] = useState(false)

  const load = () => {
    setError(false)
    setAmError(false)
    setOrgError(false)
    setArtifactsError(false)
    getDashboardSummary().then(setData).catch(() => setError(true))
    getAMQueue().then(setAm).catch(() => {
      setAmError(true)
      setAm(null)
    })
    getOrgQueue().then(setOrg).catch(() => setOrgError(true))
    getResearchArtifacts().then((r) => setArtifacts(r.artifacts)).catch(() => {
      setArtifactsError(true)
      setArtifacts([])
    })
  }
  useEffect(load, [])

  const top = useMemo(() => (am ? rankCandidates(am.themes)[0] : undefined), [am])
  const topTheme = useMemo(() => am?.themes.find((t) => t.theme.id === top?.themeId), [am, top])
  const topProv = topTheme?.theme.provenance
  const lifecycle = useMemo(() => (am ? lifecycleCounts(am.themes) : []), [am])
  const leaders = useMemo(() => (am ? leadershipCount(am.themes) : 0), [am])

  if (error) {
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Dashboard unavailable — API error.</p>
        <p className="mt-1 text-xs text-ink-2">What failed: the dashboard summary endpoint. What's affected: this page's engine-status read.</p>
        <button type="button" onClick={load} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    )
  }
  if (!data) return <p className="text-sm text-ink-2">Loading dashboard…</p>

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
  const runId = am?.run_id
  const orgLatest = org ? latestCardUpdate(org.cards) : "…"
  const regLatest = artifactsError
    ? "unavailable"
    : artifacts.map((a) => a.modified).filter(Boolean).sort().pop() ?? "unavailable"

  return (
    <div>
      {staleWarnings.length > 0 && <StalenessBanner message={staleWarnings.join(" · ")} />}

      {/* C5 fix: AM failure is a scoped degraded state — never coerced to "awaiting run"/zero */}
      {amError ? (
        <div className="mb-8 border-b border-rule pb-6">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-warning">Alpha Momentum surface unavailable</p>
          <h1 className="mt-2 max-w-3xl font-display text-hero font-bold leading-[1.12] text-foreground">
            Momentum claims suppressed — engine status below
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-ink-2">
            The AM API did not respond (fail-closed 503, FD #47 D2). Dashboard summary and Close System remain valid.
          </p>
          <button type="button" onClick={load} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
            Retry →
          </button>
        </div>
      ) : top ? (
        <HeroInsight
          kicker="Lead insight · Alpha Momentum"
          headline={`The most interesting setup right now: ${top.ticker} — ${top.themeName}`}
          display={`${top.conviction} conviction · ${top.lifecycle} · RS ${top.rs}`}
          tone="positive"
          sub={top.whyNow}
          evidenceRef={`${runId} · ${top.themeId}`}
          chips={
            <ProvenanceChip
              mode={topProv?.hybrid ? "hybrid" : topProv?.mode}
              source={topProv?.source}
              asOf={topProv?.as_of}
            />
          }
        />
      ) : (
        <HeroInsight
          kicker="Strategy control center"
          headline="The engine is up — awaiting an admitted Alpha Momentum run"
          display="—"
          tone="info"
          sub="Engine provenance below shows each strategy's artifact state."
        />
      )}

      <section className="mt-8">
        <h2 className="mb-1 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
          Decisions required
        </h2>
        <SectionStamp text={`org_workflow_kanban · operational · as-of ${orgLatest}`} />
        {orgError ? (
          <p className="text-xs text-ink-2">Org-workflow queue unavailable — API error. Retry with the button above.</p>
        ) : org ? (
          <DecisionRequiredLedger cards={org.cards} artifacts={artifacts} />
        ) : (
          <p className="text-xs text-ink-2">Loading decisions…</p>
        )}
      </section>

      <section className="mt-8">
        <h2 className="mb-1 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
          Material changes since last review
        </h2>
        <SectionStamp text={`research_artifact_registry · REAL per artifact · as-of ${regLatest}`} />
        <MaterialChangePanel artifacts={artifacts} error={artifactsError} />
      </section>

      <section className="grid grid-cols-1 gap-x-10 gap-y-1 md:grid-cols-2">
        <FindingCard
          featured
          kicker="Finding 01 · Momentum"
          headline="Leadership lives in the pipeline right now"
          value={am ? `${leaders}/${am.themes.length} themes` : "—"}
          tone="positive"
          why={`${leaders} of ${am?.themes.length ?? "—"} themes sit in Emerging Leadership or Expansion — where the strongest candidates concentrate.`}
          evidenceRef={runId}
        />
        <FindingCard
          kicker="Finding 02 · Data"
          headline="Coverage on the admitted run"
          value={topProv?.coverage ?? "—"}
          tone="info"
          why="Real EOD from Yahoo Finance, point-in-time as shown. Staleness bounds: AM ≤7d, FO ≤30d, II ≤120d (FD #47 D3)."
          evidenceRef={runId}
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
          evidenceRef={runId}
        />
      </section>

      <section className="mt-8">
        <h2 className="mb-1 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
          Holds &amp; exceptions
        </h2>
        <SectionStamp text={`org_workflow_holds · ${org ? `${org.holds.length} recorded` : "…"} · as-of unavailable`} />
        {orgError ? (
          <p className="text-xs text-ink-2">Holds unavailable — org-workflow API error.</p>
        ) : org ? (
          (() => {
            const active = org.holds.filter((h) => h.status !== "CLEARED");
            const cleared = org.holds.filter((h) => h.status === "CLEARED");
            return active.length === 0 ? (
              <div>
                <p className="text-xs text-ink-2">
                  No active holds · {cleared.length} cleared{" "}
                  {cleared.length > 0 && `(${cleared.map((h) => h.hold_id).join(", ")})`}
                </p>
                {cleared.map((h) => (
                  <HoldBanner key={h.hold_id} hold={h} active={false} />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                {active.map((h) => (
                  <HoldBanner key={h.hold_id} hold={h} />
                ))}
              </div>
            );
          })()
        ) : (
          <p className="text-xs text-ink-2">Loading holds…</p>
        )}
      </section>

      <section className="mt-8">
        <h2 className="mb-1 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
          Research throughput
        </h2>
        <SectionStamp text={`org_workflow_kanban · derived from card workflow_column · as-of ${orgLatest}`} />
        {orgError ? (
          <p className="text-xs text-ink-2">Throughput unavailable — org-workflow API error.</p>
        ) : org ? (
          <div className="grid gap-x-8 gap-y-1 text-[13px] sm:grid-cols-2">
            {[
              ["New Requests", cardsInView(org.cards, "Inbox").length],
              ["Active Research", cardsInView(org.cards, "Active Research").length],
              ["In Review", cardsInView(org.cards, "Review Queue").length],
              ["Founder Review", cardsInView(org.cards, "Founder Review").length],
              ["Held / Blocked", org.cards.filter(isHeldOrBlocked).length],
              ["Monitoring", org.cards.filter((c) => c.workflow_column === "Monitoring").length],
              ["Closed", org.cards.filter((c) => c.workflow_column === "Closed").length],
              ["Research Results (registry)", artifacts.filter((a) => a.artifact_type === "research-result").length],
            ].map(([k, v]) => (
              <div key={k} className="flex justify-between border-b border-rule py-1.5">
                <span className="text-ink-2">{k}</span>
                <span className="font-mono text-[11px] text-ink-3">{v}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-ink-2">Loading throughput…</p>
        )}
      </section>

      <section className="mt-8">
        <h2 className="mb-2 text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
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
        <section className="mt-3 rounded-md bg-bg-panel px-4 py-3">
          <h2 className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
            Theme lifecycle breadth
          </h2>
          <div className="mt-2 space-y-2">
            {lifecycle.map(([stage, n]) => (
              <div key={stage} className="space-y-0.5">
                <div className="flex justify-between text-[11px] text-ink-2">
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
    </div>
  )
}
