import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { getCSRadar, type CSAsset } from "@/api/csClient";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import SyntheticDataBanner from "@/components/SyntheticDataBanner";

// FD #57: radar serves the v0.1 pipeline artifact (SYNTHETIC). Lead judgment =
// display ordering from admitted fields only (conviction ordinal, then layer
// alignment) — presentation, never an investment rule (AM rankCandidates doctrine).

const CONVICTION_ORDER = ["Low", "Moderate", "High", "Maximum"];

function convictionRank(a: CSAsset): number {
  return CONVICTION_ORDER.indexOf(a.conviction);
}

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
  const lead = [...assets].sort(
    (a, b) => convictionRank(b) - convictionRank(a) || b.layers_aligned - a.layers_aligned
  )[0];

  return (
    <div className="space-y-6">
      <h1 className="font-display text-h2 font-bold tracking-tight">Close System Radar</h1>

      <SyntheticDataBanner note="Radar products are synthetic demo data — labeled, never disguised." />

      {lead && (
        <section className="border-b border-rule pb-6">
          <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-primary">Lead judgment · Close System</p>
          <h2 className="mt-2 max-w-3xl font-display text-hero font-bold leading-[1.12] text-foreground">
            Most interesting product to watch: {lead.ticker} — {lead.name}
          </h2>
          <p className="mt-2 font-mono text-lg font-semibold text-positive">
            {lead.conviction} conviction · {lead.layers_aligned}/5 layers aligned
          </p>
          <p className="mt-2 max-w-2xl text-sm text-ink-2">
            {lead.recommendation}. Derived from admitted pipeline fields — display ordering, not an investment rule.
          </p>
        </section>
      )}

      <section className="mt-6">
        <h2 className="font-display text-finding font-bold text-foreground">Product Radar — Eligibility &amp; Synthesis</h2>
        <div className="mt-2 overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[120px]">Ticker</TableHead>
                <TableHead>Name</TableHead>
                <TableHead className="text-center">P1–P3</TableHead>
                <TableHead className="text-center">Layers</TableHead>
                <TableHead>Conviction</TableHead>
                <TableHead>Recommendation</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {assets.map((a) => (
                <TableRow key={a.id ?? a.ticker}>
                  <TableCell className="font-mono font-bold">
                    <Link to={`/cs-radar/${a.ticker}`} className="text-primary hover:underline">
                      {a.ticker}
                    </Link>
                  </TableCell>
                  <TableCell>
                    {a.name}
                    <div className="text-xs text-muted-foreground">{a.category}</div>
                  </TableCell>
                  <TableCell className="text-center font-mono text-[11px]">
                    {a.p1_pass && a.p2_pass && a.p3_pass ? "P1·P2·P3" : `${a.p1_pass ? "P1" : ""}${a.p2_pass ? "P2" : ""}${a.p3_pass ? "P3" : ""}`}
                  </TableCell>
                  <TableCell className="text-center font-mono text-[11px]">
                    {a.layers_aligned}/{Object.keys(a.layers).length}
                  </TableCell>
                  <TableCell>{a.conviction}</TableCell>
                  <TableCell className="max-w-[220px] whitespace-normal">{a.recommendation}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </section>
    </div>
  );
}
