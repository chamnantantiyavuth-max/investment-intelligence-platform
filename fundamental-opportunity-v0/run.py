"""
Fundamental & Opportunity V0 — Run Entry Point
Spike version — validates the 6-stage pipeline end-to-end.
"""
import sys
import os

# Add self dir so we can import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline
from display import render_full_report


def main():
    print("=" * 60)
    print("Fundamental & Opportunity V0 — Spike")
    print("Pipeline v0.1.0 · Phase 8 · FD #40")
    print("SYNTHETIC FIXTURES — NOT LIVE DATA")
    print("=" * 60)

    packages = run_pipeline()
    print(f"\nPipeline complete: {len(packages)} companies assessed.\n")

    for pkg in packages:
        moat = pkg["company_assessment"]["moat"]
        eq = pkg["earnings_trajectory"]
        conv = pkg["conviction"]
        vt = pkg["valuation_context"].get("value_trap", {})
        trap_verdict = vt.get("verdict", "N/A") if vt.get("triggered") else "Not flagged"

        print(f"  {pkg['name']} ({pkg['id']}):")
        print(f"    Moat: {moat['width']} / {moat['depth']} / {moat['trend']} "
              f"({moat['active_count']} active types)")
        print(f"    Earnings Quality: {eq['rating']} — {eq['conviction_impact']}")
        print(f"    Conviction: {conv['level']} (cap: {conv['cap']})")
        print(f"    Value Trap: {trap_verdict}" +
              (f" (score: {vt.get('score')}/{vt.get('max_score')})" if vt.get("triggered") else ""))
        print(f"    Challenges: {len(pkg['independent_challenge'])} found")
        print()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    json_path = os.path.join(output_dir, "pipeline_result.json")
    html_path = os.path.join(output_dir, "research_packages.html")

    html = render_full_report(packages, json_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Output files:")
    print(f"  HTML: {html_path}")
    print(f"  JSON: {json_path}")
    print(f"\nOpen {html_path} in browser to view Research Packages.")
    print("=" * 60)


if __name__ == "__main__":
    main()
