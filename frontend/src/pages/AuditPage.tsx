import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getDecisions, getGitLog, getModelRegistry } from "@/api/auditClient";
import { cn } from "@/lib/utils";
import { useLang } from "@/i18n/LanguageContext";

/**
 * Audit page (FD #86, WS-3 — UI-4): Decision Register + Audit Center +
 * Model Registry. Read-only operational/audit tracking (KANBAN-CONTRACT §1 —
 * card state never equals domain state). Borderless, ledger-based.
 */

function SectionHeader({ title, stamp }: { title: string; stamp: string }) {
  return (
    <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 border-b border-rule pb-2">
      <h2 className="font-display text-lg font-bold tracking-tight">{title}</h2>
      <span className="font-mono text-[10.5px] uppercase tracking-[0.1em] text-ink-3">{stamp}</span>
    </div>
  );
}

function ErrorNote({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="mt-3 rounded-[4px] bg-bg-panel px-4 py-3 text-[12.5px] text-ink-2">
      <p className="font-medium text-foreground">Could not load this section.</p>
      <p className="mt-1">{message}</p>
      <button type="button" onClick={onRetry} className="mt-2 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
        Retry →
      </button>
    </div>
  );
}

function SectionSkeleton() {
  return <div className="mt-3 space-y-2"><div className="h-4 w-full animate-pulse rounded-sm bg-bg-panel" /><div className="h-4 w-4/5 animate-pulse rounded-sm bg-bg-panel" /><div className="h-4 w-3/5 animate-pulse rounded-sm bg-bg-panel" /></div>;
}

