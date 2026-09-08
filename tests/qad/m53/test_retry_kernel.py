"""M5.3 S8 — Retry Kernel contract tests (direct, not regression).

Proves the frozen retry semantics on the canonical RunManifestStore:
bounded per-stage retry, immutable per-attempt RR-01 records, idempotent
replay, deterministic-failure no-retry, RRM integration honesty, and zero
unauthorized partial canonical state.
"""
from __future__ import annotations

import pytest

from qad.m53.retry_kernel import RetryKernel, RetryPolicy, RetryableError
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
from qad.persistence.reference import InMemoryRunManifestStore

FIXED_NOW = "2026-09-08T10:00:00Z"
CASE_ID = "CASE-M53-R1"


def _seed_case(store, case_id: str = CASE_ID) -> None:
    """Seed the canonical CASE chain (SM-01 -> CR-01 -> CASE-01) that the
    SI-01 / RRM-01 records FK against."""
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
        candidate_id="CAND-M53-R1", entity_id=sm.entity_id,
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


def _make_invocation(invocation_id: str = "SI-M53-001",
                     case_id: str = CASE_ID) -> ServiceInvocation:
    return ServiceInvocation(
        invocation_id=invocation_id,
        case_id=case_id,
        invoked_at=FIXED_NOW,
        request_type="RESEARCH_STAGE",
        service_id="S8",
        status=ServiceInvocationStatus.FAILURE,
    )


def _make_manifest(manifest_id: str = "RRM-M53-001",
                   case_id: str = CASE_ID,
                   run_state: str = "RUNNING") -> RunManifestRecord:
    kwargs: dict = dict(
        manifest_id=manifest_id,
        case_id=case_id,
        case_version="1.0",
        as_of_date="2026-01-15",
        start_time=FIXED_NOW,
        universe_version="u1",
        run_state=run_state,
        models_used=["m1"],
        providers={"p1": "x"},
        selection_policy_version="v1",
    )
    # INV-RRM-01: terminal manifests REQUIRE completion_time.
    if run_state in ("COMPLETED", "FAILED"):
        kwargs["completion_time"] = FIXED_NOW
    return RunManifestRecord(**kwargs)


def _kernel(max_attempts: int = 3):
    store = InMemoryRunManifestStore()
    _seed_case(store)
    return RetryKernel(store, policy=RetryPolicy(max_attempts=max_attempts),
                       now=lambda: FIXED_NOW), store


def _attempts(store, invocation_id: str) -> list[RetryRecord]:
    return store.list_all("RR-01") and [
        r for r in store.list_all("RR-01")
        if r.invocation_id == invocation_id
    ] or []


# =====================================================================
# Tests
# =====================================================================

