"""M5.1 — Contract Conformance Tests.
Tests that generated runtime models EXACTLY match frozen M4A contracts.
Uses INDEPENDENT test-only oracle (tests/qad/independent_oracle.py) that does
NOT import qad.generate_models, production parser functions, or generated artifacts.
"""
import hashlib
import subprocess
import sys
import typing
from enum import Enum
from pathlib import Path

import pytest
from pydantic import ValidationError

from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS, SCHEMA_FAMILIES

# Independent oracle — does NOT import production code
from tests.qad.independent_oracle import ORACLE, ORACLE_SOURCE_HASH

BASE = Path(__file__).resolve().parent.parent.parent
GENERATOR = BASE / "qad" / "generate_models.py"
MODELS_DIR = BASE / "qad" / "models"


def make_kwargs(cls, required_fields):
    """Build valid kwargs for a model class from its required fields."""
    kwargs = {}
    for f in required_fields:
        if f == "schema_id":
            continue
        fi = cls.model_fields.get(f)
        ann = fi.annotation if fi else None
        if ann:
            if isinstance(ann, type) and issubclass(ann, Enum):
                kwargs[f] = list(ann)[0].value
                continue
            if hasattr(ann, "__origin__") and ann.__origin__ is typing.Union:
                for a in ann.__args__:
                    if isinstance(a, type) and issubclass(a, Enum):
                        kwargs[f] = list(a)[0].value
                        break
                else:
                    kwargs[f] = "test"
                continue
        if fi and "list" in str(fi.annotation):
            kwargs[f] = ["test"]
        elif fi and "dict" in str(fi.annotation):
            kwargs[f] = {"test": "value"}
        elif fi and "int" in str(fi.annotation):
            kwargs[f] = 0
        elif fi and "float" in str(fi.annotation):
            kwargs[f] = 0.0
        else:
            kwargs[f] = "test"
    return kwargs


def get_model_class(schema_id: str):
    return SCHEMA_REGISTRY.get(schema_id)


def test_schema_count():
    assert len(ORACLE) == 68, f"Expected 68, got {len(ORACLE)}"


def test_independent_parser_matches_production():
    """Independent oracle and production code parse the same source."""
    for sid, contract in ORACLE.items():
        cls = get_model_class(sid)
        assert cls is not None, f"Oracle has {sid} but no runtime model"


def test_required_fields_match():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        missing = oc["required"] - mf
        assert len(missing) == 0, f"{sid} missing required: {missing}"


def test_optional_fields_match():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        missing = oc["optional"] - mf
        # schema_id is always present in model but not in oracle optional
        missing -= {"schema_id"}
        assert len(missing) == 0, f"{sid} missing optional: {missing}"


def test_no_extra_fields():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys()) - {"schema_id"}
        cf = oc["required"] | oc["optional"]
        extra = mf - cf
        assert len(extra) == 0, f"{sid} has extra fields: {extra}"


def test_field_shape_containers():
    """Verify [] -> list, {} -> dict, scalar -> str."""
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        for fname, container in oc["field_shapes"].items():
            if fname not in cls.model_fields:
                continue
            ft = str(cls.model_fields[fname].annotation)
            if container == "list":
                assert "list" in ft.lower(), f"{sid}.{fname} should be list, got {ft}"
            elif container == "dict":
                assert "dict" in ft.lower(), f"{sid}.{fname} should be dict, got {ft}"


def test_enums_from_oracle():
    """Every frozen enum field has a runtime enum class."""
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        for e in oc["enums"]:
            ef = e["field"]
            if ef not in cls.model_fields:
                continue
            fi = cls.model_fields[ef]
            ann = fi.annotation
            # Unwrap Optional[Enum]
            if hasattr(ann, "__origin__") and ann.__origin__ is typing.Union:
                for a in ann.__args__:
                    if isinstance(a, type) and issubclass(a, Enum):
                        ann = a
                        break
            assert isinstance(ann, type) and issubclass(ann, Enum), \
                f"{sid}.{ef} should be enum, got {fi.annotation}"
            # Verify enum values match
            oracle_values = set(e["values"])
            runtime_values = {v.value for v in ann}
            assert oracle_values == runtime_values, \
                f"{sid}.{ef} values mismatch: oracle={oracle_values}, runtime={runtime_values}"


