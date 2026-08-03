# CRR-2026-0001 — Independent Challenge Review: Microsoft Corporation (MSFT)

## 1. Verdict: FAIL

The draft cannot proceed to Founder Review in its present form. The core SEC-reported operating figures are mostly accurate, but the executor's `PASS` claims for deterministic calculation, unsupported-claim, accounting-red-flag, stale-source, per-share, permanent-loss, and thesis-falsification gates do not survive independent re-performance. Most importantly, the owner-earnings calculation double-counts stock-based compensation, the FY2023 ROIC calculation uses the wrong effective tax rate, a material OpenAI/RPO statement conflates two different disclosures, and the off-balance-sheet commitment review omits highly material lease and purchase commitments.

This verdict is advisory to the Founder. Reviewer agreement is **not** Founder approval, and `FAIL` returns the artifact to the executor under `CIW-QUALITY-GATES.md` §2/§6.

## 2. Independence and provenance disclosure

- **Executor disclosed by the draft:** Parent agent, DeepSeek V4 Flash, main session.
- **Independent reviewer:** Hermes Agent subagent, `gpt-5.6-sol` via `openai-codex`, in a separate delegated context. I did not participate in drafting `research-draft.md` and approached the review from a hostile/skeptical stance.
- **Method:** I read the governing CIW contracts, approved request, source map, and draft, then fetched the primary-source response bodies directly over HTTP (SEC request used an identifying User-Agent), parsed the SEC HTML/XBRL and Microsoft DOCX, searched the underlying passages, and independently recomputed FCF, ROIC, owner earnings, P/E, and approximate enterprise value. I did not rely solely on the writer's summaries. Source bodies were inspected in memory and were not added to the repository.
- **Direct sources independently fetched and inspected (HTTP 200):**
  - **IR-SEC26-10K:** Microsoft FY2026 Form 10-K, accession `0001193125-26-323660`, `msft-20260630.htm` (8,585,501 bytes): MD&A, financial statements, Notes 12, 13 and 18, OpenAI related-party disclosure, commitments and contingencies.
  - **IR-SEC26-PR:** FY2026 Q4 earnings release, 8-K Exhibit 99.1, accession `0001193125-26-323632`, `msft-ex99_1.htm` (901,600 bytes).
  - **IR-XBRL:** SEC company facts, CIK `0000789019` (4,881,196 bytes): annual facts and instant balance-sheet facts used for independent calculations.
  - **IR-SEC25-10K:** Microsoft FY2025 Form 10-K, accession `0000950170-25-100235`, `msft-20250630.htm` (8,158,067 bytes): historical financial, tax, debt, cash, and lease values.
  - **IR-DEF14A:** 2025 DEF 14A, accession `0001193125-25-245150`, `d908201ddef14a.htm` (2,430,412 bytes): Summary Compensation Table and compensation/governance provisions.
  - **IR-Q4-TRANSCRIPT:** Microsoft FY2026 Q4 earnings call transcript, direct Microsoft download `TranscriptQandAFY26q4.docx` (386,105 bytes): RPO/OpenAI discussion, capex and cash-paid-for-PP&E distinction, useful-life change, and outlook.
  - **IR-MKT:** Yahoo Finance chart API response for MSFT daily history (market source, not SEC primary): 2026-07-31 unadjusted/adjusted close `$464.720001`.
- **Repository mutation:** only this `challenge-review.md` was created. No draft, contract, source-map, code, or other repository file was edited.

### Evidence references used below

- **[IR-SEC26-10K MD&A/Statements]** <https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm>
- **[IR-SEC26-PR]** <https://www.sec.gov/Archives/edgar/data/789019/000119312526323632/msft-ex99_1.htm>
- **[IR-XBRL]** <https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json>
- **[IR-SEC25-10K]** <https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm>
- **[IR-DEF14A]** <https://www.sec.gov/Archives/edgar/data/789019/000119312525245150/d908201ddef14a.htm>
- **[IR-Q4-TRANSCRIPT]** <https://www.microsoft.com/en-us/investor/earnings/FY-2026-Q4/Document/DownloadDocument/37/TranscriptQandAFY26q4.docx>

