# QAD-M5.3 — CORRECTION PASS 5 IMPLEMENTATION STATE (14 Sep 2026)

> **Status:** ✅ **CORRECTION PASS 5 IMPLEMENTED / READY FOR NEW FOUNDER INDEPENDENT RE-AUDIT**
> **NOT CLOSED / NOT FROZEN.** M5.3 remains a HOLD milestone pending the next
> independent re-audit (no self-audit, no self-close). No production release,
> no M6/M7, no workforce/cron cutover. M6 remains PARKED.

## 1. Verdict being implemented

CP4 independent re-audit verdict (14 Sep 2026), audited baseline
`origin/main @ 7238c43` — **FAIL / FOUNDER DECISION REQUIRED** with two
contract collisions (D1 SI-01 invocation granularity, D2 RRM-01.retries
semantics) plus one bounded implementation finding (F4-R). The read-only
decision package was accepted and the Founder ruled (FD #140):

| Decision | Ruling | Disposition |
|---|---|---|
| D1 SI-01 invocation granularity | **D1-A** — ONE SI-01 invocation_id per logical stage execution | Implemented (cluster 3) |
| D2 RRM-01.retries semantics | **D2-A** — maximum retry depth observed in the run | Implemented (cluster 4) |
| F4-R terminal FAILED → RFR | **AUTHORIZED** — exactly one RFR-01 per terminal SM-3 FAILED | Implemented (cluster 5) |

All corrections are BOUNDED under the existing frozen schemas (no new
canonical field — the execution↔invocation binding rides in the existing
RSR-01.checkpoint_ref string encoding). F7–F10 remain under
`POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE`; the generic APPEND_ONLY_STATE
residual remains under
`POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER`. Neither is
implemented by CP5.

## 2. Ground truth (verified, not aspirational)

- State hygiene: HEAD == origin/main == `dfb642b` (docs-only on top of the
  audited CP4 baseline) before CP5; the unrelated untracked monitoring draft
  (`docs/ciw-pilot-msft/monitoring/2026-09-14-monitoring-draft.md`) was
  NEVER staged, committed, or modified (explicit-path staging only; no
  `git add -A`).
- Diagnostics committed FIRST as RED: `bbccc00` — **10 RED / 4 GREEN**
  against the untouched pre-CP5 runtime; truthful record (the 4 GREEN are
  contract guards that already held on CP4).
- Governance: FD #140 registered (`operational/FOUNDERS-DECISIONS.md` item
  140) + decision package APPROVED — commit `49dadc9` (governance-only,
  BEFORE any runtime change).
- Runtime clusters: D1-A `f98d605` · D2-A `32ff683` · F4-R `69f013b`
  (qad/m53/retry_kernel.py).
- Fixture corrections: `3b147d4` (test_retry_kernel, correction passes
  2/3/4 — the 49cb6ee fail-first adaptations REMOVED and replaced by the
  section-7 truthful distinct-invocation matrix).
- Locked authority-date sync: CP4-7 pattern repeated for FD #140
  (`tests/locked/test_audit_api.py` latest-decision date 13→14 Sep 2026).

## 3. CP5 fixes implemented

