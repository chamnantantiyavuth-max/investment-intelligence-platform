# Phase 3 Plan — Real-Data Production Path (FD #46)

> Version: v1.1 · 3 Aug 2026 · Critical Mode · Phase 3 (revised after Plan Council Lite: PASS WITH FIXES, 8 findings addressed)
> Basis: `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.4 (committed `5cc5db2`). Council evidence: reviewer summary (8 findings) — all folded (tags C1–C8).
> Founder decisions required: D1 (stdlib sqlite3), D2 (fail closed), D3 (staleness bounds), D4 (2R disposition). **All default Option A — MUST be recorded as Founder-approval FDs before T1 executes (C8/T0).**

## T0 — Founder approval gate (precondition, C8)
- Record Founder approval of D1–D4 in `operational/FOUNDERS-DECISIONS.md` (items 63–66 or one consolidated entry) + vault fd-register before ANY implementation task starts.
- **Verify:** grep FOUNDERS-DECISIONS.md for the four decision IDs; git commit the approval record.

## T1 — Locked acceptance tests, written FIRST (TDD RED, C1)
- **Scope:** `tests/locked/test_real_data_api.py` — the FULL 12-point charter from arch §9 (route inventory, auth matrix, AM/FO/II/CS contracts, dashboard agreement, persistence lineage, fail-closed/stale, concurrency, E2E subprocess, frontend build). Written before implementation; every task below must make its slice GREEN.
- **RED gate:** run `python -m pytest tests/locked/test_real_data_api.py -q` → must FAIL (file exists, tests fail against current code). This is the contract.
- **Contract (persistence, C7 — both mutation cases locked):** (a) bytes WITH embedded run_id mutated → same (module,run_id) different sha256 → REJECT (raise); (b) bytes WITHOUT run_id → hash-derived id, new bytes → new id. Both asserted.
- **Verify:** RED confirmed, then each task T2–T9 runs its slice to GREEN.

## T2 — Persistence layer (`backend/persistence.py`, new)
- **Scope:** SQLite stdlib; DB `backend/data/iip.db`; artifact store `backend/data/artifacts/<sha256>.json`; tables `pipeline_runs`, `api_reads`, `api_read_runs`, `settings`.
- **Contract:** `PRAGMA foreign_keys=ON` + WAL + `busy_timeout=5000` every connection; `ingest_run(module, bytes)` (sha256, store bytes, upsert-or-reject-immutable per C7); `log_read(endpoint, params, data_source, response_sha256, status, adapter_version, runs:[(run_id, component)])` → `api_reads` + `api_read_runs` rows; `settings` init `schema_version=1`, reject newer; nonce get/set.
- **Edge cases:** FK violation rejected; concurrent writes busy-retried; newer schema → refuse boot; corrupt JSON → raise.
- **Verify:** `pytest tests/locked/test_real_data_api.py -k persistence` GREEN; ad-hoc: ingest → re-ingest same → no dup; mutate-with-run_id → raises; no-run_id → new id.

## T3 — Auth (`backend/auth.py` + middleware in `main.py`)
- **Scope:** login/logout/status; `require_auth`; loopback Host middleware; startup guards; nonce persistence.
- **Contract:** env `IIP_AUTH_USER`(default founder)/`IIP_AUTH_PASSWORD`(required)/`IIP_AUTH_SECRET`(≥32 chars, required); cookie `{nonce, issued_at, expires_at} | HMAC-SHA256`; server validates sig+nonce+expiry; logout revokes; `hmac.compare_digest`; allowlist exactly health/login/status; non-loopback Host → 403.
- **Edge cases:** missing/weak env → refuse boot; tampered/expired/revoked → 401; wrong password → 401; non-loopback → 403.
- **Verify:** `pytest -k auth` GREEN; curl login ok/401; restart keeps session.

## T4 — Response contracts (`backend/schemas/responses.py`, revise + add)
- **Scope:** `Provenance`; `ThemeSummary` (real fields), `CandidateSummary` (6-field entry_readiness), `AMQueueResponse {run_id, point_in_time, themes:[{theme, candidates}]}`; `IISignalSummary`/`IISignalsResponse`; `DashboardSummary` per-component; FO summary/detail + provenance; remove synthetic-only fields + `data_source` defaults from real surfaces.
- **Contract:** every field maps to real artifact field or locked derivation; `value_trap_verdict` per §3; provenance required on all real surfaces.
- **Edge cases:** missing optional field → empty/None, never fabricated; hybrid flag correct.
- **Verify:** `pytest -k schemas` GREEN; pydantic validation of real artifact samples.

## T5 — Adapters (`backend/adapters.py`, new) + adapter registry (C5)
- **Scope:** `load_snapshot(module)` single read; `admit(module, artifact)` → provenance | raise 503 (mode real required, staleness D3); AM mapping (theme/candidate/evidence_provenance real|synthetic|human_sourced); FO envelope + locked flattening; II passthrough + partial; dashboard per-component admission (unadmitted → null).
- **Adapter registry (C5):** `ADAPTER_REGISTRY = {"v1": {"code_hash": <sha256 of adapters.py at load>, ...}}` — deterministic code-hash computed at import; `adapter_version` persisted in `api_reads` comes from this registry; a source change without registry/hash update fails the locked assertion.
- **Edge cases:** missing/synthetic/unknown-mode/stale artifact → 503; legacy FO root list → 503; `source:null`/`Founder Obsidian Vault`/`Founder Journal` → `human_sourced`; `SRC-SYN-*` → `synthetic`; `_real_eod` → `real`.
- **Verify:** `pytest -k adapter` GREEN; ad-hoc: real AM artifact → hybrid:true, 9 themes; **mutate adapters.py → registry hash test FAILS (C5)**.

## T6 — Routes + ASGI capture (`backend/api/am_routes.py`, `fo_routes.py`, `ii_routes.py` new, `cs_routes.py` untouched, `main.py`)
- **Scope:** wire adapters; `require_auth` on all except allowlist; `ii_routes` `/api/ii-signals`; dashboard consumes admitted runs + exact cs mock; ASGI middleware captures ordered response body chunks → `response_sha256` committed after send completes.
- **Contract:** read-don't-re-run; 503 with metadata; 404 preserved; CS unchanged; dashboard CS counts == cs mock (SOL-003); response hash over exact bytes.
- **Edge cases:** concurrent refresh → old-or-new; auth-before-503 ordering; hash over exact bytes.
- **Verify:** `pytest -k routes` GREEN; curl with/without cookie; hash matches served bytes.

## T7 — Runner provenance + atomicity (C3: full propagation surface)
- **FO (`fundamental-opportunity-v0/`):** `run.py` envelope `{run_id, provenance, packages}` + atomic write (tmp+fsync+os.replace). **Mode propagation contract (C3):** `run_pipeline(companies=None, mode="synthetic")` → `build_research_package(company, mode)` → `_supporting_evidence(company, mode)` — **backward-compatible default `synthetic`** so existing callers unchanged; the "Financial data: synthetic fixture" line (pipeline.py:300) emitted only when `mode=="synthetic"`. Real runs pass `mode="real"`.
- **II (`institutional-intelligence-v0/`):** `run.py` meta.data_source reflects `--real`; stamp `as_of`; **`display.py:134-141` `save_json` → atomic write (tmp+os.replace)** (file added to scope, C3); partial preserved.
- **Contract:** provenance metadata only — no analytical logic change; existing FO/II test_locked tests still pass (91/91).
- **Edge cases:** interrupted write → old file intact; no network → honest synthetic mode stamped, never fake real.
- **Verify:** `pytest fundamental-opportunity-v0/test_locked institutional-intelligence-v0/test_locked` (91 GREEN); ad-hoc: real-mode run → envelope root + no synthetic-fixture line; atomicity via interrupted-write simulation.

## T8 — Frontend migration (`frontend/src/`) — FULL surface (C4)
- **Scope:** types — `types/am.ts` (locked contracts), **`types/fo.ts` + `types/ii.ts` (NEW, add provenance)**, dashboard response type; clients — `amClient.ts`/`foClient.ts`/`csClient.ts` `credentials: 'include'` + **new `iiClient.ts` + `authClient.ts`**; `App.tsx` auth gate + login route/page; **`DashboardPage.tsx` consumes `/api/dashboard/summary` (remove hardcoded 8/3)**; **AM pages adapt to `{theme, candidates}` + provenance banners; FO pages (`FundamentalQueuePage`, `FundamentalDetailPage`, `CheapQualityPage`) consume real provenance, remove unconditional synthetic labels (C4)**.
- **Contract:** `npm run build` exit 0; no hardcoded synthetic counts; login → protected pages render; no unconditional synthetic label on AM/FO surfaces.
- **Edge cases:** 401 → redirect login; login failure message; page refresh keeps session; unadmitted component renders unavailable state.
- **Verify:** `npm run build` exit 0; browser smoke (login → am-queue → dashboard agreement → FO provenance banner).

## T9 — Real runs (data refresh; C2 committable artifacts)
- **Precondition (C2):** config task FIRST — `.gitignore` adds `/backend/data/*.db*`, `!.env.example`, and **narrow exceptions for the two approved JSON artifacts** (root output/ exception refined to track only `fundamental-opportunity-v0/output/pipeline_result.json` + `institutional-intelligence-v0/output/institutional_signals.json`); create `.env.example` (3 vars documented, no real values). **Verify `git check-ignore -v` + `git status --short` before running.**
- **Scope:** `python3 fundamental-opportunity-v0/run.py --real --json-only`; `python3 institutional-intelligence-v0/run.py --real --json-only`.
- **Contract (separate assertions per artifact, C8):** FO — envelope `{run_id, provenance, packages}` present, `provenance.mode == "real"`, no synthetic-fixture evidence text; II — `meta.data_source == "REAL 13F"` (or real-partial), `as_of` stamped. Retry bounded: max 2 attempts, then report failure honestly (never fake).
- **Verify:** inspect both output files per the separate assertions; `git status --short` shows the two tracked artifacts + `.env.example` + `.gitignore` changes only.

## T10 — Evidence QA → integration (C6: infrastructure + baseline commands)
- **Precondition (C6):** create `scripts/gate-check.sh` + `scripts/isolation-scan.sh` (adapted from workflow references; project currently has NO scripts/ files — verified).
- **Phase 5:** 10-point checklist + `bash scripts/gate-check.sh` exit 0 + `bash scripts/isolation-scan.sh` exit 0 + Parent re-verify (locked tests run independently) + mutation-testing-lite on admission/auth logic.
- **Phase 6 per-directory suite (exact commands + expected counts, C6):**
  - `python -m pytest tests/locked -q` → 90 + new locked (≥102)
  - `python -m pytest alpha-momentum-v0/experimental -q` → 56
  - `python -m pytest fundamental-opportunity-v0/test_locked -q` → 42
  - `python -m pytest close_system/test_locked -q` → 25
  - `python -m pytest institutional-intelligence-v0/test_locked -q` → 49
  - `npm run build` → exit 0
- **Verify:** each exits 0 independently (per-directory convention, MEM-IIP-004 — never one root-level pytest).

## T11 — Release gates
- **Final Council** (Sol Medium, mandatory — artifact `evidence/COUNCIL_DECISION-final-2026-08-03.md` before Founder presentation).
- **Final production audit** — prelaunch-close-beta split-lane: Parent browser + Sol Medium API/oracle (per 3 Aug pattern).

## Verification tags policy
Every closeout claim tagged: TEST_VERIFIED / STATIC_OBSERVATION / EXTERNAL_NOT_TESTED / INFERENCE.

## Constraints (unchanged from FD #46)
No broker/execution/allocation · no new investment rules · no CS real data · no multi-user · no external deployment · financial logic untouched · provenance never invented.

## Rollback
Checkpoint before T7 (runner changes): `git tag rollback-fd46-pre-runners`. DB + artifact store are regenerable artifacts.

<!-- 2026-08-03 21:45 UTC+7 -->
