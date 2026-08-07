# Independent Publication Audit — Apple Leadership Transition Follow-up + CRO Opposing Essay

**Audit date:** 2026-08-07  
**Auditor:** Independent Auditor (IIP research organization)  
**Artifacts audited (read-only):**

1. `reports/apple-leadership-transition-2026-08-07.md` (MAIN)
2. `reports/apple-leadership-transition-opposing-2026-08-07.md` (CRO OPPOSING)

**Evidence inspected:** `research/companies/AAPL/evidence-log.md` (especially §§1, 2, 6, 6c, 6d, 6e, 7, 10); `research/companies/AAPL/source-inventory.md`; `reports/apple-moat-2026-08-06.md`; `reports/apple-services-margin-verification-2026-08-06.md`; `reports/README.md`; Constitution §23.8.1 and §23.9.

## Verdict: MAJOR FINDINGS

The drafts are **not publication-ready**. All arithmetic that could be re-performed from retained raw inputs recomputed correctly at the stated precision; no contradictory or arithmetically fabricated numerical value was found. Publication is nevertheless blocked by (i) an unsupported change-condition disposition, (ii) material mischaracterization of the main note in the CRO essay, (iii) derived figures that cannot be independently re-performed from the retained evidence packet, and (iv) unsupported causal/actor attributions. Corrections and re-audit are required.

## Findings

### F1 — MAJOR — MAIN — §6 change-condition table, “Normalized product-margin erosion” (lines 72; related discussion lines 57, 61, 80)

**What is wrong:** The draft marks the condition **“Partially triggered, cause = memory”** from total-company gross-margin guidance of 47–48%. That evidence does not disclose **Products** gross margin, does not isolate mix, and does not produce a normalized margin. The prior Services-margin verification note also establishes that the tariff-refund allocation between Products and Services is unknown. Accordingly, the draft cannot infer either normalized product-margin erosion or its cause from company-level guidance. Memory pressure is an observed risk/input; the claimed product-margin disposition is not established.

**Exact correction:** Replace the status with: **“Indeterminate / monitoring signal live — September company gross-margin guidance is 47–48% including ~1pp tariff-refund benefit, but Apple did not disclose guided Products gross margin, mix, or refund allocation; normalized product-margin erosion cannot be tested from this evidence.”** In §§5 and 7, describe memory as management's disclosed pressure mechanism, not as a measured cause of normalized Products-margin erosion.

### F2 — MAJOR — CRO OPPOSING — conclusion and verdict (lines 55–57)

**What is wrong:** The essay attributes a **“continuity-preserving, no moat change”** conclusion to the main note and says the main treats durability as “unchanged.” The main does not make that claim: its actual language is **“continuity-preserving on disclosed evidence, but it is not a no-op,”** calls the omission a genuine governance gap, and adds a new leadership monitoring condition. This is a material strawman of the companion artifact.

**Exact correction:** Quote the main note accurately and frame the disagreement as one of **weight and forward risk**, e.g.: **“The main note concludes that the transition is continuity-preserving on disclosed evidence but not a no-op; this essay disagrees with the reassuring weight assigned to continuity and argues that continuity itself may increase adaptation risk.”** Remove “no moat change” and “unchanged” unless clearly labeled as the CRO's inference rather than the main note's stated conclusion.

### F3 — MAJOR — BOTH — derived-figure reproducibility (MAIN lines 38–40, 68, 74; CRO line 49)

**What is wrong:** Several material y/y or margin figures are stated in the evidence log only as completed percentages, without both raw inputs needed for independent re-performance. The retained packet lacks the comparator/raw cost input for: Q1 FY26 iPhone +23.3%; Q2 FY26 iPhone +21.7%; Q2 FY26 Greater China +28.1%; Q3 FY26 Greater China +22.4%; and Q1 FY26 Services GM 76.52%. The drafts cite named filings, but under the audit's evidence-log source-of-truth and deterministic-reperformance rule, these values are **not independently cleared**. Q2 Services GM is reproducible; Q3 FY26/FY25 Services GM is reproducible from the prior verification note.

