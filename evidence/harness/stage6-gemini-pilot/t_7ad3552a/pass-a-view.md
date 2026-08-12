# Pass A — Independent Hermes View: Apple Inc. (AAPL)

**Task:** t_7ad3552a · [DR][CHILD] S2 — Independent Hermes Pass A (anti-anchoring)
**Analyst:** Equity Alpha Analyst (org-equity-analyst), Hermes Pass A
**RESEARCH_AS_OF:** 2026-08-12 (retrieval day; filing/quote timestamps below)
**Pilot:** IIP × Gemini Deep Research v1.4 — Apple Rehearsal (PILOT-NONCANONICAL, Stage 6)
**Status:** ISOLATED FIRST PASS — formed without reading any published IIP conclusion, prior first-pass view, evidence-log narrative, or Gemini lane output. FROZEN at write time (S5 freeze applies after this file).
**Portfolio-blind:** true. Advisory research context only — no recommendation.

---

## Isolation & Anti-Anchoring Declaration

- This view was formed from the ADMITTED SOURCE packet only (S1 contract; mandate RM-2026-0001 §9 source gate):
  primary SEC filings first, market data supporting.
- **NOT read (anti-anchoring):** `reports/apple-*.md`, `research/companies/AAPL/*` (essays, evidence-log, prior first-pass views, CRO/audit notes), any Gemini output, Pass B workspace.
- Per handoff v1.4 §9: prior Hermes essays, old narratives, thesis statements, and publication prose are excluded by design.
- All figures below carry a source reference + as-of; derived metrics state their formula.

## Admitted sources used (S1 packet → this pass)

| ID | Document | Accession | Filed / As-of |
|----|----------|-----------|----------------|
| SRC-01 | FY2025 Form 10-K (Apple Inc.) | 0000320193-25-000079 | filed 2025-10-31; FYE 2025-09-27 |
| SRC-02 | Q3 FY26 Form 8-K (results press release) | 0000320193-26-000018 | furnished 2026-07-30; QE 2026-06-27 |
| SRC-03 | Q3 FY26 Form 10-Q (condensed financials) | 0000320193-26-000020 | filed 2026-07-31; QE 2026-06-27 |
| SRC-04 | SEC XBRL company facts (CIK 0000320193) | — | retrieved 2026-08-12 |
| SRC-05 | Market quote — Yahoo Finance (supporting) | — | 2026-08-12 |

---

# VIEW 1 — Business Understanding (Module A)

**What Apple economically does:** designs, manufactures and markets smartphones (iPhone), personal computers (Mac), tablets (iPad), wearables/home/accessories (Apple Watch, AirPods, Vision Pro, TV 4K, HomePod), and sells related services — advertising, AppleCare, cloud (iCloud), digital content, payments (Apple Pay) [SRC-01 §Item 1]. Fiscal year = 52/53-week ending last Saturday of September [SRC-01].

**Revenue engine (FY25):** total net sales $416.16B (+6% YoY), of which Products $322.6B (est. from 9M/quarter splits — see VIEW 2 for exact segment math) and Services $91.7B+ trajectory; iPhone is the dominant single category (9M FY26: $196.5B of $364.4B = 53.9%). Services 9M FY26: $91.7B (25.2% of total) [SRC-02].

**Who pays / why chosen:** consumers and enterprises buy integrated hardware+software+services; the 10-K describes the ecosystem (iOS/macOS/iPadOS/watchOS/visionOS/tvOS), retail + online + carrier + reseller distribution [SRC-01]. The 8-K management statements describe an installed base of active devices at an all-time high across all major product categories and geographic segments (CFO quote) [SRC-02] — issuer-reported indicator, not independently verified here.

**Demand type:** discretionary consumer electronics + services subscriptions; hardware is cyclical/replacement-driven; services are recurring and higher-margin. Geographic dispersion is wide (Americas 43%, Europe 27%, Greater China 15%, Japan 7%, ROW 8% of FY25) [SRC-01 segment table].

