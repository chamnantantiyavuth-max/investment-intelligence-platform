# Gold Transmission — Watch-Item Test Evidence Log (ORG-2026-0012)

**Question (card):** Has the marginal driver of gold rotated from geopolitical hedging to
monetary-policy expectations (rate-cut pivot), and does a gold rally concurrent with cycle-high
real yields, risk-on equities, and Hormuz de-escalation weaken, strengthen, or leave intact the
0008 flow-dominance thesis — and is the gold–real-yield transmission break now testable at this scale?

**Card:** ORG-2026-0012 (gold watch-item test, deferred Founder triage A 2026-08-07)
**Workspace:** research/macro/gold-watch-item-0012/
**Parent thesis:** ORG-2026-0008 — `research/macro/gold-transmission/` (published 2026-08-06, Founder gate A)
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance.

## Deferral-condition assessment (executed 2026-08-13)

The 2026-08-07 deferral required a *settled macro window*: Hormuz live, jobs-report day, price
still moving. As of 2026-08-13 both scheduled data events have printed cleanly:

- **July jobs report released 2026-08-08:** NFP **−23,000** (unexpected decline), unemployment
  **4.1%** (up from June). (Reuters/CNBC/eciks coverage, 9–10 Aug 2026)
- **July CPI released 2026-08-12:** **+0.1% m/m** as expected, **3.4% y/y** (down from June 3.46%);
  core "subdued" per Bloomberg. (CNBC/WSJ/Reuters/Bloomberg, 12 Aug 2026)

Hormuz is **not** settled — the premise has *inverted* (de-escalation → live standoff; see S12–S14).
This is recorded as a named limitation, not a blocker: the two clean macro prints give the
multi-observation test the 0008 note specified. Verdict: **window OPENED for the test**; residual
Hormuz tail risk carried as an explicit caveat.

## Source register

| # | Figure / fact | Source | Date | Status |
|---|---|---|---|---|
| S1 | GC=F (COMEX gold Dec 26) close **4,477.90**; 8/3 close 4,033.70 → **+11.01%** (derived) | Yahoo Finance chart API (GC=F, range 1mo, interval 1d) | 2026-08-12 (pulled 2026-08-12 19:29 UTC) | VERIFIED (re-derived) |
| S2 | GC=F crossed **$4,500** intraday NY 12 Aug — "first time since June"; "tame US inflation cools Fed hike bets" | Mining.com headline; Caliber.Az ("Gold futures break above $4,500") | 2026-08-12 | VERIFIED (news RSS) |
| S3 | XAU spot **4,417.80** (2026-08-12 19:30 UTC); was 4,286.20 (2026-08-07 07:52 UTC) → +3.07% (derived) | gold-api.com /price/XAU | 2026-08-12 | VERIFIED (re-derived) |
| S4 | DFII10 (10y real yield) **2.43%** (2026-08-10); 8/7 2.40%; peak 2.47% (2026-07-31) — near cycle highs | FRED fredgraph.csv | last obs 2026-08-10 (pulled 2026-08-12 19:29 UTC) | VERIFIED (8/11–8/12 not yet published at pull — stated as unmeasured) |
| S5 | DGS10 **4.72%** (8/10); DGS2 **4.25%** (8/10); ^TNX 4.68 (8/12, −2bp vs 8/10) | FRED; Yahoo ^TNX | 2026-08-10/12 | VERIFIED |
| S6 | DXY **99.99** (8/12) vs 99.69 (8/5) → +0.30% (derived); DTWEXBGS 119.0649 (8/7, softened from 119.70 7/31) | Yahoo DX-Y.NYB; FRED DTWEXBGS | 2026-08-12 / 2026-08-07 | VERIFIED (re-derived) |
| S7 | S&P 500 **7,751.42** (8/12) vs 7,723.55 (8/5) → +0.36% (derived); record territory (7,753.11 on 8/10) | Yahoo ^GSPC | 2026-08-12 | VERIFIED (re-derived) |
| S8 | CL=F (WTI) **83.14** (8/12) vs 75.22 (8/5) → **+10.53% 5d** (derived); 8/3 84.67→8/5 75.22 was the −11% de-escalation leg | Yahoo CL=F | 2026-08-12 | VERIFIED (re-derived) |
| S9 | July NFP **−23,000**; unemployment **4.1%** | Reuters ("US nonfarm payroll employment fell 23,000 in July"), CNBC, eciks | released 2026-08-08 | VERIFIED (news RSS, multiple) |
| S10 | July CPI **+0.1% m/m** (as expected), **3.4% y/y** (down from June); core subdued | CNBC ("Consumer prices rose 0.1% in July... annual rate at 3.4%"), WSJ ("Down Slightly From the Previous Month"), Bloomberg ("US Core Inflation Comes in Subdued") | released 2026-08-12 | VERIFIED (news RSS, multiple) |
| S11 | Rate-odds repricing: "Fed Rate Hike Odds Near 48%" (pre-CPI, 8/12); post-CPI "July CPI Report Lowers September Rate-Hike Odds" (Kiplinger); "The Odds of a September Rate Hike Have Plunged" (Yahoo/Motley Fool); "Gold Breaks Through $4,400... as Rate-Cut Bets Intensify" (biggo, 8/11) | IndexBox / Kiplinger / Yahoo Finance / biggo headlines | 2026-08-11/12 | VERIFIED (news RSS; CME FedWatch API bot-gated 403 — odds cited from news, not raw API) |
| S12 | Hormuz: "U.S.-Iran deal in doubt" (CNBC: ship traffic near 3-month low); "attacks dent hopes for Strait of Hormuz reopening" (Al Jazeera); "Hormuz Standoff Derails Oil Supply Recovery... IEA" (WSJ); "IEA warns... supply shortfall to deepen as Hormuz reopening remains elusive" (Reuters) | CNBC / Al Jazeera / WSJ / Reuters headlines | 2026-08-12 | VERIFIED (news RSS, multiple) |
| S13 | "Gold remains over $4,400 as Iran situation worsens" | Yahoo Finance | 2026-08-11 | VERIFIED (news RSS) |
| S14 | Oil: "Oil prices rise as attacks dent hopes for Strait of Hormuz reopening" (Al Jazeera) — co-moves with gold | Al Jazeera | 2026-08-12 | VERIFIED (news RSS) |
| S15 | Official sector: "Central Bank Gold Buying Holds Through Fed Rate Uncertainty" (Crux Investor); "China Adds 20 Tonnes of Gold" (Yahoo/SCMP) | Crux Investor / Yahoo Finance | 2026-08-10/11 | VERIFIED (news RSS; tonnage not independently re-pulled — news-attested) |
| S16 | GLD +10.34% 1mo (367.13 → 405.10); SLV +13.37% 1mo; USO +8.14% 1mo | Yahoo GLD/SLV/USO | 2026-08-12 | VERIFIED (re-derived) |
| S17 | "Gold Up 10% MTD as US Inflation Soothes Fed Rate-Hike Fears" (BullionVault); LBMA snapshot survey: avg near **$4,500/oz by year-end** (Kitco) | BullionVault / Kitco | 2026-08-12 | VERIFIED (news RSS; MTD re-derived +10.6% from 7/31 close 4,049.10) |
| S18 | Prior observation (obs 1, 7 Aug): GC=F 4,033.70 (8/3) → 4,344.70 (8/7 ~07:55 UTC intraday) = +7.71% in 4 sessions; DFII10 2.41% (8/5); Hormuz-deal optimism (WTI −11% from 7/31 peak); JOLTS 7.36M (8/4) | ORG-2026-0012 legacy card radar_observation (frozen source) | 2026-08-07 | VERIFIED (frozen card; re-derived) |

