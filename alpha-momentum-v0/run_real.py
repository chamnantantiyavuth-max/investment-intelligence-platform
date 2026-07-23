"""
Alpha Momentum V0.5 — Real Data Pipeline Runner
Fetches EOD data via source_adapter.py (system Python 3.14),
merges with fixture structure, runs pipeline, renders output.
"""
import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).parent
SYSTEM_PYTHON = r"C:\Users\Admin\AppData\Local\Programs\Python\Python314\python.exe"
CACHE_DIR = HERE / "data" / "cache"
OUTPUT_DIR = HERE / "output"

# Import V0 pipeline
from pipeline import run_pipeline
from display import render_all


def fetch_eod(force_refresh: bool = False):
    """Run source_adapter.py with system Python to fetch/cache EOD data."""
    adapter = HERE / "source_adapter.py"
    args = [SYSTEM_PYTHON, str(adapter)]
    if force_refresh:
        args.append("--refresh")
    result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("❌ source_adapter.py failed:")
        print(result.stderr)
        sys.exit(1)
    print(result.stdout)


def load_eod_cache() -> dict[str, dict]:
    """Load all cached EOD data from JSON files."""
    eod = {}
    for f in sorted(CACHE_DIR.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        ticker = data.get("ticker", f.stem)
        # Skip error entries
        if "error" in data:
            print(f"⚠️  {ticker}: {data['error']}")
            continue
        eod[ticker] = data
    return eod


def run():
    print("=" * 60)
    print("Alpha Momentum V0.5 — Real EOD Pipeline")
    print("=" * 60)

    # Step 1: Fetch data
    print("\n[1/4] Fetching EOD data...")
    fetch_eod()

    # Step 2: Load cache
    print("\n[2/4] Loading cache...")
    eod = load_eod_cache()
    print(f"  {len(eod)} tickers loaded")
    for t, d in eod.items():
        p = d.get("price", {}) or {}
        print(f"  {t}: ${p.get('close','?')} — {d.get('name','?')[:45]}")

    # Step 3: Run pipeline with real data enrichment
    print("\n[3/4] Running pipeline (real data)...")
    result = run_pipeline()

    # Enrich candidates with real EOD data
    for tid, tdata in result["queue"]:
        for c in tdata["candidates"]:
            ticker = c.get("ticker", "")
            if ticker in eod:
                rd = eod[ticker]
                p = rd.get("price", {}) or {}
                c["_real_eod"] = {
                    "price_close": p.get("close"),
                    "price_as_of": p.get("as_of"),
                    "volume": p.get("volume"),
                    "market_cap": rd.get("market_cap"),
                    "pe_ratio": rd.get("pe_ratio"),
                    "name": rd.get("name"),
                    "sector": rd.get("sector"),
                    "fetched_at": rd.get("_fetched_at", ""),
                }
                # Update data confidence with real freshness
                dc = c.get("data_confidence", {})
                dc["freshness"] = f"Live — as of {p.get('as_of', 'unknown')}"
                dc["reliability"] = "High — Yahoo Finance EOD"
                c["data_confidence"] = dc

    # Update metadata
    result["pipeline_version"] = "v0.5.0"
    result["fixture_category"] = "REAL EOD — YAHOO FINANCE — FOR V0.5 DEVELOPMENT ONLY"
    result["point_in_time"] = datetime.now().strftime("%Y-%m-%d")

    # Step 4: Render
    print("\n[4/4] Rendering HTML...")
    outputs = render_all(result)

    print(f"\nOutput Files:")
    print(f"  queue: {outputs['queue']}")
    print(f"  inbox: {outputs.get('inbox', 'N/A')}")
    print(f"  theme_cards: {len(outputs['theme_cards'])} files")
    for p in outputs["theme_cards"]:
        print(f"    → {p}")
    print(f"  json: {outputs['json']}")

    print(f"\n{'=' * 60}")
    print(f"Run ID: {result['run_id']}")
    print(f"Pipeline: {result['pipeline_version']}")
    print(f"NOT LIVE TRADING DATA — FOR V0.5 DEVELOPMENT ONLY")
    print(f"{'=' * 60}")

    return result


if __name__ == "__main__":
    run()
