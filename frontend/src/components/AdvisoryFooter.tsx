/** Fixed advisory footer — advisory-only framing on every page (§1, §23.8.1). */
export function AdvisoryFooter({ provenance }: { provenance?: string }) {
  return (
    <footer className="mt-6 border-t border-border pt-3 text-[11px] leading-relaxed text-muted-foreground">
      Advisory only — no buy / sell / allocate advice. Portfolio-blind. Evidence-first: every surface
      carries a provenance label.
      {provenance && <div className="mt-1 font-mono text-muted-foreground/80">{provenance}</div>}
    </footer>
  )
}
