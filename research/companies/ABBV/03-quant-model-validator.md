# Quant Model Validator — Independent View (ABBV)

**Date:** 2026-08-11 · **Mandate:** RM-2026-0005
**Sources:** H1 scanner record (universe-scan-2026-08-11.json), E2 (10-Q cash flows), E3 (companyfacts annual), E1 (adjusted EPS)

## 1. Scanner trigger — arithmetic verification

- TTM diluted EPS $3.54 > prior 2y max $3.00 ✓ (as-of 2026-06-30 EDGAR filed, quarters_used=58).
- Revenue +10.2% YoY ✓ ($16.99B vs $15.42B).
- **Consistency check:** TTM EPS $3.54 with ~1.766B diluted shares → TTM net income ≈ $6.25B. But reported TTM GAAP NI (FY2025 $4.2B + Q1/Q2 FY26 $4.31B − Q1/Q2 FY25 ~$2.2B) ≈ $6.3B ✓ — the scanner's EPS series is consistent with reported net income. No arithmetic defect.
- **BUT:** the prior-2y max ($3.00) was itself depressed (FY2024-FY2025 EPS ~$2.4-2.6 run-rate under charges). Breaking a depressed ceiling is not the same as breaking a normal ceiling. The scanner has no "quality of the base" filter — that's the analyst's job, and it's the key caveat.

## 2. Low-base quantification

- Q2 FY26 GAAP EPS $2.03 vs Q2 FY25 $0.52: **+$1.51/share swing**, of which the IPR&D/charges removal (contingent consideration FV + IPR&D + litigation reserves, H1 total ~$4.9B pre-tax ≈ $2.8/share at 21%+state) explains the bulk.
- Adjusted EPS +22.9% is the growth signal (cleaner, management-defined). Implied Q2 adjusted net income ≈ $6.45B (3.65 × 1.766B) — a credible run-rate (vs $4.31B H1 GAAP — the gap is the charges, as expected).
- **Modeling implication:** do NOT project GAAP EPS from the +290% print. Project from adjusted + guidance: FY26 adjusted EPS guidance $13.87–14.07 (mid $13.97, +~15% vs FY25 adjusted ~$12.1). TTM adjusted run-rate ≈ $3.65×2 + prior halves ≈ $13.5-14 — consistent with guidance. The scanner H1 (GAAP TTM $3.54) is NOT the number to anchor; adjusted TTM ≈ $14 is.

## 3. Cash-flow corroboration

- OCF TTM ≈ $19B; capex ≈ $1.2B → FCF ≈ $17.8B; dividends $11.7B → payout ~66% of FCF, ~85% of adjusted NI — sustainable but leaves little for buyback (matches observed ~$10M/qtr).
- Contingent consideration swings ($3.9B H1 non-cash) make GAAP OCF/NI conversion unstable; adjusted metrics are the modeling basis.

## 4. Stage model sanity (FD #89)

S2-early verified: close $247.97, 50MA $240.71 > 150MA $222.39, slopes +8.3%/+2.4%/mo, extension ~1.1% (recomputed: (247.97−240.71)/240.71 = 3.0% vs scanner's earlier AAPL convention — ABBV extension is small either way). Not extended; no range-position red flag (range_position=0 means within range).

## 5. What the model CANNOT say

- Whether Adjusted EPS growth (22.9%) decelerates in H2 (guidance implies moderation: full-year +15% vs Q2 +22.9%).
- The Apogee accretion math (deal terms not yet in filings).
- Whether the Aug 2026 debt proceeds sit idle (opportunistic) or deploy.

**Core view:** scanner trigger is arithmetically sound but measures a LOW-BASE rebound; the honest modeling anchor is Adjusted EPS ~$14 TTM / guidance ~$13.97, growing ~15% — a good-not-spectacular compounder profile, not a hockey-stick.
<!-- 2026-08-11 16:27 UTC+7 -->
