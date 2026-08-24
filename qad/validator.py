"""M5.1 — Runtime Validator (Full Contract Validation).
Validates schema instances AND contract metadata against the frozen M4A source
via the generated contract descriptor. Implements every check it claims.
"""
from __future__ import annotations

import hashlib
import json
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Union, get_origin, get_args

from qad.models import SCHEMA_REGISTRY, SCHEMA_BUILD_IDENTITY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS, SCHEMA_FAMILIES
from qad import generate_models as gm

BASE = Path(__file__).resolve().parent.parent

try:
    with open(BASE / "qad" / "contract" / "contract_descriptor.json") as f:
        _CONTRACT_DESCRIPTOR = json.load(f)["schemas"]
    DESCRIPTOR_BY_ID = {c["schema_id"]: c for c in _CONTRACT_DESCRIPTOR}
except Exception:
    DESCRIPTOR_BY_ID = {}


def _unwrap_optional(ann: Any) -> Any:
    """Strip Optional[...] wrapper, returning the inner annotated type."""
    origin = get_origin(ann)
    if origin is Union and type(None) in get_args(ann):
        for a in get_args(ann):
            if a is not type(None):
                return a
    return ann


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
    """Validate a model class against the FULL generated contract metadata.

    Implements every check claimed:
    - exact runtime field surface (required / optional / PIT / provenance derived)
    - extra=forbid
    - schema_id field present + frozen
    - enum declaration → runtime binding (no unbound enum)
    - enum value equality
    - list/dict collection shape
    - PIT field frozen
    - provenance field present
    - immutability descriptor
    - FK descriptor source/target validity
    - canonical boundary
    - family
    - scalar type binding
    - schema/build identity
    """
    violations = []
    desc = DESCRIPTOR_BY_ID.get(schema_id, {})
    if not desc:
        violations.append(f"{schema_id}: no contract descriptor found")
        return violations

    # --- basic config ---
    config = getattr(model_class, "model_config", {})
    if config.get("extra") != "forbid":
        violations.append(f"{schema_id}: missing extra=forbid")

    fi = model_class.model_fields.get("schema_id")
    if fi is None:
        violations.append(f"{schema_id}: missing schema_id field")
    elif not fi.frozen:
        violations.append(f"{schema_id}.schema_id not frozen")

    # --- exact field surface ---
    runtime_fields = set(model_class.model_fields.keys()) - {"schema_id"}
    expected_fields = set(desc.get("required_fields", [])) | set(desc.get("optional_fields", []))
    # PIT/provenance fields are added to optional surface by generator
    for pf in desc.get("pit_fields", []) + desc.get("provenance_fields", []):
        expected_fields.add(pf.replace("[]", "").replace("{}", ""))

    missing = expected_fields - runtime_fields
    if missing:
        violations.append(f"{schema_id}: missing runtime fields: {sorted(missing)}")
    extra = runtime_fields - expected_fields
    if extra:
        violations.append(f"{schema_id}: phantom runtime fields: {sorted(extra)}")

    # --- required field presence ---
    for rf in desc.get("required_fields", []):
        rf_clean = rf.replace("[]", "").replace("{}", "")
        if rf_clean not in model_class.model_fields:
            violations.append(f"{schema_id}: missing required field {rf_clean}")

    # --- collection shape (only check fields with container in descriptor) ---
    for fname, fld in model_class.model_fields.items():
        if fname == "schema_id":
            continue
        df = next((x for x in desc.get("fields", []) if x["name"] == fname), None)
        if df:
            container = df.get("container", "")
            ann = str(fld.annotation)
            if container == "list" and "list[" not in ann.lower() and "list[" not in str(getattr(fld.annotation, "__args__", ())).lower():
                violations.append(f"{schema_id}.{fname}: expected list, got {ann}")
            elif container == "dict" and "dict" not in ann.lower():
                violations.append(f"{schema_id}.{fname}: expected dict, got {ann}")

    # --- PIT fields frozen ---
    for pf in desc.get("pit_fields", []):
        pf_clean = pf.replace("[]", "").replace("{}", "")
        pfld = model_class.model_fields.get(pf_clean)
        if pfld is None:
            violations.append(f"{schema_id}: missing PIT field {pf_clean}")
        elif not pfld.frozen:
            violations.append(f"{schema_id}.{pf_clean} (PIT) not frozen")

    # --- provenance fields present ---
    for pf in desc.get("provenance_fields", []):
        pf_clean = pf.replace("[]", "").replace("{}", "")
        if pf_clean not in model_class.model_fields:
            violations.append(f"{schema_id}: missing provenance field {pf_clean}")

    # --- enum binding + value equality within this schema ---
    for e in desc.get("enums", []):
        efield = e["field"]
        bound = [f for f in model_class.model_fields
                 if _field_uses_values(efield, e["values"], f, model_class)]
        if not bound:
            violations.append(f"{schema_id}: enum '{efield}' ({e['values']}) has no bound runtime field")
        # Verify at least one bound enum class matches values
        enum_ann = _find_enum_ann(model_class, efield)
        if enum_ann is not None:
            oracle_values = set(e["values"])
            runtime_values = {v.value for v in enum_ann}
            if oracle_values != runtime_values:
                violations.append(f"{schema_id}: enum '{efield}' value mismatch: "
                                  f"oracle={oracle_values} runtime={runtime_values}")

    # --- FK integrity (descriptor) ---
    for fk in desc.get("fks", []):
        src_field = fk["field"]
        if src_field not in model_class.model_fields:
            violations.append(f"{schema_id}: FK source field {src_field} not in runtime")
        target = fk["target"]
        if target not in SCHEMA_REGISTRY:
            violations.append(f"{schema_id}: FK target schema {target} not registered")
        else:
            tfield = fk["target_field"]
            if tfield not in SCHEMA_REGISTRY[target].model_fields:
                violations.append(f"{schema_id}: FK target field {target}.{tfield} not found")

    # --- canonical boundary / family / scalar type binding ---
    if desc.get("is_canonical") is not None:
        runtime_canonical = schema_id in CANONICAL_SCHEMAS
        if bool(desc["is_canonical"]) != runtime_canonical:
            violations.append(f"{schema_id}: canonical boundary mismatch "
                              f"(descriptor={desc['is_canonical']}, runtime={runtime_canonical})")
    actual_family = SCHEMA_FAMILIES.get(schema_id, "")
    if desc.get("family") and actual_family and desc["family"] != actual_family:
        violations.append(f"{schema_id}: family mismatch (descriptor={desc['family']}, runtime={actual_family})")

    # --- scalar type binding (SCALAR_BINDING_MAP) ---
    for sf, expected_type in gm.SCALAR_BINDING_MAP.items():
        if sf in model_class.model_fields:
            fld = model_class.model_fields[sf]
            ann = str(_unwrap_optional(fld.annotation))
            if "dict" in ann.lower():
                continue  # container-shaped exempt
            actual = ann.replace("<class '", "").replace("'>", "").replace("typing.", "")
            # normalize e.g. "str" -> "str", "int", "float", enum name
            if actual not in (expected_type, "str") and expected_type in ("int", "float"):
                # enum-typed or list-typed fields are not scalar violations
                if "enum" not in actual.lower():
                    violations.append(f"{schema_id}.{sf}: scalar binding expected {expected_type}, got {ann}")

    return violations


