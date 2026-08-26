"""M5.2 Item 7 — REAL FINANCIAL FACT LINEAGE.

Adversarial tests proving that the financial lineage correctly preserves
the frozen topology: FF, NFF via formal FK, CALC with provenance, SCEN standalone.
"""

from __future__ import annotations

import hashlib

import pytest

from qad.persistence.errors import IntegrityConflict, MissingForeignKey
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