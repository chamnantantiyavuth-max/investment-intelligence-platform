"""M5.3 CORRECTION PASS 6 — RED diagnostic contract tests (Founder re-audit FAIL,
21 Sep 2026).

The Founder independent re-audit of CP5 (origin/main @ b4d2dad) returned FAIL /
BOUNDED CORRECTION REQUIRED with TWO implementation defects:

- C1 — RFR.retry_count OFF BY ONE.  Terminal retry paths construct
  `rfr=self._ensure_rfr(execution, state, ...)` as an argument to
  `_write_rsr(... attempt_number=N ...)`.  Python evaluates `_ensure_rfr()`
  BEFORE `_write_rsr()` mutates `state.retry_count = attempt_number`, so a
  terminal retry can persist RSR.retry_count = N with RFR.retry_count = N-1.
  Required invariant: for a terminal FAILED caused by retry attempt N,
  RFR.retry_count == RSR.retry_count == N.

- C2 — D1 instance binding integrity incomplete.  The existing-execution
  validator verifies the invocation binding but NOT the checkpoint's
  stage_id against the canonical RSR.stage_id, NOT the checkpoint
  case_version against the authoritative execution case_version, and NOT
  that one logical execution has exactly ONE stable stage_id.

These tests are diagnostic-first (CP5 precedent): expected RED against the
untouched b4d2dad runtime, GREEN only after the CP6 fixes.  Guard tests that
already hold pre-fix are regression anchors (expected GREEN both before and
after) per the audit instruction §5 / §7.

Coverage:
C1 (audit §5):
  A. retry #3 terminal failure -> RSR.retry_count == 3, exactly one RFR,
     RFR.retry_count == 3
  B. retry #1 deterministic terminal failure -> RSR.retry_count == 1,
     exactly one RFR, RFR.retry_count == 1
  C. (guards) initial deterministic failure -> RFR.retry_count == 0;
     over-budget resume at authoritative retry_count 3 -> RFR.retry_count == 3
C2 (audit §7):
  A. checkpoint stage_id != canonical RSR.stage_id -> IntegrityConflict
     BEFORE callback; no RR/RRM mutation; no replay
  B. two RSR records (same case/case_version/stage_name/invocation) with
     stage_id A and B -> IntegrityConflict BEFORE callback; no arbitrary
     `last` selection; no retry/replay; no canonical mutation
  C. checkpoint case_version != authoritative execution case_version
     (and malformed checkpoint) -> fail closed
"""
from __future__ import annotations

import pytest

