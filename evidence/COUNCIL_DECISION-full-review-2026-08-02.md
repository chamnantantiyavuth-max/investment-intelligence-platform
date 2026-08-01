# COUNCIL DECISION

## Gate
Full Project Review

## Verdict
RETEST

## Material Findings
1. Frontend build is blocked by 31 TypeScript errors (missing `@tanstack/react-query` dependency; type-only import errors; unused imports; `unknown` values rendered as React nodes).
2. AM/CS/dashboard/weak-signal UI and API surfaces present unlabeled synthetic data (`backend/api/am_routes.py`, `backend/api/cs_routes.py`, `AMQueuePage.tsx`, `AMThemeCardPage.tsx`, `CSRadarPage.tsx`, `WeakSignalInboxPage.tsx`, `DashboardPage.tsx`) — truth-safety violation vs Constitution §§8/10/11/23.4 and DNA-002/DNA-016.
3. Mandatory evidence, council artifacts, and automated gate scripts are absent — no `evidence/`, no `scripts/gate-check.sh`, no `scripts/isolation-scan.sh`, no `COUNCIL_DECISION-*.md` persisted before this run.
4. Project-state documents report contradictory test counts (251 vs 226 vs 91) and `closeout_status: pending` after a declared closeout.
5. Alpha Momentum core pipeline (S1–S6, `alpha-momentum-v0/pipeline.py`) lacks direct automated acceptance coverage — the 10 Phase-3 ACs are not independently executable.
6. Human-review UI is visibly incomplete (`AMThemeCardPage.tsx:134–140` "pending implementation"; Weak Signal buttons have no handlers; no mutation/persistence endpoints).
7. New independent findings: missing React Query `QueryClientProvider` (main.tsx), FO frontend/backend `conviction` type mismatch (fo.ts:19 vs responses.py:79), AM detail route ignores `:id` (AMThemeCardPage), fabricated HTTP 200 "Unknown" records for invalid AM IDs (am_routes.py:46–56), hardcoded Python 3.14 interpreter path (run_real.py:11), and silent SEC partial-failure handling (fetcher.py:280–293).

## Required Changes
1. Repair frontend build and runtime provider/type contracts (`npm run build` exit 0).
2. Block or label all synthetic AM/CS/dashboard/weak-signal data surfaces.
3. Add direct AM core pipeline tests mapped to AC-1 through AC-10 (no locked-test modification).
4. Correct API not-found semantics (404 for invalid AM IDs) and AM detail routing.
5. Synchronize project-state and index documents (PROJECT_STATE, SESSION_CLOSEOUT, AGENTS, README, project-definition/README, vault fd-register).
6. Resolve ADR-001 status (currently Draft while frontend shipped).
7. Restore or explicitly gate missing council/evidence automation.
8. Re-run backend, frontend, and browser verification independently.

## Evidence Gaps
- No `evidence/COUNCIL_DECISION-*.md` artifacts existed before this run (this file is the first).
- No `scripts/gate-check.sh` / `scripts/isolation-scan.sh`.
- No browser evidence (build fails; no browser smoke test performed).
- No SEC EDGAR live verification.
- No persistence/history workflow evidence.
- No direct automated tests for the approved Alpha Momentum S1–S6 pipeline.
- No verified production build artifact (frontend/dist/ is stale, Jul 25 04:00).

## Founder Decisions Required
1. React/FastAPI approval status — approved implementation direction or still provisional?
2. Phase 11 authorization — authorize or defer Deep Research Handoff?
3. Current-scope status of AM/CS API-backed workflows — implement now or explicitly demo-only?
4. Acceptance of `CODEBUDDY.md` as a governance entrypoint (untracked file)?
5. Whether real-data integrations (yfinance, SEC EDGAR) remain development-only.

## Minority Warning
The Python suite is green (251 passed), but treating that as evidence of application readiness would be unsafe. Passing tests cover substantial pipeline logic but do not cover frontend compilation, browser workflows, API provenance, persistence, or the full Alpha Momentum acceptance contract.

## Scope Expansion Check
**Rejected:** Phase 11 implementation, broad database adoption, broad cross-module integration, final stack declaration, and UI redesign are outside the smallest sufficient recovery. They remain deferred pending Founder authorization.

---
*Council run: 2026-08-02 · Reviewer: openai/gpt-5.6-luna (OpenRouter) — Sol Medium unavailable (HTTP 400: model not supported with ChatGPT-account Codex auth). Full report: `evidence/FULL_PROJECT_REVIEW-2026-08-02.md`.*
<!-- 2026-08-02 04:35 UTC+7 -->
