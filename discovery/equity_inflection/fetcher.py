"""Equity Inflection Discovery — shadow data fetcher (yfinance + SEC EDGAR).

RUNS UNDER SYSTEM PYTHON 3.14 (`python3`) — the pytest venv (3.11) lacks a
working yfinance/numpy. The scanner itself (`scanner.py`) is pure and runs
anywhere; this module only fetches and shapes data for it.

Point-in-time discipline (FD #58): every quarterly figure carries an
`eps_available_at` / `revenue_available_at` stamp.

Source strategy (shadow phase, honest):
  1. SEC EDGAR companyfacts (primary) — quarterly EPS + revenue with the
     actual FILING date -> true point-in-time availability (FD #58) and
     enough history for the 2-year lookback. Verified 2026-08-10 that
     yfinance's quarterly_income_stmt returns only 5 quarters — insufficient
     for the 9-quarter requirement (scanner surfaced this honestly).
  2. yfinance — daily prices + volume + liquidity meta only.

Shadow mode: output feeds `scanner.run_shadow()` — NO cards, NO CoS triage,
NO research capacity consumed (FD #88).
"""
from __future__ import annotations

import json
import time
import urllib.request
from datetime import date
from pathlib import Path

import yfinance as yf

# FO-universe first (data-proven, FD #88 plan §8); expand later per validation.
# CIKs from role 11 PRINCIPAL.md / FD #81 (verified against company_tickers.json).
FO_UNIVERSE = {
    "AAPL": "0000320193", "MSFT": "0000789019", "NVDA": "0001045810",
    "GOOGL": "0001652044", "AMZN": "0001018724", "META": "0001326801",
    "TSLA": "0001318605", "JNJ": "0000200406",
}

USER_AGENT = "IIP-Research/1.0 (admin@iip.local)"
REQUEST_DELAY = 0.15  # SEC: 10 req/s limit


def _sec_get(url: str, timeout: int = 30) -> dict:
    time.sleep(REQUEST_DELAY)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_date(s: str):
    """ISO date string -> date. Returns None on garbage (defensive)."""
    try:
        from datetime import date as _d
        return _d.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _split_adjust(series: list[dict], share_series: list[dict]) -> list[dict]:
    """Thin alias — split adjustment logic lives in scanner.split_adjust
    (pure module, testable without yfinance)."""
    from discovery.equity_inflection.scanner import split_adjust as _sa
    return _sa(series, share_series)


def _edgar_companyfacts(cik: str) -> dict:
    """Fetch and cache raw SEC companyfacts for a CIK."""
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    return _sec_get(url)


