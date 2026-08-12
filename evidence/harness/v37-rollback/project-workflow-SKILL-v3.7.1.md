---
name: project-workflow
description: Canonical workflow for all governed projects — Bible-First discipline, SMART-SCOPE principle, Domain Drift Guardrail, evidence-based QA, architecture review gates, locked acceptance tests, automated gate enforcement (v3.3), Loop Protocol v3, LLM Council independent review gates (v3.7), Milestone Council materiality rule + Quick Mode text-only exception + milestone evidence log (v3.7.1), and UI Dashboard Plugin.
version: 3.7.1
author: Chamnan + Hermes Agent
---

# Project Workflow v3.7.1 (Canonical)

Standard operating procedure for building software with Hermes Agent. Two execution modes: **Critical** (full) and **Quick** (lightweight).

> **v3.7.1 Changes (2026-08-02, FD-2026-08-02-REVIEW-FOLLOWUP — independent review of v3.7):** three improvements from the ChatGPT independent review (8.7/10):
> 1. **Execution order clarified** — Phase numbers = gate identities, NOT chronology; normative sequence: 0 Discovery/Grilling → -1 Constitution draft → Founder approval → 1 Spike → 2 Architecture → 2R Review → 3 Plan → 4 Implement → 5 Evidence QA → 6 Integration → 7 Release.
> 2. **Milestone Council Materiality Rule** — council mandatory only for material milestones (financial/architecture/data-integrity/security/user-workflow/irreversible/broad-regression); routine sub-milestones → Parent Evidence QA only. Conservative default: when in doubt, material.
> 3. **Quick Mode Text-Only Exception** — blacklisted-path changes may use Quick Mode if diff is verified text/CSS-only with zero logic change (`[quick-text-only]` commit tag); any logic change → escalate to Critical.
> Plus: milestone evidence-log template (`references/milestone-evidence-log.md`) for evidence-driven evolution, and one-page adoption cheat-sheet (`references/workflow-cheat-sheet.md`).
> **v3.7.1 capability adaptations (2026-08-02, FD-2026-08-02-CAP-ADAPT — ChatGPT capability-upgrade recommendations, Option B):** adopted 4 operational controls without new governance layers: (1) **Session Preflight Check** (`references/session-preflight.sh`) — deterministic pre-work verification of profile/branch/tree/Bible/state/Council artifacts/secrets/model; (2) **Project Truth Map** (`references/project-truth-map-template.md`) — explicit authoritative-source table + conflict rule; (3) **Mutation Testing Lite** (`references/mutation-testing-lite.md`) — Evidence QA point 11 for high-value financial logic; (4) **Property/Invariant Testing** (`references/property-invariant-testing.md`) — Evidence QA point 12. Per review §5: no further governance additions until 2-3 projects of evidence (v3.8).
> **v3.7 Changes:** FD-2026-08-01-LLM-COUNCIL — LLM Council integration (Option B). Added §0C: independent review gates at 6 decision points (Bible Council, Plan Council Lite, Test Charter Review, Diagnostic Council, Milestone Council, Final Council) with structured COUNCIL DECISION output contract. Reuses existing Sol Medium delegation — zero new infrastructure. Companion skill: `llm-council` v1.0.0. Mandatory gates: Bible (-1), Milestone (5→6), Final (7). Conditional Lite: Plan (3), Test Charter, Diagnostic (5). Prohibited: Quick Mode, typo fixes, routine CRUD.
> **v3.7 reconciliation (2026-08-01):** internal consistency fix — architecture header corrected to 2 Roles, 3 Models; duplicated ROLE 4 line removed from Sol Medium diagram; ALL Sol Medium fallback references unified to `openai/gpt-5.6-luna` (openrouter). No semantic change, version stays 3.7.0.
> **v3.7 enforcement (2026-08-01):** Council Artifact Gate (A+B+C) — every council run MUST persist `evidence/COUNCIL_DECISION-<gate>-<date>.md`; presentation to Founder blocked without artifact (kills silent-skip + fast-approval race); Closeout Checklist item added; SOUL.md triggers hardened (artifact-gated, mandatory gates have NO skip). Companion skill `llm-council` → v1.1.0.
> **v3.6 Changes:** FD-2026-08-01-FLASH-PRIMARY — DeepSeek V4 Flash (reasoning: high) promoted to primary model. Pro tier retired. Flash handles ALL Parent-level work: conversation, planning, architecture, financial logic, and easy/mechanical tasks. Sol Medium remains for audit delegation only.
> **v3.5 Changes:** FD-2026-07-31-DELEGATION-SOL — 3-Tier Model Routing. Flash tier removed (delegate_task only supports ONE delegation.model). All 7 profiles set to `gpt-5.6-sol` via `openai-codex`. Easy/mechanical tasks → Parent handles directly. Escalation ladder simplified 5→4 steps (L1=Parent, L2=Re-spec, L3=Sol Medium, L4=Founder).
> **v3.3.0 Changes:** Automated Gate Enforcement (FD-2026-07-30-AUTO-GATES) — 5 enforcement mechanisms: (1) gate-check script for automated Gate 1-6 verification, (2) Parent re-verify rule for Evidence QA, (3) closeout_status tracking in PROJECT_STATE.md, (4) regression_count in task contracts, (5) isolation-scan.sh for forbidden_paths violation detection. Evidence QA expanded 8→10 points. Reference scripts: `gate-check-template.sh` + `isolation-scan.sh`.
> **v3.2.1 Changes:** Phase 3 Plan granularity upgrade (FD-2026-07-30-PLAN-DETAIL) — task contracts now require expected test outputs, edge case specs, and verify commands per task. `plan` skill upgraded to v2.1.0. Full copy-pasteable code no longer required — code contracts/patterns sufficient.
> **v3.2 Changes:** Added 6 Systemic Quality Gates (FD-108) — Root-Cause Gate, Validation Boundary Rule, Deployment Verify, Feature Complete Definition, Batch Atomicity, Verification Evidence Tags. Evidence QA expanded from 6→8 points (negative paths + deployment smoke). Acceptance Lock Rule (ห้ามเปลี่ยน locked test โดยไม่มี Bible quote). Canonical Test Rule (ทุก Acceptance Example ต้องมี automated test). Added Verify-First Enforcement (FD-HERMES-003) — automated gate in SOUL.md. Added SMART-SCOPE Escape Hatch (FD-2026-07-30-SMART-AUDIT) — governance-audit Layer 0.9 anti-overinvestment. Added Automated Governance Regression (FD-2026-07-30-GOV-REGRESSION) — 3 watchdog crons (cross-profile sync, governance health, frontend synthetic data). Added FINISHING THE JOB rule — deliver working artifact, never fabricate output. Added Audit Delegation Rule (FD-HERMES-007) — all governance audits MUST delegate to gpt-5.6-sol (openai-codex); Parent FORBIDDEN from handling audits directly.
> **v3.1 Changes:** Added Smart Scope Principle (FD-2026-07-28-SMART-SCOPE) — "Work smart, not think hard but not smart." Anti-overengineering guardrails for all models. Added UI Dashboard Plugin — delegates dashboard/UI tasks to `ui-dashboard-workflow` skill. Model routing table updated with scope verification column.
> **v3.0 Changes:** Removed Luna/Luna Pro Max references → DeepSeek-only. Simplified escalation (7→3 steps). Removed False-Pass Rate tracking. Aligned with Loop Protocol (AGENTS.md + SESSION_CLOSEOUT.md). Removed MAX suffix. Config section reflects FD-HERMES-002.