export default function AuditPage() {
  const { lang } = useLang();
  const [search, setSearch] = useState("");

  const decisions = useQuery({ queryKey: ["audit-decisions"], queryFn: getDecisions, staleTime: 60_000 });
  const gitLog = useQuery({ queryKey: ["audit-git-log"], queryFn: getGitLog, staleTime: 60_000 });
  const registry = useQuery({ queryKey: ["audit-model-registry"], queryFn: getModelRegistry, staleTime: 60_000 });

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return decisions.data?.decisions ?? [];
    return (decisions.data?.decisions ?? []).filter(
      (d) => d.title.toLowerCase().includes(q) || d.preview.toLowerCase().includes(q)
    );
  }, [decisions.data, search]);

  const versions = useMemo(
    () => Object.entries(registry.data?.versions ?? {}).sort(([a], [b]) => a.localeCompare(b)),
    [registry.data]
  );

  return (
    <div className="mx-auto w-full max-w-[1120px] px-6 py-8">
      <header className="border-b border-ink pb-4">
        <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-primary">Operational Audit</p>
        <h1 className="mt-2 font-display text-[clamp(24px,3vw,32px)] font-bold tracking-tight">{lang === "th" ? "ทะเบียนการตัดสินใจและการตรวจสอบ" : "Decision Register &amp; Audit"}</h1>
        <p className="mt-2 max-w-[720px] text-[13.5px] leading-[1.6] text-ink-2">
          The Founder decision history, the git trail behind every published report, and the
          adapter registry — read-only, straight from the committed repository. No composite
          scores; every item below is the source record itself.
        </p>
      </header>

      {/* ── Section 1: Decision Register ── */}
      <section className="mt-8">
        <SectionHeader
          title="Decision Register"
          stamp={decisions.data ? `${decisions.data.decisions.length} items · ${decisions.data.data_source}` : "loading…"}
        />
        <div className="mt-3 flex items-center gap-2 text-[11px] text-ink-2">
          <label className="uppercase tracking-[0.08em]">Search</label>
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="title or text…"
            className="w-56 rounded-sm border border-rule bg-background px-1.5 py-0.5 font-mono text-[11px] text-ink-2 placeholder:text-ink-3"
          />
        </div>
        {decisions.isLoading && <SectionSkeleton />}
        {decisions.isError && <ErrorNote message={String(decisions.error)} onRetry={() => decisions.refetch()} />}
        {decisions.isSuccess && (
          <div className="mt-2">
            {filtered.length === 0 ? (
              <p className="mt-3 text-[12.5px] text-ink-3">No decisions match “{search}”. Clear the search to see the full register.</p>
            ) : (
              filtered.map((d) => (
                <div key={d.num} className="grid grid-cols-1 gap-x-5 gap-y-0.5 border-b border-rule px-1 py-2.5 sm:grid-cols-[64px_minmax(0,1fr)_92px]">
                  <span className="font-mono text-[11px] text-ink-3">#{d.num}</span>
                  <div>
                    <p className="font-display text-[14.5px] font-semibold tracking-tight">{d.title}</p>
                    <p className="mt-0.5 text-[12px] leading-[1.55] text-ink-2">{d.preview}</p>
                  </div>
                  <span className="font-mono text-[11px] text-ink-3 sm:text-right">{d.date}</span>
                </div>
              ))
            )}
          </div>
        )}
      </section>

      {/* ── Section 2: Audit Center (git trail + §23.9 corrections) ── */}
      <section className="mt-10">
        <SectionHeader title="Audit Center" stamp={gitLog.data ? `git_history · ${gitLog.data.commits.length} commits` : "loading…"} />
        <div className="mt-3 grid grid-cols-1 gap-8 lg:grid-cols-2">
          <div>
            <h3 className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-ink-3">Recent commits</h3>
            {gitLog.isLoading && <SectionSkeleton />}
            {gitLog.isError && <ErrorNote message={String(gitLog.error)} onRetry={() => gitLog.refetch()} />}
            {gitLog.isSuccess && (
              <div className="mt-1">
                {gitLog.data.commits.map((c) => (
                  <div key={c.hash} className="flex items-baseline gap-3 border-b border-rule px-1 py-1.5">
                    <span className="font-mono text-[10.5px] text-ink-3">{c.hash}</span>
                    <span className="font-mono text-[10.5px] text-ink-3">{c.date}</span>
                    <span className="min-w-0 flex-1 truncate text-[12.5px] text-ink">{c.subject}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div>
            <h3 className="text-[10.5px] font-bold uppercase tracking-[0.14em] text-ink-3">§23.9 Correction records</h3>
            {gitLog.isLoading && <SectionSkeleton />}
            {gitLog.isError && <ErrorNote message={String(gitLog.error)} onRetry={() => gitLog.refetch()} />}
            {gitLog.isSuccess && (
              <div className="mt-1">
                {gitLog.data.corrections.length === 0 ? (
                  <p className="mt-3 text-[12.5px] text-ink-3">No correction records committed yet.</p>
                ) : (
                  gitLog.data.corrections.map((c) => (
                    <div key={c.path} className="flex items-baseline gap-3 border-b border-rule px-1 py-1.5">
                      <span className="min-w-0 flex-1 truncate font-mono text-[11px] text-ink-2">{c.path}</span>
                      <span className="font-mono text-[10.5px] text-ink-3">
                        {new Date(c.modified * 1000).toISOString().slice(0, 10)}
                      </span>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* ── Section 3: Model Registry ── */}
      <section className="mt-10">
        <SectionHeader title="Model Registry" stamp={registry.data ? `adapter_registry · current ${registry.data.current_version}` : "loading…"} />
        {registry.isLoading && <SectionSkeleton />}
        {registry.isError && <ErrorNote message={String(registry.error)} onRetry={() => registry.refetch()} />}
        {registry.isSuccess && (
          <div className="mt-2">
            <p className="max-w-[720px] text-[12.5px] leading-[1.6] text-ink-2">
              The pipeline adapter registry is an immutable version → committed-code-hash map
              (plan T5 / council F3). Each version pins the exact adapters.py source; editing
              the registry can never change the code hash.
            </p>
            <div className="mt-3 max-w-[520px]">
              {versions.map(([v, hash]) => (
                <div key={v} className="flex items-baseline gap-3 border-b border-rule px-1 py-1.5">
                  <span className={cn("w-8 font-mono text-[11px]", v === registry.data.current_version ? "font-bold text-primary" : "text-ink-2")}>
                    {v}
                  </span>
                  <span className="truncate font-mono text-[10.5px] text-ink-3">{hash.slice(0, 16)}…</span>
                  {v === registry.data.current_version && (
                    <span className="text-[10px] font-semibold uppercase tracking-[0.1em] text-positive">current</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
