# Company Intelligence Workbench — Monitoring Contract (Module Q) — MSFT

**Status:** APPROVED v0.1 — Founder approval recorded 2026-08-03 (Option A; approved content SHA-256 `d7ef7168cc3fe89d37ad880a1f828f6ef31a968cb1f3c1cb64b6f661ecfa64e3`, Constitution §21). The observation job (Cron Class A, `ciw-msft-class-a-monitor`) is LIVE as of this approval. Status-metadata update only — analytical content unchanged from the approved version.
**Approval record:** prior state `Draft (for approval)` → `Approved`; actor: **Founder** (Option A, session 2026-08-03); evidence: this document + FD-CIW-014; timestamp 2026-08-03; workflow version: CIW v0.2 + monitoring contract v0.1.
**Version:** 0.1 (approved)
**Date:** 2026-08-03
**Owner:** Founder
**Authority:** FD-CIW-013 (Phase 11 implementation slice — Module Q monitoring contract + Cron Class A); FD-CIW-005 (Class A = scheduled observation, output always draft/pending review, never official promotion); CIW-CONCEPT §6 (monitoring deferred to later slice — this contract opens it); CIW-RESEARCH-FRAMEWORK §3 Module Q; `docs/ciw-pilot-msft/research-result.md` v1 (Module J falsification conditions — trigger basis)
**Derived from:** RESEARCH-FRAMEWORK Module Q (Monitoring and Falsification); research-result v1 Module J falsification conditions; CRR-2026-0001 justified omission (Module Q deferred at research time, now opened by FD-CIW-013)

---

## 1. Status: Advisory Monitoring, Not Operational Standard

- This contract defines **observation indicators and review triggers** for the published MSFT research result (CRR-2026-0001 v1). It is **advisory only**.
- Monitoring output **never changes** official Candidate, Thesis, Theme, Moat, Earnings-Quality, Value-Trap, or Investment state (LIFECYCLE §4; FD-CIW-013).
- Falsification-trigger candidates **route to Founder review** — they never auto-execute anything (FD-CIW-005/013; Constitution §23).
- A monitoring note is a **draft** until the Founder acknowledges it; acknowledgement records audit fields, it does not create an authoritative state.

## 2. Scope

- **Company:** MSFT (CIK 0000789019) — the published pilot company.
- **Job class:** ONE Cron Class A scheduled observation job (weekly tick; quarterly data-point collection when filings land).
- **Data sources:** SEC EDGAR (submissions API, XBRL companyfacts, filings), market quote (Yahoo Finance chart API), Microsoft IR (transcripts for narrative items).
- **Out of scope (NOT authorized):** Cron Class B/C, Obsidian sync, DB/schema, expanded tree, Master Paper, new repo/profile, earnings automation, valuation contracts, official state changes, autonomous action.

## 3. Indicator Set (measured against research-result v1 baseline, as-of 2026-08-03)

| ID | Indicator | Frequency | Source | Baseline (v1, FY26 / 2026-07-31) |
|---|---|---|---|---|
| I-1 | Commercial RPO (total) | Quarterly | 10-Q/10-K Note 12 + earnings call | $678B (+84% YoY) |
| I-2 | Commercial RPO growth ex-OpenAI | Quarterly | earnings call disclosure | +25% YoY |
| I-3 | Microsoft Cloud revenue + growth | Quarterly | 10-Q/10-K MD&A + earnings call | $214.4B FY26 (+27%); ~90% ex-frontier-model customers |
| I-4 | Azure and other cloud services growth | Quarterly | earnings call | +41% FY26; Q1-FY27 guided ~45% CC |
| I-5 | Capex (additions to PP&E) | Quarterly | 10-Q/10-K cash flow / XBRL | $115.9B FY26; ~$175B CY26 guided (post reclassification) |
| I-6 | Incremental ROIC proxy (ΔNOPAT / Σ(capex−D&A), FY23 base) | Annual | XBRL companyfacts | FY26 incremental-ROIC input data published in draft §6 |
| I-7 | OCF, FCF, FCF margin | Quarterly | XBRL companyfacts | OCF $182.9B; FCF $67.0B; FCF margin 20.2% |
| I-8 | Operating margin | Quarterly | XBRL | 46.8% FY26 |
| I-9 | M365 Copilot paid seats | Quarterly | earnings call | >30M (Q4 FY26); net adds 2× QoQ |
| I-10 | M365 Commercial seats growth | Quarterly | earnings call | +6% YoY |
| I-11 | Share count (diluted) | Quarterly | XBRL | 7.45B |
| I-12 | Market price + trailing P/E | Weekly | Yahoo chart API | $464.72 (2026-07-31); P/E ~25.9× |
| I-13 | Regulatory / legal events (antitrust, IDPC) | Event-based | filings + public proceedings | IDPC LinkedIn appeal pending; antitrust scrutiny ongoing |
| I-14 | Platform-control signals (bundling remedies, mass migration) | Event-based | filings + regulatory orders | none observed at baseline |

## 4. Falsification-Trigger Mapping (Module J conditions → indicators)