## 3. Material findings

### F1 — Owner earnings double-count stock-based compensation

- **Finding:** Module G starts from GAAP net income, adds `$38.534B` of “depreciation, amortization, and other,” and then subtracts `$12.405B` of SBC. SBC is already an expense in GAAP net income and is separately shown in the cash-flow reconciliation; subtracting it again double-counts the economic cost. This conflicts with RESEARCH-FRAMEWORK §3: recurring economic costs should be subtracted when they were **excluded** from reported earnings, not when already included.
- **Evidence:** The FY2026 cash-flow statement shows net income `$133.749B`, “Depreciation, amortization, and other” `$38.534B`, and “Stock-based compensation expense” `$12.405B` as separate reconciliation lines. [IR-SEC26-10K Statements; IR-XBRL]
- **Independent verification:** Recomputed from the filed values and diluted shares `7.453B`. Holding the draft's maintenance-capex assumptions constant, the provisional NI-based cases are:
  - low: `133.749 + 38.534 − 115.948 = $56.335B` (`$7.56/share`), not `$43.9B`;
  - base: `133.749 + 38.534 − 0.60×115.948 = $102.714B` (`$13.78/share`), not `$90.3B`;
  - high: `133.749 + 38.534 − 38.534 = $133.749B` (`$17.95/share`), not `$121.3B`.
  The executor must also substantiate how much of “and other” is a genuine add-back.
- **Material impact:** The error understates each case by `$12.405B`, corrupts OE/share and P/OE, and invalidates the deterministic-calculation, valuation-assumption, and per-share gate passes. Corrected base/high P/OE at `$464.72` are approximately `33.7×/25.9×`, not `38×/28.5×`.
- **Smallest correction:** Remove the second SBC subtraction (or start from a cash-flow measure and reconcile consistently), decompose the `$38.534B` add-back, recompute all cases/per-share multiples, and update every dependent conclusion.

### F2 — FY2023 ROIC uses the wrong effective tax rate; the lease treatment is not fully specified

- **Finding:** Calculation lineage states FY2023 ETR `14.2%` and reports FY2023 ROIC about `54%`. The filed FY2023 provision was `$16.950B` on `$89.311B` pretax income, an ETR of `18.98%`. Under the draft's own beginning-IC formula, FY2023 ROIC is about `51.16%`, not `54%`.
- **Evidence:** FY2025 10-K comparative statements report FY2023 pretax income `$89.311B` and tax provision `$16.950B`. Company facts provide beginning invested-capital components totaling `$140.185B`. [IR-SEC25-10K Statements; IR-XBRL]
- **Independent verification:** Reperformed the complete series under the stated formula: FY2022 `77.13%`, FY2023 `51.16%`, FY2024 `51.31%`, FY2025 `37.27%`, FY2026 `34.65%`. The FY2026 endpoint is supported; the FY2023 value and lineage are not. In addition, operating lease liabilities are capitalized in the denominator without a stated operating-lease interest adjustment to NOPAT, so the metric convention is incomplete.
- **Material impact:** The overall declining-return conclusion survives, but the claimed rerunnable calculation does not. The error is direct evidence that the deterministic gate was not actually re-performed correctly.
- **Smallest correction:** Replace the FY2023 ETR/ROIC, publish the annual component table, and state/justify the operating-lease numerator adjustment convention.

### F3 — “~90% ex-OpenAI” is attached to the wrong metric

