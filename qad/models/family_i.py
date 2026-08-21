"""Family I — Reproducibility & Operations
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class BudgetUsageResource_type(str, Enum):
    TOKEN = "TOKEN"
    API_CALL = "API_CALL"
    DEEP_RESEARCH = "DEEP_RESEARCH"
    NOTEBOOKLM = "NOTEBOOKLM"
    COMPUTATION = "COMPUTATION"
    STORAGE = "STORAGE"
    OTHER = "OTHER"

class CaseLockLock_state(str, Enum):
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    PENDING = "PENDING"

class EvaluationHarnessRunEvaluation_type(str, Enum):
    TYPE_A_RESEARCH_QUALITY = "TYPE_A_RESEARCH_QUALITY"
    TYPE_B_DISCOVERY_RECALL = "TYPE_B_DISCOVERY_RECALL"
    CALIBRATION = "CALIBRATION"
    COST_EVAL = "COST_EVAL"

class EvaluationHarnessRunStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    EVALUATION_INCOMPLETE = "EVALUATION_INCOMPLETE"
    FAILED = "FAILED"

class ModelInvocationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RATE_LIMITED = "RATE_LIMITED"
    TIMEOUT = "TIMEOUT"

class PITContextMode(str, Enum):
    LIVE_CASE_UPDATE = "LIVE_CASE_UPDATE"
    SEALED_HISTORICAL_EVALUATION = "SEALED_HISTORICAL_EVALUATION"
    REPLAY_EXCEPTION = "REPLAY_EXCEPTION"

class ProviderInvocationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    FALLBACK_USED = "FALLBACK_USED"

class RetryRecordStatus(str, Enum):
    RETRYING = "RETRYING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    ESCALATED = "ESCALATED"

class ServiceInvocationStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PARTIAL = "PARTIAL"
    TIMEOUT = "TIMEOUT"


class BudgetUsage(BaseModel):
    """BU-01: BudgetUsage. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="BU-01", frozen=True)
    amount_consumed: str = Field(frozen=True)
    budget_id: str = Field(frozen=True)
    case_id: str = Field(frozen=True)
    resource_type: BudgetUsageResource_type = Field(frozen=True)
    usage_id: str = Field(frozen=True)
    usage_timestamp: str = Field(frozen=True)
    cost: Optional[str] = Field(default=None, frozen=True)
    model: Optional[str] = Field(default=None, frozen=True)
    provider: Optional[str] = Field(default=None, frozen=True)
    tokens: Optional[str] = Field(default=None, frozen=True)

    # FK: budget_id -> RB-01.budget_id


class CaseLock(BaseModel):
    """CLK-01: CaseLock. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="CLK-01", frozen=True)
    case_id: str = Field(frozen=True)
    case_version: str = Field(frozen=True)
    lock_id: str = Field(frozen=True)
    lock_state: CaseLockLock_state = Field(frozen=True)
    locked_at: str = Field(frozen=True)
    locked_by: str = Field(frozen=True)
    lock_reason: Optional[str] = Field(default=None, frozen=True)
    unlocked_at: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class EvaluationHarnessRun(BaseModel):
    """EHR-01: EvaluationHarnessRun. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="EHR-01", frozen=True)
    corpus_version: str = Field(frozen=True)
    eval_run_id: str = Field(frozen=True)
    evaluation_type: EvaluationHarnessRunEvaluation_type = Field(frozen=True)
    pit_snapshot: str = Field(frozen=True)
    policy_version: str = Field(frozen=True)
    started_at: str = Field(frozen=True)
    status: EvaluationHarnessRunStatus = Field(frozen=True)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    cost: Optional[str] = Field(default=None, frozen=True)
    failures: Optional[list[str]] = Field(default=None, frozen=True)
    fixture_results: Optional[list[str]] = Field(default=None, frozen=True)
    metrics: Optional[dict] = Field(default=None, frozen=True)
    token_usage: Optional[str] = Field(default=None, frozen=True)


