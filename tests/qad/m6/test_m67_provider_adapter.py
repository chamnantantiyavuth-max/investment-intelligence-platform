"""QAD M6.7 - PROVIDER ADAPTER + MOCK TRANSPORT - acceptance suite.

FD #151 (M6.7 = Provider Adapter + Mock Transport) with the Founder-approved plan
decisions R1-R6 (all "A"). Nothing here executes a real provider: every path is
deterministic and offline (no Gemini Notebook, no browser/CDP, no network, no
credentials).
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import pathlib
import socket
import sqlite3

import pytest

from qad.m6.ledger import (
    CandidateDisposition,
    DeepResearchRunLedgerStore,
    LedgerNotFound,
    LedgerValidationError,
    RetryMode,
    TelemetryStatus,
    TerminalStatus,
)
from qad.m6.mock_proof import MockProofResolver
from qad.m6.mock_transport import (
    DeterministicMockTransport,
    MockEvidenceStore,
    MockTransportScript,
)
from qad.m6.orchestration import (
    OrchestrationError,
    OrchestrationMode,
    ProviderExecutionOutcome,
    ProviderSet,
    RetryPolicyError,
    idempotency_key_for_request,
    plan_attempt,
    resolve_or_create_logical_run,
    run_provider_attempt,
)
from qad.m6.provider import (
    MOCK_PROVIDER_SURFACE,
    MOCK_TRANSPORT_TYPE,
    ProviderOutcomeKind,
    not_exposed_provider_telemetry,
)
from qad.m6.research_contract import (
    DEFAULT_PROOF_RESOLVER,
    DeepResearchProofResolver,
    ProofKind,
    ProofVerificationRequest,
    build_deep_research_request,
)
from qad.m6.snapshot import build_sealed_input_snapshot
from qad.m6.source_bridge import (
    DEFAULT_ORIGINAL_SOURCE_VERIFIER,
    SourceFailureKind,
    SourceVerificationCandidate,
    compute_source_candidate_id,
    pending_candidates,
)
from qad.models.family_a import (
    CandidateRecord,
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecord,
    CaseRecordCase_state,
    SecurityMaster,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
)
from qad.models.family_b import (
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_i import PITContext, PITContextMode
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]

AS_OF = "2026-01-01"
ADMITTED = "2025-12-15T00:00:00+00:00"
#: An admission instant AFTER as_of — such a source must be ineligible for a SEALED
#: historical snapshot (FD #150 / M6.2 PIT boundary).
ADMITTED_LATE = "2026-02-01T00:00:00+00:00"
DISCOVERED_AT = "2026-10-14T09:00:00+00:00"
CORPUS_A = (("S1", b"alpha"), ("S2", b"beta"))
CORPUS_B = (("S3", b"gamma"),)
SURFACE_A = "surface_a"
SURFACE_B = "surface_b"

#: Distinguishes "no trusted resolver injected" from "use the harness resolver".
_UNSET = object()


def _src(sid, raw):
    return SourceRecord(
        source_id=sid,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier="https://sec.gov/" + sid,
        content_hash=hashlib.sha256(raw).hexdigest(),
        retrieval_date="2025-12-01",
        publication_date="2025-11-20",
    )


def _seed_case(pit_store, case_id):
    sm = SecurityMaster(
        entity_id="SM-" + case_id, cik="0000998877", exchange="NYSE",
        name="M67 Mock Corp", primary_ticker="M67O",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    pit_store.store(sm)
    cand = CandidateRecord(
        candidate_id="CR-" + case_id, entity_id=sm.entity_id,
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


def _world(case_id="CASE-1", corpus=CORPUS_A, admitted=ADMITTED):
    """A deterministic SEALED world: archive + PIT store + approved snapshot."""
    archive = InMemoryRawSourceArchive(
        clock=lambda: dt.datetime.fromisoformat(admitted))
    pit_store = InMemoryPITContextStore()
    _seed_case(pit_store, case_id)
    pit_store.store(PITContext(
        pit_context_id="PITC-1", case_id=case_id, as_of_date=AS_OF,
        mode=PITContextMode.SEALED_HISTORICAL_EVALUATION, created_by="founder",
    ))
    for sid, raw in corpus:
        archive.admit_source(_src(sid, raw), raw)
    snapshot = build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
        case_version="v1", source_ids=[sid for sid, _ in corpus],
    )
    return archive, pit_store, snapshot


def _request(snapshot, request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
             provider_surface=MOCK_PROVIDER_SURFACE):
    return build_deep_research_request(
        snapshot=snapshot, request_id=request_id, research_run_id=research_run_id,
        ledger_id=ledger_id, rrm_manifest_id="RRM-2026-0001", evidence_gap_id="EG-1",
        research_question="Why is the moat durable?", provider_surface=provider_surface,
    )


def _create_kwargs(request):
    return dict(
        ledger_id=request.ledger_id,
        research_run_id=request.research_run_id,
        rrm_manifest_id=request.rrm_manifest_id,
        case_id=request.case_id,
        case_version=request.case_version,
        evidence_gap_id=request.evidence_gap_id,
        request_id=request.request_id,
        idempotency_key=idempotency_key_for_request(request),
        notebook_identity="nb-m67-mock-1",
        pit_context_id=request.pit_context_id,
        pit_mode=request.pit_mode,
        as_of=request.as_of,
        input_snapshot_hash=request.input_snapshot_hash,
        provider_surface=request.provider.provider_surface,
        transport_type=MOCK_TRANSPORT_TYPE,
    )


class Harness:
    """One deterministic mock harness: transport + evidence store + mock resolver."""

    def __init__(self, archive, script=None, surface=MOCK_PROVIDER_SURFACE,
                 reuse_context=False):
        self.evidence = MockEvidenceStore()
        self.transport = DeterministicMockTransport(
            archive=archive, evidence_store=self.evidence, script=script,
            surface=surface, reuse_context=reuse_context,
        )
        self.resolver = MockProofResolver(self.evidence)


def _store(tmp_path, name="m67.sqlite3"):
    return DeepResearchRunLedgerStore(tmp_path / name)


def _ps():
    return ProviderSet((MOCK_PROVIDER_SURFACE,))


def _attempt(store, request, harness, plan, policy=None, archive=None,
             resolver=_UNSET, telemetry=None, verifier=None, registry=None,
             pit_store=None, kwargs=True):
    return run_provider_attempt(
        store,
        request=request,
        provider=harness.transport,
        provider_set=_ps() if policy is None else policy,
        transport_type=MOCK_TRANSPORT_TYPE,
        plan=plan,
        telemetry=not_exposed_provider_telemetry() if telemetry is None else telemetry,
        proof_resolver=harness.resolver if resolver is _UNSET else resolver,
        original_source_verifier=verifier,
        archive=archive,
        evidence_registry=registry,
        pit_context_store=pit_store,
        discovery_timestamp=DISCOVERED_AT,
        create_run_kwargs=_create_kwargs(request) if kwargs else None,
    )



# --------------------------------------------------- 1 / 19 end-to-end SUCCESS


def test_01_valid_mock_request_reaches_atomic_success(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive, pit_store=pit_store,
                      registry=InMemoryEvidenceRegistry(source_archive=archive))

    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = result.record
    assert rec.terminal_status is TerminalStatus.SUCCESS
    assert rec.is_terminal is True
    assert rec.result_sha256 == result.result_sha256
    assert rec.result_artifact_ref == result.result_artifact_ref
    assert rec.result_sha256 == hashlib.sha256(
        harness.transport.result_bytes).hexdigest()
    assert [a.attempt_number for a in rec.attempts] == [1]
    assert [a.outcome for a in rec.attempts] == [TerminalStatus.SUCCESS.value]
    kinds = [e[1] for e in store.events("L-1")]
    assert kinds.count("ATTEMPT_APPENDED") == 1
    assert kinds.count("RUN_TERMINALIZED") == 1
    con = sqlite3.connect(str(tmp_path / "m67.sqlite3"))
    try:
        assert con.execute(
            "SELECT COUNT(*) FROM ledger_attempt WHERE ledger_id='L-1'"
        ).fetchone()[0] == 1
        assert con.execute(
            "SELECT COUNT(*) FROM ledger_terminal WHERE ledger_id='L-1'"
        ).fetchone()[0] == 1
    finally:
        con.close()


def test_19_durable_reopen_preserves_exact_result_identity(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    path = tmp_path / "m67.sqlite3"
    store = _store(tmp_path)
    plan = plan_attempt(provider_set=_ps(), attempt_number=1)
    first = _attempt(store, request, harness, plan, archive=archive)

    reopened = DeepResearchRunLedgerStore(path)
    rec = reopened.load_run("L-1")
    assert rec.terminal_status is TerminalStatus.SUCCESS
    assert rec.result_sha256 == first.result_sha256
    assert rec.result_artifact_ref == first.result_artifact_ref
    assert [a.attempt_number for a in rec.attempts] == [1]
    assert [tuple(e) for e in reopened.events("L-1")] == [
        tuple(e) for e in store.events("L-1")]
    with pytest.raises(RetryPolicyError):
        _attempt(reopened, request, harness, plan, archive=archive)


# --------------------------------------------------------- 2-6 proof boundary


def test_02_without_an_injected_resolver_success_is_rejected(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    denied = DEFAULT_PROOF_RESOLVER.verify_proof(ProofVerificationRequest(
        proof_kind=ProofKind.REQUEST_ISOLATION, request_id="R", research_run_id="RR",
        ledger_id="L", provider_surface="s", input_snapshot_hash="h", evidence_ref="e",
    ))
    assert denied.verified is False

    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive, resolver=None)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is ProviderOutcomeKind.PROOF_NOT_VERIFIED
    rec = store.load_run("L-1")
    assert rec.is_terminal is False
    assert rec.result_sha256 is None
    assert not any(a.outcome == TerminalStatus.SUCCESS.value for a in rec.attempts)


def test_03_closed_corpus_proof_missing_fails_closed(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(
        withhold_closed_corpus_evidence=True))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is ProviderOutcomeKind.PROOF_NOT_VERIFIED
    assert store.load_run("L-1").is_terminal is False


def test_04_isolation_proof_missing_fails_closed(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(
        withhold_isolation_evidence=True))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is ProviderOutcomeKind.PROOF_NOT_VERIFIED
    assert store.load_run("L-1").is_terminal is False


def test_05_request_a_proof_cannot_authorize_request_b(tmp_path):
    archive_a, _pa, snap_a = _world("CASE-1", CORPUS_A)
    archive_b, _pb, snap_b = _world("CASE-2", CORPUS_B)
    request_a = _request(snap_a, request_id="REQ-A", research_run_id="RR-A",
                         ledger_id="L-A")
    request_b = _request(snap_b, request_id="REQ-B", research_run_id="RR-B",
                         ledger_id="L-B")
    store = _store(tmp_path)

    harness_a = Harness(archive_a)
    first = _attempt(store, request_a, harness_a,
                     plan_attempt(provider_set=_ps(), attempt_number=1),
                     archive=archive_a)
    assert first.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    stolen = first.provider_outcome.evidence_refs
    assert len(stolen) == 2

    harness_b = Harness(archive_b, MockTransportScript(forced_evidence_refs=stolen))
    second = _attempt(store, request_b, harness_b,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive_b)
    assert second.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert second.provider_outcome.kind is ProviderOutcomeKind.PROOF_NOT_VERIFIED
    assert store.load_run("L-B").is_terminal is False


def test_06_reused_provider_context_leaks_and_is_refused(tmp_path):
    """Request-isolation canary (FD #149 B3, deterministic mock form).

    ONE archive, two snapshots over DISJOINT source subsets. A REUSED harness carries
    request A's corpus into request B, so the canary observes the leak and B fails
    closed. A FRESH harness per request (the required per-request reconstruction) is
    isolated and succeeds.
    """
    archive, pit_store, _full = _world("CASE-1", CORPUS_A + CORPUS_B)
    snap_a = build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
        case_version="v1", source_ids=["S1", "S2"])
    snap_b = build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
        case_version="v1", source_ids=["S3"])
    request_a = _request(snap_a, request_id="REQ-A", research_run_id="RR-A",
                         ledger_id="L-A")
    request_b = _request(snap_b, request_id="REQ-B", research_run_id="RR-B",
                         ledger_id="L-B")
    plan1 = plan_attempt(provider_set=_ps(), attempt_number=1)

    store = _store(tmp_path)
    reused = Harness(archive, reuse_context=True)
    assert _attempt(store, request_a, reused, plan1,
                    archive=archive).outcome is (
        ProviderExecutionOutcome.SUCCESS_FINALIZED)
    leaked = _attempt(store, request_b, reused, plan1, archive=archive)
    assert leaked.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert store.load_run("L-B").is_terminal is False
    assert reused.evidence.foreign_canary_tokens() == ("S1", "S2")

    store2 = _store(tmp_path, name="m67b.sqlite3")
    fresh_a = Harness(archive)
    assert _attempt(store2, request_a, fresh_a, plan1,
                    archive=archive).outcome is (
        ProviderExecutionOutcome.SUCCESS_FINALIZED)
    fresh_b = Harness(archive)
    ok = _attempt(store2, request_b, fresh_b, plan1, archive=archive)
    assert ok.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert fresh_b.evidence.foreign_canary_tokens() == ()
    assert fresh_b.evidence.observed_source_ids() == ("S3",)


def test_06b_resolver_is_not_an_echo_of_provider_claims():
    resolver = MockProofResolver(MockEvidenceStore())
    verification = resolver.verify_proof(ProofVerificationRequest(
        proof_kind=ProofKind.CLOSED_CORPUS_ENFORCEMENT, request_id="REQ-X",
        research_run_id="RR-X", ledger_id="L-X", provider_surface="s",
        input_snapshot_hash="h", evidence_ref="MOCK-EVID-fabricated",
    ))
    assert verification.verified is False
    assert verification.evidence_ref is None
    assert verification.failure_reason


def test_06c_mock_resolver_satisfies_the_m6_4_protocol(tmp_path):
    archive, _pit, _snap = _world()
    harness = Harness(archive)
    assert isinstance(harness.resolver, DeepResearchProofResolver)


# --------------------------------------------- 7-9 source discovery/disposition


def test_07_dispositions_occur_before_success_finalization(tmp_path, monkeypatch):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    seen = []
    real = store.finalize_success_attempt_atomic

    def _spy(*args, **kw):
        seen.append(pending_candidates(store.load_run("L-1")))
        return real(*args, **kw)

    monkeypatch.setattr(store, "finalize_success_attempt_atomic", _spy, raising=False)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)

    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert seen == [()]
    rec = store.load_run("L-1")
    assert rec.candidates and rec.dispositions
    assert len(rec.dispositions) == len(rec.candidates)
    assert len({d.source_candidate_id for d in rec.dispositions}) == len(
        rec.candidates)


def test_08_undisposed_candidate_prevents_success(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    resolve_or_create_logical_run(
        store, idempotency_key=idempotency_key_for_request(request),
        create_run_kwargs=_create_kwargs(request),
    )
    store.register_candidate(
        "L-1", source_candidate_id="SC-FOREIGN",
        url_or_identifier="https://example.com/foreign",
        discovery_timestamp=DISCOVERED_AT,
        original_source_verification_status="PENDING", pit_eligibility="UNKNOWN",
    )
    with pytest.raises(LedgerValidationError):
        _attempt(store, request, harness,
                 plan_attempt(provider_set=_ps(), attempt_number=1),
                 archive=archive)
    rec = store.load_run("L-1")
    assert rec.is_terminal is False
    assert rec.result_sha256 is None
    assert pending_candidates(rec) == ("SC-FOREIGN",)


def test_09_original_source_verification_is_never_fabricated(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive, verifier=DEFAULT_ORIGINAL_SOURCE_VERIFIER,
                      registry=InMemoryEvidenceRegistry(source_archive=archive),
                      pit_store=pit_store)

    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = store.load_run("L-1")
    assert rec.dispositions
    assert all(d.disposition is CandidateDisposition.DEFERRED
               for d in rec.dispositions)
    assert all(d.src01_id is None for d in rec.dispositions)
    bridge = result.bridge_outcome
    assert bridge is not None
    assert all(o.disposition is CandidateDisposition.DEFERRED
               for o in bridge.outcomes)
    assert all(o.src01_id is None for o in bridge.outcomes)
    assert all(not o.evidence_ids and not o.ear_ids for o in bridge.outcomes)


def test_09b_out_of_corpus_citation_is_a_hard_failure(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(extraneous_citations=("S9",)))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is ProviderOutcomeKind.PROOF_NOT_VERIFIED
    assert store.load_run("L-1").is_terminal is False



# ------------------------------------------------------------ 10-11 PIT boundary


def test_10_sealed_execution_uses_only_admitted_attested_bytes(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    evidence = result.provider_outcome.transport_evidence
    assert evidence is not None
    assert evidence.sealed_bytes_verified is True
    assert evidence.network_used is False
    assert evidence.sent_source_ids == ("S1", "S2")
    declared = dict(request.corpus.exact_blob_hashes)
    for sid, digest in evidence.sent_blob_hashes:
        assert digest == declared[sid]
        assert digest == hashlib.sha256(dict(CORPUS_A)[sid]).hexdigest()
    assert evidence.corpus_hash == request.corpus.corpus_hash


def test_10b_sealed_byte_mismatch_fails_closed(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(byte_tampering=True))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is ProviderOutcomeKind.PIT_BLOCK
    assert store.load_run("L-1").is_terminal is False


def test_10c_provider_without_a_closed_corpus_capability_fails_closed(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(
        cannot_enforce_closed_corpus=True))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.FAIL_CLOSED
    assert result.provider_outcome.kind is (
        ProviderOutcomeKind.PROVIDER_CAPABILITY_INSUFFICIENT)
    assert store.load_run("L-1").is_terminal is False


def test_10d_unattested_sealed_source_cannot_be_snapshotted(tmp_path):
    archive = InMemoryRawSourceArchive(
        clock=lambda: dt.datetime.fromisoformat(ADMITTED_LATE))
    pit_store = InMemoryPITContextStore()
    _seed_case(pit_store, "CASE-1")
    pit_store.store(PITContext(
        pit_context_id="PITC-1", case_id="CASE-1", as_of_date=AS_OF,
        mode=PITContextMode.SEALED_HISTORICAL_EVALUATION, created_by="founder",
    ))
    for sid, raw in CORPUS_A:
        archive.admit_source(_src(sid, raw), raw)   # admitted_at > AS_OF
    with pytest.raises(Exception):
        build_sealed_input_snapshot(
            pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
            case_version="v1", source_ids=[sid for sid, _ in CORPUS_A],
        )


# -------------------------------------- 12-17 retry / idempotency / telemetry


def test_12_transport_failure_records_attempt_and_retry_decision(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)))
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.RETRY_SCHEDULED
    assert result.provider_outcome.kind is ProviderOutcomeKind.TRANSPORT_FAILURE
    rec = store.load_run("L-1")
    assert [a.attempt_number for a in rec.attempts] == [1]
    assert [a.outcome for a in rec.attempts] == [
        TerminalStatus.TRANSPORT_FAILURE.value]
    assert rec.is_terminal is False
    decision = result.retry_decision
    assert decision is not None and decision.should_retry is True
    assert decision.next_attempt is not None
    assert decision.next_attempt.attempt_number == 2
    assert decision.next_attempt.retry_mode is RetryMode.SAME_PROVIDER_RETRY


def test_13_mode_b_same_provider_retry_bounded_at_three(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(attempt_outcomes=(
        (1, "TRANSPORT_FAILURE"), (2, "TRANSPORT_FAILURE"))))
    store = _store(tmp_path)
    ps = _ps()
    assert ps.mode is OrchestrationMode.MODE_B

    first = _attempt(store, request, harness,
                     plan_attempt(provider_set=ps, attempt_number=1), archive=archive)
    second = _attempt(store, request, harness, first.retry_decision.next_attempt,
                      policy=ps, archive=archive, kwargs=False)
    assert [a.retry_mode for a in store.load_run("L-1").attempts] == [
        RetryMode.INITIAL_ATTEMPT.value, RetryMode.SAME_PROVIDER_RETRY.value]
    third_plan = second.retry_decision.next_attempt
    assert third_plan.attempt_number == 3
    assert third_plan.retry_mode is RetryMode.SAME_PROVIDER_RETRY
    assert third_plan.fallback_used is False


def test_14_mode_a_fallback_only_when_the_provider_actually_changes(tmp_path):
    archive, pit_store, snapshot = _world()
    # M6.4/M6.5 interface note: the trusted proof context derives provider_surface from
    # the REQUEST, and a SUCCESS result must carry the same surface as both its proof
    # attestation and the validated plan. A Mode A fallback can therefore only reach
    # SUCCESS when the logical request declares the surface that actually produces the
    # result (surface_b), while the ledger run keeps its own configured surface
    # (surface_a) for the deterministic INITIAL attempt.
    request = _request(snapshot, provider_surface=SURFACE_B)
    run_kwargs = _create_kwargs(request)
    run_kwargs["provider_surface"] = SURFACE_A
    ps = ProviderSet((SURFACE_A, SURFACE_B))
    assert ps.mode is OrchestrationMode.MODE_A
    store = _store(tmp_path)
    harness_a = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)), surface=SURFACE_A)

    first = run_provider_attempt(
        store, request=request, provider=harness_a.transport, provider_set=ps,
        transport_type=MOCK_TRANSPORT_TYPE,
        plan=plan_attempt(provider_set=ps, attempt_number=1),
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=harness_a.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT, create_run_kwargs=run_kwargs,
    )
    assert first.outcome is ProviderExecutionOutcome.RETRY_SCHEDULED
    nxt = first.retry_decision.next_attempt
    assert nxt.provider_surface == SURFACE_B
    assert nxt.provider_changed is True and nxt.fallback_used is True
    assert nxt.retry_mode is RetryMode.PROVIDER_FALLBACK

    harness_b = Harness(archive, surface=SURFACE_B)
    second = run_provider_attempt(
        store, request=request, provider=harness_b.transport, provider_set=ps,
        transport_type=MOCK_TRANSPORT_TYPE, plan=nxt,
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=harness_b.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT,
    )
    assert second.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert second.provider_outcome.provider_surface == SURFACE_B
    rec = store.load_run("L-1")
    assert [a.retry_mode for a in rec.attempts] == [
        RetryMode.INITIAL_ATTEMPT.value, RetryMode.PROVIDER_FALLBACK.value]
    assert rec.terminal_status is TerminalStatus.SUCCESS


def test_15_exhaustion_leads_to_research_unavailable(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive, MockTransportScript(attempt_outcomes=(
        (1, "TRANSPORT_FAILURE"), (2, "TRANSPORT_FAILURE"),
        (3, "TRANSPORT_FAILURE"))))
    store = _store(tmp_path)
    ps = _ps()
    first = _attempt(store, request, harness,
                     plan_attempt(provider_set=ps, attempt_number=1), archive=archive)
    second = _attempt(store, request, harness, first.retry_decision.next_attempt,
                      policy=ps, archive=archive, kwargs=False)
    third = _attempt(store, request, harness, second.retry_decision.next_attempt,
                     policy=ps, archive=archive, kwargs=False)
    assert third.outcome is ProviderExecutionOutcome.RESEARCH_UNAVAILABLE
    rec = store.load_run("L-1")
    assert rec.terminal_status is TerminalStatus.RESEARCH_UNAVAILABLE
    assert [a.attempt_number for a in rec.attempts] == [1, 2, 3]
    assert third.retry_decision is not None
    assert third.retry_decision.should_retry is False
    gap = third.retry_decision.evidence_gap_instruction
    assert gap is not None and gap.to_status == "DEFERRED"


def test_16_telemetry_truthfulness(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    store = _store(tmp_path)
    harness = Harness(archive)
    ok = _attempt(store, request, harness,
                  plan_attempt(provider_set=_ps(), attempt_number=1), archive=archive)
    assert ok.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    metric = store.load_run("L-1").attempts[0].telemetry["model_identity"]
    assert metric.status is TelemetryStatus.NOT_EXPOSED
    assert metric.value is None and metric.reason

    store2 = _store(tmp_path, name="m67-tel.sqlite3")
    harness2 = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)))
    with pytest.raises(LedgerValidationError):
        _attempt(store2, request, harness2,
                 plan_attempt(provider_set=_ps(), attempt_number=1), archive=archive,
                 telemetry={})
    assert store2.load_run("L-1").attempts == ()


def test_17_reprocessing_a_completed_run_creates_no_duplicates(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    plan = plan_attempt(provider_set=_ps(), attempt_number=1)
    first = _attempt(store, request, harness, plan, archive=archive)
    assert first.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    before = store.load_run("L-1")
    with pytest.raises(RetryPolicyError):
        _attempt(store, request, harness, plan, archive=archive)
    after = store.load_run("L-1")
    assert after == before
    assert len(after.attempts) == 1
    assert len(after.dispositions) == len(before.dispositions)
    assert len(after.candidates) == len(before.candidates)


# --------------------------------------------- 18 / 20 atomicity + no egress


class _FailOn:
    def __init__(self, conn, needle):
        self._conn, self._needle = conn, needle

    def execute(self, sql, *a, **kw):
        if self._needle in sql:
            raise RuntimeError("INJECTED FAILURE on " + repr(self._needle))
        return self._conn.execute(sql, *a, **kw)

    def __getattr__(self, item):
        return getattr(self._conn, item)


def test_18_failed_atomic_finalization_leaves_no_half_written_success(
    tmp_path, monkeypatch
):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    # create the logical run FIRST so the injection lands inside the atomic SUCCESS
    # finalization rather than inside run creation
    resolve_or_create_logical_run(
        store, idempotency_key=idempotency_key_for_request(request),
        create_run_kwargs=_create_kwargs(request),
    )
    real_connect = store._connect
    monkeypatch.setattr(
        store, "_connect", lambda: _FailOn(real_connect(), "COMMIT"), raising=False)
    with pytest.raises(RuntimeError, match="INJECTED FAILURE"):
        _attempt(store, request, harness,
                 plan_attempt(provider_set=_ps(), attempt_number=1), archive=archive)
    monkeypatch.undo()

    rec = store.load_run("L-1")
    assert rec.is_terminal is False
    assert rec.result_sha256 is None
    assert not any(a.outcome == TerminalStatus.SUCCESS.value for a in rec.attempts)
    assert all(e[1] != "RUN_TERMINALIZED" for e in store.events("L-1"))
    second = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert second.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert store.load_run("L-1").result_sha256 == second.result_sha256


def test_20_no_network_browser_credential_or_gemini_execution(tmp_path, monkeypatch):
    for rel in ("qad/m6/provider.py", "qad/m6/mock_transport.py",
                "qad/m6/mock_proof.py"):
        tree = ast.parse((REPO_ROOT / rel).read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        banned = {"socket", "http", "urllib", "requests", "selenium", "playwright",
                  "websocket", "subprocess", "aiohttp", "httpx"}
        assert not (imported & banned), (rel, imported & banned)

    def _no_socket(*a, **kw):
        raise AssertionError("M6.7 mock path attempted real network access")

    monkeypatch.setattr(socket, "socket", _no_socket)
    monkeypatch.setattr(socket, "create_connection", _no_socket)
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive)
    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED


def test_20b_the_adapter_never_mutates_the_ledger(tmp_path, monkeypatch):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    calls = []
    for name in ("append_attempt", "terminalize", "finalize_success_attempt_atomic",
                 "register_candidate", "dispose_candidate", "create_run"):
        real = getattr(store, name)

        def _make(real=real, name=name):
            def _spy(*a, **kw):
                calls.append(name)
                return real(*a, **kw)
            return _spy

        monkeypatch.setattr(store, name, _make(), raising=False)
    harness.transport.execute(request, proof_resolver=harness.resolver,
                              attempt_number=1)
    assert calls == []


# ---------------------------------------------------------- negative test cases


def test_neg_tampered_result_is_refused_at_the_consumption_boundary(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    outcome = harness.transport.execute(request, proof_resolver=harness.resolver,
                                        attempt_number=1)
    assert outcome.kind is ProviderOutcomeKind.RESULT
    object.__setattr__(outcome.result, "result_sha256", "f" * 64)
    with pytest.raises(Exception):
        outcome.result.assert_proof_verified()


def test_neg_source_identity_mismatch_is_never_promoted(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    cid_real = compute_source_candidate_id(
        ledger_id="L-1", pointer_index=0, reference="mock://source/S1")

    class _MismatchedVerifier:
        def verify(self, verification_request, /):
            if verification_request.source_candidate_id != cid_real:
                return SourceVerificationCandidate(
                    verified=False, reason="NO_FIXTURE_FOR_CANDIDATE",
                    failure_kind=SourceFailureKind.INSUFFICIENT_PROOF)
            return SourceVerificationCandidate(
                verified=True, reason="INDEPENDENTLY_VERIFIED", source_id="SRC-X",
                source_tier="L1", source_type="SEC_FILING",
                content_hash=hashlib.sha256(b"other").hexdigest(),
                raw_bytes=b"other", location="https://sec.gov/SRC-X",
                retrieval_date="2025-11-01")

    result = _attempt(store, request, harness,
                      plan_attempt(provider_set=_ps(), attempt_number=1),
                      archive=archive, verifier=_MismatchedVerifier(),
                      registry=InMemoryEvidenceRegistry(source_archive=archive))
    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = store.load_run("L-1")
    assert all(d.src01_id is None for d in rec.dispositions)


def test_neg_run_provider_capability_mismatch_is_refused(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    with pytest.raises(RetryPolicyError):
        run_provider_attempt(
            store, request=request, provider=harness.transport,
            provider_set=ProviderSet(("other_surface",)),
            transport_type=MOCK_TRANSPORT_TYPE,
            plan=plan_attempt(provider_set=ProviderSet(("other_surface",)),
                              attempt_number=1),
            telemetry=not_exposed_provider_telemetry(),
            proof_resolver=harness.resolver, archive=archive,
            create_run_kwargs=_create_kwargs(request),
        )
    # FD #151 Round-1 finding 3 reconciliation: the refusal now precedes run creation.
    # The previous accepted assertion ("the run exists with zero attempts") encoded the
    # WEAKER behaviour where an unusable run was left behind; the corrected contract is
    # strictly stronger, so the assertion is strengthened, not weakened.
    assert not store.contains("L-1")
    with pytest.raises(LedgerNotFound):
        store.load_run("L-1")


def test_neg_request_must_be_bound_to_the_target_run(tmp_path):
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    other = _request(snapshot, request_id="REQ-OTHER")
    harness = Harness(archive)
    store = _store(tmp_path)
    resolve_or_create_logical_run(
        store, idempotency_key=idempotency_key_for_request(request),
        create_run_kwargs=_create_kwargs(request),
    )
    with pytest.raises(RetryPolicyError):
        _attempt(store, request=other, harness=harness,
                 plan=plan_attempt(provider_set=_ps(), attempt_number=1),
                 archive=archive, kwargs=False)
    assert store.load_run("L-1").attempts == ()


# =====================================================================
# ROUND 2 - REQUEST/RUN IDENTITY PREFLIGHT (FD #151 Round-1 finding 3)
# =====================================================================
#
# The authoritative DeepResearchRequest must be validated against any caller-supplied
# `create_run_kwargs` BEFORE any run creation, provider execution, source registration,
# source disposition or attempt/terminal write. A refusal must leave ZERO durable trace.


class _CountingTransport:
    """Wraps a real provider and counts execute() calls (proves no provider call)."""

    def __init__(self, inner):
        self._inner = inner
        self.calls = 0
        self.transport_type = inner.transport_type
        self.surface = inner.surface

    def capability(self):
        return self._inner.capability()

    def execute(self, request, *, proof_resolver=None, attempt_number=1):
        self.calls += 1
        return self._inner.execute(
            request, proof_resolver=proof_resolver, attempt_number=attempt_number)


def _run_with_kwargs(store, request, harness, archive, *, overrides=None, drop=(),
                     plan=None, transport=None):
    """Call the entry point with (possibly corrupted) caller-supplied run kwargs."""
    kwargs = _create_kwargs(request)
    if overrides:
        kwargs.update(overrides)
    for key in drop:
        kwargs.pop(key, None)
    return run_provider_attempt(
        store, request=request, provider=transport or harness.transport,
        provider_set=_ps(), transport_type=MOCK_TRANSPORT_TYPE,
        plan=plan or plan_attempt(provider_set=_ps(), attempt_number=1),
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=harness.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT, create_run_kwargs=kwargs,
    )


def _assert_zero_mutation(store, ledger_id, *, alias=None):
    """No run, no candidates, no dispositions, no attempts, no terminal, no events."""
    assert not store.contains(ledger_id), "a rejected call must not create the run"
    if alias is not None:
        assert not store.contains(alias)
    assert store.events(ledger_id) == [], "a rejected call must write NO audit events"


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("ledger_id", "L-OTHER"),              # 1
        ("request_id", "REQ-WRONG"),           # 2
        ("research_run_id", "RR-WRONG"),       # 3
        ("input_snapshot_hash", "d" * 64),     # 4
        ("pit_context_id", "PITC-WRONG"),      # 5a
        ("pit_mode", "LIVE_OPINION"),          # 5b
        ("as_of", "2026-06-01"),               # 5c
        ("case_id", "CASE-WRONG"),             # 6a
        ("case_version", "v9"),                # 6b
        ("evidence_gap_id", "EG-WRONG"),       # 6c
        ("rrm_manifest_id", "RRM-WRONG"),      # 6d
        ("idempotency_key", "IK-WRONG"),       # 7
    ],
)
def test_pref_01_to_07_identity_mismatch_is_refused_before_any_mutation(
    tmp_path, field, bad_value
):
    """Criteria 1-7: any request-bound field that disagrees is refused pre-mutation."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    counter = _CountingTransport(harness.transport)

    with pytest.raises(RetryPolicyError, match=field):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={field: bad_value}, transport=counter)

    assert counter.calls == 0, "the provider must NOT be called before validation"
    _assert_zero_mutation(store, request.ledger_id,
                          alias=bad_value if field == "ledger_id" else None)
    assert store.load_run_by_idempotency_key(idempotency_key_for_request(request)) is None


