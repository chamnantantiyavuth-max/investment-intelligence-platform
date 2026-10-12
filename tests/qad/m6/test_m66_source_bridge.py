"""M6.6 — Noncanonical Source Discovery + Admission Bridge (FD #151).

Deterministic, provider-neutral tests. NO network, NO Gemini, NO Notebook, NO
browser/CDP, NO provider execution. Test-only deterministic verifiers and
archived/fixture bytes only.
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import pathlib

import pytest

from qad.m6.ledger import (
    DeepResearchRunLedgerStore,
    LedgerIdentityConflict,
    LedgerTerminalError,
    LedgerValidationError,
    TerminalStatus,
)
from qad.m6.research_contract import SourcePointer
from qad.m6.source_bridge import (
    DEFAULT_ORIGINAL_SOURCE_VERIFIER,
    CandidateIdentityConflict,
    CanonicalPairState,
    DiscoveredSourceReference,
    EvidenceAdmissionClassification,
    EvidenceAdmissionDecision,
    OriginalSourceVerification,
    SourceBridgeError,
    SourceEvidenceConflict,
    SourceEvidenceIncomplete,
    SourceFailureKind,
    SourceVerificationCandidate,
    admit_candidate_evidence,
    attempt_canonical_evidence_admission,
    build_evidence_admission,
    classify_evidence_admission_failure,
    coerce_discovered_reference,
    compute_source_candidate_id,
    construct_candidate_evidence,
    dispose_settled_candidate,
    pending_candidates,
    process_discovered_sources,
    reconcile_canonical_evidence_pair,
    register_discovered_candidates,
    verify_and_admit_source,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.persistence.errors import (
    CanonicalBoundaryViolation,
    IntegrityConflict,
    MissingForeignKey,
    PITBlockError,
    TransactionFailure,
)
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryRawSourceArchive,
)
from qad.persistence.serialization import compute_canonical_hash

AS_OF = "2026-01-01"
ADMITTED_BEFORE = "2025-12-01T00:00:00+00:00"   # <= AS_OF  -> SEALED-eligible
ADMITTED_AFTER = "2026-02-01T00:00:00+00:00"    # >  AS_OF  -> NOT eligible
DISCOVERED_AT = "2026-10-09T10:00:00+00:00"
LIVE = "LIVE_CASE_UPDATE"
SEALED = "SEALED_HISTORICAL_EVALUATION"
REPLAY_EXCEPTION = "REPLAY_EXCEPTION"

BRIDGE_PATH = pathlib.Path(__file__).resolve().parents[3] / "qad" / "m6" / "source_bridge.py"


# ----------------------------------------------------------------- fixtures


@pytest.fixture()
def store(tmp_path):
    return DeepResearchRunLedgerStore(tmp_path / "m66.sqlite3")


def _make_run(
    store,
    *,
    ledger_id="L-1",
    pit_mode=LIVE,
    as_of=AS_OF,
    provider_surface="gemini_notebook",
    run_id="RR-1",
    request_id="REQ-1",
):
    store.create_run(
        ledger_id=ledger_id,
        research_run_id=run_id,
        rrm_manifest_id="RRM-2026-0001",
        case_id="CASE-1",
        case_version="v1",
        evidence_gap_id="EG-1",
        request_id=request_id,
        idempotency_key=f"idem-{ledger_id}",
        notebook_identity="nb-1",
        pit_context_id="PITC-1",
        pit_mode=pit_mode,
        as_of=as_of,
        input_snapshot_hash="b" * 64,
        provider_surface=provider_surface,
        transport_type="BROWSER_UI_AUTOMATION",
    )
    return ledger_id


def _archive(admitted=ADMITTED_BEFORE):
    return InMemoryRawSourceArchive(clock=lambda: dt.datetime.fromisoformat(admitted))


def _registry(archive):
    return InMemoryEvidenceRegistry(source_archive=archive)


def _ptr(index, reference, **kw):
    return DiscoveredSourceReference(index=index, reference=reference, **kw)


def _verified(source_id, raw=b"alpha", tier="L1", source_type="SEC_FILING", **kw):
    """An UNTRUSTED verifier-returned CANDIDATE for a verified original document."""
    return SourceVerificationCandidate(
        verified=True,
        reason="INDEPENDENTLY_VERIFIED",
        source_id=source_id,
        source_tier=tier,
        source_type=source_type,
        content_hash=hashlib.sha256(raw).hexdigest(),
        raw_bytes=raw,
        location=f"https://sec.gov/{source_id}",
        retrieval_date="2025-11-01",
        publication_date="2025-10-01",
        title="Original Document",
        **kw,
    )


def _failed(kind, reason="NOT_VERIFIED"):
    return SourceVerificationCandidate(
        verified=False, reason=reason, failure_kind=kind
    )


class _StubVerifier:
    """DETERMINISTIC TEST-ONLY verifier. NOT a production verifier."""

    def __init__(self, results):
        self._results = dict(results)

    def verify(self, request, /):
        return self._results.get(
            request.source_candidate_id,
            _failed(SourceFailureKind.INSUFFICIENT_PROOF, "NO_FIXTURE_FOR_CANDIDATE"),
        )


def _cid(ledger_id, index, reference):
    return compute_source_candidate_id(
        ledger_id=ledger_id, pointer_index=index, reference=reference
    )


def _dispositions(store, ledger_id):
    return {d.source_candidate_id: d for d in store.load_run(ledger_id).dispositions}


def _ev(evidence_id, source_id, *, evidence_type=EvidenceRecordEvidence_type.CLAIM,
        status=EvidenceRecordValidation_status.RAW, contradicts=None):
    return EvidenceRecord(
        admitting_role="Research Director",
        as_of=AS_OF,
        content="Verified extract from the original document.",
        evidence_id=evidence_id,
        evidence_type=evidence_type,
        extractor="M6.6 bridge fixture",
        source_id=source_id,
        source_tier="L1",
        validation_status=status,
        contradicts_ids=contradicts,
    )


def _ear(evidence_id, admission_id, admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
         osv=None):
    from qad.models.family_b import EvidenceAdmissionRecord

    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        admission_method=admission_method,
        admission_timestamp=DISCOVERED_AT,
        admitting_role="Research Director",
        evidence_id=evidence_id,
        source_tier_check="L1",
        validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
        original_source_verified=osv,
    )


def _admit_direct_source(archive, source_id, raw=b"seeded", retrieval_date="2025-11-01"):
    """Seed an already-admitted SRC-01 through the AUTHORITATIVE boundary only."""
    archive.admit_source(
        SourceRecord(
            source_id=source_id,
            content_hash=hashlib.sha256(raw).hexdigest(),
            retrieval_date=retrieval_date,
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier=f"https://sec.gov/{source_id}",
        ),
        raw,
    )


def _evidence_builder(*, ledger_id="L-1", evidence_id="EV-A", admission_id="EAR-A",
                      method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
                      evidence_type=EvidenceRecordEvidence_type.CLAIM,
                      contradicts=None, raises=None):
    """The DOCUMENTED 3-argument builder signature: (candidate_id, src01_id, verification)."""

    def _build(candidate_id, src01_id, verification):
        if raises is not None:
            raise raises
        ev = _ev(evidence_id, src01_id, evidence_type=evidence_type, contradicts=contradicts)
        ear = build_evidence_admission(
            evidence=ev, verification=verification, admission_id=admission_id,
            ledger_id=ledger_id, source_candidate_id=candidate_id,
            admission_timestamp=DISCOVERED_AT, admitting_role="Research Director",
            admission_method=method,
            validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
        )
        return ev, ear

    return _build


def _per_candidate_builder(mapping, *, ledger_id="L-1"):
    def _build(candidate_id, src01_id, verification):
        spec = mapping[candidate_id]
        ev = _ev(spec["ev"], src01_id, contradicts=spec.get("contradicts"))
        ear = build_evidence_admission(
            evidence=ev, verification=verification, admission_id=spec["ear"],
            ledger_id=ledger_id, source_candidate_id=candidate_id,
            admission_timestamp=DISCOVERED_AT, admitting_role="Research Director",
            admission_method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
            validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
        )
        return ev, ear

    return _build


# ============================================================ 1-4 identity


def test_01_a_citation_is_noncanonical_discovery_only(store):
    archive, registry = _archive(), _registry(_archive())
    _make_run(store)
    refs = [SourcePointer(index=0, reference="https://sec.gov/a", title="A")]
    registered = register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    assert len(registered) == 1
    # discovery registered NOTHING canonical
    assert registry._data.get("EV-01", {}) == {}
    assert [c.source_candidate_id for c in store.load_run("L-1").candidates] == [
        registered[0].source_candidate_id
    ]
    assert coerce_discovered_reference(SourcePointer(index=3, reference="x")).index == 3


def test_02_every_discovered_candidate_is_registered_durably(store):
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a"), _ptr(1, "https://sec.gov/b"), _ptr(2, "https://sec.gov/c")]
    registered = register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    assert len(registered) == 3
    rec = store.load_run("L-1")
    assert len(rec.candidates) == 3
    assert all(c.original_source_verification_status == "PENDING" for c in rec.candidates)
    assert all(c.pit_eligibility == "UNKNOWN" for c in rec.candidates)


def test_03_candidate_identity_is_stable_on_replay(store):
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a"), _ptr(1, "https://sec.gov/b")]
    first = register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    second = register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp="2026-10-10T10:00:00+00:00"
    )
    assert [r.source_candidate_id for r in first] == [r.source_candidate_id for r in second]
    assert all(r.already_registered for r in second)
    assert len(store.load_run("L-1").candidates) == 2  # no silent duplicate


def test_04_duplicate_candidate_registration_cannot_silently_overwrite(store):
    _make_run(store)
    reference = "https://sec.gov/a"
    candidate_id = _cid("L-1", 0, reference)
    # pre-seed the SAME deterministic id for a DIFFERENT reference (corruption/replay)
    store.register_candidate(
        "L-1",
        source_candidate_id=candidate_id,
        url_or_identifier="https://evil.example/other",
        discovery_timestamp=DISCOVERED_AT,
        original_source_verification_status="PENDING",
        pit_eligibility="UNKNOWN",
    )
    with pytest.raises(CandidateIdentityConflict):
        register_discovered_candidates(
            store, ledger_id="L-1", references=[_ptr(0, reference)],
            discovery_timestamp=DISCOVERED_AT,
        )
    assert len(store.load_run("L-1").candidates) == 1


# ================================================= 5-8 verification boundary


def test_05_a_source_pointer_cannot_declare_itself_verified(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a", provider_claim_original_source_verified="true")]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    # no verifier configured -> default DENY (the provider's claim is not authority)
    out = verify_and_admit_source(store, ledger_id="L-1", source_candidate_id=cid, archive=archive)
    assert out.disposition.value == "DEFERRED"
    assert out.admitted is False
    assert not archive.contains("SRC-01", "https://sec.gov/a")
    assert isinstance(DEFAULT_ORIGINAL_SOURCE_VERIFIER, object)


def test_06_unverifiable_original_source_cannot_become_canonical_evidence(store):
    archive = _archive()
    _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _failed(SourceFailureKind.NOT_FOUND)})
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "UNAVAILABLE"
    assert not archive.contains("SRC-01", "https://sec.gov/a")


def test_07_source_byte_mismatch_is_rejected(store):
    # a TRUSTED verdict cannot be constructed directly at all (FD #152 principle)
    with pytest.raises(SourceBridgeError):
        OriginalSourceVerification(verified=True, reason="x")
    with pytest.raises(SourceBridgeError):
        OriginalSourceVerification(verified=False, reason="x")
    # a candidate whose content_hash != sha256(raw_bytes) cannot even be formed
    with pytest.raises(SourceBridgeError):
        SourceVerificationCandidate(
            verified=True, reason="x", source_id="S", source_tier="L1",
            source_type="SEC_FILING", content_hash="0" * 64, raw_bytes=b"alpha",
            retrieval_date="2025-11-01",
        )
    archive = _archive()
    _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _failed(SourceFailureKind.MISMATCH)})
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "REJECTED"
    assert not archive.contains("SRC-01", "https://sec.gov/a")


def test_08_source_tier_mismatch_is_rejected(store):
    archive = _archive()
    _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _verified("SRC-A", tier="NOT_A_TIER")})
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "REJECTED"
    assert not archive.contains("SRC-01", "SRC-A")


# ================================================= 9-12 canonical admission


def test_09_valid_source_is_admitted_via_raw_source_archive(store):
    archive = _archive()
    _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _verified("SRC-A")})
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "IMPORTED" and out.admitted is True
    assert archive.contains("SRC-01", "SRC-A")
    assert archive.verify_admission_attestation("SRC-A") is True
    assert archive.get_admission_attestation("SRC-A").attestation_id


def test_10_direct_src01_bypass_is_rejected(store):
    archive = _archive()
    with pytest.raises(CanonicalBoundaryViolation):
        archive.store(
            SourceRecord(
                source_id="SRC-X", content_hash="a" * 64, retrieval_date="2025-11-01",
                source_tier=SourceRecordSource_tier.L1,
                source_type=SourceRecordSource_type.SEC_FILING,
                url_or_identifier="https://sec.gov/x",
            )
        )


def test_11_same_source_reprocessing_is_idempotent(store):
    archive = _archive()
    _make_run(store, ledger_id="L-1", run_id="RR-1", request_id="REQ-1")
    _make_run(store, ledger_id="L-2", run_id="RR-2", request_id="REQ-2")
    for lid in ("L-1", "L-2"):
        register_discovered_candidates(
            store, ledger_id=lid, references=[_ptr(0, "https://sec.gov/a")],
            discovery_timestamp=DISCOVERED_AT,
        )
        cid = _cid(lid, 0, "https://sec.gov/a")
        out = verify_and_admit_source(
            store, ledger_id=lid, source_candidate_id=cid,
            verifier=_StubVerifier({cid: _verified("SRC-A")}), archive=archive,
        )
        assert out.disposition.value == "IMPORTED"
    # ONE canonical object; the second run REUSED it
    assert len(archive._data["SRC-01"]) == 1


def test_12_conflicting_source_identity_is_rejected(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A", raw=b"original-bytes")
    store_run = _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    # same source_id, DIFFERENT bytes -> an identity conflict, never a silent reuse
    # and never an overwrite of immutable canonical bytes
    verifier = _StubVerifier({cid: _verified("SRC-A", raw=b"conflicting-bytes")})
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "REJECTED"
    assert out.reason == "SOURCE_IDENTITY_CONFLICT"
    assert archive.load_raw_blob("SRC-A") == b"original-bytes"
    assert store_run == "L-1"


# ================================================== 13-16 evidence admission


def test_13_valid_ev01_ear01_uses_the_existing_gate(store):
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    out = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
        registry=registry, evidence_builder=_evidence_builder(),
    )
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == ("EV-A",) and o.ear_ids == ("EAR-A",)
    assert o.evidence_admission_error is None   # the documented 3-arg builder ran
    assert registry.load("EV-01", "EV-A").evidence_id == "EV-A"
    assert "EAR-A" in registry._data["EAR-01"]


def test_14_ai_extraction_without_actual_verification_is_rejected(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A")
    registry = _registry(archive)
    ev = _ev("EV-A", "SRC-A")
    # an UNTRUSTED candidate (or any non-minted object) can never mint "true"
    ear = build_evidence_admission(
        evidence=ev, verification=_verified("SRC-A"), admission_id="EAR-A",
        ledger_id="L-1", source_candidate_id="SC-x",
        admission_timestamp=DISCOVERED_AT, admitting_role="Research Director",
        admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION,
        validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
    )
    assert ear.original_source_verified is None  # never synthesized
    with pytest.raises(IntegrityConflict):
        registry.admit_evidence(ev, ear)
    assert registry._data.get("EV-01", {}) == {}

    # and a caller-CONSTRUCTED verification object cannot even be passed as a verdict
    class _Forged:
        verified = True
        mismatches = ()
        source_id = "SRC-A"

    ear2 = build_evidence_admission(
        evidence=ev, verification=_Forged(), admission_id="EAR-A2",
        ledger_id="L-1", source_candidate_id="SC-x",
        admission_timestamp=DISCOVERED_AT, admitting_role="Research Director",
        admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION,
        validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
    )
    assert ear2.original_source_verified is None
    with pytest.raises(IntegrityConflict):
        registry.admit_evidence(ev, ear2)


def test_15_direct_ev01_ear01_bypass_is_rejected(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A")
    registry = _registry(archive)
    with pytest.raises(CanonicalBoundaryViolation):
        registry.store(_ev("EV-DIRECT", "SRC-A"))


def test_16_raw_evidence_is_not_auto_promoted_to_validated(store):
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
        registry=registry, evidence_builder=_evidence_builder(),  # EV built as RAW
    )
    assert registry.load("EV-01", "EV-A").validation_status is EvidenceRecordValidation_status.RAW


# ============================================================= 17-19 PIT


def test_17_sealed_post_as_of_source_cannot_be_injected(store):
    archive = _archive()  # nothing admitted yet
    _make_run(store, pit_mode=SEALED, as_of=AS_OF)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/new")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/new")
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid,
        verifier=_StubVerifier({cid: _verified("SRC-NEW")}), archive=archive,
    )
    assert out.disposition.value == "DEFERRED"
    assert out.reason == "NOT_ELIGIBLE_FOR_SEALED_PIT"
    assert not archive.contains("SRC-01", "SRC-NEW")  # SEALED corpus not expanded


def test_18_backdated_publication_metadata_cannot_bypass_attestation(store):
    # admitted AFTER as_of, but with backdated publication/retrieval metadata
    archive = _archive(admitted=ADMITTED_AFTER)
    _admit_direct_source(archive, "SRC-OLD", retrieval_date="2025-01-01")
    _make_run(store, pit_mode=SEALED, as_of=AS_OF)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/old")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/old")
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid,
        verifier=_StubVerifier({cid: _verified("SRC-OLD", raw=b"seeded")}), archive=archive,
    )
    assert out.disposition.value == "UNAVAILABLE"
    assert out.reason == "NOT_ELIGIBLE_FOR_SEALED_PIT"


def test_19_live_and_replay_exception_retain_existing_authority_rules(store):
    # LIVE: selective admission is allowed
    archive = _archive()
    _make_run(store, ledger_id="L-1", pit_mode=LIVE, run_id="RR-1", request_id="REQ-1")
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/live")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/live")
    live_out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid,
        verifier=_StubVerifier({cid: _verified("SRC-LIVE")}), archive=archive,
    )
    assert live_out.disposition.value == "IMPORTED"

    # REPLAY_EXCEPTION: the existing explicit authorization boundary is required
    _make_run(store, ledger_id="L-2", pit_mode=REPLAY_EXCEPTION, run_id="RR-2", request_id="REQ-2")
    register_discovered_candidates(
        store, ledger_id="L-2", references=[_ptr(0, "https://sec.gov/replay")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid2 = _cid("L-2", 0, "https://sec.gov/replay")
    replay_out = verify_and_admit_source(
        store, ledger_id="L-2", source_candidate_id=cid2,
        verifier=_StubVerifier({cid2: _verified("SRC-REPLAY")}), archive=archive,
    )
    assert replay_out.disposition.value == "DEFERRED"
    assert replay_out.reason == "REPLAY_EXCEPTION_AUTHORIZATION_BOUNDARY_REQUIRED"


# ==================================================== 20-23 dedup/contradiction


def test_20_duplicate_source_references_do_not_erase_candidate_histories(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/same"), _ptr(1, "https://sec.gov/same")]
    registered = register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    assert len({r.source_candidate_id for r in registered}) == 2  # distinct candidates
    assert len(store.load_run("L-1").candidates) == 2
    # settling ONE leaves the other pending
    cid0 = _cid("L-1", 0, "https://sec.gov/same")
    verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid0,
        verifier=_StubVerifier({cid0: _verified("SRC-SAME")}), archive=archive,
    )
    from qad.m6.source_bridge import admit_candidate_evidence  # noqa: F401

    store.dispose_candidate("L-1", cid0, disposition="IMPORTED", reason="settled", src01_id="SRC-SAME")
    assert pending_candidates(store.load_run("L-1")) == (_cid("L-1", 1, "https://sec.gov/same"),)


def test_21_conflicting_evidence_is_preserved(store):
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a"), _ptr(1, "https://sec.gov/b")]
    c0 = _cid("L-1", 0, "https://sec.gov/a")
    c1 = _cid("L-1", 1, "https://sec.gov/b")
    process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive,
        verifier=_StubVerifier({c0: _verified("SRC-A", raw=b"a"),
                                c1: _verified("SRC-B", raw=b"b")}),
        registry=registry,
        evidence_builder=_per_candidate_builder({
            c0: {"ev": "EV-A", "ear": "EAR-A"},
            c1: {"ev": "EV-B", "ear": "EAR-B", "contradicts": ["EV-A"]},
        }),
    )
    # BOTH sides preserved; neither averaged away nor deleted
    assert registry.load("EV-01", "EV-A") is not None
    assert registry.load("EV-01", "EV-B").contradicts_ids == ["EV-A"]


def test_22_all_four_dispositions_persist_with_honest_reasons(store):
    archive = _archive(admitted=ADMITTED_AFTER)
    # seed a source admitted AFTER as_of so the SEALED eligibility branch yields UNAVAILABLE
    _admit_direct_source(archive, "SRC-STALE", retrieval_date="2025-01-01")
    _make_run(store)
    refs = [
        _ptr(0, "https://sec.gov/imported"),
        _ptr(1, "https://sec.gov/rejected"),
        _ptr(2, "https://sec.gov/unavailable"),
        _ptr(3, "https://sec.gov/deferred"),
    ]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    results = {
        _cid("L-1", 0, "https://sec.gov/imported"): _verified("SRC-IMP"),
        _cid("L-1", 1, "https://sec.gov/rejected"): _failed(SourceFailureKind.MISMATCH),
        _cid("L-1", 2, "https://sec.gov/unavailable"): _failed(SourceFailureKind.NOT_FOUND),
        _cid("L-1", 3, "https://sec.gov/deferred"): _failed(SourceFailureKind.INSUFFICIENT_PROOF),
    }
    out = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier(results),
    )
    kinds = {o.disposition.value for o in out.outcomes}
    assert kinds == {"IMPORTED", "REJECTED", "UNAVAILABLE", "DEFERRED"}
    for d in store.load_run("L-1").dispositions:
        assert d.reason.strip()
    assert pending_candidates(store.load_run("L-1")) == ()


def test_23_source_admission_succeeds_but_evidence_fails_is_truthful(store):
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")

    def _boom(source_candidate_id, src01_id, verification):
        raise RuntimeError("evidence builder unavailable")

    out = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
        registry=registry, evidence_builder=_boom,
    )
    outcome = out.outcomes[0]
    assert outcome.disposition.value == "IMPORTED"       # the SOURCE was imported
    assert outcome.evidence_ids == () and outcome.ear_ids == ()
    assert "no canonical evidence was admitted" in outcome.reason
    assert registry._data.get("EV-01", {}) == {}
    d = _dispositions(store, "L-1")[cid]
    assert tuple(d.evidence_ids) == () and tuple(d.ear_ids) == ()
    assert d.src01_id == "SRC-A"


# ======================================== 24-27 lifecycle / completeness


def test_24_disposition_failure_never_fabricates_overall_success(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
    )
    rec = store.load_run("L-1")
    assert rec.is_terminal is False          # the bridge never terminalizes
    assert rec.result_sha256 is None


def test_25_process_reentry_reconciles_committed_state_safely(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _verified("SRC-A")})
    first = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=verifier,
    )
    second = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp="2026-10-11T10:00:00+00:00",
        archive=archive, verifier=verifier,
    )
    assert [o.disposition for o in second.outcomes] == [o.disposition for o in first.outcomes]
    assert [o.reason for o in second.outcomes] == [o.reason for o in first.outcomes]
    assert len(archive._data["SRC-01"]) == 1              # no duplicate canonical object
    assert len(store.load_run("L-1").candidates) == 1     # no duplicate candidate
    assert len(store.load_run("L-1").dispositions) == 1   # no rewritten disposition


def test_26_terminal_run_refuses_candidate_and_disposition_mutation(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
    )
    store.terminalize("L-1", terminal_status=TerminalStatus.RESEARCH_UNAVAILABLE)
    with pytest.raises(LedgerTerminalError):
        register_discovered_candidates(
            store, ledger_id="L-1", references=[_ptr(1, "https://sec.gov/b")],
            discovery_timestamp=DISCOVERED_AT,
        )
    with pytest.raises(LedgerTerminalError):
        store.dispose_candidate("L-1", cid, disposition="REJECTED", reason="late")
    with pytest.raises(LedgerTerminalError):
        verify_and_admit_source(
            store, ledger_id="L-1", source_candidate_id=cid, archive=archive
        )
    assert [c.source_candidate_id for c in store.load_run("L-1").candidates] == [cid]


def test_27_incomplete_source_dispositions_block_terminalization(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a"), _ptr(1, "https://sec.gov/b")]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    store.dispose_candidate(
        "L-1", _cid("L-1", 0, "https://sec.gov/a"),
        disposition="UNAVAILABLE", reason="document not available",
    )
    assert pending_candidates(store.load_run("L-1")) == (_cid("L-1", 1, "https://sec.gov/b"),)
    with pytest.raises(LedgerValidationError):
        store.terminalize("L-1", terminal_status=TerminalStatus.RESEARCH_UNAVAILABLE)
    assert store.load_run("L-1").is_terminal is False


# ================================= 28-30 no SUCCESS writer / gate / no provider


def _bridge_imports_and_calls():
    tree = ast.parse(BRIDGE_PATH.read_text(encoding="utf-8"))
    modules: set[str] = set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                modules.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module)
            for a in node.names:
                names.add(a.name)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Name):
            names.add(node.id)
    return modules, names


def test_28_m66_never_writes_deep_research_success():
    """AST-precise: no SUCCESS-writing CALL exists anywhere in the bridge module."""
    tree = ast.parse(BRIDGE_PATH.read_text(encoding="utf-8"))
    forbidden_calls = {
        "finalize_success_attempt_atomic",   # FD #153 atomic SUCCESS writer
        "accept_success_result",
        "terminalize_research_unavailable",
        "terminalize",                       # the generic terminalizing writer
    }
    offending: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = (
            func.attr if isinstance(func, ast.Attribute)
            else func.id if isinstance(func, ast.Name)
            else None
        )
        if name in forbidden_calls:
            offending.append(name)
        for kw in node.keywords:
            if kw.arg in ("outcome", "terminal_status") and "SUCCESS" in ast.unparse(kw.value):
                offending.append(f"{name}({kw.arg}={ast.unparse(kw.value)})")
    assert offending == [], f"SUCCESS-writing calls present: {offending}"
    # the module documents the prohibition but only inside its docstring/comments,
    # so no executable statement may reference the SUCCESS terminal status either
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "SUCCESS":
            offending.append(node.attr)
    assert offending == []


def test_29_raw_success_api_gate_remains_open_and_untouched():
    _, names = _bridge_imports_and_calls()
    assert not any("raw_success_api_gate" in n.lower() for n in names)
    # the gate is recorded OPEN by FD #154 in the register
    register = BRIDGE_PATH.resolve().parents[2] / "operational" / "FOUNDERS-DECISIONS.md"
    text = register.read_text(encoding="utf-8")
    assert "M6_RAW_SUCCESS_API_GATE" in text
    assert "OPEN / BLOCKING M6.7 PROVIDER-EXECUTION INTEGRATION" in text
    bridge_src = BRIDGE_PATH.read_text(encoding="utf-8")
    assert "M6_RAW_SUCCESS_API_GATE" in bridge_src  # documents it, never closes it
    assert "remains OPEN" in bridge_src


def test_30_no_network_gemini_browser_or_provider_code():
    modules, _ = _bridge_imports_and_calls()
    banned = (
        "socket", "requests", "urllib", "http", "httpx", "aiohttp", "selenium",
        "playwright", "pyppeteer", "webbrowser", "subprocess", "chromium", "cdp",
        "gemini", "notebook", "notebooklm", "google",
    )
    hits = [m for m in modules if any(b in m.lower() for b in banned)]
    assert hits == [], f"banned imports present: {hits}"
    src = BRIDGE_PATH.read_text(encoding="utf-8")
    for token in ("import requests", "urlopen(", "socket.", "chromedriver", "selenium"):
        assert token not in src


# ======================== 31-34 round-9 closure (forgery / index / duplicates)


def test_31_a_verdict_cannot_authorize_another_candidate_run_or_source(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A", raw=b"alpha")
    _make_run(store)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/a")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid,
        verifier=_StubVerifier({cid: _verified("SRC-A")}), archive=archive,
    )
    verdict = out.verification
    assert verdict is not None and verdict.verified is True
    # bound to THIS run + candidate
    verdict.assert_attested_for(ledger_id="L-1", source_candidate_id=cid, source_id="SRC-A")
    with pytest.raises(SourceBridgeError):
        verdict.assert_attested_for(ledger_id="L-1", source_candidate_id="SC-someone-else")
    with pytest.raises(SourceBridgeError):
        verdict.assert_attested_for(ledger_id="L-OTHER", source_candidate_id=cid)
    with pytest.raises(SourceBridgeError):
        verdict.assert_attested_for(
            ledger_id="L-1", source_candidate_id=cid, source_id="SRC-DIFFERENT"
        )
    # and it can authorize canonical evidence ONLY for its own run+candidate+source
    assert verdict.authorizes_evidence_for(
        ledger_id="L-1", source_candidate_id=cid, source_id="SRC-A"
    ) is True
    assert verdict.authorizes_evidence_for(
        ledger_id="L-1", source_candidate_id="SC-someone-else", source_id="SRC-A"
    ) is False
    assert verdict.authorizes_evidence_for(
        ledger_id="L-OTHER", source_candidate_id=cid, source_id="SRC-A"
    ) is False
    assert verdict.authorizes_evidence_for(
        ledger_id="L-1", source_candidate_id=cid, source_id="SRC-B"
    ) is False


def test_32_no_importable_mint_path_can_forge_a_trusted_verdict():
    import qad.m6.source_bridge as sb

    with pytest.raises(SourceBridgeError):
        OriginalSourceVerification(verified=True, reason="forged")
    with pytest.raises(SourceBridgeError):
        OriginalSourceVerification(verified=False, reason="forged")
    # ...and valid-looking BINDINGS do not help: the module-private mint token is what
    # actually gates a trusted verdict (this isolates the token check from the binding check)
    with pytest.raises(SourceBridgeError):
        OriginalSourceVerification(
            verified=True, reason="forged",
            bound_ledger_id="L-1", bound_source_candidate_id="SC-forged",
        )
    # no module-addressable mint CALLABLE exists (the minter is closure-scoped; only
    # the non-callable sentinel token lives at module scope)
    assert [n for n in dir(sb) if "mint" in n.lower() and callable(getattr(sb, n))] == []
    tree = ast.parse(BRIDGE_PATH.read_text(encoding="utf-8"))
    module_level = [
        n.name for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and "mint" in n.name.lower()
    ]
    assert module_level == []


def test_33_the_pointer_index_is_reported_to_the_verifier_exactly(store):
    archive = _archive()
    _make_run(store)
    seen: dict[str, int] = {}

    class _Recording:
        def verify(self, request, /):
            seen["index"] = request.pointer_index
            return _failed(SourceFailureKind.NOT_FOUND)

    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(512, "https://sec.gov/x")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 512, "https://sec.gov/x")
    verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=_Recording(),
        archive=archive,
    )
    assert seen["index"] == 512


def test_34_duplicate_input_yields_one_outcome_per_candidate(store):
    archive = _archive()
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a"), _ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    out = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A")}),
    )
    assert len(out.outcomes) == 1
    assert len(store.load_run("L-1").candidates) == 1
    assert len(store.load_run("L-1").dispositions) == 1


# ======================== 35-37 round-10 closure (proof-bound evidence, binding, replay)


def test_35_a_caller_authored_verified_ear_is_refused(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A")
    registry = _registry(archive)
    # an ordinary caller hand-builds the canonical truth value without any verification
    forged = _ear(
        "EV-A", "EAR-A",
        admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION, osv="true",
    )
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-A", "SRC-A"), admission=forged,
            ledger_id="L-1", source_candidate_id="SC-x", verified_source_id="SRC-A",
            verification=None,
        )
    # ...and even an EAR that does NOT assert verification is refused without a verdict
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-A", "SRC-A"), admission=_ear("EV-A", "EAR-A"),
            ledger_id="L-1", source_candidate_id="SC-x", verified_source_id="SRC-A",
            verification=None,
        )
    # ...and a NONEXISTENT run/candidate cannot satisfy the binding
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-A", "SRC-A"), admission=_ear("EV-A", "EAR-A"),
            ledger_id="NO-SUCH-RUN", source_candidate_id="NO-SUCH-CANDIDATE",
            verified_source_id="SRC-A", verification=None,
        )
    assert registry._data.get("EV-01", {}) == {}
    assert registry._data.get("EAR-01", {}) == {}

    # evidence for a source that was NOT the independently verified/admitted one is refused
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-C", "SRC-C"), admission=_ear("EV-C", "EAR-C"),
            ledger_id="L-1", source_candidate_id="SC-x", verified_source_id="SRC-A",
            verification=None,
        )
    assert registry._data.get("EV-01", {}) == {}

    # the EAR/EV identity must agree
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-A", "SRC-A"), admission=_ear("EV-OTHER", "EAR-A"),
            ledger_id="L-1", source_candidate_id="SC-x", verified_source_id="SRC-A",
            verification=None,
        )
    assert registry._data.get("EV-01", {}) == {}


def test_36_a_verdict_from_one_run_cannot_authorize_another(store):
    archive = _archive()
    _admit_direct_source(archive, "SRC-A", raw=b"alpha")
    _make_run(store, ledger_id="L-1", run_id="RR-1", request_id="REQ-1")
    _make_run(store, ledger_id="L-2", run_id="RR-2", request_id="REQ-2")
    c1 = _cid("L-1", 0, "https://sec.gov/a")
    c2 = _cid("L-2", 0, "https://sec.gov/a")
    for lid in ("L-1", "L-2"):
        register_discovered_candidates(
            store, ledger_id=lid, references=[_ptr(0, "https://sec.gov/a")],
            discovery_timestamp=DISCOVERED_AT,
        )
    v1 = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=c1,
        verifier=_StubVerifier({c1: _verified("SRC-A")}), archive=archive,
    ).verification
    assert v1 is not None
    assert v1.authorizes_evidence_for(
        ledger_id="L-1", source_candidate_id=c1, source_id="SRC-A"
    ) is True
    # NEVER for another run/candidate even when both cite the same source
    assert v1.authorizes_evidence_for(
        ledger_id="L-2", source_candidate_id=c2, source_id="SRC-A"
    ) is False
    assert v1.authorizes_evidence_for(
        ledger_id="L-2", source_candidate_id=c1, source_id="SRC-A"
    ) is False
    registry = _registry(archive)
    with pytest.raises(SourceBridgeError):
        admit_candidate_evidence(
            registry, evidence=_ev("EV-B", "SRC-A"),
            admission=_ear("EV-B", "EAR-B", osv="true"),
            ledger_id="L-2", source_candidate_id=c2, verified_source_id="SRC-A",
            verification=v1,
        )
    assert registry._data.get("EV-01", {}) == {}


class _StubPitStore:
    """Deterministic test double for the AUTHORITATIVE PITC-01 resolution surface.

    Only the resolution contract the bridge needs (contains/load) is provided; the
    slope of authorization truth is the PITC record itself, which mirrors the accepted
    runtime rule (mode + Founder role + non-empty exception_reason).
    """

    def __init__(self, pitc):
        self._pitc = pitc

    def contains(self, schema_id, record_id):
        return schema_id == "PITC-01" and record_id == self._pitc.pit_context_id

    def load(self, schema_id, record_id):
        return self._pitc


def test_37_replay_exception_requires_the_authoritative_boundary(store):
    from qad.models.family_i import PITContext, PITContextMode

    def _pitc(*, created_by, exception_reason=None):
        return PITContext(
            pit_context_id="PITC-1", case_id="CASE-1", as_of_date=AS_OF,
            mode=PITContextMode.REPLAY_EXCEPTION, created_by=created_by,
            exception_reason=exception_reason,
        )

    archive = _archive()  # admitted_at <= AS_OF, so the source IS sealed-eligible
    _admit_direct_source(archive, "SRC-OLD", raw=b"seeded")
    _make_run(store, pit_mode=REPLAY_EXCEPTION, as_of=AS_OF)
    register_discovered_candidates(
        store, ledger_id="L-1", references=[_ptr(0, "https://sec.gov/old")],
        discovery_timestamp=DISCOVERED_AT,
    )
    cid = _cid("L-1", 0, "https://sec.gov/old")
    verifier = _StubVerifier({cid: _verified("SRC-OLD", raw=b"seeded")})

    # (a) no authorization surface at all -> fail closed
    out = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier, archive=archive
    )
    assert out.disposition.value == "DEFERRED"
    assert out.reason == "REPLAY_EXCEPTION_AUTHORIZATION_BOUNDARY_REQUIRED"

    # (b) PITC present but NOT Founder-authorized (no exception reason) -> refused
    out2 = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier,
        archive=archive,
        pit_context_store=_StubPitStore(_pitc(created_by="Research Director")),
    )
    assert out2.disposition.value == "DEFERRED"

    # (b2) Founder role but EMPTY exception reason -> still refused
    out2b = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier,
        archive=archive,
        pit_context_store=_StubPitStore(_pitc(created_by="FOUNDER", exception_reason="")),
    )
    assert out2b.disposition.value == "DEFERRED"

    # (c) properly authorized -> the existing labelled path proceeds (eligible reuse)
    out3 = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid, verifier=verifier,
        archive=archive,
        pit_context_store=_StubPitStore(_pitc(
            created_by="FOUNDER", exception_reason="Founder-authorized re-evaluation",
        )),
    )
    assert out3.disposition.value == "IMPORTED"
    assert out3.reused is True


# ======================== 38 round-11 closure (cross-store re-entry reconciliation)


def test_38_disposition_failure_after_evidence_admission_is_reconciled_on_retry(
    store, monkeypatch
):
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _verified("SRC-A")})

    # inject a ONE-TIME failure in the ledger disposition write, AFTER canonical
    # evidence admission has already committed.
    real_dispose = store.dispose_candidate
    calls = {"n": 0}

    def _flaky(ledger_id, source_candidate_id, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LedgerValidationError("INJECTED disposition failure")
        return real_dispose(ledger_id, source_candidate_id, **kw)

    monkeypatch.setattr(store, "dispose_candidate", _flaky, raising=False)
    # the disposition write fails AFTER the canonical evidence was committed -> the
    # whole call fails closed (nothing is silently claimed), leaving the candidate pending
    with pytest.raises(LedgerValidationError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=verifier, registry=registry,
            evidence_builder=_evidence_builder(),
        )
    assert registry.contains("EV-01", "EV-A")
    assert registry.contains("EAR-01", "EAR-A")
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}

    # re-entry must RECONCILE the committed evidence (not report a false failure)
    second = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp="2026-10-12T10:00:00+00:00",
        archive=archive, verifier=verifier, registry=registry,
        evidence_builder=_evidence_builder(),
    )
    o = second.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == ("EV-A",) and o.ear_ids == ("EAR-A",)
    assert o.evidence_admission_error is None
    d = _dispositions(store, "L-1")[cid]
    assert tuple(d.evidence_ids) == ("EV-A",) and tuple(d.ear_ids) == ("EAR-A",)
    assert pending_candidates(store.load_run("L-1")) == ()
    # exactly ONE canonical object each — reconciliation did not duplicate anything
    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1

# ================== 39 round-12 closure (conflicting canonical record is NOT reconciled)


def test_39_a_conflicting_canonical_evidence_record_is_not_reconciled(store):
    archive = _archive()
    registry = _registry(archive)
    _admit_direct_source(archive, "SRC-A", raw=b"seeded")
    # pre-seed the SAME canonical ids (through the existing gate) with a DIFFERENT payload
    seed_ev = EvidenceRecord(
        admitting_role="Research Director", as_of=AS_OF,
        content="DIFFERENT PAYLOAD", evidence_id="EV-A",
        evidence_type=EvidenceRecordEvidence_type.CLAIM,
        extractor="seeded fixture", source_id="SRC-A", source_tier="L1",
        validation_status=EvidenceRecordValidation_status.RAW,
    )
    registry.admit_evidence(seed_ev, _ear("EV-A", "EAR-A"))
    assert registry.load("EV-01", "EV-A").content == "DIFFERENT PAYLOAD"

    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    # a same-id / different-payload conflict must SURFACE, never be reconciled as success
    with pytest.raises(SourceEvidenceConflict):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A", raw=b"seeded")}),
            registry=registry, evidence_builder=_evidence_builder(),
        )
    # the candidate stays UNDISPOSED and no false linkage is recorded
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}
    # the stored canonical record is preserved, never rewritten
    assert registry.load("EV-01", "EV-A").content == "DIFFERENT PAYLOAD"
    assert len(registry._data["EV-01"]) == 1


# ======== 40-41 round-13 closure (incomplete pre-existing canonical pair is a conflict)


def _simulate_collision(monkeypatch, registry, *, ev_exists, ear_exists, exc):
    """Deterministically simulate an INCOMPLETE pre-existing canonical pair.

    The accepted registry cannot be driven into holding a LONE EV-01 or EAR-01 through its
    own admission gate, so the collision surface is simulated: `admit_evidence` raises the
    given persistence error and `contains` reports the partial pre-existing pair.
    """
    real_contains = registry.contains

    def _contains(schema_id, record_id):
        if schema_id == "EV-01" and ev_exists:
            return True
        if schema_id == "EAR-01" and ear_exists:
            return True
        return real_contains(schema_id, record_id)

    monkeypatch.setattr(registry, "contains", _contains, raising=False)
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(exc), raising=False,
    )


def _collision_run(store, monkeypatch, *, ev_exists, ear_exists, exc):
    archive = _archive()
    registry = _registry(archive)
    _admit_direct_source(archive, "SRC-A", raw=b"seeded")
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    _simulate_collision(
        monkeypatch, registry, ev_exists=ev_exists, ear_exists=ear_exists, exc=exc
    )
    with pytest.raises(SourceEvidenceConflict):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified("SRC-A", raw=b"seeded")}),
            registry=registry, evidence_builder=_evidence_builder(),
        )
    # the candidate is NOT settled on a canonical identity collision
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}


def test_40_an_ev_only_collision_is_a_propagated_conflict(store, monkeypatch):
    _collision_run(
        store, monkeypatch, ev_exists=True, ear_exists=False,
        exc=IntegrityConflict("INJECTED EV-only canonical collision"),
    )


def test_41_an_ear_only_collision_is_a_propagated_conflict(store, monkeypatch):
    _collision_run(
        store, monkeypatch, ev_exists=False, ear_exists=True,
        exc=TransactionFailure("INJECTED EAR-only canonical collision"),
    )


# ============================================================================
# 42-47 round-14 closure — CLOSED DECISION STRUCTURE (structural refactor, FD #151 A+)
#
# Row coverage of the mandated classification table:
#   1  neither exists + explicitly retryable operational error -> row01
#   2  neither exists + unexpected exception                  -> row02
#   3  EV exists, EAR absent                                  -> row03
#   4  EAR exists, EV absent                                  -> row04
#   5  both exist, identical payload/hash                     -> row05
#   6  both exist, EV payload mismatch                        -> row06
#   7  both exist, EAR payload mismatch                       -> row07
#   8  both exist, source mismatch                            -> row08
#   9  canonical record load/read-back fails                  -> row09_load / row09_contains
#   10 unknown integrity exception                            -> row10
#   11 proof-verification exception                           -> row11
#   12 PIT-validation exception                               -> row12
#   13 evidence-builder exception                             -> test_43 (pre-boundary stage)
#   14 disposition write fails after canonical admission       -> test_44
#   15 re-entry after identical evidence commit                -> row13 + test_38 + test_46
#   16 re-entry after conflicting evidence commit               -> row14 + tests 39/40/41
#   17 no candidate settlement on unresolved governance error  -> test_45 + test_47
#   18 no duplicate canonical records during replay             -> test_46
#
# The table calls the refactored CLASSIFIER directly (not a public happy path), so it
# proves the classifier itself.
# ============================================================================

EXPECTED_EV_ID = "EV-A"
EXPECTED_EAR_ID = "EAR-A"
EXPECTED_SRC = "SRC-A"

#: The functions that make up the refactored admission/reconciliation boundary.
_REFACTORED_FUNCTIONS = (
    "process_discovered_sources",
    "construct_candidate_evidence",
    "attempt_canonical_evidence_admission",
    "classify_evidence_admission_failure",
    "reconcile_canonical_evidence_pair",
    "dispose_settled_candidate",
)


def _mk_ev(
    evidence_id,
    source_id,
    *,
    content="Verified extract from the original document.",
):
    """Exactly the EV-01 the bridge's 3-argument fixture builder would produce."""
    return EvidenceRecord(
        admitting_role="Research Director",
        as_of=AS_OF,
        content=content,
        evidence_id=evidence_id,
        evidence_type=EvidenceRecordEvidence_type.CLAIM,
        extractor="M6.6 bridge fixture",
        source_id=source_id,
        source_tier="L1",
        validation_status=EvidenceRecordValidation_status.RAW,
    )


