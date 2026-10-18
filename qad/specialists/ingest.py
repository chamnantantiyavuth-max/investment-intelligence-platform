"""Ingest one specialist result file.

Example:
    python -m qad.specialists.ingest --case CASE-2026-001 \\
        --result research/qad-cases/CASE-2026-001/results/<gap-id>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from qad.specialists.ingestion import attach_role_from_task, ingest_result, load_charter_file
from qad.specialists.routing import reload_case_records
from research.qad_pilot.unh.case_slice import (
    FounderReadyRejected,
    assert_founder_ready_allowed,
    case_view,
    recover_case,
)


def _charter_for_gap(charter_dir: Path, gap_id: str) -> dict:
    path = charter_dir / f"{gap_id}.charter.json"
    charter = load_charter_file(path)
    return attach_role_from_task(charter, charter_dir / f"{gap_id}.task.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest a specialist result")
    parser.add_argument("--case", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--charters", default=None)
    parser.add_argument(
        "--verify-sources",
        action="store_true",
        help="Fetch https sources and write M6 receipt files. Case reads do not fetch.",
    )
    args = parser.parse_args(argv)
    result_path = Path(args.result)
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    charter_dir = Path(args.charters) if args.charters else result_path.parents[1] / "charters"
    bundle = recover_case(args.case, replay=False)
    reload_case_records(bundle, charter_dir)
    # Routing also moved stages. Rebuild leaves them NOT_STARTED, so replay
    # the stage note by loading the manifest only as a record of intent.
    # A result ingest moves SCUTTLEBUTT from NOT_STARTED through IN_PROGRESS.
    from qad.specialists.stages import transition_stage

    transition_stage(
        bundle.registry,
        bundle.case_id,
        "SCUTTLEBUTT",
        "IN_PROGRESS",
        "Result ingest reopened SCUTTLEBUTT on a rebuilt case.",
        [],
    )
    charter = _charter_for_gap(charter_dir, payload["gap_id"])
    manifest = json.loads((charter_dir / "route-manifest.json").read_text(encoding="utf-8"))
    issued = [row["gap_id"] for row in manifest["selected"]]
    ledger_path = charter_dir / "actor-ledger.json"
    ledger = []
    if ledger_path.is_file():
        ledger = [tuple(pair) for pair in json.loads(ledger_path.read_text(encoding="utf-8"))]
    reported_path = charter_dir / "reported-gaps.json"
    reported = set()
    if reported_path.is_file():
        reported = set(json.loads(reported_path.read_text(encoding="utf-8")))
    outcome = ingest_result(
        bundle,
        payload,
        charter,
        ledger,
        issued_ids=issued,
        reported_ids=reported,
        fetch_sources=bool(args.verify_sources),
        receipt_dir=result_path.parents[1] / "receipts",
    )
    deduped: list[tuple[str, str]] = []
    for pair in ledger:
        if pair not in deduped:
            deduped.append(pair)
    ledger = deduped
    reported.add(outcome.gap_id)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    reported_path.write_text(json.dumps(sorted(reported), indent=2) + "\n", encoding="utf-8")
    journal_dir = charter_dir.parent / "ingest"
    journal_dir.mkdir(parents=True, exist_ok=True)
    journal_path = journal_dir / f"{outcome.gap_id}.json"
    view = case_view(bundle)
    founder_ready = True
    try:
        assert_founder_ready_allowed(bundle.registry, bundle.case_id)
    except FounderReadyRejected:
        founder_ready = False
    journal = {
        "case_id": outcome.case_id,
        "gap_id": outcome.gap_id,
        "investigation_disposition": outcome.investigation_disposition,
        "ir_disposition": outcome.ir_disposition,
        "investigation_id": outcome.investigation_id,
        "admitted_count": len(outcome.admitted_evidence_ids),
        "quarantined_count": len(outcome.quarantined),
        "verified_fact_count": len(outcome.verified_fact_ids),
        "verified_fact_ids": outcome.verified_fact_ids,
        "preserved": outcome.preserved,
        "admitted_evidence_ids": outcome.admitted_evidence_ids,
        "admitted_source_ids": outcome.admitted_source_ids,
        "quarantined": outcome.quarantined,
        "gap_status": outcome.gap_status,
        "stage_state": outcome.stage_state,
        "case_state": view["case_state"],
        "founder_ready": founder_ready,
        "stages": [
            {
                "stage_name": row["stage_name"],
                "stage_state": row["stage_state"],
                "responsible_role": row["responsible_role"],
            }
            for row in view["stages"]
        ],
        "actor_id": outcome.actor_id,
        "canonical_role": outcome.canonical_role,
        "stop_rule_triggered": payload.get("stop_rule_triggered"),
        "usage": payload.get("usage"),
        "cross_retrieval": outcome.cross_retrieval,
    }
    journal_path.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "journal": str(journal_path),
                "admitted_count": journal["admitted_count"],
                "quarantined_count": journal["quarantined_count"],
                "gap_status": outcome.gap_status,
                "stage_state": outcome.stage_state,
                "case_state": view["case_state"],
                "founder_ready": founder_ready,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
