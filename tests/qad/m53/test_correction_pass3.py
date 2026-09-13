"""M5.3 CORRECTION PASS 3 — diagnostic contract tests (FD #139, GO 13 Sep 2026).

Founder independent review of the Correction Pass 3 Decision Package +
Addendum confirmed F1–F6 and issued the CP3 GO with rulings R1–R6.  These
tests are diagnostic-first (ruling §11): they are expected RED against the
untouched `283a7aa` functional baseline, and GREEN only after the CP3 runtime
fixes.

Coverage (FD #139 rulings):
- F1 (R1) — RSR-01/SM-3 APPEND_ONLY_STATE transition enforcement (bounded):
  IN_PROGRESS→COMPLETE/FAILED/INCOMPLETE legal; FAILED→COMPLETE, COMPLETE→
  FAILED, INCOMPLETE→COMPLETE ILLEGAL; generic residual registered as
  POST_M5.3_PRE_PRODUCTION_PERSISTENCE_CONFORMANCE_BLOCKER (NOT built here).
- F2 (R2) — cross-anchor partial-terminal recovery: RSR terminal persists,
  RR/RRM batch fails, restart -> deterministic reconcile (preserve attempt
  numbering, no duplicate RR, restore RRM summary) BEFORE terminal replay.
- F3 (R3) — honest SI-01: RSR-01 IN_PROGRESS anchor persisted BEFORE the
  initial stage callback; SI-01 written AFTER the initial outcome with the
  ACTUAL immutable status (SUCCESS/FAILURE/TIMEOUT); RR-01 only after SI-01.
  Crash rule: RSR IN_PROGRESS + SI-01 absent + restart -> FAIL CLOSED (never
  silently new-initial / SUCCESS / FAILURE / retry#1).
- F4 (R4) — RFR-01 created exactly once on SM-3 terminal FAILED (deterministic
  idempotent failure_id; no duplicate on restart; intermediate retry failure
  creates NO terminal RFR; retry exhaustion DOES; deterministic initial
  terminal failure DOES).
- F5 (R5) — deterministic_uuid7 timestamp = REAL unix epoch ms from the
  persisted RSR-01.started_at execution anchor (not hash-derived); rand = 
  deterministic cryptographic derivation from execution identity + semantic
  label; same execution+label -> same UUID; distinct labels -> distinct UUIDs;
  version=7 + RFC variant; stable across retry/restart.
- F6 (R6) — RRM-01.retries = retry COUNT summary ("0".."3"), NOT comma-
  separated RR IDs; RR-01 remains the authoritative per-retry ledger.

These tests do NOT implement F7–F10 (stage ordering / budget INCOMPLETE /
S9 case-lock / S8->S7 PIT-AS_OF binding) — those are registered under
POST_M5.3_PRE_PRODUCTION_S8_INTEGRATION_GATE per FD #139.
"""
from __future__ import annotations

import datetime as _dt
import uuid

import pytest

