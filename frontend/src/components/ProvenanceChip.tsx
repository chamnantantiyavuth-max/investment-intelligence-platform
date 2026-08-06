/** Provenance chip — REAL / HYBRID / SYNTHETIC / UNKNOWN (audit C3 fix: full state set).
 *  Mandatory on every surface (FD #46/47). Text + color, never color alone. */
export type ProvenanceMode = "real" | "hybrid" | "synthetic" | "unknown"

const STYLE: Record<ProvenanceMode, string> = {
  real: "border-positive/30 bg-positive/10 text-positive",
  hybrid: "border-info/30 bg-info/10 text-info",
  synthetic: "border-warning/30 bg-warning/10 text-warning",
  unknown: "border-ink-3/30 bg-ink-3/10 text-ink-2",
}

const LABEL: Record<ProvenanceMode, string> = {
  real: "Real data",
  hybrid: "Hybrid data",
  synthetic: "Synthetic data",
  unknown: "Source unknown",
}

export function ProvenanceChip({
  mode,
  source,
  asOf,
}: {
  mode?: string | null
  source?: string | null
  asOf?: string | null
}) {
  const m: ProvenanceMode =
    mode === "real" ? (asOf ? "real" : "real") : mode === "hybrid" ? "hybrid" : mode === "synthetic" ? "synthetic" : "unknown"
  return (
    <span
      className={`inline-flex items-center whitespace-nowrap rounded-full border px-2 py-0.5 font-mono text-[11px] font-medium ${STYLE[m]}`}
      title={`data: ${m}${source ? ` · ${source}` : ""}${asOf ? ` · ${asOf}` : ""}`}
    >
      {LABEL[m]}
      {source ? ` · ${source}` : ""}
      {asOf ? ` · ${asOf}` : ""}
    </span>
  )
}