**D1-A — ONE SI-01 invocation_id PER LOGICAL STAGE EXECUTION (FD #140).**
Logical stage execution identity = case_id + case_version + stage_name; a
NEW logical stage execution requires a NEW ServiceInvocation / invocation_id
(restart/retry/replay of the SAME logical execution reuse it). The kernel
NEVER mints invocation_ids — the caller supplies the ServiceInvocation and
the kernel VERIFIES it. The persisted execution↔invocation binding rides in
the existing RSR-01.checkpoint_ref as the CP5 encoding
`cp:<case_version>:<stage_id>:<invocation_id>` (one bounded parser contract —
`_cp_decode` → `_CpBinding`; no canonical schema change):
- FRESH execution (no RSR chain) + supplied invocation_id already exists as
  SI-01 → **FAIL CLOSED BEFORE any anchor/callback/RR/mutation** (illegal
  reuse, never "reuse because status matches").
- EXISTING execution → `_validate_existing_execution` checks: A binding
  exists · B all chain versions agree · C supplied invocation_id == persisted
  binding · D authoritative SI-01 exists for terminal states · E SI-01 stable
  identity fields (invocation_id/case_id/service_id/request_type/invoked_at)
  agree — any conflict FAILS CLOSED.
- LEGACY_UNBOUND_EXECUTION (pre-CP5 two-field checkpoint) FAILS CLOSED; no
  automatic migration (reference implementation, not production migration).
- `_persist_si01_actual` idempotency now requires the stable identity fields
  to match — not status alone.
- Defensive race handling retained: preflight passes → a conflicting SI-01
  appears before outcome persistence → terminalize FAILED + exactly one RFR
  atomically + raise IntegrityConflict.

**D2-A — RRM-01.retries = MAXIMUM RETRY DEPTH OBSERVED ANYWHERE IN THE RUN
(FD #140).** RRM-01 is the authoritative run-level accumulator (the schema
does not place manifest_id on RSR-01, so no RSR→manifest scan):
- `_parse_run_retry_summary`: valid CP5 forms None/empty → 0, "0".."3";
  anything else → **FAIL CLOSED** (never silently overwritten).
- `_merge_run_retry_summary` = max(existing, current_execution_depth) —
  monotonic, never decreases.
- `_write_attempt_and_manifest` (live writer) and
  `_restore_rrm_retry_summary` (F2 reconciliation) both use the SAME rule:
  F2 reconcile of a shallower stage can never lower an existing "3".

**F4-R — every terminal SM-3 FAILED produces exactly ONE RFR-01 (FD #140).**
Full source audit of all `ResearchStageRecordStage_state.FAILED` write
sites: A SI-conflict terminalization and B over-budget resume were MISSING
the RFR — both now terminalize atomically with exactly one RFR-01 via
`_ensure_rfr` + same-store `store_batch` (RSR FAILED + RFR); C deterministic
initial terminal failure, D retry exhaustion, E deterministic retry terminal
failure were already atomic (kept); F replay repair of an already-FAILED RSR
repairs a missing RFR without rewriting the RSR (kept, CP4-3).

## 4. Gate evidence (exact counts from real runs, 14 Sep 2026)

| Gate | Count | Status |
|---|---|---|
| CP5 diagnostics (tests/qad/m53/test_correction_pass5.py) | 14/14 | ✅ PASS (RED record 10/4 pre-CP5) |
| CP4 diagnostics (test_correction_pass4.py) | 12/12 | ✅ PASS |
| CP3 diagnostics (test_correction_pass3.py) | 23/23 | ✅ PASS |
| tests/qad/m53/ (all) | 108/108 | ✅ PASS |
| tests/qad/ (complete) | 528/528 | ✅ PASS |
| tests/locked | 162/162 | ✅ PASS |
| **FULL pytest** | **764/764** | ✅ PASS (CP4 baseline 746/746) |
| M4A validator (validate-m4a-contracts.py) | — | ✅ PASS |
| M4B validator (validate-m4b-pack.py) | — | ✅ PASS |
| gate-check.sh | Gate 6 tag in final commit | ✅ PASS |
| isolation-scan.sh | 0 violations | ✅ PASS (pending final run) |

## 5. Explicit statements

```
M5.3 — CORRECTION PASS 5 IMPLEMENTED / READY FOR NEW FOUNDER INDEPENDENT RE-AUDIT
M5.3 REMAINS NOT CLOSED / NOT FROZEN
M6 REMAINS PARKED
F7–F10 GATE UNCHANGED (POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE)
GENERIC APPEND_ONLY_STATE BLOCKER UNCHANGED (POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER)
```

No self-audit, no self-close performed. A new Founder independent re-audit
is mandatory before any further step.

<!-- 2026-09-14 11:37 UTC+7 -->