class ModelInvocation(BaseModel):
    """MOD-01: ModelInvocation. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="MOD-01", frozen=True)
    case_id: str = Field(frozen=True)
    completion_tokens: str = Field(frozen=True)
    cost: str = Field(frozen=True)
    invoked_at: str = Field(frozen=True)
    model: str = Field(frozen=True)
    model_invocation_id: str = Field(frozen=True)
    prompt_tokens: str = Field(frozen=True)
    provider: str = Field(frozen=True)
    status: ModelInvocationStatus = Field(frozen=True)
    error: Optional[str] = Field(default=None, frozen=True)
    latency_ms: Optional[str] = Field(default=None, frozen=True)
    prompt_hash: Optional[str] = Field(default=None, frozen=True)
    response_hash: Optional[str] = Field(default=None, frozen=True)
    retry_count: Optional[int] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id


class PITContext(BaseModel):
    """PITC-01: PITContext. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="PITC-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    case_id: str
    created_by: str
    mode: PITContextMode
    pit_context_id: str
    created_at: Optional[str] = Field(default=None, frozen=True)
    evidence_count_post: Optional[str] = Field(default=None)
    evidence_count_pre: Optional[str] = Field(default=None)
    exception_reason: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ProviderInvocation(BaseModel):
    """PROV-01: ProviderInvocation. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="PROV-01", frozen=True)
    case_id: str = Field(frozen=True)
    cost: str = Field(frozen=True)
    invoked_at: str = Field(frozen=True)
    provider: str = Field(frozen=True)
    provider_invocation_id: str = Field(frozen=True)
    service: str = Field(frozen=True)
    status: ProviderInvocationStatus = Field(frozen=True)
    error: Optional[str] = Field(default=None, frozen=True)
    fallback_used: Optional[str] = Field(default=None, frozen=True)
    model_invocation_ids: Optional[list[str]] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id
    # FK: model_invocation_ids[] -> MOD-01.model_invocation_id


class RetryRecord(BaseModel):
    """RR-01: RetryRecord. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RR-01", frozen=True)
    attempt_number: str = Field(frozen=True)
    attempted_at: str = Field(frozen=True)
    error: str = Field(frozen=True)
    invocation_id: str = Field(frozen=True)
    retry_id: str = Field(frozen=True)
    status: RetryRecordStatus = Field(frozen=True)
    escalated_to: Optional[str] = Field(default=None, frozen=True)
    resolution: Optional[str] = Field(default=None, frozen=True)

    # FK: invocation_id -> SI-01.invocation_id


class RunManifestRecord(BaseModel):
    """RRM-01: ResearchRunManifest. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="RRM-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    case_id: str
    case_version: str
    completion_time: str = Field(frozen=True)
    manifest_id: str
    models_used: list[str]
    providers: dict
    selection_policy_version: str
    start_time: str = Field(frozen=True)
    universe_version: str
    calculation_version: Optional[str] = Field(default=None)
    cost: Optional[dict] = Field(default=None)
    deep_research_runs: Optional[list[str]] = Field(default=None)
    failures: Optional[list[str]] = Field(default=None)
    model_versions: Optional[dict] = Field(default=None)
    notebook_runs: Optional[list[str]] = Field(default=None)
    output_version: Optional[str] = Field(default=None)
    prompts_contracts: Optional[list[str]] = Field(default=None)
    retries: Optional[str] = Field(default=None)
    sources_added: Optional[str] = Field(default=None)
    token_usage: Optional[dict] = Field(default=None)

    # FK: case_id -> CASE-01.case_id


class ServiceInvocation(BaseModel):
    """SI-01: ServiceInvocation. Frozen M4A canonical schema. Family I. """
    model_config = {"extra": "forbid"}

    schema_id: str = Field(default="SI-01", frozen=True)
    case_id: str = Field(frozen=True)
    invocation_id: str = Field(frozen=True)
    invoked_at: str = Field(frozen=True)
    request_type: str = Field(frozen=True)
    service_id: str = Field(frozen=True)
    status: ServiceInvocationStatus = Field(frozen=True)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    duration_ms: Optional[int] = Field(default=None, frozen=True)
    error: Optional[str] = Field(default=None, frozen=True)
    input_summary: Optional[str] = Field(default=None, frozen=True)
    output_summary: Optional[str] = Field(default=None, frozen=True)
    retry_count: Optional[int] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id