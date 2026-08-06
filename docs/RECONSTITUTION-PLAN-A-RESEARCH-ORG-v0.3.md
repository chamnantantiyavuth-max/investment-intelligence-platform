# PLAN A — IIP AI-Native Research Organization Reconstitution (v0.3)

**Status:** Founder-amended (FD #64, 6 Aug 2026) — for approval: R-1, R-2. Plan Council fixes incorporated (F2 authority disposition).
**Version:** v0.3
**Date:** 2026-08-06
**Authority:** Founder direction `ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md` §1–10, §19 · FD #62 (platform pivot) · FD #63 (review authorized) · FD #64 (split amendment) · Plan Council PASS WITH FIXES (`evidence/COUNCIL_DECISION-plan-2026-08-06.md`)
**Scope:** Read-only plan. No implementation, no deletion. Supersedes the combined v0.1/v0.2 draft; the Independent Portfolio Manager is NO LONGER part of this plan (see PLAN B).
**Design objective:** Structure the operations, not the thinking.

---

## 1. Objective

Reconstitute IIP as an AI-native independent research organization: deep written analysis (essays, opposing theses, evidence appendices) produced by the 10 Principal roles acting as research Principals, with the legacy platform frozen as input/evidence. IIP remains portfolio-blind and performs no allocation, no buy/sell decisions, no portfolio management, and no execution — unchanged.

## 2. Freeze — Legacy Platform (archive in place, NO deletion)

- Pipeline modules `alpha-momentum-v0/`, `close_system/`, `fundamental-opportunity-v0/`, `institutional-intelligence-v0/`, `shared/` — screening data becomes research INPUT only
- Frontend app pages tied to pipeline surfaces — frozen; `/library` stays live ONLY as a passive renderer of markdown reports
- Backend pipeline adapters (`adapters.py`, ADAPTER_VERSION, `org_store.py`) — API shape frozen; no new pipeline wiring
- Kanban/org-workflow columns — operational tracking only where it matches the new workflow; never the analysis structure
- 311-test suite — regression protection for frozen components; not extended for research-org behavior

## 3. Keep — IIP Governance UNCHANGED (no constitutional amendment)

- **IIP Constitution + DNA + Manifesto: unchanged.** No amendment, no exception for portfolio decisions. IIP retains: no allocation; no buy/sell decisions; no portfolio management; no execution; portfolio-blind operation (§23.8.1). The council-proposed "scoped exception" is REMOVED per FD #64.
- FD machinery (FOUNDERS-DECISIONS + vault fd-register), EVIDENCE-DOCTRINE (incl. FD #58 point-in-time rule), VERIFICATION-DOCTRINE, SECURITY-AND-UNTRUSTED-CONTENT
- SACRED constraints: no autonomous buy/sell, never rewrite history, AI advisory only, Experimental ≠ official
- Reports contract (FD #62): markdown is the research source of truth; blog/`/library` = passive renderer. No API schema, report template, or frontend requirement may determine the intellectual structure of an essay.

## 4. Amend — Minimum Set (no 13-template redesign)

- **10 Principal + 10 Assistant role contracts** (`operational/hermes-organization/roles/*/`) + installed `org-*` profile prompts: reframe pipeline/org-workflow operators → research Principals (Analytical Freedom Doctrine; independent first pass; challenge duties; no checklist-shaped outputs)
- **Reports contract:** three minimum artifacts only — Main Research Essay · Evidence & Quant Appendix · Opposing Thesis & Audit Note. Other output types (Intelligence Note, Postmortem) come later when a pilot justifies them
- **State mirrors** (AGENTS.md / PROJECT_STATE / SESSION_CLOSEOUT / _Hermes-Memory) updated when FDs land
- Domain specs (`project-definition/`, CIW): **unchanged textually**; see §5 for their role

## 5. Analytical Independence (no checklist anchoring)

Domain specifications and old platform checklists are **NOT auto-loaded** into a Lead or Supporting Analyst's independent first pass. They may be used later as **optional analytical lenses** (analyst's choice) or **reviewer-side QA references** (Data Steward / Quant / Auditor). For frozen legacy modules the specs remain binding; for the research path they are non-binding references. This is an operational authority statement, not a constitutional change — recorded in R-2.

## 6. Research Workflow (direction §7)

```
Founder Research Mandate (ONE question; purpose/horizon/use/non-scope; no predefined conclusion)
  → CoS scoping (lead + only relevant support roles)
  → Independent first pass (each Principal forms a view BEFORE reading others — anti-anchoring)
  → Evidence build (Assistants + Data Steward: primary/secondary sources, filings, data, conflicting evidence)
  → Deep analysis (lead writes coherent thesis essay — conclusion/evidence/mechanism/assumptions/
    uncertainty/strongest counter-case/change-condition; depth standards, not headings)
  → Cross-examination (relevant roles challenge mechanisms)
  → Independent Challenge (CRO writes the strongest coherent opposing ESSAY — not a risk list)
  → Audit (Internal Auditor: evidence integrity, process, governance — separate from the essay)
  → Synthesis (IC Secretary: one coherent article; preserve unresolved dissent; no concatenation)
  → Founder review (publish / return / publish with dissent / opposing thesis / monitor / reject / archive)
```

## 7. Initial Cadence (pilot-limited — no daily watches yet)

| Active now | Deferred until pilots demonstrate value |
|---|---|
| Weekly Intelligence Letter (Secretary) | Daily Material Change Watch |
| On-demand Deep Research (per mandate) | Monthly Research Agenda, Quarterly Postmortem, Thesis Monitoring |

## 8. Repository

Stay in the existing repo, markdown-first. Research artifacts land in `reports/` (extended contract) or a `research/` tree decided at R-2. No new platform, no new state machine, no new pipeline/API/DB surface.

## 9. Approval Request (this plan — 2 decisions)

- **R-1 — Approve IIP research pivot + legacy-platform freeze** (§1–§3)
- **R-2 — Approve role amendments + first research pilot** (§4–§7; includes the spec-authority statement §5 and the pilot mandate §6)

## 10. Explicit Non-Authorization

This plan does NOT authorize: deletion of legacy code (archive-in-place); rebuilding a platform or new state machine; new pipeline/API/DB surface; any portfolio management, allocation, buy/sell, or execution activity of any kind (real or simulated); a portfolio-blind exception of any form; redesigning all 13 templates; activating daily watches now; turning this plan into a checklist.

## 11. Verification (when implementation is later authorized)

- git diff: no changes to frozen dirs (docs/ + research artifacts only)
- org-* profile prompts vs role contracts consistent (grep)
- No active research contract mandates fixed sections/scores/pass-fail/all-role participation (grep)
- 311-test suite green at each step; FD registers current (four mirrors)

<!-- 2026-08-06 18:30 UTC+7 -->
