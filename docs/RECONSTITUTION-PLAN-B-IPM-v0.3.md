# PLAN B — Independent Portfolio Manager Simulation (v0.3)

**Status:** Founder-amended (FD #64, 6 Aug 2026) — for approval: P-1, P-2. Minimum Simulated-Ledger Contract preserved from the v0.2 combined draft (Plan Council F3 fix).
**Version:** v0.3
**Date:** 2026-08-06
**Authority:** Founder direction `ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md` §11–17 · FD #64 (split amendment — IPM is a SEPARATE Founder-level project, NOT an IIP subsystem)
**Scope:** Read-only plan. No implementation, no live orders. Independent of PLAN A.
**Design objective:** Structure the operations, not the thinking.

---

## 1. Objective

A completely separate, Founder-level project: a simulated institutional portfolio office that manages a USD 200,000 internal simulated ledger, expresses independent views, and makes its judgment legible to the Founder through institutional prose. It is NOT an IIP subsystem, downstream consumer of IIP workflow, or exception under the IIP Constitution.

## 2. Separation (mandatory)

- **Own repository (recommended):** the IPM must not inherit IIP `AGENTS.md`, the IIP Constitution, IIP workflow authority, or the Founder Chief of Staff reporting line.
- **Own Hermes profile (recommended):** a separate profile (e.g. `ipm`) — never the `iip` profile, never the `org-*` profiles.
- **Own Constitution:** a new IPM Constitution authorizes autonomous decisions ONLY inside its USD 200,000 internal simulated ledger.
- Both IPM and IIP report to the Founder only. No organizational line connects them. The IPM may read published IIP reports only if the Founder makes them available — no required handoff, no dependency, may disagree completely.

## 3. Autonomy (explicit)

The IPM **may autonomously make and record simulated transactions WITHOUT prior Founder approval.** Every action MUST create an Investment Decision Letter and an append-only ledger record. **Remain prohibited: live orders, real accounts, real capital, broker credentials, and the Founder's actual portfolio** (the IPM never receives the Founder's real holdings, positions, cost basis, or transactions). Every transaction states: **SIMULATED PORTFOLIO — NOT A LIVE ORDER.**

## 4. Entity & Philosophy

- Simulated office, starting capital **USD 200,000**, multi-month/multi-year institutional orientation, NO day trading, NO obligation to be invested.
- Broad Mudley principles (not a rigid allocation formula): survival before return; main army + opportunistic forces (opportunistic must not destroy the main portfolio); Close System thinking as philosophy/tool, not mandatory strategy; buffer before expansion; multiple strategies, one portfolio; position management over prediction; freedom to hold cash; no artificial activity.
- Team: Portfolio Manager (sole decision-maker) + up to 3 bounded assistants (Portfolio Research / Structure & Risk / IBKR Instrument & Ledger). Assistants advise; the PM decides.

## 5. Minimum Simulated-Ledger Contract (PRESERVED — governs accounting integrity)

- **Opening balance:** USD 200,000 cash, single-currency USD base; no other assets at inception.
- **Append-only record:** every simulated transaction, correction, and valuation adjustment is an append-only journal entry (timestamp, entry id, immutable reference to its decision letter or correction note). Corrections are new entries, never edits.
- **Deterministic reconciliation:** cash, positions, realized/unrealized results, reserves, and committed obligations DERIVED from the journal by deterministic rules — never stored as opaque state. A no-trade opening ledger must reconcile exactly to USD 200,000.
- **Required per-entry fields:** instrument identifier; IBKR-eligibility verification reference (§6); exchange; currency; contract multiplier; expiry (if applicable); quantity (full units — no fractional-share assumptions); simulated fill price; simulated fill basis; fees; FX rate (non-USD legs); timestamp; decision-letter reference. **Missing eligibility evidence → NO ledger entry (fail-closed).**
- **Capital classification (direction §13.4):** original capital vs realized profit vs released capital vs reserve vs available cash vs committed obligations as derived categories.
- **Explicit exclusions:** no broker credentials, no live-account data, no live-order connectivity, no real-time market feed requirements — fills are simulated from verified reference prices.

## 6. IBKR Eligibility Verification

Never assume availability. The IBKR assistant verifies contract/exchange/currency/multiplier/expiry per instrument before any simulated transaction:
1. Baseline: re-verify (per FD #58) the verified facts in the separate workspace `Grid Trading System for IBKR\docs\RESEARCH.md` (2026-07-10) — order limits (20 active/contract/side), API pacing, `ib_async` v2.1.0 (not ib_insync), `cashQty` Forex-only → full-share sizing, minTick/multiplier discipline, whatIfOrder validation, paper port 7497.
2. Primary source: IBKR official public documentation — `interactivebrokers.github.io/tws-api` + public contract search.
3. Optional later: TWS Paper (port 7497) — requires Founder approval + install; not needed to start.
4. Verification note attaches to every Investment Decision Letter involving a new instrument.

## 7. Minimum Outputs (three artifacts only)

- **Portfolio Finding Letter** — when the team discovers something that materially changes its understanding, even with no transaction
- **Investment Decision Letter** — for every initiate/add/reduce/close/hedge/replace/restructure/deliberate no-action (thesis, mechanism, timing, instrument choice, portfolio interaction, strongest counter-case, uncertainty, what would change the decision)
- **Portfolio Manager Letter** — weekly: how the Manager sees the portfolio, what changed, where risk concentrates, what it is waiting for, why it acted or stayed inactive

Institutional prose; auditable rationale; NO hidden chain-of-thought; no Buy/Sell/Hold-only responses.

## 8. Initial Cadence (pilot-limited)

| Active now | Deferred until pilots demonstrate value |
|---|---|
| Weekly Portfolio Review (one Portfolio Manager Letter) | Daily Material Portfolio Watch |
| Event-driven Review (thesis-changing event, dislocation, structural change, instrument failure, liquidity change, risk concentration, new opportunity) | Monthly Structure Review |

## 9. Repository

Separate repo (recommended) with own tree: `philosophy/ research/ findings/ decisions/ portfolio-ledger/ weekly-letters/ postmortems/ roles/`. If the Founder prefers a single repo, the two trees stay fully separate in authority and workflow.

## 10. Approval Request (this plan — 2 decisions)

- **P-1 — Approve separate IPM project: USD 200,000 simulation, Mudley philosophy, and the Minimum Simulated-Ledger Contract** (§1–§6)
- **P-2 — Approve first IPM pilot and initial cadence** (§7–§8)

## 11. Explicit Non-Authorization

This plan does NOT authorize: live orders, real accounts, real capital, broker credentials, access to the Founder's actual portfolio, day trading, obligation to be invested, integration into IIP governance or the IIP repo authority, authority over IIP research, deletion of anything, or building a trading platform.

## 12. Verification (when implementation is later authorized)

- No-trade opening ledger reconciles to USD 200,000
- One representative multi-currency/derivative simulation reconciles journal ↔ cash ↔ positions ↔ obligations ↔ letter references with zero live-order path
- Every letter references its ledger entries and vice versa (grep)
- No IIP file, profile, or authority referenced anywhere in the IPM tree

<!-- 2026-08-06 18:30 UTC+7 -->
