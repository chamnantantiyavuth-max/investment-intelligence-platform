import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { QConditionGrid } from "@/components/QConditionGrid"
import { ConfidenceGauge } from "@/components/ConfidenceGauge"
import SyntheticDataBanner from "@/components/SyntheticDataBanner"

const ASSETS = [
  {
    ticker: "BRK.B", name: "Berkshire Hathaway", sector: "Financials",
    qMet: 4, qTotal: 5,
    qDetails: [
      { name: "Earnings Stability", met: true, value: "15yr positive" },
      { name: "Earnings Growth", met: true, value: "12% 10yr CAGR" },
      { name: "P/E Moderate", met: true, value: "P/E 14.2" },
      { name: "Debt/Equity Low", met: true, value: "D/E 0.3" },
      { name: "Price/Book", met: false, value: "P/B 1.6x" },
    ],
    suitability: 8.0, opportunity: 5.5, regime: "compatible", confidence: 85,
  },
  {
    ticker: "JNJ", name: "Johnson & Johnson", sector: "Healthcare",
    qMet: 5, qTotal: 5,
    qDetails: [
      { name: "Earnings Stability", met: true, value: "20yr+ positive" },
      { name: "Earnings Growth", met: true, value: "6% 10yr CAGR" },
      { name: "P/E Moderate", met: true, value: "P/E 16.1" },
      { name: "Debt/Equity Low", met: true, value: "D/E 0.5" },
      { name: "Dividend Record", met: true, value: "62yr growth" },
    ],
    suitability: 9.0, opportunity: 7.0, regime: "compatible", confidence: 90,
  },
  {
    ticker: "PG", name: "Procter & Gamble", sector: "Consumer Staples",
    qMet: 4, qTotal: 5,
    qDetails: [
      { name: "Earnings Stability", met: true, value: "Consistent" },
      { name: "Earnings Growth", met: true, value: "5% 10yr" },
      { name: "P/E Moderate", met: false, value: "P/E 25.1" },
      { name: "Debt/Equity Low", met: true, value: "D/E 0.7" },
      { name: "Dividend Record", met: true, value: "68yr" },
    ],
    suitability: 7.5, opportunity: 4.0, regime: "caution", confidence: 75,
  },
]

export default function CSRadarPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">Close System Radar</h1>

      <SyntheticDataBanner note="Radar assets are static demonstration data — the Close System pipeline is not yet wired to this API surface." />

      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-medium">Product Radar — Q-Conditions Screening</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[120px]">Ticker</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Q-Conditions</TableHead>
                <TableHead className="text-center">Suitability</TableHead>
                <TableHead className="text-center">Opportunity</TableHead>
                <TableHead>Regime</TableHead>
                <TableHead>Confidence</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ASSETS.map((a) => (
                <TableRow key={a.ticker}>
                  <TableCell className="font-mono font-bold">{a.ticker}</TableCell>
                  <TableCell>
                    {a.name}
                    <div className="text-xs text-muted-foreground">{a.sector}</div>
                  </TableCell>
                  <TableCell>
                    <QConditionGrid conditions={a.qDetails} />
                    <span className="text-xs text-muted-foreground">{a.qMet}/{a.qTotal} met</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{a.suitability}</span>
                  </TableCell>
                  <TableCell className="text-center">
                    <span className="font-semibold">{a.opportunity}</span>
                  </TableCell>
                  <TableCell>
                    <Badge variant={a.regime === "compatible" ? "secondary" : "outline"}>
                      {a.regime}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <ConfidenceGauge value={a.confidence} size="sm" />
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
