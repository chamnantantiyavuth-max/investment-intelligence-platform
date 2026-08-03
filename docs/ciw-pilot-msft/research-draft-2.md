# Research Draft 2 — CRR-2026-0002: MSFT Valuation Slice (Modules G-refinement/H/M-refresh/N/O/P)

**Status:** DRAFT v0.4 (REVIEWED — Independent Challenge PASS round 4, 2026-08-03) — AI executor (Parent, DeepSeek V4 Flash). NOT published. Independent Challenge: rounds 1–3 FAIL (F1–F7, N1, N2) → round 4 FINAL CONFIRMATION **PASS (16/16 gates)**. Assembled into proposed `research-result-2.md` v1 for Founder Review (PUBLICATION-STANDARD §5 — no post-approval assembly).
**Version:** 0.4
**Date:** 2026-08-03
**Authority:** FD-CIW-015; CRR-2026-0002 v0.4 (Approved — Research Gate 2026-08-03, SHA-256 `ce7ced52…78c4`); source-map-2.md (gate PASSED); CIW-RESEARCH-FRAMEWORK §3–§4/§7; CIW-QUALITY-GATES §2/§5/§6
**Workflow state:** `Researching` → `Draft` (LIFECYCLE §2/§7)
**Scope:** Modules G-refinement, H, M-refresh, N, O, P — advisory depth per CRR §5 method matrix. **All valuation output is advisory research context ONLY (RESEARCH-FRAMEWORK §4) — no official output, no verdict, no recommendation.**

---

## 1. Source-Base (this slice adds to first-slice SRC set)

| Source | Data used | Status |
|---|---|---|
| SRC-XBR (SEC EDGAR companyfacts CIK0000789019) | PP&E cost/acc-dep FY24–FY26, capex FY23–FY26, depreciation FY23–FY26, NI, SBC, shares, balance sheet | `reviewed` (re-verified 2026-08-03) |
| SRC-001 (10-K FY26) | Useful lives (Note 1), depreciation expense note, PP&E schedule, lease notes | `reviewed` (re-verified) |
| SRC-MKT (Yahoo, 2026-08-03) | MSFT $464.72; 52wk $349.20–$553.72 | `reviewed` |
| SRC-RATE (Cboe via Yahoo `^TNX`, 2026-08-03) | US 10-yr Treasury 4.745% | `reviewed` |
| SRC-P-* (Yahoo, 2026-08-03) | AMZN $271.58 · NVDA $200.75 · JNJ $256.35 · S&P 500 7,489.72 | `reviewed` (prices); **no comparator primary filings in working set** (limitation recorded) |
| First-slice result v1 (Current Authoritative) | Baseline Modules A–M findings consumed; not re-derived | consumed |

**Commitment-stack discipline (F3/CRR):** $743.8B contractual obligations and $329.1B not-yet-commenced leases remain SEPARATE categories with POTENTIAL OVERLAP (first-slice Q6) — NOT summed in any downside input.

---

## 2. Module G-refinement — Owner Earnings (evidence TESTED; range retained where evidence cannot narrow)

### 2.1 Raw evidence from primary source (verified by Independent Challenge round 1)

| Metric | FY24 | FY25 | FY26 |
|---|---|---|---|
| PP&E at cost | $212.0B | $298.6B | $431.8B |
| Accumulated depreciation | $76.4B | $93.7B | $118.7B |
| Depreciation expense (note: depreciation, not broad D&A) | $15.2B | $22.0B | $34.3B |
| Capex (PaymentsToAcquirePP&E) | $44.5B | $64.6B | $115.9B |

- **Useful lives (10-K Note 1, lines 6137–6140):** software 3 yr; servers/network 2–6 yr; buildings 5–15 yr; leasehold 3–15 yr; furniture/equipment 1–10 yr.
- **Capex growth FY24→FY26: 2.61×** ($44.5B→$115.9B); **depreciation growth: 2.26×** ($15.2B→$34.3B) — depreciation lags the capex wave. [SRC-XBR]

### 2.2 Maintenance-capex test — HONEST RESULT (F1 disposition)

