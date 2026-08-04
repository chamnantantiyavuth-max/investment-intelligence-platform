import { useQuery } from "@tanstack/react-query"
import { Link, useParams } from "react-router-dom"
import { HeroInsight } from "@/components/HeroInsight"
import { ProvenanceChip } from "@/components/ProvenanceChip"
import { StatusBadge } from "@/components/StatusBadge"
import { EvidencePanel, supportingSection, contradictingSection, missingSection } from "@/components/EvidencePanel"
import { ExplainPanel } from "@/components/ExplainPanel"
import { EmptyState } from "@/components/EmptyState"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMTheme } from "@/api/amClient"

function DimPanel({ title, note, rows }: { title: string; note: string; rows: [string, string][] }) {
  return (
    <div className="rounded-md bg-bg-panel px-4 py-3">
      <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      <p className="text-[11px] text-ink-2">{note}</p>
      <div className="mt-2 space-y-1">
        {rows.map(([k, v]) => (
          <div key={k} className="flex items-center justify-between gap-2 text-xs">
            <span className="text-ink-2">{k}</span>
            <StatusBadge value={v} className="max-w-[62%] whitespace-normal text-right" />
          </div>
        ))}
      </div>
    </div>
  )
}

export default function AMThemeCardPage() {
  const { id } = useParams<{ id: string }>()
  const { data: tc, isLoading, error, refetch } = useQuery({
    queryKey: ["am-theme", id],
    queryFn: () => getAMTheme(id!),
    enabled: !!id,
  })

  if (isLoading) return <Skeleton className="h-96 w-full" />
  if (error) {
    const is404 = String(error).includes("NOT_FOUND")
    return (
      <div>
        <Button variant="ghost" size="icon-sm" render={<Link to="/am-queue" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <div className="mt-3 rounded-md bg-bg-panel px-5 py-8 text-center">
          <p className="text-sm font-medium text-foreground">{is404 ? `Theme '${id}' not found.` : "Failed to load theme."}</p>
          {!is404 && (
            <button onClick={() => refetch()} className="mt-2 text-sm text-primary underline">
              Retry
            </button>
          )}
        </div>
      </div>
    )
  }
  if (!tc) return null
  const theme = tc.theme
  const candidates = tc.candidates ?? []

  return (
    <div>
      <div className="mb-2">
        <Button variant="ghost" size="icon-sm" render={<Link to="/am-queue" />}>
          <ArrowLeft className="size-4" />
        </Button>
      </div>

      <HeroInsight
        kicker={`Theme card · ${theme.id}`}
        headline={theme.name}
        display={theme.confidence}
        tone="positive"
        sub={theme.why_now}
        evidenceRef={`${theme.id} · ${theme.provenance.source}`}
        chips={
          <ProvenanceChip
            mode={theme.provenance.hybrid ? "hybrid" : theme.provenance.mode}
            source={theme.provenance.source}
            asOf={theme.provenance.as_of}
          />
        }
      />

      <div className="mb-4 flex flex-wrap items-center gap-1.5">
        <StatusBadge value={theme.lifecycle} />
        <StatusBadge value={theme.approval_status} />
        <StatusBadge value={theme.monitoring_status} />
        <span className="ml-auto font-mono text-[11px] text-ink-2">
          {theme.sector} / {theme.industry} · {theme.stocks_in_industry} stocks ·{" "}
          {theme.key_tickers.length} key tickers · {candidates.length} candidates
        </span>
      </div>

      <Tabs defaultValue="dimensions">
        <TabsList>
          <TabsTrigger value="dimensions">Quality Dimensions</TabsTrigger>
          <TabsTrigger value="falsification">Falsification</TabsTrigger>
          <TabsTrigger value="candidates">Candidates ({candidates.length})</TabsTrigger>
          <TabsTrigger value="evidence">Evidence ({theme.evidence_provenance.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="dimensions" className="space-y-3 pt-4">
          <div className="grid gap-3 lg:grid-cols-2">
            <DimPanel
              title="Theme Quality"
              note="Theme-level dimension — separate from candidate/entry/data axes (§10, §13)"
              rows={[
                ["Lifecycle", theme.lifecycle],
                ["Approval Status", theme.approval_status],
                ["Monitoring Status", theme.monitoring_status],
                ["Confidence", theme.confidence],
                ["Breadth (stocks in industry)", String(theme.stocks_in_industry)],
              ]}
            />
          </div>
          {candidates.length === 0 ? (
            <EmptyState message="No candidates in this theme." sub="Unsupported roles are left empty (spec §3.3)." />
          ) : (
            candidates.map((c) => (
              <div key={c.id} className="grid gap-3 lg:grid-cols-3">
                <DimPanel
                  title={`${c.ticker} — Candidate Quality`}
                  note={`${c.research_state} · ${c.conviction_level}`}
                  rows={[
                    ["Fundamentals", c.candidate_quality.fundamentals],
                    ["Growth", c.candidate_quality.growth],
                    ["Liquidity", c.candidate_quality.liquidity],
                    ["Relative Strength", c.candidate_quality.relative_strength],
                    ["Trend Quality", c.candidate_quality.trend_quality],
                    ["Accumulation", c.candidate_quality.accumulation],
                    ["Industry Leadership", c.candidate_quality.industry_leadership],
                  ]}
                />
                <DimPanel
                  title="Entry Readiness"
                  note="Price structure / base / breakout — not a buy signal"
                  rows={[
                    ["Price Structure", c.entry_readiness.price_structure],
                    ["Base Quality", c.entry_readiness.base_quality],
                    ["Breakout Proximity", c.entry_readiness.breakout_proximity],
                    ["Volume Behavior", c.entry_readiness.volume_behavior],
                    ["Volatility Contraction", c.entry_readiness.volatility_contraction],
                    ["Extension Risk", c.entry_readiness.extension_risk],
                  ]}
                />
                <DimPanel
                  title="Data Confidence"
                  note="Freshness / completeness / reliability of the underlying data"
                  rows={[
                    ["Freshness", c.data_confidence.freshness],
                    ["Completeness", c.data_confidence.completeness],
                    ["Reliability", c.data_confidence.reliability],
                    ["Conflicts", c.data_confidence.conflicts],
                    ["Missing Data", c.data_confidence.missing_data],
                  ]}
                />
              </div>
            ))
          )}
        </TabsContent>

        <TabsContent value="falsification" className="space-y-3 pt-4">
          <p className="text-[11px] text-ink-2">
            Scoped §11 panel (FD #50, 4 Aug 2026): alternative explanations, evidence register, and
            unresolved counter-evidence — read-only passthrough from the admitted artifact. Milestones
            and invalidation conditions are not yet represented.
          </p>
          <EvidencePanel
            sections={[
              supportingSection([]),
              contradictingSection(theme.unresolved_counter_evidence ?? []),
              missingSection(
                candidates
                  .map((c) =>
                    c.data_confidence.missing_data && c.data_confidence.missing_data !== "None"
                      ? `${c.ticker}: ${c.data_confidence.missing_data}`
                      : null
                  )
                  .filter((x): x is string => !!x)
              ),
            ]}
          />
          {theme.alternative_explanations && (
            <div className="rounded-md bg-bg-panel px-4 py-3">
              <h3 className="text-sm font-semibold text-foreground">Alternative Explanations</h3>
              <p className="text-[11px] text-ink-2">
                What could make this thesis wrong — kept visible, never erased (§11, §22)
              </p>
              <ul className="mt-2 space-y-1">
                {Object.entries(theme.alternative_explanations).map(([k, v]) => (
                  <li key={k} className="text-[13px] leading-relaxed text-ink-2">
                    {v}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {theme.evidence && theme.evidence.length > 0 && (
            <div className="rounded-md bg-bg-panel px-4 py-3">
              <h3 className="text-sm font-semibold text-foreground">
                Evidence Register ({theme.evidence.length})
              </h3>
              <p className="text-[11px] text-ink-2">
                Raw records from the admitted artifact — read-only passthrough (FD #50, 4 Aug 2026)
              </p>
              <ul className="mt-2 space-y-1.5">
                {theme.evidence.map((e) => (
                  <li key={e.id} className="text-[13px] leading-relaxed">
                    <span className="font-mono text-xs font-semibold text-foreground">{e.id}</span>{" "}
                    <StatusBadge value={e.type} className="mx-1" />
                    <span className="text-ink-2">{e.content}</span>
                    {e.source && (
                      <span className="ml-1 font-mono text-[11px] text-ink-2">({e.source})</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </TabsContent>

        <TabsContent value="candidates" className="pt-4">
          {candidates.length === 0 ? (
            <EmptyState message="No candidates in this theme." />
          ) : (
            <div>
              {candidates.map((c, i) => (
                <div
                  key={c.id}
                  className={`flex flex-wrap items-center gap-x-4 gap-y-1 border-b border-rule py-3 text-xs ${
                    i === 0 ? "border-t" : ""
                  }`}
                >
                  <span className="font-mono text-sm font-semibold text-foreground">{c.ticker}</span>
                  <StatusBadge value={c.research_state} />
                  <StatusBadge value={c.conviction_level} />
                  <span className="text-ink-2">
                    RS {c.candidate_quality.relative_strength} · Trend {c.candidate_quality.trend_quality}
                  </span>
                  <span className="text-ink-2">
                    Base {c.entry_readiness.base_quality} · Breakout {c.entry_readiness.breakout_proximity}
                  </span>
                  <span className="font-mono text-ink-2">
                    dc: {c.data_confidence.freshness} · {c.data_confidence.completeness}
                  </span>
                </div>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="evidence" className="space-y-3 pt-4">
          {theme.evidence_provenance.length === 0 ? (
            <EmptyState message="No evidence provenance recorded for this theme." />
          ) : (
            <div className="flex flex-wrap gap-1.5">
              {theme.evidence_provenance.map((e) => (
                <StatusBadge key={e.source_id} value={`${e.source_id} · ${e.source_type}`} />
              ))}
            </div>
          )}
          <p className="text-[11px] text-ink-2">
            Evidence source labels from the real artifact — synthetic and human-sourced entries are marked
            individually; no blanket label over mixed content. Contradicting-evidence fields land with the
            read-only schema extension (FD #50, §11 falsification panel).
          </p>
        </TabsContent>
      </Tabs>

      <ExplainPanel title="How to read this theme card">
        Governance is two independent axes (Constitution §5): Approval Status and Monitoring Status — a
        transition in one never auto-changes the other. The four quality dimensions stay separate (§10):
        Theme Quality at theme level; Candidate Quality, Entry Readiness, and Data Confidence per candidate
        — never collapsed into one opaque score (§2.5). Theme roles come from the canonical taxonomy
        (FD #26, §13): Confirmed Leader, Emerging Challenger, Direct Beneficiary, Enabler, Bottleneck
        Owner, Second-order Beneficiary, Watchlist Member, Former Leader, Deteriorating Member.
      </ExplainPanel>
    </div>
  )
}
