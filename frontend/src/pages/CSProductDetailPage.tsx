import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getCSProduct, type CSAsset } from "@/api/csClient";
import { Skeleton } from "@/components/ui/skeleton";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

/** Close System product note (P2 — institutional standard, FD #60).
 *  One-scroll research note; macro context is honest about its depth limit
 *  (single-line pipeline assessments today — known limit, not hidden). */

const LAYER_LABELS: Record<string, string> = {
  L1_macro: "Macro economics",
  L2_policy: "Government policy",
  L3_cost: "Cost structure",
  L4_supply_demand: "Supply / demand",
  L5_hidden: "Hidden signals",
};

const SIGNAL_LABEL: Record<string, string> = {
  supporting: "supporting",
  contradicting: "contradicting",
  neutral: "neutral",
};

function signalTone(s: string): string | undefined {
  if (s === "supporting") return "text-positive";
  if (s === "contradicting") return "text-negative";
  return undefined;
}

function Row({ k, v, tone }: { k: string; v: string; tone?: string }) {
  return (
    <div className="flex items-baseline justify-between gap-6 border-b border-rule/60 py-1.5 last:border-b-0">
      <span className="text-[12px] text-ink-2">{k}</span>
      <span className={cn("font-mono text-[12.5px] tabular-nums", tone ?? "text-foreground")}>{v}</span>
    </div>
  );
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

function LayerAssessment({ keyName, layer }: { keyName: string; layer: { signal: string; note: string } }) {
  return (
    <div className="border-b border-rule/60 py-2.5 last:border-b-0">
      <p className="flex items-baseline gap-2 text-[11px] font-bold uppercase tracking-[0.14em]">
        {LAYER_LABELS[keyName] ?? keyName}
        <span className={cn("font-mono font-normal normal-case tracking-normal", signalTone(layer.signal) ?? "text-ink-3")}>
          {SIGNAL_LABEL[layer.signal] ?? layer.signal}
        </span>
      </p>
      {layer.note && <p className="mt-1 text-[13px] leading-relaxed text-ink-2">{layer.note}</p>}
    </div>
  );
}

export default function CSProductDetailPage() {
  const { id = "" } = useParams();
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cs-product", id],
    queryFn: () => getCSProduct(id),
    enabled: Boolean(id),
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error || !data) {
    const status404 = (error as { status?: number } | null)?.status === 404;
    return (
      <div className="rounded-md bg-bg-panel px-4 py-8">
        <p className="text-sm font-medium text-negative">
          {status404 ? `Product ${id} not found in the Close System radar.` : "Close System detail unavailable — API error."}
        </p>
        {!status404 && (
          <button type="button" onClick={() => refetch()} className="mt-3 text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
            Retry →
          </button>
        )}
      </div>
    );
  }

  const a: CSAsset = data.asset;
  const layers = Object.entries(a.layers ?? {});
  const macroLayers = layers.filter(([k]) => k === "L1_macro" || k === "L2_policy");
  const fundamentalLayers = layers.filter(([k]) => k === "L3_cost" || k === "L4_supply_demand" || k === "L5_hidden");
  const discountRows = Object.entries(a.discount_detail ?? {});
  const demandRows = Object.entries(a.demand_detail ?? {});
  const allPass = a.p1_pass && a.p2_pass && a.p3_pass;

  return (
    <div className="mx-auto max-w-[880px]">
      <Link to="/cs-radar" className="inline-flex items-center gap-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-3 hover:text-foreground">
        <ArrowLeft className="size-3.5" /> Close System radar
      </Link>

      <header className="mt-4 border-b border-rule pb-6">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{a.category}</span>
          <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-ink-3">
            Synthetic data
          </span>
        </div>
        <h1 className="mt-2 font-display text-h1 font-bold leading-tight tracking-tight">
          {a.ticker} — {a.name}
        </h1>
        <p className="mt-1 font-mono text-[12px] text-ink-2">
          {a.currency} {a.current_price} · {a.status} · {a.conviction} conviction
        </p>
      </header>

      <section>
        <SectionKicker n="01" title="The question" />
        <h2 className="mt-3 font-display text-[22px] font-semibold leading-snug tracking-tight">
          Does {a.ticker} deserve a place on the radar?
        </h2>
        <p className="mt-2 max-w-[720px] text-[13.5px] leading-relaxed text-ink-2">
          The pipeline rates it <span className="font-semibold text-foreground">{a.conviction.toLowerCase()} conviction</span> with{" "}
          <span className="font-semibold text-foreground">{a.layers_aligned} of {layers.length} layers aligned</span>.{" "}
          {a.recommendation}. Eligibility:{" "}
          <span className={cn("font-semibold", allPass ? "text-positive" : "text-negative")}>
            {allPass ? "passes all three checks" : "does not pass all three checks"}
          </span>
          .
        </p>
      </section>

      <section>
        <SectionKicker n="02" title="Why it is on the radar" />
        <div className="mt-3 grid grid-cols-1 gap-x-10 md:grid-cols-2">
          <Row k="P1 — cannot go to zero" v={a.p1_pass ? "PASS" : "FAIL"} tone={a.p1_pass ? "text-positive" : "text-negative"} />
          <Row k="P2 — discount pricing" v={a.p2_pass ? "PASS" : "FAIL"} tone={a.p2_pass ? "text-positive" : "text-negative"} />
          <Row k="P3 — structural demand" v={a.p3_pass ? "PASS" : "FAIL"} tone={a.p3_pass ? "text-positive" : "text-negative"} />
          <Row k="Discount type" v={a.discount_type || "—"} />
          <Row k="Discount depth" v={a.discount_depth || "—"} />
          <Row k="Demand type" v={a.demand_type || "—"} />
        </div>
        {a.p1_rationale && <p className="mt-3 max-w-[720px] text-[13px] leading-relaxed text-ink-2">{a.p1_rationale}</p>}
      </section>

      <section>
        <SectionKicker n="03" title="Commodity fundamentals" />
        {discountRows.length > 0 && (
          <div className="mt-3">
            <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">Discount / cost detail</p>
            <div className="mt-1 grid grid-cols-1 gap-x-10 md:grid-cols-2">
              {discountRows.map(([k, v]) => (
                <Row key={k} k={k.replace(/_/g, " ")} v={String(v)} />
              ))}
            </div>
          </div>
        )}
        {demandRows.length > 0 && (
          <div className="mt-4">
            <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">Demand breakdown</p>
            <div className="mt-1 grid grid-cols-1 gap-x-10 md:grid-cols-2">
              {demandRows.map(([k, v]) => (
                <Row key={k} k={k.replace(/_/g, " ")} v={String(v)} />
              ))}
            </div>
          </div>
        )}
        {fundamentalLayers.length > 0 && (
          <div className="mt-4">
            {fundamentalLayers.map(([k, layer]) => (
              <LayerAssessment key={k} keyName={k} layer={layer} />
            ))}
          </div>
        )}
        {discountRows.length === 0 && demandRows.length === 0 && fundamentalLayers.length === 0 && (
          <p className="mt-3 text-[12.5px] text-ink-3">No commodity detail in this artifact yet.</p>
        )}
      </section>

      <section>
        <SectionKicker n="04" title="Macro context" />
        {macroLayers.length > 0 ? (
          <div className="mt-3">
            {macroLayers.map(([k, layer]) => (
              <LayerAssessment key={k} keyName={k} layer={layer} />
            ))}
            <p className="mt-3 max-w-[720px] text-[12px] leading-relaxed text-ink-2">
              Each dimension currently carries a single-line assessment from the pipeline. The macro backdrop for
              this product deserves deeper context — this is a known limit of the current data, not the full picture.
            </p>
          </div>
        ) : (
          <p className="mt-3 text-[12.5px] text-ink-3">No macro layer in this artifact yet.</p>
        )}
      </section>

      <section>
        <SectionKicker n="05" title="Close System assessment" />
        <div className="mt-3 grid grid-cols-2 gap-x-10 md:grid-cols-4">
          <Row k="Layers aligned" v={`${a.layers_aligned}/${layers.length}`} />
          <Row k="Contradicting" v={String(a.layers_contradicting)} tone={a.layers_contradicting > 0 ? "text-warning" : undefined} />
          <Row k="Conviction" v={a.conviction} />
          <Row k="Recommendation" v={a.recommendation} />
        </div>
        {a.recommendation_rationale && (
          <p className="mt-3 max-w-[720px] text-[13px] leading-relaxed text-ink-2">{a.recommendation_rationale}</p>
        )}
        {a.key_risks.length > 0 && (
          <div className="mt-4">
            <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-ink-3">Key risks</p>
            <ul className="mt-1 space-y-1">
              {a.key_risks.map((r) => (
                <li key={r} className="border-b border-rule/60 py-1 text-[13px] leading-relaxed text-ink-2">— {r}</li>
              ))}
            </ul>
          </div>
        )}
        <p className="mt-4 text-[12px] leading-relaxed text-ink-2">
          Alpha Momentum applies its own entry-condition checks; the Close System surface does not produce them.
        </p>
      </section>

      <section>
        <SectionKicker n="06" title="Challenge & evidence" />
        <p className="mt-3 text-[12.5px] leading-relaxed text-ink-2">
          No challenge record is attached to this product yet. An options overlay is deferred — no options
          pipeline exists; instrument structure and strategy families will appear here when an options surface
          is authorized.
        </p>
      </section>

      <section className="mt-10 rounded-md bg-bg-panel px-4 py-3">
        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-ink-3">Analysis limits</p>
        <p className="mt-1 text-[12px] leading-relaxed text-ink-2">
          This note reflects the current pipeline artifact, which is synthetic demonstration data: layer
          assessments are single-line, macro depth is limited, and no challenge record exists. Treat the
          assessment as directional, not conclusive.
        </p>
      </section>
    </div>
  );
}
