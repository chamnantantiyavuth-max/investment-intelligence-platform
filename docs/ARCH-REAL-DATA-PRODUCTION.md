# Architecture — Real-Data Production Path (FD #46)

> Version: v0.4 · 3 Aug 2026 · Critical Mode · Phase 2 (revision 3; Phase 2R rounds 1–3 all FAIL, findings converged → implementation-level contracts)
> FD #46: Real-Data Production Path (API wiring + persistence + auth) — supersedes FD #44 for THIS SCOPE ONLY.
> Phase 2R: R1 FAIL (8 findings) → R2 FAIL (F3/F7 closed; 6 partial + NF1–NF3) → R3 FAIL (F3/F7/NF1/NF2/NF3 closed; 6 partial + NF4–NF8). **v0.4 closes all remaining items. Verification of implementation-level contracts moves to Phase 4 locked tests + Phase 5 Evidence QA + Phase 7 Final Council + final production audit (reviewer's own evidence gaps: runtime/browser behavior unverifiable without implementation).**

## 1. Verified current state (2026-08-03)

| Surface | Current behavior | Real data available |
|---|---|---|
| `GET /api/am-queue`, `/api/am-theme/{id}` | `_MOCK_THEMES` (5 hardcoded demo themes) | ✅ `alpha-momentum-v0/output/pipeline_result.json` — **REAL EOD (YAHOO FINANCE)**, point_in_time 2026-08-03, coverage 9/9, `queue` = `[theme_id, {theme, candidates}]`; **10 `_real_eod` market overlays (2026-07-31) + 13 `SRC-SYN` evidence + human-sourced metadata (Founder Obsidian Vault / Founder Journal) — hybrid artifact (verified)** |
| `GET /api/fo-queue`, `/api/fo-package/{id}`, `/api/fo-cheap-quality` | **Re-runs synthetic `run_pipeline()` in-memory per request** (fixture, generated 2026-07-26) | ⚠️ Real path: `run.py --real` (yfinance). Current artifact = root list, **no run metadata**, `value_trap: {triggered: false}` only; `pipeline.py:300` hardcodes "Financial data: synthetic fixture" evidence text even on real runs; **adapter extracts/flattens nested objects (sector/industry/moat/earnings/value-trap) — flattening must be documented + locked** (F1) |
| `GET /api/cs-radar` | `_MOCK_ASSETS` (3), `synthetic_demo` | ❌ None — CS has NO real data. **Stays synthetic (FD #46 explicit).** Served mock ≠ CS pipeline artifact |
| `GET /api/dashboard/summary` | **`frontend/src/pages/DashboardPage.tsx:61-67` hardcodes 8/3 — never calls the API (SOL-003 triple-agreement regression survives; verified)** | AM/FO/II run metadata available |
| `GET /api/health` | ok | — |
| Institutional Intelligence | **NO API surface** | ✅ Real 13F via `run.py --real` (SEC EDGAR). Current artifact `meta.data_source: SYNTHETIC` — **must be rejected on real endpoint until a real run exists** (F5) |

**Environment (verified):** backend on `python` = hermes-agent venv 3.11 (fastapi/uvicorn/pydantic; no sqlalchemy/itsdangerous/jose; broken numpy). `python3` = WindowsApps 3.14 (working yfinance — FO/II real runs). Tests run per-directory (MEM-IIP-004): 262/262. `.gitignore` covers `*.env`; `/backend/data/*.db*` rule **added in this workstream** (F6 — verified absent at commit `53aed9a`).

## 2. Design principles

1. **Read, don't re-run** — API reads approved pipeline output JSONs (per-module single source of truth). **[F3] Atomic handoff:** runners write tmp → flush/fsync → `os.replace`. Adapter loads **one immutable byte snapshot per request**; same bytes drive hash, ingest, map, serve (no TOCTOU).
2. **Provenance read from the artifact, never invented.** Canonical object `{source, mode, as_of, coverage, completeness, hybrid}` derived from artifact fields. **[F4] Three-way component classification (locked, no invention):** `real` (market/price/rank data from `_real_eod` overlays + real pipeline outputs), `synthetic` (explicit `SRC-SYN-*` evidence), `human_sourced` (evidence with `source: null`, `Founder Obsidian Vault`, `Founder Journal` — recorded as human, NOT auto-classified real/synthetic). Theme-level metadata (`why_now`, `confidence`, `lifecycle`, `approval_status`) originates from the human/synthetic review layer → **theme-level provenance is hybrid when any non-real component exists; every theme/candidate/evidence component carries a label; no blanket `real_*` over mixed content.** II preserves `PARTIAL (x/y)` verbatim. FO evidence text gated on mode (pipeline.py:300 fix).
3. **[F5] Fail closed — admission rule (per component).** Real endpoints (AM/FO/II) **reject** artifacts whose mode is `synthetic`, `unknown`, or missing → **HTTP 503** + failed-artifact metadata. **The dashboard applies the SAME mode+freshness admission independently per component** (NF7): unadmitted components → explicit `null`/`unavailable` state, never silent synthetic. NO synthetic fallback on real surfaces (CS is the sole synthetic surface, FD #46). **Staleness D3:** AM EOD ≤7d, FO ≤30d, II ≤120d (operational bounds, Founder decision).
4. **Zero new runtime dependencies** (stdlib `sqlite3`, `hmac`, `secrets`, `hashlib`). **D1 — Founder decision** (F7): FD text names SQLAlchemy; stdlib meets intent without installing into the fragile shared hermes venv.
5. **CS stays synthetic** — no real CS data exists.

## 3. Response contract revision (F1 — locked from real artifact fields)

> Current contracts embed synthetic-only fields (`driver_count`, evidence counts, numeric quality scores) and default `data_source: "synthetic_demo"`. Contracts below verified against actual artifacts (2026-08-03). No score/ranking/quality computation changes.

### Provenance object (required on every real surface)

```json
{ "source": "yahoo_finance_eod", "mode": "real", "as_of": "2026-08-03",
  "coverage": "9/9", "completeness": "complete", "hybrid": true }
```
`hybrid: true` when real + non-real components coexist. `as_of` = market overlay date (price/rank); `point_in_time` = pipeline run date (separate field).

### AM (`/am-queue`, `/am-theme/{id}`)

- **`ThemeSummary` (locked):** `id, name, sector, industry, lifecycle, approval_status, monitoring_status, confidence, key_tickers, stocks_in_industry, why_now` + `provenance` (theme-level, hybrid-aware) + `evidence_provenance: [{source_id, source_type: real|synthetic|human_sourced}]`.
- **`CandidateSummary` (locked):** `id, ticker, research_state, conviction_level, candidate_quality {7 categorical}, entry_readiness {6 fields — verified: price_structure, base_quality, breakout_proximity, volume_behavior, volatility_contraction, extension_risk}, data_confidence {freshness, completeness, reliability, conflicts, missing_data}` + `provenance` (component map: which fields real vs synthetic vs human).
- **`AMQueueResponse` (locked):** `{run_id, point_in_time, themes: [{theme, candidates}]}`.
- **`/am-theme/{id}` (locked):** same `{theme, candidates}` shape as queue item (single theme) — NOT the old flat `ThemeSummary`. 404 on unknown id. (F1)

### FO (envelope + locked flattening)

- **Persisted envelope locked (NF2):** `{run_id, provenance, packages: [...]}` — runner stamps; legacy root-list rejected on real endpoints.
- **Locked flattening map (F1 — documented extraction, no invention):** `sector`/`industry` ← `industry_assessment`; `moat_width/depth/trend` ← `company_assessment.moat`; `earnings_quality` ← `earnings_trajectory.rating`; `conviction` (summary: level string) ← `conviction.level`; `value_trap_verdict` ← derivation rule below. Detail keeps full nested objects. These extractions are exactly what `fo_routes.py:17-71` does today — now documented as the locked contract.
- **`value_trap_verdict` derivation (locked, spec §3.6.2 + test_value_trap.py):** `triggered == true` → artifact `verdict` (vocabulary: `NOT_A_TRAP`/`VALUE_TRAP`/…); `triggered == false` → `"NOT_TRIGGERED"` (display label — check not run). **`/fo-cheap-quality` filter unchanged:** `value_trap_verdict == "NOT_A_TRAP"`.
- **Evidence text fix (F4):** `fundamental-opportunity-v0/pipeline.py:300` gates "Financial data: synthetic fixture" line on `mode == synthetic`.

### II (new `/ii-signals`)

- `IISignalSummary`: `filer_name, filer_cik, filer_category, ticker, filing_quarter, report_date, pct_of_portfolio, conviction, action, change_pct, signal_score, value_usd`.
- `IISignalsResponse`: `{signals, summary, meta}` passthrough + `provenance` — mode must be real (or real-partial `completeness: partial_x_y`). `SYNTHETIC` → 503 (F5).
- **II runner stamps `as_of` explicitly** (NF7/F5) — filing-consistent date, not `generated_at`, used for the 120-day staleness test.

### Dashboard (`/api/dashboard/summary`)

- **Per-component provenance (NF3/NF7):** `{am: {run_id, point_in_time, data_source} | null-if-unadmitted, fo: ..., ii: ..., cs: {run_id: null, point_in_time: null, data_source: "synthetic_demo", source: "backend_static_mock"}}`. Each real component passes mode+freshness admission independently; unadmitted → `null`/`unavailable`.
- **CS counts = exact served mock bytes (SOL-003 fix, verified live):** dashboard derives CS radar items + Q-met from the same `_MOCK_ASSETS` the `/api/cs-radar` endpoint serves. **Frontend `DashboardPage` MUST consume `/api/dashboard/summary` — hardcoded 8/3 removed (NF5, verified regression exists today).**

### CS (`/api/cs-radar`)

- **Unchanged** — mock + `synthetic_demo` (authorized).

## 4. Persistence — SQLite (stdlib `sqlite3`), immutable, content-addressed (F2/NF1/NF6/NF8)

DB: `backend/data/iip.db` + **immutable artifact store** `backend/data/artifacts/<sha256>.json`. **`.gitignore` rule `/backend/data/*.db*` added (F6 — was absent).** WAL, `busy_timeout=5000`, per-operation connections, **`PRAGMA foreign_keys=ON` every connection (NF1)**.

```sql
CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,
    run_id TEXT NOT NULL,              -- artifact run_id, else sha256[:16]
    point_in_time TEXT,
    fixture_category TEXT,             -- provenance verbatim
    artifact_sha256 TEXT NOT NULL,     -- immutable identity; bytes in artifacts/<sha256>.json
    artifact_path TEXT NOT NULL,
    ingested_at TEXT NOT NULL,
    UNIQUE (module, run_id)
);
-- IMMUTABLE: same (module, run_id) + different artifact_sha256 → REJECT (raise)

CREATE TABLE IF NOT EXISTS api_reads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,            -- F2: endpoint IS part of replay key
    route_params TEXT,                 -- JSON (theme_id, company_id, …)
    data_source TEXT NOT NULL,
    response_sha256 TEXT NOT NULL,     -- ASGI capture over exact serialized bytes
    status INTEGER NOT NULL,
    adapter_version TEXT NOT NULL,
    served_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS api_read_runs (   -- NF6: composite lineage (dashboard = AM+FO+II+CS)
    api_read_id INTEGER NOT NULL REFERENCES api_reads(id),
    run_id_fk INTEGER NOT NULL REFERENCES pipeline_runs(id),
    component TEXT NOT NULL,           -- 'am' | 'fo' | 'ii'
    PRIMARY KEY (api_read_id, component)
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);  -- schema_version (init=1, upgrade/reject logic at startup — NF8); active_session_nonce (runtime session value, NOT a secret — F6)
```

**Lineage (F2/NF6):** single-artifact reads → `api_reads` row. Composite reads (dashboard) → `api_reads` row + `api_read_runs` rows per component. Static CS → no `api_read_runs` row; provenance `source: backend_static_mock` documented in the read's `data_source`/params. Replay key = `(endpoint, route_params, adapter_version, artifact_sha256…)`. `adapter_version` bound to an immutable adapter registry constant + code-hash asserted in tests (NF8). **Schema lifecycle (NF8):** startup reads `schema_version` → init if absent (transaction), reject if newer than supported, migrate only via versioned script (none needed at v1).

**Response reconstruction:** served response is deterministically reproducible from `(artifact bytes, adapter_version, endpoint, route_params)`; `response_sha256` (ASGI middleware capturing ordered body chunks, committed after send completes) verifies the exact bytes.

## 5. Auth — single-user, stdlib HMAC session (F6)

1. **Startup guard (fail fast):** refuse to boot if `IIP_AUTH_PASSWORD` unset/empty or `IIP_AUTH_SECRET` <32 chars. No default credentials. **Secrets env-only — never in SQLite settings** (settings holds only `schema_version` + `active_session_nonce` runtime value, not credentials).
2. `POST /api/auth/login` — `{username, password}` → constant-time `hmac.compare_digest` vs env (username default `founder`). Success → nonce (stored in `settings.active_session_nonce`), cookie `iip_session` = `{nonce, issued_at, expires_at} | HMAC-SHA256(secret)`. **Server-side expiry + nonce validation on every request** (copied token rejected after `expires_at`/logout server-side).
3. `POST /api/auth/logout` — **revokes server-side** (clears nonce) + clears cookie.
4. `GET /api/auth/status` — independently verifies cookie signature+nonce+expiry; returns `{authenticated: bool}` only. Exempt, leaks nothing.
5. `require_auth` on ALL `/api/*` except exactly: `/api/health`, `/api/auth/login`, `/api/auth/status` (route-inventory test enforces).
6. **Loopback enforcement:** launch pins `--host 127.0.0.1`; middleware rejects non-loopback `Host` → 403 while `Secure=False`. Cookie: HttpOnly, SameSite=Lax, max_age 12h (advisory — server enforces `expires_at`).
7. **Frontend (NF4):** `credentials: 'include'` on ALL API clients (`amClient`, `foClient`, `csClient`, new `iiClient`, new `authClient`); React Router auth gate + minimal login page; `App.tsx` routes protected; frontend types (`types/am.ts` etc.) updated to the locked contracts; frontend build + browser tests added to charter.
8. Secrets: env vars only (`IIP_AUTH_USER`/`IIP_AUTH_PASSWORD`/`IIP_AUTH_SECRET`), `.env` gitignored, **`.env.example` created in this workstream** (F6 — was absent).

## 6. API wiring map

| Endpoint | Reads | Provenance from |
|---|---|---|
| `/api/am-queue`, `/am-theme/{id}` | AM artifact `queue` (byte snapshot) | `fixture_category` + per-component overlay/evidence labels → `{source, mode, as_of, coverage, completeness, hybrid}`; evidence_provenance (real/synthetic/human) |
| `/api/fo-queue`, `/fo-package/{id}`, `/fo-cheap-quality` | FO artifact envelope `{run_id, provenance, packages}` | envelope `provenance`; value_trap_verdict per §3 locked derivation |
| `/api/ii-signals` (**NEW**) | II artifact | `meta.data_source` — mode must be real; partial preserved; `as_of` stamped by runner |
| `/api/cs-radar` | **unchanged** mock | `synthetic_demo` |
| `/api/dashboard/summary` | per-module latest ADMITTED run + cs mock | per-component provenance; unadmitted → null (NF7) |
| `/api/health` | — | — |

**Runner changes (provenance + atomicity only):** FO `run.py` envelope + atomic write + mode-gated evidence (pipeline.py:300); II `run.py` meta.data_source reflects `--real`, stamps `as_of`, atomic write, partial preserved.

## 7. Real runs (data refresh)

FO: `python3 fundamental-opportunity-v0/run.py --real --json-only` · II: `python3 institutional-intelligence-v0/run.py --real --json-only` · AM: already real (ingest as-is, hybrid preserved). Network reachable (429/403 = UA-limited; repo fetchers set headers).

## 8. Decisions required from Founder

| # | Decision | Recommendation |
|---|---|---|
| D1 | **Persistence:** stdlib `sqlite3` vs FD-literal SQLAlchemy (install into fragile hermes venv) | **A — stdlib sqlite3.** |
| D2 | **Synthetic fallback / wrong-mode serving on real surfaces** — fail closed 503 (admission rule) | **A — fail closed.** |
| D3 | **Staleness bounds** — AM ≤7d, FO ≤30d, II ≤120d (operational freshness, NOT investment rules) | **A — approve bounds.** |
| D4 | **Phase 2R disposition** — 3 rounds all FAIL, findings converged to implementation-level contracts; verify via Phase 4 locked tests + Phase 5 QA + Final Council + production audit instead of a 4th doc round | **A — proceed to Phase 3 with locked-test enforcement.** |

## 9. Locked test charter (F8 + NF4/NF5/NF6/NF7/NF8 — full)

`tests/locked/test_real_data_api.py` + frontend build/browser:
1. **Route inventory:** every `/api/*` route except allowlist → 401 without cookie
2. **Auth:** login ok / wrong password / unset-credentials + weak-secret startup guards / tampered cookie / **expired server-side** / **revoked after logout** / status independent / **non-loopback Host → 403** / **frontend credentialed fetch works (NF4)**
3. **AM:** real artifact fields (no fabricated counts), **per-theme + per-candidate provenance incl. hybrid:true + evidence_provenance (real|synthetic|human_sourced)**, **exact 6-field entry_readiness**, **/am-theme/{id} returns {theme, candidates} shape**, 404
4. **FO:** envelope `{run_id, provenance, packages}` (no re-run), provenance marker, **locked flattening map (every summary field matches extraction rule)**, value_trap_verdict derivation, **legacy root-list → 503**, /fo-package/{id} 404, cheap-quality filter unchanged
5. **II:** /ii-signals 200 shape + meta + partial provenance; **SYNTHETIC → 503; stale (as_of > D3 bound) → 503**
6. **CS:** unchanged synthetic_demo contract
7. **Dashboard (NF5/NF7):** per-component provenance; CS `{null, null, synthetic_demo, backend_static_mock}`; **CS counts == /api/cs-radar collection + Q-met (triple agreement, browser+API)**; **unadmitted/stale component → null (never silent synthetic)**
8. **Persistence (NF1/NF6/NF8):** ingest upsert; same run_id+diff hash → rejected; api_reads + **api_read_runs composite rows**; FK NOT NULL + PRAGMA ON + invalid-FK rejected; response_sha256 matches actual served bytes (ASGI capture); **schema_version init + newer-schema reject**; adapter_version bound to registry code-hash
9. **Fail-closed + stale:** corrupt/missing → 503; wrong-mode (synthetic) → 503; stale → 503; **unknown-mode → 503**
10. **Concurrency:** refresh (`os.replace`) during read → old or new complete artifact, never partial
11. **E2E smoke:** subprocess `python3` produces temp FO envelope → 3.11 FastAPI ingests + serves; artifact store bytes == served provenance
12. **Frontend (NF4/NF5):** `npm run build` exit 0; types match locked contracts; DashboardPage consumes `/api/dashboard/summary` (no hardcoded counts); browser smoke on authenticated pages

## 10. Explicitly NOT in scope (FD #46)

Broker/execution/allocation · new pipeline stages · new investment rules/thresholds/weights/formulas/lookbacks · CS real data · CIW Phase 11 · multi-user/OAuth · external deployment · DB beyond SQLite · changing any score/quality/ranking computation · synthetic fallback on real surfaces · serving wrong-mode artifacts on real endpoints.

## 11. Regression & review disposition

Phase 2R: R1 FAIL (8 findings) → R2 FAIL (3 closed, 6 partial, NF1–NF3) → R3 FAIL (5 closed, 6 partial, NF4–NF8). **Regression budget 2/2 used; escalation round 3 run; Founder timed out → best judgment: v0.4 + verification moved to implementation gates.** Remaining items are implementation-level contracts (frontend DTOs, dashboard UI agreement, composite lineage, DB versioning) — unverifiable in a doc-only review (reviewer's own Evidence Gaps). **D4 presented to Founder at Phase 3 plan gate; a 4th doc round available on Founder request.**

<!-- 2026-08-03 21:20 UTC+7 -->
