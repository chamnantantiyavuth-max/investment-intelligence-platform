"""M5.3 CORRECTION PASS 5 — diagnostic contract tests (FD #140, GO 14 Sep 2026).

Founder rulings on the CP4 independent re-audit (FD #140):
- D1-A — ONE SI-01 invocation_id PER LOGICAL STAGE EXECUTION
  (case_id + case_version + stage_name). A NEW logical stage execution
  requires a NEW ServiceInvocation / invocation_id; the same invocation_id may
  be reused ONLY for restart / retry / replay of that SAME logical execution.
  Binding carrier = existing RSR-01.checkpoint_ref:
  `cp:<case_version>:<stage_id>:<invocation_id>`.
- D2-A — RRM-01.retries = MAXIMUM RETRY DEPTH OBSERVED ANYWHERE IN THE RUN
  (monotonic; range "0".."3"; RRM-01 = run-level accumulator).
- F4-R — every terminal SM-3 FAILED must produce exactly ONE RFR-01.

These tests are diagnostic-first (FD #140): they encode the EXACT bounded
findings and are expected RED against the untouched pre-CP5 runtime
(audited baseline origin/main 7238c43, CP4 code), GREEN only after the CP5
fixes. Guard tests that already hold on CP4 (D1-3, D2-8, D2-9, F4-R-14) are
regression anchors and are expected GREEN both before and after.

Coverage (FD #140 section 13 numbering):
D1-A — invocation granularity:
  1. same invocation reused across a different stage -> fail BEFORE callback
  2. same invocation reused across case_version -> fail BEFORE callback
  3. different invocation IDs allow independent initial outcomes across stages
  4. wrong invocation supplied on restart of an existing stage -> fail closed
  5. legacy checkpoint lacking the invocation binding -> fail closed
  6. conflicting stable SI identity fields -> fail closed
D2-A — monotonic run retry summary:
  7. Stage A retry depth 3 then Stage B depth 1 -> final RRM.retries stays "3"
  8. Stage A depth 1 then Stage B depth 3 -> becomes "3"
  9. after reaching "3", a clean/no-retry later stage -> stays "3"
 10. F2 reconciliation of a shallower stage does not decrease "3"
 11. malformed RRM.retries value -> fail closed
F4-R — terminal FAILED -> exactly one RFR:
 12. SI-conflict terminal path creates exactly one RFR
 13. over-budget resume terminal path creates exactly one RFR
 14. repeated restart produces no duplicate RFR

These tests do NOT open F7-F10 and do NOT touch canonical schemas.
"""
from __future__ import annotations

import pytest

from qad.ids import deterministic_uuid7
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
    ResearchFailureRecordResolution,
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
    _make_manifest,
)
from tests.qad.m53.test_correction_pass3 import _seed_running_manifest

COMPLETE = ResearchStageRecordStage_state.COMPLETE
FAILED_ST = ResearchStageRecordStage_state.FAILED
IN_PROGRESS = ResearchStageRecordStage_state.IN_PROGRESS

OTHER_STAGE = ResearchStageRecordStage_name.DEEP_RESEARCH


def _sid(n: int) -> str:
    return f"00000000-0000-7000-8000-{n:012x}"


def _rsr_fix(stage_store, *, stage_id=None, state=IN_PROGRESS, retry_count=0,
             failure_reason=None, invocation_id=None, started_at=FIXED_NOW):
    """RSR fixture with the CP5 checkpoint REFLECTING its invocation binding.

    ``invocation_id=None`` -> pre-CP5 two-field `cp:<case_version>:<stage_id>`
    form (the LEGACY_UNBOUND shape D1-A must fail closed on).
    """
    sid = stage_id or _sid(0xC00)
    if invocation_id is None:
        cp = f"cp:1.0:{sid}"
    else:
        cp = f"cp:1.0:{sid}:{invocation_id}"
    return ResearchStageRecord(
        stage_id=sid, case_id=CASE_ID, stage_name=STAGE_NAME,
        stage_state=state, started_at=started_at, completed_at=started_at,
        responsible_role="S8", checkpoint_ref=cp,
        output_ids=[], retry_count=retry_count, failure_reason=failure_reason,
    )


def _rfrs(stage_store) -> list:
    return [r for r in stage_store.list_all("RFR-01")
            if r.case_id == CASE_ID]


# =====================================================================
# D1-A — one SI-01 invocation_id per logical stage execution
# =====================================================================

