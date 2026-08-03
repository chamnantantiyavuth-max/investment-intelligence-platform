import type { ReactNode } from "react"

export type InsightTone = "positive" | "negative" | "warning" | "info" | "neutral"

const toneBg: Record<InsightTone, string> = {
  positive: "bg-positive/[0.07]",
  negative: "bg-negative/[0.07]",
  warning: "bg-warning/[0.07]",
  info: "bg-info/[0.07]",
  neutral: "bg-elevated",
}

const toneText: Record<InsightTone, string> = {
  positive: "text-positive",
  negative: "text-negative",
  warning: "text-warning",
  info: "text-info",
  neutral: "text-foreground",
}

/**
 * HERO INSIGHT — the single most interesting thing on the page, pitched like a headline.
 * No border; tonal fill + typographic hierarchy carry the weight (FD #49 amendment).
 */
export function HeroInsight({
  kicker,
  headline,
  display,
  sub,
  tone = "neutral",
  chips,
}: {
  kicker: string
  headline: string
  display: ReactNode
  sub?: ReactNode
  tone?: InsightTone
  chips?: ReactNode
}) {
  return (
    <section className={`mb-4 rounded-2xl px-6 py-6 ${toneBg[tone]}`}>
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          {kicker}
        </span>
        {chips}
      </div>
      <h1 className="mt-2 max-w-3xl text-heroline font-semibold leading-tight tracking-tight text-foreground">
        {headline}
      </h1>
      <div className={`mt-2 font-mono text-hero font-semibold leading-none tracking-tight ${toneText[tone]}`}>
        {display}
      </div>
      {sub && <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground">{sub}</p>}
    </section>
  )
}
