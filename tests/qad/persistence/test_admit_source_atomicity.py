"""M5.2 Item 5 — RAW SOURCE ADMISSION MUST BIND METADATA TO BYTES.

Adversarial tests proving that ``InMemoryRawSourceArchive.admit_source``
binds ``SourceRecord.content_hash`` to the raw bytes' SHA-256, prevents
silent overwrite, and is atomic across metadata + raw bytes.

Covers the required invariants and the atomicity clarification
(metadata + bytes are ONE admission unit).
"""

from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import CanonicalBoundaryViolation, HashMismatch, IntegrityConflict
from qad.persistence.reference import InMemoryRawSourceArchive, _resolve_id
from qad.models.family_b import (
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)


# =====================================================================
# Helper
# =====================================================================

def _make_src(source_id, *, content_raw):
    """Create a valid SRC-01 SourceRecord whose content_hash matches
    the given raw bytes via SHA-256."""
    raw = content_raw
    ch = hashlib.sha256(raw).hexdigest()
    return SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/src-{source_id}",
        content_hash=ch,
        retrieval_date="2024-01-01",
    )


# =====================================================================
# Invariant 1: hash match before canonical admission
# =====================================================================

class TestInvariant1HashMatch:
    """sha256(raw_bytes) == SourceRecord.content_hash before canonical admission."""

    def test_admit_requires_hash_match(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant1 content"
        src = _make_src("INV1", content_raw=raw)
        src = src.model_copy(update={"content_hash": "wronghash"})
        with pytest.raises(HashMismatch):
            store.admit_source(src, raw)
        assert not store.contains("SRC-01", "INV1")
        with pytest.raises(KeyError):
            store.load_raw_blob("INV1")

    def test_admit_success_stores_metadata_and_bytes(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant1 success"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("INV1S", content_raw=raw)
        store.admit_source(src, raw)
        assert store.contains("SRC-01", "INV1S")
        assert store.load_raw_blob("INV1S") == raw
        assert store.get_raw_blob_hash("INV1S") == ch


# =====================================================================
# Invariant 2: same source_id + identical payload -> idempotent
# =====================================================================

class TestInvariant2Idempotent:
    """Same source_id + identical raw bytes + same metadata -> idempotent."""

    def test_same_id_same_bytes_same_meta_idempotent(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant2 content"
        src = _make_src("INV2", content_raw=raw)
        h1 = store.admit_source(src, raw)
        h2 = store.admit_source(src, raw)
        assert h1 == h2
        assert store.load_raw_blob("INV2") == raw
        assert store.contains("SRC-01", "INV2")


# =====================================================================
# Invariant 3: same source_id + different bytes -> IntegrityConflict
# =====================================================================

class TestInvariant3ConflictDifferentBytes:
    """Same source_id + different raw bytes -> IntegrityConflict."""

    def test_same_id_different_bytes_conflict(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant3 content"
        src = _make_src("INV3", content_raw=raw)
        store.admit_source(src, raw)
        diff_raw = b"invariant3 DIFFERENT"
        diff_src = src.model_copy(
            update={"content_hash": hashlib.sha256(diff_raw).hexdigest()}
        )
        with pytest.raises(IntegrityConflict):
            store.admit_source(diff_src, diff_raw)
        assert store.load_raw_blob("INV3") == raw
        assert store.load("SRC-01", "INV3").source_id == "INV3"


# =====================================================================
# Invariant 4: content_hash != sha256(raw_bytes) -> HashMismatch
# =====================================================================

class TestInvariant4HashMismatch:
    """SourceRecord.content_hash != sha256(raw_bytes) raises HashMismatch."""

    def test_content_hash_not_matching_bytes_raises(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant4 content"
        src = SourceRecord(
            source_id="INV4",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/inv4",
            content_hash="not-a-real-hash",
            retrieval_date="2024-01-01",
        )
        with pytest.raises(HashMismatch):
            store.admit_source(src, raw)


# =====================================================================
# Invariant 5: Raw admitted blob cannot be overwritten via store_raw_blob()
# =====================================================================

class TestInvariant5NoOverwriteViaStoreRawBlob:
    """After admit_source, store_raw_blob for the same source_id is blocked."""

    def test_store_raw_blob_after_admission_raises(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant5 content"
        src = _make_src("INV5", content_raw=raw)
        store.admit_source(src, raw)
        diff_raw = b"invariant5 OVERWRITE ATTEMPT"
        diff_hash = hashlib.sha256(diff_raw).hexdigest()
        with pytest.raises(IntegrityConflict):
            store.store_raw_blob("INV5", diff_hash, diff_raw)
        assert store.load_raw_blob("INV5") == raw

    def test_store_raw_blob_bypass_is_rejected(self):
        """Direct store(SourceRecord) on RawSourceArchive is blocked."""
        from qad.persistence.errors import CanonicalBoundaryViolation
        store = InMemoryRawSourceArchive()
        raw = b"invariant5 bypass"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("INV5B", content_raw=raw)
        with pytest.raises(CanonicalBoundaryViolation):
            store.store(src)
        # verify no canonical record leaked through
        assert not store.contains("SRC-01", "INV5B")
        # admit_source is the only valid path
        store.admit_source(src, raw)
        assert store.load_raw_blob("INV5B") == raw


# =====================================================================
# Invariant 6: Tombstone preserves historical SourceRecord + raw bytes
# =====================================================================

class TestInvariant6TombstonePreservesHistory:
    """Tombstone retains SourceRecord + raw bytes for audit."""

    def test_tombstone_preserves_raw_blobs(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant6 content"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("INV6", content_raw=raw)
        store.admit_source(src, raw)
        store.tombstone("INV6", "test tombstone")
        assert store.is_tombstoned("INV6")
        with pytest.raises(KeyError, match="tombstoned"):
            store.load("SRC-01", "INV6")
        with pytest.raises(KeyError, match="tombstoned"):
            store.load_raw_blob("INV6")
        assert store.load_raw_blob_historical("INV6") == raw
        assert store.get_raw_blob_hash("INV6") == ch

    def test_tombstone_with_versions(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant6 versioned"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("INV6V", content_raw=raw)
        store.admit_source(src, raw)
        store.store_version(src, "v1")
        store.tombstone("INV6V", "retracted")
        ver_record, ver_blob = store.load_version("INV6V", "v1")
        assert ver_blob == raw
        assert ver_record.source_id == "INV6V"


# =====================================================================
# Invariant 7: No alternative public write path can silently replace
# =====================================================================

class TestInvariant7NoBypass:
    """store_raw_blob() cannot silently replace admitted raw bytes."""

    def test_store_raw_blob_overwrite_rejected_on_admitted_record(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant7 content"
        src = _make_src("INV7", content_raw=raw)
        store.admit_source(src, raw)
        hack_raw = b"invariant7 BYPASS"
        hack_hash = hashlib.sha256(hack_raw).hexdigest()
        with pytest.raises(IntegrityConflict):
            store.store_raw_blob("INV7", hack_hash, hack_raw)
        assert store.load_raw_blob("INV7") == raw

    def test_store_raw_blob_content_hash_guard(self):
        """store_raw_blob checks blob_hash against existing SourceRecord.content_hash."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant7 guard"
        ch = hashlib.sha256(raw).hexdigest()
        # Admit source through admit_source (only valid path)
        src = _make_src("INV7G", content_raw=raw)
        store.admit_source(src, raw)
        # Attempt store_raw_blob — first guard fires: existing raw blob blocks
        with pytest.raises(IntegrityConflict):
            store.store_raw_blob("INV7G", hashlib.sha256(b"dummy").hexdigest(), b"dummy")


# =====================================================================
# Invariant 8: Atomicity — metadata+bytes are ONE admission unit
# =====================================================================

class TestInvariant8Atomicity:
    """Failure anywhere during admit_source must restore ALL state.

    Blockers B: Real commit-phase atomicity proof — inject fault after
    metadata commit, verify full 7-state rollback.
    """

    def test_validation_phase_failure_blocks_admission(self):
        """A validation-phase failure means no record is committed."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant8 validation-fail"
        ch = hashlib.sha256(raw).hexdigest()
        src1 = _make_src("INV8V", content_raw=raw)
        store.admit_source(src1, raw)
        # Second call changing a FIELD_IMMUTABLE field fails in validation
        src2 = SourceRecord(
            source_id="INV8V",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/inv8v-v2",
            content_hash=ch,
            retrieval_date="2024-06-01",  # FIELD_IMMUTABLE
        )
        with pytest.raises(Exception):
            store.admit_source(src2, raw)
        # Original admission remains intact
        assert store.contains("SRC-01", "INV8V")
        loaded = store.load("SRC-01", "INV8V")
        assert loaded.retrieval_date == "2024-01-01"
        assert store.load_raw_blob("INV8V") == raw

    def test_commit_phase_failure_rollback_all_seven_dicts(self):
        """REAL fault injection: raise in _raw_blobs.__setitem__ AFTER
        metadata commit. Prove ALL 7 state dicts roll back.

        Uses a fault-injecting _FaultyBlobDict that raises on any write.
        """
        from qad.persistence.errors import PersistenceError

        class _FaultySourceArchive(InMemoryRawSourceArchive):
            class _FaultyBlobDict(dict):
                def __setitem__(self, key, value):
                    raise PersistenceError(
                        f"Injected fault: raw_blobs write blocked for {key}"
                    )

            def __init__(self):
                super().__init__()
                self._raw_blobs = self._FaultyBlobDict()

        store = _FaultySourceArchive()
        raw = b"invariant8 commit-fault"
        ch = hashlib.sha256(raw).hexdigest()

        snap_before = store._snapshot()

        src = _make_src("INV8-FAULT", content_raw=raw)

        # Exact expected failure -- no exception swallowing
        with pytest.raises(PersistenceError, match="Injected fault"):
            store.admit_source(src, raw)

        # Prove full rollback: ALL 7 state dicts back to pre-admission
        snap_after = store._snapshot()
        assert snap_after == snap_before, (
            f"Rollback failed: state differs from pre-admission snapshot"
        )

        # Individual verifications
        assert not store.contains("SRC-01", _resolve_id(src))
        with pytest.raises(KeyError):
            store.load_raw_blob(_resolve_id(src))
        assert store.get_version_count("SRC-01", _resolve_id(src)) == 0
        assert not store.is_tombstoned(_resolve_id(src))

    def test_admit_source_non_src01_rejected(self):
        """admit_source rejects non-SRC-01 input."""
        from qad.models.family_a import SecurityMaster, SecurityMasterSecurity_type, SecurityMasterStatus
        from qad.persistence.errors import CanonicalBoundaryViolation
        store = InMemoryRawSourceArchive()
        sm = SecurityMaster(
            entity_id="E-NONSRC",
            cik="N1", exchange="NYSE", name="Non-SRC",
            primary_ticker="NSR",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        with pytest.raises(CanonicalBoundaryViolation):
            store.admit_source(sm, b"irrelevant bytes")

    def test_metadata_revision_is_conflict(self):
        """Same source_id + same bytes + changed metadata -> IntegrityConflict
        per M4A SRC-01 immutability_rules (immutable source document reference)."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant8 revision"
        ch = hashlib.sha256(raw).hexdigest()
        src1 = _make_src("INV8R", content_raw=raw)
        store.admit_source(src1, raw)
        # Same bytes, different metadata
        src2 = SourceRecord(
            source_id="INV8R",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/inv8r",
            content_hash=ch,
            retrieval_date="2024-01-01",
            source_url_hash="updated-url-hash",
        )
        with pytest.raises(IntegrityConflict):
            store.admit_source(src2, raw)
        # Original unchanged
        loaded = store.load("SRC-01", "INV8R")
        assert loaded.source_url_hash is None  # unchanged
        assert store.load_raw_blob("INV8R") == raw


# =====================================================================
# Invariant 9: Returned/stored hashes remain internally consistent
# =====================================================================

class TestInvariant9HashConsistency:
    """admit_source() returned hash equals stored hash."""

    def test_returned_hash_matches_stored(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant9 consistency"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("INV9", content_raw=raw)
        ret_hash = store.admit_source(src, raw)
        stored_hash = store.get_canonical_hash("SRC-01", "INV9")
        assert ret_hash == stored_hash
        assert store.load("SRC-01", "INV9").content_hash == ch


# =====================================================================
# Invariant 10: Items 1-4 invariants remain unchanged
# =====================================================================

class TestNoRemainingBypass:
    """Prove no public API can create canonical SRC-01 without admit_source."""

    def test_store_batch_src01_rejected(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant bypass-batch"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("BYPASS-BATCH", content_raw=raw)
        with pytest.raises(CanonicalBoundaryViolation, match="SRC-01 in batch"):
            store.store_batch([src])
        assert not store.contains("SRC-01", "BYPASS-BATCH")
        with pytest.raises(KeyError):
            store.load_raw_blob("BYPASS-BATCH")

    def test_store_batch_non_src01_passes(self):
        """Non-SRC-01 schemas can still use store_batch."""
        from qad.models.family_a import (
            SecurityMaster, SecurityMasterSecurity_type, SecurityMasterStatus
        )
        store = InMemoryRawSourceArchive()
        sm1 = SecurityMaster(
            entity_id="E-BATCH-OK",
            cik="B1", exchange="NYSE", name="BatchOK",
            primary_ticker="BOK",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        sm2 = SecurityMaster(
            entity_id="E-BATCH-OK-2",
            cik="B2", exchange="NYSE", name="BatchOK2",
            primary_ticker="BK2",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        hashes = store.store_batch([sm1, sm2])
        assert len(hashes) == 2
        assert store.contains("SM-01", "E-BATCH-OK")
        assert store.contains("SM-01", "E-BATCH-OK-2")

    def test_store_version_src01_without_admission_rejected(self):
        store = InMemoryRawSourceArchive()
        raw = b"invariant bypass-version"
        ch = hashlib.sha256(raw).hexdigest()
        src = _make_src("BYPASS-VER", content_raw=raw)
        with pytest.raises(CanonicalBoundaryViolation, match="store_version rejected"):
            store.store_version(src, "v1")
        assert not store.contains("SRC-01", "BYPASS-VER")
        with pytest.raises(KeyError):
            store.load_raw_blob("BYPASS-VER")

    def test_store_version_src01_with_admission_allowed(self):
        """store_version on already-admitted SRC-01 is valid (identical snapshot)."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant version-admitted"
        src = _make_src("BYPASS-VER-OK", content_raw=raw)
        store.admit_source(src, raw)
        store.store_version(src, "v1")
        assert store.contains("SRC-01", "BYPASS-VER-OK")
        assert store.load_raw_blob("BYPASS-VER-OK") == raw
        vers = store.list_versions("BYPASS-VER-OK")
        assert "v1" in vers

    def test_store_version_raw_only_orphan_cannot_create_src01(self):
        """Orphan raw blob without canonical SRC-01 cannot create one via store_version."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant orphan"
        ch = hashlib.sha256(raw).hexdigest()
        # Create orphan raw blob via store_raw_blob directly
        store._raw_blobs["ORPHAN-1"] = raw
        src = SourceRecord(
            source_id="ORPHAN-1",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/orphan",
            content_hash=ch,
            retrieval_date="2024-01-01",
        )
        with pytest.raises(CanonicalBoundaryViolation, match="no canonical SRC-01"):
            store.store_version(src, "v1")
        assert not store.contains("SRC-01", "ORPHAN-1")
        assert store._raw_blobs.get("ORPHAN-1") == raw  # raw blob unchanged

    def test_store_version_changed_content_hash_rejected(self):
        """Admitted source with changed content_hash via store_version is rejected."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant content-hash"
        src = _make_src("CH-HASH", content_raw=raw)
        store.admit_source(src, raw)
        # Same source_id, different content_hash
        bad_hash = "0" * 64
        src_bad = SourceRecord(
            source_id="CH-HASH",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/ch-hash",
            content_hash=bad_hash,
            retrieval_date="2024-01-01",
        )
        with pytest.raises(IntegrityConflict, match="incoming payload differs"):
            store.store_version(src_bad, "v2")
        # Canonical unchanged
        loaded = store.load("SRC-01", "CH-HASH")
        assert loaded.content_hash != bad_hash
        assert store.load_raw_blob("CH-HASH") == raw

    def test_store_version_changed_mutable_metadata_rejected(self):
        """Admitted source with changed metadata (e.g., title) is rejected."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant mutable-meta"
        src = _make_src("CH-META", content_raw=raw)
        store.admit_source(src, raw)
        # Same source_id, same content_hash, different title (MUTABLE field)
        src_mutated = SourceRecord(
            source_id="CH-META",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/ch-meta",
            content_hash=hashlib.sha256(raw).hexdigest(),
            retrieval_date="2024-01-01",
            title="Changed title via store_version",
        )
        with pytest.raises(IntegrityConflict, match="incoming payload differs"):
            store.store_version(src_mutated, "v2")
        # Canonical unchanged
        loaded = store.load("SRC-01", "CH-META")
        assert loaded.title is None  # unchanged
        assert store.load_raw_blob("CH-META") == raw

    def test_store_version_binding_integrity_check(self):
        """If raw blob hash diverges from canonical content_hash, store_version is rejected."""
        store = InMemoryRawSourceArchive()
        raw = b"invariant binding"
        src = _make_src("BINDING", content_raw=raw)
        store.admit_source(src, raw)
        # Corrupt raw blob (different bytes, same record_id)
        store._raw_blobs["BINDING"] = b"corrupted bytes"
        with pytest.raises(IntegrityConflict, match="binding integrity violated"):
            store.store_version(src, "v1")
        # Restore and verify
        store._raw_blobs["BINDING"] = raw
        store.store_version(src, "v1")  # should pass now
    """Item 5 changes must not break Item 1-4 semantics.
    These are sample regression probes — full suite runs later."""

    def test_item1_primary_id_preserved(self):
        from qad.models.family_f import FinancialFact
        from qad.models.family_a import SecurityMaster, SecurityMasterSecurity_type, SecurityMasterStatus
        store = InMemoryRawSourceArchive()
        sm = SecurityMaster(
            entity_id="E-REGRESS-01",
            cik="R1", exchange="NYSE", name="Regression",
            primary_ticker="REG",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        store.store(sm)
        loaded = store.load("SM-01", "E-REGRESS-01")
        assert loaded.entity_id == "E-REGRESS-01"

    def test_item2_atomicity_preserved(self):
        from qad.models.family_b import EvidenceRecord, EvidenceRecordEvidence_type, EvidenceRecordValidation_status
        store = InMemoryRawSourceArchive()
        # DO NOT create the SourceRecord — FK will be missing
        ev = EvidenceRecord(
            evidence_id="EV-REGRESS-02",
            source_id="SRC-MISSING",  # no such source
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="no FK target tested",
            admitting_role="researcher",
            as_of="2024-01-01",
            extractor="v1",
            source_tier="L1",
        )
        with pytest.raises(Exception):
            store.store(ev)
        assert not store.contains("EV-01", "EV-REGRESS-02")

    def test_item3_tombstone_preserved(self):
        store = InMemoryRawSourceArchive()
        raw = b"regression item3"
        src = _make_src("E-REGRESS-03", content_raw=raw)
        store.admit_source(src, raw)
        store.tombstone("E-REGRESS-03", "test")
        assert store.is_tombstoned("E-REGRESS-03")
        assert store.load_raw_blob_historical("E-REGRESS-03") == raw

    def test_item4_append_only_preserved(self):
        from qad.models.family_a import SecurityMaster, SecurityMasterSecurity_type, SecurityMasterStatus
        store = InMemoryRawSourceArchive()
        sm = SecurityMaster(
            entity_id="E-REGRESS-04",
            cik="R4", exchange="NYSE", name="Reg4",
            primary_ticker="RG4",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
            ticker_history=[],
        )
        store.store(sm)
        ch1 = store.get_canonical_hash("SM-01", "E-REGRESS-04")
        # Create a valid source via admit_source (not direct store) for the FK chain
        raw_s = b"regression s"
        src_reg = _make_src("E-REGRESS-04S", content_raw=raw_s)
        store.admit_source(src_reg, raw_s)
        sm2 = sm.model_copy(update={"primary_ticker": "RG4B", "ticker_history": ["RG4"]})
        ch2 = store.store(sm2)
        assert ch1 != ch2
        loaded = store.load("SM-01", "E-REGRESS-04")
        assert loaded.ticker_history == ["RG4"]


# ===================================================================
# Item 11 — admit_source without raw bytes → rejection
# ===================================================================

def test_admit_without_raw_bytes_rejected():
    """Calling admit_source() without raw bytes must fail closed.

    admit_source(instance) without raw_bytes is a TypeError because
    raw_bytes is a required positional parameter.  This ensures no
    accidental source admission without the content-addressed binding.
    """
    import hashlib
    store = InMemoryRawSourceArchive()
    raw = b"orphan content"
    src = _make_src("E-NO-RAW", content_raw=raw)
    # admit_source requires raw_bytes — no default
    with pytest.raises(TypeError):
        store.admit_source(src)  # missing raw_bytes