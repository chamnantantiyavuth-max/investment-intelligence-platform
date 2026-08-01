import { MetricCard } from "@/components/MetricCard"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArrowRight, TrendingUp, Shield, Building2 } from "lucide-react"
import { Link } from "react-router-dom"
import SyntheticDataBanner from "@/components/SyntheticDataBanner"

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Strategy Control Center</h1>

      <SyntheticDataBanner note="Dashboard metrics are static demonstration values — no live pipeline is connected to this surface yet." />

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <MetricCard label="Total Themes" value={143} trend="up" trendLabel="12 this week" />
        <MetricCard label="Approved" value={12} trend="up" trendLabel="+3 this month" />
        <MetricCard label="Active Signals" value={7} trend="up" trendLabel="2 new" />
        <MetricCard label="Queue Size" value={5} trend="flat" trendLabel="no change" />
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
                <p className="text-2xl font-bold">12</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Queue</span>
                <p className="text-2xl font-bold">5</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">Last run: 2 hours ago</p>
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
                <p className="text-2xl font-bold">8</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Q-Met</span>
                <p className="text-2xl font-bold">3</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">Regime: Risk-On · Structural Decay: Low</p>
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
                <p className="text-2xl font-bold">8</p>
              </div>
              <div>
                <span className="text-xs uppercase text-muted-foreground">Wide Moat</span>
                <p className="text-2xl font-bold">5</p>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">Cheap & Quality: 1 · Value Traps: 2</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
