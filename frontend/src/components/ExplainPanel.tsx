import { useState } from "react"
import type { ReactNode } from "react"
import { ChevronDown } from "lucide-react"

/** Collapsible methodology panel (Research Desk v3.0) — tonal, no border (C6).
 *  The WHY behind a page's logic, with spec refs. */
export function ExplainPanel({
  title = "Methodology",
  children,
}: {
  title?: string
  children: ReactNode
}) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-6 rounded-md bg-bg-panel">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center justify-between gap-2 px-3 py-2.5 text-left"
      >
        <span className="text-[11px] font-bold uppercase tracking-wider text-ink-2">{title}</span>
        <ChevronDown className={`size-3.5 text-ink-3 transition-transform ${open ? "rotate-180" : ""}`} />
      </button>
      {open && (
        <div className="border-t border-rule px-3 py-3 text-[13px] leading-relaxed text-ink-2">{children}</div>
      )}
    </div>
  )
}
