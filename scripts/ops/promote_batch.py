"""Deterministic multi-job P1 promotion helper (FD #142 §10–§13; R0.1-B; R0.2).

Exact file-content transfer from the FROZEN ops snapshot onto a target branch —
never a branch merge, never a broad cherry-pick, never an implicitly-newer
artifact. TOCTOU: current main MUST equal manifest_main_sha, else HOLD.

REAL P1 CONTRACT (R0.2 §2–§6): `into_primary=True` is reserved EXCLUSIVELY for
target_branch == 'main', MUST imply do_push=True, and may begin ONLY from the
exact reviewed canonical main SHA — local primary main clean + local HEAD ==
origin/main == manifest_main_sha. `into_primary + verify_only` is invalid
(verify-only must never dirty governed main; rehearse on a temporary worktree/
branch from frozen canonical main).

SUCCESS ORDER (R0.2 §4): verify contract -> fetch -> verify clean local main ->
verify local == origin == manifest_main_sha -> revalidate frozen ops snapshot +
artifact provenance -> transfer exact files -> explicit-path stage -> commit
governed main -> verify committed raw blobs -> push main -> fetch -> verify
origin/main == promotion commit -> ONLY THEN advance last_promoted_ops_sha, clear
the promotion-pending lock, persist receipt, remove interactive manifest residue.

REVALIDATION (R0.2 §10–§12): the manifest is editable JSON, so the consumer
re-derives authority: frozen ops head must still be in canonical origin/ops
lineage; the recomputed canonical batch delta (manifest_main..manifest_ops_head)
must EQUAL the manifest artifact set exactly (no omitted/added/deleted/renamed/
unknown/denylisted/ambiguous entries); per artifact the source_commit must be a
commit, be the LATEST path-touch within the frozen batch, exist at that commit,
still match the mechanically derived owning job, and hash to the manifest sha256
(raw git blob bytes).

FAILURE STATE (R0.2 §13): a real-P1 push/remote-verify failure after the local
promotion commit is created leaves `P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY` —
local commit PRESERVED, origin/main unchanged, last_promoted NOT advanced,
manifest preserved, no reset. `--recover` verifies the preserved commit
(parent == manifest_main_sha, artifact hashes == manifest) and retries the
EXACT push.

PROMOTION-PENDING LOCK (R0.2 §14): writing a manifest sets
promotion_pending_manifest_id in external ops-state (NOT a repo write); artifact
cron preflight / G0 FAILS CLOSED while it is set. Cleared ONLY by a verified REAL
P1 success or explicit cancellation.

Canary (into_primary=False) may use temporary target branches, may push them, and
NEVER advances last_promoted, NEVER touches promotion state, NEVER removes the
review manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import ops_config
import ops_git

_ARTIFACT_REQUIRED = ("path", "job_id", "source_commit", "sha256")


def load_manifest(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for req in ("manifest_id", "batch_base_sha", "manifest_main_sha",
                "manifest_ops_head_sha", "artifacts"):
        if req not in data:
            raise ValueError(f"manifest missing required field {req!r}")
    if not isinstance(data["artifacts"], list) or not data["artifacts"]:
        raise ValueError("manifest has no artifacts")
    for art in data["artifacts"]:
        for req in _ARTIFACT_REQUIRED:
            if req not in art:
                raise ValueError(f"manifest artifact missing required field {req!r}: {art.get('path')}")
    return data


def _remove_worktree_manifest(manifest_path: str | Path, operations_worktree: str | Path) -> None:
    """R0.1 §14: after a successful REAL P1, drop the interactive manifest residue
    from the automation worktree so G0 returns clean (gitignored + reproducible).
    Canary NEVER removes it (R0.2 §5 — the review manifest is not canary state)."""
    mp = Path(manifest_path).resolve()
    wt = Path(operations_worktree).resolve()
    try:
        inside = mp.is_relative_to(wt)
    except AttributeError:  # py < 3.9
        inside = str(mp).startswith(str(wt) + os.sep)
    if inside and mp.exists():
        mp.unlink()


def _batch_delta_paths(repo: str, base: str, head: str) -> set[str]:
    """Mechanical canonical batch delta — added/modified paths in base..head.
    Deletions/renames FAIL CLOSED (R0.2 §12)."""
    out = ops_git.run_git(repo, "diff", "--name-status", f"{base}..{head}")
    paths: set[str] = set()
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status, path = parts[0][0], parts[-1]
        if status in {"D"}:
            raise ValueError(f"deletion in batch range not promotable: {path}")
        if status[0] == "R":
            raise ValueError(f"rename in batch range not promotable: {path}")
        if status in {"A", "M"}:
            paths.add(path)
    return paths


def _latest_source_in_range(repo: str, base: str, head: str, path: str) -> str:
    """Mechanical: the LATEST commit in base..head that touched path (R0.2 §11E)."""
    out = ops_git.run_git(repo, "log", "-1", "--format=%H", f"{base}..{head}", "--", path)
    sha = out.strip()
    if not sha:
        raise ValueError(f"no commit in {base[:12]}..{head[:12]} touches {path}")
    return sha


def promote_batch(manifest_path: str | Path, target_branch: str, repo: str | Path,
                  operations_worktree: str | Path, do_push: bool = False,
                  into_primary: bool = False, verify_only: bool = False) -> dict:
    repo = str(repo)
    manifest = load_manifest(manifest_path)
    res: dict = {"ok": False, "stage": "", "reason": "", "commit": "", "promoted": []}

    if os.environ.get("OPS_MAINTENANCE_MODE") == "ON":
        res["stage"] = "maintenance"; res["reason"] = "GOVERNED_MAINTENANCE_MODE=ON — promotion refused"
        return res

    # 1. invocation contract (R0.2 §3/§5/§6) — BEFORE any fetch or file write
    if into_primary:
        if target_branch != "main":
            res["stage"] = "target"; res["reason"] = (
                "into_primary is reserved EXCLUSIVELY for target_branch == 'main' (R0.2 §5)"
            )
            return res
        if verify_only:
            res["stage"] = "contract"; res["reason"] = (
                "into_primary + verify_only is invalid — verify-only must NEVER dirty "
                "governed main; rehearse on a temporary worktree/branch derived from "
                "frozen canonical main (R0.2 §6)"
            )
            return res
        if not do_push:
            res["stage"] = "contract"; res["reason"] = (
                "into_primary MUST imply do_push=True — a real P1 is not complete "
                "merely because local main received a commit (R0.2 §3)"
            )
            return res

    # 2. fetch; 4. local == origin == manifest_main_sha for the primary
    ops_git.run_git(repo, "fetch", "origin")
    cur_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()
    if cur_main != manifest["manifest_main_sha"]:
        res["stage"] = "toctou"; res["reason"] = (
            f"HOLD — current origin/main {cur_main} != manifest_main_sha "
            f"{manifest['manifest_main_sha']}; revalidate/regenerate the manifest."
        )
        return res
    cur_ops = ops_git.run_git(repo, "rev-parse", "origin/ops/automation").strip()

    # 10. frozen ops snapshot must STILL be in canonical ops lineage (R0.2 §10)
    if not ops_git.is_ancestor(repo, manifest["manifest_ops_head_sha"], cur_ops):
        res["stage"] = "frozen_lineage"; res["reason"] = (
            f"HOLD — manifest ops head {manifest['manifest_ops_head_sha']} is no "
            f"longer in canonical origin/ops/automation lineage ({cur_ops}); do NOT "
            "promote from an arbitrary reachable commit (R0.2 §10)"
        )
        return res

    # 3/4. primary readiness (R0.2 §2 P1-1) — REAL P1 only
    if into_primary:
        cur = ops_git.run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
        if cur != target_branch:
            res["stage"] = "target"; res["reason"] = f"primary is on {cur}, not {target_branch}"
            return res
        dirty = ops_git.porcelain(repo)
        if dirty:
            res["stage"] = "dirty"; res["reason"] = (
                "primary main worktree is NOT clean — FAIL CLOSED (never reset/clean); "
                f"entries={dirty[:10]} (R0.2 §2C)"
            )
            return res
        local_head = ops_git.run_git(repo, "rev-parse", "HEAD").strip()
        if local_head != cur_main:  # cur_main == manifest_main_sha (toctou checked)
            res["stage"] = "baseline"; res["reason"] = (
                f"HOLD — local primary main {local_head} != origin/main {cur_main} "
                "(ahead/behind/diverged); a real P1 may begin ONLY from the exact "
                "reviewed canonical main SHA (R0.2 §2D)"
            )
            return res

    head = manifest["manifest_ops_head_sha"]
    try:
        ops_git.run_git(repo, "cat-file", "-e", f"{head}^{{commit}}")
    except ops_git.OpsGitError:
        res["stage"] = "frozen_missing"; res["reason"] = f"manifest ops head {head} no longer exists"
        return res

    # 12. canonical batch delta revalidation (R0.2 §12) — EXACT set equality
    try:
        delta_paths = _batch_delta_paths(repo, manifest["manifest_main_sha"], head)
    except ValueError as e:
        res["stage"] = "delta"; res["reason"] = f"canonical batch delta invalid: {e}"
        return res
    manifest_paths = {a["path"] for a in manifest["artifacts"]}
    if delta_paths != manifest_paths:
        omitted = sorted(manifest_paths - delta_paths)
        added = sorted(delta_paths - manifest_paths)
        res["stage"] = "delta"; res["reason"] = (
            "manifest artifact set != canonical batch delta "
            f"({manifest['manifest_main_sha'][:12]}..{head[:12]}) — "
            f"omitted={omitted} added={added}; Founder approval applies to the exact "
            "deterministic batch, not a mutable subset (R0.2 §12)"
        )
        return res

    # target location: REAL P1 -> primary worktree; canary -> temp worktree
    if into_primary:
        target_cwd = Path(repo)
        tmp_worktree = None
    else:
        try:
            ops_git.run_git(repo, "rev-parse", "--verify", f"refs/heads/{target_branch}")
        except ops_git.OpsGitError:
            ops_git.run_git(repo, "branch", target_branch, "origin/main")
        tmp_worktree = Path(tempfile.mkdtemp(prefix="ops-promote-"))
        ops_git.run_git(repo, "worktree", "add", str(tmp_worktree), target_branch)
        target_cwd = tmp_worktree

    try:
        # 11. per-artifact revalidation (R0.2 §11 A–G) — never trust manifest fields
        for art in manifest["artifacts"]:
            rel = ops_config.normalize_rel(art["path"])
            if ops_config.is_denied(rel):
                raise ValueError(f"denied path in manifest: {art['path']}")
            owner = art["job_id"]
            if not ops_config.job_exists(owner):
                res["stage"] = "owner"; res["reason"] = (
                    f"unknown owning job {owner!r} for {art['path']}"
                )
                return res
            # authority scoped to THAT artifact's owning job — never widened
            if not ops_config.allowed_for(owner, rel):
                res["stage"] = "owner"; res["reason"] = (
                    f"target path not allowed for owning job {owner}: {art['path']}"
                )
                return res
            src = art["source_commit"]
            # A: source_commit is a commit
            try:
                ver = ops_git.run_git(repo, "rev-parse", "--verify", f"{src}^{{commit}}").strip()
            except ops_git.OpsGitError:
                res["stage"] = "source"; res["reason"] = (
                    f"source_commit {src} is not a commit object (R0.2 §11A)"
                )
                return res
            if ver != src:
                res["stage"] = "source"; res["reason"] = (
                    f"source_commit {src} is not a commit object (R0.2 §11A)"
                )
                return res
            # E: source_commit is the LATEST path-touch within the frozen batch
            # (checked BEFORE blob existence — a commit outside the batch must HOLD
            # as out-of-range, not fall through to a missing-blob stage)
            latest = _latest_source_in_range(repo, manifest["manifest_main_sha"], head, art["path"])
            if latest != src:
                res["stage"] = "source"; res["reason"] = (
                    f"source_commit {src} is NOT the latest path-touch in the frozen "
                    f"batch (latest={latest}) — HOLD (R0.2 §11E)"
                )
                return res
            # D: the exact path exists at source_commit
            try:
                ops_git.run_git(repo, "cat-file", "-e", f"{src}:{art['path']}")
            except ops_git.OpsGitError:
                res["stage"] = "blob"; res["reason"] = (
                    f"frozen source blob missing: {art['path']} @ {src}"
                )
                return res
            # G: raw blob sha256 matches (binary git blob bytes, same definition)
            data = ops_git.run_git_bytes(repo, "show", f"{src}:{art['path']}")
            h = hashlib.sha256(data).hexdigest()
            if h != art["sha256"]:
                res["stage"] = "hash"; res["reason"] = (
                    f"altered artifact hash: {art['path']} manifest={art['sha256']} actual={h}"
                )
                return res
            dest = Path(target_cwd) / art["path"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            res["promoted"].append(art["path"])

        # 6. verify-only (canary rehearsal only — into_primary is prohibited above)
        if verify_only:
            ok = all(
                hashlib.sha256((Path(target_cwd) / art["path"]).read_bytes()).hexdigest() == art["sha256"]
                for art in manifest["artifacts"]
            )
            res["ok"] = ok; res["stage"] = "verify-only"
            return res

        # 7/8/9. explicit-path commit — never a merge of ops — then raw-blob verify
        ops_git.run_git(target_cwd, "add", "--", *[a["path"] for a in manifest["artifacts"]])
        staged = [s.strip() for s in ops_git.run_git(target_cwd, "diff", "--cached", "--name-only").splitlines() if s.strip()]
        if set(staged) != {a["path"] for a in manifest["artifacts"]}:
            raise ValueError(f"staged set mismatch: {staged}")
        jobs = ",".join(sorted({a["job_id"] for a in manifest["artifacts"]}))
        ops_git.run_git(
            target_cwd, "commit", "-m",
            f"ops(promotion): manifest {manifest['manifest_id']} — {len(manifest['artifacts'])} "
            f"artifacts, jobs [{jobs}] (P1 batch, FD #142)",
        )
        res["commit"] = ops_git.run_git(target_cwd, "rev-parse", "HEAD").strip()
        for art in manifest["artifacts"]:
            data = ops_git.run_git_bytes(target_cwd, "show", f"HEAD:{art['path']}")
            if hashlib.sha256(data).hexdigest() != art["sha256"]:
                raise ValueError(f"post-commit hash mismatch: {art['path']}")

        if into_primary:  # do_push guaranteed True by the contract
            # 10/11/12. push -> fetch -> verify origin/main == promotion commit
            try:
                ops_git.run_git(target_cwd, "push", "origin", target_branch)
            except ops_git.OpsGitError as e:
                res["stage"] = "push_recovery"
                res["pending_state"] = "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
                res["reason"] = (
                    f"push FAILED after local promotion commit {res['commit']} — commit "
                    "PRESERVED, origin/main unchanged, last_promoted NOT advanced, "
                    "manifest preserved; recover with --recover (verifies parent + hashes, "
                    f"retries the EXACT push) or Founder disposition. ({str(e)[:120]}) (R0.2 §13)"
                )
                return res
            ops_git.run_git(repo, "fetch", "origin")
            remote = ops_git.run_git(repo, "rev-parse", f"origin/{target_branch}").strip()
            if remote != res["commit"]:
                res["stage"] = "verify"
                res["pending_state"] = "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
                res["reason"] = (
                    f"remote {remote} != local {res['commit']} — "
                    "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY (R0.2 §13)"
                )
                return res
            res["remote_verified"] = True
            # 13/14/15. ONLY AFTER remote verification: advance + clear + remove residue
            state = ops_config.load_state()
            state["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]
            ops_config.save_state(state)
            ops_config.set_promotion_pending(None)
            res["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]
            _remove_worktree_manifest(manifest_path, operations_worktree)
        else:
            # canary — NEVER advances real promotion state, NEVER removes residue
            if do_push:
                ops_git.run_git(target_cwd, "push", "origin", target_branch)
                ops_git.run_git(repo, "fetch", "origin")
                remote = ops_git.run_git(repo, "rev-parse", f"origin/{target_branch}").strip()
                if remote != res["commit"]:
                    res["stage"] = "verify"; res["reason"] = f"remote {remote} != local {res['commit']}"
                    return res
                res["remote_verified"] = True

        res["ok"] = True; res["stage"] = "promoted"
        return res
    finally:
        if tmp_worktree is not None:
            ops_git.run_git(repo, "worktree", "remove", "--force", str(tmp_worktree))


def recover_local_promotion(manifest_path: str | Path, repo: str | Path,
                            operations_worktree: str | Path,
                            target_branch: str = "main") -> dict:
    """Deterministic P1-13 recovery (R0.2 §13): verify the PRESERVED local
    promotion commit — parent == manifest_main_sha and artifact raw-blob hashes ==
    manifest — then retry the EXACT push. No reset, no history rewrite. Only for
    into_primary / governed main."""
    repo = str(repo)
    manifest = load_manifest(manifest_path)
    res: dict = {"ok": False, "stage": "", "reason": "", "commit": ""}
    if target_branch != "main":
        res["stage"] = "target"; res["reason"] = "recovery is reserved for governed main"
        return res
    cur = ops_git.run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if cur != target_branch:
        res["stage"] = "target"; res["reason"] = f"primary is on {cur}, not {target_branch}"
        return res
    head = ops_git.run_git(repo, "rev-parse", "HEAD").strip()
    try:
        parent = ops_git.run_git(repo, "rev-parse", "HEAD^").strip()
    except ops_git.OpsGitError:
        res["stage"] = "parent"; res["reason"] = "no parent — HEAD is not a promotion commit"
        return res
    if parent != manifest["manifest_main_sha"]:
        res["stage"] = "parent"; res["reason"] = (
            f"preserved commit parent {parent} != manifest_main_sha "
            f"{manifest['manifest_main_sha']} — exact push NOT safe; Founder disposition (R0.2 §13)"
        )
        return res
    for art in manifest["artifacts"]:
        try:
            data = ops_git.run_git_bytes(repo, "show", f"HEAD:{art['path']}")
        except ops_git.OpsGitError:
            res["stage"] = "hash"; res["reason"] = f"artifact missing at HEAD: {art['path']}"
            return res
        if hashlib.sha256(data).hexdigest() != art["sha256"]:
            res["stage"] = "hash"; res["reason"] = f"artifact hash mismatch at HEAD: {art['path']}"
            return res
    ops_git.run_git(repo, "fetch", "origin")
    origin_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()
    if origin_main != manifest["manifest_main_sha"]:
        res["stage"] = "main_moved"; res["reason"] = (
            "origin/main advanced past the reviewed base — exact push no longer safe; "
            "Founder disposition required (R0.2 §13)"
        )
        return res
    try:
        ops_git.run_git(repo, "push", "origin", target_branch)
    except ops_git.OpsGitError as e:
        res["stage"] = "push"; res["reason"] = f"exact push retry failed: {str(e)[:120]}"
        res["pending_state"] = "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
        return res
    ops_git.run_git(repo, "fetch", "origin")
    remote = ops_git.run_git(repo, "rev-parse", f"origin/{target_branch}").strip()
    if remote != head:
        res["stage"] = "verify"; res["reason"] = f"remote {remote} != local {head}"
        res["pending_state"] = "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
        return res
    state = ops_config.load_state()
    state["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]
    ops_config.save_state(state)
    ops_config.set_promotion_pending(None)
    _remove_worktree_manifest(manifest_path, operations_worktree)
    res.update({"ok": True, "stage": "recovered", "commit": head,
                "remote_verified": True, "last_promoted_ops_sha": manifest["manifest_ops_head_sha"]})
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ deterministic multi-job P1 batch promotion / recovery")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--target-branch", default="main")
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--into-primary", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--recover", action="store_true",
                    help="P1-13 deterministic recovery: verify the preserved local "
                         "promotion commit (parent == manifest_main_sha, artifact "
                         "hashes == manifest) then retry the EXACT push")
    args = ap.parse_args()

    if args.recover:
        res = recover_local_promotion(args.manifest, args.repo, args.worktree, args.target_branch)
    else:
        res = promote_batch(args.manifest, args.target_branch, args.repo, args.worktree,
                            do_push=args.push, into_primary=args.into_primary,
                            verify_only=args.verify_only)
    print(json.dumps(res, indent=2, sort_keys=True))
    if res.get("stage") in {"toctou", "push_recovery", "verify"}:
        return 2
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-24 14:00 UTC+7 (R0.2 P1 hardening: contract, exact order, revalidation, recovery, lock)
