import { useEffect, useState } from "react"
import { MetricCard } from "@/components/MetricCard"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowRight, TrendingUp, Shield, Building2, Landmark } from "lucide-react"
import { Link } from "react-router-dom"
import { getDashboardSummary, type DashboardSummary } from "@/api/dashboardClient"

function provenanceLabel(p: { data_source: string | null; state: string }) {
  if (p.state === "unavailable") return "Unavailable — no admitted artifact"
  return p.data_source ?? "unknown"
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    getDashboardSummary().then(setData).catch(() => setError(true))
  }, [])

  if (error) return <p className="text-sm text-pink-600">Dashboard unavailable — API error</p>
  if (!data) return <p className="text-sm text-slate-500">Loading dashboard…</p>

  const am = data.components.am
  const fo = data.components.fo
  const ii = data.components.ii
  const cs = data.components.cs

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Strategy Control Center</h1>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <MetricCard label="Total Themes" value={data.total_themes} trend="flat" />
        <MetricCard label="Approved" value={data.approved_themes} trend="flat" />
        <MetricCard label="Active Signals" value={data.active_signals} trend="flat" />
        <MetricCard label="Queue Size" value={data.queue_size} trend="flat" />
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp className="size-5 text-[#10b981]" />
              <CardTitle className="text-base">Alpha Momentum</CardTitle>
            </div>
            <Button variant="ghost" size="xs" render={<Link to="/am-queue" />}>
              View <ArrowRight className="ml-1 size-3" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-xs uppercase text-muted-foreground">Active Themes</span>
                <p className="text-2xl font-bold">{data.total_themes}</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Queue</span>
                <p className="text-2xl font-bold">{data.queue_size}</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">Last run: {data.am_last_run ?? "—"}</p>
            <p className="text-xs text-slate-500">Data: {provenanceLabel(am)}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="size-5 text-[#ec4899]" />
              <CardTitle className="text-base">Close System</CardTitle>
            </div>
            <Button variant="ghost" size="xs" render={<Link to="/cs-radar" />}>
              View <ArrowRight className="ml-1 size-3" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-xs uppercase text-muted-foreground">Radar Items</span>
                <p className="text-2xl font-bold">{data.cs_radar_items}</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Q-Met</span>
                <p className="text-2xl font-bold">{data.cs_qc_met}</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">Regime: {data.cs_regime}</p>
            <p className="text-xs text-slate-500">Data: {provenanceLabel(cs)}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2">
              <Building2 className="size-5 text-[#8b5cf6]" />
              <CardTitle className="text-base">Fundamental & Opportunity</CardTitle>
            </div>
            <Button variant="ghost" size="xs" render={<Link to="/fundamental" />}>
              View <ArrowRight className="ml-1 size-3" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-xs uppercase text-muted-foreground">Companies</span>
                <p className="text-2xl font-bold">{fo.state === "available" ? "—" : "—"}</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Status</span>
                <p className="text-2xl font-bold">{fo.state === "available" ? "✓" : "∅"}</p>
              </div>
            </div>
            <p className="text-xs text-slate-500">Data: {provenanceLabel(fo)}</p>
            {ii.state === "available" && (
              <p className="flex items-center gap-1 text-xs text-slate-500">
                <Landmark className="size-3" /> II: {provenanceLabel(ii)}
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
