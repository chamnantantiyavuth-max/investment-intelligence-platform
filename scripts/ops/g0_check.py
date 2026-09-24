"""G0 PRESERVATION GATE (FD #142 §4, hard invariant).

Runs BEFORE every cron run in repo-ops. NEVER resets, NEVER discards. Cases:
  A equal + clean            -> continue
  B local behind (ff-ready)  -> continue (sync step performs the fast-forward)
  C local ahead (push fail)  -> BLOCK: no reset, no new job; push-recovery only
  D diverged                 -> FAIL CLOSED
  E dirty / untracked residue -> FAIL CLOSED and preserve

Exit 0 = safe to continue; 1 = blocked (JSON reason); 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import ops_config
import ops_git


def g0_check(worktree: str | Path, repo: str | Path, do_fetch: bool = True) -> dict:
    cwd = Path(worktree)
    repo = str(repo)
    result: dict = {"ok": False, "case": None, "local_head": "", "remote_head": "", "reasons": []}

    # branch/worktree sanity
    try:
        branch = ops_git.current_branch(cwd)
    except ops_git.OpsGitError as e:
        result["reasons"] = [f"G0-E0 worktree unusable: {e}"]
        return result
    if branch != ops_config.OPS_BRANCH:
        result["reasons"] = [f"G0-E0 worktree is on '{branch}', expected '{ops_config.OPS_BRANCH}'"]
        return result

    # ops-state FAIL-CLOSED (R0.3 §6): corrupt/unreadable/structurally-malformed
    # existing state is NEVER interpreted as 'no lock' — G0 returns STATE_CORRUPT
    # and every governed gate holds until the state is repaired/reviewed.
    try:
        ops_config.load_state()
    except ops_config.StateError as e:
        result["case"] = "STATE_CORRUPT"
        result["reasons"] = [
            "G0-STATE_CORRUPT " + str(e) + " — FAIL CLOSED; ops-state carries the "
            "promotion-pending lock, approval receipt and recovery identity, so "
            "corrupt state must be repaired/reviewed, never silently treated as "
            "empty. (R0.3 §6)"
        ]
        return result

    # promotion-pending lock (R0.2 §14): a Founder-review P1 manifest exists or a
    # promotion awaits recovery — artifact jobs FAIL CLOSED; cleared ONLY after a
    # verified REAL P1 promotion or explicit cancellation/disposition.
    pending = ops_config.promotion_pending()
    if pending:
        result["case"] = "PENDING"
        result["reasons"] = [
            "G0-PENDING promotion_pending_manifest_id="
            f"{pending!r} — artifact jobs FAIL CLOSED while a P1 manifest awaits "
            "Founder review/recovery (mechanical pause, R0.2 §14); cleared only "
            "after a verified REAL P1 promotion or explicit cancellation."
        ]
        return result

    if do_fetch:
        try:
            ops_git.run_git(cwd, "fetch", "origin")
        except ops_git.OpsGitError as e:
            result["case"] = "FETCH"
            result["reasons"] = [f"G0-FETCH fail closed: cannot determine remote state ({str(e)[:120]})"]
            return result

    dirty = ops_git.porcelain(cwd)
    if dirty:
        result["case"] = "E"
        result["reasons"] = [
            "G0-E dirty/untracked output exists — FAIL CLOSED and preserve (never reset/clean). "
            f"entries={dirty[:10]}"
        ]
        result["local_head"] = ops_git.heads(cwd)["local_head"]
        return result

    h = ops_git.heads(cwd)
    result["local_head"] = h["local_head"]
    result["remote_head"] = h["origin_ops"]

    if not h["local_head"]:
        result["case"] = "E0"
        result["reasons"] = ["G0-E0 no local HEAD on ops worktree"]
        return result
    if not h["origin_ops"]:
        # remote branch missing entirely (first bootstrap only, before first push)
        result["case"] = "A"
        result["ok"] = True
        result["reasons"] = ["G0-A remote ops/automation absent (pre-first-push bootstrap); local is clean"]
        return result

    if h["local_head"] == h["origin_ops"]:
        result["case"] = "A"
        result["ok"] = True
        return result

    if ops_git.is_ancestor(cwd, h["local_head"], h["origin_ops"]):
        result["case"] = "B"
        result["ok"] = True
        result["reasons"] = ["G0-B local behind remote, no local commits — fast-forward via sync step"]
        return result

    if ops_git.is_ancestor(cwd, h["origin_ops"], h["local_head"]):
        result["case"] = "C"
        result["reasons"] = [
            "G0-C local AHEAD of remote (earlier push failed) — DO NOT RESET, DO NOT RUN NEW JOB; "
            "attempt exact push recovery of the existing commit only."
        ]
        return result

    result["case"] = "D"
    result["reasons"] = ["G0-D local/remote DIVERGED — FAIL CLOSED (no merge, no reset)"]
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ G0 preservation gate")
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--no-fetch", action="store_true")
    args = ap.parse_args()
    res = g0_check(args.worktree, args.repo, do_fetch=not args.no_fetch)
    print(json.dumps(res, indent=2, sort_keys=True))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7