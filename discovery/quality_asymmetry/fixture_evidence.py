"""Offline fixture scan for the Quality & Asymmetry evidence engine.

The standing shadow runner (``python -m discovery.quality_asymmetry.run_shadow``)
fetches EDGAR and market data. This module does not. It reads one JSON fixture
of already-supplied annual figures and returns the existing deterministic
evidence block.

The output is shadow evidence only (FD #53 proposed thresholds, FD #88
firewall): no score, no recommendation, no Task Idea Card, no network, and no
filled-in numbers when a series is missing.

Usage::

    python -m discovery.quality_asymmetry.fixture_evidence --fixture PATH
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

from discovery.quality_asymmetry.archetypes import scan_ticker

_FORBIDDEN_KEYS = frozenset({
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "cookies",
    "credential",
    "credentials",
    "password",
    "refresh_token",
    "secret",
    "storage_state",
    "token",
    "access_token",
})

_TOP_LEVEL = frozenset({"ticker", "fin", "market", "recon"})

# archetypes.py input contract: these 12 annual columns, oldest→newest, same length.
_FIN_FIELDS = frozenset({
    "revenue",
    "net_income",
    "operating_income",
    "total_assets",
    "total_equity",
    "total_debt",
    "cash",
    "ocf",
    "capex",
    "dividends_paid",
    "buybacks_paid",
    "ebitda",
})

_MARKET_FIELDS = frozenset({
    "price",
    "eps_ttm",
    "book_value_per_share",
    "shares_out",
    "market_cap",
    "price_52w_high",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "buyback_yield_ttm",
    "valuation_discount_vs_5y_median",
})


class FixtureRejected(ValueError):
    """The fixture is unusable. No evidence is produced."""


def canonical_fixture_bytes(payload: dict) -> bytes:
    """Stable bytes for the fixture object. Whitespace in the file is ignored."""
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")


def _reject_forbidden_keys(node: object) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).strip().lower() in _FORBIDDEN_KEYS:
                raise FixtureRejected(f"forbidden key {key}")
            _reject_forbidden_keys(value)
    elif isinstance(node, list):
        for item in node:
            _reject_forbidden_keys(item)


def _require_number(value: object, label: str) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FixtureRejected(f"{label} must be a number or null")
    if not math.isfinite(value):
        raise FixtureRejected(f"{label} must be a finite number or null")


def _validate(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise FixtureRejected("fixture must be an object")
    _reject_forbidden_keys(payload)
    unknown = set(payload) - _TOP_LEVEL
    if unknown:
        raise FixtureRejected(f"unknown fixture field {sorted(unknown)[0]}")
    ticker = payload.get("ticker")
    if not isinstance(ticker, str) or not ticker.strip():
        raise FixtureRejected("ticker must be a non-blank string")
    if len(ticker.strip()) > 32 or "/" in ticker or "\\" in ticker:
        raise FixtureRejected("ticker is not a short label")
    fin = payload.get("fin")
    if not isinstance(fin, dict):
        raise FixtureRejected("fin must be an object")
    unknown_fin = set(fin) - _FIN_FIELDS
    if unknown_fin:
        raise FixtureRejected(f"unknown fin field {sorted(unknown_fin)[0]}")
    lengths: list[int] = []
    for key, series in fin.items():
        if not isinstance(series, list):
            raise FixtureRejected(f"fin.{key} must be a list")
        lengths.append(len(series))
        for index, item in enumerate(series):
            _require_number(item, f"fin.{key}[{index}]")
    if len(set(lengths)) > 1:
        raise FixtureRejected(
            "annual series must have equal length; pad missing years with null"
        )
    market = payload.get("market")
    if market is not None:
        if not isinstance(market, dict):
            raise FixtureRejected("market must be an object")
        extra = set(market) - _MARKET_FIELDS
        if extra:
            raise FixtureRejected(f"unknown market field {sorted(extra)[0]}")
        for key, value in market.items():
            _require_number(value, f"market.{key}")
    recon = payload.get("recon")
    if recon is not None:
        if not isinstance(recon, dict):
            raise FixtureRejected("recon must be an object")
        extra = set(recon) - {"special_situation"}
        if extra:
            raise FixtureRejected(f"unknown recon field {sorted(extra)[0]}")
        situations = recon.get("special_situation", [])
        if not isinstance(situations, list) or not all(
            isinstance(item, str) and item.strip() for item in situations
        ):
            raise FixtureRejected("recon.special_situation must be a list of strings")
    return payload


def load_fixture(path: Path | str) -> dict:
    """Read and validate a fixture file. Does not scan it."""
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FixtureRejected(f"cannot read fixture: {exc.strerror}") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise FixtureRejected(f"fixture is not JSON: {exc.msg}") from exc
    return _validate(payload)


def evidence_from_fixture(payload: dict) -> dict:
    """Scan one validated fixture. Missing series stay null; nothing is invented."""
    checked = _validate(payload)
    fin = checked["fin"]
    market = checked.get("market")
    recon = checked.get("recon")
    evidence = scan_ticker(str(checked["ticker"]).strip(), fin, market, recon)
    return {
        "ticker": evidence["ticker"],
        "input_sha256": hashlib.sha256(canonical_fixture_bytes(checked)).hexdigest(),
        "network_used": False,
        "thresholds": "PROPOSED_FD53_SHADOW",
        "score": None,
        "recommendation": None,
        "invented_values": False,
        "evidence": evidence,
    }


def render_envelope(envelope: dict) -> str:
    """Serialize the whole envelope, or reject it. Never returns partial JSON."""
    try:
        body = json.dumps(envelope, indent=2, sort_keys=True, allow_nan=False)
    except ValueError as exc:
        raise FixtureRejected(f"non-finite evidence output: {exc}") from exc
    return body + "\n"


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] != ["--fixture"] or len(args) != 2:
        print(
            "usage: python -m discovery.quality_asymmetry.fixture_evidence --fixture PATH",
            file=sys.stderr,
        )
        return 2
    try:
        text = render_envelope(evidence_from_fixture(load_fixture(args[1])))
    except FixtureRejected as exc:
        print(f"fixture rejected: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
