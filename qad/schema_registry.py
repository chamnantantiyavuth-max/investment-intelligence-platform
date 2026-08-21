"""M5.1 — Schema Registry.
Auto-generated from M4A parser output. See qad/contract/ for source.
"""
from __future__ import annotations

from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS


def resolve_fk(schema_id: str, field_name: str) -> str | None:
    """Resolve a field name to its FK target schema. Returns target schema_id or None."""
    fks = FK_REGISTRY.get(schema_id, [])
    for fk in fks:
        if fk["field"] == field_name:
            return fk["target"]
    return None


def is_canonical(schema_id: str) -> bool:
    """Return True if the schema is canonical (source of truth)."""
    return schema_id in CANONICAL_SCHEMAS


def is_infrastructure(schema_id: str) -> bool:
    """Return True if the schema is infrastructure (non-canonical operational metadata)."""
    return schema_id in NON_CANONICAL_SCHEMAS