"""M5.1 — QAD Schema Registry.
Runtime registry of all 68 frozen M4A canonical schemas with FK resolution,
schema versioning, and canonical/noncanonical distinction.
"""
from __future__ import annotations

from typing import Any

from qad.models import *


# ── Schema Registry ───────────────────────────────────────────────────────────

SCHEMA_REGISTRY: dict[str, type] = {
    "SM-01": SecurityMaster,
    "RU-01": ResearchableUniverseRecord,
    "SR-01": SignalRecord,
    "CR-01": CandidateRecord,
    "QU-01": QualityUniverseRecord,
    "CASE-01": CaseRecord,
    "SRC-01": SourceRecord,
    "EV-01": EvidenceRecord,
    "FACT-01": FactRecord,
    "CLM-01": ClaimRecord,
    "INF-01": InferenceRecord,
    "HYP-01": HypothesisRecord,
    "CTR-01": ContradictionRecord,
    "EAR-01": EvidenceAdmissionRecord,
    "SRCV-01": SourceVersion,
    "IC-01": InvestigatorCharter,
    "RSR-01": ResearchStageRecord,
    "RSR-02": ResearchStopRecord,
    "EG-01": EvidenceGap,
    "RB-01": ResearchBudgetRecord,
    "RFR-01": ResearchFailureRecord,
    "HS-01": HypothesisSet,
    "IR-01": InvestigationReport,
    "RC-01": ResearchCharter,
    "QA-01": QualityAssessment,
    "MA-01": MoatAssessment,
    "IE-01": IndustryEconomicsRecord,
    "MC-01": ManagementClaim,
    "CAE-01": CapitalAllocationEvent,
    "MDL-01": ManagementDecisionLedger,
    "MO-02": ManagementOutcome,
    "DR-01": DislocationRecord,
    "IA-01": ImpairmentAssessment,
    "CE-01": CompetingExplanation,
    "RM-01": RecoveryModel,
    "TK-01": ThesisKiller,
    "FE-01": FlipEvidence,
    "FF-01": FinancialFact,
    "NFF-01": NormalizedFinancialFact,
    "CALC-01": CalculationRecord,
    "SCEN-01": ScenarioRecord,
    "PLA-01": PermanentLossAssessment,
    "RDCF-01": ReverseDCFRecord,
    "VA-01": ValuationAssessment,
    "PIE-01": PriceImpliedExpectation,
    "RTC-01": RedTeamChallenge,
    "AG-01": AuditGate,
    "AF-01": AuditFinding,
    "UV-01": UnderwritingVerdict,
    "PUB-01": PublicationRecord,
    "FDR-01": FounderDecisionReference,
    "CRESP-01": ChallengeResponse,
    "MI-01": MonitoringIndicator,
    "MO-01": MonitoringObservation,
    "MASS-01": MonitoringAssessment,
    "CL-01": CandidateLesson,
    "IKR-01": InstitutionalKnowledgeRecord,
    "IPR-01": IndustryPlaybookRecord,
    "CCV-01": CrossCaseValidation,
    "RRM-01": RunManifestRecord,
    "PITC-01": PITContext,
    "SI-01": ServiceInvocation,
    "RR-01": RetryRecord,
    "CLK-01": CaseLock,
    "BU-01": BudgetUsage,
    "MOD-01": ModelInvocation,
    "PROV-01": ProviderInvocation,
    "EHR-01": EvaluationHarnessRun,
}

# ── Foreign Key Registry ──────────────────────────────────────────────────────

