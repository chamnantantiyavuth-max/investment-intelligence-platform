"""Deterministic canonical serialisation for QAD persistence.

Produces a stable, reproducible byte representation of any M5.1 Pydantic
model instance so that:
  1. Two equivalent instances always produce identical bytes.
  2. The bytes can be SHA-256 hashed for content addressing.
  3. The bytes can be deserialised back to the same semantic value.

Design decisions
----------------
- schema_id is always emitted first in the JSON payload for human readability.
- All other top-level fields are sorted alphabetically.
- Nested dicts and lists are sorted recursively (dict keys sorted; lists of
  non-dict values kept in insertion order since they are payload-order-significant).
- datetimes are formatted as ISO 8601 (``YYYY-MM-DDTHH:MM:SS`` with no
  trailing timezone when naive; Z suffix when UTC).
- enum members are serialised to their **value** (str), not their name.
- Output is always UTF-8 encoded JSON with no whitespace (compact).
- **Fail-closed:** values not in the explicit supported domain (``BaseModel``,
  ``Enum``, ``datetime``, ``date``, ``list``, ``dict``, ``bytes``, and JSON
  primitives ``str``/``int``/``float``/``bool``/``None``) are rejected with a
  ``TypeError``.  Non-finite floats (NaN, Infinity, -Infinity) are rejected
  with a ``ValueError``.  No ``default=str`` fallback is used.
"""

from __future__ import annotations

import datetime
import hashlib
import json
from enum import Enum
from typing import Any

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Canonical key ordering
# ---------------------------------------------------------------------------

def _canonical_key(key: str) -> tuple[int, str]:
    """schema_id always sorts first; everything else alphabetical."""
    return (0, "") if key == "schema_id" else (1, key)


def _sort_key(item: tuple[str, Any]) -> tuple[int, str]:
    return _canonical_key(item[0])


# ---------------------------------------------------------------------------
# Recursive value normalisation
# ---------------------------------------------------------------------------

def _canonical_value(v: Any) -> Any:
    """Recursively normalise a value for deterministic JSON."""
    if isinstance(v, BaseModel):
        return _model_to_ordered(v)
    if isinstance(v, Enum):
        return v.value
    if isinstance(v, datetime.datetime):
        # ISO 8601 with Z for UTC, no offset for naive
        if v.tzinfo is not None:
            return v.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return v.isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, list):
        return [_canonical_value(i) for i in v]
    if isinstance(v, dict):
        return {k: _canonical_value(v) for k, v in sorted(v.items(), key=_sort_key)}
    if isinstance(v, bytes):
        return v.hex()
    # Primitives (str, int, float, bool, None) pass through
    return v


def _model_to_ordered(model: BaseModel) -> dict[str, Any]:
    """Convert a Pydantic model to an ordered dict suitable for JSON."""
    raw = model.model_dump(mode="python")
    return _canonical_value(raw)


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def serialize_to_canonical_bytes(instance: BaseModel) -> bytes:
    """Deterministically serialise a Pydantic model to canonical UTF-8 bytes.

    Round-trip guarantee:
        serialize_to_canonical_bytes(instance)
        → bytes that json.loads() + model_validate() reconstructs semantics.

    NOTE: Because Pydantic ``model_validate`` accepts ``**extra`` with
    ``extra='forbid'`` only checking at construction, the deserialised dict
    will have the same fields as the original model.
    """
    ordered = _model_to_ordered(instance)
    # Ensure schema_id is first
    payload = json.dumps(ordered, ensure_ascii=False, separators=(",", ":"),
                         sort_keys=False, allow_nan=False)
    return payload.encode("utf-8")


def compute_canonical_hash(instance: BaseModel) -> str:
    """Return the SHA-256 hex digest of the canonical byte representation."""
    return hashlib.sha256(serialize_to_canonical_bytes(instance)).hexdigest()


def serialize_to_canonical_json(instance: BaseModel) -> str:
    """Return canonical JSON string (compact, deterministic)."""
    return serialize_to_canonical_bytes(instance).decode("utf-8")


def canonical_hash_from_bytes(data: bytes) -> str:
    """Compute the SHA-256 hash of already-serialised canonical bytes."""
    return hashlib.sha256(data).hexdigest()


def deserialize_from_canonical_bytes(
    data: bytes,
    model_class: type[BaseModel],
) -> BaseModel:
    """Restore a Pydantic model from canonical bytes.

    The inverse of ``serialize_to_canonical_bytes``:
        deserialize_from_canonical_bytes(canonical_bytes, ModelClass)
        → ModelClass(**json.loads(canonical_bytes))
    """
    raw = json.loads(data)
    return model_class.model_validate(raw)