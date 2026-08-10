"""Equity Inflection Validation Phase 1 — PIT historical validation (FD #88).

PURE LOGIC ONLY (no yfinance/numpy at import) — testable under the pytest
venv. Data comes from `fetcher.fetch_validation_data()` (full revision
history + 10y prices) run under system Python 3.14.

Method (point-in-time as-of reconstruction, FD #58):
  as-of view at T = for every quarter, the value whose filed date is the
  LATEST filed <= T (revision history honored), restricted to quarters
  REPORTED by T. TTM/H1/H2/revenue/stage computed on that view only.

Boundaries (FD #88): validation output is EVIDENCE ONLY — no threshold
becomes production, no cards, no CoS triage, no research capacity consumed.
Primary metric = research-discovery quality, NOT forward returns.
"""
from __future__ import annotations

from datetime import date

from discovery.equity_inflection import scanner

QUARTER_DUR_DAYS = 150   # pure-quarter XBRL duration (start->end)
ANNUAL_DUR_DAYS = 200    # FY annual threshold


def _d(s: str):
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def latest_by_filed(entries: list[dict], asof: str) -> dict[str, dict]:
    """Per period_end, the best PIT value as of `asof`.

    Selection rule (matches the shadow fetcher's dedup): among entries filed
    <= asof, prefer the SHORTEST duration (pure quarterly figure beats the
    YTD-cumulative/annual figure that shares the same period_end); among
    equal durations, prefer the LATEST filed (restatement honored). ISO date
    strings compare lexicographically. Returns {period_end: entry}."""
    out: dict[str, dict] = {}

    def dur(e: dict) -> int:
        d0, d1 = _d(e.get("start", e["period_end"])), _d(e["period_end"])
        return (d1 - d0).days if (d0 and d1) else 9999

    for e in entries:
        if e["filed"] > asof:
            continue  # look-ahead guard: values filed after T never enter
        key = e["period_end"]
        cur = out.get(key)
        if cur is None or dur(e) < dur(cur) or (
                dur(e) == dur(cur) and e["filed"] > cur["filed"]):
            out[key] = e
    return out


def asof_quarters(eps_entries: list[dict], rev_entries: list[dict],
                  share_entries: list[dict], asof: str) -> list[dict]:
    """Build the PIT quarterly series as of date `asof` (scanner-compatible).

    Steps (all as-of T):
      1. latest value per period_end (restatement history honored)
      2. keep pure quarters (duration <= 150d); drop annual-only slots with
         <3 quarters inside (insufficient XBRL granularity — honest omission)
      3. derive fiscal-Q4 = annual - sum(3 pure quarters inside its window)
      4. split-adjust EPS via DilutedAverageShares ratios (as-known-at-T)
    """
    eps = latest_by_filed(eps_entries, asof)
    rev = latest_by_filed(rev_entries, asof)
    shares = latest_by_filed(share_entries, asof)

    def dur(e: dict) -> int | None:
        d0, d1 = _d(e.get("start", e["period_end"])), _d(e["period_end"])
        if d0 and d1:
            return (d1 - d0).days
        return None

    eps_q = {k: v for k, v in eps.items()
             if (dur(v) if dur(v) is not None else 9999) <= QUARTER_DUR_DAYS}
    eps_a = {k: v for k, v in eps.items()
             if (dur(v) if dur(v) is not None else 0) > ANNUAL_DUR_DAYS}

    # derive fiscal-Q4 (annual minus its 3 inside quarters)
    for a_end, a in eps_a.items():
        a0, a1 = _d(a.get("start")), _d(a["period_end"])
        if not (a0 and a1):
            continue
        inside = [q for q_end, q in eps_q.items()
                  if (d0 := _d(q_end)) and a0 <= d0 <= a1]
        if len(inside) == 3:
            q4 = a["value"] - sum(q["value"] for q in inside)
            if q4 != 0 and q4 == q4:
                eps_q.setdefault(a_end, {**a, "value": round(q4, 6),
                                         "derived": True})

    # split-adjust EPS (as-known-at-T share counts)
    share_map = {k: v["value"] for k, v in shares.items()}
    eps_list = sorted(
        ({"period_end": k, "value": v["value"], "filed": v["filed"],
          "derived": bool(v.get("derived"))} for k, v in eps_q.items()),
        key=lambda x: x["period_end"])
    share_list = sorted(({"period_end": k, "value": v["value"], "filed": v["filed"]}
                         for k, v in shares.items()), key=lambda x: x["period_end"])
    adj = scanner.split_adjust(eps_list, share_list)

    rev_q = {k: v for k, v in rev.items()
             if (dur(v) if dur(v) is not None else 9999) <= QUARTER_DUR_DAYS}
    rev_by_end = dict(rev_q)

    quarters = []
    for a in adj:
        r = rev_by_end.get(a["period_end"], {})
        quarters.append({
            "period_end": a["period_end"],
            "eps_diluted": a["value"],
            "revenue": float(r.get("value", 0.0) or 0.0),
            "eps_available_at": f"{a['filed']} (as-of {asof})",
            "revenue_available_at": f"{r.get('filed', asof)} (as-of {asof})",
        })
    return quarters


