"""
Institutional Intelligence V0 — Pipeline
6-stage: Load → Match → Detect → Score → Rank → Output

Dual-mode: synthetic fixtures (default) or real 13F data (--real flag).
FD #42 · Phase 10 + 10.5 · 26 July 2026
"""

from collections import defaultdict
from fixtures import FIXTURES
from analyzer import (
    concentration_to_conviction,
    detect_action,
    score_signal,
    detect_sector_flows,
)
from cusip_mapper import enrich_holdings


def run_pipeline(filings: list[dict] = None) -> dict:
    """Run the full Institutional Intelligence pipeline.

    Args:
        filings: Optional list of 13F filing dicts. If None, uses FIXTURES.

    Returns:
        {
            "signals": list[InstitutionalSignal],
            "summary": {fund_stats, ticker_stats, sector_flows},
            "meta": {version, generated_at},
        }
    """
    source = filings if filings is not None else FIXTURES
    if not source:
        return {"signals": [], "summary": {}, "meta": {"version": "v0.1.0", "error": "No data"}}

    # Enrich holdings with ticker mapping (for real 13F data which has CUSIP but no ticker)
    for filing in source:
        if filing.get("holdings") and filing["holdings"] and "ticker" not in filing["holdings"][0]:
            filing["holdings"] = enrich_holdings(filing["holdings"])
        # Ensure all holdings have ticker
        for h in filing.get("holdings", []):
            if "ticker" not in h:
                h["ticker"] = h.get("cusip", "UNKNOWN")

    # ── Group filings by fund CIK + quarter ──
    filing_map: dict[str, dict] = {}  # key: cik_quarter
    for f in source:
        key = f"{f['filer_cik']}_{f['filing_quarter']}"
        filing_map[key] = f

    # ── For each fund, find prior quarter for action detection ──
    signals = []
    fund_stats = defaultdict(lambda: {"filings": 0, "total_positions": 0, "top_conviction": "Minimal"})
    ticker_stats = defaultdict(lambda: {
        "total_funds": 0, "total_conviction_score": 0,
        "buying_funds": 0, "selling_funds": 0,
        "aggregate_conviction": "Minimal",
    })

    for filing in source:
        cik = filing["filer_cik"]
        quarter = filing["filing_quarter"]
        fund_name = filing["filer_name"]

        # Find prior quarter filing
        prev_q = _previous_quarter(quarter)
        prev_key = f"{cik}_{prev_q}"
        prev_filing = filing_map.get(prev_key)
        prev_holdings = {h["ticker"]: h for h in prev_filing["holdings"]} if prev_filing else {}

        # Analyze each holding
        for h in filing["holdings"]:
            ticker = h["ticker"]
            pct = h["pct_of_portfolio"]

            # Conviction from concentration
            conviction = concentration_to_conviction(pct)

            # Action vs prior quarter
            prev_h = prev_holdings.get(ticker)
            prev_pct = prev_h["pct_of_portfolio"] if prev_h else None
            is_baseline = prev_filing is None  # Oldest quarter — no prior data
            action = detect_action(pct, prev_pct, is_baseline=is_baseline)

            # Signal score
            s = score_signal(pct, action["action"], conviction["level"])

            signal = {
                "filer_name": fund_name,
                "filer_cik": cik,
                "filer_category": _get_category(cik),
                "ticker": ticker,
                "filing_quarter": quarter,
                "report_date": filing["report_date"],
                "pct_of_portfolio": pct,
                "conviction": conviction["level"],
                "conviction_rationale": conviction["rationale"],
                "action": action["action"],
                "action_detail": action["detail"],
                "change_pct": action.get("change_pct", 0),
                "signal_score": s,
                "value_usd": h.get("value_usd", 0),
            }
            signals.append(signal)

            # Update stats
            fund_stats[cik]["filings"] += 1
            fund_stats[cik]["name"] = fund_name
            fund_stats[cik]["total_positions"] = filing.get("total_positions", 0)

            ts = ticker_stats[ticker]
            ts["total_funds"] += 1
            ts["total_conviction_score"] += s
            if action["action"] in ("NEW", "ADD"):
                ts["buying_funds"] += 1
            elif action["action"] in ("REDUCE", "EXIT"):
                ts["selling_funds"] += 1

    # Aggregate ticker conviction
    for ticker, ts in ticker_stats.items():
        avg_score = ts["total_conviction_score"] / max(ts["total_funds"], 1)
        ts["aggregate_conviction"] = _score_to_conviction(avg_score)

    # Sort signals by score descending
    signals.sort(key=lambda x: x["signal_score"], reverse=True)

    # Sector flow detection (V1 — no sector map, returns placeholder)
    sector_flows = detect_sector_flows(source)

    from datetime import datetime
    return {
        "signals": signals,
        "summary": {
            "total_funds_tracked": len(set(s["filer_cik"] for s in signals)),
            "total_signals": len(signals),
            "total_filings": len(source),
            "fund_stats": dict(fund_stats),
            "ticker_stats": dict(ticker_stats),
            "sector_flows": sector_flows,
            "top_signals": signals[:10],  # Top 10 by signal score
        },
        "meta": {
            "version": "v0.1.0",
            "spec_ref": "FD #42 · Phase 10",
            "generated_at": datetime.now().isoformat(),
            "data_source": "SYNTHETIC" if filings is None else "REAL 13F",
            "latency_note": "13F data has ~45-day lag from quarter end. Signals are informational — not trading triggers.",
        },
    }


def query_signals_by_ticker(ticker: str, signals: list[dict]) -> list[dict]:
    """Filter signals for a specific ticker, sorted by score."""
    return sorted([s for s in signals if s["ticker"].upper() == ticker.upper()],
                  key=lambda x: x["signal_score"], reverse=True)


def query_signals_by_fund(cik: str, signals: list[dict]) -> list[dict]:
    """Filter signals for a specific fund CIK, sorted by score."""
    return sorted([s for s in signals if s["filer_cik"] == cik],
                  key=lambda x: x["signal_score"], reverse=True)


def query_top_conviction(signals: list[dict], min_conviction: str = "High") -> list[dict]:
    """Return signals with conviction >= threshold."""
    levels = ["Maximum", "High", "Moderate", "Low", "Minimal"]
    threshold_idx = levels.index(min_conviction) if min_conviction in levels else 2
    return [s for s in signals
            if levels.index(s["conviction"]) <= threshold_idx]


# ── Helpers ──

def _previous_quarter(q: str) -> str:
    """Compute the previous quarter string. E.g., '2026Q1' → '2025Q4'."""
    parts = q.split("Q")
    year, quarter = int(parts[0]), int(parts[1])
    if quarter == 1:
        return f"{year - 1}Q4"
    return f"{year}Q{quarter - 1}"


def _get_category(cik: str) -> str:
    """Look up fund category from watchlist. Falls back to 'Unknown'."""
    from watchlist import get_fund
    fund = get_fund(cik=cik)
    return fund["category"] if fund else "Unknown"


def _score_to_conviction(avg_score: float) -> str:
    """Convert average signal score back to conviction label."""
    if avg_score >= 80:
        return "Maximum"
    elif avg_score >= 60:
        return "High"
    elif avg_score >= 35:
        return "Moderate"
    elif avg_score >= 15:
        return "Low"
    return "Minimal"
