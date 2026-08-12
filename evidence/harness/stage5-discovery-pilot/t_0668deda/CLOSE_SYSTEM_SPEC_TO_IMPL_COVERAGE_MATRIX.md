# Close System Product Radar — Spec-to-Implementation Coverage Matrix (Bounded Sample)

- **Task:** t_0668deda — [DISC][CHILD] E — Close System Spec-to-Impl Coverage (Underlying vs Wrapper)
- **Methodology anchor (canonical):** `investment-intelligence-platform/ChatGPT/Integration 12 Aug 2026/IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md` — §17 (Spec-to-Implementation Coverage Matrix), §18 (Close System Universe Audit), §18A (Product / Wrapper Coverage), Workstream E.
- **Subject repo:** `C:/Users/Admin/Desktop/Antigravity/Close System Product Radar` (Sprint 0-60, commit `6f165d2`)
- **Date:** 2026-08-12
- **Bound:** 3 products — **SLV, TLT, GLD** — from the 8-product radar universe (SLV/TLT/FXI/GLD/KRE/LIT/COPX/SPY). Sample spans 2 approved product classes (physical commodities: silver/gold; fixed income: long-duration treasuries). Per §18, products were NOT added to make the matrix look complete; unrepresented approved classes are reported as M1 universe gaps, not filled.
- **State-change discipline:** no repo writes, no data mutation, no new thresholds, no composite suitability score. This file lives only in the task workspace.

## 0. Spec inventory — what the approved spec says Close System discovery should cover

| # | Spec row (§17) | Spec requirement source |
|---|---|---|
| R1 | Product categories | §4/C1 + §18: broad-market ETFs, sector/thematic ETFs, physical commodities, fixed income, diversified producer / strategic-resource products where authorized, agricultural commodities where approved, strategic minerals where approved |
| R2 | Underlying assets/products | §17 row; identity + asset-level coverage |
| R3 | P1 (eligibility/identity) | §17 row; **term used but NOT defined in canonical doc** (see F-7) |
| R4 | P2 (measurable evidence) | §17/§18 "measurable P2 evidence?" — **term used but NOT defined** (see F-7) |
| R5 | P3 (forward evidence) | §17/§18 "measurable P3 evidence?" — **term used but NOT defined** (see F-7) |
| R6 | Intelligence Layer 1 Macro | §17 row; §4/C1 "macro coverage" |
| R7 | Layer 2 Policy | §17 row; §4/C1 "policy coverage" |
| R8 | Layer 3 Cost | §17 row; §4/C1 "cost-data coverage" |
| R9 | Layer 4 Supply/Demand | §17 row; §4/C1 "inventory-data coverage / supply-demand coverage" |
| R10 | Layer 5 Hidden Signals | §17 row; §4/C1 "hidden-signal coverage" |
| R11 | Source availability | §17 row |
| R12 | Source freshness | §17 row; §4/C1 "data-source reliability" |
| R13 | Detector implementation | §17 row; "Which patterns exist in spec but not code?" |
| R14 | Human interpretation path | §17 row; "Hermes interprets meaning" (bias/thesis/risks) |
| R15 | Wrapper structural suitability (§18A) | physical-vs-synthetic, tracking diff/error, roll structure, contango/backwardation, issuer/counterparty, liquidity/spread, AUM/closure, collateral, leverage/inverse decay exclusion, tax mechanics, thesis-vs-holdings mismatch, producer-ETF vs physical risk — **each dimension reported separately, no composite score** |

Implementation-side spec surface (repo docs): `docs/SCORING_MODEL.md` (close-system-fit-v0.1.0: 6 hard gates + 7 weighted components), `docs/PRODUCT_DECISION_LOGIC.md` (decision order + wrapper rule caps), `docs/DISCOVERY_WORKFLOW.md` (explicit: "Discovery score is not a Close System suitability score"), `docs/METRIC_REQUIREMENTS.md`.

## 1. Coverage matrix — bounded sample (SLV / TLT / GLD)

Status legend: ✅ implemented live · ◑ partial (fixture/static/review-gated) · ❌ gap (no implementation) · ⛔ NOT EVALUABLE WITH CURRENT DATA (§18 wording) · N/A not applicable

