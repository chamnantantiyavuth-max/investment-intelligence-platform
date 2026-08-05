# FD Proposal — IIP Hermes AI Workforce Integration (Proposed Operating Standard)

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED
**Version:** 0.1 (draft for review — NOT approved, NOT an FD)
**Date:** 2026-08-05
**FD number:** NOT ASSIGNED. This is a proposal only; no FD number is claimed or registered. Upon Founder approval, the next FD identifier in the canonical register (`operational/FOUNDERS-DECISIONS.md` + vault `fd-register.md`) is assigned by the Founder/recorder. **No invented FD number.**
**Proposer:** IIP profile (Hermes Agent)
**Evidence base:** `evidence/organization/ORG-INTEGRATION-FIT-GAP-v0.1.md` (findings F-01..F-22) + `operational/hermes-organization/INTEGRATION-PLAN-v0.1.md` + `ROLE-MAPPING-v0.1.md` + `TEMPLATE-DISPOSITION-v0.1.md`
**Source:** `C:\Users\Admin\Desktop\Antigravity\_staging\IIP_Hermes_Organization_Pack_v0.1` (34 files, all read; read-only discovery — nothing installed, nothing modified)

---

## 1. Exact Founder Decision Requested

Approve, with the corrections and scope below, the **integration of the proposed IIP Hermes AI Workforce Organization Pack v0.1** into the IIP project as a **subordinate operational standard** under `operational/hermes-organization/`, per the companion INTEGRATION-PLAN, ROLE-MAPPING, and TEMPLATE-DISPOSITION (v0.1 drafts). Specifically approve:

1. **Demotion and renaming** of the pack's `00-IIP-ORG-CONSTITUTION-v0.1.md` to `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md` — an operational artifact **subordinate to** the IIP Constitution, Founder Decisions, approved Project Definitions, ADRs, and plans (fit-gap F-01). No second Constitution. No amendment to Constitution §21.
2. **Canonical state contract:** org workflow/artifact fields use ONLY the approved state machines — two-axis Theme governance (Approval Status × Monitoring Status, Constitution §5 / THEME-MODEL §3), Thesis Lifecycle (CANDIDATE §3.3.2), Research State (§3.3), CIW artifact states (CIW-LIFECYCLE §5). The pack's flat `governance_state` and parallel "Research Lifecycle State" are **deleted, not adapted** (F-02, F-05).
3. **New authority grants (explicit, scoped):**
   - **Holds** (F-03): DATA HOLD (Data Steward), VALIDATION HOLD (Quant & Model Validator), RISK HOLD (Chief Risk Officer), GOVERNANCE HOLD (Internal Auditor) — **org-workflow-level only**: a Hold pauses promotion/canonical publication within the org workflow, never erases work, never vetoes domain state. Clearance by issuing role only; Founder override recorded per Constitution §21 with accepted residual risk.
   - **IC Secretary administrative completeness gate** (F-04): the Secretary may return a packet as ADMINISTRATIVELY INCOMPLETE and is the sole mover of complete packets into Founder Review. Administrative only — no investment judgment, no vote.
   - **Card movement rights + WIP limits** per KANBAN-CONTRACT (movement to `Approved`/`Rejected` governance states remains Founder-only — unchanged from today).
4. **Role definitions** as **operators of existing logical responsibilities** per ROLE-MAPPING (10 Principals; Assistants as bounded support), including: Equity Alpha **must not reopen the paused CIW path** (F-09); CRO = operator of the existing Independent Challenge function (F-10); Internal Auditor = audit orchestrator with execution routed to Sol Medium per FD-HERMES-007 (F-11); material review steps route to Sol Medium (F-14).
5. **Template disposition** per TEMPLATE-DISPOSITION: 13 mapped forms kept under `operational/hermes-organization/templates/`; pack templates 04 (deep-dive paper — Master Paper deferred) and 05 (Theme card — canonical exists) **rejected** (F-06/F-07).
6. **Runtime topology:** **Option A** — preserve the `iip` profile as project control; create up to **10 thin Principal role profiles** (identity + startup contract + role reference; canonical content stays in repo) with **Assistants as bounded delegated subagents/worker prompts** under their Principal. **No 20 persistent profiles.** (F-15/F-16; §7 of fit-gap.)
7. **Kanban vehicle:** repo-based single board under `operational/hermes-organization/kanban/` (Hermes kanban toolset is disabled in profile config; enabling it would be a separate config decision). (F-12)
8. **Cadence:** daily/weekly cadence as org standard; **no new cron jobs** without a separate named authorization (FD-CIW-005 discipline; F-19). Pilot runs manually.
9. **Bounded dry-run pilot authorization** (design in INTEGRATION-PLAN §6): 5-role simulation on ONE existing published/synthetic artifact (`docs/ciw-pilot-msft/research-result.md` v1), zero new profiles, zero canonical changes, zero cron, portfolio-blind, pass/fail criteria defined. Pilot executes only after this FD and Stage 1–2 commits.
10. **NOT authorized by this FD:** profile installation (Stage 4 requires a separate FD); any constitutional amendment; any change to canonical Theme/Candidate/Thesis/Investment state; any Hermes config change (kanban toolset, model routing, disabled skills); any CIW implementation; any portfolio data access; any commit/merge of this proposal's content without a separate instruction.

