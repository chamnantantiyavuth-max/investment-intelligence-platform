"""Protocol (structural typing) interfaces for all QAD persistence stores.

This module defines the *contracts* that every store adapter must fulfil.
Concrete implementations live in ``reference.py`` (in-memory) and future
production adapters (SQLite, PostgreSQL, …).

Store hierarchy
---------------
::

  BlobStore                        — raw bytes, content-addressed (no FK/canonical checks)
  │
  CanonicalRecordStore              — CRUD + batch for canonical records
  ├── RawSourceArchive              — + content-addressed blob, versioning, tombstone
  ├── EvidenceRegistry              — + FK-on-source, immutable-content-after-admission
  ├── FinancialFactStore            — + lineage, normalisation-chain persistence
  ├── RunManifestStore              — (pure CanonicalRecordStore extension)
  └── PITContextStore               — (pure CanonicalRecordStore extension)

  NonCanonicalResearchArtifactStore — separate hierarchy (no canonical checks)

Every ``CanonicalRecordStore`` implementer MUST call, in store():
  1. ``canonical_boundary_check`` — reject non-canonical schema IDs
  2. ``fk_enforcer.validate`` — every FK reference exists
  3. ``immutability_enforcer.check`` — no immutable field/record violations
  4. ``serialization.compute_canonical_hash`` — for content-addressing
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

RecordID = str
"""Primary identity of a record within its schema's store (e.g. case_id,
source_id, evidence_id …)."""

SchemaID = str
"""M4A schema identifier (e.g. ``CASE-01``, ``SRC-01``, ``EV-01``)."""

BlobHash = str
"""SHA-256 hex digest of raw blob content."""

CanonicalHash = str
"""SHA-256 hex digest of a canonical serialisation of a record."""

BatchID = str
"""Opaque identifier for a group of operations submitted atomically."""


# ===================================================================
# BlobStore — raw bytes, content-addressable
# ===================================================================

@runtime_checkable
class BlobStore(Protocol):
    """Content-addressable binary blob storage.

    Every blob is keyed by its own SHA-256 hash.  The caller provides the
    expected hash; the store verifies it matches the actual content and
    raises ``HashMismatch`` on disagreement.
    """

    def put(self, blob_hash: BlobHash, data: bytes) -> None:
        """Store raw bytes under a hash key.

        Raises:
            HashMismatch: ``sha256(data) != blob_hash``.
        """
        ...

    def get(self, blob_hash: BlobHash) -> bytes:
        """Retrieve raw bytes by hash.

        Raises:
            KeyError: hash not found.
        """
        ...

    def delete(self, blob_hash: BlobHash) -> None:
        """Remove a blob from the store."""
        ...

    def exists(self, blob_hash: BlobHash) -> bool:
        """Return True if the hash is present."""
        ...

    def list_blobs(self) -> list[BlobHash]:
        """Return every stored blob hash."""
        ...


# ===================================================================
# CanonicalRecordStore — base CRUD protocol for all canonical stores
# ===================================================================

@runtime_checkable
class CanonicalRecordStore(Protocol):
    """Abstract canonical record store.

    Every store works with M5.1 Pydantic model instances.  The schema_id
    is always derived from the instance itself (``instance.schema_id``).

    Implementers **must** enforce:
    - canonical boundary check
    - FK existence (via ``FK_REGISTRY``)
    - immutability rules (via contract descriptor)
    - deterministic canonical hashing (via ``serialization``)
    """

    # -- CRUD ---------------------------------------------------------------

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        """Persist a canonical record.

        Returns the canonical hash of the stored record.

        Raises:
            ValidationFailure: instance fails contract validation.
            CanonicalBoundaryViolation: schema is non-canonical.
            MissingForeignKey: FK reference not resolvable.
            ImmutabilityViolation: update would modify immutable data.
            IntegrityConflict: same ID with different payload.
        """
        ...

    def load(self, schema_id: SchemaID, record_id: RecordID, /) -> BaseModel:
        """Retrieve a single record.

        Raises:
            KeyError: record not found.
        """
        ...

    def delete(self, schema_id: SchemaID, record_id: RecordID, /) -> None:
        """Remove a record.

        Raises:
            KeyError: record not found.
        """
        ...

    def list_ids(self, schema_id: SchemaID, /) -> list[RecordID]:
        """Return all record IDs for a given schema."""
        ...

    def list_all(self, schema_id: SchemaID, /) -> list[BaseModel]:
        """Return all records for a given schema."""
        ...

    # -- Batch support ------------------------------------------------------

    def store_batch(self, instances: list[BaseModel], /) -> list[CanonicalHash]:
        """Atomically persist multiple records.

        All-or-nothing: if **any** check (FK, immutability, canonical
        boundary, integrity) fails, ZERO records are committed.

        Raises:
            TransactionFailure: wraps the list of individual errors.
        """
        ...

    def delete_batch(
        self, pairs: list[tuple[SchemaID, RecordID]], /,
    ) -> None:
        """Atomically delete multiple records.

        Raises:
            TransactionFailure: wraps errors.
        """
        ...

    # -- Introspection ------------------------------------------------------

    def get_canonical_hash(
        self, schema_id: SchemaID, record_id: RecordID, /,
    ) -> CanonicalHash:
        """Return the stored canonical hash for a record.

        Raises:
            KeyError: record not found.
        """
        ...

    def contains(self, schema_id: SchemaID, record_id: RecordID, /) -> bool:
        """Check existence without loading the full record."""
        ...


# ===================================================================
# RawSourceArchive — content-addressed source storage
# ===================================================================

@runtime_checkable
class RawSourceArchive(CanonicalRecordStore, Protocol):
    """Extends ``CanonicalRecordStore`` with raw-source workflow.

    In addition to the canonical record, the archive stores the original
    raw blob (web scrape, PDF, API response, …), supports versioning,
    and allows tombstoning (soft-delete with preservation of history).
    """

    def store_raw_blob(
        self, record_id: RecordID, blob_hash: BlobHash, data: bytes,
    ) -> None:
        """Store the raw binary source alongside its canonical record.

        Raises:
            HashMismatch: actual content hash != blob_hash.
        """
        ...

    def load_raw_blob(self, record_id: RecordID) -> bytes:
        """Retrieve the raw binary source.

        Raises:
            KeyError: record not found.
        """
        ...

    def get_raw_blob_hash(self, record_id: RecordID) -> BlobHash:
        """Return the hash of the raw blob for a given source record."""
        ...

    # -- Versioning ---------------------------------------------------------

    def store_version(
        self, instance: BaseModel, version_label: str, /,
    ) -> CanonicalHash:
        """Store a new version of a source record.

        Previous versions remain accessible via ``load_version``.
        """
        ...

    def load_version(
        self, record_id: RecordID, version_label: str, /,
    ) -> tuple[BaseModel, bytes | None]:
        """Retrieve a specific historical version (record + raw blob).

        Raises:
            KeyError: version not found.
        """
        ...

    def list_versions(self, record_id: RecordID) -> list[str]:
        """Return version labels for a source, newest first."""
        ...

    # -- Tombstone ----------------------------------------------------------

    def tombstone(self, record_id: RecordID, reason: str, /) -> None:
        """Soft-delete a source record.

        The record is marked as tombstoned but its history is preserved.
        ``load()`` raises ``KeyError`` for tombstoned records.
        """
        ...

    def is_tombstoned(self, record_id: RecordID) -> bool:
        """Return True if the record has been tombstoned."""
        ...

    def list_tombstoned_ids(self) -> list[RecordID]:
        """Return all tombstoned record IDs."""
        ...


# ===================================================================
# EvidenceRegistry — FK-backed, immutable-after-admission evidence
# ===================================================================

@runtime_checkable
class EvidenceRegistry(CanonicalRecordStore, Protocol):
    """Evidence record store with source-FK enforcement and admission gate.

    Once an evidence record is *admitted* (written through
    ``admit_evidence``), its identity-bearing fields (evidence_id,
    source_id) are immutable.  Only status fields may be updated.

    ``admit_evidence`` is the ONLY path for creating new canonical
    evidence.  Direct ``store(EV-01)`` for a non-existent evidence
    record is rejected.
    """

    def admit_evidence(
        self,
        evidence: BaseModel,
        admission: BaseModel,
        /,
    ) -> CanonicalHash:
        """Atomically admit an EvidenceRecord with its EvidenceAdmissionRecord.

        The admission gate enforces:
        - Source (SRC-01) exists in the authoritative RawSourceArchive
        - Source record is not tombstoned
        - Source content binding is intact (raw bytes exist)
        - EAR.evidence_id == EV.evidence_id
        - AI_EXTRACTION / AI_SYNTHESIS requires original_source_verified == true
        - Both records pass contract validation

        Failure rollback guarantees zero partial state.
        """
        ...

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        """Store evidence record.

        On first write, the source FK (``source_id → SRC-01``) is
        enforced.  After admission the content is immutable; only
        mutable status fields may change.
        """
        ...


# ===================================================================
# FinancialFactStore — lineage-aware fact storage
# ===================================================================

@runtime_checkable
class FinancialFactStore(CanonicalRecordStore, Protocol):
    """Financial fact store with lineage and normalisation-chain support.

    Every fact carries a ``source_id`` FK to ``SRC-01`` and may be
    linked to a parent fact (``FF-01.financial_fact_id``) to form a
    normalisation chain (raw → normalised → restated).
    """

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        """Store a financial fact, enforcing source FK.

        Raises:
            MissingForeignKey: source_id references a non-existent source.
        """
        ...

    def get_lineage(
        self, financial_fact_id: RecordID, /,
    ) -> list[BaseModel]:
        """Return the normalisation chain for a fact, raw → normalised.

        The first element is the root (raw) fact; the last is the most
        recent normalised version.
        """
        ...


# ===================================================================
# RunManifestStore — manifest records (pure CR)
# ===================================================================

@runtime_checkable
class RunManifestStore(CanonicalRecordStore, Protocol):
    """Run-manifest record store.

    Manifests are written once and never updated (``RECORD_IMMUTABLE``
    per contract descriptor for ``RRM-01``).
    """
    pass


# ===================================================================
# PITContextStore — point-in-time context records (pure CR)
# ===================================================================

@runtime_checkable
class PITContextStore(CanonicalRecordStore, Protocol):
    """PIT-context record store.

    Context records are written once and never updated (``RECORD_IMMUTABLE``
    per contract descriptor for ``PITC-01``).
    """
    pass


# ===================================================================
# NonCanonicalResearchArtifactStore
# ===================================================================

@runtime_checkable
class NonCanonicalResearchArtifactStore(Protocol):
    """Store for research artifacts that have NOT passed the canonical
    boundary.

    This store sits **outside** the canonical pipeline.  No FK enforcement,
    no canonical-hash enforcement, no immutability policy.  It is a
    lightweight, schema-agnostic storage for drafts, LLM raw outputs,
    notebook extracts, etc.

    Records are stored by an arbitrary namespace + key.
    """

    def store(self, namespace: str, key: RecordID, data: Any, /) -> None:
        """Persist a non-canonical artifact."""
        ...

    def load(self, namespace: str, key: RecordID, /) -> Any:
        """Retrieve a non-canonical artifact.

        Raises:
            KeyError: not found.
        """
        ...

    def delete(self, namespace: str, key: RecordID, /) -> None:
        """Remove a non-canonical artifact."""
        ...

    def list_namespaces(self) -> list[str]:
        """Return all namespaces in the store."""
        ...

    def list_keys(self, namespace: str) -> list[RecordID]:
        """Return all keys in a namespace."""
        ...