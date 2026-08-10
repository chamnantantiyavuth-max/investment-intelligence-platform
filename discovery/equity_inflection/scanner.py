"""Equity Inflection Discovery — deterministic scanner (FD #88, shadow phase).

PURE DETERMINISTIC LOGIC ONLY — no yfinance/numpy at import time (the pytest
venv is Python 3.11 and lacks a working yfinance/numpy; the data-fetch layer
runs under system Python 3.14). This module operates on already-fetched
quarterly + daily series dicts so every invariant is unit-testable.

Boundaries (FD #88, binding):
  - Scanner output = deterministic evidence block ONLY. It NEVER creates a
    Task Idea Card, never enters CoS triage, never auto-loads into research
    first passes (FD #64 item 7), never publishes.
  - Enrichment signals are ADVISORY — they never gate eligibility.
  - Every signal carries an as-of availability stamp (FD #58).
  - No invented production thresholds (FD #53): the numeric bands below are
    PRODUCTION values from Stage Definition v0.1, approved by FD #89 (10 Aug 2026)
    on validation Phase 1 evidence (see output/validation-2026-08-10/).
"""
from __future__ import annotations

from typing import Any

# ── PRODUCTION parameters (FD #89, 10 Aug 2026 — approved on validation evidence) ──
H1_TTM_WINDOW_QUARTERS = 4        # TTM = trailing 4 quarters
H1_PRIOR_WINDOW_QUARTERS = 8      # comparison = prior 8 quarters (~2 years)
H2_PRIOR_WINDOW_QUARTERS = 8      # YoY-growth comparison window
MIN_QUARTERS_FOR_SCAN = 9         # 4 (TTM anchor) + 8 (prior window) - 3 overlap guard
MIN_PRICE_SESSIONS = 200          # stage signature needs 150MA (150) + slope lookback

# Stage Def v0.1 bands (PRODUCTION — FD #89)
STAGE1_PRICE_BAND = 0.05          # price within ±5% of 50MA
STAGE1_MA_BAND = 0.05             # 50MA within ±5% of 150MA
STAGE1_SLOPE_PCT_MONTH = 0.5      # |slope| < 0.5%/month (≈21 sessions)
STAGE1_RANGE_LOW, STAGE1_RANGE_HIGH = 0.30, 0.70   # 52-week range band
EARLY_S2_MAX_EXTENSION = 0.15     # price ≤ ~15% above 50MA
EARLY_S2_MAX_WEEKS = 8            # ≤ ~8 weeks since crossing above both MAs
EARLY_S2_MAX_SESSIONS = EARLY_S2_MAX_WEEKS * 5     # 5 sessions/week proxy
LATE_S2_EXTENSION_HARD = 0.20     # >20% above 50MA = clearly late
SESSION_MONTH = 21                # trading sessions ≈ 1 month


def _last(xs: list) -> Any:
    return xs[-1]


# ── H1: TTM EPS level breakout ───────────────────────────────────────────────

def _ttm_eps(quarters: list[dict], end_idx: int) -> float:
    """Trailing-4-quarter diluted EPS sum ending at end_idx (inclusive)."""
    return sum(float(q["eps_diluted"]) for q in quarters[end_idx - H1_TTM_WINDOW_QUARTERS + 1: end_idx + 1])


def earnings_breakout_h1(quarters: list[dict]) -> dict:
    """Hypothesis 1 — EPS-LEVEL breakout: latest TTM EPS > max TTM of the
    prior 8 quarters. Uses availability stamps as as-of (FD #58).

    Returns {"hypothesis": "H1", "signal": bool, "latest_ttm_eps": float,
             "prior_max_ttm_eps": float, "as_of": str, "quarters_used": int}
    """
    if len(quarters) < MIN_QUARTERS_FOR_SCAN:
        return {"hypothesis": "H1", "signal": False,
                "reason": f"insufficient quarterly history ({len(quarters)} < {MIN_QUARTERS_FOR_SCAN})",
                "as_of": quarters[-1]["eps_available_at"] if quarters else None,
                "quarters_used": len(quarters)}
    latest = len(quarters) - 1
    latest_ttm = _ttm_eps(quarters, latest)
    # prior window = the 8 quarters IMMEDIATELY before the latest (2-year
    # lookback), never the whole history — stale/pre-split values far in the
    # past must not suppress the signal (split-adjusted series assumed)
    prior_start = max(0, latest - H1_PRIOR_WINDOW_QUARTERS)
    prior_max = max(_ttm_eps(quarters, i) for i in range(prior_start, latest))
    return {
        "hypothesis": "H1",
        "signal": latest_ttm > prior_max,
        "latest_ttm_eps": round(latest_ttm, 6),
        "prior_max_ttm_eps": round(prior_max, 6),
        "as_of": quarters[latest]["eps_available_at"],
        "quarters_used": len(quarters),
    }


