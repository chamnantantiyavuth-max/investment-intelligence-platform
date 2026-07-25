"""
Moat Classification System — §3.4.1
Per FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)

Classifies companies across 6 moat types + Width + Depth + Trend.
"""

MOAT_TYPES = [
    "Share of Mind",
    "Network Effect",
    "High Switching Cost",
    "Cost Advantage",
    "Intangible Assets",
    "Efficient Scale",
]

MOAT_WIDTHS = ["Wide", "Narrow", "None"]
MOAT_DEPTHS = ["Deep", "Moderate", "Shallow"]
MOAT_TRENDS = ["Stable", "Widening", "Narrowing"]


def classify_moat(company: dict) -> dict:
    """Classify a company's moat across all dimensions.

    Returns a structured moat assessment dict.
    """
    moat_types = company.get("moat_types", [])
    width = company.get("moat_width", "None")
    depth = company.get("moat_depth", "Shallow")
    trend = company.get("moat_trend", "Stable")

    # Validate width/depth against types
    if not moat_types:
        width = "None"
        depth = "Shallow"

    active_types = [t for t in moat_types if t.get("strength") not in ("Weak", None)]

    return {
        "types": moat_types,
        "active_count": len(active_types),
        "total_types": len(moat_types),
        "width": width,
        "depth": depth,
        "trend": trend,
        "types_summary": ", ".join(
            f"{t['type']} ({t['strength']})" for t in moat_types
        ),
    }


def moat_conviction_cap(moat: dict) -> str:
    """Determine max conviction based on moat width + depth.

    Per Moat × Conviction table (§3.4.1).
    """
    w, d = moat["width"], moat["depth"]

    if w == "Wide" and d == "Deep":
        return "Maximum"
    elif (w == "Wide" and d in ("Moderate", "Shallow")) or (w == "Narrow" and d == "Deep"):
        return "High"
    elif w == "Narrow" and d in ("Moderate", "Shallow"):
        return "Moderate"
    else:
        return "Moderate"  # None moat = extraordinary earnings required


def moat_strength_score(moat: dict) -> int:
    """Aggregate moat strength into a numeric score for comparisons.

    0-100 scale. Not used for decisions — informational only.
    """
    base = {"Wide": 60, "Narrow": 30, "None": 0}.get(moat["width"], 0)
    depth_bonus = {"Deep": 20, "Moderate": 10, "Shallow": 0}.get(moat["depth"], 0)
    trend_bonus = {"Widening": 10, "Stable": 5, "Narrowing": -10}.get(moat["trend"], 0)
    type_bonus = min(moat["active_count"] * 5, 15)

    return min(max(base + depth_bonus + trend_bonus + type_bonus, 0), 100)


def moat_narrative(moat: dict) -> str:
    """Generate a one-paragraph moat narrative."""
    if moat["width"] == "None":
        return "No structural competitive advantage identified. The company competes on price, features, or operational efficiency without a defendable moat."

    parts = []
    if moat["width"] == "Wide":
        parts.append(f"Wide moat ({moat['depth']} depth) — {moat['active_count']} active moat type(s) providing structural competitive advantage.")
    else:
        parts.append(f"Narrow moat ({moat['depth']} depth) — limited competitive advantage scope.")

    parts.append(f"Moat trend: {moat['trend'].lower()}.")
    parts.append(f"Types: {moat['types_summary']}.")

    return " ".join(parts)
