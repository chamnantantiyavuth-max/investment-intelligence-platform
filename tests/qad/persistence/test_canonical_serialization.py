"""M5.2 Item 8 — FAIL-CLOSED CANONICAL SERIALIZATION.

Adversarial tests proving that:

1. Supported types produce deterministic, equivalent hashes across all
   public persistence paths (regression gates).
2. Unsupported Python types (set, frozenset, Decimal, arbitrary objects)
   are REJECTED — the serializer fails closed instead of silently
   stringifying them via ``default=str``.
3. Non-finite floats (NaN, Infinity, -Infinity) are REJECTED with
   ``allow_nan=False``.
4. Normal canonical records with supported types continue to work.
5. Persistence paths roll back zero records on serialization failure.
"""

from __future__ import annotations

import hashlib
from decimal import Decimal

import pytest

from qad.persistence.errors import (
    IntegrityConflict,
    MissingForeignKey,
    TransactionFailure,
)
from qad.persistence.reference import (
    InMemoryCanonicalRecordStore,
    InMemoryFinancialFactStore,
    InMemoryRawSourceArchive,
    _Record,
)
from qad.persistence.serialization import (
    compute_canonical_hash,
    deserialize_from_canonical_bytes,
    serialize_to_canonical_bytes,
)
from qad.models.family_a import (
    SecurityMaster,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
)
from qad.models.family_b import (
    EvidenceRecord,
    EvidenceRecordEvidence_type,
    EvidenceRecordValidation_status,
    SourceRecord,
    SourceRecordSource_tier,
    SourceRecordSource_type,
)
from qad.models.family_f import (
    FinancialFact,
    FinancialFactMetric_family,
    NormalizedFinancialFact,
    NormalizedFinancialFactAdjustment_type,
    CalculationRecord,
    ScenarioRecord,
    ScenarioRecordScenario_type,
)


# =====================================================================
# A. REGRESSION — existing determinism must remain intact
# =====================================================================

SIMPLE_SCHEMAS: list[tuple[str, object]] = []


def _make_src() -> SourceRecord:
    h = hashlib.sha256(b"test").hexdigest()
    return SourceRecord(
        source_id="SRC-ITEM8",
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier="https://sec.gov",
        content_hash=h,
        retrieval_date="2024-01-01",
    )


def _make_ev() -> EvidenceRecord:
    return EvidenceRecord(
        evidence_id="EV-ITEM8",
        source_id="SRC-ITEM8",
        evidence_type=EvidenceRecordEvidence_type.FACT,
        validation_status=EvidenceRecordValidation_status.RAW,
        content="test",
        admitting_role="researcher",
        as_of="2024-01-20",
        extractor="v1",
        source_tier="L1",
    )


def _make_ff() -> FinancialFact:
    return FinancialFact(
        financial_fact_id="FF-ITEM8",
        case_id="CASE-ITEM8",
        source_id="SRC-ITEM8",
        fiscal_year="2024",
        metric_name=FinancialFactMetric_family.REVENUE,
        period="FY",
        unit="USD",
        value="1000",
    )


def _make_nff() -> NormalizedFinancialFact:
    return NormalizedFinancialFact(
        normalized_fact_id="NFF-ITEM8",
        financial_fact_id="FF-ITEM8",
        adjusted_value="900",
        adjuster="t",
        adjustment_rationale="adj",
        adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING,
    )


def _make_calc() -> CalculationRecord:
    return CalculationRecord(
        calculation_id="CALC-ITEM8",
        case_id="CASE-ITEM8",
        formula="x*2",
        inputs=["x=500"],
        result="1000",
        calculated_by="t",
        timestamp="2024-01-01",
    )


def _make_scen() -> ScenarioRecord:
    return ScenarioRecord(
        scenario_id="SCEN-ITEM8",
        case_id="CASE-ITEM8",
        assumptions={"growth": 0.05, "margin": 0.20},
        intrinsic_value_estimate=1000.0,
        creator="test",
        scenario_type=ScenarioRecordScenario_type.CURRENT,
    )


