import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { getIISignals } from "@/api/iiClient"
import type { IISignalsResponse } from "@/types/ii"

const PAGE_SIZE = 50

function fmtUSD(v: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 1 }).format(v)
}

function fmtPct(v: number): string {
  return `${v.toFixed(2)}%`
}

function convictionColor(c: string): string {
  const map: Record<string, string> = {
    Maximum: "bg-red-100 text-red-700 border-red-200",
    High: "bg-orange-100 text-orange-700 border-orange-200",
    Moderate: "bg-amber-100 text-amber-700 border-amber-200",
    Minimal: "bg-slate-100 text-slate-600 border-slate-200",
  }
  return map[c] ?? "bg-slate-100 text-slate-600 border-slate-200"
}

function actionColor(a: string): string {
  const map: Record<string, string> = {
    INCREASED: "bg-emerald-100 text-emerald-700 border-emerald-200",
    NEW: "bg-emerald-100 text-emerald-700 border-emerald-200",
    REDUCED: "bg-pink-100 text-pink-700 border-pink-200",
    EXITED: "bg-pink-100 text-pink-700 border-pink-200",
  }
  return map[a] ?? "bg-slate-100 text-slate-600 border-slate-200"
}

export default function InstitutionalPage() {
  const [page, setPage] = useState(0)

  const { data, isLoading, isError } = useQuery<IISignalsResponse>({
    queryKey: ["ii-signals", page],
    queryFn: () => getIISignals(PAGE_SIZE, page * PAGE_SIZE),
  })

  const total = data?.total ?? 0
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE))
  const meta = data?.meta ?? {}
  const provenance = data?.provenance

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Institutional Intelligence</h1>
          <p className="text-sm text-muted-foreground">
            {total.toLocaleString()} signals · 13F filings · {String(meta.data_source ?? "n/a")}
          </p>
        </div>
        {provenance && (
          <Badge variant="outline" className="text-xs">
            {provenance.mode === "real" ? `REAL · ${provenance.source} · ${provenance.completeness ?? ""}` : "SYNTHETIC — NOT LIVE DATA"}
          </Badge>
        )}
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader><CardTitle className="text-sm text-muted-foreground">Funds Tracked</CardTitle></CardHeader>
          <CardContent className="text-2xl font-semibold">{String(data?.summary?.total_funds_tracked ?? "—")}</CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm text-muted-foreground">Total Signals</CardTitle></CardHeader>
          <CardContent className="text-2xl font-semibold">{total.toLocaleString()}</CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm text-muted-foreground">As Of</CardTitle></CardHeader>
          <CardContent className="text-2xl font-semibold">{String(meta.as_of ?? "—")}</CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm">13F Signal Detail</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && <div className="py-8 text-center text-sm text-muted-foreground">Loading signals…</div>}
          {isError && <div className="py-8 text-center text-sm text-pink-600">Failed to load institutional signals.</div>}
          {!isLoading && !isError && (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Filer</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Position</TableHead>
                    <TableHead>Quarter</TableHead>
                    <TableHead>Portfolio</TableHead>
                    <TableHead>Conviction</TableHead>
                    <TableHead>Action</TableHead>
                    <TableHead>Δ</TableHead>
                    <TableHead>Score</TableHead>
                    <TableHead className="text-right">Value</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {(data?.signals ?? []).map((s, i) => (
                    <TableRow key={`${s.filer_cik}-${s.ticker}-${i}`}>
                      <TableCell className="font-medium">{s.filer_name}</TableCell>
                      <TableCell><Badge variant="outline" className="text-xs">{s.filer_category}</Badge></TableCell>
                      <TableCell className="font-mono text-xs">{s.ticker}</TableCell>
                      <TableCell className="text-xs">{s.filing_quarter}</TableCell>
                      <TableCell>{fmtPct(s.pct_of_portfolio)}</TableCell>
                      <TableCell><Badge className={convictionColor(s.conviction)}>{s.conviction}</Badge></TableCell>
                      <TableCell><Badge className={actionColor(s.action)}>{s.action}</Badge></TableCell>
                      <TableCell className={s.change_pct > 0 ? "text-emerald-600" : s.change_pct < 0 ? "text-pink-600" : "text-muted-foreground"}>
                        {s.change_pct === 0 ? "—" : `${s.change_pct > 0 ? "+" : ""}${s.change_pct.toFixed(1)}%`}
                      </TableCell>
                      <TableCell>{s.signal_score}</TableCell>
                      <TableCell className="text-right">{fmtUSD(s.value_usd)}</TableCell>
                    </TableRow>
                  ))}
                  {data?.signals?.length === 0 && (
                    <TableRow><TableCell colSpan={10} className="py-8 text-center text-sm text-muted-foreground">No signals in this range.</TableCell></TableRow>
                  )}
                </TableBody>
              </Table>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs text-muted-foreground">
                  Page {page + 1} of {pages} · {total.toLocaleString()} signals
                </span>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" disabled={page === 0} onClick={() => setPage((p) => Math.max(0, p - 1))}>
                    Previous
                  </Button>
                  <Button variant="outline" size="sm" disabled={page >= pages - 1} onClick={() => setPage((p) => p + 1)}>
                    Next
                  </Button>
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