**Exact correction:** Before publication, add each missing raw numerator and comparator/denominator to the retained evidence log and show the claim-level formula (or remove the percentage). Minimum forms: `(current/prior − 1) × 100` for y/y values and `(Services sales − Services cost of sales)/Services sales × 100` for Q1 Services GM. Re-run the audit after the evidence packet is complete.

### F4 — MAJOR — MAIN — §3 China risk re-test (line 40)

**What is wrong:** The sentence that three quarters of >22% China growth are **“a longer rebound than one product cycle would alone explain”** is not supported by a defined product-cycle duration, launch cohort, unit evidence, or causal test. It overstates what the three revenue-growth observations establish and conflicts with the same paragraph's otherwise appropriate conclusion that structural reversal remains unproven.

**Exact correction:** Replace with: **“Three consecutive quarters of >22% Greater China growth establish a sustained FY26 rebound, but this evidence does not distinguish product-cycle effects from structural reversal; the full-year re-test remains pending.”**

### F5 — MAJOR — CRO OPPOSING — succession/capital-allocation discussion (line 29)

**What is wrong:** **“the board calls it seamless”** is an unsupported actor attribution. Neither the evidence log nor source inventory records an Apple board statement using “seamless.” The essay may characterize the succession as seamless as its own analytical framing, but it may not attribute that characterization to the board without a named, dated source.

**Exact correction:** Replace with **“the transition may appear seamless”** or provide a named and dated board/issuer source that uses that characterization.

### F6 — MINOR — MAIN — §5 guidance (line 56)

**What is wrong:** The draft calls FX a **“−2.5pp sequential headwind.”** The retained evidence records “FX −2.5pp headwind” but does not support the added word “sequential” or define a sequential comparison basis.

**Exact correction:** Delete “sequential,” leaving **“FX −2.5pp headwind,”** unless the transcript is re-checked and the exact comparison basis is added.

### F7 — MINOR — MAIN — §5 memory discussion (line 58)

**What is wrong:** **“iPhone prices raised ‘reluctantly’ on iPad/Mac”** is internally malformed and appears to conflate the product named with the products on which prices were changed.

**Exact correction:** Use **“prices were raised ‘reluctantly’ on iPad and Mac”** if that exact product attribution is confirmed against the transcript; otherwise state only that management discussed selective price increases and cite the transcript without a verbatim quote.

### F8 — MINOR — CRO OPPOSING — frontmatter (lines 1–9)

**What is wrong:** The frontmatter omits the required `updated` field from the `reports/README.md` contract.

**Exact correction:** Add `updated: 2026-08-07` between `status` and `summary` (or the actual correction date if revised later).

## Re-performed arithmetic

All results below were independently recalculated from raw inputs retained in the evidence log or, for Q3 Services margins, the named prior verification note. “Match” means the draft's stated precision is reproduced.