from qad.ids import deterministic_uuid7, is_uuid7
from qad.m53.retry_kernel import (
    RetryableError,
    RetryKernel,
    RetryPolicy,
    StageContext,
)
from qad.models.family_c import (
    ResearchFailureRecord,
    ResearchFailureRecordFailure_type,
    ResearchFailureRecordResolution,
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import (
    RetryRecordStatus,
    ServiceInvocationStatus,
)
from qad.persistence import ImmutabilityViolation, IntegrityConflict
from qad.persistence.errors import TransactionFailure

from tests.qad.m53.test_retry_kernel import (
    CASE_ID,
    FIXED_NOW,
    STAGE_NAME,
    _attempts,
    _kernel,
    _make_invocation,
    _make_manifest,
    _seed_case,
)

COMPLETE = ResearchStageRecordStage_state.COMPLETE
FAILED_ST = ResearchStageRecordStage_state.FAILED
IN_PROGRESS = ResearchStageRecordStage_state.IN_PROGRESS
INCOMPLETE = ResearchStageRecordStage_state.INCOMPLETE


def _anchor_ts_ms(started_at: str) -> int:
    """Real epoch-ms for the RSR-01.started_at RFC3339 second-precision value."""
    dt = _dt.datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    return int(dt.timestamp()) * 1000


def _seed_running_manifest(store, *, case_version="1.0"):
    m = _make_manifest(case_version=case_version)
    store.store(m)
    return m


def _rsr(stage_store, *, stage_id=None, state=IN_PROGRESS, retry_count=0,
         failure_reason=None):
    sid = stage_id or f"00000000-0000-7000-8000-{0xA00:012x}"
    return ResearchStageRecord(
        stage_id=sid, case_id=CASE_ID, stage_name=STAGE_NAME,
        stage_state=state, started_at=FIXED_NOW, completed_at=FIXED_NOW,
        responsible_role="S8", checkpoint_ref=f"cp:1.0:{sid}",
        output_ids=[], retry_count=retry_count, failure_reason=failure_reason,
    )


def _stored_stage_id(stage_store) -> str:
    """Single current RSR-01 stage_id in the stage anchor (F1 direct-store
    transition tests MUST re-store the SAME stage_id to exercise a state
    transition rather than an insert)."""
    rsrs = [r for r in stage_store.list_all("RSR-01")
            if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
    assert rsrs, "no RSR-01 record stored"
    return rsrs[-1].stage_id


# =====================================================================
# F1 (R1) — RSR-01 / SM-3 APPEND_ONLY_STATE transition enforcement
# =====================================================================

class TestF1RsrSm3Transitions:
    """Direct canonical-store test: illegal RSR-01 stage_state transitions
    must be REJECTED at the persistence layer (SM-3 ILLEGAL list)."""

    def test_f1_failed_to_complete_rejected(self):
        store = _kernel()[2]
        _seed_case(store)
        store.store(_rsr(store, stage_id=None, state=FAILED_ST))
        sid = _stored_stage_id(store)
        with pytest.raises((ImmutabilityViolation, TransactionFailure)):
            store.store(_rsr(store, stage_id=sid, state=COMPLETE))

    def test_f1_complete_to_failed_rejected(self):
        store = _kernel()[2]
        _seed_case(store)
        store.store(_rsr(store, stage_id=None, state=COMPLETE))
        sid = _stored_stage_id(store)
        with pytest.raises((ImmutabilityViolation, TransactionFailure)):
            store.store(_rsr(store, stage_id=sid, state=FAILED_ST))

    def test_f1_incomplete_to_complete_rejected(self):
        store = _kernel()[2]
        _seed_case(store)
        store.store(_rsr(store, stage_id=None, state=INCOMPLETE))
        sid = _stored_stage_id(store)
        with pytest.raises((ImmutabilityViolation, TransactionFailure)):
            store.store(_rsr(store, stage_id=sid, state=COMPLETE))

    def test_f1_inprogress_to_complete_legal(self):
        store = _kernel()[2]
        _seed_case(store)
        store.store(_rsr(store, stage_id=None, state=IN_PROGRESS))
        sid = _stored_stage_id(store)
        # Same stage_id, IN_PROGRESS -> COMPLETE: legal forward transition.
        store.store(_rsr(store, stage_id=sid, state=COMPLETE))
        assert store.load("RSR-01", sid).stage_state is COMPLETE

    def test_f1_inprogress_to_failed_legal(self):
        store = _kernel()[2]
        _seed_case(store)
        store.store(_rsr(store, stage_id=None, state=IN_PROGRESS))
        sid = _stored_stage_id(store)
        store.store(_rsr(store, stage_id=sid, state=FAILED_ST))
        assert store.load("RSR-01", sid).stage_state is FAILED_ST


# =====================================================================
# F2 (R2) — cross-anchor partial-terminal recovery
# =====================================================================

class TestF2CrossAnchorReconcile:
    """RSR terminal write survives but the RR/RRM batch fails -> restart must
    reconcile deterministically BEFORE replaying the terminal outcome."""

    def test_f2_retry_success_batch_failure_reconciles(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient initial")
            if calls["n"] == 2:
                raise RetryableError("transient retry1")

        # Fault injection: fail ONLY the RR/RRM batch for the terminal
        # (SUCCEEDED) attempt — RSR COMPLETE is written BEFORE the batch.
        orig_batch = store.store_batch

        def bad_batch(instances, /):
            if any(getattr(i, "status", None) is RetryRecordStatus.SUCCEEDED
                   for i in instances):
                raise TransactionFailure("injected RR/RRM batch failure")
            return orig_batch(instances)

        store.store_batch = bad_batch
        try:
            with pytest.raises(TransactionFailure):
                kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        finally:
            store.store_batch = orig_batch

        # RSR is terminal COMPLETE but RR/RRM provenance is partial.
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is COMPLETE
        assert len(_attempts(store, inv.invocation_id)) == 1  # only retry#1 landed

        # Restart: new kernel over the SAME stores -> reconcile -> complete chain.
        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        outcome = kernel2.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        rrs = _attempts(store, inv.invocation_id)
        assert [r.attempt_number for r in rrs] == ["1", "2"]  # attempt numbers preserved
        assert rrs[-1].status is RetryRecordStatus.SUCCEEDED
        # No duplicate RR records after repeated restart/reconcile.
        kernel2.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert len(_attempts(store, inv.invocation_id)) == 2
        # RRM summary restored (retry count summary per F6).
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "2"

    def test_f2_terminal_failure_batch_failure_reconciles(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        orig_batch = store.store_batch

        def bad_batch(instances, /):
            if any(getattr(i, "status", None) is RetryRecordStatus.FAILED
                   for i in instances):
                raise TransactionFailure("injected RR/RRM batch failure")
            return orig_batch(instances)

        store.store_batch = bad_batch
        try:
            with pytest.raises(TransactionFailure):
                kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        finally:
            store.store_batch = orig_batch

        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is FAILED_ST

        # Restart -> reconcile terminal FAILED provenance chain.
        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        outcome = kernel2.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.FAILED
        rrs = _attempts(store, inv.invocation_id)
        assert rrs[-1].attempt_number == "3"
        assert rrs[-1].status is RetryRecordStatus.FAILED
        assert len({r.retry_id for r in rrs}) == len(rrs)  # no duplicates
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "3"

    def test_f2_cross_stage_rr_never_scoped_by_invocation_alone(self):
        """Same invocation_id across TWO stages (CP3 F2 §10 adversarial):

        Stage A (SOURCE_FOUNDATION) leaves retry history under the
        invocation.  Stage B (INITIAL_ANALYSIS) — a DIFFERENT stage identity,
        SAME invocation/case_version — goes terminal FAILED with its own
        terminal RR batch injected-failed.

        F2 MUST NOT:
          * count Stage A's RR toward Stage B's provenance,
          * declare Stage B complete because the invocation-wide RR count
            happens to match,
          * reconstruct Stage B's RR using Stage A's execution identity.

        Only Stage B's missing terminal attempt is rebuilt, with Stage B's
        OWN deterministic retry identity.  Stage A's RR is untouched.
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)

        # --- Stage A (SOURCE_FOUNDATION): initial retryable-fail, retry#1
        #     succeeds -> RR_A attempt-1 SUCCEEDED under the invocation. ---
        calls_a = {"n": 0}

        def stage_a(ctx):
            calls_a["n"] += 1
            if calls_a["n"] == 1:
                raise RetryableError("A transient initial")

        kernel.execute(inv, STAGE_NAME, stage_a, manifest_id=manifest.manifest_id)
        rsr_a = [r for r in stage_store.list_all("RSR-01")
                 if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsr_a[-1].stage_state is COMPLETE
        rr_a = _attempts(store, inv.invocation_id)
        assert len(rr_a) == 1 and rr_a[0].attempt_number == "1"
        assert rr_a[0].status is RetryRecordStatus.SUCCEEDED
        rr_a_id = rr_a[0].retry_id

        # --- Stage B (INITIAL_ANALYSIS): always retryable-fails; the terminal
        #     (attempt 3) RR/RRM batch is injected to fail AFTER RSR_B FAILED
        #     is already terminal.  RSR_B retry_count = 3. ---
        stage_b = ResearchStageRecordStage_name.INITIAL_ANALYSIS
        calls_b = {"n": 0}

        def stage_b_fn(ctx):
            calls_b["n"] += 1
            raise RetryableError(f"B boom {calls_b['n']}")

        orig_batch = store.store_batch

        def bad_batch(instances, /):
            if any(getattr(i, "status", None) is RetryRecordStatus.FAILED
                   for i in instances):
                raise TransactionFailure("injected B terminal batch failure")
            return orig_batch(instances)

        store.store_batch = bad_batch
        try:
            with pytest.raises(TransactionFailure):
                kernel.execute(inv, stage_b, stage_b_fn,
                               manifest_id=manifest.manifest_id)
        finally:
            store.store_batch = orig_batch

        rsr_b = [r for r in stage_store.list_all("RSR-01")
                 if r.case_id == CASE_ID and r.stage_name == stage_b]
        assert rsr_b[-1].stage_state is FAILED_ST
        assert rsr_b[-1].retry_count == 3

        # Invocation-wide ledger: A(1 SUCCEEDED) + B(1,2 RETRYING) —
        # B's terminal attempt 3 is MISSING.
        all_rr = _attempts(store, inv.invocation_id)
        assert len(all_rr) == 3, f"expected A1+B1+B2, got {len(all_rr)}"
        assert all_rr[0].retry_id == rr_a_id  # Stage A RR intact, attempt-1

        # Full live attempt count: initial (1) + retries 1..3 (3) — the
        # terminal batch (attempt 3) is where the injection fires.
        live_b_calls = calls_b["n"]
        assert live_b_calls == 4, f"expected 4 live calls, got {live_b_calls}"

        # --- Restart Stage B: F2 must reconcile B ONLY. ---
        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        outcome = kernel2.execute(inv, stage_b, stage_b_fn,
                                  manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.FAILED
        # No stage callback on replay/reconcile — count unchanged.
        assert calls_b["n"] == live_b_calls

        after = _attempts(store, inv.invocation_id)
        # A(1) + B(1) + B(2) + reconstructed B(3) — exactly one new RR.
        assert len(after) == 4, f"expected 4 RR, got {len(after)}"
        assert len({r.retry_id for r in after}) == len(after)
        # Stage A's RR is byte-identical (same id, SUCCEEDED, attempt 1).
        a_after = [r for r in after if r.retry_id == rr_a_id]
        assert len(a_after) == 1
        assert a_after[0].status is RetryRecordStatus.SUCCEEDED
        assert a_after[0].attempt_number == "1"
        # Stage B reconstructed terminal attempt: attempt 3, FAILED, and its
        # identity is a valid deterministic UUIDv7 that differs from Stage A's.
        b_terminal = [r for r in after
                      if r.retry_id != rr_a_id and r.attempt_number == "3"]
        assert len(b_terminal) == 1
        assert b_terminal[0].status is RetryRecordStatus.FAILED
        assert b_terminal[0].retry_id != rr_a_id
        # Restart AGAIN -> fully reconciled, no new records, same ids.
        kernel2.execute(inv, stage_b, stage_b_fn, manifest_id=manifest.manifest_id)
        after2 = _attempts(store, inv.invocation_id)
        assert len(after2) == 4
        assert {r.retry_id for r in after2} == {r.retry_id for r in after}


# =====================================================================
# F3 (R3) — honest SI-01 initial outcome + RSR-anchor crash rule
# =====================================================================

class TestF3HonestSi01:
    def test_f3_clean_success_si01_is_success(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        # SI-01 must reflect the ACTUAL initial outcome: SUCCESS (not the
        # caller-supplied request default of FAILURE).
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.SUCCESS

    def test_f3_initial_retryable_failure_si01_is_failure(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError("initial transient")

        outcome = kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.FAILURE

    def test_f3_rsr_anchor_persisted_before_stage_callback(self):
        """R3: the RSR-01 IN_PROGRESS anchor must exist BEFORE the stage
        callback runs (pre-execution stage anchor)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        anchor_seen = {}

        def stage(ctx):
            rsrs = [r for r in stage_store.list_all("RSR-01")
                    if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
            anchor_seen["anchor_exists"] = bool(rsrs)
            anchor_seen["anchor_state"] = rsrs[0].stage_state.value if rsrs else None

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert anchor_seen["anchor_exists"] is True
        assert anchor_seen["anchor_state"] == "IN_PROGRESS"

    def test_f3_crash_rsr_inprogress_si01_absent_fails_closed(self):
        """R3 crash rule: RSR IN_PROGRESS anchor + SI-01 absent + restart MUST
        fail closed — must NOT silently become new-initial / SUCCESS / FAILURE
        / retry#1."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        # Simulate: anchor persisted but outcome never persisted (crash window).
        stage_store.store(_rsr(stage_store, state=IN_PROGRESS, retry_count=0))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 0  # stage never re-ran

    def test_f3_crash_rsr_inprogress_si01_success_reconciles_to_complete(self):
        """Deterministic recovery: SI-01 SUCCESS persisted but RSR stuck at
        IN_PROGRESS (crash between SI-01 write and RSR COMPLETE write) ->
        advance RSR to COMPLETE and return SUCCEEDED — never retry#1."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        # Recorded state: RSR anchor IN_PROGRESS + SI-01 SUCCESS (the fixture
        # default is FAILURE — override so the persisted SI-01 matches the
        # test's documented crash state; FD #139 R3 crash-rule reconcile
        # keys on the recorded SI-01.status).
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        stage_store.store(_rsr(stage_store, state=IN_PROGRESS, retry_count=0))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        outcome = kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        assert calls["n"] == 0  # no re-execution
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is COMPLETE


# =====================================================================
# F4 (R4) — RFR-01 exactly once on SM-3 terminal FAILED
# =====================================================================

class TestF4RfrExactlyOnce:
    def _rfrs(self, stage_store):
        return [r for r in stage_store.list_all("RFR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME.value]

    def test_f4_retry_exhaustion_creates_rfr_exactly_once(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        outcome = kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.FAILED
        rfrs = self._rfrs(stage_store)
        assert len(rfrs) == 1, f"expected exactly 1 RFR, got {len(rfrs)}"
        # Restart: replay terminal FAILED -> no duplicate RFR (deterministic id).
        kernel2 = RetryKernel(store, stage_store, policy=RetryPolicy(max_retries=3))
        kernel2.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert len(self._rfrs(stage_store)) == 1

    def test_f4_deterministic_initial_failure_creates_rfr(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise IntegrityConflict("deterministic initial contract failure")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        rfrs = self._rfrs(stage_store)
        assert len(rfrs) == 1
        assert rfrs[0].failure_type is ResearchFailureRecordFailure_type.RETRY_LIMIT

    def test_f4_intermediate_retry_failure_no_terminal_rfr(self):
        """An intermediate retry failure (budget remaining) must NOT create a
        terminal RFR — RFR is only for SM-3 terminal FAILED."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] < 3:
                raise RetryableError("transient")
            ctx.produced_output_ids.append("final")

        outcome = kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        assert self._rfrs(stage_store) == []  # succeeded -> no RFR


# =====================================================================
# F5 (R5) — deterministic_uuid7 REAL timestamp + deterministic identity
# =====================================================================

class TestF5UuidV7RealTimestamp:
    def test_f5_timestamp_is_real_epoch_ms_anchor(self):
        anchor_ms = _anchor_ts_ms(FIXED_NOW)
        u = deterministic_uuid7("exec1|cp1|gap", ts_ms=anchor_ms)
        assert u.int >> 80 == anchor_ms, "48-bit ts field must equal real anchor ms"

    def test_f5_same_execution_same_label_same_uuid(self):
        anchor_ms = _anchor_ts_ms(FIXED_NOW)
        a = deterministic_uuid7("exec1|cp1|gap", ts_ms=anchor_ms)
        b = deterministic_uuid7("exec1|cp1|gap", ts_ms=anchor_ms)
        assert a == b
        assert is_uuid7(a)

    def test_f5_distinct_labels_distinct_uuids(self):
        anchor_ms = _anchor_ts_ms(FIXED_NOW)
        gap = deterministic_uuid7("exec1|cp1|gap", ts_ms=anchor_ms)
        note = deterministic_uuid7("exec1|cp1|note", ts_ms=anchor_ms)
        assert gap != note

    def test_f5_version_and_variant_correct(self):
        anchor_ms = _anchor_ts_ms(FIXED_NOW)
        u = deterministic_uuid7("any|seed", ts_ms=anchor_ms)
        assert u.version == 7
        assert u.variant == uuid.RFC_4122

    def test_f5_stable_across_retry_restart(self):
        """Same logical execution + same semantic label -> same UUID across
        process restarts (the anchor is the persisted RSR-01.started_at)."""
        anchor_ms = _anchor_ts_ms(FIXED_NOW)
        first = deterministic_uuid7("case|1.0|stage|sid|gap", ts_ms=anchor_ms)
        # Restart recomputes from the SAME persisted anchor -> identical.
        second = deterministic_uuid7("case|1.0|stage|sid|gap", ts_ms=anchor_ms)
        assert first == second


# =====================================================================
# F6 (R6) — RRM-01.retries = retry COUNT summary; RR-01 = ledger
# =====================================================================

class TestF6RrmRetriesCount:
    def test_f6_rrm_retries_is_count_not_ids(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        m = store.load("RRM-01", manifest.manifest_id)
        # retries is the retry COUNT summary ("3"), NOT comma-separated RR IDs.
        assert m.retries == "3"
        # RR-01 remains the authoritative detailed ledger.
        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 3
        assert all(r.retry_id and r.invocation_id and r.attempt_number
                   and r.status and r.attempted_at for r in rrs)

    def test_f6_clean_success_rrm_retries_zero(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries in ("0", None)
