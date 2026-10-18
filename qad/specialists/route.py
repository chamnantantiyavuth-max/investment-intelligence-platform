"""Route a case's evidence gaps to specialist charters.

Example:
    python -m qad.specialists.route --case CASE-2026-001 --max 3 \\
        --out research/qad-cases/CASE-2026-001/charters/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from qad.specialists.routing import route_case, write_artifacts
from research.qad_pilot.unh.case_slice import recover_case


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Research Director specialist router")
    parser.add_argument("--case", required=True)
    parser.add_argument("--max", type=int, default=3)
    parser.add_argument("--out", required=True)
    parser.add_argument("--founder-priority-file", default=None)
    parser.add_argument("--no-founder-priority", action="store_true")
    args = parser.parse_args(argv)
    bundle = recover_case(args.case)
    priority = None
    priority_path = (
        Path(args.founder_priority_file)
        if args.founder_priority_file
        else Path("research/qad-cases") / args.case / "founder-priority.json"
    )
    if not args.no_founder_priority and priority_path.is_file():
        priority = json.loads(priority_path.read_text(encoding="utf-8"))
    result = route_case(bundle, max_n=args.max, founder_priority=priority)
    written = write_artifacts(result, Path(args.out), bundle.registry)
    print(
        json.dumps(
            {
                "case_id": result.case_id,
                "override_applied": result.override["applied"],
                "selected": [
                    {
                        "gap_id": item.gap_id,
                        "specialist_id": item.specialist_id,
                        "budget": item.budget,
                        "task": f"{item.gap_id}.task.json",
                    }
                    for item in result.selected
                ],
                "files": [str(path) for path in written],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
