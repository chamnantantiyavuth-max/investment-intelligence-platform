import type { ResearchArtifact } from "@/api/orgClient";

/** Briefing "Material Changes" — one append-first delta per versioned pair.
 *  v1 is the base; every later slice renders as a delta line referencing the
 *  prior result (append-first doctrine, FD-CIW-012/016). No invented diff. */
function clean(s: string | undefined, max = 60): string {
  if (!s) return "—";
  return s
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .split(/\s*;\s*/)[0]
    .trim()
    .slice(0, max);
}

export function MaterialChangePanel({
  artifacts,
  error = false,
}: {
  artifacts: ResearchArtifact[];
  error?: boolean;
}) {
  if (error) {
    return (
      <p className="text-xs text-negative">
        Artifact registry unavailable — API error. Material changes cannot be read; retry from the page.
      </p>
    );
  }
  // Base = first-slice result (no "-2"); later slices render as deltas.
  const results = [...artifacts.filter((a) => a.artifact_type === "research-result")].sort((a, b) => {
    const a2 = a.artifact_id.includes("-2") ? 1 : 0;
    const b2 = b.artifact_id.includes("-2") ? 1 : 0;
    return a2 - b2 || a.artifact_id.localeCompare(b.artifact_id);
  });
  if (results.length === 0) {
    return (
      <p className="text-xs text-ink-2">
        No versioned artifact changes since your last review.
      </p>
    );
  }
  const base = results[0];
  return (
    <div className="divide-y divide-rule">
      <div className="py-2">
        <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
          <span className="font-mono text-[11px] text-ink-3">{base.research_id ?? base.artifact_id}</span>
          <span className="font-display text-[15px] font-semibold tracking-tight text-foreground">
            {base.title}
          </span>
          <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">
            {clean(base.research_version)} · {clean(base.research_status, 80)}
          </span>
        </div>
        <p className="mt-0.5 text-[11px] text-ink-2">
          modified {base.modified} · first-slice result
        </p>
      </div>
      {results.slice(1).map((a) => (
        <div key={a.artifact_id} className="py-2">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5">
            <span className="font-mono text-[11px] text-ink-3">{a.research_id ?? a.artifact_id}</span>
            <span className="font-display text-[15px] font-semibold tracking-tight text-foreground">
              {a.title}
            </span>
            <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">
              {clean(a.research_version)} · {clean(a.research_status, 80)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-ink-2">
            modified {a.modified} · → supplements {base.research_id ?? base.artifact_id} ({base.title};
            append-first — {base.research_id ?? "the prior result"} remains Current Authoritative for its scope)
          </p>
        </div>
      ))}
    </div>
  );
}
