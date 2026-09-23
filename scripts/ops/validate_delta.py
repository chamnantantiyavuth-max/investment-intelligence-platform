"""CRON-DELTA AUTHORITY (FD #142 §6, §7, §8).

Validates ONLY the delta base_sha (OPS_SYNC_BASE_SHA) -> job-produced working state.
Never evaluates previous-ops-head -> new-ops-head (that would falsely classify
legitimate main->ops sync changes as cron writes).

Rules:
  - every changed path must fullmatch the job's anchored allowlist
  - allowlist EMPTY (Learning Loop) + any delta = FAIL
  - any denylist hit = FAIL (allowlist PASS never overrides)
  - deletions: always FAIL unless the allowlist explicitly permits them (none do)
  - renames: always FAIL (source or dest must be allowed; default no renames)
  - untracked/unexplained files = FAIL (fail closed)

Exit 0 = PASS; 3 = violations; 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ops_config
import ops_git

# status chars from `git diff --name-status`
_ADDED = {"A"}
_DELETED = {"D"}
_RENAMED = {"R"}
_MODIFIED = {"M", "T", "U", "X", "B"}


def collect_delta(worktree: str | Path, base: str) -> list[dict]:
    """[{path, status}] relative to worktree root, base -> working tree (incl. untracked)."""
    cwd = Path(worktree)
    out = ops_git.run_git(cwd, "diff", "--find-renames", "--name-status", base)
    rows: list[dict] = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status = parts[0][0]
        # R100\tsrc\tdst ; M\tpath ; A\tpath ; D\tpath
        if status in _RENAMED and len(parts) >= 3:
            rows.append({"path": parts[1], "status": "R", "dest": parts[2]})
        else:
            rows.append({"path": parts[-1], "status": status})
    # untracked (job-created files are untracked until staged)
    for u in ops_git.run_git(cwd, "ls-files", "--others", "--exclude-standard").splitlines():
        if u.strip():
            rows.append({"path": u.strip(), "status": "A"})
    return rows


def validate_delta(job_id: str, worktree: str | Path, base: str) -> dict:
    if not ops_config.job_exists(job_id):
        return {"ok": False, "job": job_id, "violations": [f"unknown job id {job_id!r}"]}
    delta = collect_delta(worktree, base)
    violations: list[str] = []

    for row in delta:
        path, status = row["path"], row["status"]
        try:
            rel = ops_config.normalize_rel(path)
        except ValueError as e:
            violations.append(f"FAIL path escapes root: {path!r} ({e})")
            continue

        if ops_config.is_denied(rel):
            violations.append(f"FAIL denylist hit: {path}")
            continue
        if status in _DELETED:
            violations.append(f"FAIL deletion not allowed: {path}")
            continue
        if status in _RENAMED:
            violations.append(f"FAIL rename not allowed: {path} -> {row.get('dest')}")
            continue
        if not ops_config.allowed_for(job_id, rel):
            kind = "unknown/unallowed path" if status in _MODIFIED | _ADDED else f"status {status}"
            violations.append(f"FAIL {kind}: {path}")

    allowed = []
    for r in delta:
        path, status = r["path"], r["status"]
        try:
            rel = ops_config.normalize_rel(path)
        except ValueError:
            continue
        if status in _DELETED or status in _RENAMED:
            continue
        if ops_config.is_denied(rel):
            continue
        if ops_config.allowed_for(job_id, rel):
            allowed.append({"path": path, "status": status})
    return {
        "ok": not violations,
        "job": job_id,
        "base_sha": base,
        "delta": [{"path": r["path"], "status": r["status"]} for r in delta],
        "allowed": allowed,
        "violations": violations,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ cron-delta validator")
    ap.add_argument("--job", required=True)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--base", default=None,
                    help="OPS_SYNC_BASE_SHA (default: ops state, else origin/ops/automation)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    base = args.base
    if base is None:
        state = ops_config.load_state()
        base = state.get("ops_sync_base_sha") or ""
    if not base:
        try:
            base = ops_git.run_git(args.worktree, "rev-parse", "origin/ops/automation").strip()
        except ops_git.OpsGitError:
            print("no base sha available (run sync_main_to_ops first)", file=sys.stderr)
            return 2

    res = validate_delta(args.job, args.worktree, base)
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7