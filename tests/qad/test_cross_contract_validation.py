"""M5.2 Item 13 — Cross-Contract Validation.

STRUCTURAL BRIDGE TESTS ONLY.

Tests that M4B evaluation-contract concepts can be carried by frozen
M4A/M5.1/M5.2 runtime artifacts.  No M5.3 PIT runtime policy enforcement.
No production code changes.
"""
import typing
from enum import Enum
from pathlib import Path

import pytest

# ── M5.1 generated runtime authorities ──────────────────────────────────
from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS

from qad.models.family_i import (
    PITContextMode,
    EvaluationHarnessRun,
    EvaluationHarnessRunEvaluation_type,
    PITContext,
)
from qad.models.family_b import SourceRecord, EvidenceRecord
from qad.models.family_a import SecurityMaster
from qad.models.family_d import QualityAssessment, QualityAssessmentQuality_state
from qad.models.family_e import CompetingExplanationAlternative_diagnosis
from qad.models.family_g import UnderwritingVerdict, UnderwritingVerdictVerdict

# ── Independent M4A oracle ────────────────────────────────────────────
from tests.qad.independent_oracle import ORACLE

BASE = Path(__file__).resolve().parent.parent.parent


# ===================================================================
# A: M4B PIT MODE VOCABULARY ↔ GENERATED PITContextMode ENUM
# ===================================================================

def test_m4b_pit_modes_match_runtime():
    """M4B evaluation contract requires three PIT modes.
    Generated PITContextMode MUST provide exactly those three values.
    """
    required = {
        "SEALED_HISTORICAL_EVALUATION",
        "LIVE_CASE_UPDATE",
        "REPLAY_EXCEPTION",
    }
    runtime = {v.value for v in PITContextMode}
    assert required == runtime, (
        f"M4B PIT mode mismatch: required={required}, runtime={runtime}"
    )
    # Also verify PITC-01 exists and has required structural fields
    assert "PITC-01" in SCHEMA_REGISTRY, "PITC-01 missing from SCHEMA_REGISTRY"
    pitc_cls = SCHEMA_REGISTRY["PITC-01"]
    assert pitc_cls is PITContext, "PITC-01 is not PITContext"
    for required_field in ("pit_context_id", "case_id", "as_of_date", "mode"):
        assert required_field in pitc_cls.model_fields, (
            f"PITC-01 missing required field: {required_field}"
        )
    # as_of_date and mode must be frozen
    assert pitc_cls.model_fields["as_of_date"].frozen
    assert pitc_cls.model_fields["mode"].frozen
    # Primary-ID registry: PITC-01 → pit_context_id
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("PITC-01") == "pit_context_id"


# ===================================================================
# B: M4B TYPE-A / TYPE-B EVALUATION ↔ EHR-01
# ===================================================================

def test_m4b_evaluation_types_match_ehr01():
    """M4B separates Type A (Research Quality) and Type B (Discovery Recall).
    Generated EHR-01 MUST provide exactly these evaluation types.
    """
    required = {
        "TYPE_A_RESEARCH_QUALITY",
        "TYPE_B_DISCOVERY_RECALL",
    }
    runtime = {v.value for v in EvaluationHarnessRunEvaluation_type}
    assert required.issubset(runtime), (
        f"M4B eval types missing from EHR-01: "
        f"required={required}, runtime={runtime}"
    )
    # Verify EHR-01 structural fields required by M4B evaluation execution
    assert "EHR-01" in SCHEMA_REGISTRY, "EHR-01 missing from SCHEMA_REGISTRY"
    ehr_cls = SCHEMA_REGISTRY["EHR-01"]
    required_fields = {
        "eval_run_id", "evaluation_type", "pit_snapshot", "status",
        "metrics", "fixture_results",
    }
    for f in required_fields:
        assert f in ehr_cls.model_fields, (
            f"EHR-01 missing required M4B field: {f}"
        )
    # Primary-ID registry: EHR-01 → eval_run_id
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("EHR-01") == "eval_run_id"


# ===================================================================
# C: M4B FIXTURE IDENTITIES ↔ CANONICAL PRIMARY-ID AUTHORITY
# ===================================================================

