import { useQuery } from "@tanstack/react-query"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { EvidenceIndicator } from "@/components/EvidenceIndicator"
import { ConfidenceGauge } from "@/components/ConfidenceGauge"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMQueue } from "@/api/amClient"
import SyntheticDataBanner from "@/components/SyntheticDataBanner"

export default function AMQueuePage() {
  const { data: themes, isLoading, error, refetch } = useQuery({
    queryKey: ["am-queue"],
    queryFn: getAMQueue,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) return <Skeleton className="h-96 w-full" />;
  if (error) return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Alpha Momentum Queue</h1>
      <Card className="border-rose-200 bg-rose-50">
        <CardContent className="p-6 text-center">
          <p className="text-rose-700 font-medium">Failed to load Alpha Momentum Queue</p>
          <button onClick={() => refetch()} className="mt-2 text-sm text-rose-600 underline">Retry</button>
        </CardContent>
      </Card>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Alpha Momentum Queue</h1>
      </div>

      <SyntheticDataBanner note="Theme rankings come from the AM API, which currently serves demonstration data — the real AM pipeline is not yet connected to this API surface." />

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Theme Rankings</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[280px]">Theme</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Evidence</TableHead>
                <TableHead className="text-center">Theme Q.</TableHead>
                <TableHead className="text-center">Candidate Q.</TableHead>
                <TableHead className="text-center">Data Conf.</TableHead>
                <TableHead className="w-[60px]" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {themes?.map((t) => (
                <TableRow key={t.id}>
                  <TableCell className="font-medium">{t.name}</TableCell>
                  <TableCell>
                    <ThemeStatusBadge
                      approvalStatus={t.approval_status as "detected" | "experimental" | "under_review" | "approved" | "rejected"}
                      lifecycle={t.lifecycle as "weak_signal" | "formation" | "emerging" | "expansion" | "crowded" | "deterioration" | undefined}
                    />
                  </TableCell>
                  <TableCell>
                    <EvidenceIndicator
                      supporting={t.evidence_supporting}
                      contradicting={t.evidence_contradicting}
                      missing={t.evidence_missing}
                      className="w-32"
                    />
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{t.theme_quality}</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{t.candidate_quality}</span>
                  </TableCell>
                  <TableCell>
                    <ConfidenceGauge value={t.data_confidence * 20} size="sm" />
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon-sm" render={<Link to={`/am-theme/${t.id}`} />}>
                      <ArrowRight className="size-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
