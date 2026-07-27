"""
Narrative vs Reality Gap Detector — FD #43
Per Founder Decision #43 (28 July 2026)

Measures the divergence between Market Cap (narrative-driven) and
Fair Value (fundamentals-based, weighted from scenario analysis).
Signals are informational only — never alter rankings or scores.
"""


def compute_fair_value(company: dict) -> float:
    """Compute weighted fair value from scenario analysis.

    Weights: Bull 20% + Base 60% + Bear 20%.
    Fair Value = weighted_avg_price * implied_shares
    where implied_shares = market_cap / current_price.
    """
    market_cap = company.get("market_cap", 0)
    current_price = company.get("current_price", 0)
    bull = company.get("scenario_bull", current_price)
    base = company.get("scenario_base", current_price)
    bear = company.get("scenario_bear", current_price)

    if current_price == 0 or market_cap == 0:
        return 0

    # Weighted average price
    weighted_price = (bull * 0.20) + (base * 0.60) + (bear * 0.20)

    # Implied shares outstanding
    implied_shares = market_cap / current_price

    return weighted_price * implied_shares


def run_narrative_gap(company: dict) -> dict:
    """Compute narrative vs reality gap.

    Gap Ratio = Market Cap / Fair Value.
    - gap > 2.0  -> BUBBLE_RISK (market cap driven by narrative, not fundamentals)
    - gap < 0.5  -> UNDERVALUED (market ignoring fundamentals)
    - 0.5-2.0    -> FAIR (narrative and fundamentals roughly aligned)
    """
    name = company.get("name", company.get("id", "?"))
    market_cap = company.get("market_cap", 0)
    fair_value = compute_fair_value(company)

    if fair_value == 0:
        return {
            "triggered": False,
            "gap_ratio": None,
            "verdict": "INSUFFICIENT_DATA",
            "detail": "Fair value cannot be computed — missing scenario data.",
        }

    gap_ratio = market_cap / fair_value

    if gap_ratio > 2.0:
        verdict = "BUBBLE_RISK"
        detail = (
            f"🔴 Narrative Premium: {name} market cap ${market_cap:.0f}B is "
            f"{gap_ratio:.1f}x fair value (${fair_value:.0f}B). "
            f"The market is pricing a story that fundamentals don't support. "
            f"Bull scenario: ${company.get('scenario_bull', 0):.0f}, "
            f"Base: ${company.get('scenario_base', 0):.0f}, "
            f"Bear: ${company.get('scenario_bear', 0):.0f}."
        )
    elif gap_ratio < 0.5:
        verdict = "UNDERVALUED"
        detail = (
            f"🟢 Narrative Discount: {name} market cap ${market_cap:.0f}B is "
            f"only {gap_ratio:.1f}x fair value (${fair_value:.0f}B). "
            f"Market is ignoring fundamentals — potential opportunity "
            f"if thesis is intact and no structural problems exist."
        )
    elif gap_ratio > 1.5:
        verdict = "ELEVATED"
        detail = (
            f"🟡 Narrative Stretch: {name} trades at {gap_ratio:.1f}x "
            f"fair value. Not yet bubble territory but narrative is "
            f"running ahead of fundamentals. Monitor for reversion risk."
        )
    else:
        verdict = "FAIR"
        detail = (
            f"✅ Fairly Priced: {name} market cap ${market_cap:.0f}B at "
            f"{gap_ratio:.1f}x fair value (${fair_value:.0f}B). "
            f"Narrative and fundamentals are roughly aligned."
        )

    return {
        "triggered": gap_ratio > 2.0 or gap_ratio < 0.5,
        "gap_ratio": round(gap_ratio, 2),
        "verdict": verdict,
        "market_cap": market_cap,
        "fair_value": round(fair_value, 1),
        "weighted_price": round((company.get("scenario_bull", 0) * 0.20 +
                                 company.get("scenario_base", 0) * 0.60 +
                                 company.get("scenario_bear", 0) * 0.20), 1),
        "detail": detail,
    }