## Architecture: 2 Roles, 3 Models

```
┌──────────────────────────────────────────────────────┐
│  👤 FOUNDER — Final Authority                         │
│  approve · escalate · kill tasks · resolve conflicts  │
└──────────────────────┬───────────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────────┐
│  🤖 PARENT — deepseek-v4-flash (reasoning: high)       │
│                                                       │
│  ROLE 1 (CTO): Architecture · Planning · Delegate    │
│  ROLE 2 (QA):   Integration · Review · Release       │
│                                                       │
│  Complex/Financial/Judgement → Parent handles         │
│  Easy/Mechanical → Parent handles directly             │
│  Architecture Review / Debug Escalation → Sol Medium   │
└───────┬───────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│  🤖 SOL MEDIUM — GPT-5.6 Sol Medium (subagent only)   │
│                                                       │
│  ROLE 3 (Reviewer): Architecture QA · Debug escalate  │
│                                                       │
│  Isolated worktrees · owned/forbidden paths           │
│  max_concurrent_children: 10 (ceiling, not default)   │
│                                                       │
│  Provider: openai-codex (subscription)                 │
│  Phase 2R hostile reviewer · L3 fresh-eyes debugger   │
│  Different model family = unbiased review             │
│  Unavailable → fallback to Luna (openrouter)          │
└──────────────────────────────────────────────────────┘
```

## §0 Core Principles (Non-Negotiable)

Three pillars that govern ALL work, ALL models, ALL projects:

### Pillar 1: Bible-First (Domain Authority)

```
Bible → AGENTS.md → delegate audit → fix stale → plan
New requirement → record as FD (Founder Decision) → update Bible
```

- Bible is the single source of domain truth — NOT memory, NOT FD summaries, NOT module names
- Never say "ไม่มี logic" if Bible FDs exist — say "ยังไม่มี service layer ที่ enforce domain rules ในโค้ด"
- Every material decision must be traceable to a Bible section or FD

### Pillar 2: SMART-SCOPE (Work Smart, Not Think Hard)

> **FD-2026-07-28** — The single most important behavioral rule.

| ✅ DO | ❌ DON'T |
|-------|---------|
| Answer what Founder asked | Add features "เผื่อไว้ก่อน" |
| Solve the stated problem | Solve problems you imagine |
| 2-3 relevant options | 5+ options with diminishing returns |
| Minimal architecture that works | "Best practice" gold-plating |
| Verify objective is met | Test scenarios outside scope |

**Self-Check (Before Every Action):** *"Is this directly addressing the Founder's objective, or am I creating work?"*

### Pillar 3: Domain Guardrail (Drift Prevention)

> **FD-2026-07-28** — 2.5-layer system to prevent AI from drifting from core domain understanding.

| Layer | Mechanism | When |
|-------|-----------|------|
| **Layer 1** | Identity Card in memory (~250 chars) | Every turn |
| **Layer 1.5** | Domain Index in AGENTS.md | Session start |
| **Layer 2** | Spec-before-Answer rule | On domain questions |

