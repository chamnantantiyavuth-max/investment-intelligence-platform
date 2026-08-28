"""M5.2 Item 8 — FAIL-CLOSED CANONICAL SERIALIZATION.

Adversarial tests proving that:

1. Supported types produce deterministic, equivalent hashes across all
   public persistence paths (regression gates).
2. Unsupported Python types (set, frozenset, Decimal, arbitrary objects)
   are REJECTED — the serializer fails closed instead of silently
   stringifying them via ``default=str``.
3. Non-finite floats (NaN, Infinity, -Infinity) are REJECTED with
   ``allow_nan=False``.
4. Cross-process PYTHONHASHSEED does not affect frozenset rejection.
5. Normal canonical records with supported types continue to work.
6. Persistence paths roll back zero records on serialization failure.
7. Version snapshot hash matches ``compute_canonical_hash(historical instance)``.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

from qad.persistence.errors import (
    TransactionFailure,
)
from qad.persistence.reference import (
    InMemoryCanonicalRecordStore,
    InMemoryEvidenceRegistry,
    InMemoryFinancialFactStore,
    InMemoryRawSourceArchive,
    _Record,
)
from qad.persistence.serialization import (
    compute_canonical_hash,
    deserialize_from_canonical_bytes,
    serialize_to_canonical_bytes,
    serialize_to_canonical_json,
)
from qad.models.family_a import (
    SecurityMaster,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
)
from qad.models.family_b import (
    EvidenceAdmissionRecord,
    EvidenceAdmissionRecordAdmission_method,
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


def _make_ear() -> EvidenceAdmissionRecord:
    return EvidenceAdmissionRecord(
        admission_id="EAR-ITEM8",
        evidence_id="EV-ITEM8",
        admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION,
        original_source_verified="true",
        admitting_role="researcher",
        admission_timestamp="2024-01-01T00:00:00",
        source_tier_check="L1",
        validation_method="HASH_MATCH",
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


_ALL_SCHEMAS = [_make_src, _make_ev, _make_ear, _make_ff,
                _make_nff, _make_calc, _make_scen]


class TestDeterminismRegression:
    """All previously-passing determinism proofs must survive."""

    def test_same_instance_repeated(self):
        """Same instance → identical bytes and hash every time.

        Covers ALL 7 schemas: SRC-01, EV-01, EAR-01, FF-01, NFF-01,
        CALC-01, SCEN-01.
        """
        for factory in _ALL_SCHEMAS:
            model = factory()
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

    def test_nested_dict_insertion_order_independent(self):
        """Nested dict key order does not affect canonical bytes."""
        a = ScenarioRecord(
            scenario_id="SCEN-NEST",
            case_id="CASE-ITEM8",
            assumptions={
                "operating": {"growth": 0.05, "margin": 0.20},
                "capital": {"wacc": 0.10, "terminal": 0.03},
            },
            intrinsic_value_estimate=1.0,
            creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        b = ScenarioRecord(
            scenario_id="SCEN-NEST",
            case_id="CASE-ITEM8",
            assumptions={
                "capital": {"terminal": 0.03, "wacc": 0.10},
                "operating": {"margin": 0.20, "growth": 0.05},
            },
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
        for factory in [_make_src, _make_ev, _make_scen, _make_ear]:
            model = factory()
            b1 = serialize_to_canonical_bytes(model)
            restored = deserialize_from_canonical_bytes(b1, type(model))
            b2 = serialize_to_canonical_bytes(restored)
            assert b1 == b2
            assert compute_canonical_hash(model) == compute_canonical_hash(restored)

    def test_enum_by_name_differs_from_value(self):
        """Enum members serialize by .value, not .name.

        Uses FinancialFactMetric_family.SGA whose .name='SGA' and
        .value='SG&A' — proving .value semantics.
        """
        ff = FinancialFact(
            financial_fact_id="FF-ENUM",
            case_id="CASE-ITEM8",
            source_id="SRC-ITEM8",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.SGA,
            period="FY",
            unit="USD",
            value="500",
        )
        raw = serialize_to_canonical_bytes(ff)
        # Must contain the VALUE "SG&A", not the enum name "SGA"
        assert b'"SG&A"' in raw, "serializer must use Enum .value, not .name"
        # The field 'metric_name' must NOT contain bare "SGA" as the value
        # (it may appear as substring of "SG&A" — we need a field-aware check)
        raw_str = raw.decode("utf-8")
        import json
        parsed = json.loads(raw_str)
        assert parsed["metric_name"] == "SG&A", (
            f"metric_name must be 'SG&A', got {parsed['metric_name']!r}"
        )

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

    def test_frozenset_rejected_cross_process(self):
        """frozenset rejection is deterministic across PYTHONHASHSEED values.

        Verifies that under PYTHONHASHSEED=0 and PYTHONHASHSEED=9999
        a subprocess deterministically rejects the same frozenset payload.
        Uses a temp script file to avoid Windows command-line length limits.
        """
        import os as _os
        from pathlib import Path
        _project_root = str(Path(__file__).resolve().parents[3])
        _script = (
            "from qad.persistence.serialization import serialize_to_canonical_bytes\n"
            "from qad.models.family_f import ScenarioRecord, ScenarioRecordScenario_type\n"
            "scen = ScenarioRecord("
            "scenario_id='SCEN-XP', case_id='CASE-X', "
            "assumptions={'items': frozenset(['aaa','bbb','ccc','ddd'])}, "
            "intrinsic_value_estimate=1.0, creator='t', "
            "scenario_type=ScenarioRecordScenario_type.CURRENT)\n"
            "try:\n"
            "    serialize_to_canonical_bytes(scen)\n"
            "    print('WRONG_ERROR:no_error')\n"
            "except TypeError:\n"
            "    print('DETERMINISTIC_REJECTION')\n"
            "except Exception as e:\n"
            "    print(f'WRONG_ERROR:{type(e).__name__}:{e}')\n"
        )
        _tmp_path = _os.path.join(_project_root, "_cross_proc_test.py")
        try:
            with open(_tmp_path, "w") as f:
                f.write(_script)
            for seed in ("0", "9999"):
                env = {**__import__("os").environ, "PYTHONHASHSEED": seed}
                result = subprocess.run(
                    [sys.executable, _tmp_path],
                    capture_output=True, text=True, timeout=30,
                    env=env, cwd=_project_root,
                )
                output = result.stdout.strip()
                assert result.returncode == 0, (
                    f"seed={seed}: child process failed (rc={result.returncode}, "
                    f"stderr: {result.stderr[:300]})"
                )
                assert output == "DETERMINISTIC_REJECTION", (
                    f"seed={seed}: expected DETERMINISTIC_REJECTION, "
                    f"got {output!r} (stderr: {result.stderr[:500]})"
                )
        finally:
            if _os.path.exists(_tmp_path):
                _os.unlink(_tmp_path)
        # Prove no residue
        assert not _os.path.exists(_tmp_path), f"temp file {_tmp_path} must be cleaned up"

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
# C. PUBLIC PERSISTENCE HASH EQUIVALENCE
# =====================================================================


class TestPublicPersistenceHashEquivalence:
    """Every public persistence path must return/store hash matching
    ``compute_canonical_hash(instance)``."""

    def test_store_sm01(self):
        store = InMemoryCanonicalRecordStore()
        sm = SecurityMaster(
            entity_id="E-HASH", cik="HASH", exchange="NYSE",
            name="HashCo", primary_ticker="HASH",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        returned = store.store(sm)
        stored = store.get_canonical_hash("SM-01", "E-HASH")
        loaded = store.load("SM-01", "E-HASH")
        loaded_hash = compute_canonical_hash(loaded)
        assert returned == stored == loaded_hash

    def test_store_batch(self):
        store = InMemoryCanonicalRecordStore()
        sm_a = SecurityMaster(
            entity_id="E-BA", cik="BA", exchange="NYSE", name="A",
            primary_ticker="BA",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        sm_b = SecurityMaster(
            entity_id="E-BB", cik="BB", exchange="NYSE", name="B",
            primary_ticker="BB",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        hashes = store.store_batch([sm_a, sm_b])
        loaded_a = store.load("SM-01", "E-BA")
        loaded_b = store.load("SM-01", "E-BB")
        assert hashes[0] == compute_canonical_hash(loaded_a)
        assert hashes[1] == compute_canonical_hash(loaded_b)
        assert hashes[0] == store.get_canonical_hash("SM-01", "E-BA")
        assert hashes[1] == store.get_canonical_hash("SM-01", "E-BB")

    def test_admit_source(self):
        archive = InMemoryRawSourceArchive()
        raw = b"source content for hash test"
        h = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-HASH-EQ", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=h,
            retrieval_date="2024-01-01",
        )
        returned = archive.admit_source(src, raw)
        stored = archive.get_canonical_hash("SRC-01", "SRC-HASH-EQ")
        loaded = archive.load("SRC-01", "SRC-HASH-EQ")
        loaded_hash = compute_canonical_hash(loaded)
        assert returned == stored == loaded_hash

    def test_admit_evidence(self):
        archive = InMemoryRawSourceArchive()
        raw = b"source for evidence hash"
        h = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-EV-HASH", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=h,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)

        registry = InMemoryEvidenceRegistry(source_archive=archive)
        ev = EvidenceRecord(
            evidence_id="EV-HASH-EQ", source_id="SRC-EV-HASH",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="evidence hash test", admitting_role="researcher",
            as_of="2024-01-20", extractor="v1", source_tier="L1",
        )
        ear = EvidenceAdmissionRecord(
            admission_id="EAR-HASH-EQ", evidence_id="EV-HASH-EQ",
            admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION,
            original_source_verified="true", admitting_role="researcher",
            admission_timestamp="2024-01-01T00:00:00",
            source_tier_check="L1", validation_method="HASH_MATCH",
        )
        returned = registry.admit_evidence(ev, ear)
        stored_ev = registry.get_canonical_hash("EV-01", "EV-HASH-EQ")
        stored_ear = registry.get_canonical_hash("EAR-01", "EAR-HASH-EQ")
        loaded_ev = registry.load("EV-01", "EV-HASH-EQ")
        loaded_ear = registry.load("EAR-01", "EAR-HASH-EQ")
        assert returned == stored_ev
        assert stored_ev == compute_canonical_hash(loaded_ev)
        assert stored_ear == compute_canonical_hash(loaded_ear)

    def test_financial_fact_store(self):
        archive = InMemoryRawSourceArchive()
        raw = b"source for ff hash"
        h = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-FF-HASH", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=h,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)

        ff_store = InMemoryFinancialFactStore(source_archive=archive)
        ff_store._data.setdefault("CASE-01", {})["CASE-FF-HASH"] = _Record(
            instance=object(), canonical_hash="x",
        )
        ff = FinancialFact(
            financial_fact_id="FF-HASH-EQ", case_id="CASE-FF-HASH",
            source_id="SRC-FF-HASH", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000",
        )
        returned = ff_store.store(ff)
        stored = ff_store.get_canonical_hash("FF-01", "FF-HASH-EQ")
        loaded = ff_store.load("FF-01", "FF-HASH-EQ")
        loaded_hash = compute_canonical_hash(loaded)
        assert returned == stored == loaded_hash

    def test_financial_fact_store_batch(self):
        archive = InMemoryRawSourceArchive()
        raw = b"source for batch hash"
        h = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-BATCH-HASH", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=h,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)

        ff_store = InMemoryFinancialFactStore(source_archive=archive)
        ff_store._data.setdefault("CASE-01", {})["CASE-FF-HASH"] = _Record(
            instance=object(), canonical_hash="x",
        )
        ff_store.store(FinancialFact(
            financial_fact_id="FF-BATCH-HASH", case_id="CASE-FF-HASH",
            source_id="SRC-BATCH-HASH", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="500",
        ))
        nff = NormalizedFinancialFact(
            normalized_fact_id="NFF-BATCH-HASH",
            financial_fact_id="FF-BATCH-HASH", adjusted_value="450",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING,
        )
        hashes = ff_store.store_batch([nff])
        loaded = ff_store.load("NFF-01", "NFF-BATCH-HASH")
        assert hashes[0] == compute_canonical_hash(loaded)
        assert hashes[0] == ff_store.get_canonical_hash("NFF-01", "NFF-BATCH-HASH")


# =====================================================================
# D. VERSION SNAPSHOT HASH PROOF
# =====================================================================


class TestVersionSnapshotHash:
    """Version snapshots must preserve the hash of the original instance."""

    def test_historical_version_hash_matches(self):
        """Prove stored historical canonical_hash ==
        compute_canonical_hash(historical instance)."""
        archive = InMemoryRawSourceArchive()
        raw = b"source for version"
        h = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-VER-HASH", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=h,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)

        registry = InMemoryEvidenceRegistry(source_archive=archive)

        # Admit v1
        ev_v1 = EvidenceRecord(
            evidence_id="EV-VER", source_id="SRC-VER-HASH",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.RAW,
            content="v1", admitting_role="r", as_of="2024-01-20",
            extractor="v1", source_tier="L1",
        )
        ear_v1 = EvidenceAdmissionRecord(
            admission_id="EAR-VER", evidence_id="EV-VER",
            admission_method=EvidenceAdmissionRecordAdmission_method.AI_EXTRACTION,
            original_source_verified="true", admitting_role="r",
            admission_timestamp="2024-01-01T00:00:00",
            source_tier_check="L1", validation_method="HASH_MATCH",
        )
        registry.admit_evidence(ev_v1, ear_v1)
        v1_hash = compute_canonical_hash(ev_v1)

        # Update to v2 (CHALLENGED status)
        ev_v2 = EvidenceRecord(
            evidence_id="EV-VER", source_id="SRC-VER-HASH",
            evidence_type=EvidenceRecordEvidence_type.FACT,
            validation_status=EvidenceRecordValidation_status.VALIDATED,
            content="v1", admitting_role="r", as_of="2024-01-20",
            extractor="v1", source_tier="L1",
        )
        registry.store(ev_v2)

        # Load v1 from version history
        historical_v1 = registry.load_version("EV-01", "EV-VER", "v0001")

        # The stored canonical hash of the current record is the v2 hash
        # (not the same as v1), but the version snapshot stores the hash
        # of the v1 instance at the time it was archived.
        # Access the hash stored with the version snapshot.
        ver_record = registry._versions.get("EV-01", {}).get("EV-VER", {}).get("v0001")
        assert ver_record is not None, "version v1 must exist in _versions"
        ver_hash = ver_record.canonical_hash

        # Hash the actual loaded historical instance
        historical_instance_hash = compute_canonical_hash(historical_v1)

        # All three must match: original v1 == version snapshot == loaded historical
        assert ver_hash == historical_instance_hash, (
            f"version snapshot hash ({ver_hash}) must match "
            f"compute_canonical_hash(historical_v1) ({historical_instance_hash})"
        )
        assert historical_instance_hash == v1_hash, (
            f"historical instance hash ({historical_instance_hash}) must match "
            f"original v1 hash ({v1_hash})"
        )


# =====================================================================
# E. PERSISTENCE ZERO-COMMIT PROOF
# =====================================================================


class TestPersistenceRejectsUnsupported:
    """Persistence paths must roll back on serialization failure."""

    def test_store_rollback_on_set(self):
        """store() with set in nested dict — no record committed."""
        store = InMemoryCanonicalRecordStore()
        sm = SecurityMaster(
            entity_id="E-ROLL", cik="ROLL", exchange="NYSE",
            name="Rollback", primary_ticker="ROLL",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        store.store(sm)
        assert store.contains("SM-01", "E-ROLL")

        scen = ScenarioRecord(
            scenario_id="SCEN-ROLL", case_id="CASE-ITEM8",
            assumptions={"items": {1, 2, 3}},
            intrinsic_value_estimate=1.0, creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TransactionFailure):
            store.store(scen)

        assert store.contains("SM-01", "E-ROLL")
        assert not store.contains("SCEN-01", "SCEN-ROLL")

    def test_store_batch_rollback_on_frozenset(self):
        """store_batch() with frozenset — zero records committed."""
        store = InMemoryCanonicalRecordStore()
        sm = SecurityMaster(
            entity_id="E-B-OK", cik="BOK", exchange="NYSE",
            name="BatchOK", primary_ticker="BOK",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE,
        )
        scen = ScenarioRecord(
            scenario_id="SCEN-ROLL-B", case_id="CASE-ITEM8",
            assumptions={"x": frozenset(["a"])},
            intrinsic_value_estimate=1.0, creator="t",
            scenario_type=ScenarioRecordScenario_type.CURRENT,
        )
        with pytest.raises(TransactionFailure):
            store.store_batch([sm, scen])

        assert not store.contains("SM-01", "E-B-OK")
        assert not store.contains("SCEN-01", "SCEN-ROLL-B")

    def test_financial_fact_store_rejects_bad_nan(self):
        """FinancialFactStore.store() with NaN in dict — zero commit."""
        src_archive = InMemoryRawSourceArchive()
        raw = b"src"
        ch = hashlib.sha256(raw).hexdigest()
        src = SourceRecord(
            source_id="SRC-NAN", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=ch,
            retrieval_date="2024-01-01",
        )
        src_archive.admit_source(src, raw)

        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        ff_store._data.setdefault("CASE-01", {})["CASE-NAN"] = _Record(
            instance=ScenarioRecord(
                scenario_id="DUMMY", case_id="CASE-NAN", assumptions={},
                intrinsic_value_estimate=0, creator="t",
                scenario_type=ScenarioRecordScenario_type.CURRENT,
            ),
            canonical_hash="x",
        )

        scen = ScenarioRecord(
            scenario_id="SCEN-NAN-F", case_id="CASE-NAN",
            assumptions={"val": float("nan")},
            intrinsic_value_estimate=1.0, creator="t",
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
            source_id="SRC-NORM", source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov", content_hash=ch,
            retrieval_date="2024-01-01",
        )
        archive.admit_source(src, raw)
        assert archive.contains("SRC-01", "SRC-NORM")

        ff_store = InMemoryFinancialFactStore(source_archive=archive)
        ff_store._data.setdefault("CASE-01", {})["CASE-NORM"] = _Record(
            instance=object(), canonical_hash="x",
        )
        ff = FinancialFact(
            financial_fact_id="FF-NORM", case_id="CASE-NORM",
            source_id="SRC-NORM", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="500",
        )
        ff_store.store(ff)
        assert ff_store.contains("FF-01", "FF-NORM")