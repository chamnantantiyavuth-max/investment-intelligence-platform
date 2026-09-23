"""MAIN -> OPS SYNC (FD #142 §5).

After G0 succeeds: sync origin/main -> ops/automation ONLY (never reverse).
Merge allowed only as a mechanical fast-forward; conflict/divergence = FAIL CLOSED.
After successful sync captures OPS_SYNC_BASE_SHA (persisted in ops state) — the
baseline the next cron job's delta is validated against.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ops_config
import ops_git


def sync_main_to_ops(worktree: str | Path, repo: str | Path, do_fetch: bool = True,
                     persist: bool = True) -> dict:
    cwd = Path(worktree)
    repo = str(repo)
    result: dict = {"ok": False, "ops_sync_base_sha": "", "reason": ""}

    if do_fetch:
        ops_git.run_git(cwd, "fetch", "origin")

    h = ops_git.heads(cwd)
    main = h["origin_main"]
    if not main:
        result["reason"] = "origin/main unavailable"
        return result
    local = h["local_head"]

    if local == main:
        base = local
        result.update({"ok": True, "ops_sync_base_sha": base})
        if persist:
            _persist(base, result)
        return result

    if ops_git.is_ancestor(cwd, local, main):
        # mechanical fast-forward only
        ops_git.run_git(cwd, "merge", "--ff-only", "origin/main")
        base = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()
        result.update({"ok": True, "ops_sync_base_sha": base, "reason": "fast-forwarded"})
        if persist:
            _persist(base, result)
        return result

    result["reason"] = (
        "sync FAIL CLOSED: ops is not an ancestor of origin/main (diverged or ahead). "
        "No merge, no reset, no auto-resolution."
    )
    return result


def _persist(base: str, result: dict) -> None:
    state = ops_config.load_state()
    state["ops_sync_base_sha"] = base
    ops_config.save_state(state)
    result["state_file"] = str(ops_config.state_dir() / "ops-state.json")


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ main->ops sync (fast-forward only)")
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--no-persist", action="store_true")
    args = ap.parse_args()
    res = sync_main_to_ops(args.worktree, args.repo, do_fetch=not args.no_fetch,
                           persist=not args.no_persist)
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7