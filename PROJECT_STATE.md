# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.
> Build metrics (test counts, commit counts) are tracked HERE — see §Build Metrics below.

## Current state

- Product phase: `IIP-Phase 10` complete (Institutional Intelligence V1). `IIP-Phase 10.5` complete (Real 13F data via FD #42 amendment). All authorized phases (0–10.5) delivered. **Phase 11 (Deep Research Handoff / CIW): Design Path OPENED + Pilot Execution AUTHORIZED (FD-CIW-010/011, 3 Aug 2026)** for the MSFT first slice per `docs/CIW-FIRST-SLICE-DESIGN.md` v0.3 (Phase 2R PASSED — 3 rounds). Full implementation (Cron/Obsidian sync/expanded tree/schema) remains deferred.
- Workflow gate: `WF-Phase -1` — Bible Council COMPLETE (CIW proposal): verdict FOUNDER DECISION REQUIRED, 10 Required Changes accepted (Option A), FD-CIW-001..007 approved (all Option A), amendment map drafted. **CIW Spec v0.2 BATCH APPROVED (FD-CIW-008, 2 Aug 2026)** — 7 specs in `project-definition/company-intelligence-workbench/` + amendment map APPROVED + 11 targeted amendments issued (documentation-only; Phase 11 implementation still not opened). **Pilot company selected: MSFT (FD-CIW-009). Pilot IN PROGRESS (3 Aug 2026):** design v0.3 approved (2R PASSED), CRR-2026-0001 approved (Research Gate), Source Map gate passed (real SEC EDGAR verification) — bounded research (Modules A–M, initial) next.
- Latest FDs: `FD-CIW-010` (Design Path OPENED, docs-only, 3 Aug 2026) + `FD-CIW-011` (Pilot Execution Authorization — MSFT first slice, supersedes FD #44 for pilot scope only, 3 Aug 2026). Chain: FD-CIW-001..011 (55 total).
- Tests: **262/262 all passing** — verified 2 August 2026.

## Build Metrics (single source of truth — v3.3.0)

| Metric | Value | Last verified |
|--------|-------|---------------|
| Python tests | 262/262 passing | 2026-08-02 |
| Frontend build | ✅ passes (`npm run build` exit 0) | 2026-08-02 |
| Frontend lint | 0 errors, 4 warnings (shadcn/ui fast-refresh advisories) | 2026-08-02 |
| Commits | 82 on `main` (synced with origin after push) | 2026-08-03 |
| FDs approved | #1–44 + FD-CIW-001..011 (55) | 2026-08-03 |
| closeout_status | **completed** (CIW design path + pilot authorization session) | 2026-08-03 |

> Stale mirrors to update together: `SESSION_CLOSEOUT.md`, `AGENTS.md` checkpoints, `README.md`, `project-definition/README.md`, vault `fd-register.md`. Audit/council reports live in `evidence/`.

## Open constraints

- No active blockers. AM/CS API surfaces serve labeled synthetic demo data — real pipeline wiring deferred.
- Deferred items: DR-004 (Legacy Knowledge Salvage), Phase 11 Deep Research Handoff / CIW (concept approved in principle only — FD-CIW-001; implementation/automation/schemas/pilot require a separate named FD superseding FD #44), CIW pilot company selection (FD-CIW-007 — shortlist after specs), AM/CS API-backed workflows, automated challenge/earnings/trap detection, cross-module institutional signal integration, final stack declaration, database/persistence expansion. Templates TPL-* remain deferred.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- No schema or migration without explicit authorization.

## Next allowed action

CIW pilot first slice IN PROGRESS: FD-CIW-010 (design path) + FD-CIW-011 (pilot execution authorization) approved; design v0.3 passed Phase 2R (3 rounds); CRR-2026-0001 approved at Research Gate; Source Map gate passed (real SEC EDGAR). **Next action: bounded initial research (Modules A–M, initial depth) → `research-draft.md` → Independent Challenge (Sol Medium) → Founder Review → structured Research Result (Founder publication on exact version/hash).** No further authorization needed to begin research; every Founder gate remains binding.

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`
- `evidence/` — audit reports + council decisions

## Lifecycle sync

- Last session: 2026-08-03 CIW design path + pilot authorization (morning)
- Outcome: FD-CIW-010 (design path) → design v0.3 (Phase 2R PASSED, 3 rounds, evidence persisted) → FD-CIW-011 (pilot execution authorization) → CRR-2026-0001 approved (Research Gate) → Source Map gate passed (real SEC EDGAR). Side items: CODEBUDDY.md/ChatGPT/ declared, origin pushed (synced), *.env gitignore gap closed.
- Evidence: `evidence/PHASE-2R-CIW-FIRST-SLICE-2026-08-03.md`, `docs/CIW-FIRST-SLICE-DESIGN.md` v0.3, `docs/ciw-pilot-msft/CRR-2026-0001-request.md`, `docs/ciw-pilot-msft/source-map.md`
- Blockers: none
- Next phase: bounded initial research (Modules A–M) → Independent Challenge → Founder Review → structured Research Result
- Last verified: 2026-08-03

## Session

| Field | Value |
|-------|-------|
| closeout_status | completed |
| fd_count | 44 + 11 CIW (55 total) |
| audit_verdict | FOUNDER DECISION REQUIRED → accepted (CIW Bible Council) → spec v0.2 batch approved (FD-CIW-008) → pilot company selected (FD-CIW-009, MSFT) → design v0.3 Phase 2R PASSED → pilot execution authorized (FD-CIW-011) → Research Gate passed (CRR-2026-0001) |

<!-- 2026-08-03 01:50 UTC+7 -->
