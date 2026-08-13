# STAGE 1.1 — Amended Design Review Report

**Project:** IIP + IPM Hermes Harness Reconstitution (Single Kanban)
**Status:** Stage 1 APPROVED WITH REQUIRED AMENDMENTS — Stage 2 NOT authorized
**Date:** 2026-08-12
**Mode:** READ-ONLY (no config/profile/repo/skill/kanban mutation). One artifact write (this file) approved as O6.
**Evidence base:** live Hermes v0.20.0 runtime + IIP repo HEAD 9967459 + IPM repo HEAD abc7436 + FD register (FOUNDERS-DECISIONS item 89/109) + installed configs/skills.

---

## Part 1 — Required Amendments Incorporated (10/10)

### 1. P0 — MODEL ROUTING GOVERNANCE DRIFT (elevated)

| Layer | Delegation model | Reasoning |
|---|---|---|
| Global `config.yaml` (top-level) | **`gpt-5.6-sol-medium`** ← drift | high |
| All 20 profile configs (incl. iip + 11 org-*) | `gpt-5.6-sol` | high |
| FD #93 (FOUNDERS-DECISIONS item 109, 11 Aug 2026) | `gpt-5.6-sol` (openai-codex) | **high** (reverted from medium) |
| sync-governance.py CUR_DELEG text | `gpt-5.6-sol` | high |
| SOUL.md Model Routing sections (shared + iip) | `gpt-5.6-sol` | high |

**Verdict: real drift, single point** — global `config.yaml` differs from approved `gpt-5.6-sol`. Every profile overrides it correctly today, but any profile relying on global inheritance (e.g. future `ipm` delegation config, or a new profile) inherits the wrong model name.

