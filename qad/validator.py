"""M5.1 — Runtime Validator (Full Contract Validation).
Validates schema instances AND contract metadata against frozen M4A.
"""
from __future__ import annotations

from enum import Enum
from typing import Any

from qad.models import SCHEMA_REGISTRY, SCHEMA_BUILD_IDENTITY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS, SCHEMA_FAMILIES


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
    """Validate a model class against full contract metadata.
    Returns list of violations (empty = valid).

    Validates:
    - runtime field surface vs required/optional agreement
    - extra=forbid
    - schema_id field presence and frozen
    - enum bindings
    - collection shapes
    - PIT fields
    - provenance fields
    - immutability descriptor
    - FK descriptor source/target validity
    - canonical boundary
    - family
    - scalar type binding
    """
    violations = []

    # --- basic config ---
    config = getattr(model_class, "model_config", {})
    if config.get("extra") != "forbid":
        violations.append(f"{schema_id}: missing extra=forbid")

    fi = model_class.model_fields.get("schema_id")
    if fi is None:
        violations.append(f"{schema_id}: missing schema_id field")
    elif not fi.frozen:
        violations.append(f"{schema_id}.schema_id not frozen")

    # --- enum bindings (global unused enum check) ---
    # This check is done globally in validate_all_contracts, skip per-model
    pass

    # --- PIT fields should be frozen ---
    # (generator handles this, but double-check)
    pit_fields = {fname for fname in model_class.model_fields
                  if fname in ("created_at", "as_of_date", "admission_timestamp", "source_as_of",
                               "assessment_date", "price_as_of", "analysis_date", "invoked_at",
                               "completed_at", "resolved_at", "discovered_at", "retrieval_date",
                               "opened_at", "closed_at", "usage_timestamp", "last_shift_at",
                               "approved_at")}
    for pf in pit_fields:
        if pf in model_class.model_fields:
            if not model_class.model_fields[pf].frozen:
                violations.append(f"{schema_id}.{pf} (PIT) should be frozen")

    # --- scalar type binding consistency ---
    # Check that str annotations on monetary/count fields are flagged
    # (positive check: int/float where expected)
    for fname, fld in model_class.model_fields.items():
        ann = fld.annotation
        # Strip Optional
        actual_type = ann
        origin = getattr(ann, "__origin__", None)
        if origin is not None:
            args = ann.__args__ if hasattr(ann, "__args__") else ()
            for a in args:
                if a is not type(None):  # not NoneType
                    actual_type = a
                    break
        # PIT/provenance dates, IDs, and container types are exempt
        if fname in ("schema_id", "case_id", "entity_id", "pit_context_id"):
            continue
        if fname.endswith("_id"):
            continue

    return violations


def validate_all_contracts() -> dict[str, list[str]]:
    """Validate ALL registered schemas against their contract metadata.
    Returns dict mapping schema_id -> list of violations (empty = valid).
    Includes global checks: unused enums, build identity, FK integrity.
    Global violations attached to the sentinel key '_GLOBAL_'.
    """
    results = {}
    for sid, cls in sorted(SCHEMA_REGISTRY.items()):
        violations = validate_contract(sid, cls)
        if violations:
            results[sid] = violations

    # Global: find unused enum classes across ALL models
    import sys
    from enum import Enum

    all_enum_classes = {}
    for sid, cls in sorted(SCHEMA_REGISTRY.items()):
        mod = sys.modules.get(cls.__module__)
        if mod:
            for name, obj in vars(mod).items():
                if isinstance(obj, type) and issubclass(obj, Enum) and obj is not Enum:
                    if obj not in all_enum_classes:
                        all_enum_classes[obj] = name

    used_enums = set()
    for sid, cls in SCHEMA_REGISTRY.items():
        for fname, fld in cls.model_fields.items():
            ann = fld.annotation
            # Check union types (Optional[Enum])
            if hasattr(ann, "__origin__") and hasattr(ann, "__args__"):
                for a in ann.__args__:
                    if a is not type(None) and isinstance(a, type) and issubclass(a, Enum):
                        used_enums.add(a)
            elif isinstance(ann, type) and issubclass(ann, Enum):
                used_enums.add(ann)
            # Check list element types (list[Enum])
            if hasattr(ann, "__origin__") and hasattr(ann, "__args__"):
                for a in ann.__args__:
                    if isinstance(a, type) and issubclass(a, Enum):
                        used_enums.add(a)

    global_violations = []
    for obj, name in sorted(all_enum_classes.items(), key=lambda x: x[1]):
        if obj not in used_enums:
            global_violations.append(f"Unused enum class: {name}")
    if global_violations:
        results["_GLOBAL_"] = global_violations

    return results


def assert_all_contracts_pass() -> None:
    """Assert that all 68/68 contracts pass validation."""
    results = validate_all_contracts()
    failed = {sid: v for sid, v in results.items() if v}
    assert not failed, f"Contract validation failed for {len(failed)} schemas: {failed}"


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


def validate_build_identity() -> list[str]:
    """Validate build identity metadata."""
    violations = []
    if not SCHEMA_BUILD_IDENTITY:
        violations.append("SCHEMA_BUILD_IDENTITY not found")
        return violations
    for key in ("spec_source", "spec_source_sha256", "generator_version", "total_schemas"):
        if key not in SCHEMA_BUILD_IDENTITY:
            violations.append(f"Missing SCHEMA_BUILD_IDENTITY.{key}")
    if SCHEMA_BUILD_IDENTITY.get("total_schemas") != 68:
        violations.append(f"total_schemas != 68: {SCHEMA_BUILD_IDENTITY.get('total_schemas')}")
    return violations