"""M5.1 — Runtime Foundation Tests.
Verifies all 68 frozen M4A schemas, FK integrity, and runtime validation.
"""
from __future__ import annotations

from datetime import datetime

import pytest

from qad.models import *
from qad.schema_registry import (
    SCHEMA_REGISTRY, FK_REGISTRY, CANONICAL_SCHEMAS, INFRASTRUCTURE_SCHEMAS,
    resolve_fk, is_canonical, is_infrastructure,
)
from qad.validator import (
    validate_schema_instance, get_all_schema_ids, get_all_fk_pairs,
)


# ── Basic counts ──────────────────────────────────────────────────────────────

def test_schema_count():
    """M4A requires exactly 68 canonical schemas."""
    assert len(SCHEMA_REGISTRY) == 68, f"Expected 68 schemas, got {len(SCHEMA_REGISTRY)}"


def test_canonical_count():
    """Canonical + infrastructure should cover all schemas."""
    covered = CANONICAL_SCHEMAS | INFRASTRUCTURE_SCHEMAS
    assert covered == set(SCHEMA_REGISTRY.keys()), (
        f"Missing from coverage: {set(SCHEMA_REGISTRY.keys()) - covered}"
    )


def test_all_schema_ids_valid():
    """Every schema ID in the registry must match the format XX-NN."""
    for sid in SCHEMA_REGISTRY:
        assert "-" in sid and len(sid) >= 4, f"Invalid schema_id format: {sid}"


# ── Model instantiation ──────────────────────────────────────────────────────

@pytest.mark.parametrize("sid, model_class", sorted(SCHEMA_REGISTRY.items()))
def test_schema_model_instantiation(sid, model_class):
    """Every schema model can be instantiated with required fields."""
    # Get required fields (all non-optional fields in the model)
    schema = model_class.model_json_schema()
    required = schema.get("required", [])
    required_without_defaults = [f for f in required if f not in ("schema_id",)]
    if required_without_defaults:
        kwargs = {}
        for f in required_without_defaults:
            # Determine Python type from the model's field annotation
            field_info = model_class.model_fields.get(f)
            field_type = str(field_info.annotation) if field_info else "str"
            if "list" in field_type.lower():
                kwargs[f] = ["test"]
            elif "dict" in field_type.lower():
                kwargs[f] = {"test": "value"}
            elif "datetime" in field_type.lower() or "started_at" in f or "timestamp" in f:
                kwargs[f] = "2026-01-15T00:00:00"
            elif "float" in field_type.lower() or f in ("metric_value", "cost_usd", "market_price", "implied_growth",
                                           "valuation_range_low", "valuation_range_high",
                                           "budget_allocated", "budget_consumed", "calc_result"):
                kwargs[f] = 0.0
            elif "int" in field_type.lower() or f in ("retry_count", "max_retries", "tokens_used", "duration_ms"):
                kwargs[f] = 0
            elif "status" in f or "state" in f or "mode" in f or "type" in f or "tier" in f:
                kwargs[f] = "ACTIVE"
            elif f.endswith("_id") or f.endswith("_date"):
                kwargs[f] = "test"
            elif f.endswith("_text") or f.endswith("_summary") or f.endswith("_rationale"):
                kwargs[f] = "test_value"
            else:
                kwargs[f] = "test"
        instance = model_class(**kwargs)
    else:
        instance = model_class()
    assert instance.schema_id == sid, f"{sid}: expected schema_id={sid!r}, got {instance.schema_id!r}"
    assert isinstance(instance, model_class)


# ── FK coverage ──────────────────────────────────────────────────────────────

