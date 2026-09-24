"""MAIN -> OPS SYNC LIFECYCLE (FD #142 §5, R0.1-A correction, 24 Sep 2026).

OPS_AHEAD is the NORMAL state after every cron artifact commit (`main = A`,
`ops = A -> artifact_commit`); it is NOT an error. Sync accepts the full
S0/S1/S2/S3 lifecycle:

  S0 SAME          ops == main                          -> no-op, base = ops HEAD
  S1 MAIN AHEAD    ops is ancestor of main              -> ff ops to main,
                                                           push/verify ops baseline,
                                                           base = resulting ops HEAD
  S2 OPS AHEAD     main is ancestor of ops              -> NO merge, NO reset,
                                                           artifact history preserved,
                                                           base = current ops HEAD
  S3 DIVERGED      neither is ancestor                  -> attempt normal `main -> ops`
                                                           merge in the OPS worktree only.
                                                           Clean  -> push/verify, base = merge HEAD
                                                           Conflict -> abort, verify clean
                                                           worktree, preserve pre-merge ops
                                                           HEAD, FAIL CLOSED. Never touch main.

Pre-condition (remote-first): BEFORE evaluating main vs ops, local ops is
fast-forwarded to origin/ops/automation (--ff-only) and verified equal. A true
local/remote ops divergence must be blocked by G0 earlier — sync never resolves
it silently.

Durable baseline (R0.1 §4): if S1 or S3 changes ops HEAD, the new baseline is
PUSHED and remote-verified BEFORE OPS_SYNC_BASE_SHA is stored. Otherwise an
unpushed sync commit plus a mid-run job failure would make the next G0 see a
false case-C (local ahead) condition.

Arrow is ALWAYS main -> ops. No reverse direction. No rebase. No history
rewrite. No automatic conflict resolution.
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
    result: dict = {"ok": False, "sync_case": "", "ops_sync_base_sha": "",
                    "reason": "", "remote_verified": False}

    if do_fetch:
        ops_git.run_git(cwd, "fetch", "origin")

    # G0-E defense (G0 normally blocks dirty before sync; never proceed dirty)
    if ops_git.porcelain(cwd):
        result["reason"] = "sync FAIL CLOSED: worktree dirty — G0 case E must block first"
        return result

    h = ops_git.heads(cwd)
    main = h["origin_main"]
    if not main:
        result["reason"] = "origin/main unavailable"
        return result
    local = h["local_head"]
    origin_ops = h["origin_ops"]
    if not local:
        result["reason"] = "no local HEAD on ops worktree"
        return result

    # ---- remote-first: synchronize LOCAL ops to origin/ops/automation ---------
    # (G0 case B contract: sync performs the --ff-only; case C/D are G0 blocks)
    if origin_ops and local != origin_ops:
        if ops_git.is_ancestor(cwd, local, origin_ops):
            ops_git.run_git(cwd, "merge", "--ff-only", "origin/ops/automation")
            local = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()
            if local != origin_ops:
                result["reason"] = (
                    "sync FAIL CLOSED: post-ff verify failed — local ops != origin/ops/automation"
                )
                return result
        elif ops_git.is_ancestor(cwd, origin_ops, local):
            result["reason"] = (
                "sync FAIL CLOSED: local ops is AHEAD of origin/ops/automation (unpushed sync/artifact "
                "commit). G0 case C must block and recover the exact existing commit — sync never "
                "resolves local-ahead."
            )
            return result
        else:
            result["reason"] = (
                "sync FAIL CLOSED: local ops and origin/ops/automation DIVERGED — G0 case D must "
                "block; sync never resolves divergence silently."
            )
            return result

    # ---- evaluate main vs ops: S0 / S1 / S2 / S3 ------------------------------
    ops_changed = False
    if local == main:
        base = local
        result["sync_case"] = "S0"
        result["reason"] = "S0 same: ops == main, no-op"
    elif ops_git.is_ancestor(cwd, local, main):
        ops_git.run_git(cwd, "merge", "--ff-only", "origin/main")
        base = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()
        ops_changed = True
        result["sync_case"] = "S1"
        result["reason"] = f"S1 main ahead: fast-forwarded ops to {base[:12]}"
    elif ops_git.is_ancestor(cwd, main, local):
        base = local
        result["sync_case"] = "S2"
        result["reason"] = "S2 ops ahead: main is ancestor of ops — artifact history preserved, no merge"
    else:
        # S3 true divergence: normal main -> ops merge in the ops worktree only.
        pre_merge = local
        try:
            ops_git.run_git(cwd, "merge", "--no-edit", "origin/main")
        except ops_git.OpsGitError as e:
            try:
                ops_git.run_git(cwd, "merge", "--abort")
            except ops_git.OpsGitError:
                pass
            now = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()
            if now != pre_merge or ops_git.porcelain(cwd):
                result["reason"] = (
                    "sync FAIL CLOSED: merge abort left an unexpected state — ops HEAD/residue "
                    "must be inspected manually"
                )
            else:
                result["reason"] = (
                    "sync FAIL CLOSED: main->ops merge CONFLICT — aborted; ops HEAD preserved at "
                    f"{pre_merge}; worktree clean; main untouched; no remote ops mutation."
                    f" detail: {str(e)[:200]}"
                )
            return result
        base = ops_git.run_git(cwd, "rev-parse", "HEAD").strip()
        ops_changed = True
        result["sync_case"] = "S3"
        result["reason"] = f"S3 diverged: clean main->ops merge created {base[:12]}"

    # ---- durable remote baseline (R0.1 §4) ------------------------------------
    if ops_changed:
        try:
            ops_git.run_git(cwd, "push", "origin", ops_config.OPS_BRANCH)
            ops_git.run_git(cwd, "fetch", "origin")
            remote = ops_git.run_git(cwd, "rev-parse", "origin/ops/automation").strip()
        except ops_git.OpsGitError as e:
            result["reason"] = (
                "sync FAIL CLOSED: baseline PUSH FAILED — local sync commit PRESERVED (never reset); "
                "OPS_SYNC_BASE_SHA NOT stored; job MUST NOT start; next G0 case C blocks until the "
                f"exact sync commit is pushed. detail: {str(e)[:200]}"
            )
            return result
        if remote != base:
            result["reason"] = (
                f"sync FAIL CLOSED: remote verify failed — origin/ops/automation {remote[:12]} "
                f"!= local {base[:12]}"
            )
            return result
        result["remote_verified"] = True

    result.update({"ok": True, "ops_sync_base_sha": base})
    if persist:
        _persist(base, result)
    return result


def _persist(base: str, result: dict) -> None:
    state = ops_config.load_state()
    state["ops_sync_base_sha"] = base
    ops_config.save_state(state)
    result["state_file"] = str(ops_config.state_dir() / "ops-state.json")


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ main->ops sync lifecycle (S0/S1/S2/S3)")
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

# footer: 2026-09-24 12:20 UTC+7 (R0.1-A lifecycle correction)