class TestD1aInvocationGranularity:
    def test_d1a_reuse_invocation_across_stage_fails_before_callback(self):
        """D1-1 (section 13): a different stage is a DIFFERENT logical
        execution and MUST use a new invocation_id.  Reuse of the invocation
        fails closed BEFORE the callback — no anchor, no RR, no mutation."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 1  # Stage A completed under invocation A

        # Stage B (a different stage identity) MUST NOT reuse invocation A.
        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, OTHER_STAGE, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 1  # fail closed BEFORE callback
        rsr_b = [r for r in stage_store.list_all("RSR-01")
                 if r.stage_name == OTHER_STAGE]
        assert rsr_b == []  # no RSR anchor for the illegal reuse

    def test_d1a_reuse_invocation_across_case_version_fails_before_callback(self):
        """D1-2 (section 13): a new case_version is a NEW logical execution and
        MUST use a new invocation_id."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest_v1 = _seed_running_manifest(store, case_version="1.0")
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=manifest_v1.manifest_id)
        assert calls["n"] == 1
        manifest_v2 = _make_manifest(case_version="2.0").model_copy(
            update={"manifest_id": _sid(0xC30)})
        store.store(manifest_v2)
        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest_v2.manifest_id)
        assert calls["n"] == 1  # fail closed BEFORE callback

    def test_d1a_distinct_invocations_independent_outcomes(self):
        """D1-3 (section 13): with distinct invocation IDs, stage outcomes are
        TRUTHFULLY independent — Stage A initial FAILURE (retry #1 success),
        Stage B initial SUCCESS with zero retries.  No outcome manipulation."""
        kernel, store, stage_store = _kernel()
        inv_a = _make_invocation(invocation_id=_sid(0xC21))
        inv_b = _make_invocation(invocation_id=_sid(0xC22))
        manifest = _seed_running_manifest(store)
        calls_a = {"n": 0}

        def stage_a(ctx):
            calls_a["n"] += 1
            if calls_a["n"] == 1:
                raise RetryableError("A transient initial")

        out_a = kernel.execute(inv_a, STAGE_NAME, stage_a,
                               manifest_id=manifest.manifest_id)
        assert out_a.status is RetryRecordStatus.SUCCEEDED
        si_a = store.load("SI-01", inv_a.invocation_id)
        assert si_a.status is ServiceInvocationStatus.FAILURE

        def stage_b(ctx):
            pass  # actual initial SUCCESS

        out_b = kernel.execute(inv_b, OTHER_STAGE, stage_b,
                               manifest_id=manifest.manifest_id)
        assert out_b.status is RetryRecordStatus.SUCCEEDED
        si_b = store.load("SI-01", inv_b.invocation_id)
        assert si_b.status is ServiceInvocationStatus.SUCCESS
        # Ledgers are per invocation: A has RR#1; B has none.
        assert len(_attempts(store, inv_a.invocation_id)) == 1
        assert _attempts(store, inv_b.invocation_id) == []

    def test_d1a_wrong_invocation_on_restart_fails_closed(self):
        """D1-4 (section 13): restart of an EXISTING (bound) stage with a
        DIFFERENT invocation_id than the persisted binding fails closed."""
        kernel, store, stage_store = _kernel()
        inv_a = _make_invocation(invocation_id=_sid(0xC41))
        inv_b = _make_invocation(invocation_id=_sid(0xC42))
        manifest = _seed_running_manifest(store)
        sid = _sid(0xC04)
        # Authoritative bound COMPLETE chain for Stage/version, bound to inv A.
        store.store(inv_a.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid, state=COMPLETE, retry_count=0,
            invocation_id=inv_a.invocation_id))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv_b, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0  # fail closed, no callback

    def test_d1a_legacy_unbound_checkpoint_fails_closed(self):
        """D1-5 (section 13): a persisted stage execution whose checkpoint_ref
        carries NO invocation binding (pre-CP5 `cp:<case_version>:<stage_id>`)
        is LEGACY_UNBOUND_EXECUTION and FAILS CLOSED under D1-A enforcement —
        the invocation is never guessed from case_id/RR count/SI status."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        # 2-field pre-CP5 checkpoint — no invocation binding.
        stage_store.store(_rsr_fix(
            stage_store, stage_id=_sid(0xC05), state=COMPLETE,
            retry_count=0, invocation_id=None))
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0

    def test_d1a_conflicting_si_stable_identity_fails_closed(self):
        """D1-6 (section 13): the persisted SI-01 record for the bound
        invocation must AGREE on the stable request-identity fields
        (invocation_id / case_id / service_id / request_type / invoked_at).
        A conflict fails closed — status alone never establishes consistency."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        sid = _sid(0xC06)
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid, state=COMPLETE, retry_count=0,
            invocation_id=inv.invocation_id))
        # Same invocation_id but a DIFFERENT stable service identity.
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS,
                    "service_id": "S9"}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0