- **Finding:** Module A says commercial RPO was `$678B` (`+84%`, “`~90% ex-OpenAI`”). The transcript does **not** say 90% of RPO is ex-OpenAI. It says RPO grew `25%` excluding OpenAI, while **full-year Microsoft Cloud revenue** was over `$214B`, with nearly `90%` from customers outside frontier-model companies.
- **Evidence:** The Q4 transcript states: commercial RPO grew `84%` to `$678B`; RPO increased `25%` excluding OpenAI; weighted-average duration was `2.3 years`; roughly `30%` is expected within 12 months. The next sentence states nearly `90%` of Microsoft Cloud revenue came from outside frontier-model companies. [IR-Q4-TRANSCRIPT; IR-SEC26-10K Note 12]
- **Independent verification:** Read the adjacent transcript sentences and the 10-K RPO note directly.
- **Material impact:** The conflation materially overstates diversification of contracted backlog and weakens the draft's treatment of OpenAI concentration. This is especially important because the 10-K separately reports `$24.1B` of related-party revenue from OpenAI.
- **Smallest correction:** Delete “~90% ex-OpenAI” from the RPO statement; attach it only to Microsoft Cloud revenue, and state that the percentage of total RPO attributable to OpenAI was not established by the cited passage.

### F4 — Moat “evidence” largely confirms the canonical label with management scale/adoption indicators

- **Finding:** Module C labels switching costs and network effects “evidenced,” but the cited facts are installed base, bundling, RPO duration, GitHub user counts, Fortune 500 adoption, and datacenter economies of scale. Those facts show scale, adoption, contractual visibility, and possible lock-in; they do not directly measure switching cost, churn, customer surplus, cross-side network effects, or replicability. “Datacenter economies of scale” are not themselves network effects.
- **Evidence:** The 10-K and transcript support the cited adoption and scale figures, but they are management/issuer disclosures. No customer cohort, churn, competitive win/loss, migration-cost, competitor filing, or independent customer evidence is offered. [IR-SEC26-10K Item 1/MD&A; IR-Q4-TRANSCRIPT]
- **Independent verification:** Compared each asserted mechanism with the exact primary-source fact used to support it and applied RESEARCH-FRAMEWORK §3's distinction discipline.
- **Material impact:** The primary research question is moat durability. Calling indirect first-party indicators proof, after starting from a canonical “Wide/Deep/Widening” classification, creates the exact confirmation-bias risk the challenge is meant to expose and invalidates the unsupported-claim gate pass for this central conclusion.
- **Smallest correction:** Recast these as “issuer-reported indicators consistent with the moat hypothesis,” distinguish scale economies from network effects, identify missing disconfirming evidence, and temper “widening” to an initial-depth hypothesis without altering the canonical Phase 8 label.

### F5 — The off-balance-sheet/commitment review omits the largest disclosed obligations

- **Finding:** Module F discusses recognized lease liabilities (`$66.594B` finance; `$21.925B` operating) but omits the 10-K's much larger contractual-obligation and not-yet-commenced lease disclosures while claiming the accounting-red-flag review passed.
- **Evidence:** The FY2026 10-K reports total contractual obligations of `$743.821B`, including operating and finance lease payments (including imputed interest) of `$443.506B`, purchase commitments of `$194.060B`, and construction commitments of `$34.566B`; `$241.922B` is scheduled in FY2027. Note 13 also reports `$329.1B` of additional, primarily datacenter, leases not yet commenced. The `$329.1B` may overlap the lease-payment table and must not be double-counted. [IR-SEC26-10K Liquidity/Contractual Obligations; Note 13]
- **Independent verification:** Read the contractual-obligations table and Note 13 directly and compared them with Modules F, J, K, and L.
- **Material impact:** These commitments are central to AI-capex flexibility, severe-stress resilience, private-owner economics, and the short thesis. Net cash does not eliminate fixed operating/capital commitments. Their omission makes “off-balance-sheet reviewed,” “no refinancing risk,” and the permanent-loss analysis incomplete.
- **Smallest correction:** Add the disclosed obligations with a clear overlap/non-double-counting note; reassess stress liquidity, capex flexibility, permanent-loss ranking, and the private-owner answer.

### F6 — Module J falsification conditions are arbitrary, lagging, and not tied tightly enough to the conclusion