| Spec row | SLV (iShares Silver Trust) — physical commodity | TLT (iShares 20+ Yr Treasury ETF) — fixed income | GLD (SPDR Gold Shares) — physical commodity |
|---|---|---|---|
| R1 Category coverage | ✅ physical commodity (precious metals: silver) | ✅ fixed income (long-duration treasuries) | ✅ physical commodity (precious metals: gold) |
| R2 Underlying identity | ✅ symbol/name/category/rank in radar fixture | ✅ same | ✅ same |
| R3 P1 | ◑ identity + research record present; P1 eligibility per approved gates NOT computed by radar | ◑ same | ◑ same |
| R4 P2 | ◑ live price/momentum + static macro evidence; cost = checkpoint only | ◑ live price/momentum + **live FRED macro** (DGS10, T10YIE) | ◑ live price/momentum + static macro; cost checkpoint only; flow capture review-gated |
| R5 P3 | ◑ bias + thesis + researchExpansion lane (research-level, seeded graph) | ◑ bias + thesis + expansion + disinflation chain seeded | ◑ bias + thesis + expansion + central-bank chain seeded; ETF flow proxy (review-gated) |
| R6 L1 Macro | ◑ macro.strength=STRONG but **static fixture** (Silver Institute), no live macro connector | ✅ **only product in sample with live macro connector** (FRED DGS10, T10YIE) | ◑ static central-bank/real-rate narrative; **no live real-yield connector wired to GLD** |
| R7 L2 Policy | ❌ no policy layer | ◑ breakeven inflation (T10YIE) only; no Fed stance / auction supply | ❌ no policy layer (central-bank demand is static research, not a live policy input) |
| R8 L3 Cost | ◑ commodityCostProfile (USGS/Silver Institute) but **checkpoint only** — reviewNote requires fresh AISC capture that does not exist | N/A (no commodity cost) | ◑ WGC cost profile checkpoint only; no live cost curve / AISC |
| R9 L4 Supply/Demand | ◑ static reviewed evidence (Silver Institute 2025); no live ingestion | ❌ Treasury supply = narrative only | ◑ static central-bank demand + **live SPDR GLD archive flow connector** (5-session tonnes proxy, sign-off gated, cannot change scores) |
| R10 L5 Hidden Signals | ❌ none | ❌ none | ❌ none |
| R11 Source availability | ◑ Yahoo public chart (live) + static Silver Institute/USGS URLs | ✅ Yahoo + FRED public CSV (live) | ◑ Yahoo + static WGC + SPDR archive xlsx (live capture) |
| R12 Source freshness | ◑ market CURRENT when live; sentiment SAMPLE; macro REVIEWED but no freshness monitor on static evidence | ◑ market CURRENT; macro live fetchedAt; sentiment SAMPLE | ◑ market CURRENT; flow LATEST_FLOW_CAPTURED/READY_FOR_SIGNOFF; macro static |
| R13 Detector implementation | ◑ price-position (52w percentile→valuation), momentum (1d/1m/3m), drawdown, mood proxy — all live; cost/supply-demand detectors absent | ◑ price/momentum/mood live + live FRED series; no duration/convexity detector | ◑ price/momentum/mood live + flow proxy detector (review-gated); no cost detector |
| R14 Human interpretation path | ✅ bias (action/summary/invalidation/horizon/confidence) + thesis + risks on detail page | ✅ same | ✅ same |
| R15 Wrapper structural suitability | ⛔ **NOT EVALUABLE** — zero wrapper dimensions in data model | ⛔ **NOT EVALUABLE** — zero wrapper dimensions | ⛔ **NOT EVALUABLE** — zero wrapper dimensions |

## 2. Underlying (data/calculation) gap register

Classification per §7 miss taxonomy: M1 Universe / M2 Data / M3 Detector.

