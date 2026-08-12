# Gold vs Real Rates — Transmission Evidence Log (ORG-2026-0008)

**Question (card):** Are conflict- and inflation-risk flows overpowering the traditional real-yield drag on gold as the Federal Reserve turns more hawkish?
**Card:** ORG-2026-0008 (RADAR-001) · **Workspace:** research/macro/gold-transmission/
**Point-in-time rule (FD #58):** every figure valid only at its source date; re-verify before reliance.

## Source register

| # | Figure | Source | Date | Status |
|---|---|---|---|---|
| S1 | FOMC held fed funds 3.50–3.75% by 9-3 vote; all 3 dissents preferred +25bp hike | federalreserve.gov (FOMC statement + meeting minutes context) | 2026-07-29 | VERIFIED (radar pull, deleg_c98d7277) |
| S2 | 2y yield 4.20% (+73bp since 2025-12-31); 10y 4.63% (+45bp); 10y real 2.40% (+47bp) | FRED DGS2 / DGS10 / DFII10 | 2026-08-04 | VERIFIED (radar pull) |
| S3 | LBMA gold PM $4,206.60/oz; +24.6% YoY | LBMA gold_pm.json | 2026-08-05 | VERIFIED (radar pull; cross-checked in SLV evidence-log S5) |
| S4 | Fed broad dollar index −1.7% YoY | FRED DTWEXBGS | 2026-07-31 | VERIFIED (radar pull) |
| S5 | June CPI 3.46% YoY; core CPI 2.57% YoY | FRED CPIAUCSL / CPILFESL | 2026-06 (release ~2026-07) | VERIFIED (radar pull) |
| S6 | Implied prior-year gold ≈ $3,376.08 (derived: 4,206.60 ÷ 1.246) | derived from S3 | — | DERIVED (arithmetic re-run: 4206.60/1.246 = 3376.08) |

## The transmission puzzle (draft framing for the note)

- Traditional channel: higher real yields → higher opportunity cost of non-yielding gold → downward pressure. 10y real +47bp since year-end (S2) should have been a drag.
- Observed: gold +24.6% YoY (S3) with dollar only −1.7% (S4) — the move is NOT a dollar story (a −1.7% dollar would traditionally explain only a small fraction of +24.6%).
- Hawkish internal signal: 9-3 vote with all dissents preferring hikes (S1) — policy is TIGHTENING-leaning, not easing; headline CPI 3.46% above target (S5) sustains the hawkish regime.
- Candidate explanations for the residual (to test in the note):
  1. Conflict/geopolitical risk premium (safe-haven bid) — dominant candidate
  2. Inflation-risk / debasement flows (headline above target; sticky core 2.57%)
  3. Official-sector absorption (central-bank diversification — data not re-pulled)
  4. Policy-error hedging (hawkish hold raises hard-landing risk → gold as hedge)
  5. Real-yield channel broken or lagging (transmission regime change)
- What would confirm/break (watch items): gold's beta to real-yield moves (regression); official-sector purchase data (World Gold Council); ETF flows; real-yield behavior at new highs vs gold reaction; dollar regime shift.

## Data gaps (named, not estimated)

- Gold ETF flows; central-bank/official-sector purchase data (World Gold Council); CFTC positioning; a fitted beta of gold to 10y-real yields — none re-pulled this session.
- FRED level series for DGS2/DGS10/DFII10 (only the point-in-time snapshots from the radar are on record).
- The +24.6% YoY gold figure and its base-period comparison are source-attributed (LBMA); the underlying prior-year fixing was not re-pulled this session (implied ≈ $3,376.08, subject to rounding).

## Sources & limitations

S1–S5 from radar pass deleg_c98d7277 (browser-verified public sources). S6 derived. Analysis is advisory-only, portfolio-blind — no rate forecast, no price target, no buy/sell. The macro layer is a single-line assessment per dimension — directionally indicative, not a full forecast.

<!-- 2026-08-07 00:15 UTC+7 -->

## Raw endpoint observations (added 2026-08-07, audit correction 4 — independent reproduction)

| Series | Current level | Prior-year level | YoY (computed) | Reported | Status |
|---|---|---|---|---|---|
| DTWEXBGS (broad dollar) | 119.7034 (2026-07-31) | 121.7210 (2025-07-31) | −1.6576% | −1.7% | REPRODUCED (119.7034/121.7210−1) |
| CPIAUCSL (headline CPI) | 332.568 (2026-06) | 321.435 (2025-06) | +3.4635% | 3.46% | REPRODUCED (332.568/321.435−1) |
| CPILFESL (core CPI) | 336.065 (2026-06) | 327.658 (2025-06) | +2.5658% | 2.57% | REPRODUCED (336.065/327.658−1) |

Source: FRED fredgraph.csv (pulled 2026-08-07, curl). All three radar-reported percentages independently reproduced — no discrepancy.

## Watch-item test (ORG-2026-0012, 2026-08-13)

The driver-ranking watch-item test (card ORG-2026-0012, deferred Founder triage A 7 Aug — "re-test at a settled macro window") has been executed at the 12 Aug observation: gold +11.01% from 8/3 (GC=F 4,477.90 close; $4,500 intraday), DFII10 2.43% (8/10), Hormuz premise inverted (standoff live, WTI +10.53% 5d), July NFP −23k + July CPI 3.4% clearing the data window. Marginal driver of the 11–12 Aug leg = monetary-policy expectations (rate-path repricing); 0008 thesis consistent-with, permanent break NOT established (expectation channel explains the move). Artifacts: `research/macro/gold-watch-item-0012/` (evidence-log, analyst-note, cro-opposing-essay, draft-report-thai). Publication pending Founder gate.
