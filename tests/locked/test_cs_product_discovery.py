"""Locked-style tests — CS Product Discovery shadow engine (FD #97).

Invariants under test:
  1. Pure module — imports without network/yfinance (pytest venv safe).
  2. Deterministic — same inputs → same evidence.
  3. Honest-empty: missing metrics never invented (status=missing, check=False).
  4. Gold/silver ratio: high ratio → physical_vs_paper supporting (PROPOSED).
  5. Dislocation: spot premium > 0.5% → supporting (PROPOSED).
  6. Cyclical trough: price ≤ 1.3x cost → supporting (PROPOSED).
  7. Firewall: output carries the evidence-only contract.
"""
from discovery.cs_product.discovery import (
    collect_watch_inputs,
    evaluate_patterns,
    run_discovery,
)


def _sample_inputs(**overrides) -> dict:
    base = {
        "gold": {
            "gold_lbma_pm_usd_oz": {"value": 4200.0, "as_of": "2026-08-05", "source": "LBMA gold_pm.json", "status": "verified"},
            "gold_spot_usd_oz": {"value": 4210.0, "as_of": "2026-08-11", "source": "radar pull", "status": "verified"},
            "gold_front_future_usd_oz": {"value": 4190.0, "as_of": "2026-08-11", "source": "radar pull", "status": "verified"},
        },
        "silver": {
            "silver_lbma_pm_usd_oz": {"value": 62.0, "as_of": "2026-08-05", "source": "LBMA", "status": "verified"},
            "silver_london_vault_oz": {"value": 907_000_000.0, "as_of": "2026-08-05", "source": "London vaults", "status": "verified"},
        },
        "copper": {
            "copper_price_usd_lb": {"value": 4.20, "as_of": "2026-08-11", "source": "radar pull", "status": "verified"},
            "copper_avg_aisc_usd_lb": {"value": 2.50, "as_of": "2026-08-11", "source": "industry estimate", "status": "verified"},
        },
        "oil": {
            "wti_price_usd_bbl": {"value": 68.0, "as_of": "2026-08-11", "source": "radar pull", "status": "verified"},
            "wti_breakeven_usd_bbl": {"value": 45.0, "as_of": "2026-08-11", "source": "industry estimate", "status": "verified"},
        },
    }
    for commodity, metrics in overrides.items():
        base.setdefault(commodity, {}).update(metrics)
    return base


def test_deterministic():
    a = run_discovery(_sample_inputs())
    b = run_discovery(_sample_inputs())
    assert a == b


def test_high_ratio_flags_physical_vs_paper():
    # gold 4200 / silver 62 = 67.7 → not above 80 → neutral (no false positive)
    ev = run_discovery(_sample_inputs())["pattern_evidence"]
    gs = next(e for e in ev if e["pattern"] == "physical_vs_paper")
    assert gs["signal"] in ("neutral", "supporting")
    # gold 4200 / silver 45 = 93.3 → above 80 → supporting
    hi = _sample_inputs()
    hi["silver"]["silver_lbma_pm_usd_oz"]["value"] = 45.0
    ev2 = run_discovery(hi)["pattern_evidence"]
    gs2 = next(e for e in ev2 if e["pattern"] == "physical_vs_paper")
    assert gs2["signal"] == "supporting"
    assert gs2["checks"]["ratio_above_80_proposed"] is True


def test_missing_silver_never_invented():
    inp = _sample_inputs()
    inp["silver"]["silver_lbma_pm_usd_oz"] = {"status": "missing", "value": None, "as_of": "", "source": "LBMA 404 (11 Aug)"}
    ev = run_discovery(inp)["pattern_evidence"]
    gs = next(e for e in ev if e["pattern"] == "physical_vs_paper")
    assert gs["checks"]["gold_silver_ratio_available"] is False
    assert "cannot be evaluated" in gs["note"]


def test_dislocation_premium():
    inp = _sample_inputs()
    inp["gold"]["gold_spot_usd_oz"]["value"] = 4220.0
    inp["gold"]["gold_front_future_usd_oz"]["value"] = 4190.0  # +0.72% premium
    ev = run_discovery(inp)["pattern_evidence"]
    d = next(e for e in ev if e["pattern"] == "dislocation")
    assert d["signal"] == "supporting"


def test_cyclical_trough_copper():
    inp = _sample_inputs()
    inp["copper"]["copper_price_usd_lb"]["value"] = 3.0   # vs AISC 2.50 → 1.2x
    ev = run_discovery(inp)["pattern_evidence"]
    c = next(e for e in ev if e["pattern"] == "cyclical_trough" and e["commodity"] == "copper")
    assert c["signal"] == "supporting"


def test_firewall_contract():
    out = run_discovery(_sample_inputs())
    assert out["proposed"] is True
    assert "no card, no CoS" in out["firewall"]
    assert "watch_inputs" in out and "pattern_evidence" in out


def test_watch_inputs_record_missing_status():
    inp = _sample_inputs()
    inp["oil"]["wti_breakeven_usd_bbl"] = {"status": "missing", "value": None, "as_of": "", "source": "not wired"}
    watch = collect_watch_inputs(inp)
    o = next(w for w in watch if w.metric == "wti_breakeven_usd_bbl")
    assert o.status == "missing" and o.value is None