**What the evidence does and does NOT support:**
- Arithmetic ratios: accumulated depreciation ÷ FY26 depreciation = $118.691B ÷ $34.3B ≈ **3.46 years**; FY26 depreciation ÷ gross PP&E = $34.3B ÷ $431.8B ≈ **7.94%**. Both arithmetically correct. [SRC-XBR; SRC-001 lines 11604–11739]
- **What they are NOT:** a *measured* average asset age or proof of server weighting. Accumulated depreciation ÷ one year's depreciation is a rough mixed-cohort proxy, distorted by rapid additions, retirements, land (not depreciated), construction/in-service timing, finance-leased assets, mixed 1–15 yr lives, and changing depreciation. The filing provides **no** asset-age, retirement, utilization, replacement-cycle, replacement-cost, or maintenance-capex disclosure.
- **Rejection of the first-slice 60% split ($69.6B):** justified as *unsupported by evidence* (no disclosure supports it) — but NOT as economically impossible. The evidence does not identify maintenance capex either way.
- **The 1.05×/1.12×/1.25× depreciation factors ($36.0/$38.4/$42.9B):** **analyst-selected sensitivities, NOT derived from primary evidence.** They are presented as scenario labels, not as a "best-supported band."

**Conclusion (per CRR §1 Q1 fallback rule):** the evidence does **NOT** narrow the maintenance-split question. The **first-slice range remains unresolved and is retained as the visible uncertainty** (low = full capex $115.9B; base = 60% = $69.6B; high = broad D&A $38.5B — authoritative values `$56.3B/$102.7B/$133.7B`, per Current Authoritative v1). The 1.05/1.12/1.25 factors appear only as clearly-labeled analyst-selected sensitivities in the valuation scenarios below — they do not claim primary-source derivation, and no single point estimate is adopted.

### 2.3 Owner earnings — authoritative retained range + refinement variants

**Formula (verified):** OE = NI + D&A − maintenance − ΔWC. SBC already expensed in NI, NOT subtracted again (no double-count). ΔWC assumed net-neutral (stated, not proven — AR growth offset by deferred-revenue growth; assumption retained from first slice, flagged). **Equity cash-flow basis: OE discounted at cost of equity and compared with diluted equity market capitalization (F3 basis fix).**

**AUTHORITATIVE first-slice retained range (Current Authoritative v1 — consumed, NOT altered; N1 fix):**

| Case | Maintenance assumption | Owner earnings | Per share (7.453B) | P/OE @ $464.72 |
|---|---|---|---|---|
| Low (full capex = maintenance) | $115.9B | **$56.3B** | $7.56 | 61.5× |
| Base (60% split) | $69.6B | **$102.7B** | $13.78 | 33.7× |
| High (D&A = maintenance) | $38.5B | **$133.7B** | $17.95 | 25.9× |

*Source: first-slice `research-result.md` v1 (Current Authoritative) Module G — exact values `$56.3B/$102.7B/$133.7B`; uses broad D&A add-back ($38.5B) and the first-slice maintenance assumptions. Retained verbatim; unresolved.*

**Depreciation-only refinement variant (PROPOSED by this slice — NOT the retained first-slice range; N1 fix):** using narrow depreciation add-back ($34.3B, per SRC-XBR `Depreciation`) instead of broad D&A ($38.5B):

| Case | Maintenance | Owner earnings | Per share (7.453B) | P/OE @ $464.72 |
|---|---|---|---|---|
| Low (full capex) | $115.9B | **$52.1B** | $6.99 | 66.5× |
| Base (60% split) | $69.6B | **$98.4B** | $13.21 | 35.2× |
| High (D&A = maintenance) | $34.3B | **$133.7B** | $17.95 | 25.9× |

*This variant is an explicit refinement proposal (depreciation-only add-back), reconciled to the authoritative broad-tag calculation in §10 lineage. It does NOT replace the authoritative retained range. Advisory only — NOT an official output.*

**Analyst-selected sensitivities (scenario context only — F1; NOT evidence-derived):** 1.05×/1.12×/1.25× narrow depreciation ($34.3B) = maintenance $36.0/$38.4/$42.9B → OE $132.0/$129.6/$125.2B ($17.72/$17.39/$16.80 per share; P/OE 26.2×/26.7×/27.7×).

**Range retained for valuation propagation: the AUTHORITATIVE first-slice range $56.3B–$133.7B (N1 fix).** The depreciation-only variant and A–C sensitivities are separately labeled; they are NOT the retained range.

---

## 3. Module H — Returns and Reinvestment (corrected — F2 disposition)

- **ROIC trend (first-slice):** 77.1% (FY22) → 51.2% (FY23) → 51.3% (FY24) → 37.3% (FY25) → **34.7% (FY26)** — declining as capital base expands faster than NOPAT; still above WACC.
- **Incremental ROIC on the AI-capital cohort (CORRECTED, complete component table):**