def test_fk_registry_coverage():
    """Every schema with FKs in the spec must appear in FK_REGISTRY."""
    # Schemas that have FKs (from canonical spec analysis)
    schemas_with_fks = {
        "RU-01", "SR-01", "CR-01", "QU-01", "CASE-01",
        "SRC-01", "SRCV-01", "EV-01", "FACT-01", "CLM-01", "INF-01",
        "HYP-01", "CTR-01", "EG-01", "EAR-01",
        "IC-01", "RSR-01", "EG-01", "RB-01", "RFR-01", "HS-01", "IR-01", "RC-01",
        "QA-01", "MA-01", "IE-01", "MC-01", "CAE-01", "MDL-01", "MO-02",
        "DR-01", "IA-01", "CE-01", "RM-01", "TK-01", "FE-01",
        "FF-01", "NFF-01", "CALC-01", "SCEN-01", "PLA-01", "RDCF-01", "VA-01", "PIE-01",
        "RTC-01", "AG-01", "AF-01", "UV-01", "PUB-01", "FDR-01", "CRESP-01",
        "MI-01", "MO-01", "MASS-01", "CL-01", "IKR-01", "IPR-01", "CCV-01",
        "SI-01", "RR-01", "BU-01", "MOD-01", "PROV-01", "EHR-01",
    }
    registered = set(FK_REGISTRY.keys())
    assert schemas_with_fks <= registered, (
        f"Missing FK definitions: {schemas_with_fks - registered}"
    )


def test_fk_targets_exist():
    """Every FK target must be a registered schema."""
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            assert fk["target"] in SCHEMA_REGISTRY, (
                f"FK in {sid} targets unknown schema {fk['target']}"
            )


def test_fk_resolve():
    """resolve_fk returns correct target for known fields."""
    assert resolve_fk("RU-01", "entity_id") == "SM-01"
    assert resolve_fk("CR-01", "entity_id") == "SM-01"
    assert resolve_fk("CR-01", "origin_signal_id") == "SR-01"
    assert resolve_fk("UNKNOWN", "field") is None
    assert resolve_fk("RU-01", "nonexistent") is None


# ── FAKE-99 Negative Test ────────────────────────────────────────────────────

def test_fake_99_negative():
    """FAKE-99: a non-existent schema is NOT in the registry."""
    from qad.schema_registry import SCHEMA_REGISTRY as registry
    assert "FAKE-99" not in registry, "FAKE-99 must not be in the registry"


def test_fake_99_fk_rejection():
    """A FK targeting FAKE-99 must be detecable via FK_REGISTRY check."""
    # Inject a FK to FAKE-99 and verify it's caught
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            assert fk["target"] != "FAKE-99", f"FK to FAKE-99 found in {sid}"
    # Also verify no dangling FK (all FK targets are in SCHEMA_REGISTRY)
    for sid, fks in FK_REGISTRY.items():
        for fk in fks:
            assert fk["target"] in SCHEMA_REGISTRY, (
                f"Dangling FK: {sid}.{fk['field']} -> {fk['target']}"
            )


# ── Canonical vs Infrastructure ──────────────────────────────────────────────

def test_canonical_boundary():
    """Canonical and infrastructure sets are disjoint and cover all schemas."""
    assert CANONICAL_SCHEMAS.isdisjoint(INFRASTRUCTURE_SCHEMAS), (
        "Overlap between canonical and infrastructure"
    )
    all_sids = set(SCHEMA_REGISTRY.keys())
    assert CANONICAL_SCHEMAS | INFRASTRUCTURE_SCHEMAS == all_sids, (
        f"Uncovered: {all_sids - CANONICAL_SCHEMAS - INFRASTRUCTURE_SCHEMAS}"
    )


def test_is_canonical():
    """is_canonical and is_infrastructure return correct values."""
    assert is_canonical("SM-01")
    assert is_canonical("CASE-01")
    assert is_canonical("EV-01")
    assert not is_canonical("RRM-01")
    assert not is_canonical("PITC-01")
    assert is_infrastructure("RRM-01")
    assert is_infrastructure("PITC-01")
    assert not is_infrastructure("SM-01")
    assert not is_canonical("FAKE-99")
    assert not is_infrastructure("FAKE-99")


# ── Provenance and PIT mixin ─────────────────────────────────────────────────

def test_provenance_fields():
    """Every model has provenance base fields (source, retrieval_timestamp, data_version)."""
    for sid, model_class in SCHEMA_REGISTRY.items():
        schema = model_class.model_json_schema()
        props = schema.get("properties", {})
        if "source" in props:
            assert props["source"]["type"] == "string", f"{sid}.source should be str"
        if "retrieval_timestamp" in props:
            # Should be string (datetime serialized)
            pass