> `ก่อนตอบคำถามเกี่ยวกับ domain logic → อ่าน spec จริงจาก project-definition/ หรือ PROJECT_BIBLE ก่อนตอบ ห้าม deduce จากชื่อ module, FD summary, หรือ memory`

### New Requirements → Record as FD

When the Founder proposes new requirements:
- Record as FD (Founder Decision) immediately — do NOT wait until end of session
- Update Bible if the FD changes domain rules, invariants, or module specs

---

## Two Execution Modes

### 🔴 CRITICAL MODE

Use for: architecture, financial logic, multi-file features, new subsystems, **AND any task touching these paths:**

| Forbidden for Quick Mode |
|--------------------------|
| `src/auth/**` · `src/broker/**` · `src/ml/**` |
| `src/migration/**` · `src/calculation/**` |
| `src/database/schema/**` · `src/audit/**` |

```
Critical Workflow:
Discovery → Spike → Architecture → Review Gate → Plan →
Isolated Implementation (locked tests) → Evidence QA → Integration → Release
```

### 🟢 QUICK MODE

Use for: typo fixes, docs, CSS, log statements, single-file edits NOT in blacklist.

```
Quick Workflow:
  1. Inspect → 2. Change → 3. Smoke Test → 4. Commit
```

**Quick Mode Examples:**

| Task | Mode | Reason |
|------|------|--------|
| เปลี่ยนสีปุ่มจาก blue → mint | 🟢 Quick | Visual only, no logic change |
| เพิ่ม tooltip บน KPI card | 🟢 Quick | Single component, no data change |
| แก้คำผิดใน label | 🟢 Quick | Text only |
| ปรับ spacing ระหว่าง cards | 🟢 Quick | CSS only, layout structure unchanged |
| เปลี่ยน chart จาก line → bar | 🔴 Critical | Changes how data is interpreted — requires Architecture review |
| เพิ่ม filter ใหม่บน dashboard | 🔴 Critical | Changes data flow — requires Plan + Evidence QA |
| เพิ่มหน้าใหม่ทั้งหน้า | 🔴 Critical | New subsystem — full workflow |
| เปลี่ยน layout จาก 2-column → 3-column | 🔴 Critical | Structural change — affects all components |

**Safety Net:** After Quick commit, run 3-5 critical-path smoke tests. Any fail → escalate to Critical.

**Text-Only Exception (v3.7.1 — FD-2026-08-02-REVIEW-FOLLOWUP):** A change INSIDE a blacklisted path may use Quick Mode IF it is verified **text/CSS-only with zero logic change**:

- Allowed: typo fix in an error message, label text, comment, log string, CSS value/color/spacing
- Verify before commit: `git diff` shows ONLY string/CSS changes — no conditionals, no control flow, no validation logic, no schema, no API signature change
- If the diff touches any code beyond text/CSS → **escalate to Critical Mode** immediately
- Record the verification in the commit message: `[quick-text-only] diff verified no logic change`

This keeps the blacklist conservative for behavior changes while removing ceremony for genuinely cosmetic edits. When in doubt → Critical Mode (safety over speed).

## Session Start: Loop Protocol v3

Every project uses the standard Loop Protocol (defined in project AGENTS.md):

```
START → AGENTS.md → Domain Index → PROJECT_STATE.md → SESSION_CLOSEOUT.md → Verify → Execute → CLOSEOUT
```

