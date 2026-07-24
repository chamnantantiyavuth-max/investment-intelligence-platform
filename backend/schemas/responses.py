"""Pydantic response schemas for API endpoints."""
from __future__ import annotations
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
