/** Honest empty state — the queue may return zero (Constitution §14, FD #9). */
export function EmptyState({ message, sub }: { message: string; sub?: string }) {
  return (
    <div className="rounded-md border border-dashed border-border bg-card/50 px-4 py-8 text-center">
      <p className="text-sm text-muted-foreground">{message}</p>
      {sub && <p className="mt-1 text-xs text-muted-foreground/70">{sub}</p>}
    </div>
  )
}