@pytest.mark.parametrize(
    "missing", ["ledger_id", "request_id", "research_run_id", "input_snapshot_hash",
                "idempotency_key", "pit_context_id", "case_version", "evidence_gap_id"]
)
def test_pref_08_missing_identity_field_is_refused(tmp_path, missing):
    """Criterion 8: a missing authoritative identity field is never defaulted."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    counter = _CountingTransport(harness.transport)

    with pytest.raises(OrchestrationError, match="missing required run field"):
        _run_with_kwargs(store, request, harness, archive, drop=(missing,),
                         transport=counter)

    assert counter.calls == 0
    _assert_zero_mutation(store, request.ledger_id)


def test_pref_08b_unknown_identity_field_is_refused(tmp_path):
    """An unrecognized run keyword is refused rather than silently carried."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    with pytest.raises(OrchestrationError, match="unknown run field"):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={"not_a_run_field": "x"})
    _assert_zero_mutation(store, request.ledger_id)


def test_pref_08c_blank_identity_value_is_refused(tmp_path):
    """A blank (present-but-empty) identity value is refused, not accepted."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    with pytest.raises(OrchestrationError, match="non-blank"):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={"notebook_identity": "   "})
    _assert_zero_mutation(store, request.ledger_id)


def test_pref_09_existing_run_with_mismatched_request_is_refused_and_preserved(tmp_path):
    """Criterion 9: an existing run + mismatched request is refused, record untouched."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    store = _store(tmp_path)
    failing = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)))
    first = _run_with_kwargs(store, request, failing, archive)
    assert first.outcome is ProviderExecutionOutcome.RETRY_SCHEDULED

    before = store.load_run("L-1")
    events_before = store.events("L-1")

    # a DIFFERENT logical request reusing the same ledger id must be refused
    other = _request(snapshot, request_id="REQ-OTHER", research_run_id="RR-OTHER")
    counter = _CountingTransport(Harness(archive).transport)
    with pytest.raises(RetryPolicyError, match="not bound to the target ledger run"):
        run_provider_attempt(
            store, request=other, provider=counter, provider_set=_ps(),
            transport_type=MOCK_TRANSPORT_TYPE,
            plan=plan_attempt(provider_set=_ps(), attempt_number=2,
                              previous_provider_surface=MOCK_PROVIDER_SURFACE),
            telemetry=not_exposed_provider_telemetry(),
            proof_resolver=Harness(archive).resolver, archive=archive,
            discovery_timestamp=DISCOVERED_AT,
        )
    assert counter.calls == 0, "refusal must precede provider execution"

    after = store.load_run("L-1")
    assert [(a.attempt_number, a.outcome) for a in after.attempts] == \
        [(a.attempt_number, a.outcome) for a in before.attempts]
    assert after.candidates == before.candidates
    assert after.dispositions == before.dispositions
    assert after.terminal_status == before.terminal_status
    assert after.result_sha256 == before.result_sha256
    assert store.events("L-1") == events_before, "no new durable events"


