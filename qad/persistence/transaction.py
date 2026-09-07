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
        commit_delete=my_store._remove_record,
        commit_snapshot=my_store._snapshot,
        commit_restore=my_store._restore,
    )

    for instance in batch:
        tx.add_store(instance)

    tx.execute()          # validate + commit (atomic)
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
# LIVE_CASE_UPDATE carrier validation (Erratum-002 / FD #137)
# ---------------------------------------------------------------------------
# SM-12 / PITC-01 require post-AS_OF evidence in LIVE_CASE_UPDATE mode to be
# explicitly tagged UPDATE with provenance.  EAR-01 now carries:
#   is_update            — bool flag
#   update_provenance    — free-text provenance (NOT an authorization token)
#   update_pit_context_id → PITC-01.pit_context_id  (machine-readable link)
# Deterministic semantics: if is_update = true, the referenced PITContext must
# EXIST, its mode MUST equal LIVE_CASE_UPDATE, and its created_by MUST represent
# Research Director authority (frozen SM-12).  Free-text provenance alone never
# grants LIVE access.


def _validate_live_update_carrier(
    instance: BaseModel,
    get_existing: Callable[[SchemaID, RecordID], BaseModel | None],
) -> None:
    """Validate EAR-01 LIVE_CASE_UPDATE provenance carrier (Erratum-002)."""
    dump = instance.model_dump(mode="python")
    is_update = dump.get("is_update")
    update_provenance = dump.get("update_provenance")
    update_pit_context_id = dump.get("update_pit_context_id")

    if not is_update:
        return  # not an update — no LIVE authorization claim

    problems: list[str] = []

    if not update_provenance:
        problems.append("is_update=true requires update_provenance")
    if not update_pit_context_id:
        problems.append("is_update=true requires update_pit_context_id")
        if problems:
            raise ValidationFailure(
                f"{instance.schema_id}: LIVE_CASE_UPDATE carrier invalid: {'; '.join(problems)}",
                schema_id=str(instance.schema_id),
                violations=problems,
            )
        return

    # Machine-readable PITContext link: must exist + be LIVE_CASE_UPDATE + RD-authorized
    pitc = get_existing("PITC-01", update_pit_context_id)
    if pitc is None:
        problems.append(
            f"update_pit_context_id {update_pit_context_id!r} does not reference an existing PITC-01"
        )
    else:
        pitc_dump = pitc.model_dump(mode="python")
        mode = getattr(pitc_dump.get("mode"), "value", pitc_dump.get("mode"))
        created_by = pitc_dump.get("created_by")
        if mode != "LIVE_CASE_UPDATE":
            problems.append(
                f"referenced PITC-01 {update_pit_context_id!r} mode={mode!r} "
                "is not LIVE_CASE_UPDATE"
            )
        # SM-12: LIVE_CASE_UPDATE authorized by Research Director.  The PITC
        # created_by must name the Research Director role for the update to be
        # authorized.  admitting_role is NOT the authority (admission vs LIVE
        # authorization are distinct concepts).
        if not created_by or "Research Director" not in str(created_by):
            problems.append(
                f"referenced PITC-01 {update_pit_context_id!r} created_by={created_by!r} "
                "does not represent Research Director authority"
            )

    if problems:
        raise ValidationFailure(
            f"{instance.schema_id}: LIVE_CASE_UPDATE carrier invalid: {'; '.join(problems)}",
            schema_id=str(instance.schema_id),
            violations=problems,
        )


def _check_rrm_contract_rules(
    instance: BaseModel,
    schema_id: str,
    record_id: RecordID,
) -> None:
    """Validate RRM-01 cross-field contract rules (Erratum-002 / FD #137).

    Frozen contract (QAD-M4A-CANONICAL-SCHEMAS.md I-1):
    * ``completion_time`` MUST be absent if ``run_state = RUNNING``
    * ``completion_time`` REQUIRED if ``run_state = COMPLETED`` or ``FAILED``

    Applies on first-write and on update (the immutability layer handles
    lifecycle transitions separately).
    """
    dump = instance.model_dump(mode="python")
    run_state = _enum_value(dump.get("run_state"))
    run_state_s = run_state if isinstance(run_state, str) else str(run_state)
    completion_time = dump.get("completion_time")

    problems: list[str] = []
    if run_state_s == "RUNNING" and completion_time is not None:
        problems.append("completion_time MUST be absent if run_state = RUNNING")
    elif run_state_s in ("COMPLETED", "FAILED") and completion_time is None:
        problems.append(
            f"completion_time REQUIRED if run_state = {run_state_s}"
        )

    if problems:
        raise ValidationFailure(
            f"{schema_id}/{record_id}: RRM-01 contract rule violation: {'; '.join(problems)}",
            schema_id=schema_id,
            record_id=record_id,
            violations=problems,
        )


def _enum_value(v: Any) -> Any:
    """Normalize a generated (str, Enum) member to its raw value."""
    return getattr(v, "value", v)

