# IIP × Hermes Organization Pack — Integration Plan

**Status:** PROPOSED — FOUNDER REVIEW REQUIRED
**Version:** 0.1 (draft for review — NOT approved, NOT canonical)
**Date:** 2026-08-05
**Depends on:** `evidence/organization/ORG-INTEGRATION-FIT-GAP-v0.1.md` (findings F-01..F-22) + `operational/FD-PROPOSAL-IIP-HERMES-WORKFORCE-v0.1.md`
**Scope:** Docs-only integration design. No profiles installed, no config changed, no code/schema/Constitution touched, no commit.

---

## 1. Design Principles

1. **Subordination** — every integrated artifact lives under `operational/hermes-organization/` as a proposed operational standard; nothing is promoted to Constitution/Project-Definition status without a separate named FD.
2. **No duplication of canonical content** — role contracts reference specs (OM §5/§6, EVIDENCE-MODEL, THEME-MODEL, CIW contracts, VERIFICATION-DOCTRINE); they do not re-define domain logic.
3. **Canonical state only** — all workflow/artifact fields use the approved state machines (two-axis Theme governance, Thesis Lifecycle, Research State, CIW artifact states). The pack's parallel state models are deleted, not adapted.
4. **Thin runtime** — repo is the single source of role definitions; local profiles (if created) hold loader + identity + role reference only.
5. **Portfolio-blind forever** — no role/Assistant receives holdings, positions, cost basis, transactions, or account data (Constitution §23.8.1).
6. **Explicit approval per stage** — no stage starts without the Founder decision it requires.

---

## 2. Proposed Target Structure (evaluated, adjusted from the pack's proposal)

```
operational/hermes-organization/
  README.md                          — purpose, authority hierarchy, navigation, status
  AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md   — renamed from pack 00 (F-01), state model corrected (F-02/F-05)
  AUTHORITY-MATRIX-v0.1.md           — corrected: Hold/gate rows marked "pending FD grant" until approved
  DAILY-WEEKLY-WORKFLOW-v0.1.md      — cadence; cron additions gated (F-19)
  KANBAN-CONTRACT-v0.1.md            — repo-based board contract (F-12); canonical state fields (F-02)
  ROLE-REGISTRY-v0.1.md              — one-line per role → ROLE-MAPPING + role dirs
  roles/
    01-founder-chief-of-staff/   PRINCIPAL.md · ASSISTANT.md
    02-investment-committee-secretary/  PRINCIPAL.md · ASSISTANT.md
    03-commodity-product-analyst/  PRINCIPAL.md · ASSISTANT.md
    04-global-macro-strategist/  PRINCIPAL.md · ASSISTANT.md
    05-equity-alpha-analyst/  PRINCIPAL.md · ASSISTANT.md
    06-options-strategist/  PRINCIPAL.md · ASSISTANT.md
    07-chief-risk-officer/  PRINCIPAL.md · ASSISTANT.md
    08-quant-model-validator/  PRINCIPAL.md · ASSISTANT.md
    09-data-steward/  PRINCIPAL.md · ASSISTANT.md
    10-internal-auditor-red-team/  PRINCIPAL.md · ASSISTANT.md
  templates/                         — ONLY the 7 kept templates (TEMPLATE-DISPOSITION): intake, evidence (mapped), brief,
                                       data-quality (mapped), quant-validation (mapped), risk-challenge (mapped),
                                       IC decision pack (mapped), weekly brief, change-request (mapped), assistant worklog
  installation/
    HERMES-PROFILE-MAPPING.md        — real paths (AppData\Local\hermes\profiles\…), sync-script extension, watchdog
    PROFILE-STARTUP-CONTRACT.md      — thin loader: identity + boundary + role reference + label contract (F-17)
    RUNTIME-VERIFICATION-CHECKLIST.md — checks per stage (see §5)
  kanban/                            — repo board: board.md + cards/ (YAML per KANBAN-CONTRACT §3) + holds/ (F-03)
```

**Explicitly NOT created:** pack `00-IIP-ORG-CONSTITUTION` (renamed), combined 3,426-line edition (F-22), deep-dive paper template (F-07, Master Paper deferred), pack `governance_state` anywhere, 20 profiles.

**Not placed in `project-definition/`:** Hermes runtime instructions stay under `operational/hermes-organization/installation/` (task constraint: do not put Hermes runtime instructions in project-definition unless authority requires it — it does not).

---

## 3. File-by-File Actions

