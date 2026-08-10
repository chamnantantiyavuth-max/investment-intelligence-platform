"""Locked-style invariants — Equity Inflection Validation Phase 1 (FD #88).

Charter (per docs/PLAN-EQUITY-INFLECTION-VALIDATION-P1-v0.1.md §5):
  1. Look-ahead — a value filed AFTER asof T never appears in the as-of view at T.
  2. Revision leakage — a synthetic restatement (value revised +filed later)
     flips the as-of view ONLY after its filed date; signal flip rate measured.
  3. Stage uses only prices <= asof (trailing MAs are PIT by construction).
  4. Fiscal-Q4 derivation + split adjustment behave inside the as-of view.
  5. Stability perturbations return to baseline after measurement (no global
     threshold mutation leaks between runs).

Pure logic ONLY — no network, no yfinance. Do NOT modify expected values
without an FD (Acceptance Lock Rule, FD-108).
"""
from __future__ import annotations

import pytest

from discovery.equity_inflection import scanner as s
from discovery.equity_inflection import validation as v

# ISO quarter-end dates (chronological) — date parsing requires real ISO dates
Q = ["2022-03-31", "2022-06-30", "2022-09-30", "2022-12-31",
     "2023-03-31", "2023-06-30", "2023-09-30", "2023-12-31",
     "2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31",
     "2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31"]


def _entry(end, value, filed, start=None, form="10-Q", fp="Q"):
    return {"period_end": end, "value": value, "filed": filed,
            "start": start or end, "form": form, "fp": fp}


def _mk_eps(ends, values, filed):
    return [_entry(e, val, f) for e, val, f in zip(ends, values, filed)]


def _shares(ends, values, filed):
    return [{"period_end": e, "value": val, "filed": f, "start": e,
             "form": "10-Q", "fp": "Q"} for e, val, f in zip(ends, values, filed)]


def _std_eps(values=None, filed=None):
    """16 ISO quarters; default steady climb 1.0 + 0.1*i, filed ~45d after end."""
    values = values or [1.0 + 0.1 * i for i in range(len(Q))]
    filed = filed or [("20%s-%02d-15" % (e[2:4], int(e[5:7]) % 12 + 1)) for e in Q]
    return _mk_eps(Q, values, filed)


# ── 1. look-ahead guard ──────────────────────────────────────────────────────

def test_lookahead_value_filed_after_asof_never_in_view():
    # 13 quarters; the LAST entry (high EPS) is filed AFTER the asof date
    ends = Q[:13]
    values = [1.0] * 12 + [99.0]               # 99.0 = future restatement/late filing
    filed = ["2024-01-05"] * 12 + ["2099-01-01"]  # filed far in the future
    eps = _mk_eps(ends, values, filed)
    view = v.latest_by_filed(eps, "2025-12-31")
    assert "2099" not in {e["filed"] for e in view.values()}
    assert all(e["filed"] <= "2025-12-31" for e in view.values())
    assert len(view) == 12                       # late 99.0 entry excluded
    assert v.lookahead_violations(eps, ["2025-12-31", "2026-06-30"]) == []


def test_lookahead_guard_is_at_the_source():
    """The guard lives inside latest_by_filed: an entry filed after asof can
    never enter the view, so the violations detector (defense-in-depth check
    over built views) returns empty by construction."""
    eps = _mk_eps(["2024-03-31"], [5.0], ["2099-01-01"])
    view = v.latest_by_filed(eps, "2025-01-01")
    assert view == {}          # future-filed value excluded at the source
    assert v.lookahead_violations(eps, ["2025-01-01"]) == []  # nothing leaked


# ── 2. revision leakage ──────────────────────────────────────────────────────

def test_revision_flips_view_only_after_its_filed_date():
    """Original EPS 1.0 filed 2024-01-05; restated to 2.0 filed 2025-06-01.
    Both are the SAME duration (pure quarter) — the tie-break is filed date.
    As-of 2025-01-01 must see 1.0; as-of 2025-12-31 must see 2.0."""
    eps = [_entry("2024-03-31", 1.0, "2024-01-05", start="2024-01-01"),
           _entry("2024-03-31", 2.0, "2025-06-01", start="2024-01-01")]
    v1 = v.latest_by_filed(eps, "2025-01-01")
    v2 = v.latest_by_filed(eps, "2025-12-31")
    assert v1["2024-03-31"]["value"] == 1.0
    assert v2["2024-03-31"]["value"] == 2.0


def test_revision_flip_rate_measureable_and_honest():
    filed = ["2022-05-15", "2022-08-15", "2022-11-15", "2023-02-15",
             "2023-05-15", "2023-08-15", "2023-11-15", "2024-02-15",
             "2024-05-15", "2024-08-15", "2024-11-15", "2025-02-15"]
    eps = _mk_eps(Q[:12], [1.0 + 0.1 * i for i in range(12)], filed)
    rev = [_entry(e, 100.0, f, start="2021-10-01") for e, f in zip(Q[:12], filed)]
    shares = _shares(Q[:12], [1.0] * 12, filed)
    prices = [{"date": "2025-03-01", "close": 100.0, "volume": 1_000_000}]
    res = v.revision_flip_rate(eps, rev, shares, prices, "2025-02-20")
    assert res["measureable"] is True
    assert res["h1_flip"] in (True, False)   # honest — either outcome recorded
    assert "asof_signal" in res and "final_signal" in res


