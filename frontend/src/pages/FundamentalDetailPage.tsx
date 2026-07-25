import { useQuery } from "@tanstack/react-query";
import { useParams, Link } from "react-router-dom";
import { getFOPackage } from "@/api/foClient";
import { ResearchPackageDetail, MoatType } from "@/types/fo";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { ArrowLeft } from "lucide-react";
import { cn } from "@/lib/utils";

function moatColor(width: string) { return { Wide: "text-emerald-600", Narrow: "text-amber-600", None: "text-rose-600" }[width] || ""; }
function depthColor(d: string) { return { Deep: "text-emerald-600", Moderate: "text-amber-600", Shallow: "text-rose-600" }[d] || ""; }
function trendColor(t: string) { return { Widening: "text-emerald-600", Stable: "text-blue-600", Narrowing: "text-rose-600" }[t] || ""; }
function qualityColor(r: string) { return { HIGH: "bg-emerald-100 text-emerald-700", MEDIUM: "bg-amber-100 text-amber-700", LOW: "bg-rose-100 text-rose-700", COSMETIC: "bg-rose-200 text-rose-800 line-through" }[r] || ""; }

export default function FundamentalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: pkg, isLoading, error, refetch } = useQuery({
    queryKey: ["fo-package", id],
    queryFn: () => getFOPackage(id!),
    enabled: !!id,
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error) return (
    <Card className="border-rose-200 bg-rose-50"><CardContent className="p-6 text-center text-rose-700">Failed to load package. <button onClick={() => refetch()} className="underline">Retry</button></CardContent></Card>
  );
  if (!pkg) return <Card><CardContent className="p-12 text-center text-muted-foreground">Company not found.</CardContent></Card>;

  const moat = pkg.company_assessment?.moat as Record<string, unknown> | undefined;
  const fin = pkg.company_assessment?.financial_quality as Record<string, unknown> | undefined;
  const mgmt = pkg.company_assessment?.management as Record<string, unknown> | undefined;
  const eq = pkg.earnings_trajectory;
  const val = pkg.valuation_context as Record<string, unknown>;
  const vt = val?.value_trap as Record<string, unknown> | undefined;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Link to="/fundamental" className="text-muted-foreground hover:text-foreground"><ArrowLeft className="size-5" /></Link>
        <div>
          <h1 className="text-2xl font-bold">{pkg.name} <span className="text-muted-foreground text-base font-normal">({pkg.id})</span></h1>
          <p className="text-sm text-muted-foreground">{pkg.sector} · {pkg.industry} · Thesis: {pkg.thesis_lifecycle}</p>
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="moat">🏰 Moat</TabsTrigger>
          <TabsTrigger value="earnings">📊 Earnings</TabsTrigger>
          <TabsTrigger value="valuation">💰 Valuation</TabsTrigger>
          <TabsTrigger value="analysis">⚔️ Analysis</TabsTrigger>
        </TabsList>

        {/* Overview */}
        <TabsContent value="overview" className="space-y-4">
          <Card><CardHeader><CardTitle className="text-base">Thesis Summary</CardTitle></CardHeader><CardContent><p className="text-sm">{pkg.thesis_summary}</p></CardContent></Card>
          <div className="grid grid-cols-2 gap-4">
            <Card>
              <CardContent className="p-4 text-center">
                <span className="text-xs text-muted-foreground uppercase">Conviction</span>
                <p className="text-2xl font-bold">{pkg.conviction}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <span className="text-xs text-muted-foreground uppercase">Thesis Lifecycle</span>
                <p className="text-2xl font-bold">{pkg.thesis_lifecycle}</p>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Moat */}
        <TabsContent value="moat" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="grid grid-cols-4 gap-4 text-center mb-6">
                <div><span className="text-xs text-muted-foreground uppercase block">Width</span><span className={cn("text-2xl font-bold", moatColor(moat?.width as string || ""))}>{moat?.width}</span></div>
                <div><span className="text-xs text-muted-foreground uppercase block">Depth</span><span className={cn("text-2xl font-bold", depthColor(moat?.depth as string || ""))}>{moat?.depth}</span></div>
                <div><span className="text-xs text-muted-foreground uppercase block">Trend</span><span className={cn("text-2xl font-bold", trendColor(moat?.trend as string || ""))}>{moat?.trend}</span></div>
                <div><span className="text-xs text-muted-foreground uppercase block">Score</span><span className="text-2xl font-bold">{moat?.moat_score as number}/100</span></div>
              </div>
              <Separator className="my-4" />
              <p className="text-sm mb-4">{moat?.moat_narrative as string}</p>
              <div className="flex flex-wrap gap-2">
                {((moat?.types as MoatType[]) || []).map((t, i) => (
                  <Badge key={i} variant="secondary" className={cn("text-xs font-medium", t.strength === "Strong" ? "bg-emerald-100 text-emerald-700" : t.strength === "Moderate" ? "bg-amber-100 text-amber-700" : "bg-rose-100 text-rose-700")}>
                    {t.type} ({t.strength})
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Earnings */}
        <TabsContent value="earnings" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <Badge className={cn("text-sm font-bold px-3 py-1", qualityColor(eq?.rating || ""))}>{eq?.rating}</Badge>
                <span className="text-sm text-muted-foreground">{eq?.conviction_impact}</span>
              </div>
              <p className="text-sm mb-4">{eq?.narrative}</p>
              <div className="grid grid-cols-3 gap-3 text-xs">
                <div><span className="text-muted-foreground">Surprise:</span> <span className="font-semibold">{eq?.surprise_direction} ({eq?.surprise_magnitude_pct?.toFixed(1)}%)</span></div>
                <div><span className="text-muted-foreground">Revenue Quality:</span> <span className="font-semibold">{eq?.revenue_quality}</span></div>
                <div><span className="text-muted-foreground">Margin Quality:</span> <span className="font-semibold">{eq?.margin_quality}</span></div>
                <div><span className="text-muted-foreground">FCF Conversion:</span> <span className="font-semibold">{eq?.fcf_conversion?.toFixed(2)}x</span></div>
                <div><span className="text-muted-foreground">One-Time Items:</span> <span className="font-semibold">{eq?.one_time_items ? "Yes" : "No"}</span></div>
                <div><span className="text-muted-foreground">Guidance:</span> <span className="font-semibold">{eq?.guidance_direction}</span></div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Valuation */}
        <TabsContent value="valuation" className="space-y-4">
          <Card>
            <CardContent className="p-6">
              <div className="grid grid-cols-2 gap-4 text-sm mb-6">
                <div><span className="text-muted-foreground">P/E (TTM):</span> <span className="font-semibold">{(val?.pe_ttm as number)?.toFixed(1)}x</span></div>
                <div><span className="text-muted-foreground">P/E (5Y avg):</span> <span className="font-semibold">{(val?.pe_5y_avg as number)?.toFixed(1)}x</span></div>
                <div><span className="text-muted-foreground">EV/EBITDA:</span> <span className="font-semibold">{(val?.ev_ebitda as number)?.toFixed(1)}x</span></div>
                <div><span className="text-muted-foreground">FCF Yield:</span> <span className="font-semibold">{((val?.fcf_yield as number || 0) * 100).toFixed(1)}%</span></div>
              </div>
              {vt && vt.triggered && (
                <div className="border border-rose-200 bg-rose-50 rounded-lg p-4">
                  <h4 className="font-bold text-rose-700 mb-2">⚠️ Value Trap Detector</h4>
                  <p className="text-sm font-semibold text-rose-700 mb-2">Score: {vt.score as number}/5 — {vt.verdict as string}</p>
                  <p className="text-xs text-rose-600">{vt.action as string}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Analysis */}
        <TabsContent value="analysis" className="space-y-4">
          <Card>
            <CardHeader><CardTitle className="text-base text-rose-600">⚔️ Independent Challenge</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {pkg.independent_challenge.map((ch, i) => <li key={i} className="text-sm text-rose-700">• {ch}</li>)}
              </ul>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-base text-amber-600">⚠️ Key Risks</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {pkg.key_risks.map((r, i) => <li key={i} className="text-sm text-amber-700">• {r}</li>)}
              </ul>
            </CardContent>
          </Card>
          <div className="grid grid-cols-2 gap-4">
            <Card>
              <CardHeader><CardTitle className="text-base text-emerald-600">✅ Supporting Evidence</CardTitle></CardHeader>
              <CardContent>{pkg.supporting_evidence.map((e, i) => <p key={i} className="text-xs text-muted-foreground mb-1">{e}</p>)}</CardContent>
            </Card>
            <Card>
              <CardHeader><CardTitle className="text-base text-rose-600">❌ Contradicting</CardTitle></CardHeader>
              <CardContent>{pkg.contradicting_evidence.map((e, i) => <p key={i} className="text-xs text-muted-foreground mb-1">{e}</p>)}</CardContent>
            </Card>
          </div>
          <Card>
            <CardHeader><CardTitle className="text-base">❓ Open Questions</CardTitle></CardHeader>
            <CardContent>
              <ul className="space-y-2">{pkg.open_questions.map((q, i) => <li key={i} className="text-sm text-muted-foreground">• {q}</li>)}</ul>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
