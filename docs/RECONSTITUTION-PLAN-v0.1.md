# IIP Reconstitution Plan — AI-Native Research Organization + Independent Portfolio Manager

**Status:** **SUPERSEDED 2026-08-06 (FD #64)** — Founder amendment split this combined draft into two independent plans: **PLAN A** `docs/RECONSTITUTION-PLAN-A-RESEARCH-ORG-v0.3.md` (IIP research org) and **PLAN B** `docs/RECONSTITUTION-PLAN-B-IPM-v0.3.md` (separate IPM project). Historical record of the council-fixed v0.2 only.
**Status (historical):** Council-fixed draft — Plan Council (Lite) PASS WITH FIXES (3 findings, 2026-08-06) → fixes applied v0.2 → Founder approval
**Version:** v0.2
**Date:** 2026-08-06
**Authority:** Founder direction `ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md` §19 ("Hermes should first perform a read-only fit-gap… The next step should be a concise reconstitution plan, not implementation")
**Scope:** Read-only analysis + plan only. No implementation, no deletion, no code changes.
**Council:** Plan Council (Lite, Sol Medium) verdict PASS WITH FIXES — `evidence/COUNCIL_DECISION-plan-2026-08-06.md`; findings F1 (governance classification), F2 (spec authority disposition), F3 (simulated-ledger contract) — all applied below (new §3.6, §3.4 authority note, §6.1 ledger contract, expanded D-3/D-5/D-6).

---

## 1. Purpose

Plan the reconstitution of IIP from a pipeline-platform product into (a) an AI-native independent research organization producing deep written analysis, and (b) a fully separate simulated Independent Portfolio Manager (IPM). Per direction §19, this plan identifies what to freeze, keep, amend, remove, and create, and lists the Founder decisions required. This document changes nothing in the repository.

---

## 2. Fit-Gap Summary (direction §1–§18 vs current repo)

| Direction requirement | Current state (verified 2026-08-06) | Gap |
|---|---|---|
| §1 Reports = the product | FD #62 pivot live: `reports/` + /library blog, Silver note PUBLISHED | Reports exist for 1 pilot; output taxonomy (§10) not yet formalized |
| §2 Structure ops, not thinking | Platform is pipeline/checklist-heavy (AM gates, CS scoring, ADAPTER_VERSION, kanban workflow columns, 9 approved specs with mandatory fields) | Analytical freedom doctrine not encoded; specs/pipelines must become evidence/QA layer, not report structure |
| §3 Free-form over checklist output | FD #61 analysis-content direction; reports are free-form markdown | Aligned; needs reinforcement in role contracts + report contract |
| §4 Ten-role research org | FD #54: 10 Principal profiles installed (`org-cos`…`org-auditor`) + role contracts + 13 templates | Role contracts framed as "org-workflow/pipeline workers" — need amendment to research-principal framing |
| §5 Analytical Freedom Doctrine | Not encoded anywhere | New — encode in Principal role contracts + report contract |
| §6 Checklists → QA appendices | Data Steward / Quant / Auditor role contracts carry checklist duties | Align to appendix/audit-note placement; remove checklist-shaped main-analysis requirements |
| §7 Research workflow (mandate→synthesis→Founder review→monitoring) | CIW pilot proved the pattern (Research Gate → Source Map → research → Independent Challenge → Founder review → Published); org kanban exists | Independent first pass (pre-anchoring) + CRO opposing ESSAY + Secretary synthesis (not concatenation) not in the standing workflow |
| §8 Recurring work (daily watch / weekly letter / monthly agenda / quarterly postmortem) | Weekly AM pipeline cron + daily org-workflow crons exist | Output types missing (Intelligence Letter, Research Agenda, Postmortem); "NO MATERIAL CHANGE" silence convention not encoded |
| §10 Output taxonomy (essay + evidence appendix + opposing thesis/audit note + intelligence note + postmortem) | `reports/` contract has frontmatter (type: company/product/weekly/quarterly/theme) | Taxonomy extension + appendix/opposition pairing needed |
| §11–17 Independent Portfolio Manager | **Does not exist anywhere** | New subsystem — separate tree, $200k simulated ledger, letters, philosophy, IBKR verification |
| §18 Markdown/Obsidian-first repo identity | Repo is code-heavy (backend/frontend/pipelines); `reports/` + `docs/` are markdown; vault exists for Obsidian | Research tree proposal (§6 below) — decision for Founder |

---

## 3. Classification: Freeze / Keep / Amend / Remove / Create

### 3.1 FREEZE AS LEGACY (no deletion — archived in place, read-only)
- Pipeline modules: `alpha-momentum-v0/`, `close_system/`, `fundamental-opportunity-v0/`, `institutional-intelligence-v0/`, `shared/` — screening data becomes report INPUT only
- Frontend app pages tied to pipeline surfaces (AM/FO/CS/II dashboards) — frozen as-is; /library stays live (it is the new product surface)
- Backend pipeline adapter surfaces (`adapters.py`, ADAPTER_VERSION mechanics, `org_store.py`) — freeze API shape; no new pipeline wiring
- Kanban board + org-workflow kanban columns — retain as operational tracking ONLY where it matches the new workflow (see §5), not as the analysis structure
- 311-test suite — retained as regression protection for frozen components; not extended for new research-org behavior

### 3.2 KEEP (governance that survives, unchanged or lightly touched)
- Constitution + 01-PROJECT-DNA + 00-FOUNDERS-MANIFESTO (authority model, §23 AI Operating Constitution, evidence doctrine)
- `operational/FOUNDERS-DECISIONS.md` + vault fd-register (FD machinery)
- `operational/EVIDENCE-DOCTRINE.md` incl. FD #58 point-in-time rule (directly supports the new evidence discipline)
- `operational/VERIFICATION-DOCTRINE.md`, `SECURITY-AND-UNTRUSTED-CONTENT.md`
- **§23.8.1 Blind Portfolio Rule** — reaffirmed; the IPM operates on its OWN simulated ledger only, never the Founder's real portfolio; research org stays portfolio-blind
- **SACRED constraints:** no autonomous buy/sell (IPM is simulated; no live orders), never rewrite history, AI advisory only, Experimental ≠ official
- No-AI-invented-rules constraint — applies to the SYSTEM's deterministic machinery; IPM discretion is a decision output, not a system rule (needs explicit FD wording, see §9 D-6)
- Reports contract (FD #62) + /library blog + /api/reports read-only auth-gated store

### 3.3 AMEND (existing artifacts to revise)
- **10 Principal role contracts** (`operational/hermes-organization/roles/*/PRINCIPAL.md`) + Assistant contracts: reframe from pipeline/org-workflow operators to independent research Principals (Analytical Freedom Doctrine §5, independence first pass §7.3, challenge duties §7.6–7.7, no checklist-shaped outputs)
- **Role prompts in installed profiles** (`~/.hermes/profiles/org-*`): same reframing, synchronized with role contracts
- **13 templates** (`operational/hermes-organization/templates/`): map to new workflow (RISK-CHALLENGE-MEMO → CRO opposing essay; IC-DECISION-PACK → Secretary synthesis; add Opposing Thesis + Audit Note + Intelligence Note + Postmortem templates)
- **`reports/README.md` contract**: extend output taxonomy (§10) — types + appendix + opposing-thesis pairing + status flow unchanged (draft → review → published)
- **`operational/hermes-organization/DAILY-WEEKLY-WORKFLOW-v0.1.md` + KANBAN-CONTRACT**: re-map cadences to §8 (daily watch = material-change detection with silence convention; weekly letter; monthly agenda; quarterly postmortem; thesis monitoring)
- **AGENTS.md / PROJECT_STATE.md / SESSION_CLOSEOUT.md**: state mirrors updated when FDs land
- **9 domain specs** (`project-definition/`): remain as DOMAIN REFERENCE + QA checklists (§6), not as report outlines; specs unchanged textually unless Founder orders otherwise

### 3.4 REMOVE (from active operation — not deletion, retirement from the critical path)

**Authority disposition (council F2 fix):** approved platform/domain specifications (`project-definition/`, CIW specs) continue to GOVERN the frozen legacy modules — they remain binding there, unchanged. For the NEW research path they are demoted to **non-binding analytical lenses and QA references** (direction §2: "Requirements and analytical lenses define the search space. They do not define the structure of the final answer"). This demotion is a Founder decision (D-3) recorded per Constitution §21; the specs themselves are NOT rewritten and NO new checklist is created.

Checklist-shaped output mandates are retired from these ACTIVE research artifacts (not from the frozen platform):
- 10 Principal role contracts + 10 Assistant contracts (`operational/hermes-organization/roles/*/PRINCIPAL.md`, `ASSISTANT.md`) — mandatory-field analysis requirements removed; Analytical Freedom Doctrine (direction §5) governs
- Installed org-* profile prompts (`~/.hermes/profiles/org-*`) — same retirement, synced with the contracts
- Mapped templates (`operational/hermes-organization/templates/`) — checklist-shaped ones converted to QA/audit appendices or replaced per §3.3
- `reports/README.md` contract — output structure free-form per direction §7.5 (depth standards, not headings); frontmatter status flow unchanged

- Mandatory-field analysis requirements in prompts/specs that force checklist outputs ("Macro: Pass" class) — retire from the ACTIVE research path; keep as QA-only
- All-ten-roles-per-task convention (direction §4: "avoid involving all ten roles merely to make the process look complete")
- Daily/weekly cadences that produce low-value routine output (replaced by silence convention §8)

### 3.5 CREATE (new artifacts)
- **Independent Portfolio Manager office** — separate tree, philosophy, ledger, letters (see §6)
- **Research repository structure** — mandates/evidence/monitoring/postmortems/debates (see §7)
- **IBKR eligibility verification path** (see §8)
- **New recurring-work contracts** (see §5)
- **New report types** (see §3.3 reports contract)

### 3.6 Governance Authority Map — clause-level disposition (council F1/F2 fix)

Existing higher-authority clauses that the reconstitution touches must each get an explicit status. This map is the basis for the D-6 Constitution §21 amendment decision. Statuses: **Retained** (unchanged, applies as-is) / **Legacy-Scope Only** (continues to bind the frozen platform, not the new research path) / **Amended** (text updated via Constitution §21 process, per Founder decision D-6) / **Superseded** (replaced by this direction, recorded via §21).

| Clause (verified text 2026-08-06) | Status | Disposition |
|---|---|---|
| Constitution §1 Mission — "It does not autonomously answer: What should be bought, sold, or allocated?" | **Amended (scoped exception)** | Research org unchanged (never recommends allocation autonomously). IPM gets a NARROW exception: autonomous decisions INSIDE the simulated USD 200k office only; real capital, live orders, and real accounts remain absolutely prohibited |
| Constitution §2 Product Structure — Strategy Control Center entry point | **Legacy-Scope Only** | Frozen app remains structured as-is; the product surface becomes the research blog/reports per FD #62 + this direction |
| Constitution §3 Development Direction — AM first vertical slice | **Superseded** (per §21) | Development direction now = research organization + IPM; AM pipeline frozen as completed legacy |
| Constitution §17 Knowledge Architecture — "The application is the structured source of truth" | **Amended** | Pipeline evidence stays structured in the frozen app; RESEARCH truth (mandates, essays, evidence appendices, monitoring, postmortems) lives markdown-first in the research repo (direction §18); Obsidian remains narrative layer |
| Constitution §18 Initial Non-Scope — automated allocation; autonomous buy/sell recommendations | **Amended (scoped exception)** | Retained for all live/real-capital paths; exception ONLY for simulated-office decisions (no live orders, no real allocation) |
| Constitution §20 V0 Thesis | **Legacy-Scope Only** | AM slice complete; frozen; no new V0 obligations |
| Constitution §23.2 Three-Layer Authority — AI output non-authoritative until validation/review status | **Retained** | Research essays carry Founder-review status; IPM letters are advisory, never authoritative for real capital |
| Constitution §23.8.1 Blind Portfolio Rule | **Retained + extended** | Research org stays portfolio-blind; IPM operates on its OWN simulated ledger ONLY; IPM never receives Founder's real holdings, positions, cost basis, or transactions |
| DNA-001 Decision Intelligence, Not Automated Decision-Making | **Amended (scoped exception)** | Same narrow simulated-office exception as §1/§18; live prohibition unchanged |
| DNA-004 Breadth Before Depth | **Retained (as research lens)** | Consistent with mandate → scoping → deep research; no change needed |
| DNA-018 Structured Source of Truth, Narrative Learning Layer | **Amended** | Mirrors §17 disposition: research repo becomes the primary product record; frozen app remains the structured source for pipeline evidence |
| DNA-020 Company Research Must Return Intelligence to the System | **Amended** | Research returns intelligence to the RESEARCH ORGANIZATION (evidence repo, monitoring contracts, next questions, postmortems) rather than to the frozen pipeline modules |
| AGENTS.md "Do not introduce broker connectivity, execution, or portfolio allocation" | **Amended (scoped exception)** | Live prohibition unchanged; exception = simulated office with NO broker connectivity, NO execution, NO real allocation |
| AGENTS.md "No AI-invented investment rules, thresholds, weights, formulas…" | **Retained** | Applies to deterministic system machinery; IPM discretionary decisions are decision OUTPUTS with auditable rationale, not system rules |
| SACRED: no autonomous buy/sell; never rewrite history; AI advisory only; Experimental ≠ official | **Retained** | All four bind the whole system; IPM simulation is advisory demonstration only, never live authority |

Verification (council F1): a Constitution §21 amendment record lists each clause above as Retained / Legacy-Scope Only / Amended / Superseded with the D-6 Founder decision; no unresolved contradiction remains between the IPM mandate and higher-authority documents.

---

## 4. Target Research Workflow (direction §7)

Standing workflow replaces the pipeline-gate mental model:

```
Founder Research Mandate (ONE important question; purpose/horizon/use/non-scope; no predefined conclusion)
  → Chief of Staff scoping (lead + only relevant support roles; no checklist-ification)
  → Independent first pass (each selected Principal forms a view BEFORE reading others — anti-anchoring)
  → Evidence build (Assistants + Data Steward: primary/secondary sources, filings, data series, conflicting evidence)
  → Deep analysis (lead writes coherent thesis essay — conclusion/evidence/mechanism/assumptions/uncertainty/
    strongest counter-case/change-condition; standards for depth, not headings)
  → Cross-examination (relevant roles challenge mechanisms — Macro↔Commodity↔Quant↔Options↔Equity)
  → Independent Challenge (CRO writes the strongest coherent opposing ESSAY — one or two mechanisms, not a risk list)
  → Audit (Internal Auditor: evidence integrity, process, governance — separate from the essay)
  → Synthesis (IC Secretary: one coherent article; preserve unresolved dissent; no concatenation)
  → Founder review (publish / return / publish with dissent / opposing thesis / monitor / reject / archive)
  → Monitoring contracts (published theses only) + Postmortems (lessons = proposals until Founder approves)
```

Outputs per direction §10: Main Research Essay + Evidence/Quant Appendix + Opposing Thesis/Audit Note + Intelligence Note + Research Postmortem.

---

## 5. Recurring Work Contracts (direction §8)

| Cadence | Owner | Output | Silence convention |
|---|---|---|---|
| Daily Material Change Watch | CoS + Data | Research Trigger Note only when warranted | `NO MATERIAL RESEARCH CHANGE` |
| Weekly Intelligence Letter | Secretary | Small number of developments that changed understanding + one question deserving deeper work | No fixed sections |
| Monthly Research Agenda | CoS | Proposed Research Mandate (not auto-launch) | — |
| Quarterly Research Postmortem | Quant + CRO + Auditor | Most instructive successes/failures + habit changes; no report-count grading | — |
| Thesis-Specific Monitoring | Data + relevant analyst | Monitoring notes on published theses only | No auto-rewrite of published thesis |

---

## 6. Independent Portfolio Manager (direction §11–17) — new, separate

- **Separation:** IPM is NOT part of the ten-role research org. No reporting line to the CoS, no authority over research, no dependency on research workflow. May read published IIP reports only if the Founder makes them available. Both report to the Founder only.
- **Entity:** Simulated office, starting capital **USD 200,000**, multi-month/multi-year institutional orientation, NO day trading. Manages only its own simulated portfolio.
- **Team:** Portfolio Manager (sole decision-maker) + up to 3 assistants (Portfolio Research / Structure & Risk / IBKR Instrument & Ledger). Assistants advise; PM decides.
- **Philosophy:** Broad Mudley principles (§13): survival before return, main army + opportunistic forces, Close System thinking as tool not mandate, buffer before expansion, multiple strategies one portfolio, position management over prediction, freedom to hold cash, no artificial activity.
- **Ledger:** Simulated ledger maintained as source of truth for the simulation; every transaction states **SIMULATED PORTFOLIO — NOT A LIVE ORDER**. Distinguish idea → eligible instrument → simulated order → simulated fill. No live orders authorized.
- **Outputs:** Portfolio Finding Letter / Investment Decision Letter / Weekly Letter / Monthly Structure Review. Institutional prose; auditable rationale; NO hidden chain-of-thought; no Buy/Sell/Hold-only responses.
- **Recurring:** Daily material watch (`NO MATERIAL PORTFOLIO CHANGE`), weekly review, monthly structure review, event-driven review.
- **Placement:** separate tree (`independent-portfolio-manager/` §7) — same repo or separate repo, but authority/workflow fully separate.

### 6.1 Minimum Simulated-Ledger Contract (council F3 fix — D-5 basis)

The simulated ledger is the source of truth for the office. Minimum accounting contract, approved with D-5:

- **Opening balance:** USD 200,000 cash, single currency (USD) base; no other assets at inception.
- **Append-only record:** every simulated transaction, correction, and valuation adjustment is an append-only journal entry with timestamp, entry id, and immutable reference to its decision letter (or correction note). Corrections are new entries, never edits (never rewrite history — SACRED).
- **Deterministic reconciliation:** cash, positions, realized/unrealized results, reserves, and committed obligations are DERIVED from the journal by deterministic rules — never stored as opaque state. A no-trade opening ledger must reconcile exactly to USD 200,000.
- **Required per-entry fields:** instrument identifier; IBKR-eligibility verification reference (per §8); exchange; currency; contract multiplier; expiry (if applicable); quantity (full units — no fractional share assumptions); simulated fill price; simulated fill basis (e.g., verified reference price + spread/fee model); fees; FX rate (non-USD legs); timestamp; decision-letter reference. Missing eligibility evidence → NO ledger entry (fail-closed).
- **Capital classification (direction §13.4):** journal tracks original capital vs realized profit vs released capital vs reserve vs available cash vs capital committed to future obligations as derived categories, not manually maintained numbers.
- **Explicit exclusions:** no broker credentials, no live-account data, no live-order connectivity, no real-time market feed requirements — all fills are simulated from verified reference prices per §8.
- **Verification:** (1) no-trade opening ledger reconciles to USD 200,000; (2) one representative multi-currency or derivative simulation reconciles journal ↔ cash ↔ positions ↔ obligations ↔ letter references with zero live-order path.

---

## 7. Repository Restructure (direction §18 — proposal, Founder decision)

Proposal: keep ONE repository, add two top-level research trees, freeze existing app dirs in place:

```
investment-intelligence-platform/           (existing repo root)
├── (existing governance + frozen platform dirs — unchanged)
├── research/                               NEW
│   ├── mandates/
│   ├── countries/ commodities/ industries/ companies/ options-volatility/ cross-asset/ special-situations/
│   ├── intelligence-notes/ debates/ monitoring/ postmortems/ evidence/
│   └── published-blog/                     (maps to existing reports/ + /library)
├── reports/                                (existing — publishing contract, extended)
└── independent-portfolio-manager/          NEW — separate authority
    ├── philosophy/ research/ findings/ decisions/ portfolio-ledger/ weekly-letters/ monthly-reviews/ postmortems/ roles/
```

Decision points for Founder: (a) same repo vs separate repo for IPM; (b) adopt `research/` tree now or keep `reports/` + `docs/` flat and restructure at first deep-research milestone.

---

## 8. IBKR Eligibility Verification (direction §12.2, §14)

Requirement: never assume availability; verify actual IBKR contract/exchange/currency/multiplier/expiry before any simulated transaction.

Path (no install today):
1. **Baseline:** re-verify (per FD #58) the verified facts in the separate workspace `C:\Users\Admin\Desktop\Antigravity\Grid Trading System for IBKR\docs\RESEARCH.md` (2026-07-10): order limits (20 active orders/contract/side), API pacing, `ib_async` v2.1.0 (ib_insync archived), `cashQty` Forex-only → full-share sizing, minTick/multiplier verification discipline, whatIfOrder pre-trade validation, paper port 7497.
2. **Primary verification source:** IBKR official public documentation — `interactivebrokers.github.io/tws-api` + public contract search — the IBKR assistant queries these per instrument class before any simulated order.
3. **Optional later:** TWS Paper (port 7497) on this machine for deeper instrument checks — requires Founder approval + install; not needed to start.
4. The IBKR assistant's verification note attaches to every Investment Decision Letter that involves a new instrument.

---

## 9. Required Founder Decisions

| # | Decision | Effect |
|---|---|---|
| D-1 | Approve this reconstitution plan (as amended by council) | Unlocks the reconstitution workstream |
| D-2 | Freeze classification (§3.1) — pipeline surfaces + app frozen as legacy, archive-in-place, no deletion | Sets legacy boundary; rollback = git history + archive plan |
| D-3 | Role amendment authorization (§3.3 + §3.4) — 10 Principal/Assistant contracts + installed profile prompts reframed to research organization + Analytical Freedom Doctrine; **authority disposition of approved domain specs (binding for frozen legacy modules; non-binding analytical lenses/QA references for the research path — per §3.4, council F2)** | Updates FD #54 operating artifacts; resolves spec authority conflict |
| D-5 | Independent Portfolio Manager creation (§6) — separate tree, letter set, philosophy; simulated only; **approves the Minimum Simulated-Ledger Contract (§6.1, council F3): opening USD 200k, append-only journal, deterministic reconciliation, fail-closed eligibility, no broker/live paths** | Creates new subsystem (separate from research org) |
| D-6 | Governance authority map + portfolio-blind + no-live-trading reconciliation — **Constitution §21 amendment recording the §3.6 clause-level map (Retained / Legacy-Scope Only / Amended / Superseded), including the NARROW scoped exception for autonomous decisions inside the simulated office only**; research org remains portfolio-blind (§23.8.1); IPM never receives Founder's real holdings; IPM discretion is a decision output, not a system rule (no-AI-invented-rules boundary); SACRED no-autonomous-buy/sell + no live orders/real capital reaffirmed for the whole system | Resolves Constitution §§1/3/17/18/20/23.2 + DNA-001/018/020 + AGENTS.md prohibitions vs the simulation (council F1) |
| D-7 | IBKR verification path (§8) — public docs/contract search baseline; TWS Paper optional later | Stands up the IBKR assistant requirement |
| D-8 | Repository structure decision (§7) — same-repo two trees vs separate repo; adopt research/ tree now vs at first milestone | Sets layout |
| D-9 | Recurring-work activation order (§5) — which cadences start first (daily watch + weekly letter recommended) | Sets operating rhythm |
| D-10 | First research mandate (per §7.1) — ONE question to pilot the new workflow end-to-end | Pilot gate |

---

## 10. Explicit Non-Authorization (direction §19 "Hermes should not")

This plan does NOT authorize, and the reconstitution must NOT:
- rebuild a new platform or create a new complex state machine;
- turn this document into a larger checklist;
- define rigid portfolio allocations without Founder approval;
- force all ten research roles into every task;
- integrate the IPM into the research-team authority chain;
- give the IPM authority over research;
- implement live trading (any order, any instrument);
- delete previous application code before a rollback and archival plan is approved (archive-in-place is the default);
- extend the frozen platform's pipeline/API/DB surface.

---

## 11. Verification Plan (for the reconstitution itself)

- Freeze classification verified by git diff: no code changes to frozen dirs (only docs/ + new trees touched)
- Role contracts + profile prompts amended consistently (grep org-* profile SOULs vs role contracts)
- FD #63..N registered in all four mirrors (repo FOUNDERS-DECISIONS, vault fd-register, _Hermes-Memory Decisions/CURRENT-STATE, native memory)
- 311-test suite still green (frozen platform untouched) at each step
- Council artifact present before Founder presentation (Plan Council — this run)
- No new live-order/portfolio code introduced anywhere
- **Authority map verified (council F1):** Constitution §21 amendment record lists every §3.6 clause with its status; no unresolved contradiction between IPM mandate and higher-authority docs
- **Spec authority verified (council F2):** grep confirms no ACTIVE research contract (role contracts, templates, reports contract) mandates fixed analytical sections, scores, pass/fail conclusions, or all-role participation
- **Ledger verified (council F3):** no-trade opening ledger reconciles to USD 200,000; one representative multi-currency/derivative simulation reconciles journal ↔ cash ↔ positions ↔ obligations ↔ letters with zero live-order path

---

## 12. Next Step

Founder approval of D-1 (plan) + D-2..D-10 (one decision at a time, per working method). Each approved decision recorded as an FD immediately. Implementation begins only after D-1.

<!-- 2026-08-06 17:50 UTC+7 -->
