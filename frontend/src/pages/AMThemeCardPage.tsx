import { Link } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { EvidenceIndicator } from "@/components/EvidenceIndicator"
import { ConfidenceGauge } from "@/components/ConfidenceGauge"
import { ArrowLeft } from "lucide-react"

const MOCK = {
  id: "theme-ai-infra",
  name: "AI Infrastructure",
  approval: "approved" as const,
  lifecycle: "formation" as const,
  monitoring: "Active Monitoring",
  narrative: "The build-out of AI infrastructure — data centers, GPUs, networking, and power — represents a multi-year capital cycle. Demand is driven by hyperscaler capex, enterprise AI adoption, and sovereign AI initiatives.",
  drivers: ["GPU supply constraints", "Cloud capex expansion", "LLM inference scaling", "Power infrastructure bottleneck"],
  candidates: [
    { ticker: "NVDA", role: "Confirmed Leader", score: 87 },
    { ticker: "AMD", role: "Emerging Challenger", score: 72 },
    { ticker: "SMCI", role: "Direct Beneficiary", score: 65 },
    { ticker: "ANET", role: "Enabler", score: 58 },
  ],
  evidence: { supporting: 23, contradicting: 4, missing: 2 },
  scores: { theme: 4.2, candidate: 4.0, entry: 3.1, data: 4.3 },
}

export default function AMThemeCardPage() {

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon-sm" render={<Link to="/am-queue" />}>
          <ArrowLeft className="size-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{MOCK.name}</h1>
          <div className="mt-1 flex items-center gap-2">
            <ThemeStatusBadge approvalStatus={MOCK.approval} lifecycle={MOCK.lifecycle} />
            <Badge variant="outline" className="text-xs">{MOCK.monitoring}</Badge>
          </div>
        </div>
      </div>

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
            <CardContent><p className="text-sm text-muted-foreground">{MOCK.narrative}</p></CardContent>
          </Card>

          <Card>
            <CardHeader><CardTitle className="text-sm">Key Drivers</CardTitle></CardHeader>
            <CardContent>
              <ul className="list-disc space-y-1 pl-5 text-sm">
                {MOCK.drivers.map((d, i) => <li key={i}>{d}</li>)}
              </ul>
            </CardContent>
          </Card>

          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Theme Quality</span>
                <span className="text-2xl font-bold">{MOCK.scores.theme}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Candidate Q.</span>
                <span className="text-2xl font-bold">{MOCK.scores.candidate}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Entry Readiness</span>
                <span className="text-2xl font-bold">{MOCK.scores.entry}</span>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="flex flex-col items-center gap-1 p-4 pt-4">
                <span className="text-[11px] uppercase text-muted-foreground">Data Confidence</span>
                <ConfidenceGauge value={MOCK.scores.data * 20} />
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
                    <TableHead>Role</TableHead>
                    <TableHead className="text-right">Score</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {MOCK.candidates.map((c) => (
                    <TableRow key={c.ticker}>
                      <TableCell className="font-mono font-bold">{c.ticker}</TableCell>
                      <TableCell>{c.role}</TableCell>
                      <TableCell className="text-right font-semibold">{c.score}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evidence" className="space-y-4 pt-4">
          <EvidenceIndicator {...MOCK.evidence} className="max-w-md" />
          <Separator />
          <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <Card><CardHeader><CardTitle className="text-sm">Supporting</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-[#10b981]">{MOCK.evidence.supporting}</p></CardContent></Card>
            <Card><CardHeader><CardTitle className="text-sm">Contradicting</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-[#ec4899]">{MOCK.evidence.contradicting}</p></CardContent></Card>
            <Card><CardHeader><CardTitle className="text-sm">Missing</CardTitle></CardHeader><CardContent><p className="text-3xl font-bold text-slate-400">{MOCK.evidence.missing}</p></CardContent></Card>
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