def _mk_ear(
    evidence_id,
    admission_id,
    *,
    method=EvidenceAdmissionRecordAdmission_method.DIRECT_SOURCE,
    validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
    osv=None,
):
    """Exactly the EAR-01 the bridge's 3-argument fixture builder would produce."""
    return EvidenceAdmissionRecord(
        admission_id=admission_id,
        admission_method=method,
        admission_timestamp=DISCOVERED_AT,
        admitting_role="Research Director",
        evidence_id=evidence_id,
        source_tier_check="L1",
        validation_method=validation_method,
        original_source_verified=osv,
    )


class _LoadBombRegistry:
    """contains() reports the pair, but the AUTHORITATIVE load fails."""

    def __init__(self, exc):
        self._exc = exc

    def contains(self, schema_id, record_id):
        return True

    def load(self, schema_id, record_id):
        raise self._exc


class _ContainsBombRegistry:
    """The authoritative EXISTS check itself fails: the state cannot be established."""

    def __init__(self, exc):
        self._exc = exc

    def contains(self, schema_id, record_id):
        raise self._exc

    def load(self, schema_id, record_id):  # pragma: no cover - never reached
        raise self._exc


def _patch_pair_state(monkeypatch, registry, *, ev_exists, ear_exists):
    """Deterministically report a partial pre-existing canonical pair (read-only patch)."""
    real_contains = registry.contains

    def _contains(schema_id, record_id):
        if schema_id == "EV-01" and ev_exists:
            return True
        if schema_id == "EAR-01" and ear_exists:
            return True
        return real_contains(schema_id, record_id)

    monkeypatch.setattr(registry, "contains", _contains, raising=False)