FK_REGISTRY: dict[str, list[dict]] = {
    # A — Identity & Coverage
    "RU-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"}],
    "SR-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"}],
    "CR-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"},
              {"field": "origin_signal_id", "target": "SR-01", "target_field": "signal_id"}],
    "QU-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"}],
    "CASE-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"},
                {"field": "candidate_id", "target": "CR-01", "target_field": "candidate_id"}],
    # B — Evidence & Sources
    "SRC-01": [{"field": "entity_id", "target": "SM-01", "target_field": "entity_id"}],
    "SRCV-01": [{"field": "source_id", "target": "SRC-01", "target_field": "source_id"}],
    "EV-01": [{"field": "source_id", "target": "SRC-01", "target_field": "source_id"},
              {"field": "entity_id", "target": "SM-01", "target_field": "entity_id"}],
    "FACT-01": [{"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id"}],
    "CLM-01": [{"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id"}],
    "INF-01": [{"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id"}],
    "HYP-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "CTR-01": [{"field": "evidence_ids", "target": "EV-01", "target_field": "evidence_id"}],
    "EAR-01": [{"field": "evidence_id", "target": "EV-01", "target_field": "evidence_id"}],
    # C — Research Case & Execution
    "IC-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "RSR-01": [{"field": "charter_id", "target": "IC-01", "target_field": "charter_id"}],
    "EG-01": [{"field": "charter_id", "target": "IC-01", "target_field": "charter_id"}],
    "RB-01": [{"field": "charter_id", "target": "IC-01", "target_field": "charter_id"}],
    "RFR-01": [{"field": "stage_id", "target": "RSR-01", "target_field": "stage_id"}],
    "HS-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "IR-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"},
              {"field": "charter_id", "target": "IC-01", "target_field": "charter_id"}],
    "RC-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    # D — Business & Industry Quality
    "QA-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "MA-01": [{"field": "quality_id", "target": "QA-01", "target_field": "quality_id"}],
    "IE-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "MC-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "CAE-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "MDL-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "MO-02": [{"field": "decision_id", "target": "MDL-01", "target_field": "decision_id"}],
    # E — Dislocation & Impairment
    "DR-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "IA-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "CE-01": [{"field": "impairment_id", "target": "IA-01", "target_field": "impairment_id"}],
    "RM-01": [{"field": "impairment_id", "target": "IA-01", "target_field": "impairment_id"}],
    "TK-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "FE-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    # F — Financial & Valuation
    "FF-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "NFF-01": [{"field": "financial_fact_id", "target": "FF-01", "target_field": "financial_fact_id"}],
    "CALC-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "SCEN-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "PLA-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "RDCF-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "VA-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "PIE-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    # G — Challenge, Audit & Governance
    "RTC-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "AG-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "AF-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "UV-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"},
              {"field": "audit_id", "target": "AF-01", "target_field": "audit_id"}],
    "PUB-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "FDR-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "CRESP-01": [{"field": "challenge_id", "target": "RTC-01", "target_field": "challenge_id"}],
    # H — Monitoring & Knowledge
    "MI-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "MO-01": [{"field": "indicator_id", "target": "MI-01", "target_field": "indicator_id"}],
    "MASS-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "CL-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "IKR-01": [{"field": "case_id", "target": "CASE-01", "target_field": "case_id"}],
    "IPR-01": [{"field": "industry_id", "target": "IE-01", "target_field": "industry_id"}],
    "CCV-01": [{"field": "case_ids", "target": "CASE-01", "target_field": "case_id"}],
    # I — System & Infrastructure
    "SI-01": [{"field": "manifest_id", "target": "RRM-01", "target_field": "manifest_id"}],
    "RR-01": [{"field": "invocation_id", "target": "SI-01", "target_field": "invocation_id"}],
    "BU-01": [{"field": "manifest_id", "target": "RRM-01", "target_field": "manifest_id"}],
    "MOD-01": [{"field": "manifest_id", "target": "RRM-01", "target_field": "manifest_id"}],
    "PROV-01": [{"field": "model_id", "target": "MOD-01", "target_field": "model_id"}],
    "EHR-01": [{"field": "manifest_id", "target": "RRM-01", "target_field": "manifest_id"}],
}

# ── Canonical vs Non-Canonical Boundary ─────────────────────────────────────

# Schemas that are CANONICAL (source of truth for QAD operations)
CANONICAL_SCHEMAS = {
    "SM-01", "RU-01", "SR-01", "CR-01", "QU-01", "CASE-01",
    "SRC-01", "SRCV-01", "EV-01", "FACT-01", "CLM-01", "INF-01",
    "HYP-01", "CTR-01", "EG-01", "EAR-01",
    "IC-01", "RSR-01", "RSR-02", "EG-01", "RB-01", "RFR-01", "HS-01", "IR-01", "RC-01",
    "QA-01", "MA-01", "IE-01", "MC-01", "CAE-01", "MDL-01", "MO-02",
    "DR-01", "IA-01", "CE-01", "RM-01", "TK-01", "FE-01",
    "FF-01", "NFF-01", "CALC-01", "SCEN-01", "PLA-01", "RDCF-01", "VA-01", "PIE-01",
    "RTC-01", "AG-01", "AF-01", "UV-01", "PUB-01", "FDR-01", "CRESP-01",
    "MI-01", "MO-01", "MASS-01", "CL-01", "IKR-01", "IPR-01", "CCV-01",
}

# Schemas that are INFRASTRUCTURE (non-canonical — operational metadata)
INFRASTRUCTURE_SCHEMAS = {
    "RRM-01", "PITC-01", "SI-01", "RR-01", "CLK-01", "BU-01", "MOD-01", "PROV-01", "EHR-01",
}


def resolve_fk(schema_id: str, field_name: str) -> str | None:
    """Resolve a field name to its FK target schema. Returns target schema_id or None."""
    fks = FK_REGISTRY.get(schema_id, [])
    for fk in fks:
        if fk["field"] == field_name:
            return fk["target"]
    return None


def validate_fk_integrity(instance: object, schema_id: str, store: dict[str, dict]) -> list[str]:
    """Validate FK references for a single instance against a store.
    Returns list of violation messages (empty = clean).
    """
    violations = []
    fks = FK_REGISTRY.get(schema_id, [])
    for fk in fks:
        fk_field = fk["field"]
        target_id = fk["target"]
        target_field = fk["target_field"]
        fk_value = getattr(instance, fk_field, None)
        if fk_value is None:
            continue
        # Check if target exists in store
        if isinstance(fk_value, list):
            for val in fk_value:
                target_key = f"{target_id}.{val}"
                if target_key not in store:
                    violations.append(f"FK violation: {schema_id}.{fk_field} → {target_id}.{target_field}: "
                                      f"value '{val}' not found in store")
        else:
            target_key = f"{target_id}.{fk_value}"
            if target_key not in store:
                violations.append(f"FK violation: {schema_id}.{fk_field} → {target_id}.{target_field}: "
                                  f"value '{fk_value}' not found in store")
    return violations


def is_canonical(schema_id: str) -> bool:
    """Return True if the schema is canonical (source of truth)."""
    return schema_id in CANONICAL_SCHEMAS


def is_infrastructure(schema_id: str) -> bool:
    """Return True if the schema is infrastructure (non-canonical operational metadata)."""
    return schema_id in INFRASTRUCTURE_SCHEMAS