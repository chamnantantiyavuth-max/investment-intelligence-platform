"""
Fundamental & Opportunity V0 — Synthetic Fixtures
Per FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)
SYNTHETIC — FOR V0 TESTING ONLY. NOT LIVE DATA.
"""

FIXTURES = [
    {
        "id": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "market_cap": 3200,  # billions
        # ── Moat (§3.4.1) ──
        "moat_types": [
            {"type": "Share of Mind", "strength": "Strong",
             "evidence": "#1 consumer tech brand globally, NPS 72, brand value $500B+"},
            {"type": "High Switching Cost", "strength": "Moderate",
             "evidence": "iOS ecosystem lock-in: iMessage, iCloud, App Store, 2B+ active devices"},
            {"type": "Intangible Assets", "strength": "Weak",
             "evidence": "Design patents; many expiring. Services IP growing (Apple Pay, Fitness+)"},
        ],
        "moat_width": "Wide",
        "moat_depth": "Deep",
        "moat_trend": "Stable",
        # ── Financial Quality (§3.4) ──
        "gross_margin": 0.46,
        "operating_margin": 0.31,
        "fcf_conversion": 1.15,  # FCF/EPS
        "debt_to_equity": 1.8,
        "roe": 1.45,
        "revenue_growth_3y": 0.08,
        # ── Earnings Quality (§3.5.1) ──
        "latest_eps": 1.52,
        "consensus_eps": 1.46,
        "surprise_direction": "Beat",
        "surprise_magnitude_pct": 4.2,
        "revenue_quality": "HIGH",
        "margin_quality": "HIGH",
        "one_time_items": False,
        "share_buyback_impact_pct": 0.3,
        "guidance_direction": "Raised",
        "guidance_reason": "Organic demand — Services accelerating",
        # ── Valuation (§3.6) ──
        "pe_ttm": 31.2,
        "pe_5y_avg": 28.5,
        "pe_10y_avg": 22.0,
        "ev_ebitda": 23.4,
        "ev_ebitda_industry": 18.2,
        "fcf_yield": 0.036,
        "scenario_bull": 220,
        "scenario_base": 185,
        "scenario_bear": 140,
        "current_price": 190,
        # ── Management ──
        "ceo_tenure_years": 13,
        "management_credibility": "HIGH",
        "insider_activity": "CEO sold $50M for tax purposes — no concern",
        "cfo_turnover_3y": 0,
    },
    {
        "id": "INTC",
        "name": "Intel Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "market_cap": 180,
        # ── Moat ──
        "moat_types": [
            {"type": "Share of Mind", "strength": "Weak",
             "evidence": "Brand declining — 'Intel Inside' less relevant in mobile/AI era"},
            {"type": "Intangible Assets", "strength": "Weak",
             "evidence": "x86 architecture still relevant but ARM encroaching in client and server"},
        ],
        "moat_width": "Narrow",
        "moat_depth": "Shallow",
        "moat_trend": "Narrowing",
        # ── Financial Quality ──
        "gross_margin": 0.41,
        "operating_margin": 0.05,  # crumbling
        "fcf_conversion": -0.30,  # negative FCF
        "debt_to_equity": 0.55,
        "roe": 0.02,
        "revenue_growth_3y": -0.08,
        # ── Earnings Quality ──
        "latest_eps": 0.13,
        "consensus_eps": 0.20,
        "surprise_direction": "Miss",
        "surprise_magnitude_pct": -35.0,
        "revenue_quality": "LOW",
        "margin_quality": "LOW",
        "one_time_items": True,  # restructuring charges
        "share_buyback_impact_pct": 0.0,
        "guidance_direction": "Lowered",
        "guidance_reason": "PC TAM softening, foundry investment weighing on margins",
        # ── Valuation ──
        "pe_ttm": 14.0,
        "pe_5y_avg": 22.0,
        "pe_10y_avg": 18.5,
        "ev_ebitda": 7.2,
        "ev_ebitda_industry": 12.5,
        "fcf_yield": -0.02,
        "scenario_bull": 35,
        "scenario_base": 22,
        "scenario_bear": 12,
        "current_price": 22,
        # ── Management ──
        "ceo_tenure_years": 3,
        "management_credibility": "LOW",
        "insider_activity": "4th CEO in 6 years; missed foundry targets consistently",
        "cfo_turnover_3y": 2,
    },
    {
        "id": "COST",
        "name": "Costco Wholesale Corporation",
        "sector": "Consumer Staples",
        "industry": "Retail — Wholesale",
        "market_cap": 350,
        # ── Moat ──
        "moat_types": [
            {"type": "Cost Advantage", "strength": "Strong",
             "evidence": "Membership model + bulk purchasing = lowest cost structure in retail. Operating margin 3% but membership fees = pure profit."},
            {"type": "Efficient Scale", "strength": "Moderate",
             "evidence": "Limited warehouse locations per metro area — natural geographic oligopoly"},
        ],
        "moat_width": "Wide",
        "moat_depth": "Deep",
        "moat_trend": "Widening",
        # ── Financial Quality ──
        "gross_margin": 0.13,
        "operating_margin": 0.036,
        "fcf_conversion": 1.30,
        "debt_to_equity": 0.30,
        "roe": 0.28,
        "revenue_growth_3y": 0.09,
        # ── Earnings Quality ──
        "latest_eps": 3.78,
        "consensus_eps": 3.62,
        "surprise_direction": "Beat",
        "surprise_magnitude_pct": 4.4,
        "revenue_quality": "HIGH",
        "margin_quality": "MEDIUM",  # low margin business model by design
        "one_time_items": False,
        "share_buyback_impact_pct": 0.0,
        "guidance_direction": "Maintained",
        "guidance_reason": "Membership renewal rate 92.4% — steady organic growth",
        # ── Valuation ──
        "pe_ttm": 42.0,
        "pe_5y_avg": 36.5,
        "pe_10y_avg": 30.0,
        "ev_ebitda": 25.0,
        "ev_ebitda_industry": 14.5,
        "fcf_yield": 0.025,
        "scenario_bull": 650,
        "scenario_base": 520,
        "scenario_bear": 380,
        "current_price": 520,
        # ── Management ──
        "ceo_tenure_years": 12,
        "management_credibility": "HIGH",
        "insider_activity": "No material insider sales; consistent modest buying",
        "cfo_turnover_3y": 0,
    },
    {
        "id": "CRM",
        "name": "Salesforce, Inc.",
        "sector": "Technology",
        "industry": "Enterprise Software",
        "market_cap": 280,
        # ── Moat ──
        "moat_types": [
            {"type": "High Switching Cost", "strength": "Strong",
             "evidence": "CRM data integrated into sales/marketing workflows — migration pain, retraining cost, data loss risk"},
            {"type": "Network Effect", "strength": "Moderate",
             "evidence": "AppExchange ecosystem + customer community; more users = more integrations"},
        ],
        "moat_width": "Wide",
        "moat_depth": "Moderate",
        "moat_trend": "Stable",
        # ── Financial Quality ──
        "gross_margin": 0.76,
        "operating_margin": 0.20,
        "fcf_conversion": 0.95,
        "debt_to_equity": 0.25,
        "roe": 0.12,
        "revenue_growth_3y": 0.11,
        # ── Earnings Quality ──
        "latest_eps": 2.12,
        "consensus_eps": 2.08,
        "surprise_direction": "Beat",
        "surprise_magnitude_pct": 1.9,
        "revenue_quality": "MEDIUM",  # growth slowing from 20% to 11%
        "margin_quality": "HIGH",  # margin expanding via efficiency
        "one_time_items": False,
        "share_buyback_impact_pct": 1.2,
        "guidance_direction": "Maintained",
        "guidance_reason": "Revenue growth decelerating but margins improving",
        # ── Valuation ──
        "pe_ttm": 25.0,
        "pe_5y_avg": 55.0,
        "pe_10y_avg": 65.0,
        "ev_ebitda": 18.0,
        "ev_ebitda_industry": 22.0,
        "fcf_yield": 0.04,
        "scenario_bull": 320,
        "scenario_base": 255,
        "scenario_bear": 180,
        "current_price": 255,
        # ── Management ──
        "ceo_tenure_years": 24,  # Marc Benioff, founder
        "management_credibility": "HIGH",
        "insider_activity": "CEO sold shares per 10b5-1 plan — routine diversification",
        "cfo_turnover_3y": 1,
    },
    {
        "id": "XYZ",
        "name": "XYZ Legacy Manufacturing (Synthetic — Cosmetic Beat)",
        "sector": "Industrials",
        "industry": "Industrial Machinery",
        "market_cap": 45,
        # ── Moat ──
        "moat_types": [],
        "moat_width": "None",
        "moat_depth": "Shallow",
        "moat_trend": "Narrowing",
        # ── Financial Quality ──
        "gross_margin": 0.28,
        "operating_margin": 0.09,
        "fcf_conversion": 0.40,  # low quality
        "debt_to_equity": 1.5,
        "roe": 0.08,
        "revenue_growth_3y": -0.03,
        # ── Earnings Quality (COSMETIC — the point of this fixture) ──
        "latest_eps": 1.20,
        "consensus_eps": 1.00,
        "surprise_direction": "Beat",
        "surprise_magnitude_pct": 20.0,
        "revenue_quality": "LOW",  # revenue declining!
        "margin_quality": "LOW",
        "one_time_items": True,  # $0.15 EPS from legal settlement
        "share_buyback_impact_pct": 4.0,  # bought back 4% of shares — masking EPS decline
        "guidance_direction": "Unchanged",
        "guidance_reason": "Management avoided guidance update despite revenue decline",
        # ── Valuation ──
        "pe_ttm": 8.5,
        "pe_5y_avg": 15.0,
        "pe_10y_avg": 14.0,
        "ev_ebitda": 5.5,
        "ev_ebitda_industry": 11.0,
        "fcf_yield": 0.045,  # low quality FCF
        "scenario_bull": 55,
        "scenario_base": 32,
        "scenario_bear": 18,
        "current_price": 32,
        # ── Management ──
        "ceo_tenure_years": 2,
        "management_credibility": "LOW",
        "insider_activity": "CFO resigned last quarter; CEO sold 30% of holdings",
        "cfo_turnover_3y": 2,
    },
]

# Macro regime context (applied to all companies)
MACRO_REGIME = {
    "regime": "Growth — Late Cycle",
    "gdp_growth": 0.025,
    "inflation": 0.031,
    "fed_funds": 0.0525,
    "yield_curve": "Flat",
    "credit_spreads": "Narrow",
    "sector_implications": {
        "Technology": "Neutral — AI capex tailwind, valuation headwind from rates",
        "Consumer Staples": "Slight headwind — consumer slowing, but staples defensive",
        "Industrials": "Neutral — manufacturing PMI 48.7 (contracting), but infra spending supportive",
    },
}
