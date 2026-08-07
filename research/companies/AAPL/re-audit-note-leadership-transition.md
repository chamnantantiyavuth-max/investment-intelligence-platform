# Bounded Re-Audit — Apple Leadership Transition Follow-up + CRO Opposing Essay

**Re-audit date:** 2026-08-07  
**Scope:** F1–F8 corrections only, plus the prior audit's required re-checks for frontmatter, portfolio-blind/advisory framing, and transcript caveat. No settled issue was reopened except where necessary to verify a corrected claim site.  
**Artifacts reviewed read-only:**

1. `reports/apple-leadership-transition-2026-08-07.md` (MAIN)
2. `reports/apple-leadership-transition-opposing-2026-08-07.md` (CRO OPPOSING)
3. `research/companies/AAPL/evidence-log.md`
4. `research/companies/AAPL/audit-note-leadership-transition.md`
5. `research/companies/AAPL/CORRECTIONS-RECORD.md`
6. `reports/README.md`

## Verdict: REMAINS BLOCKED

Seven findings are corrected. **F3 remains partially unresolved** because the MAIN draft's §6 Services-GM change-condition claim states `derived Q1 76.52%` without the required claim-level formula. The raw inputs and formula are now retained in evidence-log §6c, and the arithmetic recomputes correctly, but the prior audit's exact correction required the formula at the draft claim site. This is a residual of the prior MAJOR finding, not a new scope expansion.

## Per-finding confirmation

| Finding | Result | Bounded re-audit evidence |
|---|---|---|
| F1 | PASS | MAIN §5 identifies memory as management's disclosed pressure mechanism and explicitly says normalized product-margin erosion cannot be tested; §6 changes the disposition to **“Indeterminate / monitoring signal live”**; §7 retains the indeterminate conclusion rather than assigning memory as a measured Products-margin cause. |
| F2 | PASS | CRO summary and conclusion accurately characterize the MAIN as **“continuity-preserving on disclosed evidence but not a no-op”** and frame disagreement around reassuring weight and forward adaptation risk. The remaining “largely unchanged” wording is expressly qualified as **“In this essay's reading”**, not attributed as the MAIN's stated conclusion. |
| F3 | FAIL | Evidence-log §§6/6c/6d now retain all six required raw input sets, and every recomputation matches. MAIN §3 supplies formulas for Q1/Q2 iPhone and Q1/Q2/Q3 Greater China. CRO supplies claim-level formulas for its affected Greater China claims. However, MAIN §6 states **“derived Q1 76.52%”** without `(30,013 − 7,047) / 30,013`; citing evidence-log §6c does not satisfy the required claim-level-formula correction. |
| F4 | PASS | MAIN §3 now says the three quarters establish a sustained FY26 rebound but do not distinguish product-cycle effects from structural reversal; the full-year re-test remains pending. The unsupported product-cycle-duration inference is gone. |
| F5 | PASS | CRO now says the transition **“may appear seamless in the company's framing”** and labels it scenario inference; the unsupported “board calls it seamless” attribution is gone. |
| F6 | PASS | MAIN §5 reads **“FX −2.5pp headwind”**; “sequential” has been removed from that FX statement. |
| F7 | PASS | MAIN §5 accurately names the affected products: **“prices were raised ‘reluctantly’ on iPad and Mac.”** |
| F8 | PASS | CRO frontmatter includes `updated: 2026-08-07`. |

## F3 arithmetic re-performance

| Input pair | Formula | Independent result | Draft % | Match? |
|---|---|---:|---:|---|
| Q1 iPhone: 85,269 vs 69,138 | `(85,269 / 69,138 − 1) × 100` | 23.3315976742% → **23.3%** | 23.3% | Yes |
| Q2 iPhone: 56,994 vs 46,841 | `(56,994 / 46,841 − 1) × 100` | 21.6754552636% → **21.7%** | 21.7% | Yes |
| Q1 Greater China: 25,526 vs 18,513 | `(25,526 / 18,513 − 1) × 100` | 37.8814886836% → **37.9%** | 37.9% | Yes |
| Q2 Greater China: 20,497 vs 16,002 | `(20,497 / 16,002 − 1) × 100` | 28.0902387202% → **28.1%** | 28.1% | Yes |
| Q3 Greater China: 18,816 vs 15,369 | `(18,816 / 15,369 − 1) × 100` | 22.4282646887% → **22.4%** | 22.4% | Yes |
| Q1 Services GM: sales 30,013; cost 7,047 | `((30,013 − 7,047) / 30,013) × 100` | 76.5201745910% → **76.52%** | 76.52% | Yes |

## Required re-checks

| Re-check | Result | Evidence |
|---|---|---|
| Frontmatter contract — MAIN | PASS | `title`, `type`, `subject`, `date`, `author`, `status`, `updated`, and `summary` are present. |
| Frontmatter contract — CRO | PASS | `title`, `type`, `subject`, `date`, `author`, `status`, `updated`, and `summary` are present. |
| Portfolio-blind/advisory framing | PASS | MAIN identifies itself as advisory, not a recommendation, and portfolio-blind. CRO is advisory and portfolio-blind and excludes valuation, price target, buy/sell advice, and portfolio action. |
| Transcript caveat | PASS | Both drafts identify AlphaStreet/transcript material as third-party or as-transcribed and require checking against Apple's official recording/audio or filed disclosure before publication/verbatim use. |

## New material findings

**None.** The blocking point is the uncompleted claim-site portion of prior finding F3. No new publication-blocking issue was identified within this bounded re-audit.

## Final recommendation

**REMAINS BLOCKED.** Add the Q1 Services gross-margin formula at the MAIN §6 claim site—for example, `derived Q1 76.52% = (30,013 − 7,047) / 30,013`—without changing the result. Then run a narrowly bounded confirmation of F3 only. Do not advance the two drafts to Founder Review until that residual correction passes.

---

## Final Targeted Confirmation — F3 Residual

**Verdict: CLEARED FOR FOUNDER REVIEW**

| Services GM claim | Formula | Recomputed % | Draft % | Match? |
|---|---|---:|---:|---|
| Q3 FY26 | `(30,739 − 7,494) / 30,739` | 75.620547187612% → **75.62%** | 75.62% | Yes |
| Q3 FY25 | `(27,423 − 6,698) / 27,423` | 75.575247055391% → **75.58%** | 75.58% | Yes |
| Q1 FY26 | `(30,013 − 7,047) / 30,013` | 76.520174591011% → **76.52%** | 76.52% | Yes |
| Q2 FY26 | `(30,976 − 7,224) / 30,976` | 76.678719008264% → **76.68%** | 76.68% | Yes |

The MAIN §6 change-condition table now carries all four claim-level formulas, and each independently recomputed percentage matches the stated draft percentage at two decimal places. No other items were re-opened.

**Final recommendation:** The sole F3 residual is resolved; advance the Apple leadership-transition follow-up note to Founder Review.
