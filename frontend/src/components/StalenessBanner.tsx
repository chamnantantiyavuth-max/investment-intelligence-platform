/** Staleness / degraded-mode banner (FD #47 D3 bounds are operational, not investment rules). */
export function StalenessBanner({ message }: { message: string }) {
  return (
    <div className="mb-3 rounded-md border border-warning/40 bg-warning/10 px-3 py-2 text-xs text-warning">
      {message}
    </div>
  )
}
