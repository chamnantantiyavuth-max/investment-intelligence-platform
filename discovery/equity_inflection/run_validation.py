"""Validation Phase 1 runner — PIT historical validation (FD #88).

RUNS UNDER SYSTEM PYTHON 3.14 (`python3`) — fetches real SEC companyfacts
revision history + 10y yfinance prices, then runs the pure validation logic
from validation.py. Produces the evidence pack in
`discovery/equity_inflection/output/validation-2026-08-10/`.

Usage: python3 discovery/equity_inflection/run_validation.py
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root

from discovery.equity_inflection import fetcher, validation as v  # noqa: E402

OUT_DIR = Path(__file__).parent / "output" / "validation-2026-08-10"


def asof_dates() -> list[str]:
    """Quarter-end as-of dates 2021-06-30 .. 2026-06-30 (~21 dates)."""
    dates = []
    y, m = 2021, 6
    while (y, m) <= (2026, 6):
        # last day of month m
        if m == 12:
            last = 31
        elif m in (4, 6, 9, 11):
            last = 30
        else:
            last = 30  # quarter-ends are 3/6/9/12 — all 30/31; Jun/Sep use 30
        dates.append(f"{y}-{m:02d}-{last}")
        m += 3
        if m > 12:
            m = 3
            y += 1
    return dates


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dates = asof_dates()
    print(f"Validation Phase 1 — {len(dates)} as-of dates x {len(fetcher.FO_UNIVERSE)} names")

    payloads = {}
    for t in fetcher.FO_UNIVERSE:
        try:
            payloads[t] = fetcher.fetch_validation_data(t)
            print(f"  fetched {t}: eps_entries={len(payloads[t]['eps_entries'])} "
                  f"rev={len(payloads[t]['rev_entries'])} shares={len(payloads[t]['share_entries'])} "
                  f"prices={len(payloads[t]['prices'])}")
        except Exception as e:  # noqa: BLE001
            payloads[t] = {"error": f"{type(e).__name__}: {e}"}
            print(f"  ERROR {t}: {e}")

    (OUT_DIR / "payloads.json").write_text(
        json.dumps({k: {"error": pv["error"]} if "error" in pv else
                    {"eps_entries": pv["eps_entries"][-80:],
                     "rev_entries": pv["rev_entries"][-80:],
                     "share_entries": pv["share_entries"][-80:],
                     "prices": pv["prices"][-260:]}
                    for k, pv in payloads.items()}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    # T2: historical run
    results = v.historical_run(payloads, dates)
    (OUT_DIR / "historical-run.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    # T3: bias tests
    bias = {"lookahead": {}, "revision_flip_rate": []}
    for t, p in payloads.items():
        if "error" in p:
            bias["lookahead"][t] = {"error": p["error"]}
            continue
        bias["lookahead"][t] = v.lookahead_violations(p["eps_entries"], dates)
        for asof in dates[-6:]:  # recent dates only — 10y revision comparisons
            try:
                flip = v.revision_flip_rate(p["eps_entries"], p["rev_entries"],
                                            p["share_entries"], p["prices"], asof, t)
                bias["revision_flip_rate"].append(flip)
            except Exception as e:  # noqa: BLE001
                bias["revision_flip_rate"].append({"ticker": t, "asof": asof,
                                                   "measureable": False,
                                                   "error": str(e)})
    (OUT_DIR / "bias-tests.json").write_text(
        json.dumps(bias, indent=2, ensure_ascii=False), encoding="utf-8")

    # T4: stability perturbations (per candidate-capable ticker at last 4 dates)
    stability = {}
    for t, p in payloads.items():
        if "error" in p:
            continue
        stability[t] = {}
        for asof in dates[-4:]:
            try:
                stability[t][asof] = v.stability_perturbations(p, asof)
            except Exception as e:  # noqa: BLE001
                stability[t][asof] = {"error": str(e)}
    (OUT_DIR / "stability.json").write_text(
        json.dumps(stability, indent=2, ensure_ascii=False), encoding="utf-8")

    # T5: false-positive review (H1-hit asofs) + capacity load
    hit_asofs_by_ticker = {}
    for r in results:
        if r["signals"].get("h1", {}).get("signal"):
            hit_asofs_by_ticker.setdefault(r["ticker"], []).append(r["asof"])
    fp = {}
    for t, p in payloads.items():
        if "error" in p:
            continue
        try:
            fp[t] = v.false_positive_review(p["eps_entries"], p["rev_entries"],
                                            p["share_entries"],
                                            hit_asofs_by_ticker.get(t, []))
        except Exception as e:  # noqa: BLE001
            fp[t] = [{"error": str(e)}]
    (OUT_DIR / "false-positive-review.json").write_text(
        json.dumps(fp, indent=2, ensure_ascii=False), encoding="utf-8")
    load = v.capacity_load(results)
    (OUT_DIR / "capacity-load.json").write_text(
        json.dumps(load, indent=2, ensure_ascii=False), encoding="utf-8")

    # console summary
    print("\n=== historical-run summary (eligible per asof) ===")
    for r in results:
        if r["eligible"]:
            print(f"  {r['asof']} {r['ticker']} eligible  (stage {r['stage'].get('stage')})")
    print("=== capacity load ===")
    print(f"  {load}")
    print("=== bias: lookahead violations (should be all empty) ===")
    for t, viol in bias["lookahead"].items():
        print(f"  {t}: {len(viol)} violations")
    print("=== revision flip rate (last 6 asofs, measurable) ===")
    flips = [f for f in bias["revision_flip_rate"] if f.get("measureable")]
    print(f"  measurable={len(flips)}  h1_flips={sum(1 for f in flips if f['h1_flip'])}  "
          f"h2_flips={sum(1 for f in flips if f['h2_flip'])}  "
          f"rev_flips={sum(1 for f in flips if f['rev_flip'])}")
    print(f"\nEvidence pack: {OUT_DIR}")


if __name__ == "__main__":
    main()