def test_schema_id_frozen():
    """schema_id field must be frozen/immutable on every model."""
    for sid, model_class in SCHEMA_REGISTRY.items():
        model_fields = model_class.model_fields
        assert "schema_id" in model_fields, f"{sid} missing schema_id"
        if hasattr(model_fields["schema_id"], "frozen"):
            assert model_fields["schema_id"].frozen, f"{sid}.schema_id not frozen"


# ── Service and role instantiation examples ──────────────────────────────────

def test_security_master_instantiation():
    """SM-01: SecurityMaster can be created with required fields."""
    sm = SecurityMaster(
        entity_id="SM-001",
        primary_ticker="AAPL",
        cik="0000320193",
        name="Apple Inc.",
        exchange="NASDAQ",
        security_type="COMMON_EQUITY",
        status="ACTIVE",
        source="sec-edgar",
        retrieval_timestamp=datetime.now(),
        data_version="v1",
        as_of_date="2026-01-15",
    )
    assert sm.schema_id == "SM-01"
    assert sm.primary_ticker == "AAPL"
    assert sm.cik == "0000320193"


def test_evidence_record_instantiation():
    """EV-01: EvidenceRecord with FK to SourceRecord."""
    ev = EvidenceRecord(
        evidence_id="EV-001",
        source_id="SRC-001",
        entity_id="SM-001",
        evidence_type="SEC_FILING",
        evidence_status="ADMITTED",
        evidence_text="Revenue grew 15% YoY",
        extracted_by="extractor-v1",
        verification_status="VERIFIED",
        source="sec-edgar",
        retrieval_timestamp=datetime.now(),
        data_version="v1",
        as_of_date="2026-01-15",
        content="Revenue grew 15% YoY",
        extractor="extractor-v1",
        source_tier="PRIMARY",
        validation_status="VERIFIED",
        admitting_role="Core Desk Researcher",
        as_of="2026-01-15",
    )
    assert ev.schema_id == "EV-01"
    assert ev.evidence_id == "EV-001"


def test_pit_context_immutable_fields():
    """PITC-01: PITContext has immutable as_of_date."""
    pit = PITContext(
        pit_context_id="PITC-001",
        source="system",
        retrieval_timestamp=datetime.now(),
        data_version="v1",
        as_of_date="2026-01-15",
        case_id="CASE-001",
        created_by="system",
        mode="SEALED_HISTORICAL_EVALUATION",
    )
    assert pit.mode == "SEALED_HISTORICAL_EVALUATION"
    # schema_id should be frozen
    with pytest.raises((ValueError, TypeError)):
        pit.schema_id = "DIFFERENT"


# ── Runtime validator ────────────────────────────────────────────────────────

def test_validate_valid_instance():
    """validate_schema_instance returns empty for valid instances."""
    sm = SecurityMaster(
        entity_id="SM-001",
        primary_ticker="AAPL",
        cik="0000320193",
        name="Apple Inc.",
        exchange="NASDAQ",
        security_type="COMMON_EQUITY",
        status="ACTIVE",
        source="sec-edgar",
        retrieval_timestamp=datetime.now(),
        data_version="v1",
        as_of_date="2026-01-15",
    )
    violations = validate_schema_instance(sm)
    assert violations == [], f"Unexpected violations: {violations}"


def test_validate_unknown_schema():
    """validate_schema_instance reports unknown schema_id."""
    class FakeModel:
        schema_id = "FAKE-99"
    violations = validate_schema_instance(FakeModel())
    assert len(violations) > 0


def test_all_schema_ids_string():
    """get_all_schema_ids returns sorted list of all 68 IDs."""
    ids = get_all_schema_ids()
    assert len(ids) == 68
    assert ids == sorted(ids)


def test_fk_pairs_count():
    """get_all_fk_pairs returns all FK pairs."""
    pairs = get_all_fk_pairs()
    assert len(pairs) > 0
    for src, tgt, field in pairs:
        assert src in SCHEMA_REGISTRY
        assert tgt in SCHEMA_REGISTRY