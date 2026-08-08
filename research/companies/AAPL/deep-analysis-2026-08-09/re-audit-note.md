# Targeted Re-Audit — RM-2026-0004 Apple Deep Analysis v3

**Artifact re-audited:** `main-deep-analysis-essay.md` (corrected artifact identified as v3 in its footer)  
**Prior audit:** `audit-note.md` — item 8 FAIL; items 1–7 and A1–A3 PASS  
**Opposing control:** `cro-opposing-essay.md` — FAIL verdict at line 25  
**Scope:** item 8 disposition only, plus regression checks for prior items 1–7 and re-performance of A1–A3  
**Point-in-time:** 2026-08-09 under FD #58  
**Re-audit timestamp:** 2026-08-09 03:35:20 +0700  
**Gate rule:** any FAIL blocks publication

## Item 8 targeted disposition

| Check | PASS/FAIL | Evidence and judgment |
|---|---|---|
| **8a. Unresolved rent-capture erosion is binding on any attractive-investment finding** | **PASS** | The core verdict now says attractiveness is “unestablished unless two conditions are jointly met”: a synchronized valuation that explicitly incorporates and tests the full rent-loss chain, and survival of that scenario. It further states that deterioration in profit captured per relationship prevents the evidence base from establishing attractiveness and that both conditions remain unsatisfied (`main-deep-analysis-essay.md:16`). Section 6 independently propagates the same two-condition requirement (`:78`). This is substantive control of the investment conclusion, not merely a “controlling risk” label, and disposes the CRO FAIL (`cro-opposing-essay.md:25`). |
| **8b. “The gap is price” is reconciled; price is not the sole missing condition** | **PASS** | The former sole-gap formulation is gone. The core verdict expressly says “not only because of price” and identifies both missing valuation and unresolved rent-capture economics (`main-deep-analysis-essay.md:16`). Section 6 calls valuation “one of two unmet conditions,” with survival of the rent-capture-loss scenario as the other (`:78`). |
| **8c. No invented price, discount, probability, or threshold introduced** | **PASS** | The correction supplies no price, discount, probability, hurdle, or new numerical threshold. It preserves valuation as indeterminate and states that no synchronized price/model exists (`main-deep-analysis-essay.md:14,73-78,101`). The existing −2σ reference remains the approved value-trap detector requirement and was already cleared under prior item 7; it is not a correction-created threshold (`:52-56`). |
| **8d. Correction did not regress prior items 1–7** | **PASS** | All seven prior dispositions remain intact, as detailed below. |

## Regression check — prior items 1–7

| Prior item | PASS/FAIL | Regression evidence |
|---|---|---|
| **1. Moat primary-integrator framing** | **PASS** | The customer interface remains the “primary integrator and rent-capture control point,” explicitly not a sole moat engine or three independent proofs (`main-deep-analysis-essay.md:12,27-40`). |
| **2. Six-area taxonomy** | **PASS** | Share of Mind, Switching Cost, Network Effect, Intangible Assets, Cost Advantage, and Efficient Scale remain separately assessed; Migration Cost remains nested under Switching Cost; shared interface evidence is counted once (`:27-40`). |
| **3. Earnings ADEQUATE with blockers** | **PASS** | The verdict remains **ADEQUATE**, with FY25 88.18% FCF/NI, NI/OCF divergence, unexplained intangible growth, and working-capital/maintenance-capex gaps blocking HIGH (`:14,42-50`). |
| **4. Capital-allocation capacity strong / quality INCONCLUSIVE** | **PASS** | The A− grade remains withdrawn; capacity is strong and allocation quality remains **INCONCLUSIVE**, with price-vs-value, ASR timing, M&A-return, and intangible-classification gaps retained (`:60-71`). |
| **5. Rent-capture causal chain in §7** | **PASS** | Section 7 retains `attachment/retention → transaction routing & take rate → Services gross profit → organic NI/OCF → buyback-supported EPS` (`:80-87`). |
| **6. 75.62% claim-site lineage** | **PASS** | The claim site retains both inputs, formula, exact result, accession, filing date, derived/reported-basis label, and tariff/operating-margin limitations (`:46-47`). |
| **7. Value-trap INCONCLUSIVE** | **PASS** | The detector remains **INCONCLUSIVE** because the synchronized series, lookback, and current observation are unavailable; narrative lean remains expressly rejected (`:52-58`). |

## Independent arithmetic re-performance

| Check | Re-performance | PASS/FAIL |
|---|---|---|
| **A1. FY25 Services share of gross profit** | `82,314 / 195,201 = 42.168841%`, which rounds to **42.2%** at the essay’s one-decimal precision | **PASS** |
| **A2. Q3 FY26 Services gross margin** | `(30,739 − 7,494) / 30,739 = 75.620547%`, which rounds to **75.62%** | **PASS** |
| **A3. FY25 FCF/NI** | `(111,482 − 12,715) / 112,010 = 88.176948%`, which rounds to **88.18%** | **PASS** |

## Minor finding (non-blocking)

- **M1 — stale version label:** the header still says `**Version:** v2` (`main-deep-analysis-essay.md:6`), while the footer identifies the corrected artifact as v3 (`:106`). Correct the header to v3 before the Founder gate so the artifact’s internal version identity is consistent. This metadata defect does not reverse item 8’s substantive PASS or any regression/arithmetic result, but it should not be carried into exact-version/hash approval.

## Final verdict

# **CLEAN WITH MINORS**

Item 8 is substantively disposed: unresolved rent-capture erosion is now a binding condition on any attractive-investment finding; price is no longer the sole gap; no unsupported quantitative condition was introduced. Prior items 1–7 and all three arithmetic checks remain PASS. The only finding is the non-substantive v2/v3 header/footer mismatch.

## Publication gate

# **READY**

There are no FAILs and therefore no publication blocker under the stated strict rule. Apply M1 before the Founder exact-version/hash gate; no further substantive re-audit is required if that edit is limited to the version label.