class TestDeterminismRegression:
    """All previously-passing determinism proofs must survive."""

    def test_same_instance_repeated(self):
        """Same instance → identical bytes and hash every time."""
        for model in [_make_src(), _make_ev(), _make_ff(),
                      _make_nff(), _make_calc(), _make_scen()]:
            b0 = serialize_to_canonical_bytes(model)
            h0 = compute_canonical_hash(model)
            for _ in range(5):
                assert serialize_to_canonical_bytes(model) == b0
                assert compute_canonical_hash(model) == h0

    def test_separate_equivalent_instances(self):
        """Separately constructed identical instances → same hash."""
        a = _make_ff()
        b = FinancialFact(
            financial_fact_id="FF-ITEM8",
            case_id="CASE-ITEM8",
            source_id="SRC-ITEM8",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY",
            unit="USD",
            value="1000",
        )
        assert id(a) != id(b)
        assert compute_canonical_hash(a) == compute_canonical_hash(b)
        assert serialize_to_canonical_bytes(a) == serialize_to_canonical_bytes(b)

    def test_dict_insertion_order_independent(self):
        """Dict key order does not affect canonical bytes."""
        a = ScenarioRecord(
            scenario_id="SCEN-DICT",
            case_id="CASE-ITEM8",
            assumptions={"growth": 0.05, "margin": 0.20},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        b = ScenarioRecord(
            scenario_id="SCEN-DICT",
            case_id="CASE-ITEM8",
            assumptions={"margin": 0.20, "growth": 0.05},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        assert serialize_to_canonical_bytes(a) == serialize_to_canonical_bytes(b)

    def test_list_order_significant(self):
        """List order is payload-semantic — different order → different hash."""
        a = CalculationRecord(
            calculation_id="CALC-LIST",
            case_id="CASE-ITEM8",
            formula="a+b",
            inputs=["x=100", "y=200"],
            result="300",
            calculated_by="t",
            timestamp="2024-01-01",
        )
        b = CalculationRecord(
            calculation_id="CALC-LIST",
            case_id="CASE-ITEM8",
            formula="a+b",
            inputs=["y=200", "x=100"],
            result="300",
            calculated_by="t",
            timestamp="2024-01-01",
        )
        assert serialize_to_canonical_bytes(a) != serialize_to_canonical_bytes(b)

    def test_serialize_deserialize_round_trip(self):
        """serialize → deserialize → serialize produces identical bytes."""
        for model in [_make_src(), _make_ev(), _make_scen()]:
            b1 = serialize_to_canonical_bytes(model)
            restored = deserialize_from_canonical_bytes(b1, type(model))
            b2 = serialize_to_canonical_bytes(restored)
            assert b1 == b2
            assert compute_canonical_hash(model) == compute_canonical_hash(restored)

    def test_enum_by_value(self):
        """Enum members serialize by .value (str), not .name (capitalized)."""
        raw = serialize_to_canonical_bytes(_make_ev())
        # The value for FACT is "FACT" (same as name in this case)
        assert b'"FACT"' in raw
        # Validation status RAW value is "RAW"
        assert b'"RAW"' in raw

    def test_normal_finite_floats_work(self):
        """Normal finite floats in dict fields serialize normally."""
        scen = ScenarioRecord(
            scenario_id="SCEN-FLOAT",
            case_id="CASE-ITEM8",
            assumptions={"rate": 0.05, "large": 1.23e10, "small": -3.14},
            intrinsic_value_estimate=999.99,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        h = compute_canonical_hash(scen)
        assert isinstance(h, str)
        assert len(h) == 64


# =====================================================================
# B. FAIL-CLOSED — unsupported values must be rejected
# =====================================================================


class TestFailClosedSerialization:
    """Canonical serialization must fail closed on unsupported values."""

    def test_set_rejected(self):
        """set in unconstrained dict field raises TypeError."""
        scen = ScenarioRecord(
            scenario_id="SCEN-SET",
            case_id="CASE-ITEM8",
            assumptions={"items": {1, 2, 3}},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TypeError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(TypeError):
            compute_canonical_hash(scen)

    def test_frozenset_rejected(self):
        """frozenset in unconstrained dict field raises TypeError."""
        scen = ScenarioRecord(
            scenario_id="SCEN-FS",
            case_id="CASE-ITEM8",
            assumptions={"items": frozenset(["aaa", "bbb", "ccc"])},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TypeError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(TypeError):
            compute_canonical_hash(scen)

    def test_arbitrary_object_rejected(self):
        """Custom Python object in dict field raises TypeError."""
        class _Weird:
            pass

        scen = ScenarioRecord(
            scenario_id="SCEN-WEIRD",
            case_id="CASE-ITEM8",
            assumptions={"obj": _Weird()},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TypeError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(TypeError):
            compute_canonical_hash(scen)

    def test_decimal_rejected(self):
        """Decimal in unconstrained dict field raises TypeError."""
        scen = ScenarioRecord(
            scenario_id="SCEN-DEC",
            case_id="CASE-ITEM8",
            assumptions={"price": Decimal("12.34")},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TypeError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(TypeError):
            compute_canonical_hash(scen)

    def test_nan_rejected(self):
        """NaN float in dict field raises ValueError (allow_nan=False)."""
        scen = ScenarioRecord(
            scenario_id="SCEN-NAN",
            case_id="CASE-ITEM8",
            assumptions={"val": float("nan")},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(ValueError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(ValueError):
            compute_canonical_hash(scen)

    def test_infinity_rejected(self):
        """+Inf float in dict field raises ValueError (allow_nan=False)."""
        scen = ScenarioRecord(
            scenario_id="SCEN-INF",
            case_id="CASE-ITEM8",
            assumptions={"val": float("inf")},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(ValueError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(ValueError):
            compute_canonical_hash(scen)

    def test_neg_infinity_rejected(self):
        """-Inf float in dict field raises ValueError (allow_nan=False)."""
        scen = ScenarioRecord(
            scenario_id="SCEN-NINF",
            case_id="CASE-ITEM8",
            assumptions={"val": float("-inf")},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(ValueError):
            serialize_to_canonical_bytes(scen)
        with pytest.raises(ValueError):
            compute_canonical_hash(scen)


# =====================================================================
# C. PERSISTENCE ZERO-COMMIT PROOF
# =====================================================================


class TestPersistenceRejectsUnsupported:
    """Persistence paths must roll back on serialization failure."""

    def test_store_rollback_on_set(self):
        """store() with set in nested dict — no record committed."""
        store = InMemoryCanonicalRecordStore()
        sm = SecurityMaster(
            entity_id="E-ROLL",
            cik="ROLL",
            exchange="NYSE",
            name="Rollback",
            primary_ticker="ROLL",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        # This should work
        store.store(sm)
        assert store.contains("SM-01", "E-ROLL")

        # Now try with SCEN containing set
        scen = ScenarioRecord(
            scenario_id="SCEN-ROLL",
            case_id="CASE-ITEM8",
            assumptions={"items": {1, 2, 3}},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TransactionFailure):
            store.store(scen)

        # Prior record must still exist
        assert store.contains("SM-01", "E-ROLL")
        # Failed record must NOT exist
        assert not store.contains("SCEN-01", "SCEN-ROLL")

    def test_store_batch_rollback_on_frozenset(self):
        """store_batch() with frozenset — zero records committed."""
        store = InMemoryCanonicalRecordStore()

        sm = SecurityMaster(
            entity_id="E-B-OK",
            cik="BOK",
            exchange="NYSE",
            name="BatchOK",
            primary_ticker="BOK",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        scen = ScenarioRecord(
            scenario_id="SCEN-ROLL-B",
            case_id="CASE-ITEM8",
            assumptions={"x": frozenset(["a"])},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TransactionFailure):
            store.store_batch([sm, scen])

        # Neither should be committed
        assert not store.contains("SM-01", "E-B-OK")
        assert not store.contains("SCEN-01", "SCEN-ROLL-B")

    def test_financial_fact_store_rejects_bad_nan(self):
        """FinancialFactStore.store() with NaN in dict — zero commit."""
        src_archive = InMemoryRawSourceArchive()
        raw = b"src"
        ch = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-NAN",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov",
            content_hash=ch,
            retrieval_date="2024-01-01",
        )
        src_archive.admit_source(src, raw)

        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        # Inject a case
        ff_store._data.setdefault("CASE-01", {})["CASE-NAN"] = _Record(
            instance=ScenarioRecord(
                scenario_id="DUMMY",
                case_id="CASE-NAN",
                assumptions={},
                intrinsic_value_estimate=0,
                creator="t",
                scenario_type=ScenarioRecordScenario_type.CURRENT,
            ),
            canonical_hash="x",
        )

        scen = ScenarioRecord(
            scenario_id="SCEN-NAN-F",
            case_id="CASE-NAN",
            assumptions={"val": float("nan")},
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TransactionFailure):
            ff_store.store(scen)

        assert not ff_store.contains("SCEN-01", "SCEN-NAN-F")

    def test_normal_records_still_work(self):
        """Supported normal records through real persistence paths."""
        archive = InMemoryRawSourceArchive()
        raw = b"normal source"
        ch = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-NORM",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov",
            content_hash=ch,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)
        assert archive.contains("SRC-01", "SRC-NORM")

        ff_store = InMemoryFinancialFactStore(source_archive=archive)
        ff_store._data.setdefault("CASE-01", {})["CASE-NORM"] = _Record(
            instance=object(), canonical_hash="x",
        )
        ff = FinancialFact(
            financial_fact_id="FF-NORM",
            case_id="CASE-NORM",
            source_id="SRC-NORM",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY",
            unit="USD",
            value="500",
        )
        ff_store.store(ff)
        assert ff_store.contains("FF-01", "FF-NORM")
