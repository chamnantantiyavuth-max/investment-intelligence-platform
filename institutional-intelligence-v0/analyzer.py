"""
Institutional Intelligence V0 — Analyzer
Concentration Ratio → Conviction mapping + Action Detection.

FD #42 · Phase 10 · 26 July 2026
"""

# ── Concentration → Conviction ──

CONVICTION_THRESHOLDS = [
    (20.0, "Maximum",  "Dominant position — fund has extreme conviction in this name."),
    (10.0, "High",     "Major position — significant conviction, likely a top-5 holding."),
    (5.0,  "Moderate", "Meaningful position — conviction above passive allocation."),
    (1.0,  "Low",      "Small position — monitoring or building, low conviction."),
    (0.0,  "Minimal",  "Minimal position — likely tracking/optionality, not conviction."),
]


def concentration_to_conviction(pct_of_portfolio: float) -> dict:
    """Map concentration % to conviction level + rationale."""
    for threshold, level, rationale in CONVICTION_THRESHOLDS:
        if pct_of_portfolio >= threshold:
            return {"level": level, "rationale": rationale}
    return {"level": "Minimal", "rationale": CONVICTION_THRESHOLDS[-1][2]}


# ── Action Detection ──

def detect_action(current_pct: float, previous_pct: float | None, is_baseline: bool = False) -> dict:
    """Compare current vs previous quarter to determine action.

    Args:
        current_pct: Current quarter position % of portfolio.
        previous_pct: Previous quarter position % (None if no prior data).
        is_baseline: True if this is the oldest available quarter (no prior data exists).

    Returns:
        Action dict with type + detail.
    """
    if previous_pct is None:
        if is_baseline:
            return {"action": "BASELINE", "detail": "Oldest available filing — no prior quarter for comparison.", "change_pct": 0.0}
        return {"action": "NEW", "detail": "New position — not present in prior quarter.", "change_pct": 100.0}

    if current_pct == 0 and previous_pct > 0:
        return {"action": "EXIT", "detail": "Position closed — fully exited.", "change_pct": -100.0}

    change = ((current_pct - previous_pct) / previous_pct) * 100 if previous_pct > 0 else 0

    if change > 50:
        return {"action": "ADD", "detail": f"Significantly increased — +{change:.0f}% position size.", "change_pct": round(change, 1)}
    elif change > 10:
        return {"action": "ADD", "detail": f"Increased position — +{change:.0f}% vs prior quarter.", "change_pct": round(change, 1)}
    elif change < -50:
        return {"action": "REDUCE", "detail": f"Significantly reduced — {change:.0f}% position size.", "change_pct": round(change, 1)}
    elif change < -10:
        return {"action": "REDUCE", "detail": f"Reduced position — {change:.0f}% vs prior quarter.", "change_pct": round(change, 1)}
    else:
        return {"action": "MAINTAIN", "detail": f"Position maintained — {change:+.0f}% change vs prior quarter.", "change_pct": round(change, 1)}


# ── Sector Rotation Detection (Phase 10.5+) ──

def detect_sector_flows(filings: list[dict], ticker_sector_map: dict[str, str] = None) -> dict:
    """Detect sector-level institutional flows across all tracked funds.

    Placeholder for Phase 10.5 — requires real ticker → sector mapping.
    """
    if not ticker_sector_map:
        return {"status": "Not available in V1 — requires sector mapping data."}

    # Aggregate flows by sector
    sector_flows: dict[str, dict] = {}
    for filing in filings:
        for h in filing.get("holdings", []):
            t = h["ticker"]
            sec = ticker_sector_map.get(t, "Unknown")
            if sec not in sector_flows:
                sector_flows[sec] = {"inflow": 0, "outflow": 0, "tickers": set()}
            if h.get("action") == "NEW" or h.get("action") == "ADD":
                sector_flows[sec]["inflow"] += h["pct_of_portfolio"]
            elif h.get("action") == "REDUCE" or h.get("action") == "EXIT":
                sector_flows[sec]["outflow"] += h["pct_of_portfolio"]
            sector_flows[sec]["tickers"].add(t)

    return sector_flows