def test_pref_10_existing_run_with_consistent_identity_supports_a_valid_retry(tmp_path):
    """Criterion 10: a valid retry on an existing consistent run still works."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    store = _store(tmp_path)
    failing = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)))
    first = _run_with_kwargs(store, request, failing, archive)
    assert first.retry_decision.should_retry is True
    nxt = first.retry_decision.next_attempt

    healthy = Harness(archive)
    second = run_provider_attempt(
        store, request=request, provider=healthy.transport, provider_set=_ps(),
        transport_type=MOCK_TRANSPORT_TYPE, plan=nxt,
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=healthy.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT,
    )
    assert second.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = store.load_run("L-1")
    assert rec.terminal_status is TerminalStatus.SUCCESS
    assert [a.attempt_number for a in rec.attempts] == [1, 2]
    assert rec.result_sha256 == second.result_sha256


def test_pref_11_mode_a_fallback_is_not_falsely_rejected_by_the_preflight(tmp_path):
    """Criterion 11: the preflight must NOT force request-surface == run-surface.

    A Mode A request declares the surface that ultimately produces the result while the
    ledger run is configured with the INITIAL attempt's surface. The preflight must accept
    that combination (no new equality requirement that would break legitimate fallback).
    """
    archive, pit_store, snapshot = _world()
    request = _request(snapshot, provider_surface=SURFACE_B)
    ps = ProviderSet((SURFACE_A, SURFACE_B))
    store = _store(tmp_path)
    kwargs = _create_kwargs(request)
    kwargs["provider_surface"] = SURFACE_A          # the run's INITIAL configured surface
    harness_a = Harness(archive, MockTransportScript(
        attempt_outcomes=((1, "TRANSPORT_FAILURE"),)), surface=SURFACE_A)

    first = run_provider_attempt(
        store, request=request, provider=harness_a.transport, provider_set=ps,
        transport_type=MOCK_TRANSPORT_TYPE,
        plan=plan_attempt(provider_set=ps, attempt_number=1),
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=harness_a.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT, create_run_kwargs=kwargs,
    )
    assert store.load_run("L-1").provider_surface == SURFACE_A
    assert first.outcome is ProviderExecutionOutcome.RETRY_SCHEDULED
    nxt = first.retry_decision.next_attempt
    assert nxt.provider_surface == SURFACE_B

    harness_b = Harness(archive, surface=SURFACE_B)
    second = run_provider_attempt(
        store, request=request, provider=harness_b.transport, provider_set=ps,
        transport_type=MOCK_TRANSPORT_TYPE, plan=nxt,
        telemetry=not_exposed_provider_telemetry(),
        proof_resolver=harness_b.resolver, archive=archive,
        discovery_timestamp=DISCOVERED_AT,
    )
    assert second.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert store.load_run("L-1").terminal_status is TerminalStatus.SUCCESS


def test_pref_11b_retry_plan_on_a_new_run_is_refused(tmp_path):
    """A retry plan cannot create a run: a retry implies an existing attempt history."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    with pytest.raises(RetryPolicyError, match="requires an EXISTING ledger run"):
        _run_with_kwargs(
            store, request, harness, archive, transport=_CountingTransport(
                harness.transport),
            plan=plan_attempt(provider_set=_ps(), attempt_number=2,
                              previous_provider_surface=MOCK_PROVIDER_SURFACE),
        )
    _assert_zero_mutation(store, request.ledger_id)