- **Finding:** “Azure growth <10% for 2+ quarters,” “ROIC <15%,” and “Copilot seat growth negative for 4 quarters” are not derived from a source, valuation bridge, or predeclared thesis contract. A consolidated ROIC below 15% could still exceed WACC, while four quarters of negative seats could identify failure only after substantial capital has already been impaired. The conditions also omit the key ex-OpenAI/incremental-return question.
- **Evidence:** research-draft.md Module J and §7; QUALITY-GATES §2 thesis-falsification requirement. The primary sources establish current growth and demand, not these break thresholds.
- **Independent verification:** Tested whether each condition logically reverses the draft's actual conclusion (“durable business quality and competitive advantage sufficient to support current EV”). None by itself cleanly does so.
- **Material impact:** The thesis-falsification gate should not be `PASS`; the conditions may fail to detect the central failure mode and could falsely declare a break for a still-good business or too late for a bad investment.
- **Smallest correction:** Tie falsification to (a) ex-OpenAI demand/backlog and retention, (b) a reproducible incremental-return-on-AI-capital measure below the required return for a defined evidence window, and/or (c) a structural loss of platform control/bundling economics. State the minimum evidence and rationale for each threshold.

### F7 — Stress-case precision is not rerunnable and mixes CY2026 capex guidance with FY2027 scenarios

- **Finding:** Module J gives FY2027 revenue, margin, OCF/FCF and capex point ranges without a calculation bridge. It also uses “capex ~$175B” in a FY2027 scenario, while management's cited statement is explicitly **calendar-year 2026** capex expectation after lease-classification effects.
- **Evidence:** The Q4 transcript says the useful-life change shifts future datacenter leases from finance to operating leases and adjusts **calendar year 2026** capex expectation to about `$175B`; it does not guide FY2027 capex to that number. [IR-Q4-TRANSCRIPT]
- **Independent verification:** Checked the guidance wording and attempted to reproduce the Module J revenue-to-OCF/FCF bridge; no inputs/formulas are supplied.
- **Material impact:** Numerical stress conclusions are not auditable, and the deterministic-calculation/unsupported-claim gate passes are false.
- **Smallest correction:** Either provide a period-consistent, rerunnable revenue→operating income→OCF→FCF bridge with explicit assumptions, or remove unsupported numerical precision and keep the stress case qualitative.

### F8 — The stale-source gate rationale is factually false and freshness classes are absent

- **Finding:** The self-check says “All sources ≤90 days old.” The inventory itself includes the 2025 proxy and FY2021–FY2025 historical 10-Ks; several are plainly older than 90 days. Historical financial facts can validly be old for normalization, but they must be classified by purpose rather than described as fresh current evidence.
- **Evidence:** research-draft.md §1/§4; RESULT-CONTRACT §5 and QUALITY-GATES §2 require freshness/staleness discipline.
- **Independent verification:** Compared publication dates in the source inventory with the 2026-08-03 as-of date.
- **Material impact:** This is a false gate attestation. It obscures which evidence supports current narrative claims versus historical trend calculations.
- **Smallest correction:** Assign freshness classes by source/use, state that current anchors (FY2026 10-K/Q4 release/transcript) are fresh, classify older filings as historical normalization evidence, and identify any narrative reliance outside the three-year default.

## 4. RESEARCH-FRAMEWORK §7 challenge answers

### 1. Which three assumptions drive intrinsic value most? Is the draft's selection right?

The three highest-impact assumptions are: **(i)** the maintenance/growth split of AI infrastructure spend and the incremental after-tax return earned on that capital; **(ii)** sustainable, economically independent cloud/AI growth after separating OpenAI-related demand and temporary capacity pricing; and **(iii)** durable operating margins/competitive duration after depreciation, energy, inference, model and regulatory costs. The draft is directionally right to emphasize AI-capex returns and Azure/Copilot growth, but its Azure and Copilot assumptions overlap and it omits the explicit maintenance-capex/economic-life and margin assumptions that actually drive its owner-earnings spread.

### 2. Which assumption is least supported? Did the draft identify it?

