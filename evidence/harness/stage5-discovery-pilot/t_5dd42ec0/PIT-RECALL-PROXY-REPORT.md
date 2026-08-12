# Recall Proxy #1 — Historical PIT Benchmark Recall (bounded)

> Task C of IIP Discovery Recall & Coverage v1.1 (Stage 5 bounded pilot).
> Method anchor: IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md §10 + §6.
> Run: 2026-08-12 — snapshot sample: 5 quarter-ends × 3 tickers = 15 PIT snapshots.

## 1. Benchmark (pre-registered, bounded denominator — §6)

| Case | Asof | Ticker | Label | Expected |
|---|---|---|---|---|
| first H1 hit of AI inflection (Phase 1 TTM 4.14) | 2023-09-30 | NVDA | POS | H1 fires |
| canonical inflection moment (Phase 1 TTM 7.58, confirmed) | 2023-12-31 | NVDA | POS | H1 fires |
| post 10:1-split regime; inflection held (Phase 1 TTM 11.93+) | 2024-12-31 | NVDA | POS | H1 fires |
| 2021 earnings inflection (Phase 1 TTM 7.34, confirmed) | 2021-06-30 | MSFT | POS | H1 fires |
| pre-inflection rate-hike selloff; EPS declining — must NOT f | 2022-06-30 | NVDA | NEG | H1 silent |
| quiet quality, no earnings inflection — must NOT fire | 2023-12-31 | JNJ | NEG | H1 silent |

## 2. Headline

- **Signal-level (H1) bounded recall: 100%** (4/4) — the detector recalled every pre-registered inflection.  
- **Signal-level bounded precision: 80%** (4/5) — 1 false positive on negative controls (JNJ, one-time-item spike; see §6.1).
- **Candidate-level (full eligibility gate) bounded recall: 50%** (2/4); precision: 100% (2/2).
- Look-ahead: **CLEAN** (15/15 snapshots clean).
- Identity: **stable** — CIK/title constant across all as-ofs, CIK-unique (yes).

## 3. Per-case results

| Case | Asof | Ticker | Label | H1 | TTM | prior max | Rev confirm | Stage | Eligible |
|---|---|---|---|---|---|---|---|---|---|
| first H1 hit of AI inflection (Phase 1 TTM 4.14) | 2023-09-30 | NVDA | POS | 🔥 | 4.14 | 3.85 | ✓ | UNCLASSIFIED | False |
| canonical inflection moment (Phase 1 TTM 7.58, c | 2023-12-31 | NVDA | POS | 🔥 | 7.58 | 4.14 | ✓ | S2-early | True |
| post 10:1-split regime; inflection held (Phase 1 | 2024-12-31 | NVDA | POS | 🔥 | 3.099784 | 2.356847 | ✓ | UNCLASSIFIED | False |
| 2021 earnings inflection (Phase 1 TTM 7.34, conf | 2021-06-30 | MSFT | POS | 🔥 | 7.34 | 6.71 | ✓ | S2-early | True |
| pre-inflection rate-hike selloff; EPS declining  | 2022-06-30 | NVDA | NEG | — | 3.73 | 3.85 | ✓ | S4 | False |
| quiet quality, no earnings inflection — must NOT | 2023-12-31 | JNJ | NEG | 🔥 | 13.46 | 7.81 | ✓ | S3 | False |

## 4. No-look-ahead verification (explicit method, §10)

1. **Guard at source:** `validation.latest_by_filed()` admits ONLY entries with `filed <= asof` (validation.py L48).
2. **Independent audit pass:** for each of the 15 snapshots, every EPS/revenue/share entry selected into the as-of view was re-checked for `filed > asof`; all price rows after `asof` were excluded (`asof_prices`).
3. **Helper cross-check:** `validation.lookahead_violations()` re-run on the bounded set.

Result: **15/15 snapshots clean** — zero violations.

## 5. Stable identity verification

- ticker→CIK→title from `equity_universe.py` (UNIVERSE_AS_OF 2026-08-11), identical for every as-of date.
- CIK uniqueness: **PASS** (0001045810, 0000789019, 0000200406).
- Split-basis PIT correctness: NVDA 10:1 split (Jun-2024) — as-ofs 2023-09-30/2023-12-31 see PRE-split basis (TTM ~4–8, old share counts), as-of 2024-12-31 sees split-adjusted series (share counts known at T). This is correct PIT semantics, not drift (Phase 1 §2.4).

## 6. Findings (diagnosis, NOT curve-fitting)

- The canonical NVDA AI inflection (2023-09-30 first hit, 2023-12-31 confirmation) is **recalled** by H1 at both quarter-ends using only then-available data; 2023-12-31 clears the full candidate gate (S2-early).
- MSFT 2021 inflection recalled (candidate-level ✓). Negative control NVDA@2022-06-30 (rate-hike selloff) correctly silent at both levels.
- No look-ahead leak, no identity drift, no revision leakage within the measurable window.

### 6.1 JNJ false positive — one-time item spike (signal-level only)

JNJ@2023-12-31: H1 fired on TTM EPS $13.46 because quarter 2023-10-01 shows EPS **$10.21** (filed 2023-10-27 — PIT-correct) vs adjacent quarters $1.3–2.0. That quarter carries a one-time item (Kenvue separation-era tax benefit). The detector has no one-time-item filter (EPS breakout is computed on the raw series, as designed in the approved spec). The **candidate gate correctly suppressed it** (stage S3 — price below 150MA, death-cross zone) → not eligible. Net effect at the pipeline's surfacing layer: no false candidate. This is the §10 "false-positive exciting story" control working as intended: detector fires, gate filters.

### 6.2 NVDA UNCLASSIFIED stages — stage strictness, not detector miss

NVDA@2023-09-30 and NVDA@2024-12-31: H1 AND revenue confirmation BOTH fired (signal-level recall ✓). Stage returned UNCLASSIFIED because the stock was in a parabolic uptrend (slope150 +44%/+19% per month, range position 0.85) — not a Stage-1 base and past the S2-early window. The detector surfaced the inflection; the stage gate declined a candidate in an extended price regime. This is stage-gate strictness (timing filter), explicitly NOT a detector miss — consistent with Phase 1's characterization.

## 7. Honest limitations

- Bounded denominator only (6 labeled cases). No claim about universal opportunity recall (§6).
- Survivorship: sample tickers are live FO-8 names; delisting coverage not tested (Phase 1 D1, deferred — no free PIT delisting source).
- Historical universe membership: the 98-name universe is as-of 2026-08-11; NVDA/MSFT/JNJ are FO-8 (in-universe throughout the pipeline's life).
- Stage/liquidity depend on then-available prices (yfinance 10y history) — prices are as-of-correct but yfinance is a shadow-phase source (FD #88).
- One-time-item sensitivity (JNJ §6.1) is reported as a detector characteristic, NOT tuned here — threshold changes require separate evidence + approval (§10, FD #53).

<!-- 2026-08-12 UTC+7 -->