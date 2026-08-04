"""Pydantic response schemas for API endpoints — locked to REAL artifact fields (arch v0.4 §3, plan T4).

Real-Data Production Path (FD #46): synthetic-only fields (driver_count, evidence counts,
numeric quality scores) REMOVED from real surfaces. Provenance required on every real surface.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


# ── Provenance (required on every real surface; never invented) ──────────────
class Provenance(BaseModel):
    source: str
    mode: str                  # real | synthetic
    as_of: Optional[str] = None
    coverage: Optional[str] = None
    completeness: Optional[str] = None
    hybrid: bool = False       # true when real + non-real components coexist
    component_map: dict[str, str] = {}  # per-component label (arch §3): field -> real|synthetic|human_sourced


class EvidenceProvenance(BaseModel):
    source_id: str
    source_type: str           # real | synthetic | human_sourced


class EvidenceRecord(BaseModel):
    """Full evidence register entry (falsification extension — mini-FD, 4 Aug 2026)."""
    id: str
    type: str
    content: str
    source: Optional[str] = None


# ── Dashboard ────────────────────────────────────────────────────────────────
class ComponentProvenance(BaseModel):
    run_id: Optional[str] = None
    point_in_time: Optional[str] = None
    data_source: Optional[str] = None
    source: Optional[str] = None        # e.g. backend_static_mock for CS
    state: str = "available"            # available | unavailable


class DashboardSummary(BaseModel):
    total_themes: int = 0
    approved_themes: int = 0
    active_signals: int = 0
    queue_size: int = 0
    am_last_run: Optional[str] = None
    cs_radar_items: int = 0
    cs_qc_met: int = 0
    cs_regime: str = "unknown"
    components: dict[str, ComponentProvenance]  # am / fo / ii / cs — per-component provenance


# ── AM (locked to real artifact fields) ───────────────────────────────────────
class ThemeSummary(BaseModel):
    id: str
    name: str
    sector: str
    industry: str
    lifecycle: str
    approval_status: str
    monitoring_status: str
    confidence: str
    key_tickers: list[str]
    stocks_in_industry: int
    why_now: str
    provenance: Provenance
    evidence_provenance: list[EvidenceProvenance]
    # Falsification read-only extension (mini-FD 4 Aug 2026, Constitution §11) —
    # optional passthrough of artifact fields; never a rule change.
    alternative_explanations: Optional[dict[str, str]] = None
    evidence: Optional[list[EvidenceRecord]] = None
    unresolved_counter_evidence: Optional[list[str]] = None


class CandidateQuality(BaseModel):
    fundamentals: str
    growth: str
    liquidity: str
    relative_strength: str
    trend_quality: str
    accumulation: str
    industry_leadership: str


class EntryReadiness(BaseModel):
    price_structure: str
    base_quality: str
    breakout_proximity: str
    volume_behavior: str
    volatility_contraction: str
    extension_risk: str


class DataConfidence(BaseModel):
    freshness: str
    completeness: str
    reliability: str
    conflicts: str
    missing_data: str


class CandidateSummary(BaseModel):
    id: str
    ticker: str
    research_state: str
    conviction_level: str
    candidate_quality: CandidateQuality
    entry_readiness: EntryReadiness
    data_confidence: DataConfidence
    provenance: Provenance


class ThemeWithCandidates(BaseModel):
    theme: ThemeSummary
    candidates: list[CandidateSummary]


class AMQueueResponse(BaseModel):
    run_id: str
    point_in_time: Optional[str] = None
    themes: list[ThemeWithCandidates]


# ── FO (envelope {run_id, provenance, packages}; locked flattening) ──────────
class ResearchPackageSummary(BaseModel):
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
    provenance: Provenance


class ResearchPackageDetail(ResearchPackageSummary):
    """Full research package: summary fields + full content sections."""
    conviction: Any
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


# ── II (new surface) ──────────────────────────────────────────────────────────
class IISignalSummary(BaseModel):
    filer_name: str
    filer_cik: str
    filer_category: str
    ticker: str
    filing_quarter: str
    report_date: str
    pct_of_portfolio: float
    conviction: str
    action: str
    change_pct: float
    value_usd: float


class IISignalsResponse(BaseModel):
    signals: list[IISignalSummary]
    summary: dict[str, Any] = {}
    meta: dict[str, Any] = {}
    provenance: Provenance
    total: int = 0  # total signals available (set when pagination used)


# ── CS (unchanged synthetic contract) ─────────────────────────────────────────
class CSRadarResponse(BaseModel):
    data_source: str = "synthetic_demo"
    assets: list[Any]
