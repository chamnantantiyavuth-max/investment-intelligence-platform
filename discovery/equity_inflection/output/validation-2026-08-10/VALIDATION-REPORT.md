# Equity Inflection Validation Phase 1 — PIT Historical Validation Report (2026-08-10)

> Per `docs/PLAN-EQUITY-INFLECTION-VALIDATION-P1-v0.1.md` (T6/T7). Evidence pack:
> `discovery/equity_inflection/output/validation-2026-08-10/` (payloads.json,
> historical-run.json, bias-tests.json, stability.json, false-positive-review.json,
> capacity-load.json).
> Method: as-of reconstruction at 21 quarter-end dates (2021-06-30 .. 2026-06-30) ×
> FO-universe 8 names; every signal computed ONLY from facts filed ≤ asof (SEC
> companyfacts filed-date stamps, FD #58). Shadow-gated — no cards, no research
> capacity consumed (FD #88).

## 1. Headline results

| Metric | Result |
|---|---|
| Historical window | 21 as-of dates × 8 names = 168 snapshots |
| Candidate snapshots (eligible) | **12** (7 cycles with ≥1 candidate) |
| Capacity load | avg **1.71** candidates/cycle, max 3 (vs direction illustrative 4–8 recon-worthy) |
| Look-ahead violations | **0 / 168** (all tickers, all dates) |
| Revision flip rate | **0 flips / 48 measurable** (H1/H2/revenue unchanged when restatements ignored) |
| Stability | 7 perturbations × 4 dates × 8 names — **0 candidate-set flips** |

## 2. Point-in-time integrity (direction §4D tests)

### 2.1 Look-ahead bias — CLEAN
`lookahead_violations` on every ticker × every as-of date returned zero. The guard
lives inside `latest_by_filed` (values filed > T never enter the view — locked test
`test_lookahead_guard_is_at_the_source`).

### 2.2 Revision leakage — CLEAN (measurable window)
48 measurable as-of comparisons (8 names × last 6 as-of dates): **0 flips** of
H1/H2/revenue between the as-of view (restatement-aware) and the final-value view.
The FO-8 did not have material restatements inside the measured window; the
mechanism itself is proven by locked test `test_revision_flips_view_only_after_its_filed_date`
(synthetic restatement 1.0→2.0 flips the view only after its filed date).

### 2.3 Survivorship — HONEST LIMITATION (deferred, D1)
FO-universe = 8 live names, all survivors. Delisting coverage requires a PIT
universe source (CRSP-style, paid) — **deferred**. This validation is NOT
survivor-free and makes no such claim.

### 2.4 Corporate actions — verified + one honest artifact
Split adjustment via `WeightedAverageNumberOfDilutedSharesOutstanding` (tag verified
2026-08-10 — "DilutedAverageShares" returns 0 entries; fixed mid-run). Locked test
`test_asof_view_split_adjusts_pre_split_eps` proves pre-split EPS scales down 10x.
**Known artifact (documented, not a bug):** GOOGL/AMZN 2021–2022 candidates show
pre-split-basis TTM (e.g. GOOGL TTM 75–112, AMZN 52–64) — at those as-of dates the
2022 20:1 splits were unknown (correct PIT semantics); the false-positive review
must not interpret those as genuine inflections. This is exactly the
split-awareness the direction §4A requires, and it is honest about the basis.

## 3. Signal behavior (research-discovery quality, NOT forward returns)

### 3.1 The scanner caught the big one: NVDA AI inflection
- 2023-09-30 hit (TTM 4.14) → next 7.58 → next2 11.93 → **confirmed**.
- 2023-12-31 hit (TTM 7.58) → next 11.93 → **confirmed**.
This is the canonical "business inflection before/early market recognition" the
Founder's hypothesis targets — the 2023 NVIDIA earnings explosion was surfaced by
H1 at the moment TTM EPS first broke its 2-year frame. **Missed-opportunity review:
PASS on the highest-value case.**

### 3.2 Other confirmed inflections (TTM kept rising 2 quarters after hit)
- MSFT 2021 (7.34 → 8.94) — confirmed; faded into 2022 (rate-of-change cooled).
- GOOGL 2021 (75.03 → 103.75) — confirmed on pre-split basis; 2024 (5.80 → 6.97) confirmed.
- META 2021 (11.68 → 14.00), 2024 (14.87 → 17.38) — confirmed.
- JNJ 2021 (6.65 → 6.69) — marginal; mostly flat/faded afterwards.

### 3.3 Faded/one-off (correctly flagged — the false-positive filter works)
- AMZN 2022–2024: several H1 hits that faded (split-basis artifact in 2021–22; genuine
  fade in 2023–24). The scanner's `inflection_held=False` labels these honestly.
- TSLA 2022 (7.37 → 3.55), 2024 (4.30 → 3.55) — faded.
- META 2021-12 (14.00 → 13.19) — faded.

**Character mix across 49 H1-hit snapshots: 14 confirmed (29%), 35 faded/one-off (71%).**
For a discovery filter this is healthy — the funnel is designed to surface more than
deep research can absorb (direction §12), and the recon step exists to discriminate.

## 4. Stability (threshold sensitivity — plan §J Phase 6)

7 perturbations (extension ±5pp, slope ±0.2%/mo, range band ±10pp, window 6q/10q) ×
last 4 as-of dates × 8 names: **0 changes to any candidate-set membership**.
The proposed Stage Def v0.1 bands sit in a stable region — no radical candidate-set
flip from small threshold changes (direction §18J requirement satisfied).

## 5. Capacity load (plan §J Phase 5)

avg 1.71 candidates/cycle over the 8-name universe. Extrapolating the illustrative
funnel (direction §12): a ~300-name liquid universe at this hit rate ≈ 60+ hits/cycle
→ 15–20 interesting → 6–8 recon-worthy → 1–3 mandates. **Consistent with the
direction's funnel** (5,000 → 40–60 → 10–15 → 4–8 → 1–3).

## 6. Data-quality failure behavior

- Per-ticker fetch errors recorded honestly in payloads.json (`{"error": ...}`) —
  no fabricated candidates (verified: GOOGL share_entries=30 due to sparse early
  tagging; documented, not hidden).
- Snapshots with insufficient quarters (`<9`) return `eligible=False` + reason —
  never a silent signal.

## 7. Findings fixed during this run (real bugs caught by validation)

| # | Bug | Fix | Test |
|---|---|---|---|
| 1 | yfinance quarterly history = 5 quarters only | Primary EPS source → SEC EDGAR companyfacts | run-level |
| 2 | YTD-cumulative vs pure-quarter same period_end | Shortest-duration dedup (pure quarter wins) | `test_asof_view_derives_fiscal_q4` |
| 3 | Fiscal-Q4 not reported as pure quarter | Derive Q4 = annual − 3 quarters (`derived: true`) | `test_asof_view_derives_fiscal_q4` |
| 4 | `dur(v) or 9999` treats 0-day duration as missing | Explicit `is not None` check | 8/8 validation tests |
| 5 | Wrong share tag (`DilutedAverageShares` = 0 entries) | `WeightedAverageNumberOfDilutedSharesOutstanding` | run-level + `test_asof_view_split_adjusts_pre_split_eps` |
| 6 | `latest_by_filed` kept YTD over pure quarter | Selection = shortest duration, then latest filed | `test_revision_flips_view_only_after_its_filed_date` |

## 8. Verdict

**Validation Phase 1 PASS on the evidence gates that matter for a discovery filter:**
point-in-time integrity clean (0 look-ahead violations, 0 revision flips), the signal
surfaced the canonical NVDA AI inflection at the right moment, stability is robust to
threshold perturbation, and capacity load fits the direction's funnel. Survivorship
coverage remains the one honest limitation (D1, deferred — no free PIT delisting
source).

**NOT authorized by this report:** any production threshold, standing scanning,
Task Idea Cards / CoS intake, cron, radar/blog/UI/schema changes, or forward-return
acceptance criteria. Each requires a separate named Founder Decision (FD #88).

## 9. Next options for the Founder

(a) Approve the PROPOSED Stage Def v0.1 thresholds as production values (new named FD
    with this evidence pack as the basis) → standing scanner behavior.
(b) Expand universe (~100–300 liquid names) for a broader shadow pass first.
(c) Adjust signal/stage definitions (e.g., UNCLASSIFIED disposition, H2 handling,
    split-basis annotation in false-positive review).
(d) Stop — keep as a reference validation artifact.

<!-- 2026-08-10 13:20 UTC+7 -->