class TestRetryLifecycle:
    def test_retryable_failure_enters_retrying(self):
        """A transient failure schedules a retry -> an RR-01 with
        status=RETRYING is recorded (attempt 1)."""
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            if calls["n"] == 1:
                raise RetryableError("transient network failure")
            return None

        outcome = kernel.execute(inv, stage)
        records = _attempts(store, inv.invocation_id)
        assert len(records) == 2
        assert records[0].status is RetryRecordStatus.RETRYING
        assert records[1].status is RetryRecordStatus.SUCCEEDED
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        assert outcome.retried is True

    def test_success_after_retry_is_succeeded(self):
        """Second attempt succeeds -> final RR-01 SUCCEEDED; outcome SUCCEEDED."""
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            if calls["n"] < 2:
                raise RetryableError("backoff")
            return None

        outcome = kernel.execute(inv, stage)
        assert outcome.status is RetryRecordStatus.SUCCEEDED
        records = _attempts(store, inv.invocation_id)
        assert [r.status for r in records] == [
            RetryRecordStatus.RETRYING, RetryRecordStatus.SUCCEEDED,
        ]

    def test_retry_exhaustion_is_failed(self):
        """Transient failure on every attempt; budget exhausted -> FAILED
        (frozen rule: max 3 retries, after 3 -> FAILED)."""
        kernel, store = _kernel(max_attempts=3)
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            raise RetryableError(f"boom {calls['n']}")

        outcome = kernel.execute(inv, stage)
        assert outcome.status is RetryRecordStatus.FAILED
        records = _attempts(store, inv.invocation_id)
        assert len(records) == 3
        assert [r.status for r in records] == [
            RetryRecordStatus.RETRYING,
            RetryRecordStatus.RETRYING,
            RetryRecordStatus.FAILED,
        ]
        assert calls["n"] == 3

    def test_retry_exhaustion_with_escalation(self):
        """When the caller supplies escalated_to at exhaustion -> ESCALATED
        with the target recorded; no fake completion timestamp."""
        kernel, store = _kernel(max_attempts=2)
        inv = _make_invocation()
        store.store(inv)

        def stage():
            raise RetryableError("persistent")

        outcome = kernel.execute(inv, stage, escalated_to="FOUNDER")
        assert outcome.status is RetryRecordStatus.ESCALATED
        records = _attempts(store, inv.invocation_id)
        assert records[-1].status is RetryRecordStatus.ESCALATED
        assert records[-1].escalated_to == "FOUNDER"
        assert records[-1].attempted_at == FIXED_NOW  # honest real timestamp

    def test_deterministic_failure_not_retried(self):
        """A deterministic validation/fk failure is NOT retried: a single
        FAILED attempt, stage called exactly once, error class preserved."""
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            raise MissingForeignKey(
                "deterministic FK failure", schema_id="RR-01",
                field="invocation_id", target_schema="SI-01",
            )

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, stage)

        assert calls["n"] == 1            # no blind retry
        records = _attempts(store, inv.invocation_id)
        assert len(records) == 1
        assert records[0].status is RetryRecordStatus.FAILED
        assert "MissingForeignKey" in records[0].error


class TestRetryIdempotency:
    def test_duplicate_retry_produces_no_duplicate_canonical_record(self):
        """Executing the same invocation twice (terminal outcome) yields the
        same record set — no duplicate canonical RR-01 records."""
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            return None

        o1 = kernel.execute(inv, stage)
        o2 = kernel.execute(inv, stage)   # replay
        assert calls["n"] == 1            # stage NOT re-run
        assert o2.status is RetryRecordStatus.SUCCEEDED
        assert len(o1.attempt_records) == len(o2.attempt_records) == 1
        ids = {r.retry_id for r in o2.attempt_records}
        assert len(ids) == 1              # one canonical record total

    def test_same_payload_retry_is_idempotent(self):
        """Same invocation + same outcome replay returns the existing outcome
        with identical canonical hashes — zero new writes."""
        kernel, store = _kernel(max_attempts=2)
        inv = _make_invocation()
        store.store(inv)

        def stage():
            raise RetryableError("transient")

        o1 = kernel.execute(inv, stage)   # attempt 1 RETRYING, attempt 2 FAILED
        h1 = [store.get_canonical_hash("RR-01", r.retry_id)
              for r in o1.attempt_records]
        o2 = kernel.execute(inv, stage)   # replay
        h2 = [store.get_canonical_hash("RR-01", r.retry_id)
              for r in o2.attempt_records]
        assert h1 == h2
        assert len(o1.attempt_records) == len(o2.attempt_records) == 2

    def test_conflicting_payload_under_immutable_identity_fails(self):
        """A caller-supplied retry_id that already exists with DIFFERENT
        content is NOT a harmless retry -> the canonical store's immutable-
        identity protection fires (Inner IntegrityConflict wrapped in
        TransactionFailure) — the kernel never suppresses it (fail closed).

        The colliding record belongs to a DIFFERENT invocation so the kernel
        does not short-circuit on its (terminal) idempotent-replay path —
        it MUST attempt the write and collide at the canonical store.
        """
        from qad.persistence import IntegrityConflict as _IC
        from qad.persistence import TransactionFailure as _TF
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        other = _make_invocation("SI-OTHER-001")
        store.store(other)
        # Pre-existing immutable record under the retry_id the caller reuses.
        store.store(RetryRecord(
            retry_id="RR-CONFLICT-1", invocation_id=other.invocation_id,
            attempt_number="1", attempted_at=FIXED_NOW,
            status=RetryRecordStatus.FAILED, error="original content",
        ))
        calls = {"n": 0}

        def stage():
            calls["n"] += 1
            raise RetryableError("different content")

        with pytest.raises(_TF) as exc:
            kernel.execute(inv, stage, retry_id="RR-CONFLICT-1")
        # The store rejects the immutable-identity collision deterministically.
        assert any(isinstance(e, _IC) for e in exc.value.errors), exc.value.errors
        # No unauthorized partial canonical state: the original record stands.
        assert len(_attempts(store, other.invocation_id)) == 1

    def test_missing_invocation_fails_closed(self):
        """RR-01 requires SI-01; a missing invocation -> MissingForeignKey,
        no attempt records written."""
        kernel, store = _kernel()
        inv = _make_invocation("SI-NO-SUCH")

        def stage():
            return None

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, stage)
        assert store.list_all("RR-01") == []


