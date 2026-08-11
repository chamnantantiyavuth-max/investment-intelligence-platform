"""Locked-style tests — Quality & Asymmetry fetcher annual extraction (WP2).

The fetcher needs yfinance/numpy (system python only), so these tests exercise
the PURE extraction helpers directly (they don't import yfinance):

  1. Flow tags: merged candidate tags survive tag switches (NVDA case).
  2. Instant tags: balance-sheet values align by fiscal year-end (date-keyed).
  3. Total debt = LT debt + LT current, date-aligned.
  4. Honest-empty: missing tag → [], never a fabricated number.
"""
import json
import os
from pathlib import Path

import pytest

from discovery.quality_asymmetry.fetcher import (
    _flow_series,
    _fiscal_year_ends,
    _instant_at_year_ends,
    _merge_instant,
    _as_series,
    _TAG_MAP,
)

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "discovery" / "quality_asymmetry" / "output" / "cache"


def _cf(cik: str) -> dict:
    p = CACHE / f"CIK{cik}.json"
    if not p.exists():
        pytest.skip(f"cache {p.name} missing (fetched by system-python run)")
    return json.loads(p.read_text(encoding="utf-8"))


def test_flow_series_merges_tag_switch():
    """NVDA switched revenue tags — merged series must reach FY2025+ (real:
    revenue FY2025 ~$130.5B, FY2026 ~$215.9B). A single-tag lookup stops at
    FY2022 (~$26.9B) — this is the exact bug the merge fixes."""
    cf = _cf("0001045810")
    rev = _flow_series(cf, _TAG_MAP["revenue"])
    assert len(rev) >= 6, f"expected >=6 fiscal years, got {len(rev)}"
    latest = rev[-1] / 1e9
    assert latest > 100, f"NVDA latest annual revenue {latest:.1f}B — tag merge failed"
    assert rev[-2] / 1e9 > 100, f"NVDA FY2025 revenue {rev[-2]/1e9:.1f}B — expected ~130B"


def test_fiscal_year_ends_dates():
    cf = _cf("0001045810")
    ye = _fiscal_year_ends(cf)
    assert ye[-1].startswith("2025") or ye[-1].startswith("2026"), f"last FY end {ye[-1]}"
    assert len(ye) >= 6


def test_instant_alignment_by_year_end():
    """Instant tags are date-keyed; assets at FY-end must be present and
    plausible (NVDA FY2026 assets ~$206B)."""
    cf = _cf("0001045810")
    ye = _fiscal_year_ends(cf)
    assets = _instant_at_year_ends(cf, "Assets", ye)
    assert assets, "Assets missing at year-ends"
    latest = max(assets.values()) / 1e9
    assert latest > 100, f"NVDA latest assets {latest:.1f}B — alignment failed"


def test_total_debt_merge():
    """LT debt + LT current, summed at the SAME year-end dates."""
    cf = _cf("0000320193")  # AAPL
    ye = _fiscal_year_ends(cf)
    lt = _instant_at_year_ends(cf, "LongTermDebt", ye)
    cur = _instant_at_year_ends(cf, "LongTermDebtCurrent", ye)
    merged = _merge_instant(lt, cur, ye)
    series = _as_series(merged, ye)
    assert series, "no debt series"
    assert len(series) >= 3, "debt series too short"
    latest = series[-1] / 1e9
    assert 80 < latest < 130, f"AAPL latest total debt {latest:.1f}B — expected ~90-110B (LT+current)"


def test_missing_tag_honest_empty():
    """A tag that doesn't exist → empty, never a fabricated value."""
    cf = _cf("0000320193")
    vals = _flow_series(cf, ["DefinitelyNotARealXbrlTagXYZ"])
    assert vals == []
