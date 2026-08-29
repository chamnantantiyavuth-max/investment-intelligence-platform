"""
Alpha Momentum V0.5 — Real EOD Source Adapter
Fetches EOD price + fundamental data via yfinance.
Caches to local JSON. Normalizes output for pipeline consumption.
Run with system Python (3.14) — venv is 3.11 and lacks numpy compat.

Usage: python source_adapter.py            # fetch + cache all tickers
       python source_adapter.py --refresh  # force re-fetch
       python source_adapter.py --summary  # show cache summary

NOT LIVE TRADING DATA — FOR V0.5 DEVELOPMENT ONLY.
"""
import os, sys, json, argparse, math
from datetime import datetime
from pathlib import Path

import yfinance as yf

CACHE_DIR = Path(__file__).parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Tickers we track in V0
# GAP-006 fix (FD #45, 2026-08-03): extended 5 -> 9 — added CRWD, PANW, SMCI, AVGO
# (previously synthetic-only candidates; real EOD coverage now 9/9)
V0_TICKERS = ["NVDA", "INTC", "AMD", "MDT", "FSLR", "CRWD", "PANW", "SMCI", "AVGO"]


def _cache_path(ticker: str) -> Path:
    return CACHE_DIR / f"{ticker}.json"


def _load_cache(ticker: str, max_age_hours: int = 24) -> dict | None:
    """Load cached data if fresh enough. Returns None if stale or missing."""
    path = _cache_path(ticker)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    fetched = datetime.fromisoformat(data.get("_fetched_at", "2000-01-01"))
    age = (datetime.now() - fetched).total_seconds() / 3600
    if age > max_age_hours:
        return None
    return data


def _save_cache(ticker: str, data: dict):
    data["_fetched_at"] = datetime.now().isoformat()
    _cache_path(ticker).write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def fetch_eod(ticker: str, force_refresh: bool = False) -> dict:
    """Fetch EOD price + fundamentals for one ticker. Uses cache by default."""
    if not force_refresh:
        cached = _load_cache(ticker)
        if cached:
            return cached

    stock = yf.Ticker(ticker)
    info = stock.info or {}

    # Price data — last 12 months of EOD
    hist = stock.history(period="1y")
    prices = None
    if not hist.empty:
        last = hist.iloc[-1]
        as_of = str(hist.index[-1].date())
        close = float(last["Close"])
        if not math.isfinite(close):
            # The final history bar is occasionally served all-NaN (partial/stale
            # bar; observed 2026-08-29: 9/9 tickers as_of 2026-08-28 with NaN OHLC
            # while fast_info carried the real Friday close). Fall back to
            # fast_info.lastPrice (real last trade), then to the most recent
            # completed bar if that is unavailable too.
            close = None
            try:
                fi_close = stock.fast_info.get("lastPrice")
                if fi_close is not None:
                    fi_close = float(fi_close)
                    if math.isfinite(fi_close):
                        close = round(fi_close, 2)
            except Exception:
                pass
            if close is None:
                valid = hist.dropna(subset=["Close"])
                if not valid.empty:
                    last = valid.iloc[-1]
                    close = round(float(last["Close"]), 2)
                    as_of = str(valid.index[-1].date())
        if close is not None:
            prices = {
                "close": close,
                "open": round(float(last["Open"]), 2) if math.isfinite(float(last["Open"])) else None,
                "high": round(float(last["High"]), 2) if math.isfinite(float(last["High"])) else None,
                "low": round(float(last["Low"]), 2) if math.isfinite(float(last["Low"])) else None,
                "volume": int(last["Volume"]) if math.isfinite(float(last["Volume"])) else None,
                "as_of": as_of,
            }

    data = {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName", ticker),
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "eps": info.get("trailingEps"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "beta": info.get("beta"),
        "fifty_day_avg": info.get("fiftyDayAverage"),
        "two_hundred_day_avg": info.get("twoHundredDayAverage"),
        "price": prices,
        "source": "yfinance",
        "fixture_category": "REAL EOD — YAHOO FINANCE — FOR V0.5 DEVELOPMENT ONLY",
    }
    _save_cache(ticker, data)
    return data


def fetch_all(tickers: list[str] = None, force_refresh: bool = False) -> dict[str, dict]:
    """Fetch EOD data for all V0 tickers."""
    tickers = tickers or V0_TICKERS
    results = {}
    for t in tickers:
        try:
            results[t] = fetch_eod(t, force_refresh=force_refresh)
        except Exception as e:
            results[t] = {"ticker": t, "error": str(e), "source": "yfinance_failed"}
    return results


def summarize(results: dict[str, dict]) -> str:
    """One-line summary per ticker."""
    lines = []
    for t, d in results.items():
        if "error" in d:
            lines.append(f"  {t}: ERROR — {d['error'][:60]}")
        else:
            p = d.get("price", {}) or {}
            lines.append(f"  {t}: ${p.get('close','?')} — {d.get('name','?')[:40]}")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AM V0.5 EOD source adapter")
    parser.add_argument("--refresh", action="store_true",
                        help="force re-fetch all tickers (bypass 24h cache)")
    args = parser.parse_args()
    print("Fetching EOD data...")
    data = fetch_all(force_refresh=args.refresh)
    print(summarize(data))
    print(f"\nCache: {CACHE_DIR} ({len(list(CACHE_DIR.glob('*.json')))} files)")
