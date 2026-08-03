"""
Fundamental & Opportunity V0 Pipeline — 6-Stage
Per FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)

Stages:
  S1: Macro Analysis — regime classification + sector implications
  S2: Industry Analysis — sector health + competitive dynamics
  S3: Product Analysis — investability check (bridge to Close System)
  S4: Company Analysis — moat classification + financial quality
  S5: Earnings & Change — earnings quality + thesis impact
  S6: Valuation Context — value trap detection + cheap vs history

Spike version — simplified for V0 concept validation.
"""

from datetime import datetime
from fixtures import FIXTURES, MACRO_REGIME
from moat import classify_moat, moat_conviction_cap, moat_strength_score, moat_narrative
from earnings_quality import assess_earnings_quality
from value_trap import is_unusually_cheap, run_value_trap_check, run_profit_rate_trend
from narrative_gap import run_narrative_gap


def run_pipeline(companies: list[dict] = None, mode: str = "synthetic") -> list[dict]:
    """Run the full 6-stage Fundamental & Opportunity pipeline.

    Args:
        companies: Optional list of company dicts. If None, uses FIXTURES.
        mode: "synthetic" (default, backward-compatible) or "real" (yfinance).
            Propagated to evidence generation so real runs never claim
            "synthetic fixture" (arch v0.4 §3, FD #46 provenance).

    Returns a list of Research Packages, one per company.
    """
    source = companies if companies is not None else FIXTURES
    packages = []
    for company in source:
        pkg = build_research_package(company, mode=mode)
        packages.append(pkg)
    return packages


def build_research_package(company: dict, mode: str = "synthetic") -> dict:
    """Build a complete 13-section Research Package for one company.

    Gracefully handles missing fields — uses defaults rather than crashing.
    """
    tid = company.get("id", "UNKNOWN")
    name = company.get("name", tid)

    # ── S1: Macro Analysis ──
    macro = {
        "regime": MACRO_REGIME["regime"],
        "gdp_growth": MACRO_REGIME["gdp_growth"],
        "inflation": MACRO_REGIME["inflation"],
        "fed_funds": MACRO_REGIME["fed_funds"],
        "sector_implication": MACRO_REGIME["sector_implications"].get(
            company.get("sector", ""), "Not assessed"
        ),
    }

    # ── S2: Industry Analysis ──
    industry = {
        "sector": company.get("sector", "Unknown"),
        "industry": company.get("industry", "Unknown"),
        "position": _industry_position(company),
    }

    # ── S3: Product Analysis ──
    product = {
        "type": "Common Stock",
        "exchange": "NASDAQ" if company.get("sector") == "Technology" else "NYSE",
        "liquidity": "HIGH" if company.get("market_cap", 0) > 100 else "MODERATE",
        "options_available": True,
    }

    # ── S4: Company Analysis (CORE) ──
    moat = classify_moat(company)
    financial_quality = {
        "gross_margin": company.get("gross_margin", 0),
        "operating_margin": company.get("operating_margin", 0),
        "fcf_conversion": company.get("fcf_conversion", 1.0),
        "debt_to_equity": company.get("debt_to_equity", 0),
        "roe": company.get("roe", 0),
        "revenue_growth_3y": company.get("revenue_growth_3y", 0),
    }
    capital_allocation = _assess_capital_allocation(company)
    management = {
        "ceo_tenure_years": company.get("ceo_tenure_years", 0),
        "credibility": company.get("management_credibility", "UNKNOWN"),
        "insider_activity": company.get("insider_activity", ""),
        "cfo_turnover_3y": company.get("cfo_turnover_3y", 0),
    }
    conviction_cap = moat_conviction_cap(moat)

    # ── S5: Earnings & Change ──
    earnings_quality = assess_earnings_quality(company)
    thesis_impact = _determine_thesis_impact(earnings_quality, moat)

    # ── S6: Valuation Context ──
    valuation = {
        "pe_ttm": company.get("pe_ttm"),
        "pe_5y_avg": company.get("pe_5y_avg"),
        "pe_10y_avg": company.get("pe_10y_avg"),
        "ev_ebitda": company.get("ev_ebitda"),
        "ev_ebitda_industry": company.get("ev_ebitda_industry"),
        "fcf_yield": company.get("fcf_yield"),
        "scenario_bull": company.get("scenario_bull"),
        "scenario_base": company.get("scenario_base"),
        "scenario_bear": company.get("scenario_bear"),
        "current_price": company.get("current_price"),
    }
    unusually_cheap = is_unusually_cheap(company)
    value_trap = run_value_trap_check(company, moat) if unusually_cheap else {"triggered": False}
    profit_rate_trend = run_profit_rate_trend(company)
    narrative_gap = run_narrative_gap(company)

    # ── Key Risks ──
    key_risks = _identify_key_risks(company, moat, earnings_quality)

    # ── Open Questions ──
    open_questions = _identify_open_questions(company, moat, earnings_quality)

    # ── Assemble Package ──
    return {
        "id": tid,
        "name": company["name"],
        "generated_at": datetime.now().isoformat(),
        "spec_ref": "FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1",
        # 13 sections
        "thesis_summary": _build_thesis_summary(company, moat),
        "thesis_lifecycle": "Confirmed" if moat["width"] != "None" else "Under Review",
        "conviction": _assign_conviction(conviction_cap, earnings_quality, moat),
        "macro_context": macro,
        "industry_assessment": industry,
        "company_assessment": {
            "moat": moat,
            "financial_quality": financial_quality,
            "capital_allocation": capital_allocation,
            "management": management,
            "conviction_cap": conviction_cap,
            "moat_narrative": moat_narrative(moat),
            "moat_score": moat_strength_score(moat),
        },
        "earnings_trajectory": earnings_quality,
        "valuation_context": {
            **valuation,
            "unusually_cheap": unusually_cheap,
            "value_trap": value_trap,
            "profit_rate_trend": profit_rate_trend,
            "narrative_gap": narrative_gap,
        },
        "key_risks": key_risks,
        "independent_challenge": _independent_challenge(company, moat, earnings_quality),
        "supporting_evidence": _supporting_evidence(company, mode),
        "contradicting_evidence": _contradicting_evidence(company, moat),
        "open_questions": open_questions,
    }


