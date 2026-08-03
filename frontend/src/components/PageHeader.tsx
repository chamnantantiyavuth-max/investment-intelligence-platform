import type { ReactNode } from "react"

interface PageHeaderProps {
  title: string
  question?: string
  children?: ReactNode
}

/** Page header: mono title + the decision the page supports + right-side chip slot. */
export function PageHeader({ title, question, children }: PageHeaderProps) {
  return (
    <div className="mb-4 flex flex-wrap items-start justify-between gap-3 border-b border-border pb-4">
      <div>
        <h1 className="font-mono text-lg font-semibold tracking-tight text-foreground">{title}</h1>
        {question && <p className="mt-0.5 max-w-2xl text-sm text-muted-foreground">{question}</p>}
      </div>
      {children && <div className="flex flex-wrap items-center gap-2">{children}</div>}
    </div>
  )
}
