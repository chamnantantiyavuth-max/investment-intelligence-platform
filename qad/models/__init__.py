"""QAD Runtime Schema Models — all 68 frozen M4A canonical schemas."""
from __future__ import annotations

from qad.models.family_a import (
    CaseRecord,
    CandidateRecord,
    QualityUniverseRecord,
    ResearchableUniverseRecord,
    SecurityMaster,
    SignalRecord,
)

from qad.models.family_b import (
    ClaimRecord,
    ContradictionRecord,
    EvidenceAdmissionRecord,
    EvidenceGap,
    EvidenceRecord,
    FactRecord,
    HypothesisRecord,
    InferenceRecord,
    SourceRecord,
    SourceVersion,
)

from qad.models.family_c import (
    HypothesisSet,
    InvestigatorCharter,
    InvestigationReport,
    ResearchBudgetRecord,
    ResearchCharter,
    ResearchFailureRecord,
    ResearchStageRecord,
    ResearchStopRecord,
)

from qad.models.family_d import (
    CapitalAllocationEvent,
    IndustryEconomicsRecord,
    MoatAssessment,
    ManagementClaim,
    ManagementDecisionLedger,
    ManagementOutcome,
    QualityAssessment,
)

from qad.models.family_e import (
    CompetingExplanation,
    DislocationRecord,
    FlipEvidence,
    ImpairmentAssessment,
    RecoveryModel,
    ThesisKiller,
)

from qad.models.family_f import (
    CalculationRecord,
    FinancialFact,
    NormalizedFinancialFact,
    PriceImpliedExpectation,
    PermanentLossAssessment,
    ReverseDCFRecord,
    ScenarioRecord,
    ValuationAssessment,
)

from qad.models.family_g import (
    AuditFinding,
    AuditGate,
    ChallengeResponse,
    FounderDecisionReference,
    PublicationRecord,
    RedTeamChallenge,
    UnderwritingVerdict,
)

from qad.models.family_h import (
    CrossCaseValidation,
    CandidateLesson,
    InstitutionalKnowledgeRecord,
    IndustryPlaybookRecord,
    MonitoringAssessment,
    MonitoringIndicator,
    MonitoringObservation,
)

from qad.models.family_i import (
    BudgetUsage,
    CaseLock,
    EvaluationHarnessRun,
    ModelInvocation,
    PITContext,
    ProviderInvocation,
    RetryRecord,
    RunManifestRecord,
    ServiceInvocation,
)


__all__ = [
    "AuditFinding",
    "AuditGate",
    "BudgetUsage",
    "CalculationRecord",
    "CandidateLesson",
    "CandidateRecord",
    "CapitalAllocationEvent",
    "CaseLock",
    "CaseRecord",
    "ChallengeResponse",
    "ClaimRecord",
    "CompetingExplanation",
    "ContradictionRecord",
    "CrossCaseValidation",
    "DislocationRecord",
    "EvaluationHarnessRun",
    "EvidenceAdmissionRecord",
    "EvidenceGap",
    "EvidenceRecord",
    "FactRecord",
    "FinancialFact",
    "FlipEvidence",
    "FounderDecisionReference",
    "HypothesisRecord",
    "HypothesisSet",
    "ImpairmentAssessment",
    "IndustryEconomicsRecord",
    "IndustryPlaybookRecord",
    "InferenceRecord",
    "InstitutionalKnowledgeRecord",
    "InvestigationReport",
    "InvestigatorCharter",
    "ManagementClaim",
    "ManagementDecisionLedger",
    "ManagementOutcome",
    "MoatAssessment",
    "ModelInvocation",
    "MonitoringAssessment",
    "MonitoringIndicator",
    "MonitoringObservation",
    "NormalizedFinancialFact",
    "PITContext",
    "PermanentLossAssessment",
    "PriceImpliedExpectation",
    "ProviderInvocation",
    "PublicationRecord",
    "QualityAssessment",
    "QualityUniverseRecord",
    "RecoveryModel",
    "RedTeamChallenge",
    "ResearchBudgetRecord",
    "ResearchCharter",
    "ResearchFailureRecord",
    "ResearchStageRecord",
    "ResearchStopRecord",
    "ResearchableUniverseRecord",
    "RetryRecord",
    "ReverseDCFRecord",
    "RunManifestRecord",
    "ScenarioRecord",
    "SecurityMaster",
    "ServiceInvocation",
    "SignalRecord",
    "SourceRecord",
    "SourceVersion",
    "ThesisKiller",
    "UnderwritingVerdict",
    "ValuationAssessment",
]