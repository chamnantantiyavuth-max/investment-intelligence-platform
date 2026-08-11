"""Quality & Asymmetry Discovery — pure deterministic archetype engine (WP2).

Four qualitative archetypes (ChatGPT FIT-GAP WP2, 11 Aug 2026) — NOT a score:

    A. Durable Compounder   (Buffett / Li Lu)  — high & stable returns on capital
    B. Long-Runway 100-Bagger (Fisher)         — ROIC × reinvestment × runway
    C. Mispriced Quality    (Buffett / Li Lu)  — great business, market doubt
    D. Asymmetric Value     (Pabrai)           — limited permanent downside,
                                                 large upside (special situations)

Design rules (binding):
  - PURE DETERMINISTIC LOGIC ONLY — no yfinance/numpy at import time (pytest venv
    is Python 3.11; the fetch layer runs under system Python 3.14, same as
    discovery/equity_inflection). This module operates on already-fetched
    annual-financial dicts so every invariant is unit-testable.
  - Output = deterministic EVIDENCE BLOCK ONLY. It NEVER creates a Task Idea
    Card, never enters CoS triage, never auto-loads into research first passes,
    never publishes (same firewall as FD #88).
  - No invented production thresholds (FD #53): every numeric band below is
    PROPOSED for the shadow phase only — production values require Founder
    approval on validation evidence (same path as FD #89 for inflection).
  - Portfolio-blind (Constitution §23.8.1); advisory identity only.
  - Archetypes are lenses, not gates: a company may match several; the engine
    reports signals per archetype and lets the Equity Alpha Analyst (role 05)
    judge — "what deserves investigation?", not a score.
"""
from __future__ import annotations

from typing import Any, Optional

# ─────────────────────────────────────────────────────────────────────────────
# PROPOSED thresholds (FD #53 — shadow phase only, NOT production values).
# Each must be validated on historical evidence before any standing use.
# ─────────────────────────────────────────────────────────────────────────────
PROPOSED = {
    # Archetype A — Durable Compounder
    "A_ROIC_MIN": 0.15,            # ROIC >= 15% (latest year)
    "A_ROIC_5Y_MIN": 0.12,         # 5y average ROIC >= 12%
    "A_INCR_ROIC_MIN": 0.10,       # incremental ROIC >= 10% (3y change)
    "A_FCF_CONV_MIN": 0.60,        # FCF / Net income >= 60% (3y avg)
    "A_NET_DEBT_EBITDA_MAX": 2.0,  # Net debt / EBITDA <= 2.0
    # Archetype B — Long-Runway 100-Bagger
    "B_ROIC_MIN": 0.12,            # ROIC >= 12%
    "B_REINVEST_RATE_MIN": 0.50,   # reinvested earnings / net income >= 50%
    "B_REV_CAGR5_MIN": 0.15,       # 5y revenue CAGR >= 15%
    # Archetype C — Mispriced Quality
    "C_QUALITY_ROIC_MIN": 0.12,    # quality pass: ROIC >= 12%
    "C_QUALITY_FCF_POS": True,     # quality pass: positive FCF
    "C_QUALITY_NET_DEBT_EBITDA_MAX": 1.5,
    "C_PRICE_DISC_MIN": 0.25,      # valuation discount vs history >= 25%
    "C_DRAWDOWN_MIN": 0.30,        # or price -30% from 52w high
    "C_REV_NOT_SHRINKING": True,   # revenue not shrinking (quality intact)
    # Archetype D — Asymmetric Value
    "D_NET_CASH_OR_LOW_DEBT": True,      # net cash or net debt/equity < 0.3
    "D_BUYBACK_YIELD_MIN": 0.04,         # buyback yield >= 4% (TTM)
    "D_PB_MAX": 1.5,                     # P/B <= 1.5
    "D_SPECIAL_SITUATION": True,         # any of: forced sale, holding-co
                                          # discount, hidden asset, distress,
                                          # misunderstood cyclicality (flag set
                                          # by analyst judgment in recon phase)
}

ARCHETYPE_NAMES = {
    "A": "Durable Compounder",
    "B": "Long-Runway 100-Bagger",
    "C": "Mispriced Quality",
    "D": "Asymmetric Value",
}


def _f(xs: list[float]) -> Optional[float]:
    """Last non-None value, or None."""
    for x in reversed(xs):
        if x is not None:
            return float(x)
    return None


def _avg(xs: list[float]) -> Optional[float]:
    vals = [float(x) for x in xs if x is not None]
    return sum(vals) / len(vals) if vals else None