**Segments FY25 (net sales):** Americas $178.35B (+7%), Europe $111.03B (+10%), Greater China $64.38B (−4%), Japan $28.70B (+15%), Rest of Asia Pacific $33.70B (+10%) [SRC-01]. Greater China declined two consecutive years (−8% FY24, −4% FY25) before the Q3 FY26 rebound (+22% YoY to $18.8B) [SRC-02].

**Contract/dependence:** no customer concentration disclosed as material; supplier dependence on single/limited sources for certain components is disclosed as a risk [SRC-01 Item 1A]. NAND/DRAM and AI-compute components named as supply risks (risk factor text) [SRC-01].

---

# VIEW 2 — Financial Quality (Module F)

**Five-year headline (all $B, SRC-04 XBRL, FY 10-K rows):**

| Metric | FY21 | FY22 | FY23 | FY24 | FY25 |
|---|---|---|---|---|---|
| Revenue | 365.82 | 394.33 | 383.29 | 391.04 | 416.16 |
| Gross profit | 152.84 | 170.78 | 169.15 | 180.68 | 195.20 |
| Operating income | 108.95 | 119.44 | 114.30 | 123.22 | 133.05 |
| Net income | 94.68 | 99.80 | 97.00 | 93.74 | 112.01 |
| Operating cash flow | 104.04 | 122.15 | 110.54 | 118.25 | 111.48 |
| Capex | 11.09 | 10.71 | 10.96 | 9.45 | 12.71 |
| SBC | 7.91 | 9.04 | 10.83 | 11.69 | 12.86 |
| R&D | 21.91 | 26.25 | 29.91 | 31.37 | 34.55 |

**Margins (derived):** GM% FY23 44.1% → FY24 46.2% → FY25 46.9% (rising). OI% FY25 32.0%. NI% FY25 26.9%. Q3 FY26 GM **50.1%** — but management states this includes a favorable ~2pt impact from tariff refunds [SRC-02]; ex-refund GM ≈ 48.1% (derived, labeled analyst estimate).

**FY26 acceleration (SRC-02, 9M):** revenue $364.36B (+16.2% vs $313.70B), operating income $122.43B (+21.7%), net income $101.46B (+20.0%), diluted EPS $6.88 (+22.4%). Q3 alone: revenue $109.4B (+16%), EPS $2.02 (+29% incl. $0.11 tariff refund) [SRC-02]. This is a sharp acceleration vs FY21–FY25's ~3% revenue CAGR (derived: (416.16/365.82)^(1/4)−1 ≈ 3.3%).

**Cash conversion (derived):** FY25 FCF = OCF 111.48 − capex 12.71 = $98.8B; FCF/NI ≈ 88%. OCF has exceeded NI in 4 of 5 years (FY24: 118.25 vs 93.74). SBC is already inside GAAP NI (no double-count); D&A FY25 $11.70B [SRC-04].

**Earnings quality flags (from filings themselves):**
1. Tariff-refund benefits are disclosed as non-recurring-ish favorable items (Q3 FY26 GM +2pts, EPS +$0.11) — current-quarter quality boosted by a disclosed event; without it, growth is still strong but lower [SRC-02].
2. Inventories $11.09B at Q3 FY26 vs $5.72B at FY25-end (+94%) [SRC-03] — build-up could be tariff pre-buying / AI-infrastructure build / new product ramp; direction flagged for monitoring, cause not determinable from filings alone.
3. Intangible assets net $20.34B at Q3 FY26 vs $11.09B at FY25-end (+83%) [SRC-03] — large increase; suggests acquisitions or capitalized internal-use software (ASU 2025-06 internal-use software capitalization is disclosed as a recent pronouncement) [SRC-01].
4. Effective tax rate FY25 15.6% (20.72/132.73, derived) vs FY24 24.1% (29.75/123.48) — FY24 included a large one-time charge (filings note prior-year items); Q3 FY26 ETR 17.9% (6,478/36,267, derived). Rate swings are large; treat NI as noisy YoY.

