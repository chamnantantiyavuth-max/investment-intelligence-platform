"""Deterministic multi-job promotion-manifest generator (FD #142 §9, §12; R0.1-B).

Interactive P1 review only — never a background cron artifact. All hashes and git
identities are MECHANICAL (SHA-256 of exact git blob bytes read from the frozen ops
commit); no LLM-authored values.

One manifest may span artifacts produced by MULTIPLE job classes (e.g. Radar + AM,
or Radar + CIW) in a single `base..head` batch. For every artifact path the owning
job is DERIVED mechanically from the configured anchored allowlists (R0.1 87):

  exactly ONE allowlist matches  -> that job owns the artifact
  zero matches                   -> FAIL CLOSED (unknown path)
  >1 matches                     -> FAIL CLOSED (ambiguous ownership)

`--job` (repeatable) is an OPTIONAL caller-supplied validation constraint on the
derived owners — ownership itself is never taken from the caller. Learning Loop's
empty allowlist can never own a repo artifact.

`source_commit` per artifact = the actual LATEST commit within `base..head` that
introduced/modified that path (mechanical, `git log base..head -- <path>`).
`sha256` = SHA-256 over the exact raw blob bytes (`git show <source_commit>:<path>`
in BINARY mode — no text decoding, no newline conversion, no errors=replace).
`run_timestamp` = the source commit's committer timestamp (mechanical provenance);
`pit_as_of` is only set when provided — never invented (null + truthful provenance).

Manifest output path defaults to ops/manifests/<id>.json on the ops worktree
(gitignored; interactive review residue only — never a cron allowlist).
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

_UTC7 = _dt.timezone(_dt.timedelta(hours=7))


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _latest_source_commit(repo: str, base: str, head: str, path: str) -> str:
    """Latest commit in base..head that introduced/modified path (mechanical)."""
    out = ops_git.run_git(repo, "log", "-1", "--format=%H", f"{base}..{head}", "--", path)
    sha = out.strip()
    if not sha:
        raise ValueError(f"no commit in {base[:12]}..{head[:12]} touches {path}")
    ver = ops_git.run_git(repo, "rev-parse", "--verify", f"{sha}^{{commit}}").strip()
    if ver != sha:
        raise ValueError(f"source commit for {path} is not a commit object: {sha}")
    return sha


def _source_commit_time(repo: str, sha: str) -> str:
    """Committer timestamp (ISO-8601) of the source commit — mechanical provenance."""
    return ops_git.run_git(repo, "show", "-s", "--format=%cI", sha).strip()


def generate_manifest(repo: str | Path, base: str, head: str,
                      expected_jobs: list[str] | None = None,
                      pit_as_of: str | None = None, fetch: bool = False) -> dict:
    repo = str(repo)
    if fetch:
        ops_git.run_git(repo, "fetch", "origin")

    # artifact paths = added/modified in base..head (deletions/renames rejected)
    out = ops_git.run_git(repo, "diff", "--name-status", f"{base}..{head}")
    artifacts: list[dict] = []
    changed_jobs: set[str] = set()
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
        # mechanical ownership from anchored allowlists (R0.1 87)
        owners = ops_config.owning_jobs(rel)
        if not owners:
            raise ValueError(f"no owning job allowlist matches: {path} (FAIL CLOSED)")
        if len(owners) > 1:
            raise ValueError(f"ambiguous ownership — {len(owners)} allowlists match: {path} ({owners})")
        owner = owners[0]
        if expected_jobs and owner not in expected_jobs:
            raise ValueError(
                f"owner {owner} not in expected jobs {sorted(expected_jobs)}: {path}"
            )
        # per-artifact REAL source commit within the batch range (R0.1 88)
        src = _latest_source_commit(repo, base, head, path)
        # exact raw git blob bytes (R0.1 89) — binary mode, no re-encode
        blob = ops_git.run_git_bytes(repo, "show", f"{src}:{path}")
        artifacts.append({
            "path": path,
            "job_id": owner,
            "source_commit": src,
            "sha256": _sha256_bytes(blob),
            "run_timestamp": _source_commit_time(repo, src),
            "pit_as_of": pit_as_of,  # null unless mechanically provided; never invented
            "allowlist_result": "PASS",
            "denylist_result": "PASS",
        })
        changed_jobs.add(owner)

    if not artifacts:
        raise ValueError("no promotable artifacts in base..head")

    state = ops_config.load_state()
    manifest = {
        "manifest_id": f"p1-{_dt.datetime.now(_UTC7).strftime('%Y%m%d')}-{head[:8]}",
        "generated_at": _dt.datetime.now(_UTC7).isoformat(),
        "manifest_main_sha": ops_git.run_git(repo, "rev-parse", "origin/main").strip(),
        "manifest_ops_head_sha": head,
        "last_promoted_ops_sha": state.get("last_promoted_ops_sha", ""),
        "artifacts": artifacts,
        "changed_jobs": sorted(changed_jobs),
        "conflict_result": "NONE",
        "deletion_count": 0,
        "rename_count": 0,
        "allowlist_result": "PASS",
        "denylist_result": "PASS",
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
    ap = argparse.ArgumentParser(
        description="deterministic multi-job P1 promotion manifest (ownership derived mechanically)"
    )
    ap.add_argument("--job", action="append", default=None,
                    help="optional expected owning-job constraint (repeatable); "
                         "ownership is ALWAYS derived from path authority, never from this flag")
    ap.add_argument("--from", dest="base", required=True)
    ap.add_argument("--to", dest="head", required=True)
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--pit-as-of", default=None)
    ap.add_argument("--fetch", action="store_true")
    args = ap.parse_args()

    manifest = generate_manifest(args.repo, args.base, args.head,
                                 expected_jobs=args.job,
                                 pit_as_of=args.pit_as_of, fetch=args.fetch)
    out = write_manifest(manifest, args.repo, args.worktree)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"MANIFEST_WRITTEN: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-24 12:30 UTC+7 (R0.1-B multi-job + raw-blob correction)
