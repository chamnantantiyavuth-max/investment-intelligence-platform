# AAPL — Primary Source Inventory (RM-2026-0001 evidence build)

**Mandate:** RM-2026-0001 — Apple moat durability across six qualitative dimensions
**Lead:** Equity Alpha Analyst (research cell: Macro / Quant / Data / CRO / Red Team)
**Evidence build started:** 2026-08-06
**Rule:** every material figure date-stamped + sourced; FD #58 point-in-time rule applies (reference books valid only at publication — primary filings are the backbone)

## Filings (SEC EDGAR, verified 2026-08-06 via submissions API)

| Filing | Period end | Filed | Accession | Primary doc | Use |
|---|---|---|---|---|---|
| 10-K FY2025 | 2025-09-27 | 2025-10-31 | 0000320193-25-000079 | aapl-20250927.htm | Business (Item 1), Risk Factors (1A), MD&A (7), Financials (8), Segment Note 13 |
| 10-Q Q3 FY2026 | 2026-06-27 | 2026-07-31 | 0000320193-26-000020 | aapl-20260627.htm | Legal proceedings detail, new risk factors, buyback programs (EXTRACTED + reconciled) |
| 10-Q Q2 FY2026 | 2026-03-28 | 2026-05-01 | 0000320193-26-000013 | aapl-20260328.htm | Interim trend |
| 10-Q Q1 FY2026 | 2025-12-27 | 2026-01-30 | 0000320193-26-000006 | aapl-20251227.htm | Interim trend |
| 8-K Q3 FY26 earnings | 2026-07-30 | 2026-07-30 | 0000320193-26-000018 | a8-kex991q3202606272026.htm (ex99.1) | Latest earnings release + guidance |
| 8-K Q4 FY25 earnings | 2025-10-30 | 2025-10-30 | 0000320193-25-000077 | aapl-20251030.htm (+ex99.1) | FY25 release |
| DEF 14A | FY2026 | 2026-01-08 | 0001308179-26-000008 | aapl014016-def14a.htm | Governance/comp — optional lens |

## Structured data

- XBRL Company Facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json` (annual income statement, balance sheet, cash flow, share counts, buybacks; FY ends late September — filter fp=FY, end=YYYY-09-2x)
- Market data: yfinance fallback via Yahoo chart API (skill §6)

## Working files (outside repo — system temp)

- `/tmp/apl-evidence/` — submissions.json, aapl-10k-fy2025.txt (converted), aapl-8k-q3fy26-ex991.txt (converted), aapl-10q-q3fy26.txt (converted, 96KB), aapl-xbrl-facts.json (3.8MB), 8k-index.json, 10q-q3fy26-index.json
- Repo carries only: this inventory + evidence-log.md (working log with accession refs); the published Evidence & Quant Appendix lives in reports/ at publication

## Evidence log

- 2026-08-06: source inventory built from submissions API (CIK 0000320193)
- 2026-08-06: 10-K FY2025 downloaded + converted; product-mix table + geographic segments + net income/share counts extracted → `evidence-log.md` (accession 0000320193-25-000079)
- 2026-08-06: **evidence build COMPLETE** — Note 13 segment op income (3 years), gross margin detail (Products/Services), Services narrative (Item 1 + MD&A), Item 1A risk factors, Q3 FY2026 8-K (ex99.1, accession 0000320193-26-000018), XBRL FY21–25 annual series (rev/GM/NI/OCF/capex/buybacks/shares)
- 2026-08-06: **Q3 FY2026 10-Q extracted + reconciled** (accession 0000320193-26-000020, filed 2026-07-31) — legal proceedings detail (€500M DMA fine, DOJ suit, Epic injunctions, Google licensing), new risk factors (NAND/DRAM, AI compute, Siri AI interoperability), buyback programs (new $100B April 2026 + $10B ASRs), shares outstanding 14.594B as of 2026-07-17
<!-- 2026-08-06 16:34 UTC+7 -->
