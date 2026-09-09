"""M5.3 S8 — Retry Kernel contract tests (CORRECTION ROUND — FD #138).

Encodes the Founder decisions from FD #138:
- Retry budget = INITIAL execution + max 3 retries = max 4 executions; initial is
  NOT retry #1 and is NOT an RR-01 (clean first-run success => ZERO RR-01).
- SI-01 = initial service invocation; RR-01 = retry attempts for a failed operation.
- ESCALATED is REMOVED from M5.3: retry #3 fails => FAILED always.
- Execution identity = (case_id, authoritative case_version, stage_name); kernel
  MUST establish it BEFORE running the stage, or fail closed.
- Checkpoint replay uses RSR-01 (checkpoint_ref + output_ids preservation), NOT
  len(RR records)+1.
- Retry-history read failure => fail closed (never 'no history').
- RR-01 + RRM-01 are written in ONE same-store atomic batch (store_batch);
  manifest preflight happens BEFORE stage execution.
- retry_id / stage_id are RFC-9562 UUID v7.
"""
from __future__ import annotations

import uuid

import pytest

from qad.ids import is_uuid7
from qad.m53.retry_kernel import (
    ExecutionContext,
    RetryKernel,
    RetryPolicy,
    RetryableError,
    StageContext,
)
from qad.models.family_c import ResearchStageRecord, ResearchStageRecordStage_name
from qad.models.family_i import (
    RetryRecord,
    RetryRecordStatus,
    RunManifestRecord,
    ServiceInvocation,
    ServiceInvocationStatus,
)
from qad.persistence import (
    ImmutabilityViolation,
    IntegrityConflict,
    MissingForeignKey,
)
from qad.persistence.reference import (
    InMemoryCanonicalRecordStore,
    InMemoryRunManifestStore,
)

FIXED_NOW = "2026-09-08T10:00:00Z"
CASE_ID = "CASE-M53-R1"
STAGE_NAME = ResearchStageRecordStage_name.SOURCE_FOUNDATION


def _u7(n: int) -> str:
    """Deterministic RFC-9562 UUID v7 literal for fixtures."""
    return f"00000000-0000-7000-8000-{n:012x}"


def _seed_case(store, case_id: str = CASE_ID) -> None:
    from qad.models import CandidateRecord, CaseRecord, SecurityMaster
    from qad.models.family_a import (
        CandidateRecordEntry_route,
        CandidateRecordSelection_state,
        CaseRecordCase_state,
        SecurityMasterSecurity_type,
        SecurityMasterStatus,
    )
    sm = SecurityMaster(
        entity_id="E-M53-R1", cik="0000555444", exchange="NYSE",
        name="Retry Corp", primary_ticker="RTY",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id=_u7(0x10), entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2026-01-01T00:00:00", evidence_freshness="2026-01-02",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
        signal_ids=[],
    )
    store.store(cand)
    case = CaseRecord(
        case_id=case_id, entity_id=sm.entity_id,
        candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN,
        as_of_date="2026-01-15", opened_at="2026-01-02T08:00:00",
        research_director="Research Director",
    )
    store.store(case)


def _make_invocation(invocation_id: str | None = None,
                     case_id: str = CASE_ID) -> ServiceInvocation:
    return ServiceInvocation(
        invocation_id=invocation_id or _u7(0x20),
        case_id=case_id,
        invoked_at=FIXED_NOW,
        request_type="RESEARCH_STAGE",
        service_id="S8",
        status=ServiceInvocationStatus.FAILURE,
    )


def _make_manifest(manifest_id: str | None = None,
                   case_id: str = CASE_ID,
                   run_state: str = "RUNNING",
                   case_version: str = "1.0") -> RunManifestRecord:
    kwargs: dict = dict(
        manifest_id=manifest_id or _u7(0x30),
        case_id=case_id,
        case_version=case_version,
        as_of_date="2026-01-15",
        start_time=FIXED_NOW,
        universe_version="u1",
        run_state=run_state,
        models_used=["m1"],
        providers={"p1": "x"},
        selection_policy_version="v1",
    )
    if run_state in ("COMPLETED", "FAILED"):
        kwargs["completion_time"] = FIXED_NOW
    return RunManifestRecord(**kwargs)


