import type { ReactNode } from "react"

export type KpiTone = "positive" | "negative" | "warning" | "info" | "neutral"

export interface KpiItem {
  label: string
  value: ReactNode
  sub?: string
  tone?: KpiTone
}

const toneClass: Record<KpiTone, string> = {
  positive: "text-positive",
  negative: "text-negative",
  warning: "text-warning",
  info: "text-info",
  neutral: "text-foreground",
}

/** Dense hero-metric strip. Values are display-only renderings of approved fields. */
export function KpiStrip({ items }: { items: KpiItem[] }) {
  return (
    <div className="mb-4 grid grid-cols-2 gap-2 md:grid-cols-3 xl:grid-cols-6">
      {items.map((k) => (
        <div key={k.label} className="rounded-md border border-border bg-card px-3 py-2">
          <div className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
            {k.label}
          </div>
          <div className={`mt-0.5 font-mono text-xl font-semibold leading-tight ${toneClass[k.tone ?? "neutral"]}`}>
            {k.value}
          </div>
          {k.sub && <div className="mt-0.5 text-[11px] text-muted-foreground">{k.sub}</div>}
        </div>
      ))}
    </div>
  )
}
