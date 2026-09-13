# QAD-M5.3 — CORRECTION PASS 4 IMPLEMENTATION STATE (13 Sep 2026)

> **Status:** ✅ **CORRECTION PASS 4 IMPLEMENTED / READY FOR NEW FOUNDER INDEPENDENT RE-AUDIT**
> **NOT CLOSED / NOT FROZEN.** M5.3 remains a HOLD milestone pending the next
> independent re-audit. No production release, no M6/M7, no workforce/cron cutover.

## 1. Verdict being implemented

Independent re-audit verdict (13 Sep 2026), audit baseline `origin/main @ 4fa14cd`:

| Finding | Ruling | Verdict | CP4 disposition |
|---|---|---|---|
| F1 | R1 | PASS | retained unchanged |
| F2 | R2 | PASS | retained unchanged |
| F3 | R3 | FAIL | CP4-1 (SI-01 conflict) + CP4-2 (TIMEOUT) |
| F4 | R4 | FAIL | CP4-3 (replay repairs missing RFR) |
| F5 | R5 | FAIL | CP4-4 (anchor fail-closed) |
| F6 | R6 | FAIL | CP4-5/CP4-6 (execution-scoped count) |

All corrections are BOUNDED under existing FD #139 semantics. No new
investment/system semantics; F7–F10 remain outside CP4.

## 2. Ground truth (verified, not aspirational)

- Diagnostics committed FIRST as RED: `d3094cc` — 10 RED / 2 GREEN
  (contract checks) against the audited runtime; then runtime fixed.
- Test-correction commit `49cb6ee` BEFORE the runtime commit: legacy
  fixtures that pre-stored a FAILURE-default SI-01 request stub before an
  actual-SUCCESS initial execution encoded the pre-CP4 contract
  (silent-accept); CP4-1 makes that fail-closed, so the fixtures were
  aligned to the corrected contract (documented per-test).
- Runtime commit `45671d3`: CP4-1..CP4-6 kernel changes only.
- Locked-suite commit `9cf1810`: CP4-7 mechanical date sync (FD #139).

## 3. CP4 fixes implemented

**CP4-1 — SI-01 conflict FAIL CLOSED (F3).** `_persist_si01_actual`:
- SI-01 absent -> persist actual outcome normally;
- SI-01 present, status EXACTLY consistent -> idempotent no-op;
- SI-01 present, status CONFLICTS -> IntegrityConflict; the RSR anchor is
  terminalized (IN_PROGRESS->FAILED legal) so the contradictory state can
  NEVER later replay as COMPLETE on restart. Immutable SI-01 never
  overwritten, never silently accepted.
Adversarial coverage: pre-stored SUCCESS + actual FAILURE; pre-stored
FAILURE + actual SUCCESS; restart-replay proof (FAILED, never COMPLETE).

**CP4-2 — TIMEOUT is REAL (F3).** Typed `TimeoutError` on the initial
attempt persists `SI-01.status = TIMEOUT` (existing enum value, no new
canonical enum, no string matching). Retry lifecycle proceeds only AFTER
SI TIMEOUT exists. Retry-loop timeouts are retryable (typed).

**CP4-3 — FAILED replay repairs a MISSING RFR (F4).** Terminal FAILED
replay now PERSISTS the reconstructed RFR-01 when absent (previously the
returned record was discarded). Deterministic failure_id -> exactly one
RFR across repeated restarts; callback never re-executed; terminal RSR not
mutated to create the RFR.

**CP4-4 — invalid execution anchor FAIL CLOSED (F5).** `_started_at_to_ms`
raises IntegrityConflict for missing/malformed RSR-01.started_at BEFORE any
UUID creation. No epoch-1970 (ts=0) fallback UUID, no wall-clock
substitution, no hash-derived timestamp. Persisted anchor remains the R5
authority.

**CP4-5/CP4-6 — F6 retry count is EXECUTION-scoped.** RRM-01.retries is
derived from the exact expected DETERMINISTIC retry identities for THIS
execution (policy-allowed attempts) intersected with the authoritative RR
ledger (+1 for the current atomic batch). Sibling-stage retries sharing the
invocation_id have different identities and are NEVER counted. CP4-6
cross-stage test proves: Stage A RR_R1 preserved, Stage B RR_R1 distinct
deterministic id, count "1" (never "2"), F2 reconciliation still scoped.

## 4. Exact test results (13 Sep 2026, real runs)

- CP4 diagnostics: 12/12 (incl. both SI-conflict mismatches, TIMEOUT,
  RFR-repair, anchor fail-closed, scoped count)
- CP3 diagnostics: 23/23
- all `tests/qad/m53/`: 90/90
- `tests/qad/test_ids.py`: 16/16
- complete `tests/qad/`: 510/510
- locked suite: 162/162
- **FULL pytest: 746/746 PASSED — genuinely GREEN (previous full suite had
  733 pass + 1 locked-literal RED; the CP4-7 sync removed that failure and
  CP4 added 13 tests)**
- M4A validator: PASS (173/173) · M4B validator: PASS (93/93)
- authority/isolation regressions: Gate 1–5 + Isolation Scan PASS; Gate 6
  (verification-evidence tag) satisfied by the docs commit message

## 5. Scope integrity

- Authorized files touched: `qad/m53/retry_kernel.py`,
  `tests/qad/m53/test_correction_pass4.py` (new diagnostics),
  `tests/qad/m53/test_correction_pass2.py` + `test_retry_kernel.py`
  (documented fixture alignment), `tests/locked/test_audit_api.py`
  (CP4-7 mechanical date only).
- NOT opened: F7–F10, generic APPEND_ONLY_STATE, Budget Controller,
  S9 case-lock, S8→S7 PIT/AS_OF binding (all stay under
  `POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE` / the persistence
  conformance blocker).
- No canonical schema change; Erratum-002 NOT reopened; F1 and F2
  semantics untouched.

## 6. Blockers / gates (unchanged)

- `POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER` (generic
  non-RSR APPEND_ONLY_STATE) — still open.
- `POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE` (F7–F10) — still open.
- Reference implementation ≠ production S8.
- Production/Live Autonomous QAD / workforce / cron cutover NOT authorized.
- M5.3 NOT closed / NOT frozen / NOT accepted.

## 7. M6 / parking

- `docs/m6-gemini-notebook-dr @ a37e92d` — untouched, parked.
- `wip/pre-m53-cp3-local-docs-20260913 @ cab62fc` — preserved.

Next action (not started here): NEW FOUNDER INDEPENDENT RE-AUDIT of CP4.
<!-- 2026-09-13 23:30 UTC+7 -->