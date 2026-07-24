import { cn } from "@/lib/utils"

interface EvidenceIndicatorProps {
  supporting: number
  contradicting: number
  missing: number
  className?: string
}

export function EvidenceIndicator({ supporting, contradicting, missing, className }: EvidenceIndicatorProps) {
  const total = supporting + contradicting + missing
  if (total === 0) return <span className="text-xs text-muted-foreground">No evidence</span>

  const sPct = (supporting / total) * 100
  const cPct = (contradicting / total) * 100
  const mPct = (missing / total) * 100

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <div className="flex h-2 flex-1 overflow-hidden rounded-full bg-muted">
        <div className="h-full bg-[#10b981]" style={{ width: `${sPct}%` }} title={`${supporting} supporting`} />
        <div className="h-full bg-[#ec4899]" style={{ width: `${cPct}%` }} title={`${contradicting} contradicting`} />
        <div className="h-full bg-slate-300" style={{ width: `${mPct}%` }} title={`${missing} missing`} />
      </div>
      <span className="whitespace-nowrap text-xs text-muted-foreground">
        {supporting}s / {contradicting}c / {missing}m
      </span>
    </div>
  )
}
