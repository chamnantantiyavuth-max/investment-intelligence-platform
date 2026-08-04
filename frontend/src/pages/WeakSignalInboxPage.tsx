import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Lightbulb, Zap } from "lucide-react"
import SyntheticDataBanner from "@/components/SyntheticDataBanner"

const ANOMALIES = [
  { id: 1, title: "Sector rotation into Utilities", age: "New", desc: "Defensive sector volume 3σ above 20-day average. No credible explanation yet." },
  { id: 2, title: "Small-cap breadth divergence", age: "2d", desc: "Russell 2000 advance/decline line diverging from price. Liquidity signal?" },
  { id: 3, title: "Treasury yield curve steepening", age: "New", desc: "2s10s spread widening rapidly. End-of-cycle or reflation?" },
]

const HYPOTHESES = [
  { id: 1, title: "Grid Modernization Supercycle", status: "Experimental", confidence: 62, evidence: 8, entities: ["GE", "VRT", "ETN", "HUBB"] },
  { id: 2, title: "Nuclear Renaissance for AI Power", status: "Experimental", confidence: 45, evidence: 5, entities: ["CEG", "BWXT", "LEU"] },
  { id: 3, title: "Insurance Hard Market Cycle", status: "Under Review", confidence: 71, evidence: 12, entities: ["BRK.B", "TRV", "CB"] },
  { id: 4, title: "Reshoring Capex Cycle", status: "Experimental", confidence: 55, evidence: 7, entities: ["CAT", "URI", "PWR"] },
]

export default function WeakSignalInboxPage() {
  return (
    <div className="space-y-6">
      <h1 className="font-display text-h2 font-bold tracking-tight">Weak Signal Inbox</h1>

      <SyntheticDataBanner note="Anomalies and hypotheses are static demonstration data — the experimental pipeline (E1–E4) is not yet wired to this page." />

      <Tabs defaultValue="anomalies">
        <TabsList>
          <TabsTrigger value="anomalies">
            <Zap className="mr-1 size-3" />
            Unexplained Anomalies ({ANOMALIES.length})
          </TabsTrigger>
          <TabsTrigger value="hypotheses">
            <Lightbulb className="mr-1 size-3" />
            Theme Hypotheses ({HYPOTHESES.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="anomalies" className="space-y-3 pt-4">
          {ANOMALIES.map((a) => (
            <Card key={a.id}>
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <CardTitle className="text-sm">{a.title}</CardTitle>
                  <Badge variant="outline" className="text-xs">{a.age}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-2">
                <p className="text-sm text-muted-foreground">{a.desc}</p>
                <div className="flex gap-2">
                  <Button variant="outline" size="xs" disabled title="Pending implementation — no backend endpoint">Propose Hypothesis</Button>
                  <Button variant="ghost" size="xs" disabled title="Pending implementation — no backend endpoint">Dismiss</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="hypotheses" className="space-y-3 pt-4">
          {HYPOTHESES.map((h) => (
            <Card key={h.id}>
              <CardHeader className="pb-2">
                <div className="flex items-start justify-between">
                  <CardTitle className="text-sm">{h.title}</CardTitle>
                  <Badge variant="secondary" className="text-xs">{h.status}</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex gap-4 text-xs text-muted-foreground">
                  <span>Confidence: <strong>{h.confidence}%</strong></span>
                  <span>Evidence: <strong>{h.evidence} items</strong></span>
                </div>
                <div className="flex flex-wrap gap-1">
                  {h.entities.map((e) => (
                    <Badge key={e} variant="outline" className="font-mono text-xs">{e}</Badge>
                  ))}
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="xs" disabled title="Pending implementation — no backend endpoint">Request Review</Button>
                  <Button variant="ghost" size="xs" disabled title="Pending implementation — no backend endpoint">Add Evidence</Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>
      </Tabs>
    </div>
  )
}