The least-supported assumption is the **60% maintenance-capex base case**, including the related assertion that incremental working capital is neutral. No asset-age, replacement-cycle, useful-life, capacity-utilization, or growth/maintenance reconciliation supports 60%. The draft correctly identifies the broad “AI capex return” issue, but it does not identify the specific base-case assumption as arbitrary, and its owner-earnings formula is wrong before that assumption is even tested.

### 3. What fact would reverse the conclusion? Are Module J's falsification conditions adequate?

A reversing fact would be credible evidence that, **excluding related-party/frontier-model commitments**, Azure/AI workloads cannot earn the required return through a full capacity cycle—e.g., reproducibly sub-WACC incremental NOPAT on the AI capital cohort combined with weakening renewal/consumption—or that regulatory/platform change destroys bundling/data-gravity economics. Module J's three thresholds are not adequate for the reasons in F6: they are arbitrary, lagging, and not tightly linked to the primary conclusion.

### 4. Where could confirmation bias have entered?

It entered at the start: the canonical moat was already “Wide/Deep/Widening,” and CIW then treated issuer-reported scale, adoption and bookings as proof of switching costs/network effects. Counterevidence was listed, but the moat mechanism was not seriously tested against customer churn/migration, competitor economics, model commoditization, multi-cloud bargaining power, or regulatory remedies. The depth work therefore mostly confirmed the prior label rather than independently challenging it.

### 5. What would a skeptical short seller argue? Is the draft's argument strong enough?

A stronger short thesis is: GAAP EPS is flattered relative to economic cash generation by an unprecedented infrastructure build; FCF fell to `$66.987B` despite revenue and accounting earnings growth; the disclosed commitment stack is far larger than recognized lease liabilities; OpenAI is simultaneously a related-party revenue source, investment, and major backlog driver; and the 15→25-year life/lease-classification change lowers reported capex/depreciation optics without proving asset-level economic life. If AI models and inference commoditize, customers capture the surplus while Microsoft retains depreciation, power and lease obligations. The draft's short paragraph is not strong enough: it mentions capex and accounting optics but omits the `$743.821B` commitment table, `$329.1B` not-yet-commenced leases, related-party economic circularity, and the owner-earnings error. It is too easy to dismiss as a multiple-compression story.

### 6. What would a knowledgeable operator argue?

A knowledgeable bullish operator would stress the integrated control plane—identity, data, GitHub, M365 distribution, Azure capacity and model choice—and management's disclosed ability to slow short-lived CPU/GPU purchases if demand changes. A knowledgeable skeptical operator would add that integration is operationally hard, RPO is not consumed workload or profit, energy/interconnect/permitting constrain deployment, multi-cloud customers retain bargaining power, and model/harness layers can commoditize. The draft presents the bullish operator case but not the equally knowledgeable execution/cost/portability response.

### 7. Is the opportunity based on mispricing, uncertainty, distress, or optimistic assumptions? Is the classification supported?

**Optimistic assumptions plus genuine uncertainty** is the best-supported classification. There is no distress, and the approved scope does not establish mispricing. At `25.9×` trailing GAAP EPS, the price requires durable growth and capital productivity; the unresolved maintenance-capex and OpenAI-independent-demand questions make uncertainty central. The draft's classification is substantially supported, but “mispricing” cannot be inferred.

### 8. Would a rational private owner buy the whole company at current enterprise value? Is “borderline” honest?

Using the 2026-07-31 price, 2026-06-30 outstanding shares (`7.427B`), filed debt/cash, and recognized lease liabilities gives approximately `$3.415T` conventional EV or `$3.503T` lease-adjusted EV—not `$3.55T`, though the difference is not conclusion-changing. At that price, corrected provisional owner-earnings yields are roughly `1.6%/2.9%/3.8%` for low/base/high cases before resolving “and other” and future commitments. A private owner without a liquid exit would require strong evidence of long-duration reinvestment returns. “Borderline” is too accommodating; the honest initial-depth answer is **not demonstrated / no at the conservative and base evidence presently available**, with a possible yes only under the high-growth/high-return case.

