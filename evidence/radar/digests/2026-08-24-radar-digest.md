# Radar Digest — 2026-08-24 (Weekly Scan, FD #78 cron)

**Role:** Radar Scout (role 11, `org-radar-scout`) — discovery only, portfolio-blind, no analysis/recommendation.
**Run:** 2026-08-24 (Mon), pulls ~04:30–05:00 UTC (11:30–12:00 UTC+7). Continuity: read `2026-08-13-radar-midweek.md` + `2026-08-10-radar-digest.md`.
**Note:** The 2026-08-17 Monday weekly scan was MISSED (scheduler downtime — see SESSION_CLOSEOUT.md). This is the first scan in ~14 days since the 8/10 Monday digest.
**Run task:** t_3605264d (board `[DISC] IIP Weekly Radar Scan 2026-08-24`)
**Result:** 1 Task Idea Card filed (t_380da62e) → kanban triage, awaiting CoS triage.
**Status:** Advisory only. No state change. Figures point-in-time per FD #58 — valid at the pull timestamp, re-verify before reliance.

## 1. What was scanned

| Area | Sources used (all pulled 2026-08-24) |
|------|--------------------------------------|
| Standing: Gold vs real yields (0012 do-not-reraise respected; continuity check only) | Yahoo Finance GC=F (futures daily, 1mo), 10Y yield ^TNX, DXY DX-Y.NYB; FRED DFII10 attempted — API returned 404/error, gap persists |
| Standing: Silver (LBMA vault ACTIVE retry, COMEX known-gap, lease rates known-gap) | Yahoo Finance SI=F (futures daily, 1mo); COMEX not retried (CME 403 known-gap unchanged); CFTC COT not retried (404 known-gap unchanged); lease rates known-gap unchanged |
| Standing: Oil (ORG-2026-0022 continuity) | Yahoo Finance CL=F (futures daily, 1mo) |
| Standing: Apple (material events only) | SEC EDGAR submissions API (AAPL CIK 0000320193) |
| EDGAR filings pass (FD #81) — FO-universe 8 CIKs | SEC EDGAR submissions API ×8 (rate-limited ~3s between calls); primary-doc reads for candidates (NVDA 8-K full text read) |
| Event triggers (workflow §4) | Yahoo Finance broad market data (S&P 500 ^GSPC, Dow ^DJI, VIX) |
| Broad cross-asset context | Gold futures $4,695.3, Silver futures $68.92, WTI $85.62, S&P 500 7,674.37, DXY 98.84, 10Y 4.738%, VIX 15.13 |
| Feedback-loop refinements (card-outcomes.md) | 0012 do-not-reraise respected; 0013/0015 monitoring conditions checked against EDGAR; known-gaps retried per policy |

## 2. Top observations (cards filed)

1. **NVDA 8-K (17 Aug 2026): $105B capped residual-value guarantee for 4.25GW AI data center campus** (EQUITY, P1, M3 advisory, org-equity-analyst). Card: t_380da62e. One-line rationale: a surprise 8-K outside the earnings window (Items 1.01/2.03/7.01) — NVIDIA entered residual-value guaranties for ~4.25 GW IT load at the PORTS Technology Campus (Pike County, OH), with an option for +3.8 GW; aggregate payment obligation capped at $105B; an OpenAI affiliate is the tenant. This is a genuinely unusual, material, primary-source observation — a $105B off-balance-sheet contingent obligation that raises a real equity research question about NVDA's capital allocation, risk exposure, and the AI infrastructure financing structure.

## 3. What was deliberately ignored, and why

- **Gold's continued rally (futures $4,695.3, +16.4% from 3 Aug, +7.6% from 10 Aug)** — continuation of ORG-2026-0012's do-not-reraise question. The acceleration is noteworthy (gold unwinding from $4,033 → $4,695 in 3 weeks) but the core question is the same (gold vs real yields regime). **Flagged for CoS: 0012's re-test window may now be partially open** — CPI out, jobs report stale, Hormuz still live but oil stabilized ~$85. The do-not-reraise from 7 Aug (ORG-2026-0012) was conditioned on "until macro window settles." The window has partially settled. This is a digest note only, not a new card.
- **Silver rally (SI=F $68.92, +19.5% from 3 Aug)** — continuation of 0016's series (vaults, no visible scarcity). No new data point since LBMA July (907.059 Moz, 5-year high). LBMA August not yet published (~mid-Sept).
- **Oil (CL=F $85.62, stable from 8/14)** — ORG-2026-0022 is in process (awaiting Founder publish gate per SESSION_CLOSEOUT.md). No new card.
- **S&P 500 pullback (-1.4% from 8/17 peak)** — explained by rates repricing and macro rotation; not a crash (VIX 15.13). Below the bar.
- **Dollar weakness (DXY 98.84, ~2-year low)** — continuation of the known trend since July jobs miss. Feeds 0012, not a new card.
- **META Form 4 cluster (12 filings 8/18)** — resolved to Christopher K. Cox option exercises (code M, price $0, 16,388 shares acquired) + tax withholding (code F, 8,127 shares sold at $589.85). Routine option exercise pattern. Below the bar.
- **META Form 4 (8/20)** — Curtis J. Mahoney sold 1,559 shares at $558 (~$870K). Single officer sale, small. Below the bar.
- **AMZN 424B3 (8/18) + S-4/A (8/14)** — related to the Globalstar acquisition (not Amazon itself). Routine regulatory filings for the pending deal. Below the bar.
- **AAPL Form 4 (8/20)** — routine single filing. No material event. Q4 FY26 earnings ~Oct 2026.
- **GOOGL** — nothing in window. ORG-2026-0017 (ATM drawdown question) remains open.
- **TSLA** — nothing in window.
- **JNJ** — Form 4s (8/14, 8/18) + 144 (8/17). No talc-participation update (0015 monitoring unchanged).
- **MSFT Form 4 (8/17)** — digest note only per FD #81 CIW boundary (CIW paused).
- **13F-HR season (Q2, due 14 Aug)** — NVDA 13F-HR (8/14) and others are routine institutional season. Not cards.
- **Momentum screening** — out of scope by FD #75.

## 4. EDGAR pass outcome (FD #81)

8/8 CIKs screened (window 8/14–8/24, catching the 8/17–8/24 gap from the missed 8/17 Monday scan). **1 card filed.** Primary docs read for candidates. Rate-limited ~3s between calls.

| CIK | Company | Filings in window | Material/unusual? | Card? |
|-----|---------|-------------------|-------------------|-------|
| 0000320193 | AAPL | 4 (8/20) | Routine | No |
| 0000789019 | MSFT | 4 (8/17) | Digest note only (CIW boundary) | No |
| 0001045810 | **NVDA** | **8-K (8/17) + 13F-HR (8/14)** | **Surprise 8-K, $105B guarantee (Items 1.01/2.03/7.01)** | **Yes (t_380da62e)** |
| 0001652044 | GOOGL | None | — | No |
| 0001018724 | AMZN | 424B3 (8/18), S-4/A (8/14), 144s (8/17, 8/21), 4 (8/19), EFFECT (8/18) | 424B3/S-4/A = Globalstar acquisition, routine | No |
| 0001326801 | META | 12 × 4 (8/18), 3 × 4 (8/20), 3 × 144 (8/18) | Option exercises + tax withholding (Cox), small sale (Mahoney) — routine | No |
| 0001318605 | TSLA | None | — | No |
| 0000200406 | JNJ | 4 (8/14, 8/18), 144 (8/17) | Routine. No talc-participation update. | No |

## 5. Honest statement

**One card cleared the bar** — the NVDA 8-K with its $105B capped residual-value guarantee is a genuinely unusual, material, primary-source filing that the interest-rate path (8/17 is outside the earnings window, Item 1.01/2.03/7.01 disclosure). This is the most significant EDGAR finding since the Alphabet $65B issuance cluster (0017). The 14-day gap from the missed 8/17 scan meant this was the first pass to catch it.

Everything else in the standing series (gold, silver, oil, dollar, equities) is continuation of existing questions. Gold's accelerated rally is noteworthy and may warrant a re-test of 0012, but that is a CoS triage decision, not a new radar card.

The FRED DFII10 real-yield data source remains inaccessible (API 404). Data gaps for COMEX, CFTC COT, and silver lease rates are unchanged. LBMA August vault data is due ~mid-Sept (ACTIVE monthly retry).

## 6. Data gaps (honest, not signals)

| Gap | Status | Notes |
|-----|--------|-------|
| FRED DFII10 (10y real yield) | ⚠ STILL GAPPED (8/13+ window) | API returned 404/error page this pass. Retry each pass. |
| COMEX deliverable silver (CME primary) | KNOWN-GAP (unchanged) | Third-party metalcharts 99.8 Moz registered as of 8/6 still latest. |
| CFTC COT primary (silver positioning) | KNOWN-GAP (unchanged) | All URL variants 404. Finimize 8/9 "2-year bullish extreme" claim still unverified. |
| Silver lease rates | KNOWN-GAP (unchanged) | No new free source appeared. |
| LBMA August 2026 vault data | ACTIVE (monthly cadence) | Publication ~mid-Sept. Retry automatically after publication. |
| FRED DFII10 8/13+ | GAPPED | The 8/10 digest had 8/6 as latest (2.43%). FRED API not accessible this pass. |

## 7. Point-in-time flags (FD #58)

- All gold/silver futures figures: pulled 2026-08-24 ~04:30 UTC from Yahoo Finance. Current market session values.
- S&P 500, Dow, VIX, DXY, 10Y yield: pulled 2026-08-24 from Yahoo Finance. Some values are 8/21 close (Friday) since the market is still in Monday's session.
- EDGAR submissions data: pulled 2026-08-24 from SEC EDGAR API. Point-in-time at pull timestamp.
- NVDA 8-K: read 2026-08-24 from SEC EDGAR archives. Filing date 2026-08-17.
- WTI CL=F figures: pulled 2026-08-24 from Yahoo Finance.

## 8. Next steps (advisory)

- Card t_380da62e sits in triage for CoS D1 triage → suggested owner: org-equity-analyst; materiality M3 advisory.
- Consider re-testing ORG-2026-0012 (gold vs real yields) now that CPI is out and the macro window has partially settled. CoS decision.
- ORG-2026-0022 (IEA OMR oil supply dislocation) remains in process awaiting Founder publish gate.
- FRED DFII10 data gap persists — suggest Data Steward D2 check alternative sources (FRED API key, alternative series).
- No research mandates created, no reports touched, no state changed, no push (per cron contract).

---
*Radar Digest 2026-08-24 — FD #78 weekly scan (+ FD #81 EDGAR pass + FD #82 feedback loop). Advisory only; discovery-only; portfolio-blind.*
<!-- 2026-08-24 12:00 UTC+7 -->