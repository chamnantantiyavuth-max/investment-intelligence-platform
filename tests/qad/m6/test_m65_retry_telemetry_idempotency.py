"""QAD M6.5 — RETRY / TELEMETRY / IDEMPOTENCY — acceptance suite (FD #148 §1/§3).

Covers the brief's required RED→GREEN criteria:

Idempotency (1–15) · Retry (16–35) · Telemetry (36–47) · M6.4 integration (48–52).

The module under test performs NO provider execution — there is no Gemini, no
Notebook, no browser/CDP, no network and no credential use here. Deterministic test
doubles are used only where execution behaviour must be exercised (a test-only
proof resolver, in the test boundary — never a production resolver).
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import os
import random
import socket
import time
import uuid

import pytest

from qad.contract.canonical_boundary import CANONICAL_SCHEMAS
from qad.models import CandidateRecord, CaseRecord, SecurityMaster
from qad.models.family_a import (
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecordCase_state,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
)
from qad.models.family_b import (
    EvidenceGapOperational_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_i import PITContext, PITContextMode
from qad.persistence.reference import InMemoryPITContextStore, InMemoryRawSourceArchive

from qad.m6.ledger import (
    DeepResearchRunLedgerStore,
    LedgerIdentityConflict,
    RetryMode,
    TerminalStatus,
)
from qad.m6.orchestration import (
    MAX_ATTEMPTS,
    NOT_EXPOSED_BY_PROVIDER,
    AttemptClassification,
    IdempotencyError,
    OrchestrationError,
    OrchestrationMode,
    ProviderSet,
    ResolutionOutcome,
    RetryPolicyError,
    accept_success_result,
    build_telemetry,
    classify_attempt_outcome,
    classify_result_status,
    compute_idempotency_key,
    decide_retry,
    exposed,
    idempotency_key_for_request,
    not_exposed,
    not_exposed_telemetry,
    plan_attempt,
    record_failed_attempt,
    resolve_or_create_logical_run,
    terminalize_research_unavailable,
)
from qad.m6.research_contract import (
    ClosedCorpusEnforcement,
    DeepResearchResult,
    IsolationVerification,
    ProofKind,
    ProofVerification,
    ProofVerificationRequest,
    ResearchResultError,
    ResearchResultStatus,
    SourcePointer,
    build_deep_research_request,
    build_deep_research_result,
    compute_result_sha256,
)
from qad.m6.snapshot import SEALED_PIT_MODE, build_sealed_input_snapshot

AS_OF = "2026-01-01"
ADMITTED = "2025-12-15T00:00:00+00:00"
_FIXED_NOW = dt.datetime(2026, 10, 9, 12, 0, 0, tzinfo=dt.timezone.utc)
_PAYLOAD = b"orchestration synthesis [1][2]"
_POINTERS = (
    SourcePointer(index=1, reference="https://a.example/1"),
    SourcePointer(index=2, reference="https://b.example/2"),
)

_UNSET = object()


# =====================================================================
# Fixtures
# =====================================================================

@pytest.fixture()
def store(tmp_path) -> DeepResearchRunLedgerStore:
    return DeepResearchRunLedgerStore(
        tmp_path / "m65-ledger.sqlite3", clock=lambda: _FIXED_NOW
    )


def _keys(**overrides) -> dict:
    base = dict(
        case_id="CASE-1",
        case_version="v1",
        evidence_gap_id="EG-1",
        request_payload_hash="a" * 64,
        input_snapshot_hash="b" * 64,
    )
    base.update(overrides)
    return base


def _create_kwargs(key: str, **overrides) -> dict:
    kw = dict(
        ledger_id="L-1",
        research_run_id="RR-1",
        rrm_manifest_id="RRM-2026-0001",
        case_id="CASE-1",
        case_version="v1",
        evidence_gap_id="EG-1",
        request_id="REQ-1",
        idempotency_key=key,
        notebook_identity="nb-0193-1",
        pit_context_id="PITC-1",
        pit_mode=SEALED_PIT_MODE,
        as_of=AS_OF,
        input_snapshot_hash="b" * 64,
        provider_surface="gemini_notebook",
        transport_type="BROWSER_UI_AUTOMATION",
    )
    kw.update(overrides)
    return kw


def _tel() -> dict:
    return not_exposed_telemetry()


def _append(store, ledger_id="L-1", n=1, mode=RetryMode.INITIAL_ATTEMPT,
            outcome="TRANSPORT_FAILURE", provider="gemini_notebook"):
    store.append_attempt(
        ledger_id, attempt_number=n, retry_mode=mode, provider_surface=provider,
        transport_type="BROWSER_UI_AUTOMATION", completed_at=_FIXED_NOW.isoformat(),
        outcome=outcome, error="boom", telemetry=_tel(),
    )


# ---- M6.4 SUCCESS fixture (test-only resolver; never production) -------------

def _src(sid: str, raw: bytes) -> SourceRecord:
    return SourceRecord(
        source_id=sid,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/{sid}",
        content_hash=hashlib.sha256(raw).hexdigest(),
        retrieval_date="2025-12-01",
        publication_date="2025-11-20",
    )


def _seed_case(pit_store, case_id: str) -> None:
    sm = SecurityMaster(
        entity_id=f"SM-{case_id}", cik="0000998877", exchange="NYSE",
        name="M65 Orchestration Corp", primary_ticker="M65O",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    pit_store.store(sm)
    cand = CandidateRecord(
        candidate_id=f"CR-{case_id}", entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2025-10-01T00:00:00", evidence_freshness="2025-11-01",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW, signal_ids=[],
    )
    pit_store.store(cand)
    pit_store.store(CaseRecord(
        case_id=case_id, entity_id=sm.entity_id, candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN, as_of_date=AS_OF,
        opened_at="2025-10-02T08:00:00", research_director="Research Director",
    ))


def _snapshot():
    archive = InMemoryRawSourceArchive(clock=lambda: dt.datetime.fromisoformat(ADMITTED))
    pit_store = InMemoryPITContextStore()
    _seed_case(pit_store, "CASE-1")
    pit_store.store(PITContext(
        pit_context_id="PITC-1", case_id="CASE-1", as_of_date=AS_OF,
        mode=PITContextMode.SEALED_HISTORICAL_EVALUATION, created_by="founder",
    ))
    for sid, raw in (("S1", b"alpha"), ("S2", b"beta")):
        archive.admit_source(_src(sid, raw), raw)
    return build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
        case_version="v1", source_ids=["S1", "S2"],
    )


def _request(**overrides):
    kw = dict(
        snapshot=_snapshot(), request_id="REQ-1", research_run_id="RR-1",
        ledger_id="L-1", rrm_manifest_id="RRM-2026-0001", evidence_gap_id="EG-1",
        research_question="Why is the moat durable?",
        provider_surface="gemini_notebook",
    )
    kw.update(overrides)
    return build_deep_research_request(**kw)


class _StubProofResolver:
    """DETERMINISTIC TEST-ONLY resolver. NOT a production resolver."""

    def __init__(self, *, closed_corpus: bool = True, isolation: bool = True) -> None:
        self._closed_corpus = closed_corpus
        self._isolation = isolation

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        is_corpus = context.proof_kind is ProofKind.CLOSED_CORPUS_ENFORCEMENT
        verified = self._closed_corpus if is_corpus else self._isolation
        return ProofVerification(
            proof_kind=context.proof_kind,
            verified=verified,
            request_id=context.request_id,
            research_run_id=context.research_run_id,
            ledger_id=context.ledger_id,
            provider_surface=context.provider_surface,
            input_snapshot_hash=context.input_snapshot_hash,
            evidence_ref=context.evidence_ref if verified else None,
            failure_reason=None if verified else "stub: not verified",
        )


def _build_success(request, resolver=_UNSET) -> DeepResearchResult:
    kw = dict(
        request_id=request.request_id,
        research_run_id=request.research_run_id,
        ledger_id=request.ledger_id,
        status=ResearchResultStatus.SUCCESS,
        provider_surface=request.provider.provider_surface,
        result_bytes=_PAYLOAD,
        result_sha256=hashlib.sha256(_PAYLOAD).hexdigest(),
        source_pointers=_POINTERS,
        completed_at="2026-10-09T12:05:00+00:00",
        closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
        isolation_verification=IsolationVerification.VERIFIED,
        closed_corpus_evidence_ref="EVID-CORPUS-1",
        isolation_evidence_ref="EVID-ISOLATION-1",
        request=request,
        proof_resolver=_StubProofResolver() if resolver is _UNSET else resolver,
    )
    return build_deep_research_result(**kw)


# =====================================================================
# §12 Idempotency — key determinism (1–11)
# =====================================================================

class TestIdempotencyKey:
    def test_01_identical_logical_request_identical_key(self):
        assert compute_idempotency_key(**_keys()) == compute_idempotency_key(**_keys())

    @pytest.mark.parametrize(
        "field,value",
        [
            ("case_id", "CASE-2"),
            ("case_version", "v2"),
            ("stage", "S11"),
            ("evidence_gap_id", "EG-2"),
            ("request_payload_hash", "c" * 64),
            ("input_snapshot_hash", "d" * 64),
        ],
    )
    def test_02_to_07_each_field_changes_the_key(self, field, value):
        base = compute_idempotency_key(**_keys())
        assert compute_idempotency_key(**_keys(**{field: value})) != base

    def test_08_wall_clock_does_not_affect_the_key(self, monkeypatch):
        first = compute_idempotency_key(**_keys())
        monkeypatch.setattr(time, "time", lambda: 1.0)
        monkeypatch.setattr(time, "monotonic", lambda: 2.0)
        a = compute_idempotency_key(**_keys())
        monkeypatch.setattr(time, "time", lambda: 9_999_999.0)
        monkeypatch.setattr(time, "monotonic", lambda: 5.0)
        b = compute_idempotency_key(**_keys())
        assert first == a == b

    def test_09_uuid_and_random_identity_do_not_affect_the_key(self, monkeypatch):
        first = compute_idempotency_key(**_keys())
        monkeypatch.setattr(uuid, "uuid4", lambda: uuid.UUID(int=1))
        monkeypatch.setattr(random, "random", lambda: 0.111)
        monkeypatch.setattr(os, "getpid", lambda: 4242)
        a = compute_idempotency_key(**_keys())
        monkeypatch.setattr(uuid, "uuid4", lambda: uuid.UUID(int=2))
        monkeypatch.setattr(random, "random", lambda: 0.999)
        monkeypatch.setattr(os, "getpid", lambda: 9999)
        assert first == a == compute_idempotency_key(**_keys())

    def test_10_filesystem_path_does_not_affect_the_key(self, monkeypatch, tmp_path):
        first = compute_idempotency_key(**_keys())
        monkeypatch.chdir(tmp_path)
        via_cwd = compute_idempotency_key(**_keys())
        (tmp_path / "nested").mkdir()
        monkeypatch.chdir(tmp_path / "nested")
        assert first == via_cwd == compute_idempotency_key(**_keys())

    def test_11_provider_selection_does_not_affect_the_logical_key(self):
        base = compute_idempotency_key(**_keys())
        # provider set / mode are NOT inputs to the logical identity
        ProviderSet(("gemini_notebook",))
        ProviderSet(("gemini_notebook", "other_surface"))
        assert compute_idempotency_key(**_keys()) == base
        # two requests identical except the configured provider surface agree
        req_a = _request(provider_surface="gemini_notebook")
        req_b = _request(provider_surface="other_surface", request_id="REQ-2")
        assert idempotency_key_for_request(req_a) == idempotency_key_for_request(req_b)

    def test_key_matches_the_formula_field_set(self):
        key = compute_idempotency_key(**_keys())
        assert key.startswith("idem-") and len(key) == len("idem-") + 64
        assert all(c in "0123456789abcdef" for c in key[len("idem-"):])


# =====================================================================
# §12 Idempotency — one logical run (12–15)
# =====================================================================

class TestIdempotentResolution:
    def test_12_repeat_request_creates_no_second_logical_run(self, store):
        key = compute_idempotency_key(**_keys())
        first = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert first.outcome is ResolutionOutcome.CREATED
        second = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert second.outcome is ResolutionOutcome.EXISTING_ACTIVE
        assert second.ledger_id == first.ledger_id
        assert store.list_runs() == [first.ledger_id]
        assert len(store.list_runs()) == 1

    def test_13_racing_create_reconciles_to_the_existing_logical_run(
        self, store, monkeypatch
    ):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )

        def _lose_the_race(**kwargs):
            raise LedgerIdentityConflict("simulated concurrent duplicate create")

        monkeypatch.setattr(store, "create_run", _lose_the_race)
        raced = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert raced.outcome is ResolutionOutcome.EXISTING_ACTIVE
        assert raced.ledger_id == "L-1"
        assert len(store.list_runs()) == 1

    def test_13b_duplicate_idempotency_key_is_still_refused_by_the_ledger(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        # the M6.3 UNIQUE constraint is preserved, never weakened
        with pytest.raises(LedgerIdentityConflict):
            store.create_run(**_create_kwargs(key, ledger_id="L-2", research_run_id="RR-2"))

    def test_14_terminal_identical_request_does_not_execute_again(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        _append(store, n=1)
        terminalize_research_unavailable(store, ledger_id="L-1", failure_detail="exhausted")
        again = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert again.outcome is ResolutionOutcome.EXISTING_TERMINAL
        assert again.is_terminal is True
        assert again.may_attempt is False
        assert again.next_attempt_number is None
        assert again.terminal_status is TerminalStatus.RESEARCH_UNAVAILABLE
        assert len(store.list_runs()) == 1

    def test_15_retry_budget_cannot_be_reset_by_resubmission(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        _append(store, n=1)
        _append(store, n=2)
        again = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert again.attempts_recorded == 2
        assert again.next_attempt_number == 3
        assert again.retry_budget_remaining == 1
        _append(store, n=3)
        exhausted = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert exhausted.attempts_recorded == 3
        assert exhausted.next_attempt_number is None
        assert exhausted.retry_budget_remaining == 0
        assert exhausted.may_attempt is False

    def test_resolution_requires_kwargs_only_when_no_run_exists(self, store):
        key = compute_idempotency_key(**_keys())
        with pytest.raises(IdempotencyError):
            resolve_or_create_logical_run(store, idempotency_key=key)
        with pytest.raises(IdempotencyError):
            resolve_or_create_logical_run(
                store, idempotency_key=key,
                create_run_kwargs=_create_kwargs("idem-DIFFERENT"),
            )


# =====================================================================
# §13 Retry — Mode B (16–25)
# =====================================================================

class TestModeB:
    def _ps(self):
        return ProviderSet(("gemini_notebook",))

    def test_16_one_configured_provider_is_mode_b(self):
        assert self._ps().mode is OrchestrationMode.MODE_B

    def test_17_to_19_attempt_semantics_and_provider_identity(self):
        ps = self._ps()
        p1 = plan_attempt(provider_set=ps, attempt_number=1)
        p2 = plan_attempt(provider_set=ps, attempt_number=2,
                          previous_provider_surface=p1.provider_surface)
        p3 = plan_attempt(provider_set=ps, attempt_number=3,
                          previous_provider_surface=p2.provider_surface)
        assert p1.retry_mode is RetryMode.INITIAL_ATTEMPT
        assert p2.retry_mode is RetryMode.SAME_PROVIDER_RETRY
        assert p3.retry_mode is RetryMode.SAME_PROVIDER_RETRY
        # 20 — the provider stays identical on every Mode-B attempt
        assert len({p1.provider_surface, p2.provider_surface, p3.provider_surface}) == 1

    def test_21_mode_b_never_reports_provider_fallback(self):
        ps = self._ps()
        plans = [plan_attempt(provider_set=ps, attempt_number=1)]
        for n in (2, 3):
            plans.append(plan_attempt(
                provider_set=ps, attempt_number=n,
                previous_provider_surface=plans[-1].provider_surface,
            ))
        for plan in plans:
            assert plan.retry_mode is not RetryMode.PROVIDER_FALLBACK
            assert plan.fallback_used is False
            assert plan.provider_changed is False

    def test_22_attempt_four_is_impossible(self):
        ps = self._ps()
        with pytest.raises(RetryPolicyError):
            plan_attempt(provider_set=ps, attempt_number=4,
                         previous_provider_surface="gemini_notebook")
        assert MAX_ATTEMPTS == 3

    def test_23_exhaustion_ends_research_unavailable(self):
        ps = self._ps()
        for n in (1, 2):
            d = decide_retry(provider_set=ps, attempt_number=n,
                             outcome=TerminalStatus.TRANSPORT_FAILURE,
                             previous_provider_surface="gemini_notebook",
                             evidence_gap_id="EG-1")
            assert d.should_retry is True
            assert d.next_attempt.attempt_number == n + 1
            assert d.next_attempt.retry_mode is RetryMode.SAME_PROVIDER_RETRY
        last = decide_retry(provider_set=ps, attempt_number=3,
                            outcome=TerminalStatus.TRANSPORT_FAILURE,
                            previous_provider_surface="gemini_notebook",
                            evidence_gap_id="EG-1")
        assert last.should_retry is False
        assert last.terminal_status is TerminalStatus.RESEARCH_UNAVAILABLE

    def test_24_exhaustion_never_weakens_quality_or_evidence_gates(self):
        ps = self._ps()
        d = decide_retry(provider_set=ps, attempt_number=3,
                         outcome=TerminalStatus.RESEARCH_UNAVAILABLE,
                         previous_provider_surface="gemini_notebook",
                         evidence_gap_id="EG-1")
        assert d.evidence_gates_weakened is False
        with pytest.raises(RetryPolicyError):
            dataclasses.replace(d, evidence_gates_weakened=True)

    def test_25_exhaustion_surfaces_the_eg01_deferred_instruction(self):
        ps = self._ps()
        d = decide_retry(provider_set=ps, attempt_number=3,
                         outcome=TerminalStatus.TRANSPORT_FAILURE,
                         previous_provider_surface="gemini_notebook",
                         evidence_gap_id="EG-1")
        inst = d.evidence_gap_instruction
        assert inst is not None
        assert inst.evidence_gap_id == "EG-1"
        assert inst.schema_id == "EG-01"
        assert inst.to_status == EvidenceGapOperational_status.DEFERRED.value == "DEFERRED"
        assert inst.applied is False  # M6.5 never writes canonical EG state
        assert "FD #148" in inst.authority_ref


# =====================================================================
# §13 Retry — Mode A (26–31)
# =====================================================================

class TestModeA:
    def _ps(self):
        return ProviderSet(("surface_b", "surface_a"))

    def test_26_two_or_more_explicit_providers_is_mode_a(self):
        assert self._ps().mode is OrchestrationMode.MODE_A
        assert ProviderSet(("a", "b", "c")).mode is OrchestrationMode.MODE_A

    def test_27_different_provider_retry_records_provider_fallback(self):
        ps = self._ps()
        p1 = plan_attempt(provider_set=ps, attempt_number=1)
        p2 = plan_attempt(provider_set=ps, attempt_number=2,
                          previous_provider_surface=p1.provider_surface)
        assert p2.provider_surface != p1.provider_surface
        assert p2.retry_mode is RetryMode.PROVIDER_FALLBACK
        assert p2.fallback_used is True
        assert p2.provider_changed is True

    def test_28_fallback_flag_is_true_only_when_the_provider_really_changed(self):
        for providers in (("only_one",), ("a", "b"), ("a", "b", "c")):
            ps = ProviderSet(providers)
            previous = ps.default_provider
            for n in (2, 3):
                plan = plan_attempt(provider_set=ps, attempt_number=n,
                                    previous_provider_surface=previous)
                assert plan.fallback_used == plan.provider_changed
                assert (plan.retry_mode is RetryMode.PROVIDER_FALLBACK) == plan.provider_changed
                previous = plan.provider_surface

    def test_29_no_provider_is_ever_invented(self):
        ps = self._ps()
        p1 = plan_attempt(provider_set=ps, attempt_number=1)
        p2 = plan_attempt(provider_set=ps, attempt_number=2,
                          previous_provider_surface=p1.provider_surface)
        p3 = plan_attempt(provider_set=ps, attempt_number=3,
                          previous_provider_surface=p2.provider_surface)
        for plan in (p1, p2, p3):
            assert plan.provider_surface in ps.compliant_providers

    def test_30_single_provider_configuration_cannot_masquerade_as_mode_a(self):
        ps = ProviderSet(("gemini_notebook",))
        assert ps.mode is OrchestrationMode.MODE_B
        retry = plan_attempt(provider_set=ps, attempt_number=2,
                             previous_provider_surface="gemini_notebook")
        assert retry.retry_mode is RetryMode.SAME_PROVIDER_RETRY
        assert retry.fallback_used is False

    def test_31_provider_selection_is_deterministic_and_order_insensitive(self):
        a = ProviderSet(("surface_b", "surface_a"))
        b = ProviderSet(("surface_a", "surface_b"))
        assert a.compliant_providers == b.compliant_providers == ("surface_a", "surface_b")
        assert a.default_provider == b.default_provider == "surface_a"
        for n in (1, 2, 3):
            prev = None if n == 1 else ("surface_a" if n == 2 else "surface_b")
            kw = {} if prev is None else {"previous_provider_surface": prev}
            assert plan_attempt(provider_set=a, attempt_number=n, **kw) == \
                plan_attempt(provider_set=b, attempt_number=n, **kw)

    def test_unknown_provider_is_refused(self):
        ps = self._ps()
        with pytest.raises(RetryPolicyError):
            plan_attempt(provider_set=ps, attempt_number=2,
                         previous_provider_surface="not_configured")


# =====================================================================
# §13 Retry — failure handling (32–35)
# =====================================================================

class TestFailureHandling:
    def test_32_fail_closed_failures_never_retry_even_with_budget(self):
        ps = ProviderSet(("gemini_notebook",))
        for outcome in (TerminalStatus.PIT_BLOCK, TerminalStatus.INCOMPLETE,
                        TerminalStatus.FAILED):
            d = decide_retry(provider_set=ps, attempt_number=1, outcome=outcome,
                             previous_provider_surface=None, evidence_gap_id="EG-1")
            assert d.should_retry is False
            assert d.terminal_status is outcome
            assert d.evidence_gap_instruction is None
        # M6.4 contractually fail-closed result statuses
        for status in ("PROVIDER_CANNOT_ENFORCE_SEALED_INPUT",
                       "REQUEST_ISOLATION_UNVERIFIED"):
            assert classify_result_status(status) is AttemptClassification.NON_RETRYABLE
            assert classify_attempt_outcome(TerminalStatus.FAILED) is \
                AttemptClassification.NON_RETRYABLE

    def test_33_retryable_failure_respects_the_remaining_budget(self):
        ps = ProviderSet(("gemini_notebook",))
        for n, expected in ((1, True), (2, True), (3, False)):
            d = decide_retry(provider_set=ps, attempt_number=n,
                             outcome=TerminalStatus.TRANSPORT_FAILURE,
                             previous_provider_surface="gemini_notebook",
                             evidence_gap_id="EG-1")
            assert d.should_retry is expected
            if expected:
                assert d.next_attempt.attempt_number == n + 1
            else:
                assert d.terminal_status is TerminalStatus.RESEARCH_UNAVAILABLE

    def test_34_attempt_history_is_append_only_and_ordered(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        record_failed_attempt(
            store, ledger_id="L-1", attempt_number=1,
            retry_mode=RetryMode.INITIAL_ATTEMPT, provider_surface="gemini_notebook",
            transport_type="BROWSER_UI_AUTOMATION", outcome=TerminalStatus.TRANSPORT_FAILURE,
            error="boom", telemetry=_tel(), completed_at=_FIXED_NOW.isoformat(),
        )
        record_failed_attempt(
            store, ledger_id="L-1", attempt_number=2,
            retry_mode=RetryMode.SAME_PROVIDER_RETRY, provider_surface="gemini_notebook",
            transport_type="BROWSER_UI_AUTOMATION", outcome=TerminalStatus.TRANSPORT_FAILURE,
            error="boom again", telemetry=_tel(), completed_at=_FIXED_NOW.isoformat(),
        )
        record = store.load_run("L-1")
        assert [a.attempt_number for a in record.attempts] == [1, 2]
        assert [a.retry_mode for a in record.attempts] == [
            RetryMode.INITIAL_ATTEMPT, RetryMode.SAME_PROVIDER_RETRY
        ]
        with pytest.raises(LedgerIdentityConflict):
            _append(store, n=1)

    def test_35_reentry_uses_durable_history_not_attempt_one(self, tmp_path):
        path = tmp_path / "durable.sqlite3"
        first = DeepResearchRunLedgerStore(path, clock=lambda: _FIXED_NOW)
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            first, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        _append(first, n=1)
        # simulate a process/restart/re-entry: a fresh store over the same durable file
        second = DeepResearchRunLedgerStore(path, clock=lambda: _FIXED_NOW)
        resumed = resolve_or_create_logical_run(
            second, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert resumed.outcome is ResolutionOutcome.EXISTING_ACTIVE
        assert resumed.attempts_recorded == 1
        assert resumed.next_attempt_number == 2  # never restarts at attempt 1
        assert len(second.list_runs()) == 1


# =====================================================================
# §14 Telemetry truthfulness (36–47)
# =====================================================================

class TestTelemetry:
    def _exposed_all(self, **overrides):
        metrics = {
            "model_identity": exposed("gemini-3-pro"),
            "prompt_tokens": exposed(1234),
            "completion_tokens": exposed(567),
            "cost": exposed(0.0123),
            "model_version": exposed("2026-08-01"),
        }
        metrics.update(overrides)
        return build_telemetry(metrics=metrics)

    def test_36_exposed_model_identity_is_preserved_exactly(self):
        tel = self._exposed_all()
        assert tel["model_identity"] == {
            "status": "EXPOSED", "value": "gemini-3-pro", "reason": None
        }

    def test_37_exposed_token_values_are_preserved_exactly(self):
        tel = self._exposed_all()
        assert tel["prompt_tokens"]["value"] == 1234
        assert tel["completion_tokens"]["value"] == 567

    def test_38_exposed_cost_is_preserved_exactly(self):
        assert self._exposed_all()["cost"]["value"] == 0.0123

    def test_39_a_real_exposed_zero_remains_zero(self):
        tel = self._exposed_all(prompt_tokens=exposed(0), cost=exposed(0))
        assert tel["prompt_tokens"]["value"] == 0
        assert tel["cost"]["value"] == 0
        assert tel["prompt_tokens"]["status"] == "EXPOSED"

    def test_40_not_exposed_requires_a_null_value(self):
        assert not_exposed()["value"] is None
        with pytest.raises(OrchestrationError):
            build_telemetry(metrics={
                "model_identity": {"status": "NOT_EXPOSED", "value": 0, "reason": "r"},
                "prompt_tokens": exposed(1), "completion_tokens": exposed(1),
                "cost": exposed(1), "model_version": exposed("v"),
            })

    def test_41_not_exposed_requires_a_non_blank_reason(self):
        with pytest.raises(OrchestrationError):
            not_exposed("   ")
        with pytest.raises(OrchestrationError):
            build_telemetry(metrics={
                "model_identity": {"status": "NOT_EXPOSED", "value": None, "reason": ""},
                "prompt_tokens": exposed(1), "completion_tokens": exposed(1),
                "cost": exposed(1), "model_version": exposed("v"),
            })

    def test_42_unknown_can_never_be_encoded_as_zero(self):
        for name in ("prompt_tokens", "completion_tokens", "cost"):
            payload = not_exposed_telemetry()
            assert payload[name]["value"] is None
            assert payload[name]["value"] != 0
            assert payload[name]["status"] == "NOT_EXPOSED"
        with pytest.raises(OrchestrationError):
            exposed(None)  # an unknown value cannot be declared EXPOSED

    def test_43_unknown_is_never_guessed_or_estimated(self):
        import qad.m6.orchestration as orch

        names = [n for n in dir(orch) if "estimat" in n.lower() or "guess" in n.lower()]
        assert names == []
        # the only truthful-unavailability encoding carries no numeric at all
        assert not_exposed()["value"] is None
        assert NOT_EXPOSED_BY_PROVIDER == "NOT_EXPOSED_BY_PROVIDER"

    def test_44_required_metric_omission_fails_closed(self):
        partial = {
            "model_identity": not_exposed(),
            "prompt_tokens": not_exposed(),
            "completion_tokens": not_exposed(),
            "cost": not_exposed(),
        }  # model_version missing
        with pytest.raises(OrchestrationError):
            build_telemetry(metrics=partial)

    def test_45_an_undeclared_metric_cannot_substitute_for_a_required_one(self):
        substituted = {
            "model_identity": not_exposed(),
            "prompt_tokens": not_exposed(),
            "completion_tokens": not_exposed(),
            "model_version": not_exposed(),
            "total_tokens": not_exposed(),  # declared-optional, but does NOT satisfy cost
        }
        with pytest.raises(OrchestrationError):
            build_telemetry(metrics=substituted)
        with pytest.raises(OrchestrationError):
            build_telemetry(metrics={
                "model_identity": not_exposed(), "prompt_tokens": not_exposed(),
                "completion_tokens": not_exposed(), "cost": not_exposed(),
                "model_version": not_exposed(), "my_metric": not_exposed(),
            })

    def test_46_telemetry_persists_durably_per_attempt(self, store, tmp_path):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        store.append_attempt(
            "L-1", attempt_number=1, retry_mode=RetryMode.INITIAL_ATTEMPT,
            provider_surface="gemini_notebook", transport_type="BROWSER_UI_AUTOMATION",
            completed_at=_FIXED_NOW.isoformat(), outcome=TerminalStatus.TRANSPORT_FAILURE,
            error="boom", telemetry=build_telemetry(metrics={
                "model_identity": exposed("gemini-3-pro"), "prompt_tokens": exposed(11),
                "completion_tokens": exposed(22), "cost": exposed(0.5),
                "model_version": exposed("2026-08-01"),
            }),
        )
        reopened = DeepResearchRunLedgerStore(
            store._db_path, clock=lambda: _FIXED_NOW
        )
        attempt = reopened.load_run("L-1").attempts[0]
        assert attempt.telemetry["model_identity"].value == "gemini-3-pro"
        assert attempt.telemetry["prompt_tokens"].value == 11
        assert attempt.telemetry["cost"].value == 0.5

    def test_47_prior_attempt_telemetry_cannot_be_rewritten(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        _append(store, n=1)
        first = store.load_run("L-1").attempts[0]
        _append(store, n=2, mode=RetryMode.SAME_PROVIDER_RETRY)
        after = store.load_run("L-1")
        assert after.attempts[0].telemetry == first.telemetry
        assert after.attempts[0].completed_at == first.completed_at
        assert len(after.attempts) == 2
        with pytest.raises(LedgerIdentityConflict):
            _append(store, n=1)

    def test_consumer_surface_expected_state_is_not_exposed(self):
        payload = not_exposed_telemetry()
        for name, spec in payload.items():
            assert spec["status"] == "NOT_EXPOSED"
            assert spec["value"] is None
            assert spec["reason"].strip()
        assert "total_tokens" not in payload  # optional -> omitted, never guessed


# =====================================================================
# §15 M6.4 SUCCESS consumption — the hard carry-forward condition (48–52)
# =====================================================================

class TestSuccessConsumption:
    def test_48_proof_gate_runs_before_anything_is_recorded(self, store, monkeypatch):
        req = _request()
        ok = _build_success(req)
        resolve_or_create_logical_run(
            store, idempotency_key=compute_idempotency_key(**_keys()),
            create_run_kwargs=_create_kwargs(compute_idempotency_key(**_keys())),
        )
        calls = {"append": 0, "terminal": 0}

        def _append_probe(*a, **k):
            calls["append"] += 1

        def _terminal_probe(*a, **k):
            calls["terminal"] += 1

        monkeypatch.setattr(store, "append_attempt", _append_probe)
        monkeypatch.setattr(store, "terminalize", _terminal_probe)

        def _gate_called(*a, **k):
            raise RuntimeError("assert_proof_verified was called first")

        monkeypatch.setattr(DeepResearchResult, "assert_proof_verified", _gate_called)
        with pytest.raises(RuntimeError):
            accept_success_result(
                store, ledger_id="L-1", result=ok, attempt_number=1,
                retry_mode=RetryMode.INITIAL_ATTEMPT,
                transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
            )
        assert calls == {"append": 0, "terminal": 0}

    def test_49_forged_unverified_success_cannot_terminalize_as_success(self, store):
        req = _request()
        ok = _build_success(req)
        object.__setattr__(ok, "_proof_attestation", None)
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        with pytest.raises(ResearchResultError):
            accept_success_result(
                store, ledger_id="L-1", result=ok, attempt_number=1,
                retry_mode=RetryMode.INITIAL_ATTEMPT,
                transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
            )
        record = store.load_run("L-1")
        assert record.attempts == ()
        assert record.is_terminal is False

    def test_50_tampered_success_cannot_terminalize_as_success(self, store):
        req = _request()
        ok = _build_success(req)
        tampered = b"post-construction tamper"
        object.__setattr__(ok, "result_bytes", tampered)
        object.__setattr__(ok, "result_sha256", compute_result_sha256(tampered))
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        with pytest.raises(ResearchResultError):
            accept_success_result(
                store, ledger_id="L-1", result=ok, attempt_number=1,
                retry_mode=RetryMode.INITIAL_ATTEMPT,
                transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
            )
        record = store.load_run("L-1")
        assert record.attempts == ()
        assert record.is_terminal is False

    def test_51_valid_verified_success_retains_its_exact_result_hash(self, store):
        req = _request()
        ok = _build_success(req)
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        record = accept_success_result(
            store, ledger_id="L-1", result=ok, attempt_number=1,
            retry_mode=RetryMode.INITIAL_ATTEMPT,
            transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
            completed_at=_FIXED_NOW.isoformat(),
        )
        assert record.terminal_status is TerminalStatus.SUCCESS
        assert record.result_sha256 == ok.result_sha256
        assert record.result_sha256 == compute_result_sha256(_PAYLOAD)
        assert [a.attempt_number for a in record.attempts] == [1]
        assert record.attempts[0].outcome == TerminalStatus.SUCCESS.value

    def test_52_valid_verified_success_remains_non_canonical(self, store):
        req = _request()
        ok = _build_success(req)
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        accept_success_result(
            store, ledger_id="L-1", result=ok, attempt_number=1,
            retry_mode=RetryMode.INITIAL_ATTEMPT,
            transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
        )
        assert ok.non_canonical is True
        assert len(CANONICAL_SCHEMAS) == 68
        import qad.m6.orchestration as orch

        for banned in ("admit_evidence", "to_canonical", "admit_source"):
            assert not hasattr(orch, banned)

    def test_success_cannot_be_recorded_through_the_failure_path(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        with pytest.raises(OrchestrationError):
            record_failed_attempt(
                store, ledger_id="L-1", attempt_number=1,
                retry_mode=RetryMode.INITIAL_ATTEMPT,
                provider_surface="gemini_notebook",
                transport_type="BROWSER_UI_AUTOMATION",
                outcome=TerminalStatus.SUCCESS, error=None, telemetry=_tel(),
            )
        assert store.load_run("L-1").attempts == ()

    def test_decide_retry_refuses_to_handle_success(self):
        with pytest.raises(RetryPolicyError):
            decide_retry(
                provider_set=ProviderSet(("gemini_notebook",)), attempt_number=1,
                outcome=TerminalStatus.SUCCESS, previous_provider_surface=None,
                evidence_gap_id="EG-1",
            )


# =====================================================================
# Boundaries — no provider transport, no M6.6+ scope, canonical set intact
# =====================================================================

class TestBoundaries:
    def test_no_provider_network_or_browser_transport(self, monkeypatch):
        def _boom(*a, **k):
            raise AssertionError("network access attempted by the M6.5 layer")

        monkeypatch.setattr(socket, "socket", _boom)
        monkeypatch.setattr(socket, "create_connection", _boom)
        from pathlib import Path

        import qad.m6.orchestration as orch

        source = Path(orch.__file__).read_text(encoding="utf-8").lower()
        for banned in (
            "import requests", "import urllib", "import socket", "import httpx",
            "import selenium", "import playwright", "import chromedriver",
            "import gemini", "import notebook", "chrome.debugger",
        ):
            assert banned not in source
        # the layer is exercised with no network available at all
        assert compute_idempotency_key(**_keys()).startswith("idem-")
        assert not_exposed_telemetry()["cost"]["value"] is None

    def test_no_m66_or_later_scope_creep(self):
        import qad.m6.orchestration as orch

        for banned in ("admit_source", "discovery", "source_bridge", "gemini_adapter",
                       "browser_transport", "canary"):
            assert not hasattr(orch, banned)

    def test_canonical_schema_count_is_still_68(self):
        assert len(CANONICAL_SCHEMAS) == 68
        for added in ("M65-01", "M6.5", "ORCH-01", "IDEM-01", "TELEM-01"):
            assert added not in CANONICAL_SCHEMAS

    def test_rrm01_deep_research_runs_is_still_id_strings_only(self):
        from qad.models.family_i import RunManifestRecord

        annotation = RunManifestRecord.model_fields["deep_research_runs"].annotation
        assert "list[str]" in str(annotation)


# =====================================================================
# Round-1 reviewer closure — two bounded implementation defects
# =====================================================================

class TestRound1Closure:
    def test_r1_01_provider_set_rejects_a_bare_string(self):
        """A string iterates into characters and would fabricate provider surfaces."""
        with pytest.raises(RetryPolicyError):
            ProviderSet("openai")
        with pytest.raises(RetryPolicyError):
            ProviderSet(b"openai")
        # a genuine one-element collection is still Mode B
        one = ProviderSet(("openai",))
        assert one.mode is OrchestrationMode.MODE_B
        assert one.compliant_providers == ("openai",)

    def test_r1_02_provider_names_must_be_non_blank_strings(self):
        with pytest.raises(RetryPolicyError):
            ProviderSet((123,))
        with pytest.raises(RetryPolicyError):
            ProviderSet(("  ",))
        with pytest.raises(RetryPolicyError):
            ProviderSet(())
        with pytest.raises(RetryPolicyError):
            ProviderSet(("dup", "dup"))

    def test_r1_03_a_gapped_attempt_history_is_fail_closed_and_coherent(self, store):
        """A gap must never yield 'no next attempt' + 'two attempts remaining'."""
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        # write a GAPPED durable state directly through the M6.3 ledger (legacy state)
        _append(store, n=3, mode=RetryMode.SAME_PROVIDER_RETRY)
        resolved = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert resolved.history_consistent is False
        assert resolved.next_attempt_number is None
        assert resolved.retry_budget_remaining == 0
        assert resolved.may_attempt is False

    def test_r1_04_m65_recording_refuses_a_non_contiguous_attempt(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        with pytest.raises(RetryPolicyError):
            record_failed_attempt(
                store, ledger_id="L-1", attempt_number=2,
                retry_mode=RetryMode.SAME_PROVIDER_RETRY,
                provider_surface="gemini_notebook",
                transport_type="BROWSER_UI_AUTOMATION",
                outcome=TerminalStatus.TRANSPORT_FAILURE, error="boom", telemetry=_tel(),
            )
        assert store.load_run("L-1").attempts == ()
        # attempt 1 is accepted, attempt 3 (out of order) is refused
        record_failed_attempt(
            store, ledger_id="L-1", attempt_number=1,
            retry_mode=RetryMode.INITIAL_ATTEMPT, provider_surface="gemini_notebook",
            transport_type="BROWSER_UI_AUTOMATION",
            outcome=TerminalStatus.TRANSPORT_FAILURE, error="boom", telemetry=_tel(),
        )
        with pytest.raises(RetryPolicyError):
            record_failed_attempt(
                store, ledger_id="L-1", attempt_number=3,
                retry_mode=RetryMode.SAME_PROVIDER_RETRY,
                provider_surface="gemini_notebook",
                transport_type="BROWSER_UI_AUTOMATION",
                outcome=TerminalStatus.TRANSPORT_FAILURE, error="boom", telemetry=_tel(),
            )
        assert [a.attempt_number for a in store.load_run("L-1").attempts] == [1]

    def test_r1_05_accept_success_enforces_contiguity_and_the_budget(self, store):
        key = compute_idempotency_key(**_keys())
        resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        ok = _build_success(_request())
        with pytest.raises(RetryPolicyError):
            accept_success_result(
                store, ledger_id="L-1", result=ok, attempt_number=2,
                retry_mode=RetryMode.SAME_PROVIDER_RETRY,
                transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
            )
        record = store.load_run("L-1")
        assert record.attempts == () and record.is_terminal is False
        # attempt 1 is accepted (§15 tests 51/52 cover the success semantics)
        assert accept_success_result(
            store, ledger_id="L-1", result=ok, attempt_number=1,
            retry_mode=RetryMode.INITIAL_ATTEMPT,
            transport_type="BROWSER_UI_AUTOMATION", telemetry=_tel(),
        ).terminal_status is TerminalStatus.SUCCESS

    def test_r1_06_budget_is_coherent_across_the_whole_lifecycle(self, store):
        key = compute_idempotency_key(**_keys())
        created = resolve_or_create_logical_run(
            store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
        )
        assert (created.next_attempt_number, created.retry_budget_remaining) == (1, 3)
        for n in (1, 2, 3):
            _append(store, n=n, mode=RetryMode.SAME_PROVIDER_RETRY)
            resolved = resolve_or_create_logical_run(
                store, idempotency_key=key, create_run_kwargs=_create_kwargs(key)
            )
            assert resolved.history_consistent is True
            if n < MAX_ATTEMPTS:
                assert resolved.next_attempt_number == n + 1
                assert resolved.retry_budget_remaining == MAX_ATTEMPTS - n
            else:
                assert resolved.next_attempt_number is None
                assert resolved.retry_budget_remaining == 0
        # the 4th attempt is unrecordable through the M6.5 boundary
        with pytest.raises(RetryPolicyError):
            record_failed_attempt(
                store, ledger_id="L-1", attempt_number=4,
                retry_mode=RetryMode.SAME_PROVIDER_RETRY,
                provider_surface="gemini_notebook",
                transport_type="BROWSER_UI_AUTOMATION",
                outcome=TerminalStatus.TRANSPORT_FAILURE, error="boom", telemetry=_tel(),
            )
