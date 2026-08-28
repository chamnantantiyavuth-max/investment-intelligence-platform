"""M5.2 Item 7 — REAL FINANCIAL FACT LINEAGE.

Adversarial tests proving that the financial lineage correctly preserves
the frozen topology: FF, NFF via formal FK, CALC with provenance, SCEN standalone.
"""

from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import CanonicalBoundaryViolation, IntegrityConflict, ImmutabilityViolation, MissingForeignKey, TransactionFailure
from qad.persistence.reference import (
    InMemoryFinancialFactStore,
    InMemoryRawSourceArchive,
    _Record,
)
from qad.persistence.serialization import compute_canonical_hash
from qad.models.family_a import (
    SecurityMaster,
    SecurityMasterSecurity_type,
    SecurityMasterStatus,
    SignalRecord,
    SignalRecordSignal_type,
    SignalRecordSignal_family,
    SignalRecordEntry_route,
    CandidateRecord,
    CandidateRecordEntry_route,
    CandidateRecordSelection_state,
    CaseRecord,
    CaseRecordCase_state,
)
from qad.models.family_b import (
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
# Helpers
# =====================================================================

_COUNTER = 0


def _cid():
    global _COUNTER
    _COUNTER += 1
    return f"CASE-{_COUNTER:03d}"


def _inject(store, schema_id, record_id, instance):
    """Inject a record directly into _data (bypasses Transaction)."""
    ch = compute_canonical_hash(instance)
    store._data.setdefault(schema_id, {})[record_id] = _Record(
        instance=instance, canonical_hash=ch,
    )


def _inject_case(store, case_id):
    """Inject all FK ancestors then CASE-01 via direct _data injection."""
    _inject(store, "SM-01", "E-FAKE", SecurityMaster(
        entity_id="E-FAKE", cik="X", exchange="NYSE", name="Fake",
        primary_ticker="FAKE",
        security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
        status=SecurityMasterStatus.ACTIVE,
    ))
    _inject(store, "SR-01", "S-FAKE", SignalRecord(
        signal_id="S-FAKE", entity_id="E-FAKE",
        signal_type=SignalRecordSignal_type.QUALITY,
        signal_family=SignalRecordSignal_family.GOVERNANCE,
        entry_route=SignalRecordEntry_route.QUALITY_FIRST,
        detection_timestamp="2024-01-01T00:00:00",
    ))
    _inject(store, "CR-01", "C-FAKE", CandidateRecord(
        candidate_id="C-FAKE", entity_id="E-FAKE",
        entry_route=CandidateRecordEntry_route.QUALITY_FIRST,
        entry_timestamp="2024-01-01T00:00:00",
        evidence_freshness="2024-01-20",
        selection_state=CandidateRecordSelection_state.AUTO_RESEARCH_NOW,
        signal_ids=["S-FAKE"],
    ))
    _inject(store, "CASE-01", case_id, CaseRecord(
        case_id=case_id, entity_id="E-FAKE", candidate_id="C-FAKE",
        case_state=CaseRecordCase_state.CASE_OPEN,
        as_of_date="2024-01-01", opened_at="2024-01-01T00:00:00",
        research_director="test",
    ))


def _make_src(archive, raw, source_id="SRC-ITEM7"):
    ch = hashlib.sha256(raw).hexdigest()
    src = SourceRecord(
        source_id=source_id,
        source_tier=SourceRecordSource_tier.L1,
        source_type=SourceRecordSource_type.SEC_FILING,
        url_or_identifier=f"https://sec.gov/src-{source_id}",
        content_hash=ch,
        retrieval_date="2024-01-01",
    )
    archive.admit_source(src, raw)
    return src


def _paired_store():
    """RawSourceArchive + FinancialFactStore with injected case CASE-001."""
    src_archive = InMemoryRawSourceArchive()
    ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
    _inject_case(ff_store, "CASE-001")
    return src_archive, ff_store


def _ff_store_only():
    """FinancialFactStore with injected case CASE-001 (no source archive)."""
    ff_store = InMemoryFinancialFactStore()
    _inject_case(ff_store, "CASE-001")
    return ff_store


# =====================================================================
# Tests
# =====================================================================

class TestPrimaryIDs:
    def test_ff_uses_financial_fact_id(self):
        src_archive, ff_store = _paired_store()
        _make_src(src_archive, b"s", "SRC-ID-FF")
        ff = FinancialFact(financial_fact_id="FF-UNIQUE", case_id="CASE-001",
            source_id="SRC-ID-FF", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")
        ff_store.store(ff)
        assert ff_store.contains("FF-01", "FF-UNIQUE")

    def test_nff_uses_normalized_fact_id(self):
        ff_store = _ff_store_only()
        _inject(ff_store, "FF-01", "FF-PARENT", FinancialFact(
            financial_fact_id="FF-PARENT", case_id="CASE-001",
            source_id="SRC-FAKE", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000"))
        nff = NormalizedFinancialFact(normalized_fact_id="NFF-UNIQUE",
            financial_fact_id="FF-PARENT", adjusted_value="900",
            adjuster="test", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)
        ff_store.store(nff)
        assert ff_store.contains("NFF-01", "NFF-UNIQUE")

    def test_calc_uses_calculation_id(self):
        ff_store = _ff_store_only()
        calc = CalculationRecord(calculation_id="CALC-UNIQUE", case_id="CASE-001",
            formula="x*2", inputs=["x=500"], result="1000",
            calculated_by="test", timestamp="2024-01-01")
        ff_store.store(calc)
        assert ff_store.contains("CALC-01", "CALC-UNIQUE")

    def test_scen_uses_scenario_id(self):
        ff_store = _ff_store_only()
        scen = ScenarioRecord(scenario_id="SCEN-UNIQUE", case_id="CASE-001",
            assumptions={"growth": 0.05}, intrinsic_value_estimate=1000.0,
            creator="test", scenario_type=ScenarioRecordScenario_type.CURRENT)
        ff_store.store(scen)
        assert ff_store.contains("SCEN-01", "SCEN-UNIQUE")


class TestNFFLineage:
    def test_multiple_nff_per_ff(self):
        src_archive, ff_store = _paired_store()
        _make_src(src_archive, b"s", "SRC-NFF")
        ff = FinancialFact(financial_fact_id="FF-MULTI", case_id="CASE-001",
            source_id="SRC-NFF", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")
        ff_store.store(ff)
        for i, adj in enumerate([("NFF-M1", "900"), ("NFF-M2", "800")]):
            ff_store.store(NormalizedFinancialFact(
                normalized_fact_id=adj[0], financial_fact_id="FF-MULTI",
                adjusted_value=adj[1], adjuster="a", adjustment_rationale="a",
                adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING))
        assert ff_store.contains("NFF-01", "NFF-M1")
        assert ff_store.contains("NFF-01", "NFF-M2")
        assert ff_store.contains("FF-01", "FF-MULTI")

    def test_nff_lineage_returns_ff_then_nff(self):
        src_archive, ff_store = _paired_store()
        _make_src(src_archive, b"s", "SRC-LIN")
        ff_store.store(FinancialFact(financial_fact_id="FF-LIN", case_id="CASE-001",
            source_id="SRC-LIN", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000"))
        ff_store.store(NormalizedFinancialFact(normalized_fact_id="NFF-LIN",
            financial_fact_id="FF-LIN", adjusted_value="900", adjuster="t",
            adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING))
        lineage = ff_store.get_lineage("NFF-01", "NFF-LIN")
        assert len(lineage) == 2
        assert lineage[0].financial_fact_id == "FF-LIN"
        assert lineage[1].normalized_fact_id == "NFF-LIN"


class TestCALCRoundTrip:
    def test_calc_formula_inputs_result_round_trip(self):
        ff_store = _ff_store_only()
        calc = CalculationRecord(calculation_id="CALC-RT", case_id="CASE-001",
            formula="revenue*0.3", inputs=["revenue=1000"], result="300",
            calculated_by="test", timestamp="2024-01-01",
            input_fact_ids=["FF-100"])
        ff_store.store(calc)
        loaded = ff_store.load("CALC-01", "CALC-RT")
        assert loaded.formula == "revenue*0.3"
        assert loaded.inputs == ["revenue=1000"]
        assert loaded.result == "300"
        assert loaded.input_fact_ids == ["FF-100"]


class TestSCENStandalone:
    def test_scen_assumptions_round_trip(self):
        ff_store = _ff_store_only()
        a = {"rate": 0.05}
        scen = ScenarioRecord(scenario_id="SCEN-RT", case_id="CASE-001",
            assumptions=a, intrinsic_value_estimate=5000.0,
            creator="test", scenario_type=ScenarioRecordScenario_type.CURRENT)
        ff_store.store(scen)
        assert ff_store.load("SCEN-01", "SCEN-RT").assumptions == a


class TestGetLineage:
    def test_each_schema(self):
        src_archive, ff_store = _paired_store()
        _make_src(src_archive, b"s", "SRC-LIN")
        ff_store.store(FinancialFact(financial_fact_id="FF-L", case_id="CASE-001",
            source_id="SRC-LIN", fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="100"))
        ff_store.store(NormalizedFinancialFact(normalized_fact_id="NFF-L",
            financial_fact_id="FF-L", adjusted_value="90", adjuster="t",
            adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING))
        ff_store.store(CalculationRecord(calculation_id="CALC-L", case_id="CASE-001",
            formula="x*0.9", inputs=["x=100"], result="90",
            calculated_by="t", timestamp="2024-01-01"))
        ff_store.store(ScenarioRecord(scenario_id="SCEN-L", case_id="CASE-001",
            assumptions={}, intrinsic_value_estimate=90.0,
            creator="t", scenario_type=ScenarioRecordScenario_type.CURRENT))
        assert len(ff_store.get_lineage("FF-01", "FF-L")) == 1
        assert len(ff_store.get_lineage("NFF-01", "NFF-L")) == 2
        assert len(ff_store.get_lineage("CALC-01", "CALC-L")) == 1
        assert len(ff_store.get_lineage("SCEN-01", "SCEN-L")) == 1

    def test_unsupported_raises(self):
        with pytest.raises(TypeError):
            InMemoryFinancialFactStore().get_lineage("SM-01", "X")

    def test_nonexistent_raises(self):
        with pytest.raises(KeyError):
            InMemoryFinancialFactStore().get_lineage("FF-01", "GHOST")


class TestFFSourceAuthority:
    def test_missing_source_rejected(self):
        _, ff_store = _paired_store()
        with pytest.raises(MissingForeignKey):
            ff_store.store(FinancialFact(financial_fact_id="FF-X", case_id="CASE-001",
                source_id="SRC-NOPE", fiscal_year="2024",
                metric_name=FinancialFactMetric_family.REVENUE,
                period="FY", unit="USD", value="100"))

    def test_tombstoned_source_rejected(self):
        sa, ff = _paired_store()
        _make_src(sa, b"s", "SRC-T")
        sa.tombstone("SRC-T", "gone")
        with pytest.raises(MissingForeignKey):
            ff.store(FinancialFact(financial_fact_id="FF-T", case_id="CASE-001",
                source_id="SRC-T", fiscal_year="2024",
                metric_name=FinancialFactMetric_family.REVENUE,
                period="FY", unit="USD", value="100"))


class TestItems1to6Regression:
    def test_item1_primary_id_preserved(self):
        store = InMemoryFinancialFactStore()
        sm = SecurityMaster(entity_id="E-R7", cik="R7", exchange="NYSE",
            name="Reg7", primary_ticker="RG7",
            security_type=SecurityMasterSecurity_type.COMMON_EQUITY,
            status=SecurityMasterStatus.ACTIVE)
        store.store(sm)
        assert store.load("SM-01", "E-R7").entity_id == "E-R7"


# =====================================================================
# M5.2 Item 7 — Final Public-Path + Incomplete-Lineage Closure
# =====================================================================
# A. CLOSE FINANCIAL STORE SRC-01 SHADOW / BATCH BYPASS
# =====================================================================

SHA256 = hashlib.sha256


class TestStoreBatchAuthorityClosure:
    """Prove FinancialFactStore.store_batch() enforces source authority."""

    def test_direct_store_src01_on_financial_store_rejected(self):
        """FinancialFactStore.store(SRC-01) must raise."""
        store = InMemoryFinancialFactStore()
        src = SourceRecord(source_id="SHADOW",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/shadow",
            content_hash=SHA256(b"x").hexdigest(),
            retrieval_date="2024-01-01")
        with pytest.raises(CanonicalBoundaryViolation):
            store.store(src)

    def test_store_batch_shadow_src_plus_ff_rejected(self):
        """Batch containing shadow SRC-01 + FF-01 must be rejected
        and leave zero records committed."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        # Shadow SRC — never admitted through RawSourceArchive
        src = SourceRecord(source_id="SHADOW-SRC",
            source_tier=SourceRecordSource_tier.L1,
            source_type=SourceRecordSource_type.SEC_FILING,
            url_or_identifier="https://sec.gov/shadow",
            content_hash=SHA256(b"x").hexdigest(),
            retrieval_date="2024-01-01")

        ff = FinancialFact(financial_fact_id="FF-SHADOW-BATCH",
            case_id="CASE-001", source_id="SHADOW-SRC",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        # SR-01 in batch must be rejected before Transaction touches data
        with pytest.raises(CanonicalBoundaryViolation):
            ff_store.store_batch([src, ff])

        # Prove zero records committed
        assert not ff_store.contains("SRC-01", "SHADOW-SRC")
        assert not ff_store.contains("FF-01", "FF-SHADOW-BATCH")

    def test_store_batch_ff_with_authoritative_source_succeeds(self):
        """FF with real RawSourceArchive-admitted SRC works in batch."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        raw = b"real content"
        _make_src(src_archive, raw, "SRC-AUTH")

        ff = FinancialFact(financial_fact_id="FF-AUTH-BATCH",
            case_id="CASE-001", source_id="SRC-AUTH",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        hashes = ff_store.store_batch([ff])
        assert len(hashes) == 1
        assert ff_store.contains("FF-01", "FF-AUTH-BATCH")

    def test_store_batch_ff_plus_nff_with_authoritative_source_succeeds(self):
        """FF + NFF referencing same FF in same batch (same-batch FK resolution)."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"x", "SRC-BATCH-NFF")

        ff = FinancialFact(financial_fact_id="FF-BATCH-NFF",
            case_id="CASE-001", source_id="SRC-BATCH-NFF",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        nff = NormalizedFinancialFact(normalized_fact_id="NFF-BATCH",
            financial_fact_id="FF-BATCH-NFF", adjusted_value="900",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)

        hashes = ff_store.store_batch([ff, nff])
        assert len(hashes) == 2
        assert ff_store.contains("FF-01", "FF-BATCH-NFF")
        assert ff_store.contains("NFF-01", "NFF-BATCH")

        # Full lineage should work
        lineage = ff_store.get_lineage("NFF-01", "NFF-BATCH")
        assert len(lineage) == 2
        assert lineage[0].financial_fact_id == "FF-BATCH-NFF"

    def test_tombstoned_authoritative_source_rejects_ff_batch(self):
        """FF referencing a tombstoned SRC must be rejected in batch."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"x", "SRC-TOMB")
        src_archive.tombstone("SRC-TOMB", "test tombstone")

        ff = FinancialFact(financial_fact_id="FF-TOMB-BATCH",
            case_id="CASE-001", source_id="SRC-TOMB",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        with pytest.raises(MissingForeignKey):
            ff_store.store_batch([ff])

        assert not ff_store.contains("FF-01", "FF-TOMB-BATCH")

    def test_corrupted_raw_binding_rejects_single_store(self):
        """store(FF) must reject when the raw-byte binding is corrupted."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        # Admit source with real bytes
        _make_src(src_archive, b"real content", "SRC-CORRUPT")

        # Corrupt the binding: store a different blob in the archive
        src_archive._raw_blobs["SRC-CORRUPT"] = b"different bytes"

        ff = FinancialFact(financial_fact_id="FF-CORRUPT",
            case_id="CASE-001", source_id="SRC-CORRUPT",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        with pytest.raises(MissingForeignKey):
            ff_store.store(ff)

        assert not ff_store.contains("FF-01", "FF-CORRUPT")

    def test_corrupted_raw_binding_rejects_store_batch(self):
        """store_batch([FF]) must reject when the raw-byte binding is corrupted."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"real", "SRC-CORRUPT-B")
        src_archive._raw_blobs["SRC-CORRUPT-B"] = b"different bytes"

        ff = FinancialFact(financial_fact_id="FF-CORRUPT-B",
            case_id="CASE-001", source_id="SRC-CORRUPT-B",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="1000")

        with pytest.raises(MissingForeignKey):
            ff_store.store_batch([ff])

        assert not ff_store.contains("FF-01", "FF-CORRUPT-B")


# =====================================================================
# B. CALC PROVENANCE MUST NOT FAIL SILENTLY
# =====================================================================

class TestCALCProvenance:
    """CALC input_fact_ids provenance must surface deterministically."""

    def test_calc_resolved_provenance_two_ff(self):
        """CALC with two real FF input_fact_ids returns ordered lineage."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"a", "SRC-C1")
        _make_src(src_archive, b"b", "SRC-C2")

        ff_store.store(FinancialFact(financial_fact_id="FF-C1",
            case_id="CASE-001", source_id="SRC-C1",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="100"))
        ff_store.store(FinancialFact(financial_fact_id="FF-C2",
            case_id="CASE-001", source_id="SRC-C2",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="200"))

        calc = CalculationRecord(calculation_id="CALC-PROV",
            case_id="CASE-001", formula="a+b", inputs=["a=100", "b=200"],
            result="300", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-C1", "FF-C2"])
        ff_store.store(calc)

        lineage = ff_store.get_lineage("CALC-01", "CALC-PROV")
        assert len(lineage) == 3  # CALC + FF-C1 + FF-C2
        assert lineage[0].calculation_id == "CALC-PROV"
        # Order deterministic per input_fact_ids
        assert lineage[1].financial_fact_id == "FF-C1"
        assert lineage[2].financial_fact_id == "FF-C2"

    def test_calc_unresolved_provenance_raises(self):
        """CALC with one valid + one missing input_fact_id raises error."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"a", "SRC-C3")
        ff_store.store(FinancialFact(financial_fact_id="FF-C3",
            case_id="CASE-001", source_id="SRC-C3",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="100"))

        # CALC references one real FF and one ghost
        calc = CalculationRecord(calculation_id="CALC-GHOST",
            case_id="CASE-001", formula="a+b", inputs=["a=100", "b=0"],
            result="100", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-C3", "FF-GHOST"])
        ff_store.store(calc)  # Store-time must be permitted (not formal FK)

        # get_lineage must surface the incomplete provenance
        with pytest.raises(KeyError) as exc:
            ff_store.get_lineage("CALC-01", "CALC-GHOST")
        msg = str(exc.value)
        assert "incomplete provenance" in msg
        assert "FF-GHOST" in msg

    def test_calc_unresolved_store_permitted(self):
        """CALC with unresolved input_fact_ids stores without error.
        input_fact_ids is provenance-only, NOT a formal FK."""
        ff_store = _ff_store_only()
        calc = CalculationRecord(calculation_id="CALC-STORE-OK",
            case_id="CASE-001", formula="x*2", inputs=["x=500"],
            result="1000", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-GHOST"])
        # This must NOT raise MissingForeignKey
        ff_store.store(calc)
        assert ff_store.contains("CALC-01", "CALC-STORE-OK")


# =====================================================================
# C. NFF FORMAL PARENT MUST NOT FAIL SILENTLY
# =====================================================================

class TestNFFParentMissing:
    """NFF.financial_fact_id is a frozen formal FK — must fail loudly."""

    def test_nff_valid_lineage(self):
        """Normal NFF with existing FF parent returns [FF, NFF]."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"p", "SRC-PARENT")
        ff_store.store(FinancialFact(financial_fact_id="FF-PARENT",
            case_id="CASE-001", source_id="SRC-PARENT",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="500"))
        ff_store.store(NormalizedFinancialFact(normalized_fact_id="NFF-PARENT",
            financial_fact_id="FF-PARENT", adjusted_value="400",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING))

        lineage = ff_store.get_lineage("NFF-01", "NFF-PARENT")
        assert len(lineage) == 2
        assert lineage[0].financial_fact_id == "FF-PARENT"
        assert lineage[1].normalized_fact_id == "NFF-PARENT"

    def test_nff_missing_parent_fails_deterministically(self):
        """NFF whose formal FF parent is absent must raise deterministically.
        This is a controlled adversarial read-path test: the NFF is injected
        directly (corrupted/historical state simulation)."""
        ff_store = InMemoryFinancialFactStore()
        _inject_case(ff_store, "CASE-001")

        # Inject NFF with a ghost parent FF — corrupted state simulation
        _inject(ff_store, "NFF-01", "NFF-ORPHAN", NormalizedFinancialFact(
            normalized_fact_id="NFF-ORPHAN",
            financial_fact_id="FF-GHOST-PARENT",
            adjusted_value="100", adjuster="t",
            adjustment_rationale="corrupted state test",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING))

        with pytest.raises(KeyError) as exc:
            ff_store.get_lineage("NFF-01", "NFF-ORPHAN")
        msg = str(exc.value)
        assert "NFF-01" in msg
        assert "FF-GHOST-PARENT" in msg
        assert "not found" in msg.lower()
        assert "complete lineage" in msg.lower()


# =====================================================================
# D. IMMUTABILITY PROOF
# =====================================================================

class TestFinancialLineageImmutability:
    """Canonical lineage fields cannot be mutated in place."""

    def test_nff_financial_fact_id_mutation_rejected(self):
        """NFF.financial_fact_id mutation after first store must be rejected."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"x", "SRC-IMM")
        ff_store.store(FinancialFact(financial_fact_id="FF-IMM",
            case_id="CASE-001", source_id="SRC-IMM",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="100"))

        nff = NormalizedFinancialFact(normalized_fact_id="NFF-IMM",
            financial_fact_id="FF-IMM", adjusted_value="90",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)
        ff_store.store(nff)

        # Try to mutate financial_fact_id (immutable FK field)
        mutated = NormalizedFinancialFact(normalized_fact_id="NFF-IMM",
            financial_fact_id="FF-DIFFERENT", adjusted_value="90",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)
        with pytest.raises(TransactionFailure):
            ff_store.store(mutated)

        # Original NFF must remain intact
        loaded = ff_store.load("NFF-01", "NFF-IMM")
        assert loaded.financial_fact_id == "FF-IMM"
        # Original FF must remain intact
        assert ff_store.contains("FF-01", "FF-IMM")

    def test_calc_fields_mutation_rejected(self):
        """CALC input_fact_ids/formula/result mutation after store rejected."""
        ff_store = _ff_store_only()
        calc = CalculationRecord(calculation_id="CALC-IMM",
            case_id="CASE-001", formula="x*2", inputs=["x=500"],
            result="1000", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-OLD"])
        ff_store.store(calc)

        # Try to mutate formula
        mutated = CalculationRecord(calculation_id="CALC-IMM",
            case_id="CASE-001", formula="x*3", inputs=["x=500"],
            result="1500", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-OLD"])
        with pytest.raises(TransactionFailure):
            ff_store.store(mutated)

        # Try to mutate input_fact_ids
        mutated2 = CalculationRecord(calculation_id="CALC-IMM",
            case_id="CASE-001", formula="x*2", inputs=["x=500"],
            result="1000", calculated_by="t", timestamp="2024-01-01",
            input_fact_ids=["FF-NEW"])
        with pytest.raises(TransactionFailure):
            ff_store.store(mutated2)

        # Original CALC preserved
        loaded = ff_store.load("CALC-01", "CALC-IMM")
        assert loaded.formula == "x*2"
        assert loaded.input_fact_ids == ["FF-OLD"]

    def test_ff_preserved_after_nff_mutation_attempt(self):
        """Raw FF unchanged after NFF creation and failed NFF mutation."""
        src_archive = InMemoryRawSourceArchive()
        ff_store = InMemoryFinancialFactStore(source_archive=src_archive)
        _inject_case(ff_store, "CASE-001")

        _make_src(src_archive, b"x", "SRC-PRES")
        ff_store.store(FinancialFact(financial_fact_id="FF-PRES",
            case_id="CASE-001", source_id="SRC-PRES",
            fiscal_year="2024",
            metric_name=FinancialFactMetric_family.REVENUE,
            period="FY", unit="USD", value="777"))

        nff = NormalizedFinancialFact(normalized_fact_id="NFF-PRES",
            financial_fact_id="FF-PRES", adjusted_value="700",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)
        ff_store.store(nff)

        # Confirm FF still has original value
        ff_loaded = ff_store.load("FF-01", "FF-PRES")
        assert ff_loaded.value == "777"

        # Failed mutation attempt
        mutated = NormalizedFinancialFact(normalized_fact_id="NFF-PRES",
            financial_fact_id="FF-DIFFERENT", adjusted_value="700",
            adjuster="t", adjustment_rationale="adj",
            adjustment_type=NormalizedFinancialFactAdjustment_type.NON_RECURRING)
        try:
            ff_store.store(mutated)
        except TransactionFailure:
            pass

        # FF must still be intact after failed mutation
        ff_loaded2 = ff_store.load("FF-01", "FF-PRES")
        assert ff_loaded2.value == "777"