**Gate (binding):** No CRO / Auditor / independent-reviewer Kanban pilot may begin until global config is reconciled to `gpt-5.6-sol` and verified 13/13 configs (re-run FD #93 verification pattern). No CRO/Audit pilot bypasses this gate.

### 2. Filesystem Isolation Verdict — DEFERRED (was: B accepted)

**Previous claim "hard isolation not practical on Windows" — RETRACTED as unproven.** v0.20.0 supports **6 terminal backends**: `local`, `docker`, `modal`, `ssh`, `daytona`, `vercel_sandbox` (setup.py idx_to_backend: 0-5). Hard isolation is therefore *feasible in principle*; it was never tested on this machine.

```
FILESYSTEM ISOLATION VERDICT: DEFERRED — FEASIBILITY TEST REQUIRED
```

- **Allowed now:** sanitized IPM pilot task (no portfolio-sensitive data) on the shared board.
- **Blocked:** production IPM task on shared board until an explicit isolation verdict + Founder acceptance of residual risk (if logical-only is the outcome).

**Feasibility test scope (Stage 3):** (a) docker backend availability on this host (`hermes setup terminal` → docker), (b) WSL2/container mount design for IIP-only vs IPM-only workspaces, (c) `restricted backend` / per-profile terminal backend separation, (d) OS ACL alternative. Document results → verdict A (hard) or B (logical-only + quantified residual risk) → Founder acceptance.

### 3. Pre-Migration Repository Hygiene Gate — REQUIRED

Current IIP working tree (verified 2026-08-12):

```
Deleted (unstaged): ChatGPT/FOUNDER-DIRECTION-EQUITY-INFLECTION-DISCOVERY-AUDITED.md
                    ChatGPT/IIP-CONSOLIDATED-BIBLE-CIW-INTEGRATION-v0.1-COUNCIL-DRAFT.md
                    ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md
Modified:           PROJECT_STATE.md, SESSION_CLOSEOUT.md
Untracked:          ChatGPT/Integration 12 Aug 2026/  (handoff files — source of this report)
                    docs/ciw-pilot-msft/monitoring/2026-08-10-monitoring-draft.md
No stash. Branches: main (HEAD 9967459), agent/T0-phase5-arch, agent/T1-weak-signal,
                    agent/T2-anomaly, agent/T3-hypothesis, agent/T4-radar, org-pack-v0.1
```

**Gate:** Stage 2 MUST run from a **clean migration branch/worktree created from known HEAD** (`main` 9967459), or an explicitly Founder-approved preservation plan for the dirty items. **Hermes must NOT stash / commit / delete / overwrite the current dirty work automatically.** Uncommitted items get owner/source identification and explicit reconciliation decision before any migration patch touches the tree.

### 4. Progressive Kanban Enablement — NOT bulk

Enablement order (pilot only):

```
1. iip          (control — orchestrator)
2. org-cos      (triage/routing)
3. org-data-steward  (one specialist; source-preflight role)
4. ipm          (sanitized task only)
```

Test per profile: create → assign → dispatch → worker → heartbeat → block → comment → complete → restart. Only after the full lifecycle passes on this set do subsequent profiles get enabled (one batch at a time, Founder gate per batch).

### 5. Skill Responsibility Overlap Matrix — replaces "8 NEW skills"

Founder principle adopted: **approve responsibilities, not filenames.**

| Proposed responsibility (Harness v1.1) | Existing skill | Coverage | Action |
|---|---|---|---|
| Evidence / source admission / PIT / lineage | `sec-edgar-research` (retrieval), `iip-evidence` (n/a — none exists) | partial | compose/extend sec-edgar + Evidence Model; new only if gap proven |
| Publication / Facts Locked / Thai editorial | `iip-editorial-publication` | **substantial** | AMEND — do not create new |
| Deep company research | `fundamental-company-research` (CIW slices) | partial/substantial | inspect; extend for Gemini DR lane |
| Org/harness operation (10 profiles, kanban/holds) | `iip-hermes-workforce` | **overlap** | reshape/retire into capital-kanban + hermes-harness-admin ownership |
| Discovery audit (v1.1) | none (new workstream) | none | NEW likely justified (iip-discovery-audit) |
| Kanban org policy (one-board/tenant/privacy) | `iip-hermes-workforce` (partial), KANBAN-CONTRACT (repo) | partial | NEW or extend — pending matrix |
| IPM operating review | `simulated-portfolio-office` (skill exists per skill index) | partial | inspect before creating ipm-operating-review |
| IIP↔IPM handoff/firewall | none dedicated | none | NEW or fold into capital-kanban |

**Expected outcome:** net-new skills likely **3–5, not 8**. Every "create" must pass a documented gap: responsibility not covered by any existing skill/repo contract.

### 6. SOUL Instruction Migration Matrix — REQUIRED before convergence

The 26KB profile SOULs are composed by `sync-governance.py` = canonical `shared/SOUL.md` + spliced `shared/project-context/<profile>.md` between `PROFILE_CONTEXT_BEGIN/END` markers. Section inventory of installed iip SOUL (387 lines):

| Existing SOUL clause | Destination |
|---|---|
| Verify-First Rule, Audit Delegation, Production-Ready Audit Gate, LLM Council Gate, Governance Sync Gate | AGENTS (project rules) — already in AGENTS.md |
| Founder Context, Communication Style | shared USER/identity — keep in SOUL (identity) |
| Obsidian Memory Recall/Capture, Session Protocol, PROJECT_STATE rules, Closeout Gate | Skill (obsidian-memory) / AGENTS |
| Workflow Rules, Smart Scope, Automated Gates, Model Routing (3-Tier), UI/Design Rules, Documentation Rules | AGENTS + project-workflow v3.8 + config/FD |
| Project Context, Central KB, Vault Brain | AGENTS / skill references |
| Role-specific project-context splice (per-profile) | PRINCIPAL.md (canonical role contracts in repo) |

**Constraint (binding):** 0 binding instructions lost. Matrix must be completed (clause-by-clause) BEFORE any profile SOUL converges; each clause maps to exactly one destination. Content-hash verification of composed SOULs after switch.

**Mechanism note:** v0.20.0 has NO SOUL inheritance/pointer mechanism — convergence means **same content**, not same filesystem pointer. `sync-governance.py` composition already implements this (canonical shared + per-profile context splice); converge by shrinking canonical SOUL + moving instruction classes to AGENTS/PRINCIPAL/skills, preserving the compose-sync architecture.

### 7. `/kanban` + `/org-office` — READ-ONLY adapter only (initial round)

Current frontend: `KanbanBoardPage.tsx` + `OrgOfficePage.tsx` consume `orgClient.ts` → `backend/api/org_routes.py` (FD #55 read-only endpoints, repo-board data).

**Locked design for Stage 7 rewire:**
```
Hermes Kanban (kanban/boards/iip/kanban.db)
        │
        ▼
local read-only adapter/proxy (new backend route — READ ONLY)
        │
        ├── /kanban  (KanbanBoardPage)
        └── /org-office (OrgOfficePage)
```
- Browser frontend never calls Hermes mutation endpoints directly.
- Writes remain in `hermes kanban` CLI / native dashboard / agent tools.
- Founder drag/drop from IIP UI = later decision, after stable pilot.

### 8. Board `other` — DO NOT DELETE; provenance classified

Provenance query (board `other` kanban.db, 185 tasks):

```
created_at range:  2026-07-27 15:37:35 → 16:29:46  (single ~52-min window)
created_by:        dashboard=143, None=36, alice=6
workspace_kind:    scratch=185 (100%)
tenant:            None=182, acme/t1/t2 = 3 (test tenants)
titles:            "x", "a", "b", "c", "parent", "child", "renamed",
                   "other-only", "default-live", "other-live" (test artifacts)
bodies:            decomposer boilerplate ("Clarify the idea...", "Keep the task...")
board "default"    board.json default_workdir → .pytest-hermes-kanban-final/ (test path)
```

**Classification: TEST_CONFIRMED (high confidence) — created during kanban feature testing (dashboard + pytest, 27 Jul).** Still NOT deleted: deletion requires (a) Founder decision, (b) one more spot-check (sample full task bodies/comments for any non-test content), (c) deletion through `hermes kanban boards rm` (archive path) rather than raw file removal.

**"One Board" scope clarification (adopted):** One board applies to **IIP + IPM only**. `capital-command`, `notebooklm-kb`, `robot-trading`, `default` boards belong to other projects — **NOT deleted, NOT merged**. Current board pointer must switch from `other` → `iip` during Stage 3.

### 9. Legacy top-level `user.md` — DO NOT delete yet

Verified dependency: `sync-governance.py` treats `shared/user.md` as CANONICAL and writes `HERMES/user.md` (top-level) + `profiles/<p>/memories/USER.md` as TARGETS (USER_TARGETS). The watchdog (`cross-profile-sync-watchdog.py`) also reads `memories/USER.md`. **Top-level user.md is a live sync target — deleting it without editing the script breaks sync.** Required before retirement: inspect full sync/load path (which file runtime actually loads at session start — memory system loads `memories/USER.md`; top-level user.md is a sync artifact), then amend script + retire duplicates together with rollback.

### 10. Memory char limit — determined AFTER cleanup, not fixed

Current: `memory_char_limit: 3500`, `user_char_limit: 2000` (config); iip MEMORY.md = 3,793 bytes (97% full — 3,489/3,500 chars).
- NOT treating 2200 as sacred. Process: clean wrong content (thesis/evidence/FD register/task state → repo/skills/Obsidian) → measure remaining legitimate operational facts → choose a small limit that fits reality (could be 900 or 2,400).
- Same principle for USER.md: sync content, then measure.

---

## Part 2 — Additional Findings from Stage 1.1 Verification

1. **sync-governance.py PROFILES list missing `org-radar-scout`** (16 profiles listed; watchdog has 17 incl. radar-scout). `iip-hermes-workforce` skill explicitly requires every org role in BOTH scripts. → Stage 2 must add org-radar-scout to sync script PROFILES (and re-run sync twice per the skill recipe). Drift source found.
2. **Board rename supported**: `hermes kanban boards rename <slug> <name>` exists (slug immutable) → O2 rename `iip` display name → "Capital Intelligence" is technically clean. `set-default-workdir` also exists → clearing board-level `default_workdir=IIP` is possible before IPM pilot (verify clear/empty semantics in Stage 3).
3. **`max_in_progress`** — not in config_defaults kanban block; only `max_in_progress_per_profile` exists (default None). Handoff's `max_in_progress: 3` is stale/invalid for v0.20.0 → use `max_in_progress_per_profile: 1` (handoff intent) + dispatcher's global behavior. **`auto_promote_children` — key does not exist**; dependency promotion is native dispatcher behavior. Both flagged in J section.
4. **IPM profile**: no `delegation` section (inherits global → would inherit the drifted `gpt-5.6-sol-medium`!). IPM model config must be an explicit Founder decision (not auto-copied from IIP) — O-IPM-MODEL below. IPM SOUL (2.6KB) already separate and correct.
5. **Cron health**: "IIP Daily Learning Loop" last_status = **error** — investigate before migration (independent of this reconstitution, but relevant to Cron plan L).

---

## Part 3 — Revised Founder Decisions Required (O1–O10 + O-IPM-MODEL)

| ID | Decision | Status |
|---|---|---|
| **O1** | Stage 1 evidence base | **APPROVE WITH REQUIRED AMENDMENTS** (this document) |
| **O2** | Single board target = existing board slug `iip` (IIP + IPM); rename display name → "Capital Intelligence" (slug unchanged); **clear board-level `default_workdir` before IPM pilot** | **APPROVE** |
| **O3** | Filesystem isolation verdict | **DEFER** — feasibility test required; production IPM blocked until verdict + Founder acceptance |
| **O4** | project-workflow v3.7.1 → v3.8 direction (engineering-only; KEEP Bible-first/SMART-SCOPE/root-cause/locked tests/Evidence QA/isolation/E2E/rollback; REMOVE all-task autoload/hard-coded models/per-task state machine/universal closeout/research Council duplication/domain truth in MEMORY) | **APPROVE DIRECTION** — v3.8 built as CANDIDATE beside v3.7.1 in Stage 2; promote only after Stage 4 pilot |
| **O5** | Board `other` deletion | **DO NOT DELETE YET** — provenance classified TEST_CONFIRMED (52-min test window 27 Jul); deletion after spot-check + explicit Founder decision |
| **O6** | Stage 1 evidence artifact | **APPROVE AFTER AMENDMENTS** — this file: `evidence/harness/STAGE1-REPORT-2026-08-12.md` |
| **O7** | Pre-Migration Repository Hygiene Gate | **REQUIRED** — clean migration branch/worktree from HEAD 9967459 or Founder-approved preservation plan; no auto stash/commit/delete of dirty work |
| **O8** | Skill architecture | **APPROVE responsibility map** (Part 1 §5); new skill creation DEFERRED pending overlap audit; net-new likely 3–5 |
| **O9** | SOUL convergence | **APPROVE direction** (one shared IIP Research SOUL) SUBJECT TO instruction-migration matrix (Part 1 §6) + 0 binding instructions lost |
| **O10** | Model routing drift | **RECONCILE REQUIRED** before any independent audit/challenger/CRO pilot — global config → `gpt-5.6-sol`; verify 13/13; P0 gate |
| **O-IPM-MODEL** | IPM model config | **FOUNDER DECISION REQUIRED (new)** — propose IPM model as separate decision; do not auto-copy IIP config; ipm profile currently has no delegation section |

---

## Part 4 — Gate Status

```
Stage 0  (baseline/backup): PARTIAL — runtime facts captured; backups at Stage 2 start
Stage 1  (design review):   APPROVED WITH AMENDMENTS  ← current position
Stage 2  (context/skills):  NOT AUTHORIZED
Stages 3–9: NOT AUTHORIZED
```

**Hermes will now STOP.** No config/profile/repo/skill/kanban/cron/UI mutation performed in Stage 1 or 1.1 (single artifact write = this report, O6-approved).

---
<!-- 2026-08-12 19:10:33 +0700 — M1: captured via scripts/artifact_timestamp.py (system clock at correction; agent-guessed timestamps rejected) -->
