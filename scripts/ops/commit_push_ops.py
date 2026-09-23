"""Explicit-path stage -> commit -> push ops/automation -> fetch -> verify remote SHA.

Never `git add -A`. Never push main. On push failure: PRESERVE the local commit,
exit non-zero (no reset) — the next run's G0 sees case C and refuses a new job
until the exact commit is recovered (FD #142 §10, §11).
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

import ops_config
import ops_git
from validate_delta import validate_delta


def commit_push_ops(job_id: str, worktree: str | Path, repo: str | Path, base: str,
                    do_push: bool = True, message: str | None = None) -> dict:
    cwd = Path(worktree)
    res: dict = {"ok": False, "commit": "", "remote_verified": False, "reason": ""}

    vres = validate_delta(job_id, cwd, base)
    if not vres["ok"]:
        res["reason"] = f"delta validation FAILED: {vres['violations']}"
        return res

    allowed_paths = [a["path"] for a in vres["allowed"]]
    if not allowed_paths:
        res["reason"] = "no allowed artifact paths to commit (empty delta?)"
        return res

    # explicit-path stage only
    ops_git.run_git(cwd, "add", "--", *allowed_paths)
    staged = ops_git.run_git(cwd, "diff", "--cached", "--name-only").splitlines()
    staged = [s.strip() for s in staged if s.strip()]
    if set(staged) != set(allowed_paths):
        res["reason"] = f"staged set mismatch: staged={staged} vs allowed={allowed_paths}"
        return res

    msg = message or (
        f"ops(automation): {ops_config.JOB_NAMES.get(job_id, job_id)} artifact "
        f"{_dt.date.today().isoformat()} [{job_id}] (base {base[:12]})"
    )
    ops_git.run_git(cwd, "commit", "-m", msg)
    res["commit"] = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()

    if do_push:
        try:
            ops_git.run_git(cwd, "push", "origin", ops_config.OPS_BRANCH)
            ops_git.run_git(cwd, "fetch", "origin")
            remote = ops_git.run_git(cwd, "rev-parse",
                                     "origin/ops/automation").strip()
            if remote != res["commit"]:
                res["reason"] = f"remote verify FAILED: remote={remote} local={res['commit']}"
                return res
            res["remote_verified"] = True
            state = ops_config.load_state()
            state["last_pushed_ops_sha"] = res["commit"]
            ops_config.save_state(state)
        except ops_git.OpsGitError as e:
            res["reason"] = (
                "PUSH FAILED — local artifact commit PRESERVED (never reset). "
                "No new cron run until recovery. "
                f"detail: {str(e)[:300]}"
            )
            return res

    res["ok"] = True
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ explicit artifact commit + push + verify")
    ap.add_argument("--job", required=True)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--base", default=None)
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    base = args.base
    if base is None:
        state = ops_config.load_state()
        base = state.get("ops_sync_base_sha") or ""
    if not base:
        print("no base sha (run sync_main_to_ops first)", file=sys.stderr)
        return 2

    res = commit_push_ops(args.job, args.worktree, args.repo, base, do_push=not args.no_push)
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7