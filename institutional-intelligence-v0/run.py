"""
Institutional Intelligence V0 — Run Entry Point

Usage:
    python run.py                        # synthetic fixtures
    python run.py --ticker AAPL          # filter by ticker
    python run.py --fund 0001067983      # filter by fund CIK
    python run.py --top 5                # top N signals only

SYNTHETIC FIXTURES — FOR V0 TESTING ONLY.
FD #42 · Phase 10 · 26 July 2026
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline, query_signals_by_ticker, query_signals_by_fund, query_top_conviction
from display import render_report
from watchlist import summary as watchlist_summary


def main():
    parser = argparse.ArgumentParser(description="Institutional Intelligence V0 — Pipeline Runner")
    parser.add_argument("--ticker", type=str, default=None, help="Filter signals by ticker")
    parser.add_argument("--fund", type=str, default=None, help="Filter signals by fund CIK")
    parser.add_argument("--top", type=int, default=20, help="Show top N signals (default: 20)")
    parser.add_argument("--min-conviction", type=str, default=None,
                        choices=["Maximum", "High", "Moderate", "Low", "Minimal"],
                        help="Filter by minimum conviction level")
    parser.add_argument("--watchlist", action="store_true", help="Show watchlist summary only")
    parser.add_argument("--json-only", action="store_true", help="JSON output only — skip HTML")
    args = parser.parse_args()

    if args.watchlist:
        print("Super-Investor Watchlist:")
        print(watchlist_summary())
        return

    print("=" * 60)
    print("Institutional Intelligence V0 — Pipeline")
    print("Pipeline v0.1.0 · Phase 10 · FD #42")
    print("SYNTHETIC FIXTURES — NOT LIVE DATA")
    print("=" * 60)

    result = run_pipeline()
    signals = result["signals"]

    # Apply filters
    if args.ticker:
        signals = query_signals_by_ticker(args.ticker, signals)
        print(f"\nFiltered by ticker: {args.ticker.upper()} → {len(signals)} signals")
    if args.fund:
        signals = query_signals_by_fund(args.fund, signals)
        print(f"Filtered by fund CIK: {args.fund} → {len(signals)} signals")
    if args.min_conviction:
        signals = query_top_conviction(signals, args.min_conviction)
        print(f"Filtered by conviction >= {args.min_conviction} → {len(signals)} signals")

    # Update result with filtered signals
    result["signals"] = signals
    result["summary"]["total_signals"] = len(signals)
    result["summary"]["top_signals"] = signals[:args.top]

    # Display
    for s in signals[:args.top]:
        print(f"\n  {s['filer_name']} | {s['ticker']}")
        print(f"    {s['pct_of_portfolio']:.1f}% of portfolio | Conviction: {s['conviction']} | Action: {s['action']}")
        print(f"    Score: {s['signal_score']} | {s['action_detail']}")

    print(f"\n{'─' * 40}")
    print(f"Signals: {len(signals)} (showing top {min(args.top, len(signals))})")

    # Output
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    json_path = os.path.join(output_dir, "institutional_signals.json")
    html_path = os.path.join(output_dir, "institutional_signals.html")

    html = render_report(result, json_path=json_path)
    print(f"JSON saved: {json_path}")

    if not args.json_only:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML saved: {html_path}")
        print(f"\nOpen {html_path} in browser.")

    print("=" * 60)


if __name__ == "__main__":
    main()
