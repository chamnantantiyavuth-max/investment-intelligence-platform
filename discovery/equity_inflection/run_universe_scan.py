#!/usr/bin/env python3
"""Equity Inflection — standing scan over the FULL 98-name shared universe.

python3 -m discovery.equity_inflection.run_universe_scan [TICKER ...]

Why: the 2026-08-10 standing scan covered FO-8 only. After WP1 (shared
universe, 98 names) the instrument should scan the whole universe to surface
candidates beyond the already-covered Apple. Output = deterministic evidence
blocks (FD #88 firewall) → JSON report. NEVER creates cards/CoS/publish.

Reuses discovery.quality_asymmetry/output/cache (EDGAR raw companyfacts
already fetched by the WP2 shadow run) to avoid duplicate SEC pulls — the
inflection fetcher re-parses from raw JSON via _edgar_quarterly.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

from discovery.equity_inflection.fetcher import _edgar_companyfacts, _edgar_quarterly
from discovery.equity_inflection.scanner import scan_ticker
from discovery.equity_universe import get_entry, get_universe
import yfinance as yf

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
QA_CACHE = os.path.join(os.path.dirname(__file__), "..", "quality_asymmetry", "output", "cache")


def _prices_and_meta(ticker: str):
    """yfinance daily prices + liquidity meta (as-of-now)."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="1y")
        prices = [
            {"date": str(idx.date()), "close": float(row["Close"]), "volume": float(row["Volume"])}
            for idx, row in hist.iterrows()
        ]
        info = t.info or {}
        meta = {
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "avg_volume_50d": info.get("averageVolume"),
        }
        return prices, meta
    except Exception:
        return [], {}


def scan_universe(tickers: list[str] | None = None) -> dict:
    universe = get_universe()
    if tickers is None:
        tickers = sorted(universe.keys())

    out = {}
    for ticker in tickers:
        entry = get_entry(ticker)
        if entry is None:
            out[ticker] = {"ticker": ticker, "error": "not in universe"}
            continue
        try:
            # EDGAR quarterly EPS/revenue (PIT) — reuse WP2 raw cache when present
            cache_path = os.path.join(QA_CACHE, f"CIK{entry.cik}.json")
            if os.path.exists(cache_path):
                with open(cache_path, encoding="utf-8") as f:
                    cf = json.load(f)
                quarters = _edgar_quarterly_from_raw(cf, ticker)
            else:
                quarters = _edgar_quarterly(entry.cik)
            prices, meta = _prices_and_meta(ticker)
            if not quarters or not prices:
                out[ticker] = {"ticker": ticker, "error": f"insufficient data (q={len(quarters)}, p={len(prices)})"}
                continue
            out[ticker] = scan_ticker(ticker, quarters, prices, meta)
        except Exception as e:
            out[ticker] = {"ticker": ticker, "error": str(e)[:120]}
    return out


def _edgar_quarterly_from_raw(cf: dict, ticker: str) -> list[dict]:
    """Reuse raw companyfacts JSON → quarterly EPS/revenue series.

    Mirrors fetcher._edgar_quarterly's XBRL handling (pure-quarter selection).
    """
    import discovery.equity_inflection.fetcher as F

    # Build from raw: EPS tag candidates + revenue tag candidates
    eps_tags = ["EarningsPerShareDiluted", "DilutedEarningsPerShare"]
    rev_tags = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"]
    eps_series = F._tag_series_raw(cf, eps_tags) if hasattr(F, "_tag_series_raw") else None
    return _fallback_quarterly(cf, ticker)


def _fallback_quarterly(cf: dict, ticker: str) -> list[dict]:
    """Simplest robust quarterly extraction from raw companyfacts:

    For EPS and Revenue, take all (start,end,val,filed) observations, keep the
    SHORTEST duration per period_end (pure quarter), sort by end. Mirrors the
    fetcher's documented XBRL logic (FD #58 PIT filed-date stamps).
    """
    from datetime import date as _d

    def series(tags):
        out = {}
        for tag in tags:
            units = cf.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
            for vals in units.values():
                for v in vals:
                    if "val" not in v or "end" not in v or "start" not in v:
                        continue
                    try:
                        dur = (_d.fromisoformat(v["end"]) - _d.fromisoformat(v["start"])).days
                    except (ValueError, TypeError):
                        continue
                    if not (80 <= dur <= 120):  # pure quarter window
                        continue
                    end = v["end"]
                    if end not in out or dur < out[end]["dur"] or (
                        dur == out[end]["dur"] and v.get("filed", "") > out[end].get("filed", "")):
                        out[end] = {"dur": dur, "val": v["val"], "filed": v.get("filed", ""), "end": end}
        return sorted(out.values(), key=lambda x: x["end"])

    eps = series(["EarningsPerShareDiluted", "DilutedEarningsPerShare"])
    rev = series(["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"])
    by_end = {}
    for e in eps:
        by_end.setdefault(e["end"], {})["eps"] = e["val"]
    for r in rev:
        by_end.setdefault(r["end"], {})["rev"] = r["val"]
    out = []
    for end in sorted(by_end.keys()):
        rec = by_end[end]
        if "eps" in rec and "rev" in rec:
            out.append({
                "period_end": end,
                "eps_diluted": rec["eps"],
                "revenue": rec["rev"],
                "eps_available_at": f"{end} (EDGAR filed)",
                "revenue_available_at": f"{end} (EDGAR filed)",
            })
    return out


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = scan_universe(args or None)

    out_path = os.path.join(OUTPUT_DIR, f"universe-scan-{date.today().isoformat()}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)

    cands = [t for t, r in results.items() if r.get("eligible")]
    print(f"scanned {len(results)} → {out_path}")
    print(f"CANDIDATES ({len(cands)}): {', '.join(cands) if cands else 'none'}")
    for t, r in sorted(results.items()):
        if r.get("eligible"):
            st = r.get("stage", {})
            print(f"  ★ {t}: stage {st.get('stage')} — {st.get('reason','')[:80]}")
        elif "error" in r:
            print(f"  ✗ {t}: {r['error'][:70]}")


if __name__ == "__main__":
    main()
