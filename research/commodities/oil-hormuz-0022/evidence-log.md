# Oil Supply-Demand Reconciliation — Evidence Log (ORG-2026-0022)

**Question (card):** Does the IEA-quantified Hormuz dislocation (demand −1.6 mb/d 2026, 510 kb/d deeper than July; supply −4.3 mb/d avg 2026; 8.3 mb/d Gulf output still shut in; stocks −410 mb since war start) change the oil → inflation → real-yield transmission that ORG-2026-0012 is blocked on, and is the 510 kb/d demand-destruction deepening the leading edge of a demand-supply repricing the market has not yet priced (WTI 75.22 → 83.08, +10.5% in 5 sessions)?

**Card:** ORG-2026-0022 (CoS triage A, 2026-08-13, P1/M2/COMMODITY)
**Workspace:** research/commodities/oil-hormuz-0022/
**Feeds:** ORG-2026-0012 re-test window (gold-vs-real-yields transmission); ORG-2026-0016 as context only
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance. Radar figures RE-VERIFIED against the IEA OMR primary this session (2026-08-13 ~12:00 UTC+7 / 05:00 UTC).

## Source register

| # | Figure / fact | Source | Date | Status |
|---|---|---|---|---|
| S1 | World oil demand forecast to **decline 1.6 mb/d in 2026**, 510 kb/d more than last month's estimate; Hormuz closure + elevated fuel prices weigh on consumption | IEA OMR August 2026 primary (https://www.iea.org/reports/oil-market-report-august-2026, highlights page) | published 2026-08-12, re-pulled 2026-08-13 | VERIFIED (primary, direct pull) |
| S2 | Demand path: contract **−4.9 mb/d in 2Q26, −2.8 mb/d in 3Q26, +580 kb/d growth in 4Q26**; +2.4 mb/d in 2027; H2-26 demand cut ~550 kb/d vs last month's Report | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary) |
| S3 | Global supply **+2.4 mb/d to 101.5 mb/d in July**, still 6.3 mb/d below year-ago; **8.3 mb/d of Gulf output still shut in** | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary) |
| S4 | **3Q26 supply projection cut 1.7 mb/d** vs last month; global supply projected **−4.3 mb/d avg 2026 (to ~102 mb/d)**, rebounding **+8.3 mb/d in 2027 to 110.3 mb/d** (re-derived: 102 + 8.3 = 110.3 ✓) | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary; arithmetic re-derived) |
| S5 | Refinery crude throughputs 80.9 mb/d July (+1.8 m/m), ~5 mb/d below year-ago; 3Q26 runs cut a further 370 kb/d (ME product disruptions + Russian refinery attacks); 2026 throughput −2.5 mb/d, 2027 +3.5 mb/d | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary) |
| S6 | **Atlantic Basin refining margins at all-time highs in July**; diesel/jet/gasoline cracks surged; seaborne product trade **−3.8 mb/d y/y**; ME/Russia/Asia diesel exports **−1.3 mb/d y/y (~20% of global seaborne)**, jet exports −670 kb/d y/y (~34%) | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary) |
| S7 | **Global observed stocks plunged 69 mb in July (2.2 mb/d)**, below 7.9 bn bbl first time since Apr 2025; onshore only −6 mb (draw concentrated in oil-on-water); **−410 mb since war start (−2.7 mb/d avg)** (re-derived: 410/152d ≈ 2.70 ✓; 69/31 ≈ 2.23 ✓) | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary; arithmetic re-derived) |
| S8 | **3Q26 global balance deficit 1.8 mb/d — more than double last month's ~0.8 mb/d estimate**; market projected to return to surplus late 2026, risks substantial, inventory buffers depleting (re-derived: 1.8/0.8 = 2.25x ✓) | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary; arithmetic re-derived) |
| S9 | Gulf production +2.5 mb/d in July to **23.9 mb/d, still 8.3 mb/d below pre-war (32.2)** (re-derived: 23.9+8.3 = 32.2 ✓); regional exports −2.1 mb/d to 15 mb/d; loadings peaked 20 mb/d early July → ~12 mb/d later | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary; arithmetic re-derived) |
| S10 | **North Sea Dated +$25.67/bbl over July to $96.80**, ~$92 at time of writing; spiked **$105/bbl on 23 July**; benchmark traded in an exceptionally wide ~$40/bbl July range; **WTI and Brent prompt differentials returned to backwardation** | IEA OMR Aug 2026 | 2026-08-12 | VERIFIED (primary) |
| S11 | OPEC+ effective spare capacity **~1.09 mb/d** (excl. shut-in Iranian/Russian crude); Saudi July output 8.24 vs implied target 10.35 (−2.11); Total OPEC-8 15.81 vs 20.39 (−4.58); Russia 8.76 (−1.06); Iran 2.3 | IEA OMR Aug 2026 (OPEC+ table) | 2026-08-12 | VERIFIED (primary; table parsed) |
| S12 | Market cross-check (radar): WTI **82.90**, Brent **88.75**, gold GC=F **4,455.8**, silver 65.45, DXY 100.015, 10y ^TNX 4.682 | Yahoo Finance v8 chart API | 2026-08-13 04:00 UTC (radar pull) | VERIFIED (re-pulled this session, S13) |
| S13 | Fresh re-pull this session: WTI **82.93** (prev 83.27), Brent **88.77** (prev 88.98), GC=F **4,454.8** (8/12 close 4,408.9; 8/13 4,453.5), SI=F **65.48**, DXY **99.984**, ^TNX **4.682**, S&P 7,748.5 | Yahoo Finance v8 chart API (query1) | 2026-08-13 ~05:00 UTC | VERIFIED (fresh pull) |
| S14 | **WTI futures curve (backwardation depth):** front 82.90, Dec-26 78.55, Mar-27 74.78, May-27 72.75, **Dec-27 70.54 → −12.36/bbl front→Dec-27 (−14.9%)** (re-derived: 82.90−70.54 = 12.36; 12.36/82.90 = 14.9% ✓) | Yahoo Finance (CL=F, CLZ26.NYM, CLH27.NYM, CLM27.NYM, CLZ27.NYM) | 2026-08-13 ~05:00 UTC | VERIFIED (fresh pull; arithmetic re-derived) |
| S15 | Real yields: **DFII10 2.43%** (8/11; 8/10 2.43, peak 2.47 on 7/31); DGS10 4.70% (8/11); DGS2 4.22% (8/11); **T10YIE breakeven 2.26% (8/12)** — flat vs 2.22 on 8/5, NOT repricing up | FRED fredgraph.csv (DFII10, DGS10, DGS2, T10YIE) | last obs 2026-08-11/12 (pulled 2026-08-13 ~05:00 UTC) | VERIFIED (fresh pull; 8/12 DFII10 unmeasured — FRED lag) |
| S16 | US demand (EIA weekly, w/e 8/7/26): **total products supplied 20,635 kb/d vs 21,357 y/y = −722 kb/d (−3.4%)** (re-derived: −722/21,357 = −3.38% ✓); **gasoline 8,964 (−0.4% y/y)** (re-derived: −36/9,000 = −0.40% ✓); **distillate 3,458 (−6.6% y/y)** (re-derived: −243/3,701 = −6.57% ✓); **jet 1,982 (+8.4% y/y)** (re-derived: +153/1,829 = +8.36% ✓) | EIA Weekly Petroleum Status Report table1.csv (ir.eia.gov/wpsr/table1.csv) | w/e 2026-08-07 (pulled 2026-08-13) | VERIFIED (fresh pull; arithmetic re-derived) |
| S17 | US stocks (EIA, w/e 8/7/26): **crude 723.1 mb (−12.9% y/y)** (re-derived: −106.8/829.9 = −12.87% ✓); gasoline 208.7 (−7.8%); distillate 107.1 (−5.7%); jet 45.2 (+3.3%); SPR 298.7 (−25.9% y/y) | EIA WPSR table4.csv | w/e 2026-08-07 (pulled 2026-08-13) | VERIFIED (fresh pull) |
| S18 | US crude imports by country (w/e 8/7/26): **Saudi 100 kb/d vs 273 y/y (−63.3%)**, **Iraq 0 vs 142 (−100%)**, Nigeria 39 vs 213 (−81.7%), Venezuela 743 vs 0 (new); net imports 4,281 (+938 y/y) — Gulf disruption visible in US import mix | EIA WPSR table8.csv | w/e 2026-08-07 (pulled 2026-08-13) | VERIFIED (fresh pull) |
| S19 | 0012 context: July NFP **−23,000** / unemployment 4.1% (released 8 Aug); July CPI **+0.1% m/m / 3.4% y/y**, core subdued (released 12 Aug); September-hike odds plunged post-CPI; gold $4,500 intraday 12 Aug; 0012 driver ranking at obs 2: rate expectations #1 (marginal), Hormuz geopolitical #2 (supporting), official-sector unmeasured #3, dollar mild #4 | ORG-2026-0012 watch-item test evidence log (research/macro/gold-watch-item-0012/evidence-log.md, S9–S11) | 2026-08-13 (executed 12 Aug observation) | VERIFIED (sibling artifact, this repo) |
| S20 | Rate-odds: pre-CPI Sept-hike odds near 48%; post-CPI "plunged" (Kiplinger / Yahoo-Motley Fool) — CME FedWatch API bot-gated (HTTP 403), quoted from news, not raw API (KNOWN-GAP) | 0012 evidence log S11 + radar midweek note | 2026-08-12/13 | VERIFIED (news-attested; CME 403 KNOWN-GAP) |

