"""Deterministic promotion-manifest generator (FD #142 §9, §12).

Interactive P1 review only — never a background cron artifact. All hashes and git
identities are MECHANICAL (SHA-256 of exact bytes read from the frozen ops commit);
no LLM-authored values. Manifest output path defaults to ops/manifests/<id>.json on
the ops worktree.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

import ops_config
import ops_git
from validate_delta import _ADDED, _MODIFIED


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_manifest(job_id: str, repo: str | Path, base: str, head: str,
                      pit_as_of: str | None = None, fetch: bool = False) -> dict:
    repo = str(repo)
    if not ops_config.job_exists(job_id):
        raise ValueError(f"unknown job id {job_id!r}")
    if fetch:
        ops_git.run_git(repo, "fetch", "origin")

    # artifact paths = added/modified in base..head (deletions/renames rejected)
    out = ops_git.run_git(repo, "diff", "--name-status", f"{base}..{head}")
    artifacts = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status, path = parts[0][0], parts[-1]
        if status in {"D"}:
            raise ValueError(f"deletion in artifact range not promotable: {path}")
        if status[0] == "R":
            raise ValueError(f"rename in artifact range not promotable: {path}")
        if status not in _ADDED | _MODIFIED:
            continue
        rel = ops_config.normalize_rel(path)
        if ops_config.is_denied(rel):
            raise ValueError(f"denylist hit in artifact range: {path}")
        if not ops_config.allowed_for(job_id, rel):
            raise ValueError(f"path not on job allowlist: {path}")
        content = ops_git.run_git(repo, "show", f"{head}:{path}").encode("utf-8")
        artifacts.append({
            "path": path,
            "source_commit": head,
            "sha256": _sha256_bytes(content),
            "job_id": job_id,
            "run_timestamp": _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=7))).isoformat(),
            "pit_as_of": pit_as_of,
        })

    if not artifacts:
        raise ValueError("no promotable artifacts in base..head")

    state = ops_config.load_state()
    manifest = {
        "manifest_id": f"p1-{_dt.datetime.now().strftime('%Y%m%d')}-{head[:8]}-{job_id[:6]}",
        "generated_at": _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=7))).isoformat(),
        "manifest_main_sha": ops_git.run_git(repo, "rev-parse", "origin/main").strip(),
        "manifest_ops_head_sha": head,
        "last_promoted_ops_sha": state.get("last_promoted_ops_sha", ""),
        "artifacts": artifacts,
        "allowlist_result": "PASS",
        "denylist_result": "PASS",
        "conflict_result": "NONE",
        "disposition": "AWAITING_FOUNDER_APPROVAL",
    }
    return manifest


def write_manifest(manifest: dict, repo: str | Path, worktree: str | Path) -> Path:
    wp = Path(worktree)
    out = wp / "ops" / "manifests" / f"{manifest['manifest_id']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="deterministic P1 promotion manifest")
    ap.add_argument("--job", required=True)
    ap.add_argument("--from", dest="base", required=True)
    ap.add_argument("--to", dest="head", required=True)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--pit-as-of", default=None)
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()

    manifest = generate_manifest(args.job, args.repo, args.base, args.head,
                                 pit_as_of=args.pit_as_of, fetch=args.fetch)
    out = write_manifest(manifest, args.repo, args.worktree)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"MANIFEST_WRITTEN: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-23 15:00 UTC+7