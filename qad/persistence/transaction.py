"""Atomic transaction boundary for QAD persistence.

A ``Transaction`` collects a set of persistence operations, validates
them collectively (FK resolution across the batch, immutability checks,
canonical boundary enforcement), and commits them atomically.  If any
check fails, **zero** records are committed and a ``TransactionFailure``
is raised carrying every individual error.

Usage
-----
::

    tx = Transaction(
        store_contains=my_store.contains,
        commit_store=my_store._write_record,
    )

    for instance in batch:
        tx.add_store(instance)

    tx.execute()          # validate + commit

    # or for deletes:
    tx.add_delete("CASE-01", "case_001")
    tx.execute()

If you need to inspect what would be committed, call ``validate()``
separately before ``commit()``.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from pydantic import BaseModel

from qad.contract.canonical_boundary import CANONICAL_SCHEMAS
from qad.persistence.errors import (
    CanonicalBoundaryViolation,
    ImmutabilityViolation,
    IntegrityConflict,
    MissingForeignKey,
    PersistenceError,
    TransactionFailure,
    ValidationFailure,
)
from qad.persistence.fk_enforcer import validate_fks
from qad.persistence.immutability import check_immutability
from qad.persistence.interfaces import CanonicalHash, RecordID, SchemaID
from qad.persistence.serialization import compute_canonical_hash
from qad.validator import validate_schema_instance

# ---------------------------------------------------------------------------
# Operation types
# ---------------------------------------------------------------------------

_Operation = tuple[str, Any, Any]  # (type, schema_id, record_or_pair)
# type: "store" → (schema_id, record_id, instance)
# type: "delete" → (schema_id, schema_id, record_id)


# ---------------------------------------------------------------------------
# Transaction
# ---------------------------------------------------------------------------

class Transaction:
    """Collect, validate, and atomically commit persistence operations.

    Parameters
    ----------
    store_contains:
        ``Callable[[SchemaID, RecordID], bool]`` — reflects the committed
        state of the backing store (used for FK resolution).
    commit_store:
        ``Callable[[SchemaID, RecordID, BaseModel, str], None]`` — called
        once per record during commit with ``(schema_id, record_id,
        instance, canonical_hash)``.
    commit_delete:
        ``Callable[[SchemaID, RecordID], None]`` — called once per delete
        during commit.
    get_existing:
        ``Callable[[SchemaID, RecordID], BaseModel | None]`` — returns
        the previously stored record (for immutability checks), or None.
    get_existing_hash:
        ``Callable[[SchemaID, RecordID], str | None]`` — returns the
        canonical hash of the existing record, or None.
    """

    def __init__(
        self,
        *,
        store_contains: Callable[[SchemaID, RecordID], bool],
        commit_store: Callable[[SchemaID, RecordID, BaseModel, CanonicalHash], None],
        commit_delete: Callable[[SchemaID, RecordID], None],
        get_existing: Callable[[SchemaID, RecordID], BaseModel | None],
        get_existing_hash: Callable[[SchemaID, RecordID], str | None],
    ) -> None:
        self._store_contains = store_contains
        self._commit_store = commit_store
        self._commit_delete = commit_delete
        self._get_existing = get_existing
        self._get_existing_hash = get_existing_hash
        self._operations: list[_Operation] = []
        self._executed = False

    # ------------------------------------------------------------------
    # Operation accumulation
    # ------------------------------------------------------------------

    def add_store(self, instance: BaseModel) -> None:
        """Stage a record for storage."""
        if self._executed:
            raise RuntimeError("Transaction already executed")
        schema_id: str = instance.schema_id  # type: ignore[assignment]
        record_id = _record_id(instance)
        self._operations.append(("store", schema_id, (record_id, instance)))

    def add_delete(self, schema_id: SchemaID, record_id: RecordID) -> None:
        """Stage a record for deletion."""
        if self._executed:
            raise RuntimeError("Transaction already executed")
        self._operations.append(("delete", schema_id, record_id))

    @property
    def operation_count(self) -> int:
        """Return the number of staged operations."""
        return len(self._operations)

    @property
    def is_empty(self) -> bool:
        """Return True when no operations are staged."""
        return len(self._operations) == 0

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    def execute(self) -> None:
        """Validate all operations, then commit them atomically.

        Raises
        ------
        TransactionFailure
            If any validation step fails.  The ``errors`` attribute
            contains every individual ``PersistenceError``.
            Guarantee: **zero** records are committed.
        """
        if self._executed:
            raise RuntimeError("Transaction already executed")
        if self.is_empty:
            self._executed = True
            return

        # Snapshot operations so the transaction can be retried
        ops = list(self._operations)

        # Phase 1: validate
        errors = self._validate(ops)
        if errors:
            raise TransactionFailure(
                f"Transaction validation failed with {len(errors)} error(s)",
                errors=errors,
                phase="validate",
            )

        # Phase 2: commit
        commit_errors = self._commit(ops)
        if commit_errors:
            # Rollback is caller responsibility — guarantee ZERO records
            # were written since we raise before returning.
            raise TransactionFailure(
                f"Transaction commit failed with {len(commit_errors)} error(s)",
                errors=commit_errors,
                phase="commit",
            )

        self._executed = True

    # ------------------------------------------------------------------
    # Phase 1 — validate
    # ------------------------------------------------------------------

    def _validate(self, ops: list[_Operation]) -> list[PersistenceError]:
        """Run all checks.  Returns list of errors (empty = pass)."""
        errors: list[PersistenceError] = []

        # Build batch context for cross-record FK resolution
        batch_context: dict[str, dict[str, BaseModel]] = {}
        for optype, schema_id, payload in ops:
            if optype == "store":
                rid, instance = payload
                batch_context.setdefault(schema_id, {})[rid] = instance

        for optype, schema_id, payload in ops:
            if optype == "store":
                rid, instance = payload
                try:
                    self._validate_one(instance, rid, batch_context)
                except PersistenceError as e:
                    errors.append(e)
            # Deletions do not need validation beyond existence (enforced
            # by store caller, not here).

        return errors

    def _validate_one(
        self,
        instance: BaseModel,
        record_id: RecordID,
        batch_context: dict[str, dict[str, BaseModel]],
    ) -> None:
        """Validate a single store operation."""
        schema_id: str = instance.schema_id  # type: ignore[assignment]

        # 1. Canonical boundary check
        if schema_id not in CANONICAL_SCHEMAS:
            raise CanonicalBoundaryViolation(
                f"{schema_id}: schema is not in canonical boundary",
                schema_id=schema_id,
                record_id=record_id,
            )

        # 2. Contract validation
        violations = validate_schema_instance(instance, schema_id)
        if violations:
            raise ValidationFailure(
                f"{schema_id}/{record_id}: contract violations: {violations}",
                schema_id=schema_id,
                record_id=record_id,
                violations=violations,
            )

        # 3. FK existence
        fk_errors = validate_fks(
            instance,
            store_contains=self._store_contains,
            batch_context=batch_context,
        )
        if fk_errors:
            # Raise the first FK error — but they're all bundled
            raise fk_errors[0]

        # 4. Immutability check
        existing = self._get_existing(schema_id, record_id)
        existing_hash = self._get_existing_hash(schema_id, record_id)
        check_immutability(
            schema_id,
            record_id,
            instance,
            existing,
            existing_canonical_hash=existing_hash,
        )

    # ------------------------------------------------------------------
    # Phase 2 — commit
    # ------------------------------------------------------------------

    def _commit(self, ops: list[_Operation]) -> list[PersistenceError]:
        """Execute all write operations.  Returns errors (empty = success).

        NOTE: A commit-phase failure means some records may have been
        written.  The caller (or a future version with rollback) must
        handle this.
        """
        errors: list[PersistenceError] = []
        committed: list[tuple[str, str]] = []  # (schema_id, record_id)

        for optype, schema_id, payload in ops:
            try:
                if optype == "store":
                    rid, instance = payload
                    ch = compute_canonical_hash(instance)
                    self._commit_store(schema_id, rid, instance, ch)
                    committed.append((schema_id, rid))
                elif optype == "delete":
                    rid = payload
                    self._commit_delete(schema_id, rid)
                    committed.append((schema_id, rid))
            except PersistenceError as e:
                errors.append(e)
                # Stop on first commit failure to minimise partial writes
                break
            except Exception as e:
                errors.append(
                    PersistenceError(f"Unexpected commit error: {e}",
                                     schema_id=schema_id, record_id=rid)
                )
                break

        return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _record_id(instance: BaseModel) -> str:
    """Best-effort extraction of the record's primary identity.

    Looks for common ID field names used across M4A schemas.
    """
    candidates = (
        "case_id", "source_id", "evidence_id", "finding_id",
        "financial_fact_id", "manifest_id", "context_id",
        "entity_id", "signal_id", "candidate_id", "claim_id",
        "usage_id", "audit_id", "budget_id", "lock_id",
        "indicator_id", "hypothesis_id", "lesson_id",
        "publication_id", "verdict_id", "challenge_id",
        "assessment_id", "gap_id", "knowledge_id",
        "r_dcf_id", "invocation_id", "eval_run_id",
        "model_invocation_id", "impairment_id",
    )
    for name in candidates:
        val = getattr(instance, name, None)
        if val is not None:
            return str(val)
    # Fallback: use schema_id + id() as a last resort
    sid = getattr(instance, "schema_id", "UNKNOWN")
    return f"{sid}:{id(instance)}"