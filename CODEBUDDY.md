# CODEBUDDY.md — Investment Intelligence Platform

> Auto-loaded by Codex CLI, Cursor, Windsurf, and compatible coding agents.

## Identity

- **Project:** Investment Intelligence Platform (IIP)
- **Stack:** Python + pandas + FastAPI + React + shadcn/ui
- **Repo:** `C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform`

## Session Start

1. Read `AGENTS.md` — authority, rules
2. Read `PROJECT_STATE.md` — current phase, blockers, next action
3. Read `SESSION_CLOSEOUT.md` — last session context
4. Verify state before working

## Workflow Modes

### 🔴 Critical (default for IIP)
Use for: architecture, financial logic, multi-file features, `src/auth/**`, `src/broker/**`, `src/ml/**`, `src/migration/**`, `src/calculation/**`, `src/database/schema/**`

```
Discovery → Spike → Architecture → Review → Plan → Implement → QA → Integrate → Release
```

### 🟢 Quick
Use for: typos, docs, CSS, single-file edits NOT in blacklist.
```
Inspect → Change → Smoke Test → Commit
```
Any smoke test fail → escalate to Critical.

## Key Rules

- **Financial logic → handle directly** (Cost Basis, P&L, Options, Capital) — never delegate to sub-agents
- **Locked tests** — write acceptance tests before delegating; subagent must not modify
- **Phase 2R Architecture Review** — MANDATORY before Phase 3 (Founder review or Fresh QA)
- **Max 2 regressions per task** — 3rd → escalate to Founder with A/B/C
- **Re-spec before escalate** — agent fail 2× → force task re-spec
- **No broker connectivity, execution, or portfolio allocation** (IIP is discovery only)
- **No AI-invented investment rules, thresholds, or formulas**

## Task Complexity Routing

| Task Type | Handle By |
|---|---|
| Complex, financial, architecture, judgement | Handle directly |
| Bulk, mechanical, repetitive, verifiable | Delegate to sub-agent |

Sub-agents never: change architecture, interpret Bible, handle financial logic, self-approve.

## Task Contract

```yaml
task_id: T12
branch: agent/T12-name
isolation: worktree
owned_paths: [src/...]
forbidden_paths: [src/database/**, src/broker/**]
locked_tests: [tests/locked/test_*.py]
```

## Escalation

```
L1: Sub-agent fail 2× → re-spec
L2: Re-spec → re-delegate
L3: Handle directly
L4: 👤 Founder — "Tried X,Y,Z. Options: A/B/C."
```

## Verification

1. Locked tests pass
2. Targeted suite passes
3. No regression
4. Diff clean
5. Git clean
6. Smoke test passes

## Close

Update `PROJECT_STATE.md` + write `SESSION_CLOSEOUT.md`.
