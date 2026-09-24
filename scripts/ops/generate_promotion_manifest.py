"""Deterministic multi-job promotion-manifest generator (FD #142 §9, §12; R0.1-B; R0.2).

Interactive P1 review only — never a background cron artifact. All hashes and git
identities are MECHANICAL (SHA-256 of exact git blob bytes read from the frozen ops
commit); no LLM-authored values.

CANONICAL AUTHORITY MODEL (R0.2 §7/§8/§9): the batch range is derived MECHANICALLY
from the fetched origin refs — MANIFEST_MAIN_SHA = origin/main and
MANIFEST_OPS_HEAD_SHA = origin/ops/automation. Under C+, main = canonical
governed/promoted state and ops = canonical main + unpromoted automation artifacts,
so `main..ops` is the authoritative pending-promotion delta. Caller-supplied refs
are accepted ONLY as an explicit test/debug surface and MUST equal the mechanical
refs — production P1 never trusts arbitrary SHAs.

HOLD unless origin/main is an ancestor of (or equal to) origin/ops/automation: an
unsynchronized/diverged snapshot is not promotable — run the normal main->ops sync
first. last_promoted_ops_sha is retained purely as provenance/prior-promotion
checkpoint; at generation it must resolve to a commit that is an ancestor of (or
equal to) the current manifest ops head, else HOLD — it never overrides the
canonical current-main -> current-ops delta.

One manifest may span artifacts produced by MULTIPLE job classes (e.g. Radar + AM,
or Radar + CIW). For every artifact path the owning job is DERIVED mechanically from
the configured anchored allowlists: exactly ONE allowlist matches -> that job owns
the artifact; zero -> FAIL CLOSED; >1 -> FAIL CLOSED (ambiguous). `--job`
(repeatable) is an OPTIONAL caller-supplied validation constraint on the derived
owners — ownership itself is never taken from the caller. Learning Loop's empty
allowlist can never own a repo artifact.

`source_commit` per artifact = the actual LATEST commit within main..ops that
introduced/modified that path (mechanical, `git log main..ops -- <path>`). `sha256`
= SHA-256 over the exact raw blob bytes (`git show <source_commit>:<path>` in
BINARY mode). `run_timestamp` = source commit committer timestamp (mechanical
provenance); `pit_as_of` is only set when provided — never invented.

Writing a manifest sets the external promotion-pending lock (R0.2 §14): while a
Founder-review manifest exists, artifact-cron preflight / G0 FAILS CLOSED until a
verified REAL P1 clears it or the manifest is explicitly cancelled.
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


# Founder-approval dispositions (R0.3 §2). Promotion accepts ONLY APPROVED;
# any other value (AWAITING_FOUNDER_APPROVAL / REJECTED / CANCELLED / missing /
# malformed / unknown) refuses with stage 'approval'.
DISPOSITIONS = ("AWAITING_FOUNDER_APPROVAL", "APPROVED", "REJECTED", "CANCELLED")


def manifest_immutable_digest(m: dict) -> str:
    """R0.3 §3: SHA-256 over a deterministic canonical serialization of the
    IMMUTABLE promotion payload — manifest_id, batch range, exact ordered
    artifact entries (path/job_id/source_commit/sha256) and changed_jobs.

    Mutable review metadata (disposition=APPROVED, generated_at, review notes,
    last_promoted_ops_sha…) are EXCLUDED so an untouched batch has ONE stable
    digest and a re-stamped disposition cannot change what was approved.

    Approval binds to this digest (ops-state approved_manifest_sha256); a real
    P1 recomputes it and FAILS CLOSED on any mismatch.
    """
    payload = {
        "manifest_id": m["manifest_id"],
        "batch_base_sha": m["batch_base_sha"],
        "manifest_main_sha": m["manifest_main_sha"],
        "manifest_ops_head_sha": m["manifest_ops_head_sha"],
        "artifacts": [{"path": a["path"], "job_id": a["job_id"],
                       "source_commit": a["source_commit"], "sha256": a["sha256"]}
                      for a in m["artifacts"]],
        "changed_jobs": m["changed_jobs"],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


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


def _parse_diff_status(status: str) -> str:
    return status[0]


def generate_manifest(repo: str | Path,
                      manifest_main_sha: str | None = None,
                      manifest_ops_head_sha: str | None = None,
                      expected_jobs: list[str] | None = None,
                      pit_as_of: str | None = None, fetch: bool = True) -> dict:
    """Deterministic multi-job promotion manifest over the CANONICAL C+ snapshot.

    Batch range is MECHANICAL: MANIFEST_MAIN_SHA = origin/main and
    MANIFEST_OPS_HEAD_SHA = origin/ops/automation after fetch (R0.2 §7/§8).
    Caller-supplied refs are accepted ONLY as a test/debug surface and MUST equal
    the mechanically derived refs. HOLD unless main is an ancestor of (or equal
    to) ops — run the normal main->ops sync first.
    """
    repo = str(repo)
    if fetch:
        ops_git.run_git(repo, "fetch", "origin")

    mech_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()
    mech_ops = ops_git.run_git(repo, "rev-parse", "origin/ops/automation").strip()
    if manifest_main_sha is not None and manifest_main_sha != mech_main:
        raise ValueError(
            f"caller manifest_main_sha != mechanically derived origin/main "
            f"({mech_main}) — production P1 uses the canonical refs only (R0.2 §8)"
        )
    if manifest_ops_head_sha is not None and manifest_ops_head_sha != mech_ops:
        raise ValueError(
            f"caller manifest_ops_head_sha != mechanically derived "
            f"origin/ops/automation ({mech_ops}) — production P1 uses the "
            "canonical refs only (R0.2 §8)"
        )
    main_sha, ops_sha = mech_main, mech_ops

    # R0.2 §7: an unsynchronized/diverged snapshot is not promotable
    if not ops_git.is_ancestor(repo, main_sha, ops_sha):
        raise ValueError(
            "HOLD — origin/main is NOT an ancestor of origin/ops/automation "
            "(unsynchronized/diverged snapshot); run the normal main->ops sync "
            "before generating a promotion manifest (R0.2 §7)"
        )

    # R0.2 §9: last_promoted_ops_sha is provenance only — must resolve and be in
    # the current ops lineage, but never overrides the canonical delta.
    # R0.3 §6: corrupt existing ops-state must HOLD generation (NEVER treated as {}).
    try:
        state = ops_config.load_state()
    except ops_config.StateError as e:
        raise ValueError(f"HOLD — cannot generate: ops-state is corrupt: {e}")
    lp = state.get("last_promoted_ops_sha", "")
    if lp:
        try:
            ver = ops_git.run_git(repo, "rev-parse", "--verify", f"{lp}^{{commit}}").strip()
        except ops_git.OpsGitError:
            raise ValueError(f"last_promoted_ops_sha {lp} does not resolve to a commit (HOLD, R0.2 §9)")
        if ver != lp:
            raise ValueError(f"last_promoted_ops_sha {lp} is not a commit object (HOLD, R0.2 §9)")
        if not ops_git.is_ancestor(repo, lp, ops_sha):
            raise ValueError(
                f"last_promoted_ops_sha {lp} is outside the current ops lineage — "
                "HOLD (R0.2 §9)"
            )

    # canonical batch delta = main..ops (deletions/renames rejected)
    out = ops_git.run_git(repo, "diff", "--name-status", f"{main_sha}..{ops_sha}")
    artifacts: list[dict] = []
    changed_jobs: set[str] = set()
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status, path = _parse_diff_status(parts[0]), parts[-1]
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
        # per-artifact REAL source commit within the canonical batch (R0.1 88)
        src = _latest_source_commit(repo, main_sha, ops_sha, path)
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
        raise ValueError("no promotable artifacts in main..ops")

    manifest = {
        "manifest_id": f"p1-{_dt.datetime.now(_UTC7).strftime('%Y%m%d')}-{ops_sha[:8]}",
        "generated_at": _dt.datetime.now(_UTC7).isoformat(),
        "batch_base_sha": main_sha,          # R0.2 §8: canonical current-main
        "manifest_main_sha": main_sha,       # == origin/main at generation (R0.2 §7)
        "manifest_ops_head_sha": ops_sha,    # == origin/ops/automation at generation (R0.2 §10)
        "last_promoted_ops_sha": lp,         # provenance checkpoint only (R0.2 §9)
        "artifacts": artifacts,
        "changed_jobs": sorted(changed_jobs),
        "conflict_result": "NONE",
        "deletion_count": 0,
        "rename_count": 0,
        "allowlist_result": "PASS",
        "denylist_result": "PASS",
        "disposition": "AWAITING_FOUNDER_APPROVAL",
        # R0.3 §3: digest over the immutable payload — the Founder approval
        # receipt binds to this exact value; a different/edited batch requires
        # NEW approval. Never include the mutable approval field itself.
        "immutable_digest": manifest_immutable_digest({
            "manifest_id": f"p1-{_dt.datetime.now(_UTC7).strftime('%Y%m%d')}-{ops_sha[:8]}",
            "batch_base_sha": main_sha,
            "manifest_main_sha": main_sha,
            "manifest_ops_head_sha": ops_sha,
            "artifacts": [
                {k: a[k] for k in ("path", "job_id", "source_commit", "sha256")}
                for a in artifacts
            ],
            "changed_jobs": sorted(changed_jobs),
        }),
    }
    return manifest


def write_manifest(manifest: dict, repo: str | Path, worktree: str | Path) -> Path:
    wp = Path(worktree)
    out = wp / "ops" / "manifests" / f"{manifest['manifest_id']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    # R0.2 §14: a Founder-review manifest exists — artifact-cron preflight / G0
    # FAILS CLOSED until a verified REAL P1 clears it or explicit cancellation
    ops_config.set_promotion_pending(manifest["manifest_id"])
    return out


_MANIFEST_REQUIRED = ("manifest_id", "batch_base_sha", "manifest_main_sha",
                      "manifest_ops_head_sha", "artifacts", "changed_jobs")


def _load_manifest_file(path: str | Path):
    """Load + minimum-shape-validate a manifest FILE (approve/cancel path; no
    import cycle with promote_batch)."""
    try:
        m = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError(f"cannot read manifest {path}: {e}")
    if not isinstance(m, dict):
        raise ValueError(f"manifest {path} is not a JSON object")
    for key in _MANIFEST_REQUIRED:
        if key not in m:
            raise ValueError(f"manifest {path} missing required key {key!r}")
    return m


# footer: 2026-09-24 15:30 UTC+7 (R0.3 immutable-digest + approval/cancel CLI + corrupt-state HOLD)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="deterministic multi-job P1 promotion manifest (ownership derived "
                    "mechanically; batch range = origin/main -> origin/ops/automation)"
    )
    ap.add_argument("--job", action="append", default=None,
                    help="optional expected owning-job constraint (repeatable); "
                         "ownership is ALWAYS derived from path authority, never from this flag")
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--pit-as-of", default=None)
    ap.add_argument("--approve", action="store_true",
                    help="Founder approval (R0.3 §3): loads the manifest at --manifest, "
                         "requires disposition == APPROVED, binds the immutable payload "
                         "digest into ops-state (approved_manifest_id + "
                         "approved_manifest_sha256). Approval applies to ONE exact batch.")
    ap.add_argument("--cancel", action="store_true",
                    help="explicit cancellation/disposition (R0.3 §13): clears the "
                         "pending lock + approval receipt ONLY for the exact manifest id "
                         "and digest at --manifest; other manifests' locks are untouched.")
    ap.add_argument("--manifest", default=None,
                    help="manifest file to approve or cancel")
    ap.add_argument("--no-fetch", action="store_true",
                    help="test/debug only: read origin refs without fetching "
                         "(production generation ALWAYS fetches per R0.2 §7)")
    args = ap.parse_args()

    if args.approve or args.cancel:
        if not args.manifest:
            print("error: --approve/--cancel requires --manifest <path>", file=sys.stderr)
            return 1
        m = _load_manifest_file(args.manifest)
        digest = manifest_immutable_digest(m)
        try:
            pending = ops_config.promotion_pending()
        except ops_config.StateError as e:
            print(f"error: ops-state corrupt — HOLD: {e}", file=sys.stderr)
            return 1
        if pending != m["manifest_id"]:
            print(f"error: pending manifest {pending!r} != supplied {m['manifest_id']!r} "
                  f"— cancellation/approval must name the EXACT pending manifest (R0.3 §13)",
                  file=sys.stderr)
            return 1
        if args.approve:
            if m.get("disposition") != "APPROVED":
                print(f"error: disposition is {m.get('disposition')!r}, not APPROVED — "
                      "the Founder-approved manifest must carry disposition=APPROVED "
                      "before the receipt is bound (R0.3 §2)", file=sys.stderr)
                return 1
            ops_config.set_approval_receipt(m["manifest_id"], digest)
            print(json.dumps({"approved_manifest_id": m["manifest_id"],
                              "approved_manifest_sha256": digest,
                              "pending": pending}, indent=2, sort_keys=True))
            print("APPROVAL_RECEIPT_BOUND — real P1 now matches pending + receipt + "
                  "recomputed digest + disposition=APPROVED")
            return 0
        if m.get("disposition") == "APPROVED" or ops_config.approval_receipt():
            print("error: manifest has an approval receipt / APPROVED disposition — "
                  "cancellation of an approved manifest requires explicit Founder "
                  "disposition (set manifest disposition=CANCELLED first)",
                  file=sys.stderr)
            return 1
        ops_config.set_promotion_pending(None)
        print(json.dumps({"cancelled_manifest_id": m["manifest_id"],
                          "immutable_digest": digest}, indent=2, sort_keys=True))
        print("PROMOTION_PENDING_CLEARED — exact manifest cancelled (R0.3 §13)")
        return 0

    manifest = generate_manifest(args.repo, expected_jobs=args.job,
                                 pit_as_of=args.pit_as_of, fetch=not args.no_fetch)
    out = write_manifest(manifest, args.repo, args.worktree)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"MANIFEST_WRITTEN: {out}")
    print("PROMOTION_PENDING: set (artifact-cron preflight/G0 FAILS CLOSED until "
          "verified REAL P1 or explicit cancellation — R0.2 §14)")
    print("APPROVAL REQUIRED: real P1 needs disposition=APPROVED + a digest-bound "
          "approval receipt — use --approve after Founder approval (R0.3 §2/§3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# footer: 2026-09-24 12:30 UTC+7 (R0.1-B multi-job + raw-blob correction)
