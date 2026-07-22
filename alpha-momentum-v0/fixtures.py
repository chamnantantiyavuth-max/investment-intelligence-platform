"""
Alpha Momentum V0 — Synthetic Fixtures
Minimum fixture set per FIXTURE-AND-ACCEPTANCE-SCENARIOS.md §4
All data is synthetic (Category A) unless noted as historical snapshot (Category B).
NOT LIVE DATA — FOR V0 TESTING ONLY.
"""
from datetime import datetime, date
from dataclasses import dataclass, field
from typing import Optional
import json

FIXTURE_CATEGORY = "SYNTHETIC — FOR V0 TESTING ONLY"

# ── Timestamps ─────────────────────────────────────────────
AS_OF = date(2024, 7, 1)
TS_EARLY  = datetime(2023, 6, 15, 10, 0, 0)
TS_MID    = datetime(2024, 1, 15, 10, 0, 0)
TS_LATE   = datetime(2024, 7, 1, 10, 0, 0)

# ═══════════════════════════════════════════════════════════
# EVIDENCE
# ═══════════════════════════════════════════════════════════
EVIDENCE = [
    # ── TH-004 Semiconductors ──
    {"id": "EV-001", "type": "Observed Fact", "content": "NVDA data center revenue: $14.5B in Q1 FY2025, +427% YoY", "source": "SRC-SYN-001", "pub_ts": "2024-05-22T08:00:00Z", "effective": "2024-Q1", "relationship": "supporting", "theme": "TH-004", "candidate": "NVDA"},
    {"id": "EV-002", "type": "Observed Fact", "content": "Global cloud infrastructure spending: $78B in Q1 2024, +21% YoY (Synergy Research)", "source": "SRC-SYN-002", "pub_ts": "2024-04-30T08:00:00Z", "effective": "2024-Q1", "relationship": "supporting", "theme": "TH-004", "candidate": None},
    {"id": "EV-003", "type": "Claim",       "content": "Semiconductor cycle historically boom-bust; memory oversupply risk rising", "source": "SRC-SYN-003", "pub_ts": "2024-06-01T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-004", "candidate": None},
    {"id": "EV-004", "type": "Observed Fact", "content": "AMD data center revenue: $2.3B in Q1 2024, +80% YoY", "source": "SRC-SYN-004", "pub_ts": "2024-04-30T08:00:00Z", "effective": "2024-Q1", "relationship": "supporting", "theme": "TH-004", "candidate": "AMD"},
    {"id": "EV-005", "type": "Claim",       "content": "AI inference efficiency improvements (DeepSeek, Grok) may reduce GPU demand per query by 50-90%", "source": "SRC-SYN-005", "pub_ts": "2024-06-15T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-004", "candidate": None},
    {"id": "EV-006", "type": "Missing",     "content": "Missing: inference-to-training compute ratio long-term projection", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-004", "candidate": None},

    # ── TH-014 Medical Devices ──
    {"id": "EV-007", "type": "Observed Fact", "content": "MDT Q4 FY2024 revenue: $8.6B, +5.2% YoY; procedure volumes normalizing post-COVID", "source": "SRC-SYN-006", "pub_ts": "2024-05-23T08:00:00Z", "effective": "2024-Q4", "relationship": "supporting", "theme": "TH-014", "candidate": "MDT"},
    {"id": "EV-008", "type": "Claim",       "content": "GLP-1 drugs may reduce demand for certain surgical interventions (bariatric, orthopedic)", "source": "SRC-SYN-007", "pub_ts": "2024-03-01T08:00:00Z", "effective": "2024-Q1", "relationship": "contradicting", "theme": "TH-014", "candidate": None},
    {"id": "EV-009", "type": "Missing",     "content": "Missing: GLP-1 long-term impact on surgical procedure volumes (data < 2 years)", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-014", "candidate": None},

    # ── TH-010 Solar ──
    {"id": "EV-010", "type": "Observed Fact", "content": "FSLR module shipments: 3.5 GW in Q1 2024, backlog 78 GW", "source": "SRC-SYN-008", "pub_ts": "2024-05-01T08:00:00Z", "effective": "2024-Q1", "relationship": "supporting", "theme": "TH-010", "candidate": "FSLR"},
    {"id": "EV-011", "type": "Claim",       "content": "Solar project ROI compressed at sustained 5%+ interest rates — industry reports", "source": "SRC-SYN-009", "pub_ts": "2024-06-01T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-010", "candidate": None},
    {"id": "EV-012", "type": "Missing",     "content": "Missing: solar project ROI at sustained 5%+ interest rates by region", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-010", "candidate": None},
    {"id": "EV-013", "type": "Missing",     "content": "Missing: utility-scale battery storage cost trajectory 2025-2030", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-010", "candidate": None},
]

# ═══════════════════════════════════════════════════════════
# ENTITIES (Issuers)
# ═══════════════════════════════════════════════════════════
ENTITIES = [
    {"id": "ENT-001", "name": "NVIDIA Corporation",       "sector": "Technology",             "industry": "Semiconductors",             "fixture_type": "Historical identifier, synthetic data"},
    {"id": "ENT-002", "name": "Intel Corporation",         "sector": "Technology",             "industry": "Semiconductors",             "fixture_type": "Historical identifier, synthetic data"},
    {"id": "ENT-003", "name": "Advanced Micro Devices",    "sector": "Technology",             "industry": "Semiconductors",             "fixture_type": "Historical identifier, synthetic data"},
    {"id": "ENT-004", "name": "Medtronic plc",             "sector": "Healthcare",             "industry": "Medical Devices",            "fixture_type": "Historical identifier, synthetic data"},
    {"id": "ENT-005", "name": "First Solar, Inc.",         "sector": "Technology",             "industry": "Solar",                      "fixture_type": "Historical identifier, synthetic data"},
]

# ═══════════════════════════════════════════════════════════
# ASSETS (Instruments)
# ═══════════════════════════════════════════════════════════
ASSETS = [
    {"id": "AST-001", "ticker": "NVDA", "entity_id": "ENT-001", "exchange": "NASDAQ",        "asset_type": "Common Stock"},
    {"id": "AST-002", "ticker": "INTC", "entity_id": "ENT-002", "exchange": "NASDAQ",        "asset_type": "Common Stock"},
    {"id": "AST-003", "ticker": "AMD",  "entity_id": "ENT-003", "exchange": "NASDAQ",        "asset_type": "Common Stock"},
    {"id": "AST-004", "ticker": "MDT",  "entity_id": "ENT-004", "exchange": "NYSE",          "asset_type": "Common Stock"},
    {"id": "AST-005", "ticker": "FSLR", "entity_id": "ENT-005", "exchange": "NASDAQ",        "asset_type": "Common Stock"},
]

# ═══════════════════════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════════════════════
THEMES = [
    {
        "id": "TH-004", "name": "Semiconductors", "sector": "Technology", "industry": "Semiconductors",
        "lifecycle": "Expansion", "approval_status": "Approved", "monitoring_status": "Active Monitoring",
        "why_now": "AI compute demand driving 200%+ data center revenue growth. Multi-year capex cycle. CHIPS Act providing domestic manufacturing incentives.",
        "confidence": "High",
        "lifecycle_transitions": [
            {"prior": "Emerging Leadership", "new": "Expansion", "reason": "AI capex cycle confirmed across all major hyperscalers; broad-based revenue acceleration", "actor": "Founder", "timestamp": "2024-01-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Under Human Review", "reason": "Initial theme proposal", "actor": "Founder", "timestamp": "2023-06-15T10:00:00Z", "version": "v0.1.0"},
            {"prior": "Under Human Review", "new": "Approved", "reason": "Structural driver confirmed; identifiable beneficiaries mapped", "actor": "Founder", "timestamp": "2023-09-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Theme approved — begin active tracking", "actor": "Founder", "timestamp": "2023-09-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 71,
        "key_tickers": ["NVDA", "AMD", "AVGO", "QCOM", "INTC", "TXN"],
    },
    {
        "id": "TH-014", "name": "Medical Devices", "sector": "Healthcare", "industry": "Medical Devices",
        "lifecycle": "Emerging Leadership", "approval_status": "Approved", "monitoring_status": "Active Monitoring",
        "why_now": "Procedure volume normalization post-COVID. Aging population (65+ growing 10,000/day). Robotics and minimally-invasive adoption accelerating.",
        "confidence": "Medium",
        "lifecycle_transitions": [
            {"prior": "Formation", "new": "Emerging Leadership", "reason": "Leaders distinguishable; operational evidence accumulating across multiple sub-segments", "actor": "Founder", "timestamp": "2023-06-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Under Human Review", "reason": "Initial theme proposal", "actor": "Founder", "timestamp": "2023-03-01T10:00:00Z", "version": "v0.1.0"},
            {"prior": "Under Human Review", "new": "Approved", "reason": "Structural demographic driver; broad beneficiary set across device categories", "actor": "Founder", "timestamp": "2023-06-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Theme approved — begin active tracking", "actor": "Founder", "timestamp": "2023-06-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 139,
        "key_tickers": ["ABT", "MDT", "BSX", "SYK", "ISRG", "EW"],
    },
    {
        "id": "TH-010", "name": "Solar", "sector": "Technology", "industry": "Solar",
        "lifecycle": "Formation", "approval_status": "Approved", "monitoring_status": "Active Monitoring",
        "why_now": "IRA tax credits providing multi-year policy visibility. Utility-scale pipeline at record levels. Grid modernization creating structural demand.",
        "confidence": "Low",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Under Human Review", "reason": "Initial theme proposal", "actor": "Founder", "timestamp": "2023-12-01T10:00:00Z", "version": "v0.1.0"},
            {"prior": "Under Human Review", "new": "Approved", "reason": "Structural driver (decarbonization) confirmed; evidence available for V0 fixtures", "actor": "Founder", "timestamp": "2024-01-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Theme approved — begin active tracking", "actor": "Founder", "timestamp": "2024-01-15T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 22,
        "key_tickers": ["ENPH", "FSLR", "SEDG", "RUN", "CSIQ", "ARRY"],
    },
]

# ═══════════════════════════════════════════════════════════
# CANDIDATES (Strategy Context: Alpha Momentum)
# ═══════════════════════════════════════════════════════════
CANDIDATES = [
    {
        "id": "CAND-001", "asset_id": "AST-001", "entity_id": "ENT-001", "ticker": "NVDA",
        "candidate_quality": {
            "fundamentals": "Strong", "growth": "Accelerating", "liquidity": "High",
            "relative_strength": "Leading", "trend_quality": "Smooth", "accumulation": "Confirmed",
            "industry_leadership": "Confirmed Leader",
        },
        "entry_readiness": {
            "price_structure": "Stage 2 — Advancing", "base_quality": "Constructive",
            "breakout_proximity": "Near", "volume_behavior": "Accumulation",
            "volatility_contraction": "Tightening", "extension_risk": "Moderate",
        },
        "data_confidence": {"freshness": "Current — 8/8 fields", "completeness": "Complete — 8/8 expected", "reliability": "High — Verified filings", "conflicts": "None", "missing_data": "None"},
        "research_state": "Priority Research",
        "research_transitions": [
            {"prior": "Watchlist", "new": "Priority Research", "actor": "Founder", "timestamp": "2024-06-01T10:00:00Z", "rationale": "Strong fundamentals + breakout proximity"},
        ],
    },
    {
        "id": "CAND-002", "asset_id": "AST-002", "entity_id": "ENT-002", "ticker": "INTC",
        "candidate_quality": {
            "fundamentals": "Weak", "growth": "Declining", "liquidity": "Adequate",
            "relative_strength": "Lagging", "trend_quality": "Choppy", "accumulation": "Distribution",
            "industry_leadership": "Former Leader",
        },
        "entry_readiness": {
            "price_structure": "Stage 4 — Declining", "base_quality": "Destructive",
            "breakout_proximity": "None", "volume_behavior": "Distribution",
            "volatility_contraction": "Expanding", "extension_risk": "High — below moving averages",
        },
        "data_confidence": {"freshness": "Current — 8/8 fields", "completeness": "Complete — 8/8 expected", "reliability": "High — Verified filings", "conflicts": "None", "missing_data": "None"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
    {
        "id": "CAND-003", "asset_id": "AST-003", "entity_id": "ENT-003", "ticker": "AMD",
        "candidate_quality": {
            "fundamentals": "Strong", "growth": "Accelerating", "liquidity": "High",
            "relative_strength": "Leading", "trend_quality": "Smooth", "accumulation": "Confirmed",
            "industry_leadership": "Emerging Challenger",
        },
        "entry_readiness": {
            "price_structure": "Stage 2 — Advancing", "base_quality": "Constructive",
            "breakout_proximity": "Near", "volume_behavior": "Accumulation",
            "volatility_contraction": "Tightening", "extension_risk": "Low",
        },
        "data_confidence": {"freshness": "Current — 8/8 fields", "completeness": "Complete — 8/8 expected", "reliability": "High — Verified filings", "conflicts": "None", "missing_data": "None"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
    {
        "id": "CAND-004", "asset_id": "AST-004", "entity_id": "ENT-004", "ticker": "MDT",
        "candidate_quality": {
            "fundamentals": "Strong", "growth": "Stable", "liquidity": "High",
            "relative_strength": "Neutral", "trend_quality": "Moderate", "accumulation": "Neutral",
            "industry_leadership": "Confirmed Leader",
        },
        "entry_readiness": {
            "price_structure": "Stage 3 — Topping", "base_quality": "Neutral",
            "breakout_proximity": "Far", "volume_behavior": "Neutral",
            "volatility_contraction": "None", "extension_risk": "High — extended from base",
        },
        "data_confidence": {"freshness": "Current — 7/8 fields", "completeness": "Incomplete — 7/8 expected", "reliability": "High — Verified filings", "conflicts": "None", "missing_data": "Missing: competitive landscape update Q2 2024"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
    {
        "id": "CAND-005", "asset_id": "AST-005", "entity_id": "ENT-005", "ticker": "FSLR",
        "candidate_quality": {
            "fundamentals": "Moderate", "growth": "Decelerating", "liquidity": "Adequate",
            "relative_strength": "Lagging", "trend_quality": "Choppy", "accumulation": "Neutral",
            "industry_leadership": "Emerging Challenger",
        },
        "entry_readiness": {
            "price_structure": "Stage 1 — Basing", "base_quality": "Early — insufficient duration",
            "breakout_proximity": "Far", "volume_behavior": "Low",
            "volatility_contraction": "None", "extension_risk": "Low",
        },
        "data_confidence": {"freshness": "Stale — 3/8 fields > 90 days", "completeness": "Incomplete — 3/8 expected", "reliability": "Medium — mixed sources", "conflicts": "None", "missing_data": "Missing: 5 fields (ROI, cost trajectory, competitive pricing, policy impact, margin forecast)"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
]

# ═══════════════════════════════════════════════════════════
# CANDIDATE–THEME RELATIONSHIPS
# ═══════════════════════════════════════════════════════════
CANDIDATE_THEME = [
    {
        "id": "CTR-001", "candidate_id": "CAND-001", "theme_id": "TH-004",
        "primary_role": "Direct Beneficiary", "secondary_roles": ["Enabler"],
        "leadership_state": "Confirmed Leader",
        "leadership_transitions": [],
        "evidence_refs": ["EV-001"],
    },
    {
        "id": "CTR-002", "candidate_id": "CAND-002", "theme_id": "TH-004",
        "primary_role": "Direct Beneficiary", "secondary_roles": [],
        "leadership_state": "Former Leader",
        "leadership_transitions": [
            {"prior": "Confirmed Leader", "new": "Former Leader", "reason": "Lost process leadership; revenue declining; market share erosion to AMD and NVDA", "actor": "System", "timestamp": "2021-07-15T10:00:00Z", "evidence": ["EV-003"]},
        ],
        "evidence_refs": [],
    },
    {
        "id": "CTR-003", "candidate_id": "CAND-003", "theme_id": "TH-004",
        "primary_role": "Direct Beneficiary", "secondary_roles": ["Enabler"],
        "leadership_state": "Emerging Challenger",
        "leadership_transitions": [],
        "evidence_refs": ["EV-004"],
    },
    {
        "id": "CTR-004", "candidate_id": "CAND-004", "theme_id": "TH-014",
        "primary_role": "Direct Beneficiary", "secondary_roles": [],
        "leadership_state": "Confirmed Leader",
        "leadership_transitions": [],
        "evidence_refs": ["EV-007"],
    },
    {
        "id": "CTR-005", "candidate_id": "CAND-005", "theme_id": "TH-010",
        "primary_role": "Direct Beneficiary", "secondary_roles": [],
        "leadership_state": "Emerging Challenger",
        "leadership_transitions": [],
        "evidence_refs": ["EV-010"],
    },
]

# ═══════════════════════════════════════════════════════════
# HUMAN OVERRIDE
# ═══════════════════════════════════════════════════════════
HUMAN_OVERRIDES = [
    {
        "id": "OVR-001",
        "candidate_id": "CAND-002",
        "system_assessment": "Candidate Quality: Weak (all dimensions deteriorating). Entry Readiness: Stage 4 — no setup. Recommendation: Archive this candidate.",
        "machine_dissent": "Warning: Despite weak technical picture, INTC remains a Direct Beneficiary of Semiconductor theme via government CHIPS Act funding and domestic manufacturing strategy.",
        "unresolved_counter_evidence": "EV-003: Semiconductor cycle historically boom-bust — INTC may benefit from cycle trough. CHIPS Act provides $8.5B direct funding — thesis not yet invalidated.",
        "founder_rationale": "Maintaining Watchlist. CHIPS Act funding creates structural floor. INTC's foundry strategy (IFS) is a multi-year transformation — cannot evaluate on current momentum alone. Will reassess after next 2 earnings.",
        "required_confirmation": "Next 2 quarterly reports must show revenue stabilization and foundry customer announcements.",
        "reassessment_point": "2025-01-15",
        "eventual_outcome": "Pending",
        "decision_type_and_scope": "Research State demotion override — maintain Watchlist for INTC in TH-004 (Semiconductors)",
        "timestamp": "2024-07-01T10:00:00Z",
    },
]

# ═══════════════════════════════════════════════════════════
# ALTERNATIVE EXPLANATIONS
# ═══════════════════════════════════════════════════════════
ALTERNATIVE_EXPLANATIONS = {
    "TH-004": "Alternative: AI infrastructure buildout may be a short-term inventory cycle rather than structural shift. Cloud providers may overbuild then pause (2018 pattern repeat).",
    "TH-014": None,
    "TH-010": "Alternative: Solar demand may be primarily policy-driven (IRA) rather than economic — policy change risk is material.",
}

# ═══════════════════════════════════════════════════════════
# PIPELINE CONFIG (provisional — no investment rules invented)
# ═══════════════════════════════════════════════════════════
PIPELINE_CONFIG = {
    "pipeline_version": "v0.1.0",
    "strategy": "Alpha Momentum",
    "universe": "NYSE + NASDAQ + ADRs (synthetic fixture subset)",
    "point_in_time": "2024-07-01",
    "fixture_category": FIXTURE_CATEGORY,
    "theme_context_mode": "Filter — Candidate must have >= 1 Theme relationship",
    "queue_grouping": "Theme-first",
    "queue_ordering": "V0 fixed: sector → industry → lifecycle-prioritized within theme",
    "adaptive_capacity": True,
    "empty_queue_valid": True,
    "show_all_candidates": True,
    "no_quality_threshold": True,
}
