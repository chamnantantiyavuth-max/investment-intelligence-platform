# Independent Data-Steward Verification — JNJ Talc-Litigation Evidence Log

**Review role:** Data Steward / independent evidence-integrity gate  
**Evidence log reviewed:** `evidence-log.md`  
**Primary files reviewed:** all eight supplied raw files in `C:\Users\Admin\AppData\Local\Temp\jnj-evidence\`  
**Supplemental primary metadata:** SEC filing-detail page for accession `0000200406-26-000155`, downloaded directly from SEC EDGAR to the same temp directory to verify filing date.

## Verdict

**Overall: PASS WITH CORRECTIONS.** The central transaction, reserve, earnings, and balance-sheet figures are supported by the primary filings. I found no invented central financial amount. I did find:

1. **One threshold error:** the open-item heading says `>95%`; the source says **at least 95%** (that is, `>=95%`).
2. **One misleading payment shorthand:** the reserve table says “none before 2028” after describing a 2027 payment. The source says **no additional payments due before 2028**.
3. **One false source-characterization:** the open item says Sail option terms/milestones are not in the exhibit beyond the headline. Exhibit 99.2 does disclose the $785M initial payments, $465M equity component, $140M contingent development payments, $2.58B option payment, and the conditional EPS effects.
4. **Two accounting-basis nuances:** FY2024 repurchases are $2,407M in the treasury-stock note but $2,432M in the cash-flow statement; H1 2026 repurchases are $4,253M including excise tax in equity but $4,249M cash in the cash-flow statement. The evidence log uses the stated treasury/equity basis and is supportable, but the basis must remain explicit.
5. **One source mis-attribution:** FY2023 repurchases of $5,054M are supported by the consolidated statement of equity, not Note 12. Note 12 reports $5,079M for FY2023.
6. **Two claims not established by the supplied period-end filings:** the assertion that the proposed $5.5B was “not yet accrued,” and the asserted $1.2B decomposition between the FY2024 reserve, reversal, and Q4 2025 reserve. These are reasonable hypotheses, but the cited sources do not prove them.

### Citation method

The supplied 8-K HTML exhibits are largely collapsed into one physical raw line. For auditable citations, I parsed only visible text from each raw HTML file into a line-numbered normalized copy in the same temp directory. Quotes below are verbatim visible filing text and cite those normalized line numbers. The 10-Q and 10-K citations refer directly to the supplied line-numbered text files. No other research role’s work was read.

---

## 1. Proposed ovarian-talc resolution — SRC-01

| Evidence-log claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Announcement was dated **July 27, 2026** | **PASS** | `8k-155-ex991-talc.htm`, normalized l.15: **“New Brunswick, N.J. – JULY 27, 2026 –”** |
| **$5.5B** commitment | **PASS** | Talc exhibit normalized l.32: **“Calls for per claim payments, with a $5.5 billion commitment by the Company…”** |
| First payment **no more than $3B in 2027** | **PASS** | Same line: **“…the first payment of no more than $3 billion to be made in 2027…”** |
| **No additional payments due before 2028** | **PASS** | Same line: **“…and no additional payments due before 2028.”** |
| Reserve-table shorthand “first payment <=$3B in 2027, **none before 2028**” | **FAIL** | The source does not say no payment before 2028; it expressly provides for the first payment in 2027. Correct wording: **“first payment of no more than $3B in 2027; no additional payments due before 2028.”** |
| Participation condition of **at least 95%** of remaining claims | **PASS** | Talc exhibit normalized l.16: **“…conditioned on… the express participation of at least 95% of the remaining claims.”** Line 30 further states: **“participation of lead plaintiff firms in all ovarian talc litigation pending in state and federal court, representing at least 95% of the remaining claims.”** |
| Open-item heading says participation threshold **`>95%`** | **FAIL** | Correct value is **`>=95%`**, not `>95%`; see normalized ll.16 and 30 above. |
| Remaining **76,000 ovarian talc claims** | **PASS** | Talc exhibit normalized l.14: **“Efficient Conclusion… Eliminates Expense Associated with Litigating Remaining 76,000 Ovarian Talc Claims.”** Scope note: the later Q2 10-Q describes approximately 76,000 U.S. plaintiffs across pending talc suits, while this post-quarter PR characterizes the resolution as covering remaining ovarian claims. The two labels should not be silently treated as identical populations. |
| July 22, 2026 show-cause order and withdrawal of **two** specific-causation experts | **PASS** | Talc exhibit normalized l.22: **“On July 22, 2026, the MDL court ordered plaintiffs to show why the remaining pending talc claims should not be dismissed for inability to prove specific causation.”** Line 24: **“The order followed plaintiffs’ withdrawal of their specific causation experts in two bellwether cases…”** |
| Company prevailed in overwhelming majority / vast majority of tried ovarian cases | **PASS** | Talc exhibit normalized l.20: **“The Company has prevailed in the overwhelming majority of ovarian cases tried to date.”** The quoted management statement at l.17 says it prevailed **“in the vast majority of cases tried to date.”** This is an issuer claim, not an independently adjudicated statistic. |
| About **95%** of filed mesothelioma suits settled; all state consumer-protection claims and talc-supplier disputes settled | **PASS** | Talc exhibit normalized l.34: **“…previously settling about 95% of filed mesothelioma lawsuits, all State consumer protection claims, and all talc-supplier disputes.”** |
| Talc powder discontinued globally in **2023**; Kenvue separated **August 2023**; JNJ retained and indemnifies U.S./Canada liabilities | **PASS** | Talc exhibit normalized l.41: **“Johnson & Johnson agreed to retain all the talc-related liabilities and indemnify Kenvue for any and all costs—arising from litigation in the United States and Canada.”** Line 43: **“…discontinue talc-based JOHNSON’S Baby Powder globally in 2023… separated its consumer health business, Kenvue, in August 2023.”** |

---

## 2. Firefly Bio and Sail Biomedicines — SRC-02

| Claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Firefly purchase price **$1B cash** | **PASS** | `8k-163-ex991-firefly.htm`, normalized l.22: **“…acquisition of Firefly Bio, Inc… for $1 billion in cash.”** |
| Firefly accounted for as an **asset acquisition**; approximately **$1B IPR&D charge in Q3 2026** | **PASS** | Firefly exhibit normalized l.30: **“The transaction will be accounted for as an asset acquisition, resulting in an in-process research and development charge of approximately $1 billion in the third quarter of 2026.”** |
| Firefly adjusted-EPS dilution **$0.46 in 2026** and **$0.08 in 2027** | **PASS** | Firefly exhibit normalized l.30: **“…dilute adjusted operational earnings per share and adjusted earnings per share by approximately $0.46 in 2026 and approximately $0.08 in 2027.”** |
| Firelink DAC / pan-KRAS / next-generation oncology characterization | **PASS** | Firefly exhibit normalized ll.14-18: **“Advance Next-Generation Oncology Innovation”; “Broadens capabilities in targeting pan-KRAS…”; “Adds novel degrader antibody conjugate platform…”** Line 22 identifies the proprietary Firelink DAC platform. |
| Sail collaboration, equity investment, exclusive option to acquire Sail for **$2.58B** | **PASS** | `8k-163-ex992-sail.htm`, normalized l.34: **“Johnson & Johnson will also make an equity investment in Sail. Additionally, Johnson & Johnson has been granted an exclusive option to acquire Sail for $2.58 billion.”** |
| Sail 2026 EPS impact **$0.18** and 2027 impact **$1.28**, conditional | **PASS** | Sail exhibit normalized l.46: **“Subject to Johnson & Johnson's decision to exercise the option… Assuming exercise of the option… dilute… by approximately $0.18 in 2026 and approximately $1.28 in 2027.”** The 8-K cover adds that the 2027 effect assumes certain development milestones and exercise of the option (`8k-163-cover.htm`, normalized l.196). |
| Open item says option terms/milestones are not in exhibit text “beyond headline” | **FAIL** | Sail exhibit normalized ll.44-46 discloses: **“total initial payments of $785 million, including a $465 million equity investment, and additional contingent payments of $140 million if certain development milestones are achieved… an additional payment of $2.58 billion.”** Detailed contractual mechanics may be absent, but the exhibit contains materially more than a headline. |

---

## 3. July 29, 2026 guidance update — SRC-02 cover

| Claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Combined Firefly + Sail 2026 adjusted-EPS impact **-$0.64 = -$0.46 + -$0.18** | **PASS** | `8k-163-cover.htm`, normalized l.134: **“…reduce… Adjusted EPS by approximately $0.64 in 2026, consisting of approximately $0.46 attributable to the Firefly acquisition and approximately $0.18 attributable to the Sail transaction.”** |
| Adjusted EPS guidance changed from **$11.60-$11.75 / $11.68 midpoint** to **$10.96-$11.11 / $11.04 midpoint** | **PASS** | Cover normalized ll.175-180: **“Adjusted EPS (diluted)… $10.96 - $11.11 / $11.04; $11.60 - $11.75 / $11.68; Decrease $0.64.”** |
| Adjusted operational EPS changed from **$11.50-$11.65 / $11.58** to **$10.86-$11.01 / $10.94** | **PASS** | Cover normalized ll.162-167: **“$10.86 - $11.01 / $10.94; $11.50 - $11.65 / $11.58; Decrease $0.64.”** |
| Adjusted pre-tax operating margin changed from **increase ~75 bps** to **decrease ~75 bps**, a **~150 bps** transaction impact | **PASS** | Cover normalized ll.157-161: **“Decrease by ~75 bps vs. prior year; Increase by ~75 bps vs. prior year; Decrease ~150 bps.”** |
| Combined 2027 impact **-$1.36 = -$0.08 Firefly + -$1.28 Sail** | **PASS** | Cover normalized l.196: **“…reduce… 2027… by approximately $1.36, consisting of approximately $0.08 attributable to the Firefly acquisition and approximately $1.28 attributable to the Sail transaction…”** It explicitly conditions Sail on milestones and option exercise. |
| Sales guidance unchanged at reported **$100.8-$101.4B / $101.1B**, **+7.3% midpoint** | **PASS** | Cover normalized ll.151-156: **“Estimated reported sales / midpoint $100.8B - $101.4B / $101.1B; Change vs. prior year / midpoint 7.0% - 7.6% / 7.3%.”** The July 15 release reports the identical range/midpoint at normalized ll.186-193. |

---

## 4. Talc reserve and MDL chronology — Q2 2026 10-Q and FY2025 10-K

| Claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Q2 2026 talc reserve **~$3.7B present value**, **~40% current** | **PASS** | `10q-20260628.txt` l.1740: **“the total present value of the reserve… is approximately $3.7 billion… Approximately 40% of the reserve is recorded as a current liability.”** |
| Q2 2026 approximately **76,000 U.S. plaintiffs** | **PASS** | 10-Q l.1737: **“As of June 28, 2026, there are approximately 76,000 plaintiffs in the United States with direct claims… in pending lawsuits…”** |
| Red River / Pecos allocation and **~$7.0B reversal in Q1 2025** | **PASS** | 10-Q l.1739: **“ovarian and other gynecological cancers were… allocated to Red River, and mesothelioma, governmental unit and certain other claims… to Pecos River… the Company reversed substantially all, or approximately $7.0 billion… in the fiscal first quarter of 2025.”** |
| LTL Chapter 11 filings in **October 2021** and **April 2023**, both dismissed; LTL became LLT in **December 2023** | **PASS** | `10k-20251228.txt` l.2757: **“filed voluntary petitions… in October 2021 and again in April 2023; both petitions were dismissed.”** Line 2758: **“In December 2023, LTL changed its state of formation to Texas and its name to LLT Management LLC.”** |
| May 2024 prepack: **$6.475B PV**, **25 years**, **~$8.0B nominal**, **4.4% discount**, **99.75%** of pending suits | **PASS** | 10-K l.2759 quotes all figures: **“…present value of approximately $6.475 billion payable over 25 years (nominal value of approximately $8.0 billion, discounted at a rate of 4.4%). The claims… constituted 99.75% of then-pending lawsuits…”** |
| August 2024 restructuring into Red River and Pecos; September 2024 Red River Chapter 11 in Southern District of Texas | **PASS** | 10-K ll.2760 and 2762: **“In August 2024… Red River… Pecos River…”** and **“In September 2024… Red River filed… with the United States Bankruptcy Court for the Southern District of Texas…”** |
| FY2024 cumulative incremental talc charge **~$5.0B**; year-end reserve **~$11.6B PV / ~$13.5B nominal** | **PASS** | 10-K l.2763: **“cumulative incremental charge of approximately $5.0 billion during fiscal year 2024… total present value… approximately $11.6 billion (or nominal value of approximately $13.5 billion).”** Nuance: MD&A l.811 reports total FY2024 talc charges of approximately **$5.1B**; the **$5.0B** figure is specifically the cumulative incremental charge for the contemplated plan. |
| March 2025 Texas dismissal; **~$7B** reversed; Q4 2025 reserve **~$3.4B**, about **one-third current** | **PASS** | 10-K l.2764: **“In March 2025… dismissing the case… reversed… approximately $7 billion… As of the fourth quarter 2025, the total present value… approximately $3.4 billion… Approximately one-third… current liability.”** |
| 2026 MDL chronology: January general-causation R&R; May hearings; withdrawal of **two** experts; June motion; July grant; August conference; July asbestos-method R&R granted in part | **PASS** | 10-Q ll.1741-1742 states each event verbatim: **“In January 2026…”; “In May 2026…”; “plaintiffs withdrew two…”; “In June 2026…”; “In July 2026, the court granted…”; “scheduled for August 2026”; “In July 2026… asbestos testing methods, granting in part…”** |
| Ingham: **$4.7B** verdict -> **$2.1B**; paid **~$2.5B including interest in June 2021** | **PASS** | 10-K l.2751: **“a July 2018 verdict of $4.7 billion… reducing… to $2.1 billion… In June 2021, the Company paid the award, which, including interest, totaled approximately $2.5 billion.”** |
| Securities class: class certification affirmed **July 2025**; cert denied **April 2026**; expert discovery proceeding | **PASS** | 10-Q l.1743: **“In July 2025, the Third Circuit affirmed… the Supreme Court denied [certiorari] in April 2026. Expert discovery is proceeding.”** |
| Imerys/Cyprus settlement order approved **October 2024**; district appeal denied **August 2025**; Third Circuit briefing complete / ruling pending | **PASS** | 10-Q l.1744 states each event: **“In October 2024… approving… Settlement Order… In August 2025, the district court denied… Briefing in the Third Circuit appeal is complete and a ruling is pending.”** |
| Opioid settlement **up to $5.0B**, about **80% paid** by FY2025; **23** state, **285** Ohio MDL, **3** other federal cases | **PASS** | 10-K ll.2778-2779: **“settle… for up to $5.0 billion. Approximately 80%… paid…”** and **“approximately 23… state courts, 285… Ohio… and 3… other federal courts.”** |
| **~$1.1B opioid reserve** | **PASS WITH WORDING NUANCE** | 10-K ll.903 and 907 say **“the remaining approximately $1.1 billion to settle opioid litigation.”** The amount is supported; the quoted liquidity section does not itself use the noun “reserve.” Prefer “remaining amount to settle opioid litigation” unless another balance-sheet note explicitly labels it a reserve. |

---

## 5. Q2 FY2026 results and pre-transaction guidance

| Claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Q2 sales **$25,310M**, **+6.6% reported**, **+5.6% operational** | **PASS** | `8k-146-ex991-q2earnings.htm`, normalized ll.30-33: **“Reported Sales $25,310; $23,743; 6.6%.”** Lines 47-49 report **“Operational Sales… 5.6%.”** The 10-Q l.295 independently reports $25,310M. |
| Q2 net earnings **$5,534M, -0.1%**; diluted EPS **$2.27, -0.9%** | **PASS** | Earnings exhibit normalized ll.34-41: **“Net Earnings $5,534; $5,537; -0.1%… EPS (diluted) $2.27; $2.29; -0.9%.”** |
| Adjusted net earnings **$7,081M**; adjusted EPS **$2.90, +4.7%** | **PASS** | Earnings exhibit normalized ll.53-62: **“Adjusted Net Earnings… $7,081… Adjusted EPS (diluted)… $2.90… 4.7%.”** |
| H1 sales **$49,372M, +8.2%** | **PASS — amount filed; growth derived** | 10-Q l.327: **“Sales to customers… $49,372… $45,636.”** Arithmetic gives `(49,372 / 45,636) - 1 = 8.19%`, rounding to **8.2%**. The 8.2% is not printed in the supplied earnings exhibit. |
| H1 net earnings **$10,769M vs $16,536M** and diluted EPS **$4.41** | **PASS** | 10-Q ll.339-343: **“Net earnings $10,769… $16,536… Diluted $4.41 $6.82.”** |
| Prior-year H1 included talc-reversal benefit | **PASS** | 10-Q l.2128: **“The fiscal six months of 2025 includes approximately $7.0 billion related to the talc reserve reversal.”** |
| FY2026 estimated reported-sales guidance **$100.8-$101.4B / $101.1B**, **+7.3% midpoint** | **PASS** | Earnings exhibit normalized ll.186-193: **“$100.8B - $101.4B / $101.1B; 7.0% - 7.6% / 7.3%.”** |
| Pre-transaction adjusted EPS guidance **$11.60-$11.75 / $11.68**, **+8.2% midpoint** | **PASS** | Earnings exhibit normalized ll.202-209: **“$11.60 - $11.75 / $11.68; 7.5% - 8.9% / 8.2%.”** |
| More than **$100B** annual revenue for first time in **140-year** history | **PASS** | Earnings exhibit normalized l.23: **“…more than $100 billion in annual revenue for the first time in our Company’s 140-year history.”** This is issuer historical characterization. |
| H1 estimated FCF **~$8,700M vs $6,214M** | **PASS** | Earnings exhibit normalized ll.63-66: **“Free Cash Flow… ~$8,700; $6,214.”** Lines 75-78 define FCF and specify that Q2 YTD 2026 is **“estimated as of July 15, 2026.”** |

---

## 6. Balance sheet, debt, dividends, repurchases, and FY2025 cash deployment

| Claim / figure | Status | Exact primary-source evidence and determination |
|---|---|---|
| Cash **$20,422M** plus marketable securities **$336M** = **$20,758M** at June 28, 2026 | **PASS** | 10-Q ll.236-237: **“Cash and cash equivalents… $20,422… Marketable securities 336.”** Lines 907-910: **“Total cash, cash equivalents and current marketable securities $20,758… 20,422… 336.”** |
| Loans/notes payable **$11,692M** plus long-term debt **$37,344M** = **$49,036M (~$49.0B)** | **PASS** | 10-Q ll.256 and 264: **“Loans and notes payable $11,692”** and **“Long-term debt… 37,344.”** The 10-Q MD&A l.2183 independently states **“debt position was $49.0 billion.”** |
| H1 2026 repurchases **$4,253M including excise tax**, versus **$2,127M** H1 2025 | **PASS WITH BASIS NOTE** | 10-Q l.419: **“Repurchase of common stock (including excise tax) (4,253).”** Prior-year equity line l.459: **“Repurchase… (2,127).”** The cash-flow statement l.534 reports $4,249M cash; the $4M difference is consistent with the explicit excise-tax-inclusive equity basis. |
| FY2025 cash + securities **$20.1B**; debt **$47.9B**; net debt **$27.8B** | **PASS** | 10-K l.814: **“Cash, cash equivalents and marketable securities totaled $20.1 billion… total debt… $47.9 billion.”** Line 903: **“net debt position was $27.8 billion… debt balance… $47.9 billion.”** |
| FY2025 repurchases **$5,953M / 33.9M shares**; FY2024 **$2,407M**; FY2023 **$5,054M** | **PASS AMOUNTS / FAIL SOURCE ATTRIBUTION FOR FY2023** | Note 12, 10-K ll.2192-2195, reports **“Repurchase of common stock 15,183 | 2,407”** for 2024 and **“33,903 | 5,953”** for 2025, supporting approximately 33.9M shares and $5,953M for 2025 and $2,407M for 2024. The consolidated statement of equity—not Note 12—reports FY2023 **$5,054M** at l.1209. Note 12 instead reports FY2023 **31,085 thousand shares / $5,079M** at l.2188. The FY2024 cash-flow statement separately reports **$2,432M** at l.1265. Therefore the three evidence-log amounts exist, but the blanket “10-K Note 12” citation is wrong for FY2023 and cash-versus-equity/treasury bases must be labeled. |
| FY2025 dividend **$5.14/share**, **63rd** consecutive annual increase | **PASS** | 10-K l.931: **“increased its dividend in 2025 for the 63rd consecutive year. Cash dividends paid were $5.14 per share…”** |
| H1 2026 dividends paid **$2.64/share** | **PASS** | 10-Q ll.416-417: **“Cash dividends paid ($2.64 per share) (6,358).”** |
| FY2025 OCF **$24.5B**; investing **-$23.6B**; financing **-$5.5B** | **PASS** | 10-K ll.865-870: **“24.5 cash generated from operating activities; (23.6) net cash used for investing activities; (5.5) net cash used for financing activities.”** Exact statements: ll.1252, 1262, and 1281 report $24,530M, -$23,588M, and -$5,539M. |
| FY2025 acquisitions **~$17.5B** | **PASS** | 10-K l.887: **“(17.5) acquisitions, net of cash acquired.”** Exact cash-flow line l.1256: **“Acquisitions, net of cash acquired… (17,541).”** |
| Intra-Cellular acquisition **~$14.5B**, closed **April 2, 2025**, funded in part by **$9.2B** senior unsecured notes issued Q1 2025 | **PASS** | 10-K l.903: **“In the fiscal first quarter of 2025… senior unsecured notes… $9.2 billion… used to fund the Intra-Cellular… acquisition for approximately $14.5 billion which closed on April 2, 2025…”** |

---

## 7. Radar-observation corrections

| Correction | Status | Exact primary-source evidence and determination |
|---|---|---|
| August 4 8-K did **not** announce a notes offering; operative items are only **Item 5.02** and **Item 9.01** | **PASS** | `8k-167-cover.htm`, normalized ll.96-132 labels the note list **“SECURITIES REGISTERED PURSUANT TO SECTION 12(b) OF THE ACT”** and lists standing note classes. The filing then contains **“Item 5.02…”** at l.133 and **“Item 9.01 Financial statements and exhibits”** at l.136, with no offering item or issuance disclosure. Lines 134-135 concern Jennifer Taubert’s retirement and the related press release. Correct conclusion: the Section 12(b) table is not evidence of a new offering. |
| The talc PR was dated **July 27, 2026** and the 8-K was filed **July 28, 2026** | **PASS** | Talc exhibit normalized l.15 dates the PR **“JULY 27, 2026.”** Supplemental SEC filing-detail page for accession 0000200406-26-000155, normalized ll.18-26: **“Filing Date 2026-07-28… Accepted 2026-07-27 20:15:31… Period of Report 2026-07-27.”** This confirms the date nuance. |
| Most recent notes offering identified in supplied evidence: **$9.2B in Q1 2025** for Intra-Cellular | **PASS** | 10-K l.1840: **“In the fiscal first quarter of 2025, the Company issued senior unsecured notes for approximately $9.2 billion. The net proceeds… used to fund the Intra-Cellular… acquisition…”** |

---

## 8. Derived figures and formulas

| Derived item | Status | Recalculation / integrity finding |
|---|---|---|
| Proposed commitment above Q2 reserve: **$5.5B - $3.7B = ~$1.8B** | **PASS** | Recalculated exactly from sourced inputs: $1.8B. This is a comparison, not a statement that the commitment and reserve have identical scope, timing, or accounting treatment. |
| Adjusted-EPS midpoint cut: **$11.68 - $11.04 = $0.64**; transaction components **$0.46 + $0.18 = $0.64** | **PASS** | Recalculation matches the 8-K’s stated $0.64 decrease. |
| H1 repurchase pace: **$4,253M / 6 = ~$709M/month**; FY2025 **$5,953M / 12 = ~$496M/month**; increase **~43%** | **PASS — arithmetic only** | Recalculated: $708.83M/month versus $496.08M/month; ratio increase 42.89%, rounding to 43%. This is not company guidance and should remain labeled as a mechanical run-rate comparison. |
| Reserve bridge: **$11.6B - $7.0B = $4.6B**, versus reported **$3.4B**, leaving **~$1.2B** | **PASS — arithmetic** | Arithmetic is correct. However, calling $4.6B “pre-reversal” is backwards; it is the simple expected **post-reversal** balance before any other movements. |
| The **~$1.2B** residual equals settlement payments / defense spend / rounding | **CANNOT-VERIFY** | The filings say the ending reserve comprises executed settlement agreements, defense, and other costs, but do not provide a line-by-line $11.6B-to-$3.4B bridge. The residual could include payments, new charges, estimate changes, timing, and rounding. Preserve only as an unexplained residual unless a roll-forward is sourced. |

---

## 9. Figures/claims not located or not provable from the cited raw sources

These are the only material items that should not be presented as established source facts:

1. **“The $5.5B is NOT yet accrued.” — CANNOT-VERIFY.** The June 28 10-Q predates the July 27 proposal; the PR calls the arrangement proposed and conditioned but does not state the accounting entry. A Q3 2026 filing or explicit company accounting disclosure is required to establish whether and when an accrual was recognized.
2. **Exact reserve-roll-forward attribution for the ~$1.2B residual — CANNOT-VERIFY.** No supplied source gives the claimed decomposition.
3. **Detailed mechanics for non-participants, participating firms, exclusivity, and state-court implementation — CANNOT-VERIFY.** The PR provides only the “at least 95%” condition and state/federal scope; no terms sheet is among the supplied sources.
4. **Any claim that the Sail exhibit contains no terms beyond a headline — FAIL.** The exhibit contains several material payment and milestone terms, quoted in Section 2.

No central transaction amount, reserve amount, reported result, guidance midpoint, debt/cash balance, or repurchase amount appears fabricated. The corrections above concern threshold precision, wording, source characterization, and accounting-basis labeling rather than invented core figures.

---

## Required corrections to `evidence-log.md`

1. Line 24 reserve-table note: replace **“first payment <=$3B in 2027, none before 2028”** with **“first payment <=$3B in 2027; no additional payments due before 2028.”**
2. Line 91: replace **“Participation threshold (>95%)”** with **“Participation threshold (at least 95%)”.**
3. Line 94: replace the assertion that option terms/milestones are absent beyond the headline with a precise gap statement, e.g. **“The exhibit discloses $785M initial payments (including $465M equity), $140M contingent development payments, the $2.58B option payment, and conditional EPS effects, but not the full option agreement or detailed milestone definitions.”**
4. Line 85: change **“$4.6 (pre-reversal)”** to **“$4.6 simple post-reversal balance before other reserve movements,”** and do not attribute the $1.2B residual without a sourced roll-forward.
5. Line 93: label “not yet accrued” as **unverified / awaiting Q3 accounting disclosure**, not as an established fact.
6. Keep repurchase bases explicit: **treasury/equity statement** versus **cash-flow statement**, especially for FY2024 ($2,407M vs $2,432M) and H1 2026 ($4,253M including excise tax vs $4,249M cash).
7. Correct the FY2023 repurchase source attribution: **$5,054M is from the consolidated statement of equity (10-K l.1209); Note 12 reports $5,079M (l.2188).**