def _cagr(first: float, last: float, years: int) -> Optional[float]:
    if first is None or last is None or first <= 0 or years <= 0:
        return None
    return (last / first) ** (1 / years) - 1.0


def _as_list(series: list[float] | None) -> list[float]:
    return list(series or [])


# ── Input shape: annual_financials dict (already-fetched, per-ticker) ──
# Keys (all lists, chronological oldest→newest, same length):
#   revenue, net_income, operating_income, total_assets, total_equity,
#   total_debt, cash, ocf (operating cash flow), capex, dividends_paid,
#   buybacks_paid, ebitda
# Optional market dict (current):
#   price, eps_ttm, book_value_per_share, shares_out, market_cap,
#   price_52w_high, pe_ratio, pb_ratio, ev_ebitda, buyback_yield_ttm
# Optional recon dict (analyst judgment, Archetype D special situations):
#   special_situation: list[str]  e.g. ["forced_selling", "holding_co_discount"]


def _roic(fin: dict) -> Optional[float]:
    """ROIC = NOPAT / invested capital; NOPAT ≈ operating income * (1 - 0.21)
    (21% US statutory proxy — PROPOSED, not a company-specific tax rate)."""
    oi = _f(fin.get("operating_income", []))
    assets = _f(fin.get("total_assets", []))
    cash = _f(fin.get("cash", []))
    debt = _f(fin.get("total_debt", []))
    if oi is None or assets is None or cash is None or debt is None:
        return None
    nopat = oi * (1 - 0.21)
    invested = assets - cash  # total assets minus cash ≈ invested capital proxy
    if invested <= 0:
        return None
    return nopat / invested


def _incremental_roic(fin: dict) -> Optional[float]:
    """ΔNOPAT / Δinvested capital over the last 3 annual observations."""
    oi = _as_list(fin.get("operating_income", []))
    assets = _as_list(fin.get("total_assets", []))
    cash = _as_list(fin.get("cash", []))
    if len(oi) < 4 or len(assets) < 4 or len(cash) < 4:
        return None
    d_nopat = (oi[-1] - oi[-4]) * (1 - 0.21)
    d_inv = (assets[-1] - cash[-1]) - (assets[-4] - cash[-4])
    if d_inv <= 0:
        return None
    return d_nopat / d_inv


def _fcf_series(fin: dict) -> list[Optional[float]]:
    ocf = _as_list(fin.get("ocf", []))
    capex = _as_list(fin.get("capex", []))
    out = []
    for i in range(max(len(ocf), len(capex))):
        o = ocf[i] if i < len(ocf) else None
        c = capex[i] if i < len(capex) else None
        if o is not None and c is not None:
            out.append(o + c)  # capex negative convention → FCF = OCF + capex
        else:
            out.append(None)
    return out


def _fcf_conversion_3y(fin: dict) -> Optional[float]:
    fcf = _fcf_series(fin)
    ni = _as_list(fin.get("net_income", []))
    if len(fcf) < 3 or len(ni) < 3:
        return None
    vals = []
    for i in range(-3, 0):
        if fcf[i] is not None and ni[i] not in (None, 0):
            vals.append(fcf[i] / ni[i])
    return _avg(vals) if vals else None


def _net_debt_ebitda(fin: dict) -> Optional[float]:
    debt = _f(fin.get("total_debt", []))
    cash = _f(fin.get("cash", []))
    ebitda = _f(fin.get("ebitda", []))
    if debt is None or cash is None or ebitda in (None, 0):
        return None
    return (debt - cash) / ebitda


def _reinvestment_rate(fin: dict) -> Optional[float]:
    ni = _as_list(fin.get("net_income", []))
    div = _as_list(fin.get("dividends_paid", []))
    buy = _as_list(fin.get("buybacks_paid", []))
    if not ni or ni[-1] in (None, 0):
        return None
    latest_ni = ni[-1]
    # dividends/buybacks are negative cash flows → subtract their negative
    payout = 0.0
    if div:
        payout += abs(div[-1]) if div[-1] is not None else 0.0
    if buy:
        payout += abs(buy[-1]) if buy[-1] is not None else 0.0
    reinvest = latest_ni - payout
    return reinvest / latest_ni if latest_ni > 0 else None