def _edgar_quarterly(cik: str):
    """Fetch quarterly DilutedEPS + Revenues from SEC companyfacts (PIT).

    Returns (eps_series, rev_series) where each entry is
    {"period_end": str, "value": float, "filed": str, "derived": bool}. Uses
    the actual 'filed' date as the as-of availability stamp (FD #58).

    XBRL reality handled explicitly:
      - companyfacts carries BOTH pure-quarter and YTD-cumulative values for
        the same period_end (e.g. Q2 EPS and H1 EPS both dated at the Q2
        filing) -> keep ONE value per period_end: SHORTEST duration = pure
        quarter.
      - The fiscal Q4 slot is NOT reported as a pure quarter: the 10-K only
        carries the FY annual value at that period_end. Derive Q4 =
        annual - sum(other 3 quarters of that fiscal year), labelled
        derived=True (standard derivation, never a silent substitution).
    """
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    facts = _sec_get(url)
    tax = facts.get("facts", {}).get("us-gaap", {})
    def dedup_raw(tag: str) -> list[dict]:
        """All 10-Q/10-K values, deduped per period_end (shortest duration)."""
        by_end: dict[str, dict] = {}
        for u in tax.get(tag, {}).get("units", {}).values():
            for v in u:
                if v.get("form") not in ("10-Q", "10-K"):
                    continue
                end = v.get("end")
                if not end or v.get("val") is None:
                    continue
                start = v.get("start", end)
                d_start, d_end = _parse_date(start), _parse_date(end)
                dur = (d_end - d_start).days if (d_start and d_end) else 3650
                cur = by_end.get(end)
                if cur is None or dur < cur["_dur"] or (
                        dur == cur["_dur"] and v.get("filed", end) > cur["filed"]):
                    by_end[end] = {"period_end": end, "value": float(v["val"]),
                                   "filed": v.get("filed", end), "_dur": dur,
                                   "_start": start, "_end": end,
                                   "_fp": v.get("fp", "")}
        return list(by_end.values())

    def build(tag: str) -> list[dict]:
        raw = dedup_raw(tag)
        quarters = [x for x in raw if x["_dur"] <= 150]          # pure quarters
        annuals = [x for x in raw if x["_dur"] > 200]            # FY annuals
        by_end = {x["period_end"]: x for x in quarters}
        # derive fiscal-Q4: annual minus the 3 pure quarters inside its window
        derived = []
        for a in annuals:
            a_start, a_end = _parse_date(a["_start"]), _parse_date(a["_end"])
            if not (a_start and a_end):
                continue
            inside = [q for q in quarters
                      if (_parse_date(q["period_end"]) or a_start) >= a_start
                      and _parse_date(q["period_end"]) <= a_end]
            if len(inside) == 3:
                q4 = a["value"] - sum(q["value"] for q in inside)
                if q4 != 0 and q4 == q4:  # non-zero, not NaN
                    derived.append({"period_end": a["period_end"],
                                    "value": round(q4, 6),
                                    "filed": a["filed"], "derived": True})
            # period_ends with only an annual (and <3 quarters inside) are
            # dropped — insufficient XBRL granularity, honest omission
        all_q = {q["period_end"]: q for q in quarters}
        for d in derived:
            all_q.setdefault(d["period_end"], d)
        out = [{"period_end": k, "value": v["value"], "filed": v["filed"],
                "derived": bool(v.get("derived"))}
               for k, v in sorted(all_q.items())]
        return out

    eps = build("EarningsPerShareDiluted")
    # share count tag: companyfacts uses WeightedAverageNumberOfDilutedSharesOutstanding
    shares = build("WeightedAverageNumberOfDilutedSharesOutstanding")
    if not shares:
        shares = build("WeightedAverageNumberOfSharesOutstandingBasic")
    eps = _split_adjust(eps, shares)
    # revenue tag: MERGE all candidates — filers switch tags across eras
    # (e.g. AAPL: SalesRevenueNet pre-FY2018 -> RevenueFromContract... post-ASC606).
    rev_raw: dict[str, dict] = {}
    for tag in ("Revenues", "SalesRevenueNet",
                "RevenueFromContractWithCustomerExcludingAssessedTax"):
        for u in tax.get(tag, {}).get("units", {}).values():
            for v in u:
                if v.get("form") not in ("10-Q", "10-K") or v.get("end") is None or v.get("val") is None:
                    continue
                end = v["end"]
                start = v.get("start", end)
                d_start, d_end = _parse_date(start), _parse_date(end)
                dur = (d_end - d_start).days if (d_start and d_end) else 3650
                cur = rev_raw.get(end)
                if cur is None or dur < cur["_dur"] or (
                        dur == cur["_dur"] and v.get("filed", end) > cur["filed"]):
                    rev_raw[end] = {"period_end": end, "value": float(v["val"]),
                                    "filed": v.get("filed", end), "_dur": dur,
                                    "_start": start, "_end": end}
    # same fiscal-Q4 derivation for revenue
    rev_quarters = [x for x in rev_raw.values() if x["_dur"] <= 150]
    rev_annuals = [x for x in rev_raw.values() if x["_dur"] > 200]
    rev_by_end = {x["period_end"]: x for x in rev_quarters}
    for a in rev_annuals:
        a_start, a_end = _parse_date(a["_start"]), _parse_date(a["_end"])
        if not (a_start and a_end):
            continue
        inside = [q for q in rev_quarters
                  if (_parse_date(q["period_end"]) or a_start) >= a_start
                  and _parse_date(q["period_end"]) <= a_end]
        if len(inside) == 3:
            q4 = a["value"] - sum(q["value"] for q in inside)
            if q4 != 0 and q4 == q4:
                rev_by_end.setdefault(a["period_end"], {
                    "period_end": a["period_end"], "value": round(q4, 6),
                    "filed": a["filed"], "derived": True})
    rev = sorted(({"period_end": k, "value": v["value"], "filed": v["filed"],
                   "derived": bool(v.get("derived"))}
                  for k, v in rev_by_end.items()), key=lambda x: x["period_end"])
    return eps, rev


def fetch_ticker(ticker: str) -> dict:
    """Fetch quarterly EPS/revenue (EDGAR, PIT) + daily prices (yfinance).

    Returns {"quarters": [...], "prices": [...], "meta": {...}} — the payload
    shape consumed by scanner.run_shadow(). Raises on hard failure so the
    shadow run records an honest per-ticker error.
    """
    cik = FO_UNIVERSE.get(ticker)
    if not cik:
        raise ValueError(f"{ticker}: no CIK in FO_UNIVERSE")

    eps_series, rev_series = _edgar_quarterly(cik)
    if len(eps_series) < 9:
        raise ValueError(
            f"{ticker}: EDGAR quarterly diluted EPS history insufficient "
            f"({len(eps_series)} < 9 quarters needed for 2-year lookback)")

    rev_by_end = {r["period_end"]: r for r in rev_series}
    quarters = []
    for e in eps_series:
        r = rev_by_end.get(e["period_end"], {})
        quarters.append({
            "period_end": e["period_end"],
            "eps_diluted": e["value"],
            "revenue": float(r["value"]) if r.get("value") is not None else 0.0,
            "eps_available_at": f"{e['filed']} (EDGAR filed date)",
            "revenue_available_at": f"{r.get('filed', e['filed'])} (EDGAR filed date)",
        })

    # daily prices — need >= 260 sessions for 150MA + slope lookbacks
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2y")
    if hist is None or hist.empty:
        raise ValueError(f"{ticker}: yfinance price history empty")
    prices = []
    for idx, row in hist.iterrows():
        prices.append({
            "date": str(idx.date()),
            "close": round(float(row["Close"]), 4),
            "volume": int(row["Volume"]),
        })

    meta = {
        "price": round(float(hist["Close"].iloc[-1]), 2),
        "avg_volume_50d": float(hist["Volume"].tail(50).mean()),
        "as_of": str(hist.index[-1].date()),
    }
    return {"quarters": quarters, "prices": prices, "meta": meta}