# ---------------------------------------------------------------------------
# Operation types
# ---------------------------------------------------------------------------

_Operation = tuple[str, Any, Any]  # (type, schema_id, record_or_pair)


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
    commit_snapshot:
        ``Callable[[], dict[str, Any]]`` — returns a deep-copy snapshot
        of the committed state *before* the commit begins.  Used for
        rollback if the commit fails partway.
    commit_restore:
        ``Callable[[dict[str, Any]], None]`` — restores committed state
        from a snapshot taken by ``commit_snapshot``.  Called only when
        a commit-phase failure occurs.
    """

    def __init__(
        self,
        *,
        store_contains: Callable[[SchemaID, RecordID], bool],
        commit_store: Callable[[SchemaID, RecordID, BaseModel, CanonicalHash], None],
        commit_delete: Callable[[SchemaID, RecordID], None],
        get_existing: Callable[[SchemaID, RecordID], BaseModel | None],
        get_existing_hash: Callable[[SchemaID, RecordID], str | None],
        commit_snapshot: (
            Callable[[], dict[str, Any]] | None
        ) = None,
        commit_restore: (
            Callable[[dict[str, Any]], None] | None
        ) = None,
    ) -> None:
        self._store_contains = store_contains
        self._commit_store = commit_store
        self._commit_delete = commit_delete
        self._get_existing = get_existing
        self._get_existing_hash = get_existing_hash
        self._commit_snapshot = commit_snapshot
        self._commit_restore = commit_restore
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

        # Phase 2: commit with rollback support
        snapshot = None
        if self._commit_snapshot:
            try:
                snapshot = self._commit_snapshot()
            except Exception:
                pass  # best-effort snapshot; we still try to commit

        commit_errors = self._commit(ops)
        if commit_errors:
            # Rollback: restore committed state from snapshot
            if snapshot is not None and self._commit_restore:
                try:
                    self._commit_restore(snapshot)
                except Exception as rb_err:
                    # Chain rollback error into the report
                    commit_errors.append(
                        PersistenceError(
                            f"Rollback after commit failure also failed: {rb_err}",
                        )
                    )
            raise TransactionFailure(
                f"Transaction commit failed with {len(commit_errors)} error(s)"
                + ("; rollback applied" if snapshot is not None and self._commit_restore else ""),
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

        # 5. RRM-01 cross-field contract rules (Erratum-002 / FD #137)
        # Validated on both first-write and update — the contract rules are
        # independent of the immutability lifecycle check.
        if schema_id == "RRM-01":
            _check_rrm_contract_rules(instance, schema_id, record_id)

        # 6. LIVE_CASE_UPDATE carrier validation (Erratum-002 / FD #137)
        if schema_id == "EAR-01":
            _validate_live_update_carrier(instance, self._get_existing)

    # ------------------------------------------------------------------
    # Phase 2 — commit
    # ------------------------------------------------------------------

    def _commit(self, ops: list[_Operation]) -> list[PersistenceError]:
        """Execute all write operations.  Returns errors (empty = success).

        Uses rollback callbacks (``commit_snapshot`` / ``commit_restore``)
        to guarantee atomicity.  If a commit-phase failure occurs after
        some records have been written, the snapshot is restored.
        """
        errors: list[PersistenceError] = []

        for optype, schema_id, payload in ops:
            try:
                if optype == "store":
                    rid, instance = payload
                    ch = compute_canonical_hash(instance)
                    self._commit_store(schema_id, rid, instance, ch)
                elif optype == "delete":
                    rid = payload
                    self._commit_delete(schema_id, rid)
            except PersistenceError as e:
                errors.append(e)
                break
            except Exception as e:
                errors.append(
                    PersistenceError(
                        f"Unexpected commit error: {e}",
                        schema_id=schema_id, record_id=rid,
                    )
                )
                break

        return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _record_id(instance: BaseModel) -> str:
    """Extract record primary identity.

    Uses the schema-specific identity-field resolution via the
    M4A-derived primary-identity registry.  Same resolution as
    ``qad.persistence.reference._resolve_id``.

    Must FAIL CLOSED when the authoritative mapping is unavailable — no
    heuristic FK fallback or synthetic identity.  See ``_resolve_id``
    for the full rationale.

    Raises
    ------
    PersistenceError
        If the authoritative primary-ID mapping is unavailable, or the
        mapped field is missing/None on the instance.
    """
    schema_id: str = getattr(instance, "schema_id", "")
    from qad.persistence.reference import _schema_identity_field

    identity_field = _schema_identity_field(schema_id)
    if identity_field is None:
        raise PersistenceError(
            f"{schema_id}: authoritative primary-ID mapping unavailable — "
            f"schema not found in primary-id registry",
            schema_id=schema_id,
        )
    val = getattr(instance, identity_field, None)
    if val is None:
        raise PersistenceError(
            f"{schema_id}: authoritative primary-ID field '{identity_field}' "
            f"is missing or None on instance",
            schema_id=schema_id,
        )
    return str(val)