def test_pref_11c_initial_plan_surface_must_match_the_created_run_surface(tmp_path):
    """The initial attempt must use the surface the run is created with."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    ps = ProviderSet((SURFACE_A, SURFACE_B))
    harness = Harness(archive, surface=SURFACE_B)
    store = _store(tmp_path)
    kwargs = _create_kwargs(request)
    kwargs["provider_surface"] = SURFACE_A

    with pytest.raises(RetryPolicyError, match="executing provider surface"):
        run_provider_attempt(
            store, request=request, provider=harness.transport, provider_set=ps,
            transport_type=MOCK_TRANSPORT_TYPE,
            plan=plan_attempt(provider_set=ps, attempt_number=1),
            telemetry=not_exposed_provider_telemetry(),
            proof_resolver=harness.resolver, archive=archive,
            discovery_timestamp=DISCOVERED_AT, create_run_kwargs=kwargs,
        )
    _assert_zero_mutation(store, request.ledger_id)


def test_pref_12_re_entry_after_a_rejected_request_leaves_no_pollution(tmp_path):
    """Criterion 12: after a refusal the SAME store accepts a valid request cleanly."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    with pytest.raises(RetryPolicyError):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={"request_id": "REQ-WRONG"})

    good = _run_with_kwargs(store, request, harness, archive)
    assert good.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = store.load_run("L-1")
    assert rec.request_id == request.request_id
    assert len(rec.attempts) == 1
    assert len(rec.candidates) == 2 and len(rec.dispositions) == 2
    assert rec.terminal_status is TerminalStatus.SUCCESS
    assert [e[1] for e in store.events("L-1")] == [
        "RUN_CREATED", "CANDIDATE_REGISTERED", "CANDIDATE_REGISTERED",
        "CANDIDATE_DISPOSED", "CANDIDATE_DISPOSED", "ATTEMPT_APPENDED",
        "RUN_TERMINALIZED",
    ]


