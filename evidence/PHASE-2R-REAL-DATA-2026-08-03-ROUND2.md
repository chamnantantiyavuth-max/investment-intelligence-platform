# Phase 2R — Architecture Review, Round 2 (Real-Data Production Path, FD #46)

> Gate: Phase 2R · Date: 2026-08-03 · Reviewer: Sol Medium (gpt-5.6-sol, openai-codex) · Duration: 512s
> Subject: `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.2 · Result: **FAIL** — F3/F7 closed; F1/F2/F4/F5/F6/F8 retained defects + NF1–NF3 new findings → revision to v0.3
> Regression: 2 of 2 used → 3rd round requires Founder escalation

## Verdict (round 2)

Round 2 does not close all eight round-1 findings: F3 and F7 are closed at the architecture level, but F1, F2, F4, F5, F6, and F8 retain material contract, lineage, truth-safety, or authentication defects. Most seriously: synthetic artifacts still permitted on nominally real endpoints, historical served responses not reconstructable, component-level AM provenance undefined, server-enforced session expiry missing.

## Round-1 Finding Status (round 2)

| Finding | Status | Notes |
|---|---|---|
| F1 | partially closed | AM fields verified real; entry_readiness = **6** fields (doc said 5); FO `value_trap` = `{triggered}` only while contract requires verdict string (adapter fabricates); dashboard CS lineage would attest to unserved artifact |
| F2 | partially closed | Content-addressed run IDs + immutable semantics + FK declared; but no immutable artifact bytes stored, response body not reconstructable, response_sha256 has no ASGI capture guarantee |
| F3 | closed | Atomic tmp+os.replace + single byte snapshot + WAL/busy_timeout — race closed at architecture level |
| F4 | partially closed | Canonical object stated; but AM hybrid (10 `_real_eod` overlays + 13 `SRC-SYN`) has no component-level representation; FO pipeline.py:300 hardcodes "synthetic fixture" text; sample provenance `hybrid:false` contradicted artifact |
| F5 | not closed | Admission rule doesn't reject valid-JSON synthetic artifacts; II artifact is SYNTHETIC today; FO/II default runners overwrite production path with synthetic; "stale" undefined |
| F6 | not closed | Auth secret still listed in SQLite settings; cookie max_age is browser-only (no server expiry); loopback guard unspecified; `.gitignore` *.db rule only prospective |
| F7 | closed | D1 correctly flagged as Founder decision |
| F8 | partially closed | Charter omits dashboard lineage, stale/wrong-mode rejection, exact categorical equality, weak-secret/non-loopback tests |

## New Material Findings (round 2)

1. **NF1 — SQLite FK integrity syntactic only:** `run_id_fk` nullable + no `PRAGMA foreign_keys=ON` per connection (SQLite disables by default) → orphan lineage records possible. Fix: FK ON every connection, NOT NULL for successful reads, invalid-FK test.
2. **NF2 — FO provenance envelope undefined:** artifact is a root list; doc claims unchanged shape + stamped provenance simultaneously. Fix: lock persisted envelope `{run_id, provenance, packages}`, reject legacy root lists on real endpoints.
3. **NF3 — Dashboard CS lineage would attest to unserved artifact:** dashboard reads pipeline_runs for CS while /cs-radar serves `_MOCK_ASSETS` (differs from CS artifact). Fix: CS dashboard provenance = `{run_id: null, point_in_time: null, data_source: synthetic_demo, source: backend_static_mock}`.

## Parent verification (2026-08-03)

All round-2 claims re-verified against repo before acceptance: FO `value_trap` = `{triggered}` only ✅; AM entry_readiness = 6 fields ✅; AM hybrid 10× `_real_eod` + 13× `SRC-SYN` ✅; FO pipeline.py:300 synthetic-fixture text ✅; II meta SYNTHETIC ✅; `.gitignore` no *.db rule (only Thumbs.db matched) ✅; FO value-trap vocabulary locked in spec §3.6.2 + test_value_trap.py (`NOT_A_TRAP` etc., `NOT_TRIGGERED` display label for non-flagged).

## Resolution

All findings addressed in `docs/ARCH-REAL-DATA-PRODUCTION.md` v0.3 (tags F1–F8, NF1–NF3). Regression budget 2/2 used → Founder escalation + D1/D2/D3 decisions at Phase 3 plan gate (Section 11).

<!-- 2026-08-03 21:05 UTC+7 -->
