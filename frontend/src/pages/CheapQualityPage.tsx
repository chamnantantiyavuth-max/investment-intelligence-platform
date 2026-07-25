import { useQuery } from "@tanstack/react-query";
import { getFOCheapQuality } from "@/api/foClient";
import { ResearchPackageSummary } from "@/types/fo";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { DollarSign } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

function moatColor(width: string) { return { Wide: "bg-emerald-100 text-emerald-700", Narrow: "bg-amber-100 text-amber-700", None: "bg-rose-100 text-rose-700" }[width] || ""; }

export default function CheapQualityPage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-cheap-quality"],
    queryFn: getFOCheapQuality,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-64 w-full" />;
  if (error) return (
    <Card className="border-rose-200 bg-rose-50">
      <CardContent className="p-6 text-center text-rose-700">Failed to load. <button onClick={() => refetch()} className="underline">Retry</button></CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Cheap & Quality Watchlist</h1>
        <p className="text-sm text-muted-foreground">
          Companies that are unusually cheap vs own history AND passed Value Trap detection
        </p>
      </div>

      {!data?.length ? (
        <Card>
          <CardContent className="p-12 text-center text-muted-foreground">
            <DollarSign className="size-12 mx-auto mb-3 opacity-30" />
            <p className="font-medium">No companies in Cheap & Quality watchlist</p>
            <p className="text-sm">Unusually cheap companies that pass all 5 Value Trap checks will appear here.</p>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Company</TableHead>
                <TableHead>Moat</TableHead>
                <TableHead>Conviction</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((pkg: ResearchPackageSummary) => (
                <TableRow key={pkg.id} className="cursor-pointer hover:bg-muted/50">
                  <TableCell>
                    <Link to={`/fundamental/${pkg.id}`} className="block">
                      <span className="font-semibold">{pkg.name}</span>
                      <span className="text-muted-foreground ml-2 text-xs">({pkg.id})</span>
                      <div className="text-xs text-muted-foreground">{pkg.sector} · {pkg.industry}</div>
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={cn("text-xs font-medium", moatColor(pkg.moat_width))}>{pkg.moat_width}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className="text-xs font-medium bg-emerald-100 text-emerald-700">{pkg.conviction}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Card>
      )}
    </div>
  );
}
