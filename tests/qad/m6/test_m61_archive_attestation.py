"""M6.1 — Archive Admission Attestation — acceptance tests (FD #150 design / FD #151 authorization).

RED→GREEN acceptance suite for the M6.1 cluster. Proves that
``RawSourceArchive.admit_source`` atomically creates an archive-owned,
caller-non-overridable, immutable ``ArchiveAdmissionAttestation`` bound to the
canonical SRC-01 identity + ``content_hash`` + exact raw-blob SHA-256, and that
the trusted SEALED capture rule (FD #150) blocks a caller-backdated
``retrieval_date``.

Run:  pytest tests/qad/m6/test_m61_archive_attestation.py -q
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib

import pytest

from qad.models.family_b import (
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
    SourceVersion,
)
from qad.persistence.attestation import (
    ArchiveAdmissionAttestation,
    ATTESTATION_FORMAT_VERSION,
    utc_now,
)
from qad.persistence.errors import AttestationNotFound
from qad.persistence.reference import InMemoryRawSourceArchive
from qad.m6.eligibility import (
    SealedEligibility,
    SRCV_ONLY_CAPTURE_PROOF_INELIGIBLE,
    evaluate_sealed_source_eligibility,
)


# =====================================================================
# Helpers
# =====================================================================

def _src(sid: str, raw: bytes, retrieval_date: str = "2025-12-01") -> SourceRecord:
    ch = hashlib.sha256(raw).hexdigest()
    return SourceRecord(
        source_id=sid,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/{sid}",
        content_hash=ch,
        retrieval_date=retrieval_date,
    )


def _archive(*, admitted_at_iso: str | None = None) -> InMemoryRawSourceArchive:
    """Archive with an injected archive-owned test clock (production callers cannot inject)."""
    if admitted_at_iso is None:
        return InMemoryRawSourceArchive()
    fixed = dt.datetime.fromisoformat(admitted_at_iso)
    return InMemoryRawSourceArchive(clock=lambda: fixed)


# =====================================================================
# 1–5: attestation creation + binding + archive-owned time + override refusal
# =====================================================================

class TestAttestationCreationAndBinding:
    def test_attestation_created_atomically_with_admission(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"m61 content"
        src = _src("M61-A", raw)
        store.admit_source(src, raw)
        att = store.get_admission_attestation("M61-A")
        assert isinstance(att, ArchiveAdmissionAttestation)
        assert store.verify_admission_attestation("M61-A") is True

    def test_attestation_binds_source_hash_bytes_length(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"bind me"
        src = _src("M61-B", raw)
        store.admit_source(src, raw)
        att = store.get_admission_attestation("M61-B")
        assert att.source_id == "M61-B"
        assert att.source_content_hash == src.content_hash
        assert att.raw_blob_sha256 == hashlib.sha256(raw).hexdigest()
        assert att.raw_blob_sha256 == src.content_hash          # FD #150 condition H
        assert att.raw_byte_length == len(raw)
        assert att.attestation_format_version == ATTESTATION_FORMAT_VERSION

    def test_admitted_at_is_archive_owned_utc(self):
        store = _archive(admitted_at_iso="2025-12-15T12:30:00+00:00")
        raw = b"clock"
        store.admit_source(_src("M61-C", raw), raw)
        att = store.get_admission_attestation("M61-C")
        assert att.admitted_at == "2025-12-15T12:30:00+00:00"
        parsed = dt.datetime.fromisoformat(att.admitted_at)
        assert parsed.tzinfo is not None
        assert parsed.utcoffset() == dt.timedelta(0)

    def test_caller_cannot_supply_admitted_at(self):
        store = _archive()
        raw = b"nope"
        src = _src("M61-D", raw)
        with pytest.raises(TypeError):
            # no admit_source parameter can carry an archive timestamp
            store.admit_source(src, raw, admitted_at="2020-01-01T00:00:00+00:00")  # type: ignore[call-arg]
        assert store.get_admission_attestation.__doc__ is not None

    def test_verification_rejects_swapped_source_identity(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"identical bytes"
        store.admit_source(_src("M61-S1", raw), raw)
        store.admit_source(_src("M61-S2", raw), raw)   # same bytes, other source
        # replay S1's attestation against S2 (same hash + length would pass a
        # hash-only binding check) — identity binding must reject it
        store._attestations["M61-S2"] = store._attestations["M61-S1"]
        assert store.verify_admission_attestation("M61-S2") is False

    def test_attestation_is_immutable(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"immutable"
        store.admit_source(_src("M61-E", raw), raw)
        att = store.get_admission_attestation("M61-E")
        with pytest.raises(dataclasses.FrozenInstanceError):
            att.admitted_at = "1999-01-01T00:00:00+00:00"  # type: ignore[misc]


# =====================================================================
# 6–8: no attestation without admission; rollback; integrity verification
# =====================================================================

class TestAttestationAbsenceAndRollback:
    def test_no_attestation_before_admission(self):
        store = _archive()
        with pytest.raises(AttestationNotFound):
            store.get_admission_attestation("NEVER-ADMITTED")

    def test_failed_admission_leaves_no_attested_state(self):
        store = _archive()
        raw = b"bad"
        src = _src("M61-F", raw).model_copy(update={"content_hash": "wrong"})
        from qad.persistence.errors import HashMismatch
        with pytest.raises(HashMismatch):
            store.admit_source(src, raw)
        # atomic rollback: no source, no blob, no attestation
        assert not store.contains("SRC-01", "M61-F")
        with pytest.raises(KeyError):
            store.load_raw_blob("M61-F")
        with pytest.raises(AttestationNotFound):
            store.get_admission_attestation("M61-F")

    def test_rollback_after_partial_write(self, monkeypatch):
        """Failure AFTER SRC-01 + bytes are written must roll all three back.

        The archive clock is consulted after the bytes are stored (step 3c), so a
        clock failure is a genuine mid-admission failure past the first writes.
        """
        store = InMemoryRawSourceArchive()

        def _boom():
            raise RuntimeError("archive clock failure after bytes written")

        monkeypatch.setattr(store, "_clock", _boom)
        raw = b"partial write"
        with pytest.raises(RuntimeError):
            store.admit_source(_src("M61-RB", raw), raw)
        assert not store.contains("SRC-01", "M61-RB")
        with pytest.raises(KeyError):
            store.load_raw_blob("M61-RB")
        with pytest.raises(AttestationNotFound):
            store.get_admission_attestation("M61-RB")

    def test_verification_detects_tampered_blob(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"tamper target"
        store.admit_source(_src("M61-G", raw), raw)
        # simulate storage corruption (white-box, reference adapter only)
        store._raw_blobs["M61-G"] = b"different bytes"
        assert store.verify_admission_attestation("M61-G") is False

    def test_idempotent_readmission_preserves_attestation(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"idempotent"
        src = _src("M61-H", raw)
        store.admit_source(src, raw)
        att1 = store.get_admission_attestation("M61-H")
        store.admit_source(src, raw)  # identical re-admission
        att2 = store.get_admission_attestation("M61-H")
        assert att1.attestation_id == att2.attestation_id
        assert att1.admitted_at == att2.admitted_at


# =====================================================================
# 8b: public/archive boundary (M6.1 review R2)
# =====================================================================

class TestPublicBoundary:
    def test_low_level_verifier_is_not_public(self):
        import qad.persistence as P
        assert not hasattr(P, "verify_attestation_binding")
        assert "verify_attestation_binding" not in getattr(P, "__all__", [])

    def test_detached_attestation_is_not_archive_proof(self):
        store = _archive()
        detached = ArchiveAdmissionAttestation(
            attestation_id="forged", source_id="X", source_ref="SRC-01:X",
            source_content_hash="a" * 64, raw_blob_sha256="a" * 64,
            raw_byte_length=1, admitted_at="1999-01-01T00:00:00+00:00",
            archive_instance="CallerMade", admission_method="ADMIT_SOURCE",
        )
        assert detached.source_id == "X"  # constructible, but carries no authority
        with pytest.raises(AttestationNotFound):
            store.get_admission_attestation("X")
        with pytest.raises(AttestationNotFound):
            store.verify_admission_attestation("X")


# =====================================================================
# 9–13: SEALED eligibility — the mandatory combined backdating fixture
# =====================================================================

class TestSealedEligibility:
    def test_MANDATORY_combined_backdating_fixture(self):
        """FD #151 §5 mandatory fixture.

        AS_OF 2026-01-01; caller retrieval_date 2025-12-01; archive admission
        (admitted_at) 2026-02-01 → SEALED BLOCKED despite retrieval_date < AS_OF.
        """
        store = _archive(admitted_at_iso="2026-02-01T00:00:00+00:00")
        raw = b"backdated"
        store.admit_source(_src("M61-BACK", raw, retrieval_date="2025-12-01"), raw)

        att = store.get_admission_attestation("M61-BACK")
        assert att.admitted_at == "2026-02-01T00:00:00+00:00"

        verdict = evaluate_sealed_source_eligibility(store, "M61-BACK", dt.date(2026, 1, 1))
        assert verdict is SealedEligibility.UNAVAILABLE_FOR_SEALED_PIT
        # explicitly: caller backdating cannot create historical eligibility
        assert dt.date.fromisoformat("2025-12-01") < dt.date(2026, 1, 1)

    def test_eligible_when_admitted_before_as_of(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"pre-asof"
        store.admit_source(_src("M61-OK", raw), raw)
        assert evaluate_sealed_source_eligibility(store, "M61-OK", dt.date(2026, 1, 1)) \
            is SealedEligibility.ELIGIBLE

    def test_blocked_when_admitted_after_as_of(self):
        store = _archive(admitted_at_iso="2026-03-01T00:00:00+00:00")
        raw = b"post-asof"
        store.admit_source(_src("M61-LATE", raw), raw)
        assert evaluate_sealed_source_eligibility(store, "M61-LATE", dt.date(2026, 1, 1)) \
            is SealedEligibility.UNAVAILABLE_FOR_SEALED_PIT

    def test_legacy_unattested_src01_blocked(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"legacy"
        store.admit_source(_src("M61-LEGACY", raw), raw)
        # simulate a pre-attestation legacy record (white-box, reference adapter only)
        store._attestations.pop("M61-LEGACY")
        assert evaluate_sealed_source_eligibility(store, "M61-LEGACY", dt.date(2026, 1, 1)) \
            is SealedEligibility.LEGACY_UNATTESTED_SRC01

    def test_srcv_only_capture_proof_ineligible(self):
        assert SRCV_ONLY_CAPTURE_PROOF_INELIGIBLE is True
        store = _archive()
        assert evaluate_sealed_source_eligibility(store, "MISSING", dt.date(2026, 1, 1)) \
            is SealedEligibility.SOURCE_NOT_FOUND

    def test_srcv_only_capture_proof_yields_srcv_verdict(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"srcv only"
        store.admit_source(_src("M61-SRCV", raw), raw)
        sv = SourceVersion(
            version_id="M61-SRCV-V1", source_id="M61-SRCV", version_number="1",
            retrieval_date="2025-12-01", content_hash=hashlib.sha256(raw).hexdigest(),
        )
        store.store(sv)                                    # SRCV-01 evidence
        store._attestations.pop("M61-SRCV")                # no archive attestation
        assert evaluate_sealed_source_eligibility(store, "M61-SRCV", dt.date(2026, 1, 1)) \
            is SealedEligibility.SRCV_ONLY_CAPTURE_PROOF

    def test_archive_version_snapshot_is_not_srcv_evidence(self):
        """M6.1 review R2: store_version()/list_versions() are SRC-01 snapshots,
        NOT SRCV-01 records — such a source is LEGACY_UNATTESTED, not SRCV-only."""
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"snapshot only"
        src = _src("M61-SNAP", raw)
        store.admit_source(src, raw)
        store.store_version(src, "v0001")            # archive version snapshot
        assert store.list_versions("M61-SNAP")       # labels exist...
        store._attestations.pop("M61-SNAP")
        assert evaluate_sealed_source_eligibility(store, "M61-SNAP", dt.date(2026, 1, 1)) \
            is SealedEligibility.LEGACY_UNATTESTED_SRC01

    def test_verification_failure_blocks_sealed(self):
        store = _archive(admitted_at_iso="2025-12-15T00:00:00+00:00")
        raw = b"integrity"
        store.admit_source(_src("M61-INT", raw), raw)
        store._raw_blobs["M61-INT"] = b"corrupted"
        assert evaluate_sealed_source_eligibility(store, "M61-INT", dt.date(2026, 1, 1)) \
            is SealedEligibility.UNAVAILABLE_FOR_SEALED_PIT
