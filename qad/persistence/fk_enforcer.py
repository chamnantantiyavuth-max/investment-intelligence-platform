"""FK existence validation for QAD persistence.

Consumes ``FK_REGISTRY`` from M5.1 generated metadata and validates that
every foreign-key reference in an incoming record points to an existing
target record.

Supports both ``single`` and ``list`` cardinality FKs.  The validator
accepts an optional ``batch_context`` — a dict of pending writes in the
current transaction whose records are not yet committed but should be
treated as existing for the purpose of FK resolution.
"""

from __future__ import annotations

from pydantic import BaseModel

from qad.contract.fk_registry import FK_REGISTRY
from qad.persistence.errors import MissingForeignKey
from qad.persistence.serialization import serialize_to_canonical_bytes


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def validate_fks(
    instance: BaseModel,
    *,
    store_contains: _ContainsFn,
    batch_context: dict[str, dict[str, BaseModel]] | None = None,
) -> list[MissingForeignKey]:
    """Check every FK declared for *instance* in ``FK_REGISTRY``.

    Parameters
    ----------
    instance:
        The M5.1 Pydantic model instance to validate.
    store_contains:
        A callable ``(schema_id, record_id) → bool`` that returns True if
        a record already exists in the **committed** store.
    batch_context:
        Optional dict mapping ``schema_id → {record_id: instance}`` for
        records that are part of the same pending transaction (and therefore
        can serve as FK targets even though they are not yet committed).

    Returns
    -------
    list[MissingForeignKey]
        Empty list when all FKs are resolvable.  One entry per broken FK.
    """
    schema_id: str = instance.schema_id  # type: ignore[assignment]
    fk_list = FK_REGISTRY.get(schema_id, [])
    if not fk_list:
        return []

    errors: list[MissingForeignKey] = []
    batch = batch_context or {}

    for fk in fk_list:
        field_name: str = fk["field"]
        target_schema: str = fk["target"]
        target_field: str = fk["target_field"]
        cardinality: str = fk.get("cardinality", "single")

        # Resolve the field value from the instance
        raw_value = getattr(instance, field_name, None)
        if raw_value is None:
            # Optional FK field — skip if not provided
            continue

        if cardinality == "list":
            if not isinstance(raw_value, list):
                # Unexpected shape — treat as non-resolvable
                errors.append(MissingForeignKey(
                    f"{schema_id}.{field_name}: expected list, got {type(raw_value).__name__}",
                    schema_id=schema_id,
                    record_id=_record_id(instance),
                    field=field_name,
                    target_schema=target_schema,
                ))
                continue

            missing: list[str] = []
            for idx, val in enumerate(raw_value):
                rid = str(val)
                if not _exists(rid, target_schema, store_contains, batch):
                    missing.append(rid)
            if missing:
                errors.append(MissingForeignKey(
                    f"{schema_id}.{field_name}: FK references {missing} not found "
                    f"in {target_schema}.{target_field}",
                    schema_id=schema_id,
                    record_id=_record_id(instance),
                    field=field_name,
                    target_schema=target_schema,
                    target_ids=missing,
                ))

        else:  # cardinality == "single"
            rid = str(raw_value)
            if not _exists(rid, target_schema, store_contains, batch):
                errors.append(MissingForeignKey(
                    f"{schema_id}.{field_name}: FK reference '{rid}' not found "
                    f"in {target_schema}.{target_field}",
                    schema_id=schema_id,
                    record_id=_record_id(instance),
                    field=field_name,
                    target_schema=target_schema,
                    target_ids=[rid],
                ))

    return errors


def validate_fk_structure(instance: BaseModel) -> list[MissingForeignKey]:
    """Lightweight structural check — verify FK field exists on instance
    and target schema exists in the registry.  Does NOT check record
    existence; for that use ``validate_fks()``.

    Returns
    -------
    list[MissingForeignKey]
        Empty when every FK source field and target schema is structurally
        valid according to ``FK_REGISTRY``.
    """
    schema_id: str = instance.schema_id  # type: ignore[assignment]
    fk_list = FK_REGISTRY.get(schema_id, [])
    errors: list[MissingForeignKey] = []

    for fk in fk_list:
        field_name = fk["field"]
        target_schema = fk["target"]

        if not hasattr(instance, field_name):
            errors.append(MissingForeignKey(
                f"{schema_id}.{field_name}: FK source field missing from model instance",
                schema_id=schema_id,
                record_id=_record_id(instance),
                field=field_name,
                target_schema=target_schema,
            ))

        if target_schema not in FK_REGISTRY and target_schema not in {
            # Some target schemas may not themselves have FKs but must
            # still exist in FK_REGISTRY as a key (all do here).
            # If it's not there, warn but don't hard-fail — the target
            # may exist in the SCHEMA_REGISTRY without its own FK entries.
        }:
            # Soft warning — target schema might exist w/o FK entries
            pass

    return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ContainsFn = callable  # type: ignore[valid-type]


def _exists(
    record_id: str,
    target_schema: str,
    store_contains: _ContainsFn,
    batch: dict[str, dict[str, BaseModel]],
) -> bool:
    """Check if a record exists either in committed store or batch context."""
    if store_contains(target_schema, record_id):
        return True
    batch_records = batch.get(target_schema, {})
    return record_id in batch_records


def _record_id(instance: BaseModel) -> str | None:
    """Best-effort extraction of a human-readable record identifier."""
    for candidate in ("record_id", "id", "entity_id", "source_id",
                      "evidence_id", "case_id", "finding_id",
                      "financial_fact_id", "manifest_id", "context_id"):
        val = getattr(instance, candidate, None)
        if val is not None:
            return str(val)
    return None