def _seeded_registry(*, seed_ev=None, seed_ear=None):
    """A registry holding an ALREADY-COMMITTED canonical pair (authoritative gate only)."""
    archive = _archive()
    _admit_direct_source(archive, EXPECTED_SRC, raw=b"seeded")
    registry = _registry(archive)
    if seed_ev is not None and seed_ear is not None:
        registry.admit_evidence(seed_ev, seed_ear)
    return registry


_IDENTICAL_SEED = dict(
    seed_ev=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
    seed_ear=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
)

CLASSIFICATION_TABLE = [
    pytest.param(
        dict(
            id="row01_neither_exists_retryable",
            error=TransactionFailure("INJECTED retryable batch failure"),
            expect=EvidenceAdmissionClassification.TRANSIENT_PARTIAL,
        ),
        id="row01_neither_exists_retryable",
    ),
    pytest.param(
        dict(
            id="row02_neither_exists_unexpected",
            error=RuntimeError("UNEXPLAINED canonical failure"),
            raises=RuntimeError,
            original_propagates=True,
        ),
        id="row02_neither_exists_unexpected",
    ),
    pytest.param(
        dict(
            id="row03_ev_only",
            error=IntegrityConflict("INJECTED EV-only canonical collision"),
            ev_exists=True, ear_exists=False,
            expect=EvidenceAdmissionClassification.CONFLICT_INCOMPLETE,
        ),
        id="row03_ev_only",
    ),
    pytest.param(
        dict(
            id="row04_ear_only",
            error=TransactionFailure("INJECTED EAR-only canonical collision"),
            ev_exists=False, ear_exists=True,
            expect=EvidenceAdmissionClassification.CONFLICT_INCOMPLETE,
        ),
        id="row04_ear_only",
    ),
    pytest.param(
        dict(
            id="row05_identical_pair",
            error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
            seed=True,
            expect=EvidenceAdmissionClassification.RECONCILED_IDENTICAL,
        ),
        id="row05_identical_pair",
    ),
    pytest.param(
        dict(
            id="row06_ev_payload_mismatch",
            error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
            seed=True,
            seed_ev=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC, content="DIFFERENT PAYLOAD"),
            seed_ear=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
            expect=EvidenceAdmissionClassification.CONFLICT_DIVERGENT,
        ),
        id="row06_ev_payload_mismatch",
    ),
    pytest.param(
        dict(
            id="row07_ear_payload_mismatch",
            error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
            seed=True,
            seed_ev=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            seed_ear=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID, validation_method="DIFFERENT"),
            expect=EvidenceAdmissionClassification.CONFLICT_DIVERGENT,
        ),
        id="row07_ear_payload_mismatch",
    ),
    pytest.param(
        dict(
            id="row08_source_mismatch",
            error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
            seed=True,
            verified_source_id="SRC-OTHER",
            expect=EvidenceAdmissionClassification.CONFLICT_DIVERGENT,
        ),
        id="row08_source_mismatch",
    ),
    pytest.param(
        dict(
            id="row09_read_back_load_fails",
            error=IntegrityConflict("ORIGINAL collision error"),
            read_back="load",
            raises=KeyError,
        ),
        id="row09_read_back_load_fails",
    ),
    pytest.param(
        dict(
            id="row09_read_back_contains_fails",
            error=IntegrityConflict("ORIGINAL collision error"),
            read_back="contains",
            raises=KeyError,
        ),
        id="row09_read_back_contains_fails",
    ),
    pytest.param(
        dict(
            id="row10_unknown_integrity_exception",
            error=IntegrityConflict("UNEXPLAINED integrity failure"),
            raises=IntegrityConflict,
            original_propagates=True,
        ),
        id="row10_unknown_integrity_exception",
    ),
    pytest.param(
        dict(
            id="row11_proof_verification_exception",
            error=SourceBridgeError("forged proof / binding refused"),
            raises=SourceBridgeError,
            original_propagates=True,
        ),
        id="row11_proof_verification_exception",
    ),
    pytest.param(
        dict(
            id="row12_pit_validation_exception",
            error=PITBlockError("PIT enforcement forbids this read"),
            raises=PITBlockError,
            original_propagates=True,
        ),
        id="row12_pit_validation_exception",
    ),
    pytest.param(
        dict(
            id="row13_reentry_after_identical_commit",
            error=TransactionFailure("disposition write failed AFTER the commit"),
            seed=True,
            expect=EvidenceAdmissionClassification.RECONCILED_IDENTICAL,
        ),
        id="row13_reentry_after_identical_commit",
    ),
    pytest.param(
        dict(
            id="row14_reentry_after_conflicting_commit",
            error=TransactionFailure("disposition write failed AFTER a conflicting commit"),
            seed=True,
            seed_ev=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC, content="DIFFERENT PAYLOAD"),
            seed_ear=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
            expect=EvidenceAdmissionClassification.CONFLICT_DIVERGENT,
        ),
        id="row14_reentry_after_conflicting_commit",
    ),
]


