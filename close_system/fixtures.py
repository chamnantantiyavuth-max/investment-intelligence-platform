"""
Close System Product Radar V0 — Synthetic Fixtures
Per CLOSE-SYSTEM-PRODUCT-RADAR.md §2-5 (FD #39, 25 July 2026)
All data is synthetic (Category A). NOT LIVE DATA — FOR V0 TESTING ONLY.

Products across 4 categories:
  - Broad Market ETFs, Sector/Thematic ETFs, Physical Commodities, Fixed Income
Each product assessed against P1-P3 eligibility + 5 intelligence layers.
"""
from datetime import datetime, date

FIXTURE_CATEGORY = "SYNTHETIC — FOR V0 TESTING ONLY"
AS_OF = date(2024, 7, 25)

# ═══════════════════════════════════════════════════════════════
# PRODUCTS — 5 synthetic, covering all 4 categories
# ═══════════════════════════════════════════════════════════════

PRODUCTS = [
    {
        "id": "CS-001",
        "ticker": "GDX",
        "name": "VanEck Gold Miners ETF",
        "category": "Sector/Thematic ETF",
        "description": "Diversified gold mining companies — producers, not explorers.",
        "current_price": 31.50,
        "currency": "USD",

        # ── P1: Cannot Go to Zero ──
        "p1_eligible": True,
        "p1_rationale": "Diversified producers (50+ holdings) with hard-asset backing. Individual miners can fail, but the sector cannot go to zero. Physical gold provides intrinsic floor.",

        # ── P2: Discount Pricing ──
        "p2_discount": True,
        "discount_type": "Production Cost Proximity",
        "discount_depth": "Moderate",
        "discount_detail": {
            "gold_price": 1950,
            "avg_aisc": 1350,
            "marginal_aisc": 1500,
            "price_to_aisc_ratio": 1.30,
            "signal": "Gold at $1,950 vs marginal AISC $1,500 — top-quartile producers at breakeven. Not yet at fear-driven discount but trending toward cost floor.",
        },

        # ── P3: Structural Demand ──
        "p3_demand": True,
        "demand_type": "Monetary / Store-of-Value",
        "demand_detail": {
            "central_bank_buying": "+1,037 tons in 2023 (record), PBoC + RBI + Poland accumulating",
            "inflation_hedge": "Real rates still negative in 60% of developed markets",
            "supply_constraints": "New mine permitting 5-10 years, depletion rate 4%/year",
        },

        # ── 5-Layer Synthesis ──
        "layers": {
            "L1_macro": {"signal": "supporting", "note": "Weakening DXY, real rates negative → gold tailwind"},
            "L2_policy": {"signal": "supporting", "note": "Central bank reserve diversification (de-dollarization)"},
            "L3_cost": {"signal": "supporting", "note": "Price 30% above AISC — moderate floor, not deep discount"},
            "L4_supply_demand": {"signal": "supporting", "note": "Mine supply flat, central bank demand structural"},
            "L5_hidden": {"signal": "neutral", "note": "ETF flows flat, no physical premium anomaly"},
        },
        "layers_aligned": 4,
        "layers_contradicting": 0,
        "conviction": "Moderate",

        # ── Key Risks ──
        "key_risks": [
            "Gold selloff if real rates rise sharply (Fed hawkish pivot)",
            "GDX underperforms physical gold due to operational costs",
            "USD strength from safe-haven flows in risk-off event",
        ],

        # ── Recommendation ──
        "recommendation": "Deep Research",
        "recommendation_rationale": "4 layers aligned, not yet at deep discount. Monitor for gold pullback below $1,800 (P2 strengthens) or GDX breakout confirmation.",
    },
    {
        "id": "CS-002",
        "ticker": "XLE",
        "name": "Energy Select Sector SPDR Fund",
        "category": "Sector/Thematic ETF",
        "description": "US energy sector — integrated majors (XOM, CVX) + E&P + services.",
        "current_price": 82.25,
        "currency": "USD",

        "p1_eligible": True,
        "p1_rationale": "Entire energy sector — global demand for energy does not disappear. Diversified across majors (XOM, CVX), E&P, refiners, services.",

        "p2_discount": True,
        "discount_type": "Cyclical Trough",
        "discount_depth": "Strong",
        "discount_detail": {
            "wti_price": 68.50,
            "marginal_breakeven": 55.00,
            "sector_pe": 10.2,
            "historical_median_pe": 14.5,
            "signal": "Energy sector at 10.2x P/E vs 14.5x historical median. WTI at $68 — moderate but sector pricing in recession fear. Capital discipline (buybacks + dividends) creating shareholder value regardless of oil direction.",
        },

        "p3_demand": True,
        "demand_type": "Industrial Consumption + Inelastic",
        "demand_detail": {
            "global_demand": "102.5 mb/d (record), growing 1.5 mb/d YoY",
            "inelastic": "Transportation, petrochemicals, heating — limited short-term substitution",
            "supply_discipline": "OPEC+ cuts extended, US shale capex discipline (returns to shareholders)",
        },

        "layers": {
            "L1_macro": {"signal": "neutral", "note": "PMI expanding but recession fears capping oil sentiment"},
            "L2_policy": {"signal": "neutral", "note": "SPR refill paused; no major policy catalyst"},
            "L3_cost": {"signal": "supporting", "note": "WTI $68 vs breakeven $55 — profitable but not premium"},
            "L4_supply_demand": {"signal": "supporting", "note": "OPEC+ cuts + US discipline = tight supply; demand at record"},
            "L5_hidden": {"signal": "supporting", "note": "US producers returning 50%+ FCF to shareholders — capital discipline structural"},
        },
        "layers_aligned": 3,
        "layers_contradicting": 0,
        "conviction": "Moderate",

        "key_risks": [
            "Global recession → oil demand collapse (demand destruction)",
            "OPEC+ discipline cracks (Russia/ Iraq cheating on quotas)",
            "Energy transition accelerates → long-term demand peak uncertainty",
        ],

        "recommendation": "Add to Radar Watchlist",
        "recommendation_rationale": "3 layers aligned. Energy sector at cyclical trough on P/E basis + capital discipline story intact. Wait for recession fear to peak (P2 deepens) or oil breakout above $80 for conviction upgrade.",
    },
    {
        "id": "CS-003",
        "ticker": "TLT",
        "name": "iShares 20+ Year Treasury Bond ETF",
        "category": "Fixed Income",
        "description": "Long-duration US Treasury bonds — duration ~16 years. Sensitive to rate expectations.",
        "current_price": 92.40,
        "currency": "USD",

        "p1_eligible": True,
        "p1_rationale": "Backed by US sovereign credit. Can lose purchasing power through inflation but cannot go to zero barring US default.",

        "p2_discount": True,
        "discount_type": "Fear-Driven Selloff",
        "discount_depth": "Maximum",
        "discount_detail": {
            "ytm": 4.65,
            "price_drawdown": "-48% from 2020 highs",
            "real_yield": 1.90,
            "historical_context": "Largest bond bear market in 40 years. TLT at levels last seen in 2011. 10Y real yield at highest since 2008.",
            "signal": "Extreme fear-driven selloff — bond market pricing in permanent higher rates. If Fed cuts (recession or inflation defeated), long bonds reprice dramatically.",
        },

        "p3_demand": True,
        "demand_type": "Monetary / Store-of-Value + Infrastructure Backing",
        "demand_detail": {
            "sovereign_backing": "Full faith and credit of US government",
            "flight_to_safety": "Treasuries rally in every recession — ultimate safe haven",
            "structural_demand": "Pension funds, insurance companies, foreign reserves — structural buyers at these yields",
        },

        "layers": {
            "L1_macro": {"signal": "supporting", "note": "Fed at peak rates — cutting cycle = bond bull. Yield curve still inverted → recession signal."},
            "L2_policy": {"signal": "supporting", "note": "Fiscal deficit $1.7T — but sovereign backing unchanged."},
            "L3_cost": {"signal": "neutral", "note": "No cost floor for bonds — valuation based on rate expectations"},
            "L4_supply_demand": {"signal": "neutral", "note": "Treasury issuance heavy but foreign buying steady"},
            "L5_hidden": {"signal": "supporting", "note": "Commercial bank treasury holdings at record → yield-hungry buyers"},
        },
        "layers_aligned": 3,
        "layers_contradicting": 0,
        "conviction": "High",

        "key_risks": [
            "Inflation re-accelerates → Fed hikes again → bonds fall further",
            "Fiscal concerns → term premium rises permanently",
            "Holding TLT requires patience — negative carry while waiting for cuts (coupon < short rates)",
        ],

        "recommendation": "Present to Founder",
        "recommendation_rationale": "3 layers aligned + Maximum discount depth. Largest bond bear market in 40 years = asymmetric payoff. Rate cutting cycle historically rewards long bonds. Key risk: timing — negative carry until Fed acts.",
    },
    {
        "id": "CS-004",
        "ticker": "COPPER",
        "name": "Copper (Physical Commodity)",
        "category": "Physical Commodities",
        "description": "Industrial metal — electrification, construction, EVs. Not an ETF; assessed as physical commodity exposure.",
        "current_price": 3.85,
        "currency": "USD/lb",

        "p1_eligible": True,
        "p1_rationale": "Physical commodity with intrinsic industrial utility. Cannot go to zero — even at cyclical lows, copper retains scrap/recycling value. Essential to modern economy.",

        "p2_discount": False,
        "discount_type": "None — above structural floor",
        "discount_depth": "None",
        "discount_detail": {
            "copper_price": 3.85,
            "avg_aisc": 2.50,
            "marginal_cost": 3.00,
            "signal": "Copper at $3.85 vs AISC $2.50 — profitable for all producers. NOT at discount. However, structural deficit narrative makes this worth monitoring for a fear-driven pullback.",
            "target_discount_entry": "$3.00 — at or below marginal cost where supply contraction begins.",
        },

        "p3_demand": True,
        "demand_type": "Industrial Consumption + Secular Trend",
        "demand_detail": {
            "electrification_demand": "EVs use 4x copper vs ICE. Grid modernization + renewables = massive incremental demand.",
            "supply_deficit": "Mine supply growing 1.5%/year, demand 3.5%/year → structural 500K ton deficit by 2026",
            "permitting": "New copper mine: 5-10 years from discovery to production. No quick supply response.",
            "inventories": "LME + COMEX + SHFE at 5-year lows",
        },

        "layers": {
            "L1_macro": {"signal": "supporting", "note": "Global PMI expanding, China stimulus → copper demand tailwind"},
            "L2_policy": {"signal": "supporting", "note": "IRA + EU Green Deal + China grid investment → electrification capex"},
            "L3_cost": {"signal": "contradicting", "note": "Price 54% above AISC — no cost floor, producers very profitable"},
            "L4_supply_demand": {"signal": "supporting", "note": "Structural deficit: supply 1.5% vs demand 3.5% growth"},
            "L5_hidden": {"signal": "supporting", "note": "China copper imports +15% YoY (stockpiling), LME inventories draining"},
        },
        "layers_aligned": 4,
        "layers_contradicting": 1,  # L3 cost: not at discount
        "conviction": "Low",

        "key_risks": [
            "China property crisis → copper demand shock (construction = 30% of demand)",
            "New mine approvals (Chile, Peru, DRC) flood supply",
            "Aluminum substitution in some applications",
        ],

        "recommendation": "Monitor — Wait for Better Price",
        "recommendation_rationale": "4 layers aligned but FAILS P2 (no discount). The thesis is intact — structural deficit + electrification demand. But entry requires a macro scare (Layer 1) pushing copper to $3.00 target. Currently ineligible for Radar — waitlisted.",
    },
    {
        "id": "CS-005",
        "ticker": "SLV",
        "name": "iShares Silver Trust",
        "category": "Physical Commodities (ETF)",
        "description": "Physical silver ETF — tracks spot silver price. Industrial + monetary dual demand.",
        "current_price": 22.10,
        "currency": "USD",

        "p1_eligible": True,
        "p1_rationale": "Physical silver trust — backed by allocated silver bars in vault. Intrinsic industrial + monetary value. Cannot go to zero.",

        "p2_discount": True,
        "discount_type": "Dislocation + Sentiment Divergence",
        "discount_depth": "Strong",
        "discount_detail": {
            "silver_price": 22.10,
            "gold_silver_ratio": 88,
            "historical_ratio_median": 65,
            "signal": "Gold/Silver ratio at 88:1 — extreme. Historically, ratios above 80 signal silver undervaluation vs gold. Silver has not participated in gold's rally. Paper market (COMEX futures) discounting while physical market tight.",
        },

        "p3_demand": True,
        "demand_type": "Industrial Consumption + Monetary",
        "demand_detail": {
            "solar_demand": "Silver in solar PV: +20% YoY (record). Each GW solar = 700K oz silver.",
            "electronics": "Silver in connectors, switches, relays — industrial consumption growing",
            "physical_premium": "US Mint silver Eagle sales +40% YoY, Indian imports at record",
            "supply": "Mine supply flat, recycling stagnant",
        },

        "layers": {
            "L1_macro": {"signal": "supporting", "note": "Gold rallying (L1 bullish), silver lags. Dollar weakening."},
            "L2_policy": {"signal": "supporting", "note": "Solar subsidies (IRA, EU, India) → silver demand structural"},
            "L3_cost": {"signal": "supporting", "note": "Silver AISC ~$14/oz — price well above cost. But gold/silver ratio extreme = relative discount."},
            "L4_supply_demand": {"signal": "supporting", "note": "4th consecutive annual deficit (2024E). Solar demand surge + flat supply."},
            "L5_hidden": {"signal": "supporting", "note": "Shanghai silver premium $2/oz over London. Indian imports record. Physical tight while paper weak."},
        },
        "layers_aligned": 5,
        "layers_contradicting": 0,
        "conviction": "High",

        "key_risks": [
            "Gold selloff drags silver down (silver = leveraged gold in downturns)",
            "Recession → industrial demand component drops",
            "High inventories in COMEX warehouses (paper market overhang)",
        ],

        "recommendation": "Present to Founder",
        "recommendation_rationale": "All 5 layers aligned — rare Maximum conviction candidate. P2: gold/silver ratio at 88:1 extreme + physical premium divergence. P3: solar demand structural + 4th year supply deficit. Hidden signals all confirm. This is the strongest signal in the V0 Radar.",
    },
]

# ═══════════════════════════════════════════════════════════════
# PIPELINE CONFIG
# ═══════════════════════════════════════════════════════════════

PIPELINE_CONFIG = {
    "pipeline_version": "v0.1.0",
    "name": "Close System Product Radar V0",
    "strategy": "Close System",
    "spec_ref": "CLOSE-SYSTEM-PRODUCT-RADAR.md (PD-v0.1, FD #39)",
}
