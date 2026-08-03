import type { ReactNode } from "react"
import type { InsightTone } from "@/components/HeroInsight"

const toneBg: Record<InsightTone, string> = {
  positive: "bg-positive/[0.06]",
  negative: "bg-negative/[0.06]",
  warning: "bg-warning/[0.06]",
  info: "bg-info/[0.06]",
  neutral: "bg-elevated",
}

const toneText: Record<InsightTone, string> = {
  positive: "text-positive",
  negative: "text-negative",
  warning: "text-warning",
  info: "text-info",
  neutral: "text-foreground",
}

const toneDot: Record<InsightTone, string> = {
  positive: "bg-positive",
  negative: "bg-negative",
  warning: "bg-warning",
  info: "bg-info",
  neutral: "bg-muted-foreground",
}

/**
 * FINDING CARD — a discovery panel: kicker + headline + display value + why-it-matters.
 * Marketing-pitch rhythm; tonal fill instead of borders (FD #49 amendment).
 */
export function FindingCard({
  kicker,
  headline,
  value,
  why,
  tone = "neutral",
  featured = false,
}: {
  kicker: string
  headline: string
  value?: ReactNode
  why?: string
  tone?: InsightTone
  featured?: boolean
}) {
  return (
    <article className={`rounded-2xl px-5 py-4 ${toneBg[tone]} ${featured ? "sm:col-span-2" : ""}`}>
      <div className="flex items-center gap-1.5">
        <span className={`size-1.5 rounded-full ${toneDot[tone]}`} />
        <span className="text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
          {kicker}
        </span>
      </div>
      <h2 className="mt-2 text-finding font-semibold leading-snug tracking-tight text-foreground">
        {headline}
      </h2>
      {value && (
        <div className={`mt-1.5 font-mono ${featured ? "text-display" : "text-xl"} font-semibold leading-tight ${toneText[tone]}`}>
          {value}
        </div>
      )}
      {why && <p className="mt-2 text-[13px] leading-relaxed text-muted-foreground">{why}</p>}
    </article>
  )
}
