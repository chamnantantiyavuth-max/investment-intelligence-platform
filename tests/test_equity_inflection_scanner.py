"""Locked-style deterministic invariants — Equity Inflection Discovery Scanner (FD #88, shadow phase).

Charter (per docs/PLAN-EQUITY-INFLECTION-SHADOW-SCANNER-v0.1.md §5):
  1. Breakout math — H1 (TTM EPS level) and H2 (YoY growth-rate) computed INDEPENDENTLY;
     a case where H1 fires but H2 does not (and vice versa) must exist (hypothesis separation).
  2. Revenue confirmation — latest-quarter revenue must not be shrinking (YoY >= 0);
     rising EPS with shrinking revenue = NOT confirmed (buyback/one-off filter).
  3. Stage classification — constructed price series classify per Stage Def v0.1:
     S4 excluded, S3 excluded, S1 eligible (watch), S2-early eligible, S2-late excluded.
  4. Empty-output honesty — insufficient quarters/price history -> no candidate + explicit
     reason; never a fabricated signal (DNA-016).
  5. PIT stamp presence — every computed signal carries an as-of availability stamp (FD #58).
  6. Enrichment never gates — varying advisory enrichment (RS percentile, volume trend) does
     NOT change eligibility (FD #88: enrichment signals advisory only).

Pure deterministic logic ONLY — no yfinance/numpy at import (pytest venv is 3.11;
scanner data layer runs under system Python 3.14). Do NOT modify expected values without
an FD (Acceptance Lock Rule, FD-108).
"""
from __future__ import annotations

import pytest

from discovery.equity_inflection import scanner as s

# ── helpers: synthetic quarterly + price series ──────────────────────────────

def mk_quarters(eps_list, revenue_list=None, base_date="2023-06-30"):
    """Build chronological quarterly dicts. eps_list/revenue_list same length (>=13)."""
    revenue_list = revenue_list or [100.0 + i for i in range(len(eps_list))]
    out = []
    y, q = int(base_date[:4]), int(base_date[5:7])
    for i, (eps, rev) in enumerate(zip(eps_list, revenue_list)):
        out.append({
            "period_end": f"{y}-{q:02d}-30",
            "eps_diluted": eps,
            "revenue": rev,
            "eps_available_at": f"{y}-{q:02d}-05",   # availability AFTER the quarter
            "revenue_available_at": f"{y}-{q:02d}-05",
        })
        q += 1
        if q > 4:
            q = 1
            y += 1
    return out


def mk_prices(closes, start_date="2025-01-02", volume=1_000_000):
    """Build daily price series [{date, close, volume}] from a close list."""
    from datetime import date, timedelta
    d = date.fromisoformat(start_date)
    out = []
    for i, c in enumerate(closes):
        out.append({"date": str(d + timedelta(days=i)), "close": c, "volume": volume})
    return out


def flat_base(n, level=100.0, noise=0.02):
    """Deterministic basing series: sine oscillation that ENDS at the level
    (sin(0) at the last point -> close == level -> mid 52-week range, stable
    Stage-1 classification). No RNG."""
    import math
    return [level * (1 + (noise / 2.0) * math.sin((i - (n - 1)) / 5.0)) for i in range(n)]


# ── 1. hypothesis separation ─────────────────────────────────────────────────

def test_h1_ttm_level_breakout_positive():
    """Latest TTM EPS above the max TTM of the prior 8 quarters -> H1 fires."""
    # steady climb: each quarter +5% from 1.00; 13 quarters (4 TTM anchor + 8 window + latest)
    eps = [1.00 * (1.05 ** i) for i in range(13)]
    q = mk_quarters(eps)
    r = s.earnings_breakout_h1(q)
    assert r["signal"] is True
    assert r["hypothesis"] == "H1"
    assert r["latest_ttm_eps"] > r["prior_max_ttm_eps"]


def test_h1_no_breakout_within_range():
    """Latest TTM EPS below the 2-year max -> H1 does NOT fire."""
    eps = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
    r = s.earnings_breakout_h1(mk_quarters(eps))
    assert r["signal"] is False
    assert r["latest_ttm_eps"] <= r["prior_max_ttm_eps"]


