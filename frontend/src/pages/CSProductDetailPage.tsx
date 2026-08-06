import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getCSProduct, type CSAsset } from "@/api/csClient";
import { EmptyState } from "@/components/EmptyState";
import { Skeleton } from "@/components/ui/skeleton";

// FD #57: /cs-radar/:productId — product detail from the v0.1 pipeline artifact
// (SYNTHETIC-labeled). Options Overlay DEFERRED (no options pipeline; template 09
// research-only) — honest note, never invented data.

const SECTIONS = [
  "Product Thesis",
  "Commodity Fundamentals",
  "Macro Context",
  "Close System Assessment",
  "Challenge & Evidence",
] as const;
type Section = (typeof SECTIONS)[number];

const LAYER_LABELS: Record<string, string> = {
  L1_macro: "Macro Economics",
  L2_policy: "Government Policy",
  L3_cost: "Cost Structure",
  L4_supply_demand: "Supply / Demand Balance",
  L5_hidden: "Hidden Signals",
};

function Row({ k, v, mono = true }: { k: string; v: string; mono?: boolean }) {
  return (
    <div className="flex justify-between gap-6 border-b border-rule py-1.5 text-[13px]">
      <span className="shrink-0 text-ink-2">{k}</span>
      <span className={`text-right ${mono ? "font-mono text-[11px] text-ink-3" : "max-w-[70%] text-ink-3"}`}>{v}</span>
    </div>
  );
}

