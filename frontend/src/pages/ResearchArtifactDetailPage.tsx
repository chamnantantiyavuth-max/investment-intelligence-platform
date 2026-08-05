import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getOrgQueue, getResearchArtifact, getResearchArtifacts } from "@/api/orgClient";
import { ProvenanceChip } from "@/components/ProvenanceChip";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";
import { ReviewGatePanel } from "@/components/ReviewGatePanel";
import { DecisionTimeline, type FounderRecord } from "@/components/DecisionTimeline";
import { familyOf, linkArtifact } from "@/lib/researchWorkflow";

const SECTIONS = [
  "Executive Summary",
  "Research",
  "Evidence",
  "Independent Challenge",
  "Validation",
  "Data Quality",
  "Decision History",
] as const;
type Section = (typeof SECTIONS)[number];

function firstParagraph(text: string): string {
  for (const line of text.split(/\n+/)) {
    const t = line.trim();
    if (t && !t.startsWith("#") && !t.startsWith("|") && !t.startsWith("**") && t.length > 40) return t;
  }
  return "";
}

export default function ResearchArtifactDetailPage() {
  const params = useParams();
  const artifactId = params["*"] ?? "";
  const [section, setSection] = useState<Section>("Executive Summary");

  const detail = useQuery({
    queryKey: ["research-artifact", artifactId],
    queryFn: () => getResearchArtifact(artifactId),
    enabled: Boolean(artifactId),
  });
  const registry = useQuery({ queryKey: ["research-artifacts"], queryFn: getResearchArtifacts, staleTime: 60_000 });
  const queue = useQuery({ queryKey: ["org-queue"], queryFn: getOrgQueue, staleTime: 60_000 });

  const artifact = detail.data?.artifact;
  const all = useMemo(() => registry.data?.artifacts ?? [], [registry.data]);
  const cards = useMemo(() => queue.data?.cards ?? [], [queue.data]);
  const family = useMemo(() => (artifact ? familyOf(artifact.artifact_id, all) : []), [artifact, all]);
  const sourceMaps = family.filter((a) => a.artifact_type === "source-map");
  const challenges = family.filter((a) => a.artifact_type === "challenge-review");
  const founderRecords = family.filter((a) => a.artifact_type === "founder-review-record");
  // Card join: the org-workflow card whose expected_artifact resolves to THIS artifact.
  const card = useMemo(
    () => (artifact ? cards.find((c) => linkArtifact(c, all)?.artifact_id === artifact.artifact_id) : undefined),
    [artifact, all, cards]
  );
  // Founder-record content (for the publication transition table) — fetched
  // individually; failed fetches stay visible as records but are reported so
  // Decision History can show a scoped warning instead of silent title-only.
  const recordsQ = useQuery({
    queryKey: ["founder-record-content", founderRecords.map((r) => r.artifact_id).join(",")],
    queryFn: async () => {
      const records: FounderRecord[] = [];
      const failed: string[] = [];
      for (const r of founderRecords) {
        try {
          records.push({ artifact: r, content: (await getResearchArtifact(r.artifact_id)).artifact.content });
        } catch {
          failed.push(r.artifact_id);
          records.push({ artifact: r });
        }
      }
      return { records, failed };
    },
    enabled: founderRecords.length > 0,
  });
  const evidenceRefs = useMemo(() => {
    if (!artifact) return [];
    const set = new Set<string>();
    for (const m of artifact.content.matchAll(/SRC-[\w-]+/g)) set.add(m[0]);
    return Array.from(set).sort();
  }, [artifact]);
  const registryDown = registry.isError;
  const queueDown = queue.isError;
  const status404 = (detail.error as { status?: number } | null)?.status === 404;

  if (detail.isLoading || registry.isLoading) return <Skeleton className="h-64 w-full" />;
  if (detail.isError || !artifact) {
    if (status404) {
      return (
        <div className="rounded-md bg-bg-panel px-4 py-8">
          <p className="text-sm font-medium text-negative">Artifact not found.</p>
          <p className="mt-1 text-xs text-ink-2">What failed: no registry entry for “{artifactId}”. Check the path or browse the desk.</p>
          <Link to="/research" className="mt-3 inline-block text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
            ← Research Desk
          </Link>
        </div>
      );
    }
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Artifact detail unavailable — API error.</p>
        <p className="mt-1 text-xs text-ink-2">
          What failed: the artifact detail endpoint for “{artifactId}”. What's affected: this artifact's sections.
        </p>
        <button type="button" onClick={() => { detail.refetch(); }} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );
  }

  const mode = artifact.artifact_id.startsWith("ciw-pilot-msft") ? "real" : "synthetic";
  const identity: Array<[string, string]> = [
    ["research_id", artifact.research_id ?? "—"],
    ["research_version", artifact.research_version ?? "—"],
    ["research_status", artifact.research_status ?? "—"],
    ["artifact_type", artifact.artifact_type],
    ["modified", artifact.modified],
    ["path", artifact.path],
  ];

  return (
    <div className="space-y-6">
      <Link to="/research" className="text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
        ← Research Desk
      </Link>

      <div className="border-b border-rule pb-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{artifact.artifact_type}</span>
          <ProvenanceChip mode={mode} source={`${registry.data?.data_source ?? "research_artifact_registry"} · ${artifact.path}`} asOf={artifact.modified} />
        </div>
        <h1 className="mt-2 font-display text-h2 font-bold leading-tight tracking-tight">{artifact.title}</h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">{artifact.artifact_id}</p>
      </div>

      <div className="flex flex-wrap gap-1 border-b border-rule pb-3" role="tablist" aria-label="Artifact sections">
        {SECTIONS.map((s) => (
          <button
            key={s}
            type="button"
            role="tab"
            aria-selected={section === s}
            onClick={() => setSection(s)}
            className={`rounded-sm px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.1em] ${
              section === s ? "bg-bg-panel text-foreground" : "text-ink-3 hover:text-foreground"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {section === "Executive Summary" && (
        <section className="text-[13px]">
          {identity.map(([k, v]) => (
            <div key={k} className="flex justify-between gap-6 border-b border-rule py-1.5">
              <span className="shrink-0 text-ink-2">{k}</span>
              <span className="text-right font-mono text-[11px] text-ink-3">{v}</span>
            </div>
          ))}
          <p className="mt-3 text-sm leading-relaxed text-foreground">{firstParagraph(artifact.content) || "No lead summary in this artifact."}</p>
        </section>
      )}

      {section === "Research" && (
        <pre className="max-h-[70vh] overflow-auto whitespace-pre-wrap font-mono text-xs leading-relaxed text-foreground">
          {artifact.content}
        </pre>
      )}

      {section === "Evidence" && (
        <div className="space-y-4">
          {evidenceRefs.length > 0 ? (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Citations in this artifact</p>
              <div className="mt-1 flex flex-wrap gap-1">
                {evidenceRefs.map((r) => (
                  <span key={r} className="rounded-sm bg-bg-panel px-1.5 py-0.5 font-mono text-[11px] text-ink-2">{r}</span>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-xs text-ink-2">No SRC- citations found in this artifact body.</p>
          )}
          {registryDown ? (
            <p className="text-xs text-negative">Artifact registry unavailable — source maps cannot be listed.</p>
          ) : (
            sourceMaps.length > 0 && (
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Source maps (provenance)</p>
                <div className="mt-1 divide-y divide-rule">
                  {sourceMaps.map((s) => (
                    <Link key={s.artifact_id} to={`/research/${s.artifact_id}`} className="block py-1.5 text-[13px] text-primary hover:underline">
                      {s.title} <span className="font-mono text-[11px] text-ink-3">· {s.modified}</span>
                    </Link>
                  ))}
                </div>
              </div>
            )
          )}
          <p className="text-[11px] text-ink-3">
            Full evidence register (template 02) appears here as the org-workflow produces it.
          </p>
        </div>
      )}

      {section === "Independent Challenge" && (
        <div>
          {registryDown ? (
            <p className="text-xs text-negative">Artifact registry unavailable — challenge records cannot be listed.</p>
          ) : challenges.length > 0 ? (
            <div className="divide-y divide-rule">
              {challenges.map((c) => (
                <Link key={c.artifact_id} to={`/research/${c.artifact_id}`} className="block py-2">
                  <p className="text-[13px] font-medium text-foreground">{c.title}</p>
                  <p className="font-mono text-[11px] text-ink-3">{c.artifact_id} · {c.modified}</p>
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState
              message="No independent challenge record for this artifact"
              sub="CRO / Red Team challenge memos (template 08) and challenge-review files appear here when issued."
            />
          )}
        </div>
      )}

      {section === "Validation" && (
        <div className="space-y-4">
          {queueDown ? (
            <div className="rounded-md bg-bg-panel px-4 py-3">
              <p className="text-xs text-negative">Org-workflow queue unavailable — card status cannot be read.</p>
              <button type="button" onClick={() => { queue.refetch(); }} className="mt-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
                Retry →
              </button>
            </div>
          ) : (
            card && (
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
                  Card status · {card.card_id} (org_workflow_kanban)
                </p>
                <div className="mt-1">
                  <ReviewGatePanel card={card} />
                </div>
              </div>
            )
          )}
          <EmptyState
            message="No quant validation report published for this artifact yet"
            sub="Quant validation reports (template 07) record method version, dataset version, tests run/failed, and known limitations — they appear here when issued. Card-level status is shown above when the artifact links to a workflow card."
          />
        </div>
      )}

      {section === "Data Quality" && (
        <div className="space-y-4">
          {queueDown ? (
            <div className="rounded-md bg-bg-panel px-4 py-3">
              <p className="text-xs text-negative">Org-workflow queue unavailable — card data status cannot be read.</p>
              <button type="button" onClick={() => { queue.refetch(); }} className="mt-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
                Retry →
              </button>
            </div>
          ) : (
            card && (
              <div>
                <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">
                  Card data status · {card.card_id}
                </p>
                <p className="mt-1 text-[13px]">
                  <span className="text-ink-2">data_status </span>
                  <span className="font-mono text-[11px] text-ink-3">{card.data_status}</span>
                </p>
              </div>
            )
          )}
          {!registryDown && sourceMaps.length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Source coverage</p>
              <div className="mt-1 divide-y divide-rule">
                {sourceMaps.map((s) => (
                  <Link key={s.artifact_id} to={`/research/${s.artifact_id}`} className="block py-1.5 text-[13px] text-primary hover:underline">
                    {s.title}
                  </Link>
                ))}
              </div>
            </div>
          )}
          {registryDown && (
            <p className="text-xs text-negative">Artifact registry unavailable — source coverage cannot be listed.</p>
          )}
          <p className="text-xs text-ink-2">
            Freshness, completeness, conflicts, and restatements (EVIDENCE-MODEL §9) are recorded in data-quality
            reports (template 06) as the org-workflow produces them.
          </p>
        </div>
      )}

      {section === "Decision History" && (
        registryDown ? (
          <p className="text-xs text-negative">Artifact registry unavailable — decision records cannot be listed.</p>
        ) : (
          <div className="space-y-3">
            <DecisionTimeline artifact={artifact} records={recordsQ.data?.records ?? []} />
            {recordsQ.data && recordsQ.data.failed.length > 0 && (
              <div className="rounded-md bg-bg-panel px-4 py-3">
                <p className="text-xs text-warning">
                  {recordsQ.data.failed.length} founder record(s) unavailable — transition could not be read (
                  {recordsQ.data.failed.join(", ")})
                </p>
                <button type="button" onClick={() => { recordsQ.refetch(); }} className="mt-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
                  Retry →
                </button>
              </div>
            )}
          </div>
        )
      )}

      {!registryDown && family.length > 0 && (
        <section>
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Related artifacts</p>
          <div className="mt-1 divide-y divide-rule">
            {family.map((f) => (
              <Link key={f.artifact_id} to={`/research/${f.artifact_id}`} className="block py-1.5">
                <span className="text-[13px] text-primary hover:underline">{f.title}</span>
                <span className="ml-2 font-mono text-[11px] text-ink-3">· {f.artifact_type} · {f.modified}</span>
              </Link>
            ))}
          </div>
        </section>
      )}
      {registryDown && (
        <p className="text-xs text-negative">Artifact registry unavailable — related artifacts cannot be listed.</p>
      )}
    </div>
  );
}
