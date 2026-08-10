# Plan — Equity Inflection Validation Phase 1: PIT Historical Validation (Shadow)

> Version: v0.1 · 10 Aug 2026 · Critical Mode (financial signal validation, shadow-gated)
> Basis: FD #88 (item 104) validation gate + `docs/PLAN-EQUITY-INFLECTION-SHADOW-SCANNER-v0.1.md` §9(a) + direction §18J
> Input: shadow scanner v0.1 (commit `341da7e`) — H1/H2 EPS breakout + revenue confirmation + Stage Def v0.1
> Status: **DRAFT — awaiting Founder approval (T0 gate). No implementation until approved.**

---

## 1. Goal

Prove the Equity Inflection signals are **point-in-time honest** and behave sensibly on
historical data — WITHOUT consuming research capacity (shadow-gated, FD #88). Output:
a validation evidence pack the Founder reviews before ANY threshold hardening or
standing behavior. Primary metric = **research-discovery quality**, NOT forward returns
(direction §18J — return analysis is secondary and must not become a trading backtest).

## 2. Authority and Constraints

| Source | Rule |
|---|---|
| FD #88 (item 104) | Scanner shadow-gated until Founder approves validation evidence; no production threshold without separate named FD |
| Direction §18J | PIT historical validation; look-ahead/survivorship/revision-leakage tests; hypothesis separation; false-positive + missed-opportunity review; capacity load; stability/sensitivity; honest empty-output |
| FD #53 | No invented thresholds — every perturbation/band in this plan is a MEASUREMENT, never an approval |
| FD #58 | Point-in-time discipline mandatory; availability = filing date |
| FD #65 | Frozen pipelines untouched — this runs inside `discovery/equity_inflection/` only |
| Constitution | Portfolio-blind §23.8.1; no broker/allocation; deterministic/AI separation §23.3 |

## 3. Material vs Non-Material

| Item | Classification | Reason |
|---|---|---|
| `discovery/equity_inflection/validation.py` (new) | Material (financial validation logic) | FD #88 validation gate authorizes shadow validation; no production behavior |
| fetcher extension (full companyfacts history + 10y prices) | Material (data-layer) | Same gate |
| `tests/test_equity_inflection_validation.py` (new) | Material | New test surface; suite must stay 332+ green |
| Validation run + evidence pack | Non-material | No cards, no CoS, no research capacity |
| Any threshold value | **NOT approved by this plan** | FD #53 — evidence only |

## 4. Method (PIT as-of reconstruction)

**Core idea — companyfacts IS a revision history.** Verified 2026-08-10: 68/74 AAPL
period_ends carry multiple entries with different `filed` dates (e.g. FY2008 EPS
restated 5.36 → 6.78 in the FY2010 10-K). For each as-of date T:

```
as-of view at T = for every quarter, take the value whose filed date is the
                  LATEST filed <= T  (the most recent knowledge at T)
                + only include quarters REPORTED by T (filed <= T)
TTM(T)   = sum of the 4 most recent quarter values as-known-at-T
H1(T)    = TTM(T) > max TTM of prior 8 quarters (as-of T)
H2(T)    = latest YoY growth (as-of T) > max prior 8 YoY (as-of T)
Revenue  = latest quarter revenue (as-of T) >= year-ago (as-of T)
Stage(T) = Stage Def v0.1 on price history ≤ T only (MAs are trailing → naturally PIT)
Splits   = EPS adjusted via DilutedAverageShares ratios as-known-at-T;
           prices = yfinance split-adjusted close (both sides PIT)
```

**Historical windows:** quarter-end as-of dates 2021-06-30 → 2026-06-30 (~21 dates)
× FO-universe 8 names. Each as-of date yields a full candidate-set snapshot.

## 5. File-by-File Plan

| File | Action | Details |
|---|---|---|
| `discovery/equity_inflection/fetcher.py` | EDIT | `fetch_full_companyfacts(cik)` — return ALL entries (every filed-date revision), not just latest; `fetch_ticker` gains `period="10y"` for prices; existing shadow behavior unchanged |
| `discovery/equity_inflection/validation.py` | NEW | `asof_series(entries, T)` (PIT view), `historical_run(tickers, asof_dates)` (H1/H2/revenue/stage per date), `bias_tests()` (look-ahead invariant + revision-leakage quantification), `stability_perturbations()` (threshold bands), `false_positive_review()`, `capacity_load()`. Pure logic — testable without network |
| `tests/test_equity_inflection_validation.py` | NEW | Locked-style invariants: (a) look-ahead — a value filed AFTER T never appears in asof view at T; (b) revision-leakage — synthetic restatement (5.36→6.78) flips as-of views only AFTER the restatement filed date; (c) signal flip rate = |as-of signal − final-value signal|; (d) stage uses only prices ≤ T |
| `discovery/equity_inflection/output/validation-2026-08-10/` | NEW | Evidence pack: per-date candidate tables, bias-test results, stability matrix, false-positive character, missed-opportunity review, capacity-load summary + VALIDATION-REPORT.md |

## 6. Assumptions and Deferred

| ID | Assumption | Risk |
|---|---|---|
| A1 | companyfacts revision entries cover material restatements for the FO-8 | Minor revisions may be absent (filed-date dedup) — documented in the report |
| A2 | FO-universe = live 8 names, all survivors | **Survivorship bias inherent** — delisting coverage needs a PIT universe source (CRSP-style, paid) → DEFERRED (D1); report labels this honestly; no claim of survivor-free validation |
| A3 | yfinance 10y close is split-adjusted and adequate for stage history | Verified 2,514 rows AAPL 2016–2026; corporate-action edge cases documented |
| A4 | Filed date = public availability date | SEC filed timestamps are the availability proxy (earnings calls often precede by hours — immaterial for quarterly granularity) |
| D1 | Delisted-name universe for survivorship testing | DEFERRED — no free PIT delisting source; mitigation: FO-8 + qualitative note |
| D2 | Guidance / estimate-revision signals | DEFERRED (unchanged from shadow plan) |
| D3 | Any production threshold | DEFERRED — this plan produces evidence only |

## 7. Approval Requested (T0 Gate)

| Step | What | Material |
|---|---|---|
| T0 | **Approve this plan** (method + file scope + shadow-only + threshold-evidence-only status) | Yes — stops here until Founder approval |
| T1 | fetcher: full companyfacts history + 10y prices | Material |
| T2 | validation.py: asof_series + historical_run | Material |
| T3 | bias tests (look-ahead + revision-leakage) | Material |
| T4 | stability perturbations (bands: extension ±5pp, slope ±0.2%/mo, range ±10pp, window 6/8/10q) | Material |
| T5 | false-positive character + missed-opportunity review + capacity load | Non-material |
| T6 | Validation run (21 as-of dates × 8 names) | Non-material |
| T7 | Verification (suite 332+ green, ad-hoc) + evidence pack + commit | Non-material |

**Explicit non-authorization (mirroring FD #88):** this plan does NOT authorize (a) any
threshold becoming a production gate, (b) standing scanning, (c) Task Idea Cards / CoS
intake from validation output, (d) cron/automation, (e) radar/blog/UI/schema changes,
(f) forward-return trading analysis as the acceptance metric. Each requires a separate
named Founder Decision.

## 8. Verification Plan

| Feature | Verification |
|---|---|
| Look-ahead invariant | Test: value filed > T never present in asof view at T; ad-hoc: injected future restatement absent |
| Revision-leakage | Test: synthetic restatement flips as-of only after its filed date; signal flip rate computed from real data (as-of vs final) |
| Survivorship honesty | Report explicitly labels FO-8 as survivor-biased; no survivor-free claim |
| Split/corporate actions | EPS split-adjusted via as-known-at-T share ratios; prices split-adjusted; internal consistency check (no >3x adjusted-EPS jumps unexplained) |
| Stability | Perturbation matrix with candidate-set Jaccard similarity per band |
| Capacity load | Candidates per as-of date → avg/cycle vs direction illustrative funnel (5,000→40–60→10–15→4–8→1–3) |
| No regression | `python -m pytest -q` full suite = 332+ baseline intact |
| Scope lock | `git status` shows ONLY planned files; frozen dirs untouched |

## 9. Next After This Phase

Founder reviews the validation evidence pack → decide: (a) approve specific thresholds
for standing behavior (new named FD), (b) adjust signal/stage definitions, (c) expand
universe, (d) stop. Standing production behavior requires a further named FD (FD #88).

<!-- 2026-08-10 13:00 UTC+7 -->
