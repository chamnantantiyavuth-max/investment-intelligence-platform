# Radar Mid-Week Watch Note — 2026-09-10 (FD #80 cron)

**Role:** Radar Scout (role 11, `org-radar-scout`) — discovery only, portfolio-blind, no analysis/recommendation.
**Run:** 2026-09-10 (Thu), pulls ~09:30–09:52 UTC+7 (02:30–02:52 UTC).
**Continuity:** Read `2026-09-07-radar-digest.md` (Monday weekly scan — 1 card filed t_72053221).
**Run task:** t_0252bb19 (board `[DISC] IIP Radar Mid-Week Watch 2026-09-10`)
**Result:** 0 Task Idea Cards filed — nothing cleared the bar this pass.
**Status:** Advisory only. No state change. Figures point-in-time per FD #58 — valid at the pull timestamp, re-verify before reliance.

## 1. What changed since the Monday digest (one-line bullets)

| Series | Sep 7 (Monday) | Sep 10 (this pass) | Change | Notable? |
|--------|---------------|--------------------|--------|----------|
| Gold (GC=F) | $4,476.6 | **$4,457.5** | −$19.1 / −0.4% | Modest decline; within $4,430-4,490 range flagged Monday |
| Silver (SI=F) | $66.75 | **$68.085** | **+$1.34 / +2.0%** | Slight outperformance vs gold; Volcker rule/regulation timing? |
| Gold/silver ratio | ~67.1 | **~65.5** | −1.6 | Modest compression; not regime change |
| WTI crude (CL=F) | $91.48 | **$96.46** | **+$4.98 / +5.4%** | **🔴 MOST NOTABLE MOVE** — oil broke $100 intra-period per headlines (AP/Reuters/CNBC: "US-Iran new attacks", "$101/barrel") |
| S&P 500 | 7,718.60 | **7,636.36** | −82.2 / −1.1% | Modest pullback; no crash |
| VIX | 14.53 | **16.46** | **+1.93 / +13.3%** | Notable volatility increase — FOMC anxiety + oil escalation |
| DXY | 99.18 | **98.76** | −0.42 / −0.4% | Slight dollar weakening |
| 10Y nominal (^TNX) | 4.784% | **4.837%** | **+5.3bp** | Yields extending rise; 4.857% 52-week high touched intra-day |
| Real yields (DFII10) | 2.44% (Sep 1) | ⚠ GAPPED (still timeout) | — | FRED CSV route timed out again; Sep 1 data is now 9 days stale |

### Key narrative drivers (sourced)
- **Oil past $100:** Multiple news sources report oil surged past $100/barrel on renewed US-Iran attacks. AP News (Sep 8): "Oil surges above $100 a barrel as US and Iran launch new attacks, while gasoline prices also jump." Reuters (Sep 9): "Oil pushes past $100 as wave of US-Iran attacks exposes dwindling safety net." CNBC (Sep 8): "Oil rises to $99 on report Iran launched second undisclosed attack on U.S. Navy ships." Reuters (Sep 10): "Oil ends week higher on renewed US-Iran strikes, diesel hits record." This material escalation validates the ORG-2026-0022 thesis (IEA OMR-quantified supply dislocation) but at an intensity not fully captured in the IEA baseline.
- **EIA STEO:** Reuters (Sep 8): "US EIA hikes oil price forecasts as Iran war drains global stockpile" — new agency forecast data released between Monday and this pass.
- **10Y yield at 52-week high:** ^TNX touched 4.857% intra-day, just below the 52-week high. Yields rising on oil→inflation expectations (breakevens) + FOMC tightening fear.
- **VIX spike:** +13.3% from Monday, reflecting both FOMC (Sep 16-17) and oil/macro uncertainty. Not a crash signal yet (VIX 16.46 is elevated but not panic).

## 2. Data-gap retries and outcome (per card-outcomes.md retry policy)

