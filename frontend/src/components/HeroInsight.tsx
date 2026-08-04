import type { ReactNode } from "react"
import { ExternalLink } from "lucide-react"

export type InsightTone = "positive" | "negative" | "warning" | "info" | "neutral"

const toneText: Record<InsightTone, string> = {
  positive: "text-positive",
  negative: "text-negative",
  warning: "text-warning",
  info: "text-info",
  neutral: "text-foreground",
}

/**
 * HERO INSIGHT (Research Desk v3.0) — the single most interesting setup, pitched
 * like a research lead story: kicker → serif headline → mono display → lede.
 * Borderless; typography carries the weight (FD #51 direction A).
 * Audit C4 fix: every claim carries an evidence reference line.
 */
export function HeroInsight({
  kicker,
  headline,
  display,
  sub,
  tone = "neutral",
  chips,
  evidenceRef,
}: {
  kicker: string
  headline: string
  display: ReactNode
  sub?: ReactNode
  tone?: InsightTone
  chips?: ReactNode
  evidenceRef?: string
}) {
  return (
    <section className="mb-8 border-b border-rule pb-6">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">{kicker}</span>
        {chips}
      </div>
      <h1 className="mt-3 max-w-3xl font-display text-hero font-bold leading-[1.12] tracking-[-0.01em] text-foreground">
        {headline}
      </h1>
      <div className={`mt-3 font-mono text-2xl font-semibold leading-none tracking-tight ${toneText[tone]}`}>
        {display}
      </div>
      {sub && <p className="mt-3 max-w-3xl text-[15px] leading-relaxed text-ink-2">{sub}</p>}
      {evidenceRef && (
        <div className="mt-3 flex items-center gap-1 font-mono text-[11px] text-ink-3">
          <ExternalLink className="size-3" />
          <span>evidence: {evidenceRef}</span>
        </div>
      )}
    </section>
  )
}