## 2. Authority Changes (delta vs today)

| Authority | Today | Proposed |
|---|---|---|
| Amend governance documents | Constitution §21 + CHANGE-CONTROL-AND-APPROVAL only | Unchanged — org standard amends itself only via §21 process |
| Approve Themes / canonical state | Founder only | Unchanged |
| Publish canonical research artifacts | Founder (CIW precedent: exact artifact + version + hash) | Unchanged; org artifacts never auto-promote |
| Hold issuance/clearance | **Nonexistent** | New: 4 role-scoped org-workflow Holds; Founder override recorded |
| Founder Review packet movement | Executor compiles → Founder reviews (CIW precedent) | IC Secretary completeness gate added (administrative) |
| Audit execution | Sol Medium delegation (FD-HERMES-007) | Unchanged; Internal Auditor orchestrates, Sol Medium executes |
| Role deployment | No persistent roles (only iip Parent + Sol Medium subagents) | 10 thin Principal profiles (Option A); Assistants as subagents |
| Kanban | None (toolset disabled; task tracking via PROJECT_STATE + plans) | Repo-based board (new, zero-config) |

## 3. Trade-offs

- **Independence vs cost:** Option A (10 profiles) buys memory/session isolation and clean audit attribution; it costs sync-script maintenance and drift surface. Option B (20 profiles) buys nothing extra (Assistants gain no model/permission difference) at double the maintenance. Option C is cheapest and is the pilot vehicle.
- **Holds power vs simplicity:** org-workflow Holds add a real pause mechanism (valuable for data/validation/risk discipline) but add process overhead; keeping them out of canonical state avoids a constitutional amendment.
- **Repo-based kanban vs Hermes tool:** zero config + git-tracked audit trail; loses native board UI (acceptable for a research org; revisit later).
- **13 templates vs 16:** fewer forms, all mapped to canonical sources; no parallel standards (Master Paper, Theme Card) — protects single-source-of-truth.

## 4. Downstream Impact

- **Docs:** new `operational/hermes-organization/` tree + `evidence/organization/`; no existing canonical file touched. PROJECT_STATE/AGENTS checkpoints updated ONLY at Stage 0 decision (and remain in-progress items C-04/C-05/M-02 — org work is a separate track).
- **Runtime (Stage 4, if separately approved):** sync-governance.py PROFILES extension + 10 project-context files + watchdog coverage; existing 8 profiles must remain unaffected (backup + rollback checkpoints).
- **Workflow:** daily/weekly cadence artifacts (Daily Work Queue, Weekly Brief) complement the existing daily-review cron and CIW Class A monitor without adding cron.
- **CIW:** explicitly NOT reopened; Equity Alpha role bounded to published/synthetic artifacts.
- **Tests/code/schema:** none. Financial logic: none. Repo: new untracked files only in this task (no commit).

## 5. Accepted Risks

1. Flash-to-Flash role "independence" is procedural, not model-based (F-14) — mitigated by Sol Medium routing for material review/audit.
2. Repo-board concurrency (multiple writers) — mitigated by single-writer discipline (CoS Assistant) + git history.
3. Role-prompt drift — mitigated by repo-canonical role content + thin profiles + startup contract.
4. Assistant label is prose, not mechanical — mitigated by startup contract + audit sampling.
5. 10 profiles increase sync surface — mitigated by staged activation + rollback checkpoints.

## 6. Unresolved Risks (accepted only with Founder sign-off, or resolved before activation)

1. Hold authority semantics if Founder wants Holds to gate **canonical** state (would require a constitutional amendment — currently out of scope).
2. Whether the org standard should eventually enable the Hermes kanban toolset / MOA for committee synthesis (config changes — deferred decisions).
3. Master Paper / deep-dive narrative standard — stays REJECTED until Phase 11 authorization.
4. IC "committee" naming — retained with advisory-only definition (F-08); rename possible at Founder's call.

## 7. What This FD Is NOT

Not a profile-installation FD (Stage 4 separate). Not a config-change FD. Not a constitutional amendment. Not a CIW reopening. Not an approval of any pack document as canonical. Not a data-access grant (portfolio-blind persists). Not an FD number assignment.

---

*Proposed draft for Founder review. No FD number claimed. No approval inferred. No commit made.*
<!-- 2026-08-05 14:26 UTC+7 -->
