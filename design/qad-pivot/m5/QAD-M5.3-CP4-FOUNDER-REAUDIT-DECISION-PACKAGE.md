# QAD-M5.3 — CP4 FOUNDER INDEPENDENT RE-AUDIT DECISION PACKAGE (READ-ONLY)

> **Status:** ✅ **FOUNDER RULINGS RECORDED (FD #140, 14 Sep 2026)** — D1-A + D2-A SELECTED · F4-R AUTHORIZED · Correction Pass 5 = GO
> **Verdict (Founder independent re-audit):** FAIL / FOUNDER DECISION REQUIRED → NOW RULED · CP5 IMPLEMENTATION AUTHORIZED
> **Rulings:** D1-A (one SI-01 invocation_id per logical stage execution) · D2-A (RRM-01.retries = maximum retry depth observed in the run) · F4-R (every terminal SM-3 FAILED ⟹ exactly one RFR-01)
> **Audited baseline:** origin/main `7238c438df6d1599a69ecc9eabe7c3c934bcb6da` (CP4 implementation state)
> **Current repo state (verified 2026-09-14):** HEAD == origin/main == `dfb642b` (docs-only commit on top of audited baseline) · working tree clean except 1 untracked draft (`docs/ciw-pilot-msft/monitoring/2026-09-14-monitoring-draft.md`)
> **Local regression:** full suite `746 passed / 0 failed` — ACCEPTED as the current local result
> **M5.3:** NOT CLOSED · NOT FROZEN · **M6:** REMAINS PARKED
> **MODE:** READ-ONLY — DO NOT begin CP5 · DO NOT modify runtime/tests/frozen schemas · DO NOT register a new FD yet

---

## 1. Audited baseline and current status

- Audited baseline: `origin/main @ 7238c438...` (M5.3 CP4 implementation state). Verified present in history.
- Current: HEAD == origin/main == `dfb642b` ("docs: cron review 14 Sep — M5.3 CP4 reconciled + independently verified (suite 746/746)") — a docs-only commit on top of the audited code baseline; working tree clean apart from one unrelated untracked monitoring draft.
- Reported full suite `746 passed / 0 failed` accepted as the current local regression result.
- Commit `49cb6ee` (test adaptation) confirmed in history: it changed legacy cross-stage/cross-version tests so later executions deliberately fail their initial attempt to match the already-persisted SI-01 status. **This test adaptation is NOT treated as a resolution of the D1 contract collision.**

## 2. DECISION D1 — SI-01 invocation granularity (contract collision)

Existing accepted RetryKernel semantics: a different stage or case_version under the SAME invocation executes fresh. CP4-1 now requires a pre-existing immutable SI-01 status to match the ACTUAL initial outcome of the fresh execution. Impossible hidden coupling: same invocation_id, Stage A initial = FAILURE (SI-01 immutable = FAILURE), Stage B fresh execution initial = SUCCESS → CP4 FAIL CLOSED because FAILURE != SUCCESS. Two independent stage executions sharing one invocation are forced to have the same initial outcome status — not a defensible invariant.

## 3. D1 options

- **D1-A — ONE SI-01 invocation_id PER LOGICAL STAGE EXECUTION (RECOMMENDED).** New logical execution identity `(case_id, case_version, stage_name)` → new ServiceInvocation / invocation_id. Same invocation_id reused ONLY for restart/retry/replay of that same logical execution. Consequences: SI-01 truthfully = ACTUAL initial outcome; RR-01 cleanly belongs to that invocation's retries; different stage/case-version no longer shares immutable SI status; no new canonical field/schema required; RetryKernel can fail closed BEFORE callback when no RSR chain exists for the requested execution AND that invocation_id already exists as SI-01; old cross-stage same-invocation tests replaced with distinct invocation identities.
- **D1-B — One invocation across stage executions; redefine SI-01.status as broader invocation-level status.** Conflicts with FD #139 R3. NOT recommended.
- **D1-C — One invocation across stages; later stages ignore SI status.** Destroys SI-01 crash authority. NOT recommended.

## 4. Recommendation — D1-A

## 5. DECISION D2 — Exact semantics of RRM-01.retries (semantic collision)

FD #139 R6: RRM-01 = run-level summary; `RRM-01.retries` = retry COUNT summary, conceptual `"0".."3"`. Current CP4 stores the retry count of the CURRENT execution (verified: `qad/m53/retry_kernel.py` writes `retries = str(retry_count)` of the current execution). Stage A retry depth 3 → `"3"`; Stage B depth 1 → overwrite to `"1"`. Not a stable run-level summary.

## 6. D2 options

- **D2-A — RRM-01.retries = MAXIMUM RETRY DEPTH OBSERVED ANYWHERE IN THIS RUN (RECOMMENDED).** No retry → `"0"`; any stage reaches #1 → `"1"`; any stage reaches #3 → `"3"`; later shallower stage → stays `"3"`. Run-level, monotonic, preserves FD #139 conceptual range `"0".."3"`; RR-01 remains the detailed ledger; no schema change. Preferred authority: derive MAX over authoritative `RSR-01.retry_count` for `case_id + case_version` across stage executions in the run — never from stale RRM strings.
- **D2-B — RRM.retries = cumulative TOTAL number of RR records across the run.** Intuitive total but can exceed `"3"` → requires explicit Founder change to the prior conceptual range.
- **D2-C — retry count of the most recent/current execution (current CP4 behavior).** Not meaningfully run-level; can decrease. NOT recommended.

## 7. Recommendation — D2-A

## 8. BOUNDED IMPLEMENTATION FINDING — F4-R (no Founder semantic decision required)

Current CP4-1 conflict path terminalizes `RSR-01 → FAILED` but does NOT create RFR-01 in the same transition. The over-budget resume path (`IN_PROGRESS` + `retry_count > max_retries` → FAILED) must be inspected for the same missing-RFR behavior. FD #139 R4 requires one logical terminal FAILED → exactly one RFR-01. After Founder decides D1/D2, correction must make every terminal FAILED site preserve the RFR invariant, preferably via the existing same-store atomic RSR FAILED + RFR batch. NOT to be implemented now.

## Additional D1 implementation note

`_persist_si01_actual()` currently treats an existing SI as idempotently consistent when STATUS matches only. Under D1-A this path should largely disappear for fresh execution (existing invocation_id + no RSR chain → early fail-closed). If any same-invocation idempotency remains, stable identity fields must also match — not status alone. Final mechanics deferred until the Founder ruling is recorded.

## 9. Files/tests likely affected per option

Canonical model locations (all frozen M4A schemas — NO schema field changes in any option):
- `qad/models/family_i.py` — RR-01 RetryRecord, RRM-01 RunManifestRecord, SI-01 ServiceInvocation
- `qad/models/family_c.py` — RFR-01 ResearchFailureRecord, RSR-01 ResearchStageRecord
- (registry: `qad/models/__init__.py`)

D1-A: `qad/m53/retry_kernel.py` (invocation-identity derivation per logical execution `(case_id, case_version, stage_name)`; new fail-closed branch — SI-01 exists + no RSR chain → typed error before callback; `_persist_si01_actual` / `_persist_si01_actual_closed` strict identity matching) + module docstring (current lines ~30-32 "different stage or case_version under the same invocation executes fresh" rewritten) + `tests/qad/m53/test_retry_kernel.py`, `test_correction_pass2.py`, `test_correction_pass3.py`, `test_correction_pass4.py` (cross-stage/cross-version fixtures move to distinct invocation identities — replaces the `49cb6ee` fail-first-to-match adaptations).
D1-B: `qad/models/family_i.py` SI-01 docstring + `retry_kernel.py` SI readers + `design/qad-pivot/m4a/QAD-M4A-CANONICAL-SCHEMAS.md` contract note — requires FD #139 R3 amendment.
D1-C: `retry_kernel.py` CP4-1 conflict fail-closed path (SI-01 write/check region, `_persist_si01_actual_closed`) + CP4-1 conflict tests (`test_correction_pass4.py`) — contradicts FD #139 R3.

D2-A: `qad/m53/retry_kernel.py` RRM-01.retries write (lines ~926-929) — recompute as MAX authoritative RSR-01.retry_count across stage executions for the run's `(case_id, case_version)`, never from stale RRM strings; retry-summary assertions in `tests/qad/m53/test_retry_kernel.py` / `test_correction_pass4.py` (monotonicity cases). No schema change.
D2-B: same write path as cumulative RR count — requires explicit Founder change to FD #139 R6 conceptual range `"0".."3"`; no schema change.
D2-C: no change (current behavior).

F4-R (post-D1/D2): `qad/m53/retry_kernel.py` — CP4-1 conflict terminal path and over-budget resume path must create exactly one RFR-01 (same-store atomic RSR FAILED + RFR batch); RFR-invariant tests (`test_correction_pass4.py`, `test_retry_kernel.py`). No Founder semantic decision required.

## 10. Explicit statements

```
NO IMPLEMENTATION AUTHORIZED YET
M5.3 REMAINS NOT CLOSED / NOT FROZEN
M6 REMAINS PARKED
```

Next step: Founder rulings on D1 (recommend D1-A) and D2 (recommend D2-A), then F4-R correction scope may be planned. This package is a draft artifact; nothing is committed.

---

## 11. FOUNDER RULINGS RECORDED (FD #140 — 14 Sep 2026)

**FOUNDER SELECTED: D1-A · D2-A · F4-R AUTHORIZED** — Correction Pass 5 = GO.

- **D1-A — ONE SI-01 invocation_id PER LOGICAL STAGE EXECUTION.** Logical stage
  execution identity = `case_id + case_version + stage_name`. A NEW logical
  stage execution requires a NEW ServiceInvocation / invocation_id. The same
  invocation_id may be reused ONLY for restart / retry / replay of that SAME
  logical execution. RetryKernel MUST NOT mint invocation_ids — the caller
  supplies the ServiceInvocation; the kernel VERIFIES the supplied invocation
  is valid for the requested logical stage execution. Persisted execution ↔
  invocation binding carrier = existing RSR-01 `checkpoint_ref`:
  `cp:<case_version>:<stage_id>:<invocation_id>` (implementation encoding, NOT
  a canonical schema change; one bounded parser/helper contract; legacy
  unbound checkpoints = `LEGACY_UNBOUND_EXECUTION` → FAIL CLOSED).
- **D2-A — `RRM-01.retries` = MAXIMUM RETRY DEPTH OBSERVED ANYWHERE IN THE
  AUTHORITATIVE RUN** (range `"0"`..`"3"`; run-level · monotonic · summary
  only; RR-01 remains the detailed ledger). Implementation: RRM-01 is the
  authoritative RUN-LEVEL accumulator; every retry-summary update parses the
  current authoritative `RRM-01.retries` (valid forms after CP5: None / empty
  / `"0"`..`"3"`; anything else FAIL CLOSED) and writes
  `max(existing, current_execution_retry_depth)`. NEVER decrease. F2 terminal
  provenance reconciliation uses the SAME monotonic rule.
- **F4-R — AUTHORIZED bounded correction under the existing R4 invariant.**
  Every terminal SM-3 FAILED must produce exactly ONE RFR-01; audit ALL
  terminal FAILED write sites (SI-conflict terminalization, over-budget
  resume, deterministic initial terminal failure, retry exhaustion,
  deterministic retry terminal failure, any additional FAILED writer found by
  source search), preferring the same-store atomic `RSR FAILED + RFR-01`
  batch via `store_batch`.
- **D. No new canonical schema** (no invocation_id on RSR, no
  stage_name/case_version on SI, frozen schemas untouched; Erratum-002 not
  reopened; F1/F2 not reopened except where D1/D2 mechanics require
  integration).
- **E. F7–F10** remain under `POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE`.
- **F. generic APPEND_ONLY_STATE residual** remains under
  `POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER`.

CP5 diagnostics-first discipline applies (RED before runtime mutation).
GREEN GATE after CP5: CP5/CP4/CP3 diagnostics + all tests/qad/m53/ + IDs +
persistence + complete tests/qad/ + locked + FULL pytest + M4A validator +
M4B validator + authority/isolation regressions + gate-check +
isolation-scan. FULL PYTEST MUST BE GREEN. Final: STOP at
`M5.3 — CORRECTION PASS 5 IMPLEMENTED / READY FOR NEW FOUNDER INDEPENDENT RE-AUDIT`
— NOT CLOSED / NOT FROZEN. No self-audit, no self-close, no M6 touch.

<!-- 2026-09-14 11:37 UTC+7 -->