# Equity Inflection Shadow Scan — Report 2026-08-10 (FO-universe, 8 names)

> Phase 0 shadow run per `docs/PLAN-EQUITY-INFLECTION-SHADOW-SCANNER-v0.1.md` (T7).
> Shadow mode: NO Task Idea Cards, NO CoS triage, NO research capacity consumed (FD #88).
> Data: SEC EDGAR companyfacts (PIT, filed-date stamps) + yfinance prices (split-adjusted).
> Run: 2026-08-10 · artifact `discovery/equity_inflection/output/shadow-2026-08-10.json`

## Result

| Ticker | H1 (TTM level) | H2 (YoY rate) | Revenue | Stage | Verdict |
|---|---|---|---|---|---|
| **AAPL** | ✅ 8.71 > 8.26 | ❌ | ✅ | S2-early | **CANDIDATE** |
| AMZN | ✅ 12.43 > 8.36 | ✅ | ✅ | UNCLASSIFIED | — (stage) |
| GOOGL | ✅ 19.91 > 13.11 | ✅ | ✅ | UNCLASSIFIED | — (stage) |
| MSFT | ✅ 17.95 > 16.80 | ❌ | ✅ | UNCLASSIFIED | — (stage) |
| NVDA | ✅ 6.53 > 4.90 | ❌ | ✅ | UNCLASSIFIED | — (stage) |
| JNJ | ❌ 8.61 < 15.15 | ❌ | ✅ | S2-early | — (H1) |
| META | ❌ 27.50 < 27.56 | ❌ | ✅ | S4 | — (H1+stage) |
| TSLA | ❌ 1.08 < 3.69 | ❌ | ✅ | S4 | — (H1+stage) |

## Interpretation (honest, per plan §8)

1. **AAPL = the only candidate** — latest TTM EPS ($8.71) breaks above the prior
   2-year max ($8.26); revenue confirmed; price in S2-early (above both MAs, recent
   cross, small extension). This matches the Founder's core hypothesis: an earnings
   breakout out of its frame with price not yet run far. **Note:** AAPL is a large-cap
   already well-covered by the org — the scanner surfaced it correctly but its
   *incremental* research value is low (consistent with FD #75's concern about
   low-incremental-value names in an ATH market).

2. **Hypothesis separation demonstrated on real data:** AMZN/GOOGL fire BOTH H1+H2;
   AAPL/MSFT/NVDA fire H1 only; none fire H2 only in this small set. The two
   hypotheses behave differently — combination decision correctly deferred (FD #88).

3. **Stage filter did its job:** 4 names (AMZN/GOOGL/MSFT/NVDA) passed the earnings
   signal but are UNCLASSIFIED — price above both MAs but 50MA slope negative
   (post-pullback) or 150MA rolling over (MSFT). These are exactly the
   "price already ran / structure unclear" cases the Founder wants kept OUT of the
   watch list. META/TSLA are confirmed S4 (excluded).

4. **Data-layer findings (real, fixed in this run):**
   - yfinance quarterly history = 5 quarters only → switched primary EPS source to
     SEC EDGAR companyfacts (PIT filed-date stamps).
   - companyfacts carries YTD-cumulative + pure-quarter values for the same
     period_end → dedup by shortest duration.
   - Fiscal-Q4 not reported as pure quarter → derived as annual − 3 quarters,
     labelled `derived: true` (AAPL Q4 FY25 = $1.84).
   - NVDA 10:1 split (Jun 2024) handled via DilutedAverageShares ratio (pre-split
     EPS scaled to current basis, `split_factor` recorded).

## Capacity load (plan §J Phase 5 estimate)

8 names → 1 candidate (12.5%). Extrapolating the illustrative funnel: a ~300-name
liquid universe at this hit rate would produce ~35–40 candidates/cycle → ~10–15
genuinely interesting → ~4–8 recon-worthy → 1–3 deep-research mandates. Consistent
with the direction's illustrative funnel (5,000 → 40–60 → 10–15 → 4–8 → 1–3).
Thresholds remain PROPOSED (FD #53) — no production use without Founder approval.

## What was NOT done (scope lock)

- No Task Idea Cards filed, no CoS triage, no radar contract change.
- No threshold promoted to production; no cron; no blog/UI/schema change.
- No standing behavior — this is a shadow artifact for Founder review.

## Next options for the Founder

(a) Accept shadow result → proceed to validation Phase 1 (PIT historical validation
    plan — separate plan, includes look-ahead/survivorship/revision-leakage tests).
(b) Expand universe (~100–300 liquid names) for a broader shadow pass first.
(c) Adjust signal/stage definitions (e.g., UNCLASSIFIED disposition, H2 handling).
(d) Stop — keep as a reference artifact only.

<!-- 2026-08-10 12:45 UTC+7 -->
