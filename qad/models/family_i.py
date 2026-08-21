"""Family I — System & Infrastructure
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class BudgetUsage(ProvenanceMixin, PITMixin, BaseModel):
    """BU-01: BudgetUsage. Frozen M4A canonical schema."""
    schema_id: str = Field(default="BU-01", frozen=True)
    amount_consumed: str
    budget_id: str
    case_id: str
    cost: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    provider: Optional[str] = Field(default=None)
    resource_type: str
    tokens: Optional[str] = Field(default=None)
    usage_id: str
    usage_timestamp: str = Field(frozen=True)

    # FK: budget_id -> RB-01.budget_id

class CaseLock(ProvenanceMixin, PITMixin, BaseModel):
    """CLK-01: CaseLock. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CLK-01", frozen=True)
    case_id: str
    case_version: str
    lock_id: str
    lock_reason: Optional[str] = Field(default=None)
    lock_state: str
    locked_at: str = Field(frozen=True)
    locked_by: str
    unlocked_at: Optional[str] = Field(default=None, frozen=True)

    # FK: case_id -> CASE-01.case_id

class EvaluationHarnessRun(ProvenanceMixin, PITMixin, BaseModel):
    """EHR-01: EvaluationHarnessRun. Frozen M4A canonical schema."""
    schema_id: str = Field(default="EHR-01", frozen=True)
    completed_at: Optional[str] = Field(default=None, frozen=True)
    corpus_version: str
    cost: Optional[str] = Field(default=None)
    eval_run_id: str
    evaluation_type: str
    failures: Optional[str] = Field(default=None)
    fixture_results: Optional[str] = Field(default=None)
    metrics: Optional[str] = Field(default=None)
    pit_snapshot: str = Field(frozen=True)
    policy_version: str
    started_at: str = Field(frozen=True)
    status: str
    token_usage: Optional[str] = Field(default=None)

class ModelInvocation(ProvenanceMixin, PITMixin, BaseModel):
    """MOD-01: ModelInvocation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="MOD-01", frozen=True)
    case_id: str
    completion_tokens: str
    cost: str
    error: Optional[str] = Field(default=None)
    invoked_at: str = Field(frozen=True)
    latency_ms: Optional[str] = Field(default=None)
    model: str
    model_invocation_id: str
    prompt_hash: Optional[str] = Field(default=None)
    prompt_tokens: str
    provider: str
    response_hash: Optional[str] = Field(default=None)
    retry_count: Optional[int] = Field(default=None)
    status: str

    # FK: case_id -> CASE-01.case_id

class PITContext(ProvenanceMixin, PITMixin, BaseModel):
    """PITC-01: PITContext. Frozen M4A canonical schema."""
    schema_id: str = Field(default="PITC-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    case_id: str
    created_by: str
    evidence_count_post: Optional[str] = Field(default=None)
    evidence_count_pre: Optional[str] = Field(default=None)
    exception_reason: Optional[str] = Field(default=None)
    mode: str
    pit_context_id: str

    # FK: case_id -> CASE-01.case_id

class ProviderInvocation(ProvenanceMixin, PITMixin, BaseModel):
    """PROV-01: ProviderInvocation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="PROV-01", frozen=True)
    case_id: str
    cost: str
    error: Optional[str] = Field(default=None)
    fallback_used: Optional[str] = Field(default=None)
    invoked_at: str = Field(frozen=True)
    model_invocation_ids: Optional[str] = Field(default=None)
    provider: str
    provider_invocation_id: str
    service: str
    status: str

    # FK: case_id -> CASE-01.case_id
    # FK: model_invocation_ids -> MOD-01.model_invocation_id

class RetryRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RR-01: RetryRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RR-01", frozen=True)
    attempt_number: str
    attempted_at: str = Field(frozen=True)
    error: str
    escalated_to: Optional[str] = Field(default=None)
    invocation_id: str
    resolution: Optional[str] = Field(default=None)
    retry_id: str
    status: str

    # FK: invocation_id -> SI-01.invocation_id

class RunManifestRecord(ProvenanceMixin, PITMixin, BaseModel):
    """RRM-01: ResearchRunManifest. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RRM-01", frozen=True)
    as_of_date: str = Field(frozen=True)
    calculation_version: Optional[str] = Field(default=None)
    case_id: str
    case_version: str
    completion_time: str = Field(frozen=True)
    cost: Optional[str] = Field(default=None)
    deep_research_runs: Optional[str] = Field(default=None)
    failures: Optional[str] = Field(default=None)
    manifest_id: str
    model_versions: Optional[str] = Field(default=None)
    models_used: str
    notebook_runs: Optional[str] = Field(default=None)
    output_version: Optional[str] = Field(default=None)
    prompts_contracts: Optional[str] = Field(default=None)
    providers: str
    retries: Optional[str] = Field(default=None)
    selection_policy_version: str
    sources_added: Optional[str] = Field(default=None)
    start_time: str = Field(frozen=True)
    token_usage: Optional[str] = Field(default=None)
    universe_version: str

    # FK: case_id -> CASE-01.case_id

class ServiceInvocation(ProvenanceMixin, PITMixin, BaseModel):
    """SI-01: ServiceInvocation. Frozen M4A canonical schema."""
    schema_id: str = Field(default="SI-01", frozen=True)
    case_id: str
    duration_ms: Optional[int] = Field(default=None)
    error: Optional[str] = Field(default=None)
    input_summary: Optional[str] = Field(default=None)
    invocation_id: str
    invoked_at: str = Field(frozen=True)
    output_summary: Optional[str] = Field(default=None)
    request_type: str
    retry_count: Optional[int] = Field(default=None)
    service_id: str
    status: str

    # FK: case_id -> CASE-01.case_id