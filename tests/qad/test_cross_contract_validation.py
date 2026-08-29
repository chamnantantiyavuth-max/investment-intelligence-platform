"""M5.2 Item 13 — Cross-Contract Validation.

STRUCTURAL BRIDGE TESTS ONLY.

Tests that M4B evaluation-contract concepts are structurally supported by
frozen M4A/M5.1/M5.2 runtime artifacts.  Every test reads the actual frozen
M4B contract artifact as its upstream authority.

No M5.3 PIT runtime policy enforcement.
No production code changes.
"""
import typing
from pathlib import Path

import pytest

# ── M5.1 generated runtime authorities ──────────────────────────────────
from qad.models import SCHEMA_REGISTRY
from qad.contract.fk_registry import FK_REGISTRY
from qad.contract.canonical_boundary import CANONICAL_SCHEMAS

from qad.models.family_i import (
    PITContextMode,
    EvaluationHarnessRunEvaluation_type,
    PITContext,
)
from qad.models.family_d import QualityAssessmentQuality_state
from qad.models.family_e import ImpairmentAssessmentDiagnosis
from qad.models.family_g import UnderwritingVerdictVerdict

# ── Independent M4A oracle ────────────────────────────────────────────
from tests.qad.independent_oracle import ORACLE

BASE = Path(__file__).resolve().parent.parent.parent
M4B_CONTRACT_PATH = BASE / "design" / "qad-pivot" / "m4b" / "QAD-M4B-EVALUATION-CONTRACT.md"
M4B_CONTRACT_TEXT = M4B_CONTRACT_PATH.read_text(encoding="utf-8")


# ===================================================================
# 1: M4B SEALED EVALUATION MODE ↔ PIT RUNTIME CARRIER
# ===================================================================

def test_m4b_sealed_evaluation_mode_is_supported_by_pit_runtime():
    """M4B evaluation contract requires SEALED_HISTORICAL_EVALUATION mode
    for sealed evaluation (see §2.2 PIT Enforcement).

    Frozen M4A/PIT runtime provides SEALED_HISTORICAL_EVALUATION plus
    LIVE_CASE_UPDATE and REPLAY_EXCEPTION as the broader PIT vocabulary.
    This test proves the M4B-required mode is supported.
    """
    # 1. Verify M4B contract explicitly requires SEALED_HISTORICAL_EVALUATION
    assert "SEALED_HISTORICAL_EVALUATION" in M4B_CONTRACT_TEXT, (
        "M4B contract missing SEALED_HISTORICAL_EVALUATION mode"
    )
    # 2. Generated PITContextMode supports that exact required mode
    runtime_values = {v.value for v in PITContextMode}
    assert "SEALED_HISTORICAL_EVALUATION" in runtime_values, (
        "SEALED_HISTORICAL_EVALUATION missing from PITContextMode"
    )
    # 3. PITC-01 exists and structurally carries required fields
    assert "PITC-01" in SCHEMA_REGISTRY, "PITC-01 missing from SCHEMA_REGISTRY"
    pitc_cls = SCHEMA_REGISTRY["PITC-01"]
    assert pitc_cls is PITContext, "PITC-01 is not PITContext"
    for required_field in ("pit_context_id", "case_id", "as_of_date", "mode"):
        assert required_field in pitc_cls.model_fields, (
            f"PITC-01 missing required field: {required_field}"
        )
    # 4. as_of_date and mode are frozen
    assert pitc_cls.model_fields["as_of_date"].frozen
    assert pitc_cls.model_fields["mode"].frozen
    # 5. Primary-ID registry: PITC-01 → pit_context_id
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("PITC-01") == "pit_context_id"


# ===================================================================
# 2: M4B TYPE A / TYPE B ↔ EHR-01
# ===================================================================

def test_m4b_type_a_and_type_b_are_supported_by_ehr01():
    """M4B separates Type A (Research Quality) and Type B (Discovery Recall)
    as distinct evaluation typologies (see §1 Evaluation Typology).

    Generated EHR-01 provides TYPE_A_RESEARCH_QUALITY and
    TYPE_B_DISCOVERY_RECALL as evaluation_type enum members.
    """
    # 1. Verify M4B contract defines Type A and Type B
    assert "TYPE A" in M4B_CONTRACT_TEXT, "M4B missing Type A"
    assert "TYPE B" in M4B_CONTRACT_TEXT, "M4B missing Type B"
    assert "research quality" in M4B_CONTRACT_TEXT.lower()
    assert "discovery recall" in M4B_CONTRACT_TEXT.lower()

    # 2. Verify EHR-01 supports both required types
    runtime = {v.value for v in EvaluationHarnessRunEvaluation_type}
    assert "TYPE_A_RESEARCH_QUALITY" in runtime
    assert "TYPE_B_DISCOVERY_RECALL" in runtime

    # 3. EHR-01 structural fields required for evaluation execution
    assert "EHR-01" in SCHEMA_REGISTRY, "EHR-01 missing from SCHEMA_REGISTRY"
    ehr_cls = SCHEMA_REGISTRY["EHR-01"]
    required_fields = {
        "eval_run_id", "evaluation_type", "pit_snapshot", "status",
        "metrics", "fixture_results",
    }
    for f in required_fields:
        assert f in ehr_cls.model_fields, (
            f"EHR-01 missing required M4B evaluation field: {f}"
        )
    # 4. Primary-ID registry: EHR-01 → eval_run_id
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("EHR-01") == "eval_run_id"


