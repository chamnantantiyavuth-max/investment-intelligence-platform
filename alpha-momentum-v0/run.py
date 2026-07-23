#!/usr/bin/env python
"""
Alpha Momentum V0 — CLI Entry Point
Run: python run.py — executes pipeline and generates HTML reports.
"""
import sys
import os

# Ensure we can import from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from pipeline import run_pipeline
from display import render_all


def main():
    print("=" * 60)
    print("Alpha Momentum V0 — Pipeline Runner")
    print("=" * 60)
    print()

    # Run pipeline
    print("Running pipeline...")
    result = run_pipeline()

    # Print stage summary
    print()
    print("Pipeline Stages:")
    print("-" * 40)
    for s in result["stages"]:
        sid = s["stage_id"]
        name = s["stage"]
        val = s.get("output_count", s.get("passed_count",
             s.get("dimensions_assessed", s.get("total_candidates", "—"))))
        print(f"  {sid}  {name:<40} → {val}")

    # Queue summary
    queue = result["queue"]
    total = sum(len(td["candidates"]) for _, td in queue)
    empty = sum(1 for _, td in queue if len(td["candidates"]) == 0)

    print()
    print("Queue Summary:")
    print("-" * 40)
    print(f"  Themes in queue:      {len(queue)}")
    print(f"  Themes with candidates: {len(queue) - empty}")
    print(f"  Empty themes:          {empty}")
    print(f"  Total candidates:      {total}")
    if total == 0:
        print("  ⚠️  EMPTY QUEUE — Honest Empty State (DNA-016)")

    # Inbox summary
    anomalies = result.get("inbox_anomalies", [])
    hypotheses = result.get("inbox_hypotheses", [])
    print()
    print("Weak Signal Inbox:")
    print("-" * 40)
    print(f"  Anomalies:            {len(anomalies)}")
    print(f"  Theme Hypotheses:     {len(hypotheses)}")

    # Experimental summary
    experimental = result.get("experimental", {})
    if experimental.get("has_data"):
        exp_queue = experimental.get("queue", [])
        exp_total = sum(len(td["candidates"]) for _, td in exp_queue)
        print()
        print("Experimental Queue:")
        print("-" * 40)
        print(f"  Experimental themes:  {len(exp_queue)}")
        print(f"  Exp. candidates:      {exp_total}")

    # Render outputs
    print()
    print("Rendering HTML...")
    outputs = render_all(result)

    print()
    print("Output Files:")
    print("-" * 40)
    for key, path in outputs.items():
        if isinstance(path, list):
            print(f"  {key}: {len(path)} files")
            for p in path[:3]:
                print(f"    → {p}")
            if len(path) > 3:
                print(f"    ... and {len(path) - 3} more")
        else:
            print(f"  {key}: {path}")

    print()
    print("=" * 60)
    print(f"Run ID: {result['run_id']}")
    print(f"Pipeline: {result['pipeline_version']}")
    print(f"NOT LIVE DATA — FOR V0 TESTING ONLY")
    print("=" * 60)

    # Open queue in browser (Windows)
    queue_path = outputs.get("queue")
    if queue_path and os.name == "nt":
        os.startfile(queue_path)


if __name__ == "__main__":
    main()
