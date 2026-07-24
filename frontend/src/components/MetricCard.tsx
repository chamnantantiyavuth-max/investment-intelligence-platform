import { Card, CardContent } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"

interface MetricCardProps {
  label: string
  value: string | number
  trend?: "up" | "down" | "flat"
  trendLabel?: string
  className?: string
}

export function MetricCard({ label, value, trend, trendLabel, className }: MetricCardProps) {
  return (
    <Card className={cn("min-w-[140px]", className)}>
      <CardContent className="flex flex-col items-center gap-1 p-4 text-center">
        <span className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
          {label}
        </span>
        <span className="text-[28px] font-bold tracking-tight">
          {value}
        </span>
        {trend && trendLabel && (
          <span
            className={cn(
              "flex items-center gap-0.5 text-[13px] font-medium",
              trend === "up" && "text-[#10b981]",
              trend === "down" && "text-[#ec4899]",
              trend === "flat" && "text-muted-foreground",
            )}
          >
            {trend === "up" && <TrendingUp className="size-3" />}
            {trend === "down" && <TrendingDown className="size-3" />}
            {trend === "flat" && <Minus className="size-3" />}
            {trendLabel}
          </span>
        )}
      </CardContent>
    </Card>
  )
}
