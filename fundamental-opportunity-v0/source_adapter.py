"""
Fundamental & Opportunity V0 — Real Data Source Adapter
Fetches fundamental + price data via yfinance.
Caches to local JSON. Normalizes output for pipeline consumption.

Usage: python source_adapter.py                 # fetch + cache all tickers
       python source_adapter.py --refresh       # force re-fetch
       python source_adapter.py --summary       # show cache summary

NOT LIVE TRADING DATA — FOR V0 DEVELOPMENT ONLY.
Phase 9 · FD #41 · 26 July 2026
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

import yfinance as yf

CACHE_DIR = Path(__file__).parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Tickers for FO V0.1 — parity with synthetic fixtures (8 companies)
FO_TICKERS = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "JNJ"]


def _cache_path(ticker: str) -> Path:
    return CACHE_DIR / f"{ticker}.json"


def _load_cache(ticker: str, max_age_hours: int = 24) -> dict | None:
    """Load cached data if fresh enough. Returns None if stale or missing."""
    path = _cache_path(ticker)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    fetched = datetime.fromisoformat(data.get("_fetched_at", "2000-01-01"))
    age = (datetime.now() - fetched).total_seconds() / 3600
    if age > max_age_hours:
        return None
    return data


def _save_cache(ticker: str, data: dict):
    data["_fetched_at"] = datetime.now().isoformat()
    _cache_path(ticker).write_text(
        json.dumps(data, indent=2, default=str), encoding="utf-8"
    )


def _safe_float(value, default=0.0) -> float:
    """Coerce to float, returning default on None/NaN/inf."""
    if value is None:
        return default
    try:
        f = float(value)
        if f != f or f in (float("inf"), float("-inf")):  # NaN / inf check
            return default
        return f
    except (ValueError, TypeError):
        return default


def _market_cap_billions(info: dict) -> float:
    """Extract market cap in billions USD."""
    raw = info.get("marketCap")
    if raw is None:
        return 0.0
    return round(_safe_float(raw) / 1e9, 1)


def fetch_fundamental_data(ticker: str, force_refresh: bool = False) -> dict:
    """Fetch yfinance data for one ticker → pipeline-compatible company dict.

    Fields yfinance CAN provide are populated. Analyst-assessment fields
    (moat, management, earnings surprises, guidance) are set to None —
    the pipeline handles them gracefully via defaults.
    """
    if not force_refresh:
        cached = _load_cache(ticker)
        if cached:
            return cached

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    # ── Price data ──
    hist = stock.history(period="1y")
    prices = None
    if not hist.empty:
        last = hist.iloc[-1]
        prices = {
            "close": round(float(last["Close"]), 2),
            "open": round(float(last["Open"]), 2),
            "high": round(float(last["High"]), 2),
            "low": round(float(last["Low"]), 2),
            "volume": int(last["Volume"]),
            "as_of": str(hist.index[-1].date()),
        }

    current_price = (
        prices["close"] if prices else _safe_float(info.get("currentPrice"))
    )

    # ── Financial ratios (from yfinance info) ──
    gross_margin = _safe_float(info.get("grossMargins"), 0.0)
    operating_margin = _safe_float(info.get("operatingMargins"), 0.0)
    roe = _safe_float(info.get("returnOnEquity"), 0.0)
    debt_to_equity_raw = _safe_float(info.get("debtToEquity"), 0.0)
    # yfinance returns debtToEquity as percentage (e.g. 79.5 = 79.5% → 0.795 ratio)
    # but some tickers may return it as a ratio. Heuristic: if > 10, assume percentage.
    debt_to_equity = debt_to_equity_raw / 100.0 if debt_to_equity_raw > 10 else debt_to_equity_raw
    pe_ttm = _safe_float(info.get("trailingPE"), 0.0)
    ev_ebitda = _safe_float(info.get("enterpriseToEbitda"), 0.0)
    eps = _safe_float(info.get("trailingEps"), 0.0)
    revenue_growth = _safe_float(info.get("revenueGrowth"), 0.0)

    # FCF yield: freeCashflow per share / price
    fcf = _safe_float(info.get("freeCashflow"), 0.0)
    shares_outstanding = _safe_float(info.get("sharesOutstanding"), 0.0)
    fcf_per_share = fcf / shares_outstanding if shares_outstanding > 0 else 0.0
    fcf_yield = fcf_per_share / current_price if current_price > 0 else 0.0

    # FCF conversion: freeCashflow / netIncome (approximation)
    net_income = _safe_float(info.get("netIncomeToCommon"), 0.0)
    fcf_conversion = fcf / net_income if net_income > 0 else 0.0

    # ── Historical PE averages (5Y) ──
    pe_5y_avg = 0.0
    try:
        hist_5y = stock.history(period="5y")
        if not hist_5y.empty and eps > 0:
            # Approximate: average close / current trailing EPS
            avg_close = float(hist_5y["Close"].mean())
            pe_5y_avg = round(avg_close / eps, 1) if eps > 0 else 0.0
    except Exception:
        pass

    # ── Build pipeline-compatible company dict ──
    company = {
        "id": ticker,
        "name": info.get("longName") or info.get("shortName", ticker),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "market_cap": _market_cap_billions(info),
        # ── Financial Quality ──
        "gross_margin": round(gross_margin, 4),
        "operating_margin": round(operating_margin, 4),
        "fcf_conversion": round(fcf_conversion, 4),
        "debt_to_equity": round(debt_to_equity, 4),
        "roe": round(roe, 4),
        "revenue_growth_3y": round(revenue_growth, 4),  # yfinance gives YoY
        # ── Earnings ──
        "latest_eps": round(eps, 4),
        "consensus_eps": 0,  # analyst — not from yfinance
        "surprise_direction": "",
        "surprise_magnitude_pct": 0,
        "revenue_quality": "",  # analyst
        "margin_quality": "",   # analyst
        "one_time_items": False,
        "share_buyback_impact_pct": 0,
        "guidance_direction": "",
        "guidance_reason": "",
        # ── Valuation ──
        "pe_ttm": round(pe_ttm, 1),
        "pe_5y_avg": pe_5y_avg,
        "pe_10y_avg": 0,  # not available from yfinance
        "ev_ebitda": round(ev_ebitda, 1),
        "ev_ebitda_industry": 0,  # needs sector comparison
        "fcf_yield": round(fcf_yield, 4),
        "scenario_bull": 0,  # analyst targets
        "scenario_base": 0,
        "scenario_bear": 0,
        "current_price": round(current_price, 2),
        # ── Moat (analyst assessment — NOT from yfinance) ──
        "moat_types": [],
        "moat_width": None,
        "moat_depth": None,
        "moat_trend": None,
        # ── Management (analyst assessment — NOT from yfinance) ──
        "ceo_tenure_years": 0,
        "management_credibility": "UNKNOWN",
        "insider_activity": "",
        "cfo_turnover_3y": 0,
        # ── Metadata ──
        "price": prices,
        "source": "yfinance",
        "fixture_category": "REAL EOD — YAHOO FINANCE — FOR V0 DEVELOPMENT ONLY",
    }

    _save_cache(ticker, company)
    return company


def fetch_all(tickers: list[str] = None, force_refresh: bool = False) -> list[dict]:
    """Fetch fundamental data for all FO tickers. Returns list of company dicts."""
    tickers = tickers or FO_TICKERS
    results = []
    for t in tickers:
        try:
            results.append(fetch_fundamental_data(t, force_refresh=force_refresh))
        except Exception as e:
            # Return a minimal entry so pipeline doesn't break
            results.append({
                "id": t,
                "name": t,
                "sector": "Unknown",
                "industry": "Unknown",
                "market_cap": 0,
                "error": str(e),
                "source": "yfinance_failed",
            })
    return results


def summarize(results: list[dict]) -> str:
    """One-line summary per ticker."""
    lines = []
    for d in results:
        if d.get("error"):
            lines.append(f"  {d['id']}: ERROR — {d['error'][:60]}")
        else:
            p = d.get("price", {}) or {}
            name = d.get("name", d["id"])[:40]
            lines.append(f"  {d['id']}: ${p.get('close', '?')} — {name}")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FO V0 — Real Data Source Adapter")
    parser.add_argument("--refresh", action="store_true", help="Force re-fetch, ignore cache")
    parser.add_argument("--summary", action="store_true", help="Show cache summary only")
    parser.add_argument("--tickers", nargs="*", default=None, help="Specific tickers to fetch")
    args = parser.parse_args()

    if args.summary:
        data = fetch_all(force_refresh=False)
        print(summarize(data))
        print(f"\nCache: {CACHE_DIR} ({len(list(CACHE_DIR.glob('*.json')))} files)")
    else:
        tickers = args.tickers if args.tickers else FO_TICKERS
        print(f"Fetching fundamental data for {len(tickers)} tickers...")
        data = fetch_all(tickers, force_refresh=args.refresh)
        print(summarize(data))
        print(f"\nCache: {CACHE_DIR} ({len(list(CACHE_DIR.glob('*.json')))} files)")
