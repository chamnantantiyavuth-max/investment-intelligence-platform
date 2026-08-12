---
name: project-workflow
description: Canonical ENGINEERING / SYSTEM CHANGE-CONTROL workflow for governed projects — Bible/authority discipline, SMART-SCOPE, root-cause analysis, locked acceptance tests, Evidence QA, isolation scanning, rollback, and material engineering review gates. Scope: code, architecture, schema, API, UI implementation, data pipelines, deterministic financial calculation implementation, Hermes config/profile/SOUL/AGENTS/skills/memory-system changes, Kanban integration, Cron/automation, release/deployment. NOT loaded for investment research, Radar, filings analysis, Gemini Deep Research, evidence research, CRO, research audit, Thai editorial, or IPM investment reasoning.
version: 3.8.0-candidate
author: Chamnan + Hermes Agent (v3.8 candidate — Stage 2D, not promoted)
supersedes: 3.7.1 (candidate only — v3.7.1 remains production until Stage 4 pilot passes)
---

# Project Workflow v3.8 — Engineering Change-Control Workflow (CANDIDATE)

> **v3.8 scope change (Stage 2D, FD-98):** v3.7.1 was the universal IIP operating workflow. v3.8 re-scopes it to **software / system / harness engineering change control only**. Investment-research workflows (Radar, Deep Research, CRO, research audit, editorial, IPM reasoning) do NOT auto-load this skill — they use their IIP research skills (iip-evidence, iip-deep-research, iip-publication, iip-discovery-audit, capital-kanban) and their own challenge chain (Cross-Exam → CRO → research audit → Facts Locked → Founder).

## Scope

### USE FOR (mandatory engineering triggers)
- application code changes
- architecture / subsystem design
- schema / database / migration
- API design or changes
- UI/UX implementation (with ui-dashboard-workflow plugin)
- data pipeline implementation
- deterministic financial calculation implementation
- Hermes config / profile / SOUL / AGENTS / skill / memory-system changes
- Hermes Harness changes
- Kanban integration / adapter
- Cron / automation
- deployment / release

### DO NOT AUTO-LOAD FOR
- Radar scanning
- 10-K/10-Q reading / filings analysis
- equity/commodity fundamental research
- Gemini Deep Research
- evidence admission (as research)
- CRO opposing thesis
- research audit
- Thai editorial
- IPM weekly investment reasoning

**If a research run discovers a software change is needed:** create a separate `[ENGINEERING]` / `[HARNESS]` task and apply this workflow there. Do not contaminate the research first-pass context with engineering governance.

## Core Principles (Non-Negotiable)

1. **Bible / Authoritative-Source Discipline** — the project's approved authority hierarchy (AGENTS.md → Constitution/Bible → FDs → specs → plans) is the source of domain truth. Never deduce from memory/module names. New material requirements → recorded Founder Decision.
2. **SMART-SCOPE** — "Is this directly addressing the objective, or am I creating work?" Simplest correct solution. No gold-plating.
3. **Root-Cause-First Debugging** — trace to the data model / origin before changing outputs.
4. **Locked Acceptance Tests** — acceptance expectations are immutable without Bible quote / FD; spec-as-code.
5. **Evidence QA** — every completion claim carries verification evidence (TEST_VERIFIED / STATIC_OBSERVATION / EXTERNAL_NOT_TESTED / INFERENCE).
6. **End-to-End Verification** — feature done = user completes the workflow, not "API exists".
7. **Isolation** — task isolation via worktree/branch; forbidden-path scanning per project policy.
8. **Security / Secret Discipline** — no secrets in repo/logs; .env ignored; untrusted content doctrine.
9. **Rollback** — every material change has a tested rollback point.
10. **Material Independent Engineering Review** — material engineering decisions pass an independent review gate (below); NOT the investment-research challenge chain.

## Execution Modes