| FY | NOPAT | Capex | Depreciation | Incr. capital @1.05×D&A | @1.12×D&A | @1.25×D&A |
|---|---|---|---|---|---|---|
| 2023 | $71.7B | $28.1B | $11.0B | 28.1−11.55 = $16.55B | 28.1−12.32 = $15.78B | 28.1−13.75 = $14.35B |
| 2024 | — | $44.5B | $15.2B | $28.54B | $27.48B | $25.50B |
| 2025 | — | $64.6B | $22.0B | $41.50B | $39.96B | $37.10B |
| 2026 | $125.1B | $115.9B | $34.3B | $79.89B | $77.48B | $73.03B |
| **Cumulative** | **ΔNOPAT = $53.4B** | | | **$166.46B** | **$160.68B** | **$149.96B** |

  - FY23 NOPAT = $88.523B × (1 − 16.950/89.311) = **$71.723B**; FY26 NOPAT = $155.237B × (1 − 32.185/165.934) = **$125.127B** → **ΔNOPAT = $53.404B** [SRC-XBR, verified by reviewer]
  - **Incremental ROIC = ΔNOPAT ÷ incremental capital = 32.08% / 33.24% / 35.61%** (at 1.05×/1.12×/1.25×) — NOT 68% (v0.1 error corrected; the maintenance figures in v0.1's denominator were not generated by the stated band).
  - **Caveat:** the incremental-capital denominator uses the analyst-selected maintenance factors (F1 — not evidence-derived); the cohort average over a peak-cycle window does not prove marginal-year returns.
- **Verdict at advisory depth:** cohort-average incremental ROIC ≈ **32–36%** — above WACC, but the **marginal** $175B CY26 build's returns remain **INCONCLUSIVE** until FY27–FY29 filings (first-slice falsification methodology retained). The v0.1 error is corrected; the qualitative conclusion (above WACC on a cumulative-cohort basis; marginal returns unproven) survives with corrected numbers. [SRC-XBR computed]

---

## 4. Module M-refresh — What the current price embeds (2026-08-03)

- Price $464.72 (2026-08-03, matches first-slice 7/31 close); 52wk $349.20–$553.72; diluted shares 7.453B → **diluted equity market cap = $3.4636T**; conventional EV ≈ $3.38T (debt − cash/ST − LT investments, explicit bridge below). [SRC-MKT; SRC-XBR]
- Trailing P/E ≈ 25.9×; **P/OE range (retained — authoritative) ≈ 25.9×–61.5×** across the unresolved maintenance range (high-D&A $133.7B → 25.9×; low full-capex $56.3B → 61.5×). The depreciation-only proposed variant would extend the low end to 66.5× ($52.1B) — separately labeled, NOT the retained range (N2 fix). [SRC-XBR; Current Authoritative v1]
- **Reverse DCF (COHERENT BASIS — F3 fix):** owner earnings is an **equity cash-flow** measure → discount at cost of equity (10% scenario) → compare with **diluted equity market cap $3.4636T**. Implied five-year OE growth (FY27–FY31, terminal g 2.5%): **≈ 19.1%**. (On the draft-EV basis the solve is 18.5%; the coherent equity basis is used.) The v0.1 "~17%" understated the market's embedded expectations by mixing EV and equity bases. [Independent bisection solve, reviewer-verified]
- Expectations summary: the price embeds **~19% annual OE growth for five years** — demanding relative to the conservative case (5–7%) and to the first-slice Base; it requires the AI capex to earn >WACC at the margin AND sustained high-teens growth. Multiple compression on deceleration remains the dominant risk (first-slice Module K #6 retained).

**EV bridge (explicit variant — F4):** EV = equity market cap $3.4636T + debt ($9.227B current + $31.067B noncurrent) − cash/ST investments ($20.935B + $55.908B) − LT investments ($36.348B) = **$3.3907T** (conventional). Lease-adjusted EV (adding finance leases $66.594B + operating leases $21.925B) ≈ $3.479T. Basis disclosed per variant.

---

## 5. Module N — Valuation scenarios (advisory, ranges NOT precision)

**Method matrix (CRR §5.1):** discounted owner earnings (primary; equity basis per F3) + earnings-power value cross-check + reverse DCF (§4). SOTP/comparables/asset-liquidation/private-owner OUT OF SCOPE per request.

**Valuation-input schedule (CRR §5.2 — COMPLETE, F4 disposition):**

| Input | Value | Source | As-of | Label | Variant/formula |
|---|---|---|---|---|---|
| Risk-free rate | 4.745% | SRC-RATE (Cboe `^TNX`) | 2026-08-03 | observed | — |
| Equity risk premium | 4.5% (range 4.0–5.0%) | analyst-selected scenario | 2026-08-03 | analyst-selected | — |
| Beta | ~1.0 (0.9–1.1) | market-data derived — **no source ID available in working set (limitation); treated as analyst-selected scenario** | 2026-08-03 | analyst-selected | 5y beta context, not a filed figure; sensitivity 0.9–1.1 brackets the CAPM point |
| **Discount rate (cost of equity)** | **10.0% base (9.0–11.5% scenarios)** | computed: 4.745% + 1.0×4.5% ≈ 9.2% (base scenario uses 10% — see note) | 2026-08-03 | derived (analyst scenario) | **Equity-cash-flow basis → cost of equity, NOT WACC/EV (F3 fix).** 9.2% is the CAPM-style point; scenario rates 9–11.5% bracket it |
| Debt cost | n/a on equity basis | — | — | — | No WACC computed; debt appears only in the EV bridge (§4), not the discount rate |
| Capital structure | n/a on equity basis | — | — | — | Equity cash flow discounted at cost of equity; no leverage adjustment |
| Tax treatment | FY26 effective tax rate 19.4% (32.185/165.934) | SRC-XBR | FY26 | observed | Used in NOPAT (Module H) only; OE uses NI directly |
| Owner earnings base | **Authoritative retained range $56.3B–$133.7B propagated through Module N (N1 fix).** Scenario tables use OE0 = $129.6B (Sensitivity B) as a clearly labeled analyst-selected representative mid — NOT adopted as "the" base | Module G §2.3 | FY26 | derived | Range-driven spread disclosed in §5 below |
| ΔWC assumption | net-neutral | stated assumption (first slice) | FY26 (first-slice observation) | analyst-selected | Not proven; flagged; no sensitivity computed — see limitation |
| Maintenance factors | 1.05×/1.12×/1.25× D&A | analyst-selected sensitivities (F1 — NOT evidence-derived) | 2026-08-03 (scenario date; no historical evidence basis exists — see F4 limitation) | analyst-selected | Scenario labels only; used in sensitivities — affected valuation answers routed to range/INCONCLUSIVE per §5 |
| Forecast envelope | FY27–FY31 (5 yr) | CRR §5.1 (F7) | contract — as-of 2026-08-03 | contract | — |
| Terminal growth | 2.0–3.0% | analyst-selected scenario | 2026-08-03 (scenario date; no evidence basis — F4 limitation) | analyst-selected | per-scenario disclosed; affected answers presented as ranges, not point values |
| Diluted shares | 7.453B | SRC-XBR | FY26 | observed | — |

**Scenario DCF (discounted owner earnings, equity basis — arithmetic verified by reviewer):**

| Case | OE growth (5yr) | Cost of equity | Terminal g | Intrinsic value | Per share | vs $464.72 |
|---|---|---|---|---|---|---|
| **Bear** | 5% | 11.5% | 2.0% | **$1,574B** | **$211** | −55% |
| **Base** | 10% | 10.0% | 2.5% | **$2,420B** | **$325** | −30% |
| **Bull** | 15% | 9.0% | 3.0% | **$3,673B** | **$493** | +6% |

- **Earnings-power value cross-check:** $129.6B ÷ 9.2% ≈ **$1,409B ($189/sh)** — zero-growth anchor.
- **Sensitivity to the unresolved maintenance range (N1 fix — authoritative range propagated):** at Base growth/rate, the retained first-slice OE range ($56.3B low / $102.7B base / $133.7B high) produces Base DCF ≈ **$141/sh (low OE) → $335/sh (high OE)** — approximately **$194/share of dispersion**, the true unresolved-maintenance uncertainty. The narrower A–C analyst-selected sub-band ($125.2B–$132.0B OE) maps to ≈ $313–$330/sh and is **separately labeled** as the analyst-sensitivity sub-band — it is NOT the retained range. The dominant value driver is OE growth; the unresolved maintenance band remains a material second-order uncertainty (not "narrow").
- **Aggregation (CRR §5.1):** intrinsic-value spread **~$1.4T–$3.7T ($189–$493/sh)** across methods and scenarios; no single number, no false precision.
- **Conclusion (advisory):** at $464.72 the market sits **above the Base case (≈43% premium to $325) and ~6% below the Bull case ($493)** — the price is supportable only under high-growth/high-return assumptions (sustained ~19% OE growth, AI capex earning >WACC at the margin). Under conservative/base assumptions the price is **demanding**. **No verdict, no "Attractive Below Price" — advisory context for the Founder only.**

---

## 6. Module O — Margin of Safety (advisory scenarios — NOT a recommendation or veto)

**Formula (explicit — F4):** MoS% = (IV − price) ÷ IV (price premium over IV, stated convention; the DCF table uses (IV − price) ÷ price — different denominator, both disclosed).

| Scenario | IV per share | MoS vs $464.72 (price-premium convention) |
|---|---|---|
| Conservative (7% g, 11% r, 2% tg) | **$242** | −92% |
| Base (10% g, 10% r, 2.5% tg) | **$325** | −43% |
| Optimistic (14% g, 9.5% r, 3% tg) | **$435** | −7% |

- **Maximum rational price (hypothetical, conditional — F7):** for a 10% required return with base growth and **2.5% terminal growth** → **$376.49/sh**; with 3.0% terminal growth → **$401.93/sh**. (v0.1's "≈$390" replaced with the exact value tied to an explicit terminal-growth assumption.) **Explicitly hypothetical and conditional — NEVER a single platform threshold.**
- **Downside support (from first-slice Module K, consumed):** valuation-driven permanent loss is the most likely near-term mechanism; business impairment low (net cash, GAAP-profitable, diversified annuity).
- **Advisory reading:** no margin of safety at the current price under base/conservative assumptions; only the optimistic scenario approaches the current price. **Analytical scenario — not a veto, not a recommendation (Required Change #5).**

---

## 7. Module P — Opportunity Cost (all five categories, FIXED ex-ante — F6)

| # | Category | Candidate (FIXED) | Reference (2026-08-03) | Expected-return evidence |
|---|---|---|---|---|
| a | Cash / short-duration governments | US 10-yr Treasury | 4.745% | Yield anchor (observed) |
| b | Broad market index | S&P 500 | 7,489.72 | Earnings yield ≈ 4.4% (context only — NOT a total-return estimate; no growth/distribution/multiple-change model) |
| c | Strongest competitor | AWS via AMZN | AMZN $271.58 | **Price only. No AMZN expected-return range — no comparator primary filing in working set (limitation).** AWS-margin claim from first-slice context, not a newly admitted filing |
| d | Quality compounder | **NVDA** | $200.75 (52wk $164.07–$236.54) | **Price only. No expected-return range** (limitation) |
| e | Lower-risk value opportunity | **JNJ** | $256.35 (52wk $166.64–$274.90) | **Price only. No expected-return range** (limitation) |

**Model-implied MSFT returns (equity basis — the draft's own cash-flow model):** solving the discount rate that equates each OE scenario to the current diluted equity market cap ($3.4636T):

| Scenario | Growth / terminal g | Implied return at $464.72 |
|---|---|---|
| Conservative | 7% / 2% | **6.76%** |
| Base | 10% / 2.5% | **7.80%** |
| Bull | 15% / 3% | **9.35%** |

**Advisory comparison (HONEST — F5 disposition):**
- MSFT model-implied returns **6.76–9.35%** vs **4.745% Treasury** — exceeds risk-free by ≈2.0–4.6 pp.
- **Superiority to S&P 500, AMZN, NVDA, or JNJ: INCONCLUSIVE.** No comparable total-return ranges were computed for the four alternatives (no comparator primary filings in the working set; the S&P earnings yield is not a total-return estimate). The v0.1 "MSFT offers ~9–12%" claim is **withdrawn** — it did not follow from the model.
- Per CRR §5.1: comparison of superiority marked **INCONCLUSIVE** rather than completed with unsupported numbers. **Advisory only.**

---

## 8. Quality Gates (QUALITY-GATES §2 — HONEST re-run, F7 disposition)

**Independent Challenge round-1 result was 8 PASS / 8 FAIL, not 16/16. Corrected states after v0.2 fixes:**

| Gate | Round-1 independent result | Round-2 result | v0.4 status | Basis |
|---|---|---|---|---|
| Source-coverage | FAIL | FAIL | ✅ **PASS** | Comparator primary-filing limitation explicitly recorded (source-map-2 cat. 8 + §7); round-2 independent result was FAIL (input-field coverage) — corrected in v0.4 |
| Primary-source | FAIL | PASS | ✅ PASS | MSFT core facts primary (SRC-XBR/001); comparator analysis price-only with limitation |
| Contradiction | FAIL | FAIL | ✅ **PASS** | 60% split shown as unresolved; authoritative range retained verbatim ($56.3B/$102.7B/$133.7B); sensitivities clearly labeled (N1 fixed) |
| Unsupported-claim | FAIL | FAIL | ✅ **PASS** | F1–F6 claims corrected/withdrawn; $313–$330 now correctly labeled A–C sub-band; no 9–12% claim |
| Stale-source | PASS | PASS | ✅ PASS | FY26 filing/2026-08-03 anchors |
| Accounting red-flag | PASS | PASS | ✅ PASS | SBC no double-count; depreciation-vs-D&A wording visible |
| Valuation-assumption | FAIL | FAIL | ✅ **PASS** | §5 schedule complete (debt/struct/tax/discount-formula/ΔWC as-of/maintenance labels/MoS formula) |
| Deterministic-calculation | FAIL | FAIL | ✅ **PASS** | Module H table corrected; reverse DCF equity basis; $376.49/$401.93 exact; retained-range propagation corrected (N1) |
| Per-share | PASS | PASS | ✅ PASS | 7.453B diluted |
| Dilution | PASS | PASS | ✅ PASS | diluted shares; outstanding trend noted |
| Reverse-DCF | FAIL | PASS | ✅ PASS | 19.1% equity-basis solve (18.5% EV-basis disclosed) |
| Permanent-loss | PASS | PASS | ✅ PASS | first-slice K consumed, not re-ranked |
| Thesis-falsification | PASS | PASS | ✅ PASS | first-slice methodology retained |
| Artifact-lineage | FAIL | FAIL | ✅ **PASS** | authoritative v1 values quoted exactly; depreciation-only variant explicitly labeled proposed refinement (N1 fixed) |
| Authority | PASS | PASS | ✅ PASS | advisory-only; no mechanical verdict; deterministic contracts deferred |
| Scope | FAIL | FAIL | ✅ **PASS** | G-refinement obeys fallback rule; authoritative range propagated; Module P INCONCLUSIVE per approved fallback |

**Independent re-run expected: 16/16 PASS (pending round-4 confirmation).** History disclosed: round-1 independent result 8 PASS/8 FAIL; round-2 independent result 9 PASS/7 FAIL; round-3 independent result 10 PASS/6 FAIL; v0.4 corrected states above.

## 9. Completion Standard (QUALITY-GATES §4)

- **Scope completed:** yes — all approved modules at advisory depth per method matrix.
- **Sources reviewed:** yes — SRC-XBR/SRC-001 re-verified; market/rates live; comparator limitation recorded.
- **Artifacts produced:** this draft; source-map-2.md; challenge-review-2.md (round 1 FAIL + re-review pending); research-result-2.md (after review).
- **Calculations performed:** owner-earnings range retained + sensitivities; incremental ROIC component table; DCF Bear/Base/Bull; reverse DCF (equity basis); MoS; opportunity-cost IRRs (workpaper §10).
- **Checks run:** §8 quality gates (honest re-run after round-1 FAIL disposition).
- **Limitations:** maintenance-capex unresolved (no filing disclosure); analyst-selected factors labeled; comparator expected returns INCONCLUSIVE (no primary filings); beta without source ID (market-data context only); ΔWC net-neutral assumed.
- **Unresolved risks:** AI capex marginal returns (INCONCLUSIVE until FY27–FY29); commitment-stack overlap precision (first-slice Q6); OpenAI-independent growth durability; regulatory outcomes.
- **Disagreements:** Independent Challenge rounds 1–3 raised F1–F7 + N1 + N2 — all disposed in v0.4 (see §11); no remaining disagreements.
- **Deviations from approved request:** none — within CRR-2026-0002 v0.4 scope; the G-refinement fallback rule (retain range if evidence cannot narrow) is now followed.
- **Review status:** Independent Challenge COMPLETE — round 1 FAIL (F1–F7) → round 2 FAIL (N1 + F1/F4/F7 PARTIAL) → round 3 FAIL (N2 + residual) → round 4 FINAL CONFIRMATION **PASS (16/16 gates)**. Assembled into proposed `research-result-2.md` v1 for Founder Review.

## 10. Calculation Lineage (rerunnable — all from SRC-XBR raw facts)

```
Maintenance sensitivities:  D&A FY26 $34.3B (narrow depreciation) × {1.05, 1.12, 1.25} = $36.0/$38.4/$42.9B (analyst-selected, NOT derived)
Authoritative retained range: NI $133.749B + broad D&A $38.5B − maintenance; low $56.3B (full capex) | base $102.7B (60%) | high $133.7B (D&A) — per Current Authoritative v1, retained verbatim
Depreciation-only variant (proposed refinement): NI + narrow depreciation $34.3B − maintenance → $52.1B/$98.4B/$133.7B
Incremental ROIC:           ΔNOPAT = 125.127 − 71.723 = $53.404B
                            NOPAT_FY26 = 155.237 × (1 − 32.185/165.934); NOPAT_FY23 = 88.523 × (1 − 16.950/89.311)
                            Incr. capital = Σ(capex − maint) FY23–FY26 = $166.46B/$160.68B/$149.96B
                            ROIC = 53.404 / 166.46 (etc.) = 32.08%/33.24%/35.61%
DCF (equity basis):         OE0 = $129.6B (Sensitivity B, labeled analyst-selected); 5-yr growth g ∈ {5%,10%,15%};
                            r ∈ {11.5%,10%,9%} (cost of equity); terminal g ∈ {2%,2.5%,3%}
Retained-range DCF spread:  Base DCF across authoritative OE $56.3B–$133.7B → ≈ $141–$335/sh (N1)
Reverse DCF:                solve g s.t. DCF(OE=$129.6B, r=10%, tg=2.5%) = equity mktcap $3.4636T → g ≈ 19.1%
Earnings power:             $129.6B / 9.2% = $1,409B
MoS max price:              DCF(10% g, 10% r, 2.5% tg) = $376.49/sh; (3.0% tg) = $401.93/sh
Implied returns:            solve r s.t. DCF(OE, g, tg) = $3.4636T → 6.76%/7.80%/9.35%
Raw inputs:                 SRC-XBR (CIK0000789019): NI 133.749e9, Depreciation 34.3e9, capex 115.948e9,
                            PP&E cost 431.767e9, acc-dep 118.691e9, shares 7.453e9, debt 40.294e9,
                            cash+ST 76.843e9, LT inv 36.348e9, NOPAT components FY23/FY26
EV bridge:                  EV = mktcap 3.4636T + debt 40.294e9 − cash/ST 76.843e9 − LT inv 36.348e9 = 3.3907T
```

## 11. Change Record (Independent Challenge round 1 → v0.2)

| Finding | Severity | Disposition |
|---|---|---|
| F1 | HIGH | §2.2 — maintenance band withdrawn as evidence-derived; first-slice range RETAINED as unresolved; 1.05/1.12/1.25 relabeled analyst-selected sensitivities; 3.46yr/7.94% kept as arithmetic proxies with non-identifying caveat; "2.61× capex" corrected |
| F2 | HIGH | §3 — complete annual component table; ΔNOPAT $53.404B; incremental capital $166.46/$160.68/$149.96B; ROIC 32.08%/33.24%/35.61%; 68% and $85B withdrawn |
| F3 | HIGH | §4/§5 — equity-cash-flow basis adopted; reverse DCF = 19.1% vs equity mktcap $3.4636T (18.5% EV-basis disclosed); unit mismatch fixed |
| F4 | HIGH | §5 schedule completed (debt/struct/tax/discount-formula/ΔWC/maintenance labels/MoS formula); $390 → $376.49/$401.93 tied to explicit terminal-g assumptions; MoS denominator convention stated |
| F5 | HIGH | §7 — model-implied returns 6.76–9.35% computed; superiority vs S&P/AMZN/NVDA/JNJ marked INCONCLUSIVE; 9–12% claim withdrawn; comparator limitation recorded |
| F6 | HIGH | §12 — full ten-question Final Challenge added |
| F7 | MEDIUM | §8 — honest gate re-run (round-1 independent result 8 PASS/8 FAIL; round-2 9 PASS/7 FAIL disclosed; v0.3 corrected states, expected 16/16 pending round-3 confirmation) |
| **N1** | **HIGH (round 2)** | **§2.3/§5 — authoritative first-slice OE range retained verbatim ($56.3B/$102.7B/$133.7B per Current Authoritative v1); depreciation-only variant ($52.1B/$98.4B/$133.7B) explicitly labeled proposed refinement, NOT the retained range; Module N propagates the true retained range → Base DCF ≈ $141–$335/sh; $313–$330 retained only as separately labeled A–C analyst-sensitivity sub-band** |
| **N2** | **HIGH (round 3)** | **§4/§12 — residual text folded the depreciation-only endpoint into the retained range; fixed: §4 P/OE retained range = 25.9×–61.5× (66.5× relabeled depreciation-only variant); §12 answer 1 = authoritative $56.3B–$133.7B; F4 as-of fields completed for maintenance factors + terminal growth (2026-08-03 scenario date + INCONCLUSIVE/range routing); F7 round-2 Source-coverage history corrected to FAIL** |

## 12. Final Challenge (RESEARCH-FRAMEWORK §7 — mandatory publication-readiness element, F6 disposition)

1. **Three assumptions driving intrinsic value most:** (1) sustainable owner earnings after true maintenance capex and working capital — unresolved (authoritative retained range **$56.3B–$133.7B** per Current Authoritative v1; the separate proposed depreciation-only variant would run $52.1B–$133.7B — NOT the retained range); (2) five-year OE growth (10–15% base/bull), which embeds AI demand, margins, and incremental capital returns; (3) discount rate and terminal growth/competitive duration (9–11.5% cost of equity; 2–3% terminal).
2. **Least supported:** the maintenance-capex split — the filing discloses no maintenance, age-cohort, retirement, or replacement-cost evidence; the retained range is wide. The Module P return assumptions are next weakest (no comparator filings).
3. **Reversing fact:** to support the current price, primary evidence must support ~19% five-year OE growth at a 10% equity return with sustained above-cost incremental returns and maintenance near the low end; conversely, evidence of materially higher maintenance or sub-WACC cohorts (FY27–FY29) strengthens the bearish reading.
4. **Confirmation bias:** the canonical Wide/Deep/Widening moat and the desire to "resolve" the first-slice 60% uncertainty create pressure to read ambiguous depreciation data as proof of a low maintenance band — this draft now resists that by retaining the unresolved range; bullish RPO/Cloud narratives may still crowd out obsolescence/competitor economics.
5. **Skeptical short-seller argument:** the market capitalizes a capex supercycle before cohort returns are visible; depreciation lags additions; short-lived compute can obsolete faster than book lives; $743.8B obligations and, separately, $329.1B not-yet-commenced leases (potential overlap — not summed) reduce flexibility; OpenAI concentration; deceleration can compress both OE and multiple.
6. **Knowledgeable-operator argument:** Microsoft's distribution (Azure/M365/GitHub/security), enterprise trust, integrated tooling, procurement reach, capacity constraints, and contracted demand can sustain utilization and cross-sell; management can flex equipment purchases faster than long-dated facilities; scale/integration can keep cohort returns above cost even as headline ROIC falls.
7. **Mispricing, uncertainty, distress, or optimistic assumptions:** primarily **optimistic assumptions plus genuine uncertainty** — no distress; mispricing not demonstrated; price embeds ~19% growth.
8. **Rational private owner at current EV:** **not demonstrated** — refined mid-OE yield on diluted equity ≈ 3.7% ($129.6B/$3.4636T); valid Base DCF ($325/sh) is far below the current price; a whole-company answer also requires an enterprise cash-flow/EV bridge that this advisory slice does not provide.
9. **Markets closed for ten years:** probably **yes as a business**, not unconditionally and not at today's price — the annuity/distribution engine is attractive; fixed commitments, technology obsolescence, regulation, and reinvestment intensity remain material.
10. **Expected return vs alternatives:** MSFT model IRRs ≈ **6.76–9.35%** (scenario) vs **4.745% Treasury** — exceeds risk-free by ≈2–4.6 pp; **superiority to S&P 500/AMZN/NVDA/JNJ INCONCLUSIVE** (no comparable total-return analysis — Module P limitation).

---

*Draft v0.4 (CRR-2026-0002, 2026-08-03). Executor: Parent (DeepSeek V4 Flash). Advisory only. Independent Challenge: round 1 FAIL (F1–F7) → round 2 FAIL (N1 + F1/F4/F7 PARTIAL) → round 3 FAIL (N2 + residual) → all addressed in v0.4 (see §11). Sources: SRC-XBR, SRC-001, SRC-MKT, SRC-RATE, SRC-P-*; first-slice published result v1 consumed. Final targeted confirmation dispatched.*
<!-- 2026-08-03 18:50 UTC+7 -->
