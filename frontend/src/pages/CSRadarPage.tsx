import { useQuery } from "@tanstack/react-query";
import { getCSRadar, type CSAsset } from "@/api/csClient";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
    <Card className="border-rose-200 bg-rose-50">
      <CardContent className="p-6 text-center text-rose-700">Failed to load. <button onClick={() => refetch()} className="underline">Retry</button></CardContent>
    </Card>
  );

  const assets: CSAsset[] = data?.assets ?? [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Close System Radar</h1>

      <SyntheticDataBanner note="Radar assets are static demonstration data — the Close System pipeline is not yet wired to this API surface." />

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Product Radar — Q-Conditions Screening</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 p-0">
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
        </CardContent>
      </Card>
    </div>
  );
}
