import type { ReactNode } from "react"

interface PageHeaderProps {
  title: string
  question?: string
  children?: ReactNode
}

/** Page header (Research Desk v3.0): serif title + the decision the page supports
 *  + right-side chip slot. Hairline rule underneath. */
export function PageHeader({ title, question, children }: PageHeaderProps) {
  return (
    <div className="mb-6 flex flex-wrap items-start justify-between gap-3 border-b border-rule pb-4">
      <div>
        <h1 className="font-display text-h2 font-bold tracking-tight text-foreground">{title}</h1>
        {question && <p className="mt-0.5 max-w-2xl text-sm text-ink-2">{question}</p>}
      </div>
      {children && <div className="flex flex-wrap items-center gap-2">{children}</div>}
    </div>
  )
}
