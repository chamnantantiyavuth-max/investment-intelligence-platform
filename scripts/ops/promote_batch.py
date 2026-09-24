"""Deterministic multi-job P1 promotion helper (FD #142 §10-§13; R0.1-B; R0.2; R0.3).

Exact file-content transfer from the FROZEN ops snapshot onto a target branch —
never a branch merge, never a broad cherry-pick. All hashes and git identities
are MECHANICAL; the raw git blob bytes are authoritative (binary run_git_bytes,
no text decode / no CRLF conversion).

R0.3 GOVERNANCE + ATOMICITY (POST-M5.3 O3 R0.3, FD #142 conformance):

* APPROVAL GATE (R0.3 §2/§3): a REAL P1 (into_primary=True) refuses BEFORE any
  mutation unless the manifest disposition == APPROVED AND ops-state carries an
  external receipt binding Founder approval to the EXACT immutable payload digest
  (approved_manifest_id == manifest_id; approved_manifest_sha256 == recomputed
  manifest_immutable_digest). The mutable string alone is never sufficient; a
  different/edited batch requires NEW approval; one pending manifest can never
  promote/clear another (R0.3 §13).

* TWO-PHASE (R0.3 §4): PHASE V validates the ENTIRE batch (approval binding,
  canonical refs/TOCTOU, frozen lineage, canonical delta equality, duplicate
  paths, per-artifact owner RE-DERIVED at consumption (R0.3 §8), source commit,
  latest path-touch, blob existence, raw hash) with ZERO primary mutation —
  validated artifact bytes are held in memory; PHASE M only then writes, stages
  explicit paths, commits, verifies the committed set + hashes, pushes, fetches,
  remote-verifies, advances state, cleans up. Any Phase V failure leaves primary
  main byte-for-byte clean.

* EXACT COMMIT (R0.3 §10): before push the newly-created local promotion commit
  is verified — parent == manifest_main_sha, diff --name-status main..HEAD equals
  the manifest path set (A/M only), and every committed raw blob hash equals the
  manifest — protecting against hooks/index mutation between the staged-set check
  and commit. Failure: DO NOT PUSH; preserve the local commit; bounded
  recovery / manual disposition.

* RECOVERY (R0.3 §9): a push failure RECORDS pending_p1_manifest_id + digest +
  exact local commit sha in ops-state. --recover requires those three exact
  matches (identity is never inferred from HEAD alone), re-verifies parent ==
  manifest_main_sha and the EXACT commit delta + hashes, then retries the exact
  push. Recovery proceeds ONLY for a promotion whose ORIGINAL manifest passed the
  approval gate — --recover can never bypass approval.

* FAIL-CLOSED STATE (R0.3 §6): ops-state is read through ops_config.load_state(),
  which raises StateError on corrupt/truncated/unreadable/malformed existing
  state — real P1 and recovery HOLD with stage 'state_corrupt' (corrupt state is
  NEVER interpreted as 'no lock').

* Canary (into_primary=False) may rehearse an AWAITING manifest on temporary
  target branches and NEVER advances last_promoted, NEVER touches real promotion
  state, NEVER implies Founder approval, NEVER removes the review manifest.
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
from generate_promotion_manifest import DISPOSITIONS, manifest_immutable_digest

_ARTIFACT_REQUIRED = ("path", "job_id", "source_commit", "sha256")
_MANIFEST_REQUIRED = ("manifest_id", "batch_base_sha", "manifest_main_sha",
                      "manifest_ops_head_sha", "artifacts", "changed_jobs")

PENDING_RECOVERY = "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"


def load_manifest(path: str | Path) -> dict:
    """Load + validate manifest shape. Raises ValueError on structural damage."""
    try:
        m = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ValueError(f"cannot read manifest {path}: {e}")
    if not isinstance(m, dict):
        raise ValueError(f"manifest {path} is not a JSON object")
    for key in _MANIFEST_REQUIRED:
        if key not in m:
            raise ValueError(f"manifest {path} missing required key {key!r}")
    if not isinstance(m["artifacts"], list) or not m["artifacts"]:
        raise ValueError(f"manifest {path} artifacts must be a non-empty list")
    for art in m["artifacts"]:
        if not isinstance(art, dict) or any(k not in art for k in _ARTIFACT_REQUIRED):
            raise ValueError(f"manifest {path} artifact missing required keys "
                             f"{sorted(_ARTIFACT_REQUIRED)}")
    return m


def _latest_source_in_range(repo: str, base: str, head: str, path: str) -> str:
    """Mechanical: the latest commit in base..head that touched path (R0.2 §11E)."""
    out = ops_git.run_git(repo, "log", "-1", "--format=%H", f"{base}..{head}", "--", path)
    sha = out.strip()
    if not sha:
        raise ValueError(f"no commit in {base[:12]}..{head[:12]} touches {path}")
    return sha


def _batch_delta_paths(repo: str, base: str, head: str) -> set[str]:
    """Mechanical canonical batch delta (added/modified only; D/R fail closed)."""
    out = ops_git.run_git(repo, "diff", "--name-status", f"{base}..{head}")
    paths: set[str] = set()
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status, path = parts[0][:1], parts[-1]
        if status == "D":
            raise ValueError(f"deletion in batch range not promotable: {path}")
        if status == "R":
            raise ValueError(f"rename in batch range not promotable: {path}")
        if status in {"A", "M"}:
            paths.add(path)
    return paths


def _remove_worktree_manifest(manifest_path: str | Path, operations_worktree: str | Path) -> None:
    """Interactive manifest residue removal — REAL P1 success only (R0.3 §5;
    canary NEVER deletes/updates real promotion artifacts)."""
    try:
        mp = Path(manifest_path).resolve()
        wt = Path(operations_worktree).resolve()
        inside = mp.is_relative_to(wt)
    except (OSError, AttributeError):
        inside = False
    if inside and mp.exists():
        try:
            mp.unlink()
        except OSError:
            pass


def _stage(res, stage, reason):
    res["stage"] = stage
    res["reason"] = reason
    res["ok"] = False
    return res


def _validate_batch(manifest, repo, res):
    """PHASE V — PURE read-only validation of the ENTIRE batch (R0.3 §4/§5).

    Returns the validated [(rel, raw_bytes, source_commit)] list, or None after
    setting the failure stage. PRIMARY MAIN IS NEVER MUTATED HERE — no file
    writes, no staging, no commit, no ops-state change, no lock clearing.
    """
    manifest_paths = {a["path"] for a in manifest["artifacts"]}

    # R0.3 §12: batch_base_sha must equal the canonical current reviewed main
    if manifest["batch_base_sha"] != manifest["manifest_main_sha"]:
        return _stage(res, "manifest",
                      "batch_base_sha != manifest_main_sha — internally contradictory "
                      "provenance fields are never retained (R0.3 §12)")
    # R0.3 §11: duplicate artifact path entries are FAIL CLOSED (never collapse)
    if len([a["path"] for a in manifest["artifacts"]]) != len(manifest_paths):
        return _stage(res, "manifest",
                      f"duplicate artifact path entries in manifest "
                      f"{manifest['manifest_id']} — R0.3 §11")

    # R0.2 §12: canonical artifact-set equality (exact, not subset/superset)
    try:
        delta_paths = _batch_delta_paths(repo, manifest["manifest_main_sha"],
                                         manifest["manifest_ops_head_sha"])
    except ValueError as e:
        return _stage(res, "delta", str(e))
    if delta_paths != manifest_paths:
        return _stage(res, "delta",
                      "manifest artifact set != canonical batch delta "
                      f"({manifest['manifest_main_sha']}..{manifest['manifest_ops_head_sha']}): "
                      f"omitted={sorted(manifest_paths - delta_paths)} "
                      f"added={sorted(delta_paths - manifest_paths)} — R0.2 §12")

    validated = []
    for idx, art in enumerate(manifest["artifacts"]):
        rel = ops_config.normalize_rel(art["path"])
        # target-path authority (R0.2 §7 / R0.3 §8): absolute denylist first,
        # then the UNIQUE owner MECHANICALLY RE-DERIVED at consumption
        if ops_config.is_denied(rel):
            return _stage(res, "denylist",
                          f"artifact {idx} denied by current config: {art['path']}")
        if not ops_config.job_exists(art["job_id"]):
            return _stage(res, "owner", f"artifact {idx} claims unknown job id {art['job_id']!r}")
        owners = ops_config.owning_jobs(rel)
        if len(owners) == 0:
            return _stage(res, "owner",
                          f"no owner allowlist matches {art['path']} — FAIL CLOSED (R0.3 §8)")
        if len(owners) > 1:
            return _stage(res, "owner_ambiguous",
                          f"{len(owners)} allowlists match {art['path']}: {owners} — "
                          "HOLD, main pristine (R0.3 §8)")
        if owners[0] != art["job_id"]:
            return _stage(res, "owner_mismatch",
                          f"unique owner {owners[0]} != manifest claimed {art['job_id']} "
                          f"for {art['path']} — R0.3 §8")

        src = art["source_commit"]
        try:
            ver = ops_git.run_git(repo, "rev-parse", "--verify", f"{src}^{{commit}}").strip()
        except ops_git.OpsGitError:
            return _stage(res, "source", f"source_commit {src} is not a commit (R0.2 §11A)")
        if ver != src:
            return _stage(res, "source", f"source_commit {src} is not a commit (R0.2 §11A)")
        # R0.2 §11E: source_commit is the LATEST path-touch within the frozen batch
        try:
            latest = _latest_source_in_range(repo, manifest["manifest_main_sha"],
                                             manifest["manifest_ops_head_sha"], art["path"])
        except ValueError as e:
            return _stage(res, "source", str(e))
        if latest != src:
            return _stage(res, "source",
                          f"source_commit {src} is NOT the latest path-touch in the frozen "
                          f"batch (latest={latest}) — HOLD (R0.2 §11E)")
        try:
            ops_git.run_git(repo, "cat-file", "-e", f"{src}:{art['path']}")
        except ops_git.OpsGitError:
            return _stage(res, "blob", f"path {art['path']} does not exist at {src}")
        data = ops_git.run_git_bytes(repo, "show", f"{src}:{art['path']}")
        if hashlib.sha256(data).hexdigest() != art["sha256"]:
            return _stage(res, "hash",
                          f"raw blob sha256 mismatch at {src}:{art['path']} (R0.1 89)")
        validated.append((rel, data, src))
    return validated


def _post_commit_exactness(repo, target_cwd, manifest, commit_sha):
    """R0.3 §10: verify the newly-created local promotion commit BEFORE push —
    parent == manifest_main_sha, diff main..<commit> path set == manifest set,
    committed raw blob hashes == manifest. Returns None or an error string."""
    try:
        parent = ops_git.run_git(target_cwd, "rev-parse", f"{commit_sha}^").strip()
    except ops_git.OpsGitError:
        return "promotion commit has no parent"
    if parent != manifest["manifest_main_sha"]:
        return (f"promotion commit parent {parent} != manifest_main_sha "
                f"{manifest['manifest_main_sha']}")
    expected = {a["path"] for a in manifest["artifacts"]}
    try:
        delta = _batch_delta_paths(repo, manifest["manifest_main_sha"], commit_sha)
    except ValueError as e:
        return str(e)
    if delta != expected:
        return (f"committed delta != manifest path set: "
                f"omitted={sorted(expected - delta)} added={sorted(delta - expected)}")
    for art in manifest["artifacts"]:
        try:
            data = ops_git.run_git_bytes(repo, "show", f"{commit_sha}:{art['path']}")
        except ops_git.OpsGitError:
            return f"artifact missing at promoted commit: {art['path']}"
        if hashlib.sha256(data).hexdigest() != art["sha256"]:
            return f"committed raw blob hash mismatch at {commit_sha}:{art['path']}"
    return None


def _finalize_promotion(manifest, digest, head, manifest_path, operations_worktree, res):
    """R0.4 §7 — the SAME single-atomic-save finalization shared by every
    verified success path: normal P1 success, exact-delta recovery (CASE A) and
    remote-already-successful reconciliation (CASE B). Reloads authoritative
    state, re-checks EXACT identity (pending id/digest + approval id/digest +
    recovery id/digest/commit), then sets last_promoted_ops_sha and removes ALL
    SEVEN promotion-state keys in ONE save_state(). Never uses generic clear
    helpers that could clear a newly-written foreign record."""
    try:
        st = ops_config.load_state()
    except ops_config.StateError as e:
        return _stage(res, "state_corrupt",
                      f"HOLD — ops-state corrupt at finalization: {e}")
    if (st.get("promotion_pending_manifest_id") != manifest["manifest_id"]
            or st.get("promotion_pending_manifest_sha256") != digest
            or st.get("approved_manifest_id") != manifest["manifest_id"]
            or st.get("approved_manifest_sha256") != digest
            or st.get("pending_p1_manifest_id") != manifest["manifest_id"]
            or st.get("pending_p1_manifest_sha256") != digest
            or st.get("pending_p1_local_commit_sha") != head):
        return _stage(res, "state_mismatch",
                      "concurrent promotion-state change detected — NO finalization; "
                      "HOLD for manual review (R0.4 §7)")
    final = ops_config.finalize_promotion_state(st, manifest["manifest_ops_head_sha"])
    ops_config.save_state(final)          # THE one atomic final transition
    _remove_worktree_manifest(manifest_path, operations_worktree)
    res["last_promoted_ops_sha"] = manifest["manifest_ops_head_sha"]
    res["ok"] = True                      # verified success — finalization complete
    return res


def promote_batch(manifest_path, target_branch, repo, operations_worktree,
                  do_push=False, into_primary=False, verify_only=False) -> dict:
    """Promote the exact manifest batch onto target_branch (R0.3 two-phase)."""
    repo = str(repo)
    res: dict = {"ok": False, "stage": "", "reason": "", "commit": "", "promoted": []}
    if os.environ.get("OPS_MAINTENANCE_MODE") == "ON":
        return _stage(res, "maintenance", "OPS_MAINTENANCE_MODE=ON — promotion refused")

    try:
        manifest = load_manifest(manifest_path)
    except ValueError as e:
        return _stage(res, "manifest", f"invalid manifest: {e}")

    # 1. INVOCATION CONTRACT (R0.2 §3/§5/§6) — before any fetch or file write
    if into_primary:
        if target_branch != "main":
            return _stage(res, "target",
                          "into_primary is reserved EXCLUSIVELY for target_branch == 'main' (R0.2 §5)")
        if verify_only:
            return _stage(res, "contract",
                          "into_primary + verify_only is invalid — verify-only must NEVER "
                          "dirty governed main; rehearse on a temporary worktree/branch "
                          "derived from the frozen canonical main (R0.2 §6)")
        if not do_push:
            return _stage(res, "contract",
                          "into_primary MUST imply do_push=True — a real P1 is not complete "
                          "merely because local main received a commit (R0.2 §3)")

    digest = manifest_immutable_digest(manifest)
    manifest_paths = {a["path"] for a in manifest["artifacts"]}

    # 3. FETCH + TOCTOU (R0.2 §4)
    try:
        ops_git.run_git(repo, "fetch", "origin")
    except ops_git.OpsGitError as e:
        return _stage(res, "fetch", f"fetch failed: {str(e)[:120]}")
    current_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()
    if current_main != manifest["manifest_main_sha"]:
        return _stage(res, "toctou",
                      f"origin/main {current_main} != manifest_main_sha "
                      f"{manifest['manifest_main_sha']} — HOLD (R0.2 §4)")

    # 4. FROZEN OPS SNAPSHOT LINEAGE (R0.2 §10)
    current_ops = ops_git.run_git(repo, "rev-parse", "origin/ops/automation").strip()
    if not ops_git.is_ancestor(repo, manifest["manifest_ops_head_sha"], current_ops):
        return _stage(res, "frozen_lineage",
                      f"HOLD — manifest ops head {manifest['manifest_ops_head_sha']} is no "
                      f"longer in canonical origin/ops/automation lineage ({current_ops}); do "
                      "NOT promote from an arbitrary reachable commit (R0.2 §10)")

    # 5. PRIMARY WORKTREE READINESS (R0.2 §2 P1-1) for the REAL P1 — kept BEFORE the
    # approval gate so a dirty/baseline/target refusal never depends on approval state
    if into_primary:
        branch = ops_git.run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
        if branch != "main":
            return _stage(res, "target", f"primary is on {branch}, not main")
        dirty = ops_git.porcelain(repo)
        if dirty:
            return _stage(res, "dirty",
                          "primary main worktree is NOT clean — FAIL CLOSED (never "
                          f"reset/clean), entries={dirty[:10]} (R0.2 §2C)")
        local_head = ops_git.run_git(repo, "rev-parse", "HEAD").strip()
        if local_head != current_main:
            return _stage(res, "baseline",
                          f"HOLD — local primary main {local_head} != origin/main "
                          f"{current_main} (ahead/behind/diverged); a real P1 may begin ONLY "
                          "from the exact reviewed canonical main SHA (R0.2 §2D)")

    # 2. FAIL-CLOSED ops-state read (into_primary only; R0.3 §6) + APPROVAL GATE
    state = None
    if into_primary:
        try:
            state = ops_config.load_state()
        except ops_config.StateError as e:
            return _stage(res, "state_corrupt", f"HOLD — ops-state is corrupt: {e}")
        # R0.4 §2 — pending identity is MANDATORY for real P1: there is NO valid
        # real-P1 state with an absent pending lock. Missing key OR wrong id
        # FAILS CLOSED 'pending'; fall-through to the approval gate is removed.
        # The pending pair is digest-bound (R0.4 §3/§9) — exact-manifest identity
        # holds BEFORE any receipt exists.
        if state.get("promotion_pending_manifest_id") != manifest["manifest_id"]:
            return _stage(res, "pending",
                          f"promotion_pending_manifest_id "
                          f"{state.get('promotion_pending_manifest_id')!r} != supplied "
                          f"{manifest['manifest_id']!r} — pending identity is MANDATORY "
                          "for real P1; missing/wrong lock FAILS CLOSED (R0.2 §14, "
                          "R0.4 §2)")
        if state.get("promotion_pending_manifest_sha256") != digest:
            return _stage(res, "pending",
                          f"promotion_pending_manifest_sha256 "
                          f"{state.get('promotion_pending_manifest_sha256')!r} != "
                          f"recomputed immutable digest {digest} — exact-manifest "
                          "identity required (R0.4 §2/§3)")
        approved_id = state.get("approved_manifest_id")
        approved_sha = state.get("approved_manifest_sha256")
        if approved_id != manifest["manifest_id"]:
            return _stage(res, "approval",
                          "no external approval receipt for this manifest — the mutable "
                          "disposition string alone is NEVER sufficient (R0.3 §3)")
        if approved_sha != digest:
            return _stage(res, "approval",
                          f"approved_manifest_sha256 {approved_sha} != recomputed immutable "
                          f"digest {digest} — the batch differs from the Founder-approved "
                          "batch; NEW approval required (R0.3 §3)")
        if manifest.get("disposition") not in DISPOSITIONS:
            return _stage(res, "approval",
                          f"manifest disposition {manifest.get('disposition')!r} is "
                          "missing/malformed/unknown — REFUSED (R0.3 §2)")
        if manifest["disposition"] != "APPROVED":
            return _stage(res, "approval",
                          f"manifest disposition is {manifest['disposition']!r}, not "
                          "APPROVED — real P1 REFUSED before any mutation (R0.3 §2)")

    # 8-9. PHASE V — PURE VALIDATION OF THE ENTIRE BATCH, ZERO PRIMARY MUTATION.
    # Returns the validated [(rel, data, src)] list, or sets res stage + reason
    # and returns a NON-list on failure (caller returns res unchanged).
    outcome = _validate_batch(manifest, repo, res)
    if not isinstance(outcome, list):
        return res
    validated = outcome

    # 6b. TARGET LOCATION for mutation (into_primary: primary worktree; canary: temp)
    tmp_worktree = None
    if into_primary:
        target_cwd = Path(repo)
    else:
        try:
            ops_git.run_git(repo, "rev-parse", "--verify", f"refs/heads/{target_branch}")
        except ops_git.OpsGitError:
            ops_git.run_git(repo, "branch", target_branch, "origin/main")
        tmp_worktree = Path(tempfile.mkdtemp(prefix="ops-promote-"))
        try:
            ops_git.run_git(repo, "worktree", "add", str(tmp_worktree), target_branch)
        except ops_git.OpsGitError:
            import shutil
            shutil.rmtree(tmp_worktree, ignore_errors=True)
            return _stage(res, "worktree", f"cannot add temp worktree for {target_branch}")
        target_cwd = tmp_worktree

    try:
        # verify_only is canary-rehearsal ONLY (into_primary+verify_only refused above)
        if verify_only:
            res.update({"ok": True, "stage": "verify-only",
                        "validated_paths": [p for p, _, _ in validated]})
            return res

        # 10. PHASE M — MUTATION (only after EVERY artifact passed Phase V)
        for rel, data, _src in validated:
            dest = target_cwd / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        res["promoted"] = [p for p, _, _ in validated]

        # 7. explicit-path stage + staged-set verification
        jobs = ",".join(sorted({a["job_id"] for a in manifest["artifacts"]}))
        explicit = [rel for rel, _, _ in validated]
        ops_git.run_git(target_cwd, "add", "--", *explicit)
        staged = [s.strip() for s in ops_git.run_git(
            target_cwd, "diff", "--cached", "--name-only").splitlines() if s.strip()]
        if set(staged) != manifest_paths:
            return _stage(res, "staged",
                          f"staged file set != manifest artifact set: "
                          f"staged={sorted(set(staged))} expected={sorted(manifest_paths)} — "
                          "explicit-path stage only (R0.2 §7)")

        # 8. commit governed main
        ops_git.run_git(target_cwd, "commit", "-m",
                        f"ops(promotion): manifest {manifest['manifest_id']} — {jobs} "
                        "(P1 exact-content transfer, FD #142; Founder-approved batch, R0.3)")
        commit_sha = ops_git.run_git(target_cwd, "rev-parse", "HEAD").strip()
        res["commit"] = commit_sha

        # 9. POST-COMMIT EXACTNESS BEFORE PUSH (R0.3 §10)
        problem = _post_commit_exactness(repo, target_cwd, manifest, commit_sha)
        if problem is not None:
            return _stage(res, "post_commit",
                          f"committed-delta verification FAILED — DO NOT PUSH: {problem}. "
                          "Local promotion commit preserved for bounded recovery/manual "
                          "disposition (R0.3 §10)")

        # 9b. RECORD recovery identity BEFORE the uncertain push (R0.4 §6) —
        # once approval + Phase V + post-commit verification passed, persist the
        # EXACT pending id/digest + approval id/digest + recovery id/digest/commit
        # atomically, THEN push. Makes BOTH 'push failed' AND 'remote accepted
        # but process disappeared / ack lost' recoverable deterministically.
        # last_promoted is NOT marked here.
        if into_primary:
            try:
                st = ops_config.load_state()
            except ops_config.StateError as e:
                return _stage(res, "state_corrupt", f"HOLD — ops-state corrupt: {e}")
            st["pending_p1_manifest_id"] = manifest["manifest_id"]
            st["pending_p1_manifest_sha256"] = digest
            st["pending_p1_local_commit_sha"] = commit_sha
            ops_config.save_state(st)

        # 10/11/12. PUSH -> FETCH -> REMOTE VERIFY
        if into_primary or do_push:
            try:
                ops_git.run_git(target_cwd, "push", "origin", target_branch)
            except ops_git.OpsGitError as e:
                if into_primary:
                    # identity ALREADY recorded pre-push (R0.4 §6) — preserve it
                    res["pending_state"] = PENDING_RECOVERY
                    return _stage(res, "push_recovery",
                                  f"push FAILED after local promotion commit {commit_sha} — "
                                  f"commit PRESERVED, recovery identity ALREADY recorded, "
                                  f"origin/{target_branch} unchanged, last_promoted NOT "
                                  f"advanced; recover with --recover (verifies recorded "
                                  f"pending identity + parent + exact delta + hashes, then "
                                  f"reconciles remote: base/exact-commit/other, R0.4 §5) or "
                                  f"Founder disposition. ({str(e)[:120]}) (R0.3 §9, R0.4 §6)")
                return _stage(res, "push_recovery",
                              f"push FAILED after local commit {commit_sha} — HOLD "
                              f"({str(e)[:120]})")
            try:
                ops_git.run_git(repo, "fetch", "origin")
            except ops_git.OpsGitError as e:
                if into_primary:
                    # ack-loss window (R0.4 §5): remote may ALREADY hold P — the
                    # recorded identity is preserved; recovery reconciles
                    res["pending_state"] = PENDING_RECOVERY
                    return _stage(res, "push_recovery",
                                  f"post-push fetch failed — push outcome UNKNOWN; "
                                  f"recovery identity recorded, recover with --recover to "
                                  f"reconcile remote (base/exact-commit/other) ({str(e)[:120]}) "
                                  f"(R0.4 §5)")
                return _stage(res, "fetch", f"post-push fetch failed: {str(e)[:120]}")
            remote = ops_git.run_git(repo, "rev-parse", f"origin/{target_branch}").strip()
            if remote != commit_sha:
                if into_primary:
                    res["pending_state"] = PENDING_RECOVERY
                    return _stage(res, "verify",
                                  f"remote {remote} != local {commit_sha} — "
                                  f"{PENDING_RECOVERY} (identity recorded pre-push, R0.4 §6)")
                return _stage(res, "verify",
                              f"remote {remote} != local {commit_sha} — HOLD")
            res["remote_verified"] = True

        # 13/14/15. ONE ATOMIC FINAL STATE TRANSITION (R0.4 §7) — reload the
        # authoritative state and re-check EXACT identity, then set
        # last_promoted + remove ALL SEVEN promotion-state keys in ONE save.
        if into_primary:
            fin = _finalize_promotion(manifest, digest, commit_sha, manifest_path,
                                      operations_worktree, res)
            if not fin["ok"]:
                return fin
            res = fin

        res["ok"] = True
        res["stage"] = "promoted"
        return res
    finally:
        if tmp_worktree is not None:
            try:
                ops_git.run_git(repo, "worktree", "remove", "--force", str(tmp_worktree))
            except ops_git.OpsGitError:
                pass


def recover_local_promotion(manifest_path, repo, operations_worktree,
                            target_branch="main") -> dict:
    """R0.3 §9 deterministic recovery: the preserved local promotion commit must
    match the RECORDED pending identity (id + digest + exact commit sha) AND pass
    parent + exact-delta + hash verification before the EXACT push is retried.
    Proceeds only for a promotion whose ORIGINAL manifest passed the approval
    gate (R0.3 §2). No reset, no history rewrite."""
    repo = str(repo)
    res: dict = {"ok": False, "stage": "", "reason": "", "commit": ""}
    try:
        manifest = load_manifest(manifest_path)
    except ValueError as e:
        return _stage(res, "manifest", f"invalid manifest: {e}")
    digest = manifest_immutable_digest(manifest)

    try:
        state = ops_config.load_state()
    except ops_config.StateError as e:
        return _stage(res, "state_corrupt", f"HOLD — ops-state is corrupt: {e}")

    if target_branch != "main":
        return _stage(res, "target", "recovery is reserved for governed main")
    branch = ops_git.run_git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch != target_branch:
        return _stage(res, "target", f"primary is on {branch}, not {target_branch}")

    # APPROVAL GATE — --recover can never bypass Founder approval (R0.3 §2),
    # and requires the MANDATORY exact pending identity (id + digest, R0.4 §2/§6)
    if state.get("promotion_pending_manifest_id") != manifest["manifest_id"]:
        return _stage(res, "pending",
                      f"pending manifest {state.get('promotion_pending_manifest_id')!r} != "
                      f"supplied {manifest['manifest_id']!r}")
    if state.get("promotion_pending_manifest_sha256") != digest:
        return _stage(res, "pending",
                      "pending digest != recomputed immutable digest — recovery "
                      "requires the exact pending identity (R0.4 §2/§6)")
    if state.get("approved_manifest_id") != manifest["manifest_id"]:
        return _stage(res, "approval",
                      "no approval receipt for this manifest — recovery cannot bypass the "
                      "approval gate (R0.3 §2)")
    if state.get("approved_manifest_sha256") != digest:
        return _stage(res, "approval",
                      "approval digest != recomputed immutable digest — recovery refused")
    if manifest.get("disposition") != "APPROVED":
        return _stage(res, "approval",
                      f"disposition is {manifest.get('disposition')!r}, not APPROVED")

    # RECORDED recovery identity — exact matches only (R0.3 §9)
    rec = ops_config.pending_p1_record()
    if not rec:
        return _stage(res, "recovery_identity",
                      "no recorded pending-P1 identity — recovery never infers identity from "
                      "current HEAD alone (R0.3 §9)")
    head = ops_git.run_git(repo, "rev-parse", "HEAD").strip()
    if (rec.get("pending_p1_manifest_id") != manifest["manifest_id"]
            or rec.get("pending_p1_manifest_sha256") != digest
            or rec.get("pending_p1_local_commit_sha") != head):
        return _stage(res, "recovery_identity",
                      f"recorded recovery identity does not match current HEAD {head} — "
                      "manual Founder disposition required (R0.3 §9)")

    # parent == manifest_main_sha
    try:
        parent = ops_git.run_git(repo, "rev-parse", "HEAD^").strip()
    except ops_git.OpsGitError:
        return _stage(res, "parent", "no parent — HEAD is not a promotion commit")
    if parent != manifest["manifest_main_sha"]:
        return _stage(res, "parent",
                      f"preserved commit parent {parent} != manifest_main_sha "
                      f"{manifest['manifest_main_sha']} — exact push NOT safe; Founder "
                      "disposition required")

    # EXACT COMMIT DELTA (R0.3 §9): path set + A/M only + per-artifact hashes
    expected = {a["path"] for a in manifest["artifacts"]}
    try:
        delta = _batch_delta_paths(repo, manifest["manifest_main_sha"], head)
    except ValueError as e:
        return _stage(res, "commit_delta", str(e))
    if delta != expected:
        return _stage(res, "commit_delta",
                      f"preserved commit delta != manifest path set: "
                      f"omitted={sorted(expected - delta)} added={sorted(delta - expected)} — "
                      "recovery REFUSED, no push (R0.3 §9)")
    for art in manifest["artifacts"]:
        try:
            data = ops_git.run_git_bytes(repo, "show", f"HEAD:{art['path']}")
        except ops_git.OpsGitError:
            return _stage(res, "hash", f"artifact missing at HEAD: {art['path']}")
        if hashlib.sha256(data).hexdigest() != art["sha256"]:
            return _stage(res, "hash", f"artifact hash mismatch at HEAD: {art['path']}")

    try:
        ops_git.run_git(repo, "fetch", "origin")
    except ops_git.OpsGitError as e:
        return _stage(res, "fetch", f"fetch failed: {str(e)[:120]}")
    origin_main = ops_git.run_git(repo, "rev-parse", "origin/main").strip()

    # R0.4 §5 — REMOTE SUCCESS / ACKNOWLEDGEMENT-LOSS RECONCILIATION.
    # The push may have ACTUALLY SUCCEEDED while the client reported failure or
    # the process died before state finalization. Distinguish mechanically:
    #   CASE A  origin/main == base (B)   -> remote did NOT receive it -> retry EXACT push
    #   CASE B  origin/main == exact promotion commit (P) -> remote ALREADY has it
    #           -> DO NOT push again -> STATE-FINALIZATION ONLY -> reconciled_remote_success
    #   CASE C  origin/main == any other SHA -> FAIL CLOSED main_moved, Founder only
    if origin_main == manifest["manifest_main_sha"]:
        # CASE A — remote did NOT receive the promotion: retry the exact push.
        try:
            ops_git.run_git(repo, "push", "origin", target_branch)
        except ops_git.OpsGitError as e:
            res["pending_state"] = PENDING_RECOVERY
            return _stage(res, "push", f"exact push retry failed: {str(e)[:120]}")
        try:
            ops_git.run_git(repo, "fetch", "origin")
        except ops_git.OpsGitError:
            res["pending_state"] = PENDING_RECOVERY
            return _stage(res, "fetch",
                          "post-push fetch failed — outcome unknown; run --recover "
                          "again to reconcile (R0.4 §5)")
        remote = ops_git.run_git(repo, "rev-parse", f"origin/{target_branch}").strip()
        if remote != head:
            res["pending_state"] = PENDING_RECOVERY
            return _stage(res, "verify", f"remote {remote} != local {head}")
        fin = _finalize_promotion(manifest, digest, head, manifest_path,
                                  operations_worktree, res)
        if not fin["ok"]:
            return fin
        res = fin
        res.update({"stage": "recovered", "remote_verified": True,
                    "commit": head})
        return res
    if origin_main == head:
        # CASE B — the remote ALREADY holds the exact recorded promotion commit:
        # delivery succeeded, acknowledgements were lost. NO second push —
        # verify the recorded identity (done above) and finalize state ONLY.
        fin = _finalize_promotion(manifest, digest, head, manifest_path,
                                  operations_worktree, res)
        if not fin["ok"]:
            return fin
        res = fin
        res.update({"stage": "recovered", "remote_verified": True,
                    "reconciled_remote_success": True, "commit": head})
        return res
    # CASE C — remote is neither the reviewed base nor the exact promotion commit
    res["pending_state"] = PENDING_RECOVERY
    return _stage(res, "main_moved",
                  f"origin/main {origin_main} is neither the reviewed base "
                  f"{manifest['manifest_main_sha']} nor the exact promotion commit "
                  f"{head} — FAIL CLOSED, NO state clearing; Founder disposition only "
                  f"(R0.4 §5)")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="C+ deterministic multi-job P1 batch promotion / recovery "
                    "(exact-content transfer; Founder-approval gate; two-phase; FD #142)")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--target-branch", default="main")
    ap.add_argument("--repo", default=ops_config.DEFAULT_REPO)
    ap.add_argument("--worktree", default=ops_config.DEFAULT_OPS_WORKTREE)
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--into-primary", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--recover", action="store_true",
                    help="deterministic recovery (R0.3 §9): verify the recorded pending "
                         "identity + parent + exact commit delta + hashes, then retry the "
                         "EXACT push")
    args = ap.parse_args()

    if args.recover:
        res = recover_local_promotion(args.manifest, args.repo, args.worktree, args.target_branch)
    else:
        res = promote_batch(args.manifest, args.target_branch, args.repo, args.worktree,
                            do_push=args.push, into_primary=args.into_primary,
                            verify_only=args.verify_only)
    print(json.dumps(res, indent=2, sort_keys=True))
    if res.get("stage") in {"toctou", "push_recovery", "verify", "post_commit",
                            "state_corrupt", "approval", "pending"} and not res["ok"]:
        return 2
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())