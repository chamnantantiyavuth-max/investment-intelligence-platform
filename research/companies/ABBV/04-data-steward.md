# Data Steward — Independent View (ABBV)

**Date:** 2026-08-11 · **Mandate:** RM-2026-0005
**Scope:** data provenance, point-in-time compliance (FD #58), gap honesty

## 1. Data lineage (all verified this session)

| Data | Source | Pulled | Status |
|---|---|---|---|
| Q2 FY26 EPS/revenue/segments | 8-K Ex-99.1 (0001551152-26-000023) | 2026-08-11 | VERIFIED — primary source |
| H1 cash flow, contingent consideration, IPR&D | 10-Q (0001551152-26-000026) | 2026-08-11 | VERIFIED — primary source |
| Annual rev/NI series | SEC companyfacts XBRL (CIK 0001551152) | 2026-08-11 | VERIFIED — raw XBRL, fiscal-year filtered (duration 320–400d, instant tags date-aligned to 31-Dec year-ends) |
| Scanner H1 record | universe-scan-2026-08-11.json | 2026-08-11 | VERIFIED — output of FD #89 instrument |
| FY2025 10-K full text | NOT pulled | — | GAP — annual figures from XBRL only (reliable for totals; segment detail from E1) |
| Apogee deal terms | NOT in filings yet | — | GAP — announced 7/31, S-4/8-K/A pending; guidance dilution −$0.14 is the only quantified figure |
| Aug 2026 debt offering proceeds | 424B5/FWP headers | 2026-08-11 | PARTIAL — amounts/coupons not extracted this pass (E4/E5) |

## 2. Point-in-time discipline

- All Q2 figures stamped 2026-06-30 period-end / 2026-07-31+ filed (FD #58).
- Annual series fiscal-year ends 31-Dec: FY2023 $54.3B / FY2024 $56.3B / FY2025 $61.2B rev — **corrected mid-session** (an earlier evidence-log draft mislabeled FY2025 revenue as $58.1B; Verify-First caught it against the raw XBRL year-end list; corrected before any downstream use).
- Scanner as-of: EPS series filed-date-stamped; price 8/10 close.

## 3. Adjusted EPS — provenance caveat

Adjusted diluted EPS ($3.65) is **company-defined** (management non-GAAP). The add-back schedule is in the earnings release; I did not independently re-derive every adjustment this pass (gaps listed). The report must label adjusted figures as management-defined, never present them as GAAP.

## 4. Data sufficiency verdict

Sufficient for a bounded deep-research note (inflection quality + stage discipline). Would deepen with: FY25 10-K full text, earnings-call transcript (growth drivers, Apogee rationale), and the debt offering term sheet. **No figure in this workspace is un-sourced or invented.**

**Core view:** data is clean and PIT-compliant; the two named gaps (Apogee terms, debt deal amounts) must be flagged in the report, not silently omitted.
<!-- 2026-08-11 16:28 UTC+7 -->