| Metric / claim | Inputs | Formula | Independent result | Draft figure | Match? |
|---|---:|---|---:|---:|---|
| FY25 iPhone revenue share | 209,586; 416,161 | `209,586 / 416,161` | 50.3618% | 50.4% | Yes |
| FY25 Services revenue share | 109,158; 416,161 | `109,158 / 416,161` | 26.2298% | 26.2% | Yes |
| FY25 Services gross-profit share | 82,314; 195,201 | `82,314 / 195,201` | 42.1688% | 42.2% | Yes |
| FY25 Services gross margin | 82,314; 109,158 | `82,314 / 109,158` | 75.4081% | 75.4% | Yes |
| FY21–FY25 cash repurchases | 85,971; 89,402; 77,550; 94,949; 90,711 | sum | $438,583M | ~$438.6B | Yes |
| FY21→FY25 period-end share decline (rounded evidence-log endpoints) | 16.43B; 14.77B | `(14.77 / 16.43 − 1) × 100` | −10.1035% | −10.1% | Yes |
| FY25 repurchases / OCF | 90,711; 111,482 | `90,711 / 111,482` | 81.3683% | 81.4% | Yes |
| Q1 FY26 revenue y/y | 143,756; 124,300 | `(143,756 / 124,300 − 1) × 100` | 15.6525% | 15.7% | Yes |
| Q1 Greater China y/y | 25,526; 18,513 | `(25,526 / 18,513 − 1) × 100` | 37.8815% | 37.9% | Yes |
| Q1 Services y/y | 30,013; 26,340 | `(30,013 / 26,340 − 1) × 100` | 13.9446% | 13.9% | Yes |
| Q1 company GM | 69,231; 143,756 | `69,231 / 143,756` | 48.1587% | 48.2% | Yes |
| Q1 net income y/y | 42,097; 36,330 | `(42,097 / 36,330 − 1) × 100` | 15.8739% | 15.9% | Yes |
| Q1 R&D y/y | 10,887; 8,268 | `(10,887 / 8,268 − 1) × 100` | 31.6763% | 31.7% | Yes |
| Q2 FY26 revenue y/y | 111,184; 95,359 | `(111,184 / 95,359 − 1) × 100` | 16.5952% | 16.6% | Yes |
| Q2 Services y/y | 30,976; 26,645 | `(30,976 / 26,645 − 1) × 100` | 16.2545% | 16.3% | Yes |
| Q2 company GM | 54,781; 111,184 | `54,781 / 111,184` | 49.2706% | 49.3% | Yes |
| Six-month FY26 revenue y/y | 254,940; 219,659 | `(254,940 / 219,659 − 1) × 100` | 16.0617% | 16.1% | Yes |
| Q2 R&D y/y | 11,419; 8,550 | `(11,419 / 8,550 − 1) × 100` | 33.5556% | 33.6% | Yes |
| FY25 R&D y/y | 34,550; 31,370 | `(34,550 / 31,370 − 1) × 100` | 10.1371% | 10.1% | Yes |
| Q2 Services GM | sales 30,976; cost 7,224 | `(30,976 − 7,224) / 30,976` | 76.6787% | 76.68% | Yes |
| Q3 FY26 Services GM | sales 30,739; cost 7,494 | `(30,739 − 7,494) / 30,739` | 75.6205% | 75.62% | Yes |
| Q3 FY25 Services GM | sales 27,423; cost 6,698 | `(27,423 − 6,698) / 27,423` | 75.5752% | 75.58% | Yes |
| Q3 FY26 revenue y/y | 109,417; 94,036 | `(109,417 / 94,036 − 1) × 100` | 16.3565% | 16.4% | Yes |
| Q3 company GM | 54,770; 109,417 | `54,770 / 109,417` | 50.0562% | 50.1% | Yes |
| Q3 operating income y/y | 35,695; 28,202 | `(35,695 / 28,202 − 1) × 100` | 26.5690% | 26.6% | Yes |
| Q3 diluted EPS y/y | 2.02; 1.57 | `(2.02 / 1.57 − 1) × 100` | 28.6624% | 28.7% | Yes |
| Guide midpoint vs Q3 reported GM | 50.1%; 47.5% | `50.1 − 47.5` | 2.6pp | 2.6pp | Yes |
| Guide range vs Q3 reported GM | 50.1%; 48.0%/47.0% | `50.1 − 48.0`; `50.1 − 47.0` | 2.1–3.1pp | 2.1–3.1pp | Yes |
| Q3 approximate ex-refund GM | 50.1%; ~2.0pp | `50.1 − 2.0` | ~48.1% | ~48.1% | Yes, approximate |
| Guide-midpoint approximate ex-refund GM | 47.5%; ~1.0pp | `47.5 − 1.0` | ~46.5% | ~46.5% | Yes, approximate |
| Approximate adjusted sequential decline | 48.1%; 46.5% | `48.1 − 46.5` | ~1.6pp | ~1.6pp | Yes, approximate |

### Figures not independently re-performable from retained raw inputs