def archetype_a_durable_compounder(fin: dict, market: Optional[dict] = None) -> dict:
    """A — Durable Compounder: high stable ROIC, strong FCF conversion, clean BS."""
    roic = _roic(fin)
    oi = _as_list(fin.get("operating_income", []))
    assets = _as_list(fin.get("total_assets", []))
    cash = _as_list(fin.get("cash", []))
    roic_5y = None
    if len(oi) >= 5:
        vals = []
        for i in range(-5, 0):
            o, a, c = oi[i], assets[i], cash[i]
            if o and a and c is not None and (a - c) > 0:
                vals.append(o * (1 - 0.21) / (a - c))
        roic_5y = _avg(vals) if vals else None
    incr = _incremental_roic(fin)
    fcf_conv = _fcf_conversion_3y(fin)
    nde = _net_debt_ebitda(fin)

    signals = {
        "roic_latest": roic,
        "roic_5y_avg": roic_5y,
        "incremental_roic_3y": incr,
        "fcf_conversion_3y_avg": fcf_conv,
        "net_debt_ebitda": nde,
    }
    checks = {
        "roic_latest >= A_ROIC_MIN": roic is not None and roic >= PROPOSED["A_ROIC_MIN"],
        "roic_5y_avg >= A_ROIC_5Y_MIN": roic_5y is not None and roic_5y >= PROPOSED["A_ROIC_5Y_MIN"],
        "incremental_roic >= A_INCR_ROIC_MIN": incr is not None and incr >= PROPOSED["A_INCR_ROIC_MIN"],
        "fcf_conversion >= A_FCF_CONV_MIN": fcf_conv is not None and fcf_conv >= PROPOSED["A_FCF_CONV_MIN"],
        "net_debt/ebitda <= A_NET_DEBT_EBITDA_MAX": nde is not None and nde <= PROPOSED["A_NET_DEBT_EBITDA_MAX"],
    }
    return {
        "archetype": "A",
        "name": ARCHETYPE_NAMES["A"],
        "signals": signals,
        "checks": checks,
        "matched_count": sum(1 for v in checks.values() if v),
        "proposed": True,  # FD #53: thresholds are PROPOSED, not production
        "as_of": "annual financials as fetched (FD #58 — re-verify before use)",
    }


def archetype_b_long_runway(fin: dict, market: Optional[dict] = None) -> dict:
    """B — Long-Runway 100-Bagger: high ROIC × high reinvestment × growth."""
    roic = _roic(fin)
    reinv = _reinvestment_rate(fin)
    rev = _as_list(fin.get("revenue", []))
    rev_cagr5 = _cagr(rev[0], rev[-1], 5) if len(rev) >= 6 else None

    signals = {
        "roic_latest": roic,
        "reinvestment_rate_latest": reinv,
        "revenue_cagr_5y": rev_cagr5,
    }
    checks = {
        "roic >= B_ROIC_MIN": roic is not None and roic >= PROPOSED["B_ROIC_MIN"],
        "reinvestment_rate >= B_REINVEST_RATE_MIN": reinv is not None and reinv >= PROPOSED["B_REINVEST_RATE_MIN"],
        "revenue_cagr5 >= B_REV_CAGR5_MIN": rev_cagr5 is not None and rev_cagr5 >= PROPOSED["B_REV_CAGR5_MIN"],
    }
    return {
        "archetype": "B",
        "name": ARCHETYPE_NAMES["B"],
        "signals": signals,
        "checks": checks,
        "matched_count": sum(1 for v in checks.values() if v),
        "proposed": True,
        "as_of": "annual financials as fetched (FD #58 — re-verify before use)",
    }