| Gap (from register/digest) | Retry outcome |
|---------------------------|---------------|
| **FRED DFII10 (10y real yield) 9/2+** | ❌ **STILL TIMEOUT** — both curl (empty) and Python `urllib` (timeout after 20s) failed this pass. CSV route worked Sep 3 (latest 2.44% @ Sep 1). Sep 1→10 gap now extends to ~9 days. SUGGEST Data Steward D2: alternative CSV URL or FRED API key. |
| **LBMA vault August 2026** | ⏭ Not yet published (~mid-Sept) — ACTIVE monthly item, auto-retry after publication. |
| **COMEX deliverable silver (CME)** | ❌ KNOWN-GAP unchanged. Third-party metalcharts 99.8 Moz registered @8/6 still latest. |
| **CFTC COT primary (silver positioning)** | ❌ KNOWN-GAP unchanged. All URL variants 404. |
| **Silver lease rates** | ⏭ KNOWN-GAP unchanged. No new free source appeared. |
| **Sep 1 Monday scan missed** | ✅ CYCLE GAP CLOSED by Sep 7 scan. |

## 3. EDGAR delta outcome (FD #81 — filings since 2026-09-07 digest pass)

**8/8 CIKs screened (window 9/8–9/10). 0 cards filed.** Rate-limited ~3s between calls.

| CIK | Company | Filings in window (≥ Sep 8) | Material/unusual? | Card? |
|-----|---------|----------------------------|-------------------|-------|
| 0000320193 | AAPL | None | — | No |
| 0000789019 | **MSFT** | PX14A6G (9/9), **12× Form 4 (9/8)** | PX14A6G = shareholder proposal (non-management proxy material). 12× Form 4 cluster = equity plan settlement (beginning of fiscal year Q1 pattern, same as Sep 1 cluster). | **No** (CIW boundary — digest note only) |
| 0001045810 | NVDA | Form 4 (9/8) | Single insider filing. | No |
| 0001652044 | GOOGL | None | — | No |
| 0001018724 | **AMZN** | **8-K (9/9, Item 5.02), FWP (9/9), 424B5 (9/9), 2× Form 4 (9/9), Form 3 (9/9)** | **8-K = MULTI-TRANCHE NOTE ISSUANCE:** Amazon registered 8 tranches of notes for listing on Nasdaq under its S-3 shelf (Registration No. 333-23795): Floating Rate Notes due 2028, 2.800% due 2028, 3.100% due 2030, 3.350% due 2032, 3.700% due 2035, 4.050% due 2039, 4.450% due 2045, 4.850% due 2064. 424B5 = prospectus supplement for the offering. FWP = free writing prospectus. Likely a new debt issuance ($5-15B estimated range). | **No** — routine corporate capital management for AA-rated company; not unusual/moment-changing. |
| 0001326801 | META | Form 4 (9/8), 2× 144 (9/8, 9/9) | Routine insider/plan filings. | No |
| 0001318605 | TSLA | Form 4 (9/9), 144 (9/8) | Single insider filing. | No |
| 0000200406 | JNJ | None | — | No |

### Key EDGAR notes (no cards)

- **AMZN multi-tranche note issuance (Sep 9):** Amazon tapped its shelf to issue 8 tranches of notes (2028-2064 maturities). Coupons from floating rate to 4.850% for the 40-year tranche. This is a significant debt raise — Amazon has been a frequent bond issuer and has ~$200B+ of total debt. The timing (higher rate environment, 10Y at ~4.8%) is moderately interesting but not unusual for a company managing its capital structure. **Digest note only.**
- **AMZN Form 4 + Form 3 (Sep 9):** New insider filings likely related to the note issuance (new board member or officer submitting initial holdings). Not material.
- **MSFT PX14A6G (Sep 9):** Shareholder proposal notice (non-management proxy material). Detail not read (CIW boundary — digest note only, never a card). The 12-Filing Form 4 cluster on Sep 8 mirrors the Sep 1 pattern — beginning-of-fiscal-year equity plan settlement.
- **NVDA Form 4 (Sep 8):** Single insider. Likely post-acquisition filing (Form 3 from Sep 3 followed by Form 4). Not a card.