# ── 3. stage PIT ─────────────────────────────────────────────────────────────

def test_stage_uses_only_prices_up_to_asof():
    """Future price bars must not affect stage classification at asof."""
    import math
    # flat base (260 bars) ending 2025-06-30, then a modest rally AFTER asof
    prices = []
    for i in range(260):
        d = v._d("2024-07-01")  # start base mid-2024
        from datetime import timedelta
        prices.append({"date": str(d + timedelta(days=i)),
                       "close": 100.0 * (1 + 0.01 * math.sin((i - 259) / 5.0)),
                       "volume": 1_000_000})
    rally = []
    for i in range(30):
        from datetime import timedelta
        d = v._d("2025-07-01")
        rally.append({"date": str(d + timedelta(days=i)),
                      "close": 100.0 * (1.003 ** i), "volume": 1_000_000})
    all_prices = prices + rally
    st_asof = s.stage_signature(v.asof_prices(all_prices, "2025-06-30"))
    st_later = s.stage_signature(v.asof_prices(all_prices, "2025-12-31"))
    assert st_asof["stage"] == "S1"          # flat base at asof
    assert st_later["stage"] == "S2-early"   # rally visible only after asof


# ── 4. fiscal-Q4 derivation + split inside as-of view ────────────────────────

def test_asof_view_derives_fiscal_q4():
    # annual FY2024 = 6.0 (filed 2024-11-01); Q1-Q3 2024 quarters filed earlier
    eps = [_entry("2024-03-31", 1.0, "2024-04-20", start="2024-01-01"),
           _entry("2024-06-30", 1.5, "2024-07-20", start="2024-04-01"),
           _entry("2024-09-30", 2.0, "2024-10-20", start="2024-07-01"),
           _entry("2024-12-31", 6.0, "2024-11-01", start="2024-01-01", form="10-K", fp="FY")]
    rev = [_entry("2024-12-31", 100.0, "2024-11-01", start="2024-01-01", form="10-K", fp="FY")]
    shares = _shares(["2024-12-31"], [1.0], ["2024-11-01"])
    q = v.asof_quarters(eps, rev, shares, "2025-01-01")
    by_end = {x["period_end"]: x for x in q}
    # Q4 derived = 6.0 - (1.0+1.5+2.0) = 1.5
    assert by_end["2024-12-31"]["eps_diluted"] == 1.5
    assert len(q) == 4


def test_asof_view_split_adjusts_pre_split_eps():
    # split 10:1 between 2024 and 2025 (shares 1B -> 10B); pre-split EPS 6.0
    # must appear as 0.6 in the as-of view (current basis)
    ends = ["2024-03-31", "2024-06-30", "2025-03-31", "2025-06-30"]
    filed = ["2024-04-20", "2024-07-20", "2025-04-20", "2025-07-20"]
    eps = _mk_eps(ends, [6.0, 6.0, 1.0, 1.0], filed)
    rev = [_entry(e, 100.0, f, start="2024-01-01") for e, f in zip(ends, filed)]
    shares = _shares(ends, [1.0, 1.0, 10.0, 10.0], filed)
    q = v.asof_quarters(eps, rev, shares, "2025-08-01")
    assert q[0]["eps_diluted"] == 0.6   # pre-split scaled down
    assert q[-1]["eps_diluted"] == 1.0  # post-split unchanged


# ── 5. stability perturbations restore state ─────────────────────────────────

def test_stability_perturbations_restore_globals():
    filed = ["2022-05-15", "2022-08-15", "2022-11-15", "2023-02-15",
             "2023-05-15", "2023-08-15", "2023-11-15", "2024-02-15",
             "2024-05-15", "2024-08-15", "2024-11-15", "2025-02-15",
             "2025-05-15", "2025-08-15", "2025-11-15", "2026-02-15"]
    eps = _mk_eps(Q, [1.0 + 0.1 * i for i in range(16)], filed)
    rev = [_entry(e, 100.0, f, start="2021-10-01") for e, f in zip(Q, filed)]
    shares = _shares(Q, [1.0] * 16, filed)
    import math
    from datetime import timedelta
    prices = []
    for i in range(260):
        d = v._d("2024-07-01")
        prices.append({"date": str(d + timedelta(days=i)),
                       "close": 100.0 * (1 + 0.01 * math.sin((i - 259) / 5.0)),
                       "volume": 1_000_000})
    payload = {"ticker": "T", "eps_entries": eps, "rev_entries": rev,
               "share_entries": shares, "prices": prices}
    before = (s.EARLY_S2_MAX_EXTENSION, s.STAGE1_SLOPE_PCT_MONTH,
              s.STAGE1_RANGE_LOW, s.STAGE1_RANGE_HIGH,
              s.H1_PRIOR_WINDOW_QUARTERS)
    res = v.stability_perturbations(payload, "2026-01-01")
    after = (s.EARLY_S2_MAX_EXTENSION, s.STAGE1_SLOPE_PCT_MONTH,
             s.STAGE1_RANGE_LOW, s.STAGE1_RANGE_HIGH,
             s.H1_PRIOR_WINDOW_QUARTERS)
    assert before == after  # no global mutation leaks
    assert len(res["variants"]) == 7
    assert "same" in next(iter(res["variants"].values()))
