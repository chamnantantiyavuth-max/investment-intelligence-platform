import { useState } from "react"
import type { ReactNode } from "react"
import { Info, ChevronDown } from "lucide-react"

/** Collapsible methodology panel — the WHY behind a page's logic, with spec refs. */
export function ExplainPanel({
  title = "Methodology",
  children,
}: {
  title?: string
  children: ReactNode
}) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-4 rounded-md border border-border bg-card">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between gap-2 px-3 py-2 text-left"
      >
        <span className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
          <Info className="size-3.5" />
          {title}
        </span>
        <ChevronDown className={`size-3.5 text-muted-foreground transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="border-t border-border px-3 py-2.5 text-[13px] leading-relaxed text-muted-foreground">
          {children}
        </div>
      )}
    </div>
  )
}
