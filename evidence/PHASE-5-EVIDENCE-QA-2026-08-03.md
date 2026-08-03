# Phase 5 Evidence QA — Real-Data Production Path (FD #46)

> Date: 2026-08-03 · Owner: Parent (deepseek-v4-flash) · Mode: Critical
> Basis: arch v0.4 + plan v1.1 (Council findings folded). Updated after Final Council REWORK round 1 (F1–F4 fixes applied).

## 10-Point Checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Locked tests pass | ✅ | `tests/locked/test_real_data_api.py` 39/39 — TEST_VERIFIED |
| 2 | Canonical tests pass | ✅ | 301/301 total (129 locked + 56 AM + 42 FO + 25 CS + 49 II) — TEST_VERIFIED |
| 3 | Targeted suite passes | ✅ | per-directory pytest exit 0 each — TEST_VERIFIED |
| 4 | No regression in critical paths | ✅ | baseline 262 pre-change → 301 post; all 5 dirs green — TEST_VERIFIED |
| 5 | Negative path tests exist | ✅ | 401/403/503 admission, corrupt/missing/stale/unknown-mode, tampered/expired/revoked cookies, immutable-run rejection, FK violation — TEST_VERIFIED |
| 6 | Diff review (no unintended changes) | ✅ | git diff reviewed per commit; no broker/execution/allocation paths touched — STATIC_OBSERVATION |
| 7 | Git status clean | ✅ | clean after closeout commit — STATIC_OBSERVATION |
| 8 | Deployment smoke | ✅ | uvicorn boot (auth guards), all 6 endpoints 200 with real data, SQLite schema_version compatible — TEST_VERIFIED |
| 9 | gate-check.sh exit 0 | ✅ | Gate 3/4/5/6 pass — TEST_VERIFIED |
| 10 | isolation-scan.sh exit 0 | ✅ | no forbidden-path violations — TEST_VERIFIED |
| 11 | Mutation testing lite (admission/auth) | ✅ | tampered cookie, expired token, wrong-mode artifact, immutable reject all locked — TEST_VERIFIED |
| 12 | Property/invariant testing | ✅ | FK NOT NULL, UNIQUE (module,run_id), schema_version reject, dedupe by component — TEST_VERIFIED |

## Council F1–F4 Remediation Verification (round 1 REWORK)

- F1 (lineage wiring): adapters ingest exact served bytes; middleware records real status + response SHA; dashboard run_ids non-null — locked by `test_endpoint_to_db_lineage_wired` + `test_api_reads_lineage_records_real_status_and_hash` — TEST_VERIFIED
- F2 (test strength): +5 tests (subprocess startup guards, expired session, no-embedded-run mutation, endpoint→DB, real hash) — TEST_VERIFIED
- F3 (adapter registry): `backend/adapter_registry.json` immutable hash; code-change-without-version-bump fails — TEST_VERIFIED
- F4 (evidence packet): Plan Council artifact + this QA record + browser audit record committed; correct commit hash cited — STATIC_OBSERVATION

## Verification Tags
All claims tagged per policy: TEST_VERIFIED / STATIC_OBSERVATION / BROWSER_VERIFIED (browser lane: login→dashboard→AM→theme→FO→CS, 0 JS errors).

<!-- 2026-08-03 21:30 UTC+7 -->
