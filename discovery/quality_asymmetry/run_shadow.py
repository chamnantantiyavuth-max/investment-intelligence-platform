"""Quality & Asymmetry — shadow run orchestrator (WP2).

python3 -m discovery.quality_asymmetry.run_shadow [TICKER ...]

Pipeline: universe → fetch (EDGAR annual + yfinance market) → archetype engine
(run_shadow) → evidence JSON + human-readable summary. Firewall (FD #88
pattern): output = evidence blocks ONLY. No cards, no CoS, no publish.

If a payloads-<date>.json exists and --fresh is NOT passed, reuses the cached
payloads to avoid re-fetching (SEC rate limits).
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

from discovery.quality_asymmetry.archetypes import run_shadow, scan_ticker

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def _payload_path() -> str:
    return os.path.join(OUTPUT_DIR, f"payloads-{date.today().isoformat()}.json")


def load_or_fetch(tickers: list[str] | None, fresh: bool) -> dict:
    path = _payload_path()
    if not fresh and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            cached = json.load(f)
        if tickers is None:
            return cached
        return {t: cached.get(t) for t in tickers if t in cached}
    from discovery.quality_asymmetry.fetcher import fetch_universe
    payloads = fetch_universe(tickers)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payloads, f, indent=1)
    return payloads


def summarize(evidence: list[dict]) -> str:
    lines = []
    for block in evidence:
        if "error" in block:
            lines.append(f"✗ {block['ticker']}: {block['error']}")
            continue
        hits = [a for a in block["archetypes"] if a["matched_count"] >= 2]
        label = ", ".join(f"{a['archetype']}({a['matched_count']})" for a in block["archetypes"])
        if hits:
            names = ", ".join(a["name"] for a in hits)
            lines.append(f"★ {block['ticker']} [{label}] → {names}")
        else:
            lines.append(f"· {block['ticker']} [{label}]")
    return "\n".join(lines)


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fresh = "--fresh" in sys.argv
    tickers = args or None
    payloads = load_or_fetch(tickers, fresh)

    blocks = []
    for t, p in payloads.items():
        if not p or "error" in p:
            blocks.append({"ticker": t, "error": p.get("error", "no payload")})
            continue
        fin = p.get("fin", {})
        market = p.get("market")
        blocks.append(scan_ticker(t, fin, market))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ev_path = os.path.join(OUTPUT_DIR, f"shadow-evidence-{date.today().isoformat()}.json")
    with open(ev_path, "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=1)

    print(f"evidence → {ev_path}\n")
    print(summarize(blocks))


if __name__ == "__main__":
    main()