# ── Helper functions ──

def _industry_position(company: dict) -> str:
    sector = company.get("sector", "")
    margin = company.get("operating_margin", 0)
    if margin > 0.25:
        return "Leader"
    elif margin > 0.10:
        return "Strong"
    return "Challenged"


def _assess_capital_allocation(company: dict) -> dict:
    fcf_conv = company.get("fcf_conversion", 1.0)
    roe = company.get("roe", 0)
    return {
        "quality": "GOOD" if fcf_conv > 0.8 and roe > 0.12 else "WATCH",
        "fcf_available": fcf_conv > 0.8,
        "roe_adequate": roe > 0.12,
        "buyback_impact": company.get("share_buyback_impact_pct", 0),
    }


def _assign_conviction(conviction_cap: str, eq: dict, moat: dict) -> dict:
    """Assign conviction moderated by earnings quality and moat trend."""
    levels = ["Maximum", "High", "Moderate", "Low"]
    cap_idx = levels.index(conviction_cap) if conviction_cap in levels else 2

    # Downgrade for low earnings quality
    if eq.get("rating") in ("LOW", "COSMETIC"):
        cap_idx = min(cap_idx + 1, 3)
    # Downgrade for narrowing moat
    if moat.get("trend") == "Narrowing":
        cap_idx = min(cap_idx + 1, 3)
    # Upgrade for widening moat
    if moat.get("trend") == "Widening" and cap_idx > 0:
        cap_idx = max(cap_idx - 1, 0)

    final = levels[cap_idx]
    rationale = _conviction_rationale(company=None, moat=moat, eq=eq, final=final)
    return {"level": final, "cap": conviction_cap, "rationale": rationale}


def _conviction_rationale(company, moat, eq, final):
    parts = [f"Moat cap: {moat_conviction_cap(moat)}."]
    if eq.get("rating") in ("LOW", "COSMETIC"):
        parts.append(f"Downgraded: earnings quality is {eq['rating']}.")
    if moat.get("trend") == "Narrowing":
        parts.append("Downgraded: moat narrowing.")
    if moat.get("trend") == "Widening":
        parts.append("Upgraded: moat widening.")
    return " ".join(parts)


def _determine_thesis_impact(eq: dict, moat: dict) -> str:
    if eq.get("rating") == "COSMETIC":
        return "Weakens"
    if eq.get("rating") == "LOW" and moat.get("trend") == "Narrowing":
        return "Weakens"
    if eq.get("rating") == "HIGH":
        return "Confirms"
    return "Insufficient"


