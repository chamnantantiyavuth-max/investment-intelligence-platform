"""In-memory reference adapter — NON-PRODUCTION / REFERENCE ONLY.

WARNING
-------
This module implements the persistence store protocols using plain Python
``dict`` structures.  It is a **proof-of-concept** for testing and
development.  Every public class carries the ``REFERENCE / NON_PRODUCTION``
label.

Guarantees
----------
- All CRUD operations go through a ``Transaction`` boundary.
- FK enforcement, canonical boundary checks, immutability policy, and
  contract validation are applied exactly as they would be in a production
  adapter.
- Content-addressing (SHA-256 of canonical serialisation) is computed
  on every write.
- No production database, no network I/O, no filesystem persistence.

Limitations
-----------
- No concurrent-access safety (no locks).
- No durability (data lost on process restart).
- ``store_batch`` / ``delete_batch`` are atomic within a single thread
  but not ACID across thread boundaries.
- ``RawSourceArchive`` stores raw blobs in memory (RAM pressure for
  large binaries).
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from pydantic import BaseModel

from qad.persistence.errors import (
    HashMismatch,
    NonCanonicalAdmissionRejected,
    PersistenceError,
    TransactionFailure,
)
from qad.persistence.interfaces import (
    BlobHash,
    BlobStore,
    CanonicalHash,
    CanonicalRecordStore,
    EvidenceRegistry,
    FinancialFactStore,
    NonCanonicalResearchArtifactStore,
    PITContextStore,
    RawSourceArchive,
    RecordID,
    RunManifestStore,
    SchemaID,
)
from qad.persistence.serialization import (
    compute_canonical_hash,
    serialize_to_canonical_bytes,
)
from qad.persistence.transaction import Transaction


# ===================================================================
# Internal record envelope
# ===================================================================

class _Record:
    """Lightweight envelope wrapping a stored record with its metadata."""

    __slots__ = ("instance", "canonical_hash", "raw_blob")

    def __init__(self, instance: BaseModel, canonical_hash: str,
                 raw_blob: bytes | None = None):
        self.instance = instance
        self.canonical_hash = canonical_hash
        self.raw_blob = raw_blob


# ===================================================================
# InMemoryCanonicalRecordStore — base reference implementation
# ===================================================================

class InMemoryCanonicalRecordStore:
    """REFERENCE / NON-PRODUCTION — dict-backed canonical record store.

    This is the base mixin / implementation that all specialised stores
    in this module extend.  It implements ``CanonicalRecordStore`` using
    a single dict::

        _data: dict[SchemaID, dict[RecordID, _Record]] = {}

    All public write operations flow through ``Transaction``.
    """

    # -- storage (shared across instances sharing the same backing) ---------

    def __init__(self, data: dict[str, dict[str, _Record]] | None = None):
        self._data: dict[str, dict[str, _Record]] = data or {}

    # -- CanonicalRecordStore implementation ---------------------------------

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _resolve_id(instance)

        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        tx.add_store(instance)
        tx.execute()

        return compute_canonical_hash(instance)

    def load(self, schema_id: SchemaID, record_id: RecordID, /) -> BaseModel:
        rec = self._load_raw(schema_id, record_id)
        if rec is None:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        # Return a deep copy to prevent mutation of stored data
        return deepcopy(rec)

    def delete(self, schema_id: SchemaID, record_id: RecordID, /) -> None:
        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        tx.add_delete(schema_id, record_id)
        tx.execute()

    def list_ids(self, schema_id: SchemaID, /) -> list[RecordID]:
        bucket = self._data.get(schema_id, {})
        return list(bucket.keys())

    def list_all(self, schema_id: SchemaID, /) -> list[BaseModel]:
        bucket = self._data.get(schema_id, {})
        return [deepcopy(rec.instance) for rec in bucket.values()]

    def store_batch(self, instances: list[BaseModel], /) -> list[CanonicalHash]:
        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        for inst in instances:
            tx.add_store(inst)
        tx.execute()
        return [compute_canonical_hash(inst) for inst in instances]

    def delete_batch(
        self, pairs: list[tuple[SchemaID, RecordID]], /,
    ) -> None:
        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        for sid, rid in pairs:
            tx.add_delete(sid, rid)
        tx.execute()

    def get_canonical_hash(
        self, schema_id: SchemaID, record_id: RecordID, /,
    ) -> CanonicalHash:
        rec = self._data.get(schema_id, {}).get(record_id)
        if rec is None:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        return rec.canonical_hash

    def contains(self, schema_id: SchemaID, record_id: RecordID, /) -> bool:
        return record_id in self._data.get(schema_id, {})

    # -- atomic commit helpers (snapshot/restore for Transaction rollback) ---

    def _snapshot(self) -> dict[str, dict[str, "_Record"]]:
        """Deep-copy snapshot of the entire store state for rollback.

        Returns a dict of ``{schema_id: {record_id: _Record}}`` that can
        be restored via ``_restore()``.
        """
        return deepcopy(self._data)

    def _restore(self, snapshot: dict[str, dict[str, "_Record"]]) -> None:
        """Restore store state from a ``_snapshot()`` result."""
        self._data = snapshot

    # -- internal helpers (used by Transaction callbacks) --------------------

    def _write_record(
        self, schema_id: SchemaID, record_id: RecordID,
        instance: BaseModel, canonical_hash: CanonicalHash,
    ) -> None:
        """Direct write — bypasses validation; called from Transaction.commit."""
        self._data.setdefault(schema_id, {})[record_id] = _Record(
            instance=deepcopy(instance),
            canonical_hash=canonical_hash,
        )

    def _remove_record(
        self, schema_id: SchemaID, record_id: RecordID,
    ) -> None:
        """Direct delete — bypasses validation; called from Transaction.commit."""
        bucket = self._data.get(schema_id)
        if bucket is None or record_id not in bucket:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        del bucket[record_id]

    def _load_raw(
        self, schema_id: SchemaID, record_id: RecordID,
    ) -> BaseModel | None:
        """Return the stored instance or None (no exception)."""
        rec = self._data.get(schema_id, {}).get(record_id)
        return rec.instance if rec else None

    def _load_hash(
        self, schema_id: SchemaID, record_id: RecordID,
    ) -> str | None:
        """Return the stored canonical hash or None."""
        rec = self._data.get(schema_id, {}).get(record_id)
        return rec.canonical_hash if rec else None


# ===================================================================
# InMemoryRawSourceArchive
# ===================================================================

class InMemoryRawSourceArchive(InMemoryCanonicalRecordStore):
    """REFERENCE / NON-PRODUCTION — in-memory raw source archive.

    Extends ``InMemoryCanonicalRecordStore`` with raw blob storage,
    versioning, and tombstone support.
    """

    def __init__(self) -> None:
        super().__init__()
        # {record_id: {version_label: _Record}}
        self._version_data: dict[str, dict[str, _Record]] = {}
        # {record_id: raw_blob_bytes}
        self._raw_blobs: dict[str, bytes] = {}
        # {record_id: reason}
        self._tombstones: dict[str, str] = {}

    # -- Raw blob storage ---------------------------------------------------

    def store_raw_blob(
        self, record_id: RecordID, blob_hash: BlobHash, data: bytes,
    ) -> None:
        import hashlib
        actual = hashlib.sha256(data).hexdigest()
        if actual != blob_hash:
            raise HashMismatch(
                f"Blob hash mismatch: expected {blob_hash}, got {actual}",
                record_id=record_id,
                expected_hash=blob_hash,
                actual_hash=actual,
            )
        self._raw_blobs[record_id] = data

    def load_raw_blob(self, record_id: RecordID) -> bytes:
        if record_id in self._tombstones:
            raise KeyError(f"{record_id}: tombstoned")
        try:
            return self._raw_blobs[record_id]
        except KeyError:
            raise KeyError(f"{record_id}: no raw blob found")

    def get_raw_blob_hash(self, record_id: RecordID) -> BlobHash:
        data = self._raw_blobs.get(record_id)
        if data is None:
            raise KeyError(f"{record_id}: no raw blob found")
        import hashlib
        return hashlib.sha256(data).hexdigest()

    # -- Versioning ---------------------------------------------------------

    def store_version(
        self, instance: BaseModel, version_label: str, /,
    ) -> CanonicalHash:
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _resolve_id(instance)
        ch = compute_canonical_hash(instance)

        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        tx.add_store(instance)
        tx.execute()

        # Also store in version archive
        self._version_data.setdefault(record_id, {})[version_label] = _Record(
            instance=deepcopy(instance),
            canonical_hash=ch,
        )
        return ch

    def load_version(
        self, record_id: RecordID, version_label: str, /,
    ) -> tuple[BaseModel, bytes | None]:
        versions = self._version_data.get(record_id, {})
        rec = versions.get(version_label)
        if rec is None:
            raise KeyError(f"{record_id}@{version_label}: not found")
        blob = self._raw_blobs.get(record_id)
        return deepcopy(rec.instance), blob

    def list_versions(self, record_id: RecordID) -> list[str]:
        versions = self._version_data.get(record_id, {})
        return sorted(versions.keys(), reverse=True)

    # -- Tombstone ----------------------------------------------------------

    def tombstone(self, record_id: RecordID, reason: str, /) -> None:
        self._tombstones[record_id] = reason

        # Remove from active data in every schema bucket
        for schema_bucket in self._data.values():
            if record_id in schema_bucket:
                del schema_bucket[record_id]
                break

    def is_tombstoned(self, record_id: RecordID) -> bool:
        return record_id in self._tombstones

    def list_tombstoned_ids(self) -> list[RecordID]:
        return list(self._tombstones.keys())

    # -- Override load to reject tombstoned records -------------------------

    def load(self, schema_id: SchemaID, record_id: RecordID, /) -> BaseModel:
        if record_id in self._tombstones:
            raise KeyError(f"{schema_id}/{record_id}: tombstoned")
        return super().load(schema_id, record_id)


# ===================================================================
# InMemoryEvidenceRegistry
# ===================================================================

class InMemoryEvidenceRegistry(InMemoryCanonicalRecordStore):
    """REFERENCE / NON-PRODUCTION — evidence store with source-FK enforcement.

    Once admitted, evidence content is immutable.  Only mutable fields
    (per contract descriptor) may be updated in subsequent writes.
    """

    def __init__(self) -> None:
        super().__init__()
        self._admitted: set[str] = set()  # evidence_id set

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        evidence_id = _resolve_id(instance)

        # If already admitted, only mutable fields may change
        if evidence_id in self._admitted:
            existing = self._load_raw(schema_id, evidence_id)
            if existing is not None:
                return self._update_mutable_fields(schema_id, evidence_id,
                                                    instance, existing)
            # Fall through to new admission

        # First admission
        ch = super().store(instance)
        self._admitted.add(evidence_id)
        return ch

    def _update_mutable_fields(
        self, schema_id: SchemaID, evidence_id: RecordID,
        incoming: BaseModel, existing: BaseModel,
    ) -> CanonicalHash:
        """Merge mutable-field updates into the existing record.

        Immutable fields are preserved from the original.  Only fields
        whose ``immutable_policy`` is ``MUTABLE`` are updated.
        """
        from qad.persistence.immutability import _field_policy

        merged = deepcopy(existing)
        for field_name in incoming.model_fields:
            if field_name == "schema_id":
                continue
            policy = _field_policy(schema_id, field_name)
            if policy == "MUTABLE":
                new_val = getattr(incoming, field_name)
                setattr(merged, field_name, new_val)

        # Commit via Transaction
        ch = compute_canonical_hash(merged)
        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        tx.add_store(merged)
        tx.execute()
        return ch


# ===================================================================
# InMemoryFinancialFactStore
# ===================================================================

class InMemoryFinancialFactStore(InMemoryCanonicalRecordStore):
    """REFERENCE / NON_PRODUCTION — financial fact store with lineage.

    Stores facts in memory and supports retrieval of normalisation
    chains (raw → normalised) via ``get_lineage``.
    """

    def __init__(self, data: dict[str, dict[str, Any]] | None = None) -> None:
        super().__init__(data)
        # Parent fact tracking: {financial_fact_id: parent_financial_fact_id}
        self._parent_links: dict[str, str] = {}

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        # Detect parent lineage from the instance
        parent = getattr(instance, "parent_fact_id", None) or \
                 getattr(instance, "normalized_from_id", None)
        ch = super().store(instance)
        fid = _resolve_id(instance)
        if parent:
            self._parent_links[fid] = str(parent)
        return ch

    def get_lineage(
        self, financial_fact_id: RecordID, /,
    ) -> list[BaseModel]:
        """Return chain from root (raw) to current, ordered oldest first."""
        chain: list[BaseModel] = []
        current_id = financial_fact_id

        # Walk backwards to root
        while current_id:
            try:
                inst = super().load("FF-01", current_id)
                chain.insert(0, inst)
                current_id = self._parent_links.get(current_id)
            except KeyError:
                break

        if not chain:
            raise KeyError(f"FF-01/{financial_fact_id}: not found")

        return chain


# ===================================================================
# InMemoryRunManifestStore
# ===================================================================

class InMemoryRunManifestStore(InMemoryCanonicalRecordStore):
    """REFERENCE / NON-PRODUCTION — run manifest store.

    Manifests are write-once per contract (RECORD_IMMUTABLE enforcement
    inherited from ``Transaction`` → ``check_immutability``).
    """
    pass


# ===================================================================
# InMemoryPITContextStore
# ===================================================================

class InMemoryPITContextStore(InMemoryCanonicalRecordStore):
    """REFERENCE / NON-PRODUCTION — PIT context store.

    Context records are write-once (RECORD_IMMUTABLE enforcement inherited
    from ``Transaction`` → ``check_immutability``).
    """
    pass


# ===================================================================
# InMemoryBlobStore
# ===================================================================

class InMemoryBlobStore:
    """REFERENCE / NON-PRODUCTION — in-memory content-addressed blob store.

    Implements ``BlobStore`` protocol with a single dict.
    """

    def __init__(self) -> None:
        self._blobs: dict[str, bytes] = {}

    def put(self, blob_hash: BlobHash, data: bytes) -> None:
        import hashlib
        actual = hashlib.sha256(data).hexdigest()
        if actual != blob_hash:
            raise HashMismatch(
                f"Blob hash mismatch: expected {blob_hash}, got {actual}",
                expected_hash=blob_hash,
                actual_hash=actual,
            )
        self._blobs[blob_hash] = data

    def get(self, blob_hash: BlobHash) -> bytes:
        try:
            return self._blobs[blob_hash]
        except KeyError:
            raise KeyError(f"Blob {blob_hash}: not found")

    def delete(self, blob_hash: BlobHash) -> None:
        try:
            del self._blobs[blob_hash]
        except KeyError:
            raise KeyError(f"Blob {blob_hash}: not found")

    def exists(self, blob_hash: BlobHash) -> bool:
        return blob_hash in self._blobs

    def list_blobs(self) -> list[BlobHash]:
        return list(self._blobs.keys())


# ===================================================================
# InMemoryNonCanonicalResearchArtifactStore
# ===================================================================

class InMemoryNonCanonicalResearchArtifactStore:
    """REFERENCE / NON-PRODUCTION — non-canonical artifact store.

    Completely separate from canonical storage.  No FK checks, no
    canonical boundary checks, no immutability enforcement.
    """

    def __init__(self) -> None:
        self._data: dict[str, dict[str, Any]] = {}

    def store(self, namespace: str, key: RecordID, data: Any, /) -> None:
        self._data.setdefault(namespace, {})[key] = deepcopy(data)

    def load(self, namespace: str, key: RecordID, /) -> Any:
        try:
            return deepcopy(self._data[namespace][key])
        except KeyError:
            raise KeyError(f"{namespace}/{key}: not found")

    def delete(self, namespace: str, key: RecordID, /) -> None:
        try:
            del self._data[namespace][key]
        except KeyError:
            raise KeyError(f"{namespace}/{key}: not found")

    def list_namespaces(self) -> list[str]:
        return list(self._data.keys())

    def list_keys(self, namespace: str) -> list[RecordID]:
        return list(self._data.get(namespace, {}).keys())


# ===================================================================
# Helpers
# ===================================================================

def _resolve_id(instance: BaseModel) -> str:
    """Extract the record's primary identity field from a model instance.

    For schemas with an explicit identity field (e.g. ``evidence_id`` for
    ``EV-01``), that field is returned.  For schemas without one (e.g.
    ``SRC-01 SourceRecord``), the first matching FK-/ID-pattern field is
    used.  See also :func:`_schema_identity_field`.
    """
    sid: str = getattr(instance, "schema_id", "")
    identity_field = _schema_identity_field(sid)
    if identity_field:
        val = getattr(instance, identity_field, None)
        if val is not None:
            return str(val)
    # Fallback: search the general candidates list (FK-style fields).
    candidates = (
        "source_id", "evidence_id", "finding_id",
        "financial_fact_id", "manifest_id", "pit_context_id",
        "entity_id", "signal_id", "candidate_id", "claim_id",
        "usage_id", "audit_id", "budget_id", "lock_id",
        "indicator_id", "hypothesis_id", "lesson_id",
        "publication_id", "verdict_id", "challenge_id",
        "assessment_id", "gap_id", "knowledge_id",
        "r_dcf_id", "invocation_id", "eval_run_id",
        "model_invocation_id", "impairment_id",
        "case_id", "assessment_id", "provider_invocation_id",
        "expectation_id", "valuation_id",
    )
    for name in candidates:
        val = getattr(instance, name, None)
        if val is not None:
            return str(val)
    sid = getattr(instance, "schema_id", "UNKNOWN")
    return f"{sid}:{id(instance)}"


def _schema_identity_field(schema_id: str) -> str | None:
    """Return the primary identity field name for a given schema ID.

    Uses the mechanically derived primary-identity registry (generated from
    frozen M4A ``IDs / foreign keys`` declarations).  This ensures the PK
    is always correct even when the instance also carries FK fields with
    similar names.

    If the schema is not found in the registry (e.g. a non-canonical schema
    that slipped through), returns ``None`` and the caller falls back to
    heuristic candidate scanning or a ``PersistenceIdentityError``.
    """
    import json
    from pathlib import Path

    _reg_path = (
        Path(__file__).resolve().parent.parent.parent
        / "qad" / "contract" / "primary_id_registry.json"
    )
    try:
        with open(_reg_path) as _f:
            _registry = json.load(_f)["PRIMARY_ID_FIELDS"]
    except Exception:
        _registry = {}
    return _registry.get(schema_id)