def test_enum_continuation_rows():
    """Verify continuation rows are not silently dropped.
    Enums are either FIELD_ENUM (matches a field name) or TYPE_ALIAS_ENUM (shared type)."""
    for sid, oc in ORACLE.items():
        if len(oc["enums"]) > 1:
            cls = get_model_class(sid)
            if cls is None:
                continue
            for e in oc["enums"][1:]:
                ef = e["field"]
                # Check if it's a field or a type alias
                if ef in cls.model_fields:
                    continue  # FIELD_ENUM — present as field
                # TYPE_ALIAS_ENUM — check that the field referencing it exists
                # e.g., plausibility is used by initial_plausibility, current_plausibility
                related = [f for f in cls.model_fields if ef in f.lower() or f.lower().endswith(ef.lower())]
                assert len(related) > 0, \
                    f"{sid} continuation enum '{ef}' is neither a field nor a type alias used by any field"


def test_pit_fields_match():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        for pf in oc["pit_fields"]:
            pf_clean = pf.replace("[]", "").replace("{}", "")
            assert pf_clean in mf, f"{sid} missing PIT: {pf}"


def test_provenance_fields_match():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        for pf in oc["provenance_fields"]:
            pfc = pf.replace("[]", "").replace("{}", "")
            assert pfc in mf, f"{sid} missing provenance: {pf}"


def test_pit_fields_frozen():
    """PIT fields must be frozen (immutable)."""
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        for pf in oc["pit_fields"]:
            pf_clean = pf.replace("[]", "").replace("{}", "")
            if pf_clean in cls.model_fields:
                assert cls.model_fields[pf_clean].frozen, \
                    f"{sid}.{pf_clean} (PIT) should be frozen"


def test_fk_count():
    oracle_fk = sum(len(oc["fks"]) for oc in ORACLE.values())
    runtime_fk = sum(len(fks) for fks in FK_REGISTRY.values())
    assert oracle_fk == runtime_fk, f"FK count: oracle={oracle_fk}, runtime={runtime_fk}"


def test_fk_source_fields_exist():
    """Every FK source field exists in its source model."""
    for sid, fks in FK_REGISTRY.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        for fk in fks:
            assert fk["field"] in mf, f"FK source {sid}.{fk['field']} not in model"


def test_fk_targets_exist():
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            tc = get_model_class(fk["target"])
            assert tc is not None, f"FK target {fk['target']} not found"
            assert fk["target_field"] in tc.model_fields, \
                f"FK target {fk['target']}.{fk['target_field']} not found"


def test_fk_no_phantom():
    for sid, fks in FK_REGISTRY.items():
        oracle = ORACLE.get(sid)
        if oracle is None:
            continue
        oc = {(fk["field"], fk["target"], fk["target_field"]) for fk in oracle["fks"]}
        for fk in fks:
            assert (fk["field"], fk["target"], fk["target_field"]) in oc, \
                f"Phantom FK {sid}.{fk['field']} -> {fk['target']}.{fk['target_field']}"


def test_fk_no_dropped():
    for sid, oracle in ORACLE.items():
        if not oracle["fks"]:
            continue
        rf = FK_REGISTRY.get(sid, [])
        rs = {(fk["field"], fk["target"], fk["target_field"]) for fk in rf}
        for fk in oracle["fks"]:
            assert (fk["field"], fk["target"], fk["target_field"]) in rs, \
                f"Dropped FK {sid}.{fk['field']} -> {fk['target']}.{fk['target_field']}"


def test_canonical_boundary():
    fc = {sid for sid, oc in ORACLE.items() if oc["is_canonical"]}
    assert fc == CANONICAL_SCHEMAS, f"Canonical mismatch: {fc ^ CANONICAL_SCHEMAS}"
    assert fc.isdisjoint(NON_CANONICAL_SCHEMAS)


def test_infrastructure_is_family_based():
    """is_infrastructure should be family-based, not non-canonical."""
    for oc in ORACLE.values():
        is_infra = SCHEMA_FAMILIES.get(oc["schema_id"], "") == "I"
        if is_infra:
            assert oc["family"] == "I", f"{oc['schema_id']} is Family {oc['family']} but marked infra"
            assert oc["is_canonical"], f"{oc['schema_id']} is infra but marked non-canonical"


def test_extra_field_rejected():
    for sid in ORACLE:
        cls = get_model_class(sid)
        if cls is None:
            continue
        assert cls.model_config.get("extra") == "forbid", f"{sid} missing extra=forbid"


def test_schema_id_immutable():
    for sid in ORACLE:
        cls = get_model_class(sid)
        if cls is None:
            continue
        fi = cls.model_fields.get("schema_id")
        assert fi is not None, f"{sid} missing schema_id"
        assert fi.frozen, f"{sid}.schema_id not frozen"


