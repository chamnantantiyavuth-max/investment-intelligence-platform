"""M5.1 — Schema Registry.
Thin convenience layer over generated SCHEMA_REGISTRY and contract artifacts.
"""
from __future__ import annotations

from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS, SCHEMA_FAMILIES, CANONICAL_BOUNDARY_TEXT


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
    """Return True if this is an infrastructure schema (Family I - Reproducibility & Operations).
    Infrastructure schemas are CANONICAL records in the operational domain.
    This is a FAMILY/function classification, not a deposit-of-truth classification.
    """
    return SCHEMA_FAMILIES.get(schema_id, "") == "I"


def get_family(schema_id: str) -> str:
    """Return the family letter (A-I) for a schema."""
    return SCHEMA_FAMILIES.get(schema_id, "")


def get_canonical_boundary(schema_id: str) -> str:
    """Return the exact canonical_boundary text from frozen M4A."""
    return CANONICAL_BOUNDARY_TEXT.get(schema_id, "")