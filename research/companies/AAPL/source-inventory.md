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
| 10-Q Q2 FY2026 | 2026-03-28 | 2026-05-01 | 0000320193-26-000013 | aapl-20260328.htm | Interim trend (EXTRACTED 2026-08-07 — see evidence-log §6d) |
| 10-Q Q1 FY2026 | 2025-12-27 | 2026-01-30 | 0000320193-26-000006 | aapl-20251227.htm | Interim trend (EXTRACTED 2026-08-07 — see evidence-log §6c) |
| 8-K Q3 FY26 earnings | 2026-07-30 | 2026-07-30 | 0000320193-26-000018 | a8-kex991q3202606272026.htm (ex99.1) | Latest earnings release + guidance |
| 8-K Q4 FY25 earnings | 2025-10-30 | 2025-10-30 | 0000320193-25-000077 | aapl-20251030.htm (+ex99.1) | FY25 release |
| DEF 14A | FY2026 | 2026-01-08 | 0001308179-26-000008 | aapl014016-def14a.htm | Governance/comp — optional lens (not yet extracted) |

## Earnings-call transcripts (third-party; NOT SEC filings — cross-check to 8-K/10-Q before quoting)

| Call | Date | Source | Key content |
|---|---|---|---|
| Q1 FY2026 | 2026-01-29 | AlphaStreet transcript | Record quarter $143.8B; installed base 2.5B+ devices; GC +38% |
| Q2 FY2026 | 2026-04-30 | AlphaStreet transcript | **CEO succession announced (Cook → Ternus, eff. ~Sept 2026; Cook → Exec Chairman)**; $111.2B +17% |
| Q3 FY2026 | 2026-07-30 | AlphaStreet transcript | **Cook's final call**; Sept guidance +9–11%; Services GM 75.6%; paid subs 1.5B+; memory "hundred-year flood"; Broadcom $30B+ |

## Third-party market-share data (NOT filings — cite source + date)

| Source | Publication | Coverage | Apple |
|---|---|---|---|
| IDC | 2026-06-23 | Q1 2026 final | 61.8M units / 21.0% share (+4.4% YoY) — #2, statistical tie with Samsung 21.2% |
| IDC | 2025-12-02 | FY2025 forecast | ~247.4M units (+6.1%) — record year |
| IDC | 2026-06-23 | FY2026 forecast | iOS −5.2% vs Android −20%; iOS share ~22% (highest ever) |
| Counterpoint | 2026-04-10 | Q1 2026 preliminary | Apple #1 — 21% share (+5% YoY); Samsung 20% (−6%) |

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
- 2026-08-07: **evidence upgrade (Apple evidence upgrade task)** — Q1 FY2026 10-Q extracted (accession 0000320193-26-000006, filed 2026-01-30 → evidence-log §6c: $143.8B rev +15.7%, iPhone 85,269 +23.3%, GC +37.9%, buybacks 93M sh/$25B); Q2 FY2026 10-Q extracted (accession 0000320193-26-000013, filed 2026-05-01 → evidence-log §6d: $111.2B rev +16.6%, iPhone +21.7%, GC +28.1%, 6-mo buybacks 135M sh/$36B, Services GM derived 76.68%); **earnings-call transcripts Q1/Q2/Q3 FY2026 pulled** (AlphaStreet — evidence-log §6e: **CEO succession Cook→Ternus eff. ~Sept 2026 announced 30 Apr 2026 + Cook's final call 30 Jul 2026; installed base 2.5B+ devices; paid subs 1.5B+; Sept guidance +9–11% rev / GM 47–48% / memory 'hundred-year flood'; Broadcom $30B+ agreement**); **market share pulled** (IDC Q1 2026 final + FY2025/FY2026 forecasts; Counterpoint Q1 2026 — evidence-log §10: Apple 61.8M/21.0% IDC (+4.4%), Apple #1 per Counterpoint 21%; tracker disagreement documented); DEF 14A still not extracted (optional). Working files: `/tmp/apl-upgrade/` (q1fy26-10q.txt, q2fy26-10q.txt, idc-share.html, idc-fy25.html, cp-q1-2026.html, transcript snapshots).
<!-- 2026-08-06 16:34 UTC+7 · 2026-08-07 12:15 UTC+7 (evidence upgrade log entry) -->
