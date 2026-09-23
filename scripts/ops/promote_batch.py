"""Deterministic P1 promotion helper (FD #142 §10, §11, §12).

Exact file-content transfer from the FROZEN ops snapshot onto a target branch —
never a branch merge, never a broad cherry-pick, never an implicitly-newer
artifact. TOCTOU: current main MUST equal manifest_main_sha, else HOLD.

R0 canary: --target-branch <temp> promotes against a temporary branch, NOT governed
main. Real P1: --target-branch main --into-primary used only after Founder approval
of the manifest batch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import ops_config
import ops_git


def _git_bytes(repo: str, *args: str) -> bytes:
    res = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, check=True,
        text=False, encoding=None,
    )
    return res.stdout


def load_manifest(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for req in ("manifest_id", "manifest_main_sha", "manifest_ops_head_sha", "artifacts"):
        if req not in data:
            raise ValueError(f"manifest missing required field {req!r}")
    if not isinstance(data["artifacts"], list) or not data["artifacts"]:
        raise ValueError("manifest has no artifacts")
    return data


def promote_batch(manifest_path: str | Path, target_branch: str, repo: str | Path,
                  operations_worktree: str | Path, do_push: bool = False,
                  into_primary: bool = False, verify_only: bool = False) -> dict:
    repo = str(repo)
    manifest = load_manifest(manifest_path)
    res: dict = {"ok": False, "stage": "", "reason": "", "commit": "", "promoted": []}

    if os.environ.get("OPS_MAINTENANCE_MODE") == "ON":
        res["stage"] = "maintenance"; res["reason"] = "GOVERNED_MAINTENANCE_MODE=ON — promotion refused"
        return res

    ops_git.run_git(repo, "fetch", "origin")
    cur_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()
    if cur_main != manifest["manifest_main_sha"]:
        res["stage"] = "toctou"; res["reason"] = (
            f"HOLD — current origin/main {cur_main} != manifest_main_sha "
            f"{manifest['manifest_main_sha']}; revalidate/regenerate the manifest."
        )
        return res

    head = manifest["manifest_ops_head_sha"]
    try:
        ops_git.run_git(repo, "cat-file", "-e", f"{head}^{{commit}}")
    except ops_git.OpsGitError:
        res["stage"] = "frozen_missing"; res["reason"] = f"manifest ops head {head} no longer exists"
        return res

    # target location
    if into_primary:
        target_cwd = Path(repo)
        cur = ops_git.run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
        if cur != target_branch:
            res["stage"] = "target"; res["reason"] = f"primary is on {cur}, not {target_branch}"
            return res
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
        # exact content transfer
        for art in manifest["artifacts"]:
            rel = ops_config.normalize_rel(art["path"])
            if ops_config.is_denied(rel):
                raise ValueError(f"denied path in manifest: {art['path']}")
            try:
                data = ops_git.run_git(repo, "show", f"{head}:{art['path']}").encode("utf-8")
            except ops_git.OpsGitError:
                res["stage"] = "blob"; res["reason"] = f"frozen blob missing: {art['path']}"; return res
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

        if verify_only:
            ok = all(
                hashlib.sha256((Path(target_cwd) / art["path"]).read_bytes()).hexdigest() == art["sha256"]
                for art in manifest["artifacts"]
            )
            res["ok"] = ok; res["stage"] = "verify-only"
            return res

        # explicit-path commit; never a merge of ops
        ops_git.run_git(target_cwd, "add", "--", *[a["path"] for a in manifest["artifacts"]])
        staged = [s.strip() for s in ops_git.run_git(target_cwd, "diff", "--cached", "--name-only").splitlines() if s.strip()]
        if set(staged) != {a["path"] for a in manifest["artifacts"]}:
            raise ValueError(f"staged set mismatch: {staged}")
        ops_git.run_git(
            target_cwd, "commit", "-m",
            f"ops(promotion): manifest {manifest['manifest_id']} — {len(manifest['artifacts'])} artifacts (P1 batch, FD #142)",
        )
        res["commit"] = ops_git.run_git(target_cwd, "rev-parse", "HEAD").strip()
        # verify committed bytes hashes
        for art in manifest["artifacts"]:
            data = ops_git.run_git(target_cwd, "show", f"HEAD:{art['path']}").encode("utf-8")
            if hashlib.sha256(data).hexdigest() != art["sha256"]:
                raise ValueError(f"post-commit hash mismatch: {art['path']}")

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


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ deterministic P1 batch promotion")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--target-branch", required=True)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--into-primary", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()

    res = promote_batch(args.manifest, args.target_branch, args.repo, args.worktree,
                        do_push=args.push, into_primary=args.into_primary,
                        verify_only=args.verify_only)
    print(json.dumps(res, indent=2, sort_keys=True))
    if res.get("stage") == "toctou":
        return 2
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7