### CRITICAL MODE (default for engineering)
For: architecture, schema, API, multi-file features, new subsystems, config/profile/harness changes, deterministic financial calculation implementation, anything touching material/risky paths (derived from THIS project's AGENTS + task contract + repo architecture — not a universal blacklist).

```
Discovery → Architecture → Review Gate → Plan → Isolated Implementation (locked tests) → Evidence QA → Integration → Release
```

### QUICK MODE (lightweight)
For: typo fixes, docs, CSS, log statements, single-file non-material edits NOT on the project's material/risky paths.

```
Inspect → Change → Smoke Test → Commit
```

**Mode-default conflict rule:** within engineering scope, when in doubt about materiality → Critical. Outside engineering scope, these modes do not apply.

## Engineering Review Gates

Material engineering decisions (architecture, schema, permission/security, irreversible changes, broad regression) pass ONE independent review gate: the **Engineering Council** — implemented via the currently approved independent-review routing (see `llm-council` skill; model/provider routing lives in runtime config, not here). The Engineering Council is SEPARATE from the investment-research challenge chain (Cross-Exam / CRO / research audit). Do not stack both on one artifact.

- Mandatory: architecture review for material changes (hostile reviewer via approved independent routing)
- Mandatory: final release review before Founder acceptance
- Conditional: plan review for Critical Mode + forbidden paths or financial calculation
- Prohibited: Quick Mode, typo fixes, cosmetic changes, routine CRUD, every commit

**Council output contract:** verdict / material findings (concrete + evidence-linked) / required changes (smallest sufficient) / evidence gaps / Founder decisions required / minority warning / scope-expansion check. Artifact persisted to project evidence path before Founder presentation.

## Task State

**Hermes Kanban owns durable task state for organizational engineering work.** This workflow does NOT maintain a parallel per-task state machine. `PROJECT_STATE.md` remains for project-level phase, major blockers, next approved direction. Worker-level continuity lives in Kanban task result/comments/artifacts.

- Project-level closeout (PROJECT_STATE + session closeout) applies to: material Founder sessions, architecture approvals, milestone completions, major recovery, releases, harness cutovers. NOT every worker task.

## Verification

### Locked Acceptance Tests
- Immutable, contractual, spec-as-code. Never modify expected values without Bible quote / FD.

### Evidence QA Checklist (engineering)
1. Locked tests pass (Parent re-verifies independently — never trust subagent self-report)
2. Canonical tests pass (acceptance examples → automated tests)
3. Targeted suite passes; no regression in critical paths
4. Negative-path tests exist
5. Diff review (no unintended changes); git status clean
6. Deployment smoke (schema: alembic upgrade + check; API responds; UI: browser verification)
7. Gate check + isolation scan pass (project-adapted scripts)
8. Rollback point exists and is tested

### Test-Strength Checks (high-value logic only)
- Mutation Testing Lite (5–8 single mutations on financial/operational logic; suite must catch)
- Property/Invariant Testing (generated-input invariants on allocation/state/atomicity)

### Preserved v3.7.1 machinery (P5 — Capability Preservation Matrix)
- Session Preflight: `references/session-preflight.sh` (template) — run before meaningful engineering work
- Project Truth Map: `references/project-truth-map-template.md` — authoritative-source table per project
- Mutation Testing Lite: `references/mutation-testing-lite.md`
- Property/Invariant Testing: `references/property-invariant-testing.md`
- Milestone Evidence Log: `references/milestone-evidence-log.md`
- Gate check + isolation scan: `references/gate-check-template.sh` + `references/isolation-scan.sh`
- Security/secret discipline + rollback: §Core Principles #8 + §Rollback
- Full capability classification: `V38-CAPABILITY-PRESERVATION-MATRIX.md` (43 items: 30 KEEP, 8 RE-SCOPE, 1 MOVE, 4 RETIRE — M2 corrected)

## Delegation

- **Parent** (primary engineering model, per runtime config) handles architecture, planning, financial calculation implementation, and easy/mechanical work.
- **Independent review** (Phase 2R hostile review, engineering council, L3 fresh-eyes debug) → currently approved independent-review routing (runtime config / FDs). Model/provider names are NOT hard-coded here.
- Delegation stays shallow (max spawn depth 1); Kanban is the organizational work layer; `delegate_task` is a local helper call.

## Related Skills (non-overlapping engineering companions)

- `llm-council` — engineering review gates
- `ui-dashboard-workflow` — UI/dashboard design workflow plugin
- `plan` — task plans
- `test-driven-development` — TDD with locked tests
- `systematic-debugging` — root-cause debugging
- `spike` — feasibility validation
- `karpathy-guidelines` — coding behavior
- `github-pr-workflow` — PR lifecycle
- `governance-audit` — engineering/domain cross-reference audits (delegated per audit routing)
- `iip-hermes-workforce` — harness/profile/skill/memory administration (Stage 2E — KEEP NAME + EXTEND, P7)

**Not auto-loaded from engineering:** iip-evidence, fundamental-company-research, iip-editorial-publication, iip-discovery-audit, capital-kanban, simulated-portfolio-office (research-side skills — loaded by research tasks).

## Rollback

- Before destructive work: config export, DB backup, skill snapshot, git checkpoint/rollback tag.
- Rollback triggers: routing regression, tool loss, portfolio leak, memory contamination, board deletion before verification, UI task-truth mismatch, DB corruption, dispatcher storm, analytical/governance semantics changed.
- Restore harness without rewriting research history.

## Migration Status

- **v3.8 = CANDIDATE (Stage 2D).** v3.7.1 remains production (unchanged, backed up).
- Promotion path: Stage 4 bounded engineering pilot on v3.8 → Founder gate → promote.
- Rollback path: revert to v3.7.1 (still installed) without affecting research workflows.