@pytest.mark.parametrize("case", CLASSIFICATION_TABLE)
def test_42_the_failure_classifier_is_exhaustive_table_driven(case, monkeypatch):
    """The refactored classifier, driven directly over the mandated case table."""
    if case.get("read_back") == "load":
        registry = _LoadBombRegistry(KeyError("INJECTED authoritative load failure"))
    elif case.get("read_back") == "contains":
        registry = _ContainsBombRegistry(KeyError("INJECTED authoritative load failure"))
    elif case.get("seed"):
        registry = _seeded_registry(
            seed_ev=case.get("seed_ev", _IDENTICAL_SEED["seed_ev"]),
            seed_ear=case.get("seed_ear", _IDENTICAL_SEED["seed_ear"]),
        )
    else:
        registry = _seeded_registry()
    if "ev_exists" in case:
        _patch_pair_state(
            monkeypatch, registry, ev_exists=case["ev_exists"], ear_exists=case["ear_exists"]
        )

    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)
    call = dict(
        registry=registry,
        error=case["error"],
        evidence=expected_ev,
        admission=expected_ear,
        verified_source_id=case.get("verified_source_id", EXPECTED_SRC),
    )

    if case.get("raises") is not None:
        with pytest.raises(case["raises"]) as excinfo:
            classify_evidence_admission_failure(**call)
        if case.get("original_propagates"):
            # FAIL CLOSED preserves the ORIGINAL error and its provenance.
            assert excinfo.value is case["error"]
        return

    decision = classify_evidence_admission_failure(**call)
    assert decision.classification is case["expect"]
    assert decision.settled is (
        case["expect"] is not EvidenceAdmissionClassification.CONFLICT_INCOMPLETE
        and case["expect"] is not EvidenceAdmissionClassification.CONFLICT_DIVERGENT
    )
    if case["expect"] is EvidenceAdmissionClassification.RECONCILED_IDENTICAL:
        assert decision.evidence_id == EXPECTED_EV_ID
        assert decision.ear_id == EXPECTED_EAR_ID