### 9. Would the business remain desirable if markets closed for ten years?

**Probably yes as a business, not necessarily at today's purchase price.** The diversified subscription/consumption engine and `$182.935B` OCF indicate self-funding capacity. However, the answer must acknowledge the very large lease/purchase commitments and the dependence of future desirability on converting the AI build into cash returns. Market closure does not erase fixed commitments. The draft's “yes” is directionally reasonable but too unconditional.

### 10. Is expected return superior to realistic alternatives?

The draft's “not assessable under approved N–P omissions” is **correct under design §9 and CRR-2026-0001**; it is not a dodge. Module P and the required valuation/return contract were explicitly omitted. The honest consequence is that the draft cannot claim superior expected return or mispricing. Qualitative P/E commentary is not an opportunity-cost analysis.

## 5. Quality-gate spot-check results

| Gate re-run | Result | Independent result |
|---|---|---|
| Source-coverage | **PASS with limitation** | Supplied SEC/IR sources were accessible and the principal required categories exist. Regulatory proceeding mapping remains generic rather than source-specific, but this did not block the numerical checks performed here. |
| Primary-source | **PASS** | Direct SEC filings/XBRL and Microsoft transcript inspected. Yahoo used only for market close. |
| Contradiction | **FAIL** | The draft preserved its stale price reconciliation, but failed to catch its own RPO/90%-outside-frontier metric conflation and overstates “no other material conflicts.” |
| Unsupported-claim | **FAIL** | Moat mechanisms, Module J numerical ranges, and several stress/private-owner conclusions exceed the cited evidence. |
| Stale-source | **FAIL** | “All sources ≤90 days” is false; freshness classes by use are not recorded. |
| Accounting red-flag | **FAIL** | Useful-life optics are noted, but the `$743.821B` obligation table and `$329.1B` not-yet-commenced leases are omitted from the analysis. |
| Valuation-assumption | **FAIL** | Owner-earnings formula is wrong and the 60% maintenance case is unsupported. |
| Deterministic-calculation | **FAIL** | SBC is double-counted; FY2023 ETR/ROIC is wrong; stress ranges lack rerunnable lineage. |
| Per-share | **FAIL** | Filed EPS and FCF/share check, but OE/share and P/OE do not. |
| Dilution | **PASS** | Diluted shares declined from about `7.610B` FY2021 to `7.453B` FY2026; SBC remains economically material but net share count is anti-dilutive over the period. |
| Reverse-DCF | **N/A — correctly recorded** | Module N was approved as omitted; no reverse DCF should be fabricated. |
| Permanent-loss | **FAIL** | Ranked risks exist, but commitment intensity and related-party/backlog economics are not adequately incorporated. |
| Thesis-falsification | **FAIL** | Conditions exist but are not sufficiently justified or linked to the conclusion. |
| Artifact-lineage | **PASS** | Draft v0.1 and preceding request/source-map states are identifiable. |
| Authority | **PASS** | Draft remains non-authoritative; no AI publication transition is claimed. |
| Scope | **PASS** | Modules A–M initial; N–Q omissions retained; no recommendation or portfolio data used. |

### Specific numerical spot-checks

