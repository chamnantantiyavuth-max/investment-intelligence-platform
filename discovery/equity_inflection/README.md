# Equity Inflection Discovery — Deterministic Scanner (FD #88)

**Status:** Shadow phase (Phase 0) — discovery-side, deterministic, portfolio-blind.
**Authorization:** FD #88 (FOUNDERS-DECISIONS item 104, 10 Aug 2026) — research-intake
capability, NOT platform revival. Scanner SHADOW-gated: no standing production behavior
until the Founder approves validation evidence.

## Purpose

Detect companies where underlying earnings power may be changing before/during the
earliest phase of market recognition, then surface the most interesting cases for
disciplined research intake into the existing free-form research organization.

```
BUSINESS INFLECTION + MARKET RECOGNITION → RESEARCH CANDIDATE
→ WHY IS THIS HAPPENING? → CHANGE-DRIVER/CATALYST RECON → FULL COMPANY RESEARCH
```

## Firewall (binding, FD #88)

Scanner output = deterministic evidence block ONLY. It NEVER:
- creates a Task Idea Card, enters CoS triage, or consumes research capacity
- auto-loads into independent research first passes (FD #64 item 7)
- publishes to the blog, or becomes a thesis/conclusion

Radar Scout (role 11) remains the ONLY packaging path (future standing behavior —
NOT in this phase). CoS triage is the only entry into research capacity.

## Module layout

```
discovery/equity_inflection/
├── scanner.py   # PURE deterministic logic — no yfinance/numpy at import
│                # (runs under any Python; unit-tested under the pytest venv 3.11)
├── fetcher.py   # data layer — SEC EDGAR companyfacts (PIT) + yfinance prices
│                # RUNS UNDER SYSTEM PYTHON 3.14 (venv 3.11 lacks yfinance/numpy)
└── output/      # shadow run results (committed as evidence)
```

## Signal definitions (Approved Spec v0.2, FD #88)

### Eligibility (core — all must hold for CANDIDATE)

| Signal | Definition | Notes |
|---|---|---|
| **H1 — TTM EPS level breakout** | Latest TTM (trailing-4-quarter) diluted EPS > max TTM of the prior 8 quarters (~2y lookback) | EPS-level hypothesis; prior window = 8 quarters IMMEDIATELY before latest (stale history excluded) |
| **Revenue confirmation** | Latest-quarter revenue NOT shrinking YoY (revenue >= year-ago quarter) | Filters buyback/tax/one-off EPS inflation |
| **Stage eligibility** | Stage 1 (watch) or S2-early (priority); late-2/3/4 EXCLUDED | Stage Def v0.1 below |
| **Liquidity sanity** | price >= $2 AND avg 50d volume >= 100k | Production values (FD #89) |

### H2 — EPS-growth-rate acceleration (reported separately, NEVER combined silently)

Latest-quarter YoY EPS growth > max YoY growth of the prior 8 quarters. Computed
independently of H1 (hypothesis separation, FD #88). Combination decision DEFERRED
until both are validated separately.

### Enrichment (ADVISORY, never gating)

relative strength percentile, volume trend, extension context — reported in the
candidate record but NEVER affect eligibility (locked test asserts this).

## Stage Definition v0.1 (deterministic — PRODUCTION thresholds, FD #89)

| Stage | Rule (deterministic) | Eligible |
|---|---|---|
| S4 | close < 50MA < 150MA AND 150MA slope < 0 (confirmed downtrend) | ✗ excluded |
| S3 | 50MA materially below 150MA (< 0.98x) OR price < 50MA while 150MA not rising | ✗ excluded |
| S2-early | close > 50MA > 150MA, both sloping up, extension <= 15%, weeks-since-cross <= 8 | ✓ priority |
| S2-late | Stage 2 but extended > 15–20% or > 8 weeks since cross | ✗ excluded |
| S1 | price within ±5% of 50MA; 50MA within ±5% of 150MA; slopes |slope| < 0.5%/mo; price in 30–70% of 52w range | ✓ watch |
| UNCLASSIFIED | doesn't fit cleanly | ✗ (honest — no forced classification) |

All numeric bands are **PRODUCTION values approved by FD #89 (10 Aug 2026)** on
validation Phase 1 evidence (0 look-ahead violations, 0 revision flips, stability
0 flips — see `output/validation-2026-08-10/VALIDATION-REPORT.md`). Any NEW threshold
still requires Founder approval with evidence (FD #53).

## Point-in-time discipline (FD #58)

- Quarterly EPS/revenue from SEC EDGAR companyfacts with the actual FILING date as
  the as-of availability stamp (`eps_available_at` / `revenue_available_at`).
- XBRL reality handled explicitly:
  - pure-quarter vs YTD-cumulative values for the same period_end → keep SHORTEST
    duration (pure quarter).
  - fiscal-Q4 slot not reported as a pure quarter → DERIVE Q4 = annual − sum(3
    quarters), labelled `derived: true` (never a silent substitution).
  - stock splits (e.g. NVDA 10:1 Jun-2024) → pre-split EPS scaled to current share
    basis via DilutedAverageShares ratio, `split_factor` recorded per quarter.
- Price history: yfinance split-adjusted close.

## Known limitations (honest, shadow phase)

- yfinance `quarterly_income_stmt` returns only ~5 quarters — INSUFFICIENT for the
  9-quarter requirement (surfaced by the first shadow run). Primary source switched
  to SEC EDGAR companyfacts.
- Restatement history: companyfacts carries restated values; the latest-filed value
  wins per period_end (documented; revision-leakage testing deferred to validation
  Phase 1).
- Survivorship: FO-universe is a live 8-name list (validation Phase 1 adds PIT
  universe construction).
- Earnings-call disclosures (guidance, estimate revisions) not yet sourced.

## Running

```bash
# shadow scan (system Python 3.14 — has yfinance)
python3 discovery/equity_inflection/fetcher.py

# unit tests (any Python)
python -m pytest tests/test_equity_inflection_scanner.py -q
```

## Boundaries (non-authorization — FD #88)

This module does NOT authorize: standing production scanning, any threshold becoming
a hard gate, Task Idea Cards / CoS intake from scanner output, cron/automation,
radar contract changes, blog/UI/schema changes, legacy O'Neil/Minervini
entry/exit/stop-loss/position-sizing inheritance. Each requires a separate named
Founder Decision after validation evidence.

<!-- 2026-08-10 12:40 UTC+7 -->