def test_42b_the_retryable_allowlist_is_explicit_and_narrow():
    """The transient path is an EXPLICIT allowlist — never `except Exception`."""
    from qad.m6 import source_bridge as sb

    assert sb._RETRYABLE_OPERATIONAL_FAILURES == (TransactionFailure,)
    for never_transient in (
        IntegrityConflict, CanonicalBoundaryViolation, MissingForeignKey,
        PITBlockError, SourceBridgeError, RuntimeError,
    ):
        assert never_transient not in sb._RETRYABLE_OPERATIONAL_FAILURES


def test_42c_no_broad_handler_in_the_refactored_region_can_downgrade_a_failure():
    """The refactored region has NO catch-all that records or downgrades a failure class."""
    tree = ast.parse(BRIDGE_PATH.read_text(encoding="utf-8"))
    offenders = []
    seen = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name not in _REFACTORED_FUNCTIONS:
            continue
        seen.add(node.name)
        for sub in ast.walk(node):
            if not isinstance(sub, ast.ExceptHandler):
                continue
            broad = sub.type is None or (
                isinstance(sub.type, ast.Name) and sub.type.id in ("Exception", "BaseException")
            )
            if not broad:
                continue
            for stmt in sub.body:
                # an allowed broad handler may ONLY return a classification/route or raise
                if isinstance(stmt, (ast.Return, ast.Raise)):
                    continue
                offenders.append((node.name, sub.lineno, type(stmt).__name__))
    assert seen == set(_REFACTORED_FUNCTIONS), f"missing refactored functions: {seen}"
    assert offenders == [], f"broad handlers that could classify/downgrade a failure: {offenders}"


# ==================================================== 43-47 behavioural closeout of the table


def test_43_an_evidence_builder_failure_is_a_pre_boundary_transient_partial(store):
    """Row 13 — construction is mutation-free, so its failure is the truthful partial."""
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")

    def _boom(candidate_id, src01_id, verification):
        raise RuntimeError("evidence builder unavailable")

    out = process_discovered_sources(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
        archive=archive, verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}),
        registry=registry, evidence_builder=_boom,
    )
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == () and o.ear_ids == ()
    assert o.evidence_admission_error == "RuntimeError: evidence builder unavailable"
    assert "evidence construction FAILED" in o.reason
    assert "no canonical evidence was admitted" in o.reason
    # the PRE-BOUNDARY stage mutated NO canonical state at all
    assert registry._data.get("EV-01", {}) == {}
    assert registry._data.get("EAR-01", {}) == {}
    # the disposition is still written (truthful, permitted terminal outcome)
    assert _dispositions(store, "L-1")[cid].disposition.value == "IMPORTED"
    # ...and nothing was fabricated on the canonical side on re-entry either
    assert registry._data.get("EV-01", {}) == {}


def test_43b_a_governance_failure_from_the_builder_still_fails_closed(store):
    """The pre-boundary allowlist never absorbs a SourceBridgeError governance failure."""
    cid = _cid("L-1", 0, "https://sec.gov/a")

    def _governance(candidate_id, src01_id, verification):
        raise SourceBridgeError("builder governance failure")

    with pytest.raises(SourceBridgeError):
        construct_candidate_evidence(_governance, cid, EXPECTED_SRC, None)

    # and end-to-end: the candidate stays UNDISPOSED
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    with pytest.raises(SourceBridgeError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}),
            registry=registry, evidence_builder=_governance,
        )
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}


def test_44_a_disposition_write_failure_after_canonical_admission_settles_nothing(
    store, monkeypatch
):
    """Row 14 — the canonical pair is preserved and NO disposition is written."""
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")

    def _always_fail(ledger_id, source_candidate_id, **kw):
        raise LedgerValidationError("INJECTED disposition failure")

    monkeypatch.setattr(store, "dispose_candidate", _always_fail, raising=False)
    with pytest.raises(LedgerValidationError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}),
            registry=registry, evidence_builder=_evidence_builder(),
        )
    # the committed canonical pair is neither deleted nor rewritten
    assert registry.contains("EV-01", EXPECTED_EV_ID)
    assert registry.contains("EAR-01", EXPECTED_EAR_ID)
    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1
    # nothing was settled
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}


