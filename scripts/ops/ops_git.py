"""Minimal git subprocess wrapper for C+ ops tooling. Fail-closed: any non-zero exit
raises OpsGitError with stderr; callers never guess.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


class OpsGitError(RuntimeError):
    pass


def run_git(cwd: str | Path, *args: str, check: bool = True, env_extra: dict | None = None) -> str:
    env = None
    if env_extra:
        import os
        env = dict(os.environ)
        env.update(env_extra)
    res = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    if check and res.returncode != 0:
        raise OpsGitError(f"git {' '.join(args)} failed ({res.returncode}): {res.stderr.strip()}")
    return res.stdout


def is_ancestor(cwd: str | Path, ancestor: str, descendant: str) -> bool:
    try:
        run_git(cwd, "merge-base", "--is-ancestor", ancestor, descendant)
        return True
    except OpsGitError:
        return False


def heads(cwd: str | Path) -> dict[str, str]:
    """local HEAD, origin/main HEAD, origin/ops/automation HEAD (from local refs)."""
    out: dict[str, str] = {}
    for name, ref in (
        ("local_head", "HEAD"),
        ("origin_main", "refs/remotes/origin/main"),
        ("origin_ops", "refs/remotes/origin/ops/automation"),
    ):
        try:
            out[name] = run_git(cwd, "rev-parse", "--verify", ref).strip()
        except OpsGitError:
            out[name] = ""
    return out


def porcelain(cwd: str | Path) -> list[str]:
    out = run_git(cwd, "status", "--porcelain")
    return [ln for ln in out.splitlines() if ln.strip()]


def current_branch(cwd: str | Path) -> str:
    return run_git(cwd, "rev-parse", "--abbrev-ref", "HEAD").strip()


# footer: 2026-09-23 15:00 UTC+7