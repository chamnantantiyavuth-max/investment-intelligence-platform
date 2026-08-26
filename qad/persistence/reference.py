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
    IntegrityConflict,
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
        # Tombstone tracking: {schema_id: {record_id1, record_id2, ...}}
        # Records in _data persist indefinitely for historical/audit recovery.
        # Tombstoned records are excluded from active reads (load, contains,
        # list_ids, list_all) but are recoverable via load_historical().
        # Tombstone metadata: {schema_id: {record_id: {"reason": ..., "authorizer": ..., "timestamp": ...}}}
        # Records stay in _data for audit/historical recovery.
        # Active reads exclude records in this dict.
        self._tombstones: dict[str, dict[str, dict]] = {}

        # Version tracking for APPEND_ONLY / APPEND_ONLY_STATE schemas
        # {schema_id: {record_id: {version_label: _Record}}}
        self._versions: dict[str, dict[str, dict[str, _Record]]] = {}
        # Monotonic version counter keyed by schema-qualified identity
        # {schema_id:record_id: count}
        self._version_counts: dict[str, int] = {}

    # -- CanonicalRecordStore implementation ---------------------------------

    def store(self, instance: BaseModel, /) -> CanonicalHash:
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _resolve_id(instance)

        # Reject writes to tombstoned canonical records
        if record_id in self._tombstones.get(schema_id, set()):
            raise IntegrityConflict(
                f"{schema_id}/{record_id}: cannot write to tombstoned record "
                f"(canonical hard delete is forbidden)",
                schema_id=schema_id,
                record_id=record_id,
            )

        # Prepare the final canonical instance before Transaction
        # (e.g. SM-01 ticker_history enrichment — must happen before
        # validation/hashing/commit so the returned hash matches stored hash)
        instance = self._prepare_instance(instance)

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
        if record_id in self._tombstones.get(schema_id, set()):
            raise KeyError(f"{schema_id}/{record_id}: tombstoned")
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
        tombstones = self._tombstones.get(schema_id, {})
        return [rid for rid in bucket if rid not in tombstones]

    def list_all(self, schema_id: SchemaID, /) -> list[BaseModel]:
        bucket = self._data.get(schema_id, {})
        tombstones = self._tombstones.get(schema_id, {})
        return [
            deepcopy(rec.instance)
            for rid, rec in bucket.items()
            if rid not in tombstones
        ]

    # -- Canonical tombstone API (public) -----------------------------------

    def tombstone(
        self, schema_id: SchemaID, record_id: RecordID,
        reason: str = "",
        authorizer: str = "",
    ) -> None:
        """Explicitly tombstone a canonical record.

        Per M4A invariant: "Deletion without tombstone → VIOLATION."
        Per SRCV-01: "Tombstone records removal reason and authorizer."
        Per Evidence Doctrine: tombstone metadata = reason + authorizer + timestamp.

        The record stays in ``_data`` for audit recovery.
        Active reads (``load``, ``contains``, ``list_ids``, ``list_all``)
        exclude tombstoned records.
        Use ``load_historical()`` for audit/historical access.

        Raises:
            KeyError: record not found.
        """
        bucket = self._data.get(schema_id)
        if bucket is None or record_id not in bucket:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        from datetime import datetime
        self._tombstones.setdefault(schema_id, {})[record_id] = {
            "reason": reason,
            "authorizer": authorizer,
            "timestamp": datetime.now().isoformat(),
        }

    def is_tombstoned(
        self, schema_id: SchemaID, record_id: RecordID, /,
    ) -> bool:
        """Return True if the record has been tombstoned."""
        return record_id in self._tombstones.get(schema_id, {})

    def list_tombstoned_ids(
        self, schema_id: SchemaID, /,
    ) -> list[RecordID]:
        """Return all tombstoned record IDs for a schema."""
        return sorted(self._tombstones.get(schema_id, {}))

    def load_historical(
        self, schema_id: SchemaID, record_id: RecordID, /,
    ) -> BaseModel:
        """Load a record regardless of tombstone status.

        For audit/historical recovery — bypasses the tombstone gate.
        Raises KeyError if the record was never stored.
        """
        rec = self._load_raw(schema_id, record_id)
        if rec is None:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        return deepcopy(rec)

    def store_batch(self, instances: list[BaseModel], /) -> list[CanonicalHash]:
        # Check for duplicate identities — a batch is a set of independent
        # operations, not a sequence of dependent mutations.  Duplicate
        # (schema_id, record_id) pairs would produce undefined ordering
        # and incorrect history enrichment (each _prepare_instance() sees
        # the same pre-batch state).
        seen: set[tuple[str, str]] = set()
        for inst in instances:
            sid: str = inst.schema_id  # type: ignore[assignment]
            rid = _resolve_id(inst)
            key = (sid, rid)
            if key in seen:
                raise IntegrityConflict(
                    f"{sid}/{rid}: duplicate identity in batch — "
                    f"batch operations must be independent",
                    schema_id=sid,
                    record_id=rid,
                )
            seen.add(key)
            if rid in self._tombstones.get(sid, {}):
                raise IntegrityConflict(
                    f"{sid}/{rid}: cannot write to tombstoned record "
                    f"(canonical hard delete is forbidden)",
                    schema_id=sid,
                    record_id=rid,
                )

        # Prepare all instances before Transaction
        prepared = [self._prepare_instance(inst) for inst in instances]

        tx = Transaction(
            store_contains=self.contains,
            commit_store=self._write_record,
            commit_delete=self._remove_record,
            get_existing=self._load_raw,
            get_existing_hash=self._load_hash,
            commit_snapshot=self._snapshot,
            commit_restore=self._restore,
        )
        for inst in prepared:
            tx.add_store(inst)
        tx.execute()
        return [compute_canonical_hash(inst) for inst in prepared]

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

    # -- Version API (APPEND_ONLY / APPEND_ONLY_STATE history) --------------

    def load_version(
        self, schema_id: SchemaID, record_id: RecordID,
        version_label: str, /,
    ) -> BaseModel:
        """Load a specific historical version of a record.

        Prior versions are preserved for APPEND_ONLY / APPEND_ONLY_STATE
        schemas when a record is updated.  The latest version is the
        current ``load()`` state; earlier versions are retrievable here.

        Raises:
            KeyError: no such version archived for this record.
        """
        try:
            rec = self._versions[schema_id][record_id][version_label]
        except KeyError:
            raise KeyError(
                f"{schema_id}/{record_id}@{version_label}: version not found"
            )
        return deepcopy(rec.instance)

    def list_versions(self, schema_id: SchemaID, record_id: RecordID, /) -> list[str]:
        """Return all preserved version labels (oldest first) for a record.

        Does NOT include the current (active) record unless it was itself
        preserved as a prior version by a later write.

        Uses numeric ordering (v1, v2, ..., v9, v10, v11) via the
        stored version_counter metadata keyed by ``schema_id:record_id``.
        """
        versions = self._versions.get(schema_id, {}).get(record_id, {})
        # Sort by extracting the numeric suffix, not by string label
        # (v10 < v9 in string sort; we want v1, v2, ..., v9, v10, v11)
        def _sort_key(label: str) -> int:
            try:
                return int(label.lstrip("v"))
            except (ValueError, AttributeError):
                return 0
        return sorted(versions.keys(), key=_sort_key)

    def get_version_count(self, schema_id: SchemaID, record_id: RecordID, /) -> int:
        """Return the number of preserved prior versions for a record."""
        return len(self._versions.get(schema_id, {}).get(record_id, {}))

    def contains(self, schema_id: SchemaID, record_id: RecordID, /) -> bool:
        bucket = self._data.get(schema_id, {})
        if record_id not in bucket:
            return False
        if record_id in self._tombstones.get(schema_id, {}):
            return False
        return True

    # -- atomic commit helpers (snapshot/restore for Transaction rollback) ---

    def _snapshot(self) -> tuple[dict[str, dict[str, "_Record"]], dict[str, dict[str, dict]], dict[str, dict[str, dict[str, "_Record"]]], dict[str, int]]:
        """Deep-copy snapshot of the entire store state for rollback.

        Returns ``(data, tombstones, versions, version_counts)`` — all four
        must be restored via ``_restore()`` to guarantee atomic rollback.
        """
        return deepcopy(self._data), deepcopy(self._tombstones), deepcopy(self._versions), deepcopy(self._version_counts)

    def _restore(self, snapshot: tuple[dict[str, dict[str, "_Record"]], dict[str, dict[str, dict]], dict[str, dict[str, dict[str, "_Record"]]], dict[str, int]]) -> None:
        """Restore store state from a ``_snapshot()`` result."""
        self._data, self._tombstones, self._versions, self._version_counts = snapshot

    # -- internal helpers (used by Transaction callbacks) --------------------

    def _write_record(
        self, schema_id: SchemaID, record_id: RecordID,
        instance: BaseModel, canonical_hash: CanonicalHash,
    ) -> None:
        """Direct write — bypasses validation; called from Transaction.commit.

        If the record already exists and the schema requires versioning,
        the prior version is preserved in ``_versions`` before overwriting.

        SM-01 ticker-history enrichment is NOT done here — it is handled
        in ``_prepare_instance()`` before Transaction submission, so the
        canonical hash returned by ``store()`` matches the stored hash.
        """
        existing = self._data.get(schema_id, {}).get(record_id)

        # Preserve prior version if this is an update to a versioned schema
        if existing is not None and _has_versioned_fields(schema_id):
            _save_version(self, schema_id, record_id, existing)

        self._data.setdefault(schema_id, {})[record_id] = _Record(
            instance=deepcopy(instance),
            canonical_hash=canonical_hash,
        )

    def _prepare_instance(self, instance: BaseModel, /) -> BaseModel:
        """Transform the incoming instance into its final canonical form
        before Transaction submission.

        Currently handles SM-01 ticker-history enrichment: the existing
        canonical ticker_history is ALWAYS authoritative.  If the ticker
        changed, the old ticker is appended.  If the ticker is unchanged,
        the existing history is preserved as-is (never erased by a stale
        or empty incoming ``ticker_history``).

        Enrichment is only applied when the incoming instance's history
        differs from the canonical stored history, so idempotent writes
        (same ticker, same history) produce identical hashes.

        This runs BEFORE validation/hashing/commit, so the returned
        hash from ``store()`` equals the stored canonical hash.
        """
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _resolve_id(instance)

        if schema_id == "SM-01":
            existing = self._data.get(schema_id, {}).get(record_id)
            if existing is not None:
                existing_history = list(
                    getattr(existing.instance, "ticker_history", []) or []
                )
                # Determine the authoritative next history
                old_ticker = getattr(existing.instance, "primary_ticker", None)
                new_ticker = getattr(instance, "primary_ticker", None)
                next_history = list(existing_history)
                if old_ticker is not None and old_ticker != new_ticker:
                    next_history.append(str(old_ticker))

                # Only apply enrichment if the incoming instance's history
                # differs from the authoritative next history
                incoming_history = getattr(instance, "ticker_history", None) or []
                if list(incoming_history) != next_history:
                    instance = instance.model_copy(
                        update={"ticker_history": next_history}
                    )

        return instance

    def _remove_record(
        self, schema_id: SchemaID, record_id: RecordID,
    ) -> None:
        """Canonical tombstone — preserves history; called from Transaction.commit.

        The record stays in ``_data`` so its data, canonical hash, and raw
        blobs remain recoverable for audit/historical queries.  Active reads
        (``load``, ``contains``, ``list_ids``, ``list_all``) exclude
        tombstoned records.

        Canonical records MUST NOT be physically deleted through persistent
        storage.  This is a frozen M4A invariant:

            "Deletion without tombstone → VIOLATION."
        """
        bucket = self._data.get(schema_id)
        if bucket is None or record_id not in bucket:
            raise KeyError(f"{schema_id}/{record_id}: not found")
        # Mark tombstoned instead of deleting from _data (history preserved)
        from datetime import datetime
        self._tombstones.setdefault(schema_id, {})[record_id] = {
            "reason": "",
            "authorizer": "",
            "timestamp": datetime.now().isoformat(),
        }

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
        # {record_id: reason} — supplements base-class _tombstones set
        self._tombstone_reasons: dict[str, str] = {}

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
        """Load raw blob — raises KeyError for tombstoned sources."""
        if record_id in self._tombstone_reasons:
            raise KeyError(f"{record_id}: tombstoned — use load_raw_blob_historical()")
        try:
            return self._raw_blobs[record_id]
        except KeyError:
            raise KeyError(f"{record_id}: no raw blob found")

    def load_raw_blob_historical(self, record_id: RecordID) -> bytes:
        """Load raw blob for audit/historical purposes — bypasses tombstone."""
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
        self._tombstone_reasons[record_id] = reason

        # Also mark in the base class tombstone metadata for every schema bucket
        for schema_id, schema_bucket in self._data.items():
            if record_id in schema_bucket:
                from datetime import datetime
                self._tombstones.setdefault(schema_id, {})[record_id] = {
                    "reason": reason,
                    "authorizer": "",
                    "timestamp": datetime.now().isoformat(),
                }
                # Do NOT delete from _data — history preserved for audit
                break

    def is_tombstoned(self, record_id: RecordID) -> bool:
        return record_id in self._tombstone_reasons

    def list_tombstoned_ids(self) -> list[RecordID]:
        return list(self._tombstone_reasons.keys())

    # -- Override load to reject tombstoned records -------------------------

    def load(self, schema_id: SchemaID, record_id: RecordID, /) -> BaseModel:
        if record_id in self._tombstone_reasons:
            raise KeyError(f"{schema_id}/{record_id}: tombstoned")
        if record_id in self._tombstones.get(schema_id, set()):
            raise KeyError(f"{schema_id}/{record_id}: tombstoned")
        return super().load(schema_id, record_id)

    # -- Extended snapshot/restore (covers RawSourceArchive-specific state) --

    def _snapshot(
        self,
    ) -> tuple[
        dict[str, dict[str, "_Record"]],
        dict[str, dict[str, dict]],
        dict[str, dict[str, dict[str, "_Record"]]],
        dict[str, int],
        dict[str, bytes],
        dict[str, dict[str, "_Record"]],
        dict[str, str],
    ]:
        """Deep-copy snapshot — extends base with raw-blob/version/tombstone state.

        Returns ``(data, tombstones, versions, version_counts, raw_blobs,
        version_data, tombstone_reasons)``.
        """
        base = super()._snapshot()
        return (
            *base,
            deepcopy(self._raw_blobs),
            deepcopy(self._version_data),
            deepcopy(self._tombstone_reasons),
        )

    def _restore(
        self,
        snapshot: tuple[
            dict[str, dict[str, "_Record"]],
            dict[str, dict[str, dict]],
            dict[str, dict[str, dict[str, "_Record"]]],
            dict[str, int],
            dict[str, bytes],
            dict[str, dict[str, "_Record"]],
            dict[str, str],
        ],
    ) -> None:
        """Restore — extends base to include RawSourceArchive-specific state."""
        (
            self._data,
            self._tombstones,
            self._versions,
            self._version_counts,
            self._raw_blobs,
            self._version_data,
            self._tombstone_reasons,
        ) = snapshot

    # -- Atomic source admission (Item 5) ----------------------------------

    def admit_source(
        self, instance: BaseModel, raw_bytes: bytes, /,
    ) -> CanonicalHash:
        """Atomically admit a SourceRecord with its raw bytes.

        Requirements (M5.2 Item 5):
        1. ``sha256(raw_bytes) == SourceRecord.content_hash`` **before**
           canonical admission — ``HashMismatch`` otherwise.
        2. Same ``source_id`` + identical raw bytes + same metadata →
           idempotent (return existing hash).
        3. Same ``source_id`` + identical raw bytes + changed metadata →
           legitimate metadata revision (SRC-01 is not RECORD_IMMUTABLE;
           mutable fields may update while content integrity holds).
        4. Same ``source_id`` + different raw bytes → ``IntegrityConflict``
           (\"content never edited in place\").
        5. Raw blob cannot be overwritten via ``store_raw_blob()`` after
           admission (enforced by guard in ``store_raw_blob``).
        6. Metadata + bytes are ONE admission unit: failure anywhere
           restores ALL state (data, raw_blobs, version_data, tombstones).

        Single-write vs batch admission
        --------------------------------
        This method admits ONE source at a time.  Batch source admission
        is possible by calling ``admit_source`` in a loop inside the
        caller's own snapshot/restore boundary, but M5.2 does not require
        cross-source batch atomicity (each source is independent).
        """
        import hashlib

        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _resolve_id(instance)

        # ---- Step 1: hash match ----
        content_hash = getattr(instance, "content_hash", None)
        actual_hash = hashlib.sha256(raw_bytes).hexdigest()
        if content_hash != actual_hash:
            raise HashMismatch(
                f"SourceRecord.content_hash ({content_hash}) != "
                f"sha256(raw_bytes) ({actual_hash})",
                record_id=record_id,
                expected_hash=content_hash,
                actual_hash=actual_hash,
            )

        # ---- Step 2: conflict / idempotency / revision check ----
        existing_meta = self._data.get("SRC-01", {}).get(record_id)
        existing_raw = self._raw_blobs.get(record_id)

        if existing_raw is not None:
            if existing_raw == raw_bytes:
                # Same bytes — admissible
                if existing_meta is not None:
                    existing_ch = existing_meta.canonical_hash
                    incoming_ch = compute_canonical_hash(instance)
                    if incoming_ch == existing_ch:
                        return existing_ch  # Idempotent
                    # Metadata revision — allow (SRC-01 is not RECORD_IMMUTABLE)
                    # Falls through to metadata update below
                else:
                    # Raw bytes exist without metadata — inconsistent state
                    # (shouldn't happen in normal flow, but protect against it)
                    raise IntegrityConflict(
                        f"SRC-01/{record_id}: raw bytes exist without matching "
                        f"SourceRecord metadata — inconsistent state",
                        schema_id=schema_id,
                        record_id=record_id,
                    )
            else:
                # Different raw bytes → content integrity violation
                raise IntegrityConflict(
                    f"SRC-01/{record_id}: content cannot be edited in place — "
                    f"already admitted with different raw bytes",
                    schema_id=schema_id,
                    record_id=record_id,
                    existing_hash=hashlib.sha256(existing_raw).hexdigest(),
                    incoming_hash=actual_hash,
                )

        # ---- Step 3: atomic admission (snapshot/restore) ----
        snapshot = self._snapshot()
        try:
            # 3a. Store SourceRecord metadata via Transaction (full validation)
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

            # 3b. Store raw bytes
            self._raw_blobs[record_id] = raw_bytes

            # 3c. Also set content_hash on already-existing SourceRecord
            #     metadata if it was a metadata revision (content_hash unchanged
            #     since we already validated it matches)
        except BaseException:
            self._restore(snapshot)
            raise

        return compute_canonical_hash(instance)

    # -- Guarded store_raw_blob (no overwrite of admitted content) ---------

    def store_raw_blob(
        self, record_id: RecordID, blob_hash: BlobHash, data: bytes,
    ) -> None:
        """Store raw blob — guarded against overwrite of admitted content.

        Raises
        ------
        IntegrityConflict
            If ``record_id`` already has an admitted raw blob.
        HashMismatch
            If ``blob_hash != sha256(data)`` OR, when a ``SourceRecord``
            already exists for this ``record_id``, if ``blob_hash`` does
            not match the record's ``content_hash``.
        """
        import hashlib

        # Guard 1: no overwrite of existing admitted raw blob
        if record_id in self._raw_blobs:
            raise IntegrityConflict(
                f"SRC-01/{record_id}: raw blob already admitted — "
                f"content cannot be overwritten",
                record_id=record_id,
            )

        actual = hashlib.sha256(data).hexdigest()
        if actual != blob_hash:
            raise HashMismatch(
                f"Blob hash mismatch: expected {blob_hash}, got {actual}",
                record_id=record_id,
                expected_hash=blob_hash,
                actual_hash=actual,
            )

        # Guard 2: if a SourceRecord already exists, blob_hash must match
        #          its content_hash
        existing_src = self._data.get("SRC-01", {}).get(record_id)
        if existing_src is not None:
            src_content_hash = getattr(existing_src.instance, "content_hash", None)
            if blob_hash != src_content_hash:
                raise HashMismatch(
                    f"Blob hash ({blob_hash}) does not match "
                    f"existing SourceRecord.content_hash ({src_content_hash})",
                    record_id=record_id,
                    expected_hash=src_content_hash,
                    actual_hash=blob_hash,
                )

        self._raw_blobs[record_id] = data


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

        For EV-01 evidence records, status changes are append-only (per
        M4A contract: ``Status changes are append-only``).  When only
        ``validation_status`` changes, the prior version is preserved and
        the new status is stored as a new version.  Since EV-01 is
        RECORD_IMMUTABLE, this bypasses the Transaction's immutability
        check and writes directly through versioned ``_write_record``.
        """
        from qad.persistence.immutability import _field_policy

        # Collect updates as a dict (avoids setattr on frozen Pydantic fields)
        # Apply all at once via model_copy(update=...) which bypasses frozen
        # field protection (frozen means "no setattr on instance", not
        # "cannot appear in constructor").  This is contract-safe because
        # the contract's immutable_policy controls write semantics through
        # the persistence layer — Pydantic frozen is a serialisation concern.
        updates: dict[str, Any] = {}
        changed = False

        for field_name in incoming.model_fields:
            if field_name == "schema_id":
                continue
            policy = _field_policy(schema_id, field_name)
            new_val = getattr(incoming, field_name)
            old_val = getattr(existing, field_name)

            if policy == "MUTABLE":
                if new_val != old_val:
                    updates[field_name] = new_val
                    changed = True

            # EV-01: validation_status changes are append-only (versioned)
            elif (
                schema_id == "EV-01"
                and field_name == "validation_status"
                and new_val != old_val
            ):
                updates[field_name] = new_val
                changed = True

        if not changed:
            # Idempotent — nothing to update
            return compute_canonical_hash(existing)

        # Apply all collected updates atomically via model_copy
        merged = existing.model_copy(update=updates)

        ch = compute_canonical_hash(merged)

        # For EV-01 status changes, preserve prior version and write directly.
        # EV-01 is RECORD_IMMUTABLE per contract descriptor, so the normal
        # Transaction path would reject the write.  We use a snapshot/restore
        # boundary here instead, providing the same atomicity guarantee as
        # Transaction._commit() — if _write_record fails, the store state
        # (including _versions, _data, _tombstones, _version_counts) is
        # restored to the pre-update snapshot.
        if schema_id == "EV-01":
            snapshot = self._snapshot()
            try:
                _save_version(self, schema_id, evidence_id,
                              _Record(instance=deepcopy(existing),
                                      canonical_hash=compute_canonical_hash(existing)))
                self._write_record(schema_id, evidence_id, merged, ch)
            except BaseException:
                self._restore(snapshot)
                raise
            return ch

        # Non-EV-01: commit via Transaction (standard path)
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


# ---------------------------------------------------------------------------
# Versioning helpers for APPEND_ONLY / APPEND_ONLY_STATE (M5.2 Item 4)
# ---------------------------------------------------------------------------

_APPEND_ONLY_SCHEMAS: set[str] = set()


def _load_append_only_schemas() -> set[str]:
    """Load the set of schema IDs that have APPEND_ONLY or APPEND_ONLY_STATE
    fields from the contract descriptor.  Cached in ``_APPEND_ONLY_SCHEMAS``
    after first call.

    Raises:
        PersistenceError: descriptor missing, corrupt, or unparseable
            (fail-closed — versioning must not silently disable).
    """
    global _APPEND_ONLY_SCHEMAS
    if _APPEND_ONLY_SCHEMAS:
        return _APPEND_ONLY_SCHEMAS
    import json
    from pathlib import Path
    from qad.persistence.errors import PersistenceError
    _path = (
        Path(__file__).resolve().parent.parent.parent
        / "qad" / "contract" / "contract_descriptor.json"
    )
    try:
        with open(_path) as _f:
            desc = json.load(_f)
    except FileNotFoundError:
        raise PersistenceError(
            f"Contract descriptor not found at {_path} — "
            f"versioned schema set unavailable (fail-closed)"
        )
    except json.JSONDecodeError as e:
        raise PersistenceError(
            f"Contract descriptor corrupt at {_path}: {e} — "
            f"versioned schema set unavailable (fail-closed)"
        )
    except Exception as e:
        raise PersistenceError(
            f"Failed to load contract descriptor: {e} — "
            f"versioned schema set unavailable (fail-closed)"
        )
    result: set[str] = set()
    for schema in desc.get("schemas", []):
        sid = schema["schema_id"]
        for field in schema.get("fields", []):
            policy = field.get("immutable_policy", "MUTABLE")
            if policy in ("APPEND_ONLY", "APPEND_ONLY_STATE"):
                result.add(sid)
                break
    _APPEND_ONLY_SCHEMAS = result
    return result


def _load_versioned_schemas() -> set[str]:
    """Return the set of schema IDs that require prior-version preservation.

    Derivation order:
    1. Schemas with any APPEND_ONLY / APPEND_ONLY_STATE field policy in
       the contract descriptor (machine-readable).
    2. SM-01 — requires versioning because its frozen M4A contract says
       ``Ticker changes create ticker_history entries`` and ``Corporate
       actions create new version with superseded_by pointer``, but the
       contract descriptor has no APPEND_ONLY field policies for SM-01
       (all fields are MUTABLE or FIELD_IMMUTABLE).  This is a known
       contract-metadata limitation: SM-01's versioning requirement is
       expressed in prose (``immutability_rules`` / ``revision_rules``)
       rather than machine-readable field policy.  Once the contract
       descriptor gains a ``revision_policy`` or ``versioned`` flag,
       SM-01 should derive from that flag instead.

    Raises:
        PersistenceError: descriptor missing, corrupt, or unparseable.
    """
    result = set(_load_append_only_schemas())  # copy — must not mutate cache
    # SM-01: contract-required versioning (see derivation note above)
    result.add("SM-01")
    return result


def _has_versioned_fields(schema_id: str) -> bool:
    """Return True if *schema_id* requires prior-version preservation.

    See ``_load_versioned_schemas()`` for derivation logic.
    """
    return schema_id in _load_versioned_schemas()


def _save_version(
    store: InMemoryCanonicalRecordStore,
    schema_id: str,
    record_id: str,
    existing: _Record,
) -> None:
    """Preserve *existing* as a prior version before overwrite.

    Uses a monotonic counter keyed by schema-qualified identity
    (``{schema_id}:{record_id}``) to prevent counter collision between
    different schemas that share the same record_id value.

    Version labels are zero-padded to 4 digits (``v0001``) so that
    ``list_versions()`` can sort numerically without relying on lexical
    ordering of a fixed-width scheme.

    The version label is stored in ``_versions[schema_id][record_id]``
    and the counter is incremented in ``_version_counts``.
    """
    counter_key = f"{schema_id}:{record_id}"
    version_count = store._version_counts.get(counter_key, 0) + 1
    store._version_counts[counter_key] = version_count
    version_label = f"v{version_count:04d}"
    store._versions.setdefault(schema_id, {}).setdefault(record_id, {})[
        version_label
    ] = _Record(
        instance=deepcopy(existing.instance),
        canonical_hash=existing.canonical_hash,
    )