def test_45_no_candidate_settlement_on_an_unresolved_governance_error(store, monkeypatch):
    """Row 17 — every unresolved governance error leaves the candidate undisposed."""
    # (a) an UNKNOWN error with NO canonical trace: FAIL CLOSED, nothing settled
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(RuntimeError("UNEXPLAINED canonical failure")),
        raising=False,
    )
    with pytest.raises(RuntimeError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}),
            registry=registry, evidence_builder=_evidence_builder(),
        )
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert _dispositions(store, "L-1") == {}
    assert registry._data.get("EV-01", {}) == {}

    # (b) an INCOMPLETE pair: a TYPED conflict (SourceEvidenceIncomplete), nothing settled
    archive2 = _archive()
    registry2 = _registry(archive2)
    _admit_direct_source(archive2, EXPECTED_SRC, raw=b"seeded")
    ledger_id = "L-B"
    _make_run(store, ledger_id=ledger_id, run_id="RR-B", request_id="REQ-B")
    _patch_pair_state(monkeypatch, registry2, ev_exists=True, ear_exists=False)
    monkeypatch.setattr(
        registry2, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(
            IntegrityConflict("INJECTED EV-only canonical collision")
        ),
        raising=False,
    )
    cid_b = _cid(ledger_id, 0, "https://sec.gov/b")
    with pytest.raises(SourceEvidenceIncomplete):
        process_discovered_sources(
            store, ledger_id=ledger_id, references=[_ptr(0, "https://sec.gov/b")],
            discovery_timestamp=DISCOVERED_AT, archive=archive2,
            verifier=_StubVerifier({cid_b: _verified(EXPECTED_SRC, raw=b"seeded")}),
            registry=registry2, evidence_builder=_evidence_builder(ledger_id=ledger_id),
        )
    assert pending_candidates(store.load_run(ledger_id)) == (cid_b,)
    assert _dispositions(store, ledger_id) == {}


def test_46_no_duplicate_canonical_records_during_replay(store, monkeypatch):
    """Row 18 — replay reconciles; it never duplicates or rewrites canonical state."""
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    verifier = _StubVerifier({cid: _verified(EXPECTED_SRC)})

    real_dispose = store.dispose_candidate
    calls = {"n": 0}

    def _flaky(ledger_id, source_candidate_id, **kw):
        calls["n"] += 1
        if calls["n"] == 1:
            raise LedgerValidationError("INJECTED disposition failure")
        return real_dispose(ledger_id, source_candidate_id, **kw)

    monkeypatch.setattr(store, "dispose_candidate", _flaky, raising=False)
    with pytest.raises(LedgerValidationError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=verifier, registry=registry,
            evidence_builder=_evidence_builder(),
        )
    monkeypatch.setattr(store, "dispose_candidate", real_dispose, raising=False)

    for stamp in ("2026-10-12T10:00:00+00:00", "2026-10-13T10:00:00+00:00",
                  "2026-10-14T10:00:00+00:00"):
        out = process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=stamp,
            archive=archive, verifier=verifier, registry=registry,
            evidence_builder=_evidence_builder(),
        )
        o = out.outcomes[0]
        assert o.disposition.value == "IMPORTED"
        assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
        assert o.evidence_admission_error is None

    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1
    assert len(archive._data["SRC-01"]) == 1
    assert len(store.load_run("L-1").dispositions) == 1
    assert pending_candidates(store.load_run("L-1")) == ()


def test_47_the_three_operations_are_separable_and_fail_closed(store):
    """Operation A / B / C are independently testable, and C never settles an unsettled case."""
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    # the verified original bytes are ALREADY admitted, so operation A can run
    _admit_direct_source(archive, EXPECTED_SRC, raw=b"alpha")
    refs = [_ptr(0, "https://sec.gov/a")]
    register_discovered_candidates(
        store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT
    )
    cid = _cid("L-1", 0, "https://sec.gov/a")
    admission = verify_and_admit_source(
        store, ledger_id="L-1", source_candidate_id=cid,
        verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}), archive=archive,
    )
    assert admission.disposition.value == "IMPORTED"
    assert admission.verification is not None
    ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)

    # B — the authoritative read-back reports NO canonical trace
    state = reconcile_canonical_evidence_pair(
        registry, evidence=ev, admission=ear, verified_source_id=EXPECTED_SRC
    )
    assert isinstance(state, CanonicalPairState)
    assert (state.ev_exists, state.ear_exists, state.classification) == (False, False, None)

    def _attempt():
        return attempt_canonical_evidence_admission(
            registry, evidence=ev, admission=ear, ledger_id="L-1",
            source_candidate_id=cid, verified_source_id=EXPECTED_SRC,
            verification=admission.verification,
        )

    # A — a fresh canonical admission is ADMITTED_NEW; the replay is RECONCILED_IDENTICAL
    fresh = _attempt()
    assert fresh.classification is EvidenceAdmissionClassification.ADMITTED_NEW
    assert fresh.settled is True
    replay = _attempt()
    assert replay.classification is EvidenceAdmissionClassification.RECONCILED_IDENTICAL
    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1

    # B — now both exist and match EXACTLY
    state2 = reconcile_canonical_evidence_pair(
        registry, evidence=ev, admission=ear, verified_source_id=EXPECTED_SRC
    )
    assert state2.classification is EvidenceAdmissionClassification.RECONCILED_IDENTICAL

    # C — an UNSETTLED decision is refused BEFORE any disposition write
    class _RecordingStore:
        def __init__(self):
            self.writes = 0

        def dispose_candidate(self, *a, **kw):
            self.writes += 1

    recorder = _RecordingStore()
    incomplete = EvidenceAdmissionDecision(
        EvidenceAdmissionClassification.CONFLICT_INCOMPLETE, diagnostic="EV-only"
    )
    with pytest.raises(SourceEvidenceIncomplete):
        dispose_settled_candidate(
            recorder, ledger_id="L-1", registered=None, admission=None,
            decision=incomplete, reason="x", evidence_ids=(), ear_ids=(),
        )
    divergent = EvidenceAdmissionDecision(
        EvidenceAdmissionClassification.CONFLICT_DIVERGENT, diagnostic="differs"
    )
    with pytest.raises(SourceEvidenceConflict):
        dispose_settled_candidate(
            recorder, ledger_id="L-1", registered=None, admission=None,
            decision=divergent, reason="x", evidence_ids=(), ear_ids=(),
        )
    assert recorder.writes == 0          # NOTHING was settled
    assert EvidenceAdmissionDecision(
        EvidenceAdmissionClassification.TRANSIENT_PARTIAL
    ).settled is True


# ============================================================================
# 48-54 round-15 closure — RECONCILIATION-ENTRY ALLOWLIST (Round-14 material finding)
#
# The Round-14 finding: an UNRECOGNIZED exception raised by the canonical gate while an EXACT
# canonical pair already exists was reconciled into a settled IMPORTED outcome claiming the
# EV-01/EAR-01 lineage, because reconciliation was entered for any non-SourceBridgeError failure.
# The correction restores an explicit entry allowlist (_RECONCILABLE_ENTRY_FAILURES); every other
# failure class propagates UNCHANGED before any read-back.
#
# Founder-mandated cases: A (test_48) · B (test_49) · C (test_50) · D (test_51) · E (test_52) ·
# F (test_53) · G (mutation demonstration, evidence/m6.6/RED-DEMO-ROUND15-*.txt) · plus the
# probe-11 test-strength gap on the SourceBridgeError guard (test_54).
# ============================================================================


class _GovernanceCollision(SourceBridgeError, IntegrityConflict):
    """TEST-ONLY: a governance failure that ALSO carries collision-shaped semantics.

    Used to prove the SourceBridgeError guard takes PRECEDENCE over the reconciliation-entry
    allowlist: a governance failure must never be reconciled, even when its type is also one of
    the recognized collision classes (the Round-14 reviewer's probe-11 test-strength gap).
    """


class _ReadBackSpy:
    """Proves NO authoritative read-back is attempted (any call is an immediate failure)."""

    def __init__(self):
        self.calls = 0

    def contains(self, schema_id, record_id):
        self.calls += 1
        raise AssertionError("authoritative read-back must NOT be attempted")

    def load(self, schema_id, record_id):  # pragma: no cover - never reached
        self.calls += 1
        raise AssertionError("authoritative read-back must NOT be attempted")


def _canonical_hashes(registry):
    return (
        compute_canonical_hash(registry.load("EV-01", EXPECTED_EV_ID)),
        compute_canonical_hash(registry.load("EAR-01", EXPECTED_EAR_ID)),
    )


def _pending_candidate_with_exact_pair(tmp_path, *, ledger_id="L-1",
                                       reference="https://sec.gov/a"):
    """Drive a candidate into the GENUINE 'identical canonical pair already exists' state.

    The pair is committed by a real earlier attempt whose disposition write failed, so the
    candidate is still pending and the stored pair is exactly what this candidate would write.
    """
    store = DeepResearchRunLedgerStore(tmp_path / f"{ledger_id}.sqlite3")
    archive = _archive()
    registry = _registry(archive)
    _make_run(store, ledger_id=ledger_id, run_id=f"RR-{ledger_id}", request_id=f"REQ-{ledger_id}")
    refs = [_ptr(0, reference)]
    cid = _cid(ledger_id, 0, reference)
    verifier = _StubVerifier({cid: _verified(EXPECTED_SRC)})
    real_dispose = store.dispose_candidate

    def _fail(ledger, source_candidate_id, **kw):
        raise LedgerValidationError("INJECTED disposition failure")

    store.dispose_candidate = _fail
    with pytest.raises(LedgerValidationError):
        process_discovered_sources(
            store, ledger_id=ledger_id, references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=verifier, registry=registry,
            evidence_builder=_evidence_builder(ledger_id=ledger_id),
        )
    store.dispose_candidate = real_dispose
    assert registry.contains("EV-01", EXPECTED_EV_ID)
    assert registry.contains("EAR-01", EXPECTED_EAR_ID)
    assert pending_candidates(store.load_run(ledger_id)) == (cid,)
    return store, archive, registry, cid, verifier, refs


def _rerun(store, registry, archive, verifier, refs, *, ledger_id="L-1", stamp="2026-10-13T10:00:00+00:00"):
    return process_discovered_sources(
        store, ledger_id=ledger_id, references=refs, discovery_timestamp=stamp,
        archive=archive, verifier=verifier, registry=registry,
        evidence_builder=_evidence_builder(ledger_id=ledger_id),
    )


def test_48_A_unknown_error_with_an_exact_canonical_pair_fails_closed(tmp_path, monkeypatch):
    """Case A — unknown RuntimeError + an EXACT existing canonical pair."""
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    before = _canonical_hashes(registry)
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)
    unknown = RuntimeError("UNEXPLAINED canonical failure")

    # (a) DIRECT classifier: the ORIGINAL exception propagates and NOTHING is read back
    spy = _ReadBackSpy()
    with pytest.raises(RuntimeError) as excinfo:
        classify_evidence_admission_failure(
            spy, error=unknown, evidence=expected_ev, admission=expected_ear,
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is unknown          # provenance preserved
    assert spy.calls == 0                    # read-back was never attempted

    # (b) END-TO-END: same outcome through process_discovered_sources
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(RuntimeError("UNEXPLAINED canonical failure")),
        raising=False,
    )
    with pytest.raises(RuntimeError):
        _rerun(store, registry, archive, verifier, refs)
    assert pending_candidates(store.load_run("L-1")) == (cid,)   # still pending
    assert _dispositions(store, "L-1") == {}                     # no disposition
    assert _canonical_hashes(registry) == before                 # hashes unchanged
    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1


