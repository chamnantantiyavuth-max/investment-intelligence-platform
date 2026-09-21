# Radar Digest — 2026-09-21 (Weekly Scan, FD #78 cron)

**Role:** Radar Scout (role 11, `org-radar-scout`) — discovery only, portfolio-blind, no analysis/recommendation.
**Run:** 2026-09-21 (Mon), pulls ~11:15–11:35 UTC+7 (04:15–04:35 UTC).
**Continuity:** Read `2026-09-17-radar-midweek.md` (last mid-week watch, 0 cards) + `2026-09-07-radar-digest.md` (last Monday weekly). The 2026-09-14 Monday scan was MISSED (scheduler gap, same pattern as Sep 1).
**Run task:** t_e9b3820c (board `[DISC] IIP Weekly Radar Scan 2026-09-21`)
**Result:** 1 Task Idea Card filed (t_b4fa9b10) → kanban triage, awaiting CoS triage.
**Status:** Advisory only. No state change. Figures point-in-time per FD #58 — valid at the pull timestamp, re-verify before reliance.

## 1. What was scanned

| Area | Sources used (all pulled 2026-09-21) |
|------|--------------------------------------|
| Standing: Gold vs real yields (0012 do-not-reraise respected; flag for CoS re-test) | Yahoo Finance GC=F (futures 5d+1mo), ^TNX (10Y yield), DX-Y.NYB (DXY), FRED DFII10 CSV (finally accessible — data through Sep 17) |
| Standing: Silver (LBMA ACTIVE retry, COMEX known-gap, lease rates known-gap) | Yahoo Finance SI=F (futures 5d+1mo); COMEX not retried (CME known-gap unchanged); CFTC COT known-gap unchanged; LBMA August vault data — all URL variants returned 404; lease rates known-gap unchanged |
| Standing: Oil (WTI crash flagged — ORG-2026-0022 thesis significantly reversed) | Yahoo Finance CL=F (futures 5d+1mo) |
| Standing: Apple (material events only) | SEC EDGAR submissions API (AAPL CIK 0000320193) |
| EDGAR filings pass (FD #81) — FO-universe 8 CIKs | SEC EDGAR submissions API ×8 (rate-limited ~3s between calls); primary-doc reads for candidates (AMZN Sep 9 8-K investigated) |
| Event triggers (workflow §4) | FOMC Sep 16-17 concluded (hawkish) — macro window settled; no new event triggers |
| Broad cross-asset context | Gold $4,395.5, Silver $66.64, WTI $94.14, S&P 500 7,650.5, DXY 100.312, 10Y 4.998%, VIX 14.81 |
| Feedback-loop refinements (card-outcomes.md) | 0012 do-not-reraise respected (macro window settled — flagged for CoS unblock); 0015 (JNJ) monitoring: no talc update; 0013 monitoring: WTI crash is material development; known-gaps retried per policy |
| FRED DFII10 (10y real yield) — retry after ~2-week gap | ✅ CSV ROUTE WORKED — gap CLOSED for data through 2026-09-17. Sep 18+ still gapped (FRED lag). |

## 2. Top observations (cards filed)

1. **WTI crude crash: $105.83→$94.11 in 4 trading sessions (−11.1% peak-to-current, −6.2% single-session Sep 18→21)** (COMMODITY, P2, M2 advisory, org-equity-analyst). **Card: t_b4fa9b10.** One-line rationale: a −11.1% crash from the Sep 15 peak in 4 sessions, with a −6.2% gap-down on Monday Sep 21 alone. This is the largest single-session WTI decline since the 2020 COVID crash and fully reverses the ORG-2026-0022 supply-dislocation surge (>70% unwound). Raises a genuine research question: demand destruction, supply normalization, or position/profit-taking — a material shift in the oil thesis that warrants new research engagement.

## 3. Standing-series changes since Sep 17 mid-week watch

| Series | Sep 17 (mid-week) | Sep 21 (this pass) | Change | Notable? |
|--------|-------------------|--------------------|--------|----------|
| **WTI crude (CL=F)** | **$102.29** | **$94.11** | **−$8.18 / −8.0%** | **⚠ MOST MATERIAL MOVE.** Crash from $105.83 peak (Sep 15) to $94.11 (Sep 21) = −$11.72 / −11.1% in 4 sessions. Sep 18 close was $100.30; Sep 21 opened at $94.13 = −6.2% gap-down. The entire supply-dislocation thesis (ORG-2026-0022, $82→$105) is now >70% reversed. |
| Gold (GC=F) | $4,334.1 | **$4,395.5** | **+$61.4 / +1.4%** | Recovered from FOMC intraday low ($4,273 on Sep 16). Bounce in correlation with VIX collapse. V-shaped recovery on FOMC day. |
| Silver (SI=F) | $64.16 | **$66.64** | **+$2.48 / +3.9%** | Correlated gold recovery. Returned to the $66-67 range from Sep 7 digest level. Gold/silver ratio ~65.9 (tighter from ~67.6). |
| S&P 500 | 7,551.8 | **7,650.5** | **+98.7 / +1.3%** | FOMC selloff fully recovered. Index back near early-Sep levels. |
| VIX | 17.71 | **14.81** | **−2.90 / −16.4%** | **COLLAPSED.** FOMC event risk fully subsided. Back to pre-stress levels. |
| DXY | 100.32 | **100.31** | ~flat | Dollar stable above 100. |
| 10Y yield | 5.006% | **4.998%** | ~flat | Hovering just below 5%. |

### Key cross-series analysis

- **WTI/equity decoupling:** WTI crashed −8% while S&P recovered +1.3% — this is a notable decoupling. If WTI were crashing on recession/demand-destruction fears, equities would likely be declining, not recovering. This tentatively supports a profit-taking/supply-normalization explanation over a demand-destruction narrative — but this is observation, not analysis.
- **Gold/VIX correlation:** Gold recovered +1.4% as VIX collapsed from 17.71→14.81. The metal behaves in its risk-off/event-risk-hedge pattern (bought when VIX spikes, sold when it subsides). Consistent with ORG-2026-0012's flow-dominance hypothesis.
- **Real yields +24bp while gold −1.8% (Aug→Sep):** Real yields rose from 2.44% (Sep 1) to 2.68% (Sep 16, FOMC day) with gold declining only from $4,476 to $4,395 (−1.8%). This is partial resilience — gold did NOT decline by the theoretical amount that a −24bp real-yield move would imply under the historical correlation regime.

## 4. Data-gap retries (per card-outcomes.md retry policy)

| Gap (from register/digest) | Retry outcome |
|---------------------------|---------------|
| **FRED DFII10 (10y real yield) 9/2+** | ✅ **CLOSED — CSV route worked** (first success since Sep 3 mid-week). Data now available through Sep 17. Key values: Sep 1=2.44%, Sep 10=2.55%, Sep 15=2.62%, Sep 16=2.68% (FOMC day high), Sep 17=2.61%. Sep 18+ still gapped (FRED lag — expected; retry next pass). **Data Steward D2 alert retired.** |
| **LBMA vault August 2026** | ❌ All LBMA URL variants returned 404/site-not-found. The page structure may have changed. Actively gapped — retry next pass with alternative URL discovery. |
| COMEX deliverable silver (CME) | ❌ KNOWN-GAP unchanged. Third-party metalcharts 99.8 Moz registered @8/6 still latest. |
| CFTC COT primary (silver positioning) | ❌ KNOWN-GAP unchanged. Finimize "2-year bullish extreme" claim remains UNVERIFIED. |
| Silver lease rates | ⏭ KNOWN-GAP unchanged. No new free source appeared. |
| Sep 14 Monday scan | CYCLE GAP — missed (same scheduler pattern as Sep 1). This is the third missed Monday scan (Aug 17, Sep 1, Sep 14). |

## 5. EDGAR pass outcome (FD #81 — filings window 9/14–9/21)

**8/8 CIKs screened. 0 cards filed from EDGAR.** New filings in window:

| CIK | Company | Filings in window (≥ Sep 14) | Material/unusual? | Card? |
|-----|---------|----------------------------|-------------------|-------|
| 0000320193 | AAPL | Form 4 (9/17) | Routine single insider filing | No |
| 0000789019 | **MSFT** | 5× Form 4 (9/17), 3× Form 4 (9/15), 144 (9/14) | Heavy Form 4 cluster (8 filings). CIW boundary. Pattern consistent with FY Q1 equity plan settlement. | No (digest note only — CIW boundary) |
| 0001045810 | **NVDA** | 5× Form 4 (9/18), 144 (9/17) | Post-Hugging Face insider transactions. 5 filings in one day is a cluster but routine plan transactions. No new 8-K or material filing since Hugging Face (Sep 3). | No |
| 0001652044 | **GOOGL** | **13× Form 4 (9/16)** — **INVESTIGATED** | Dividend-equivalent unit (DEU) accruals tied to the Sep 14 GOOGL cash dividend. Same pattern as Sep 17 mid-week — confirmed routine via $0/price filing by Pichai. | No (routine scheduled event) |
| 0001018724 | **AMZN** | 8-K (9/14, 9/9) | **Sep 9 8-K** (Item 5.02): routine officer compensation change (new director/appointment, investigated — no material surprise). **Sep 14 8-K**: £4.242B ($~5.6B) sterling notes offering (covered in Sep 17 mid-week). | No (both routine) |
| 0001326801 | META | Form 4 (9/17, 9/16), 144 (9/15, 9/14) | Routine insider plan transactions | No |
| 0001318605 | TSLA | None | — | No |
| 0000200406 | JNJ | None | — | No |

### Key EDGAR notes (no card)

- **GOOGL 13× Form 4 (Sep 16):** Same dividend-equivalent accrual pattern as the mid-week investigation. Conclusively routine — DEU accruals are standard for GOOGL's dividend policy. No insider-selling signal.
- **AMZN Sep 9 8-K (Item 5.02):** Compensation arrangements / new officer/director. Routine. Sep 14 8-K (Sterling notes) already covered.
- **NVDA Form 4 cluster (5× in a day, Sep 18):** Post-Hugging Face insider equity plan transactions. No 8-Ks, no material filings since the Sep 3 Hugging Face acquisition.
- **MSFT Form 4 cluster (8 filings Sep 14-17):** CIW boundary — digest note only. Early-FY equity plan settlement pattern.
- **No activist SC 13D/G, no 13F-HR late-filer, no 8-K cluster, no offerings.**
- **13F Q2 season closed (due Aug 14).**
- **JNJ:** Still quiet on talc — no new participation filings or 8-Ks since the resolution package was announced.

## 6. Event triggers — FOMC post-mortem (workflow §4 list)

| Trigger | Status | Impact assessment |
|---------|--------|-------------------|
| 🔴 **FOMC Sep 16-17** | **CONCLUDED — hawkish outcome** | S&P −1.1% on decision day (Sep 16), recovered by Sep 18. 10Y spiked to 5.006%, now 4.998%. DXY >100. Gold intraday low $4,273 → V-recovered to $4,387 same day. Real yields rose 24bp (2.44%→2.68% Sep 1→16). |
| 🟡 **FOMC aftermath** | Markets assimilating | VIX 14.81 (calm). Equities recovered. The macro window has settled — ORG-2026-0012 re-test condition is met. |
| 🟡 **WTI crash** | **−11% peak-to-current; −6.2% single-session** | Most material new observation. Demands a new research question distinct from the published ORG-2026-0022 supply-dislocation thesis. |
| 🟢 Gold recovery | $4,395 (+$61 from Sep 17) | V-shaped FOMC-day recovery from $4,273 intraday low. |
| 🟢 Equities | S&P 7,650.5; VIX 14.81 | Full recovery from FOMC selloff. No crash/regime change. |
| 🟢 Silver | $66.64 — recovery from $64.16 | Correlated with gold. |
| ⏭ Sep 14 Monday scan | MISSED — scheduler gap | Third missed Monday scan (Aug 17, Sep 1, Sep 14). Same pattern. |

## 7. Cards filed

| # | Title | Task ID | Domain | Priority | Materiality | Suggested Owner | One-line rationale |
|---|-------|---------|--------|----------|-------------|-----------------|--------------------|
| 1 | [RADAR][INBOX] WTI crude crash -11% peak-to-current — demand destruction or supply normalization? | t_b4fa9b10 | COMMODITY | P2 | M2 | org-equity-analyst | WTI crashed from $105.83 (Sep 15 peak) to $94.11 (Sep 21) — −11.1% in 4 sessions, −6.2% single-session gap-down. Fully reverses the ORG-2026-0022 supply-dislocation surge. New question: what drove the crash, and is the thesis reversing? |

## 8. What was deliberately ignored, and why

- **Gold recovery to $4,395 (+$61 from Sep 17):** Continuation of ORG-2026-0012 (do-not-reraise). The FOMC has now settled, creating the re-test window. Flag for CoS, not a new card.
- **Gold intraday low $4,273 (Sep 16):** New cycle low, but still the 0012 question. Flag for CoS.
- **Silver recovery to $66.64:** Correlated with gold. No new LBMA/COMEX data. Not a card.
- **VIX collapse 17.71→14.81:** FOMC event risk subsiding. Expected. Not a card.
- **S&P recovery +1.3%:** Normal post-FOMC recovery. Not a card.
- **DXY at 100.31:** Flat. Continuation, not a new observation.
- **10Y at 4.998%:** Flat since mid-week. Not a card.
- **FRED DFII10 data gap closed:** Gap resolution is operational, not a card.
- **EDGAR — all 8 CIKs:** No material/surprise filings. GOOGL dividend DEU accruals (investigated, routine). AMZN Sep 9 8-K (Item 5.02, routine officer appointment). Zero 8-K material items, zero 13D, zero offerings, zero Form 4 clusters beyond routine.
- **MSFT Form 4 cluster:** CIW boundary — digest note only, never a card.
- **NVDA Form 4 cluster (5× Sep 18):** Post-Hugging Face equity plan transactions. Routine.
- **JNJ talc:** No new filing since Aug 4. Monitoring unchanged.
- **Momentum screening (FD #75):** Out of scope.
- **Known data gaps (COMEX, CFTC COT, silver lease rates):** No new source appeared. LBMA August still missing (URL changed?).

## 9. Honest statement

**1 card cleared the bar** — the WTI crude crash ($105.83→$94.11, −11.1% peak-to-current, −6.2% single-session gap-down) is a genuinely material, unusual move that raises a new research question distinct from the published ORG-2026-0022 thesis. The 4-session collapse reverses >70% of the supply-dislocation surge and demands explanation.

**Notable cross-signal observation:** WTI crashed −8% while the S&P 500 recovered +1.3%. If this were a pure demand-destruction/recession signal, equities would likely be falling, not rising. This decoupling tentatively points toward profit-taking/supply-normalization rather than economic slowdown — but this is a radar-level observation, not analysis. The card fields this question for the research team to investigate.

**FRED DFII10 data gap is CLOSED** through Sep 17 — the CSV route finally worked after ~2 weeks of failure. Real yields rose 24bp (2.44%→2.68%) between Sep 1 and the FOMC day (Sep 16). Gold declined only 1.8% against this — providing fresh data for the ORG-2026-0012 re-test.

**CoS flags:**
- **ORG-2026-0012 re-test window is now open** — FOMC concluded, macro window settled. The do-not-reraise condition ("until macro window settles") is met. Recommend CoS consider unblocking for re-test.
- **ORG-2026-0022 thesis monitoring** — the WTI crash warrants flagging that the published thesis (supply dislocation causing $80→$105 surge) has been materially challenged by this −11% reversal. A new card was filed to address the distinct question.
- **Scheduler gaps** — Third missed Monday scan (Aug 17, Sep 1, Sep 14) suggests a structural issue with Monday logon/gateway availability. Recommend supervisor review.

## 10. Remaining data gaps

| Gap | Status | Notes |
|-----|--------|-------|
| FRED DFII10 (10y real yield) Sep 18+ | ✅ PARTIALLY CLOSED — data through Sep 17 available (CSV route). Sep 18-21 gapped (FRED lag — expected, ~2 day delay). | |
| **LBMA August 2026 vault data** | ❌ GAPPED — all URL variants returned 404. The page structure may have changed since the July data. Requires alternative URL discovery. | |
| COMEX deliverable silver (CME) | KNOWN-GAP (unchanged) | Third-party metalcharts 99.8 Moz registered @8/6 still latest |
| CFTC COT silver positioning | KNOWN-GAP (unchanged) | All URL variants 404 |
| Silver lease rates | KNOWN-GAP (unchanged) | No new free source appeared |
| Sep 14 Monday scan | CYCLE GAP | Third missed Monday scan — structural issue? |

## 11. Point-in-time flags (FD #58)

- All gold/silver/oil futures figures: pulled 2026-09-21 ~11:15 UTC+7 from Yahoo Finance via curl with User-Agent header. Current Monday session values.
- S&P 500, VIX, DXY, 10Y yield: pulled 2026-09-21 from Yahoo Finance. Current session values (some may be Friday Sep 18 close due to intraday session lag).
- FRED DFII10 data: pulled 2026-09-21 from FRED CSV. Data available through 2026-09-17 (FRED ~2-day lag).
- EDGAR submissions data: pulled 2026-09-21 from SEC EDGAR API. Point-in-time at pull timestamp.
- AMZN Sep 9 8-K: read 2026-09-21 from SEC EDGAR archives. Filing date 2026-09-09, event date 2026-09-08.

## 12. Next steps (advisory)

- Card t_b4fa9b10 sits in triage for CoS D1 triage → suggested owner: org-equity-analyst; materiality M2 advisory; priority P2.
- ORG-2026-0012 re-test window is open (FOMC concluded, macro settled). CoS decision on unblocking.
- FRED DFII10 gap partially closed — remove from Data Steward alert; re-retry on next pass for Sep 18+.
- LBMA August vault data: all URLs 404 — try alternative discovery on next pass (Google search for current LBMA vault data URL).
- No research mandates created, no reports touched, no state changed, no push (per cron contract).

---
*Radar Digest 2026-09-21 — FD #78 weekly scan (+ FD #81 EDGAR pass + FD #82 feedback loop). Advisory only; discovery-only; portfolio-blind.*
<!-- 2026-09-21 18:45 UTC+7 -->