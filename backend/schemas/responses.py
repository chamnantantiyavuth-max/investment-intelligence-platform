"""Pydantic response schemas for API endpoints."""
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class DashboardSummary(BaseModel):
    total_themes: int = 143
    approved_themes: int = 12
    active_signals: int = 7
    queue_size: int = 5
    am_active_themes: int = 12
    am_queue_size: int = 5
    am_last_run: Optional[str] = "2026-07-25T01:00:00Z"
    cs_radar_items: int = 8
    cs_qc_met: int = 3
    cs_regime: str = "risk-on"


class ThemeSummary(BaseModel):
    id: str
    name: str
    approval_status: str
    lifecycle: str
    driver_count: int
    candidate_count: int
    evidence_supporting: int
    evidence_contradicting: int
    evidence_missing: int
    theme_quality: float
    candidate_quality: float
    entry_readiness: float
    data_confidence: float


class AMQueueResponse(BaseModel):
    themes: list[ThemeSummary]


# ── Fundamental & Opportunity Intelligence (Phase 8) ──

class MoatType(str, Enum):
    """Moat width classification per §3.4.1."""
    WIDE = "Wide"
    NARROW = "Narrow"
    NONE = "None"


class ResearchPackageSummary(BaseModel):
    """Lightweight summary for queue listing (10 fields)."""
    id: str
    name: str
    sector: str
    industry: str
    moat_width: str
    moat_depth: str
    moat_trend: str
    earnings_quality: str
    conviction: str
    value_trap_verdict: str


class ResearchPackageDetail(BaseModel):
    """Full research package with all summary fields + 13 content sections.

    Standalone model (not inheriting from summary) to avoid field type
    conflicts — e.g., summary uses ``conviction: str`` (level only) while
    detail uses ``conviction: dict`` (full conviction object).
    """
    id: str
    name: str
    sector: str
    industry: str
    moat_width: str
    moat_depth: str
    moat_trend: str
    earnings_quality: str
    conviction: dict
    value_trap_verdict: str
    generated_at: str
    spec_ref: str
    thesis_summary: str
    thesis_lifecycle: str
    macro_context: dict
    industry_assessment: dict
    company_assessment: dict
    earnings_trajectory: dict
    valuation_context: dict
    key_risks: list
    independent_challenge: list
    supporting_evidence: list
    contradicting_evidence: list
    open_questions: list
