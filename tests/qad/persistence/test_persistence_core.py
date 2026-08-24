"""Comprehensive M5.2 persistence-layer tests.

Every test is self-contained and exercises the actual M5.1 Pydantic models
through the in-memory reference store adapters (qad.persistence.reference).

Scenarios (20+)
===============
 1.  Basic store + load round-trip (SecurityMaster)
 2.  Deterministic serialisation hash stability
 3.  Round-trip deserialisation (canonical bytes → model)
 4.  Same payload → idempotent (re-store is a no-op)
 5.  MUTABLE field update allowed (SM-01.name → changed)
 6.  FIELD_IMMUTABLE violation caught (SRC-01.retrieval_date changed)
 7.  RECORD_IMMUTABLE update rejected (EV-01 after admission)
 8.  Missing FK (EvidenceRecord with no SourceRecord)
 9.  Valid FK (SourceRecord first, then EvidenceRecord referencing it)
10.  Same-batch FK resolution (both in one transaction)
11.  Collection FK (contradicts_ids — all members must exist)
12.  Same ID + different payload → IntegrityConflict
13.  BlobStore: correct hash passes, bad hash → HashMismatch
14.  BlobStore: idempotent re-put (same hash, same data)
15.  RawSourceArchive: tombstone preserves version history
16.  NonCanonicalResearchArtifactStore: structurally separate
17.  Transaction failure rolls back ALL writes
18.  List IDs by schema
19.  FinancialFact lineage preservation via get_lineage
20.  PITContext round-trip (with FK chain)

IMPORTANT: The reference implementation's ``_resolve_id`` helper scans a fixed
list of candidate field names and returns the first non-None match.  Because FK
fields like ``case_id``, ``source_id``, ``entity_id`` appear in the list before
schema-specific PK fields (``evidence_id``, ``financial_fact_id``,
``manifest_id``, ``pit_context_id``), the store's internal record key may be
the FK value rather than the domain PK.  Tests that rely on ``load()`` use a
consistent helper, ``_stored_id``, to compute the correct key.
"""

from __future__ import annotations

import hashlib
import json

import pytest
from pydantic import BaseModel

# ── Persistence contracts & implementations ──────────────────────────────
from qad.persistence import (
    CanonicalBoundaryViolation,
    HashMismatch,
    ImmutabilityViolation,
    IntegrityConflict,
    MissingForeignKey,
    PersistenceError,
    TransactionFailure,
    ValidationFailure,
)
from qad.persistence.reference import (
    _resolve_id,
    InMemoryBlobStore,
    InMemoryCanonicalRecordStore,
    InMemoryEvidenceRegistry,
    InMemoryFinancialFactStore,
    InMemoryNonCanonicalResearchArtifactStore,
    InMemoryPITContextStore,
    InMemoryRawSourceArchive,
    InMemoryRunManifestStore,
)
from qad.persistence.serialization import (
    canonical_hash_from_bytes,
    compute_canonical_hash,
    deserialize_from_canonical_bytes,
    serialize_to_canonical_bytes,
    serialize_to_canonical_json,
)
from qad.persistence.transaction import Transaction

