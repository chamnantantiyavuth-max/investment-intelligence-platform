import { useQuery } from "@tanstack/react-query";
import { useParams, Link } from "react-router-dom";
import { getFOPackage } from "@/api/foClient";
import type { MoatType, ConvictionDetail } from "@/types/fo";
import { Skeleton } from "@/components/ui/skeleton";
import { ProvenanceChip } from "@/components/ProvenanceChip";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

/** Company research note (P2 reference — institutional standard, FD #60).
 *  Narrative-led: investment question first, then evidence, then honest limits.
 *  No internal jargon; provenance is a discreet chip; numbers are the story. */

function s(v: unknown): string {
  return typeof v === "string" ? v : "";
}
function n(v: unknown): number {
  return typeof v === "number" && Number.isFinite(v) ? v : 0;
}
function pct(x: number): string {
  return `${(x * 100).toFixed(1)}%`;
}
function mult(x: number): string {
  return `${x.toFixed(2)}x`;
}
function truthy(x: number, f: (v: number) => string): string {
  return x ? f(x) : "—";
}
function asConviction(v: unknown): ConvictionDetail {
  if (v && typeof v === "object") {
    const o = v as Record<string, unknown>;
    return { level: s(o.level), cap: s(o.cap), rationale: s(o.rationale) };
  }
  return { level: "", cap: "", rationale: "" };
}
function asMoatTypes(v: unknown): MoatType[] {
  return Array.isArray(v) ? (v as MoatType[]) : [];
}

function SectionKicker({ n: num, title }: { n: string; title: string }) {
  return (
    <div className="mt-10 border-b border-rule pb-2">
      <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink-3">
        {num} · {title}
      </p>
    </div>
  );
}

function Row({ k, v, tone }: { k: string; v: string; tone?: "pos" | "neg" | "warn" }) {
  return (
    <div className="flex items-baseline justify-between gap-6 border-b border-rule/60 py-1.5 last:border-b-0">
      <span className="text-[12px] text-ink-2">{k}</span>
      <span
        className={cn(
          "font-mono text-[12.5px] tabular-nums",
          tone === "pos" ? "text-positive" : tone === "neg" ? "text-negative" : tone === "warn" ? "text-warning" : "text-foreground"
        )}
      >
        {v}
      </span>
    </div>
  );
}

