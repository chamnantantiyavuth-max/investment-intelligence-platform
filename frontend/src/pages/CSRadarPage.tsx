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

  return (
    <div className="space-y-6">
      <h1 className="font-display text-h2 font-bold tracking-tight">Close System Radar</h1>

      <SyntheticDataBanner note="Radar assets are static demonstration data — the Close System pipeline is not yet wired to this API surface." />

      <section className="mt-6">
        <h2 className="font-display text-finding font-bold text-foreground">Product Radar — Q-Conditions Screening</h2>
        <div className="mt-2">
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
