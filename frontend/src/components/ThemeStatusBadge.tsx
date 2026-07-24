import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface ThemeStatusBadgeProps {
  approvalStatus: "detected" | "experimental" | "under_review" | "approved" | "rejected"
  lifecycle?: "weak_signal" | "formation" | "emerging" | "expansion" | "crowded" | "deterioration"
  className?: string
}

const approvalColors: Record<string, string> = {
  detected: "bg-slate-100 text-slate-700",
  experimental: "bg-amber-100 text-amber-700",
  under_review: "bg-blue-100 text-blue-700",
  approved: "bg-emerald-100 text-emerald-700",
  rejected: "bg-rose-100 text-rose-700",
}

const lifecycleColors: Record<string, string> = {
  weak_signal: "bg-purple-100 text-purple-700",
  formation: "bg-cyan-100 text-cyan-700",
  emerging: "bg-blue-100 text-blue-700",
  expansion: "bg-emerald-100 text-emerald-700",
  crowded: "bg-amber-100 text-amber-700",
  deterioration: "bg-rose-100 text-rose-700",
}

const formatLabel = (s: string) =>
  s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())

export function ThemeStatusBadge({ approvalStatus, lifecycle, className }: ThemeStatusBadgeProps) {
  return (
    <span className={cn("inline-flex items-center gap-1.5", className)}>
      <Badge variant="secondary" className={cn("font-medium", approvalColors[approvalStatus] ?? "")}>
        {formatLabel(approvalStatus)}
      </Badge>
      {lifecycle && (
        <Badge variant="outline" className={cn("font-medium", lifecycleColors[lifecycle] ?? "")}>
          {formatLabel(lifecycle)}
        </Badge>
      )}
    </span>
  )
}
