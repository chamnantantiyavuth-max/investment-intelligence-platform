# QAD-M5.3 — CORRECTION PASS 3 IMPLEMENTATION STATE (13 Sep 2026)

> **Status:** ✅ **CORRECTION PASS 3 IMPLEMENTED / READY FOR NEW FOUNDER INDEPENDENT RE-AUDIT**
> **NOT CLOSED / NOT FROZEN.** M5.3 remains a HOLD milestone until the NEW
> independent audit returns PASS. FD #139 (13 Sep 2026) is the governing
> authority for this pass.

This document records the CP3 implementation state truthfully, including the
chronology facts that were NOT ideal. It does not rewrite history.

---

## 1. Chronology (as it actually happened — preserved, not rewritten)

| Commit | Content | Kind |
|---|---|---|
| `da47b97` | CP3 diagnostic RED tests F1–F6 + FD #139 registry (on `283a7aa` baseline) | diagnostic commit |
| `d2eb3f4` | **corrected F1 tests + partial F1/F5 runtime committed TOGETHER** | mixed (not ideal) |
| `1c7d472` / `1a87fbe` | CP3 session closeout + cron review docs | docs |
| `fca8b4e` | **TEST-ONLY corrections** for F3 (crash fixture SI-01=SUCCESS authority), R3 (missing-SI-01 initial lifecycle), R6 (RRM retries = count) — BEFORE the F2–F6 runtime | test-only ✅ |
| `7f1580e` | F5 runtime defect fix (74-bit random field) + exact-component tests | runtime+test |
| `9d79f84` | F3 runtime (anchor-before-callback, honest SI-01, crash states A/B/C) | runtime |
| `de4f056` | F2 runtime (deterministic retry identity + terminal reconciliation) | runtime |
| `8d5cfdd` | F4 runtime (RFR-01 exactly-once, same-store atomic) | runtime |
| `d3209db` | F6 runtime (RRM-01.retries = count from RR ledger) | runtime |

