"""Offline fixture scan for the Quality & Asymmetry evidence engine.

The shadow runner fetches EDGAR/yfinance. These tests lock a network-free
path: a synthetic fixture goes in, a deterministic evidence envelope comes
out. Formulas below are copied from discovery/quality_asymmetry/archetypes.py
and recomputed here so a change to the engine math fails this file.

Thresholds stay the existing PROPOSED shadow bands (FD #53). This file does
not approve them for production and does not add a score.
"""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from discovery.quality_asymmetry.archetypes import PROPOSED
from discovery.quality_asymmetry.fixture_evidence import (
    FixtureRejected,
    canonical_fixture_bytes,
    evidence_from_fixture,
    load_fixture,
)

REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "tests" / "fixtures" / "quality_asymmetry" / "synth_compounder.json"
TAX = 0.21  # existing PROPOSED US statutory proxy inside archetypes._roic


def _expected_from_fixture(payload: dict) -> dict:
    """Independent recomputation of the signals the engine must emit."""
    fin = payload["fin"]
    market = payload["market"]
    oi = fin["operating_income"]
    assets = fin["total_assets"]
    cash = fin["cash"]
    debt = fin["total_debt"]
    equity = fin["total_equity"]
    ni = fin["net_income"]
    ocf = fin["ocf"]
    capex = fin["capex"]
    ebitda = fin["ebitda"]
    rev = fin["revenue"]

    roic = (oi[-1] * (1 - TAX)) / (assets[-1] - cash[-1])
    roic_5y_vals = []
    for i in range(-5, 0):
        roic_5y_vals.append(oi[i] * (1 - TAX) / (assets[i] - cash[i]))
    roic_5y = sum(roic_5y_vals) / len(roic_5y_vals)
    d_nopat = (oi[-1] - oi[-4]) * (1 - TAX)
    d_inv = (assets[-1] - cash[-1]) - (assets[-4] - cash[-4])
    incremental = d_nopat / d_inv
    fcf = [o + c for o, c in zip(ocf, capex)]
    fcf_conv = sum(f / n for f, n in zip(fcf[-3:], ni[-3:])) / 3
    nde = (debt[-1] - cash[-1]) / ebitda[-1]
    reinvest = (ni[-1] - abs(fin["dividends_paid"][-1]) - abs(fin["buybacks_paid"][-1])) / ni[-1]
    cagr = (rev[-1] / rev[0]) ** (1 / 5) - 1
    drawdown = (market["price_52w_high"] - market["price"]) / market["price_52w_high"]
    return {
        "roic": roic,
        "roic_5y": roic_5y,
        "incremental": incremental,
        "fcf_conv": fcf_conv,
        "nde": nde,
        "reinvest": reinvest,
        "cagr": cagr,
        "drawdown": drawdown,
        "fcf_latest": fcf[-1],
    }