def asof_prices(prices: list[dict], asof: str) -> list[dict]:
    """Price history up to and including asof only (trailing MAs are PIT)."""
    return [p for p in prices if p["date"] <= asof]


def snapshot(ticker: str, data: dict, asof: str) -> dict:
    """One as-of-date scan: full candidate record via the shadow scanner."""
    quarters = asof_quarters(data["eps_entries"], data["rev_entries"],
                             data["share_entries"], asof)
    prices = asof_prices(data["prices"], asof)
    meta = {"price": prices[-1]["close"] if prices else 0.0,
            "avg_volume_50d": (sum(p["volume"] for p in prices[-50:]) / max(1, len(prices[-50:]))
                               if prices else 0.0),
            "as_of": asof}
    return scanner.scan_ticker(ticker, quarters, prices, meta)


def historical_run(payloads: dict[str, dict],
                   asof_dates: list[str]) -> list[dict]:
    """Run the full scan at every as-of date. Returns records with
    {'asof', 'ticker', 'eligible', 'signals', 'stage', 'reasons'}."""
    out = []
    for asof in asof_dates:
        for ticker, data in sorted(payloads.items()):
            if "error" in data:
                out.append({"asof": asof, "ticker": ticker, "eligible": False,
                            "reasons": [f"data error: {data['error']}"],
                            "signals": {}, "stage": {}})
                continue
            try:
                rec = snapshot(ticker, data, asof)
                out.append({"asof": asof, "ticker": ticker,
                            "eligible": rec["eligible"],
                            "signals": rec["signals"], "stage": rec["stage"],
                            "reasons": rec["reasons"]})
            except Exception as e:  # honest per-snapshot failure
                out.append({"asof": asof, "ticker": ticker, "eligible": False,
                            "reasons": [f"snapshot error: {type(e).__name__}: {e}"],
                            "signals": {}, "stage": {}})
    return out


# ── bias tests ───────────────────────────────────────────────────────────────

def lookahead_violations(eps_entries: list[dict], asofs: list[str]) -> list[str]:
    """Values filed AFTER asof must never appear in the as-of view. Returns
    any violations as descriptive strings (empty = clean)."""
    bad = []
    for asof in asofs:
        view = latest_by_filed(eps_entries, asof)
        for end, e in view.items():
            if e["filed"] > asof:
                bad.append(f"asof {asof}: period {end} value filed {e['filed']} leaked")
    return bad


def revision_flip_rate(eps_entries: list[dict], rev_entries: list[dict],
                       share_entries: list[dict], prices: list[dict],
                       asof: str, ticker: str = "T") -> dict:
    """Signal flip rate at one as-of: as-of view vs FINAL (latest-known) view.
    Counts how many of the eligibility components flip when restatements are
    ignored (revision leakage measurement)."""
    final = asof_quarters(eps_entries, rev_entries, share_entries, asof + "9999")
    asof_q = asof_quarters(eps_entries, rev_entries, share_entries, asof)
    if len(final) < 9 or len(asof_q) < 9:
        return {"ticker": ticker, "asof": asof, "measureable": False}
    pr = asof_prices(prices, asof)
    meta = {"price": pr[-1]["close"] if pr else 0.0,
            "avg_volume_50d": 0.0, "as_of": asof}
    r_asof = scanner.scan_ticker(ticker, asof_q, pr, meta)
    r_final = scanner.scan_ticker(ticker, final, pr, meta)
    flips = {}
    for k in ("h1", "h2", "revenue"):
        a = r_asof["signals"][k].get("signal")
        f = r_final["signals"][k].get("signal")
        flips[k] = (a, f)
    return {
        "ticker": ticker, "asof": asof, "measureable": True,
        "h1_flip": flips["h1"][0] != flips["h1"][1],
        "h2_flip": flips["h2"][0] != flips["h2"][1],
        "rev_flip": flips["revenue"][0] != flips["revenue"][1],
        "asof_signal": {k: flips[k][0] for k in flips},
        "final_signal": {k: flips[k][1] for k in flips},
        "latest_ttm_asof": r_asof["signals"]["h1"].get("latest_ttm_eps"),
        "latest_ttm_final": r_final["signals"]["h1"].get("latest_ttm_eps"),
    }


# ── stability (threshold perturbations) ──────────────────────────────────────

