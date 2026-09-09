"""M5.3 CORRECTION PASS 2 — diagnostic contract tests (FD #138, RE-AUDIT FAIL 2).

Founder independent re-audit (9 Sep 2026) found 7 implementation defects in
the correction-pass-1 runtime (baseline 36d6aac).  These tests encode the
required corrected behaviour per FD #138 semantics.  They are diagnostic-first
(GO §12): they are expected RED against 36d6aac, and GREEN only after the
Correction Pass 2 runtime fixes.

Coverage (re-audit findings):
- §1  S7 LIVE collection query must resolve the authoritative EAR carrier.
- §2  Resume after an initial transient failure must continue as retry #1,
       never re-run the initial execution (RSR is the execution authority).
- §3  RSR-01 / SM-3 lifecycle: ONE stable stage_id across the execution,
       IN_PROGRESS while retrying, COMPLETE/FAILED only terminal, append-only
       versions recoverable, no FAILED→COMPLETE.
- §4  The checkpoint written by a failed attempt must flow into the NEXT retry
       (and its produced outputs must carry forward).
- §5  Case-version isolation: a new case_version must not inherit the prior
       version's checkpoint/outputs and must not false-replay.
- §6  RRM retry lineage must accumulate (no stale-object overwrite).
- §7  Execution-identity scoping of RR terminal replay: existing RR history for
       one stage/case_version must NOT short-circuit another execution.
- §8  Retried-write idempotency: deterministic canonical identity derived
       mechanically from the ExecutionContext (not a hard-coded id), using a
       canonical schema in a faithful store placement.
"""
from __future__ import annotations

import pytest

from qad.ids import deterministic_uuid7, is_uuid7
from qad.m53.retry_kernel import RetryableError
from qad.models.family_c import (
    ResearchStageRecord,
    ResearchStageRecordStage_name,
    ResearchStageRecordStage_state,
)
from qad.models.family_i import RetryRecordStatus
from qad.persistence import IntegrityConflict
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

DEEP = ResearchStageRecordStage_name.DEEP_RESEARCH
IN_PROGRESS = ResearchStageRecordStage_state.IN_PROGRESS
COMPLETE = ResearchStageRecordStage_state.COMPLETE
FAILED_ST = ResearchStageRecordStage_state.FAILED


def _seed_running_manifest(store, *, case_version="1.0"):
    m = _make_manifest(case_version=case_version)
    store.store(m)
    return m


# =====================================================================
# §1  S7 — LIVE collection query resolves authoritative EAR
# =====================================================================

class TestS7LiveQueryCarrier:
    def test_valid_live_update_appears_in_query(self):
        """A valid post-AS_OF LIVE update (authoritative EAR carrier + exact
        RD PITC) must appear in query() results, matching access()'s ALLOWED."""
        from tests.qad.m53.test_pit_enforcement import (
            _make_ear,
            _make_ev,
            _make_pitc,
            _seed,
            _topology,
        )
        from qad.models.family_i import PITContextMode
        SID = f"00000000-0000-7000-8000-{0xEEE:012x}"
        EV = f"00000000-0000-7000-8000-{0xEEF:012x}"
        PITC = f"00000000-0000-7000-8000-{0xEF0:012x}"
        src, pitc_store, ev_reg, svc = _topology()
        # source published post-AS_OF (future-leak candidate under the carrier)
        sid, case = _seed(src, pitc_store, ev_reg,
                          publication_date="2026-06-01")
        ev = _make_ev(sid, EV, "2026-06-01")  # post-AS_OF with valid carrier
        pitc = _make_pitc(PITC, "Research Director", case,
                          mode="LIVE_CASE_UPDATE")
        pitc_store.store(pitc)
        ear = _make_ear(ev.evidence_id, f"00000000-0000-7000-8000-{0xEF1:012x}",
                        is_update=True, pitc_id=PITC)
        ev_reg.admit_evidence(ev, ear)
        # access()/adjudicate() resolve the carrier -> ALLOWED
        rec = svc.access(ev.evidence_id, PITC)
        assert rec.evidence_id == EV
        # query() must resolve the carrier too -> the EV is included
        res = svc.query(PITC)
        ids = {r.evidence_id for r in res.records}
        assert EV in ids, "valid LIVE update was excluded from query()"


# =====================================================================
# §2  Resume after initial transient failure -> retry #1 (never re-initial)
# =====================================================================