def test_module_source_does_not_import_network_clients():
    source = (REPO / "discovery" / "quality_asymmetry" / "fixture_evidence.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module)
    banned = ("yfinance", "requests", "urllib", "httpx", "fetcher", "socket")
    for name in imported:
        assert not any(part in name for part in banned), name


def test_running_the_scan_does_not_import_yfinance():
    payload = load_fixture(FIXTURE)
    evidence_from_fixture(payload)
    assert "yfinance" not in sys.modules
    assert "discovery.quality_asymmetry.fetcher" not in sys.modules


def test_synthetic_fixture_locks_hand_computed_signals():
    payload = load_fixture(FIXTURE)
    expected = _expected_from_fixture(payload)
    envelope = evidence_from_fixture(payload)
    evidence = envelope["evidence"]
    by_id = {block["archetype"]: block for block in evidence["archetypes"]}

    assert envelope["ticker"] == "SYNTH-QA"
    assert envelope["network_used"] is False
    assert envelope["thresholds"] == "PROPOSED_FD53_SHADOW"
    assert envelope["score"] is None
    assert envelope["recommendation"] is None
    assert envelope["invented_values"] is False
    assert envelope["input_sha256"] == hashlib.sha256(canonical_fixture_bytes(payload)).hexdigest()
    assert len(envelope["input_sha256"]) == 64
    assert evidence["proposed"] is True
    assert "evidence only" in evidence["firewall"]
    assert "score" not in evidence

    a = by_id["A"]["signals"]
    assert a["roic_latest"] == pytest.approx(expected["roic"], abs=1e-12)
    assert a["roic_5y_avg"] == pytest.approx(expected["roic_5y"], abs=1e-12)
    assert a["incremental_roic_3y"] == pytest.approx(expected["incremental"], abs=1e-12)
    assert a["fcf_conversion_3y_avg"] == pytest.approx(expected["fcf_conv"], abs=1e-12)
    assert a["net_debt_ebitda"] == pytest.approx(expected["nde"], abs=1e-12)
    assert expected["roic"] == pytest.approx(62 * 0.79 / 210, abs=1e-12)
    assert a["roic_latest"] > PROPOSED["A_ROIC_MIN"]
    assert by_id["A"]["checks"]["roic_latest >= A_ROIC_MIN"] is True
    assert by_id["A"]["checks"]["roic_5y_avg >= A_ROIC_5Y_MIN"] is True
    assert by_id["A"]["checks"]["incremental_roic >= A_INCR_ROIC_MIN"] is True
    assert by_id["A"]["checks"]["fcf_conversion >= A_FCF_CONV_MIN"] is True
    assert by_id["A"]["checks"]["net_debt/ebitda <= A_NET_DEBT_EBITDA_MAX"] is True
    assert by_id["A"]["matched_count"] == 5

    b = by_id["B"]["signals"]
    assert b["reinvestment_rate_latest"] == pytest.approx(expected["reinvest"], abs=1e-12)
    assert b["revenue_cagr_5y"] == pytest.approx(expected["cagr"], abs=1e-12)
    assert expected["cagr"] > PROPOSED["B_REV_CAGR5_MIN"]
    assert by_id["B"]["matched_count"] == 3

    c = by_id["C"]
    assert c["signals"]["drawdown_from_52w_high"] == pytest.approx(expected["drawdown"], abs=1e-12)
    assert expected["drawdown"] == pytest.approx(0.30, abs=1e-12)
    assert c["signals"]["fcf_latest_positive"] is True
    assert c["signals"]["revenue_not_shrinking"] is True
    assert c["quality_pass"] is True
    assert c["mispricing"] is True
    assert c["matched_count"] == 2
    assert c["signals"]["valuation_discount_vs_5y_median"] == pytest.approx(0.1, abs=1e-12)

    d = by_id["D"]
    assert d["signals"]["net_cash"] is True
    assert d["signals"]["net_debt_equity"] == pytest.approx((0 - 50) / 180, abs=1e-12)
    assert d["checks"]["buyback_yield >= D_BUYBACK_YIELD_MIN"] is True
    assert d["checks"]["pb <= D_PB_MAX"] is True
    assert d["checks"]["special situation flagged"] is True
    assert d["matched_count"] == 4


def test_missing_operating_income_stays_null_not_zero():
    payload = load_fixture(FIXTURE)
    payload["fin"]["operating_income"] = [None, None, None, None, None, None]
    envelope = evidence_from_fixture(payload)
    signals = envelope["evidence"]["archetypes"][0]["signals"]
    assert signals["roic_latest"] is None
    assert signals["roic_5y_avg"] is None
    assert signals["incremental_roic_3y"] is None
    rendered = json.dumps(envelope)
    assert '"roic_latest": null' in rendered
    assert '"roic_latest": 0' not in rendered


def test_input_hash_ignores_whitespace_and_changes_when_a_figure_changes():
    payload = load_fixture(FIXTURE)
    first = evidence_from_fixture(payload)["input_sha256"]
    again = evidence_from_fixture(json.loads(json.dumps(payload, indent=4)))["input_sha256"]
    assert first == again
    payload["fin"]["revenue"][-1] = 221
    changed = evidence_from_fixture(payload)
    assert changed["input_sha256"] != first
    assert changed["evidence"]["archetypes"][1]["signals"]["revenue_cagr_5y"] != pytest.approx(
        (220 / 80) ** (1 / 5) - 1, abs=1e-12
    )


def test_same_fixture_is_deterministic():
    payload = load_fixture(FIXTURE)
    assert evidence_from_fixture(payload) == evidence_from_fixture(payload)


def test_credential_like_keys_are_rejected():
    payload = load_fixture(FIXTURE)
    payload["market"]["api_key"] = "not-a-real-secret"
    with pytest.raises(FixtureRejected, match="api_key"):
        evidence_from_fixture(payload)


def test_non_numeric_financial_series_is_rejected():
    payload = load_fixture(FIXTURE)
    payload["fin"]["revenue"][-1] = "220"
    with pytest.raises(FixtureRejected, match="revenue"):
        evidence_from_fixture(payload)


def test_cli_prints_the_envelope_and_rejects_a_missing_file():
    proc = subprocess.run(
        [sys.executable, "-m", "discovery.quality_asymmetry.fixture_evidence",
         "--fixture", str(FIXTURE)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    body = json.loads(proc.stdout)
    assert body["ticker"] == "SYNTH-QA"
    assert body["network_used"] is False
    assert body["score"] is None
    assert body["recommendation"] is None
    assert body["evidence"]["archetypes"][0]["signals"]["roic_latest"] == pytest.approx(
        62 * (1 - TAX) / 210, abs=1e-12
    )

    missing = subprocess.run(
        [sys.executable, "-m", "discovery.quality_asymmetry.fixture_evidence",
         "--fixture", str(REPO / "tests" / "fixtures" / "quality_asymmetry" / "missing.json")],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert missing.returncode == 2
    assert "fixture rejected" in missing.stderr
    assert missing.stdout == ""