# =====================================================================
# D2-A — RRM-01.retries = maximum retry depth observed in the run
# =====================================================================

class TestD2aMonotonicRunRetrySummary:
    def test_d2a_depth3_then_depth1_stays_3(self):
        """D2-7 (section 13): Stage A exhausts retries (depth 3), Stage B
        retries once (depth 1).  The run summary must remain "3" — monotonic
        max, never the CURRENT stage's shallower count."""
        kernel, store, stage_store = _kernel()
        inv_a = _make_invocation(invocation_id=_sid(0xC71))
        inv_b = _make_invocation(invocation_id=_sid(0xC72))
        manifest = _seed_running_manifest(store)

        def stage_a(ctx):
            raise RetryableError("A always transient")

        out_a = kernel.execute(inv_a, STAGE_NAME, stage_a,
                               manifest_id=manifest.manifest_id)
        assert out_a.status is RetryRecordStatus.FAILED
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "3"

        calls_b = {"n": 0}

        def stage_b(ctx):
            calls_b["n"] += 1
            if calls_b["n"] == 1:
                raise RetryableError("B transient once")

        out_b = kernel.execute(inv_b, OTHER_STAGE, stage_b,
                               manifest_id=manifest.manifest_id)
        assert out_b.status is RetryRecordStatus.SUCCEEDED
        m2 = store.load("RRM-01", manifest.manifest_id)
        assert m2.retries == "3", \
            f"run-level max must stay '3', got {m2.retries!r}"

    def test_d2a_depth1_then_depth3_becomes_3(self):
        """D2-8 (section 13): depth 1 first, then a stage reaches depth 3 —
        the summary must climb to "3"."""
        kernel, store, stage_store = _kernel()
        inv_a = _make_invocation(invocation_id=_sid(0xC81))
        inv_b = _make_invocation(invocation_id=_sid(0xC82))
        manifest = _seed_running_manifest(store)
        calls_a = {"n": 0}

        def stage_a(ctx):
            calls_a["n"] += 1
            if calls_a["n"] == 1:
                raise RetryableError("A transient once")

        out_a = kernel.execute(inv_a, STAGE_NAME, stage_a,
                               manifest_id=manifest.manifest_id)
        assert out_a.status is RetryRecordStatus.SUCCEEDED
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "1"

        def stage_b(ctx):
            raise RetryableError("B always transient")

        out_b = kernel.execute(inv_b, OTHER_STAGE, stage_b,
                               manifest_id=manifest.manifest_id)
        assert out_b.status is RetryRecordStatus.FAILED
        m2 = store.load("RRM-01", manifest.manifest_id)
        assert m2.retries == "3"

    def test_d2a_clean_stage_after_3_stays_3(self):
        """D2-9 (section 13): once the summary is "3", a later clean
        no-retry stage must NOT reduce it."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(manifest.model_copy(update={"retries": "3"}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        out = kernel.execute(inv, STAGE_NAME, stage,
                             manifest_id=manifest.manifest_id)
        assert out.status is RetryRecordStatus.SUCCEEDED
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "3"

    def test_d2a_f2_reconcile_shallower_stage_does_not_decrease(self):
        """D2-10 (section 13): F2 terminal provenance reconciliation is bound
        by the SAME monotonic rule — reconciling a stage with retry depth 1
        must NOT overwrite an existing run summary of "3"."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation(invocation_id=_sid(0xCA1))
        manifest = _seed_running_manifest(store)
        sid = _sid(0xC0A)
        cp = f"cp:1.0:{sid}:{inv.invocation_id}"
        expected = kernel._retry_identity(
            ExecutionContext(case_id=CASE_ID, case_version="1.0",
                             stage_name=STAGE_NAME),
            _ExecState(stage_id=sid, started_at=FIXED_NOW,
                       completed_at=FIXED_NOW, checkpoint_ref=cp,
                       previous_outputs=[], retry_count=1),
            1,
        )
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        store.store(RetryRecord(
            retry_id=expected, invocation_id=inv.invocation_id,
            attempt_number="1", attempted_at=FIXED_NOW,
            status=RetryRecordStatus.FAILED, error="boom", escalated_to=None,
        ))
        store.store(manifest.model_copy(
            update={"retries": "3", "failures": [expected]}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid, state=FAILED_ST, retry_count=1,
            failure_reason="boom", invocation_id=inv.invocation_id))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        out = kernel.execute(inv, STAGE_NAME, stage,
                             manifest_id=manifest.manifest_id)
        assert out.status is RetryRecordStatus.FAILED
        m = store.load("RRM-01", manifest.manifest_id)
        assert m.retries == "3", \
            f"F2 reconcile must not decrease the run summary, got {m.retries!r}"

    def test_d2a_malformed_rrm_retries_fails_closed(self):
        """D2-11 (section 13): an unreadable RRM-01.retries value is a
        run-summary integrity failure — FAIL CLOSED, never silently
        overwritten."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(manifest.model_copy(update={"retries": "7"}))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError("boom")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)


# =====================================================================
# F4-R — every terminal SM-3 FAILED -> exactly one RFR-01
# =====================================================================

class TestF4rTerminalFailedRfrCompleteness:
    def test_f4r_si_conflict_terminal_path_creates_exactly_one_rfr(self):
        """F4-R-12 (section 13): a conflicting SI-01 appearing in the
        preflight/outcome race window terminalizes the RSR to FAILED AND
        creates exactly ONE RFR-01 atomically — never a FAILED RSR without
        RFR (FD #139 R4 + FD #140 F4-R)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            # Race/corruption: a conflicting SI-01 appears between D1-A
            # preflight and the ACTUAL outcome persistence.
            store.store(inv.model_copy(
                update={"status": ServiceInvocationStatus.SUCCESS}))
            raise RetryableError("actual transient failure")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        si01 = store.load("SI-01", inv.invocation_id)
        assert si01.status is ServiceInvocationStatus.SUCCESS  # immutable
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs[-1].stage_state is FAILED_ST
        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1, \
            f"exactly one RFR expected on the SI-conflict terminal path, got {len(rfrs)}"

    def test_f4r_over_budget_resume_creates_exactly_one_rfr(self):
        """F4-R-13 (section 13): a corrupted/over-budget IN_PROGRESS resume
        that terminalizes FAILED must create exactly ONE RFR-01."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=_sid(0xC0B), state=IN_PROGRESS,
            retry_count=3, invocation_id=inv.invocation_id))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        out = kernel.execute(inv, STAGE_NAME, stage,
                             manifest_id=manifest.manifest_id)
        assert out.status is RetryRecordStatus.FAILED
        assert calls["n"] == 0  # no re-execution at resume
        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1, \
            f"exactly one RFR expected on over-budget resume, got {len(rfrs)}"

    def test_f4r_repeated_restart_no_duplicate_rfr(self):
        """F4-R-14 (section 13): repeated restart of a terminal FAILED stage
        with an existing deterministic RFR never duplicates it."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation(invocation_id=_sid(0xCC1))
        manifest = _seed_running_manifest(store)
        sid = _sid(0xC0C)
        cp = f"cp:1.0:{sid}:{inv.invocation_id}"
        fid = str(deterministic_uuid7(
            f"{CASE_ID}|1.0|{STAGE_NAME.value}|{sid}|{cp}|research-failure",
            ts_ms=_started_at_to_ms(FIXED_NOW)))
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid, state=FAILED_ST, retry_count=1,
            failure_reason="boom", invocation_id=inv.invocation_id))
        stage_store.store(ResearchFailureRecord(
            failure_id=fid, case_id=CASE_ID, failure_reason="boom",
            failure_type=ResearchFailureRecordFailure_type.RETRY_LIMIT,
            resolution=ResearchFailureRecordResolution.UNRESOLVED,
            retry_count=1, stage_name=STAGE_NAME.value,
            error_details="boom", failure_timestamp=FIXED_NOW, recorder="S8",
        ))
        for _ in range(2):
            assert len(_rfrs(stage_store)) == 1
            reports = {"n": 0}

            def stage(ctx):
                reports["n"] += 1

            out = kernel.execute(inv, STAGE_NAME, stage,
                                 manifest_id=manifest.manifest_id)
            assert out.status is RetryRecordStatus.FAILED
            assert reports["n"] == 0  # replay — no re-execution
            assert len(_rfrs(stage_store)) == 1