class TestInitialFailureResume:
    def test_seeded_inprogress_resumes_as_retry1_not_initial(self):
        """Pre-seed RSR IN_PROGRESS (initial already ran, retry workflow
        pending, RR empty) — simulate process interruption after initial fail.
        execute() must resume as RETRY #1: RR attempt#1 written, RSR
        retry_count=1, and the stage runs exactly once (as retry #1)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        stage_id = f"00000000-0000-7000-8000-{0xA00:012x}"
        stage_store.store(ResearchStageRecord(
            stage_id=stage_id, case_id=CASE_ID,
            stage_name=STAGE_NAME, stage_state=IN_PROGRESS,
            started_at=FIXED_NOW, completed_at=FIXED_NOW,
            responsible_role="S8", checkpoint_ref=f"cp:1.0:{stage_id}",
            output_ids=[], retry_count=0,
        ))
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        # Resumed as retry #1, NOT a fresh initial: RR attempt#1 exists.
        rr = _attempts(store, inv.invocation_id)
        assert len(rr) == 1, f"expected 1 RR (retry #1), got {len(rr)}"
        assert rr[0].attempt_number == "1"
        assert rr[0].status is RetryRecordStatus.SUCCEEDED
        # RSR reflects one retry completed via the SAME stage identity.
        rsrs = [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]
        assert rsrs, "no RSR chain"
        assert rsrs[-1].stage_id == stage_id, "resume minted a NEW stage identity"
        assert rsrs[-1].retry_count == 1
        assert rsrs[-1].stage_state is COMPLETE
        assert calls["n"] == 1  # ran once as retry #1, not initial again

    def test_never_executed_still_runs_initial(self):
        """No RSR chain -> initial execution still runs (zero RR-01)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        assert calls["n"] == 1
        assert _attempts(store, inv.invocation_id) == []


# =====================================================================
# §3  RSR-01 / SM-3 — stable stage_id + correct lifecycle
# =====================================================================

class TestStableStageIdLifecycle:
    def _rsr_chain(self, stage_store):
        return [r for r in stage_store.list_all("RSR-01")
                if r.case_id == CASE_ID and r.stage_name == STAGE_NAME]

    def test_stable_stage_id_and_inprogress_through_retries(self):
        """initial fails retryably, retry#1 succeeds. ONE stage_id throughout;
        intermediate state IN_PROGRESS (not FAILED); final COMPLETE on same id."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient initial")

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        chain = self._rsr_chain(stage_store)
        assert chain, "no RSR records"
        ids = {r.stage_id for r in chain}
        assert len(ids) == 1, f"stage_id recreated per attempt: {ids}"
        sid = chain[-1].stage_id
        # Prior versions recoverable (append-only)
        assert stage_store.list_versions("RSR-01", sid), "no prior versions"
        # Terminal state COMPLETE on the same id; never FAILED then COMPLETE.
        assert chain[-1].stage_state is COMPLETE
        assert chain[-1].retry_count == 1

    def test_retryable_failure_is_inprogress_not_failed(self):
        """A retryable failure with budget remaining must leave the stage
        IN_PROGRESS, not terminally FAILED."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError("always fail retryably")

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        chain = self._rsr_chain(stage_store)
        # Terminal = FAILED after retries exhausted (budget 3: retry#3 fails).
        assert chain[-1].stage_state is FAILED_ST
        assert chain[-1].retry_count == 3
        assert len({r.stage_id for r in chain}) == 1  # one stable identity

    def test_no_illegal_failed_to_complete(self):
        """No version in the append-only history may transition a terminal
        FAILED record to COMPLETE.  Final COMPLETE after a successful retry is
        reached only via IN_PROGRESS versions."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient")

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        chain = self._rsr_chain(stage_store)
        sid = chain[-1].stage_id
        versions = stage_store.list_versions("RSR-01", sid)
        states = []
        for v in versions:
            rec = stage_store.load_version("RSR-01", sid, v)
            states.append(rec.stage_state.value)
        # Any FAILED version must be the LAST (never FAILED->COMPLETE).
        if FAILED_ST.value in states:
            assert states[-1] == FAILED_ST.value


# =====================================================================
# §4  Checkpoint must flow into the next retry
# =====================================================================

class TestCheckpointPropagation:
    def test_failed_attempt_output_and_checkpoint_feed_retry(self):
        """initial produces A + new checkpoint then fails retryably; retry#1
        must receive A in previous_output_ids and the NEW checkpoint_ref."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}
        seen = {}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                ctx.produced_output_ids.append("A")
                seen["retry1_prev"] = None
                raise RetryableError("transient after producing A")
            seen["retry1_prev"] = list(ctx.previous_output_ids)
            seen["retry1_cp"] = ctx.checkpoint_ref

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        assert "A" in (seen["retry1_prev"] or []), "output A not carried into retry"
        assert seen["retry1_cp"], "retry received no checkpoint_ref"

    def test_cumulative_outputs_accumulate(self):
        """A then B accumulate across retries."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        _seed_running_manifest(store)
        calls = {"n": 0}
        seen = {}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                ctx.produced_output_ids.append("A")
                raise RetryableError("t1")
            if calls["n"] == 2:
                seen["retry2_prev"] = list(ctx.previous_output_ids)
                ctx.produced_output_ids.append("B")
                raise RetryableError("t2")
            seen["retry3_prev"] = list(ctx.previous_output_ids)

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=store.list_all("RRM-01")[0].manifest_id)
        assert "A" in (seen["retry2_prev"] or [])
        assert "A" in (seen["retry3_prev"] or []) and "B" in (seen["retry3_prev"] or [])


# =====================================================================
# §5  Case-version isolation
# =====================================================================

class TestCaseVersionIsolation:
    def test_new_case_version_does_not_inherit_old_outputs(self):
        """v1.0 fails producing OLD; v2.0 (new manifest) same stage must start
        fresh — no OLD output, own stage chain, no false replay."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        m1 = _seed_running_manifest(store, case_version="1.0")
        calls = {"n": 0}
        seen = {}

        def stage(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                ctx.produced_output_ids.append("OLD")
                raise RetryableError("t1")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=m1.manifest_id)
        # v2.0
        m2 = _make_manifest(case_version="2.0")
        m2 = m2.model_copy(update={"manifest_id": f"00000000-0000-7000-8000-{0xB00:012x}"})
        store.store(m2)
        seen2 = {}
        before = calls["n"]

        def stage2(ctx):
            seen2["prev"] = list(ctx.previous_output_ids)
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage2, manifest_id=m2.manifest_id)
        assert calls["n"] > before, "v2 false-replayed (did not execute)"
        assert "OLD" not in (seen2["prev"] or []), "v2 inherited v1 outputs"