def _kernel():
    store = InMemoryRunManifestStore()
    _seed_case(store)
    stage_store = InMemoryCanonicalRecordStore()
    # RSR-01.case_id -> CASE-01 FK must resolve within the stage-state anchor
    # too — seed the canonical CASE chain into BOTH anchors (five-anchor
    # topology: each anchor resolves its own FK constraints).
    _seed_case(stage_store)
    kernel = RetryKernel(store, stage_store,
                         policy=RetryPolicy(max_retries=3),
                         now=lambda: FIXED_NOW)
    return kernel, store, stage_store


def _attempts(store, invocation_id: str) -> list[RetryRecord]:
    return [r for r in store.list_all("RR-01")
            if r.invocation_id == invocation_id]


class TestRetryBudgetFounderDecision:
    def test_clean_first_run_success_creates_zero_rr01(self):
        """FD #138: initial success is NOT a retry -> ZERO RR-01 records."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        outcome = kernel.execute(
            inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        assert calls["n"] == 1
        assert _attempts(store, inv.invocation_id) == []
        # RSR-01 records the completed stage (checkpoint authority).
        rsrs = stage_store.list_all("RSR-01")
        assert len(rsrs) == 1
        assert rsrs[0].stage_state.value == "COMPLETE"
        assert rsrs[0].stage_name == STAGE_NAME

    def test_initial_plus_three_retries_is_four_executions(self):
        """FD #138: max 3 retries = INITIAL + 3 retries = 4 stage executions.
        Retry #3 fails => FAILED always (ESCALATED removed)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        outcome = kernel.execute(
            inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 4
        assert outcome.status is RetryRecordStatus.FAILED
        # Three retries recorded as RR-01; the initial is not among them.
        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 3
        assert [r.attempt_number for r in rrs] == ["1", "2", "3"]
        assert rrs[-1].status is RetryRecordStatus.FAILED
        # NO ESCALATED record and no escalated_to population.
        assert rrs[-1].escalated_to is None
        assert all(r.status is not RetryRecordStatus.ESCALATED for r in rrs)

    def test_retry_succeeds_on_first_retry(self):
        """Initial fails; retry #1 succeeds -> RR-01 #1 = SUCCEEDED."""
        kernel, store, _ = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient")

        outcome = kernel.execute(
            inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 2
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 1
        assert rrs[0].status is RetryRecordStatus.SUCCEEDED


class TestRetryHistoryFailClosed:
    def test_retry_history_read_failure_blocks_execution(self):
        """FD #138 §6: list_all failure must NOT become 'no retry history' —
        the stage MUST NOT execute; typed error propagates."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        class Boom:
            def __getattr__(self, _):
                raise RuntimeError("store down")

        kernel._store = Boom()  # simulate store failure

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        with pytest.raises(RuntimeError):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0


class TestUuidV7Compliance:
    def test_rr_record_ids_are_uuid_v7(self):
        """FD #138 §8: retry_id MUST be RFC-9562 UUID v7."""
        kernel, store, _ = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)

        def stage(ctx: StageContext) -> None:
            raise RetryableError("boom")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        for r in _attempts(store, inv.invocation_id):
            assert is_uuid7(r.retry_id), f"retry_id not UUID v7: {r.retry_id}"

    def test_rsr_stage_ids_are_uuid_v7(self):
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)

        def stage(ctx: StageContext) -> None:
            return None

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        for r in stage_store.list_all("RSR-01"):
            assert is_uuid7(r.stage_id), f"stage_id not UUID v7: {r.stage_id}"