export default function FundamentalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: pkg, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-package", id],
    queryFn: () => getFOPackage(id!),
    enabled: !!id,
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error)
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">Could not load this research note.</p>
        <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          Retry →
        </button>
      </div>
    );
  if (!pkg) return <div className="rounded-md bg-bg-panel px-4 py-8 text-sm text-ink-2">Company not found.</div>;

  const moat = (pkg.company_assessment?.moat ?? {}) as Record<string, unknown>;
  const fq = (pkg.company_assessment?.financial_quality ?? {}) as Record<string, unknown>;
  const ca = (pkg.company_assessment?.capital_allocation ?? {}) as Record<string, unknown>;
  const macro = pkg.macro_context ?? {};
  const ind = pkg.industry_assessment ?? {};
  const val = pkg.valuation_context ?? {};
  const vt = (val?.value_trap ?? {}) as Record<string, unknown>;
  const conviction = asConviction(pkg.conviction);
  const moatTypes = asMoatTypes(moat?.types);
  const price = n(val?.current_price);
  const peTtm = n(val?.pe_ttm);
  const pe5y = n(val?.pe_5y_avg);
  const premium = peTtm && pe5y ? (peTtm / pe5y - 1) * 100 : 0;
  const scenarioMissing = !n(val?.scenario_bull) && !n(val?.scenario_base) && !n(val?.scenario_bear);
  const risks = pkg.key_risks ?? [];
  const challenges = pkg.independent_challenge ?? [];
  const supporting = pkg.supporting_evidence ?? [];
  const contradicting = pkg.contradicting_evidence ?? [];
  const openQuestions = pkg.open_questions ?? [];
  const hasDataGaps =
    moatTypes.length === 0 ||
    scenarioMissing ||
    !s(pkg.earnings_trajectory?.surprise_direction) ||
    risks.length === 0 ||
    challenges.length === 0;

  return (
    <div className="mx-auto max-w-[880px]">
      <Link to="/fundamental" className="inline-flex items-center gap-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-3 hover:text-foreground">
        <ArrowLeft className="size-3.5" /> Fundamental queue
      </Link>

      <header className="mt-4 border-b border-rule pb-6">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{s(ind?.sector)} · {s(ind?.industry)}</span>
          <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-[0.08em] text-ink-2">
            {s(ind?.position)}
          </span>
          <ProvenanceChip mode={pkg.provenance?.mode} source={pkg.provenance?.source} asOf={pkg.provenance?.as_of} />
        </div>
        <h1 className="mt-2 font-display text-h1 font-bold leading-tight tracking-tight">
          {pkg.name} <span className="text-ink-3">({pkg.id})</span>
        </h1>
        <p className="mt-1 font-mono text-[12px] text-ink-2">
          {price ? `US$${price.toFixed(2)}` : "Price n/a"} · {s(macro?.regime)} · thesis {s(pkg.thesis_lifecycle).toLowerCase()}
        </p>
      </header>

      <section>
        <SectionKicker n="01" title="The question" />
        <h2 className="mt-3 font-display text-[22px] font-semibold leading-snug tracking-tight">
          Does {pkg.name} deserve further investigation?
        </h2>
        <p className="mt-2 max-w-[720px] text-[13.5px] leading-relaxed text-ink-2">
          {conviction.level ? (
            <>
              The pipeline's current assessment is <span className="font-semibold text-foreground">{conviction.level.toLowerCase()} conviction</span>
              {conviction.rationale ? ` — ${conviction.rationale.replace(/\.+$/, "").toLowerCase()}` : ""}. Position in its industry:{" "}
              <span className="font-semibold text-foreground">{s(ind?.position).toLowerCase()}</span>. It trades{" "}
              {premium > 0 ? (
                <>
                  at a <span className="font-semibold text-warning">{Math.round(premium)}% premium</span> to its own five-year average P/E
                </>
              ) : peTtm ? (
                "at or below its own five-year average P/E"
              ) : (
                "at a valuation the pipeline could not yet compare"
              )}
              , and the value-trap screen is {s(vt?.verdict) ? <span className="font-semibold text-foreground">{s(vt.verdict).toLowerCase()}</span> : "not triggered"}.
            </>
          ) : (
            "The pipeline has not produced a conviction assessment for this company yet."
          )}
        </p>
      </section>

      <section>
        <SectionKicker n="02" title="Business & macro backdrop" />
        <div className="mt-3 grid grid-cols-2 gap-x-10 md:grid-cols-3">
          <Row k="Industry" v={s(ind?.industry) || "—"} />
          <Row k="Position" v={s(ind?.position) || "—"} />
          <Row k="Macro regime" v={s(macro?.regime) || "—"} />
          <Row k="GDP growth" v={truthy(n(macro?.gdp_growth), pct)} />
          <Row k="Inflation" v={truthy(n(macro?.inflation), pct)} />
          <Row k="Fed funds" v={truthy(n(macro?.fed_funds), pct)} />
        </div>
        {s(macro?.sector_implication) && (
          <p className="mt-3 max-w-[720px] text-[13px] leading-relaxed text-ink-2">{s(macro?.sector_implication)}</p>
        )}
      </section>

      <section>
        <SectionKicker n="03" title="Financial quality & capital allocation" />
        <div className="mt-3 grid grid-cols-2 gap-x-10 md:grid-cols-3">
          <Row k="Gross margin" v={truthy(n(fq?.gross_margin), pct)} />
          <Row k="Operating margin" v={truthy(n(fq?.operating_margin), pct)} />
          <Row k="Return on equity" v={truthy(n(fq?.roe), pct)} />
          <Row k="FCF conversion" v={truthy(n(fq?.fcf_conversion), mult)} />
          <Row k="Debt / equity" v={truthy(n(fq?.debt_to_equity), (x) => x.toFixed(2))} />
          <Row k="Revenue growth (3y)" v={truthy(n(fq?.revenue_growth_3y), pct)} />
          <Row k="Capital allocation" v={s(ca?.quality) || "—"} tone={s(ca?.quality) === "GOOD" ? "pos" : undefined} />
          <Row k="Free cash flow" v={ca?.fcf_available === true ? "available" : "—"} />
          <Row k="Buyback impact" v={truthy(n(ca?.buyback_impact), pct)} />
        </div>
      </section>

      <section>
        <SectionKicker n="04" title="Moat" />
        <div className="mt-3 grid grid-cols-3 gap-x-10">
          <Row k="Width" v={s(moat?.width) || "—"} tone={s(moat?.width) === "Wide" ? "pos" : s(moat?.width) === "None" ? "warn" : undefined} />
          <Row k="Depth" v={s(moat?.depth) || "—"} tone={s(moat?.depth) === "Deep" ? "pos" : s(moat?.depth) === "Shallow" ? "warn" : undefined} />
          <Row k="Trend" v={s(moat?.trend) || "—"} tone={s(moat?.trend) === "Widening" ? "pos" : s(moat?.trend) === "Narrowing" ? "neg" : undefined} />
        </div>
        {moatTypes.length > 0 ? (
          <div className="mt-3 flex flex-wrap gap-2">
            {moatTypes.map((t, i) => (
              <span
                key={i}
                className={cn(
                  "rounded-sm px-2 py-0.5 text-[11px] font-medium",
                  t.strength === "Strong" ? "bg-positive/10 text-positive" : t.strength === "Moderate" ? "bg-warning/10 text-warning" : "bg-negative/10 text-negative"
                )}
              >
                {t.type} · {t.strength}
              </span>
            ))}
          </div>
        ) : (
          <p className="mt-3 max-w-[720px] text-[12.5px] leading-relaxed text-ink-2">
            The current model has not identified qualitative moat types for this company. The quantitative
            foundation above (margins, returns, cash conversion) is the evidence available today; a
            qualitative moat narrative is not yet produced.
          </p>
        )}
        {s(moat?.moat_narrative) && <p className="mt-3 max-w-[720px] text-[13px] leading-relaxed text-ink-2">{s(moat?.moat_narrative)}</p>}
      </section>

      <section>
        <SectionKicker n="05" title="Earnings trajectory" />
        <div className="mt-3 flex flex-wrap items-baseline gap-x-4 gap-y-1">
          <span className={cn("text-[13px] font-semibold", s(pkg.earnings_trajectory?.rating) === "HIGH" ? "text-positive" : s(pkg.earnings_trajectory?.rating) === "LOW" ? "text-negative" : "text-foreground")}>
            {s(pkg.earnings_trajectory?.rating) || "—"} quality
          </span>
          {s(pkg.earnings_trajectory?.conviction_impact) && <span className="text-[13px] text-ink-2">{s(pkg.earnings_trajectory?.conviction_impact)}</span>}
        </div>
        {s(pkg.earnings_trajectory?.narrative) && (
          <p className="mt-2 max-w-[720px] text-[13px] leading-relaxed text-ink-2">{s(pkg.earnings_trajectory?.narrative)}</p>
        )}
        <div className="mt-3 grid grid-cols-2 gap-x-10 md:grid-cols-4">
          <Row k="Surprise" v={s(pkg.earnings_trajectory?.surprise_direction) || "—"} />
          <Row k="FCF conversion" v={truthy(n(pkg.earnings_trajectory?.fcf_conversion), mult)} />
          <Row k="One-time items" v={pkg.earnings_trajectory?.one_time_items ? "yes" : "no"} />
          <Row k="Guidance" v={s(pkg.earnings_trajectory?.guidance_direction) || "—"} />
        </div>
      </section>

      <section>
        <SectionKicker n="06" title="Valuation" />
        <div className="mt-3 grid grid-cols-2 gap-x-10 md:grid-cols-4">
          <Row k="P/E (ttm)" v={truthy(peTtm, (x) => `${x.toFixed(1)}x`)} />
          <Row k="P/E (5y avg)" v={truthy(pe5y, (x) => `${x.toFixed(1)}x`)} />
          <Row k="EV / EBITDA" v={truthy(n(val?.ev_ebitda), (x) => `${x.toFixed(1)}x`)} />
          <Row k="FCF yield" v={truthy(n(val?.fcf_yield), pct)} />
        </div>
        {premium > 0 && (
          <p className="mt-3 max-w-[720px] text-[12.5px] leading-relaxed text-warning">
            Trading at a {Math.round(premium)}% premium to its own five-year average P/E — the valuation carries
            an expectation of continued growth.
          </p>
        )}
        {scenarioMissing && (
          <p className="mt-2 max-w-[720px] text-[12.5px] leading-relaxed text-ink-2">
            Scenario valuation (bull / base / bear) is not yet produced for this company.
          </p>
        )}
        {s(vt?.verdict) && (
          <div className="mt-3 rounded-md bg-bg-panel px-4 py-3">
            <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-ink-2">Value-trap screen</p>
            <p className="mt-1 text-[13px] text-foreground">{s(vt.verdict)}</p>
            {s(vt?.action) && <p className="mt-0.5 text-[12px] text-ink-2">{s(vt.action)}</p>}
          </div>
        )}
      </section>

      <section>
        <SectionKicker n="07" title="Risks, challenge & evidence" />
        <div className="mt-3 space-y-4">
          {risks.length > 0 ? (
            <ul className="space-y-1.5">
              {risks.map((r, i) => (
                <li key={i} className="text-[13px] leading-relaxed text-ink-2">• {r}</li>
              ))}
            </ul>
          ) : (
            <p className="text-[12.5px] text-ink-3">No risks assessed from available data.</p>
          )}
          {challenges.length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-ink-3">Independent challenge</p>
              <ul className="mt-1.5 space-y-1.5">
                {challenges.map((c, i) => (
                  <li key={i} className="text-[13px] leading-relaxed text-ink-2">• {c}</li>
                ))}
              </ul>
            </div>
          )}
          {supporting.length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-positive">Supporting evidence</p>
              <ul className="mt-1.5 space-y-1.5">
                {supporting.map((e, i) => (
                  <li key={i} className="text-[13px] leading-relaxed text-ink-2">• {e}</li>
                ))}
              </ul>
            </div>
          )}
          {contradicting.length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.14em] text-ink-3">Contradicting evidence</p>
              <ul className="mt-1.5 space-y-1.5">
                {contradicting.map((e, i) => (
                  <li key={i} className="text-[13px] leading-relaxed text-ink-2">• {e}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </section>

      <section>
        <SectionKicker n="08" title="Open questions" />
        <ul className="mt-3 space-y-1.5">
          {openQuestions.length > 0 ? (
            openQuestions.map((q, i) => (
              <li key={i} className="text-[13px] leading-relaxed text-ink-2">• {q}</li>
            ))
          ) : (
            <li className="text-[12.5px] text-ink-3">No open questions recorded.</li>
          )}
        </ul>
      </section>

      {hasDataGaps && (
        <section className="mt-10 rounded-md bg-bg-panel px-4 py-3">
          <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink-3">Analysis limits</p>
          <p className="mt-1 text-[12px] leading-relaxed text-ink-2">
            This note reflects the data the pipeline currently admits. Qualitative moat types, scenario
            valuation, and some earnings detail fields are not yet produced — the gaps above are real, not
            hidden. The company story deepens as the underlying research layer grows.
          </p>
        </section>
      )}
    </div>
  );
}