| Draft figure | Retained evidence state | Audit disposition |
|---|---|---|
| Q1 iPhone +23.3% | Current value and completed percentage retained; prior-period value absent | Not cleared; add raw comparator + formula |
| Q2 iPhone +21.7% | Current value and completed percentage retained; prior-period value absent | Not cleared; add raw comparator + formula |
| Q2 Greater China +28.1% | Current value and completed percentage retained; prior-period value absent | Not cleared; add raw comparator + formula |
| Q3 Greater China +22.4% | Completed percentage retained; raw current/prior pair absent from evidence-log table | Not cleared; add raw pair + formula |
| Q1 Services GM 76.52% | Completed percentage retained; Q1 Services cost-of-sales input absent | Not cleared; add cost input + formula |

Third-party IDC/Counterpoint market-share percentages and management-stated transcript figures were checked as source-attributed observations against evidence-log §§6e/10; they are not presented as Apple-filed values and were not reverse-engineered as if they were filing calculations.

## Change-condition table verification

| Condition | Draft status | Audit result |
|---|---|---|
| Sustained iPhone weakness with decelerating Services | Not triggered | Consistent with retained quarterly growth observations; some iPhone y/y inputs require evidence-log completion under F3 |
| Services GM compression | Not triggered | Supported at the Q3 y/y endpoint: 75.6205% vs 75.5752%; Q1 76.52% remains unreproducible from retained inputs |
| Installed-base language no longer claiming records | Not triggered | Supported by Q1/Q3 management-stated 2.5B+ and all-time-high language |
| Commerce initiated through third-party assistants | Not observed | Consistent with bounded evidence set |
| External models without Apple-controlled identity/payments | Not observed | Consistent with bounded evidence set; not proof of absence outside the packet |
| Normalized product-margin erosion | Partially triggered | **Not supported; must be “Indeterminate / monitoring signal live” (F1)** |
| EPS outgrowing OI purely on share reduction | Not triggered | Supported: OI itself grew 26.569%; EPS grew 28.662%; the quarter is not a share-count-only earnings story |
| Renewed China underperformance despite launches | Not triggered | Directionally supported by three positive growth observations; Q2/Q3 raw comparator inputs must be retained under F3 |

## Chronology integrity

**PASS.** Both drafts correctly place the succession announcement on **2026-04-30**, Cook's final call on **2026-07-30**, and the expected effective transition around **2026-09-01**. The original moat report was published **2026-08-06**, more than three months **after** the announcement. The main draft explicitly states that the governance event was public before publication and treats the omission as a genuine gap. Neither draft claims that the moat report predates the announcement.

## Source, fabrication, and structure checks

- **Numerical fabrication:** No computable material number contradicted its retained source inputs. Five completed percentages remain unverified because the evidence packet lacks raw inputs (F3); this is an evidence-control failure, not affirmative proof that the values are false.
- **Unsupported non-numeric claims:** The main's “longer than one product cycle would alone explain” (F4) and CRO's “the board calls it seamless” (F5) are not supported by the retained evidence.
- **Transcript caveat:** PASS in both drafts. Both identify AlphaStreet as third-party/as-transcribed and require verification against Apple's official audio/recording or a filed disclosure before verbatim use.
- **Portfolio-blind/advisory framing:** PASS in both drafts. Neither includes valuation, price target, buy/sell advice, allocation advice, or portfolio-aware reasoning. The CRO expressly excludes each category; the main says advisory/not a recommendation and portfolio-blind.
- **Frontmatter contract:** MAIN passes all required fields. CRO passes title/type/subject/date/author/status/summary but fails the required `updated` field (F8).
- **Companion-content integrity:** The main does not incorrectly summarize CRO content; it merely identifies a companion dissent. The CRO is a coherent standalone alternative causal thesis with exposed control points, 1/2–3/4–5-year mechanism, counterevidence, and falsification. Its final framing nevertheless misstates the main note and must be corrected under F2.

## Final recommendation

**Corrections required; re-audit required.** Do not publish either draft as-is. Correct F1–F8, complete the missing raw evidence inputs and formulas, then dispatch a bounded re-audit covering the corrected passages, arithmetic lineage, frontmatter, and cross-companion characterization. The two draft reports were not modified by this audit.
