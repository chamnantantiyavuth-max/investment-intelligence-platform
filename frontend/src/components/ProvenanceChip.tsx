/** Provenance chip — mandatory on every real surface (FD #46/47, arch v0.4 §3). */
export function ProvenanceChip({
  mode,
  source,
  asOf,
}: {
  mode?: string | null
  source?: string | null
  asOf?: string | null
}) {
  const real = mode === "real"
  return (
    <span
      className={`inline-flex items-center whitespace-nowrap rounded-full border px-2 py-0.5 font-mono text-[11px] font-medium ${
        real
          ? "border-positive/30 bg-positive/10 text-positive"
          : "border-warning/30 bg-warning/10 text-warning"
      }`}
    >
      {real ? "REAL" : "SYNTHETIC"}
      {source ? ` · ${source}` : ""}
      {asOf ? ` · ${asOf}` : ""}
    </span>
  )
}