def archetype_c_mispriced_quality(fin: dict, market: Optional[dict] = None) -> dict:
    """C — Mispriced Quality: great business + market doubt (valuation/drawdown)."""
    roic = _roic(fin)
    fcf = _fcf_series(fin)
    fcf_pos = bool(fcf and _f(fcf) is not None and _f(fcf) > 0)
    nde = _net_debt_ebitda(fin)
    rev = _as_list(fin.get("revenue", []))
    rev_not_shrinking = bool(rev and len(rev) >= 2 and rev[-1] >= rev[-2])

    market = market or {}
    pe = market.get("pe_ratio")
    ev_ebitda = market.get("ev_ebitda")
    drawdown = None
    price = market.get("price")
    high = market.get("price_52w_high")
    if price and high and high > 0:
        drawdown = (high - price) / high
    # valuation discount vs history — needs a 5y multiple history; when absent,
    # the engine reports it as UNAVAILABLE (honest empty, like CIW practice).
    val_discount = market.get("valuation_discount_vs_5y_median")

    quality_pass = (
        roic is not None and roic >= PROPOSED["C_QUALITY_ROIC_MIN"]
        and fcf_pos
        and (nde is None or nde <= PROPOSED["C_QUALITY_NET_DEBT_EBITDA_MAX"])
        and rev_not_shrinking
    )
    mispricing = (
        (val_discount is not None and val_discount >= PROPOSED["C_PRICE_DISC_MIN"])
        or (drawdown is not None and drawdown >= PROPOSED["C_DRAWDOWN_MIN"])
    )

    signals = {
        "roic_latest": roic,
        "fcf_latest_positive": fcf_pos,
        "net_debt_ebitda": nde,
        "revenue_not_shrinking": rev_not_shrinking,
        "drawdown_from_52w_high": drawdown,
        "valuation_discount_vs_5y_median": val_discount,
        "pe_ratio": pe,
        "ev_ebitda": ev_ebitda,
    }
    checks = {
        "quality_pass (roic+fcf+debt+rev)": quality_pass,
        "mispricing (discount>=25% OR drawdown>=30%)": mispricing,
    }
    return {
        "archetype": "C",
        "name": ARCHETYPE_NAMES["C"],
        "signals": signals,
        "checks": checks,
        "quality_pass": quality_pass,
        "mispricing": mispricing,
        "matched_count": int(quality_pass) + int(mispricing),
        "proposed": True,
        "as_of": "annual financials + market snapshot as fetched (FD #58)",
    }


def archetype_d_asymmetric_value(fin: dict, market: Optional[dict] = None,
                                 recon: Optional[dict] = None) -> dict:
    """D — Asymmetric Value: limited permanent downside + large upside."""
    debt = _f(fin.get("total_debt", []))
    cash = _f(fin.get("cash", []))
    equity = _f(fin.get("total_equity", []))
    net_cash = (debt is not None and cash is not None and cash >= debt)
    nd_e = None
    if debt is not None and cash is not None and equity not in (None, 0):
        nd_e = (debt - cash) / equity

    market = market or {}
    recon = recon or {}
    buyback_yield = market.get("buyback_yield_ttm")
    pb = market.get("pb_ratio")
    special = recon.get("special_situation", [])

    signals = {
        "net_cash": net_cash,
        "net_debt_equity": nd_e,
        "buyback_yield_ttm": buyback_yield,
        "pb_ratio": pb,
        "special_situations": special,
    }
    checks = {
        "net cash or low leverage": net_cash or (nd_e is not None and nd_e < 0.3),
        "buyback_yield >= D_BUYBACK_YIELD_MIN": buyback_yield is not None and buyback_yield >= PROPOSED["D_BUYBACK_YIELD_MIN"],
        "pb <= D_PB_MAX": pb is not None and pb <= PROPOSED["D_PB_MAX"],
        "special situation flagged": bool(special),
    }
    return {
        "archetype": "D",
        "name": ARCHETYPE_NAMES["D"],
        "signals": signals,
        "checks": checks,
        "matched_count": sum(1 for v in checks.values() if v),
        "proposed": True,
        "as_of": "annual financials + market snapshot as fetched (FD #58)",
    }


def scan_ticker(ticker: str, fin: dict, market: Optional[dict] = None,
                recon: Optional[dict] = None) -> dict:
    """Run all four archetype lenses on one ticker → evidence block.

    Firewall (same as FD #88): output is deterministic evidence ONLY. No cards,
    no CoS, no research capacity consumed. The Equity Alpha Analyst (role 05)
    judges which signals deserve a Task Idea Card in the recon phase.
    """
    return {
        "ticker": ticker,
        "archetypes": [
            archetype_a_durable_compounder(fin, market),
            archetype_b_long_runway(fin, market),
            archetype_c_mispriced_quality(fin, market),
            archetype_d_asymmetric_value(fin, market, recon),
        ],
        "proposed": True,  # FD #53 — all thresholds PROPOSED (shadow phase)
        "firewall": "evidence only — no card, no CoS, no research, no publish (FD #88 pattern)",
    }


def run_shadow(tickers: dict[str, dict]) -> list[dict]:
    """Shadow run over a dict of ticker → {fin, market?, recon?}.

    Returns a list of evidence blocks (one per ticker). Never writes cards.
    """
    out = []
    for ticker, payload in tickers.items():
        fin = payload.get("fin", {})
        market = payload.get("market")
        recon = payload.get("recon")
        out.append(scan_ticker(ticker, fin, market, recon))
    return out