class TestRrmIntegration:
    def test_rrm_reflects_honest_retry_state(self):
        """The RUNNING manifest accumulates retry provenance:
        RETRYING refs -> retries; terminal FAILED ref -> failures."""
        kernel, store = _kernel(max_attempts=2)
        inv = _make_invocation()
        store.store(inv)
        store.store(_make_manifest("RRM-M53-RR"))

        def stage():
            raise RetryableError("transient")

        outcome = kernel.execute(inv, stage, manifest_id="RRM-M53-RR")
        manifest = store.load("RRM-01", "RRM-M53-RR")
        assert outcome.status is RetryRecordStatus.FAILED
        retry_refs = [x.strip() for x in (manifest.retries or "").split(",") if x.strip()]
        assert len(retry_refs) == 1           # RETRYING attempt 1
        assert len(manifest.failures or []) == 1  # FAILED attempt 2
        # manifest still RUNNING — finalization is the RRM owner's concern
        assert str(manifest.run_state.value) == "RUNNING"

    def test_terminal_manifest_remains_immutable(self):
        """Attaching retry provenance to a terminal manifest fails closed
        (ImmutabilityViolation) — no silent manifest mutation."""
        kernel, store = _kernel(max_attempts=1)
        inv = _make_invocation()
        store.store(inv)
        store.store(_make_manifest("RRM-M53-TERM", run_state="COMPLETED"))

        def stage():
            raise RetryableError("transient")

        with pytest.raises(ImmutabilityViolation):
            kernel.execute(inv, stage, manifest_id="RRM-M53-TERM")

    def test_missing_manifest_fails_closed(self):
        """A manifest_id that does not exist -> MissingForeignKey; the attempt
        record is still written BEFORE the attach attempt, then the run fails
        closed (no silent drop of provenance)."""
        kernel, store = _kernel(max_attempts=1)
        inv = _make_invocation()
        store.store(inv)

        def stage():
            raise RetryableError("transient")

        with pytest.raises(MissingForeignKey):
            kernel.execute(inv, stage, manifest_id="RRM-NO-SUCH")

    def test_retry_failure_leaves_no_unauthorized_partial_state(self):
        """A deterministic failure leaves exactly ONE honest FAILED RR-01 for
        the invocation (no RETRYING ghosts), the running manifest reflects the
        failure (authorized provenance), and nothing else is mutated."""
        kernel, store = _kernel()
        inv = _make_invocation()
        store.store(inv)
        store.store(_make_manifest("RRM-M53-PART"))

        def stage():
            raise IntegrityConflict("conflicting payload", schema_id="RR-01",
                                    record_id="RRM-PART")

        with pytest.raises(IntegrityConflict):
            kernel.execute(inv, stage, manifest_id="RRM-M53-PART")

        rrs = _attempts(store, inv.invocation_id)
        assert len(rrs) == 1
        assert rrs[0].status is RetryRecordStatus.FAILED
        assert rrs[0].escalated_to is None
        # The RUNNING manifest honestly reflects the failure (no ghost retry).
        manifest = store.load("RRM-01", "RRM-M53-PART")
        assert manifest.failures == ["RR-SI-M53-001-1"]
        assert manifest.retries in (None, "")