def test_49_B_unknown_error_with_no_canonical_pair_fails_closed(store):
    """Case B (control) — unknown RuntimeError + NO canonical pair."""
    archive = _archive()
    registry = _registry(archive)
    _make_run(store)
    refs = [_ptr(0, "https://sec.gov/a")]
    cid = _cid("L-1", 0, "https://sec.gov/a")
    unknown = RuntimeError("UNEXPLAINED canonical failure")

    with pytest.raises(RuntimeError) as excinfo:
        classify_evidence_admission_failure(
            _ReadBackSpy(), error=unknown,
            evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is unknown

    registry.admit_evidence = lambda e, a: (_ for _ in ()).throw(
        RuntimeError("UNEXPLAINED canonical failure")
    )
    with pytest.raises(RuntimeError):
        process_discovered_sources(
            store, ledger_id="L-1", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=_StubVerifier({cid: _verified(EXPECTED_SRC)}),
            registry=registry, evidence_builder=_evidence_builder(),
        )
    assert _dispositions(store, "L-1") == {}
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert registry._data.get("EV-01", {}) == {}


def test_50_C_recognized_collision_with_an_exact_pair_still_reconciles(tmp_path):
    """Case C — recognized IntegrityConflict + EXACT pair -> RECONCILED_IDENTICAL, no duplicate."""
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)

    # (a) DIRECT classifier against a committed, exactly-matching canonical pair
    decision = classify_evidence_admission_failure(
        _seeded_registry(seed_ev=expected_ev, seed_ear=expected_ear),
        error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
        evidence=expected_ev, admission=expected_ear, verified_source_id=EXPECTED_SRC,
    )
    assert decision.classification is EvidenceAdmissionClassification.RECONCILED_IDENTICAL
    assert decision.settled is True
    assert (decision.evidence_id, decision.ear_id) == (EXPECTED_EV_ID, EXPECTED_EAR_ID)

    # (b) END-TO-END with the registry's OWN natural collision (no fault injection): the pair was
    # committed by an earlier attempt of THIS candidate, so the existing ids are reused
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    out = _rerun(store, registry, archive, verifier, refs)
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
    assert o.evidence_admission_error is None
    d = _dispositions(store, "L-1")[cid]
    assert tuple(d.evidence_ids) == (EXPECTED_EV_ID,)
    assert tuple(d.ear_ids) == (EXPECTED_EAR_ID,)
    assert pending_candidates(store.load_run("L-1")) == ()
    assert len(registry._data["EV-01"]) == 1     # NO duplicate canonical record
    assert len(registry._data["EAR-01"]) == 1


def test_51_D_recognized_transaction_failure_with_an_exact_pair_reconciles(tmp_path, monkeypatch):
    """Case D — recognized TransactionFailure + EXACT pair -> read-back reconciliation."""
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)

    # (a) DIRECT classifier against a committed, exactly-matching canonical pair
    decision = classify_evidence_admission_failure(
        _seeded_registry(seed_ev=expected_ev, seed_ear=expected_ear),
        error=TransactionFailure("INJECTED batch failure"),
        evidence=expected_ev, admission=expected_ear, verified_source_id=EXPECTED_SRC,
    )
    assert decision.classification is EvidenceAdmissionClassification.RECONCILED_IDENTICAL

    # (b) END-TO-END: a recognized TransactionFailure on the retry still reconciles the pair the
    # earlier attempt committed, through the authoritative read-back + exact identity checks
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(TransactionFailure("INJECTED batch failure")),
        raising=False,
    )
    out = _rerun(store, registry, archive, verifier, refs)
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
    assert pending_candidates(store.load_run("L-1")) == ()
    assert len(registry._data["EV-01"]) == 1
    assert len(registry._data["EAR-01"]) == 1


def test_52_E_unknown_error_with_an_incomplete_or_divergent_pair_never_reconciles(
    tmp_path, monkeypatch
):
    """Case E — unknown exception + INCOMPLETE or DIVERGENT pair: never reconcile, never settle."""
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)
    unknown = RuntimeError("UNEXPLAINED canonical failure")

    # (a) INCOMPLETE pair (EV-only) + unknown error -> propagate, nothing settled
    incomplete = _seeded_registry()
    _patch_pair_state(monkeypatch, incomplete, ev_exists=True, ear_exists=False)
    with pytest.raises(RuntimeError) as excinfo:
        classify_evidence_admission_failure(
            incomplete, error=unknown, evidence=expected_ev, admission=expected_ear,
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is unknown

    # (b) DIVERGENT pair (different EV payload) + unknown error -> propagate, nothing settled
    divergent = _seeded_registry(
        seed_ev=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC, content="DIFFERENT PAYLOAD"),
        seed_ear=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
    )
    with pytest.raises(RuntimeError) as excinfo2:
        classify_evidence_admission_failure(
            divergent, error=unknown, evidence=expected_ev, admission=expected_ear,
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo2.value is unknown

    # (c) END-TO-END: incomplete pair + unknown error -> candidate undisposed
    store = DeepResearchRunLedgerStore(tmp_path / "L-E.sqlite3")
    archive = _archive()
    registry = _registry(archive)
    _admit_direct_source(archive, EXPECTED_SRC, raw=b"seeded")
    _make_run(store, ledger_id="L-E", run_id="RR-E", request_id="REQ-E")
    _patch_pair_state(monkeypatch, registry, ev_exists=True, ear_exists=False)
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(RuntimeError("UNEXPLAINED canonical failure")),
        raising=False,
    )
    cid = _cid("L-E", 0, "https://sec.gov/e")
    with pytest.raises(RuntimeError):
        process_discovered_sources(
            store, ledger_id="L-E", references=[_ptr(0, "https://sec.gov/e")],
            discovery_timestamp=DISCOVERED_AT, archive=archive,
            verifier=_StubVerifier({cid: _verified(EXPECTED_SRC, raw=b"seeded")}),
            registry=registry, evidence_builder=_evidence_builder(ledger_id="L-E"),
        )
    assert _dispositions(store, "L-E") == {}
    assert pending_candidates(store.load_run("L-E")) == (cid,)


def test_53_F_read_back_failure_under_a_recognized_exception_fails_closed(tmp_path, monkeypatch):
    """Case F — a read-back failure under an OTHERWISE recognized exception fails closed."""
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)

    # (a) DIRECT: recognized IntegrityConflict, but the authoritative load fails
    with pytest.raises(KeyError):
        classify_evidence_admission_failure(
            _LoadBombRegistry(KeyError("INJECTED authoritative load failure")),
            error=IntegrityConflict("INJECTED collision"),
            evidence=expected_ev, admission=expected_ear, verified_source_id=EXPECTED_SRC,
        )

    # (b) END-TO-END: recognized collision + a read-back that raises -> fail closed
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    monkeypatch.setattr(
        registry, "admit_evidence",
        lambda e, a: (_ for _ in ()).throw(IntegrityConflict("INJECTED collision")),
        raising=False,
    )
    monkeypatch.setattr(
        registry, "contains",
        lambda schema_id, record_id: (_ for _ in ()).throw(OSError("INJECTED read-back failure")),
        raising=False,
    )
    with pytest.raises(OSError):
        _rerun(store, registry, archive, verifier, refs)
    assert _dispositions(store, "L-1") == {}
    assert pending_candidates(store.load_run("L-1")) == (cid,)
    assert len(registry._data["EV-01"]) == 1     # canonical state untouched, no fabricated lineage


def test_54_the_governance_guard_takes_precedence_over_the_entry_allowlist(tmp_path):
    """Probe-11 test-strength gap: weakening the SourceBridgeError guard IS now detected.

    A governance failure must never reconcile — even when its type is ALSO a recognized
    collision class. Removing the guard would let reconciliation run and settle the candidate.
    """
    from qad.m6 import source_bridge as sb

    # the entry allowlist is exactly the two recognized collision classes
    assert sb._RECONCILABLE_ENTRY_FAILURES == (IntegrityConflict, TransactionFailure)
    # ...and the transient allowlist was NOT broadened
    assert sb._RETRYABLE_OPERATIONAL_FAILURES == (TransactionFailure,)

    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(
        tmp_path, ledger_id="L-G", reference="https://sec.gov/g"
    )
    before = _canonical_hashes(registry)

    # (a) DIRECT: a governance failure that is ALSO collision-shaped -> propagate, no read-back
    governance = _GovernanceCollision("builder governance failure")
    assert isinstance(governance, SourceBridgeError)
    assert isinstance(governance, IntegrityConflict)
    spy = _ReadBackSpy()
    with pytest.raises(SourceBridgeError) as excinfo:
        classify_evidence_admission_failure(
            spy, error=governance, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID),
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is governance
    assert spy.calls == 0

    # (b) END-TO-END: the builder raises a governance failure -> undisposed, nothing reconciled
    def _governance_builder(candidate_id, src01_id, verification):
        raise _GovernanceCollision("builder governance failure")

    with pytest.raises(SourceBridgeError):
        process_discovered_sources(
            store, ledger_id="L-G", references=refs, discovery_timestamp=DISCOVERED_AT,
            archive=archive, verifier=verifier, registry=registry,
            evidence_builder=_governance_builder,
        )
    assert _dispositions(store, "L-G") == {}
    assert pending_candidates(store.load_run("L-G")) == (cid,)
    assert _canonical_hashes(registry) == before


# ============================================================================
# 55-61 round-16 closure — RECONCILIATION-ENTRY CONTRACT CLOSED BY EXACT TYPE
#
# Founder ruling (12 Oct 2026): the entry allowlist is EXACTLY (IntegrityConflict,
# TransactionFailure) matched with `type(error) not in _RECONCILABLE_ENTRY_FAILURES`. A SUBCLASS is
# NOT implicitly authorized. Founder-mandated cases: A (test_55) · B (test_56) · C (test_57) ·
# D (test_58) · E (test_59) · F (test_60) · G (test_61) · H/I/J mutation demonstrations
# (evidence/m6.6/RED-DEMO-ROUND16-2026-10-12.txt).
#
# Each fail-closed case below proves a COMPLETE candidate lifecycle: the unauthorized failure
# settles nothing, and the SAME candidate is still recoverable afterwards (the recovery run then
# reconciles the identical pair through the exact allowlist) — not just a predicate assertion.
# ============================================================================


class _UnlistedIntegritySubclass(IntegrityConflict):
    """An UNLISTED subclass of an allowlisted class - not implicitly authorized (case C)."""


class _UnlistedTransactionSubclass(TransactionFailure):
    """An UNLISTED subclass of the other allowlisted class (case D)."""


class _GovernanceAndCollision(SourceBridgeError, IntegrityConflict):
    """Multiple inheritance: a governance failure that is ALSO collision-shaped (case F)."""


class _GovernanceOnly(SourceBridgeError):
    """A pure governance failure (case F companion)."""


def _fail_closed_lifecycle(tmp_path, *, ledger_id, reference, exc_factory, exc_type):
    """Complete lifecycle proof for one unauthorized failure class."""
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(
        tmp_path, ledger_id=ledger_id, reference=reference
    )
    before = _canonical_hashes(registry)
    real_admit = registry.admit_evidence
    registry.admit_evidence = lambda e, a: (_ for _ in ()).throw(exc_factory())
    with pytest.raises(exc_type):
        _rerun(store, registry, archive, verifier, refs, ledger_id=ledger_id)
    # nothing settled, no lineage, canonical state untouched, candidate still pending
    assert _dispositions(store, ledger_id) == {}
    assert pending_candidates(store.load_run(ledger_id)) == (cid,)
    assert _canonical_hashes(registry) == before
    # LIFECYCLE COMPLETES: with the registry behaving normally again, the SAME candidate
    # reconciles the identical pair through the EXACT allowlist
    registry.admit_evidence = real_admit
    out = _rerun(store, registry, archive, verifier, refs, ledger_id=ledger_id)
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
    assert pending_candidates(store.load_run(ledger_id)) == ()
    assert len(registry._data["EV-01"]) == 1 and len(registry._data["EAR-01"]) == 1