def test_h2_yoy_acceleration_positive():
    """Latest-quarter YoY growth above the prior 8-quarter YoY range -> H2 fires."""
    # flat ~1.0 for 8 quarters, then 1.6 (first real jump): YoY jump, acceleration
    eps = [1.0] * 8 + [1.0, 1.0, 1.05, 1.6, 1.75]
    r = s.earnings_breakout_h2(mk_quarters(eps))
    assert r["signal"] is True
    assert r["hypothesis"] == "H2"
    assert r["latest_yoy"] > r["prior_max_yoy"]


def test_hypotheses_can_fire_independently():
    """A case where H1 fires but H2 does not (steady TTM climb, declining YoY)."""
    # steady 5%/q climb: TTM new high every quarter (H1 True) but YoY growth is
    # monotonically ~5% and latest YoY is NOT above its own prior range (H2 False)
    eps = [1.00 * (1.05 ** i) for i in range(13)]
    q = mk_quarters(eps)
    h1 = s.earnings_breakout_h1(q)
    h2 = s.earnings_breakout_h2(q)
    assert h1["signal"] is True
    assert h2["signal"] is False
    # and the reverse: a low-base spike makes H2 fire while TTM stays under an old max
    # indices 0-7 = 2.0 (old max TTM = 8.0), then dip to 0.3, recovery 0.35/1.6/2.2:
    # latest YoY = (2.2-0.3)/0.3 = +633% vs prior window max 0% -> H2 True;
    # latest TTM = 0.3+0.35+1.6+2.2 = 4.45 < prior max 8.0 -> H1 False
    eps2 = [2.0] * 8 + [0.3, 0.3, 0.35, 1.6, 2.2]
    q2 = mk_quarters(eps2)
    r1 = s.earnings_breakout_h1(q2)
    r2 = s.earnings_breakout_h2(q2)
    assert r2["signal"] is True
    assert r1["signal"] is False


def test_h1_prior_window_ignores_stale_history():
    """The prior window is the 8 quarters BEFORE latest — stale/pre-split
    values far in the past must NOT suppress the signal (real-data bug found
    in the 2026-08-10 shadow run: pre-split 2011 EPS inflated prior_max)."""
    # 40 quarters of ancient high EPS (stale era), then 13 quarters of steady
    # growth — latest TTM must fire because the stale era is outside the window
    stale = [5.0] * 40
    recent = [1.00 * (1.05 ** i) for i in range(13)]
    q = mk_quarters(stale + recent)
    h1 = s.earnings_breakout_h1(q)
    assert h1["signal"] is True
    # the prior window's max TTM (quarter before latest) is ~6.37 from steady
    # growth — never a stale-era 20.0 (= 4 x 5.0) leaking in
    assert h1["prior_max_ttm_eps"] < 7.0


def test_split_adjust_scales_old_basis_down():
    """Pre-split EPS must scale DOWN to the current share basis (NVDA 10:1
    pattern: old-basis EPS ~10x too high)."""
    from discovery.equity_inflection import scanner as s2
    # chronological ascending: 4 PRE-split quarters (shares 1B) then 4
    # POST-split quarters (shares 10B) — split boundary between 2024-Q3/2025-Q0
    eps = ([{"period_end": f"2024-Q{i}", "value": 6.0, "filed": "d"} for i in range(4)] +
           [{"period_end": f"2025-Q{i}", "value": 1.0, "filed": "d"} for i in range(4)])
    shares = ([{"period_end": f"2024-Q{i}", "value": 1.0, "filed": "d"} for i in range(4)] +
              [{"period_end": f"2025-Q{i}", "value": 10.0, "filed": "d"} for i in range(4)])
    adj = s2.split_adjust(eps, shares)
    # pre-split quarters scaled down by 10x to current basis
    assert adj[0]["value"] == 0.6 and adj[3]["value"] == 0.6
    assert adj[0]["split_factor"] == 0.1
    # post-split quarters unchanged (factor 1.0)
    assert adj[-1]["value"] == 1.0 and adj[-4]["value"] == 1.0
    assert adj[-1]["split_factor"] == 1.0


# ── 2. revenue confirmation ──────────────────────────────────────────────────

def test_revenue_confirmation_pass_when_not_shrinking():
    q = mk_quarters([1.0] * 13, revenue_list=[100 + i for i in range(13)])
    r = s.revenue_confirmation(q)
    assert r["confirmed"] is True