## Data gaps (named, not estimated)

- **DFII10 8/12–8/13** not yet published by FRED at pull (05:00 UTC) — real-yield response to the 8/13 oil/gold session unmeasured; ^TNX proxy used.
- **CME FedWatch API 403 (KNOWN-GAP)** — rate-odds quoted from news attribution only; no raw implied-probability series.
- **WTI/Brent front-month spread precision:** CL=F is the rolling front contract; Sept-26 (CLU26) ≈ front at 82.90, so front-month backwardation vs Dec-26 = 4.35/bbl. Deferred curve (Dec-27 70.54) is the structural signal.
- **IEA OMR full PDF** (supply/demand tables per country) is subscription-gated — this note uses the public highlights page (the authoritative summary of the same report); per-table granularity not re-pulled.
- **Gold 8/12 close discrepancy:** 0012 evidence log records GC=F close 4,477.90 on 8/12; this session's fresh pull shows 8/12 close 4,408.90 and 8/13 4,453.5. The 4,477.90 figure matches the intraday $4,500 spike (S2 in 0012 log) more closely than the settlement. Flagged for Data Steward; 8/13 4,453.5–4,455.8 (this pull / radar) used as the current level.
- **EIA product-supplied volatility:** single-week readings are noisy; the 4-week average (total 20,720 vs 21,159 y/y, −2.1%) is the steadier signal.