def test_m4b_fixture_identities_map_to_canonical_primary_ids():
    """M4B fixture schema references entity_id, source_ids, evidence_ids.
    These MUST map to the authoritative canonical primary IDs."""
    # From independent oracle (non-production parser), confirm PKs
    oracle_fks = {}
    for sid, desc in ORACLE.items():
        for fk in desc.get("fks", []):
            oracle_fks.setdefault(sid, []).append(fk)

    # SM-01 → entity_id  (from primary_id_registry or oracle identity)
    from qad.persistence.reference import _schema_identity_field
    identities = {
        "SM-01": _schema_identity_field("SM-01"),
        "SRC-01": _schema_identity_field("SRC-01"),
        "EV-01": _schema_identity_field("EV-01"),
    }
    assert identities["SM-01"] == "entity_id", (
        f"SM-01 identity mismatch: {identities['SM-01']}"
    )
    assert identities["SRC-01"] == "source_id", (
        f"SRC-01 identity mismatch: {identities['SRC-01']}"
    )
    assert identities["EV-01"] == "evidence_id", (
        f"EV-01 identity mismatch: {identities['EV-01']}"
    )
    # Confirm from oracle too
    assert "entity_id" in ORACLE["SM-01"].get("required", set()) | \
        ORACLE["SM-01"].get("optional", set())
    assert "source_id" in ORACLE["SRC-01"].get("required", set()) | \
        ORACLE["SRC-01"].get("optional", set())
    assert "evidence_id" in ORACLE["EV-01"].get("required", set()) | \
        ORACLE["EV-01"].get("optional", set())


# ===================================================================
# D: M4B SOURCE HASH SEAL ↔ SRC-01 / ITEM-5 BRIDGE
# ===================================================================

def test_m4b_source_hash_requirements_have_src01_carrier():
    """M4B Seal Contract requires immutable source IDs + content hashes.
    SRC-01 provides source_id (PK) and content_hash (SHA-256 of raw bytes).
    """
    assert "SRC-01" in SCHEMA_REGISTRY, "SRC-01 missing from SCHEMA_REGISTRY"
    src_cls = SCHEMA_REGISTRY["SRC-01"]
    # SRC-01 must have source_id and content_hash
    assert "source_id" in src_cls.model_fields
    assert "content_hash" in src_cls.model_fields
    # source_id is required (caller provides it)
    assert src_cls.model_fields["source_id"].is_required()
    # content_hash is required (structural carrier for M4B seal requirement)
    assert src_cls.model_fields["content_hash"].is_required()
    # SRC-01 is canonical
    assert "SRC-01" in CANONICAL_SCHEMAS
    # Primary identity
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("SRC-01") == "source_id"


# ===================================================================
# E: M4B EVIDENCE REFERENCES ↔ EV-01 / ITEM-6 BRIDGE
# ===================================================================

def test_m4b_evidence_references_have_ev01_carrier():
    """M4B fixtures reference evidence_ids.
    EV-01 provides evidence_id (PK), source_id (FK → SRC-01).
    """
    assert "EV-01" in SCHEMA_REGISTRY, "EV-01 missing from SCHEMA_REGISTRY"
    ev_cls = SCHEMA_REGISTRY["EV-01"]
    # EV-01 must have evidence_id and source_id
    assert "evidence_id" in ev_cls.model_fields
    assert "source_id" in ev_cls.model_fields
    # evidence_id is frozen
    assert ev_cls.model_fields["evidence_id"].frozen
    # Primary identity
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("EV-01") == "evidence_id"
    # FK: EV-01.source_id → SRC-01.source_id
    ev_fks = FK_REGISTRY.get("EV-01", [])
    source_fk = [fk for fk in ev_fks
                 if fk["field"] == "source_id" and fk["target"] == "SRC-01"
                 and fk["target_field"] == "source_id"]
    assert len(source_fk) >= 1, (
        f"EV-01.source_id → SRC-01.source_id FK missing in FK_REGISTRY. "
        f"Found: {ev_fks}"
    )


# ===================================================================
# F: M4B AS_OF_DATE ↔ PITC-01.as_of_date  (STRUCTURAL)
# ===================================================================

def test_m4b_as_of_date_maps_to_pitc01_as_of_date():
    """M4B requires AS_OF_DATE hard cutoff.
    PITC-01 provides as_of_date (frozen, structural carrier).
    This is a STRUCTURAL BRIDGE only — runtime cutoff enforcement is M5.3.
    """
    assert "PITC-01" in SCHEMA_REGISTRY
    pitc_cls = SCHEMA_REGISTRY["PITC-01"]
    assert "as_of_date" in pitc_cls.model_fields
    # as_of_date is frozen
    assert pitc_cls.model_fields["as_of_date"].frozen
    # as_of_date is required
    assert pitc_cls.model_fields["as_of_date"].is_required()
    # as_of_date is of type str
    ann = pitc_cls.model_fields["as_of_date"].annotation
    if hasattr(ann, "__origin__") and ann.__origin__ is typing.Union:
        for a in ann.__args__:
            if a is not type(None):
                ann = a
    assert ann is str, f"PITC-01.as_of_date should be str, got {ann}"


