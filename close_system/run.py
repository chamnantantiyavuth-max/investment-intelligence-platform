#!/usr/bin/env python
"""
Close System Product Radar V0 — CLI Entry Point
Run: python run.py — executes pipeline and generates HTML radar.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from pipeline import run_pipeline
from display import render_all


def main():
    print("=" * 60)
    print("Close System Product Radar V0 — Pipeline Runner")
    print("=" * 60)
    print()

    result = run_pipeline()

    # Stage summary
    print("Pipeline Stages:")
    print("-" * 40)
    for s in result["stages"]:
        sid = s["stage_id"]
        name = s["stage"]
        summary = ""
        if "passed_count" in s:
            summary = f"{s['passed_count']}/{s.get('input_count', '?')} passed"
        elif "eligible_count" in s:
            summary = f"{s['eligible_count']} eligible, {s.get('ineligible_count', 0)} ineligible"
        elif "selected_count" in s:
            summary = f"{s['selected_count']} products in universe"
        elif "total_products" in s:
            summary = f"{s['total_products']} total"
        print(f"  {sid}  {name:<35} → {summary}")

    # Radar summary
    radar = result["radar"]
    print()
    print("Radar Summary:")
    print("-" * 40)
    print(f"  🟢 Present to Founder:     {len(radar['present_to_founder'])}")
    print(f"  🟡 Deep Research:          {len(radar['deep_research'])}")
    print(f"  🔵 Radar Watchlist:        {len(radar['radar_watchlist'])}")
    print(f"  ⚪ Monitor / Wait:         {len(radar['monitor'])}")
    print(f"  🔴 Ineligible:             {len(radar['ineligible'])}")

    # Top picks
    top = radar["present_to_founder"] + radar["deep_research"]
    if top:
        print()
        print("Top Picks:")
        print("-" * 40)
        for p in top:
            print(f"  {p['ticker']:<8} {p['name']:<40} [{p['conviction']}] → {p['recommendation']}")

    # Render HTML
    print()
    print("Rendering HTML...")
    outputs = render_all(result)

    print()
    print("Output Files:")
    print("-" * 40)
    for key, path in outputs.items():
        print(f"  {key}: {path}")

    print()
    print("=" * 60)
    print(f"Run ID: {result['run_id']}")
    print(f"Pipeline: {result['pipeline_version']}")
    print(f"NOT LIVE DATA — SYNTHETIC FIXTURES FOR V0 TESTING ONLY")
    print("=" * 60)

    # Open radar in browser (Windows)
    radar_path = outputs.get("radar")
    if radar_path and os.name == "nt":
        os.startfile(radar_path)


if __name__ == "__main__":
    main()
