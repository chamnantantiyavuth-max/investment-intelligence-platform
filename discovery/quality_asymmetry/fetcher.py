"""Quality & Asymmetry Discovery — shadow data fetcher (WP2, ChatGPT FIT-GAP).

Architecture mirrors discovery/equity_inflection/fetcher.py: this module needs
a working yfinance/numpy, so it runs under SYSTEM Python 3.14 (python3), NOT
the pytest venv. The archetype engine (archetypes.py) is pure and venv-safe.

Data sources (primary = SEC EDGAR companyfacts, PIT per FD #58):
  1. EDGAR companyfacts — annual (fiscal-year) series for the 12 financial
     keys the archetype engine consumes: revenue, net_income,
     operating_income, total_assets, total_equity, total_debt, cash, ocf,
     capex, dividends_paid, buybacks_paid, ebitda (ebitda computed as
     operating_income + D&A when D&A tag exists — XBRL has no native EBITDA).
     Values carry the actual 'filed' date as availability stamp.
  2. yfinance — market snapshot (price, ratios, 52w high, buyback yield proxy,
     shares out). Market data is as-of-now (FD #58: point-in-time rule applies
     to reference books; for shadow scans the snapshot date is stamped).
  3. Cache: raw companyfacts JSON cached under discovery/quality_asymmetry/
     output/cache/CIK{...}.json to avoid re-fetching on re-runs.

Shadow-only: output feeds run_shadow() evidence blocks. Never creates cards,
never enters CoS, never publishes (firewall, FD #88 pattern).
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import date

import yfinance as yf

from discovery.equity_universe import get_entry, get_universe

USER_AGENT = "IIP-Research/1.0 (admin@iip.local)"
REQUEST_DELAY = 0.15  # SEC: 10 req/s limit

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
CACHE_DIR = os.path.join(OUTPUT_DIR, "cache")


def _sec_get(url: str, timeout: int = 30) -> dict:
    time.sleep(REQUEST_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _companyfacts(cik: str) -> dict:
    """Fetch raw companyfacts with on-disk cache."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"CIK{cik}.json")
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    data = _sec_get(url)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data


# ── XBRL tag mapping (US-GAAP) ──────────────────────────────────────────────
# Each key: list of tag candidates in priority order. Annual extraction keeps
# fiscal-year observations (duration ~360±40 days), latest-filed per period_end.
_TAG_MAP: dict[str, list[str]] = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
    ],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "operating_income": [
        "OperatingIncomeLoss",
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
    ],
    "total_assets": ["Assets"],
    "total_equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "long_term_debt": [
        "LongTermDebt",
        "LongTermDebtAndCapitalLeaseObligations",
        "LongTermDebtNoncurrent",
    ],
    "long_term_debt_current": [
        "LongTermDebtCurrent",
        "LongTermDebtAndCapitalLeaseObligationsCurrent",
    ],
    "current_debt": ["DebtCurrent", "ShortTermBorrowings"],
    "cash": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquirePropertyPlantAndEquipmentAndIntangibleAssets",
    ],
    "dividends_paid": ["PaymentsOfDividends", "PaymentsOfDividendsCommonStock"],
    "buybacks_paid": ["PaymentsForRepurchaseOfCommonStock", "PaymentsForRepurchaseOfEquity"],
    "depreciation": [
        "DepreciationDepletionAndAmortization",
        "DepreciationAmortizationAndAccretionNet",
        "DepreciationDepletionAndAmortization",
    ],
}


def _tag_series(cf: dict, tag: str) -> list[dict]:
    """All observations of one tag across units, deduped by period_end."""
    out: dict[str, dict] = {}
    units = cf.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
    for vals in units.values():
        for v in vals:
            if "val" not in v or "end" not in v:
                continue
            end = v["end"]
            # keep latest-filed per period_end
            if end not in out or v.get("filed", "") > out[end].get("filed", ""):
                out[end] = {
                    "period_end": end,
                    "value": v["val"],
                    "filed": v.get("filed", ""),
                    "start": v.get("start", end),
                    "duration_days": _duration_days(v.get("start"), end),
                }
    return sorted(out.values(), key=lambda x: x["period_end"])


def _duration_days(start: str | None, end: str) -> int:
    try:
        if not start:
            return 0
        from datetime import date as _d
        return (_d.fromisoformat(end) - _d.fromisoformat(start)).days
    except (ValueError, TypeError):
        return 0


def _annual_values(cf: dict, tag: str, max_years: int = 8) -> list[float]:
    """Fiscal-year observations for FLOW tags (duration 320–400 days), chronological."""
    series = _tag_series(cf, tag)
    years = [s for s in series if 320 <= s["duration_days"] <= 400]
    return [float(s["value"]) for s in years[-max_years:]]


