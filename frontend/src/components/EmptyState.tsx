/** Honest empty state (DNA-016, audit C5): why empty + whether normal + next step.
 *  Research Desk v3.0 — tonal panel, no border. */
export function EmptyState({
  message,
  sub,
  action,
}: {
  message: string
  sub?: string
  action?: string
}) {
  return (
    <div className="rounded-md bg-bg-panel px-4 py-10 text-center">
      <p className="text-sm font-medium text-foreground">{message}</p>
      {sub && <p className="mt-1 text-xs text-ink-2">{sub}</p>}
      {action && <p className="mt-2 text-[11px] uppercase tracking-[0.1em] text-ink-3">{action}</p>}
    </div>
  )
}
