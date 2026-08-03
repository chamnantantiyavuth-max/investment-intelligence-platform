import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ArrowLeft } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMTheme } from "@/api/amClient"

export default function AMThemeCardPage() {
  const { id } = useParams<{ id: string }>();
  const { data: tc, isLoading, error, refetch } = useQuery({
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
  if (!tc) return null;
  const theme = tc.theme;
  const candidates = tc.candidates ?? [];

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
            <Badge variant="outline" className="text-xs">
              {theme.provenance.hybrid ? "hybrid" : theme.provenance.mode} · {theme.provenance.source}
            </Badge>
          </div>
        </div>
      </div>

      <p className="text-xs text-slate-500">{theme.why_now}</p>

      <Tabs defaultValue="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="candidates">Candidates ({candidates.length})</TabsTrigger>
          <TabsTrigger value="evidence">Evidence ({theme.evidence_provenance.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4 pt-4">
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Confidence</span>
                <span className="text-2xl font-bold">{theme.confidence}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Stocks in Industry</span>
                <span className="text-2xl font-bold">{theme.stocks_in_industry}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Key Tickers</span>
                <span className="text-2xl font-bold">{theme.key_tickers.length}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Data</span>
                <span className="text-lg font-bold">{theme.provenance.hybrid ? "hybrid" : "real"}</span>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="candidates" className="pt-4">
          <Card>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ticker</TableHead>
                    <TableHead>State</TableHead>
                    <TableHead>Conviction</TableHead>
                    <TableHead>Entry Structure</TableHead>
                    <TableHead>Freshness</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {candidates.map((c) => (
                    <TableRow key={c.id}>
                      <TableCell className="font-medium">{c.ticker}</TableCell>
                      <TableCell>{c.research_state}</TableCell>
                      <TableCell>{c.conviction_level}</TableCell>
                      <TableCell>{c.entry_readiness.price_structure}</TableCell>
                      <TableCell className="text-xs text-muted-foreground">{c.data_confidence.freshness}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evidence" className="space-y-4 pt-4">
          <div className="flex flex-wrap gap-2">
            {theme.evidence_provenance.map((e) => (
              <Badge key={e.source_id} variant="outline" className="text-xs">
                {e.source_id} · {e.source_type}
              </Badge>
            ))}
          </div>
          <Separator />
          <p className="text-xs text-slate-500">
            Evidence source labels from the real artifact — synthetic (SRC-SYN) and human-sourced
            entries are marked individually; no blanket label over mixed content.
          </p>
        </TabsContent>
      </Tabs>
    </div>
  )
}