| # | Product | Gap | Class |
|---|---|---|---|
| U-1 | SLV, GLD | Macro evidence is static reviewed research; no live macro connector exists for either (macroConnector config covers only TLT and SPY) | M2 Data |
| U-2 | SLV, GLD | Cost layer is a manual review checkpoint (`marginSignal` is human-labeled; fresh AISC/cost-curve capture required but absent; reviewNote admits it) | M2 Data |
| U-3 | SLV, GLD | No live supply/demand detector for the underlying commodity (silver demand/supply, central-bank gold purchases are static citations). Only GLD has an adjacent live capture (ETF flow proxy) and it is sign-off-gated | M3 Detector (+M2 for data feed) |
| U-4 | TLT | No duration/convexity or real-yield-position detector; policy layer limited to breakeven inflation; Treasury supply/auction data absent | M3 Detector + M2 Data |
| U-5 | all 3 | Intelligence Layer 5 (Hidden Signals) has zero detectors anywhere in the radar lib | M3 Detector |
| U-6 | all 3 | Radar `opportunityScore` = proxy formula (valuation×0.35 + crowd×0.25 + macro×0.3 + 90×0.1, `liveMarketMath.ts:88-90`) — it does NOT execute the approved `close-system-fit-v0.1.0` gates (survival/wrapper/liquidity/portfolio-fit/decay/options-suitability/research-completeness, SCORING_MODEL.md). Repo itself disclaims: "Discovery score is not a Close System suitability score" | M3 Detector (integration) |
| U-7 | all 3 | P1/P2/P3 referenced as matrix rows but undefined in the canonical doc → spec-definitional gap, flagged for parent synthesis; audit did not invent definitions | Spec gap (not M-classified) |
| U-8 | SLV, GLD, TLT | Static macro/evidence freshness is not monitored (dataQuality.macro REVIEWED vs NEEDS_REVIEW is a manual label); no freshness clock on cited research | M2 Data |

## 3. Wrapper (product surface) gap register — §18A, each dimension separately

No composite suitability score was computed (§18A). Every §18A dimension is **NOT EVALUABLE WITH CURRENT DATA** for all three products because the radar data model (`productRadarTypes.ts`) contains no wrapper fields and no code path reads wrapper sources. Verified by grep: zero occurrences of tracking-difference/error, contango/backwardation, roll structure, AUM, closure risk, issuer risk, or spread in `ProductRadarPage.tsx`, `ProductRadarDetailPage.tsx`, `productRadarTypes.ts`, or `src/lib/productRadar/*.ts`.

| §18A dimension | SLV | TLT | GLD |
|---|---|---|---|
| Physical vs synthetic exposure | ⛔ not measured (trust structure known informally only) | N/A (bond ETF) | ⛔ not measured |
| Tracking difference / tracking error | ⛔ | ⛔ | ⛔ |
| Futures roll structure | N/A (physical) | N/A | N/A (physical) |
| Contango / backwardation drag | ⛔ no measurement even where relevant to commodity thesis | N/A | ⛔ no measurement |
| Issuer / counterparty structure | ⛔ (BlackRock) | ⛔ (BlackRock) | ⛔ (State Street/SPDR) |
| Liquidity / spread | ⛔ | ⛔ | ⛔ |
| AUM / closure risk | ⛔ | ⛔ | ⛔ |
| Collateral structure | N/A | N/A | N/A |
| Leverage/inverse decay exclusion | ◑ exists only as rule-cap text in the OLD product-scoring model (SCORING_MODEL.md hard gate 2); radar pipeline has no such gate | ◑ same | ◑ same |
| Tax / product mechanics | ⛔ | ⛔ | ⛔ |
| Underlying thesis vs ETF holdings mismatch | ⛔ (GLD flow connector measures tonnes of gold, not holdings-vs-thesis fit) | ⛔ | ⛔ (flow proxy is holdings-level, not thesis-fit) |
| Producer-ETF equity/business risk vs physical underlying risk | ⛔ (no producer-ETF class in universe — M1) | N/A | ⛔ (no GDX-like class in universe — M1) |

Wrapper-level conclusion per §18A wording: for all three products the underlying opportunity is measurable (price-position/momentum/macro/flow), but **no currently approved wrapper can be structurally evaluated by the system** → classify as **Product / Wrapper Coverage Gap**, not "no opportunity".

## 4. M-class summary (for parent synthesis)