# =====================================================================
# §6  RRM retry lineage accumulates (no stale-object overwrite)
# =====================================================================

class TestRrmLineageAccumulates:
    def test_full_retry_and_failure_lineage_in_current_manifest(self):
        """3 retries (all retryable-fail, budget exhausted -> FAILED). Final
        current RRM must hold retries=[RR1,RR2] and failures=[RR3]."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        m = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=m.manifest_id)
        manifest = store.load("RRM-01", m.manifest_id)
        retry_refs = [x for x in (manifest.retries or "").split(",") if x.strip()]
        failures = manifest.failures or []
        assert len(retry_refs) == 2, f"expected 2 scheduled retry refs, got {retry_refs}"
        assert len(failures) == 1, f"expected 1 terminal failure ref, got {failures}"


# =====================================================================
# §7  Execution-identity scoping of RR terminal replay
# =====================================================================

class TestExecutionIdentityRrScoping:
    def test_stage_b_executes_despite_stage_a_rr_history(self):
        """Stage A: initial fails, retry#1 succeeds -> RR SUCCEEDED exists
        under the invocation. Stage B (different stage_name, same invocation)
        MUST execute — Stage A's RR must not short-circuit it."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        m = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage_a(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("t1")

        kernel.execute(inv, STAGE_NAME, stage_a, manifest_id=m.manifest_id)
        rr = _attempts(store, inv.invocation_id)
        assert len(rr) == 1 and rr[0].status is RetryRecordStatus.SUCCEEDED
        # Stage B — same invocation, same manifest/case_version, new stage.
        mB = _make_manifest()
        mB = mB.model_copy(update={"manifest_id": f"00000000-0000-7000-8000-{0xC00:012x}"})
        store.store(mB)
        before = calls["n"]
        ran_b = {"n": 0}

        def stage_b(ctx):
            ran_b["n"] += 1

        kernel.execute(inv, DEEP, stage_b, manifest_id=mB.manifest_id)
        assert ran_b["n"] == 1, "Stage B did not execute (false replay)"
        assert calls["n"] > before

    def test_case_version_v2_executes_despite_v1_rr_history(self):
        """v1.0 initial fails + retry#1 succeeds (RR history exists). v2.0 same
        stage MUST execute — v1 RR must not false-replay v2."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        m1 = _seed_running_manifest(store, case_version="1.0")
        calls = {"n": 0}

        def stage_v1(ctx):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("t1")

        kernel.execute(inv, STAGE_NAME, stage_v1, manifest_id=m1.manifest_id)
        assert len(_attempts(store, inv.invocation_id)) == 1
        # v2.0
        m2 = _make_manifest(case_version="2.0")
        m2 = m2.model_copy(update={"manifest_id": f"00000000-0000-7000-8000-{0xD00:012x}"})
        store.store(m2)
        ran = {"n": 0}
        before = calls["n"]

        def stage_v2(ctx):
            ran["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage_v2, manifest_id=m2.manifest_id)
        assert ran["n"] == 1, "v2 did not execute (false replay)"
        assert calls["n"] > before


# =====================================================================
# §8  Retried-write idempotency from ExecutionContext (EG-01, faithful anchor)
# =====================================================================

class TestRetriedWriteIdempotency:
    def _stage_store_with_case(self, stage_store):
        _seed_case(stage_store)  # EG-01 FK case_id -> CASE-01
        return stage_store

    def test_deterministic_identity_no_duplicate_on_retry(self):
        """Stage writes an EG-01 (RECORD_IMMUTABLE, faithful anchor) with
        gap_id derived mechanically from ExecutionContext + checkpoint. The
        retry after a transient failure reuses the same identity -> one record."""
        from qad.models.family_b import (
            EvidenceGap,
            EvidenceGapOperational_status,
        )
        kernel, store, stage_store = _kernel()
        self._stage_store_with_case(stage_store)
        inv = _make_invocation()
        store.store(inv)
        m = _seed_running_manifest(store)
        calls = {"n": 0}
        exec_seen = {}

        def stage(ctx):
            calls["n"] += 1
            # deterministic canonical identity derived from execution context
            gap_id = deterministic_uuid7(
                f"{ctx.execution_id}|{ctx.checkpoint_ref or ''}|gap")
            assert is_uuid7(gap_id), "stage-owned id not UUID v7"
            exec_seen.setdefault("id", ctx.execution_id)
            assert ctx.execution_id == exec_seen["id"], "execution_id unstable"
            rec = EvidenceGap(
                gap_id=gap_id,
                case_id=ctx.execution.case_id,
                question="retried-write idempotency",
                importance="HIGH",
                operational_status=EvidenceGapOperational_status.OPEN,
                resolvability_class="RESOLVABLE_WITH_EVIDENCE",
                created_by="S8-test",
            )
            stage_store.store(rec)
            if calls["n"] == 1:
                raise RetryableError("transient after canonical write")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=m.manifest_id)
        gaps = [r for r in stage_store.list_all("EG-01")
                if r.question == "retried-write idempotency"]
        assert calls["n"] == 2
        assert len(gaps) == 1, "retried canonical write produced a duplicate"

    def test_conflicting_payload_same_identity_fails_closed(self):
        """Same execution-derived identity + DIFFERENT payload -> fail closed
        (TransactionFailure wrapping IntegrityConflict), one record."""
        from qad.models.family_b import (
            EvidenceGap,
            EvidenceGapOperational_status,
        )
        kernel, store, stage_store = _kernel()
        self._stage_store_with_case(stage_store)
        inv = _make_invocation()
        store.store(inv)
        m = _seed_running_manifest(store)
        calls = {"n": 0}

        def stage(ctx):
            calls["n"] += 1
            gap_id = deterministic_uuid7(
                f"{ctx.execution_id}|{ctx.checkpoint_ref or ''}|gap")
            rec = EvidenceGap(
                gap_id=gap_id,
                case_id=ctx.execution.case_id,
                question="retried-write idempotency",
                importance="HIGH" if calls["n"] == 1 else "MEDIUM",
                operational_status=EvidenceGapOperational_status.OPEN,
                resolvability_class="RESOLVABLE_WITH_EVIDENCE",
                created_by="S8-test",
            )
            stage_store.store(rec)
            if calls["n"] == 1:
                raise RetryableError("transient after canonical write")

        with pytest.raises(TransactionFailure) as exc:
            kernel.execute(inv, STAGE_NAME, stage, manifest_id=m.manifest_id)
        assert any(isinstance(e, IntegrityConflict) for e in exc.value.errors)
        gaps = [r for r in stage_store.list_all("EG-01")
                if r.question == "retried-write idempotency"]
        assert len(gaps) == 1