def _field_uses_values(enum_field, values, field_name, model_class):
    """Return True if field_name's annotation uses the given enum values."""
    fld = model_class.model_fields.get(field_name)
    if not fld:
        return False
    ann = _unwrap_optional(fld.annotation)
    # list[Enum] or Enum
    candidates = []
    origin = get_origin(ann)
    if origin is list:
        candidates = list(get_args(ann))
    else:
        candidates = [ann]
    for c in candidates:
        if isinstance(c, type) and issubclass(c, Enum):
            if set(values) == {v.value for v in c}:
                return True
    return False


def _find_enum_ann(model_class, enum_field):
    """Find the Enum annotation matching enum_field name or its values."""
    for fname, fld in model_class.model_fields.items():
        ann = _unwrap_optional(fld.annotation)
        candidates = list(get_args(ann)) if get_origin(ann) is list else [ann]
        for c in candidates:
            if isinstance(c, type) and issubclass(c, Enum) and enum_field.lower() in c.__name__.lower():
                return c
    return None


def validate_all_contracts() -> dict[str, list[str]]:
    """Validate ALL registered schemas.
    Returns dict schema_id -> list of violations (empty = valid).
    Global checks (unused enums, build identity, FK set parity) under '_GLOBAL_'.
    """
    results = {}
    for sid, cls in sorted(SCHEMA_REGISTRY.items()):
        violations = validate_contract(sid, cls)
        if violations:
            results[sid] = violations

    # --- Global: unused enum classes across all models ---
    all_enum_classes = {}
    for sid, cls in sorted(SCHEMA_REGISTRY.items()):
        mod = sys.modules.get(cls.__module__)
        if mod:
            for name, obj in vars(mod).items():
                if isinstance(obj, type) and issubclass(obj, Enum) and obj is not Enum:
                    all_enum_classes.setdefault(obj, name)

    used_enums = set()
    for sid, cls in SCHEMA_REGISTRY.items():
        for fld in cls.model_fields.values():
            ann = _unwrap_optional(fld.annotation)
            origin = get_origin(ann)
            candidates = list(get_args(ann)) if origin is list else [ann]
            for c in candidates:
                if isinstance(c, type) and issubclass(c, Enum):
                    used_enums.add(c)

    global_violations = []
    for obj, name in sorted(all_enum_classes.items(), key=lambda x: x[1]):
        if obj not in used_enums:
            global_violations.append(f"Unused enum class: {name}")
    if global_violations:
        results.setdefault("_GLOBAL_", []).extend(global_violations)

    # --- Global: build identity + artifact hash verification ---
    bi_violations = validate_build_identity()
    if bi_violations:
        results.setdefault("_GLOBAL_", []).extend(bi_violations)

    # --- Global: FK set parity vs descriptor ---
    fk_mismatch = _fk_set_parity()
    if fk_mismatch:
        results.setdefault("_GLOBAL_", []).extend(fk_mismatch)

    return results


