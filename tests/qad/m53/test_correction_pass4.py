"""M5.3 CORRECTION PASS 4 — diagnostic contract tests (bounded re-audit fixes).

Founder independent re-audit verdict (13 Sep 2026): F1/F2 PASS, F3/F4/F5/F6
FAIL (bounded).  These tests are diagnostic-first: they encode the EXACT
bounded findings CP4-1..CP4-6 and MUST be RED against the audited
`4fa14cd` runtime baseline, GREEN only after the CP4 fixes.

Coverage:
- CP4-1 — pre-existing SI-01 must NEVER silently override the ACTUAL
  initial outcome (F3): pre-stored SUCCESS + actual retryable FAILURE, and
  pre-stored FAILURE + actual SUCCESS, both FAIL CLOSED; the contradictory
  state must never replay as COMPLETE on restart.
- CP4-2 — TIMEOUT status must be REAL (F3): a typed timeout initial outcome
  persists SI-01.status = TIMEOUT, then retry proceeds under policy; no
  string-matching classification.
- CP4-3 — FAILED terminal replay actually repairs a MISSING RFR-01 (F4):
  RSR FAILED + provenance present + NO RFR -> exactly one deterministic RFR
  persisted on FIRST restart; second restart still exactly one; callback
  never re-executed.
- CP4-4 — invalid execution anchor FAILS CLOSED (F5): missing/malformed
  RSR-01.started_at raises a deterministic typed error BEFORE any UUID
  creation; no epoch-1970 (ts=0) UUID is ever generated as a fallback.
- CP4-5/CP4-6 — F6 retry-count summary is EXECUTION-scoped (F6): the count
  for the current execution is derived from the expected deterministic
  retry identities intersected with the authoritative RR ledger — sibling
  stage retries sharing the invocation_id are NEVER counted.

CP4-7 (locked full-suite date literal) and CP4-8 (docstring truth) are
tracked in the locked audit test + forward-looking docs respectively.

These tests do NOT open F7–F10 and do NOT touch canonical schemas.
"""
from __future__ import annotations

import pytest