## 4. Cards filed

**Zero cards — nothing cleared the bar this pass.**

Rationale:
- **Oil surge to $96.46 (+$4.98 / +5.4%), headlines of $100+:** This is the most noteworthy observation of the week. However, ORG-2026-0022 (IEA OMR dislocation thesis) was filed, researched, and published. The current price action is material validation of that published thesis — the US-Iran attack escalation (Reuters/AP/CNBC) and EIA STEO hike are NEW evidence, but the core research question (does this dislocation change the macro/inflation transmission?) was already answered. Monitoring conditions from the published report should capture this escalation. **No new card — continuation of published question. Exceptionally flagged for Monday scan re-assessment.**
- **AMZN multi-tranche note issuance:** Routine for Amazon. Amazon is a regular bond issuer with ~$200B+ debt. Eight tranches is a larger offering but without unusual terms. **No card.**
- **MSFT PX14A6G + Form 4 cluster:** CIW boundary (never a card). Digest note only.
- **10Y yield at 4.837% (52-week high intra-day 4.857%):** Continuation of the yield rise trend noted Sep 3 and Sep 7. FOMC Sep 16-17 approaching. Feeds ORG-2026-0012 (do-not-reraise) — the yield rise explains gold's recent underperformance. **No card — feeds existing question.**
- **Gold $4,457.5:** Within the $4,430-4,490 consolidation range identified Monday. Continuation, not new. **No card.**
- **VIX spike to 16.46:** Symptom of oil/macro/FOMC uncertainty, not a research question. **No card.**
- **No momentum screening** (FD #75).
- **NVDA Hugging Face card (t_72053221, filed Sep 7):** RE-VERIFIED this pass — the card IS present on the board (status done, assignee iip, completed Sep 7 12:13). The not-found flag in this digest's earlier draft was a board-listing check issue; card confirmed present. Board hygiene OK.

## 5. Event triggers (workflow §4 list)

| Trigger | Status | Impact assessment |
|---------|--------|-------------------|
| 🔴 **US-Iran military escalation** | **NEW EVENT** (Sep 8-10) | Renewed attacks, Houthi Saudi strikes, Iran 2nd undisclosed attack on US Navy. Oil surged past $100. EIA hiked forecasts. **This is the most material event trigger since the weekly scan.** Validates ORG-2026-0022 thesis; escalates the risk profile beyond the IEA OMR baseline. |
| 🔴 **FOMC** | **Sep 16-17 meeting — 6 days away** | Approaching; VIX +13%, 10Y at 52-week highs, oil feeding inflation fears. ORG-2026-0012 re-test window may now be opening. |
| 🟡 **Oil at $96.46 (headlines $100+)** | Escalation of existing dislocation | See above. Continuation of published thesis at higher intensity. |
| 🟡 **10Y at 4.837% (52-week high)** | Yields rising | FOMC week next; oil→inflation→yield transmission is the critical question. |
| 🟡 **VIX +13.3%** | Volatility increasing | Not panic level, but the direction is notable ahead of FOMC. |
| 🟢 Equities | S&P 500 −1.1% | Modest pullback; no crash/regime change. |
| 🟢 Gold/Silver | Minor moves | Consolidation phase. |

**Orange-red triggers present this pass:** US-Iran military escalation (oil surge) is the most material change since Monday.

## 6. What was deliberately ignored, and why

- **Oil surge as a new card:** As above, continuation of ORG-2026-0022 published thesis. The research has been published; monitoring conditions exist. The escalation to $100+ is noted for Monday re-assessment but does not clear the bar for a genuinely new question independent of the existing published work.
- **AMZN note issuance:** Routine corporate capital management. Amazon is a frequent bond issuer. No unusual terms or structure.
- **MSFT PX14A6G:** CIW boundary (never a card).
- **Gold consolidation:** ORG-2026-0012 do-not-reraise respected. FOMC approaching could be a re-test window — CoS decision.
- **VIX spike:** Symptom of oil/macro events, not a research question.
- **Routine Form 4s:** Single insider filings, plan settlements. Below the bar.
- **NVDA Form 4:** Single filing post-acquisition. Not unusual.
- **FRED DFII10 gap not retried beyond the Python/curl attempt:** Both failed. Data Steward D2 intervention needed.
- **Momentum screening (FD #75):** Out of scope.

## 7. Honest statement

**Zero cards this pass, and I believe that's the correct output.** The most material observation — oil surging past $100 on renewed US-Iran attacks — is continuation of the ORG-2026-0022 published thesis at an escalated intensity. The research question (does the oil dislocation change macro/inflation transmission?) was answered in the published work. Monitoring conditions should capture the current escalation. If this week's Monday scan also filed no fresh card for the same escalation (it was at $91 then), that consistency supports this judgment.

EDGAR produced routine or CIW-bounded filings. Standing series: oil is the story; everything else is continuation/consolidation ahead of FOMC.

**Notable for the Monday scan:**
1. Oil escalation past $100 deserves re-assessment at Monday — if the thesis's monitoring conditions don't capture this intensity, a new card may be warranted.
2. The NVDA Hugging Face card (t_72053221) IS present on the board (done, assignee iip) — the earlier not-found flag was a listing-check issue, now resolved.
3. FRED DFII10 data gap now extends ~9 days (Sep 1 latest). Data Steward D2 intervention recommended.
4. FOMC Sep 16-17 could be a re-test window for ORG-2026-0012 (gold vs real yields) — flag for CoS.

## Remaining data gaps

| Gap | Status | Notes |
|-----|--------|-------|
| FRED DFII10 (10y real yield) 9/2+ | ⚠ STILL GAPPED (~9 days) | CSV route failed (timeout again). Suggest D2 alternative. |
| COMEX deliverable silver (CME) | KNOWN-GAP (unchanged) | Third-party metalcharts 99.8 Moz registered @8/6 still latest. |
| CFTC COT silver positioning | KNOWN-GAP (unchanged) | All URL variants 404. |
| Silver lease rates | KNOWN-GAP (unchanged) | No new free source appeared. |
| LBMA August 2026 vault data | ACTIVE (monthly cadence) | Due ~mid-Sept. Next Monday scan. |
| NVDA Hugging Face card t_72053221 persistence | ✅ RESOLVED | Re-verified this pass — card present on board (done, assignee iip). No board-hygiene gap. |

## Verification note (this finalization pass)

- Figures re-pulled 2026-09-10 ~09:52 UTC+7 from Yahoo Finance (GC=F, SI=F, CL=F, ^GSPC, ^VIX, DX-Y.NYB, ^TNX) — match digest values: S&P 500 7,636.36, VIX 16.46, DXY 98.746, 10Y 4.837 exact; gold/silver/oil within tick.
- EDGAR delta re-verified 2026-09-10 against SEC submissions API for all 8 CIKs — matches digest table exactly (AMZN 8-K/FWP/424B5 9/9, MSFT PX14A6G 9/9 + 12× Form 4 9/8, NVDA Form 4 9/8, META/TSLA routine, AAPL/GOOGL/JNJ none).
- NVDA card t_72053221 confirmed present on iip board (done) — earlier not-found flag was a listing-check issue, resolved in this pass.
- Header/footer pull-time stamps corrected to reflect actual pull window (~09:30–09:52 UTC+7), per FD #58 point-in-time discipline.

---

*Radar Mid-Week Watch Note 2026-09-10 — FD #80 mid-week watch (+ FD #81 EDGAR delta + FD #82 feedback loop). Advisory only; discovery-only; portfolio-blind. Figures point-in-time per FD #58 (verified 2026-09-10 ~10:20 UTC+7).*
<!-- 2026-09-10 10:20 UTC+7 -->