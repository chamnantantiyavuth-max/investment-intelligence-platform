# Research Result 2 — CRR-2026-0002: Microsoft Corporation (MSFT) — Valuation Slice

**Status: PROPOSED v1 — assembled by AI executor (Parent, DeepSeek V4 Flash) after Independent Challenge PASS (round 4, 2026-08-03). NOT Published — awaiting Founder approval of THIS EXACT version (identified below by version + content hash). No post-approval analytical assembly permitted (PUBLICATION-STANDARD §5).**

---

## 1. Identity and State (RESULT-CONTRACT §2)

| Field | Value |
|---|---|
| `research_id` | CRR-2026-0002 |
| `company_id` | MSFT — Microsoft Corporation (NASDAQ: MSFT); Shared Core entity identity |
| `universe` | US-listed common stocks (v0.3) |
| `universe_version` | v0.3 |
| `as_of_date` | 2026-08-03 (research retrieval and review date; financials as of FY2026-06-30; market data 2026-08-03) |
| `research_version` | **proposed v1** (this document; assembled from `research-draft-2.md` v0.4, Independent Challenge PASS round 4) |
| `research_status` | `Founder Review` — proposed; becomes `Published` ONLY on Founder approval of this exact version (LIFECYCLE §2/§5) |
| `investment_classification` | **Advisory — Founder-decided. NOT mechanically set (Required Change #5).** This result carries NO classification; the Founder may assign one on review. Second slice = valuation depth, not endorsement (FD-CIW-009). |
| `thesis_status` | No Thesis Lifecycle state proposed. CIW research completion is **not** investment approval and does not change official Candidate/Thesis/Theme state (LIFECYCLE §4). |
| `confidence` | **Medium on valuation inputs** (owner-earnings maintenance split UNRESOLVED — authoritative range $56.3B–$133.7B retained; no filing disclosure narrows it); **High on arithmetic** (all calculations independently re-verified by reviewer rounds 1–4 against SEC XBRL raw facts); **Low on Module P comparator returns** (INCONCLUSIVE — no comparator primary filings). Qualitative, evidence-linked, advisory. |
| `portfolio_blind` | `true` (Constitution §23.8.1) — no holdings, positions, cost basis, or transaction history supplied or used |

**Relationship to first slice (F10/§8 lineage):** this is a **SUPPLEMENTAL, request-bound result** — NOT a supersession of `research-result.md` v1 (Current Authoritative for CRR-2026-0001, Modules A–M initial depth). v1 remains unchanged and retrievable. Where this slice refines an advisory figure, the new figure appears here marked as a valuation-slice refinement with explicit cross-reference to v1.

---

## 2. Dimension Summaries (each linked to evidence — full lineage in draft §10)

### Owner Earnings — maintenance split UNRESOLVED (evidence tested, range retained — F1/F4 discipline)
- **Authoritative retained range (Current Authoritative v1, consumed verbatim):** Low $56.3B ($7.56/sh) · Base $102.7B ($13.78/sh) · High $133.7B ($17.95/sh). P/OE @ $464.72: 61.5× / 33.7× / 25.9×. [first-slice v1; SRC-XBR]
- **Evidence test (new, this slice):** PP&E at cost $431.8B, accumulated depreciation $118.7B, depreciation expense $34.3B (FY26); useful lives 2–15 yr by class; capex FY26 $115.9B (2.61× FY24). Arithmetic proxies: acc-dep/depr ≈ 3.46 yr; depr/cost ≈ 7.9% — **non-identifying proxies, NOT a measured asset age or a maintenance-capex basis** (no asset-age/replacement/retirement disclosure exists in the filing).
- **Result:** the first-slice 60% split ($69.6B) remains unsupported; the evidence does NOT narrow the question; **no replacement percentage is adopted.** A proposed depreciation-only variant ($52.1B/$98.4B/$133.7B) and analyst-selected sensitivities (1.05–1.25× D&A → $125–132B OE) are disclosed as clearly labeled proposals — NOT the retained range. [SRC-XBR; SRC-001 Note 1; F1/N1/N2 dispositions]
- **Impact on valuation:** Base DCF dispersion from the unresolved range ≈ **$141–$335/sh** (~$194/sh) — the maintenance question remains a material second-order uncertainty, not resolved by this slice.

### Returns and Reinvestment — corrected incremental ROIC (F2)
- ROIC trend: 77.1% (FY22) → 51.2% (FY23) → 51.3% (FY24) → 37.3% (FY25) → **34.7% (FY26)** — declining, still above WACC.
- **Incremental ROIC on the AI-capital cohort (FY23–FY26, corrected):** ΔNOPAT = **$53.4B**; incremental capital ≈ **$150–$166B** (analyst-selected maintenance factors) → **incremental ROIC ≈ 32–36%** (v0.1's 68% was wrong — corrected and verified).
- **Marginal view: INCONCLUSIVE.** The marginal $175B CY26 build's returns are unobservable until FY27–FY29 filings (first-slice falsification methodology retained — 3-yr evidence window).

### Market Expectations (Module M-refresh — 2026-08-03)
- Price $464.72 (52wk $349.20–$553.72); diluted equity market cap ≈ **$3.4636T**; conventional EV ≈ $3.39T (bridge disclosed).
- **Reverse DCF (equity basis, coherent — F3):** price embeds **≈ 19.1% owner-earnings growth for 5 years (FY27–FY31)** at 10% cost of equity, 2.5% terminal — demanding; requires AI capex to earn >WACC at the margin AND sustained high-teens growth.

### `valuation_ranges` — Advisory scenarios (Module N/O — NOT an official output)
- **Intrinsic-value spread (advisory):** Bear $1,574B ($211/sh) · Base $2,420B ($325/sh) · Bull $3,673B ($493/sh) — DCF (discounted owner earnings, equity basis); earnings-power anchor $1,409B ($189/sh). Method matrix finite per request (SOTP/comparables/liquidation/private-owner OUT OF SCOPE).
- **Position vs price:** $464.72 sits ≈ **43% above Base IV** and ≈ **6% below Bull IV** — supportable only under high-growth/high-return assumptions.
- **Margin of safety:** none at current price under base/conservative assumptions (Conservative $242/sh, −92%; Base $325/sh, −43%; Optimistic $435/sh, −7% — price-premium convention, formula disclosed). Maximum rational price (hypothetical, conditional): **$376.49/sh** (10% required return, 2.5% terminal) or **$401.93/sh** (3.0% terminal) — never a platform threshold.
- **Advisory-only (Required Change #5):** no "Attractive Below Price", no verdict, no recommendation. Deterministic valuation contracts remain deferred.

### `monitoring indicators` — NOT PRODUCED in this slice (honest empty state, DNA-016)
- Module Q governed by CIW-MONITORING-CONTRACT v0.1 (FD-CIW-014, Cron Class A live) — referenced as approved monitoring-trigger context only, never re-produced and never valuation-contract authority (F5). Next real data-point: Q1-FY27 (~Oct 2026).

### Opportunity Cost (Module P — FIXED ex-ante comparators, F6)
- Five categories covered with fixed candidates (FD-CIW-007 shortlist): US 10-yr 4.745% · S&P 500 7,489.72 · AWS/AMZN $271.58 · NVDA $200.75 · JNJ $256.35.
- **MSFT model-implied returns: 6.76% (conservative) / 7.80% (base) / 9.35% (bull)** vs 4.745% risk-free — exceeds risk-free by ≈2.0–4.6 pp.
- **Superiority to S&P 500/AMZN/NVDA/JNJ: INCONCLUSIVE** — no comparator primary filings in the working set; no comparable total-return ranges computed (honest limitation; v0.1's 9–12% claim withdrawn).

### Permanent-Loss Mechanisms (consumed from first-slice Module K — not re-ranked)
- Dominant near-term mechanism: valuation-driven permanent loss (time-value, multiple compression). Business impairment low (net cash, GAAP-profitable, diversified annuity). AI-capex-return and commitment-stack risks carried from v1 with the potential-overlap caveat (F3 — $743.8B / $329.1B separate, not summed).

---

## 3. Unresolved Questions (explicit — honest empty states)

1. **The maintenance-capex split** — unresolved; authoritative range $56.3B–$133.7B retained (no filing disclosure narrows it; Base DCF dispersion ≈ $141–$335/sh).
2. **Marginal AI-capex returns** — INCONCLUSIVE until FY27–FY29 filings (incremental ROIC 32–36% is a peak-cycle cohort average, not marginal proof).
3. **Module P comparator returns** — INCONCLUSIVE (no comparator primary filings; market data only).
4. OpenAI-independent growth durability (carried from v1 Q2).
5. Regulatory outcomes (carried from v1 Q4).
6. Commitment-stack overlap precision (carried from v1 Q6).

---

## 4. Final Challenge (RESEARCH-FRAMEWORK §7 — reviewer-passed, draft §12)

- **Three assumptions driving value most:** (1) sustainable owner earnings after true maintenance capex — UNRESOLVED ($56.3B–$133.7B); (2) five-year OE growth (10–15% base/bull); (3) discount rate + terminal growth (9–11.5% cost of equity; 2–3% terminal).
- **Least supported:** the maintenance-capex split (no filing evidence); Module P returns next weakest.
- **Reversing fact:** primary evidence supporting ~19% five-year OE growth at 10% equity return with above-cost incremental returns; conversely, higher maintenance or sub-WACC cohorts (FY27–FY29) strengthen the bearish reading.
- **Confirmation bias:** canonical moat + desire to "resolve" the 60% split — resisted by retaining the unresolved range.
- **Skeptical short seller:** capex supercycle capitalized before returns visible; depreciation lags; obsolescence risk; commitment stack ($743.8B and, separately, $329.1B — not summed); OpenAI concentration; multiple compression on deceleration.
- **Knowledgeable operator:** distribution, enterprise trust, integration, contracted demand, capacity constraints can sustain utilization and cohort returns above cost.
- **Mispricing vs uncertainty vs distress vs optimism:** primarily optimistic assumptions + genuine uncertainty; no distress; mispricing not demonstrated.
- **Rational private owner at current EV:** **not demonstrated** — mid-OE yield ≈ 3.7%; valid Base DCF far below current price.
- **Markets closed 10 years:** probably yes as a business, not unconditionally and not at today's price.
- **Expected return vs alternatives:** 6.76–9.35% vs 4.745% risk-free; vs S&P/AMZN/NVDA/JNJ **INCONCLUSIVE**.

---

## 5. Theme Feedback (RESEARCH-FRAMEWORK §8 — evidence + analysis; does NOT change official Theme state)

- **AI/Cloud Platform theme: strengthened** (from v1 — RPO, capacity constraints) — unchanged by this slice.
- **Value-capture signal:** the unresolved maintenance-split + ~$175B forward capex keeps the margin-competition/returns-compression theme signal active — the market is pricing ~19% OE growth; any FY27–FY29 evidence of sub-WACC cohorts would strengthen the compression thesis.
- **No official Theme state changes proposed.**

---

## 6. Artifact References

| Artifact | Path | Version/State |
|---|---|---|
| Research request | `docs/ciw-pilot-msft/CRR-2026-0002-request.md` | APPROVED v0.4 (Research Gate 2026-08-03, FD-CIW-015) |
| Source Map 2 | `docs/ciw-pilot-msft/source-map-2.md` | gate PASSED |
| Research draft 2 | `docs/ciw-pilot-msft/research-draft-2.md` | v0.4 (reviewed — IC PASS round 4) |
| Independent Challenge | `docs/ciw-pilot-msft/challenge-review-2{,-REVIEW,-CONFIRM,-FINAL}.md` | rounds 1–3 FAIL → round 4 **PASS** (16/16) |
| This result | `docs/ciw-pilot-msft/research-result-2.md` | **proposed v1 — awaiting Founder approval** |
| First-slice result | `docs/ciw-pilot-msft/research-result.md` | Published / Current Authoritative v1 (unchanged) |
| Monitoring contract | `project-definition/company-intelligence-workbench/CIW-MONITORING-CONTRACT.md` | Approved v0.1 (FD-CIW-014) |
| Founder decisions | FD-CIW-009/010/011/012/013/014/015 | pilot / design / execution / publication / monitoring / second-slice authorization |

---

## 7. Review Status

- **Independent Challenge: PASS (round 4, 2026-08-03)** — Sol Medium (gpt-5.6-sol via openai-codex), separate context each round, direct primary-source inspection and independent recalculation from SEC XBRL raw facts. Rounds 1–3 FAIL disposed (F1–F7, N1, N2); all affected gates re-run: **16/16 PASS**. Advisory to Founder — not Founder approval. [challenge-review-2-FINAL.md]
- **Quality gates:** 16/16 PASS at v0.4 (round-4 independent confirmation; FAIL history honestly disclosed).
- **Founder Review: PENDING** — this exact document (proposed v1). Founder approval identifies version + hash (Constitution §21); casual agreement is not approval. Approval transitions this version to `Published` / `Current Authoritative v1` (of this supplemental artifact). Any change after approval = new version + new review cycle (append-first).

---

## 8. Source Map 2 (per-source status — full detail in `source-map-2.md`)

| Source | Category | Status |
|---|---|---|
| SRC-001 (10-K FY26) | latest annual filing | `reviewed` (re-verified for valuation inputs) |
| SRC-002 (10-Q FY26 Q3) | latest interim filing | `reviewed`; Q1-FY27 `not_yet_published` (~Oct 2026) — recorded |
| SRC-003a–d (earnings + transcripts) | earnings releases + transcripts | `reviewed` (first slice; no new release) |
| SRC-004 (DEF 14A) | proxy | `reviewed` (first slice; consumed, E out of scope) |
| SRC-005 (regulatory) | industry-applicable | `reviewed_clear` (no material new development) |
| SRC-006a–e + SRC-XBR (historical + XBRL) | normalization + PP&E/depreciation evidence | `reviewed`; class-level gaps recorded `incomplete` where absent — never invented |
| SRC-MKT / SRC-RATE (market + rates) | valuation inputs | `reviewed` (2026-08-03: MSFT $464.72; 10-yr 4.745%) |
| SRC-P-* (comparators) | Module P market data | `reviewed` (prices); comparator primary filings NOT in working set — limitation recorded, Module P superiority INCONCLUSIVE |

**Source-coverage report:** no blocking `missing_required` / `failed_retrieval` statuses. Class-level PP&E disclosures present but maintenance-capex evidence absent — recorded as limitation, not hidden. Result reaches `Complete` only after Founder approval → `Published`.

---

## 9. Claim Lineage Summary (full in draft §10; all calculations rerunnable)

- All material claims carry `[SRC-ID]` references in the draft.
- All derived metrics (maintenance sensitivities, owner earnings, ΔNOPAT, incremental ROIC, DCF Bear/Base/Bull, reverse DCF, MoS prices, implied returns) independently re-verified by the reviewer against SEC XBRL raw facts (rounds 1–4; verification tags recorded).
- Epistemic separations preserved: raw source / observed fact / management claim / derived metric / analyst-selected scenario / advisory judgment — never collapsed. Unresolved items carry honest empty states (DNA-016).

---

*Research Result 2 proposed v1 (CRR-2026-0002). Assembled by Parent executor after Independent Challenge PASS (round 4, 2026-08-03). NOT Published — Founder Review pending. Approval must identify this exact version + content hash (Constitution §21). Portfolio-blind: true. Advisory only; no investment recommendation.*
<!-- 2026-08-03 19:00 UTC+7 -->