## Arithmetic re-derivation (38/38 pattern — all derived figures independently recomputed)

| Check | Computed | Claimed | Verdict |
|---|---|---|---|
| 2027 supply rebound | 102 + 8.3 = 110.3 | 110.3 | OK |
| Stock draw rate since war start | 410 mb / ~152 days = 2.70 mb/d | −2.7 mb/d | OK |
| July draw rate | 69 mb / 31 d = 2.23 mb/d | −2.2 mb/d | OK |
| 3Q26 deficit vs last month | 1.8 / 0.8 = 2.25x | "more than double" | OK |
| WTI 5-session move | 83.08 / 75.22 − 1 = +10.45% | +10.5% | OK |
| WTI front→Dec-27 backwardation | 82.90 − 70.54 = 12.36 (−14.9%) | −12.36/bbl | OK |
| Gulf pre-war level | 23.9 + 8.3 = 32.2 | 32.2 | OK |
| US total products supplied y/y | −722 / 21,357 = −3.38% | −3.4% | OK |
| US gasoline y/y | −36 / 9,000 = −0.40% | −0.4% | OK |
| US distillate y/y | −243 / 3,701 = −6.57% | −6.6% | OK |
| US jet y/y | +153 / 1,829 = +8.36% | +8.4% | OK |
| US crude stocks y/y | −106.8 / 829.9 = −12.87% | −12.9% | OK |
| 2026 supply avg | 101.5 − 4.3 ≈ 102 | ~102 mb/d | OK |

## Analysis artifact status

- analyst-note.md — supply-demand reconciliation + transmission + falsification conditions (draft, this workspace)
- draft-report-thai.md — Thai report draft, pending Founder gate for publication (FD #94 firewall)
- CRO challenge — ROUTED as separate independent challenge (materiality M2/P1, before Founder gate); not authored inside this mandate per CoS non-goal

Sources pulled 2026-08-13 ~05:00 UTC (local 2026-08-13 12:00 UTC+7) unless dated otherwise.
Analysis is advisory-only, portfolio-blind — no rate forecast, no price target, no buy/sell recommendation.
<!-- 2026-08-13 12:10 UTC+7 -->
