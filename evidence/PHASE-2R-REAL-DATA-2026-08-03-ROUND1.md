# Phase 2R — Architecture Review, Round 1 (Real-Data Production Path, FD #46)

> Gate: Phase 2R · Date: 2026-08-03 · Reviewer: Sol Medium (gpt-5.6-sol, openai-codex) · Duration: 566s
> Subject: `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.1 · Result: **FAIL — 8 material findings** → revision to v0.2 → re-review (round 2)
> Regression: 1 of 2 allowed (task regression budget)

## Verdict (round 1)

The read-don't-re-run direction, split Python environments, and stdlib HMAC are viable foundations for a loopback-only, single-user application. The architecture nevertheless fails Phase 2R because its API mapping cannot satisfy existing contracts without inventing data, its persistence model cannot reconstruct the exact response served, provenance can misrepresent hybrid or partial artifacts as fully real, and the file/session designs permit corruption or replay.

## Material Findings (round 1)

1. **F1 — Artifact-to-API mapping not representable by current contracts.** `backend/schemas/responses.py` requires `driver_count`, evidence counts, four numeric quality scores; the AM theme object has none (candidate quality is categorical/nested). Dashboard has no FO/II run metadata and one global `data_source`. → define and lock revised response schemas from actual artifact fields; per-component provenance.
2. **F2 — Three-table schema lacks FD-required run identity / snapshot / lineage.** FO artifact is a root list with no run metadata; II meta has no run_id. `api_reads` has no FK, response hash, status, adapter version; unique upsert can collapse changed bytes under one run ID. → content-addressed run ID; immutable runs (reject reused run_id with different hash); api_reads FK + route params + response SHA-256 + status + adapter version.
3. **F3 — Cross-interpreter artifact handoff TOCTOU race.** FO/II overwrite production JSON directly; persistence and adapters read separately → registered bytes ≠ served bytes; concurrent refresh can serve partial JSON. → runners write tmp + flush/fsync + os.replace; one immutable byte snapshot per request; per-op SQLite connections + WAL + busy_timeout + transactions.
4. **F4 — Provenance collapses hybrid/partial states into false real_* labels.** AM artifact contains `_real_eod` overlays + synthetic `SRC-SYN-*` evidence; II can produce PARTIAL (x/y); FO marker is generic "REAL EOD". → canonical metadata {source, mode, as_of, coverage, completeness, fixture/hybrid}; preserve II partial; component-level AM provenance.
5. **F5 — Synthetic fallback on real endpoints is unauthorized + dangerous.** AGENTS.md forbids AI-invented fallback; FD #46 names CS as the only synthetic surface. → fail closed 503 + failed artifact metadata; optional serve-last-verified-real-run; synthetic fallback needs separate FD.
6. **F6 — Auth replay + secret-handling gaps.** Stateless signed token + cookie-clear logout = stolen token valid 12h; secret persisted in SQLite; `.db` NOT gitignored. → active session nonce revoked on logout; hmac.compare_digest; password/secret strength guard; loopback binding enforcement; `.gitignore` `/backend/data/*.db*`; /api/auth/status independently verifies cookie.
7. **F7 — stdlib sqlite3 = unapproved contract deviation.** FD #46 text says "SQLite layer (SQLAlchemy)". → named Founder approval (D1) before Phase 3, or use SQLAlchemy.
8. **F8 — Locked-test charter too weak.** Missing route inventory, cookie tamper/replay, unset credentials, same-run/diff-hash, concurrency, partial/hybrid provenance, fail-closed, per-component lineage, E2E subprocess smoke. → expanded 10-point charter.

## Resolution

All 8 findings addressed in `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.2 (tags F1–F8). Round 2 re-review dispatched 2026-08-03 20:45 UTC+7. Decision D1 (stdlib sqlite3 vs SQLAlchemy) + D2 (fail-closed confirmed) presented to Founder at Phase 3 plan gate.

<!-- 2026-08-03 20:50 UTC+7 -->