# ── H2: YoY growth-rate acceleration ─────────────────────────────────────────

def _yoy_growth(quarters: list[dict], idx: int) -> float:
    """YoY growth of quarter idx vs its year-ago quarter. Negative-base -> None-safe."""
    base_idx = idx - 4
    if base_idx < 0:
        return None
    base = float(quarters[base_idx]["eps_diluted"])
    cur = float(quarters[idx]["eps_diluted"])
    if base == 0:
        return None
    return (cur - base) / abs(base)


def earnings_breakout_h2(quarters: list[dict]) -> dict:
    """Hypothesis 2 — EPS-GROWTH-RATE acceleration: latest-quarter YoY growth
    above the max YoY growth of the prior 8 comparable quarters. Computed
    independently of H1 (hypothesis separation, FD #88).

    Returns {"hypothesis": "H2", "signal": bool, "latest_yoy": float|None,
             "prior_max_yoy": float|None, "as_of": str, "quarters_used": int}
    """
    if len(quarters) < MIN_QUARTERS_FOR_SCAN:
        return {"hypothesis": "H2", "signal": False,
                "reason": f"insufficient quarterly history ({len(quarters)} < {MIN_QUARTERS_FOR_SCAN})",
                "as_of": quarters[-1]["eps_available_at"] if quarters else None,
                "quarters_used": len(quarters)}
    latest = len(quarters) - 1
    latest_yoy = _yoy_growth(quarters, latest)
    # prior window = 8 comparable quarters immediately before latest
    prior_start = max(0, latest - H2_PRIOR_WINDOW_QUARTERS)
    prior_yoy = [_yoy_growth(quarters, i) for i in range(prior_start, latest)]
    prior_max = max((v for v in prior_yoy if v is not None), default=None)
    signal = False
    if latest_yoy is not None and prior_max is not None:
        signal = latest_yoy > prior_max
    return {
        "hypothesis": "H2",
        "signal": signal,
        "latest_yoy": round(latest_yoy, 6) if latest_yoy is not None else None,
        "prior_max_yoy": round(prior_max, 6) if prior_max is not None else None,
        "as_of": quarters[latest]["eps_available_at"],
        "quarters_used": len(quarters),
    }


# ── revenue confirmation ─────────────────────────────────────────────────────

def revenue_confirmation(quarters: list[dict]) -> dict:
    """Latest-quarter revenue must NOT be shrinking YoY (revenue >= year-ago
    quarter). Rising EPS with shrinking revenue = buyback/one-off filter
    (Approved Spec v0.2). Returns {"confirmed": bool, "latest_revenue",
    "year_ago_revenue", "yoy_pct", "as_of"}.
    """
    latest = len(quarters) - 1
    base_idx = latest - 4
    if base_idx < 0:
        return {"confirmed": False, "reason": "insufficient revenue history",
                "as_of": quarters[latest]["revenue_available_at"]}
    cur = float(quarters[latest]["revenue"])
    base = float(quarters[base_idx]["revenue"])
    yoy = (cur - base) / abs(base) if base != 0 else None
    return {
        "confirmed": (yoy is not None and yoy >= 0) if base != 0 else False,
        "latest_revenue": round(cur, 4),
        "year_ago_revenue": round(base, 4),
        "yoy_pct": round(yoy * 100, 4) if yoy is not None else None,
        "as_of": quarters[latest]["revenue_available_at"],
    }


# ── stage signature (Stage Def v0.1, deterministic) ──────────────────────────

def _ma(closes: list[float], n: int, end_idx: int) -> float | None:
    if end_idx + 1 < n:
        return None
    return sum(closes[end_idx - n + 1: end_idx + 1]) / n


