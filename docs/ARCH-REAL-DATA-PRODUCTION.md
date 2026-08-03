# Architecture — Real-Data Production Path (FD #46)

> Version: v0.3 · 3 Aug 2026 · Critical Mode · Phase 2 (revision 2 after Phase 2R rounds 1–2 FAIL)
> FD #46: Real-Data Production Path (API wiring + persistence + auth) — supersedes FD #44 for THIS SCOPE ONLY.
> Phase 2R round 1 (566s): FAIL, 8 findings. Round 2 (512s): FAIL — F3/F7 closed, F1/F2/F4/F5/F6/F8 retained defects + 3 new findings (NF1–NF3). All addressed below. Regression: 2 of 2 used → **3rd review round requires Founder escalation (Section 11).**

## 1. Verified current state (2026-08-03)

| Surface | Current behavior | Real data available |
|---|---|---|
| `GET /api/am-queue`, `/api/am-theme/{id}` | `_MOCK_THEMES` (5 hardcoded demo themes) | ✅ `alpha-momentum-v0/output/pipeline_result.json` — **REAL EOD (YAHOO FINANCE)**, point_in_time 2026-08-03, coverage 9/9, `queue` = `[theme_id, {theme, candidates}]`; **10 `_real_eod` market overlays (2026-07-31) + 13 `SRC-SYN` evidence markers coexist — hybrid artifact (verified)** |
| `GET /api/fo-queue`, `/api/fo-package/{id}`, `/api/fo-cheap-quality` | **Re-runs synthetic `run_pipeline()` in-memory per request** (fixture, generated 2026-07-26) | ⚠️ Real path: `run.py --real` (yfinance). Current artifact = root list, **no run metadata**, `value_trap: {triggered: false}` only; `pipeline.py:300` hardcodes "Financial data: synthetic fixture" evidence text even on real runs |
| `GET /api/cs-radar` | `_MOCK_ASSETS` (3), `synthetic_demo` | ❌ None — CS has NO real data. **Stays synthetic (FD #46 explicit).** Served mock ≠ CS pipeline artifact (different collections) |
| `GET /api/dashboard/summary` | Derives CS counts from cs mock (SOL-003) | AM/FO/II run metadata available |
| `GET /api/health` | ok | — |
| Institutional Intelligence | **NO API surface** | ✅ Real 13F via `run.py --real` (SEC EDGAR). Current artifact `meta.data_source: SYNTHETIC` — **must be rejected on real endpoint until a real run exists (F5)** |

**Environment (verified):** backend on `python` = hermes-agent venv 3.11 (fastapi/uvicorn/pydantic; no sqlalchemy/itsdangerous/jose; broken numpy). `python3` = WindowsApps 3.14 (working yfinance — FO/II real runs). Tests run per-directory (MEM-IIP-004): 262/262. `.gitignore` covers `*.env` **but NOT `*.db`** — rule added (F6).

## 2. Design principles

1. **Read, don't re-run** — API reads approved pipeline output JSONs (per-module single source of truth). **[F3] Atomic handoff:** runners write tmp → flush/fsync → `os.replace`. Adapter loads **one immutable byte snapshot per request**; same bytes drive hash, ingest, map, serve (no TOCTOU).
2. **Provenance read from the artifact, never invented.** Canonical object `{source, mode, as_of, coverage, completeness, hybrid}` derived from artifact fields. **[F4] Component-level honesty:** AM exposes per-theme + per-candidate provenance (market overlays `real_eod` 2026-07-31 vs `SRC-SYN` synthetic evidence → `hybrid: true` when both present); II preserves `PARTIAL (x/y)` verbatim; FO evidence text fixed at the source (pipeline.py:300 gated on mode) so no blanket `real_*` over mixed content.
3. **[F5] Fail closed — admission rule.** Real endpoints (AM/FO/II) **reject** artifacts whose mode is `synthetic`, unknown, or missing → **HTTP 503** + failed-artifact metadata. NO synthetic fallback, NO serving wrong-mode artifacts on real surfaces (CS is the sole synthetic surface, per FD #46). **Staleness:** artifact must carry `point_in_time`/`as_of`; age thresholds per module → **D3 Founder decision** (AM EOD ≤7d, FO ≤30d, II ≤120d given 45-day filing lag — operational bounds, not investment rules).
4. **Zero new runtime dependencies** (stdlib `sqlite3`, `hmac`, `secrets`, `hashlib`). **D1 — Founder decision** (F7): FD text names SQLAlchemy; stdlib meets intent without installing into the fragile shared hermes venv.
5. **CS stays synthetic** — no real CS data exists.

## 3. Response contract revision (F1 — locked from real artifact fields)

> FD #46 authorizes API wiring + truthful provenance. Current contracts embed synthetic-only fields (`driver_count`, evidence counts, numeric quality scores — absent from real artifact) and default `data_source: "synthetic_demo"`. Contracts below verified against actual artifacts (2026-08-03). No score/ranking/quality computation changes.

### Provenance object (required on every real surface)

```json
{ "source": "yahoo_finance_eod", "mode": "real", "as_of": "2026-08-03",
  "coverage": "9/9", "completeness": "complete", "hybrid": true }
```
`hybrid: true` when the artifact mixes real + synthetic components (AM: `_real_eod` overlays + `SRC-SYN` evidence). `as_of` = market overlay date for price/rank fields; `point_in_time` = pipeline run date (may differ — captured separately).

### AM (`/am-queue`, `/am-theme/{id}`)

- `ThemeSummary` → real fields: `id, name, sector, industry, lifecycle, approval_status, monitoring_status, confidence, key_tickers, stocks_in_industry, why_now` + `provenance` + `evidence_provenance` (list of `{source_id, source_type: real|synthetic}` per evidence block).
- `CandidateSummary` (new): `id, ticker, research_state, conviction_level, candidate_quality {7 categorical}, entry_readiness {6 fields — verified: price_structure, base_quality, breakout_proximity, volume_behavior, volatility_contraction, extension_risk}, data_confidence {freshness, completeness, reliability, conflicts, missing_data}` + `provenance` (component map: which fields real_eod vs synthetic).
- `AMQueueResponse`: `{run_id, point_in_time, themes: [{theme, candidates}]}`.

### FO (envelope change + value-trap derivation)

- **Persisted envelope locked (NF2):** FO artifact becomes `{run_id, provenance, packages: [...]}` — runner stamps it; legacy root-list artifacts **rejected on real endpoints** until migrated.
- `ResearchPackageSummary` / `ResearchPackageDetail`: keep field shape (maps 1:1 to package fields, verified) + required `provenance`.
- **`value_trap_verdict` derivation (locked, from spec §3.6.2 + locked tests):** if artifact `valuation_context.value_trap.triggered == true` → use `verdict` (vocabulary: `NOT_A_TRAP` / `VALUE_TRAP` etc. from `value_trap.py` verdict_map, locked in `test_value_trap.py`); if `triggered == false` → `"NOT_TRIGGERED"` (display label — check was not run, company not unusually cheap). **`/fo-cheap-quality` filter unchanged:** `value_trap_verdict == "NOT_A_TRAP"` (only matches triggered-and-passed, per spec §3.6.2 Cheap & Quality watchlist). No fabricated verdicts beyond the documented `NOT_TRIGGERED` label.
- **Evidence text fix (F4):** `fundamental-opportunity-v0/pipeline.py:300` gates the "Financial data: synthetic fixture" evidence line on `mode == synthetic` — real runs emit no synthetic-fixture claim.

### II (new `/ii-signals`)

- `IISignalSummary`: `filer_name, filer_cik, filer_category, ticker, filing_quarter, report_date, pct_of_portfolio, conviction, action, change_pct, signal_score, value_usd`.
- `IISignalsResponse`: `{signals, summary, meta}` passthrough + `provenance` — mode **must be real** (or real-partial: `source: "sec_edgar_13f", mode: "real", completeness: "partial_3_5"`). `SYNTHETIC` artifact → 503 (F5).

### Dashboard (`/api/dashboard/summary`)

- **Per-component provenance** (F1/NF3): `{am: {run_id, point_in_time, data_source}, fo: {...}, ii: {...}, cs: {run_id: null, point_in_time: null, data_source: "synthetic_demo", source: "backend_static_mock"}}`. **CS is NOT linked to the unrelated CS pipeline artifact** (served mock ≠ artifact — NF3). CS counts stay from the exact served mock bytes.

### CS (`/api/cs-radar`)

- **Unchanged** — mock + `synthetic_demo` (authorized).

## 4. Persistence — SQLite (stdlib `sqlite3`), immutable, content-addressed (F2/NF1)

DB: `backend/data/iip.db` + **immutable artifact store** `backend/data/artifacts/<sha256>.json` (copy of exact served bytes). `.gitignore` gains `/backend/data/*.db*`. WAL, `busy_timeout=5000`, per-operation connections, **`PRAGMA foreign_keys=ON` on every connection (NF1)**.

```sql
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    run_id TEXT NOT NULL,              -- artifact run_id, else sha256[:16] content-addressed
    point_in_time TEXT,
    fixture_category TEXT,             -- provenance verbatim
    artifact_sha256 TEXT NOT NULL,     -- immutable identity; artifact bytes stored in artifacts/<sha256>.json
    artifact_path TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    UNIQUE (module, run_id)
);
-- IMMUTABLE: same (module, run_id) + different artifact_sha256 → REJECT (raise), never collapse (F2)

CREATE TABLE IF NOT EXISTS api_reads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id_fk INTEGER NOT NULL REFERENCES pipeline_runs(id),  -- NOT NULL for successful reads (NF1)
    endpoint TEXT NOT NULL,
    route_params TEXT,                 -- JSON (e.g. theme_id)
    data_source TEXT NOT NULL,
    response_sha256 TEXT NOT NULL,     -- hash over exact serialized response bytes (ASGI capture)
    status INTEGER NOT NULL,
    adapter_version TEXT NOT NULL,
    served_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);  -- schema_version ONLY. NO auth secret, NO credentials (F6 — env-only)
```

**Lineage (F2):** served response is deterministically reconstructable from `(artifact bytes in artifacts/<sha256>.json, adapter_version, route_params)`; `response_sha256` (captured at ASGI boundary over the exact serialized bytes sent) verifies. `run_id_fk NOT NULL` + `PRAGMA foreign_keys=ON` guarantees no orphan lineage records. **No response bodies stored** — reconstruction via immutable artifact + versioned adapter is the design; `response_sha256` is the integrity check.

**Ingest flow:** `persistence.ingest_run(module, bytes)` → hash → store bytes in artifact store → upsert-or-reject-immutable → return run row. `persistence.log_read(...)` records endpoint, params, response hash, status, adapter version, FK.

## 5. Auth — single-user, stdlib HMAC session (F6)

1. **Startup guard (fail fast):** refuse to boot if `IIP_AUTH_PASSWORD` unset/empty or `IIP_AUTH_SECRET` <32 chars. No default credentials. Secrets env-only — **never persisted to SQLite settings** (F6).
2. `POST /api/auth/login` — `{username, password}` → constant-time `hmac.compare_digest` vs env (username default `founder`). Success → generate nonce (stored in `settings.active_session_nonce`), cookie `iip_session` = `{nonce, issued_at, expires_at} | HMAC-SHA256(secret)`. **Server-side expiry + nonce validation on every request** (F6 — a copied token after `expires_at` or after logout is rejected server-side, not just by the browser).
3. `POST /api/auth/logout` — **revokes server-side** (clears nonce) + clears cookie.
4. `GET /api/auth/status` — independently verifies cookie signature + nonce + expiry; returns `{authenticated: bool}` only. Exempt from auth, leaks nothing.
5. `require_auth` on ALL `/api/*` except exactly: `/api/health`, `/api/auth/login`, `/api/auth/status` (route-inventory test enforces).
6. **Loopback enforcement (F6):** launch command pins `--host 127.0.0.1`; app middleware rejects requests whose `Host` header is non-loopback while `Secure=False` (403). Cookie: HttpOnly, SameSite=Lax, max_age 12h (advisory — server enforces `expires_at`).
7. Frontend: React Router gate → login page on 401/status=false; API client `credentials: 'include'`.
8. Secrets: env vars only (`IIP_AUTH_USER`/`IIP_AUTH_PASSWORD`/`IIP_AUTH_SECRET`), `.env` gitignored, `.env.example` documents them.

## 6. API wiring map

| Endpoint | Reads | Provenance from |
|---|---|---|
| `/api/am-queue`, `/am-theme/{id}` | AM artifact `queue` (byte snapshot) | `fixture_category` + per-theme/per-candidate overlay+evidence labels → `{source, mode, as_of, coverage, completeness, hybrid}`; evidence_provenance list |
| `/api/fo-queue`, `/fo-package/{id}`, `/fo-cheap-quality` | FO artifact envelope `{run_id, provenance, packages}` | envelope `provenance`; value_trap_verdict derived per §3 |
| `/api/ii-signals` (**NEW**) | II artifact | `meta.data_source` — mode must be real; partial preserved verbatim |
| `/api/cs-radar` | **unchanged** mock | `synthetic_demo` |
| `/api/dashboard/summary` | `pipeline_runs` latest per module | per-component `{run_id, point_in_time, data_source}`; CS = `{null, null, synthetic_demo, backend_static_mock}` |
| `/api/health` | — | — |

**Runner changes (provenance + atomicity only):**
- FO `run.py`: wrap output as `{run_id, provenance, packages}` (NF2); atomic write (tmp + `os.replace`); stamp `{source: yfinance, mode, as_of, coverage, completeness}`.
- FO `pipeline.py:300`: gate "synthetic fixture" evidence line on synthetic mode (F4).
- II `run.py`: verify `meta.data_source` reflects `--real` (fix if hardcoded); atomic write; preserve partial status.

## 7. Real runs (data refresh)

- FO: `python3 fundamental-opportunity-v0/run.py --real --json-only` (yfinance, FO_TICKERS) — envelope + atomic write
- II: `python3 institutional-intelligence-v0/run.py --real --json-only`
- AM: already real (2026-08-03, 9/9) — ingest as-is (hybrid provenance preserved)
- Network verified reachable (429/403 = UA-limited; repo fetchers set proper headers)

## 8. Decisions required from Founder

| # | Decision | Recommendation |
|---|---|---|
| D1 | **Persistence:** stdlib `sqlite3` (this arch) vs FD-literal SQLAlchemy (install into fragile shared hermes venv) | **A — stdlib sqlite3.** Same SQLite persistence, zero install risk. |
| D2 | **Synthetic fallback on real endpoints** — arch now **fails closed (503)** with admission rule rejecting wrong-mode artifacts (F5) | **A — fail closed.** Fallback or wrong-mode serving would require a separate named FD. |
| D3 | **Staleness policy** — per-module age bounds for `as_of` (AM EOD ≤7d, FO ≤30d, II ≤120d given 45-day filing lag). Operational freshness bounds, NOT investment rules | **A — approve bounds.** Alternative: no age check (rely on mode+presence only) — weaker truth guarantee. |

## 9. Locked test charter (F8 — expanded, round-2 closures)

`tests/locked/test_real_data_api.py` (new):
1. **Route inventory:** every `/api/*` route except exact allowlist → 401 without cookie
2. **Auth:** login ok / wrong password / unset-credentials + weak-secret startup guards / cookie tamper (bad signature) / **expired (server-side, after `expires_at`)** / **revoked after logout** / status independent verification / **non-loopback Host → 403**
3. **AM:** real artifact fields served (no fabricated counts), **per-theme + per-candidate provenance incl. `hybrid: true` + evidence_provenance with SRC-SYN sources**, **exact 6-field entry_readiness**, /am-theme/{id} + 404
4. **FO:** reads envelope `{run_id, provenance, packages}` (no re-run), provenance marker present, `value_trap_verdict` derivation (triggered→verdict, else NOT_TRIGGERED), **legacy root-list artifact → 503**, /fo-package/{id} + 404, /fo-cheap-quality filter `NOT_A_TRAP` unchanged
5. **II:** /ii-signals 200 shape, meta + partial provenance passthrough; **SYNTHETIC artifact → 503 (admission rule)**
6. **CS:** unchanged `synthetic_demo` contract
7. **Dashboard:** per-component lineage incl. **CS `{null, null, synthetic_demo, backend_static_mock}` (NF3)**
8. **Persistence:** ingest upsert; **same run_id + different sha256 → rejected**; api_reads FK NOT NULL + response hash + status; **PRAGMA foreign_keys=ON + invalid-FK rejected (NF1)**; settings round-trip (no secret keys)
9. **Fail-closed + stale:** corrupt/missing artifact → 503 + metadata; **wrong-mode (synthetic) artifact → 503; stale (past D3 bound) → 503**
10. **Concurrency:** refresh (`os.replace`) during read → old or new complete artifact, never partial
11. **E2E smoke:** subprocess `python3` produces temp FO artifact (envelope) → 3.11 FastAPI ingests + serves it; artifact bytes in store match served provenance

## 10. Explicitly NOT in scope (FD #46)

Broker/execution/allocation · new pipeline stages · new investment rules/thresholds/weights/formulas/lookbacks · CS real data · CIW Phase 11 · multi-user/OAuth · external deployment · DB beyond SQLite · changing any score/quality/ranking computation · synthetic fallback on real surfaces · serving wrong-mode artifacts on real endpoints.

## 11. Regression status & escalation

Phase 2R rounds: 1 FAIL → 2 FAIL (F3/F7 closed; F1/F2/F4/F5/F6/F8 + NF1–NF3 addressed in v0.3). **Regression budget 2 of 2 used.** Per project-workflow, a 3rd review round requires **Founder escalation with options** — Section 8 D1/D2/D3 decisions + round-3 go/no-go presented at the Phase 3 plan gate.

<!-- 2026-08-03 21:05 UTC+7 -->
