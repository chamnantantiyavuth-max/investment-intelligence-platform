"""Deterministic multi-job P1 promotion helper (FD #142 §10, §11, §12; R0.1-B).

Exact file-content transfer from the FROZEN ops snapshot onto a target branch —
never a branch merge, never a broad cherry-pick, never an implicitly-newer
artifact. TOCTOU: current main MUST equal manifest_main_sha, else HOLD.

Consumes the REVISED multi-job manifest without assuming one job (R0.1 §12):
for EVERY artifact independently —
  * the artifact's OWNING job (manifest `job_id`, derived mechanically at
    generation) re-validates that the target path is still on its anchored
    allowlist; never widened because the batch contains multiple jobs
  * the frozen source blob is verified to exist at `source_commit` (the REAL
    commit within the batch range that last touched that path)
  * the raw blob SHA-256 is recomputed and compared to the manifest hash
  * exact content is transferred and post-commit hashes re-verified

last_promoted_ops_sha (R0.1 §13): advances ONLY after a Founder-approved REAL P1
promotion (--into-primary) completes successfully — NEVER on canary, manifest
generation, or cron artifact commits.

Manifest residue (R0.1 §14): on successful promotion the manifest file is
removed from the automation working tree (ops/manifests/ is gitignored; G0 must
return clean before cron resumes; ops/manifests/** is NOT a cron allowlist).

R0 canary: --target-branch <temp> promotes against a temporary branch, NOT governed
main. Real P1: --target-branch main --into-primary used only after Founder approval
of the manifest batch.
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
    for req in ("manifest_id", "manifest_main_sha", "manifest_ops_head_sha", "artifacts"):
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
    """R0.1 §14: after successful promotion, drop the interactive manifest residue
    from the automation worktree so G0 returns clean (it is gitignored + reproducible)."""
    mp = Path(manifest_path).resolve()
    wt = Path(operations_worktree).resolve()
    try:
        inside = mp.is_relative_to(wt)
    except AttributeError:  # py < 3.9
        inside = str(mp).startswith(str(wt) + os.sep)
    if inside and mp.exists():
        mp.unlink()


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
        # exact content transfer, per-artifact independent authority
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
            try:
                ops_git.run_git(repo, "cat-file", "-e", f"{src}:{art['path']}")
            except ops_git.OpsGitError:
                res["stage"] = "blob"; res["reason"] = (
                    f"frozen source blob missing: {art['path']} @ {src}"
                )
                return res
            # raw git blob bytes — binary mode, same definition as the generator
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
        jobs = ",".join(sorted({a["job_id"] for a in manifest["artifacts"]}))
        ops_git.run_git(
            target_cwd, "commit", "-m",
            f"ops(promotion): manifest {manifest['manifest_id']} — {len(manifest['artifacts'])} "
            f"artifacts, jobs [{jobs}] (P1 batch, FD #142)",
        )
        res["commit"] = ops_git.run_git(target_cwd, "rev-parse", "HEAD").strip()
        # verify committed bytes hashes (binary, raw blob definition)
        for art in manifest["artifacts"]:
            data = ops_git.run_git_bytes(target_cwd, "show", f"HEAD:{art['path']}")
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

        # R0.1 §13: last_promoted_ops_sha advances ONLY on a REAL Founder-approved
        # P1 promotion into governed main (into_primary) — never canary.
        if into_primary:
            state = ops_config.load_state()
            state["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]
            ops_config.save_state(state)
            res["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]

        res["ok"] = True; res["stage"] = "promoted"
        # R0.1 §14: remove interactive manifest residue from the automation worktree
        _remove_worktree_manifest(manifest_path, operations_worktree)
        return res
    finally:
        if tmp_worktree is not None:
            ops_git.run_git(repo, "worktree", "remove", "--force", str(tmp_worktree))


def main() -> int:
    ap = argparse.ArgumentParser(description="C+ deterministic multi-job P1 batch promotion")
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

# footer: 2026-09-24 12:30 UTC+7 (R0.1-B multi-job consumption + last-promoted semantics)
