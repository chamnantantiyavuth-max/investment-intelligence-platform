import { useQuery } from "@tanstack/react-query"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"
import { Skeleton } from "@/components/ui/skeleton"
import { getAMQueue } from "@/api/amClient"

export default function AMQueuePage() {
  const { data, isLoading, error, refetch } = useQuery({
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

  const themes = data?.themes ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Alpha Momentum Queue</h1>
      </div>

      <p className="text-xs text-slate-500">
        Run {data?.run_id} · as of {data?.point_in_time ?? "—"} · {themes.length} themes
        {themes[0]?.theme.provenance.hybrid && " · hybrid data (real EOD + synthetic evidence labeled)"}
      </p>

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
                <TableHead className="text-center">Candidates</TableHead>
                <TableHead className="text-center">Stocks in Industry</TableHead>
                <TableHead className="w-[60px]" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {themes.map(({ theme: t }) => (
                <TableRow key={t.id}>
                  <TableCell className="font-medium">{t.name}</TableCell>
                  <TableCell>
                    <ThemeStatusBadge
                      approvalStatus={t.approval_status as "detected" | "experimental" | "under_review" | "approved" | "rejected"}
                      lifecycle={t.lifecycle as "weak_signal" | "formation" | "emerging" | "expansion" | "crowded" | "deterioration" | undefined}
                    />
                  </TableCell>
                  <TableCell className="text-center font-semibold">{t.key_tickers.length}</TableCell>
                  <TableCell className="text-center">{t.stocks_in_industry}</TableCell>
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