from qad.m53.retry_kernel import (
    ExecutionContext,
    RetryableError,
    RetryKernel,
)
from qad.models.family_c import (
    ResearchFailureRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import (
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
from tests.qad.m53.test_correction_pass5 import (
    _rfrs,
    _rsr_fix,
)
from tests.qad.m53.test_correction_pass3 import _seed_running_manifest

COMPLETE = ResearchStageRecordStage_state.COMPLETE
FAILED_ST = ResearchStageRecordStage_state.FAILED
IN_PROGRESS = ResearchStageRecordStage_state.IN_PROGRESS

OTHER_STAGE = ResearchStageRecordStage_name.DEEP_RESEARCH


def _sid(n: int) -> str:
    return f"00000000-0000-7000-8000-{n:012x}"


def _rsr_chain_records(stage_store) -> list:
    return [r for r in stage_store.list_all("RSR-01")
            if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]


# =====================================================================
# C1 — RFR.retry_count == RSR.retry_count == terminal attempt number
# =====================================================================

class TestC1RfrRetryCountOffByOne:
    def test_c1_retry3_terminal_records_3_in_rsr_and_rfr(self):
        """C1-A (audit §5A): initial + retries #1/#2 retryable, retry #3
        terminal retryable failure.

        The terminal RSR FAILED must carry retry_count == 3 and the RFR-01
        persisted atomically with it must ALSO carry retry_count == 3
        (F4-R + C1 content accuracy).
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError(f"always transient {calls['n']}")

        out = kernel.execute(inv, STAGE_NAME, stage,
                             manifest_id=manifest.manifest_id)
        assert out.status is RetryRecordStatus.FAILED
        assert calls["n"] == 4  # initial + 3 retries

        terminal = [r for r in _rsr_chain_records(stage_store)
                    if r.stage_state is FAILED_ST]
        assert len(terminal) == 1, "exactly one terminal RSR"
        assert terminal[0].retry_count == 3, \
            f"terminal RSR.retry_count must be 3, got {terminal[0].retry_count!r}"

        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1, f"exactly one RFR expected, got {len(rfrs)}"
        assert rfrs[0].retry_count == 3, \
            f"RFR.retry_count must equal terminal RSR.retry_count (3), " \
            f"got {rfrs[0].retry_count!r}"

    def test_c1_retry1_deterministic_terminal_records_1_in_rsr_and_rfr(self):
        """C1-B (audit §5B): initial retryable, retry #1 deterministic
        (non-retryable) terminal failure.

        The terminal RSR FAILED must carry retry_count == 1 and the RFR-01
        must ALSO carry retry_count == 1.
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient initial")
            raise ValueError("deterministic on retry")

        with pytest.raises(ValueError):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 2  # initial + retry #1

        terminal = [r for r in _rsr_chain_records(stage_store)
                    if r.stage_state is FAILED_ST]
        assert len(terminal) == 1
        assert terminal[0].retry_count == 1, \
            f"terminal RSR.retry_count must be 1, got {terminal[0].retry_count!r}"

        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1, f"exactly one RFR expected, got {len(rfrs)}"
        assert rfrs[0].retry_count == 1, \
            f"RFR.retry_count must equal terminal RSR.retry_count (1), " \
            f"got {rfrs[0].retry_count!r}"

    def test_c1_guard_initial_deterministic_failure_rfr_retry_count_0(self):
        """C1-C guard (audit §5C): an INITIAL deterministic terminal failure
        is NOT a retry — RFR.retry_count must remain 0 (initial semantic
        unchanged by CP6)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise ValueError("deterministic initial")

        with pytest.raises(ValueError):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 1

        terminal = [r for r in _rsr_chain_records(stage_store)
                    if r.stage_state is FAILED_ST]
        assert len(terminal) == 1
        assert terminal[0].retry_count == 0
        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1
        assert rfrs[0].retry_count == 0, \
            f"initial deterministic RFR.retry_count must be 0, " \
            f"got {rfrs[0].retry_count!r}"

    def test_c1_guard_over_budget_resume_rfr_retry_count_3(self):
        """C1-C guard (audit §5C): an over-budget IN_PROGRESS resume terminal
        FAILED uses the AUTHORITATIVE existing retry_count (3) in BOTH the
        RSR and the RFR — CP6 must not disturb resume semantics."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=_sid(0xD00), state=IN_PROGRESS,
            retry_count=3, invocation_id=inv.invocation_id))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        out = kernel.execute(inv, STAGE_NAME, stage,
                             manifest_id=manifest.manifest_id)
        assert out.status is RetryRecordStatus.FAILED
        assert calls["n"] == 0  # no re-execution at resume

        terminal = [r for r in _rsr_chain_records(stage_store)
                    if r.stage_state is FAILED_ST]
        assert len(terminal) == 1
        assert terminal[0].retry_count == 3
        rfrs = _rfrs(stage_store)
        assert len(rfrs) == 1
        assert rfrs[0].retry_count == 3, \
            f"over-budget resume RFR.retry_count must be 3 (authoritative " \
            f"existing), got {rfrs[0].retry_count!r}"


# =====================================================================
# C2 — checkpoint stage_id / case_version binding integrity
# =====================================================================

