"""M6.4 — TRUSTED PROOF-VERIFICATION SEAM — acceptance tests (FD #152, Option B).

RED→GREEN suite for the Founder-resolved M6.4 contract seam (FD #152):
``SUCCESS`` stays representable and testable, but it may be constructed ONLY
after BOTH the closed-corpus enforcement proof AND the request-isolation proof
have been VERIFIED through a trusted, provider-neutral
:class:`~qad.m6.research_contract.DeepResearchProofResolver` bound to the exact
run. A non-empty evidence-reference string is an IDENTIFIER only; enum values
alone never authorize SUCCESS; the direct ``DeepResearchResult(...)`` path cannot
bypass verification; the default resolver DENIES (M6.4 ships no production
resolver), and the real proof-producing/proof-resolving implementation belongs to
M6.7/M6.8.

Covers the FD #152 acceptance criteria (§11 #1–#25):
 1 SUCCESS with no resolver → rejected
 2 SUCCESS with evidence refs but no resolver → rejected
 3 SUCCESS with ENFORCED/VERIFIED enums but no resolver → rejected
 4 resolver returning an unverified closed-corpus proof → rejected
 5 resolver returning an unverified isolation proof → rejected
 6 only closed-corpus verified → rejected
 7 only isolation verified → rejected
 8 BOTH verified by the trusted resolver → SUCCESS accepted
 9 accepted SUCCESS retains the exact result-byte SHA-256
10 accepted SUCCESS retains the citation-list digest
11 accepted SUCCESS remains non_canonical == True
12 an evidence-reference string alone never authorizes SUCCESS
13 direct DeepResearchResult(...) cannot bypass the resolver
14 direct construction with invented proof references cannot bypass
15 a valid proof for Request A cannot authorize Request B
16 request_id mismatch fails    17 research_run_id mismatch fails
18 ledger_id mismatch fails     19 input_snapshot_hash mismatch fails
20 proof-kind mismatch fails
21 the default resolver is fail-closed
22 a deterministic stub resolver works only inside the test boundary
23 no provider / network / browser call
24 canonical schema count remains 68
25 RRM-01 remains unchanged
Criterion 26 (all existing Round 1–13 M6.4 regression tests stay GREEN) is
satisfied by ``test_m64_research_contract.py`` running in the same suite.

Run:  pytest tests/qad/m6/test_m64_proof_seam.py -q
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import socket
from pathlib import Path

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
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_i import (
    PITContext,
    PITContextMode,
    RunManifestRecord,
    RunManifestRecordRun_state,
)
from qad.persistence.reference import InMemoryPITContextStore, InMemoryRawSourceArchive
from qad.m6.ledger import (
    DeepResearchRunLedgerStore,
    validate_rrm_deep_research_runs,
)
from qad.m6.research_contract import (
    DEFAULT_PROOF_RESOLVER,
    NO_VERIFIED_PROOF_RESOLVER,
    ClosedCorpusEnforcement,
    DeepResearchProofResolver,
    DeepResearchRequest,
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
    compute_citation_list_sha256,
    compute_result_sha256,
    result_matches_hash,
)
from qad.m6.snapshot import SEALED_PIT_MODE, build_sealed_input_snapshot

AS_OF = "2026-01-01"
ADMITTED = "2025-12-15T00:00:00+00:00"
_FIXED_NOW = dt.datetime(2026, 10, 9, 12, 0, 0, tzinfo=dt.timezone.utc)
_PAYLOAD = b"synthesis text [1][2]"
_POINTERS = (
    SourcePointer(index=1, reference="https://a.example/1"),
    SourcePointer(index=2, reference="https://b.example/2"),
)

_UNSET = object()


# =====================================================================
# Fixtures
# =====================================================================

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


def _seed_case(store, case_id: str) -> None:
    sm = SecurityMaster(
        entity_id=f"SM-{case_id}", cik="0000998877", exchange="NYSE",
        name="M64 Seam Corp", primary_ticker="M64S",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )
    store.store(sm)
    cand = CandidateRecord(
        candidate_id=f"CR-{case_id}", entity_id=sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2025-10-01T00:00:00", evidence_freshness="2025-11-01",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW, signal_ids=[],
    )
    store.store(cand)
    store.store(CaseRecord(
        case_id=case_id, entity_id=sm.entity_id, candidate_id=cand.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN, as_of_date=AS_OF,
        opened_at="2025-10-02T08:00:00", research_director="Research Director",
    ))


def _snapshot(
    sources=(("S1", b"alpha"), ("S2", b"beta")),
    *,
    case_id: str = "CASE-1",
    case_version: str = "v1",
    as_of: str = AS_OF,
) -> "object":
    """Build a REAL M6.2 SEALED snapshot (authoritative fixture)."""
    archive = InMemoryRawSourceArchive(clock=lambda: dt.datetime.fromisoformat(ADMITTED))
    pit_store = InMemoryPITContextStore()
    _seed_case(pit_store, case_id)
    pit_store.store(PITContext(
        pit_context_id="PITC-1", case_id=case_id, as_of_date=as_of,
        mode=PITContextMode.SEALED_HISTORICAL_EVALUATION, created_by="founder",
    ))
    for sid, raw in sources:
        archive.admit_source(_src(sid, raw), raw)
    return build_sealed_input_snapshot(
        pit_context_store=pit_store, archive=archive, pit_context_id="PITC-1",
        case_version=case_version, source_ids=[s for s, _ in sources],
    )


def _request(snapshot, **overrides) -> DeepResearchRequest:
    kwargs = dict(
        snapshot=snapshot,
        request_id="REQ-1",
        research_run_id="RR-1",
        ledger_id="L-1",
        rrm_manifest_id="RRM-2026-0001",
        evidence_gap_id="EG-1",
        research_question="Why is the moat durable?",
        provider_surface="gemini_notebook",
    )
    kwargs.update(overrides)
    return build_deep_research_request(**kwargs)


def _build_result(*, request: DeepResearchRequest, proof_resolver=_UNSET, **overrides):
    """Build a SUCCESS result for ``request`` through the trusted seam."""
    kwargs = dict(
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
    )
    kwargs.update(overrides)
    if proof_resolver is not _UNSET:
        kwargs["proof_resolver"] = proof_resolver
    return build_deep_research_result(**kwargs)


# =====================================================================
# Test-only resolvers (NEVER production resolvers)
# =====================================================================

class _StubProofResolver:
    """DETERMINISTIC TEST-ONLY resolver. NOT a production resolver.

    Echoes the bound execution identity of the context it is given (so the
    run-binding checks are real), can DENY either proof kind, and can deliberately
    mis-bind its answer to prove that foreign / replayed proofs are rejected.
    """

    def __init__(
        self,
        *,
        closed_corpus: bool = True,
        isolation: bool = True,
        corpus_reason: str = "stub: closed-corpus proof not verified",
        isolation_reason: str = "stub: request-isolation proof not verified",
        bind_to: dict | None = None,
    ) -> None:
        self._closed_corpus = closed_corpus
        self._isolation = isolation
        self._corpus_reason = corpus_reason
        self._isolation_reason = isolation_reason
        self._bind_to = dict(bind_to or {})

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        is_corpus = context.proof_kind is ProofKind.CLOSED_CORPUS_ENFORCEMENT
        verified = self._closed_corpus if is_corpus else self._isolation
        reason = self._corpus_reason if is_corpus else self._isolation_reason

        def bound(name: str):
            return self._bind_to.get(name, getattr(context, name))

        return ProofVerification(
            proof_kind=bound("proof_kind"),
            verified=verified,
            request_id=bound("request_id"),
            research_run_id=bound("research_run_id"),
            ledger_id=bound("ledger_id"),
            provider_surface=bound("provider_surface"),
            input_snapshot_hash=bound("input_snapshot_hash"),
            evidence_ref=bound("evidence_ref") if verified else None,
            failure_reason=None if verified else reason,
        )


class _RecordingResolver(_StubProofResolver):
    """Verifies by echoing the context and records every context it was given."""

    def __init__(self) -> None:
        super().__init__()
        self.contexts: list[ProofVerificationRequest] = []

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        self.contexts.append(context)
        return super().verify_proof(context)


class _ReplayResolver:
    """Returns a verification bound to a PREVIOUSLY observed run (proof replay)."""

    def __init__(self, captured: ProofVerificationRequest) -> None:
        self._captured = captured

    def verify_proof(self, context: ProofVerificationRequest) -> ProofVerification:
        c = self._captured
        return ProofVerification(
            proof_kind=c.proof_kind,
            verified=True,
            request_id=c.request_id,
            research_run_id=c.research_run_id,
            ledger_id=c.ledger_id,
            provider_surface=c.provider_surface,
            input_snapshot_hash=c.input_snapshot_hash,
            evidence_ref=c.evidence_ref,
        )


def _seam_context(proof_kind: ProofKind = ProofKind.CLOSED_CORPUS_ENFORCEMENT) -> ProofVerificationRequest:
    return ProofVerificationRequest(
        proof_kind=proof_kind,
        request_id="REQ-1",
        research_run_id="RR-1",
        ledger_id="L-1",
        provider_surface="gemini_notebook",
        input_snapshot_hash="a" * 64,
        evidence_ref="EVID-CORPUS-1",
    )


# =====================================================================
# 1–8: SUCCESS requires BOTH proofs verified by the trusted resolver
# =====================================================================

class TestSuccessRequiresVerifiedProof:
    def test_01_success_without_resolver_is_rejected(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=None)
        # … and when the argument is simply omitted (the default is DENY)
        with pytest.raises(ResearchResultError):
            _build_result(request=req)

    def test_02_success_with_evidence_refs_but_no_resolver_is_rejected(self):
        """A non-empty evidence-reference string is an IDENTIFIER, not proof."""
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req,
                proof_resolver=None,
                # the ONLY 'proof-ish' input is a non-empty identifier string
                closed_corpus_enforcement=ClosedCorpusEnforcement.NOT_VERIFIED,
                isolation_verification=IsolationVerification.NOT_VERIFIED,
                closed_corpus_evidence_ref="CERTAINLY-A-CORPUS-PROOF",
                isolation_evidence_ref="CERTAINLY-AN-ISOLATION-PROOF",
            )

    def test_03_success_with_enforced_verified_enums_but_no_resolver_is_rejected(self):
        """ENFORCED / VERIFIED enum values alone never authorize SUCCESS."""
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=None)
        # the old exploit shape: enums + invented references, no trusted seam
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req,
                proof_resolver=None,
                closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                isolation_verification=IsolationVerification.VERIFIED,
                closed_corpus_evidence_ref="NOT-A-REAL-CORPUS-PROOF",
                isolation_evidence_ref="NOT-A-REAL-ISOLATION-PROOF",
            )

    def test_04_unverified_closed_corpus_proof_is_rejected(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=_StubProofResolver(closed_corpus=False))

    def test_05_unverified_isolation_proof_is_rejected(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=_StubProofResolver(isolation=False))

    def test_06_only_closed_corpus_verified_is_rejected(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req,
                proof_resolver=_StubProofResolver(closed_corpus=True, isolation=False),
            )

    def test_07_only_isolation_verified_is_rejected(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req,
                proof_resolver=_StubProofResolver(closed_corpus=False, isolation=True),
            )

    def test_08_both_verified_by_trusted_resolver_is_accepted(self):
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert ok.is_success is True
        assert ok.status is ResearchResultStatus.SUCCESS
        assert ok.closed_corpus_enforcement is ClosedCorpusEnforcement.ENFORCED
        assert ok.isolation_verification is IsolationVerification.VERIFIED
        # an accepted SUCCESS survives the consumption-boundary re-check
        assert ok.assert_proof_verified() is ok


# =====================================================================
# 9–11: properties of an ACCEPTED SUCCESS
# =====================================================================

class TestAcceptedSuccessProperties:
    def test_09_result_bytes_sha256_is_retained(self):
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert ok.result_sha256 == hashlib.sha256(_PAYLOAD).hexdigest()
        assert ok.result_sha256 == compute_result_sha256(_PAYLOAD)
        assert result_matches_hash(ok) is True

    def test_10_citation_list_digest_is_retained(self):
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert ok.citation_list_sha256 == compute_citation_list_sha256(_POINTERS)
        # deterministic + pointer-sensitive (companion digest, not the byte hash)
        assert ok.citation_list_sha256 != compute_citation_list_sha256(())

    def test_11_accepted_success_remains_non_canonical(self):
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert ok.non_canonical is True
        assert not hasattr(ok, "to_canonical_evidence")
        assert not hasattr(ok, "admit")
        for field in dataclasses.fields(ok):
            assert field.name not in (
                "canonical", "is_canonical", "evidence_id", "src_id",
                "validation_status", "canonical_truth",
            )


# =====================================================================
# 12: an evidence-reference string is never proof
# =====================================================================

class TestEvidenceStringIsNotProof:
    def test_12_evidence_reference_string_alone_never_authorizes_success(self):
        req = _request(_snapshot())
        # a blank reference is refused even with a verifying resolver …
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req, proof_resolver=_StubProofResolver(),
                closed_corpus_evidence_ref="   ",
            )
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req, proof_resolver=_StubProofResolver(),
                isolation_evidence_ref="\u200e",  # invisible-only identifier
            )
        # … and a valid-looking reference with a DENYING resolver is still refused
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=_StubProofResolver(closed_corpus=False))


# =====================================================================
# 13–14: the direct construction path cannot bypass verification
# =====================================================================

class TestDirectConstructionBypass:
    def test_13_direct_construction_cannot_bypass_the_resolver(self):
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="gemini_notebook",
                result_bytes=_PAYLOAD, result_sha256=compute_result_sha256(_PAYLOAD),
                closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                isolation_verification=IsolationVerification.VERIFIED,
                closed_corpus_evidence_ref="EVID-CORPUS-1",
                isolation_evidence_ref="EVID-ISOLATION-1",
            )

    def test_14_direct_construction_with_invented_proof_refs_cannot_bypass(self):
        for refs in (
            ("NOT-A-REAL-CORPUS-PROOF", "NOT-A-REAL-ISOLATION-PROOF"),
            ("EVID-CORPUS-1", "EVID-ISOLATION-1"),
        ):
            with pytest.raises(ResearchResultError):
                DeepResearchResult(
                    request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                    status=ResearchResultStatus.SUCCESS, provider_surface="gemini_notebook",
                    result_bytes=_PAYLOAD, result_sha256=compute_result_sha256(_PAYLOAD),
                    closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                    isolation_verification=IsolationVerification.VERIFIED,
                    closed_corpus_evidence_ref=refs[0],
                    isolation_evidence_ref=refs[1],
                )


# =====================================================================
# 15–20: verification is bound to the EXACT run (no proof replay)
# =====================================================================

class TestRunBinding:
    def test_15_valid_proof_for_request_a_cannot_authorize_request_b(self):
        req_a = _request(_snapshot(sources=(("S1", b"alpha"),)),
                         request_id="REQ-A", research_run_id="RR-A", ledger_id="L-A")
        req_b = _request(_snapshot(sources=(("S1", b"alpha"), ("S2", b"GAMMA"))),
                         request_id="REQ-B", research_run_id="RR-B", ledger_id="L-B")
        assert req_a.input_snapshot_hash != req_b.input_snapshot_hash

        recorder = _RecordingResolver()
        ok_a = _build_result(request=req_a, proof_resolver=recorder)
        assert ok_a.is_success is True
        corpus_ctx_a = next(
            c for c in recorder.contexts
            if c.proof_kind is ProofKind.CLOSED_CORPUS_ENFORCEMENT
        )
        # replaying A's verified proof while authorizing B is refused
        with pytest.raises(ResearchResultError):
            _build_result(request=req_b, proof_resolver=_ReplayResolver(corpus_ctx_a))
        # … while a legitimately bound resolver still authorizes B
        assert _build_result(request=req_b, proof_resolver=_RecordingResolver()).is_success

    @pytest.mark.parametrize(
        "field",
        ["request_id", "research_run_id", "ledger_id", "input_snapshot_hash"],
    )
    def test_16_to_19_identity_field_mismatch_fails(self, field):
        req = _request(_snapshot())
        foreign = {
            "request_id": "REQ-OTHER",
            "research_run_id": "RR-OTHER",
            "ledger_id": "L-OTHER",
            "input_snapshot_hash": "b" * 64,
        }[field]
        with pytest.raises(ResearchResultError):
            _build_result(request=req, proof_resolver=_StubProofResolver(bind_to={field: foreign}))

    def test_20_proof_kind_mismatch_fails(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req,
                proof_resolver=_StubProofResolver(
                    bind_to={"proof_kind": ProofKind.REQUEST_ISOLATION}
                ),
            )


# =====================================================================
# 21–22: default deny + the test-boundary stub
# =====================================================================

class TestDefaultDenyAndTestBoundary:
    def test_21_default_resolver_is_fail_closed(self):
        context = _seam_context()
        verdict = DEFAULT_PROOF_RESOLVER.verify_proof(context)
        assert isinstance(verdict, ProofVerification)
        assert verdict.verified is False
        assert verdict.failure_reason == NO_VERIFIED_PROOF_RESOLVER
        assert verdict.evidence_ref is None
        # M6.4 alone therefore cannot produce a real SUCCESS
        with pytest.raises(ResearchResultError):
            _build_result(request=_request(_snapshot()), proof_resolver=DEFAULT_PROOF_RESOLVER)

    def test_22_deterministic_stub_resolver_works_only_in_the_test_boundary(self):
        import qad.m6.research_contract as rc

        # the stub is defined HERE (test boundary), not in the production module
        assert _StubProofResolver.__module__ == __name__
        assert not hasattr(rc, "_StubProofResolver")
        # it still satisfies the production seam interface (Protocol conformance)
        assert isinstance(_StubProofResolver(), DeepResearchProofResolver)
        # the production module exposes exactly one public resolver OBJECT
        # (the interface Protocol is a class, not a resolver instance), and that
        # object denies
        public_resolvers = [
            name for name in dir(rc)
            if not name.startswith("_")
            and not isinstance(getattr(rc, name), type)
            and callable(getattr(getattr(rc, name), "verify_proof", None))
        ]
        assert public_resolvers == ["DEFAULT_PROOF_RESOLVER"]
        assert isinstance(rc.DeepResearchProofResolver, type)  # the seam interface
        assert DEFAULT_PROOF_RESOLVER.verify_proof(_seam_context()).verified is False


# =====================================================================
# 23–25: boundaries (no transport, no schema change, RRM-01 unchanged)
# =====================================================================

class TestBoundaries:
    def test_23_no_provider_transport_or_network_call(self, monkeypatch):
        def _boom(*a, **k):
            raise AssertionError("network access attempted by the M6.4 proof seam")

        monkeypatch.setattr(socket, "socket", _boom)
        monkeypatch.setattr(socket, "create_connection", _boom)
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert ok.non_canonical is True
        import qad.m6.research_contract as rc

        source = Path(rc.__file__).read_text(encoding="utf-8").lower()
        # no transport / provider library or client may be imported at all
        for banned in (
            "import requests", "import urllib", "import socket", "import httpx",
            "import selenium", "import playwright", "import chromedriver",
            "import gemini", "import notebook", "from selenium", "from playwright",
            "chrome.debugger",
        ):
            assert banned not in source

    def test_24_canonical_schema_count_remains_68(self):
        assert len(CANONICAL_SCHEMAS) == 68
        for added in (
            "M64-01", "PROOF-01", "PROOFVER-01", "ATTESTATION-01", "PRF-01",
        ):
            assert added not in CANONICAL_SCHEMAS

    def test_25_rrm01_linkage_is_unchanged(self, tmp_path):
        assert "RRM-01" in CANONICAL_SCHEMAS
        store = DeepResearchRunLedgerStore(
            tmp_path / "ledger.sqlite3", clock=lambda: _FIXED_NOW
        )
        store.create_run(
            ledger_id="L-1", research_run_id="RR-1", rrm_manifest_id="RRM-2026-0001",
            case_id="CASE-1", case_version="v1", evidence_gap_id="EG-1", request_id="REQ-1",
            idempotency_key="IDEM-1", notebook_identity="nb-0193-1",
            pit_context_id="PITC-1", pit_mode=SEALED_PIT_MODE, as_of=AS_OF,
            input_snapshot_hash="a" * 64, provider_surface="gemini_notebook",
            transport_type="BROWSER_UI_AUTOMATION",
        )
        refs = validate_rrm_deep_research_runs(store, ["L-1"])
        assert refs == ["L-1"]
        rrm = RunManifestRecord(
            as_of_date=AS_OF, case_id="CASE-1", case_version="v1",
            manifest_id="RRM-2026-0001", models_used=["NOT_EXPOSED_BY_PROVIDER"],
            providers={"gemini_notebook": "gemini_notebook"},
            run_state=RunManifestRecordRun_state.RUNNING,
            selection_policy_version="v1", start_time=_FIXED_NOW.isoformat(),
            universe_version="v1", deep_research_runs=refs,
        )
        assert rrm.deep_research_runs == ["L-1"]
        assert all(isinstance(x, str) for x in rrm.deep_research_runs)
        # structured dictionaries are still rejected (id refs only)
        with pytest.raises(Exception):
            validate_rrm_deep_research_runs(store, [{"not": "a string"}])  # type: ignore[list-item]


# =====================================================================
# Seam contract shape + §8 (the resolver is never stored on the result)
# =====================================================================

class TestSeamContractShape:
    def test_26_verification_is_structured_and_immutable(self):
        verdict = DEFAULT_PROOF_RESOLVER.verify_proof(_seam_context())
        assert not isinstance(verdict, bool)
        for name in (
            "proof_kind", "verified", "evidence_ref", "failure_reason",
            "request_id", "research_run_id", "ledger_id", "provider_surface",
            "input_snapshot_hash",
        ):
            assert hasattr(verdict, name)
        with pytest.raises(dataclasses.FrozenInstanceError):
            verdict.verified = True  # type: ignore[misc]
        context = _seam_context()
        with pytest.raises(dataclasses.FrozenInstanceError):
            context.request_id = "TAMPERED"  # type: ignore[misc]
        # a verified proof MUST carry a resolved reference, not just a flag
        with pytest.raises(ResearchResultError):
            ProofVerification(
                proof_kind=ProofKind.REQUEST_ISOLATION, verified=True,
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                provider_surface="p", input_snapshot_hash="a" * 64,
            )

    def test_27_result_never_carries_a_resolver_or_executable_capability(self):
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        assert not hasattr(ok, "proof_resolver")
        assert not hasattr(ok, "resolver")
        for field in dataclasses.fields(ok):
            assert field.name not in (
                "proof_resolver", "resolver", "browser", "transport", "connection",
            )
            assert not callable(getattr(ok, field.name))
        # the persisted/carried identity is data only
        assert ok.input_snapshot_hash == req.input_snapshot_hash


# =====================================================================
# Round-14 reviewer-driven closure (FD #152) — the bypasses the family-
# independent reviewer demonstrated in round 14 must all be refused.
# =====================================================================

class TestRound14BypassClosure:
    def test_r14_01_result_type_is_final_and_cannot_be_subclassed(self):
        """A subclass could override __post_init__ and skip the SUCCESS gate."""
        with pytest.raises(ResearchResultError):

            class _FakeSuccess(DeepResearchResult):  # noqa: D401
                def __post_init__(self) -> None:  # never enforces the proof gate
                    pass

    def test_r14_02_no_importable_attestation_token_exists(self):
        """The minting guard must not be a module attribute reachable by name."""
        import qad.m6.research_contract as rc

        assert not hasattr(rc, "_ATTESTATION_TOKEN")
        for name in dir(rc):
            assert not name.upper().endswith("_TOKEN"), name
        # the guard is closure-captured: a fabricated guard is refused
        with pytest.raises(ResearchResultError):
            rc._VerifiedProofAttestation(
                _guard=object(),
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                provider_surface="gemini_notebook", input_snapshot_hash="a" * 64,
                closed_corpus_evidence_ref="EVID-CORPUS-1",
                isolation_evidence_ref="EVID-ISOLATION-1",
                result_sha256="c" * 64, citation_list_sha256="d" * 64,
        )

    def test_r15_08_no_importable_minting_function_exists(self):
        """Round 15: removing the token was not enough — the MINTER itself must not
        be a module attribute, or a caller can mint an attestation from bare identity
        strings and construct a SUCCESS with no resolver at all."""
        import qad.m6.research_contract as rc

        assert not hasattr(rc, "_mint_verified_proof_attestation")
        for name in dir(rc):
            assert "MINT" not in name.upper(), name
        # the ONLY module-visible entry into the seam is the full verification
        # path, and it never mints without a resolver that verifies BOTH proofs
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            rc._verify_success_proofs(
                request=req, proof_resolver=None,
                corpus_evidence_ref="EVID-CORPUS-1",
                isolation_evidence_ref="EVID-ISOLATION-1",
                result_sha256="c" * 64, citation_list_sha256="d" * 64,
            )
        with pytest.raises(ResearchResultError):
            rc._verify_success_proofs(
                request=req, proof_resolver=_StubProofResolver(closed_corpus=False),
                corpus_evidence_ref="EVID-CORPUS-1",
                isolation_evidence_ref="EVID-ISOLATION-1",
                result_sha256="c" * 64, citation_list_sha256="d" * 64,
            )
        # … and the sanctioned builder path still works
        assert _build_result(
            request=req, proof_resolver=_StubProofResolver()
        ).assert_proof_verified() is not None

    def test_r14_03_object_new_success_refused_at_the_consumption_boundary(self):
        """object.__new__ skips __post_init__ — the boundary re-check must catch it."""
        req = _request(_snapshot())
        src = _build_result(request=req, proof_resolver=_StubProofResolver())
        forged = object.__new__(DeepResearchResult)
        for f in dataclasses.fields(DeepResearchResult):
            if f.name == "_proof_attestation":
                continue
            object.__setattr__(forged, f.name, getattr(src, f.name))
        object.__setattr__(forged, "_proof_attestation", None)
        # data-wise it looks like a success …
        assert forged.status is ResearchResultStatus.SUCCESS
        assert forged.is_success is True
        # … but it can never be CONSUMED as one
        with pytest.raises(ResearchResultError):
            forged.assert_proof_verified()

    def test_r14_04_post_construction_byte_tamper_is_caught(self):
        """A frozen dataclass does NOT stop object.__setattr__ — re-check must."""
        req = _request(_snapshot())
        ok = _build_result(request=req, proof_resolver=_StubProofResolver())
        ok.assert_proof_verified()
        object.__setattr__(ok, "result_bytes", b"post-construction tamper")
        assert result_matches_hash(ok) is False
        with pytest.raises(ResearchResultError):
            ok.assert_proof_verified()

    def test_r14_05_builder_success_passes_the_consumption_boundary(self):
        ok = _build_result(request=_request(_snapshot()), proof_resolver=_StubProofResolver())
        assert ok.assert_proof_verified() is ok

    def test_r14_06_attestation_is_not_transferable_between_results(self):
        """Copying a genuine attestation onto a different run's result is refused."""
        req_a = _request(_snapshot(sources=(("S1", b"alpha"),)),
                         request_id="REQ-A", research_run_id="RR-A", ledger_id="L-A")
        req_b = _request(_snapshot(),
                         request_id="REQ-B", research_run_id="RR-B", ledger_id="L-B")
        ok_a = _build_result(request=req_a, proof_resolver=_StubProofResolver())
        ok_b = _build_result(request=req_b, proof_resolver=_StubProofResolver())
        ok_a.assert_proof_verified()
        object.__setattr__(ok_b, "_proof_attestation", ok_a._proof_attestation)
        with pytest.raises(ResearchResultError):
            ok_b.assert_proof_verified()

    def test_r14_07_consumption_boundary_applies_only_to_success(self):
        fail = build_deep_research_result(
            request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
            status=ResearchResultStatus.PROVIDER_CANNOT_ENFORCE_SEALED_INPUT,
            provider_surface="gemini_notebook",
            failure_detail="provider cannot enforce the sealed input",
            closed_corpus_enforcement=ClosedCorpusEnforcement.CANNOT_ENFORCE,
        )
        assert fail.is_success is False
        with pytest.raises(ResearchResultError):
            fail.assert_proof_verified()

    def test_r16_09_bytes_and_matching_digest_replacement_is_refused(self):
        """Round 16: replacing the bytes AND the matching digest must still be caught.

        The validated digests are bound into the private attestation, so a
        consistently re-written (bytes, result_sha256) pair no longer agrees with
        what the trusted path validated.
        """
        ok = _build_result(request=_request(_snapshot()), proof_resolver=_StubProofResolver())
        ok.assert_proof_verified()
        tampered = b"replaced payload"
        object.__setattr__(ok, "result_bytes", tampered)
        object.__setattr__(ok, "result_sha256", compute_result_sha256(tampered))
        # the bytes and the digest now agree with each other …
        assert result_matches_hash(ok) is True
        # … but they do not agree with the attested, trusted-path-validated digest
        with pytest.raises(ResearchResultError):
            ok.assert_proof_verified()

    def test_r16_10_citation_digest_replacement_is_refused(self):
        ok = _build_result(request=_request(_snapshot()), proof_resolver=_StubProofResolver())
        ok.assert_proof_verified()
        new_pointers = (SourcePointer(index=1, reference="https://evil.example/1"),)
        object.__setattr__(ok, "source_pointers", new_pointers)
        object.__setattr__(
            ok, "citation_list_sha256", compute_citation_list_sha256(new_pointers)
        )
        with pytest.raises(ResearchResultError):
            ok.assert_proof_verified()

    def test_r16_11_builder_rejects_caller_digest_that_disagrees(self):
        """A caller-asserted digest that disagrees with the payload is refused."""
        req = _request(_snapshot())
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req, proof_resolver=_StubProofResolver(),
                result_sha256="e" * 64,
            )
        with pytest.raises(ResearchResultError):
            _build_result(
                request=req, proof_resolver=_StubProofResolver(),
                citation_list_sha256="f" * 64,
            )
