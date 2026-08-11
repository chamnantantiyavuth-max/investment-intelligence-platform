# Data Steward — Independent View (LLY)

**Date:** 2026-08-11 · **Mandate:** RM-2026-0007

## 1. Data lineage

| Data | Source | Pulled | Status |
|---|---|---|---|
| Q2 FY26 revenue/EPS/guidance | 8-K Ex-99.1 (0000059478-26-000077) | 2026-08-11 | VERIFIED — primary source |
| Cash flow, capex, buyback, debt | 10-Q (0000059478-26-000081) | 2026-08-11 | VERIFIED — OCF $16,023M, capex $5,259M, IPR&D $3,486M, dividends $3,094M, $15B buyback program, LT debt $8B+ |
| Annual rev/NI | companyfacts XBRL | 2026-08-11 | VERIFIED — FY2025 $65.2B / $20.6B |
| Scanner record | universe-scan-2026-08-11.json | 2026-08-11 | VERIFIED with reconciliation (+80.5% scanner vs +48% release — release wins) |

## 2. Point-in-time

- All Q2 figures period-end 2026-06-30, filed 2026-08-05 (FD #58)
- FY2025 annual from XBRL (filed FY2025 10-K)

## 3. Gaps

- Earnings-call transcript not pulled (capacity timeline, competitive commentary would deepen)
- Buyback actual execution vs $15B authorization: authorization ≠ executed — 10-Q financing section shows dividends but the buyback ACTUAL dollar figure needs the equity section (flag: report must say "program authorized/active", not "buyback executed $X")

**Core view:** clean lineage; one precision flag — don't claim executed buyback dollars without the equity-statement figure.
<!-- 2026-08-11 18:38 UTC+7 -->