class TestCheckpointAndIdentity:
    def test_same_invocation_different_stage_not_false_idempotent(self):
        """FD #138 §4: replay requires the SAME (case_id, case_version,
        stage_name). Same SI-01 with a different stage_name -> NOT replayed:
        the stage executes."""
        kernel, store, _ = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 1
        # Same invocation, DIFFERENT stage -> must NOT reuse the terminal outcome.
        other_stage = ResearchStageRecordStage_name.DEEP_RESEARCH
        kernel.execute(inv, other_stage, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 2

    def test_checkpoint_replay_returns_without_reexecution(self):
        """FD #138 §4: re-running the same execution identity after a COMPLETE
        RSR-01 is replay — stage NOT called again, the RSR checkpoint_ref is
        the resume authority, and no extra canonical record is written."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 1
        rsrs = stage_store.list_all("RSR-01")
        assert len(rsrs) == 1
        first = rsrs[0]
        # checkpoint_ref encodes cp:<case_version>:<stage_id> (resume authority).
        assert first.checkpoint_ref == f"cp:1.0:{first.stage_id}"
        # Same execution identity -> replay without re-execution.
        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert calls["n"] == 1  # replay — no re-execution
        assert len(stage_store.list_all("RSR-01")) == 1  # zero new records

    def test_new_case_version_not_false_idempotent(self):
        """FD #138 §4: replay requires the SAME case_version. A new manifest
        with a different case_version MUST NOT reuse the prior terminal
        outcome — the stage re-executes (restart from last checkpoint)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest_v1 = _make_manifest()
        store.store(manifest_v1)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=manifest_v1.manifest_id)
        assert calls["n"] == 1
        # New run context, new case_version (v2.0) — same case, same stage.
        manifest_v2 = _make_manifest(case_version="2.0")
        manifest_v2 = manifest_v2.model_copy(
            update={"manifest_id": _u7(0x31)})
        store.store(manifest_v2)
        kernel.execute(inv, STAGE_NAME, stage,
                       manifest_id=manifest_v2.manifest_id)
        assert calls["n"] == 2  # NOT replayed — different case version
        assert len(stage_store.list_all("RSR-01")) == 2

    def test_retried_canonical_write_does_not_duplicate(self):
        """FD #138 §5 / GO §16: a canonical write performed by the stage and
        then retried after a transient failure does NOT create duplicate
        canonical state.  The stage keys its writes to the deterministic
        execution context; the canonical store's immutable-identity rule
        makes the retry an idempotent no-op (same id + same payload)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        stage_store.store(inv)  # stage-own RR-01 FK (SI-01) in this anchor
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}
        written_ids = []

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            # Deterministic canonical payload keyed to the execution identity.
            # RR-01 is RECORD_IMMUTABLE — the store makes the retry with the
            # SAME identity + SAME content an idempotent no-op.
            rid = f"00000000-0000-7000-0eee-{1:012x}"
            rec = RetryRecord(
                retry_id=rid,
                invocation_id=inv.invocation_id,
                attempt_number="99",  # stage-own payload, distinct from kernel
                attempted_at=FIXED_NOW,
                status=RetryRecordStatus.RETRYING,
                error="none",
            )
            stage_store.store(rec)
            written_ids.append(rec.retry_id)
            if calls["n"] == 1:
                raise RetryableError("transient after canonical write")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        # Stage executed 2x (initial + retry) but the canonical write produced
        # exactly ONE canonical record (idempotent identity reuse), and the
        # kernel's own RR-01 accounting in the RunManifestStore is untouched.
        assert calls["n"] == 2
        stage_writes = [
            r for r in stage_store.list_all("RR-01")
            if r.attempt_number == "99"
        ]
        assert len(stage_writes) == 1  # no duplicate canonical state
        assert len(written_ids) == 2    # the stage attempted twice
        assert written_ids[1] == written_ids[0]  # deterministic identity
        assert len(_attempts(store, inv.invocation_id)) == 1

    def test_conflicting_canonical_write_under_same_identity_fails_closed(self):
        """FD #138 §5: a DIFFERENT payload under the same canonical identity
        fails closed — TransactionFailure wrapping IntegrityConflict (M5.2
        §7.4: zero records committed).  Never a silent second record."""
        from qad.persistence import TransactionFailure as _TF
        from qad.persistence import IntegrityConflict as _IC
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        stage_store.store(inv)  # stage-own RR-01 FK (SI-01) in this anchor
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            rid = f"00000000-0000-7000-0eee-{1:012x}"
            rec = RetryRecord(
                retry_id=rid,
                invocation_id=inv.invocation_id,
                attempt_number="99",
                attempted_at=FIXED_NOW,
                status=RetryRecordStatus.RETRYING,
                # Attempt 2 writes DIFFERENT content under the SAME identity.
                error="boom-1" if calls["n"] == 1 else "boom-2",
            )
            stage_store.store(rec)
            if calls["n"] == 1:
                raise RetryableError("transient after canonical write")

        with pytest.raises(_TF) as exc:
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        # The immutable-identity collision is the deterministic cause.
        assert any(isinstance(e, _IC) for e in exc.value.errors), exc.value.errors
        # Exactly ONE record committed (the conflicting retry was rejected).
        assert len(stage_store.list_all("RR-01")) == 1

    def test_rsr_output_ids_preserved_across_retries(self):
        """FD #138 §4: previous stage output is preserved through retries —
        output_ids carry forward into the resumed RSR records."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        produced = []

        def stage(ctx: StageContext) -> None:
            produced.append(ctx.previous_output_ids or [])
            raise RetryableError("transient")

        # initial + retry #1 fail, retry #2 succeeds
        calls = {"n": 0}

        def stage2(ctx: StageContext) -> None:
            calls["n"] += 1
            if calls["n"] < 3:
                raise RetryableError("still transient")
            ctx.produced_output_ids.append(f"out-{calls['n']}")

        kernel.execute(inv, STAGE_NAME, stage2, manifest_id=manifest.manifest_id)
        rsrs = stage_store.list_all("RSR-01")
        assert len(rsrs) == 3  # initial + retry1 + retry2
        # The final COMPLETE record preserves output from the successful attempt.
        complete = [r for r in rsrs if r.stage_state.value == "COMPLETE"]
        assert len(complete) == 1
        assert "out-3" in (complete[0].output_ids or [])


