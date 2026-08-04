import { useQuery } from "@tanstack/react-query";
import { getCSRadar, type CSAsset } from "@/api/csClient";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { QConditionGrid } from "@/components/QConditionGrid";
import { ConfidenceGauge } from "@/components/ConfidenceGauge";
import { Skeleton } from "@/components/ui/skeleton";
import SyntheticDataBanner from "@/components/SyntheticDataBanner";

// Audit SOL-003/BROWSER-003 fix: page now consumes the CS API (single source of
// truth = backend /api/cs-radar mock). The hardcoded frontend asset array was
// removed because it disagreed with the API (dashboard=8 / API=2 / UI=3).

export default function CSRadarPage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cs-radar"],
    queryFn: getCSRadar,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-64 w-full" />;
  if (error) return (
    <div className="rounded-md bg-bg-panel px-5 py-6 text-center">
      <p className="text-sm font-medium text-negative">Failed to load.</p>
      <button onClick={() => refetch()} className="mt-1 text-sm text-primary underline">Retry</button>
    </div>
  );

  const assets: CSAsset[] = data?.assets ?? [];
  // Lead judgment = display ordering from ADMITTED fields only (max opportunity, tie → suitability).
  // Presentation ordering, never an investment rule (same doctrine as AM rankCandidates).
  const lead = [...assets].sort(
    (a, b) => b.dimensions.opportunity - a.dimensions.opportunity || b.dimensions.suitability - a.dimensions.suitability
  )[0];

  return (
    <div className="space-y-6">
      <h1 className="font-display text-h2 font-bold tracking-tight">Close System Radar</h1>

      <SyntheticDataBanner note="Radar assets are static demonstration data — the Close System pipeline is not yet wired to this API surface." />

      {lead && (
        <section className="border-b border-rule pb-6">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Lead judgment · Close System</p>
          <h2 className="mt-2 max-w-3xl font-display text-hero font-bold leading-[1.12] text-foreground">
            Most interesting product to watch: {lead.ticker} — {lead.name}
          </h2>
          <p className="mt-2 font-mono text-lg font-semibold text-positive">
            opportunity {lead.dimensions.opportunity} · suitability {lead.dimensions.suitability}
          </p>
          <p className="mt-2 max-w-2xl text-sm text-ink-2">
            Regime {lead.dimensions.regime} · Q-conditions {lead.q_conditions_met}/{lead.q_conditions_total}. Derived
            from admitted Q-condition/dimension fields — display ordering, not an investment rule.
          </p>
        </section>
      )}

      {/* Council F3: P1–P3 / 5-layer / conviction / risks exist in the CS pipeline artifact but are
          NOT admitted by this synthetic API surface (FD #46) — honest unavailable states, no invented fields. */}
      <section className="rounded-md bg-bg-panel px-4 py-3">
        <h2 className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-3">Eligibility · Synthesis · Conviction</h2>
        <div className="mt-2 grid gap-x-8 gap-y-1 text-[13px] sm:grid-cols-2">
          {[
            ["P1–P3 eligibility", "Unavailable on this surface"],
            ["5-layer synthesis", "Unavailable on this surface"],
            ["Conviction (Low–Maximum)", "Unavailable on this surface"],
            ["Key risks", "Unavailable on this surface"],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between border-b border-rule py-1.5">
              <span className="text-ink-2">{k}</span>
              <span className="font-mono text-[11px] text-ink-3">{v}</span>
            </div>
          ))}
        </div>
        <p className="mt-2 text-[11px] text-ink-2">
          These fields exist in the CS pipeline artifact (pipeline_result.json: p1_pass/p2_pass/p3_pass, layers,
          conviction, key_risks) but this synthetic API surface does not admit them yet — wiring requires a separate
          FD (FD #46 boundary). Not invented here.
        </p>
      </section>

      <section className="mt-6">
        <h2 className="font-display text-finding font-bold text-foreground">Product Radar — Q-Conditions Screening</h2>
        <div className="mt-2 overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[120px]">Ticker</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Q-Conditions</TableHead>
                <TableHead className="text-center">Suitability</TableHead>
                <TableHead className="text-center">Opportunity</TableHead>
                <TableHead>Regime</TableHead>
                <TableHead>Confidence</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {assets.map((a) => (
                <TableRow key={a.ticker}>
                  <TableCell className="font-mono font-bold">{a.ticker}</TableCell>
                  <TableCell>
                    {a.name}
                    <div className="text-xs text-muted-foreground">{a.sector}</div>
                  </TableCell>
                  <TableCell>
                    <QConditionGrid conditions={a.q_details} />
                    <span className="text-xs text-muted-foreground">{a.q_conditions_met}/{a.q_conditions_total} met</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{a.dimensions.suitability}</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{a.dimensions.opportunity}</span>
                  </TableCell>
                  <TableCell>
                    <Badge variant={a.dimensions.regime === "compatible" ? "secondary" : "outline"}>
                      {a.dimensions.regime}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <ConfidenceGauge value={a.dimensions.data_confidence * 10} size="sm" />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </section>
    </div>
  );
}