| # | Action | Source | Target | Correction applied |
|---|---|---|---|---|
| P1 | COPY + RENAME + REWRITE header/§5/§15 | pack `00-IIP-ORG-CONSTITUTION-v0.1.md` | `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md` | F-01 demotion; F-02 two-axis governance; F-05 delete parallel lifecycle; F-08 glossary; F-13 materiality note; §15 → Constitution §21 pointer |
| P2 | COPY + AMEND | pack `01-AUTHORITY-MATRIX-v0.1.md` | `AUTHORITY-MATRIX-v0.1.md` | F-03/F-04: Hold + IC-gate rows carry "PENDING FD GRANT" until approved; F-11 audit row → Sol Medium routing; F-20 "Approved for Official Tracking" → `Approved` mapping |
| P3 | COPY + AMEND | pack `02-DAILY-WEEKLY-WORKFLOW-v0.1.md` | `DAILY-WEEKLY-WORKFLOW-v0.1.md` | F-19 cadence gate; D5 packet fields → CIW founder-review-record alignment; no new cron without named authorization |
| P4 | REWRITE | pack `03-KANBAN-BOARD-v0.1.md` | `KANBAN-CONTRACT-v0.1.md` | F-02 card fields (approval_status + monitoring_status, no governance_state); F-12 repo-based board + writer discipline; F-13 M0–M4 subordinate to material-change; F-17 movement audit trail |
| P5 | CREATE | — | `ROLE-REGISTRY-v0.1.md` | index table: role → OM responsibility → authority → artifact set → review deps → assistant |
| P6 | COPY + REWRITE (10 dirs) | pack `profiles/01..10` | `roles/01..10/{PRINCIPAL,ASSISTANT}.md` | F-09 CIW boundary; F-10 CRO→challenge operator; F-11 auditor→orchestrator + Sol Medium; F-14 review-routing; F-18 §23.7 failure contract; remove duplicated Shared Operating Rules boilerplate → single reference to the standard (F-16) |
| P7 | SELECT (7 of 16) | pack `templates/` | `templates/` | per TEMPLATE-DISPOSITION (REUSE/EXTEND/CREATE; REJECT 05, 04, 11-duplicate-forms, 13-dup, 14-dup→mapped) |
| P8 | CREATE | — | `installation/HERMES-PROFILE-MAPPING.md` | real profile paths; sync-governance.py PROFILES extension + project-context files; watchdog; kanban-toolset config note (disabled today) |
| P9 | CREATE | — | `installation/PROFILE-STARTUP-CONTRACT.md` | thin loader contract; `ASSISTANT DRAFT — PRINCIPAL REVIEW REQUIRED` label; no domain truth in memory; role prompt = repo path reference |
| P10 | CREATE | — | `installation/RUNTIME-VERIFICATION-CHECKLIST.md` | per-stage checks (§5) |
| P11 | CREATE | — | `kanban/` (board.md + cards/ + holds/) | repo board bootstrap; single-writer discipline |
| P12 | CREATE | — | `README.md` (org dir) | purpose, hierarchy, status ("PROPOSED — FOUNDER REVIEW REQUIRED"), links |
| P13 | DRAFT | — | `ROLE-MAPPING-v0.1.md`, `TEMPLATE-DISPOSITION-v0.1.md`, `FD-PROPOSAL-IIP-HERMES-WORKFORCE-v0.1.md` | the three companion deliverables (written in this task) |
| P14 | DRAFT | — | `evidence/organization/ORG-INTEGRATION-FIT-GAP-v0.1.md` | this analysis (written in this task) |

**Not carried over:** pack `IIP-HERMES-ORGANIZATION-PACK-v0.1.md` (combined edition, F-22); pack `README-TH.md` (absorbed into org README, Thai summary preserved); `MANIFEST.txt` (staging-only).

---

## 4. Migration and Rollback Plan

**Migration (docs-only, reversible):**
1. All changes land under `operational/hermes-organization/` + `evidence/organization/` — no existing file is modified, so rollback = delete the new directory tree.
2. No git commit in this task. When Founder approves the FD: one commit per stage (P1–P4 core docs; P5–P7 roles+templates; P8–P11 installation+kanban), each with a checkpoint tag (`org-pack-stage-1/2/3`).
3. Stage-3 profile activation (if approved): backup `sync-governance.py` + `shared/project-context/` before editing; create profiles one at a time; verify each boots (`hermes profile list`, startup contract check) before the next.

**Rollback triggers (any → stop and revert to previous checkpoint):**
- Any canonical file (Constitution, FDs, specs, AGENTS.md, PROJECT_STATE.md) is touched by org-pack content (must never happen).
- Any profile prompt attempts to change governance state, clear a Hold, or publish canonical artifacts.
- Any data incident or portfolio-data leak vector.
- Sync script breaks an existing profile (iip/capcmd/fxtrading/notebooklm) — restore from backup, re-run sync, verify all 8 existing profiles.

---

## 5. Verification Plan (per stage, from RUNTIME-VERIFICATION-CHECKLIST)