**Product mix 9M FY26 (SRC-02):** iPhone $196.52B (+22.4%), Services $91.73B (+14.1%), Wearables/Home/Accessories $27.28B (+2.3%), Mac $27.14B (+8.6%), iPad $21.70B (+3.0%). Q3 FY26: iPhone $54.25B (+21.7%), Mac $10.35B (+28.6%), Services $30.74B (+12.1%), iPad $6.19B (−5.9%), Wearables $7.88B (+6.5%).

---

# VIEW 3 — Returns & Reinvestment (Module H)

**ROE (derived, coarse):** FY25 NI 112.01 / avg equity ((56.95+73.73)/2) ≈ 171% — very high but buyback-inflated (equity base shrunk by massive repurchases); not a clean economic-return signal.

**Capital allocation disclosed (SRC-01, SRC-02):**
- FY25: repurchased **$89.3B** of common stock + paid **$15.4B** dividends [SRC-01].
- May 2025: new **$100B** repurchase authorization; quarterly dividend raised $0.25→$0.26 [SRC-01].
- Q3 FY26: dividend raised to **$0.27**/share, payable 2026-08-13 [SRC-02].
- Share count declining: 14.773B (FY25-end) → 14.609B (Q3 FY26-end) [SRC-03] — −1.1% in three quarters (derived).

**Reinvestment:** R&D $34.55B FY25 (8.3% of revenue, growing ~10% YoY) [SRC-04]; capex $12.71B FY25 (+34% YoY) [SRC-04] — both up, consistent with AI build-out narrative but verified only at the dollar level here. The company returns the bulk of FCF to shareholders (~$104.7B total FY25 returns vs ~$98.8B FCF, derived) — returns slightly exceed FCF, funded by balance-sheet cash.

---

# VIEW 4 — Balance-Sheet Resilience (Module J-stress inputs)

**Q3 FY26 balance sheet (SRC-03, $B):** Total assets $383.27; cash + marketable securities: cash $39.54 + ST securities $22.86 + LT securities $84.12 = **$146.5B**; term debt current $11.01 + non-current $71.34 + commercial paper $2.00 = **$84.3B** → **net cash ≈ $62B** (derived). Shareholders' equity $107.52B (equity rose sharply from $73.73B at FY25-end — retained earnings swing from −$14.26B to +$11.33B, largely tariff/tax-related items; flagged, not fully reconciled here).

**Stress view:** fortress liquidity. Even with $84.3B debt, cash+securities cover debt ~1.7×. Debt is mostly LT term debt with staggered maturities (not detailed here). No pension/government exposure of note disclosed. Deferred revenue $9.54B is a liability that converts to future revenue [SRC-03].

