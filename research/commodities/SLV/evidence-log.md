# SLV Challenge Memo — Evidence Log (ORG-2026-0006)

**Question:** Has the silver deficit shifted from a demand-growth problem to an inventory-and-liquidity problem, given actual and forecast industrial-demand contraction?
**Card:** ORG-2026-0006 (RADAR-001) · **Workspace:** research/commodities/SLV/
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance.

## Source register

| # | Figure | Source | Date | Status |
|---|---|---|---|---|
| S1 | 2025 deficit 40.3Moz — 5th consecutive; total demand −2%; industrial demand −3% | World Silver Survey 2026 (Silver Institute / Metals Focus) | Apr 2026 | VERIFIED (radar pull, deleg_c98d7277) |
| S2 | 2026F: industrial demand −3%; mine production 844.1Moz (−0.3%); 6th deficit 46.3Moz | World Silver Survey 2026 | Apr 2026 | VERIFIED (radar pull) |
| S3 | Primary-mine AISC fell 1% to $12.21/oz (2025) | World Silver Survey 2026 | Apr 2026 | VERIFIED (radar pull) |
| S4 | Oct-2025 liquidity squeeze subsequently EASED as metal returned to London | World Silver Survey 2026 | Apr 2026 | VERIFIED (radar pull) |
| S5 | Gold LBMA PM $4,206.60/oz; +24.6% YoY | LBMA gold_pm.json | 2026-08-05 | VERIFIED (radar pull) |
| S6 | Fed broad dollar index −1.7% YoY | FRED DTWEXBGS | 2026-07-31 | VERIFIED (radar pull) |
| S7 | Note claim: gold/silver ratio ~88:1 vs ~65:1 median ("silver cheap") | reports/silver-product-note-2026-08-06.md (pipeline artifact) | 2026-08-05 | INTERNALLY INCONSISTENT — see F1 |
| S8 | Note claim: silver price "low $20s"; AISC ~$14/oz | reports/silver-product-note-2026-08-06.md (pipeline artifact) | 2026-08-05 | INTERNALLY INCONSISTENT — see F1/F2 |
| S9 | Note claim: solar demand +20% YoY to record (~700K oz/GW) | reports/silver-product-note-2026-08-06.md (pipeline artifact) | 2026-08-05 | CONFLICTS with S1 aggregate (see F3) |
| S10 | Note claim: Shanghai premium ~$2/oz over London; COMEX discounts paper | reports/silver-product-note-2026-08-06.md (pipeline artifact) | 2026-08-05 | NOT RE-VERIFIED this session |

## Material findings to test (draft — for cross-exam + audit)

- **F1 — Ratio/price arithmetic inconsistency (arithmetic, material):** note states ratio ~88:1 AND price "low $20s". With LBMA gold at $4,206.60/oz (S5), 88:1 implies silver ≈ $47.8/oz — NOT low-$20s. Conversely "low $20s" implies ratio ≈ 175–190:1. Both figures cannot be simultaneously true; the note's valuation anchor is wrong or stale and must be re-verified before the "silver cheap" claim stands. (Re-run in audit.)
- **F2 — AISC discrepancy (minor):** note ~$14/oz (S8, pipeline) vs Survey $12.21/oz 2025 (S3). Definition/timing may differ; the note's cost-floor framing ($14) is above the Survey's primary AISC — margin is WIDER than the note stated, weakening the "no supply destruction" floor only if price is near cost (it is not at either figure).
- **F3 — Demand story partially refuted (material):** note frames deficit as demand-rebuild (solar +20%). Survey shows aggregate industrial demand −3% (2025) and −3% (2026F) with total demand −2%. A deficit persisting under CONTRACTING demand is not a demand-growth story — the residual must be inventory/liquidity mechanics, investment absorption (coin/bar), or supply-side. This is the card's core question.
- **F4 — Liquidity event resolved (material for watch items):** note treats physical tightness/premium as leading indicator; Survey says the Oct-2025 squeeze EASED (S4). The "physical premium is the leading indicator" claim needs the post-squeeze state (lease rates, London vaults) — not re-pulled this session.

## Data gaps (named, not estimated)

- Current silver spot fix: LBMA silver JSON 404 + tradingeconomics 403 this session — ratio re-verification pending a working source.
- COMEX / London vault inventory levels; LBMA lease rates; SLV ETF flows — not re-pulled this session.
- Solar-specific demand series (2025 actual vs note's +20%): Survey aggregate only; solar split not re-pulled.

## Sources & limitations

All S1–S6 from radar pass deleg_c98d7277 (browser-verified public sources). S7–S10 quoted verbatim from the published note (the challenge target). Figures are point-in-time; the memo must not present any figure as current beyond its source date.

<!-- 2026-08-06 19:35 UTC+7 -->
