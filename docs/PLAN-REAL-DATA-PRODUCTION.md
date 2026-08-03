# Phase 3 Plan — Real-Data Production Path (FD #46)

> Version: v1.0 · 3 Aug 2026 · Critical Mode · Phase 3
> Basis: `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.4 (committed `5cc5db2`) — Phase 2R rounds 1–3 findings folded in.
> Founder decisions required: D1 (stdlib sqlite3), D2 (fail closed), D3 (staleness bounds), D4 (2R disposition → locked-test enforcement). All recommended Option A.

## Execution order & task contracts

### T1 — Persistence layer (`backend/persistence.py`, new)
- **Scope:** SQLite via stdlib `sqlite3`; DB `backend/data/iip.db`; artifact store `backend/data/artifacts/<sha256>.json`; tables `pipeline_runs`, `api_reads`, `api_read_runs`, `settings`.
- **Contract:** `PRAGMA foreign_keys=ON` + WAL + `busy_timeout=5000` on every connection; `ingest_run(module, bytes) -> run_id` (sha256, store bytes, upsert-or-reject-immutable); `log_read(endpoint, params, data_source, response_sha256, status, adapter_version, runs:[(run_id, component)])`; `settings` init `schema_version=1`, reject newer; `get_active_nonce`/`set_active_nonce`.
- **Edge cases:** same (module,run_id) different sha256 → raise; corrupt JSON → raise; concurrent writes → busy_timeout retry; newer schema → refuse boot.
- **Verify:** `python -m pytest tests/locked/test_real_data_api.py -k persistence`; ad-hoc: ingest → re-ingest same → no dup; mutate bytes → new run_id; FK violation rejected.

### T2 — Auth (`backend/auth.py` + middleware in `main.py`)
- **Scope:** `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/status`; `require_auth` dependency; loopback Host middleware; startup guards.
- **Contract:** env `IIP_AUTH_USER`(default founder)/`IIP_AUTH_PASSWORD`(required)/`IIP_AUTH_SECRET`(≥32 chars, required); cookie `iip_session` = `{nonce, issued_at, expires_at} | HMAC-SHA256`; server validates signature+nonce+expiry; logout revokes nonce; `hmac.compare_digest`; allowlist exactly health/login/status; non-loopback Host → 403.
- **Edge cases:** missing/weak env → refuse boot; tampered cookie → 401; expired → 401; revoked → 401; wrong password → 401 (no user enumeration); non-loopback → 403.
- **Verify:** `pytest -k auth`; curl login ok/401; restart keeps session (nonce persisted).

### T3 — Response contracts (`backend/schemas/responses.py`, revise + add)
- **Scope:** `Provenance` object; `ThemeSummary` (real fields), `CandidateSummary` (6-field entry_readiness), `AMQueueResponse {run_id, point_in_time, themes:[{theme, candidates}]}`; `IISignalSummary`/`IISignalsResponse`; `DashboardSummary` per-component provenance; FO summary/detail + provenance; remove synthetic-only fields + `data_source` defaults from real surfaces.
- **Contract:** every field maps to a real artifact field or locked derivation; `value_trap_verdict` per §3; provenance required on all real surfaces.
- **Edge cases:** missing optional artifact field → empty string/None (never fabricated number); hybrid flag correct.
- **Verify:** `pytest -k schemas`; pydantic validation of real artifact samples.

### T4 — Adapters (`backend/adapters.py`, new)
- **Scope:** `load_snapshot(module) -> (bytes, parsed)` single read per request; `admit(module, artifact) -> provenance|raise 503` (mode real required, staleness D3); AM mapping (theme/candidate/evidence_provenance real|synthetic|human_sourced); FO envelope + locked flattening; II passthrough + partial; dashboard per-component admission (unadmitted → null).
- **Contract:** provenance derived from artifact fields only; `source:null`/`Founder Obsidian Vault`/`Founder Journal` → `human_sourced`; `SRC-SYN-*` → `synthetic`; `_real_eod` → `real`.
- **Edge cases:** missing artifact → 503; synthetic mode → 503; unknown mode → 503; stale → 503; legacy FO root list → 503.
- **Verify:** `pytest -k adapter`; ad-hoc: point at real AM artifact → hybrid:true, 9 themes.

### T5 — Routes (`backend/api/am_routes.py`, `fo_routes.py`, `ii_routes.py` new, `cs_routes.py` untouched, `main.py`)
- **Scope:** wire adapters; `require_auth` on all except allowlist; `ii_routes` new `/api/ii-signals`; dashboard consumes admitted runs + exact cs mock; ASGI middleware captures response bytes → `response_sha256`.
- **Contract:** read-don't-re-run; 503 semantics with metadata; 404 preserved; CS unchanged; dashboard CS counts == cs mock (SOL-003).
- **Edge cases:** concurrent refresh → old-or-new; 401 vs 503 ordering (auth first); response hash over exact bytes.
- **Verify:** `pytest -k routes`; curl with/without cookie.

### T6 — Runner provenance + atomicity (`fundamental-opportunity-v0/run.py` + `pipeline.py:300`, `institutional-intelligence-v0/run.py`)
- **Scope:** FO: envelope `{run_id, provenance, packages}`, atomic write (tmp+fsync+os.replace), gate "synthetic fixture" evidence line on synthetic mode; II: `meta.data_source` reflects `--real`, stamp `as_of`, atomic write, partial preserved.
- **Contract:** provenance metadata only — no analytical logic change; existing FO/II tests still pass.
- **Edge cases:** interrupted write → old file intact (atomic); no network → honest synthetic mode stamped, never fake real.
- **Verify:** `pytest fundamental-opportunity-v0/test_locked institutional-intelligence-v0/test_locked` (262 baseline intact); real run smoke.

### T7 — Frontend migration (`frontend/src/`)
- **Scope:** types updated to locked contracts (`types/am.ts` + new ii types); ALL clients `credentials: 'include'`; `authClient`; App.tsx auth gate + login route/page; **DashboardPage consumes `/api/dashboard/summary` (remove hardcoded 8/3)**; AM pages adapt to `{theme, candidates}`.
- **Contract:** `npm run build` exit 0; no hardcoded synthetic counts; login → protected pages render.
- **Edge cases:** 401 → redirect login; login failure message; page refresh keeps session (cookie).
- **Verify:** `npm run build`; browser smoke (login → am-queue → dashboard agreement).

### T8 — Real runs (data refresh)
- **Scope:** `python3 fundamental-opportunity-v0/run.py --real --json-only`; `python3 institutional-intelligence-v0/run.py --real --json-only`.
- **Contract:** outputs in envelope/meta-stamped format; committed as real artifacts; provenance labels truthful.
- **Edge cases:** yfinance partial failure → partial coverage recorded honestly; network down → retry, never fake.
- **Verify:** inspect output files: envelope present, meta.data_source REAL, as_of stamped.

### T9 — Locked tests (`tests/locked/test_real_data_api.py`, new)
- **Scope:** 12-point charter from arch §9 (route inventory, auth full matrix, AM/FO/II/CS contracts, dashboard agreement, persistence lineage, fail-closed/stale, concurrency, E2E subprocess, frontend build).
- **Contract:** locked; no expected-value change without Bible quote/FD.
- **Verify:** `pytest tests/locked/test_real_data_api.py` green.

### T10 — Evidence QA → integration → release gates
- Phase 5: 10-point checklist + gate-check.sh + isolation-scan.sh + Parent re-verify (locked tests run independently) + mutation-testing-lite on admission/auth logic.
- Phase 6: full per-directory suite (262 + new) + `npm run build` + browser.
- Phase 7: **Final Council** (Sol Medium, mandatory — artifact to `evidence/COUNCIL_DECISION-final-2026-08-03.md`) → **final production audit** (prelaunch-close-beta split-lane: Parent browser + Sol Medium API/oracle).

## Verification tags policy
Every closeout claim tagged: TEST_VERIFIED / STATIC_OBSERVATION / EXTERNAL_NOT_TESTED / INFERENCE.

## Constraints (unchanged from FD #46)
No broker/execution/allocation · no new investment rules · no CS real data · no multi-user · no external deployment · financial logic untouched · provenance never invented.

## Rollback
Checkpoint before T6/T8 (runner/output changes): `git tag rollback-fd46-pre-runners`. Destructive ops (DB file) are regenerable artifacts.

<!-- 2026-08-03 21:30 UTC+7 -->
