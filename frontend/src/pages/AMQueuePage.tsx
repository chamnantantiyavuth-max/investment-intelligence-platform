import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ThemeStatusBadge } from "@/components/ThemeStatusBadge"
import { EvidenceIndicator } from "@/components/EvidenceIndicator"
import { ConfidenceGauge } from "@/components/ConfidenceGauge"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import { Link } from "react-router-dom"

const MOCK_THEMES = [
  {
    id: "theme-ai-infra", name: "AI Infrastructure", approval: "approved" as const, lifecycle: "formation" as const,
    drivers: 3, candidates: 4, evidence: { supporting: 23, contradicting: 4, missing: 2 },
    scores: { theme: 4.2, candidate: 4.0, entry: 3.1, data: 4.3 },
  },
  {
    id: "theme-glp1", name: "GLP-1 Weight Loss", approval: "approved" as const, lifecycle: "expansion" as const,
    drivers: 5, candidates: 6, evidence: { supporting: 31, contradicting: 3, missing: 1 },
    scores: { theme: 4.5, candidate: 4.1, entry: 3.8, data: 4.6 },
  },
  {
    id: "theme-semicon", name: "Semiconductor Cycle", approval: "approved" as const, lifecycle: "expansion" as const,
    drivers: 4, candidates: 7, evidence: { supporting: 28, contradicting: 5, missing: 3 },
    scores: { theme: 4.0, candidate: 4.3, entry: 3.5, data: 4.1 },
  },
  {
    id: "theme-defense", name: "Defense Spending", approval: "experimental" as const, lifecycle: "formation" as const,
    drivers: 2, candidates: 3, evidence: { supporting: 12, contradicting: 6, missing: 4 },
    scores: { theme: 3.5, candidate: 3.2, entry: 2.5, data: 3.8 },
  },
  {
    id: "theme-grid", name: "Grid Modernization", approval: "experimental" as const, lifecycle: "weak_signal" as const,
    drivers: 3, candidates: 5, evidence: { supporting: 8, contradicting: 2, missing: 7 },
    scores: { theme: 3.0, candidate: 3.5, entry: 2.0, data: 2.8 },
  },
]

export default function AMQueuePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Alpha Momentum Queue</h1>
      </div>

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
              {MOCK_THEMES.map((t) => (
                <TableRow key={t.id}>
                  <TableCell className="font-medium">{t.name}</TableCell>
                  <TableCell>
                    <ThemeStatusBadge approvalStatus={t.approval} lifecycle={t.lifecycle} />
                  </TableCell>
                  <TableCell>
                    <EvidenceIndicator {...t.evidence} className="w-32" />
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{t.scores.theme}</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{t.scores.candidate}</span>
                  </TableCell>
                  <TableCell>
                    <ConfidenceGauge value={t.scores.data * 20} size="sm" />
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
