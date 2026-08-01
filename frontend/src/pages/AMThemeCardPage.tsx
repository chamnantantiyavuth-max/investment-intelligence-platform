import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { EvidenceIndicator } from "@/components/EvidenceIndicator"
import { ConfidenceGauge } from "@/components/ConfidenceGauge"
import { ArrowLeft } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMTheme } from "@/api/amClient"
import SyntheticDataBanner from "@/components/SyntheticDataBanner"

export default function AMThemeCardPage() {
  const { id } = useParams<{ id: string }>();
  const { data: theme, isLoading, error, refetch } = useQuery({
    queryKey: ["am-theme", id],
    queryFn: () => getAMTheme(id!),
    enabled: !!id,
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error) {
    const is404 = String(error).includes("NOT_FOUND");
    return (
      <div className="space-y-6">
        <Button variant="ghost" size="icon-sm" render={<Link to="/am-queue" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <Card className={is404 ? "border-amber-200 bg-amber-50" : "border-rose-200 bg-rose-50"}>
          <CardContent className="p-8 text-center">
            <p className={is404 ? "text-amber-700 font-medium" : "text-rose-700 font-medium"}>
              {is404 ? `Theme '${id}' not found.` : "Failed to load theme."}
            </p>
            {!is404 && (
              <button onClick={() => refetch()} className="mt-2 text-sm text-rose-600 underline">Retry</button>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }
  if (!theme) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon-sm" render={<Link to="/am-queue" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{theme.name}</h1>
          <div className="mt-1 flex items-center gap-2">
            <ThemeStatusBadge
              approvalStatus={theme.approval_status as "detected" | "experimental" | "under_review" | "approved" | "rejected"}
              lifecycle={theme.lifecycle as "weak_signal" | "formation" | "emerging" | "expansion" | "crowded" | "deterioration" | undefined}
            />
            <Badge variant="outline" className="text-xs">{theme.data_source}</Badge>
          </div>
        </div>
      </div>

      {theme.data_source === "synthetic_demo" && (
        <SyntheticDataBanner note="Theme Card summary comes from the AM API, which currently serves demonstration data — narrative, drivers, candidates, and Human Control workflow are not yet wired to this API surface." />
      )}

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="candidates">Candidates</TabsTrigger>
          <TabsTrigger value="evidence">Evidence</TabsTrigger>
          <TabsTrigger value="review">HC Review</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4 pt-4">
          <Card>
            <CardHeader><CardTitle className="text-sm">Theme Narrative</CardTitle></CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">Pending implementation — narrative is not yet available from the API.</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-sm">Key Drivers</CardTitle></CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{theme.driver_count} drivers registered — detail list pending implementation.</p>
            </CardContent>
          </Card>

          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Theme Quality</span>
                <span className="text-2xl font-bold">{theme.theme_quality}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Candidate Q.</span>
                <span className="text-2xl font-bold">{theme.candidate_quality}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Entry Readiness</span>
                <span className="text-2xl font-bold">{theme.entry_readiness}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Data Confidence</span>
                <ConfidenceGauge value={theme.data_confidence * 20} />
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="candidates" className="pt-4">
          <Card>
            <CardContent className="p-6">
              <p className="text-sm text-muted-foreground">
                {theme.candidate_count} candidates registered — candidate detail list pending implementation.
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evidence" className="space-y-4 pt-4">
          <EvidenceIndicator
            supporting={theme.evidence_supporting}
            contradicting={theme.evidence_contradicting}
            missing={theme.evidence_missing}
            className="max-w-md"
          />
          <Separator />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Card><CardHeader><CardTitle className="text-sm">Supporting</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-[#10b981]">{theme.evidence_supporting}</p></CardContent></Card>
            <Card><CardHeader><CardTitle className="text-sm">Contradicting</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-[#ec4899]">{theme.evidence_contradicting}</p></CardContent></Card>
            <Card><CardHeader><CardTitle className="text-sm">Missing</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-slate-400">{theme.evidence_missing}</p></CardContent></Card>
          </div>
        </TabsContent>

        <TabsContent value="review" className="pt-4">
          <Card>
            <CardHeader><CardTitle className="text-sm">Human Control Review</CardTitle></CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">7 HC decision slots — pending implementation.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
