# AUDIT_MANIFEST — Investment Intelligence Platform

> Pre-Launch Close Beta Audit · 2026-08-03 · profile: iip
> Adapter: `qa/prelaunch-audit/IIP-ADAPTER.md` (project facts)
> Core skill: `prelaunch-close-beta-audit` v2.0.25

## Environment (Phase 0 — PASS)

```yaml
audit_profile: strict_full_e2e
environment: isolated_staging
app_url: http://localhost:5173
api_base: http://127.0.0.1:8000
delegation_model: gpt-5.6-sol (openai-codex) — verified
production_access: none
broker/execution/allocation: none (forbidden by project constitution)
database: none (stateless API — fixtures in-memory + pipeline JSON)
auth/login: none in V0 (display platform)
reset_command: N/A (restart backend = reset)
seed_command: N/A (no DB)
```

## Critical workflows (strict full-E2E register)

| WF-ID | Name | Route | Browser | API checkpoint | Persistence | Refresh | Re-login | Oracle |
|---|---|---|---|---|---|---|---|---|
| WF-01 | Dashboard loads | `/` | renders KPI cards + SYNTHETIC banner | `/api/dashboard/summary` 200 | in-memory (N/A DB) | required | N/A (no auth) | fixture cross-check |
| WF-02 | AM Queue loads | `/am-queue` | renders 5 theme rows + SYNTHETIC banner | `/api/am-queue` 200 | N/A | required | N/A | mock vs `synthetic_demo` label |
| WF-03 | AM Theme detail | `/am-theme/theme-ai-infra` | renders theme detail | `/api/am-theme/theme-ai-infra` 200 | N/A | required | N/A | ID from list endpoint |
| WF-04 | CS Radar loads | `/cs-radar` | renders radar table + SYNTHETIC banner | `/api/cs-radar` 200 | N/A | required | N/A | `synthetic_demo` label |
| WF-05 | FO Queue loads | `/fundamental` | renders 8 companies + SYNTHETIC banner | `/api/fo-queue` 200 | N/A | required | N/A | pipeline fixture cross-check |
| WF-06 | FO Detail | `/fundamental/msft` (id from list) | renders tabs (Moat/Earnings/Valuation) | `/api/fo-package/{id}` 200 | N/A | required | N/A | pipeline fixture cross-check |
| WF-07 | Cheap & Quality | `/cheap-quality` | renders watchlist | `/api/fo-cheap-quality` 200 | N/A | required | N/A | pipeline fixture cross-check |
| WF-08 | Weak Signal Inbox | `/weak-signals` | renders disabled actions + SYNTHETIC banner | N/A (static) | N/A | required | N/A | honest disabled state |
| WF-09 | 404 page | `/made-up-path` | renders NotFound + back link | N/A | N/A | N/A | N/A | route table |
| WF-10 | All-pages JS sweep | all routes | browser_console after each: 0 JS errors | N/A | N/A | N/A | N/A | resilience sweep |

**Provenance contract (FD #44):** every data surface MUST display an explicit
SYNTHETIC/DEMO label. Absence of real pipeline data on API surfaces is BY DESIGN
(real wiring deferred) — not a defect. Absence of the provenance label IS a defect.

## Roles

- `viewer` — single role; no auth, no login, no permissions. RE-LOGIN: N/A for all workflows (no auth flow exists; manifest-declared N/A).

## Forbidden actions (audit must NOT do)

- No access to production URLs, live broker/execution/allocation endpoints, or real credentials.
- No schema/migration, no dependency install, no repo-wide refactors.
- No silent defect fixes during discovery (record first; fix after verdict).
- No yfinance re-fetch during audit (cache as-of 2026-07-31 is the oracle — avoid network churn).

## Mutation coverage

N/A — display-only platform (MASTER.md: "Buttons: none in V0"). The only
actionable controls (Weak Signal Propose/Dismiss) are intentionally disabled —
verifying they are DISABLED is the coverage, not enabling them.

## Evidence root

```
qa/prelaunch-audit/evidence/
  screenshots/  api/  console/  oracle/
```

## Known open items (pre-audit, must be re-verified)

1. FO endpoints lack item-level `data_source` field (provenance only in pipeline meta) — candidate Minor finding.
2. Sidebar renders light not dark #0f1117 (missing `--color-sidebar` theme token) — candidate Minor design finding (verified by computed style earlier today).
3. Vite proxy 8001→8000 FIXED this session (e5f4134) — verify no regression.

<!-- 2026-08-03 21:25 UTC+7 -->
