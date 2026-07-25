"""
Earnings Quality Dimension — §3.5.1
Per FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)

Assesses earnings quality as an explicit dimension (HIGH/MEDIUM/LOW/COSMETIC).
"""

QUALITY_RATINGS = ["HIGH", "MEDIUM", "LOW", "COSMETIC"]


def assess_earnings_quality(company: dict) -> dict:
    """Assess earnings quality from the latest reported quarter.

    Returns a structured quality assessment with rating + detailed breakdown.
    """
    revenue_q = company.get("revenue_quality", "MEDIUM")
    margin_q = company.get("margin_quality", "MEDIUM")
    fcf_conv = company.get("fcf_conversion", 1.0)
    one_time = company.get("one_time_items", False)
    buyback_impact = company.get("share_buyback_impact_pct", 0.0)
    surprise_dir = company.get("surprise_direction", "Meet")
    guidance_dir = company.get("guidance_direction", "Unchanged")

    # ── Determine quality rating ──
    rating = _determine_rating(revenue_q, margin_q, fcf_conv, one_time, buyback_impact,
                                surprise_dir, guidance_dir)

    # ── Conviction impact ──
    conviction_impact = {
        "HIGH": "Strengthens thesis",
        "MEDIUM": "Neutral — wait for next quarter",
        "LOW": "Weakens thesis",
        "COSMETIC": "Red flag — investigate before acting on numbers",
    }.get(rating, "Neutral")

    return {
        "rating": rating,
        "conviction_impact": conviction_impact,
        "surprise_direction": surprise_dir,
        "surprise_magnitude_pct": company.get("surprise_magnitude_pct", 0),
        "revenue_quality": revenue_q,
        "margin_quality": margin_q,
        "fcf_conversion": fcf_conv,
        "one_time_items": one_time,
        "share_buyback_impact_pct": buyback_impact,
        "guidance_direction": guidance_dir,
        "guidance_reason": company.get("guidance_reason", ""),
        "narrative": _build_narrative(rating, company),
    }


def _determine_rating(revenue_q, margin_q, fcf_conv, one_time, buyback_impact,
                      surprise_dir, guidance_dir):
    """Determine overall quality rating from component signals."""
    # Cosmetic: beat but revenue declining OR buybacks masking decline OR one-time gains
    if surprise_dir == "Beat":
        if revenue_q == "LOW" and buyback_impact >= 2.0:
            return "COSMETIC"
        if one_time and revenue_q == "LOW":
            return "COSMETIC"
        if one_time and buyback_impact >= 3.0:
            return "COSMETIC"

    # Low: declining revenue, low margins, low FCF conversion
    if revenue_q == "LOW" and fcf_conv < 0.5:
        return "LOW"
    if margin_q == "LOW" and guidance_dir == "Lowered":
        return "LOW"

    # High: all signals positive
    if revenue_q == "HIGH" and margin_q in ("HIGH", "MEDIUM") and fcf_conv >= 0.8 and not one_time and buyback_impact < 2.0:
        if guidance_dir in ("Raised", "Maintained"):
            return "HIGH"

    # Default: medium
    return "MEDIUM"


def _build_narrative(rating, company):
    """Generate human-readable earnings quality narrative."""
    name = company.get("name", company.get("id", "?"))
    surprise = company.get("surprise_direction", "Meet")
    mag = company.get("surprise_magnitude_pct", 0)

    templates = {
        "HIGH": f"{name} delivered high-quality earnings: {surprise.lower()} by {abs(mag):.1f}%, driven by organic revenue growth with strong FCF conversion and no one-time distortions.",
        "MEDIUM": f"{name} reported mixed-quality earnings: {surprise.lower()} by {abs(mag):.1f}%, but with some reliance on financial engineering alongside organic growth.",
        "LOW": f"{name}'s earnings quality is low: {surprise.lower()} by {abs(mag):.1f}% but revenue is declining and margins are under pressure. Cash conversion is weak.",
        "COSMETIC": f"{name}'s reported beat is COSMETIC: {surprise.lower()} by {abs(mag):.1f}% but underlying revenue is declining. The beat is driven by share buybacks and/or one-time items — not operational strength.",
    }
    return templates.get(rating, templates["MEDIUM"])
