"""M5.1 — Runtime Validator.
Deterministic validation of schema instances against frozen M4A contracts.
"""
from __future__ import annotations

from qad.schema_registry import SCHEMA_REGISTRY, FK_REGISTRY, CANONICAL_SCHEMAS


def validate_schema_instance(instance: object, schema_id: str | None = None) -> list[str]:
    """Validate a single schema instance against its frozen contract.
    Returns list of violation messages (empty = valid).
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


def validate_instance_collection(instances: dict[str, list[object]]) -> dict[str, list[str]]:
    """Validate a collection of instances keyed by schema_id.
    Returns dict of schema_id -> list of violations.
    """
    results = {}
    for sid, items in instances.items():
        for i, item in enumerate(items):
            violations = validate_schema_instance(item, sid)
            if violations:
                results.setdefault(sid, []).extend(f"[{i}] {v}" for v in violations)
    return results


def get_all_schema_ids() -> list[str]:
    """Return all registered schema IDs, sorted."""
    return sorted(SCHEMA_REGISTRY.keys())


def get_canonical_schema_ids() -> list[str]:
    """Return all canonical schema IDs, sorted."""
    return sorted(sid for sid in SCHEMA_REGISTRY if sid in CANONICAL_SCHEMAS)


def get_all_fk_pairs() -> list[tuple[str, str, str]]:
    """Return all FK pairs as (source_schema, target_schema, field_name)."""
    pairs = []
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            pairs.append((sid, fk["target"], fk["field"]))
    return pairs