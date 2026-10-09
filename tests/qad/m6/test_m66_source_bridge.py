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
    DiscoveredSourceReference,
    OriginalSourceVerification,
    SourceBridgeError,
    SourceFailureKind,
    SourceVerificationCandidate,
    build_evidence_admission,
    coerce_discovered_reference,
    compute_source_candidate_id,
    pending_candidates,
    process_discovered_sources,
    register_discovered_candidates,
    verify_and_admit_source,
)
from qad.models.family_b import (
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
)
from qad.persistence.reference import (
    InMemoryEvidenceRegistry,
    InMemoryRawSourceArchive,
)

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


def _evidence_builder(*, evidence_id="EV-A", admission_id="EAR-A",
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
            admission_timestamp=DISCOVERED_AT, admitting_role="Research Director",
            admission_method=method,
            validation_method="ORIGINAL_DOCUMENT_BYTE_COMPARISON",
        )
        return ev, ear

    return _build


def _per_candidate_builder(mapping):
    def _build(candidate_id, src01_id, verification):
        spec = mapping[candidate_id]
        ev = _ev(spec["ev"], src01_id, contradicts=spec.get("contradicts"))
        ear = build_evidence_admission(
            evidence=ev, verification=verification, admission_id=spec["ear"],
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
    # and it can authorize canonical evidence ONLY for its own source
    assert verdict.authorizes_evidence_for(source_id="SRC-A") is True
    assert verdict.authorizes_evidence_for(source_id="SRC-B") is False


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
