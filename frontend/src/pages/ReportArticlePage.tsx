import { useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getReport, getReports, type ReportDetail, type ReportMeta } from "@/api/reportClient";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

/**
 * Typeset report article — Long Document treatment (Hallmark macro 02,
 * FD #85/B second pass).
 * Markdown SOURCE rendered as a magazine feature: article hero (kicker +
 * display headline + standfirst + provenance chips), continuous-prose body
 * (measure 65ch, section heads emerge from the flow, roman pull-quotes —
 * `.article-body` in index.css), series footer navigation. The reader never
 * sees raw markdown.
 */

const TYPE_LABEL: Record<string, string> = {
  company: "Company Research Note",
  product: "Product Research Note",
  weekly: "Weekly Brief",
  quarterly: "Quarterly Report",
  theme: "Theme Note",
};

function statusTone(status: string): string | undefined {
  if (status === "published") return "text-positive";
  if (status === "review") return "text-warning";
  return "text-ink-3";
}

function TitleBlock({ r }: { r: ReportDetail }) {
  return (
    <header>
      <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-primary">
        {TYPE_LABEL[r.type] ?? r.type}
        {r.subject ? ` · ${r.subject}` : ""}
      </p>
      <h1 className="mt-3 font-display text-[clamp(28px,4vw,40px)] font-bold leading-[1.08] tracking-[-0.015em]">
        {r.title}
      </h1>
      {r.summary && <p className="mt-3 max-w-[700px] text-[16.5px] leading-[1.6] text-ink-2">{r.summary}</p>}
      <p className="mt-4 font-mono text-[11px] text-ink-3">
        {r.date}
        {r.author ? ` · by ${r.author}` : ""}
        {r.updated && r.updated !== r.date ? ` · updated ${r.updated}` : ""}
        <span className={cn("ml-3 font-sans text-[10.5px] font-semibold uppercase tracking-[0.12em]", statusTone(r.status))}>
          {r.status}
        </span>
      </p>
      {/* Provenance — borderless hairline strip (FD #85/B, FD #84 no-box) */}
      <div className="mt-4 flex flex-wrap gap-x-5 gap-y-1.5 border-t border-rule pt-3 text-[11px] text-ink-2">
        <span className="inline-flex items-center gap-1.5">
          <span className="size-1.5 rounded-full bg-positive" aria-hidden="true" /> Real data · sourced &amp; dated
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="size-1.5 rounded-full bg-info" aria-hidden="true" /> Portfolio-blind
        </span>
        <span className="inline-flex items-center gap-1.5">
          <span className="size-1.5 rounded-full bg-ink-3" aria-hidden="true" /> Advisory only — no buy/sell instruction
        </span>
      </div>
    </header>
  );
}

export default function ReportArticlePage() {
  const { slug = "" } = useParams();
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["report", slug],
    queryFn: () => getReport(slug),
    enabled: Boolean(slug),
  });
  const index = useQuery({ queryKey: ["reports"], queryFn: getReports, staleTime: 30_000 });

  const report = data?.report;
  const content = useMemo(() => {
    if (!report) return "";
    // Strip the leading H1 (title lives in the title block, not the body).
    return report.content.replace(/^#\s+.+\n+/, "");
  }, [report]);

  const siblings = useMemo(() => {
    if (!report) return { prev: undefined, next: undefined } as { prev?: ReportMeta; next?: ReportMeta };
    const sameSubject = (index.data?.reports ?? [])
      .filter((r) => r.subject === report.subject && r.slug !== report.slug)
      .sort((a, b) => a.date.localeCompare(b.date));
    const idx = sameSubject.findIndex((r) => r.date > report.date);
    return {
      next: idx >= 0 ? sameSubject[idx] : undefined,
      prev: idx > 0 ? sameSubject[idx - 1] : sameSubject[sameSubject.length - 1],
    };
  }, [report, index.data]);

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error || !report) {
    const status404 = (error as { status?: number } | null)?.status === 404;
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">{status404 ? "Report not found." : "Could not load this report."}</p>
        {!status404 && (
          <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
            Retry →
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-bg-page">
      <div className="mx-auto w-full max-w-[820px] flex-1 px-6 py-6">
      <Link to="/library" className="inline-flex items-center gap-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-3 hover:text-foreground">
        <ArrowLeft className="size-3.5" /> Library
      </Link>

      <div className="mt-4">
        <TitleBlock r={report} />
      </div>

      <article className="article-body mt-8">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            table: ({ children }) => (
              <div className="overflow-x-auto">
                <table>{children}</table>
              </div>
            ),
          }}
        >
          {content}
        </ReactMarkdown>
      </article>

      <footer className="mt-10 flex items-baseline justify-between gap-4 border-t border-rule pt-4 text-[11px] text-ink-3">
        <span>Research Intelligence · {report.date}</span>
        <div className="flex items-baseline gap-5">
          {siblings.next && (
            <Link to={`/library/${siblings.next.slug}`} className="font-semibold uppercase tracking-[0.1em] text-primary hover:text-foreground">
              Later {report.subject} note →
            </Link>
          )}
          {siblings.prev && (
            <Link to={`/library/${siblings.prev.slug}`} className="font-semibold uppercase tracking-[0.1em] text-primary hover:text-foreground">
              ← Earlier {report.subject} note
            </Link>
          )}
        </div>
      </footer>
      </div>
      {/* ── Magazine footer (standalone shell — FD #84) ── */}
      <footer className="mx-auto w-full max-w-[1120px] border-t border-ink px-6 py-5 text-[10px] uppercase tracking-[0.12em] text-ink-3">
        Advisory only · Portfolio-blind · Point-in-time data (FD #58)
      </footer>
    </div>
  );
}
