"""
Fundamental & Opportunity V0 — Run Entry Point
Supports: synthetic fixtures (default) and real data via yfinance (--real).

Usage:
    python run.py                    # synthetic fixtures (8 companies)
    python run.py --real             # yfinance real data (FO_TICKERS)
    python run.py --real --tickers AAPL,MSFT,NVDA  # specific tickers
    python run.py --real --refresh   # force re-fetch, ignore cache

Phase 9 · FD #41 · 26 July 2026
"""
import sys
import os
import argparse
import json

# Add self dir so we can import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline
from display import render_full_report


def main():
    parser = argparse.ArgumentParser(
        description="Fundamental & Opportunity V0 — Pipeline Runner"
    )
    parser.add_argument(
        "--real", action="store_true",
        help="Use yfinance real data instead of synthetic fixtures"
    )
    parser.add_argument(
        "--tickers", type=str, default=None,
        help="Comma-separated tickers (requires --real). Default: FO_TICKERS"
    )
    parser.add_argument(
        "--refresh", action="store_true",
        help="Force re-fetch from yfinance, ignore cache (requires --real)"
    )
    parser.add_argument(
        "--json-only", action="store_true",
        help="Output JSON only — skip HTML generation"
    )
    args = parser.parse_args()

    data_source = "SYNTHETIC"
    companies = None

    if args.real:
        from source_adapter import fetch_all

        tickers = None
        if args.tickers:
            tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

        print(f"Fetching real data via yfinance...")
        companies = fetch_all(tickers=tickers, force_refresh=args.refresh)
        data_source = "REAL EOD"
        print(f"  {len(companies)} companies fetched\n")
    else:
        data_source = "SYNTHETIC"

    print("=" * 60)
    print(f"Fundamental & Opportunity V0 — Pipeline")
    print(f"Pipeline v0.2.0 · Phase 9 · FD #41")
    print(f"DATA: {data_source}")
    print("=" * 60)

    packages = run_pipeline(companies=companies, mode="real" if data_source == "REAL EOD" else "synthetic")
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
        print(f"    Value Trap: {trap_verdict}"
              + (f" (score: {vt.get('score')}/{vt.get('max_score')})" if vt.get("triggered") else ""))
        print(f"    Challenges: {len(pkg['independent_challenge'])} found")
        print()

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    json_path = os.path.join(output_dir, "pipeline_result.json")
    html_path = os.path.join(output_dir, "research_packages.html")

    # Save JSON — envelope {run_id, provenance, packages} + atomic write (arch v0.4 §3/§6, FD #46)
    from datetime import datetime, timezone
    envelope = {
        "run_id": f"FO-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}",
        "provenance": {
            "source": "yfinance" if data_source == "REAL EOD" else "fixtures",
            "mode": "real" if data_source == "REAL EOD" else "synthetic",
            "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "coverage": f"{len(packages)}/{len(packages)}",
            "completeness": "complete",
            "hybrid": False,
        },
        "packages": packages,
    }
    tmp_path = json_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2, default=str, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, json_path)
    print(f"JSON saved: {json_path}")

    # HTML output
    if not args.json_only:
        html = render_full_report(packages, source=data_source)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML saved: {html_path}")
        print(f"\nOpen {html_path} in browser to view Research Packages.")

    print("=" * 60)


if __name__ == "__main__":
    main()