# ===================================================================
# 3: M4B FIXTURE IDENTITIES ↔ CANONICAL PRIMARY-ID AUTHORITY
# ===================================================================

def test_m4b_fixture_identities_map_to_canonical_primary_ids():
    """M4B fixture schema references entity_id, source_ids, evidence_ids
    (see §3.2 Fixture Schema).

    Frozen primary-ID authority resolves:
      SM-01 → entity_id
      SRC-01 → source_id
      EV-01 → evidence_id

    The M4A oracle confirms all three fields exist in the frozen schema.
    The independent Item-1 oracle proves the generated registry matches
    frozen M4A for all 68 schemas (referenced, not duplicated here).
    """
    # 1. Verify M4B contract references these fixture identity concepts
    assert "entity_id" in M4B_CONTRACT_TEXT
    assert "source_ids" in M4B_CONTRACT_TEXT
    assert "evidence_ids" in M4B_CONTRACT_TEXT

    # 2. Generated primary-ID authority
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

    # 3. M4A oracle field-surface confirmation (not independent PK derivation)
    assert "entity_id" in ORACLE["SM-01"].get("required", set()) | \
        ORACLE["SM-01"].get("optional", set())
    assert "source_id" in ORACLE["SRC-01"].get("required", set()) | \
        ORACLE["SRC-01"].get("optional", set())
    assert "evidence_id" in ORACLE["EV-01"].get("required", set()) | \
        ORACLE["EV-01"].get("optional", set())


# ===================================================================
# 4: M4B SOURCE SEAL CONCEPTS ↔ SRC-01  (STRUCTURAL)
# ===================================================================

def test_m4b_source_seal_concepts_have_src01_carrier():
    """M4B Seal Contract (§3.4) requires:
      - immutable source IDs
      - source content hashes (SHA-256)
      - source publication dates (≤ AS_OF_DATE)
      - allowed pre-AS_OF corpus manifest

    For the M5.2 structural bridge, SRC-01 provides:
      - source_id (PK, required)
      - content_hash (required; behavioral SHA-256 proof is Item 5)
      - publication_date (optional, frozen)

    Note: publication_date is OPTIONAL in the generic canonical SRC-01 schema.
    This is not a contradiction: M4B fixture sealing imposes the stronger
    contextual requirement that every source admitted to a SEALED evaluation
    fixture must have a verified publication_date ≤ AS_OF_DATE.
    That contextual seal enforcement is NOT an Item-13 persistence change.
    """
    # 1. Verify M4B contract requires these seal concepts
    assert "source content hashes" in M4B_CONTRACT_TEXT
    assert "source publication dates" in M4B_CONTRACT_TEXT
    assert "immutable source IDs" in M4B_CONTRACT_TEXT

    # 2. SRC-01 structural carrier
    assert "SRC-01" in SCHEMA_REGISTRY, "SRC-01 missing from SCHEMA_REGISTRY"
    src_cls = SCHEMA_REGISTRY["SRC-01"]

    # source_id — exists, required, authoritative PK
    assert "source_id" in src_cls.model_fields
    assert src_cls.model_fields["source_id"].is_required()
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("SRC-01") == "source_id"

    # content_hash — exists, required; behavioral SHA-256 proof is Item 5
    assert "content_hash" in src_cls.model_fields
    assert src_cls.model_fields["content_hash"].is_required()

    # publication_date — exists, frozen (optional in generic schema)
    assert "publication_date" in src_cls.model_fields
    assert src_cls.model_fields["publication_date"].frozen

    # SRC-01 is canonical
    assert "SRC-01" in CANONICAL_SCHEMAS


# ===================================================================
# 5: M4B EVIDENCE REFERENCES ↔ EV-01 / ITEM-6 BRIDGE
# ===================================================================

