import { useQuery } from "@tanstack/react-query";
import { getFOQueue } from "@/api/foClient";
import type { ResearchPackageSummary } from "@/types/fo";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Shield } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "@/lib/utils";

function moatColor(width: string) {
  return { Wide: "bg-emerald-100 text-emerald-700", Narrow: "bg-amber-100 text-amber-700", None: "bg-rose-100 text-rose-700" }[width] || "";
}

function qualityColor(rating: string) {
  return { HIGH: "bg-emerald-100 text-emerald-700", MEDIUM: "bg-amber-100 text-amber-700", LOW: "bg-rose-100 text-rose-700", COSMETIC: "bg-rose-200 text-rose-800 line-through" }[rating] || "";
}

function convictionColor(level: string) {
  return { Maximum: "bg-emerald-100 text-emerald-700", High: "bg-emerald-50 text-emerald-600", Moderate: "bg-amber-100 text-amber-700", Low: "bg-rose-100 text-rose-700" }[level] || "";
}

function trapColor(verdict: string) {
  return {
    NOT_A_TRAP: "bg-emerald-100 text-emerald-700",
    MIXED: "bg-amber-100 text-amber-700",
    SUSPECT: "bg-rose-100 text-rose-700",
    TRAP: "bg-rose-200 text-rose-800",
    DEFINITE_TRAP: "bg-rose-200 text-rose-800 font-bold",
    "Not flagged": "bg-slate-100 text-slate-500",
  }[verdict] || "bg-slate-100 text-slate-500";
}

function FOSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-64" />
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full" />
      ))}
    </div>
  );
}

export default function FundamentalQueuePage() {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-queue"],
    queryFn: getFOQueue,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <FOSkeleton />;
  if (error) return (
    <Card className="border-rose-200 bg-rose-50">
      <CardContent className="p-6 text-center">
        <p className="text-rose-700 font-medium">Failed to load Fundamental Queue</p>
        <button onClick={() => refetch()} className="mt-2 text-sm text-rose-600 underline">Retry</button>
      </CardContent>
    </Card>
  );
  if (!data?.length) return (
    <Card>
      <CardContent className="p-12 text-center text-muted-foreground">
        <Shield className="size-12 mx-auto mb-3 opacity-30" />
        <p className="font-medium">No companies in Fundamental Queue</p>
        <p className="text-sm">Run the pipeline to generate Research Packages.</p>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Fundamental Queue</h1>
          <p className="text-sm text-muted-foreground">
            {data.length} companies · Fundamental & Opportunity Intelligence V1
          </p>
        </div>
        <Badge variant="outline" className="text-xs">
          {data[0]?.provenance.mode === "real" ? `REAL · ${data[0].provenance.source}` : "SYNTHETIC — NOT LIVE DATA"}
        </Badge>
      </div>

      <Card>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Company</TableHead>
              <TableHead>Moat</TableHead>
              <TableHead>Earnings</TableHead>
              <TableHead>Conviction</TableHead>
              <TableHead>Value Trap</TableHead>
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
                  <div className="flex items-center gap-1.5">
                    <Badge variant="secondary" className={cn("text-xs font-medium", moatColor(pkg.moat_width))}>
                      {pkg.moat_width}
                    </Badge>
                    <span className="text-xs text-muted-foreground">{pkg.moat_depth}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="secondary" className={cn("text-xs font-medium", qualityColor(pkg.earnings_quality))}>
                    {pkg.earnings_quality}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge variant="secondary" className={cn("text-xs font-medium", convictionColor(pkg.conviction))}>
                    {pkg.conviction}
                  </Badge>
                </TableCell>
                <TableCell>
                  <Badge variant="secondary" className={cn("text-xs font-medium", trapColor(pkg.value_trap_verdict))}>
                    {pkg.value_trap_verdict}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </div>
  );
}
