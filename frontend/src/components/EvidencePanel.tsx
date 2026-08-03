import type { ReactNode } from "react"
import { CheckCircle2, XCircle, HelpCircle } from "lucide-react"

interface EvidenceSection {
  title: string
  icon?: ReactNode
  toneClass?: string
  items: ReactNode[]
}

/**
 * Evidence panel — supporting / contradicting / missing rendered as SEPARATE
 * sections (Constitution §11, §10; EVIDENCE-MODEL §7). Never merged into one list.
 */
export function EvidencePanel({ sections }: { sections: EvidenceSection[] }) {
  if (sections.every((s) => s.items.length === 0)) return null
  return (
    <div className="grid gap-2 md:grid-cols-3">
      {sections.map((s) => (
        <div key={s.title} className="rounded-md border border-border bg-card px-3 py-2">
          <div className="mb-1.5 flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
            {s.icon}
            {s.title}
          </div>
          {s.items.length === 0 ? (
            <p className="text-xs text-muted-foreground/70">— none recorded —</p>
          ) : (
            <ul className="space-y-1">
              {s.items.map((it, i) => (
                <li key={i} className="text-[13px] leading-snug text-foreground/90">
                  {it}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  )
}

export function supportingSection(items: ReactNode[]): EvidenceSection {
  return { title: "Supporting", icon: <CheckCircle2 className="size-3.5 text-positive" />, items }
}
export function contradictingSection(items: ReactNode[]): EvidenceSection {
  return { title: "Contradicting", icon: <XCircle className="size-3.5 text-negative" />, items }
}
export function missingSection(items: ReactNode[]): EvidenceSection {
  return { title: "Missing", icon: <HelpCircle className="size-3.5 text-warning" />, items }
}