def stage_signature(prices: list[dict]) -> dict:
    """Deterministic stage classification per Stage Def v0.1.

    Returns {"stage": "S1"|"S2-early"|"S2-late"|"S3"|"S4"|"UNCLASSIFIED",
             "eligible": bool, "details": {...}, "as_of": str}
    """
    if len(prices) < MIN_PRICE_SESSIONS:
        return {"stage": "UNCLASSIFIED", "eligible": False,
                "reason": f"insufficient price history ({len(prices)} < {MIN_PRICE_SESSIONS})",
                "as_of": prices[-1]["date"] if prices else None, "details": {}}
    closes = [float(p["close"]) for p in prices]
    last = len(closes) - 1
    close = closes[last]
    ma50 = _ma(closes, 50, last)
    ma150 = _ma(closes, 150, last)
    ma50_20 = _ma(closes, 50, last - SESSION_MONTH)      # 50MA ~1 month ago
    ma150_60 = _ma(closes, 150, last - 3 * SESSION_MONTH)  # 150MA ~3 months ago
    slope50 = ((ma50 - ma50_20) / ma50_20 * 100) if (ma50 is not None and ma50_20 and ma50_20 > 0) else None
    slope150 = ((ma150 - ma150_60) / ma150_60 * 100) if (ma150 is not None and ma150_60 and ma150_60 > 0) else None

    # 52-week range position
    year_win = closes[-252:] if len(closes) >= 252 else closes
    hi, lo = max(year_win), min(year_win)
    range_pos = (close - lo) / (hi - lo) if hi > lo else None

    details = {
        "close": round(close, 4), "ma50": round(ma50, 4) if ma50 else None,
        "ma150": round(ma150, 4) if ma150 else None,
        "slope50_pct_month": round(slope50, 4) if slope50 is not None else None,
        "slope150_pct_month": round(slope150, 4) if slope150 is not None else None,
        "range_position": round(range_pos, 4) if range_pos is not None else None,
    }

    if close < ma50 and close < ma150 and ma50 < ma150 and slope150 is not None and slope150 < 0:
        return {"stage": "S4", "eligible": False, "details": details, "as_of": prices[last]["date"]}
    # S3: death-cross zone (50MA materially below 150MA) OR price broken below
    # 50MA while 150MA not yet rising — topping/distribution, NOT confirmed downtrend
    if (ma50 is not None and ma150 is not None and ma50 < ma150 * 0.98) or \
       (close < ma50 and (slope150 is not None and slope150 <= 0)):
        return {"stage": "S3", "eligible": False, "details": details, "as_of": prices[last]["date"]}

    if close > ma50 and close > ma150 and ma50 > ma150 and slope50 is not None and slope50 > 0 and slope150 is not None and slope150 > 0:
        extension = (close - ma50) / ma50
        # weeks since price first crossed above both MAs (consecutive streak)
        streak = 0
        for i in range(last, -1, -1):
            c = closes[i]
            m50 = _ma(closes, 50, i)
            m150 = _ma(closes, 150, i)
            if m50 is None or m150 is None:
                break
            if c > m50 and c > m150:
                streak += 1
            else:
                break
        weeks_since_cross = streak / 5.0
        early = extension <= EARLY_S2_MAX_EXTENSION and weeks_since_cross <= EARLY_S2_MAX_WEEKS
        details.update({"extension_above_ma50_pct": round(extension * 100, 4),
                        "weeks_since_cross": round(weeks_since_cross, 2),
                        "late_by_extension": extension > LATE_S2_EXTENSION_HARD,
                        "late_by_time": weeks_since_cross > EARLY_S2_MAX_WEEKS})
        if early:
            return {"stage": "S2-early", "eligible": True, "details": details, "as_of": prices[last]["date"]}
        return {"stage": "S2-late", "eligible": False, "details": details, "as_of": prices[last]["date"]}

    # Stage 1: basing
    if ma50 and ma150 and slope50 is not None and slope150 is not None and range_pos is not None:
        near_ma50 = abs(close - ma50) / ma50 <= STAGE1_PRICE_BAND
        ma_close = abs(ma50 - ma150) / ma150 <= STAGE1_MA_BAND
        flat = abs(slope50) < STAGE1_SLOPE_PCT_MONTH and abs(slope150) < STAGE1_SLOPE_PCT_MONTH
        mid_range = STAGE1_RANGE_LOW <= range_pos <= STAGE1_RANGE_HIGH
        if near_ma50 and ma_close and flat and mid_range:
            return {"stage": "S1", "eligible": True, "details": details, "as_of": prices[last]["date"]}

    return {"stage": "UNCLASSIFIED", "eligible": False, "details": details, "as_of": prices[last]["date"]}


# ── liquidity sanity ─────────────────────────────────────────────────────────

def liquidity_sanity(meta: dict | None) -> dict:
    """Data/liquidity sanity: price floor + volume floor (production values,
    FD #89). meta: {"price": float, "avg_volume_50d": float} or None.
    """
    if not meta:
        return {"ok": False, "reason": "no liquidity data", "as_of": None}
    price = float(meta.get("price") or 0)
    vol = float(meta.get("avg_volume_50d") or 0)
    ok = price >= 2.0 and vol >= 100_000
    return {"ok": ok, "price": round(price, 2), "avg_volume_50d": vol,
            "reasons": [] if ok else [f"price ${price:.2f} < $2 or volume {vol:.0f} < 100k"],
            "as_of": meta.get("as_of")}


# ── enrichment (ADVISORY, never gating) ──────────────────────────────────────

