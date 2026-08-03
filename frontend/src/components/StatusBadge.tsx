export type BadgeTone = "positive" | "negative" | "warning" | "info" | "muted"

const toneCls: Record<BadgeTone, string> = {
  positive: "border-positive/30 bg-positive/10 text-positive",
  negative: "border-negative/30 bg-negative/10 text-negative",
  warning: "border-warning/30 bg-warning/10 text-warning",
  info: "border-info/30 bg-info/10 text-info",
  muted: "border-border bg-muted text-muted-foreground",
}

/** Presentation-only tone mapping for approved domain values. Never a rule. */
function toneFor(value: string): BadgeTone {
  const v = value.toLowerCase()
  if (/(emerging|expansion|approved|active monitoring|maximum|high|confirmed|new|add|wide|deep|stable)/.test(v)) return "positive"
  if (/(deteriorat|crowded|late stage|rejected|exit|cosmetic|trap|narrowing|shallow|none)/.test(v)) return "negative"
  if (/(under human|moderate|dormant|reduce|warning|watch|medium)/.test(v)) return "warning"
  if (/(experimental|formation|detected|maintain|narrow|opportunity|unknown)/.test(v)) return "info"
  return "muted"
}

/** Pill badge for lifecycle / approval / monitoring / conviction values. */
export function StatusBadge({ value, tone, className = "" }: { value: string; tone?: BadgeTone; className?: string }) {
  const t = tone ?? toneFor(value)
  return (
    <span
      className={`inline-flex items-center whitespace-nowrap rounded-full border px-2 py-0.5 text-[11px] font-medium leading-tight ${toneCls[t]} ${className}`}
    >
      {value}
    </span>
  )
}