1. Memory auto-injects **Identity Cards** (Layer 1 — domain checksum every turn)
2. Agent reads AGENTS.md → sees **Domain Guardrail rule** + **Domain Index** (module→spec mapping)
3. Agent reads **PROJECT_STATE.md** (🎯 current phase, blockers, next action — primary state file)
4. Agent reads SESSION_CLOSEOUT.md (last session context — supplementary)
5. Agent verifies: `hermes profile list`, git status, phase state
6. Agent presents: "ระยะนี้ ต่อด้วย X ดีไหม?"
7. Work executes. **After EVERY Founder approval/decision:**
   - Record FD in vault `fd-register.md` IMMEDIATELY (don't wait until session end)
   - Format: `FD-YYYY-MM-DD-SHORTID: [one-line title]`
   - Update Bible if the FD changes domain rules, invariants, or module specs
8. Session ends → update PROJECT_STATE.md + write new SESSION_CLOSEOUT.md + complete Closeout Checklist

**Session Preflight (v3.7.1 — FD-2026-08-02-CAP-ADAPT):** for governed projects, run `bash scripts/session-preflight.sh <project_root>` (template: `references/session-preflight.sh`) before meaningful work — deterministic check of profile, branch, working-tree, Bible/state files, required Council artifacts, `.env` ignored, and actual resolved model. Exit 1 = BLOCKED (fix operational state before reasoning). This catches the failure class: *high-quality work in the wrong operational context.*

**Project Truth Map (v3.7.1 — FD-2026-08-02-CAP-ADAPT):** projects should maintain `PROJECT_TRUTH_MAP.md` (template: `references/project-truth-map-template.md`) — the explicit table of which file is authoritative for each class of question (Bible > FD register > PROJECT_STATE > plan > session logs). Conflict rule: identify conflicts explicitly, apply hierarchy, escalate equal-authority conflicts, never change implementation to make docs appear consistent.

### §0A Systemic Quality Gates (FD-108 — v3.2)

These gates address the four discipline gaps identified in Codex audit:
1. **Domain-first reasoning** — not symptom-first
2. **End-to-end verification** — not just unit tests
3. **User-workflow completion** — not "API exists = feature done"
4. **Root-cause correction** — not patching outputs

### Gate 1: Root-Cause Gate

Before fixing any output or formula, ask:
- *"Where does this data originate? What's the aggregation grain?"*
- Trace upstream to the data model before changing the output calculation
- Symptom: changing formula → Root cause: wrong aggregation grain, wrong entity identity

**Self-check:** *"Am I fixing the symptom or the data model?"*

### Gate 2: Validation Boundary Rule

> **Base validation at schema boundary (Pydantic/request schema). Business validation at service layer.**

| Layer | What | Example |
|-------|------|---------|
| Schema (Pydantic) | side ∈ {BUY,SELL}, quantity > 0, price > 0 | ALL transactions |
| Service (Business) | Zone/Cycle lineage, LZF allocation | Close System only |

Never put base validation inside conditional blocks (e.g., only when Zone+Cycle present).

### Gate 3: Deployment Verify

After ANY schema change (new model, new column, migration):
```
alembic upgrade head && alembic check
```
Must pass on the database created by Alembic — not just on Base.metadata.create_all().

### Gate 4: Feature Complete Definition

> **Feature done = user completes workflow from UI.** Not "API endpoint exists."

Checklist before closing a feature:
- [ ] Backend endpoint + validation + error handling
- [ ] Frontend UI with loading/empty/error/success states
- [ ] User can complete the full workflow (import → preview → confirm → see result)
- [ ] Unhappy paths tested (duplicate, invalid input, missing dependency)
- [ ] Template/sample provided if applicable

### Gate 5: Batch Atomicity

> **Batch operations (import, bulk update) MUST be all-or-nothing.**

- Pre-validate all rows BEFORE committing any
- Detect duplicates by natural key (broker_ref, etc.)
- If ANY row fails → reject entire batch with error details
- Never silently partial-commit

### Gate 6: Verification Evidence Tags

Closeout must include classification of every claim:

| Tag | Meaning | Example |
|-----|---------|---------|
| `TEST_VERIFIED` | Automated test passes | 258/258 pytest |
| `STATIC_OBSERVATION` | Inspected but not tested | alembic check clean, schema matches |
| `EXTERNAL_NOT_TESTED` | Depends on external system not verified | Frontend build passes, browser not tested |
| `INFERENCE` | Logical deduction from other evidence | Grain correct because per-cycle resolution matches Bible |

### §0B Automated Gate Enforcement (FD-2026-07-30-AUTO-GATES — v3.3.0)

Gate enforcement was previously manual (Parent checks all 6 gates). v3.3.0 adds 5 automated enforcement mechanisms to reduce human error:

#### 1. Gate Check Script

Before accepting any implementation task as DONE, run `gate-check-template.sh` (project-adapted copy):

```bash
bash scripts/gate-check.sh [project_root]
# Exit 0 = all gates passed
# Exit 1 = one or more gates failed
```

Template covers: Gate 1 (root-cause evidence), Gate 2 (validation boundary), Gate 3 (alembic check if schema changed), Gate 4 (UI states), Gate 5 (batch atomicity), Gate 6 (evidence tags).

#### 2. Parent Re-Verify Rule

> **Parent MUST re-run locked tests and canonical tests independently — never trust subagent self-report.**

Subagent summary = SELF-REPORT. Parent verification sequence:
1. Run locked tests → confirm pass
2. Run canonical tests → confirm pass
3. Run `gate-check.sh` → confirm exit 0
4. Run `isolation-scan.sh` → confirm no violations
5. Only then mark task DONE

#### 3. Closeout Enforcement

`PROJECT_STATE.md` now includes `closeout_status`:

```yaml
session:
  closeout_status: pending  # pending | completed
  fd_count: 2
```

Session cannot be marked complete without `closeout_status: completed`. The Closeout Checklist is now gated — Parent must explicitly toggle this field.

#### 4. Regression Budget Tracking

Task contracts now include `regression_count`:

```yaml
task_id: T12
regression_budget:
  max: 2
  current: 0
```

Regression count persists in task state file (`tasks/T12-state.md`) — survives session boundaries. 3rd regression auto-escalates to Founder.

#### 5. Isolation Violation Scanner

Run `isolation-scan.sh` to detect subagent changes to forbidden paths:

```bash
bash scripts/isolation-scan.sh [project_root] [task_contract_file]
# Exit 0 = no violations
# Exit 1 = forbidden path(s) modified
```

Scans git diff (tracked + untracked) against `forbidden_paths` from task contract. Any match → reject task, escalate to Parent.

### §0C LLM Council Integration (FD-2026-08-01-LLM-COUNCIL — v3.7)

Independent review gates at material decision points — NOT a committee for every task. Companion skill: `llm-council` v1.0.0. Council = one independent Sol Medium subagent + structured COUNCIL DECISION contract (no multi-model, no new delegation).

#### Mandatory Council Gates

| Gate | Phase | When | Mode |
|------|-------|------|------|
| **Bible Council** | -1 | after draft PROJECT_BIBLE.md, before Founder approval | Standard (3-4 roles) |
| **Milestone Council** | 5→6 | after milestone + Close Beta verification, before Integration — **if material** (see Materiality Rule below) | Standard (3-4 roles) |
| **Final Council** | 7 | before Founder acceptance | Standard (3-4 roles) |

#### Milestone Council Materiality Rule (v3.7.1 — FD-2026-08-02-REVIEW-FOLLOWUP)

Milestone Council is mandatory ONLY for **material milestones**. Routine sub-milestones skip the council and use Parent Evidence QA only (10-point checklist + gate check + isolation scan).

**Material** milestone — Council mandatory if ANY of:
- financial impact (calculations, money movement, portfolio values)
- architecture impact (new subsystem, schema change, structural refactor)
- data integrity (migrations, aggregation grain, persistence)
- permission/security changes (auth, access control, audit paths)
- critical user workflow changes (user-facing behavior, import/export flows)
- irreversible decisions (deletions, rewrites, locked-test changes)
- broad regression exposure (touches many modules or shared paths)

**Routine sub-milestone** — Parent Evidence QA only if ALL of:
- narrow internal refactor, minor settings change, isolated helper change
- small documentation-linked implementation step
- no forbidden-path touches (`src/auth/**`, `src/broker/**`, `src/ml/**`, `src/migration/**`, `src/calculation/**`, `src/database/schema/**`, `src/audit/**`)
- no financial logic, no schema change, no permission change
- strong automated coverage on affected code

When in doubt → treat as material (conservative default). If the Founder overrides a skip, record it as an FD.

#### Conditional Council Gates (Lite — 2-3 roles)

| Gate | Trigger |
|------|---------|
| **Plan Council** (Phase 3) | Critical Mode + forbidden paths (auth/broker/ml/migration/calc/schema/audit) or financial logic |
| **Test Charter Review** (Phase 5) | milestone with high data/finance/permission risk (optional) |
| **Diagnostic Council** (Phase 5) | complex defects: unclear root cause, repeated failure, multi-layer disagreement, multiple fix paths |

#### Prohibited

Quick Mode entirely, typo fixes, cosmetic changes, routine CRUD, known deterministic fixes, trivial doc edits, every test case, every commit.

#### Council Output Contract (mandatory)

Every council run returns `COUNCIL DECISION`:

```text
## Gate        — Bible / Plan / Diagnostic / Milestone / Final
## Verdict     — PASS / PASS WITH FIXES / RETEST / REWORK / FOUNDER DECISION REQUIRED
## Material Findings     — critical only, linked to evidence
## Required Changes      — smallest sufficient corrections
## Evidence Gaps         — None | list
## Founder Decisions Required — None | list
## Minority Warning      — None | description
## Scope Expansion Check — none | rejected | founder approval required
```

#### Execution Rules

1. Council runs via existing `delegate_task` → `gpt-5.6-sol` (openai-codex) — **no config change**
2. Parent assembles Evidence Packet → delegates ONE Sol Medium subagent
3. Council NEVER edits Bible/plan/code — findings return to Main Agent
4. Parent evaluates → fixes → retests → escalates Founder decisions
5. Finding valid ONLY if: concrete + linked to evidence + material impact + smallest correction + verify method
6. Milestone question: "Is this milestone sufficiently complete, correct, and evidenced to proceed?" — NEVER "How can it be even better?"
7. Absence of findings is an acceptable result
8. **Artifact Gate (v3.7 enforcement):** Parent writes council output verbatim to `<project_root>/evidence/COUNCIL_DECISION-<gate>-<date>.md` (create `evidence/` if missing) and MUST NOT present Bible / milestone / final release to Founder without it. No artifact = no presentation = run council now

**Fallback:** Sol Medium unavailable → `gpt-5.6-luna` via openrouter (existing fallback chain). Report to Founder.

## Closeout Checklist (Mandatory — every session end)

Before closing, agent MUST confirm AND gate enforcement must pass:

- [ ] **FDs recorded?** — List FD numbers created this session (or "none")
- [ ] **Bible updated?** — Which sections changed? (or "no changes needed")
- [ ] **PROJECT_STATE.md updated?** — Phase, blockers, next action current?
- [ ] **Verify-First?** — Every claim backed by real file evidence? (FD-HERMES-003)
- [ ] **Verification Tags present?** — TEST_VERIFIED, STATIC_OBSERVATION, INFERENCE with evidence
- [ ] **Acceptance Lock respected?** — No locked test expected values changed without Bible quote
- [ ] **🆕 Closeout status toggled?** — `closeout_status: completed` in PROJECT_STATE.md (v3.3.0)
- [ ] **🆕 Gate check passed?** — `gate-check.sh` exit 0 for all modified tasks (v3.3.0)
- [ ] **🆕 Council gates fired?** — Mandatory gates (Bible -1 / Milestone 5→6 / Final 7) ran when due; `evidence/COUNCIL_DECISION-*.md` artifact present (v3.7 enforcement)

| File | Role |
|---|---|
| **PROJECT_STATE.md** | 🎯 Persistent — phase, blockers, next action, latest FD |
| **SESSION_CLOSEOUT.md** | 📝 Ephemeral — what happened last session, context supplement |

**Domain Guardrail in Action:** When a domain question arises (e.g., "Close System ทำอะไร?"), the Spec-before-Answer rule triggers → Domain Index points to the exact spec file → AI reads spec → answers from source. Never deduce from module name or memory.

**Why:** SESSION_CLOSEOUT alone = "เกิดอะไรขึ้นครั้งที่แล้ว" → ไม่รู้ว่า project อยู่ตรงไหนเมื่อทุกอย่างเสร็จ PROJECT_STATE = "project อยู่ phase ไหน อะไรค้าง" → รู้เสมอว่าต้องทำอะไรต่อ

**Audit Gate (MANDATORY — FD-HERMES-007):** All governance audits, Bible audits, and full project audits MUST delegate to `gpt-5.6-sol` via `openai-codex`. Parent is FORBIDDEN from handling audits directly.

| Trigger | Delegate Target |
|----------|-----------------|
| "full audit" / "governance audit" | `gpt-5.6-sol` (openai-codex) |
| "ตรวจ Bible" / "audit project" | `gpt-5.6-sol` (openai-codex) |
| Phase 2R Architecture Review (hostile reviewer) | `gpt-5.6-sol` (openai-codex) |
| "fresh eyes" review | `gpt-5.6-sol` (openai-codex) |

**Fallback:** If `gpt-5.6-sol` unavailable → fallback to `openai/gpt-5.6-luna` (openrouter). Report to Founder.

**Rationale:** Parent handling its own audit creates a blind spot — same agent plans AND audits (conflict of interest). Sol Medium provides independent adversarial review.

## Domain Constitution Gate (Phase -1)

Before advancing to Architecture, these MUST be Founder-approved:

```
PROJECT_BIBLE.md       — What we build, why, for whom
DOMAIN_MODEL.md        — Entities, relationships, business rules
FORBIDDEN_ACTIONS.md   — What the system must NEVER do
ACCEPTANCE_EXAMPLES.md — 3-5 real-life scenarios
```

## Phase Flow (Critical Mode)

> **Execution Order (clarified 2026-08-02, per independent review):** Phase numbers are **gate identities, NOT chronological order**. Chronologically, Discovery/Grilling happens FIRST, then the Domain Constitution is drafted and Founder-approved, then Architecture onwards:

```
Chronological:  Phase 0 Discovery & Grilling
                → Phase -1 Domain Constitution draft → Founder approval (Gate 0)
                → Phase 1 Spike → Phase 2 Architecture → Phase 2R Review
                → Phase 3 Plan → Phase 4 Implement → Phase 5 Evidence QA
                → Phase 6 Integration → Phase 7 Release
```

Phase -1 keeps its number because it is the **constitution gate** the whole project hangs on; do not reorder the numbering — only the execution sequence above is normative.

```
Phase -1: Domain Constitution → Founder approval
Phase 0:  Discovery           → grilling + domain-modeling
Phase 1:  Spike               → feasibility validation
Phase 2:  Architecture         → system design
Phase 2R: Architecture Review  → MANDATORY — Fresh QA or Founder
Phase 3:  Plan                 → task contracts (code contracts + expected outputs + edge cases + verify commands — FD-2026-07-30-PLAN-DETAIL)
Phase 4:  Implement            → delegate + TDD + locked tests

**Pre-Implementation Gate (Mandatory):** Before writing ANY code, agent MUST:
1. Read the relevant spec from Domain Index
2. State: `"Confirmed domain rule: [one-line summary from spec §X]"`
Phase 5:  Evidence QA          → 10-point checklist + automated gate check + isolation scan + locked tests
Phase 6:  Integration          → merge + code review + full suite
Phase 7:  Release              → PR workflow
```

### Phase 2R: Architecture Review Gate (MANDATORY)

Parent designs architecture in Phase 2. BEFORE Phase 3:

1. **Parent delegates Sol Medium subagent** with architecture doc + hostile reviewer prompt
2. Sol Medium reviews → returns PASS/FAIL with specific reasons
3. If Sol Medium unavailable → fallback to Luna (openrouter) review
4. **Parent presents Sol Medium findings to Founder** with recommendation
5. Founder decides: PASS → Phase 3, FAIL → revise (regression_count +1)
6. Architecture changes after review → mandatory re-review

### Regression Budget

Each task may regress phases **max 2 times**. 3rd regression → escalate to Founder with options A/B/C.

## Task Orchestration

### Financial Logic Rule

Financial calculations (Cost Basis, P&L, Options, Capital allocation) → **Parent handles directly** (Flash). Sol Medium subagents are FORBIDDEN from financial tasks. If a task contract involves financial numbers → mark `financial: true` and keep at Parent level.

### Task State Machine

```
BACKLOG → QUEUED → IN PROGRESS → DONE (evidence QA)
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
          RETRY     BLOCKED    CANCELLED
       (max 2×,    (dependency)  (obsolete)
       then re-spec)
```

### Task Isolation Contract

```yaml
task_id: T12
branch: agent/T12-auth-validation
isolation: worktree
owned_paths: [src/auth/**, tests/auth/**]
forbidden_paths: [src/database/**, src/broker/**]
locked_tests:
  - tests/locked/test_auth_validation.py
depends_on: [T8]
regression_budget:        # v3.3.0
  max: 2
  current: 0              # persists across sessions
```

## Evidence-Based Verification

### Locked Acceptance Tests

Before delegating, Parent writes acceptance tests as `locked_tests`:
- **Immutable** — subagent MUST NOT modify
- **Contractual** — subagent MUST make them pass
- **Spec-as-code** — executable specification

Parent verification: run locked tests first. If pass → spec implemented correctly.

### Acceptance Lock Rule (FD-108)

> **ห้ามเปลี่ยน expected value ใน locked/acceptance test โดยไม่มี Bible quote หรือ FD ใหม่กำกับใน commit message**

Tests are the contract between spec and implementation. If a locked test fails:
1. Read Bible → verify expected value against spec
2. If test is wrong → quote Bible section + get Founder approval BEFORE changing
3. If code is wrong → fix code, never the test

### Canonical Test Rule (FD-108)

> **Every Acceptance Example in ACCEPTANCE_EXAMPLES.md MUST have at least one automated test**

Acceptance Examples are the executable specification of the domain. Without automated tests, they are just documentation that can drift.

### Evidence QA (10-Point Checklist — v3.3.0)

1. Locked tests pass
2. Canonical tests pass (Acceptance Examples verified)
3. Targeted test suite passes
4. No regression in critical paths
5. Negative path tests exist (unhappy paths: missing dependencies, invalid input, duplicates, boundary conditions)
6. Diff review (no unintended changes)
7. Git status clean (no stray files)
8. Deployment smoke test (alembic upgrade + check if schema changed; API endpoint responds)
9. **🆕 Gate check automated — `gate-check.sh` exit 0 (v3.3.0)**
10. **🆕 Isolation scan clean — `isolation-scan.sh` exit 0 (v3.3.0)**

**Test-Strength Checks (v3.7.1 — FD-2026-08-02-CAP-ADAPT, high-value logic only):**
- **11. Mutation Testing Lite** — for financial/operational logic (cost basis, P&L, allocation, zone lifecycle, batch atomicity, permission, risk limits): apply 5–8 single mutations in an isolated worktree (op, boundary, ordering, rounding, dedup), confirm the suite catches each. Any surviving mutation = test-quality gap → add a locking test before DONE. Reference: `references/mutation-testing-lite.md`.
- **12. Property/Invariant Testing** — same high-value modules: generated-input tests for invariants (allocated ≤ available; closed cycle ⇒ no active obligation; batch all-or-nothing; reorder invariance; idempotency uniqueness; permission boundaries). Reference: `references/property-invariant-testing.md`.

> **Parent Re-Verify Rule (v3.3.0):** Parent MUST re-run locked tests and canonical tests independently. Never trust subagent self-report. Subagent summary = SELF-REPORT. Parent verification = evidence.

## Escalation Ladder (v3.5 — 4 steps)

```
L1: Parent (Flash) — retry with different approach, force re-spec
L2: Re-spec or breakdown → re-attempt (same model)
L3: Sol Medium subagent — fresh-eyes debug attempt
      (unavailable → Luna fallback; else skip to L4)
L4: 👤 FOUNDER — "Tried X, Y, Z. Options: A/B/C."
```

> **L3 (Sol Medium):** Different model family provides truly independent debugging perspective. Bounded context — only the failing task + error evidence. If Sol Medium and Luna are unavailable, skip to L4.

## Config Dependencies

```yaml
# FD-2026-08-01-FLASH-PRIMARY — 3-Tier, Flash Primary
model:
  default: deepseek-v4-flash
  provider: deepseek
  reasoning_effort: high
delegation:
  model: gpt-5.6-sol
  provider: openai-codex
  reasoning_effort: high
  max_concurrent_children: 10
```

### Model Routing (3-Tier) + Smart Scope Guard

| Task Type | Model | Guard |
|---|---|---|
| Complex/Judgement/Financial/Architecture | **Parent (Flash)** — deepseek-v4-flash | Verify: "Is this on-objective?" |
| Architecture Review / Debug Escalation | **Sol Medium** — GPT-5.6 via openai-codex (subagent) | Bounded context only; fallback to Luna |
| Easy/Mechanical (boilerplate, lint, tests) | **Parent (Flash)** — handle directly | No delegation needed |

Parent classifies every task before execution.

**Sol Medium role:** Hostile architecture reviewer (Phase 2R) + fresh-eyes debugger (L3). NEVER: main conversation, plan creation, financial decisions. Unavailable → fallback to Luna (openrouter).

**Smart Scope Rule:** If a task requires >3 layers of architectural reasoning → question if it's over-engineered. Simpler is better, as long as quality holds.

## UI Dashboard Plugin

When a task involves **creating a new dashboard or UI**, delegate to the `ui-dashboard-workflow` skill. This plugin handles the domain-specific workflow for dashboards while project-workflow retains ownership of task orchestration, agent delegation, and evidence QA.

### Phase Mapping

project-workflow owns gates and agent delegation. ui-dashboard-workflow owns domain-specific dashboard content.

```
project-workflow                         ui-dashboard-workflow v4.0.0
─────────────────                        ─────────────────────
Phase 0: Discovery
  └─ Interview Founder: what dashboard?  ──→ context passed
      who uses it? what decision?
                                            Phase A: Truth Intake
                                              └─ Bible + domain rules + FDs
                                              └─ PRODUCT_TRUTH_INVENTORY.md
                                            Phase B: Metric Design
                                              └─ KPIs, drivers, guardrails, targets
                                            Phase C: Bible-to-UI Gate (FD-104/107)
                                              └─ MANDATORY for full rebuilds
                                              └─ Every Bible § → UI (P0/P1/P2 gap table)
                                              └─ 3-question skip enforcement (FD-107)
                                              └─ Founder approves → proceed
                                            Phase D: User & Decision Mapping
                                              └─ USER_DECISION_MAP.md per role/page
                                            Phase E: Information Architecture
                                              └─ minimum pages + navigation discipline
                                            Phase F: Presentation Model
                                              └─ representation per info need
                                            Phase G: Page Blueprints + Text Wireframes
                                              └─ PAGE_BLUEPRINTS.md
                                            Phase H: Visual Direction + Reference
                                              └─ ADOPT/ADAPT/REJECT + UI_TOKENS
Phase 2R: Architecture Review Gate ──→ Founder reviews decision map + IA + blueprint
                                            Phase I: Founder Design Gate
                                              └─ packet: users/coverage/IA/wireframes/
                                                  reference/direction/tradeoffs
Phase 3: Plan
  └─ Task contracts for UI components   ──→ Component breakdown, owned_paths
Phase 4: Implement                        Phase J: Implementation
  └─ Delegate to Sol Medium sub-agents        └─ shadcn-ui (APIs) + frontend-ui-engineering
  └─ Locked tests for critical paths          └─ Card gate + borderless-by-default
                                            Phase K: Validation
                                              └─ calculations, states, data quality
                                            Phase L: Browser-First Refinement
                                              └─ implement → inspect → screenshot → refine (≥1 pass)
                                            Phase M: Visual Acceptance + Evidence
                                              └─ evidence/ui/<task-id>/ + VISUAL_QA.md
                                              └─ independent review via llm-council
                                            Phase N: Closeout
Phase 5: Evidence QA                      (feeds 10-point checklist + locked tests)
  └─ Locked tests pass
```

### Key: Who Owns What

| project-workflow owns | ui-dashboard-workflow v4.0.0 owns |
|---|---|
| Bible-First Gate enforcement | Truth intake + Bible→UI interpretation (mapping only, never meaning) |
| Agent delegation (Parent/Sol Medium) | User decision map + KPI/metric model |
| Task contracts and isolation | IA, presentation model, page blueprints, text wireframes |
| Locked acceptance tests | Visual direction, tokens, Card gate + borderless policy |
| Evidence QA checklist | Data quality + calculation validation |
| Phase gates and Founder approval | Browser-first refinement + screenshot evidence + VISUAL_QA |
| Regression budget | Component implementation details (routes to shadcn-ui/frontend-ui-engineering) |

### When to Use the Plugin

- **Creating a NEW dashboard or UI page** → route through plugin (Foundation Mode)
- **Major redesign of existing UI** → route through plugin (Foundation or Feature Mode)
- **Existing UI looks generic/card-heavy/bordered/outdated** → route through plugin (Remediation Mode: screenshot audit first)
- **Minor edits, bug fixes, adding components** → handle directly (Quick Mode), do NOT load plugin

### Plugin Contract

1. `ui-dashboard-workflow` loads Bible ONCE in Foundation phase — project-workflow does NOT re-read
2. Founder decisions from dashboard workflow are recorded as FDs — project-workflow tracks them
3. Task contracts for UI work follow standard task isolation (owned_paths, forbidden_paths, locked_tests)
4. Sol Medium sub-agents may implement UI components — Parent reviews architecture and financial impact
5. Evidence QA includes both backend (locked tests) and frontend (browser verification)

### When NOT to Use the Plugin

- Backend-only features (auth, broker, migration, data pipelines)
- Financial calculations or trading logic
- Non-UI infrastructure changes
- Minor edits to existing pages

---

## Related Skills

- `karpathy-guidelines` — mandatory coding behavior
- `ui-ux-pro-max` — UI/UX design
- `frontend-ui-engineering` — component architecture, a11y
- `plan` — task plans
- `test-driven-development` — TDD with locked-tests
- `grilling` + `domain-modeling` — requirements + domain
- `spike` — feasibility validation
- `architecture-diagram` — system design
- `governance-audit` — bible/code cross-reference
- `systematic-debugging` — root-cause debugging
- `github-pr-workflow` — PR lifecycle
- `project-state-sync` — session/phase closure
- `llm-council` — independent review gates (Bible/Plan/Milestone/Final, v1.1.1 — Milestone materiality-aligned)
- `ui-dashboard-workflow` — UI/dashboard creation plugin
- `gather-business-context` — domain context before analysis
- `design-kpis` — KPI framework and target design

## Reference Scripts (v3.3.0)

- `references/gate-check-template.sh` — Automated 6-gate enforcement script (adapt per project)
- `references/isolation-scan.sh` — Forbidden path violation scanner (adapt per task)

## Reference Files (v3.7.1)

- `references/milestone-evidence-log.md` — 🆕 per-milestone evidence instrumentation (review §5): fill one row at milestone closeout → drives evidence-based v3.8 decisions
- `references/workflow-cheat-sheet.md` — 🆕 one-page adoption cheat-sheet: mode selection, execution order, council gates, verification, escalation, delegation
<!-- 2026-08-02 03:06 UTC+7 -->
