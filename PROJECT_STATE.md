# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.
> Build metrics (test counts, commit counts) are tracked HERE — see §Build Metrics below.

## Current state

- Product phase: `IIP-Phase 10` complete (Institutional Intelligence V1). `IIP-Phase 10.5` complete (Real 13F data via FD #42 amendment). All authorized phases (0–10.5) delivered. **Phase 11 (Deep Research Handoff) NOT authorized — deferred per FD #44.**
- Workflow gate: `WF-Phase 2R` complete; all Critical Mode phases passed.
- Latest FD: `FD #44` — Full Project Review Recovery Approval (RETEST verdict; 2 August 2026). Council verdict RETEST, reviewer `openai/gpt-5.6-luna` (OpenRouter fallback — Sol Medium unavailable).
- Tests: **262/262 all passing** (251 pre-recovery + 11 new direct AM core pipeline AC-1..AC-10 tests) — verified 2 August 2026.

## Build Metrics (single source of truth — v3.3.0)

| Metric | Value | Last verified |
|--------|-------|---------------|
| Python tests | 262/262 passing | 2026-08-02 |
| Frontend build | ✅ passes (`npm run build` exit 0) | 2026-08-02 |
| Frontend lint | 0 errors, 4 warnings (shadcn/ui fast-refresh advisories) | 2026-08-02 |
| Commits | 68 on `main` (ahead of origin by 13) | 2026-08-02 |
| FDs approved | #1–44 | 2026-08-02 |
| closeout_status | **completed** (recovery session) | 2026-08-02 |

> Stale mirrors to update together: `SESSION_CLOSEOUT.md`, `AGENTS.md` checkpoints, `README.md`, `project-definition/README.md`, vault `fd-register.md`. Audit reports live in `evidence/`.

## Open constraints

- No active blockers. Frontend build restored (recovery task, FD #44). AM/CS API surfaces serve labeled synthetic demo data — real pipeline wiring deferred.
- Deferred items: DR-004 (Legacy Knowledge Salvage), Phase 11 Deep Research Handoff, AM/CS API-backed workflows, automated challenge/earnings/trap detection, cross-module institutional signal integration, final stack declaration, database/persistence expansion. Templates TPL-* remain deferred.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- No schema or migration without explicit authorization.

## Next allowed action

Recovery task (FD #44) complete: frontend build restored, mock surfaces labeled, AM core tests added, state docs synced. Next phase requires Founder decision — no Phase 11 authorization exists. Options: define Phase 11, wire AM/CS APIs to real pipelines, cross-module integration, frontend polish, or Founder-directed task.

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`
- `evidence/` — audit reports + council decisions (created 2026-08-02)

## Lifecycle sync

- Last session: 2026-08-02 IIP full project review + recovery
- Outcome: audit RETEST → recovery approved (FD #44) → frontend build fixed, synthetic surfaces labeled, AM core tests added (262/262), state synced
- Evidence: `evidence/FULL_PROJECT_REVIEW-2026-08-02.md`, `evidence/COUNCIL_DECISION-full-review-2026-08-02.md`
- Blockers: none
- Next phase: Founder decision required
- Last verified: 2026-08-02

## Session

| Field | Value |
|-------|-------|
| closeout_status | completed |
| fd_count | 44 |
| audit_verdict | RETEST (recovery approved, FD #44) |

<!-- 2026-08-02 05:10 UTC+7 -->
