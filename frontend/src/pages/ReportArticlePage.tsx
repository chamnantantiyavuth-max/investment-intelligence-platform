import { useMemo } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ReactMarkdown from "react-markdown";
import { getReport, getReports, type ReportDetail, type ReportMeta } from "@/api/reportClient";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

/** Typeset report article (FD #62) — markdown SOURCE rendered as a professional
 *  research note. The reader never sees markdown: headings, prose, tables, and
 *  quotes are mapped to the typeset standard. */

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
    <header className="border-b border-rule pb-6">
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{TYPE_LABEL[r.type] ?? r.type}</span>
        {r.subject && <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.08em] text-ink-2">{r.subject}</span>}
        <span className={cn("text-[10.5px] font-semibold uppercase tracking-[0.12em]", statusTone(r.status))}>{r.status}</span>
      </div>
      <h1 className="mt-2 font-display text-h1 font-bold leading-tight tracking-tight">{r.title}</h1>
      <p className="mt-2 font-mono text-[12px] text-ink-2">
        {r.date}
        {r.author ? ` · by ${r.author}` : ""}
        {r.updated && r.updated !== r.date ? ` · updated ${r.updated}` : ""}
      </p>
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
    <div className="mx-auto max-w-[820px]">
      <Link to="/library" className="inline-flex items-center gap-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-3 hover:text-foreground">
        <ArrowLeft className="size-3.5" /> Library
      </Link>

      <div className="mt-4">
        <TitleBlock r={report} />
      </div>

      <article className="mt-8 space-y-0 [&_h2]:mt-10 [&_h2]:border-b [&_h2]:border-rule [&_h2]:pb-2 [&_h2]:font-display [&_h2]:text-[20px] [&_h2]:font-semibold [&_h2]:tracking-tight [&_h3]:mt-6 [&_h3]:font-display [&_h3]:text-[16px] [&_h3]:font-semibold [&_h3]:tracking-tight [&_p]:mt-3 [&_p]:text-[14.5px] [&_p]:leading-[1.75] [&_p]:text-ink-1 [&_ul]:mt-3 [&_ul]:space-y-1.5 [&_ul]:pl-5 [&_ul]:list-disc [&_ol]:mt-3 [&_ol]:space-y-1.5 [&_ol]:pl-5 [&_ol]:list-decimal [&_li]:text-[14px] [&_li]:leading-relaxed [&_li]:text-ink-2 [&_strong]:font-semibold [&_strong]:text-foreground [&_em]:italic [&_a]:text-primary [&_a]:underline [&_blockquote]:my-6 [&_blockquote]:border-l-2 [&_blockquote]:border-primary/40 [&_blockquote]:pl-4 [&_blockquote]:font-display [&_blockquote]:text-[16px] [&_blockquote]:italic [&_blockquote]:leading-relaxed [&_blockquote]:text-ink-2">
        <ReactMarkdown
          components={{
            table: ({ children }) => (
              <div className="my-6 overflow-x-auto">
                <table className="w-full border-collapse text-[13px]">{children}</table>
              </div>
            ),
            thead: ({ children }) => <thead className="border-b border-rule">{children}</thead>,
            th: ({ children }) => (
              <th className="px-2 py-1.5 text-left text-[10px] font-bold uppercase tracking-[0.12em] text-ink-3">{children}</th>
            ),
            td: ({ children }) => <td className="border-b border-rule/50 px-2 py-1.5 align-top font-mono text-[12px] tabular-nums text-ink-2">{children}</td>,
          }}
        >
          {content}
        </ReactMarkdown>
      </article>

      <footer className="mt-10 flex items-baseline justify-between border-t border-rule pt-4 text-[11px] text-ink-3">
        <span>Research library · {report.date}</span>
        {siblings.prev && (
          <Link to={`/library/${siblings.prev.slug}`} className="font-semibold uppercase tracking-[0.1em] text-primary hover:text-foreground">
            ← Earlier {report.subject} note
          </Link>
        )}
      </footer>
    </div>
  );
}