class TestC2StageIdBindingIntegrity:
    def test_c2_checkpoint_stage_id_mismatch_fails_closed_before_callback(self):
        """C2-A (audit §7A): RSR.stage_id = A but checkpoint_ref binds
        stage_id B (cp:1.0:B:<invocation_id>).

        Expected: IntegrityConflict BEFORE callback; no RR mutation; no RRM
        mutation; no replay.
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        stage_id_a = _sid(0xD01)
        stage_id_b = _sid(0xD02)
        # SI-01 present (terminal COMPLETE chain would otherwise 5D-fail).
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        before_rsr = len(stage_store.list_all("RSR-01"))
        before_rr = len(store.list_all("RR-01"))
        before_rrm_hash = store.get_canonical_hash(
            "RRM-01", manifest.manifest_id)
        # canonical RSR.stage_id = A; checkpoint binds B.
        rec = _rsr_fix(
            stage_store, stage_id=stage_id_a, state=COMPLETE,
            retry_count=0, invocation_id=inv.invocation_id)
        rec = rec.model_copy(
            update={"checkpoint_ref": f"cp:1.0:{stage_id_b}:{inv.invocation_id}"})
        stage_store.store(rec)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0, "fail closed BEFORE callback"
        assert len(stage_store.list_all("RSR-01")) == before_rsr, \
            "no canonical stage mutation"
        assert len(store.list_all("RR-01")) == before_rr, "no RR mutation"
        assert store.get_canonical_hash("RRM-01", manifest.manifest_id) \
            == before_rrm_hash, "no RRM mutation"

    def test_c2_multiple_stage_ids_one_logical_execution_fails_closed(self):
        """C2-B (audit §7B): two RSR records with the SAME logical execution
        (case_id + case_version + stage_name + invocation binding) but
        DIFFERENT stage_ids (A and B).

        Expected: IntegrityConflict BEFORE callback; NO arbitrary `last`
        selection; no retry/replay; no canonical mutation.
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        sid_a = _sid(0xD11)
        sid_b = _sid(0xD12)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.FAILURE}))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid_a, state=COMPLETE,
            retry_count=0, invocation_id=inv.invocation_id))
        stage_store.store(_rsr_fix(
            stage_store, stage_id=sid_b, state=IN_PROGRESS,
            retry_count=0, invocation_id=inv.invocation_id))
        before_rsr = len(stage_store.list_all("RSR-01"))
        before_rr = len(store.list_all("RR-01"))
        before_rrm_hash = store.get_canonical_hash(
            "RRM-01", manifest.manifest_id)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0, "fail closed BEFORE callback"
        assert len(stage_store.list_all("RSR-01")) == before_rsr, \
            "no canonical mutation (no arbitrary last selection written)"
        assert len(store.list_all("RR-01")) == before_rr, "no RR mutation"
        assert store.get_canonical_hash("RRM-01", manifest.manifest_id) \
            == before_rrm_hash, "no RRM mutation"

    def test_c2_checkpoint_case_version_mismatch_fails_closed(self):
        """C2-C (audit §7C): the parsed checkpoint case_version must agree
        with the authoritative execution case_version.

        NOTE: ``_rsr_history`` already pre-filters the chain by checkpoint
        case_version (mismatched-version records are excluded), so at the
        execute() level a version-mismatch record never reaches the
        validator — the chain is empty.  The audit's own wording is
        "if practical with the existing helper boundary", so this RED test
        drives the STRENGTHENED validator directly with a crafted chain
        carrying a case_version mismatch: it must FAIL CLOSED inside
        ``_validate_existing_execution``.
        """
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        sid = _sid(0xD21)
        rec = _rsr_fix(
            stage_store, stage_id=sid, state=COMPLETE,
            retry_count=0, invocation_id=inv.invocation_id)
        # checkpoint claims case_version 2.0 while the authoritative
        # execution case_version is 1.0.
        rec = rec.model_copy(
            update={"checkpoint_ref": f"cp:2.0:{sid}:{inv.invocation_id}"})
        execution = ExecutionContext(case_id=CASE_ID, case_version="1.0",
                                     stage_name=STAGE_NAME)
        with pytest.raises(IntegrityConflict):
            kernel._validate_existing_execution(inv, execution, [rec])

    def test_c2_malformed_checkpoint_fails_closed(self):
        """C2-C guard (audit §7C): a malformed/unparseable checkpoint with a
        plausible stage_id but no binding must fail closed (LEGACY_UNBOUND /
        malformed) — never treated as a valid bound execution."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _seed_running_manifest(store)
        store.store(inv.model_copy(
            update={"status": ServiceInvocationStatus.SUCCESS}))
        sid = _sid(0xD22)
        rec = _rsr_fix(
            stage_store, stage_id=sid, state=COMPLETE,
            retry_count=0, invocation_id=inv.invocation_id)
        rec = rec.model_copy(update={"checkpoint_ref": "not-a-checkpoint"})
        stage_store.store(rec)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0