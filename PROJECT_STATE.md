# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.
> Build metrics (test counts, commit counts) are tracked HERE — see §Build Metrics below.

## Current state

- Product phase: `IIP-Phase 10` complete (Institutional Intelligence V1). `IIP-Phase 10.5` complete (Real 13F data via FD #42 amendment). All authorized phases (0–10.5) delivered. **Phase 11 (Deep Research Handoff / CIW) NOT authorized — deferred per FD #44 + FD-CIW-001 (2 Aug 2026).**
- Workflow gate: `WF-Phase -1` — Bible Council COMPLETE (CIW proposal): verdict FOUNDER DECISION REQUIRED, 10 Required Changes accepted (Option A), FD-CIW-001..007 approved (all Option A), amendment map drafted. **CIW Spec v0.2 BATCH APPROVED (FD-CIW-008, 2 Aug 2026)** — 7 specs in `project-definition/company-intelligence-workbench/` (documentation-only; Phase 11 implementation still not opened; amendment map still DRAFT).
- Latest FDs: `FD-CIW-001..008` — CIW governance decisions (2 August 2026; 001–007 all Option A, 008 spec batch approval).
- Tests: **262/262 all passing** — verified 2 August 2026.

## Build Metrics (single source of truth — v3.3.0)

| Metric | Value | Last verified |
|--------|-------|---------------|
| Python tests | 262/262 passing | 2026-08-02 |
| Frontend build | ✅ passes (`npm run build` exit 0) | 2026-08-02 |
| Frontend lint | 0 errors, 4 warnings (shadcn/ui fast-refresh advisories) | 2026-08-02 |
| Commits | 70 on `main` (ahead of origin by 17) | 2026-08-02 |
| FDs approved | #1–44 + FD-CIW-001..008 | 2026-08-02 |
| closeout_status | **completed** (CIW spec v0.2 + amendments session) | 2026-08-02 |

> Stale mirrors to update together: `SESSION_CLOSEOUT.md`, `AGENTS.md` checkpoints, `README.md`, `project-definition/README.md`, vault `fd-register.md`. Audit/council reports live in `evidence/`.

## Open constraints

- No active blockers. AM/CS API surfaces serve labeled synthetic demo data — real pipeline wiring deferred.
- Deferred items: DR-004 (Legacy Knowledge Salvage), Phase 11 Deep Research Handoff / CIW (concept approved in principle only — FD-CIW-001; implementation/automation/schemas/pilot require a separate named FD superseding FD #44), CIW pilot company selection (FD-CIW-007 — shortlist after specs), AM/CS API-backed workflows, automated challenge/earnings/trap detection, cross-module institutional signal integration, final stack declaration, database/persistence expansion. Templates TPL-* remain deferred.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- No schema or migration without explicit authorization.

## Next allowed action

CIW governance foundation complete (council verdict + amendment map + FD-CIW-001..008 + 7 approved specs). Next step requires Founder decision — options: (a) approve amendment map + issue targeted amendments per Constitution §21 (DNA-019/020, Operating Model §5.7, ROADMAP Phase 11 row, FDs register, CANDIDATE-AND-QUEUE status mapping, EVIDENCE/SECURITY source gate, DEFERRED-DECISIONS, OPEN-QUESTIONS, GLOSSARY, INDEX), (b) pilot company shortlist (FD-CIW-007 — after specs, which are now approved), or (c) Founder-directed task. Phase 11 implementation still gated behind a separate named FD superseding FD #44.

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`
- `evidence/` — audit reports + council decisions

## Lifecycle sync

- Last session: 2026-08-02 CIW Spec v0.2 drafting + batch approval + targeted amendments (evening)
- Outcome: 7 CIW specs approved (FD-CIW-008) → amendment map approved → 11 targeted amendments issued (Constitution §21) → CIW governance chain complete; Phase 11 implementation still deferred
- Evidence: `docs/CIW-INTEGRATION-AMENDMENT-MAP.md`, `project-definition/company-intelligence-workbench/`, `evidence/COUNCIL_DECISION-bible-2026-08-02.md`
- Blockers: none
- Next phase: Founder decision — pilot shortlist (FD-CIW-007) / Phase 11 design / other
- Last verified: 2026-08-02

## Session

| Field | Value |
|-------|-------|
| closeout_status | completed |
| fd_count | 44 + 8 CIW (52 total) |
| audit_verdict | FOUNDER DECISION REQUIRED → accepted (CIW Bible Council) → spec v0.2 batch approved (FD-CIW-008) |

<!-- 2026-08-02 23:50 UTC+7 -->