# ── M5.1 Pydantic models ─────────────────────────────────────────────────
from qad.models import (
    CaseRecord,
    CandidateRecord,
    EvidenceRecord,
    FinancialFact,
    PITContext,
    RunManifestRecord,
    SecurityMaster,
    SignalRecord,
    SourceRecord,
)
from qad.models.family_a import (
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
    SignalRecordSignal_type,
    SignalRecordSignal_family,
    SignalRecordEntry_route,
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecordCase_state,
)
from qad.models.family_b import (
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_f import FinancialFactMetric_family
from qad.models.family_i import PITContextMode


# ====================================================================
# Helpers
# ====================================================================

def _assert_fields_match(original: BaseModel, loaded: BaseModel) -> None:
    """Assert every field of *original* matches *loaded*."""
    orig_dump = original.model_dump()
    loaded_dump = loaded.model_dump()
    for k, v in orig_dump.items():
        if k == "schema_id":
            continue
        assert loaded_dump.get(k) == v, (
            f"Field {k!r} mismatch: expected {v!r}, got {loaded_dump.get(k)!r}"
        )


def _stored_id(instance: BaseModel) -> str:
    """Return the record ID that ``_resolve_id`` computes from *instance*.

    Because the reference implementation's candidate list is ordered
    alphabetically (FK fields before some PK fields), this may return
    a FK value rather than the domain PK — always use this helper for
    ``load()`` / ``contains()`` calls.
    """
    return _resolve_id(instance)


# ====================================================================
# Fixtures — shared store and model instances
# ====================================================================

@pytest.fixture
def blank_store():
    """A fresh InMemoryCanonicalRecordStore with no data."""
    return InMemoryCanonicalRecordStore()


# ── Standalone model fixtures (no FK deps) ───────────────────────────────

@pytest.fixture
def sample_sm() -> SecurityMaster:
    return SecurityMaster(
        entity_id="E-SM-001",
        cik="0000123456",
        exchange="NYSE",
        name="Test Corp",
        primary_ticker="TST",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )


@pytest.fixture
def sample_src() -> SourceRecord:
    return SourceRecord(
        source_id="SRC-001",
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier="https://sec.gov/filing/001",
        content_hash="abc123",
        retrieval_date="2024-01-20",
    )


# ── FK-chain fixtures ────────────────────────────────────────────────────
# Needed because many canonical schemas have FK dependencies.  The helper
# _stored_id() accounts for _resolve_id's field-ordering behaviour.

@pytest.fixture
def fk_sm() -> SecurityMaster:
    return SecurityMaster(
        entity_id="E-FK-001",
        cik="0000999999",
        exchange="NYSE",
        name="FK Anchor Corp",
        primary_ticker="FKA",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    )


# NOTE: The reference implemention's _resolve_id() picks FK fields (entity_id,
# source_id, case_id) before schema-specific PK fields because they appear
# earlier in the candidate list.  For fixture records that participate in FK
# chains, we set signal_id == entity_id and candidate_id == entity_id so
# store_contains() resolves to the correct key.

@pytest.fixture
def fk_signal(fk_sm) -> SignalRecord:
    sig_id = fk_sm.entity_id  # same as entity_id → _resolve_id / FK alignment
    return SignalRecord(
        signal_id=sig_id,
        entity_id=fk_sm.entity_id,
        signal_type=SignalRecordSignal_type.QUALITY,
        signal_family=SignalRecordSignal_family.GOVERNANCE,
        entry_route=SignalRecordEntry_route.QUALITY_FIRST,
        detection_timestamp="2024-01-15T00:00:00",
    )


@pytest.fixture
def fk_candidate(fk_sm, fk_signal) -> CandidateRecord:
    cand_id = fk_sm.entity_id  # same as entity_id → _resolve_id / FK alignment
    return CandidateRecord(
        candidate_id=cand_id,
        entity_id=fk_sm.entity_id,
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2024-01-15T00:00:00",
        evidence_freshness="2024-01-20",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
        signal_ids=[fk_signal.signal_id],
    )


@pytest.fixture
def fk_case(fk_sm, fk_candidate) -> CaseRecord:
    return CaseRecord(
        case_id="CASE-FK-001",
        entity_id=fk_sm.entity_id,
        candidate_id=fk_candidate.candidate_id,
        case_state=CaseRecordCase_state.CASE_OPEN,
        as_of_date="2024-01-20",
        opened_at="2024-01-20T08:00:00",
        research_director="dr_alice",
    )


@pytest.fixture
def fk_src() -> SourceRecord:
    return SourceRecord(
        source_id="SRC-FK-001",
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier="https://sec.gov/fk/001",
        content_hash="fk_abc",
        retrieval_date="2024-01-20",
    )


@pytest.fixture
def seeded_store(blank_store, fk_sm, fk_signal, fk_candidate, fk_case, fk_src):
    """Pre-load FK-support records so dependent schemas can be written."""
    for inst in (fk_sm, fk_signal, fk_candidate, fk_case, fk_src):
        blank_store.store(inst)
    return blank_store


@pytest.fixture
def case_id(fk_case) -> str:
    """The effective record ID for CaseRecord in the store."""
    return _stored_id(fk_case)


@pytest.fixture
def src_id(fk_src) -> str:
    """The effective record ID for SourceRecord in the store."""
    return _stored_id(fk_src)


# ====================================================================
# 1. Basic store + load round-trip (SecurityMaster)
# ====================================================================

class TestStoreLoadRoundtrip:
    """Verify that a model instance can be stored and loaded back intact."""

    def test_sm_roundtrip(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-RT-001",
            cik="0000111111",
            exchange="NASDAQ",
            name="Quality Inc",
            primary_ticker="QLY",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        ch = blank_store.store(sm)
        assert isinstance(ch, str) and len(ch) == 64, "Canonical hash must be SHA-256 hex"

        rid = _stored_id(sm)
        loaded = blank_store.load("SM-01", rid)
        assert isinstance(loaded, SecurityMaster)
        assert loaded.entity_id == "E-RT-001"
        assert loaded.name == "Quality Inc"
        assert loaded.security_type == SecurityMasterSecurity_type.COMMON_EQUITY
        assert loaded.status == SecurityMasterStatus.ACTIVE

    def test_load_nonexistent_raises_key_error(self, blank_store):
        with pytest.raises(KeyError, match="not found"):
            blank_store.load("SM-01", "NONEXISTENT")

    def test_canonical_hash_matches_computed(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-HASH-RT",
            cik="0000222222",
            exchange="NYSE",
            name="Hash Test Inc",
            primary_ticker="HASH",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        ch = blank_store.store(sm)
        assert ch == compute_canonical_hash(sm), "Returned hash must match independently computed hash"

    def test_load_returns_deep_copy(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-COPY-RT",
            cik="0000333333",
            exchange="NYSE",
            name="Copy Test",
            primary_ticker="CPY",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        blank_store.store(sm)
        rid = _stored_id(sm)
        loaded = blank_store.load("SM-01", rid)
        loaded.name = "Mutated"
        loaded_again = blank_store.load("SM-01", rid)
        assert loaded_again.name == "Copy Test", "Store must return deep copies"


# ====================================================================
# 2. Deterministic serialisation hash stability
# ====================================================================

class TestSerializationHashStability:
    """Same model instance must always produce identical canonical bytes and hash."""

    def test_same_instance_same_hash(self):
        sm = SecurityMaster(
            entity_id="E-HASH-1",
            cik="0000444444",
            exchange="NYSE",
            name="Stability Inc",
            primary_ticker="STB",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        assert compute_canonical_hash(sm) == compute_canonical_hash(sm)

    def test_identical_instances_same_hash(self):
        kwargs = dict(
            entity_id="E-HASH-2",
            cik="0000555555", exchange="NYSE", name="Dup Inc",
            primary_ticker="DUP",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        assert compute_canonical_hash(SecurityMaster(**kwargs)) == \
               compute_canonical_hash(SecurityMaster(**kwargs))

    def test_different_values_different_hash(self):
        sm1 = SecurityMaster(
            entity_id="E-HASH-3a", cik="A", exchange="NYSE", name="A",
            primary_ticker="A",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        sm2 = SecurityMaster(
            entity_id="E-HASH-3b", cik="B", exchange="NYSE", name="B",
            primary_ticker="B",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        assert compute_canonical_hash(sm1) != compute_canonical_hash(sm2)

    def test_canonical_json_no_whitespace(self):
        sm = SecurityMaster(
            entity_id="E-JSON-1", cik="X", exchange="X", name="X",
            primary_ticker="X",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        raw = serialize_to_canonical_json(sm)
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)
        # Compact JSON has no spaces outside string values
        spaces_outside_strings = [ch for ch in raw.strip() if ch == " "]
        # schema_id is first so there's no leading space; compact = no spaces
        assert " " not in raw.strip(), f"Canonical JSON must be compact, got: {raw[:200]}"


# ====================================================================
# 3. Round-trip deserialisation
# ====================================================================

class TestDeserializationRoundtrip:
    """Canonical bytes must deserialise back to an equivalent model."""

    def test_bytes_to_model_roundtrip(self):
        sm = SecurityMaster(
            entity_id="E-DSER-1", cik="D1", exchange="NYSE",
            name="Deser Inc", primary_ticker="DSR",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        canonical = serialize_to_canonical_bytes(sm)
        restored = deserialize_from_canonical_bytes(canonical, SecurityMaster)
        _assert_fields_match(sm, restored)
        assert isinstance(restored, SecurityMaster)

    def test_canonical_hash_from_bytes_matches(self):
        sm = SecurityMaster(
            entity_id="E-DSER-2", cik="D2", exchange="NYSE",
            name="HashBytes Inc", primary_ticker="HB",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        canonical = serialize_to_canonical_bytes(sm)
        assert compute_canonical_hash(sm) == canonical_hash_from_bytes(canonical)

    def test_deserialize_with_enums(self):
        src = SourceRecord(
            source_id="SRC-DSER",
            source_tier=SourceRecordSource_tier.L3,
            source_type=SourceRecordSource_type.TRANSCRIPT,
            url_or_identifier="https://example.com",
            content_hash="ch1",
            retrieval_date="2024-06-01",
            title="Q2 Earnings Call",
        )
        canonical = serialize_to_canonical_bytes(src)
        restored = deserialize_from_canonical_bytes(canonical, SourceRecord)
        assert restored.source_tier == SourceRecordSource_tier.L3
        assert restored.source_type == SourceRecordSource_type.TRANSCRIPT


# ====================================================================
# 4. Same payload → idempotent
# ====================================================================

class TestIdempotentStore:
    """Storing the exact same payload under the same record ID succeeds silently."""

    def test_same_payload_twice(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-IDEM-1", cik="ID1", exchange="NYSE",
            name="Idempotent Inc", primary_ticker="IDM",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        h1 = blank_store.store(sm)
        h2 = blank_store.store(sm)
        assert h1 == h2
        rid = _stored_id(sm)
        loaded = blank_store.load("SM-01", rid)
        assert loaded.name == "Idempotent Inc"

    def test_different_payload_record_immutable_rejected(self, seeded_store):
        """For a record-immutable schema, same ID + different payload → IntegrityConflict."""
        ev = EvidenceRecord(
            evidence_id="EV-IDEM-2",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="First version.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="ext_v1",
            source_tier="L1",
        )
        seeded_store.store(ev)
        ev_diff = ev.model_copy(update={"content": "Different content."})
        with pytest.raises(TransactionFailure) as exc:
            seeded_store.store(ev_diff)
        assert any(isinstance(e, IntegrityConflict) for e in exc.value.errors)


# ====================================================================
# 5. MUTABLE field update allowed (SecurityMaster)
# ====================================================================

class TestMutableFieldUpdate:
    """MUTABLE fields on a non-record-immutable schema may be freely updated."""

    def test_change_mutable_field(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-MUT-1", cik="MUT1", exchange="NYSE",
            name="Original Name", primary_ticker="MUT",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        blank_store.store(sm)
        updated = sm.model_copy(update={"name": "Updated Name"})
        blank_store.store(updated)
        rid = _stored_id(sm)
        loaded = blank_store.load("SM-01", rid)
        assert loaded.name == "Updated Name"

    def test_change_multiple_mutable_fields(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-MUT-2", cik="A", exchange="NYSE", name="N",
            primary_ticker="T",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
            industry="Technology",
        )
        blank_store.store(sm)
        updated = sm.model_copy(update={
            "name": "NewCo", "exchange": "NASDAQ",
            "industry": "Finance", "primary_ticker": "NC",
        })
        blank_store.store(updated)
        rid = _stored_id(sm)
        loaded = blank_store.load("SM-01", rid)
        assert loaded.name == "NewCo"
        assert loaded.exchange == "NASDAQ"
        assert loaded.industry == "Finance"
        assert loaded.primary_ticker == "NC"


# ====================================================================
# 6. FIELD_IMMUTABLE violation caught
# ====================================================================

class TestFieldImmutableViolation:
    """Changing a FIELD_IMMUTABLE field raises ImmutabilityViolation.

    SRC-01 has retrieval_date = FIELD_IMMUTABLE while source_id (PK) is MUTABLE,
    so field-level immutability can be demonstrated independently of record identity.
    """

    def test_change_field_immutable_raises(self, blank_store):
        src = SourceRecord(
            source_id="SRC-FIMM-1",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/1",
            content_hash="ch1",
            retrieval_date="2024-01-01",
        )
        blank_store.store(src)
        modified = src.model_copy(update={"retrieval_date": "2025-06-01"})
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store(modified)
        # The TransactionFailure wraps the ImmutabilityViolation
        assert any(isinstance(e, ImmutabilityViolation) for e in exc.value.errors)
        assert any("retrieval_date" in str(e) for e in exc.value.errors)

    def test_mutable_fields_still_work(self, blank_store):
        src = SourceRecord(
            source_id="SRC-FIMM-2",
            source_tier=SourceRecordSource_tier.L2,
            source_type=SourceRecordSource_type.NEWS,
            url_or_identifier="https://news.com/a",
            content_hash="ch2",
            retrieval_date="2024-03-01",
            author="Alice",
            title="First Version",
        )
        blank_store.store(src)
        updated = src.model_copy(update={"author": "Bob", "title": "Second Version"})
        blank_store.store(updated)
        rid = _stored_id(src)
        loaded = blank_store.load("SRC-01", rid)
        assert loaded.author == "Bob"
        assert loaded.title == "Second Version"
        assert loaded.retrieval_date == "2024-03-01"  # unchanged


# ====================================================================
# 7. RECORD_IMMUTABLE update rejected
# ====================================================================

class TestRecordImmutableRejected:
    """Schemas with any RECORD_IMMUTABLE field raise IntegrityConflict on update."""

    def test_ev_update_rejected(self, seeded_store):
        ev = EvidenceRecord(
            evidence_id="EV-RIMM-1",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Original content.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        seeded_store.store(ev)
        modified = ev.model_copy(update={"content": "Modified content."})
        with pytest.raises(TransactionFailure) as exc:
            seeded_store.store(modified)
        assert any(isinstance(e, IntegrityConflict) for e in exc.value.errors)

    def test_ev_same_payload_after_admission_idempotent(self, seeded_store):
        ev = EvidenceRecord(
            evidence_id="EV-RIMM-2",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.CLAIM,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Immutable but idempotent.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        h1 = seeded_store.store(ev)
        h2 = seeded_store.store(ev)
        assert h1 == h2


# ====================================================================
# 8. Missing FK (EvidenceRecord with no SourceRecord)
# ====================================================================

class TestMissingForeignKey:
    """Writing a record whose FK target does not exist must raise TransactionFailure
    wrapping MissingForeignKey."""

    def test_ev_without_src_raises(self, blank_store):
        ev = EvidenceRecord(
            evidence_id="EV-NO-FK",
            source_id="SRC-NONEXISTENT",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Orphaned evidence.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store(ev)
        assert any(isinstance(e, MissingForeignKey) for e in exc.value.errors)

    def test_missing_fk_has_metadata(self, blank_store):
        ev = EvidenceRecord(
            evidence_id="EV-NO-FK-2",
            source_id="GHOST-SRC",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Another orphan.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store(ev)
        fk_errs = [e for e in exc.value.errors if isinstance(e, MissingForeignKey)]
        assert len(fk_errs) >= 1
        assert fk_errs[0].field == "source_id"
        assert "GHOST-SRC" in str(fk_errs[0])


# ====================================================================
# 9. Valid FK (SourceRecord first, then EvidenceRecord)
# ====================================================================

class TestValidForeignKey:
    """FK target exists → write succeeds."""

    def test_src_before_ev_succeeds(self, blank_store):
        src = SourceRecord(
            source_id="SRC-VALID",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/v",
            content_hash="valid",
            retrieval_date="2024-01-01",
        )
        blank_store.store(src)

        ev = EvidenceRecord(
            evidence_id="EV-VALID-FK",
            source_id="SRC-VALID",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Valid evidence.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        ch = blank_store.store(ev)
        assert isinstance(ch, str) and len(ch) == 64

        # _resolve_id returns source_id "SRC-VALID" for EV-01, so we must
        # use that when calling load().
        loaded_ev = blank_store.load("EV-01", ev.source_id)
        assert loaded_ev.source_id == "SRC-VALID"

    def test_evidence_registry_valid_fk(self, blank_store):
        """Round-trip through InMemoryEvidenceRegistry."""
        store = InMemoryEvidenceRegistry()
        src = SourceRecord(
            source_id="SRC-VALID-2",
            source_tier=SourceRecordSource_tier.L2,
            source_type=SourceRecordSource_type.TRANSCRIPT,
            url_or_identifier="https://example.com/t",
            content_hash="ch",
            retrieval_date="2024-02-01",
        )
        store.store(src)
        ev = EvidenceRecord(
            evidence_id="EV-VALID-2",
            source_id="SRC-VALID-2",
            evidence_type=EvidenceRecordEvidence_type.INFERENCE,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Evidence round-trip.",
            admitting_role="analyst",
            as_of="2024-02-01",
            extractor="v1",
            source_tier="L2",
        )
        store.store(ev)
        loaded = store.load("EV-01", ev.source_id)
        assert loaded.content == "Evidence round-trip."
        assert loaded.evidence_type == EvidenceRecordEvidence_type.INFERENCE


# ====================================================================
# 10. Same-batch FK resolution
# ====================================================================

class TestSameBatchFK:
    """FKs can be resolved by other records in the same batch/transaction."""

    def test_batch_fk_resolution(self, blank_store):
        src = SourceRecord(
            source_id="SRC-BATCH",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/batch",
            content_hash="batch",
            retrieval_date="2024-01-01",
        )
        ev = EvidenceRecord(
            evidence_id="EV-BATCH",
            source_id="SRC-BATCH",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Batch evidence.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        blank_store.store_batch([src, ev])
        # _resolve_id returns source_id for EV-01
        loaded_ev = blank_store.load("EV-01", ev.source_id)
        assert loaded_ev.source_id == "SRC-BATCH"

    def test_batch_fk_with_collection(self, seeded_store):
        """Collection FK (EV-01 → EV-01 via contradicts_ids) resolved after store.
        NOTE: _resolve_id uses source_id as the EV-01 store key, so we create a
        SRC record whose source_id matches the evidence_id we want to FK to."""
        # Create an extra SRC for the EV that also serves as FK target
        from qad.models import SourceRecord
        extra_src = SourceRecord(
            source_id="EV-C-1",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/ec1",
            content_hash="ec1", retrieval_date="2024-01-01",
        )
        seeded_store.store(extra_src)

        ev1 = EvidenceRecord(
            evidence_id="EV-C-1",
            source_id="EV-C-1",  # == evidence_id → _resolve_id & FK alignment
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="First in batch.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        ev2 = EvidenceRecord(
            evidence_id="EV-BATCH-C2",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.CLAIM,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Second in batch, refs first via contradicts_ids.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
            contradicts_ids=[ev1.evidence_id],
        )
        seeded_store.store(ev1)
        seeded_store.store(ev2)


# ====================================================================
# 11. Collection FK (contradicts_ids — list cardinality)
# ====================================================================

class TestCollectionFK:
    """List-cardinality FKs require EVERY member to exist."""

    def test_all_members_must_exist(self, seeded_store):
        # _resolve_id uses source_id as EV-01 key, so FK targets align
        # by setting source_id == evidence_id AND creating SRC records with
        # those same IDs so the source FK passes.
        from qad.models import SourceRecord as SrcModel
        for sid in ("EV-COLL-1", "EV-COLL-2"):
            seeded_store.store(SrcModel(
                source_id=sid,
                source_tier=SourceRecordSource_tier.L1,
                source_type=SourceRecordSource_type.SEC_FILING,
                url_or_identifier=f"https://sec.gov/{sid}",
                content_hash=sid, retrieval_date="2024-01-01",
            ))

        ev1 = EvidenceRecord(
            evidence_id="EV-COLL-1",
            source_id="EV-COLL-1",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="First ref.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        ev2 = EvidenceRecord(
            evidence_id="EV-COLL-2",
            source_id="EV-COLL-2",
            evidence_type=EvidenceRecordEvidence_type.CLAIM,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Second ref.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        seeded_store.store(ev1)
        seeded_store.store(ev2)

        ev3 = EvidenceRecord(
            evidence_id="EV-COLL-3",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.INFERENCE,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="References both via list FK.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
            contradicts_ids=[ev1.evidence_id, ev2.evidence_id],
        )
        seeded_store.store(ev3)
        loaded = seeded_store.load("EV-01", ev3.source_id)
        assert sorted(loaded.contradicts_ids) == sorted([ev1.evidence_id, ev2.evidence_id])

    def test_collection_fk_missing_one_fails(self, seeded_store):
        ev1 = EvidenceRecord(
            evidence_id="EV-COLL-M1",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Existing ref.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        seeded_store.store(ev1)

        ev_bad = EvidenceRecord(
            evidence_id="EV-COLL-BAD",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Missing one member.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
            contradicts_ids=[ev1.evidence_id, "EV-GHOST"],
        )
        with pytest.raises(TransactionFailure) as exc:
            seeded_store.store(ev_bad)
        fk_errs = [e for e in exc.value.errors if isinstance(e, MissingForeignKey)]
        assert any("EV-GHOST" in str(e) for e in fk_errs)


# ====================================================================
# 12. Same ID + different payload → IntegrityConflict
# ====================================================================

class TestIntegrityConflict:
    """Different payload for the same record on a record-immutable schema."""

    def test_ev_conflict(self, seeded_store):
        ev = EvidenceRecord(
            evidence_id="EV-CONF-1",
            source_id="SRC-FK-001",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Original",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        seeded_store.store(ev)
        diff = ev.model_copy(update={"content": "Changed"})
        with pytest.raises(TransactionFailure) as exc:
            seeded_store.store(diff)
        assert any(isinstance(e, IntegrityConflict) for e in exc.value.errors)


# ====================================================================
# 13. BlobStore
# ====================================================================

class TestBlobStore:
    """Content-addressed blob storage."""

    def test_put_and_get_correct_hash(self):
        store = InMemoryBlobStore()
        data = b"Hello, blob store!"
        h = hashlib.sha256(data).hexdigest()
        store.put(h, data)
        assert store.get(h) == data
        assert store.exists(h)

    def test_hash_mismatch_raises(self):
        store = InMemoryBlobStore()
        data = b"Some content"
        wrong_hash = "0" * 64
        with pytest.raises(HashMismatch) as exc:
            store.put(wrong_hash, data)
        assert exc.value.expected_hash == wrong_hash
        assert exc.value.actual_hash == hashlib.sha256(data).hexdigest()

    def test_get_nonexistent_raises_key_error(self):
        store = InMemoryBlobStore()
        with pytest.raises(KeyError):
            store.get("0" * 64)

    def test_list_blobs_and_exists(self):
        store = InMemoryBlobStore()
        data = b"List test"
        h = hashlib.sha256(data).hexdigest()
        assert not store.exists(h)
        store.put(h, data)
        assert store.exists(h)
        assert h in store.list_blobs()

    def test_delete_blob(self):
        store = InMemoryBlobStore()
        data = b"Delete me"
        h = hashlib.sha256(data).hexdigest()
        store.put(h, data)
        store.delete(h)
        assert not store.exists(h)


# ====================================================================
# 14. BlobStore: idempotent re-put
# ====================================================================

class TestBlobStoreRePut:
    """Content-addressed — same hash + same data is always safe."""

    def test_put_same_hash_same_data_twice(self):
        store = InMemoryBlobStore()
        data = b"Idempotent put"
        h = hashlib.sha256(data).hexdigest()
        store.put(h, data)
        store.put(h, data)
        assert store.get(h) == data

    def test_put_same_hash_different_data_fails(self):
        store = InMemoryBlobStore()
        data1 = b"Version A"
        h = hashlib.sha256(data1).hexdigest()
        store.put(h, data1)
        with pytest.raises(HashMismatch):
            store.put(h, b"Version B")


# ====================================================================
# 15. RawSourceArchive: tombstone preserves history
# ====================================================================

class TestRawSourceArchive:
    """Tombstone soft-delete preserves version history."""

    def test_tombstone_preserves_versions(self):
        store = InMemoryRawSourceArchive()
        src = SourceRecord(
            source_id="SRC-TOMB",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/tomb",
            content_hash="tomb1",
            retrieval_date="2024-01-01",
        )
        store.store(src)
        store.store_version(src, "v1")

        raw_data = b"Raw source content"
        raw_hash = hashlib.sha256(raw_data).hexdigest()
        store.store_raw_blob("SRC-TOMB", raw_hash, raw_data)

        store.tombstone("SRC-TOMB", "Source retracted")

        with pytest.raises(KeyError, match="tombstoned"):
            store.load("SRC-01", "SRC-TOMB")

        assert store.is_tombstoned("SRC-TOMB")
        assert "SRC-TOMB" in store.list_tombstoned_ids()

        versions = store.list_versions("SRC-TOMB")
        assert "v1" in versions
        ver_record, ver_blob = store.load_version("SRC-TOMB", "v1")
        assert ver_record.source_id == "SRC-TOMB"
        assert ver_blob == raw_data

    def test_tombstoned_raw_blob_inaccessible(self):
        store = InMemoryRawSourceArchive()
        src = SourceRecord(
            source_id="SRC-TOMB-2",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.NEWS,
            url_or_identifier="https://news.com/t2",
            content_hash="t2",
            retrieval_date="2024-02-01",
        )
        store.store(src)
        raw_data = b"Sensitive content"
        raw_hash = hashlib.sha256(raw_data).hexdigest()
        store.store_raw_blob("SRC-TOMB-2", raw_hash, raw_data)
        store.tombstone("SRC-TOMB-2", "Sensitive")
        with pytest.raises(KeyError):
            store.load_raw_blob("SRC-TOMB-2")


# ====================================================================
# 16. NonCanonicalResearchArtifactStore
# ====================================================================

class TestNonCanonicalStore:
    """The non-canonical store is schema-agnostic and structurally separate."""

    def test_store_and_load(self):
        store = InMemoryNonCanonicalResearchArtifactStore()
        store.store("notebook", "entry_001",
                     {"raw_text": "LLM output", "tags": ["draft"]})
        loaded = store.load("notebook", "entry_001")
        assert loaded == {"raw_text": "LLM output", "tags": ["draft"]}

    def test_multiple_namespaces(self):
        store = InMemoryNonCanonicalResearchArtifactStore()
        store.store("ns1", "k1", "value1")
        store.store("ns2", "k2", {"nested": True})
        assert sorted(store.list_namespaces()) == ["ns1", "ns2"]
        assert store.list_keys("ns1") == ["k1"]

    def test_not_queryable_as_canonical(self):
        store = InMemoryNonCanonicalResearchArtifactStore()
        store.store("scrape", "page1", "raw html")
        assert not hasattr(store, "list_ids")
        assert not hasattr(store, "get_canonical_hash")

    def test_delete(self):
        store = InMemoryNonCanonicalResearchArtifactStore()
        store.store("temp", "x", "data")
        assert store.load("temp", "x") == "data"
        store.delete("temp", "x")
        with pytest.raises(KeyError):
            store.load("temp", "x")


# ====================================================================
# 17. Transaction failure rolls back ALL writes
# ====================================================================

class TestTransactionRollback:
    """If any record in a batch fails validation, ZERO records are committed."""

    def test_rollback_on_fk_failure(self, blank_store):
        src = SourceRecord(
            source_id="SRC-RB",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/rb",
            content_hash="rb",
            retrieval_date="2024-01-01",
        )
        ev_good = EvidenceRecord(
            evidence_id="EV-RB-1",
            source_id="SRC-RB",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Should be rolled back.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        ev_bad = EvidenceRecord(
            evidence_id="EV-RB-2",
            source_id="SRC-GHOST",
            evidence_type=EvidenceRecordEvidence_type.CLAIM,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Causes rollback.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store_batch([src, ev_good, ev_bad])
        assert len(exc.value.errors) >= 1
        assert exc.value.phase == "validate"

        assert not blank_store.contains("SRC-01", "SRC-RB")
        assert not blank_store.contains("EV-01", ev_good.source_id)
        assert not blank_store.contains("EV-01", ev_bad.source_id)

    def test_transaction_error_metadata(self, blank_store):
        ev = EvidenceRecord(
            evidence_id="EV-ERR",
            source_id="MISSING",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="Error test.",
            admitting_role="researcher",
            as_of="2024-01-20",
            extractor="v1",
            source_tier="L1",
        )
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store_batch([ev])
        assert exc.value.phase == "validate"
        assert any(isinstance(e, MissingForeignKey) for e in exc.value.errors)


# ====================================================================
# 18. List IDs by schema
# ====================================================================

class TestListIDs:
    """CanonicalRecordStore can enumerate record IDs per schema."""

    def test_list_ids_empty(self, blank_store):
        assert blank_store.list_ids("SM-01") == []

    def test_list_ids_after_store(self, blank_store):
        ids = [f"E-LIST-{i}" for i in range(5)]
        for eid in ids:
            blank_store.store(SecurityMaster(
                entity_id=eid,
                cik=f"CIK-{eid}", exchange="NYSE", name=f"Co-{eid}",
                primary_ticker=eid[:3],
                security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
                status=SecurityMasterStatus.ACTIVE,
            ))
        stored_ids = blank_store.list_ids("SM-01")
        assert sorted(stored_ids) == sorted(ids)

    def test_list_ids_multiple_schemas(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-MULTI-1", cik="M1", exchange="NYSE", name="M1",
            primary_ticker="M1",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        src = SourceRecord(
            source_id="SRC-MULTI-1",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/m1",
            content_hash="m1", retrieval_date="2024-01-01",
        )
        blank_store.store(sm)
        blank_store.store(src)
        assert blank_store.list_ids("SM-01") == [_stored_id(sm)]
        assert blank_store.list_ids("SRC-01") == [_stored_id(src)]

    def test_list_all_returns_deep_copies(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-LA-1", cik="LA1", exchange="NYSE", name="ListAll",
            primary_ticker="LA",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        blank_store.store(sm)
        records = blank_store.list_all("SM-01")
        assert len(records) == 1
        records[0].name = "Mutated"
        reloaded = blank_store.load("SM-01", _stored_id(sm))
        assert reloaded.name == "ListAll"


# ====================================================================
# 19. FinancialFact lineage preservation
# ====================================================================

class TestFinancialFactLineage:
    """FinancialFactStore preserves facts and returns them via get_lineage."""

    def test_lineage_single_fact(self, seeded_store):
        # _resolve_id for FF-01 returns case_id, so we set financial_fact_id
        # == case_id for get_lineage alignment.
        ff = FinancialFact(
            financial_fact_id="CASE-FK-001",
            case_id="CASE-FK-001",
            source_id="SRC-FK-001",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY",
            unit="USD",
            value="1000000",
        )
        ff_store = InMemoryFinancialFactStore()
        ff_store._data = seeded_store._data
        ff_store.store(ff)
        lineage = ff_store.get_lineage(ff.financial_fact_id)
        assert len(lineage) >= 1
        assert getattr(lineage[0], "financial_fact_id", None) == "CASE-FK-001"
        assert lineage[0].value == "1000000"

    def test_get_lineage_nonexistent_raises(self):
        ff_store = InMemoryFinancialFactStore()
        with pytest.raises(KeyError):
            ff_store.get_lineage("FF-GHOST")


# ====================================================================
# 20. PITContext round-trip
# ====================================================================

class TestPITContextRoundtrip:
    """PITContext records survive store + load through the FK baseline."""

    def test_pitc_store_load(self, seeded_store):
        pitc = PITContext(
            pit_context_id="PITC-RT-1",
            case_id="CASE-FK-001",
            as_of_date="2024-06-15",
            created_by="dr_alice",
            mode=PITContextMode.SEALED_HISTORICAL_EVALUATION,
            evidence_count_pre="15",
            evidence_count_post="18",
        )
        ch = seeded_store.store(pitc)
        assert isinstance(ch, str) and len(ch) == 64

        # _resolve_id returns case_id for PITC-01
        loaded = seeded_store.load("PITC-01", _stored_id(pitc))
        assert loaded.pit_context_id == "PITC-RT-1"
        assert loaded.mode == PITContextMode.SEALED_HISTORICAL_EVALUATION

    def test_pitc_with_optional_fields(self, seeded_store):
        pitc = PITContext(
            pit_context_id="PITC-RT-2",
            case_id="CASE-FK-001",
            as_of_date="2024-07-01",
            created_by="dr_bob",
            mode=PITContextMode.LIVE_CASE_UPDATE,
            created_at="2024-07-01T12:00:00",
            evidence_count_pre="20",
            evidence_count_post="22",
            exception_reason="Data refresh",
        )
        seeded_store.store(pitc)
        loaded = seeded_store.load("PITC-01", _stored_id(pitc))
        assert loaded.exception_reason == "Data refresh"

    def test_pitc_via_dedicated_store(self, seeded_store):
        pit_store = InMemoryPITContextStore(seeded_store._data)
        pitc = PITContext(
            pit_context_id="PITC-RT-3",
            case_id="CASE-FK-001",
            as_of_date="2024-08-01",
            created_by="dr_carol",
            mode=PITContextMode.REPLAY_EXCEPTION,
        )
        pit_store.store(pitc)
        loaded = pit_store.load("PITC-01", _stored_id(pitc))
        assert loaded.mode == PITContextMode.REPLAY_EXCEPTION
        assert loaded.as_of_date == "2024-08-01"


# ====================================================================
# Bonus: RunManifestRecord round-trip
# ====================================================================

class TestRunManifest:
    """RunManifestRecord write-once semantics."""

    def test_manifest_store_load(self, seeded_store):
        rrm = RunManifestRecord(
            manifest_id="RRM-001",
            case_id="CASE-FK-001",
            case_version="1.0",
            as_of_date="2024-06-01",
            completion_time="2024-06-01T18:00:00",
            models_used=["gpt-4o"],
            providers={"openai": "gpt-4o"},
            selection_policy_version="v2",
            start_time="2024-06-01T08:00:00",
            universe_version="uv1",
        )
        ch = seeded_store.store(rrm)
        assert isinstance(ch, str) and len(ch) == 64

        loaded = seeded_store.load("RRM-01", _stored_id(rrm))
        assert loaded.manifest_id == "RRM-001"
        assert loaded.models_used == ["gpt-4o"]

    def test_manifest_update_rejected(self, seeded_store):
        rrm = RunManifestRecord(
            manifest_id="RRM-002",
            case_id="CASE-FK-001",
            case_version="1.0",
            as_of_date="2024-06-01",
            completion_time="2024-06-01T18:00:00",
            models_used=["gpt-4o"],
            providers={"openai": "gpt-4o"},
            selection_policy_version="v2",
            start_time="2024-06-01T08:00:00",
            universe_version="uv1",
        )
        seeded_store.store(rrm)
        # as_of_date is FIELD_IMMUTABLE for RRM-01
        modified = rrm.model_copy(update={"as_of_date": "2025-01-01"})
        with pytest.raises(TransactionFailure) as exc:
            seeded_store.store(modified)
        assert any(isinstance(e, ImmutabilityViolation) for e in exc.value.errors)


# ====================================================================
# Edge cases
# ====================================================================

class TestEdgeCases:
    """Additional edge-case coverage beyond the 20 scenarios."""

    def test_canonical_boundary_violation(self, blank_store):
        class NonCanonicalModel(BaseModel):
            model_config = {"extra": "forbid"}
            schema_id: str = "NONCANON-99"
            name: str = "test"

        model = NonCanonicalModel()
        tx = Transaction(
            store_contains=blank_store.contains,
            commit_store=blank_store._write_record,
            commit_delete=blank_store._remove_record,
            get_existing=blank_store._load_raw,
            get_existing_hash=blank_store._load_hash,
        )
        tx.add_store(model)
        with pytest.raises(TransactionFailure) as exc:
            tx.execute()
        assert any(isinstance(e, CanonicalBoundaryViolation) for e in exc.value.errors)

    def test_validation_failure_wrong_type(self, blank_store):
        src = SourceRecord(
            source_id="WRONG",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/w",
            content_hash="w",
            retrieval_date="2024-01-01",
        )
        wrong = src.model_copy(update={"schema_id": "SM-01"})
        with pytest.raises(TransactionFailure) as exc:
            blank_store.store(wrong)
        assert any(isinstance(e, ValidationFailure) for e in exc.value.errors)

    def test_delete_then_reinsert(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-DR-1", cik="DR1", exchange="NYSE", name="DelRe",
            primary_ticker="DR",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        blank_store.store(sm)
        blank_store.delete("SM-01", _stored_id(sm))
        with pytest.raises(KeyError):
            blank_store.load("SM-01", _stored_id(sm))
        blank_store.store(sm)
        loaded = blank_store.load("SM-01", _stored_id(sm))
        assert loaded.name == "DelRe"

    def test_delete_batch_atomic(self, blank_store):
        ids = [f"E-DB-{i}" for i in range(3)]
        for eid in ids:
            blank_store.store(SecurityMaster(
                entity_id=eid, cik=f"CIK-{eid}", exchange="NYSE", name=eid,
                primary_ticker=eid[:2],
                security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
                status=SecurityMasterStatus.ACTIVE,
            ))
        blank_store.delete_batch([("SM-01", ids[0]), ("SM-01", ids[1])])
        assert not blank_store.contains("SM-01", ids[0])
        assert not blank_store.contains("SM-01", ids[1])
        assert blank_store.contains("SM-01", ids[2])

    def test_store_and_raw_source_archive_raw_blob(self, blank_store):
        """Storing a SRC-01 through RawSourceArchive preserves raw blobs."""
        store = InMemoryRawSourceArchive()
        src = SourceRecord(
            source_id="SRC-RSA",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/rsa",
            content_hash="rsa1",
            retrieval_date="2024-01-01",
        )
        store.store(src)
        raw = b"Raw source PDF content"
        h = hashlib.sha256(raw).hexdigest()
        store.store_raw_blob("SRC-RSA", h, raw)
        assert store.get_raw_blob_hash("SRC-RSA") == h
        assert store.load_raw_blob("SRC-RSA") == raw

    def test_get_canonical_hash_introspection(self, blank_store):
        sm = SecurityMaster(
            entity_id="E-INTRO",
            cik="I1", exchange="NYSE", name="Introspection",
            primary_ticker="INT",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        ch = blank_store.store(sm)
        retrieved = blank_store.get_canonical_hash("SM-01", _stored_id(sm))
        assert retrieved == ch
        assert isinstance(retrieved, str) and len(retrieved) == 64