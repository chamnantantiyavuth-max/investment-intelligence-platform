# IIP Project Adapter — prelaunch-close-beta-audit

```yaml
adapter_id: iip-prelaunch-2026-08-03
project_name: Investment Intelligence Platform
project_root: C:\Users\Admin\Desktop\Antigravity\investment-intelligence-platform
core_skill: prelaunch-close-beta-audit
core_version: 2.0.25
manifest_path: qa/prelaunch-audit/AUDIT_MANIFEST.md
reference_files: []
```

## Project facts (verified 2026-08-03 evening against live files)

```yaml
project_type: web_app
audit_profile: strict_full_e2e
app_url: http://localhost:5173
api_base: http://127.0.0.1:8000   # backend uvicorn; vite proxies /api -> localhost:8000
environment: isolated_staging     # localhost only; no production reachable
reset_command: N/A                # stateless API — fixtures in-memory per process; restart = reset
seed_command: N/A                 # no DB; data = Python fixtures + alpha-momentum-v0/output/pipeline_result.json
roles: [viewer]                   # no auth/login in V0 — read-only display platform
critical_workflows: []            # see AUDIT_MANIFEST.md workflow register
forbidden_actions: []
upload_fixtures: []
oracle_commands:
  - "python3 alpha-momentum-v0/run_real.py --summary"  # pipeline source of truth (cache + result json)
  - "python3 -c \"json.load(open('alpha-momentum-v0/output/pipeline_result.json'))\""  # oracle read
external_dependencies:
  - yfinance (cached EOD, as-of 2026-07-31; do NOT re-fetch during audit — cache is the oracle)
```

## Critical IIP facts (from project docs, verified)

- **Display-only platform:** MASTER.md "Buttons: none in V0 — this is a display platform, not interactive." All surfaces are read-only. Weak Signal actions (Propose Hypothesis / Dismiss) are intentionally disabled.
- **Provenance doctrine (FD #44):** every surface MUST carry explicit SYNTHETIC/DEMO label. AM/CS/dashboard = `synthetic_demo` mock API. FO = real pipeline on synthetic fixtures. Real-pipeline-to-API wiring is DEFERRED and NOT authorized — absence of real data is not a defect.
- **No DB, no auth, no broker/execution/allocation.** Stateless FastAPI + in-memory fixtures + pipeline JSON.
- **Known open items (not release blockers, but must be reported):** FO endpoints lack item-level `data_source` field (provenance only in pipeline meta). Sidebar renders light not dark #0f1117 (missing `--color-sidebar` theme token — design bug, UI-layer).

## Browser lane (Parent)

Routes (from frontend/src/App.tsx):
- `/` Strategy Control Center (dashboard)
- `/alpha-momentum` → verify actual route from App.tsx nav (404 observed on guessed path — use nav clicks)
- `/close-system`, `/fundamental`, `/cheap-quality`, `/weak-signals` — resolve exact paths from App.tsx before testing
- 404 page exists (guessed-path navigation)

## API contract (live OpenAPI, 8 endpoints — all GET)

```
GET /api/health
GET /api/dashboard/summary
GET /api/am-queue
GET /api/am-theme/{theme_id}
GET /api/cs-radar
GET /api/fo-queue
GET /api/fo-cheap-quality
GET /api/fo-package/{company_id}
```

## Historical lessons (IIP-specific)

- Vite proxy port drift (8001 vs 8000) — FIXED this session (e5f4134). Verify proxy still works before judging "failed to load".
- AM API demo IDs ≠ pipeline IDs (`theme-ai-infra` not `TH-004`). Use list-endpoint IDs.
- Windows server triple: bare `python` stub, vite IPv6 ::1, npm wrapper kill leaves node child.

<!-- 2026-08-03 21:20 UTC+7 -->
