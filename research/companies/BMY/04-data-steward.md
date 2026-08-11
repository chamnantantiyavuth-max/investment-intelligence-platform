# Data Steward — Independent View (BMY)

**Date:** 2026-08-11 · **Mandate:** RM-2026-0006

## 1. Data lineage

| Data | Source | Pulled | Status |
|---|---|---|---|
| Q2 FY26 EPS/revenue/portfolio | 8-K Ex-99.1 (0000014272-26-000018) | 2026-08-11 | VERIFIED — primary source |
| Cash flow/balance | 10-Q (0000014272-26-000020) | 2026-08-11 | DOWNLOADED — cash-flow numbers NOT yet extracted (flag: quant view needs OCF/buyback/debt) |
| Annual rev/NI series | companyfacts XBRL | 2026-08-11 | VERIFIED — FY2024 NI −$8.9B confirmed from raw XBRL (fiscal-year filtered, 31-Dec year-ends) |
| Scanner record | universe-scan-2026-08-11.json | 2026-08-11 | VERIFIED — revenue matches E1 exactly ($12,973M) |

## 2. Point-in-time

- All Q2 figures period-end 2026-06-30, filed 2026-07-30 (FD #58)
- FY2024 loss figure from XBRL (filed FY2025 10-K) — the loss year is historical fact, not estimate

## 3. Gaps

- 10-Q cash flow extraction pending (OCF, buyback, debt) — MUST complete before essay
- Earnings-call transcript not pulled (pipeline commentary, milvexian status would strengthen)
- Non-GAAP add-back schedule in the release — label company-defined

**Core view:** clean primary-source lineage; one MUST-complete gap (cash-flow extraction) before the essay can claim FCF/buyback facts.
<!-- 2026-08-11 17:28 UTC+7 -->