def stability_perturbations(payload: dict, asof: str,
                            bands: dict | None = None) -> dict:
    """Re-run the snapshot with perturbed threshold bands (PROPOSED-value
    sensitivity). Returns per-band eligibility + candidate-set Jaccard vs base.
    bands: {"extension": float, "slope": float, "range_lo": float,
            "range_hi": float, "window_q": int} — None uses current defaults.
    """
    import copy
    from discovery.equity_inflection import scanner as sc
    bands = bands or {}
    base = snapshot(payload.get("ticker", "T"), payload, asof)
    res = {"base_eligible": base["eligible"], "variants": {}}
    variants = {
        "extension_lo": {"extension": 0.10},
        "extension_hi": {"extension": 0.20},
        "slope_lo": {"slope": 0.3},
        "slope_hi": {"slope": 0.7},
        "range_narrow": {"range_lo": 0.40, "range_hi": 0.60},
        "window_6q": {"window_q": 6},
        "window_10q": {"window_q": 10},
    }
    for name, patch in variants.items():
        cur = dict(scanner.__dict__)
        saved = {}
        for k, v in patch.items():
            if k == "extension":
                saved["EARLY_S2_MAX_EXTENSION"] = sc.EARLY_S2_MAX_EXTENSION
                sc.EARLY_S2_MAX_EXTENSION = v
            elif k == "slope":
                saved["STAGE1_SLOPE_PCT_MONTH"] = sc.STAGE1_SLOPE_PCT_MONTH
                sc.STAGE1_SLOPE_PCT_MONTH = v
            elif k == "range_lo":
                saved["STAGE1_RANGE_LOW"] = sc.STAGE1_RANGE_LOW
                sc.STAGE1_RANGE_LOW = v
            elif k == "range_hi":
                saved["STAGE1_RANGE_HIGH"] = sc.STAGE1_RANGE_HIGH
                sc.STAGE1_RANGE_HIGH = v
            elif k == "window_q":
                saved["H1_PRIOR_WINDOW_QUARTERS"] = sc.H1_PRIOR_WINDOW_QUARTERS
                saved["H2_PRIOR_WINDOW_QUARTERS"] = sc.H2_PRIOR_WINDOW_QUARTERS
                sc.H1_PRIOR_WINDOW_QUARTERS = v
                sc.H2_PRIOR_WINDOW_QUARTERS = v
        try:
            var = snapshot(payload.get("ticker", "T"), payload, asof)
            res["variants"][name] = {"eligible": var["eligible"],
                                     "same": var["eligible"] == base["eligible"]}
        finally:
            for k, v in saved.items():
                setattr(sc, k, v)
    return res


# ── reviews (evidence only) ──────────────────────────────────────────────────

def false_positive_review(eps_entries: list[dict], rev_entries: list[dict],
                          share_entries: list[dict],
                          hit_asofs: list[str]) -> list[dict]:
    """For every historical as-of where H1 fired, check the OUTCOME of the
    inflection (using later filings — REVIEW, never signal computation):
    did TTM EPS stay above the frame at the NEXT two quarter-ends?
    Returns one record per hit. This is research-discovery quality review,
    NOT a forward-return trading analysis."""
    from datetime import timedelta
    out = []
    for asof in hit_asofs:
        q = asof_quarters(eps_entries, rev_entries, share_entries, asof)
        if len(q) < 9:
            continue
        latest_end = _d(q[-1]["period_end"])
        if not latest_end:
            continue
        later1 = asof_quarters(eps_entries, rev_entries, share_entries,
                               (latest_end + timedelta(days=120)).isoformat())
        later2 = asof_quarters(eps_entries, rev_entries, share_entries,
                               (latest_end + timedelta(days=210)).isoformat())
        def ttm(qs):
            return sum(x["eps_diluted"] for x in qs[-4:]) if len(qs) >= 4 else None
        t0 = ttm(q)
        t1 = ttm(later1)
        t2 = ttm(later2)
        held = (t0 is not None and t1 is not None and t2 is not None
                and t1 > t0 and t2 > t0)
        out.append({"asof": asof, "latest_end": q[-1]["period_end"],
                    "ttm_at_hit": round(t0, 4) if t0 else None,
                    "ttm_next": round(t1, 4) if t1 else None,
                    "ttm_next2": round(t2, 4) if t2 else None,
                    "inflection_held": held,
                    "character": "confirmed" if held else "faded/one-off"})
    return out


def capacity_load(results: list[dict]) -> dict:
    """Candidates per as-of date (research-capacity load estimate)."""
    per_date: dict[str, int] = {}
    for r in results:
        if r["eligible"]:
            per_date[r["asof"]] = per_date.get(r["asof"], 0) + 1
    counts = list(per_date.values())
    return {
        "candidates_per_cycle": counts,
        "avg_per_cycle": round(sum(counts) / len(counts), 2) if counts else 0.0,
        "max_per_cycle": max(counts) if counts else 0,
        "total_candidate_snapshots": sum(counts),
    }
