# CIW Monitoring Note — MSFT (CRR-2026-0001)

**DRAFT — PENDING FOUNDER REVIEW**

> **NO NEW FILINGS — baseline unchanged.** Last observation: 2026-08-24 11:26 UTC+7 (Cron Class A weekly tick). This tick: 2026-08-31 09:38 UTC+7. No new SEC filings since the FY26 10-K / 8-K pair (2026-07-29) captured in research-result v1 (as-of 2026-08-03). All indicator values below are the v1 baseline; only I-12 (market price) is refreshed this tick. Contract: CIW-MONITORING-CONTRACT.md v0.1 (FD-CIW-013/014; contract file not found in repo per QAD pivot — format follows established precedent from prior monitoring drafts).

## 1. Data Points (I-1..I-14)

| ID | Indicator | Value (baseline v1) | Source lineage | Retrieval date |
|---|---|---|---|---|
| I-1 | Commercial RPO (total) | $678B (+84% YoY) | SRC-001 (10-K FY26 Note 12); SRC-003t (Q4 FY26 call) | 2026-08-03 (baseline; no new filing) |
| I-2 | Commercial RPO growth ex-OpenAI | +25% YoY | SRC-003t (earnings call disclosure) | 2026-08-03 (baseline) |
| I-3 | Microsoft Cloud revenue + growth | $214.4B FY26 (+27%); ~90% ex-frontier-model customers | SRC-001 (10-K MD&A); SRC-003a (call) | 2026-08-03 (baseline) |
| I-4 | Azure and other cloud services growth | +41% FY26; Q1-FY27 guided ~45% CC | SRC-003a/t (call) | 2026-08-03 (baseline) |
| I-5 | Capex (additions to PP&E) | $115.9B FY26; ~$175B CY26 guided (post reclassification) | SRC-001 (10-K cash flow) | 2026-08-03 (baseline) |
| I-6 | Incremental ROIC proxy (ΔNOPAT / Σ(capex−D&A), FY23 base) | FY26 input data published in research-draft §6; **annual — first read FY27** | SRC-XBR (companyfacts) | 2026-08-03 (baseline; not evaluated) |
| I-7 | OCF, FCF, FCF margin | OCF $182.9B; FCF $67.0B; FCF margin 20.2% | SRC-XBR (companyfacts) | 2026-08-03 (baseline) |
| I-8 | Operating margin | 46.8% FY26 | SRC-XBR (companyfacts) | 2026-08-03 (baseline) |
| I-9 | M365 Copilot paid seats | >30M (Q4 FY26); net adds 2× QoQ | SRC-003t (call) | 2026-08-03 (baseline) |
| I-10 | M365 Commercial seats growth | +6% YoY | SRC-003t (call) | 2026-08-03 (baseline) |
| I-11 | Share count (diluted) | 7.45B | SRC-XBR (companyfacts) | 2026-08-03 (baseline) |
| I-12 | Market price + trailing P/E | **$513.53 (refreshed this tick); trailing P/E ~25.9× (baseline, not refreshed — no new filings)** | SRC-MKT (Yahoo chart API via ciw_msft_monitor.py); refreshed 52wk high $553.72 / low $349.20 | **2026-08-31 09:38 UTC+7 (refresh)** |
| I-13 | Regulatory / legal events | IDPC LinkedIn appeal pending ($553M accrued; ~$400M reasonably possible); EU/US antitrust scrutiny ongoing | SRC-001 + public proceedings (baseline) | 2026-08-03 (no new event this tick) |
| I-14 | Platform-control signals | None observed at baseline | Filings + regulatory orders (baseline) | 2026-08-03 (no new event this tick) |

*Price note: $513.53 is 7.3% below the 52-week high of $553.72 — the −25% WATCH band is NOT breached. Prior tick price $483.24 (2026-08-24); price increased ~+6.3% since the last observation. The 52-week low of $349.20 implies ~+47.1% range from current.*

## 2. Falsification-Trigger Status (contract §4)

| Module J condition | Indicators | State | Basis |
|---|---|---|---|
| (1) ex-OpenAI demand/backlog collapse | I-1, I-2, I-3 | **NO TRIGGER** | RPO ex-OpenAI +25% (positive; requires 2 consecutive negative quarters for trigger); Cloud +27%, ex-frontier-model ~90% (subgroup growth NOT disclosed — flagged) |
| (2) incremental AI-capital return failure | I-5, I-6 | **NO TRIGGER** | Annual evaluation only; first read FY27–FY29 window; capex $115.9B < OCF $182.9B (no capex>OCF breach) |
| (3) structural loss of platform control | I-13, I-14 | **NO TRIGGER** | No new regulatory order; no migration/seat-decline evidence |

**Overall: NO TRIGGER** across all conditions. No WATCH, no TRIGGER CANDIDATE this tick.

## 3. Early-Warning Status (contract §5)

| Indicator | WATCH threshold | Current | Status |
|---|---|---|---|
| I-2 RPO ex-OpenAI growth | <5% YoY | +25% | ✅ clear |
| I-4 Azure growth | <20% CC | +41% (guided ~45% CC Q1-FY27) | ✅ clear |
| I-5 Capex vs OCF | capex > OCF 2 consecutive qtrs | $115.9B < $182.9B | ✅ clear |
| I-6 Incremental ROIC | <12% | not yet measurable (annual) | ⏳ first read FY27 |
| I-8 Operating margin | <44% | 46.8% | ✅ clear |
| I-12 Price | 52wk high −25% (= $415.29) | $513.53 (−7.3% from high; within band) | ✅ clear (valuation context only — never a trigger by itself) |
| I-13/I-14 | proceeding escalated / remedy proposal | no change this tick | ✅ clear |

## 4. Unresolved-Questions Update (contract §7)

| # | Question | Status this tick |
|---|---|---|
| 1 | Does the AI capex build earn >WACC? (I-5/I-6) | **Remains open** — annual; first read FY27 |
| 2 | OpenAI-independent growth durability (I-2/I-3) | **Remains open** — subgroup growth NOT disclosed; flagged per contract |
| 3 | Moat mechanism verification at customer level | **Remains open** — no public source |
| 4 | Regulatory outcomes (I-13) | **Remains open** — no new event this tick |
| 5 | Accounting-optics: useful-life extension effects (I-8) | **Remains open** — next read at Q1-FY27 filing (Oct 2026) |
| 6 | Commitment-stack precision (lease overlap) | **Remains open** — needs underlying schedules |

## 5. Audit Fields

| Field | Value |
|---|---|
| Prior state | `Draft` (2026-08-24 monitoring note) |
| New state | `Draft` (pending Founder review) |
| Actor | Cron Class A observer (CIW Module Q; FD-CIW-005/013) |
| Timestamp | 2026-08-31 09:38 UTC+7 |
| Workflow version | CIW v0.2 + monitoring contract v0.1 |
| Data source | `ciw_msft_monitor.py` (exit 0; `new_filings: false`; `note: NO NEW FILINGS — baseline unchanged (research-result v1, 2026-08-03)`; price_refresh $513.53 / 52wk $553.72–$349.20) |

---

*Observation only — advisory. This note never changes official Candidate/Thesis/Theme/Moat/Earnings-Quality/Value-Trap/Investment state. No buy/sell/hold or portfolio action is proposed or implied. TRIGGER CANDIDATE, had one occurred, would route to Founder review only.*
<!-- 2026-08-31 09:38 UTC+7 -->