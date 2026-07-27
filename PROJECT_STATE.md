# Project State — Investment Intelligence Platform

> Compact bootstrap state. Source of truth remains the approved project governance documents.

## Current state

- Product phase: `IIP-Phase 9` implementation evidence verified; phase-close remains partial pending canonical review/reconciliation. `IIP-Phase 10` synthetic implementation is verified and authorized; phase-close is not claimed. A real-data extension labeled `Phase 10.5` is blocked/conditional.
- Workflow gate: `WF-Phase 2R` complete; implementation must follow the approved workflow gates.
- Latest documented project FD: `FD #42` — Institutional Intelligence V1 authorization.
- Vault FD register: `09-Agent/project-notes/investment-intelligence-platform/fd-register.md`.

## Open constraints

- Active governance blocker: commit `9dd5b77` adds real SEC EDGAR/13F fetching and CUSIP mapping, while FD #42 states synthetic/mock 13F first and real 13F in V1.5. No FD #43 authorization is recorded.
- Verification blocker: combined FO + II pytest invocation fails from module/import collision (23 failed, 57 passed); isolated locked suites pass (FO 26/26, II 54/54).
- Deferred items include DR-004 (Legacy Knowledge Salvage), selected rule implementation, automated challenge/earnings/trap detection, and Deep Research moved to a later phase.
- No broker connectivity, execution, or portfolio allocation.
- No AI-invented investment rules, thresholds, weights, formulas, lookbacks, or fallback behavior.
- No Legacy/quarantine access without separate named authorization.
- Deferred templates remain deferred.

## Next allowed action

Resolve the Phase 10.5 authorization boundary against FD #42 before advancing or closing the institutional-intelligence phase.

## Bootstrap sources

- `AGENTS.md`
- `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`
- `02-PROJECT-CONSTITUTION.md`
- `operational/FOUNDERS-DECISIONS.md`
- `PROJECT_INDEX.md`

## Lifecycle sync

- Last session: 2026-07-27 scheduled IIP review
- Outcome: blocked
- Evidence: `9dd5b77`; `operational/FOUNDERS-DECISIONS.md` FD #42; `python -m pytest institutional-intelligence-v0/test_locked -q` (54 passed); `python -m pytest fundamental-opportunity-v0/test_locked -q` (26 passed); combined run (57 passed, 23 failed); yfinance snapshot as of 2026-07-24.
- Blockers: Phase 10.5 authorization boundary; combined-suite import collision.
- Next allowed action: resolve Phase 10.5 authorization boundary before phase advancement/closure.
- Phase gate: Phase 9 partial; Phase 10 authorized with synthetic path verified; Phase 10.5 blocked/conditional.
- Phase evidence: `71d079f`, `330c572`, `9dd5b77`, and the isolated test commands above.
- Next phase: Founder decision required for the real 13F extension.
- Last verified: 2026-07-27

## Freshness

Last compact-state update: 2026-07-27. Gate 0 must still run as a read-only fresh-eyes audit; this file does not replace that audit.
