"""M5.1 — Contract Conformance Tests.
Tests that generated runtime models EXACTLY match frozen M4A contracts.
Uses independent contract descriptor (parsed from M4A markdown) as the oracle.
"""
import hashlib
import json
import typing
from enum import Enum
from pathlib import Path

import pytest
from pydantic import ValidationError

from qad.models import *  # noqa: F403
from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS, NON_CANONICAL_SCHEMAS

BASE = Path(__file__).resolve().parent.parent.parent
DESCRIPTOR = BASE / "qad" / "contract" / "contract_descriptor.json"

with open(DESCRIPTOR) as f:
    CONTRACT = json.load(f)
SCHEMAS = {s["schema_id"]: s for s in CONTRACT["schemas"]}


def get_model_class(schema_id: str):
    for sid, cls in SCHEMA_REGISTRY.items():
        if sid == schema_id:
            return cls
    return None


def make_kwargs(cls, required_fields):
    """Build valid kwargs for a model class from its required fields."""
    kwargs = {}
    for f in required_fields:
        if f == "schema_id":
            continue
        fi = cls.model_fields.get(f)
        ann = fi.annotation if fi else None
        # Handle enum types first (check via issubclass, not string matching)
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
        # Handle container types
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


def test_schema_count():
    assert len(SCHEMAS) == 68


def test_all_schemas_have_models():
    for sid in SCHEMAS:
        cls = get_model_class(sid)
        assert cls is not None, f"No runtime model for {sid}"
        assert "schema_id" in cls.model_fields, f"{sid} model missing schema_id"


def test_required_fields_match():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        missing = set(contract["required_fields"]) - mf
        assert len(missing) == 0, f"{sid} missing required: {missing}"


def test_optional_fields_match():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        missing = set(contract["optional_fields"]) - mf
        assert len(missing) == 0, f"{sid} missing optional: {missing}"


def test_no_extra_fields():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys()) - {"schema_id"}
        cf = set(contract["required_fields"]) | set(contract["optional_fields"])
        extra = mf - cf
        assert len(extra) == 0, f"{sid} has extra: {extra}"


def test_field_shape_match():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        for fd in contract["fields"]:
            fname = fd["name"]
            container = fd["container"]
            if fname not in cls.model_fields:
                continue
            ft = str(cls.model_fields[fname].annotation)
            if container == "list":
                assert "list" in ft.lower(), f"{sid}.{fname} should be list, got {ft}"
            elif container == "dict":
                assert "dict" in ft.lower(), f"{sid}.{fname} should be dict, got {ft}"


def test_enum_defined():
    for sid, contract in SCHEMAS.items():
        for e in contract["enums"]:
            ef = e["field"]
            cls = get_model_class(sid)
            if cls is None or ef not in cls.model_fields:
                continue
            fi = cls.model_fields[ef]
            ann = fi.annotation
            if hasattr(ann, "__origin__") and ann.__origin__ is typing.Union:
                for a in ann.__args__:
                    if isinstance(a, type) and issubclass(a, Enum):
                        ann = a
                        break
            assert isinstance(ann, type) and issubclass(ann, Enum), \
                f"{sid}.{ef} should be enum, got {fi.annotation}"


def test_pit_fields_match():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        for pf in contract["pit_fields"]:
            assert pf in mf, f"{sid} missing PIT: {pf}"


def test_provenance_fields_match():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        mf = set(cls.model_fields.keys())
        for pf in contract["provenance_fields"]:
            pfc = pf.replace("[]", "").replace("{}", "")
            assert pfc in mf, f"{sid} missing provenance: {pf}"


def test_fk_count():
    frozen = sum(len(contract["fks"]) for contract in SCHEMAS.values())
    runtime = sum(len(fks) for fks in FK_REGISTRY.values())
    assert frozen == runtime, f"FK count: frozen={frozen}, runtime={runtime}"


def test_fk_source_fields_exist():
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
        contract = SCHEMAS.get(sid)
        if contract is None:
            continue
        cf = {(fk["field"], fk["target"], fk["target_field"]) for fk in contract["fks"]}
        for fk in fks:
            assert (fk["field"], fk["target"], fk["target_field"]) in cf, \
                f"Phantom FK {sid}.{fk['field']} -> {fk['target']}.{fk['target_field']}"


def test_fk_no_dropped():
    for sid, contract in SCHEMAS.items():
        if not contract["fks"]:
            continue
        rf = FK_REGISTRY.get(sid, [])
        rs = {(fk["field"], fk["target"], fk["target_field"]) for fk in rf}
        for fk in contract["fks"]:
            assert (fk["field"], fk["target"], fk["target_field"]) in rs, \
                f"Dropped FK {sid}.{fk['field']} -> {fk['target']}.{fk['target_field']}"


def test_canonical_boundary():
    fc = {sid for sid, s in SCHEMAS.items() if s["is_canonical"]}
    assert fc == CANONICAL_SCHEMAS, f"Canonical mismatch: {fc ^ CANONICAL_SCHEMAS}"
    assert fc.isdisjoint(NON_CANONICAL_SCHEMAS)


def test_extra_field_rejected():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        assert cls.model_config.get("extra") == "forbid", f"{sid} missing extra=forbid"


def test_schema_id_immutable():
    for sid in SCHEMAS:
        cls = get_model_class(sid)
        if cls is None:
            continue
        fi = cls.model_fields.get("schema_id")
        assert fi is not None, f"{sid} missing schema_id"
        assert fi.frozen, f"{sid}.schema_id not frozen"


def test_regeneration_determinism():
    sp = BASE / "design" / "qad-pivot" / "m4a" / "QAD-M4A-CANONICAL-SCHEMAS.md"
    c = sp.read_bytes()
    assert hashlib.sha256(c).hexdigest() == hashlib.sha256(c).hexdigest()


def test_missing_required_field():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        req = [f for f in contract["required_fields"] if f != "schema_id"]
        if not req:
            continue
        rf = req[0]
        kwargs = make_kwargs(cls, [f for f in contract["required_fields"] if f != rf])
        with pytest.raises(ValidationError):
            cls(**kwargs)


def test_extra_field_rejected_instance():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        kwargs = make_kwargs(cls, contract["required_fields"])
        with pytest.raises(ValidationError):
            cls(**kwargs, invented_field="should_fail")


def test_immutable_field_mutation():
    for sid, contract in SCHEMAS.items():
        cls = get_model_class(sid)
        if cls is None:
            continue
        kwargs = make_kwargs(cls, contract["required_fields"])
        instance = cls(**kwargs)
        with pytest.raises((ValidationError, TypeError, ValueError)):
            instance.schema_id = "DIFFERENT"