| Module J condition (research-result v1) | Indicators | Trigger state logic |
|---|---|---|
| **(1) ex-OpenAI demand/backlog collapse** | I-1, I-2, I-3 | `TRIGGER CANDIDATE` if RPO growth ex-OpenAI negative for 2 consecutive quarters, OR Microsoft Cloud ex-frontier-model growth <10% for 2 consecutive quarters (analyst-selected threshold, grounded in disclosed total-Cloud +27% / company double-digit guidance; subgroup growth not separately disclosed — flagged when unavailable) |
| **(2) incremental AI-capital return failure** | I-5, I-6 | `TRIGGER CANDIDATE` if incremental ROIC < after-tax WACC (assumed 8–10%) measured over FY2027–FY2029 annual filings (3-yr window; annual evaluation only) |
| **(3) structural loss of platform control** | I-13, I-14 | `TRIGGER CANDIDATE` if (event route) final non-appealable regulatory order mandating unbundling/structural remedy — effective-date trigger; or (migration route) 2 consecutive quarters of net platform-seat/workload decline in enterprise filings |

**Trigger states:** `NO TRIGGER` (baseline within bounds) · `WATCH` (approaching threshold — one quarter from trigger, or single-quarter breach with no second confirmation) · `TRIGGER CANDIDATE` (conditions met per rules above). **Any `TRIGGER CANDIDATE` routes to Founder review — no autonomous action.**

## 5. Early-Warning Thresholds (before full trigger)

| Indicator | WATCH threshold | TRIGGER CANDIDATE threshold |
|---|---|---|
| I-2 RPO ex-OpenAI growth | <5% YoY | negative 2 consecutive quarters |
| I-4 Azure growth | <20% CC | <10% CC 2 consecutive quarters (analyst-selected) |
| I-5 Capex vs OCF | capex > OCF for 2 consecutive quarters | capex > 1.2× OCF for 2 consecutive quarters |
| I-6 Incremental ROIC | <12% | <8–10% WACC over 3-yr window (annual) |
| I-8 Operating margin | <44% | <40% |
| I-12 Price | 52wk high −25% | 52wk high −40% (valuation context only — never a trigger by itself) |
| I-13/I-14 | regulatory proceeding escalated (formal charge/remedy proposal) | final order / mass-migration event per §4 |

## 6. Evidence-Justifying-More-Research Categories

Any of the following, observed in monitoring, justifies proposing a deeper research slice (Founder decision required — no auto-escalation):
- I-2 or I-4 sustained deceleration not explained by disclosed capacity/contract-mix factors
- A material change in the OpenAI partnership structure or revenue concentration
- A regulatory remedy proposal (not yet final) affecting bundling
- A discrete accounting-policy change (e.g., further useful-life extension) affecting reported margins
- Market price outside the 52-week range with a fundamental driver (not purely macro)

## 7. Unresolved-Questions Tracking

Each monitoring note carries a table of unresolved questions from research-result v1 (§4) and marks whether monitoring data has begun to answer them:
1. Does the AI capex build earn >WACC? (I-5/I-6 — annual; first read FY27)
2. OpenAI-independent growth durability (I-2/I-3 — subgroup growth NOT disclosed; flagged each note)
3. Moat mechanism verification at customer level (no public source — remains open)
4. Regulatory outcomes (I-13 — event-based)
5. Accounting-optics monitoring: useful-life extension effects (I-8 — quarterly)
6. Commitment-stack precision: overlap between lease payments and not-yet-commenced leases (needs schedules — remains open)

## 8. Monitoring Note Format (Class A output)

Every note lands at `docs/ciw-pilot-msft/monitoring/YYYY-MM-DD-monitoring-draft.md` and carries:
- Header: `**DRAFT — PENDING FOUNDER REVIEW**` (never `Published`, never authoritative)
- Data-point table (I-1..I-14 with values + source lineage + retrieval date)
- Falsification-trigger status table (§4) — `NO TRIGGER / WATCH / TRIGGER CANDIDATE`
- Early-warning status (§5)
- Unresolved-questions update (§7)
- Audit fields: prior/new state (both `Draft` unless Founder acknowledges), actor (Cron Class A observer), timestamp, workflow version
- If no new filings since last run: `NO NEW FILINGS — baseline unchanged` with last-run date

## 9. Founder Review Flow

1. Cron Class A writes draft note (real data, trigger statuses).
2. **Founder reviews** the note (approve/acknowledge/return). Acknowledgment is recorded in the note's audit fields — it does NOT promote the note to an authoritative state.
3. If `TRIGGER CANDIDATE` → Founder decides next step (deeper research slice, watch, or no action). No autonomous action (FD-CIW-013).
4. Annual incremental-ROIC evaluation (I-6) reviewed by Founder in the FY27/FY28/FY29 cycle; the 3-year window completes FY2029.

## 10. Verification

- Job test-run produces a real draft note with correct header, real data, lineage, and trigger table (verified before this contract is presented for approval).
- Every Module J condition maps to ≥1 indicator (§4 table) — no unmapped falsification condition.
- Trigger logic is deterministic (thresholds in §4/§5) — no AI discretion in trigger state.

---

*Monitoring Contract v0.1 (FD-CIW-013). Status: APPROVED by Founder 2026-08-03 (Option A; content SHA-256 `d7ef7168cc3fe89d37ad880a1f828f6ef31a968cb1f3c1cb64b6f661ecfa64e3`). Cron Class A observation job `ciw-msft-class-a-monitor` LIVE. Advisory only — outputs are drafts pending Founder review; never official state. Sources: RESEARCH-FRAMEWORK Module Q; research-result v1 Module J; CRR-2026-0001; FD-CIW-005/013/014.*
<!-- 2026-08-03 15:05 UTC+7 -->