**Working capital note:** AR $31.40B, vendor non-trade receivables $27.51B (Apple's financing arm), AP $64.53B — negative working-capital model typical of the company (AP ≫ AR+inventory). Inventories doubling is the main watch item (VIEW 2).

---

# VIEW 5 — Competitive Durability / Moat Mechanics (Module C)

*Framework: mechanism → evidence → measurability → failure conditions. All evidence below is issuer-reported (10-K/8-K) unless noted; durability claims are hypotheses to be tested, not proofs.*

1. **Share of Mind / brand + ecosystem lock-in (reported indicators):** integrated hardware-software-services; installed base of active devices at all-time high across all categories and geos (CFO, 8-K) [SRC-02]. iOS/macOS cross-device continuity is a switching-cost mechanism [SRC-01 product descriptions]. **Measurability:** low — no churn/migration data disclosed. **Failure condition:** consumers substitute a different default assistant/interface.
2. **High Switching Cost (reported indicators):** paid iCloud storage, AppleCare, App Store purchases, Apple Pay, Watch/AirPods integration with iPhone — recurring ecosystem costs accumulate over years [SRC-01 Services descriptions]. **Measurability:** indirect (Services ARPU, deferred revenue growth — deferred revenue $9.54B vs $9.06B FY25-end, +5%) [SRC-03]. **Failure:** if a competitor's ecosystem reaches comparable integration at lower switching friction.
3. **Intangible Assets (reported indicators):** R&D $34.55B FY25 (+10%); intangibles $20.34B (+83% in 9 months) [SRC-03/04] — significant investment, but the *economic* return on these intangibles is not measurable from filings.
4. **Efficient Scale / supply chain (reported indicators):** minority global market share in smartphones/PCs/tablets/wearables disclosed explicitly [SRC-01 Item 1] — the company itself disclaims dominance by share; scale advantages are operational, not structural dominance.
5. **Network Effect:** iOS ecosystem benefits from app developer network (App Store described in Services) [SRC-01] — a two-sided market mechanism, but the 10-K does not quantify developer churn or engagement. **Evidence gap:** network-effect durability not quantified in filings.

**What the filings say could break it (risk factors, SRC-01 Item 1A, excerpted):** intense competition with broad-line, low-price, large-installed-base competitors; aggressive price cuts; minority market share; components from single/limited sources; AI interface competition is implicitly covered under "rapidly changing markets" and new-technology risk. Regulatory exposure: DMA fine and legal proceedings are referenced in prior filings (FY25 10-K notes litigation; €500M DMA fine and Supreme Court cert 2026-06-30 were cited in the Q3 FY26 evidence set per prior accessions — **not re-verified here**, marked as context from SRC-03 litigation note if present — see unresolved item 4).

**Verdict (preliminary, low-to-medium confidence):** durable but conditional. The moat rests on ecosystem switching costs + brand + services economics, evidenced by persistent 46–50% GM and 25%+ services share — but the filings do not prove the behavioral mechanisms (churn, migration cost, developer surplus). AI interface disintermediation and regulatory opening of the monetization layer are the two most plausible break mechanisms visible in the risk-factor text; both are outside Apple's control.

---

# VIEW 6 — Growth Quality & Predictability (Modules I, D)

- **FY26 growth quality:** +16% revenue with iPhone +22% and Services +14% is broad-based (every geographic segment double-digit per CEO quote [SRC-02]) — better quality than a single-product spike. Greater China +22% in Q3 is a notable recovery vs two years of decline [SRC-02].
- **Mix shift:** Services share 25.2% of 9M FY26 revenue and rising; services carry higher margins (Services cost of sales 21.77B on 91.73B revenue ≈ 23.7% CoS vs Products 163.81B on 272.63B ≈ 60.1% — derived [SRC-02]) → mix is structurally margin-accretive.
- **Predictability assessment:** high for Services (recurring), medium for hardware (replacement cycles + launch timing), low for regulatory/tariff overlays. The FY26 results so far are distorted by tariff-refund timing (GM +2pts in Q3); FY27 comparability will be noisy.
- **Counterevidence kept visible:** iPad −5.9% and Wearables +2.3% YoY (9M) show the non-core hardware lines are NOT inflecting; Greater China's FY23–FY25 decline shows geographic vulnerability to competition/geopolitics.

---

# VIEW 7 — Valuation Context (Modules M/N/O — advisory only, no recommendation)

**Market (SRC-05, 2026-08-12):** price $301.08; 52-week range $223.78–$344.57. Diluted shares 14.75B (9M FY26 avg) → market cap ≈ **$4.44T** (derived).

**Price-implies (derived, coarse, labeled analyst-scenario):**
- P/E on FY25 NI 112.01B ≈ 39.6×; on 9M-FY26 annualized NI (~$135B, derived 101.46×4/3) ≈ 33×.
- Dividend $1.08/yr (4 × $0.27) → yield ≈ 0.36%; buyback yield ≈ 2% (89.3B/4.44T).
- Reverse-DCF flavor: to justify ~33× forward earnings, the market embeds durable mid-teens EPS growth plus continued buyback — consistent with the FY26 print but demanding versus FY21–25's ~4% NI CAGR (derived).
- **Not assessed here:** formal DCF, comparators, margin-of-safety price levels (Modules N/O/P deferred to later stages; valuation contracts not approved — per CIW §4, advisory context only).

---

# VIEW 8 — Permanent-Loss Risk & Inversion (Modules K/L)

**Ranked risks (probability × severity, analyst assessment from filings):**
1. **AI interface disintermediation** (medium prob, high severity): if the default assistant/search/interface shifts to a competitor's model, the routing layer of the ecosystem could be bypassed — Services monetization (25% of revenue, ~40%+ of gross profit by mix) is the value at risk. Visible in 8-K CEO framing ("all-new Siri AI" at WWDC26) [SRC-02] — Apple is responding, response quality not assessable from filings.
2. **Regulatory opening of monetization layer** (medium prob, high severity): DMA fine + app-store litigation risk; regulatory changes can compress take rates. Litigation disclosed in filings [SRC-01/03 context].
3. **Tariff/trade disruption** (medium prob, medium severity): tariff refunds are currently *helping*; a reversal or escalation hits GM and demand simultaneously. Disclosed in risk factors [SRC-01].
4. **China demand/geopolitics** (medium prob, medium severity): Greater China −4% FY25, +22% Q3 FY26 — volatile; single-country dependence for supply chain.
5. **Supplier concentration** (low-medium prob, medium severity): single/limited sources for certain components [SRC-01].

**Pre-mortem (−60–80% path):** AI assistant becomes the consumer's primary interface and routing layer; App Store/ads/services take rates compressed by regulation and competition simultaneously; China share erodes further; GM falls back toward 40%; multiple compresses from 33× to ~18× on flat earnings. Each step is individually plausible; the compound is the bear case.

**Pre-mortem (exceptional compounding path):** Siri AI drives a super-cycle upgrade; services mix reaches 30%+ with expanding margins; wearables/health becomes a durable second engine; buyback compounds per-share value. Both paths kept visible — no averaging.

---

# VIEW 9 — Research Confidence & Unresolved (Module Q inputs)

**Confidence:** MEDIUM for reported economics (financials verified from XBRL + filings, internal consistency high); LOW-MEDIUM for moat mechanism durability (behavioral evidence not disclosed); HIGH for balance-sheet resilience.

**Unresolved / would-change-my-view (visible gaps):**
1. Cause of the +94% inventory build (tariff pre-buy vs AI infra vs new product) — not determinable from filings alone.
2. Nature of the $9.25B intangible increase (+83%) — acquisitions vs capitalized software; ROI unknown.
3. Ex-tariff-refund run-rate GM — the 2pt refund is disclosed; the sustainable level needs next-quarter confirmation.
4. Regulatory proceedings detail (DMA fine status, Supreme Court cert outcome) — flagged for the evidence stage; litigation note not fully re-extracted in this pass.
5. Churn/migration/switching-cost quantification — absent from filings; would need primary customer/developer evidence (outside admitted packet).
6. iPhone unit vs ASP split — revenue-only disclosed; mix story needs unit data from later stages.

**Falsification conditions I would watch (Module Q draft):** (a) Services revenue growth < total revenue growth for 2 consecutive quarters; (b) GM ex-refund < 44%; (c) Greater China re-enters decline while the rest grows; (d) share count stops declining despite authorization; (e) a single competitor's interface reaches disclosed default-status penetration metrics. These are analyst-selected thresholds (not Founder-approved values) — labeled per FD #53.

---

## Pass-level integrity

- **Isolation:** no published IIP conclusion, no prior first-pass view, no Pass B / Gemini content read. All citations point to SRC-01..05 (admitted packet). Where a fact came from prior-accession context (e.g., DMA fine) it is explicitly marked unverified in this pass.
- **Epistemic labels used:** issuer-reported / derived / analyst estimate / analyst-selected scenario / unresolved.
- **Frozen:** this document is byte-frozen at completion of Pass A. Per-view SHA-256 hashes in the manifest below.