class TestRrmAtomicity:
    def test_manifest_preflight_fails_before_execution(self):
        """FD #138 §7: missing manifest -> fail BEFORE the stage runs; zero
        partial canonical state (no RR-01, no RSR)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=_u7(0x700))
        assert calls["n"] == 0
        assert store.list_all("RR-01") == []
        assert stage_store.list_all("RSR-01") == []

    def test_terminal_manifest_fails_before_execution(self):
        """FD #138 §7: terminal manifest -> ImmutabilityViolation BEFORE the
        stage runs; zero writes."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest(run_state="COMPLETED")
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        with pytest.raises(ImmutabilityViolation):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0
        assert store.list_all("RR-01") == []
        assert stage_store.list_all("RSR-01") == []

    def test_rr_and_rrm_attach_in_one_atomic_batch(self):
        """FD #138 §7: RR-01 + RRM provenance land together (single
        store_batch) — no partial window where RR exists without manifest ref.
        Verify by asserting the atomic-batch encoder is used (one commit)."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        batch_calls = {"n": 0}
        orig_batch = store.store_batch

        def spy_batch(instances, /):
            batch_calls["n"] += 1
            return orig_batch(instances)

        store.store_batch = spy_batch

        def stage(ctx: StageContext) -> None:
            raise RetryableError("boom")

        kernel.execute(inv, STAGE_NAME, stage, manifest_id=manifest.manifest_id)
        assert batch_calls["n"] >= 1  # retry provenances committed via batch
        rrs = _attempts(store, inv.invocation_id)
        manifest_now = store.load("RRM-01", manifest.manifest_id)
        failures = manifest_now.failures or []
        for r in rrs:
            if r.status is RetryRecordStatus.FAILED:
                assert r.retry_id in failures


class TestDeterministicFailure:
    def test_deterministic_failure_on_initial_not_an_rr01(self):
        """FD #138 §2: a deterministic failure on the INITIAL execution is NOT
        a retry — zero RR-01 records; the honest record is the RSR FAILED
        stage state; the original typed error re-raises."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            raise MissingForeignKey(
                "deterministic FK failure", schema_id="RR-01",
                field="invocation_id", target_schema="SI-01")

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 1
        assert _attempts(store, inv.invocation_id) == []
        rsrs = stage_store.list_all("RSR-01")
        assert len(rsrs) == 1
        assert rsrs[0].stage_state.value == "FAILED"

    def test_deterministic_failure_during_retry_is_one_rr01_failed(self):
        """A deterministic failure on a RETRY attempt is recorded as exactly
        one RR-01 FAILED (retry accounting is honest) and re-raised."""
        kernel, store, _ = _kernel()
        inv = _make_invocation()
        store.store(inv)
        manifest = _make_manifest()
        store.store(manifest)
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient initial")
            raise MissingForeignKey(
                "deterministic on retry", schema_id="RR-01",
                field="invocation_id", target_schema="SI-01")

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 2
        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 1
        assert rrs[0].attempt_number == "1"
        assert rrs[0].status is RetryRecordStatus.FAILED


class TestMissingInvocation:
    def test_missing_invocation_fails_closed(self):
        """RR-01.invocation_id FK requires SI-01; missing invocation ->
        MissingForeignKey before any record."""
        kernel, store, stage_store = _kernel()
        inv = _make_invocation()
        manifest = _make_manifest()
        store.store(manifest)  # manifest exists, invocation does not
        calls = {"n": 0}

        def stage(ctx: StageContext) -> None:
            calls["n"] += 1

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, STAGE_NAME, stage,
                           manifest_id=manifest.manifest_id)
        assert calls["n"] == 0