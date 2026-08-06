# AAPL — Primary Source Inventory (RM-2026-0001 evidence build)

**Mandate:** RM-2026-0001 — Apple moat durability across six qualitative dimensions
**Lead:** Equity Alpha Analyst (research cell: Macro / Quant / Data / CRO / Red Team)
**Evidence build started:** 2026-08-06
**Rule:** every material figure date-stamped + sourced; FD #58 point-in-time rule applies (reference books valid only at publication — primary filings are the backbone)

## Filings (SEC EDGAR, verified 2026-08-06 via submissions API)

| Filing | Period end | Filed | Accession | Primary doc | Use |
|---|---|---|---|---|---|
| 10-K FY2025 | 2025-09-27 | 2025-10-31 | 0000320193-25-000079 | aapl-20250927.htm | Business (Item 1), Risk Factors (1A), MD&A (7), Financials (8), Segment Note 18 |
| 10-Q Q3 FY2026 | 2026-06-27 | 2026-07-31 | 0000320193-26-000020 | aapl-20260627.htm | Latest quarter — services momentum, segment check |
| 10-Q Q2 FY2026 | 2026-03-28 | 2026-05-01 | 0000320193-26-000013 | aapl-20260328.htm | Interim trend |
| 10-Q Q1 FY2026 | 2025-12-27 | 2026-01-30 | 0000320193-26-000006 | aapl-20251227.htm | Interim trend |
| 8-K Q3 FY26 earnings | 2026-07-30 | 2026-07-30 | 0000320193-26-000018 | aapl-20260730.htm (+ex99.1) | Latest earnings release + guidance |
| 8-K Q4 FY25 earnings | 2025-10-30 | 2025-10-30 | 0000320193-25-000077 | aapl-20251030.htm (+ex99.1) | FY25 release |
| DEF 14A | FY2026 | 2026-01-08 | 0001308179-26-000008 | aapl014016-def14a.htm | Governance/comp — optional lens |

## Structured data

- XBRL Company Facts: `https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json` (annual income statement, balance sheet, cash flow, share counts, buybacks; FY ends late September — filter fp=FY, end=YYYY-09-2x)
- Market data: yfinance fallback via Yahoo chart API (skill §6)

## Working files (outside repo — system temp)

- `/tmp/apl-evidence/` — submissions.json, 10-K text slices (S01-business, S03-mda, segments, S04-financials), XBRL extraction
- Repo carries only: this inventory + the Evidence & Quant Appendix (with accession refs) at publication

## Evidence log

- 2026-08-06: source inventory built from submissions API (CIK 0000320193)
- 2026-08-06: 10-K FY2025 downloaded + converted (237KB text); product-mix table + geographic segments + net income/share counts extracted → `evidence-log.md` (accession 0000320193-25-000079)
<!-- 2026-08-06 20:50 UTC+7 -->
