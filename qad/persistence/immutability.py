"""Immutability policy enforcement for QAD persistence.

Reads immutability rules from the contract descriptor and enforces them
at write time.

Policy model (per field ``immutable_policy`` in contract descriptor)
--------------------------------------------------------------------
``MUTABLE``
    Field can be freely updated.

``FIELD_IMMUTABLE``
    After initial write, this specific field cannot be changed.
    Attempting to set a different value on an existing record raises
    ``ImmutabilityViolation``.  Setting the same value is a no-op.

``RECORD_IMMUTABLE``
    The entire record is frozen after creation.  Any update attempt
    (even with identical payload) raises ``ImmutabilityViolation``
    except when the existing payload is byte-identical (idempotent).

``APPEND_ONLY``
    New fields/values may be added but existing values cannot be changed.
    Updates to APPEND_ONLY fields are versioned — the prior record is
    preserved and a new version is created (see reference adapter
    ``_write_record``).  This is NOT a rejection — the versioning layer
    handles history preservation.

``APPEND_ONLY_STATE``
    State transitions are append-only: new values replace old in a
    monotonically forward direction.  Updates to APPEND_ONLY_STATE fields
    are versioned — the prior state is preserved and a new version is
    created.  This is NOT a rejection — the versioning layer handles
    history preservation.

Record-level rules
------------------
- **Same ID + same payload** → idempotent no-op (no error).
- **Same ID + different payload** (where record is immutable) →
  ``IntegrityConflict``.
- **Same ID + different payload** (where only some fields are immutable) →
  ``ImmutabilityViolation`` listing the changed immutable fields.

The contract descriptor's ``immutability_rules`` per-schema text is
carried as metadata for M5.3 conditional enforcement but is not parsed
here — the per-field ``immutable_policy`` values are the source of truth
for M5.1 enforcement.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from qad.persistence.errors import ImmutabilityViolation, IntegrityConflict
from qad.persistence.serialization import (
    compute_canonical_hash,
    serialize_to_canonical_bytes,
)

# ---------------------------------------------------------------------------
# Load contract descriptor
# ---------------------------------------------------------------------------

_BASE = Path(__file__).resolve().parent.parent.parent
_CONTRACT_PATH = _BASE / "qad" / "contract" / "contract_descriptor.json"

try:
    with open(_CONTRACT_PATH) as _f:
        _DESCRIPTOR = json.load(_f)["schemas"]
    _DESCRIPTOR_BY_ID = {s["schema_id"]: s for s in _DESCRIPTOR}
except Exception:
    _DESCRIPTOR_BY_ID = {}


def _field_policy(schema_id: str, field_name: str) -> str:
    """Return the immutable_policy for *field_name* in *schema_id*."""
    desc = _DESCRIPTOR_BY_ID.get(schema_id)
    if desc is None:
        return "MUTABLE"
    for field in desc.get("fields", []):
        if field["name"] == field_name:
            return field.get("immutable_policy", "MUTABLE")
    return "MUTABLE"


def _get_immutability_rules(schema_id: str) -> str:
    """Return the raw immutability_rules text for a schema."""
    desc = _DESCRIPTOR_BY_ID.get(schema_id, {})
    return desc.get("immutability_rules", "")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_immutability(
    schema_id: str,
    record_id: str,
    incoming: BaseModel,
    existing: BaseModel | None,
    *,
    existing_canonical_hash: str | None = None,
) -> None:
    """Enforce immutability constraints on a store operation.

    Parameters
    ----------
    schema_id:
        M4A schema identifier.
    record_id:
        Primary identity of the record.
    incoming:
        The new (or first) instance being stored.
    existing:
        The previously stored record, or ``None`` if this is an insert.
    existing_canonical_hash:
        Pre-computed canonical hash of the existing record.  If not
        provided it is computed on demand.

    Raises
    ------
    IntegrityConflict
        Same ID, different payload, but record-level immutability
        (``RECORD_IMMUTABLE``) would be violated.
    ImmutabilityViolation
        Specific immutable fields were changed.
    """
    # -- First write: no constraint on fresh records --
    if existing is None:
        return

    incoming_hash = compute_canonical_hash(incoming)
    existing_hash = existing_canonical_hash or compute_canonical_hash(existing)

    # -- Idempotent: same ID + same payload --
    if incoming_hash == existing_hash:
        return

    # -- Detect record-level immutability --
    desc = _DESCRIPTOR_BY_ID.get(schema_id, {})
    all_policies = {
        field["name"]: field.get("immutable_policy", "MUTABLE")
        for field in desc.get("fields", [])
    }

    record_immutable = any(
        policy == "RECORD_IMMUTABLE" for policy in all_policies.values()
    )

    if record_immutable:
        raise IntegrityConflict(
            f"{schema_id}/{record_id}: record is RECORD_IMMUTABLE — "
            f"cannot replace existing payload "
            f"(existing={existing_hash[:12]}, incoming={incoming_hash[:12]})",
            schema_id=schema_id,
            record_id=record_id,
            existing_hash=existing_hash,
            incoming_hash=incoming_hash,
        )

    # -- Field-level immutability check --
    violated_fields: list[str] = []
    incoming_dump = incoming.model_dump(mode="python")
    existing_dump = existing.model_dump(mode="python")

    for field_name, policy in all_policies.items():
        if policy in ("FIELD_IMMUTABLE",):
            new_val = incoming_dump.get(field_name)
            old_val = existing_dump.get(field_name)
            if new_val != old_val:
                violated_fields.append(field_name)

    if violated_fields:
        raise ImmutabilityViolation(
            f"{schema_id}/{record_id}: cannot change immutable fields: "
            f"{violated_fields}",
            schema_id=schema_id,
            record_id=record_id,
            violated_fields=violated_fields,
        )

    # APPEND_ONLY / APPEND_ONLY_STATE — noted for M5.3 enforcement
    # (Currently treated as mutable at M5.1 scope.)


def check_field_immutable(
    schema_id: str,
    field_name: str,
) -> bool:
    """Return True if *field_name* is declared immutable (any policy) for
    *schema_id*."""
    policy = _field_policy(schema_id, field_name)
    return policy in ("FIELD_IMMUTABLE", "RECORD_IMMUTABLE",
                      "APPEND_ONLY", "APPEND_ONLY_STATE")


def is_record_immutable(schema_id: str) -> bool:
    """Return True if every field in *schema_id* uses RECORD_IMMUTABLE."""
    desc = _DESCRIPTOR_BY_ID.get(schema_id, {})
    policies = {
        field.get("immutable_policy", "MUTABLE")
        for field in desc.get("fields", [])
    }
    return policies == {"RECORD_IMMUTABLE"}


def get_immutability_rules_text(schema_id: str) -> str:
    """Return the human-readable immutability rules text for a schema."""
    return _get_immutability_rules(schema_id)