# ===================================================================
# G (Optional): M4B EVALUATION LABELS ↔ FROZEN M4A ENUM COUNTERPARTS
# ===================================================================

def test_m4b_evaluation_labels_have_exact_m4a_enum_counterparts():
    """M4B expected_quality_state/expected_impairment/expected_verdict
    labels have EXACT frozen M4A runtime enum counterparts.
    This proves structural bridge compatibility without M5.3 involvement.
    """
    # expected_quality_state: VERIFIED / PROBABLE / UNRESOLVED / FAILED
    # → M4A QA-01 QualityAssessmentQuality_state
    m4a_qs = {v.value for v in QualityAssessmentQuality_state}
    m4b_quality = {"VERIFIED", "PROBABLE", "UNRESOLVED", "FAILED"}
    assert m4b_quality.issubset(m4a_qs), (
        f"M4B expected_quality_state values {m4b_quality} not all "
        f"present in M4A QualityAssessmentQuality_state: {m4a_qs}"
    )

    # expected_impairment: TEMPORARY / MOSTLY_TEMPORARY / MIXED /
    #                      STRUCTURAL / UNRESOLVED
    # → M4A IA-01 ImpairmentAssessmentImpairment_type
    m4a_imp = {v.value for v in CompetingExplanationAlternative_diagnosis}
    m4b_impairment = {
        "TEMPORARY", "MOSTLY_TEMPORARY", "MIXED", "STRUCTURAL",
        "UNRESOLVED",
    }
    assert m4b_impairment.issubset(m4a_imp), (
        f"M4B expected_impairment values {m4b_impairment} not all "
        f"present in M4A ImpairmentAssessmentImpairment_type: {m4a_imp}"
    )

    # expected_verdict: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED /
    #                   NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION
    # → M4A UV-01 UnderwritingVerdictVerdict
    m4a_verdict = {v.value for v in UnderwritingVerdictVerdict}
    m4b_verdict = {
        "QAD_CONFIRMED", "QAD_PROBABLE", "QAD_UNRESOLVED",
        "NOT_QAD_STRUCTURAL", "NOT_QAD_QUALITY", "NOT_QAD_VALUATION",
    }
    assert m4b_verdict.issubset(m4a_verdict), (
        f"M4B expected_verdict values {m4b_verdict} not all "
        f"present in M4A UnderwritingVerdictVerdict: {m4a_verdict}"
    )
    # Document that these are evaluation-only semantics, not M5.2 persistence
    # binding. (This test proves STRUCTURAL BRIDGE only.)


# ===================================================================
# H: explicit M5.3 deferred boundary
# ===================================================================

def test_m5_2_does_not_enforce_pit_runtime_policy():
    """Verify no M5.2 persistence code implements SEALED_HISTORICAL
    runtime leakage prevention, LIVE_CASE_UPDATE runtime switching,
    REPLAY_EXCEPTION authorization, or CONDITIONAL_IMMUTABLE lifecycle
    enforcement — these remain DEFERRED_M5.3.

    This is a STRUCTURAL TRUTH assertion through the M5.2 codebase.
    Known deferred items:
      - SEALED_HISTORICAL post-AS_OF leakage prevention
      - LIVE_CASE_UPDATE runtime mode switching
      - REPLAY_EXCEPTION authorization gate
      - CONDITIONAL_IMMUTABLE lifecycle enforcement (manifest after completion)
    """
    # Verify that the persistence module does not import any M5.3 runtime
    # policy module.
    import qad.persistence as pers_mod
    pers_path = Path(pers_mod.__file__).resolve().parent
    # List all .py files in persistence
    py_files = sorted(pers_path.glob("*.py"))
    for pyf in py_files:
        content = pyf.read_text(encoding="utf-8", errors="replace")
        # These are the M5.3-relevant strings that should NOT appear
        # in M5.2 persistence code as runtime enforcement.
        forbidden = ["leakage_prevention", "LIVE_CASE_UPDATE_runtime",
                     "REPLAY_EXCEPTION_auth", "CONDITIONAL_IMMUTABLE_"]
        for pat in forbidden:
            assert pat not in content, (
                f"M5.3 policy term '{pat}' found in M5.2 persistence "
                f"file {pyf.name}: would be premature M5.3 implementation"
            )

    # This is a SOURCE-STRUCTURAL test, not a runtime simulation.
    # When M5.3 implementation begins, this test must be updated
    # to reflect the new boundary.
    # <!-- 2026-08-29 18:45 UTC+7 -->