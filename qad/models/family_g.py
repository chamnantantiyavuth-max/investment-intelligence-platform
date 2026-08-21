"""Family G — Challenge, Audit & Governance
Runtime Pydantic models generated from QAD-M4A-CANONICAL-SCHEMAS.md.
Do not edit manually — regenerate via qad/generate_models.py
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from qad.provenance import ProvenanceMixin, PITMixin


class AuditFinding(ProvenanceMixin, PITMixin, BaseModel):
    """AF-01: AuditFinding. Frozen M4A canonical schema."""
    schema_id: str = Field(default="AF-01", frozen=True)
    audit_id: str
    check_name: str
    evidence: dict
    finding_id: str
    pass_fail: str
    required_correction: str
    resolution_timestamp: Optional[str] = Field(default=None)
    resolved: Optional[str] = Field(default=None)
    resolver: Optional[str] = Field(default=None)
    severity: Optional[str] = Field(default=None)

    # FK: audit_id -> AG-01.audit_id

class AuditGate(ProvenanceMixin, PITMixin, BaseModel):
    """AG-01: AuditGate (AuditReport). Frozen M4A canonical schema."""
    schema_id: str = Field(default="AG-01", frozen=True)
    audit_id: str
    auditor: str
    blocker: Optional[str] = Field(default=None)
    case_id: str
    completed_at: Optional[str] = Field(frozen=True)
    findings: str
    notes: Optional[str] = Field(default=None)
    outcome: str

    # FK: case_id -> CASE-01.case_id
    # FK: findings -> AF-01.finding_id

class ChallengeResponse(ProvenanceMixin, PITMixin, BaseModel):
    """CRESP-01: ChallengeResponse. Frozen M4A canonical schema."""
    schema_id: str = Field(default="CRESP-01", frozen=True)
    adopted_findings: str
    case_id: str
    challenge_id: str
    notes: Optional[str] = Field(default=None)
    rejected_findings: str
    rejection_evidence: Optional[str] = Field(default=None)
    response_id: str
    responses: str
    underwriter: str

    # FK: challenge_id -> RTC-01.challenge_id
    # FK: case_id -> CASE-01.case_id

class FounderDecisionReference(ProvenanceMixin, PITMixin, BaseModel):
    """FDR-01: FounderDecisionReference. Frozen M4A canonical schema."""
    schema_id: str = Field(default="FDR-01", frozen=True)
    case_id: str
    decision_date: str = Field(frozen=True)
    decision_type: str
    fd_number: str
    founder_decision_id: str
    notes: Optional[str] = Field(default=None)
    publication_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: publication_id -> PUB-01.publication_id

class PublicationRecord(ProvenanceMixin, PITMixin, BaseModel):
    """PUB-01: PublicationRecord. Frozen M4A canonical schema."""
    schema_id: str = Field(default="PUB-01", frozen=True)
    body_english: Optional[str] = Field(default=None)
    body_thai: Optional[str] = Field(default=None)
    case_id: str
    category: str
    companion_slug: Optional[str] = Field(default=None)
    editor: str
    publication_id: str
    publication_state: str
    published_date: str = Field(frozen=True)
    research_complete_date: Optional[str] = Field(default=None)
    slug: str
    title: str
    verdict_id: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id
    # FK: verdict_id -> UV-01.verdict_id

class RedTeamChallenge(ProvenanceMixin, PITMixin, BaseModel):
    """RTC-01: RedTeamChallenge. Frozen M4A canonical schema."""
    schema_id: str = Field(default="RTC-01", frozen=True)
    case_id: str
    challenge_id: str
    cost_of_being_wrong: str
    findings: str
    hidden_risks: Optional[str] = Field(default=None)
    management_challenge: Optional[str] = Field(default=None)
    market_correctness_case: Optional[str] = Field(default=None)
    outcome: str
    quality_challenge: Optional[str] = Field(default=None)
    recovery_challenge: Optional[str] = Field(default=None)
    risk_assessment: str
    strongest_opposing_case: str
    temporary_challenge: Optional[str] = Field(default=None)
    valuation_challenge: Optional[str] = Field(default=None)

    # FK: case_id -> CASE-01.case_id

class UnderwritingVerdict(ProvenanceMixin, PITMixin, BaseModel):
    """UV-01: UnderwritingVerdict. Frozen M4A canonical schema."""
    schema_id: str = Field(default="UV-01", frozen=True)
    additional_evidence_ids: Optional[str] = Field(default=None)
    audit_report_id: Optional[str] = Field(default=None)
    case_id: str
    dissent_notes: Optional[str] = Field(default=None)
    key_uncertainties: str
    monitoring_indicators: str
    recommendation_to_founder: str
    red_team_challenge_id: Optional[str] = Field(default=None)
    scenario_weights: str
    synthesis_narrative: str
    underwriter: str
    verdict: str
    verdict_id: str

    # FK: case_id -> CASE-01.case_id
    # FK: red_team_challenge_id -> RTC-01.challenge_id
    # FK: audit_report_id -> AG-01.audit_id