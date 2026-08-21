"""M5.1 — Runtime Validator.
Validates schema instances against contract metadata.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, SCHEMA_FAMILIES


def validate_schema_instance(instance: object, schema_id: str | None = None) -> list[str]:
    """Validate a single schema instance against its frozen contract.
    Returns list of violation messages (empty = valid).
    At M5.1 scope: schema identity, field surface, enum, PIT/provenance metadata.
    """
    violations = []
    if schema_id is None:
        schema_id = getattr(instance, "schema_id", None)
    if schema_id is None:
        violations.append("Instance has no schema_id")
        return violations
    if schema_id not in SCHEMA_REGISTRY:
        violations.append(f"Unknown schema_id: {schema_id}")
        return violations
    model_class = SCHEMA_REGISTRY[schema_id]
    if not isinstance(instance, model_class):
        violations.append(f"Instance type {type(instance).__name__} does not match "
                          f"expected model {model_class.__name__} for {schema_id}")
    return violations


def validate_contract(schema_id: str, model_class: type) -> list[str]:
    """Validate a model class against basic contract metadata.
    Returns list of violations (empty = valid).
    """
    violations = []
    config = getattr(model_class, "model_config", {})
    if config.get("extra") != "forbid":
        violations.append(f"{schema_id}: missing extra=forbid")
    fi = model_class.model_fields.get("schema_id")
    if fi is None:
        violations.append(f"{schema_id}: missing schema_id field")
    elif not fi.frozen:
        violations.append(f"{schema_id}.schema_id not frozen")
    return violations


def get_all_schema_ids() -> list[str]:
    return sorted(SCHEMA_REGISTRY.keys())


def get_canonical_schema_ids() -> list[str]:
    return sorted(sid for sid in SCHEMA_REGISTRY if sid in CANONICAL_SCHEMAS)


def get_all_fk_pairs() -> list[tuple[str, str, str]]:
    pairs = []
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            pairs.append((sid, fk["target"], fk["field"]))
    return pairs


def get_schema_family(schema_id: str) -> str:
    """Return the family letter (A-I) for a schema."""
    return SCHEMA_FAMILIES.get(schema_id, "")