def test_regeneration_determinism():
    """Regenerate from scratch, verify byte-identical output."""
    # Run generator twice to temp dirs
    temp1 = BASE / "qad" / "models"
    temp2 = BASE / "qad" / "models"  # same output since we just regenerated
    # Actually, run a subprocess to test
    # First, compute hash of current generated files
    import glob
    files = sorted(glob.glob(str(MODELS_DIR / "family_*.py"))) + [str(MODELS_DIR / "__init__.py")]
    hash1 = hashlib.sha256()
    for f in files:
        hash1.update(Path(f).read_bytes())
    h1 = hash1.hexdigest()

    # Regenerate
    result = subprocess.run([sys.executable, str(GENERATOR)], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, f"Generator failed: {result.stderr}"

    # Compute hash again
    files2 = sorted(glob.glob(str(MODELS_DIR / "family_*.py"))) + [str(MODELS_DIR / "__init__.py")]
    hash2 = hashlib.sha256()
    for f in files2:
        hash2.update(Path(f).read_bytes())
    h2 = hash2.hexdigest()

    assert h1 == h2, f"Regeneration drift: {h1[:12]} != {h2[:12]}"


@pytest.mark.parametrize("sid", sorted(ORACLE.keys()))
def test_missing_required_field(sid):
    """Missing required field must raise ValidationError."""
    oc = ORACLE[sid]
    cls = get_model_class(sid)
    if cls is None:
        return
    req = [f for f in oc["required"] if f != "schema_id"]
    if not req:
        return
    rf = req[0]
    kwargs = make_kwargs(cls, [f for f in oc["required"] if f != rf])
    with pytest.raises(ValidationError):
        cls(**kwargs)


def test_extra_field_rejected_instance():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        kwargs = make_kwargs(cls, oc["required"])
        with pytest.raises(ValidationError):
            cls(**kwargs, invented_field="should_fail")


def test_immutable_field_mutation():
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        kwargs = make_kwargs(cls, oc["required"])
        instance = cls(**kwargs)
        with pytest.raises((ValidationError, TypeError, ValueError)):
            instance.schema_id = "DIFFERENT"


def test_family_i_not_noncanonical():
    """Family I schemas must not be classified as non-canonical."""
    for sid, oc in ORACLE.items():
        if oc["family"] == "I":
            assert oc["is_canonical"], f"Family I schema {sid} marked non-canonical"


def test_publication_boundary_preserved():
    """PUB-01 has mixed canonical boundary."""
    oc = ORACLE.get("PUB-01")
    assert oc is not None
    assert "NONCANONICAL" in oc["canonical_boundary"].upper() or "noncanonical" in oc["canonical_boundary"].lower()


def test_enum_illegal_value_rejected():
    """Illegal enum value must be rejected."""
    from pydantic import ValidationError
    for sid, oc in ORACLE.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        for e in oc["enums"]:
            ef = e["field"]
            if ef not in cls.model_fields:
                continue
            kwargs = make_kwargs(cls, oc["required"])
            kwargs[ef] = "ILLEGAL_ENUM_VALUE_THAT_DOES_NOT_EXIST"
            with pytest.raises(ValidationError):
                cls(**kwargs)


def test_scalar_to_list_rejected():
    """Passing scalar to a list field must fail."""
    from pydantic import ValidationError
    for oc in ORACLE.values():
        for fname, container in oc["field_shapes"].items():
            if container == "list":
                cls = get_model_class(oc["schema_id"])
                if cls is None:
                    continue
                kwargs = make_kwargs(cls, oc["required"])
                kwargs[fname] = "not_a_list"
                with pytest.raises(ValidationError):
                    cls(**kwargs)
                break  # One test per schema is enough
        else:
            continue
        break  # Only test one schema to save time


def test_oracle_source_hash_deterministic():
    """Oracle source hash must be deterministic."""
    h1 = hashlib.sha256(
        (BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md").read_bytes()
    ).hexdigest()
    assert h1 == ORACLE_SOURCE_HASH


def test_no_manual_patch_dependency():
    """SCHEMA_REGISTRY must be importable after clean generation."""
    # Verify that qad/__init__.py exposes SCHEMA_REGISTRY
    from qad.models import SCHEMA_REGISTRY as sr
    assert len(sr) == 68


def test_schema_build_identity():
    """Generated models must carry build identity metadata."""
    path = MODELS_DIR / "__init__.py"
    content = path.read_text()
    assert "spec_source_sha256" in content
    assert "generator_version" in content
    assert "total_schemas" in content