**Honest statement (FD #139 §14 / §16):** the FIRST F1 diagnostic-test
correction landed together with the partial F1/F5 runtime in `d2eb3f4`, so the
early CP3 chronology is NOT perfectly test-only-separated. From `fca8b4e`
onward the intended discipline was restored: test-only corrections first
(`fca8b4e`), then runtime clusters committed separately (F5, F3, F2, F4, F6).

**Corrected RED baseline** (recorded at `fca8b4e`):
`pytest tests/qad/m53/test_correction_pass3.py tests/qad/m53/test_retry_kernel.py tests/qad/m53/test_correction_pass2.py -q`
→ **14 failed, 40 passed**. Of the 14: 12 = the expected CP3 F2/F3/F4/F6
diagnostics (runtime not yet fixed); 2 = the corrected R3/R6 expectations
failing against the pre-CP3 runtime (the documented supersession).

## 2. Implementation (FD #139 rulings R1–R6)

### F1 (R1) — RSR-01 / SM-3 APPEND_ONLY_STATE (bounded)
`qad/persistence/immutability.py`: `_RSR01_SM3_LEGAL_TRANSITIONS` +
`_check_rsr01_sm3_transition` wired into `check_immutability` **for RSR-01
ONLY**. IN_PROGRESS→COMPLETE/FAILED/INCOMPLETE legal; IN_PROGRESS→IN_PROGRESS =
versioned retry continuation; terminal states (COMPLETE/FAILED/INCOMPLETE/
SKIPPED) have NO outgoing transitions. **No generic engine** — the generic
APPEND_ONLY_STATE gap for other schemas remains registered as
**`POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER`** (NOT built).

### F2 (R2) — cross-anchor terminal reconciliation
`qad/m53/retry_kernel.py`:
- Terminal RSR (COMPLETE/FAILED) is **never replayed before** retry provenance
  is verified or deterministically reconciled. `retry_count == 0` = valid
  INITIAL terminal, no RR required.
- RR-01 has no stage columns → the **live RR write and F2 reconcile share ONE
  deterministic retry identity** (`_retry_identity`): SHA-256(execution_id |
  checkpoint | `retry-record` | attempt) → UUIDv7 with the REAL persisted
  RSR.started_at epoch-ms timestamp. Same attempt after restart → same
  retry_id. Never a fresh random UUID during recovery.
- Only the mechanically provable MISSING TERMINAL attempt is reconstructed
  (partial-terminal window). Missing INTERMEDIATE history → FAIL CLOSED
  (IntegrityConflict) — fictional history is never synthesized.
- RRM restored via `_restore_rrm_retry_summary` (no comma-ID logic; no write
  churn when already reconciled).
- Adversarial cross-stage test: same invocation_id, two stages — Stage A RRs
  are never counted toward Stage B; B's reconstructed terminal uses B's own
  deterministic identity.

### F3 (R3) — authoritative initial lifecycle
- Initial sequence: preflight RRM → mint stable stage_id/started_at →
  **persist RSR-01 IN_PROGRESS anchor BEFORE the stage callback** → run
  callback → derive ACTUAL outcome → persist immutable SI-01 with that actual
  status (SUCCESS/FAILURE) → **only then** retry processing (RR-01 FK strict).
- The caller-supplied `ServiceInvocation.status` is **never trusted** as the
  outcome (clean success persists SI-01=SUCCESS, not the fixture FAILURE).
- Crash states (by authoritative store SI-01, not the caller object):
  - A: RSR IN_PROGRESS + SI-01 absent → **FAIL CLOSED** (no re-exec, no
    retry#1, no invented outcome, no new stage_id)
  - B: RSR IN_PROGRESS + SI-01 SUCCESS → reconcile RSR→COMPLETE, SUCCEEDED
  - C: RSR IN_PROGRESS + SI-01 FAILURE/TIMEOUT → known failure; retry only if
    policy allows.
- `_load_si01(invocation_id)` reads the authoritative persisted SI-01.

### F4 (R4) — RFR-01 exactly once on SM-3 terminal FAILED
- Deterministic failure_id: execution identity + checkpoint +
  `research-failure` label, ts_ms = real persisted RSR.started_at (corrected
  F5 UUIDv7).
- **Same-store atomicity**: terminal RSR FAILED + RFR-01 committed in ONE
  `stage_store.store_batch` — no avoidable partial window.
- Wired at: deterministic initial failure, retry exhaustion, deterministic
  failure during retry, terminal FAILED replay (idempotent).
- Intermediate retry failure → NO RFR. INCOMPLETE/Budget RFR behavior NOT
  implemented (deferred → `POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE` F8).

### F5 (R5) — deterministic_uuid7 TRUE random field
- `qad/ids.py`: `deterministic_uuid7(seed, *, ts_ms)` — 48-bit timestamp =
  REAL persisted execution-anchor epoch-ms (never hash-derived); **74-bit
  random field = SHA-256(seed) MASKED to exactly 74 bits** (pre-fix kept only
  38 bits via `digest[6:20] >> 74`, zeroing rand_a — defect caught by the new
  exact-component test).
- `tests/qad/test_ids.py`: + exact rand74 reconstruction test + semantic-label
  rand-field test (16 passed).

### F6 (R6) — RRM-01.retries = COUNT summary
- `_write_attempt_and_manifest`: `retries = str(len(authoritative RR-01
  ledger for the invocation) + 1)` recomputed at each atomic batch — never
  comma-separated IDs, never fragile string parsing of prior IDs. Successful
  retries count; a terminal failed retry counts; clean initial success stays
  "0"/None.
- RR-01 remains the authoritative detailed ledger; RRM.failures independent
  terminal-failure provenance preserved.

## 3. Gates / scopes (unchanged)

- **F7** stage ordering, **F8** Budget/INCOMPLETE, **F9** S9 Case Lock,
  **F10** full S8→S7 PIT/AS_OF binding → NOT implemented; remain registered
  under **`POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE`** (must close before
  Production Release / Live Autonomous QAD).
- Generic non-RSR APPEND_ONLY_STATE → **`POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER`**.
- The M5.3 implementation is the **bounded REFERENCE implementation — NOT
  production S8** (Production / Live / M6 / M7 / workforce-cron cutover NOT
  AUTHORIZED).
- M6 branch `docs/m6-gemini-notebook-dr @ a37e92d` remains parked, untouched.
- Parking branch `wip/pre-m53-cp3-local-docs-20260913 @ cab62fc` preserved.

## 4. Green-gate evidence (13 Sep 2026, real runs)

| Suite | Result |
|---|---|
| `tests/qad/m53/test_correction_pass3.py` (CP3 diagnostics) | 23 passed |
| `tests/qad/m53/` | 78 passed |
| `tests/qad/test_ids.py` | 16 passed |
| `tests/qad/` | 498 passed (incl. persistence 292) |
| full `pytest tests/` | **733 passed, 1 failed** — sole failure = locked
  `tests/locked/test_audit_api.py::test_decisions_register_contiguous_and_parsed`
  date literal `"9 Sep 2026"` vs register latest FD #139 `13 Sep 2026`
  (pre-existing locked-test break, OUTSIDE the FD #139 CP3 file boundary —
  locked-test bump requires separate Founder authorization) |
| M4A validator | 173/173 PASS |
| M4B validator | 93/93 PASS |
| authority/isolation regressions | included in full run |

Old `deterministic_uuid7(seed)` callers: none remaining (all use `ts_ms=`).

> NOTE on the locked-test RED: the CP3 review on `main @ 1c7d472` recorded the
> same 1 locked-literal failure with the identical root cause (`9 Sep 2026` vs
> FD #139 `13 Sep 2026`). It is documented history, not a CP3 regression.