def test_revenue_confirmation_fails_when_shrinking():
    """EPS rising (buyback-driven) but revenue shrinking -> NOT confirmed."""
    q = mk_quarters([1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2],
                    revenue_list=[100, 101, 100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90])
    r = s.revenue_confirmation(q)
    assert r["confirmed"] is False


# ── 3. stage classification (Stage Def v0.1) ─────────────────────────────────

def test_stage4_declining_excluded():
    closes = [100 * (0.995 ** i) for i in range(260)]
    st = s.stage_signature(mk_prices(closes))
    assert st["stage"] == "S4"
    assert st["eligible"] is False


def test_stage3_topping_excluded():
    # strong rise (190d) then moderate fall (70d @0.997): 50MA crosses below
    # 150MA while the 150MA slope is still positive -> topping, NOT confirmed
    # downtrend (S4 requires 150MA sloping down)
    closes = [100 * (1.003 ** i) for i in range(190)] + \
             [176.6 * (0.997 ** i) for i in range(70)]
    st = s.stage_signature(mk_prices(closes))
    assert st["stage"] == "S3"
    assert st["eligible"] is False


def test_stage1_basing_eligible():
    closes = flat_base(260, level=100.0)
    st = s.stage_signature(mk_prices(closes))
    assert st["stage"] == "S1"
    assert st["eligible"] is True


def test_stage2_early_eligible():
    # flat base 220 days then ~30-day rise: recent cross above both MAs, small
    # extension; base length >= 213 so the 150MA 3-month-ago slope is computable
    closes = flat_base(220, level=100.0) + [100 * (1.003 ** i) for i in range(30)]
    st = s.stage_signature(mk_prices(closes))
    assert st["stage"] == "S2-early"
    assert st["eligible"] is True


def test_stage2_late_excluded():
    # long uptrend: above both MAs for >8 weeks -> late, excluded
    closes = flat_base(120, level=100.0) + [100 * (1.003 ** i) for i in range(140)]
    st = s.stage_signature(mk_prices(closes))
    assert st["stage"] == "S2-late"
    assert st["eligible"] is False


# ── 4. empty-output honesty ──────────────────────────────────────────────────

def test_insufficient_quarters_no_candidate():
    q = mk_quarters([1.0] * 6)  # too few quarters
    res = s.scan_ticker("TEST", q, mk_prices(flat_base(260)))
    assert res["eligible"] is False
    assert any("quarter" in r.lower() for r in res["reasons"])


def test_insufficient_price_history_unclassified():
    q = mk_quarters([1.0 + 0.05 * i for i in range(13)])
    res = s.scan_ticker("TEST", q, mk_prices([100.0] * 50))  # <200 sessions
    assert res["eligible"] is False
    assert res["stage"]["stage"] == "UNCLASSIFIED"
    assert res["reasons"]


# ── 5. PIT stamps ────────────────────────────────────────────────────────────

def test_pit_stamp_presence():
    eps = [1.00 * (1.05 ** i) for i in range(13)]
    q = mk_quarters(eps)
    res = s.scan_ticker("TEST", q, mk_prices(flat_base(260)))
    assert res["as_of"]  # non-empty availability stamp block
    assert res["signals"]["h1"]["as_of"]
    assert res["signals"]["h2"]["as_of"]


# ── 6. enrichment never gates ────────────────────────────────────────────────

def test_enrichment_never_gates():
    eps = [1.00 * (1.05 ** i) for i in range(13)]
    q = mk_quarters(eps)
    prices = mk_prices(flat_base(260))
    meta = {"price": 100.0, "avg_volume_50d": 1_000_000, "as_of": "2025-12-31"}
    base = s.scan_ticker("TEST", q, prices, meta, enrichment={"rs_percentile": 50, "volume_trend": 0.0})
    # hostile enrichment values: terrible RS, falling volume, extreme extension context
    hostile = s.scan_ticker("TEST", q, prices, meta, enrichment={"rs_percentile": 1, "volume_trend": -0.5})
    assert base["eligible"] == hostile["eligible"]
    assert base["eligible"] is True   # S1 + breakout + revenue confirmed + liquid -> eligible regardless