## The two-observation test

| Dimension | Obs 1 (7 Aug) | Obs 2 (12 Aug) | Change |
|---|---|---|---|
| Gold (GC=F) | +7.71% in 4 sessions (→4,344.70 intraday) | +11.01% cumulative from 8/3 (→4,477.90 close; $4,500 intraday) | Anomaly **larger** at scale |
| 10y real yield (DFII10) | 2.41% (8/5); peak 2.47% (7/31) | 2.43% (8/10) | Still near cycle highs — inversion **persists** |
| Equities (S&P) | Record territory, +4.6% (7/31→8/4) | 7,751.42 record territory | Risk-on **persists** |
| Geopolitics (Hormuz) | De-escalation optimism; oil −11% (7/31 peak→8/5) | **Standoff live**; deal in doubt; oil **+10.53% 5d** | Premise **inverted** |
| Policy data | — (jobs day pending) | NFP −23k (8 Aug); CPI 3.4% (12 Aug); Sept-hike odds plunged | Data window **settled** |
| Marginal driver (observed) | Ambiguous (5 candidates) | 11–12 Aug leg headline-attributed to **rate-path repricing** | **Rotation observable** |

## Data gaps (named, not estimated)

- DFII10 8/11–8/12 obs not yet published by FRED at pull time (2026-08-12 19:29 UTC) — real-yield
  level response to CPI day not directly observed; ^TNX proxy used (4.68, flat).
- CME FedWatch API bot-gated (HTTP 403) — rate-odds quoted from news headlines, not raw API.
- ETF flows (daily creations/redemptions), CFTC positioning, World Gold Council official-purchase
  data — **not re-pulled** this session (same gap as 0008; GLD price +10.34% 1mo is a price proxy only).
- China +20t figure (S15) news-attested, not verified against WGC primary data.

## Analysis artifact status

- analyst-note.md — watch-item test / driver ranking (draft, this workspace)
- cro-opposing-essay.md — CRO dissent (draft, this workspace)
- draft-report-thai.md — Thai report draft, pending Founder gate for publication (FD #94 firewall)

Sources pulled 2026-08-12 19:29–19:31 UTC (local 2026-08-13 02:29–02:31 UTC+7) unless dated otherwise.
Analysis is advisory-only, portfolio-blind — no rate forecast, no price target, no buy/sell recommendation.

<!-- 2026-08-13 02:40 UTC+7 -->