| Stage | Verification |
|---|---|
| 0 — Founder FD decision | FD recorded with exact scope; no invented FD number (next = #54 pending register check); artifact-gate: FD proposal + fit-gap present in repo |
| 1 — Docs integration (P1–P4, P14) | Grep-verify: no `governance_state` flat axis anywhere; both Theme axes present; no "Organization Constitution" title; Constitution §21 referenced; `git status` shows only new untracked files |
| 2 — Roles + templates (P5–P7) | Every role contract has §23.5 fields (purpose/authority/permitted evidence/prohibited actions/contracts/failure/escalation/review); every template maps to a canonical source (TEMPLATE-DISPOSITION); grep-verify no pack state values leak into templates |
| 3 — Pilot dry-run (Option C runtime) | Simulate 4-role workflow (CoS + Equity + CRO + Data Steward) on ONE published/synthetic artifact (e.g., `docs/ciw-pilot-msft/research-result.md` v1 or an AM pipeline result): intake → data-readiness → research → challenge → packet → Founder review simulation. Assert: handoffs named, evidence lineage preserved, dissent preserved, Holds recorded + cleared by issuer, packet completeness gate works, no canonical state changed, portfolio-blind (no position data anywhere). Pass/fail criteria in §6. |
| 4 — Thin profiles (Option A, if approved) | Install 10 principals per HERMES-PROFILE-MAPPING; `hermes profile list` shows all; startup contract check per profile; sync-governance re-run idempotent; existing 8 profiles unaffected; isolation check (no cross-profile memory writes) |
| 5 — Cadence + audit | Weekly cadence runs as scheduled tasks with named authorization (no new cron in pilot); Internal Auditor sample audit of Stage 3/4 artifacts via Sol Medium delegation (FD-HERMES-007); findings → remediation → verified close |

**Evidence tags (Verification Doctrine §Closeout):** each stage closes with TEST_VERIFIED (where scripted greps/checks run) / STATIC_OBSERVATION (docs-only inspection) / INFERENCE (mapping claims), recorded in the stage evidence file under `evidence/organization/`.

---

## 6. Staged Activation Plan (each stage gated by explicit Founder decision)

- **Stage 0 — Decision (this task's output):** Founder reviews fit-gap + FD proposal + brief; approves Option A/B/C, Hold scope, IC gate, kanban vehicle, template dispositions. Output: FD #54 (or Founder-assigned ID) — NOT issued by this task.
- **Stage 1 — Canonical docs (docs-only):** P1–P4 + P14 committed as `org-pack-stage-1`; verification §5-stage-1.
- **Stage 2 — Roles, templates, pilot:** P5–P7 committed; **bounded dry-run pilot** per §6-of-FD (uses published/synthetic artifact; 4 roles; no profiles, no cron, no canonical changes, no CIW reopening, portfolio-blind); pass/fail criteria below. Pilot result → Founder review → decide Stage 4.
- **Stage 3 — Installation docs (docs-only):** P8–P11; no profile creation yet.
- **Stage 4 — Thin-profile activation (Option A only, separate FD):** sync-script extension + 10 principal profiles + assistant subagent prompts; staged per HERMES-PROFILE-MAPPING with rollback checkpoints.
- **Stage 5 — Cadence, audit, review:** weekly cadence (authorized tasks only), Internal Auditor via Sol Medium, quarterly control assessment; full org-standard review at 60 days → v0.2 or retire.

### Pilot Design (bounded dry-run — design only, NOT executed in this task)

- **Vehicle:** existing `iip` profile; roles simulated via role prompts loaded in-session or via `delegate_task` (Option C runtime) — zero new profiles.
- **Artifact:** ONE existing published/synthetic artifact: `docs/ciw-pilot-msft/research-result.md` v1 (Published, hash `34a1f324…`) — no new research, no live data, no portfolio information.
- **Roles (minimum useful set):** Founder Chief of Staff (triage/queue), Equity Alpha Analyst (review the published result under ROLE-MAPPING boundaries), Chief Risk Officer (Risk Challenge Memo on it), Data Steward (Data Quality Report on its source map) — plus IC Secretary for packet assembly (5 roles).
- **Exercises:** handoffs with named owners; evidence lineage (source map → claim lineage → memo); a simulated DATA HOLD + RISK HOLD issued and cleared by issuer; dissent preservation (challenge memo survives approval); Founder packet completeness gate (D5 checklist); assistant worklog for one delegated gather step.
- **Explicitly NOT exercised:** any canonical state change, any CIW-path research, any cron, any live/holdings data, any profile installation.
- **Pass criteria (all required):** 5/5 handoffs have named owner + inputs + outputs + next state; 3/3 memos trace claims to the published result's source map with zero fabricated references; 2/2 Holds recorded with scope/evidence/remediation and cleared by the issuing role only; dissent appendix preserved after simulated Founder approval; packet rejected once as ADMINISTRATIVELY INCOMPLETE and re-passed after defect fix; zero changes to repo canonical files; portfolio-blind check (no position/holdings/cost-basis text in any pilot artifact).
- **Fail criteria (any):** any role or assistant alters canonical state; any artifact claims verification not performed; Hold cleared by non-issuer without Founder override record; assistant output presented as final; pilot touches CIW implementation path or creates cron.

---

*Proposed draft for Founder review. Not approved, not canonical, not committed.*
<!-- 2026-08-05 14:26 UTC+7 -->