def _flow_series(cf: dict, candidates: list[str], max_years: int = 8) -> list[float]:
    """Merged fiscal-year flow series across candidate tags.

    Companies switch XBRL tags over time (e.g. NVDA:
    RevenueFromContractWithCustomer… → Revenues). Merge all candidates, dedup
    by period_end keeping the LATEST-FILED value, then chronological. This is
    why a single-tag-first lookup is wrong (it stops at the tag switch).
    """
    by_end: dict[str, dict] = {}
    for tag in candidates:
        for s in _tag_series(cf, tag):
            if not (320 <= s["duration_days"] <= 400):
                continue
            end = s["period_end"]
            if end not in by_end or s["filed"] > by_end[end].get("filed", ""):
                by_end[end] = s
    ordered = sorted(by_end.values(), key=lambda x: x["period_end"])
    return [float(s["value"]) for s in ordered[-max_years:]]


def _fiscal_year_ends(cf: dict) -> list[str]:
    """Fiscal year-end dates derived from the merged revenue flow series."""
    series = _flow_series(cf, _TAG_MAP["revenue"], max_years=8)
    by_end: dict[str, dict] = {}
    for tag in _TAG_MAP["revenue"]:
        for s in _tag_series(cf, tag):
            if not (320 <= s["duration_days"] <= 400):
                continue
            end = s["period_end"]
            if end not in by_end or s["filed"] > by_end[end].get("filed", ""):
                by_end[end] = s
    ordered = sorted(by_end.values(), key=lambda x: x["period_end"])
    return [s["period_end"] for s in ordered[-8:]]


def _instant_at_year_ends(cf: dict, tag: str, year_ends: list[str]) -> dict[str, float]:
    """Balance-sheet (instant, start=None) values keyed by fiscal year-end.

    Instant tags carry no duration — the value AT the year-end date is the
    annual snapshot. Fallback: nearest observation ≤ year-end + 45 days.
    Returns {year_end: value} so multi-tag sums align by DATE, not index.
    """
    series = _tag_series(cf, tag)
    out: dict[str, float] = {}
    from datetime import date as _d
    for ye in year_ends:
        ye_d = _d.fromisoformat(ye)
        best = None
        best_gap = 10**9
        for s in series:
            try:
                end_d = _d.fromisoformat(s["period_end"])
            except (ValueError, TypeError):
                continue
            gap = (ye_d - end_d).days
            if -7 <= gap <= 45 and gap < best_gap:
                best = s["value"]
                best_gap = gap
        if best is not None:
            out[ye] = float(best)
    return out


def _first_tag(cf: dict, candidates: list[str], max_years: int = 8,
               instant: bool = False, year_ends: list[str] | None = None) -> dict | list:
    for tag in candidates:
        if instant:
            vals = _instant_at_year_ends(cf, tag, year_ends or [])
        else:
            vals = _annual_values(cf, tag, max_years)
        if vals:
            return vals
    return {} if instant else []


def _lookup(cf: dict, candidates: list[str], max_years: int = 8,
            instant: bool = False, year_ends: list[str] | None = None):
    """Flow: merged series across candidates. Instant: first tag with values
    at year-ends (instant tags rarely switch, and merging would double-count
    overlapping definitions)."""
    if instant:
        return _first_tag(cf, candidates, max_years, instant=True, year_ends=year_ends)
    return _flow_series(cf, candidates, max_years)


def _align_tail(flow: list[float], instant: list[float]) -> list[float]:
    """Align an instant (shorter) series to a flow series by TAIL (latest
    fiscal year matches). Instant series may start later (fewer years of
    balance-sheet data) — LEFT-PAD with None so every series has the same
    length as the flow series. The engine indexes from the tail (range(-5,0))
    and `_f` reads the last non-None, so tail-alignment + None padding keeps
    every index consistent across series."""
    if not instant or not flow:
        return []
    if len(instant) >= len(flow):
        return instant[-len(flow):]
    return [None] * (len(flow) - len(instant)) + list(instant)


def _align_dict(d: dict, year_ends: list[str]) -> list[float]:
    """Instant dict → list aligned to the FULL year_ends list (oldest→newest).
    Missing earlier years are dropped (they can't line up with flow series of
    the same length — flow defines the time axis)."""
    return [d[ye] for ye in year_ends if ye in d]


