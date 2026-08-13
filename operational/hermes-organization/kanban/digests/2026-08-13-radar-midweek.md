# Radar Mid-Week Watch Note — 2026-08-13 (FD #80 cron)

**Role:** Radar Scout (role 11, `org-radar-scout`) — discovery only, portfolio-blind, no analysis/recommendation.
**Run:** 2026-08-13 (Thu), pulls ~04:35–05:15 UTC (11:35–12:15 UTC+7). Continuity: read `2026-08-10-radar-digest.md`.
**Result:** 1 Task Idea Card filed (ORG-2026-0022) → kanban Inbox, awaiting CoS triage.
**Status:** Advisory only. No state change. Figures point-in-time per FD #58 — valid at the pull timestamp, re-verify before reliance.

## 1. What changed since the Monday digest (one-line bullets)

- **Gold:** futures 4,361.8 (8/10) → **4,456.6 (8/13)** (+2.2%, new high for the move; +10.5% from 4,033.70 on 8/3); spot XAU 4,398.70 (gold-api 8/13 04:40 UTC) vs 4,335.40 (8/10) = +1.5%. Rally held through the CPI release.
- **Silver:** futures 65.11 (8/10) → 65.45 (8/13); spot XAG 65.417 vs 63.976 = +2.3% — new high for the recovery move.
- **Gold/silver ratio:** spot-implied ~67.2 (4,398.70/65.417) vs ~67.7 (8/10) — mild compression, no regime move.
- **Dollar (DXY):** 99.81 (8/10) → **100.01 (8/13)** — firmed slightly off the ~2-month low, no reversal.
- **Real yields (DFII10):** ✅ **FRED caught up** — 8/7 (2.40), 8/10 (2.43), 8/11 (2.43) now present; latest 2.43% (8/11) ≈ flat vs 2.43 (8/6). Gap RESOLVED.
- **10y nominal (^TNX):** 4.70 (8/10) → 4.68 (8/12) — steady.
- **Equities/vol:** S&P 500 7,753.11 (8/10) → 7,748.50 (8/12); VIX 15.46 → 14.55 — calm, near records; no anomaly.
- **Oil (WTI CL=F):** **the week's notable standing move** — 78.71 (digest @8/10) → **82.96 (8/13 close)**; +10.7% off the 8/5 low (75.22), highest of the standoff (see §4 card).

## 2. Data-gap retries and outcome (per card-outcomes.md retry policy)

| Gap (from register/digest) | Retry outcome |
|---|---|
| **FRED DFII10 8/7+** | ✅ **RESOLVED** — 8/7–8/11 now in CSV (2.40/2.43/2.43); latest 2.43% (8/11). Next pass: re-check 8/12+. |
| **LBMA vault August 2026** | ⏭ Not yet published (July resolved 8/10; August ~mid-Sept) — ACTIVE monthly item, auto-retry after publication. |
| **COMEX deliverable silver (CME)** | ❌ One-shot attempt still **403** → KNOWN-GAP unchanged (third-party metalcharts 99.8 Moz registered @8/6 still latest; Data Steward D2 confirmation still open). |
| **CFTC COT primary (silver positioning)** | ❌ Still **404** (all variants) → KNOWN-GAP unchanged; Finimize 8/9 "2-year bullish extreme" claim remains UNVERIFIED. |
| **Silver lease rates** | ⏭ Not retried — no new free source appeared (news scan returned only stale Jan–Jun 2026 items) → KNOWN-GAP unchanged. |

## 3. EDGAR delta outcome (FD #81 — filings since the 8/10 Monday pass)

**No new material/surprise filings.** 8/8 CIKs screened (window 8/11–8/13 + 8/10 late-day):

- **GOOGL 8-K (8/10, items 8.01/9.01)** — read: **expected closing of the $25B 10-tranche debt offering** (A2.375 2028 → A5.500 2041, A4.000 2044, A3.875 2045 + 6.25% Series A/B Mandatory Convertible Preferred; settle 8/10). Completion of already-filed ORG-2026-0017 — NOT a new event. Plus routine Form 4 (8/11).
- **NVDA Form 4 (8/12)** — director Suzanne M. Nora Johnson, initial board-grant RSUs (1,262 + 1,148 sh, "initial grant in connection with appointment to the Board") — a grant, not a sale; routine.
- **META Form 4 (8/12) + 144 (8/10)**, **AMZN Form 4 (8/10)** — routine insider filings, below the bar.
- **AAPL 144 (8/11)** — routine Rule 144 notice.
- **JNJ N-PX (8/11)** — annual routine (same late-Aug pattern 2024/2025/2026); no talc-participation update (0015 monitoring unchanged).
- **MSFT / TSLA** — nothing in window. **MSFT digest note only (CIW boundary, FD #81): quiet — no new filings since 8/10.**
- **13F-HR season (Q2, due 8/14):** GOOGL filed 8/6 (noted Monday); others not yet in window — routine season, no card.

## 4. Cards filed

- **ORG-2026-0022** (COMMODITY, P2, M2, org-commodity-analyst) — WTI +10.7% in five sessions (75.22 → 83.27) on the Hormuz standoff while the US claims flows "recovered to 15M bbl/day" (8/11) yet warns of disruptions into 2027 (8/11); Bloomberg counters "the Strait isn't closed" (8/13). Raises: is the oil premium pricing a real persistent supply loss, or narrative against normalized flows — and what does the answer do to the inflation/rate backdrop feeding 0012 and 0016? *One-line rationale: an unusual ~11% weekly move (workflow §4 supply-disruption/volatility trigger) on directly conflicting official-market flow claims — a distinct question from Monday's context-only Hormuz treatment, with a new evidence base since then.*

## 5. What was deliberately ignored, and why

- **Gold's continued rally to new highs (futures 4,456.6)** — that is ORG-2026-0012's live question (do-not-reraise). CPI is now OUT (8/12: July +0.1% m/m, 3.4% annual, as expected; September-hike odds plunged) but **Hormuz is still live** → **0012's re-test window is PARTIALLY open; flagged for CoS triage to consider re-testing 0012, no new card.**
- **July CPI print itself** — an explained macro event that explains the gold/silver/dollar context; feeds 0012/0022, not an anomaly.
- **Hormuz as gold-context** (for 0012/0016) — same logic as Monday; the oil *price-vs-flows* question is the new, separate item (§4).
- **13F-HR season filings** — routine institutional season.
- **Routine Form 4s/144s (NVDA grant, META, AMZN, GOOGL, AAPL)** — no officer/board concentration, no signal.
- **Momentum screening** — out of scope by FD #75.

## 6. Honest statement

One card cleared the bar — the oil price-vs-physical-flows conflict, which is new since Monday (the move extended +5.5% and the flow-recovery/disruption-2027 claims both landed 8/11). Everything else in the standing series (gold, silver, dollar, real yields) moved with or after the CPI print in an *explained* direction — continuation of 0012/0016 territory, not new anomalies. EDGAR produced nothing above routine. This is a quiet-but-not-empty mid-week pass.

## Remaining data gaps

COMEX deliverable silver (CME 403 — third-party 99.8 Moz @8/6 still latest); CFTC COT (404; Finimize claim unverified); silver lease rates (no free source); LBMA August vault data (publication ~mid-Sept); FRED DFII10 8/12+ (may lag again). All fed to the next Monday scan.

---
*Radar Mid-Week Watch Note 2026-08-13 — FD #80 mid-week watch (+ FD #81 EDGAR delta + FD #82 feedback loop). Advisory only; discovery-only; portfolio-blind.*
<!-- 2026-08-13 12:20 UTC+7 -->