def test_pref_13_valid_mock_execution_keeps_the_exact_result_binding(tmp_path):
    """Criterion 13: the corrected path preserves the exact result identity."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    counter = _CountingTransport(harness.transport)

    result = _run_with_kwargs(store, request, harness, archive, transport=counter)
    assert counter.calls == 1
    assert result.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    rec = store.load_run("L-1")
    assert rec.result_sha256 == hashlib.sha256(
        harness.transport.result_bytes).hexdigest()
    assert rec.result_sha256 == result.result_sha256
    assert rec.result_artifact_ref == harness.transport.synthesis_ref
    assert result.result_artifact_ref == harness.transport.synthesis_ref


def test_pref_14_no_provider_call_before_authoritative_identity_validation(tmp_path):
    """Criterion 14: identity validation strictly precedes provider execution."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)
    counter = _CountingTransport(harness.transport)

    with pytest.raises(RetryPolicyError):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={"case_version": "v9"}, transport=counter)
    assert counter.calls == 0

    valid = _run_with_kwargs(store, request, harness, archive, transport=counter)
    assert valid.outcome is ProviderExecutionOutcome.SUCCESS_FINALIZED
    assert counter.calls == 1


def test_pref_15_zero_new_durable_events_on_refusal(tmp_path):
    """Criterion 15: a refusal writes no events at all (new run)."""
    archive, pit_store, snapshot = _world()
    request = _request(snapshot)
    harness = Harness(archive)
    store = _store(tmp_path)

    with pytest.raises(RetryPolicyError):
        _run_with_kwargs(store, request, harness, archive,
                         overrides={"input_snapshot_hash": "e" * 64})

    assert store.events("L-1") == []
    assert not store.contains("L-1")