def test_55_A_exact_integrity_conflict_reconciles_full_lifecycle(tmp_path):
    """Case A — EXACT IntegrityConflict + exact pre-existing pair -> legitimate reconciliation."""
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)
    # (a) DIRECT classifier against a committed, exactly-matching canonical pair
    decision = classify_evidence_admission_failure(
        _seeded_registry(seed_ev=expected_ev, seed_ear=expected_ear),
        error=IntegrityConflict("EV-01/EV-A: evidence already admitted"),
        evidence=expected_ev, admission=expected_ear, verified_source_id=EXPECTED_SRC,
    )
    assert decision.classification is EvidenceAdmissionClassification.RECONCILED_IDENTICAL
    assert decision.settled is True
    assert (decision.evidence_id, decision.ear_id) == (EXPECTED_EV_ID, EXPECTED_EAR_ID)
    # (b) COMPLETE LIFECYCLE end-to-end (the registry's own natural collision, no injection)
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    out = _rerun(store, registry, archive, verifier, refs)
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
    assert o.evidence_admission_error is None
    assert pending_candidates(store.load_run("L-1")) == ()
    assert _dispositions(store, "L-1")[cid].evidence_ids == (EXPECTED_EV_ID,)


def test_56_B_exact_transaction_failure_reconciles_full_lifecycle(tmp_path):
    """Case B — EXACT TransactionFailure + exact pre-existing pair -> legitimate reconciliation."""
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(tmp_path)
    real_admit = registry.admit_evidence
    registry.admit_evidence = lambda e, a: (_ for _ in ()).throw(
        TransactionFailure("INJECTED batch failure")
    )
    out = _rerun(store, registry, archive, verifier, refs)
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)
    assert pending_candidates(store.load_run("L-1")) == ()
    assert len(registry._data["EV-01"]) == 1 and len(registry._data["EAR-01"]) == 1
    registry.admit_evidence = real_admit


def test_57_C_unlisted_integrity_subclass_fails_closed_full_lifecycle(tmp_path):
    """Case C — UNLISTED subclass of IntegrityConflict: zero read-back, nothing settled."""
    # (a) DIRECT classifier: propagates unchanged AND attempts no read-back at all
    spy = _ReadBackSpy()
    raised = _UnlistedIntegritySubclass("UNLISTED subclass collision")
    with pytest.raises(_UnlistedIntegritySubclass) as excinfo:
        classify_evidence_admission_failure(
            spy, error=raised, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is raised
    assert spy.calls == 0
    # (b) COMPLETE LIFECYCLE end-to-end
    _fail_closed_lifecycle(
        tmp_path, ledger_id="L-C", reference="https://sec.gov/c",
        exc_factory=lambda: _UnlistedIntegritySubclass("UNLISTED subclass collision"),
        exc_type=_UnlistedIntegritySubclass,
    )


def test_58_D_unlisted_transaction_subclass_fails_closed_full_lifecycle(tmp_path):
    """Case D — UNLISTED subclass of TransactionFailure: zero read-back, nothing settled."""
    spy = _ReadBackSpy()
    raised = _UnlistedTransactionSubclass("UNLISTED subclass batch failure")
    with pytest.raises(_UnlistedTransactionSubclass) as excinfo:
        classify_evidence_admission_failure(
            spy, error=raised, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is raised
    assert spy.calls == 0
    _fail_closed_lifecycle(
        tmp_path, ledger_id="L-D", reference="https://sec.gov/d",
        exc_factory=lambda: _UnlistedTransactionSubclass("UNLISTED subclass batch failure"),
        exc_type=_UnlistedTransactionSubclass,
    )


def test_59_E_an_unlisted_plain_class_fails_closed_full_lifecycle(tmp_path):
    """Case E — NotImplementedError (neither allowlisted nor a subclass): nothing settled."""
    spy = _ReadBackSpy()
    raised = NotImplementedError("UNLISTED plain failure class")
    with pytest.raises(NotImplementedError) as excinfo:
        classify_evidence_admission_failure(
            spy, error=raised, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is raised
    assert spy.calls == 0
    _fail_closed_lifecycle(
        tmp_path, ledger_id="L-E2", reference="https://sec.gov/e2",
        exc_factory=lambda: NotImplementedError("UNLISTED plain failure class"),
        exc_type=NotImplementedError,
    )


def test_60_F_governance_precedence_survives_multiple_inheritance(tmp_path):
    """Case F — a class inheriting BOTH SourceBridgeError and IntegrityConflict fails closed."""
    spy = _ReadBackSpy()
    raised = _GovernanceAndCollision("governance failure with collision shape")
    assert isinstance(raised, SourceBridgeError) and isinstance(raised, IntegrityConflict)
    assert type(raised) not in (IntegrityConflict, TransactionFailure)   # not an exact member
    with pytest.raises(SourceBridgeError) as excinfo:
        classify_evidence_admission_failure(
            spy, error=raised, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is raised
    assert spy.calls == 0
    _fail_closed_lifecycle(
        tmp_path, ledger_id="L-F", reference="https://sec.gov/f",
        exc_factory=lambda: _GovernanceAndCollision("governance failure with collision shape"),
        exc_type=SourceBridgeError,
    )
    # companion: a PURE governance failure also fails closed
    pure = _GovernanceOnly("pure governance failure")
    with pytest.raises(SourceBridgeError) as excinfo2:
        classify_evidence_admission_failure(
            _ReadBackSpy(), error=pure, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo2.value is pure


def test_61_G_the_entry_allowlist_composition_is_closed_and_exact():
    """Case G — the allowlist contains EXACTLY the two Founder-approved classes and no third."""
    from qad.m6 import source_bridge as sb

    allow = sb._RECONCILABLE_ENTRY_FAILURES
    assert isinstance(allow, tuple)
    assert allow == (IntegrityConflict, TransactionFailure)      # exact members and order
    assert len(allow) == 2                                        # no third class
    assert set(allow) == {IntegrityConflict, TransactionFailure}   # no duplicates/extras
    assert all(isinstance(cls, type) for cls in allow)
    # every non-member class is excluded, including subclasses of the members
    for excluded in (SourceBridgeError, _UnlistedIntegritySubclass, _UnlistedTransactionSubclass,
                     NotImplementedError, RuntimeError, CanonicalBoundaryViolation,
                     MissingForeignKey, PITBlockError):
        assert excluded not in allow
    # ...and the transient-partial allowlist was NOT broadened
    assert sb._RETRYABLE_OPERATIONAL_FAILURES == (TransactionFailure,)


# ============================================================================
# 62 round-17 closure — IDENTITY, NOT EQUALITY (Round-16 material finding reproduced)
#
# The Round-16 finding: `type(error) not in _RECONCILABLE_ENTRY_FAILURES` is an EQUALITY test, so a
# class whose METACLASS defines `__eq__` to compare equal to `IntegrityConflict` passed the previous
# predicate, entered the authoritative read-back, and settled a lineage-claiming success.
# The predicate is now identity-based: any(type(error) is allowed for allowed in ...).
#
# Positive controls retained unchanged elsewhere in this file: exact IntegrityConflict reconciles
# (test_55), exact TransactionFailure reconciles (test_56), ordinary subclasses stay rejected
# (test_57/test_58), NotImplementedError stays rejected (test_59), the SourceBridgeError guard keeps
# precedence (test_54/test_60), the composition is exactly the two classes (test_61).
# ============================================================================


class _EqualitySpoofMeta(type):
    """TEST-ONLY metaclass whose classes compare EQUAL to `IntegrityConflict`.

    This reproduces the Round-16 finding exactly: tuple membership (`in`) is an equality test, so a
    class built with this metaclass satisfied the PREVIOUS predicate even though it is not the actual
    `IntegrityConflict` class object.
    """

    def __eq__(cls, other):
        return other is IntegrityConflict

    def __hash__(cls):  # keep the metaclass hashable like `type`
        return type.__hash__(cls)


class _EqualitySpoofSubclass(IntegrityConflict, metaclass=_EqualitySpoofMeta):
    """An unlisted subclass that is EQUALITY-compatible with IntegrityConflict but NOT identical."""


def test_62_identity_predicate_rejects_an_equality_compatible_class(tmp_path):
    """Round-17 regression: an equality-spoofing class can never enter reconciliation."""
    from qad.m6 import source_bridge as sb

    spoof = _EqualitySpoofSubclass("SPOOFED metaclass-equality collision")

    # (1) identity is FALSE
    assert (type(spoof) is IntegrityConflict) is False
    # (2) equality-based membership (the PREVIOUS predicate) would have admitted it
    assert (type(spoof) in sb._RECONCILABLE_ENTRY_FAILURES) is True
    # (3) the NEW identity-based predicate rejects it
    assert any(
        type(spoof) is allowed for allowed in sb._RECONCILABLE_ENTRY_FAILURES
    ) is False
    assert isinstance(spoof, IntegrityConflict) is True     # ...even though isinstance would also

    # (4)+(5) DIRECT classifier: the ORIGINAL exception propagates unchanged, with ZERO read-back
    expected_ev = _mk_ev(EXPECTED_EV_ID, EXPECTED_SRC)
    expected_ear = _mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID)
    spy = _ReadBackSpy()
    with pytest.raises(_EqualitySpoofSubclass) as excinfo:
        classify_evidence_admission_failure(
            spy, error=spoof, evidence=expected_ev, admission=expected_ear,
            verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is spoof                              # (4) same object
    assert spy.calls == 0                                      # (5) no authoritative read-back

    # (6)-(9) END-TO-END: nothing is settled, no lineage, canonical state untouched
    store, archive, registry, cid, verifier, refs = _pending_candidate_with_exact_pair(
        tmp_path, ledger_id="L-SPOOF", reference="https://sec.gov/spoof"
    )
    before = _canonical_hashes(registry)
    real_admit = registry.admit_evidence
    registry.admit_evidence = lambda e, a: (_ for _ in ()).throw(
        _EqualitySpoofSubclass("SPOOFED metaclass-equality collision")
    )
    with pytest.raises(_EqualitySpoofSubclass):
        _rerun(store, registry, archive, verifier, refs, ledger_id="L-SPOOF")
    assert _dispositions(store, "L-SPOOF") == {}               # (6) ZERO dispositions
    assert pending_candidates(store.load_run("L-SPOOF")) == (cid,)  # (7) still pending
    assert _canonical_hashes(registry) == before               # (8) hashes unchanged
    assert len(registry._data["EV-01"]) == 1 and len(registry._data["EAR-01"]) == 1

    # (10) the SAME candidate recovers legitimately with the ACTUAL approved exception type
    registry.admit_evidence = real_admit
    out = _rerun(store, registry, archive, verifier, refs, ledger_id="L-SPOOF")
    o = out.outcomes[0]
    assert o.disposition.value == "IMPORTED"                   # (9) no lineage was claimed before...
    assert o.evidence_ids == (EXPECTED_EV_ID,) and o.ear_ids == (EXPECTED_EAR_ID,)  # (10) now it is
    assert pending_candidates(store.load_run("L-SPOOF")) == ()
    assert len(store.load_run("L-SPOOF").dispositions) == 1
    assert len(registry._data["EV-01"]) == 1 and len(registry._data["EAR-01"]) == 1


def test_63_a_dynamically_created_same_name_class_cannot_enter_reconciliation():
    """Round-17 regression: a same-NAME class forged at runtime is not the allowed class object."""
    forged = type("IntegrityConflict", (Exception,), {})
    assert forged.__name__ == "IntegrityConflict"
    assert forged is not IntegrityConflict
    spoof = forged("forged same-name collision")

    spy = _ReadBackSpy()
    with pytest.raises(Exception) as excinfo:
        classify_evidence_admission_failure(
            spy, error=spoof, evidence=_mk_ev(EXPECTED_EV_ID, EXPECTED_SRC),
            admission=_mk_ear(EXPECTED_EV_ID, EXPECTED_EAR_ID), verified_source_id=EXPECTED_SRC,
        )
    assert excinfo.value is spoof
    assert spy.calls == 0
