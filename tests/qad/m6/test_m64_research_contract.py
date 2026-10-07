"""M6.4 — Research Request/Result Adapter Contract — acceptance tests (FD #151).

RED→GREEN suite for the M6.4 cluster: the S10-facing logical request/result
boundary for Deep Research. Proves:

* the authoritative M6.2 SEALED snapshot cannot be overridden by the caller;
* S10 stateless / REQUEST-ISOLATED semantics are carried, not weakened;
* request identity is deterministic (no clock / UUID / path influence);
* results are always NON-CANONICAL, blank output can never be SUCCESS, and the
  result hash is exact over the stored bytes;
* source pointers are preserved faithfully as DISCOVERED SOURCE REFERENCES;
* ledger/RRM linkage keeps the existing types;
* no provider transport, no network, no canonical schema change.

Run:  pytest tests/qad/m6/test_m64_research_contract.py -q
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
    REQUEST_ISOLATION_UNVERIFIED,
    S10_CAPABILITY,
    ClosedCorpusEnforcement,
    DeepResearchRequest,
    DeepResearchResult,
    IsolationVerification,
    RequestAuthorityViolation,
    ResearchRequestError,
    ResearchResultError,
    ResearchResultStatus,
    SourceCorpusDescriptor,
    SourcePointer,
    build_deep_research_request,
    build_deep_research_result,
    compute_result_sha256,
    result_matches_hash,
    validate_ledger_linkage,
)
from qad.m6.snapshot import (
    PROVIDER_CANNOT_ENFORCE_SEALED_INPUT,
    SEALED_PIT_MODE,
    SealedInputSnapshot,
    SealedSourceSnapshot,
    build_sealed_input_snapshot,
)

AS_OF = "2026-01-01"
ADMITTED = "2025-12-15T00:00:00+00:00"
_FIXED_NOW = dt.datetime(2026, 10, 7, 12, 0, 0, tzinfo=dt.timezone.utc)


# =====================================================================
# Fixtures / helpers
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
        name="M64 Corp", primary_ticker="M64X",
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
) -> SealedInputSnapshot:
    """Build a REAL M6.2 SEALED snapshot (authoritative fixture)."""
    archive = InMemoryRawSourceArchive(
        clock=lambda: dt.datetime.fromisoformat(ADMITTED)
    )
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


def _request(snapshot: SealedInputSnapshot, **overrides):
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


def _result(**overrides):
    payload = b"synthesis text [1][2]"
    kwargs = dict(
        request_id="REQ-1",
        research_run_id="RR-1",
        ledger_id="L-1",
        status=ResearchResultStatus.SUCCESS,
        provider_surface="gemini_notebook",
        result_bytes=payload,
        result_sha256=hashlib.sha256(payload).hexdigest(),
        source_pointers=(SourcePointer(index=1, reference="https://a.example/1"),
                         SourcePointer(index=2, reference="https://b.example/2")),
        completed_at="2026-10-07T12:05:00+00:00",
        # M6.0 §5 / §11.2 R7: a PASS must carry positive proof for both
        closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
        isolation_verification=IsolationVerification.VERIFIED,
        closed_corpus_evidence_ref="EVID-CORPUS-1",
        isolation_evidence_ref="EVID-ISOLATION-1",
    )
    kwargs.update(overrides)
    return build_deep_research_result(**kwargs)


def _ledger(tmp_path: Path) -> tuple[DeepResearchRunLedgerStore, str]:
    store = DeepResearchRunLedgerStore(tmp_path / "ledger.sqlite3", clock=lambda: _FIXED_NOW)
    store.create_run(
        ledger_id="L-1", research_run_id="RR-1", rrm_manifest_id="RRM-2026-0001",
        case_id="CASE-1", case_version="v1", evidence_gap_id="EG-1", request_id="REQ-1",
        idempotency_key="IDEM-1", notebook_identity="nb-0193-1",
        pit_context_id="PITC-1", pit_mode=SEALED_PIT_MODE, as_of=AS_OF,
        input_snapshot_hash="a" * 64, provider_surface="gemini_notebook",
        transport_type="BROWSER_UI_AUTOMATION",
    )
    return store, "L-1"


# =====================================================================
# 1–5: request built from / derived from the authoritative snapshot
# =====================================================================


class TestRequestAuthority:
    def test_01_valid_snapshot_builds_valid_request(self):
        snap = _snapshot()
        req = _request(snap)
        assert req.request_id == "REQ-1"
        assert req.capability == S10_CAPABILITY
        assert req.non_canonical is True

    def test_02_case_id_derives_from_snapshot(self):
        snap = _snapshot(case_id="CASE-77")
        req = _request(snap)
        assert req.case_id == snap.case_id == "CASE-77"

    def test_03_case_version_derives_from_snapshot(self):
        snap = _snapshot(case_version="v9")
        req = _request(snap)
        assert req.case_version == snap.case_version == "v9"

    def test_04_pit_mode_and_as_of_derive_from_snapshot(self):
        snap = _snapshot(as_of="2026-02-02")
        req = _request(snap)
        assert req.pit_mode == snap.pit_mode == SEALED_PIT_MODE
        assert req.as_of == snap.as_of == "2026-02-02"
        assert req.pit_context_id == snap.pit_context_id

    def test_05_input_snapshot_hash_derives_from_snapshot(self):
        snap = _snapshot()
        req = _request(snap)
        assert req.input_snapshot_hash == snap.input_snapshot_hash
        assert req.snapshot_id == snap.snapshot_id


# =====================================================================
# 6–8: caller overrides fail closed
# =====================================================================


class TestCallerOverrideRefused:
    def test_06_caller_cannot_override_source_corpus(self):
        snap = _snapshot()
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_source_ids=["S1", "S9"])
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_source_ids=["S1", "S1"])  # duplicate
        # a matching claim is accepted (assertion, not an override)
        req = _request(snap, claimed_source_ids=["S2", "S1"])
        assert set(req.source_ids) == {"S1", "S2"}

    def test_07_caller_cannot_override_as_of(self):
        snap = _snapshot()
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_as_of="2020-01-01")
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_pit_mode="LIVE_CASE_UPDATE")
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_input_snapshot_hash="b" * 64)
        assert _request(snap, claimed_as_of=snap.as_of).as_of == snap.as_of

    def test_08_caller_cannot_override_case_identity(self):
        snap = _snapshot()
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_case_id="CASE-OTHER")
        with pytest.raises(RequestAuthorityViolation):
            _request(snap, claimed_case_version="v99")
        # a non-snapshot object cannot be used as the authority at all
        with pytest.raises(RequestAuthorityViolation):
            _request("not-a-snapshot")


# =====================================================================
# 9–11: propagation, immutability
# =====================================================================


class TestPropagationAndImmutability:
    def test_09_closed_corpus_required_propagates_true(self):
        snap = _snapshot()
        req = _request(snap)
        assert snap.closed_corpus_required is True
        assert req.corpus.closed_corpus_required is True
        assert req.closed_corpus_required is True
        assert req.provider.closed_corpus_required is True

    def test_10_request_isolation_requirement_propagates(self):
        req = _request(_snapshot())
        assert req.request_isolation_required is True
        assert req.provider.request_isolation_required is True
        # the envelope exposes no accumulated-context input surface
        for forbidden in ("notebook_chat", "previous_report", "workspace",
                          "session_id", "chat_history", "prior_notebook_sources"):
            assert not hasattr(req, forbidden)

    def test_11_request_structures_are_immutable(self):
        req = _request(_snapshot())
        with pytest.raises(dataclasses.FrozenInstanceError):
            req.case_id = "TAMPERED"  # type: ignore[misc]
        with pytest.raises(dataclasses.FrozenInstanceError):
            req.corpus.closed_corpus_required = False  # type: ignore[misc]
        with pytest.raises(dataclasses.FrozenInstanceError):
            req.provider.provider_surface = "other"  # type: ignore[misc]


# =====================================================================
# 12–16: deterministic request identity, injection refused
# =====================================================================


class TestRequestIdentity:
    def test_12_same_semantic_request_same_payload_hash(self):
        snap = _snapshot()
        a = _request(snap, request_id="REQ-A")
        b = _request(snap, request_id="REQ-B")
        assert a.request_payload_hash == b.request_payload_hash

    def test_13_volatile_identifiers_do_not_alter_payload_hash(self):
        snap = _snapshot()
        base = _request(snap)
        # different request UUID / orchestration ids / provider surface / timeout
        other = _request(
            snap, request_id="REQ-ZZZ", research_run_id="RR-ZZZ", ledger_id="L-ZZZ",
            rrm_manifest_id="RRM-ZZZ", provider_surface="another_surface",
            timeout_seconds=123,
        )
        assert other.request_payload_hash == base.request_payload_hash

    def test_14_changing_research_question_changes_payload_hash(self):
        snap = _snapshot()
        a = _request(snap, research_question="Q1")
        b = _request(snap, research_question="Q2")
        assert a.request_payload_hash != b.request_payload_hash

    def test_15_changing_input_snapshot_hash_changes_payload_hash(self):
        snap_a = _snapshot(sources=(("S1", b"alpha"), ("S2", b"beta")))
        snap_b = _snapshot(sources=(("S1", b"alpha"), ("S2", b"GAMMA")))
        assert snap_a.input_snapshot_hash != snap_b.input_snapshot_hash
        req_a = _request(snap_a)
        req_b = _request(snap_b)
        assert req_a.request_payload_hash != req_b.request_payload_hash
        # and the payload hash is a stable hex digest, not a memory/object id
        assert len(req_a.request_payload_hash) == 64
        assert req_a.request_payload_hash == _request(snap_a).request_payload_hash

    def test_16_invalid_source_authority_cannot_be_injected(self):
        snap = _snapshot(sources=(("S1", b"alpha"),))
        # claimed corpus that disagrees (extra / duplicate / empty) fails closed
        for bad in (["S1", "S2"], ["S1", "S1"], [], ["S1"], ["S2"]):
            if bad == ["S1"]:
                continue  # exact match is legitimate
            with pytest.raises(RequestAuthorityViolation):
                _request(snap, claimed_source_ids=bad)
        # the request carries no caller-supplied bytes / hashes whatsoever
        req = _request(snap)
        assert req.corpus.exact_blob_hashes == (
            ("S1", hashlib.sha256(b"alpha").hexdigest()),
        )
        for field in dataclasses.fields(req):
            assert "bytes" not in field.name
            assert field.name not in ("source_hashes", "content_hash")


# =====================================================================
# 17–22: result contract
# =====================================================================


class TestResultContract:
    def test_17_success_requires_non_empty_content(self):
        with pytest.raises(ResearchResultError):
            _result(result_bytes=b"", result_sha256=hashlib.sha256(b"").hexdigest())
        with pytest.raises(ResearchResultError):
            _result(result_bytes=None, result_sha256="a" * 64)

    def test_18_success_requires_exact_sha256(self):
        with pytest.raises(ResearchResultError):
            _result(result_sha256=None)
        with pytest.raises(ResearchResultError):
            _result(result_sha256="f" * 64)  # wrong digest
        ok = _result()
        assert result_matches_hash(ok) is True
        assert ok.result_sha256 == compute_result_sha256(ok.result_bytes)

    def test_19_changed_result_bytes_change_hash(self):
        one = b"report one"
        two = b"report two"
        assert compute_result_sha256(one) != compute_result_sha256(two)
        with pytest.raises(ResearchResultError):
            _result(result_bytes=two,
                    result_sha256=hashlib.sha256(one).hexdigest())
        ok = _result(result_bytes=two, result_sha256=hashlib.sha256(two).hexdigest())
        assert result_matches_hash(ok) is True

    def test_20_source_pointers_preserved_and_non_canonical(self):
        ok = _result()
        assert [p.reference for p in ok.source_pointers] == [
            "https://a.example/1", "https://b.example/2",
        ]
        assert ok.non_canonical is True
        # a pointer is a DISCOVERED SOURCE REFERENCE, not canonical evidence
        ptr = ok.source_pointers[0]
        assert dataclasses.fields(ptr) and not hasattr(ptr, "src_id")
        assert not hasattr(ptr, "evidence_id")
        with pytest.raises(ResearchResultError):
            _result(source_pointers=(SourcePointer(index=1, reference="   "),))

    def test_21_result_cannot_self_declare_canonical_evidence(self):
        ok = _result()
        assert ok.non_canonical is True
        assert not hasattr(ok, "to_canonical_evidence")
        assert not hasattr(ok, "admit")
        for field in dataclasses.fields(ok):
            assert field.name not in (
                "canonical", "is_canonical", "evidence_id", "src_id",
                "validation_status", "canonical_truth",
            )

    def test_22_blank_provider_result_cannot_become_success(self):
        with pytest.raises(ResearchResultError):
            _result(result_bytes=b"")
        # the correct representation of blank/absent output is a typed failure
        failed = _result(
            status=ResearchResultStatus.RESEARCH_UNAVAILABLE,
            result_bytes=None, result_sha256=None,
            failure_detail="provider returned no synthesis",
        )
        assert failed.status is ResearchResultStatus.RESEARCH_UNAVAILABLE
        assert failed.is_success is False


# =====================================================================
# 23–27: failure vocabulary + linkage
# =====================================================================


class TestFailureVocabularyAndLinkage:
    def test_23_failure_represents_research_unavailable(self):
        r = _result(status=ResearchResultStatus.RESEARCH_UNAVAILABLE,
                    result_bytes=None, result_sha256=None,
                    failure_detail="retries exhausted")
        assert r.status is ResearchResultStatus.RESEARCH_UNAVAILABLE
        with pytest.raises(ResearchResultError):  # failure must be documented
            _result(status=ResearchResultStatus.RESEARCH_UNAVAILABLE,
                    result_bytes=None, result_sha256=None)
        with pytest.raises(ResearchResultError):  # no fabricated hash
            _result(status=ResearchResultStatus.RESEARCH_UNAVAILABLE,
                    result_bytes=None, result_sha256="a" * 64,
                    failure_detail="x")

    def test_24_failure_represents_transport_failure(self):
        r = _result(status=ResearchResultStatus.TRANSPORT_FAILURE,
                    result_bytes=None, result_sha256=None,
                    failure_detail="CSRF token not found; page structure changed")
        assert r.status is ResearchResultStatus.TRANSPORT_FAILURE
        assert r.is_success is False

    def test_25_failure_represents_provider_cannot_enforce_sealed_input(self):
        r = _result(
            status=ResearchResultStatus.PROVIDER_CANNOT_ENFORCE_SEALED_INPUT,
            result_bytes=None, result_sha256=None,
            failure_detail="provider cannot disable uncontrolled discovery",
            closed_corpus_enforcement=ClosedCorpusEnforcement.CANNOT_ENFORCE,
        )
        assert r.status.value == PROVIDER_CANNOT_ENFORCE_SEALED_INPUT
        # cannot-enforce must never be dressed up as SUCCESS
        with pytest.raises(ResearchResultError):
            _result(closed_corpus_enforcement=ClosedCorpusEnforcement.CANNOT_ENFORCE)

    def test_26_failure_represents_request_isolation_unverified(self):
        r = _result(
            status=ResearchResultStatus.REQUEST_ISOLATION_UNVERIFIED,
            result_bytes=None, result_sha256=None,
            failure_detail="no positive clean-context proof",
            isolation_verification=IsolationVerification.UNVERIFIED,
        )
        assert r.status.value == REQUEST_ISOLATION_UNVERIFIED
        with pytest.raises(ResearchResultError):
            _result(isolation_verification=IsolationVerification.UNVERIFIED)

    def test_27_result_retains_linkage_and_ledger_resolves(self, tmp_path):
        store, ledger_id = _ledger(tmp_path)
        ok = _result(ledger_id=ledger_id)
        assert (ok.request_id, ok.research_run_id, ok.ledger_id) == ("REQ-1", "RR-1", ledger_id)
        validate_ledger_linkage(store, ledger_id=ledger_id, research_run_id="RR-1")
        with pytest.raises(Exception):
            validate_ledger_linkage(store, ledger_id="L-MISSING", research_run_id="RR-1")
        with pytest.raises(Exception):
            validate_ledger_linkage(store, ledger_id=ledger_id, research_run_id="RR-OTHER")

    def test_30_rrm_linkage_remains_list_of_ledger_id_strings(self, tmp_path):
        store, ledger_id = _ledger(tmp_path)
        refs = validate_rrm_deep_research_runs(store, [ledger_id])
        assert refs == [ledger_id]
        rrm = RunManifestRecord(
            as_of_date=AS_OF, case_id="CASE-1", case_version="v1",
            manifest_id="RRM-2026-0001", models_used=["NOT_EXPOSED_BY_PROVIDER"],
            providers={"gemini_notebook": "gemini_notebook"},
            run_state=RunManifestRecordRun_state.RUNNING,
            selection_policy_version="v1", start_time=_FIXED_NOW.isoformat(),
            universe_version="v1", deep_research_runs=refs,
        )
        assert rrm.deep_research_runs == [ledger_id]
        assert all(isinstance(x, str) for x in rrm.deep_research_runs)
        with pytest.raises(Exception):
            validate_rrm_deep_research_runs(store, [{"not": "a string"}])  # type: ignore[list-item]


# =====================================================================
# 28–30: no schema change, no network
# =====================================================================


class TestBoundaries:
    def test_28_no_canonical_schema_count_change(self):
        assert len(CANONICAL_SCHEMAS) == 68
        assert "M64-01" not in CANONICAL_SCHEMAS

    def test_29_no_provider_transport_or_network_call(self, monkeypatch):
        """Building request/result must not touch the network."""
        def _boom(*a, **k):
            raise AssertionError("network access attempted by M6.4")

        monkeypatch.setattr(socket, "socket", _boom)
        monkeypatch.setattr(socket, "create_connection", _boom)
        snap = _snapshot()
        req = _request(snap)
        ok = _result()
        assert req.non_canonical is True and ok.non_canonical is True
        # static corroboration: the module imports no network/transport library
        import qad.m6.research_contract as rc

        source = Path(rc.__file__).read_text(encoding="utf-8").lower()
        for banned in ("import requests", "import urllib", "import socket",
                       "import httpx", "selenium", "playwright", "chromedriver"):
            assert banned not in source


# =====================================================================
# 31–35: reviewer-driven hardening (round-2)
# =====================================================================


class TestReviewHardening:
    def test_31_forged_snapshot_fails_closed(self):
        """An inconsistent/forged SEALED snapshot must not become a request."""
        good = _snapshot()
        # a tampered authority field no longer matches the deterministic identity
        for forged in (
            dataclasses.replace(good, case_id="CASE-FORGED"),
            dataclasses.replace(good, case_version="v-forged"),
            dataclasses.replace(good, as_of="1900-01-01"),
            dataclasses.replace(good, input_snapshot_hash="0" * 64),
            dataclasses.replace(good, snapshot_id="1" * 64),
        ):
            with pytest.raises(RequestAuthorityViolation):
                _request(forged)
        # a hand-built snapshot claiming an arbitrary identity is refused
        manual = SealedInputSnapshot(
            snapshot_id="f" * 64, case_id="CASE-X", case_version="v1",
            pit_context_id="PITC-X", pit_mode=SEALED_PIT_MODE, as_of="1900-01-01",
            ordered_sources=(SealedSourceSnapshot(
                source_id="SX", source_content_hash="a" * 64, raw_blob_sha256="a" * 64,
                raw_byte_length=1, archive_attestation_id="ATT", archive_admitted_at=ADMITTED,
                raw_bytes=b"x",
            ),),
            source_count=1, input_snapshot_hash="f" * 64,
        )
        with pytest.raises(RequestAuthorityViolation):
            _request(manual)
        # the unmodified authoritative snapshot still builds
        assert _request(good).case_id == good.case_id

    def test_32_success_requires_positive_proof_references(self):
        """A bare ENFORCED/VERIFIED claim is not proof; no SUCCESS without proof."""
        # bare positive claims (no evidence reference) are refused
        with pytest.raises(ResearchResultError):
            _result(closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                    closed_corpus_evidence_ref=None)
        with pytest.raises(ResearchResultError):
            _result(isolation_verification=IsolationVerification.VERIFIED,
                    isolation_evidence_ref=None)
        # SUCCESS with no positive proof fails closed (M6.0 §5 / §11.2 R7)
        with pytest.raises(ResearchResultError):
            _result(closed_corpus_enforcement=ClosedCorpusEnforcement.NOT_VERIFIED,
                    closed_corpus_evidence_ref=None)
        with pytest.raises(ResearchResultError):
            _result(isolation_verification=IsolationVerification.NOT_VERIFIED,
                    isolation_evidence_ref=None)
        # a PROVEN success is accepted and remains non-canonical
        ok = _result()
        assert ok.non_canonical is True
        assert ok.closed_corpus_enforcement is ClosedCorpusEnforcement.ENFORCED
        assert ok.isolation_verification is IsolationVerification.VERIFIED
        assert ok.closed_corpus_evidence_ref and ok.isolation_evidence_ref

    def test_33_prior_evidence_refs_join_the_payload_identity(self):
        snap = _snapshot()
        base = _request(snap)
        a = _request(snap, authorized_prior_evidence_refs=("EV-A",))
        b = _request(snap, authorized_prior_evidence_refs=("EV-B",))
        assert len({base.request_payload_hash, a.request_payload_hash,
                    b.request_payload_hash}) == 3
        # the reference SET is order-insensitive (semantically a set)
        ab = _request(snap, authorized_prior_evidence_refs=("EV-A", "EV-B"))
        ba = _request(snap, authorized_prior_evidence_refs=("EV-B", "EV-A"))
        assert ab.request_payload_hash == ba.request_payload_hash
        assert ab.authorized_prior_evidence_refs == ("EV-A", "EV-B")

    def test_34_direct_result_construction_is_still_validated(self):
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
            )
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
                result_bytes=b"payload", result_sha256="f" * 64,
            )
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status="SUCCESS", provider_surface="p",  # type: ignore[arg-type]
            )
        payload = b"direct"
        ok = DeepResearchResult(
            request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
            status=ResearchResultStatus.SUCCESS, provider_surface="p",
            result_bytes=payload, result_sha256=compute_result_sha256(payload),
            closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
            isolation_verification=IsolationVerification.VERIFIED,
            closed_corpus_evidence_ref="EVID-CORPUS-1",
            isolation_evidence_ref="EVID-ISO-1",
        )
        assert result_matches_hash(ok) is True

    def test_35_direct_request_construction_is_still_validated(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, request_payload_hash="0" * 64)
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, capability="S9")
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, request_isolation_required=False)
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(
                req, corpus=dataclasses.replace(req.corpus, closed_corpus_required=False)
            )
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, case_id="")
        # a consistent direct construction is accepted
        assert dataclasses.replace(req).request_payload_hash == req.request_payload_hash
        # the public descriptor type is present and honest
        assert isinstance(req.corpus, SourceCorpusDescriptor)
        assert isinstance(req, DeepResearchRequest)

    def test_36_snapshot_byte_integrity_is_verified(self):
        """Captured bytes must match the declared blob hash and length."""
        good = _snapshot()
        first, second = good.ordered_sources
        # bytes swapped while the recorded hash/length stay the original ones
        tampered_bytes = dataclasses.replace(
            good, ordered_sources=(dataclasses.replace(first, raw_bytes=b"TAMPERED"), second)
        )
        with pytest.raises(RequestAuthorityViolation):
            _request(tampered_bytes)
        # declared length altered while the bytes/hash are the originals
        tampered_len = dataclasses.replace(
            good,
            ordered_sources=(dataclasses.replace(first, raw_byte_length=first.raw_byte_length + 1),
                             second),
        )
        with pytest.raises(RequestAuthorityViolation):
            _request(tampered_len)
        # declared hash altered
        tampered_hash = dataclasses.replace(
            good,
            ordered_sources=(dataclasses.replace(first, raw_blob_sha256="a" * 64), second),
        )
        with pytest.raises(RequestAuthorityViolation):
            _request(tampered_hash)
        # the untouched authoritative snapshot still builds
        assert _request(good).source_ids == ("S1", "S2")

    def test_37_direct_request_requires_consistent_snapshot_identity(self):
        req = _request(_snapshot())
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, snapshot_id="f" * 64)
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, input_snapshot_hash="f" * 64)

    def test_38_duplicate_prior_evidence_refs_rejected(self):
        snap = _snapshot()
        with pytest.raises(ResearchRequestError):
            _request(snap, authorized_prior_evidence_refs=("EV-A", "EV-A"))
        # direct construction cannot smuggle duplicates past the gate either
        req = _request(snap, authorized_prior_evidence_refs=("EV-A", "EV-B"))
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, authorized_prior_evidence_refs=("EV-A", "EV-A"))

    def test_39_whitespace_only_result_cannot_be_success(self):
        blank = b" \n\t  "
        with pytest.raises(ResearchResultError):
            _result(result_bytes=blank, result_sha256=compute_result_sha256(blank))
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
                result_bytes=blank, result_sha256=compute_result_sha256(blank),
            )
        # a real payload that merely contains whitespace still succeeds
        ok = _result()
        assert ok.is_success is True

    def test_40_prior_evidence_refs_are_immutable_after_construction(self):
        req = _request(_snapshot(), authorized_prior_evidence_refs=["EV-A", "EV-B"])
        assert isinstance(req.authorized_prior_evidence_refs, tuple)
        assert req.authorized_prior_evidence_refs == ("EV-A", "EV-B")
        with pytest.raises(AttributeError):
            req.authorized_prior_evidence_refs.append("EV-A")  # type: ignore[attr-defined]
        # identical to supplying a tuple: the hash is stable and list-order-insensitive
        as_tuple = _request(_snapshot(), authorized_prior_evidence_refs=("EV-A", "EV-B"))
        assert req.request_payload_hash == as_tuple.request_payload_hash

    def test_41_source_pointers_are_immutable_after_construction(self):
        ok = _result(source_pointers=[SourcePointer(index=1, reference="https://a/1")])
        assert isinstance(ok.source_pointers, tuple)
        with pytest.raises(AttributeError):
            ok.source_pointers.append(SourcePointer(index=2, reference="https://b/2"))  # type: ignore[attr-defined]

    def test_42_unicode_whitespace_only_result_cannot_be_success(self):
        blank_variants = [
            b"\xc2\xa0\xe2\x80\x83\xe3\x80\x80",   # NBSP + em space + ideographic space
            b"\xef\xbb\xbf",                        # BOM only
            b"\xe2\x80\x8b",                        # zero-width space
            b" \xc2\xa0\n",
        ]
        for blank in blank_variants:
            with pytest.raises(ResearchResultError):
                _result(result_bytes=blank, result_sha256=compute_result_sha256(blank))
            with pytest.raises(ResearchResultError):
                DeepResearchResult(
                    request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                    status=ResearchResultStatus.SUCCESS, provider_surface="p",
                    result_bytes=blank, result_sha256=compute_result_sha256(blank),
                )
        # real text containing Unicode whitespace still succeeds
        real = "ผลการวิจัย gold \u00a0 outlook".encode("utf-8")
        ok = _result(result_bytes=real, result_sha256=compute_result_sha256(real))
        assert ok.is_success is True
        # non-UTF-8 bytes are real (binary) payload, not blank text
        binary = b"\x00\x01\xff\xfe\x80"
        ok_bin = _result(result_bytes=binary, result_sha256=compute_result_sha256(binary))
        assert ok_bin.is_success is True

    def test_43_interleaved_blank_characters_cannot_be_success(self):
        blank_variants = [
            "\u200b \u200c".encode("utf-8"),
            " \u200b\n\ufeff".encode("utf-8"),
            "\u3000\u200b\u3000".encode("utf-8"),
            "\ufeff\u2060".encode("utf-8"),
        ]
        for blank in blank_variants:
            with pytest.raises(ResearchResultError):
                _result(result_bytes=blank, result_sha256=compute_result_sha256(blank))
            with pytest.raises(ResearchResultError):
                DeepResearchResult(
                    request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                    status=ResearchResultStatus.SUCCESS, provider_surface="p",
                    result_bytes=blank, result_sha256=compute_result_sha256(blank),
                )
        # any visible character makes it real content
        real = "\u200b x".encode("utf-8")
        assert _result(result_bytes=real,
                       result_sha256=compute_result_sha256(real)).is_success is True

    def test_44_provider_metadata_is_immutable_after_construction(self):
        caller_dict = {"model_reported": "gemini-x"}
        r = _result(provider_reported_metadata=caller_dict)
        with pytest.raises(TypeError):
            r.provider_reported_metadata["model_reported"] = "tampered"  # type: ignore[index]
        # mutating the caller's original mapping does not affect the result
        caller_dict["model_reported"] = "tampered"
        assert r.provider_reported_metadata["model_reported"] == "gemini-x"
        assert r.provider_reported_metadata == {"model_reported": "gemini-x"}
        # a result built without metadata normalizes to an immutable empty mapping
        empty = _result().provider_reported_metadata
        assert dict(empty) == {}
        with pytest.raises(TypeError):
            empty["x"] = "y"  # type: ignore[index]

    def test_45_request_authority_cannot_be_bypassed_by_direct_construction(self):
        import qad.m6.research_contract as rc

        req = _request(_snapshot())
        # a request with no bound snapshot is refused outright
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, authority_snapshot=None)
        # changing an authority field is refused …
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, case_id="UNAUTHORIZED-CASE", as_of="1900-01-01")
        # … even when the caller also recomputes a matching payload hash
        forged = rc._RequestPayloadIdentity(
            research_question=req.research_question,
            case_id="UNAUTHORIZED-CASE",
            case_version=req.case_version,
            evidence_gap_id=req.evidence_gap_id,
            input_snapshot_hash=req.input_snapshot_hash,
            pit_mode=req.pit_mode,
            as_of="1900-01-01",
            capability=req.capability,
            closed_corpus_required=True,
            request_isolation_required=True,
            authorized_prior_evidence_refs=[],
        )
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(
                req, case_id="UNAUTHORIZED-CASE", as_of="1900-01-01",
                request_payload_hash=rc._deterministic_hash(forged),
            )
        # the corpus cannot be swapped either
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(
                req, corpus=dataclasses.replace(
                    req.corpus, exact_blob_hashes=(("S9", "a" * 64),)
                )
            )
        # the unmodified request remains valid
        assert req.authority_snapshot is not None

    def test_46_provider_metadata_values_must_be_strings(self):
        with pytest.raises(ResearchResultError):
            _result(provider_reported_metadata={"model": ["m1"]})  # type: ignore[dict-item]
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
                result_bytes=b"content", result_sha256=compute_result_sha256(b"content"),
                provider_reported_metadata={"model": {"nested": "x"}},  # type: ignore[dict-item]
            )
        with pytest.raises(ResearchResultError):
            _result(provider_reported_metadata={1: "x"})  # type: ignore[dict-item]
        ok = _result(provider_reported_metadata={"model": "gemini-x", "tokens": "NOT_EXPOSED"})
        assert dict(ok.provider_reported_metadata) == {
            "model": "gemini-x", "tokens": "NOT_EXPOSED",
        }

    def test_47_invisible_only_output_beyond_the_enumerated_set(self):
        """Every invisible category is blank — not just enumerated characters."""
        blank_variants = [
            "\u200e".encode("utf-8"),          # LEFT-TO-RIGHT MARK (Cf)
            "\u200f\u200e".encode("utf-8"),    # RLM + LRM
            "\u061c".encode("utf-8"),          # ARABIC LETTER MARK (Cf)
            "\u2066\u2069".encode("utf-8"),    # isolate controls (Cf)
            "\x00\x01\x1f".encode("utf-8"),    # ASCII controls (Cc)
            "\u200e \u00a0\u3000".encode("utf-8"),
        ]
        for blank in blank_variants:
            with pytest.raises(ResearchResultError):
                _result(result_bytes=blank, result_sha256=compute_result_sha256(blank))
        # a single visible character makes it real content
        real = "\u200eA".encode("utf-8")
        assert _result(result_bytes=real,
                       result_sha256=compute_result_sha256(real)).is_success is True

    def test_48_result_hash_binds_the_citation_list(self):
        from qad.m6.research_contract import compute_citation_list_sha256

        ptrs_a = (SourcePointer(index=1, reference="https://a/1"),)
        ptrs_b = (SourcePointer(index=1, reference="https://a/1"),
                  SourcePointer(index=2, reference="https://b/2"))
        # deterministic + pointer-sensitive
        assert compute_citation_list_sha256(ptrs_a) == compute_citation_list_sha256(ptrs_a)
        assert compute_citation_list_sha256(ptrs_a) != compute_citation_list_sha256(ptrs_b)
        # the same report bytes with different citations yield a different companion digest
        a = _result(source_pointers=ptrs_a)
        b = _result(source_pointers=ptrs_b)
        assert a.result_sha256 == b.result_sha256            # exact report bytes unchanged
        assert a.citation_list_sha256 != b.citation_list_sha256
        assert a.citation_list_sha256 == compute_citation_list_sha256(ptrs_a)
        # a caller-supplied digest that disagrees is rejected
        with pytest.raises(ResearchResultError):
            _result(citation_list_sha256="f" * 64)

    def test_49_success_requires_proof_on_direct_construction_too(self):
        payload = b"content"
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
                result_bytes=payload, result_sha256=compute_result_sha256(payload),
            )
        with pytest.raises(ResearchResultError):
            DeepResearchResult(
                request_id="REQ-1", research_run_id="RR-1", ledger_id="L-1",
                status=ResearchResultStatus.SUCCESS, provider_surface="p",
                result_bytes=payload, result_sha256=compute_result_sha256(payload),
                closed_corpus_enforcement=ClosedCorpusEnforcement.ENFORCED,
                isolation_verification=IsolationVerification.VERIFIED,
                closed_corpus_evidence_ref="EVID-C",  # isolation evidence missing
            )

    def test_50_snapshot_closed_corpus_flag_cannot_be_bypassed(self):
        """A snapshot that does not require a closed corpus is not authoritative."""
        snap = _snapshot()
        req = _request(snap)
        tampered = dataclasses.replace(snap, closed_corpus_required=False)
        # the builder refuses the tampered snapshot …
        with pytest.raises(RequestAuthorityViolation):
            _request(tampered)
        # … and it cannot be attached to a request by direct construction
        with pytest.raises(RequestAuthorityViolation):
            dataclasses.replace(req, authority_snapshot=tampered)
        # the untouched snapshot is still accepted
        assert _request(_snapshot()).closed_corpus_required is True

    def test_51_invisible_only_contract_text_fields_are_rejected(self):
        invisible = "\u200e"                      # LRM
        invisible_pair = "\u2066\u2069"           # isolate controls
        # evidence references must carry visible content
        with pytest.raises(ResearchResultError):
            _result(isolation_evidence_ref=invisible)
        with pytest.raises(ResearchResultError):
            _result(closed_corpus_evidence_ref=invisible_pair)
        # a failure_detail must be a real, readable statement
        with pytest.raises(ResearchResultError):
            _result(status=ResearchResultStatus.RESEARCH_UNAVAILABLE,
                    result_bytes=None, result_sha256=None, failure_detail=f" {invisible} ")
        # a source pointer must reference something readable, not just spaces/controls
        with pytest.raises(ResearchResultError):
            _result(source_pointers=(SourcePointer(index=1, reference=invisible),))
        # request text fields obey the same rule (builder + direct construction)
        with pytest.raises(ResearchRequestError):
            _request(_snapshot(), research_question=invisible)
        req = _request(_snapshot())
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, evidence_gap_id=invisible)

    def test_52_blank_glyphs_cannot_be_success(self):
        """Render-blank glyphs outside the invisible categories are blank too."""
        blank_variants = [
            "\u2800".encode("utf-8"),                 # BRAILLE PATTERN BLANK
            "\u3164\u3164".encode("utf-8"),           # HANGUL FILLER
            "\uffa0".encode("utf-8"),                 # HALFWIDTH HANGUL FILLER
            "\ufe0f\ufe0e".encode("utf-8"),           # variation selectors
            "\u115f\u1160".encode("utf-8"),           # hangul jamo fillers
            "\u2800 \u3164".encode("utf-8"),
        ]
        for blank in blank_variants:
            with pytest.raises(ResearchResultError):
                _result(result_bytes=blank, result_sha256=compute_result_sha256(blank))
        # a genuinely visible character is still real content
        real = "\u2800\u0041".encode("utf-8")         # blank glyph + 'A'
        assert _result(result_bytes=real,
                       result_sha256=compute_result_sha256(real)).is_success is True
        # and blank glyphs cannot stand in for contract text fields
        with pytest.raises(ResearchResultError):
            SourcePointer(index=1, reference="\u2800")
        with pytest.raises(ResearchRequestError):
            _request(_snapshot(), research_question="\u3164")

    def test_53_provider_configuration_validated_on_direct_construction(self):
        from qad.m6.research_contract import ProviderConfiguration

        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="\u2800")      # invisible-only
        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="p", capability="S9")
        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="p", closed_corpus_required=False)
        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="p", request_isolation_required=False)
        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="p", timeout_seconds=0)
        with pytest.raises(ResearchRequestError):
            ProviderConfiguration(provider_surface="p", timeout_seconds=True)
        ok = ProviderConfiguration(provider_surface="p", timeout_seconds=30)
        assert ok.timeout_seconds == 30
        # a request cannot smuggle an invalid capability either
        req = _request(_snapshot())
        with pytest.raises(ResearchRequestError):
            dataclasses.replace(req, capability="S9")
        with pytest.raises(ResearchResultError):
            SourcePointer(index=-1, reference="https://a/1")
        with pytest.raises(ResearchResultError):
            SourcePointer(index=1, reference="\u3164")

    def test_54_orphan_combining_marks_are_blank(self):
        """A mark with no preceding base character has no visible content."""
        orphans = [
            "\u180b".encode("utf-8"),          # MONGOLIAN FREE VARIATION SELECTOR ONE
            "\u180c\u180d".encode("utf-8"),    # … TWO + THREE
            "\u180f".encode("utf-8"),          # … FOUR
            "\u0301".encode("utf-8"),          # COMBINING ACUTE ACCENT
            "\u20dd".encode("utf-8"),          # COMBINING ENCLOSING CIRCLE
            "\u180b \u180c".encode("utf-8"),
        ]
        for orphan in orphans:
            with pytest.raises(ResearchResultError):
                _result(result_bytes=orphan, result_sha256=compute_result_sha256(orphan))
        # … but a mark attached to a base character is real visible content
        attached = "A\u0301".encode("utf-8")
        assert _result(result_bytes=attached,
                       result_sha256=compute_result_sha256(attached)).is_success is True
        # and an orphan mark cannot stand in for contract text fields
        with pytest.raises(ResearchResultError):
            SourcePointer(index=1, reference="\u180b")
        with pytest.raises(ResearchRequestError):
            _request(_snapshot(), research_question="\u180b\u180c")
        with pytest.raises(ResearchRequestError):
            from qad.m6.research_contract import ProviderConfiguration
            ProviderConfiguration(provider_surface="\u180b")

    def test_55_surrogates_are_never_valid_text(self):
        """A Cs surrogate codepoint is not text — alone or embedded."""
        lone = "\ud800"
        embedded = "valid text \udfff more"
        with pytest.raises(ResearchResultError):
            SourcePointer(index=1, reference=lone)
        with pytest.raises(ResearchResultError):
            SourcePointer(index=1, reference=embedded)     # visible chars + surrogate
        with pytest.raises(ResearchRequestError):
            _request(_snapshot(), research_question=lone)
        with pytest.raises(ResearchRequestError):
            _request(_snapshot(), research_question=embedded)
        with pytest.raises(ResearchRequestError):
            from qad.m6.research_contract import ProviderConfiguration
            ProviderConfiguration(provider_surface=lone)
        with pytest.raises(ResearchResultError):
            _result(provider_surface=embedded)
        # a non-UTF-8 BINARY result payload is still accepted as real bytes
        binary = b"\xff\xfe\x00\x01"
        ok = _result(result_bytes=binary, result_sha256=compute_result_sha256(binary))
        assert ok.is_success is True

    def test_56_snapshot_source_content_hash_must_match_blob_hash(self):
        """M6.2 rules F/H: content_hash and raw_blob_sha256 are one authority."""
        snap = _snapshot()
        src = snap.ordered_sources[0]
        tampered_src = dataclasses.replace(src, source_content_hash="0" * 64)
        tampered = dataclasses.replace(
            snap, ordered_sources=(tampered_src,) + tuple(snap.ordered_sources[1:])
        )
        with pytest.raises(RequestAuthorityViolation):
            _request(tampered)
        # the untouched snapshot is still accepted
        assert _request(_snapshot()).case_id == snap.case_id

    def test_57_snapshot_structural_invariants_are_reenforced(self):
        """M6.2 build rules: count, order, uniqueness, eligibility, admitted<=AS_OF."""
        snap = _snapshot()
        src0 = snap.ordered_sources[0]
        # source_count must match the ordered sources
        with pytest.raises(RequestAuthorityViolation):
            _request(dataclasses.replace(snap, source_count=19))
        # a non-ELIGIBLE source is not authoritative input
        with pytest.raises(RequestAuthorityViolation):
            _request(dataclasses.replace(
                snap,
                ordered_sources=(dataclasses.replace(
                    src0, eligibility_verdict="REJECTED"),) + tuple(snap.ordered_sources[1:]),
            ))
        # admission after AS_OF violates PIT (AS_OF is 2026-01-01 here)
        with pytest.raises(RequestAuthorityViolation):
            _request(dataclasses.replace(
                snap,
                ordered_sources=(dataclasses.replace(
                    src0, archive_admitted_at="2099-01-01T00:00:00+00:00"),)
                + tuple(snap.ordered_sources[1:]),
            ))
        # non-ISO admission timestamp fails closed
        with pytest.raises(RequestAuthorityViolation):
            _request(dataclasses.replace(
                snap,
                ordered_sources=(dataclasses.replace(
                    src0, archive_admitted_at="not-a-timestamp"),)
                + tuple(snap.ordered_sources[1:]),
            ))
        # duplicate source ids cannot be smuggled in (fails closed; the identity
        # recomputation catches it as well as the explicit uniqueness check)
        with pytest.raises(RequestAuthorityViolation):
            _request(dataclasses.replace(
                snap, ordered_sources=(src0, src0), source_count=2,
            ))
        # the untouched snapshot is still accepted
        assert _request(snap).input_snapshot_hash == snap.input_snapshot_hash