from qad.ids import deterministic_uuid7, is_uuid7
from qad.m53.retry_kernel import (
    _ExecState,
    _started_at_to_ms,
    ExecutionContext,
    RetryableError,
    RetryKernel,
    RetryPolicy,
)
from qad.models.family_c import (
    ResearchFailureRecord,
    ResearchFailureRecordFailure_type,
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import (
    RetryRecord,
    RetryRecordStatus,
    ServiceInvocationStatus,
)
from qad.persistence import IntegrityConflict

from tests.qad.m53.test_retry_kernel import (
    CASE_ID,
    FIXED_NOW,
    STAGE_NAME,
    _attempts,
    _kernel,
    _make_invocation,
    _seed_case,
)
from tests.qad.m53.test_correction_pass3 import _seed_running_manifest

COMPLETE = ResearchStageRecordStage_state.COMPLETE
FAILED_ST = ResearchStageRecordStage_state.FAILED
IN_PROGRESS = ResearchStageRecordStage_state.IN_PROGRESS

TEMPORAL_STAGE_NAME = ResearchStageRecordStage_name.INITIAL_ANALYSIS


def _rsr(stage_store, *, stage_id=None, state=FAILED_ST, retry_count=0,
         failure_reason=None, started_at=FIXED_NOW):
    sid = stage_id or f"00000000-0000-7000-8000-{0xB00:012x}"
    return ResearchStageRecord(
        stage_id=sid, case_id=CASE_ID, stage_name=STAGE_NAME,
        stage_state=state, started_at=started_at, completed_at=started_at,
        responsible_role="S8", checkpoint_ref=f"cp:1.0:{sid}",
        output_ids=[], retry_count=retry_count, failure_reason=failure_reason,
    )


def _expected_retry_id(kernel, *, stage_id, retry_count, attempt,
                       started_at=FIXED_NOW):
    """The deterministic RR retry_id the kernel would derive live."""
    st = _ExecState(
        stage_id=stage_id, started_at=started_at, completed_at=started_at,
        checkpoint_ref=f"cp:1.0:{stage_id}", previous_outputs=[],
        retry_count=retry_count,
    )
    ex = ExecutionContext(case_id=CASE_ID, case_version="1.0",
                          stage_name=STAGE_NAME)
    return kernel._retry_identity(ex, st, attempt)


# =====================================================================
# CP4-1 — pre-existing SI-01 cannot silently override actual outcome
# =====================================================================

class TestCp41Si01ConflictFailClosed:
    """FD #139 R3: SI-01 is the authoritative ACTUAL INITIAL OUTCOME.

    A pre-existing caller/request SI record must never silently override an
    outcome established by execution.  Consistent pre-existing record ->
    idempotent no-op; CONFLICTING pre-existing record -> FAIL CLOSED.
    """

    def test_cp41_prestored_success_actual_retryable_failure_fails_closed(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        # Pre-existing requester SI-01 claims SUCCESS (contradicts reality).
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError("actual transient failure")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        # The actual outcome (FAILURE) must NEVER be rewritten onto the
        # immutable pre-existing SUCCESS record.
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.SUCCESS
        # No retry may begin from a contradictory state.
        assert _attempts(store, inv.invocation_id) == []
        # The RSR chain must NOT stay in a valid retry state (IN_PROGRESS) —
        # terminal FAILED is recorded so restart can NOT replay COMPLETE.
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is FAILED_ST

    def test_cp41_prestored_failure_actual_success_fails_closed(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1  # actual call SUCCEEDS

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.FAILURE  # untouched
        # RSR must NOT become COMPLETE while authoritative SI remains FAILURE.
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is FAILED_ST

    def test_cp41_contradictory_state_never_replays_complete(self):
        """Critical crash-replay check: after the CP4-1 fail-closed, a NEW
        kernel must replay FAILED (or fail), never COMPLETE."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError("actual transient failure")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)

        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        outcome = kernel2.execute(inv, STAGE_NAME, stage,
                                  manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.FAILED, \
            "contradictory state must replay FAILED, never COMPLETE"
        assert calls["n"] == 1  # stage never re-executed


# =====================================================================
# CP4-2 — TIMEOUT status must be real
# =====================================================================

class TestCp42TimeoutIsReal:
    """FD #139 R3: SUCCESS / FAILURE / TIMEOUT according to actual failure
    class.  A typed timeout (builtin TimeoutError) must persist
    SI-01.status = TIMEOUT on the INITIAL outcome — not FAILURE — and the
    retry lifecycle proceeds AFTER the SI TIMEOUT exists."""

    def test_cp42_initial_timeout_persists_si01_timeout(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise TimeoutError("upstream timed out")
            # retry #1 succeeds

        outcome = kernel.execute(inv, STAGE_NAME, stage,
                                 manifest_id=manifest.manifest_id)
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.TIMEOUT, \
            f"initial timeout must persist TIMEOUT, got {si01.status!r}"
        assert "timed out" in str(si01.error or "")
        # Retry lifecycle proceeded AFTER the SI TIMEOUT existed.
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        assert calls["n"] == 2
        assert len(_attempts(store, inv.invocation_id)) == 1

    def test_cp42_timeout_exhaustion_retries_then_terminal_failed(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise TimeoutError("always timing out")

        outcome = kernel.execute(inv, STAGE_NAME, stage,
                                 manifest_id=manifest.manifest_id)
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.TIMEOUT
        assert outcome.status is RetryRecordStatus.FAILED
        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 3  # retries 1..3 all ran after SI TIMEOUT
        assert rrs[-1].status is RetryRecordStatus.FAILED


# =====================================================================
# CP4-3 — FAILED replay must actually repair a missing RFR
# =====================================================================

class TestCp43FailedReplayRepairsMissingRfr:
    """FD #139 R4: terminal FAILED + missing RFR -> deterministic repair on
    the FIRST restart/replay; no duplicate on the second; no callback."""

    def test_cp43_replay_persists_missing_rfr_exactly_once(self):
        kernel, store, stage_store = _kernel()
        _seed_case(stage_store)
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        stage_id = f"00000000-0000-7000-8000-{0xB01:012x}"
        # Authoritative terminal FAILED RSR (rc=1) with its RR + RRM fully
        # present — but NO RFR (the crash window F4 must repair).
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        rid = _expected_retry_id(kernel, stage_id=stage_id, retry_count=1,
                                 attempt=1)
        store.store(RetryRecord(
            retry_id=rid, invocation_id=inv.invocation_id, attempt_number="1",
            attempted_at=FIXED_NOW, status=RetryRecordStatus.FAILED,
            error="boom", escalated_to=None,
        ))
        store.store(manifest.model_copy(
            update={"retries": "1", "failures": [rid]}))
        stage_store.store(_rsr(stage_store, stage_id=stage_id, state=FAILED_ST,
                               retry_count=1, failure_reason="boom"))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        def rfrs():
            return [r for r in stage_store.list_all("RFR-01")
                    if r.case_id == CASE_ID and r.stage_name == STAGE_NAME.value]

        assert rfrs() == []  # the missing-RFR crash state

        outcome = kernel.execute(inv, STAGE_NAME, stage,
                                 manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.FAILED
        assert calls["n"] == 0  # callback never re-executed
        after = rfrs()
        assert len(after) == 1, f"exactly one RFR expected, got {len(after)}"
        assert is_uuid7(after[0].failure_id)
        assert after[0].failure_type is ResearchFailureRecordFailure_type.RETRY_LIMIT

        # Second restart: still exactly one (deterministic, no duplicate).
        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert len(rfrs()) == 1
        assert calls["n"] == 0


# =====================================================================
# CP4-4 — invalid execution anchor must fail closed
# =====================================================================

class TestCp44MalformedAnchorFailsClosed:
    """FD #139 R5: RSR-01.started_at is the required anchor authority.
    Missing/malformed -> deterministic typed error BEFORE any UUID creation.
    Never ts=0 epoch-1970 UUID, never wall-clock substitution."""

    def test_cp44_valid_anchor_exact_epoch_ms(self):
        import datetime as _dt
        expected = int(_dt.datetime(2026, 9, 8, 10, 0, 0,
                                    tzinfo=_dt.timezone.utc).timestamp()) * 1000
        ms = _started_at_to_ms("2026-09-08T10:00:00Z")
        assert ms == expected, f"unexpected epoch-ms {ms} (expected {expected})"

    def test_cp44_missing_anchor_fails_closed(self):
        with pytest.raises(IntegrityConflict):
            _started_at_to_ms(None)
        with pytest.raises(IntegrityConflict):
            _started_at_to_ms("")

    def test_cp44_malformed_anchor_fails_closed_before_uuid(self):
        with pytest.raises(IntegrityConflict):
            _started_at_to_ms("not-a-timestamp")
        with pytest.raises(IntegrityConflict):
            _started_at_to_ms("2026-13-99T99:99:99Z")

    def test_cp44_kernel_resume_malformed_anchor_no_rsr_advance(self):
        """A corrupted RSR.started_at on resume must fail closed BEFORE the
        stage runs — no retry, no UUID with ts=0."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        stage_store.store(_rsr(stage_store, state=IN_PROGRESS, retry_count=0,
                               started_at="garbage-anchor"))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 0  # fail closed BEFORE callback
        assert _attempts(store, inv.invocation_id) == []  # no RR / no ts=0 UUID


# =====================================================================
# CP4-5 / CP4-6 — F6 retry count must be EXECUTION-scoped
# =====================================================================

class TestCp46ExecutionScopedRetryCount:
    """FD #139 R6: RRM-01.retries reflects the count of THIS execution's
    retry records (derived from the exact deterministic retry identities),
    NEVER the invocation-wide RR ledger (sibling stages sharing the
    invocation_id are not counted and never deleted)."""

    def test_cp46_sibling_stage_rr_not_counted_in_f6_summary(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        # Stage A: initial retryable fail, retry#1 succeeds.
        calls_a = {"n": 0}

        def stage_a(ctx):
            calls_a["n"] += 1
            if calls_a["n"] == 1:
                raise RetryableError("A transient")

        outcome_a = kernel.execute(inv, STAGE_NAME, stage_a,
                                   manifest_id=manifest.manifest_id)
        assert outcome_a.status is RetryRecordStatus.SUCCEEDED
        all_rr_a = _attempts(store, inv.invocation_id)
        assert len(all_rr_a) == 1  # RR_A1 exists

        # Stage B — SAME invocation_id, DIFFERENT stage identity: initial
        # retryable fail, retry#1 succeeds.
        calls_b = {"n": 0}

        def stage_b(ctx):
            calls_b["n"] += 1
            if calls_b["n"] == 1:
                raise RetryableError("B transient")

        outcome_b = kernel.execute(inv, TEMPORAL_STAGE_NAME, stage_b,
                                   manifest_id=manifest.manifest_id)
        assert outcome_b.status is RetryRecordStatus.SUCCEEDED
        all_rr = _attempts(store, inv.invocation_id)
        assert len(all_rr) == 2  # RR_A1 + RR_B1 both intact (nothing deleted)

        # The F6 summary is the CURRENT execution's count — ONE retry for
        # Stage B — NOT "2" merely because Stage A has an RR under the same
        # invocation.
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "1", \
            f"execution-scoped retry count expected '1', got {m.retries!r}"

        # Distinct deterministic identities; sibling record untouched.
        rr_b = [r for r in all_rr
                if str(r.attempt_number) == "1"
                and r.retry_id != all_rr_a[0].retry_id]
        assert len(rr_b) == 1
        assert rr_b[0].status is RetryRecordStatus.SUCCEEDED
        assert rr_b[0].retry_id != all_rr_a[0].retry_id
        assert all_rr_a[0].status is RetryRecordStatus.SUCCEEDED

        # F2 (replay) still scopes by execution identity — Stage B replay
        # must NOT reconstruct Stage A's record and must NOT duplicate B's.
        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        kernel2.execute(inv, TEMPORAL_STAGE_NAME, stage_b,
                        manifest_id=manifest.manifest_id)
        after = _attempts(store, inv.invocation_id)
        assert len(after) == 2
        assert {r.retry_id for r in after} == {r.retry_id for r in all_rr}


# =====================================================================
# CP4-5 direct — derive count ONLY from expected deterministic ids
# =====================================================================

class TestCp45CountDerivedFromExpectedIdentities:
    def test_cp45_expected_retry_ids_are_deterministic_and_disjoint(self):
        kernel, store, stage_store = _kernel()
        stage_id = f"00000000-0000-7000-8000-{0xB02:012x}"
        ids = {
            _expected_retry_id(kernel, stage_id=stage_id, retry_count=0,
                               attempt=n)
            for n in (1, 2, 3)
        }
        assert len(ids) == 3  # distinct per attempt
        ids_b = set(
            _expected_retry_id(kernel, stage_id=stage_id, retry_count=0,
                               attempt=n)
            for n in (1,)
        )
        # A sibling stage (different stage identity) with the same case ids
        # MUST derive disjoint identities — the mechanism that keeps the
        # count execution-scoped without canonical fields.
        id_stage_b = _expected_retry_id(
            kernel, stage_id=f"00000000-0000-7000-8000-{0xB03:012x}",
            retry_count=0, attempt=1,
        )
        assert id_stage_b not in ids_b