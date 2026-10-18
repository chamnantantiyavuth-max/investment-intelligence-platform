"""RSR-01 stage moves that SM-3 already allows.

SCUTTLEBUTT and CHARTER stay short of COMPLETE unless the caller passes
a contract predicate that is true. INCOMPLETE is a legal IN_PROGRESS edge.
NOT_STARTED cannot jump to INCOMPLETE; the path goes through IN_PROGRESS.
"""

from __future__ import annotations

from qad.models.family_c import (
    ResearchStageRecord,
    ResearchStageRecordStage_state,
)
from qad.persistence.errors import ImmutabilityViolation, TransactionFailure


class StageCompletionRejected(Exception):
    """COMPLETE was requested without the contract predicate."""


def _enum(value: object) -> str:
    return getattr(value, "value", value)  # type: ignore[return-value]


def find_stage(registry, case_id: str, stage_name: str) -> ResearchStageRecord:
    matches = [
        row
        for row in registry.list_all("RSR-01")
        if row.case_id == case_id and _enum(row.stage_name) == stage_name
    ]
    if len(matches) != 1:
        raise KeyError(f"{case_id} {stage_name}: found {len(matches)} stage rows")
    return matches[0]


def _path(current: str, target: str) -> list[str]:
    if current == target:
        return []
    if current == "NOT_STARTED" and target == "IN_PROGRESS":
        return ["IN_PROGRESS"]
    if current == "NOT_STARTED" and target == "INCOMPLETE":
        return ["IN_PROGRESS", "INCOMPLETE"]
    if current == "IN_PROGRESS" and target in {"IN_PROGRESS", "COMPLETE", "FAILED", "INCOMPLETE", "SKIPPED"}:
        return [] if target == "IN_PROGRESS" else [target]
    raise StageCompletionRejected(
        f"no SM-3 path from {current} to {target}"
    )


def transition_stage(
    registry,
    case_id: str,
    stage_name: str,
    target: str,
    issue: str,
    output_ids: list[str] | None = None,
    *,
    complete_allowed: bool = False,
) -> ResearchStageRecord:
    """Move a stage forward. Identity fields and started_at stay put."""
    if target == "COMPLETE" and not complete_allowed:
        raise StageCompletionRejected(
            f"{stage_name} COMPLETE is not allowed until the contract predicate is true"
        )
    current = find_stage(registry, case_id, stage_name)
    steps = _path(_enum(current.stage_state), target)
    outputs = list(dict.fromkeys([*(current.output_ids or []), *(output_ids or [])]))
    issues = list(current.issues or [])
    if issue and issue not in issues:
        issues.append(issue)
    if not steps and issues == list(current.issues or []) and outputs == list(current.output_ids or []):
        return current
    # Apply the note on the first write, then only the state on later steps.
    pending_issue = True
    for step in steps or [_enum(current.stage_state)]:
        current = find_stage(registry, case_id, stage_name)
        update = {
            "stage_state": ResearchStageRecordStage_state(step),
            "output_ids": outputs,
        }
        if pending_issue:
            update["issues"] = issues
            pending_issue = False
        updated = current.model_copy(update=update)
        try:
            registry.store(updated)
        except (ImmutabilityViolation, TransactionFailure):
            # A terminal stage cannot take another issue. IN_PROGRESS can.
            if not steps and _enum(current.stage_state) != "IN_PROGRESS":
                return find_stage(registry, case_id, stage_name)
            raise
        if not steps:
            break
    loaded = find_stage(registry, case_id, stage_name)
    if (
        loaded.stage_id != current.stage_id
        or loaded.started_at != current.started_at
        or loaded.responsible_role != current.responsible_role
    ):
        raise RuntimeError("stage identity, start, or responsible role changed")
    return loaded