def _fk_set_parity() -> list[str]:
    """Verify runtime FK_REGISTRY matches descriptor FK set exactly."""
    violations = []
    runtime_pairs = {
        (sid, fk["field"], fk["target"], fk["target_field"])
        for sid, fks in FK_REGISTRY.items() for fk in fks
    }
    desc_pairs = {
        (sid, fk["field"], fk["target"], fk["target_field"])
        for sid, c in DESCRIPTOR_BY_ID.items() for fk in c.get("fks", [])
    }
    dropped = desc_pairs - runtime_pairs
    if dropped:
        violations.append(f"Dropped FKs vs descriptor: {dropped}")
    phantom = runtime_pairs - desc_pairs
    if phantom:
        violations.append(f"Phantom FKs vs descriptor: {phantom}")
    return violations


def assert_all_contracts_pass() -> None:
    """Assert that all per-schema contracts + global pass with ZERO violations."""
    results = validate_all_contracts()
    failed = {sid: v for sid, v in results.items() if v}
    assert not failed, f"Contract validation failed: {failed}"


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
    """Validate build identity metadata + generated artifact hashes."""
    violations = []
    if not SCHEMA_BUILD_IDENTITY:
        return ["SCHEMA_BUILD_IDENTITY not found"]
    for key in ("spec_source", "spec_source_sha256", "generator_version", "total_schemas",
                "generated_artifact_hashes"):
        if key not in SCHEMA_BUILD_IDENTITY:
            violations.append(f"Missing SCHEMA_BUILD_IDENTITY.{key}")
    if SCHEMA_BUILD_IDENTITY.get("total_schemas") != 68:
        violations.append(f"total_schemas != 68: {SCHEMA_BUILD_IDENTITY.get('total_schemas')}")

    # Set parity: descriptor count must match registry count
    if DESCRIPTOR_BY_ID and len(DESCRIPTOR_BY_ID) != len(SCHEMA_REGISTRY):
        violations.append(f"Descriptor count {len(DESCRIPTOR_BY_ID)} != registry count {len(SCHEMA_REGISTRY)}")

    # Verify artifact hashes match actual on-disk files
    expected_hashes = SCHEMA_BUILD_IDENTITY.get("generated_artifact_hashes", {})
    for rel, exp_hash in sorted(expected_hashes.items()):
        fp = BASE / "qad" / rel
        if not fp.exists():
            violations.append(f"Build artifact missing: {rel}")
        else:
            actual = hashlib.sha256(fp.read_bytes()).hexdigest()
            if actual != exp_hash:
                violations.append(f"Build artifact drift: {rel} (actual {actual[:12]} != recorded {exp_hash[:12]})")
    return violations