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
    # ── TH-020 Cloud Infrastructure ──
    {"id": "EV-014", "type": "Observed Fact", "content": "Global cloud infra spending: $78B in Q1 2024, +21% YoY (Synergy Research)", "source": "SRC-SYN-010", "pub_ts": "2024-04-30T08:00:00Z", "effective": "2024-Q1", "relationship": "supporting", "theme": "TH-020", "candidate": None},
    {"id": "EV-015", "type": "Claim",       "content": "Enterprise AI adoption may shift compute from public cloud to on-prem/edge for latency and cost reasons", "source": "SRC-SYN-011", "pub_ts": "2024-06-01T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-020", "candidate": None},
    {"id": "EV-016", "type": "Missing",     "content": "Missing: enterprise workload migration completion rate by industry vertical", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-020", "candidate": None},
    # ── TH-030 Cybersecurity ──
    {"id": "EV-017", "type": "Observed Fact", "content": "Ransomware attacks: 4,611 incidents in 2023, +73% YoY (Verizon DBIR 2024)", "source": "SRC-SYN-012", "pub_ts": "2024-05-01T08:00:00Z", "effective": "2023-FY", "relationship": "supporting", "theme": "TH-030", "candidate": None},
    {"id": "EV-018", "type": "Claim",       "content": "Cybersecurity spending may face budget fatigue — CISO survey shows tool consolidation trend", "source": "SRC-SYN-013", "pub_ts": "2024-06-01T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-030", "candidate": None},
    {"id": "EV-019", "type": "Missing",     "content": "Missing: AI-driven attack volume projection vs AI-defense capability gap analysis", "source": None, "pub_ts": None, "effective": None, "relationship": "missing", "theme": "TH-030", "candidate": None},
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
    {
        "id": "TH-020", "name": "Cloud Infrastructure", "sector": "Technology", "industry": "Cloud & Data Centers",
        "lifecycle": "Emerging Leadership", "approval_status": "Approved", "monitoring_status": "Active Monitoring",
        "why_now": "Hyperscaler capex at record levels ($200B+ forecast 2025). Enterprise cloud migration still in early innings (< 40% workloads). AI inference driving new data center demand layer.",
        "confidence": "Medium",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Under Human Review", "reason": "Initial theme proposal", "actor": "Founder", "timestamp": "2024-03-01T10:00:00Z", "version": "v0.1.0"},
            {"prior": "Under Human Review", "new": "Approved", "reason": "Structural cloud migration trend confirmed — identifiable suppliers", "actor": "Founder", "timestamp": "2024-06-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Theme approved — begin active tracking", "actor": "Founder", "timestamp": "2024-06-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 55,
        "key_tickers": ["AMZN", "MSFT", "GOOGL", "ORCL", "SMCI", "DELL"],
    },
    {
        "id": "TH-030", "name": "Cybersecurity", "sector": "Technology", "industry": "Cybersecurity",
        "lifecycle": "Formation", "approval_status": "Approved", "monitoring_status": "Active Monitoring",
        "why_now": "Ransomware attack frequency +73% YoY. SEC disclosure rules now mandate material incident reporting within 4 days. Zero-trust architecture becoming enterprise standard.",
        "confidence": "Low",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Under Human Review", "reason": "Initial theme proposal", "actor": "Founder", "timestamp": "2024-04-01T10:00:00Z", "version": "v0.1.0"},
            {"prior": "Under Human Review", "new": "Approved", "reason": "Structural threat escalation driver; identifiable beneficiaries across endpoint, network, and cloud security", "actor": "Founder", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Theme approved — begin active tracking", "actor": "Founder", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 48,
        "key_tickers": ["CRWD", "PANW", "ZS", "FTNT", "OKTA", "NET"],
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
    {
        "id": "CTR-006", "candidate_id": "CAND-001", "theme_id": "TH-020",
        "primary_role": "Enabler", "secondary_roles": [],
        "leadership_state": "Confirmed Leader",
        "leadership_transitions": [],
        "evidence_refs": ["EV-014"],
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
    "TH-020": "Alternative: Cloud growth may already be priced in — hyperscaler multiples at decade highs. AI inference efficiency improvements could reduce total compute demand per query.",
    "TH-030": "Alternative: Cybersecurity spending growth may decelerate as AI-automated defense reduces per-seat pricing. Platform consolidation (fewer vendors) could compress total addressable market growth.",
}

# ═══════════════════════════════════════════════════════════
# ⚠️ EXPERIMENTAL THEMES (approval_status="Experimental")
# ⚠️ QUARANTINED per Phase 2R Review (23 Jul 2026)
# ⚠️ Phase 5 is NOT AUTHORIZED — preview data only
# ⚠️ Do NOT integrate into main pipeline until Phase 5 FD exists
# ═══════════════════════════════════════════════════════════
# AI-created themes tracked separately from official Approved themes.
# They may have Active Monitoring but CANNOT affect official strategy outputs.
EXPERIMENTAL_THEMES = [
    {
        "id": "TH-EXP-001", "name": "Quantum Computing Commercialization", "sector": "Technology", "industry": "Quantum Computing",
        "lifecycle": "Formation", "approval_status": "Experimental", "monitoring_status": "Active Monitoring",
        "why_now": "IBM Quantum Heron processor (1,121 qubits) and Google Willow chip demonstrating error correction at scale. DARPA US2QC program selecting vendors for utility-scale quantum by 2029. NIST post-quantum cryptography standards finalized — driving enterprise urgency.",
        "confidence": "Low",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Experimental", "reason": "AI-detected signal: multiple quantum milestones in Q2 2024 (IBM, Google, DARPA) suggest acceleration", "actor": "AI System", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Experimental theme — active monitoring for signal validation", "actor": "AI System", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 12,
        "key_tickers": ["IBM", "IONQ", "QBTS", "RGTI", "HON", "MSFT"],
    },
    {
        "id": "TH-EXP-002", "name": "Nuclear Energy Renaissance", "sector": "Energy", "industry": "Nuclear",
        "lifecycle": "Formation", "approval_status": "Experimental", "monitoring_status": "Active Monitoring",
        "why_now": "AI data center power demand projections (50-100 GW new capacity needed by 2030) forcing hyperscalers to evaluate nuclear. Microsoft PPA with Helion (fusion, 2028 target). Vogtle 3+4 completions (first new US reactors in 30 years). NRC streamlining SMR licensing. Uranium spot at $90+/lb — 16-year high.",
        "confidence": "Low",
        "lifecycle_transitions": [],
        "approval_transitions": [
            {"prior": "Detected Hypothesis", "new": "Experimental", "reason": "AI-detected signal: hyperscaler nuclear PPAs + uranium price + regulatory shift pattern", "actor": "AI System", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "monitoring_transitions": [
            {"prior": "Not Monitored", "new": "Active Monitoring", "reason": "Experimental theme — active monitoring for signal validation", "actor": "AI System", "timestamp": "2024-07-01T10:00:00Z", "version": "v0.1.0"},
        ],
        "stocks_in_industry": 22,
        "key_tickers": ["CEG", "BWXT", "CCJ", "UEC", "LEU", "SMR"],
    },
]

# ═══════════════════════════════════════════════════════════
# ⚠️ EXPERIMENTAL CANDIDATES — QUARANTINED (23 Jul 2026)
# ═══════════════════════════════════════════════════════════
EXPERIMENTAL_CANDIDATES = [
    {
        "id": "CAND-EXP-001", "asset_id": "AST-EXP-001", "entity_id": "ENT-EXP-001", "ticker": "IONQ",
        "candidate_quality": {
            "fundamentals": "Pre-Revenue", "growth": "Not Yet", "liquidity": "Adequate",
            "relative_strength": "Neutral", "trend_quality": "Choppy", "accumulation": "Neutral",
            "industry_leadership": "Emerging Challenger",
        },
        "entry_readiness": {
            "price_structure": "Stage 1 — Basing", "base_quality": "Early — insufficient duration",
            "breakout_proximity": "Far", "volume_behavior": "Low",
            "volatility_contraction": "None", "extension_risk": "Low",
        },
        "data_confidence": {"freshness": "Current — 6/8 fields", "completeness": "Incomplete — early-stage company", "reliability": "Low — pre-revenue, limited history", "conflicts": "None", "missing_data": "Missing: earnings track record, institutional ownership history"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
    {
        "id": "CAND-EXP-002", "asset_id": "AST-EXP-002", "entity_id": "ENT-EXP-002", "ticker": "CEG",
        "candidate_quality": {
            "fundamentals": "Strong", "growth": "Accelerating", "liquidity": "High",
            "relative_strength": "Leading", "trend_quality": "Smooth", "accumulation": "Confirmed",
            "industry_leadership": "Confirmed Leader",
        },
        "entry_readiness": {
            "price_structure": "Stage 2 — Advancing", "base_quality": "Constructive",
            "breakout_proximity": "In Progress", "volume_behavior": "Accumulation",
            "volatility_contraction": "Tightening", "extension_risk": "Moderate",
        },
        "data_confidence": {"freshness": "Current — 8/8 fields", "completeness": "Complete", "reliability": "High — regulated utility, audited financials", "conflicts": "None", "missing_data": "None"},
        "research_state": "Watchlist",
        "research_transitions": [],
    },
]

# Experimental entity + asset stubs (minimal — for pipeline compatibility)
EXPERIMENTAL_ENTITIES = [
    {"id": "ENT-EXP-001", "name": "IonQ, Inc.",             "sector": "Technology", "industry": "Quantum Computing", "fixture_type": "Historical identifier, synthetic data"},
    {"id": "ENT-EXP-002", "name": "Constellation Energy",   "sector": "Energy",     "industry": "Nuclear",           "fixture_type": "Historical identifier, synthetic data"},
]

EXPERIMENTAL_ASSETS = [
    {"id": "AST-EXP-001", "ticker": "IONQ", "entity_id": "ENT-EXP-001", "exchange": "NYSE", "asset_type": "Common Stock"},
    {"id": "AST-EXP-002", "ticker": "CEG",  "entity_id": "ENT-EXP-002", "exchange": "NASDAQ", "asset_type": "Common Stock"},
]

EXPERIMENTAL_CANDIDATE_THEME = [
    {"id": "CTR-EXP-001", "candidate_id": "CAND-EXP-001", "theme_id": "TH-EXP-001",
     "primary_role": "Direct Beneficiary", "secondary_roles": [],
     "leadership_state": "Emerging Challenger", "leadership_transitions": [], "evidence_refs": []},
    {"id": "CTR-EXP-002", "candidate_id": "CAND-EXP-002", "theme_id": "TH-EXP-002",
     "primary_role": "Direct Beneficiary", "secondary_roles": ["Enabler"],
     "leadership_state": "Confirmed Leader", "leadership_transitions": [], "evidence_refs": []},
]

EXPERIMENTAL_EVIDENCE = [
    {"id": "EV-EXP-001", "type": "Observed Fact", "content": "IBM Quantum Heron: 1,121 qubits demonstrated, gate fidelity 99.8%", "source": "SRC-SYN-EXP-001", "pub_ts": "2024-05-15T08:00:00Z", "effective": "2024-Q2", "relationship": "supporting", "theme": "TH-EXP-001", "candidate": "IONQ"},
    {"id": "EV-EXP-002", "type": "Claim", "content": "NISQ-era quantum may never achieve practical advantage over classical GPU clusters for ML workloads", "source": "SRC-SYN-EXP-002", "pub_ts": "2024-06-01T08:00:00Z", "effective": "2024-Q2", "relationship": "contradicting", "theme": "TH-EXP-001", "candidate": None},
    {"id": "EV-EXP-003", "type": "Observed Fact", "content": "Microsoft signed PPA with Helion Energy for fusion power starting 2028 — first-ever fusion PPA", "source": "SRC-SYN-EXP-003", "pub_ts": "2024-05-10T08:00:00Z", "effective": "2024-Q2", "relationship": "supporting", "theme": "TH-EXP-002", "candidate": "CEG"},
    {"id": "EV-EXP-004", "type": "Claim", "content": "Small modular reactor (SMR) economics remain unproven at scale — NuScale project cancellation (2023) raises viability questions", "source": "SRC-SYN-EXP-004", "pub_ts": "2024-04-15T08:00:00Z", "effective": "2024-Q1", "relationship": "contradicting", "theme": "TH-EXP-002", "candidate": None},
]

# ═══════════════════════════════════════════════════════════
# ⚠️ WEAK SIGNAL INBOX — ANOMALIES — QUARANTINED (23 Jul 2026)
# ═══════════════════════════════════════════════════════════
# Unexplained observations that don't yet fit any approved theme.
# Anomalies are facts or patterns — not yet hypotheses or themes.
ANOMALIES = [
    {
        "id": "AN-001",
        "type": "Sector Divergence",
        "description": "Healthcare sector RS ranking rose from #8 to #3 in 6 weeks while medical device theme (TH-014) remains Emerging Leadership without corresponding candidate additions. Sector breadth suggests broader participation beyond devices — biotech and services showing independent strength.",
        "first_observed": "2024-06-15",
        "related_theme": "TH-014",
        "related_tickers": ["ISRG", "SYK", "BSX", "VRTX", "REGN"],
        "status": "Unexplained",
        "source": "Price-based observation — V0 synthetic",
    },
    {
        "id": "AN-002",
        "type": "Single-Stock Outlier",
        "description": "AVGO (Broadcom) price +38% YTD with RS in top 5% of market — but AVGO is in TH-004 (Semiconductors) only as a key_ticker, not as a tracked Candidate. AVGO's AI networking revenue ($3B+ quarterly) suggests a distinct AI-networking sub-theme that TH-004 may not fully capture.",
        "first_observed": "2024-06-20",
        "related_theme": "TH-004",
        "related_tickers": ["AVGO", "MRVL", "ANET"],
        "status": "Unexplained",
        "source": "Price-based observation — V0 synthetic",
    },
    {
        "id": "AN-003",
        "type": "Volume Anomaly",
        "description": "Unusually high institutional volume (2.5x 90-day avg) in CRWD, PANW, and ZS during market down days — potential accumulation signal in TH-030 (Cybersecurity) even while theme confidence remains Low. Contradicts the 'budget fatigue' contradicting evidence (EV-018).",
        "first_observed": "2024-06-25",
        "related_theme": "TH-030",
        "related_tickers": ["CRWD", "PANW", "ZS"],
        "status": "Unexplained",
        "source": "Price-based observation — V0 synthetic",
    },
    {
        "id": "AN-004",
        "type": "Missing Correlation",
        "description": "Solar ETF (TAN) +12% in 4 weeks but FSLR (CAND-005) remains Stage 1 Basing and has not participated. ENPH and SEDG leading the move instead. FSLR's key_ticker status in TH-010 may be masking better-positioned candidates.",
        "first_observed": "2024-07-01",
        "related_theme": "TH-010",
        "related_tickers": ["FSLR", "ENPH", "SEDG", "TAN"],
        "status": "Unexplained",
        "source": "Price-based observation — V0 synthetic",
    },
]

# ═══════════════════════════════════════════════════════════
# ⚠️ WEAK SIGNAL INBOX — THEME HYPOTHESES — QUARANTINED (23 Jul 2026)
# ═══════════════════════════════════════════════════════════
# Early-stage theme proposals that have not yet advanced to
# Experimental or Approved status. These are ideas, not themes.
INBOX_HYPOTHESES = [
    {
        "id": "HY-001",
        "title": "AI Edge Computing",
        "proposed_driver": "Enterprise AI inference workloads shifting from centralized cloud to edge/on-premise for latency, cost, and data sovereignty reasons. Hyperscaler edge offerings expanding. Inference-at-edge requires different hardware (smaller models, lower power) than training — creating a distinct beneficiary set from cloud infrastructure (TH-020).",
        "why_now": "Apple Intelligence on-device processing, Microsoft Copilot+ PCs with NPUs, and AWS Outposts expansion all signaling edge-first AI deployment in 2024-2025. Inference efficiency gains (EV-005 notes 50-90% reduction per query) may paradoxically increase total edge AI demand via Jevons paradox — cheaper inference → more use cases → more total compute.",
        "potential_candidates": ["QCOM", "ARM", "INTC", "AMD", "DELL", "HPQ"],
        "potential_theme_industry": "Edge Computing / AI Hardware",
        "relationship_to_existing": "Overlaps with TH-004 (Semiconductors — hardware suppliers) and TH-020 (Cloud — competition/alternative to centralized cloud). Distinct in focus on inference-at-edge rather than training-at-datacenter.",
        "key_unknowns": [
            "Edge AI chip TAM projections vary by 10x across analyst estimates",
            "Unclear whether on-device processing reduces or increases total semiconductor demand",
            "Regulatory: EU AI Act may impose edge-specific compliance costs",
        ],
        "proposed_date": "2024-07-01",
        "status": "Hypothesis — awaiting Founder review",
    },
    {
        "id": "HY-002",
        "title": "Water Infrastructure & Scarcity",
        "proposed_driver": "Global freshwater demand projected to exceed supply by 40% by 2030 (UN). Aging US water infrastructure (EPA estimate: $744B needed over 20 years). Semiconductor manufacturing is water-intensive — CHIPS Act fabs in Arizona face water availability constraints, forcing investment in water recycling and desalination at the industrial level.",
        "why_now": "2024 Arizona water rulings limiting new industrial usage. TSMC Phoenix fab water recycling investment = leading indicator. Municipal water utilities issuing record rate-increase requests. Infrastructure bill water funding starting to flow to projects.",
        "potential_candidates": ["AWK", "XYL", "WTRG", "PNR", "BMI", "VLTO"],
        "potential_theme_industry": "Water Infrastructure",
        "relationship_to_existing": "No overlap with existing approved themes. New structural driver — distinct from renewable energy (TH-010 Solar). Water infrastructure has different capex cycle, regulatory structure, and beneficiary set.",
        "key_unknowns": [
            "Water utility rate cases take 12-18 months — revenue visibility is delayed",
            "Industrial water recycling market is fragmented — no pure-play public companies at scale",
            "Municipal procurement cycles are slow; revenue growth may not match urgency narrative",
        ],
        "proposed_date": "2024-07-01",
        "status": "Hypothesis — awaiting Founder review",
    },
    {
        "id": "HY-003",
        "title": "Robotics & Autonomous Systems",
        "proposed_driver": "AI foundation models enabling step-change in robot perception and manipulation. Humanoid robot pilots at Amazon, BMW, and Figure.ai moving from R&D to limited production in 2024-2025. Warehouse automation ROI improved by AI vision systems. Surgical robotics (ISRG da Vinci 5) expanding procedure types. Labor shortage in manufacturing and logistics (3.8% US unemployment) creates structural demand pull.",
        "why_now": "Tesla Optimus Gen 2 demonstrated improved dexterity (June 2024). NVIDIA Omniverse + GR00T foundation model for humanoid robots announced. Amazon deploying Agility Robotics Digit in fulfillment centers. ISRG da Vinci 5 launched Q2 2024 with 10,000+ system installed base.",
        "potential_candidates": ["ISRG", "TSLA", "TER", "ZBRA", "ROK", "PATH"],
        "potential_theme_industry": "Robotics & Automation",
        "relationship_to_existing": "Overlaps with TH-014 (Medical Devices — surgical robotics via ISRG) and TH-004 (Semiconductors — compute suppliers). Distinct in focus on physical automation rather than pure compute or medical.",
        "key_unknowns": [
            "Humanoid robot unit economics unproven at scale — current cost > $100K/unit",
            "Tesla as robotics play conflates EV business risk with robotics optionality",
            "Regulatory framework for autonomous systems in public spaces does not yet exist",
        ],
        "proposed_date": "2024-07-01",
        "status": "Hypothesis — awaiting Founder review",
    },
]

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
