import type { ReactNode } from "react"
import type { InsightTone } from "@/components/HeroInsight"
import { ExternalLink } from "lucide-react"

const toneText: Record<InsightTone, string> = {
  positive: "text-positive",
  negative: "text-negative",
  warning: "text-warning",
  info: "text-info",
  neutral: "text-foreground",
}

/**
 * FINDING ROW (Research Desk v3.0) — ledger row, not a card: kicker + serif headline
 * + mono value + why. Hairline separator only (FD #51 direction A; audit C6: no
 * default containment). Audit C4 fix: optional evidence reference line.
 */
export function FindingCard({
  kicker,
  headline,
  value,
  why,
  tone = "neutral",
  featured = false,
  evidenceRef,
}: {
  kicker: string
  headline: string
  value?: ReactNode
  why?: string
  tone?: InsightTone
  featured?: boolean
  evidenceRef?: string
}) {
  return (
    <article className={`border-b border-rule py-4 ${featured ? "sm:col-span-2" : ""}`}>
      <div className="flex items-center gap-2">
        <span className="text-[10px] font-bold uppercase tracking-[0.16em] text-primary">{kicker}</span>
      </div>
      <h2 className="mt-1.5 font-display text-finding font-bold leading-snug tracking-tight text-foreground">
        {headline}
      </h2>
      {value && (
        <div className={`mt-1.5 font-mono text-lg font-semibold leading-tight ${toneText[tone]}`}>{value}</div>
      )}
      {why && <p className="mt-1.5 max-w-2xl text-[13px] leading-relaxed text-ink-2">{why}</p>}
      {evidenceRef && (
        <div className="mt-1.5 flex items-center gap-1 font-mono text-[10.5px] text-ink-3">
          <ExternalLink className="size-3" />
          <span>run: {evidenceRef}</span>
        </div>
      )}
    </article>
  )
}