def fetch_financials(cik: str) -> dict:
    """Annual financial series for one CIK → archetype-engine input dict.

    Keys: revenue, net_income, operating_income, total_assets, total_equity,
    total_debt, cash, ocf, capex, dividends_paid, buybacks_paid, ebitda.
    Lists are chronological (oldest → newest). **All series are aligned to the
    same time axis (the merged revenue series) so the engine can index them
    consistently** — instant series (assets/equity/debt/cash) are truncated to
    the trailing years that overlap the revenue timeline. Missing series → [].
    """
    cf = _companyfacts(cik)
    year_ends = _fiscal_year_ends(cf)

    rev = _lookup(cf, _TAG_MAP["revenue"])
    n_flow = len(rev)
    axis = year_ends[-n_flow:] if n_flow else []

    lt_debt = _lookup(cf, _TAG_MAP["long_term_debt"], instant=True, year_ends=year_ends)
    lt_curr = _lookup(cf, _TAG_MAP["long_term_debt_current"], instant=True, year_ends=year_ends)
    total_debt = _merge_instant(lt_debt, lt_curr, year_ends)
    if not total_debt:
        total_debt = _lookup(cf, _TAG_MAP["current_debt"], instant=True, year_ends=year_ends)

    oi = _lookup(cf, _TAG_MAP["operating_income"])
    da = _lookup(cf, _TAG_MAP["depreciation"])

    def inst(candidates):
        d = _lookup(cf, candidates, instant=True, year_ends=year_ends)
        return _align_tail(rev, _align_dict(d, axis)) if isinstance(d, dict) else _align_tail(rev, [])

    return {
        "revenue": rev,
        "net_income": _lookup(cf, _TAG_MAP["net_income"]),
        "operating_income": oi,
        "total_assets": inst(_TAG_MAP["total_assets"]),
        "total_equity": inst(_TAG_MAP["total_equity"]),
        "total_debt": inst(None) if not total_debt else _align_tail(rev, _align_dict(total_debt, axis)),
        "cash": inst(_TAG_MAP["cash"]),
        "ocf": _lookup(cf, _TAG_MAP["ocf"]),
        "capex": _lookup(cf, _TAG_MAP["capex"]),  # negative convention (payments out)
        "dividends_paid": _lookup(cf, _TAG_MAP["dividends_paid"]),
        "buybacks_paid": _lookup(cf, _TAG_MAP["buybacks_paid"]),
        "ebitda": _sum_series(oi, da),
    }


def _merge_instant(a: dict, b: dict, year_ends: list[str]) -> dict:
    """Sum two instant dicts (keyed by year_end) — missing key = 0."""
    out: dict[str, float] = {}
    for ye in year_ends:
        va = a.get(ye, 0.0)
        vb = b.get(ye, 0.0)
        if ye in a or ye in b:
            out[ye] = va + vb
    return out


def _as_series(d: dict, year_ends: list[str]) -> list[float]:
    """Instant dict → chronological list aligned to year_ends (oldest→newest)."""
    return [d[ye] for ye in year_ends if ye in d]


def _sum_series(a: list[float], b: list[float]) -> list[float]:
    """Element-wise sum of two chronological series (longest-anchored)."""
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        va = a[i] if i < len(a) else 0.0
        vb = b[i] if i < len(b) else 0.0
        out.append(va + vb)
    return out


def fetch_market(ticker: str) -> dict:
    """yfinance market snapshot (as-of-now, stamped)."""
    try:
        info = yf.Ticker(ticker).info or {}
    except Exception:
        return {}
    market = {
        "as_of": date.today().isoformat(),
        "price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "eps_ttm": info.get("trailingEps"),
        "book_value_per_share": info.get("bookValue"),
        "shares_out": info.get("sharesOutstanding"),
        "market_cap": info.get("marketCap"),
        "price_52w_high": info.get("fiftyTwoWeekHigh"),
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
        "buyback_yield_ttm": None,  # yfinance has no direct TTM buyback yield — analyst recon
    }
    return {k: v for k, v in market.items() if v is not None}


def fetch_ticker(ticker: str) -> dict:
    """Full payload for one ticker: {fin, market, source, stamps}."""
    entry = get_entry(ticker)
    if entry is None:
        raise ValueError(f"{ticker}: not in shared equity universe")
    fin = fetch_financials(entry.cik)
    market = fetch_market(ticker)
    return {
        "ticker": ticker,
        "cik": entry.cik,
        "name": entry.title,
        "sector": entry.sector,
        "fin": fin,
        "market": market,
        "source": "SEC EDGAR companyfacts (annual, PIT) + yfinance market snapshot",
        "financials_as_of": fin.get("as_of", "latest fiscal years with filed-date stamps"),
        "market_as_of": market.get("as_of", "as-of-now"),
    }


def fetch_universe(tickers: list[str] | None = None) -> dict[str, dict]:
    """Fetch payloads for a subset (default: whole universe)."""
    universe = get_universe()
    if tickers is None:
        tickers = sorted(universe.keys())
    payloads: dict[str, dict] = {}
    for t in tickers:
        try:
            payloads[t] = fetch_ticker(t)
        except Exception as e:  # per-ticker isolation — one failure never kills the scan
            payloads[t] = {"ticker": t, "error": str(e)}
    return payloads


def main() -> None:
    """CLI: python3 -m discovery.quality_asymmetry.fetcher [TICKER ...]

    Writes raw payloads to output/payloads-<date>.json (shadow input).
    """
    import sys

    tickers = sys.argv[1:] or None
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    payloads = fetch_universe(tickers)
    out_path = os.path.join(OUTPUT_DIR, f"payloads-{date.today().isoformat()}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payloads, f, indent=1)
    ok = sum(1 for p in payloads.values() if "error" not in p)
    print(f"fetched {ok}/{len(payloads)} → {out_path}")


if __name__ == "__main__":
    main()