def fetch_validation_data(ticker: str) -> dict:
    """Fetch FULL revision history (every filed-date entry, not just latest)
    + 10y price history for validation Phase 1 (PIT as-of reconstruction).

    Returns {"ticker": str, "eps_entries": [...], "rev_entries": [...],
             "share_entries": [...], "prices": [...]} where each entry is
    {"period_end": str, "value": float, "filed": str, "start": str,
     "form": str, "fp": str}. ALL 10-Q/10-K entries preserved (restatement
    history intact) — the PIT as-of view is built later by validation.py.
    """
    cik = FO_UNIVERSE.get(ticker)
    if not cik:
        raise ValueError(f"{ticker}: no CIK in FO_UNIVERSE")
    facts = _edgar_companyfacts(cik)
    tax = facts.get("facts", {}).get("us-gaap", {})

    def all_entries(tag: str) -> list[dict]:
        out = []
        for u in tax.get(tag, {}).get("units", {}).values():
            for v in u:
                if v.get("form") not in ("10-Q", "10-K") or v.get("end") is None or v.get("val") is None:
                    continue
                out.append({
                    "period_end": v["end"], "value": float(v["val"]),
                    "filed": v.get("filed", v["end"]),
                    "start": v.get("start", v["end"]),
                    "form": v.get("form", ""), "fp": v.get("fp", ""),
                })
        return sorted(out, key=lambda x: (x["period_end"], x["filed"]))

    rev_tags = ("Revenues", "SalesRevenueNet",
                "RevenueFromContractWithCustomerExcludingAssessedTax")
    rev_entries = []
    for tag in rev_tags:
        rev_entries.extend(all_entries(tag))

    # share count tag: companyfacts uses WeightedAverageNumberOfDilutedSharesOutstanding
    # (verified 2026-08-10 — "DilutedAverageShares" returns 0 entries)
    share_tag = "WeightedAverageNumberOfDilutedSharesOutstanding"
    share_entries = all_entries(share_tag)
    if not share_entries:  # fallback: basic weighted average
        share_entries = all_entries("WeightedAverageNumberOfSharesOutstandingBasic")

    stock = yf.Ticker(ticker)
    hist = stock.history(period="10y")
    if hist is None or hist.empty:
        raise ValueError(f"{ticker}: yfinance 10y price history empty")
    prices = [{"date": str(idx.date()), "close": round(float(row["Close"]), 4),
               "volume": int(row["Volume"])} for idx, row in hist.iterrows()]
    return {
        "ticker": ticker,
        "eps_entries": all_entries("EarningsPerShareDiluted"),
        "rev_entries": rev_entries,
        "share_entries": share_entries,
        "prices": prices,
    }


def fetch_universe(tickers: list[str] | None = None) -> dict[str, dict]:
    """Fetch all tickers. Per-ticker errors become {"error": ...} payloads —
    the scanner records them honestly (never fabricated candidates)."""
    tickers = tickers or list(FO_UNIVERSE.keys())
    out = {}
    for t in tickers:
        try:
            out[t] = fetch_ticker(t)
        except Exception as e:  # noqa: BLE001 — honest per-ticker failure
            out[t] = {"error": f"{type(e).__name__}: {e}"}
    return out


if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root
    from discovery.equity_inflection import scanner

    payloads = fetch_universe()
    results = scanner.run_shadow(payloads)

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    # standing instrument output (FD #89 — shadow label retired)
    (out_dir / f"standing-scan-{stamp}.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Equity Inflection Standing Scan — {stamp} (FO-universe {len(payloads)} names)")
    print("=" * 70)
    for r in results:
        flag = "CANDIDATE" if r["eligible"] else "     —"
        print(f"{flag}  {r['ticker']}")
        for reason in r.get("reasons", []):
            print(f"        - {reason}")
    print("=" * 70)
    print(f"Output: {out_dir / f'standing-scan-{stamp}.json'}")
    print("NOTE: standing discovery instrument (FD #89) — deterministic evidence blocks;")
    print("      no auto Task Idea Cards, no CoS triage, no research load.")
