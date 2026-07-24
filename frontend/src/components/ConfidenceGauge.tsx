import { cn } from "@/lib/utils"

interface ConfidenceGaugeProps {
  value: number
  label?: string
  size?: "sm" | "md"
  className?: string
}

export function ConfidenceGauge({ value, label, size = "md", className }: ConfidenceGaugeProps) {
  const clamped = Math.max(0, Math.min(100, value))
  const barColor =
    clamped >= 70 ? "bg-[#10b981]" :
    clamped >= 40 ? "bg-[#f59e0b]" :
    "bg-[#ec4899]"

  const dims = size === "sm" ? "h-1.5 w-16" : "h-2 w-24"

  return (
    <div className={cn("flex flex-col gap-1", className)}>
      {label && <span className="text-xs font-medium text-muted-foreground">{label}</span>}
      <div className="flex items-center gap-2">
        <div className={cn("overflow-hidden rounded-full bg-muted", dims)}>
          <div className={cn("h-full rounded-full transition-all", barColor)} style={{ width: `${clamped}%` }} />
        </div>
        <span className="text-xs font-semibold">{clamped}%</span>
      </div>
    </div>
  )
}