def enrichment_signals(prices: list[dict], enrichment: dict | None = None) -> dict:
    """Advisory enrichment signals. Computed or passed-through — NEVER gates.
    Passed-in values override computed ones (so callers may supply RS
    percentile etc. from external sources)."""
    out = {
        "rs_percentile": None, "volume_trend": None, "extension_context": None,
        "advisory_only": True,
    }
    if enrichment:
        out.update({k: v for k, v in enrichment.items() if k in out})
    return out


def split_adjust(series: list[dict], share_series: list[dict]) -> list[dict]:
    """Adjust a value series for stock splits using DilutedAverageShares.

    companyfacts reports EPS AS FILED — pre-split quarters carry the old
    share basis (e.g. NVDA 10:1 split Jun-2024: pre-split EPS ~10x too high
    vs current basis). Detects a split when consecutive quarterly share
    counts jump by >= 1.5x and scales all EARLIER values by the ratio
    (old_shares/new_shares) so the whole series is on the current basis.

    Returns a new list of dicts with 'value' adjusted, preserving
    period_end/filed/derived. series and share_series must be chronological
    (period_end ascending). Values without a share match are left unchanged.
    """
    if len(series) < 2:
        return list(series)
    shares = {s["period_end"]: s["value"] for s in share_series}
    out = []
    factor = 1.0
    prev_shares = None
    # iterate NEWEST -> OLDEST so the factor compounds correctly
    for x in reversed(series):
        sh = shares.get(x["period_end"])
        if sh is not None and prev_shares is not None and prev_shares > 0:
            ratio = prev_shares / sh
            if ratio >= 1.5:  # split boundary (newer share count >> older)
                factor /= ratio  # earlier (old-basis) EPS scales DOWN to current basis
        out.append({
            "period_end": x["period_end"],
            "value": round(x["value"] * factor, 6),
            "filed": x["filed"],
            "derived": bool(x.get("derived")),
            "split_factor": round(factor, 6),
        })
        if sh is not None:
            prev_shares = sh
    out.reverse()
    return out


# ── assembly ─────────────────────────────────────────────────────────────────

def scan_ticker(ticker: str, quarters: list[dict], prices: list[dict],
                meta: dict | None = None, enrichment: dict | None = None) -> dict:
    """Assemble a candidate record for one ticker (shadow mode).

    Eligibility (shadow): H1 (core, per design Option 1) AND revenue
    confirmation AND stage.eligible AND liquidity ok. H2 is reported as an
    independent enrichment-class signal (hypothesis separation — combination
    decision deferred, FD #88). Enrichment dict NEVER affects eligibility.
    """
    h1 = earnings_breakout_h1(quarters)
    h2 = earnings_breakout_h2(quarters)
    rev = revenue_confirmation(quarters)
    stage = stage_signature(prices)
    liq = liquidity_sanity(meta)
    adv = enrichment_signals(prices, enrichment)

    reasons = []
    if not h1["signal"]:
        reasons.append(f"H1 (TTM EPS level breakout) not fired — {h1.get('reason', 'latest TTM below prior max')}")
    if not rev["confirmed"]:
        reasons.append(f"revenue confirmation failed — {rev.get('reason', 'revenue shrinking YoY')}")
    if not stage["eligible"]:
        reasons.append(f"stage {stage['stage']} not eligible")
    if not liq["ok"]:
        reasons.extend(liq.get("reasons", ["liquidity sanity failed"]))

    eligible = h1["signal"] and rev["confirmed"] and stage["eligible"] and liq["ok"]

    return {
        "ticker": ticker,
        "eligible": eligible,
        "reasons": reasons,
        "signals": {"h1": h1, "h2": h2, "revenue": rev},
        "stage": stage,
        "liquidity": liq,
        "enrichment": adv,
        "as_of": {
            "price_as_of": prices[-1]["date"] if prices else None,
            "quarters_as_of": quarters[-1]["eps_available_at"] if quarters else None,
            "source": "yfinance (shadow fetch) / constructed",
        },
        "firewall": "discovery evidence block — no card, no CoS triage, no research load (FD #88)",
    }


def run_shadow(tickers: dict[str, dict]) -> list[dict]:
    """Shadow run over a payload map {ticker: {"quarters": [...], "prices": [...],
    "meta": {...}, "enrichment": {...}}}. Returns candidate records. NO cards."""
    out = []
    for ticker, payload in sorted(tickers.items()):
        try:
            out.append(scan_ticker(ticker, payload.get("quarters", []),
                                   payload.get("prices", []),
                                   payload.get("meta"), payload.get("enrichment")))
        except Exception as e:  # honest per-ticker failure, never fabricate
            out.append({"ticker": ticker, "eligible": False,
                        "reasons": [f"scan error: {type(e).__name__}: {e}"],
                        "as_of": None})
    return out
