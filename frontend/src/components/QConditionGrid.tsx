import { cn } from "@/lib/utils"
import { Check, X } from "lucide-react"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"

interface QCondition {
  name: string
  met: boolean
  value?: string
}

interface QConditionGridProps {
  conditions: QCondition[]
  className?: string
}

export function QConditionGrid({ conditions, className }: QConditionGridProps) {
  return (
    <div className={cn("flex gap-2", className)}>
      {conditions.slice(0, 5).map((cond, i) => (
        <Tooltip key={i}>
          <TooltipTrigger>
            <div
              className={cn(
                "flex size-8 items-center justify-center rounded-md border text-sm font-bold",
                cond.met
                  ? "border-[#10b981] bg-[#10b981]/10 text-[#10b981]"
                  : "border-[#ec4899] bg-[#ec4899]/10 text-[#ec4899]",
              )}
            >
              {cond.met ? <Check className="size-4" /> : <X className="size-4" />}
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <p className="text-xs font-medium">{cond.name}</p>
            {cond.value && <p className="text-xs text-muted-foreground">{cond.value}</p>}
          </TooltipContent>
        </Tooltip>
      ))}
    </div>
  )
}