def _build_thesis_summary(company: dict, moat: dict) -> str:
    name = company["name"]
    if moat["width"] == "None":
        return f"{name} lacks a structural moat. Investment case depends entirely on earnings growth and valuation mean-reversion. High risk of value trap."
    return (f"{name} possesses a {moat['width'].lower()} moat ({moat['depth'].lower()} depth) "
            f"built on {moat['active_count']} structural advantage(s): {moat['types_summary']}. "
            f"Moat trend: {moat['trend'].lower()}.")


def _identify_key_risks(company, moat, eq):
    risks = []
    if moat.get("trend") == "Narrowing":
        risks.append("Moat erosion — competitive advantage weakening over time")
    if eq.get("rating") in ("LOW", "COSMETIC"):
        risks.append("Earnings quality concerns — reported numbers may overstate economic reality")
    if company.get("debt_to_equity", 0) > 1.0:
        risks.append("Elevated leverage — balance sheet risk in downturn")
    if company.get("cfo_turnover_3y", 0) >= 2:
        risks.append("Management instability — high CFO turnover signals potential issues")
    if not risks:
        risks.append("No material risks identified from available data")
    return risks


def _identify_open_questions(company, moat, eq):
    qs = []
    if moat.get("trend") == "Narrowing":
        qs.append("At what point does moat narrowing trigger thesis invalidation?")
    if eq.get("rating") == "MEDIUM":
        qs.append("Will next quarter confirm improving or deteriorating earnings quality trend?")
    if company.get("pe_ttm", 0) < company.get("pe_5y_avg", 0) * 0.6:
        qs.append("Is the discount vs history a buying opportunity or a warning? Refer to Value Trap Detector.")
    if not qs:
        qs.append("What catalyst would accelerate or threaten the current thesis trajectory?")
    return qs


def _independent_challenge(company, moat, eq):
    """Generate independent challenge (8 domains per §4.2)."""
    challenges = []

    # 1. Contradictory Evidence
    if moat.get("trend") == "Narrowing":
        challenges.append("Moat narrowing contradicts thesis of durable competitive advantage.")

    # 2. Fragile Assumptions
    if company.get("revenue_growth_3y", 0) < 0.05:
        challenges.append("Thesis assumes growth — but 3Y CAGR below 5% makes this assumption fragile.")

    # 3. Accounting Quality
    if eq.get("rating") in ("LOW", "COSMETIC"):
        challenges.append(f"Earnings quality rated {eq['rating']} — accounting may be masking operational decline.")

    # 4. Concentration Risk
    if company.get("id") == "CRM":
        challenges.append("Revenue concentrated in enterprise SaaS — macro slowdown impacts renewal rates.")

    # 5. Cyclicality Mispricing
    if company.get("id") == "INTC":
        challenges.append("Semiconductor cycle risk — current trough may be mistaken for permanent decline OR current recovery overestimated.")

    # 6. Management Credibility
    if company.get("management_credibility") == "LOW":
        challenges.append("Low management credibility — missed targets, high turnover undermine thesis assumptions.")

    # 7. Alternative Explanations
    if company.get("id") == "COST":
        challenges.append("Membership growth may be driven by inflation-era consumer behavior, not durable preference.")

    # 8. Balance Sheet Stress
    if company.get("debt_to_equity", 0) > 1.0:
        challenges.append(f"Debt/Equity {company['debt_to_equity']:.1f}x — refinancing risk if rates stay elevated.")

    return challenges if challenges else ["No material challenge identified — thesis has not been stress-tested."]


def _supporting_evidence(company, mode: str = "synthetic"):
    evidence = []
    if mode != "real":
        evidence.append(f"Financial data: synthetic fixture for {company['id']} (V0 testing only)")
    if company.get("moat_types"):
        evidence.append(f"Moat evidence: {company['moat_types'][0]['evidence']}")
    return evidence


def _contradicting_evidence(company, moat):
    evidence = []
    if moat.get("trend") == "Narrowing":
        evidence.append(f"Moat trend is {moat['trend'].lower()} — this contradicts thesis durability.")
    if company.get("surprise_direction") == "Miss":
        evidence.append(f"Latest earnings missed consensus by {abs(company.get('surprise_magnitude_pct', 0)):.1f}%.")
    return evidence if evidence else ["No contradicting evidence identified from available data."]