| Class | Count | Dominant theme |
|---|---|---|
| M1 Universe | 2 (class-level) | Approved classes with zero radar representation: agricultural commodities, energy/oil, uranium/strategic minerals beyond LIT/COPX, producer-ETF class (GDX-style), international broad-market beyond FXI. Sample bounded — no additions made |
| M2 Data | 6 (U-1, U-2, U-3, U-4, U-5, U-8 + wrapper register) | No wrapper data fields/sources at all; no live cost data; no live silver/gold supply-demand feeds; no freshness monitor on static research |
| M3 Detector | 5 (U-3, U-4, U-5, U-6 + wrapper gate) | No wrapper detector/gate in radar pipeline; no cost/margin detector; no supply-demand detector for the sample; no hidden-signal detector; radar score path bypasses approved hard gates |

## 5. What the radar DOES implement (verified, to stay honest)

- Live market price/momentum/valuation/crowd pipeline: `api/radar.ts` (Yahoo chart, 8s timeout, per-symbol fallback) → `liveMarketMath.ts` (52w percentile → DISCOUNT/FAIR/PREMIUM; moodIndex → FEAR/NEUTRAL/GREED; drawdown; 1d/1m/3m changes) → `useProductRadarSnapshot.ts` (LOADING/LIVE/PARTIAL/FALLBACK states).
- Source-mode honesty: `LIVE_MARKET` / `PARTIAL_LIVE` / `SAMPLE_FALLBACK` surfaced in UI ("Live Data Status").
- Macro connector (live): FRED DGS10 + T10YIE for TLT; NFCI for SPY (`macroConnector.ts`).
- Industry signal graph: seeded 2-3 step chains for all 8 products (`industrySignalResearch.ts`, `industrySignalGraph.ts`); live capture connectors for GLD flow (SPDR archive), KRE (SLOOS/SEC filings), LIT/COPX (IEA/PMI/market/margin) — all review/sign-off-gated, none can change scores.
- Human interpretation path (R14): bias with action/summary/invalidation/time-horizon/confidence + thesis + risks + expansion lane per product (fixture + detail page).
- Wrapper-adjacent honesty: DISCOVERY_WORKFLOW.md and radar disclaimers explicitly separate discovery score from suitability score.

## 6. Bounded-sample caveats

- 3 products ≠ full universe; findings are directional for the sample and class-level, not per-product verdicts for the other 5 radar products.
- No new thresholds were created; no product was added; no composite suitability score was produced (§18, §18A).
- P1/P2/P3 are reported as spec-referenced-but-undefined (F/U-7); parent should decide whether to resolve the definition before scaling the matrix.
- Repo was not modified (audit-only). Verification: `grep` evidence + source reads listed below; no state change.

## 7. Evidence (paths read)

- `Close System Product Radar/docs/PROJECT_MEMORY_HANDOFF.md` (capability/state of record)
- `Close System Product Radar/docs/SCORING_MODEL.md`, `docs/PRODUCT_DECISION_LOGIC.md`, `docs/DISCOVERY_WORKFLOW.md`, `docs/METRIC_REQUIREMENTS.md`
- `Close System Product Radar/src/domain/productRadarTypes.ts` (data model — no wrapper fields)
- `Close System Product Radar/src/data/productRadarResearch.ts` (8-record fixture; SLV 86/82, TLT 81/76, GLD 77/84; cost profiles only SLV/GLD/LIT/COPX)
- `Close System Product Radar/api/radar.ts`, `src/lib/productRadar/liveMarketMath.ts`, `macroConnector.ts`, `liveRadarClient.ts`, `useProductRadarSnapshot.ts`, `productRadar.ts`
- `Close System Product Radar/src/lib/productRadar/industrySignalConnectors.ts`, `industrySignalGraph.ts`, `etfFlowConnector.ts` (surface confirmed via handoff + tests)
- `Close System Product Radar/src/pages/ProductRadarPage.tsx`, `ProductRadarDetailPage.tsx` (+ SSR tests) — wrapper-term grep = 0 hits
- `IIP_Discovery_Recall_Coverage_Audit_Final_Handoff_v1.1.md` §4/§7/§10/§17/§18/§18A/§28E/§29

<!-- 2026-08-12 22:40 UTC+7 -->