def test_m4b_evidence_references_have_ev01_carrier():
    """M4B fixture schema references evidence_ids (see §3.2 Fixture Schema).

    EV-01 provides:
      - evidence_id (PK, frozen)
      - source_id (FK → SRC-01.source_id)

    Behavioral admission-gate proof is Item 6 (referenced, not duplicated here).
    """
    # 1. Verify M4B contract references evidence_ids
    assert "evidence_ids" in M4B_CONTRACT_TEXT

    # 2. EV-01 structural carrier
    assert "EV-01" in SCHEMA_REGISTRY, "EV-01 missing from SCHEMA_REGISTRY"
    ev_cls = SCHEMA_REGISTRY["EV-01"]

    # evidence_id — exists, frozen, PK
    assert "evidence_id" in ev_cls.model_fields
    assert ev_cls.model_fields["evidence_id"].frozen
    from qad.persistence.reference import _schema_identity_field
    assert _schema_identity_field("EV-01") == "evidence_id"

    # source_id — exists, FK to SRC-01
    assert "source_id" in ev_cls.model_fields

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
# 6: M4B AS_OF_DATE ↔ PITC-01.as_of_date  (STRUCTURAL)
# ===================================================================

def test_m4b_as_of_date_maps_to_pitc01_as_of_date():
    """M4B requires AS_OF_DATE hard cutoff (see §2.1 Sealed Corpus).

    PITC-01 provides as_of_date (frozen, required, str) as the structural
    carrier.  This is a STRUCTURAL BRIDGE only — runtime cutoff enforcement
    is DEFERRED_M5.3.
    """
    # 1. Verify M4B contract requires AS_OF_DATE
    assert "AS_OF_DATE" in M4B_CONTRACT_TEXT

    # 2. PITC-01 structural carrier
    assert "PITC-01" in SCHEMA_REGISTRY
    pitc_cls = SCHEMA_REGISTRY["PITC-01"]
    assert "as_of_date" in pitc_cls.model_fields
    assert pitc_cls.model_fields["as_of_date"].frozen
    assert pitc_cls.model_fields["as_of_date"].is_required()
    # Type check
    ann = pitc_cls.model_fields["as_of_date"].annotation
    if hasattr(ann, "__origin__") and ann.__origin__ is typing.Union:
        for a in ann.__args__:
            if a is not type(None):
                ann = a
    assert ann is str, f"PITC-01.as_of_date should be str, got {ann}"


# ===================================================================
# 7: M4B EVALUATION LABELS ↔ FROZEN M4A ENUM COUNTERPARTS
# ===================================================================

def test_m4b_evaluation_labels_have_exact_m4a_enum_counterparts():
    """M4B expected_quality_state / expected_impairment / expected_verdict
    labels (see §3.2 Fixture Schema) have EXACT frozen M4A runtime enum
    counterparts.

    This proves structural bridge compatibility without M5.3 involvement.
    """
    # 1. Verify M4B contract defines these labels
    assert "expected_quality_state" in M4B_CONTRACT_TEXT
    assert "expected_impairment" in M4B_CONTRACT_TEXT
    assert "expected_verdict" in M4B_CONTRACT_TEXT

    # 2. expected_quality_state → QA-01 QualityAssessmentQuality_state
    #    M4B values: VERIFIED / PROBABLE / UNRESOLVED / FAILED
    m4a_qs = {v.value for v in QualityAssessmentQuality_state}
    m4b_quality = {"VERIFIED", "PROBABLE", "UNRESOLVED", "FAILED"}
    assert m4b_quality == m4a_qs, (
        f"Quality state mismatch: M4B={m4b_quality}, M4A={m4a_qs}"
    )

    # 3. expected_impairment → IA-01 ImpairmentAssessmentDiagnosis
    #    M4B values: TEMPORARY / MOSTLY_TEMPORARY / MIXED / STRUCTURAL / UNRESOLVED
    m4a_imp = {v.value for v in ImpairmentAssessmentDiagnosis}
    m4b_impairment = {
        "TEMPORARY", "MOSTLY_TEMPORARY", "MIXED", "STRUCTURAL",
        "UNRESOLVED",
    }
    assert m4b_impairment == m4a_imp, (
        f"Impairment diagnosis mismatch: M4B={m4b_impairment}, "
        f"M4A={m4a_imp}"
    )

    # 4. expected_verdict → UV-01 UnderwritingVerdictVerdict
    #    M4B values: QAD_CONFIRMED / QAD_PROBABLE / QAD_UNRESOLVED /
    #                NOT_QAD_STRUCTURAL / NOT_QAD_QUALITY / NOT_QAD_VALUATION
    m4a_verdict = {v.value for v in UnderwritingVerdictVerdict}
    m4b_verdict = {
        "QAD_CONFIRMED", "QAD_PROBABLE", "QAD_UNRESOLVED",
        "NOT_QAD_STRUCTURAL", "NOT_QAD_QUALITY", "NOT_QAD_VALUATION",
    }
    assert m4b_verdict == m4a_verdict, (
        f"Verdict mismatch: M4B={m4b_verdict}, M4A={m4a_verdict}"
    )

    # These are evaluation-only semantics.  No M5.2 persistence binding
    # required beyond the structural bridge proven here.
    # <!-- 2026-08-29 20:00 UTC+7 -->