export default function CSProductDetailPage() {
  const { id = "" } = useParams();
  const [section, setSection] = useState<Section>("Product Thesis");
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cs-product", id],
    queryFn: () => getCSProduct(id),
    enabled: Boolean(id),
  });

  if (isLoading) return <Skeleton className="h-64 w-full" />;
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
        <Link to="/cs-radar" className="mt-3 inline-block text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
          ← Close System Radar
        </Link>
      </div>
    );
  }

  const a: CSAsset = data.asset;
  const layers = Object.entries(a.layers);
  const signalTone = (s: string) =>
    s === "supporting" ? "text-positive" : s === "contradicting" ? "text-negative" : s === "neutral" ? "text-ink-3" : "text-ink-2";

  return (
    <div className="space-y-6">
      <Link to="/cs-radar" className="text-[11px] font-semibold uppercase tracking-[0.1em] text-primary">
        ← Close System Radar
      </Link>

      <div className="border-b border-rule pb-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-[11px] uppercase tracking-[0.1em] text-ink-3">{a.category}</span>
          <span className="rounded-sm bg-bg-panel px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-[0.08em] text-ink-3">
            Synthetic data
          </span>
        </div>
        <h1 className="mt-2 font-display text-h2 font-bold leading-tight tracking-tight">
          {a.ticker} — {a.name}
        </h1>
        <p className="mt-1 font-mono text-[11px] text-ink-3">
          {a.currency} {a.current_price} · {a.status} · {a.conviction} conviction · {a.recommendation}
        </p>
      </div>

      <div className="flex flex-wrap gap-1 border-b border-rule pb-3" role="tablist" aria-label="Product sections">
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

      {section === "Product Thesis" && (
        <section className="space-y-4">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Eligibility — P1·P2·P3</p>
            <div className="mt-1">
              <Row k="P1 — cannot go to zero" v={a.p1_pass ? "PASS" : "FAIL"} />
              <Row k="P2 — discount pricing" v={a.p2_pass ? "PASS" : "FAIL"} />
              <Row k="P3 — structural demand" v={a.p3_pass ? "PASS" : "FAIL"} />
              {a.p1_rationale && <p className="mt-2 text-xs text-ink-2">{a.p1_rationale}</p>}
            </div>
          </div>
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Why it exists on the radar</p>
            <div className="mt-1">
              <Row k="Discount type" v={a.discount_type} />
              <Row k="Discount depth" v={a.discount_depth} />
              <Row k="Target entry" v={a.target_discount_entry || "Not specified in pipeline artifact"} />
              <Row k="Demand type" v={a.demand_type} />
              <Row k="Status" v={a.status} />
            </div>
          </div>
        </section>
      )}

      {section === "Commodity Fundamentals" && (
        <div className="space-y-4">
          {Object.keys(a.discount_detail).length > 0 ? (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Discount / cost detail</p>
              <div className="mt-1">
                {Object.entries(a.discount_detail).map(([k, v]) => (
                  <Row key={k} k={k.replace(/_/g, " ")} v={String(v)} mono={typeof v !== "string" || v.length < 30} />
                ))}
              </div>
            </div>
          ) : (
            <EmptyState message="No discount/cost detail in this artifact" sub="Cost-curve fields (avg/marginal AISC, price-to-cost) appear per product as the pipeline produces them." />
          )}
          {Object.keys(a.demand_detail).length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Demand breakdown</p>
              <div className="mt-1">
                {Object.entries(a.demand_detail).map(([k, v]) => (
                  <Row key={k} k={k.replace(/_/g, " ")} v={String(v)} mono={typeof v !== "string" || v.length < 30} />
                ))}
              </div>
            </div>
          )}
          {layers.filter(([k]) => k === "L3_cost" || k === "L4_supply_demand").map(([k, layer]) => (
            <div key={k}>
              <p className={`text-[11px] font-bold uppercase tracking-[0.16em] ${signalTone(layer.signal)}`}>
                {LAYER_LABELS[k] ?? k} · {layer.signal}
              </p>
              <p className="mt-0.5 text-xs text-ink-2">{layer.note}</p>
            </div>
          ))}
        </div>
      )}

      {section === "Macro Context" && (
        <div className="space-y-4">
          {layers.filter(([k]) => k === "L1_macro" || k === "L2_policy").map(([k, layer]) => (
            <div key={k}>
              <p className={`text-[11px] font-bold uppercase tracking-[0.16em] ${signalTone(layer.signal)}`}>
                {LAYER_LABELS[k] ?? k} · {layer.signal}
              </p>
              <p className="mt-0.5 text-xs text-ink-2">{layer.note}</p>
            </div>
          ))}
          {layers.filter(([k]) => k === "L1_macro" || k === "L2_policy").length === 0 && (
            <EmptyState message="No macro layer in this artifact" sub="Macro (L1) and policy (L2) layers appear per product as the pipeline produces them." />
          )}
        </div>
      )}

      {section === "Close System Assessment" && (
        <div className="space-y-4">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Synthesis</p>
            <div className="mt-1">
              <Row k="Layers aligned" v={`${a.layers_aligned}/${layers.length}`} />
              <Row k="Layers contradicting" v={String(a.layers_contradicting)} />
              <Row k="Conviction" v={a.conviction} />
              <Row k="Recommendation" v={a.recommendation} mono={false} />
            </div>
            {a.recommendation_rationale && <p className="mt-2 text-xs text-ink-2">{a.recommendation_rationale}</p>}
          </div>
          {a.key_risks.length > 0 && (
            <div>
              <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Key risks</p>
              <ul className="mt-1 space-y-1">
                {a.key_risks.map((r) => (
                  <li key={r} className="border-b border-rule py-1 text-[13px] text-ink-2">— {r}</li>
                ))}
              </ul>
            </div>
          )}
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Q-conditions</p>
            <p className="mt-1 text-xs text-ink-2">
              Q-condition analysis belongs to the Alpha Momentum surface and is not produced for Close System products.
            </p>
          </div>
        </div>
      )}

      {section === "Challenge & Evidence" && (
        <div className="space-y-4">
          <EmptyState
            message="No challenge record attached to this product"
            sub="CRO / Red Team challenge memos (template 08) and evidence records appear here as the org-workflow produces them."
          />
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Options overlay</p>
            <p className="mt-1 text-xs text-ink-2">
              Deferred — no options pipeline exists (template 09 is research-only). Instrument structure, IV/RV, skew, and
              strategy families will appear here when an options surface is authorized.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