| Item | Independent result |
|---|---|
| FY2026 revenue | **Verified:** `$331.839B` (properly rounded to `$331.8B`). [IR-SEC26-10K; IR-SEC26-PR] |
| Microsoft Cloud FY2026 | **Verified:** `$214.4B`, `+27%`. [IR-SEC26-10K MD&A] |
| Commercial RPO | **Verified:** `$678B`, `+84%`; `+25%` excluding OpenAI, 2.3-year weighted average duration, ~30% expected within 12 months. The draft's “~90% ex-OpenAI” RPO phrase is wrong. [IR-SEC26-10K Note 12; IR-Q4-TRANSCRIPT] |
| Segment revenue / operating income | **Verified:** PBP `$139,996M`; IC `$137,791M`; MPC `$54,052M`; total revenue `$331,839M`; total operating income `$155,237M`. [IR-SEC26-10K Segment Results/Note 18] |
| Capex / OCF / FCF | **Verified:** additions to PP&E `$115,948M`; OCF `$182,935M`; simple FCF `$66,987M`. [IR-SEC26-10K Cash Flows; IR-XBRL] |
| ROIC | **FY2026 verified** at `34.65%` under the draft's formula. **FY2023 wrong:** `51.16%`, not ~`54%`, because filed ETR is `18.98%`, not `14.2%`. |
| Owner earnings | **Not verified:** double-counted SBC. Provisional corrected values under the same maintenance assumptions are `$56.335B / $102.714B / $133.749B`, subject to decomposing “D&A and other.” |
| Market data / P/E | **Verified:** 2026-07-31 close `$464.72`; `$464.72 / $17.95 = 25.89×`. |
| OpenAI disclosure | **Verified:** `$24.1B` FY2026 related-party revenue inclusive of revenue-sharing payments; `$6.0B` receivable; approximate `25%` as-converted interest; `$13.0B` commitments, `$11.9B` funded. [IR-SEC26-10K OpenAI related-party note] |
| Useful life / capex guidance | **Verified with period caveat:** data centers and office buildings `15→25 years`, effective FY2027; minimal FY2027 operating-income benefit; lease classification adjusts **CY2026** capex expectation to about `$175B`. [IR-Q4-TRANSCRIPT] |
| CEO compensation | **Verified:** Nadella FY2025 total `$96,496,790`, including `$84,245,496` stock awards and `$2.5M` salary; no NEO stock options in the years shown. [IR-DEF14A Summary Compensation Table] |

## 6. Required changes before re-review

1. **Correct Module G and all dependent outputs** using a consistent NI- or cash-flow-based owner-earnings formula; do not subtract SBC twice; decompose “depreciation, amortization, and other”; recompute per-share and price/OE figures.
2. **Correct ROIC lineage**, especially FY2023 ETR/ROIC, publish the annual component table, and specify the operating-lease NOPAT convention.
3. **Correct the RPO/OpenAI sentence**: `+25%` RPO growth ex-OpenAI; “nearly 90% outside frontier-model companies” applies to Microsoft Cloud revenue, not RPO.
4. **Downgrade/reframe moat assertions** from proof to issuer-supported indicators; separate scale economies from network effects and explicitly identify missing churn/customer/competitor evidence.
5. **Add the full commitment disclosure** (`$743.821B` total contractual obligations; `$443.506B` lease payments; `$194.060B` purchase commitments; `$34.566B` construction commitments; `$329.1B` not-yet-commenced leases, with overlap caution) and update F/J/K/L and the private-owner assessment.
6. **Replace or justify falsification conditions** with measurable, conclusion-linked conditions and a minimum-evidence rule, including ex-OpenAI demand and incremental AI-capital returns.
7. **Make Module J rerunnable and period-consistent** or remove unsupported numerical precision; do not relabel CY2026 capex guidance as FY2027 guidance.
8. **Correct stale-source attestation** and add freshness classifications by source purpose.
9. **Strengthen the short-seller and operator challenges** using related-party economics, commitment intensity, portability/commoditization, and economic-cash-return evidence rather than relying mainly on multiple compression.
10. **Update the self-check statuses** honestly; failed gates may not remain shown as `PASS` after corrections are pending.

## 7. Scope check

**Scope result: PASS.** The draft stayed within the approved CRR-2026-0001 boundary: Modules A–M at initial depth, portfolio-blind, no recommendation language, and no official valuation output. Modules N (valuation), O (margin of safety), P (opportunity cost), and Q (monitoring) were omitted with the approved justifications. The qualitative price-implies work in Module M and stress work in Module J are within scope, although their calculations and period labels require correction. The “expected return not assessable under N–P omissions” answer is the correct honest empty state under design §9.

---

*Independent Challenge artifact for CRR-2026-0001. Review status: FAIL. Separate-context direct-source review completed 2026-08-03. Advisory to Founder; not Founder approval.*
