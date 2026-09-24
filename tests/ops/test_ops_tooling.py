"""C+ ops tooling full-matrix tests (FD #142 §12) — temp git repos only; never the real worktree.

Areas: allowlist/denylist anchoring, deletion/rename rejection, Learning-Loop
no-output, G0 A/B/C/D/E, sync fast-forward + fail-closed, OPS_SYNC_BASE delta
semantics, manifest determinism, TOCTOU HOLD, newer-ops frozen snapshot, altered
hash rejection, no-branch-merge, push-failure preserve + next-run refusal, explicit
minimum staging.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "ops"))

import ops_config  # noqa: E402
import ops_git  # noqa: E402
import g0_check  # noqa: E402
import sync_main_to_ops  # noqa: E402
import validate_delta  # noqa: E402
import commit_push_ops  # noqa: E402
import generate_promotion_manifest  # noqa: E402
import promote_batch  # noqa: E402

WEEKLY = "8ba233e88015"
MIDWEEK = "cda817d17236"
LL = "1f5f03f9236d"


def git(cwd, *args, check=True):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       env=dict(os.environ))
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def write(cwd, rel, content="body"):
    p = Path(cwd) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


@pytest.fixture
def fx(tmp_path, monkeypatch):
    monkeypatch.setenv("OPS_STATE_DIR", str(tmp_path / "state"))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    Path(tmp_path / "home").mkdir(parents=True, exist_ok=True)
    origin = tmp_path / "origin.git"
    git(tmp_path, "init", "--bare", str(origin))
    git(tmp_path, "--git-dir", str(origin), "symbolic-ref", "HEAD", "refs/heads/main")
    canonical = tmp_path / "canonical"
    git(tmp_path, "clone", str(origin), str(canonical))
    git(canonical, "config", "user.name", "Test"); git(canonical, "config", "user.email", "t@t")
    write(canonical, "README.md")
    write(canonical, "PROJECT_STATE.md")
    write(canonical, "evidence/radar/digests/2019-12-31-radar-digest.md", "old")
    git(canonical, "add", "-A"); git(canonical, "commit", "-m", "init")
    git(canonical, "push", "origin", "main")
    git(canonical, "push", "origin", "main:refs/heads/ops/automation")
    ops = tmp_path / "ops"
    git(tmp_path, "clone", str(origin), str(ops))
    git(ops, "config", "user.name", "Test"); git(ops, "config", "user.email", "t@t")
    git(ops, "fetch", "origin")
    git(ops, "checkout", "-b", "ops/automation", "origin/ops/automation")
    return {"tmp": tmp_path, "origin": origin, "canonical": canonical, "ops": ops}


# ---- allowlist / denylist / anchoring ----------------------------------------

def test_allowlist_success(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    d = validate_delta.validate_delta(WEEKLY, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is True
    assert d["allowed"] == [{"path": "evidence/radar/digests/2026-09-23-radar-digest.md", "status": "A"}]


def test_denylist_overrides_allowlist(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    write(fx["ops"], "PROJECT_STATE.md", "tampered")
    d = validate_delta.validate_delta(WEEKLY, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is False
    assert any("denylist" in v for v in d["violations"])


def test_path_anchoring_fullmatch(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md.bak")
    write(fx["ops"], "x2026-09-23-radar-digest.md")
    write(fx["ops"], "evidence/radar/digests/sub/2026-09-23-radar-digest.md")
    d = validate_delta.validate_delta(WEEKLY, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is False
    assert len(d["violations"]) == 3


def test_deletion_rejection(fx):
    git(fx["ops"], "rm", "evidence/radar/digests/2019-12-31-radar-digest.md")
    d = validate_delta.validate_delta(WEEKLY, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is False
    assert any("deletion" in v for v in d["violations"])


def test_rename_rejection(fx):
    git(fx["ops"], "mv", "evidence/radar/digests/2019-12-31-radar-digest.md",
        "evidence/radar/digests/2020-01-02-radar-digest.md")
    d = validate_delta.validate_delta(WEEKLY, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is False
    assert any("rename" in v for v in d["violations"])


def test_learning_loop_no_output(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")  # not LL's allowlist
    write(fx["ops"], "tmp-observer-note.md")
    d = validate_delta.validate_delta(LL, fx["ops"], git(fx["ops"], "rev-parse", "HEAD").strip())
    assert d["ok"] is False
    assert len(d["violations"]) == 2


def test_unknown_job_fails(fx):
    d = validate_delta.validate_delta("nope", fx["ops"], "HEAD")
    assert d["ok"] is False


# ---- G0 preservation gate ------------------------------------------------------

def test_g0_equal_clean(fx):
    res = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert res["ok"] is True and res["case"] == "A"


def test_g0_local_behind_ff_ready(fx):
    assert g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)["case"] == "A"
    # advance remote ops beyond local (canonical pushes a commit to ops branch)
    write(fx["canonical"], "evidence/radar/digests/2026-01-01-radar-digest.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "remote ops artifact")
    git(fx["canonical"], "push", "origin", "main:refs/heads/ops/automation")
    res = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert res["case"] == "B" and res["ok"] is True


def test_g0_local_ahead_blocked_preserved(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    git(fx["ops"], "add", "-A"); git(fx["ops"], "commit", "-m", "unpushed artifact")
    head_before = git(fx["ops"], "rev-parse", "HEAD").strip()
    res = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert res["ok"] is False and res["case"] == "C"
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == head_before  # never reset


def test_g0_diverged_fail_closed(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    git(fx["ops"], "add", "-A"); git(fx["ops"], "commit", "-m", "local divergence")
    write(fx["canonical"], "evidence/radar/digests/2026-01-01-radar-digest.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "remote divergence")
    git(fx["canonical"], "push", "origin", "main:refs/heads/ops/automation")
    res = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert res["ok"] is False and res["case"] == "D"


def test_g0_dirty_fail_closed_preserve(fx):
    write(fx["ops"], "stray-output.md")
    res = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert res["ok"] is False and res["case"] == "E"
    assert (fx["ops"] / "stray-output.md").exists()  # preserved


# ---- sync main -> ops -----------------------------------------------------------

def test_sync_ff_captures_base(fx):
    write(fx["canonical"], "docs/gov.md"); git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "main governance"); git(fx["canonical"], "push", "origin", "main")
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is True
    main = git(fx["canonical"], "rev-parse", "origin/main").strip()
    assert res["ops_sync_base_sha"] == main
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == main  # fast-forwarded
    assert ops_config.load_state()["ops_sync_base_sha"] == main


def test_ops_sync_base_delta_semantics(fx):
    """After a main->ops sync adds governance.md, the job delta base must NOT include it."""
    base_old = git(fx["ops"], "rev-parse", "HEAD").strip()
    write(fx["canonical"], "docs/gov.md"); git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "main governance"); git(fx["canonical"], "push", "origin", "main")
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    base_new = res["ops_sync_base_sha"]
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")

    d_new = validate_delta.validate_delta(WEEKLY, fx["ops"], base_new)
    assert d_new["ok"] is True  # delta excludes the synced governance.md

    d_old = validate_delta.validate_delta(WEEKLY, fx["ops"], base_old)
    assert d_old["ok"] is False  # wrong base would falsely count sync changes


# ---- commit + push -------------------------------------------------------------

def test_commit_push_explicit_staging(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    res = commit_push_ops.commit_push_ops(WEEKLY, fx["ops"], fx["canonical"],
                                          git(fx["ops"], "rev-parse", "HEAD").strip(),
                                          do_push=True)
    assert res["ok"] is True and res["remote_verified"] is True
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == res["commit"]
    assert "evidence/radar/digests/2026-09-23-radar-digest.md" in git(fx["ops"], "show", "--stat", res["commit"])


def test_push_failure_preserves_and_next_run_refuses(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    # sabotage remote URL -> push fails
    git(fx["ops"], "remote", "set-url", "origin", str(fx["tmp"] / "nonexistent.git"))
    res = commit_push_ops.commit_push_ops(WEEKLY, fx["ops"], fx["canonical"],
                                          git(fx["ops"], "rev-parse", "HEAD").strip(),
                                          do_push=True)
    assert res["ok"] is False and "PRESERVED" in res["reason"]
    head = git(fx["ops"], "rev-parse", "HEAD").strip()
    assert head != git(fx["ops"], "rev-parse", "origin/ops/automation").strip()
    # remote URL restored; next G0 refuses a new job (case C), commit preserved
    git(fx["ops"], "remote", "set-url", "origin", str(fx["origin"]))
    g0 = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert g0["case"] == "C" and g0["ok"] is False
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == head  # commit preserved


# ---- promotion ------------------------------------------------------------------

def _make_artifact_commit(fx, rel, base_sha):
    write(fx["ops"], rel)
    git(fx["ops"], "add", "--", rel)
    git(fx["ops"], "commit", "-m", f"artifact {rel}")
    git(fx["ops"], "push", "origin", "ops/automation")
    return git(fx["ops"], "rev-parse", "HEAD").strip()


def _manifest_for(fx, job, head, base=None):
    repo, ops = str(fx["canonical"]), fx["ops"]
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    base = base or git(repo, "rev-parse", "origin/ops/automation").strip()
    m = generate_promotion_manifest.generate_manifest(repo, base, head,
                                                      expected_jobs=[job], fetch=False)
    return m


def test_manifest_deterministic_hashes(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m1 = _manifest_for(fx, WEEKLY, head, base)
    m2 = _manifest_for(fx, WEEKLY, head, base)
    assert m1["manifest_id"] == m2["manifest_id"]
    a = m1["artifacts"][0]
    data = git_b(fx["canonical"], "show", f"{head}:evidence/radar/digests/2026-09-23-radar-digest.md")
    assert a["sha256"] == hashlib.sha256(data).hexdigest()
    assert a["source_commit"] == head  # real per-path source within the range
    assert a["job_id"] == WEEKLY     # mechanical ownership
    assert m1["allowlist_result"] == "PASS" and m1["denylist_result"] == "PASS"
    assert m1["manifest_main_sha"] == git(fx["canonical"], "rev-parse", "origin/main").strip()


def test_toctou_main_advance_holds(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    # advance main AFTER manifest
    write(fx["canonical"], "docs/new.md"); git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "main advanced"); git(fx["canonical"], "push", "origin", "main")
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["stage"] == "toctou" and res["ok"] is False


def test_newer_ops_frozen_snapshot_only(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head1 = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head1, base)  # frozen at head1
    _make_artifact_commit(fx, "evidence/radar/digests/2026-09-24-radar-digest.md", head1)  # newer, NOT in manifest
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is True
    assert res["promoted"] == ["evidence/radar/digests/2026-09-23-radar-digest.md"]
    # target branch contains ONLY the frozen artifact
    assert "2026-09-24" not in git(fx["canonical"], "show", f"wip/canary:evidence/radar/digests/2026-09-24-radar-digest.md", check=False)


def test_altered_hash_rejected(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["artifacts"][0]["sha256"] = "0" * 64  # tamper
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["stage"] == "hash" and res["ok"] is False


def test_promotion_no_branch_merge(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    before = git(fx["canonical"], "rev-parse", "main").strip()
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is True
    parents = git(fx["canonical"], "show", "--no-patch", "--format=%P", "wip/canary").strip().split()
    assert len(parents) == 1  # linear commit, NOT a merge
    assert git(fx["canonical"], "rev-parse", "main").strip() == before  # main untouched
    assert not git(fx["canonical"], "log", "--oneline", "--graph", "--all").startswith("*   ")  # no merge commit


def test_maintenance_mode_blocks(fx, monkeypatch):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    monkeypatch.setenv("OPS_MAINTENANCE_MODE", "ON")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["stage"] == "maintenance" and res["ok"] is False
    monkeypatch.delenv("OPS_MAINTENANCE_MODE")


# ---- R0.1 RED diagnostics (POST-M5.3 O3 R0.1, 24 Sep 2026) -------------------
# The normal ops-ahead-main lifecycle (one artifact commit on ops, main unchanged)
# is the C+ core architecture; the R0 sync must accept S0/S1/S2/S3. These tests
# demonstrate the R0 behavior gaps BEFORE the runtime correction (TDD RED).

def git_b(cwd, *args):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=False)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr!r}")
    return r.stdout


def _push_ops(fx):
    git(fx["ops"], "push", "origin", "ops/automation")
    git(fx["canonical"], "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")


# ---- T1 / T2 — the previously-missing acceptance scenario --------------------

def test_t1_ops_ahead_main_unchanged(fx):
    """OPS AHEAD / MAIN UNCHANGED: main=A, ops=A-R1 -> next sync PASS, no merge, base=R1."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()  # A
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)  # A-R1
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is True, res
    assert res["ops_sync_base_sha"] == head          # base = R1 (current ops HEAD)
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == head   # never reset / never merged
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == base  # main unchanged
    # no merge commit introduced
    assert len(git(fx["ops"], "show", "--no-patch", "--format=%P", "HEAD").strip().split()) == 1
    assert ops_config.load_state()["ops_sync_base_sha"] == head


def test_t2_two_sequential_normal_cron_cycles(fx):
    """A -> R1 artifact push -> next pre-run sync PASS -> R2 artifact push. No main movement."""
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    r1 = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", a)
    s1 = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert s1["ok"] is True and s1["ops_sync_base_sha"] == r1
    # cycle 2: job writes its second artifact and commits/pushes against base=R1
    write(fx["ops"], "evidence/radar/digests/2026-09-24-radar-digest.md")
    c2 = commit_push_ops.commit_push_ops(WEEKLY, fx["ops"], fx["canonical"],
                                         ops_config.load_state()["ops_sync_base_sha"], do_push=True)
    assert c2["ok"] is True and c2["remote_verified"] is True
    r2 = c2["commit"]
    # cycle 2's own next pre-run sync: ops=A-R1-R2, main=A -> S2 PASS
    s2 = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert s2["ok"] is True and s2["ops_sync_base_sha"] == r2
    # both artifacts are in the final ops tree; main untouched
    tree = set(git(fx["ops"], "ls-tree", "-r", "--name-only", r2).splitlines())
    assert "evidence/radar/digests/2026-09-23-radar-digest.md" in tree
    assert "evidence/radar/digests/2026-09-24-radar-digest.md" in tree
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == a


# ---- T3 — local ops behind remote ops ----------------------------------------

def test_t3_local_ops_behind_remote_ops(fx):
    """Remote ops advances; G0 case B; sync first ff's local to origin/ops; no history lost."""
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    # simulate remote ops advance from another writer: canonical commits + pushes main:ops
    write(fx["canonical"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "remote ops artifact")
    git(fx["canonical"], "push", "origin", "main:refs/heads/ops/automation")
    git(fx["ops"], "fetch", "origin")
    remote = git(fx["ops"], "rev-parse", "origin/ops/automation").strip()
    assert remote != a  # remote advanced
    assert g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)["case"] == "B"
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is True
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == remote        # local ff'd to remote
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == remote  # nothing lost
    assert res["ops_sync_base_sha"] == remote
    assert git(fx["ops"], "rev-parse", "HEAD").strip() != a


# ---- T4 — main ahead ----------------------------------------------------------

def test_t4_main_ahead_ff_and_durable_push(fx):
    """ops=A, main=A-G1 -> sync fast-forwards ops to G1 AND pushes/verifies remote ops."""
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    write(fx["canonical"], "docs/gov.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "main G1")
    git(fx["canonical"], "push", "origin", "main")
    g1 = git(fx["canonical"], "rev-parse", "origin/main").strip()
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is True
    assert res["ops_sync_base_sha"] == g1
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == g1
    # durable: remote ops == local (sync itself pushed; next G0 must NOT see case C)
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == g1
    assert g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)["case"] == "A"


# ---- T5 / T6 — true divergence -----------------------------------------------

def test_t5_divergence_clean_merge(fx):
    """ops=A-R1, main=A-G1 -> sync merges main INTO ops; ops has both; main untouched; base=merge."""
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    r1 = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", a)
    write(fx["canonical"], "docs/gov.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "main G1")
    git(fx["canonical"], "push", "origin", "main")
    g1 = git(fx["canonical"], "rev-parse", "origin/main").strip()
    assert not sync_main_to_ops.__dict__.get("_x", None)  # no-op guard
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is True, res
    head = git(fx["ops"], "rev-parse", "HEAD").strip()
    assert head == res["ops_sync_base_sha"]
    # merge commit has BOTH parents
    parents = git(fx["ops"], "show", "--no-patch", "--format=%P", "HEAD").strip().split()
    assert len(parents) == 2
    # ops contains both histories
    assert r1 in git(fx["ops"], "log", "--format=%H").split()
    assert g1 in git(fx["ops"], "log", "--format=%H").split()
    assert "docs/gov.md" in git(fx["ops"], "ls-tree", "-r", "--name-only", "HEAD").splitlines()
    assert "evidence/radar/digests/2026-09-23-radar-digest.md" in git(fx["ops"], "ls-tree", "-r", "--name-only", "HEAD").splitlines()
    # main unchanged; remote ops verified
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == g1
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == head


def test_t6_divergence_conflict_abort_fail_closed(fx):
    """ops changes X, main changes X incompatibly -> merge conflict -> abort, preserve, FAIL."""
    target = "evidence/radar/digests/2019-12-31-radar-digest.md"  # present at init ("old")
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    # ops modifies X
    write(fx["ops"], target, "ops version 1")
    git(fx["ops"], "add", "--", target); git(fx["ops"], "commit", "-m", "ops changes X")
    git(fx["ops"], "push", "origin", "ops/automation")
    r1 = git(fx["ops"], "rev-parse", "HEAD").strip()
    # main modifies X incompatibly
    write(fx["canonical"], target, "main version 1")
    git(fx["canonical"], "add", "--", target); git(fx["canonical"], "commit", "-m", "main changes X")
    git(fx["canonical"], "push", "origin", "main")
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=False)
    assert res["ok"] is False
    assert "conflict" in res["reason"].lower() or "abort" in res["reason"].lower()
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == r1          # pre-merge ops HEAD preserved
    assert not ops_git.porcelain(fx["ops"])                            # worktree clean after abort
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == r1  # no remote mutation
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() != r1  # main untouched
    # a merge never landed: HEAD has a single parent (the pre-merge commit)
    assert len(git(fx["ops"], "show", "--no-patch", "--format=%P", "HEAD").strip().split()) == 1


# ---- T7 — sync push failure ---------------------------------------------------

def test_t7_sync_push_failure_preserves_and_blocks(fx, monkeypatch):
    """Sync creates new ops baseline, push fails -> local commit preserved, base not stored,
    job MUST NOT start; next G0 blocks (case C) until the exact sync commit is recovered."""
    a = git(fx["ops"], "rev-parse", "HEAD").strip()
    write(fx["canonical"], "docs/gov.md")
    git(fx["canonical"], "add", "-A"); git(fx["canonical"], "commit", "-m", "main G1")
    git(fx["canonical"], "push", "origin", "main")
    real_run = ops_git.run_git
    def fake_run(cwd, *args, check=True, env_extra=None):
        if args and args[0] == "push":
            raise ops_git.OpsGitError("simulated sync push failure")
        return real_run(cwd, *args, check=check, env_extra=env_extra)
    monkeypatch.setattr(ops_git, "run_git", fake_run)
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=True)
    assert res["ok"] is False
    assert "PRESERVED" in res["reason"] or "preserved" in res["reason"]
    g1 = git(fx["canonical"], "rev-parse", "origin/main").strip()
    assert git(fx["ops"], "rev-parse", "HEAD").strip() == g1          # local sync commit preserved
    assert git(fx["ops"], "rev-parse", "origin/ops/automation").strip() == a  # remote unchanged
    assert "ops_sync_base_sha" not in ops_config.load_state()          # baseline NOT stored -> job must not start
    # next G0 blocks until the exact sync commit is recovered
    g0 = g0_check.g0_check(fx["ops"], fx["canonical"], do_fetch=True)
    assert g0["case"] == "C" and g0["ok"] is False


# ---- M1 / M7 — promotion manifest defects (RED against R0 generator) ---------

AM = "73e611584447"
CIW = "8b1cd19aba7d"
AM_REL = "operational/self-reflection-logs/2026-09-23-run-AM-V0-20260923-090101.md"
CIW_REL = "docs/ciw-pilot-msft/monitoring/2026-09-23-monitoring-draft.md"


def test_m1_multi_job_batch_single_manifest(fx):
    """Radar R + AM M in ONE batch range -> one manifest, two jobs, respective source commits."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()  # A
    r = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _make_artifact_commit(fx, AM_REL, r)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    # single manifest over A..M covering BOTH artifact classes
    manifest = generate_promotion_manifest.generate_manifest(repo, base, m, fetch=False)
    paths = {a["path"] for a in manifest["artifacts"]}
    assert paths == {"evidence/radar/digests/2026-09-23-radar-digest.md", AM_REL}
    owners = {a["job_id"] for a in manifest["artifacts"]}
    assert owners == {WEEKLY, AM}
    src = {a["path"]: a["source_commit"] for a in manifest["artifacts"]}
    assert src["evidence/radar/digests/2026-09-23-radar-digest.md"] == r
    assert src[AM_REL] == m
    assert manifest["manifest_ops_head_sha"] == m


def test_m7_raw_blob_hash_not_working_tree(fx):
    """Non-UTF8 + CRLF raw blob: manifest sha256 must equal raw `git show` blob bytes.

    The blob is staged via plumbing (hash-object -w --stdin + update-index
    --cacheinfo) so the EXACT bytes (CRLF + latin-1) land in the object store —
    working-tree CRLF filters (core.autocrlf) are bypassed deterministically.
    """
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    rel = "evidence/radar/digests/2026-09-23-radar-digest.md"
    blob = b"prices \xe9 2026-09-23\nsecond line\r\n"  # latin-1 byte + CRLF inside blob
    r = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=str(fx["ops"]),
                       input=blob, capture_output=True, text=False)
    assert r.returncode == 0, r.stderr
    obj = r.stdout.strip()
    git(fx["ops"], "update-index", "--add", "--cacheinfo", f"100644,{obj.decode()},{rel}")
    git(fx["ops"], "commit", "-m", "raw blob artifact")
    git(fx["ops"], "push", "origin", "ops/automation")
    head = git(fx["ops"], "rev-parse", "HEAD").strip()
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    manifest = generate_promotion_manifest.generate_manifest(repo, base, head, fetch=False)
    raw = git_b(repo, "show", f"{head}:{rel}")
    assert raw == blob  # plumbing staging preserved the exact CRLF + latin-1 bytes
    # R0.1 §9: hash over the RAW GIT BLOB BYTES, not working-tree bytes
    assert manifest["artifacts"][0]["sha256"] == hashlib.sha256(raw).hexdigest()
    # the R0 text-mode re-encode approach (errors=replace) must NOT equal it
    old = hashlib.sha256(
        subprocess.run(["git", "show", f"{head}:{rel}"], cwd=repo, capture_output=True,
                       text=True, encoding="utf-8", errors="replace").stdout.encode("utf-8")
    ).hexdigest()
    assert old != manifest["artifacts"][0]["sha256"]


def test_m2_radar_ciw_multi_job_batch(fx):
    """Radar R + CIW C in ONE batch -> one manifest, two owners, respective source commits."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    r = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    c = _make_artifact_commit(fx, CIW_REL, r)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    manifest = generate_promotion_manifest.generate_manifest(repo, base, c, fetch=False)
    paths = {a["path"] for a in manifest["artifacts"]}
    assert paths == {"evidence/radar/digests/2026-09-23-radar-digest.md", CIW_REL}
    owners = {a["job_id"] for a in manifest["artifacts"]}
    assert owners == {WEEKLY, CIW}
    src = {a["path"]: a["source_commit"] for a in manifest["artifacts"]}
    assert src["evidence/radar/digests/2026-09-23-radar-digest.md"] == r
    assert src[CIW_REL] == c
    assert sorted(manifest["changed_jobs"]) == sorted([WEEKLY, CIW])


def test_m3_unknown_path_fail_closed(fx):
    """Unknown path mixed into the batch -> FAIL CLOSED (no owning job allowlist)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    _make_artifact_commit(fx, "evidence/unknown/stray.txt", None)  # next commit includes unknown path
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    head = git(repo, "rev-parse", "origin/ops/automation").strip()
    with pytest.raises(ValueError, match="no owning job allowlist"):
        generate_promotion_manifest.generate_manifest(repo, base, head, fetch=False)


def test_m4_ambiguous_ownership_fail_closed(fx, monkeypatch):
    """One path matching TWO allowlists (synthetic config) -> FAIL CLOSED ambiguous."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    head = git(repo, "rev-parse", "origin/ops/automation").strip()
    # synthetic: make MIDWEEK also match the weekly radar-digest pattern
    monkeypatch.setattr(ops_config, "JOB_ALLOWLISTS", dict(ops_config.JOB_ALLOWLISTS))
    ops_config.JOB_ALLOWLISTS[MIDWEEK] = ops_config.JOB_ALLOWLISTS[WEEKLY]
    monkeypatch.setattr(ops_config, "_COMPILED_ALLOW", {
        jid: [re.compile(p) for p in pats] for jid, pats in ops_config.JOB_ALLOWLISTS.items()
    })
    with pytest.raises(ValueError, match="ambiguous ownership"):
        generate_promotion_manifest.generate_manifest(repo, base, head, fetch=False)


def test_m5_deletion_in_range_fails(fx):
    """Deletion in base..head -> FAIL (not promotable)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    git(fx["ops"], "rm", "evidence/radar/digests/2019-12-31-radar-digest.md")
    git(fx["ops"], "commit", "-m", "delete init digest")
    git(fx["ops"], "push", "origin", "ops/automation")
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    head = git(repo, "rev-parse", "origin/ops/automation").strip()
    with pytest.raises(ValueError, match="deletion"):
        generate_promotion_manifest.generate_manifest(repo, base, head, fetch=False)


def test_m6_rename_in_range_fails(fx):
    """Rename in base..head -> FAIL (not promotable)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    git(fx["ops"], "mv", "evidence/radar/digests/2019-12-31-radar-digest.md",
        "evidence/radar/digests/2020-01-02-radar-digest.md")
    git(fx["ops"], "commit", "-m", "rename init digest")
    git(fx["ops"], "push", "origin", "ops/automation")
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    head = git(repo, "rev-parse", "origin/ops/automation").strip()
    with pytest.raises(ValueError, match="rename"):
        generate_promotion_manifest.generate_manifest(repo, base, head, fetch=False)


def test_m8_manifest_frozen_despite_newer_ops_commits(fx):
    """Newer ops commits after the frozen manifest head -> manifest stays frozen."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head1 = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m1 = generate_promotion_manifest.generate_manifest(repo, base, head1, fetch=False)
    # newer ops commit AFTER the frozen head
    _make_artifact_commit(fx, "evidence/radar/digests/2026-09-24-radar-digest.md", head1)
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m2 = generate_promotion_manifest.generate_manifest(repo, base, head1, fetch=False)
    assert m1["manifest_ops_head_sha"] == head1 == m2["manifest_ops_head_sha"]
    assert m1["artifacts"] == m2["artifacts"]          # identical freeze
    assert m1["artifacts"][0]["source_commit"] == head1  # frozen, not the newer commit
    assert m2["artifacts"][0]["source_commit"] == head1


# ---- R0.1 §13 / §14 — last-promoted semantics + manifest residue ---------------

def test_canary_does_not_advance_last_promoted(fx):
    """Canary promotion (temp branch) must NOT advance last_promoted_ops_sha."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"],
                                      do_push=False, into_primary=False)
    assert res["ok"] is True
    assert "last_promoted_ops_sha" not in ops_config.load_state()


def test_real_p1_advances_last_promoted_and_removes_residue(fx):
    """Founder-approved REAL P1 (into_primary + push) advances last_promoted
    mechanically, clears the promotion-pending lock, and removes manifest residue
    (R0.1 §13/§14; R0.2 §3 into_primary MUST imply do_push — no local-only success)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    _pending_lock("p1-real")
    res = promote_batch.promote_batch(mp, "main", fx["canonical"], fx["ops"],
                                      do_push=True, into_primary=True)
    assert res["ok"] is True and res["remote_verified"] is True
    assert ops_config.load_state()["last_promoted_ops_sha"] == head
    assert "promotion_pending_manifest_id" not in ops_config.load_state()
    # artifact landed on governed main
    assert "evidence/radar/digests/2026-09-23-radar-digest.md" in \
        git(fx["canonical"], "ls-tree", "-r", "--name-only", "main").splitlines()
    # manifest residue removed from the automation working tree
    assert not mp.exists()


def test_promotion_owner_scope_never_widened(fx):
    """Multi-job ownership is per-artifact: a path owned by job A is rejected when
    the manifest claims job B (target-path authority is never widened by the batch)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["artifacts"][0]["job_id"] = AM  # tamper owner to a different job
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(m), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "owner"


def test_promotion_uses_real_source_commit_blob(fx):
    """Promotion verifies the blob at the artifact's REAL source commit (R0.1 §8/§12),
    not the batch head — for a range A->R(radar)->M(am), the radar blob is read at R."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    r = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _make_artifact_commit(fx, AM_REL, r)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    manifest = generate_promotion_manifest.generate_manifest(repo, base, m, fetch=False)
    mp = fx["ops"] / "m.json"; mp.write_text(json.dumps(manifest), encoding="utf-8")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is True
    assert res["promoted"] == ["evidence/radar/digests/2026-09-23-radar-digest.md", AM_REL]
    # both files present, both hashes intact on the target branch
    for art in manifest["artifacts"]:
        data = git_b(fx["canonical"], "show", f"wip/canary:{art['path']}")
        assert hashlib.sha256(data).hexdigest() == art["sha256"]


# ---- R0.2 P1 execution hardening RED diagnostics (POST-M5.3 O3 R0.2, 24 Sep 2026) ---
# The REAL P1 path must start from EXACT canonical main, require push, verify remote
# BEFORE advancing state, revalidate the entire frozen batch against the canonical
# delta, and enforce a mechanical promotion-pending lock. These tests demonstrate the
# R0.1 gaps BEFORE the runtime hardening (TDD RED). Contract: §15 P1-A..P1-G +
# recovery; §16 M9..M18. R0.1 T1-T7, M1-M8, S0-S3, G0 A-E must stay GREEN.

RADAR23 = "evidence/radar/digests/2026-09-23-radar-digest.md"
RADAR24 = "evidence/radar/digests/2026-09-24-radar-digest.md"


def _refresh_ops_ref(fx):
    git(str(fx["canonical"]), "fetch", "origin",
        "ops/automation:refs/remotes/origin/ops/automation")


def _pending_lock(state_val="p1-r02-00000000"):
    ops_config.save_state({**ops_config.load_state(),
                           "promotion_pending_manifest_id": state_val})


def _write_manifest(fx, m):
    mp = fx["ops"] / "m.json"
    mp.write_text(json.dumps(m), encoding="utf-8")
    return mp


def _real_p1_args(mp, fx):
    return dict(manifest_path=mp, target_branch="main", repo=str(fx["canonical"]),
                operations_worktree=str(fx["ops"]), do_push=True, into_primary=True)


def test_p1a_local_main_ahead_refuses(fx):
    """P1-1D: REAL P1 refuses BEFORE mutation when local primary main is AHEAD of
    origin/main (no merge/rebase/reset/auto-resolve)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    # local main advances WITHOUT push — origin/main still == manifest_main_sha
    write(fx["canonical"], "docs/unpushed.md", "x")
    git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "unpushed local commit")
    local_head = git(fx["canonical"], "rev-parse", "HEAD").strip()
    origin_before = git(fx["canonical"], "rev-parse", "origin/main").strip()
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "baseline"
    assert git(fx["canonical"], "rev-parse", "HEAD").strip() == local_head   # preserved
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == origin_before
    assert RADAR23 not in git(fx["canonical"], "ls-tree", "-r", "--name-only",
                              "main").splitlines()  # no promotion commit


def test_p1b_dirty_main_refuses(fx):
    """P1-1C: REAL P1 refuses when the primary main worktree is dirty (staged/
    unstaged/untracked) — FAIL CLOSED, never reset/clean."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    write(fx["canonical"], "evidence/unstaged.tmp", "x")   # untracked residue
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "dirty"
    assert ops_git.porcelain(fx["canonical"])               # preserved untouched


def test_p1c_into_primary_requires_push(fx):
    """P1-2: into_primary=True MUST imply do_push=True — the invalid combination
    fails BEFORE writing any artifact."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "main", fx["canonical"], fx["ops"],
                                      do_push=False, into_primary=True)
    assert res["ok"] is False and res["stage"] == "contract"
    assert RADAR23 not in git(fx["canonical"], "ls-tree", "-r", "--name-only",
                              "main").splitlines()    # main untouched


def test_p1d_into_primary_target_must_be_main(fx):
    """P1-3: into_primary is reserved exclusively for target_branch == 'main'."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"],
                                      do_push=True, into_primary=True)
    assert res["ok"] is False and res["stage"] == "target"


def test_p1e_into_primary_verify_only_refused(fx):
    """P1-6: into_primary + verify_only is invalid and must never dirty main."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "main", fx["canonical"], fx["ops"],
                                      do_push=True, into_primary=True, verify_only=True)
    assert res["ok"] is False and res["stage"] == "contract"
    assert not ops_git.porcelain(fx["canonical"])           # main stays pristine


def test_p1f_push_failure_preserves_commit_and_state(fx, monkeypatch):
    """P1-13: real-P1 push failure -> P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY:
    local promotion commit PRESERVED, origin/main unchanged, last_promoted NOT
    advanced, manifest preserved — no reset/discard."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    real_run = ops_git.run_git

    def fake_run(cwd, *args, **kw):
        if args and args[0] == "push" and "origin" in args:
            raise ops_git.OpsGitError("simulated network push failure")
        return real_run(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", fake_run)
    origin_before = git(fx["canonical"], "rev-parse", "origin/main").strip()
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False
    assert res.get("pending_state") == "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == origin_before
    assert ops_config.load_state().get("last_promoted_ops_sha") != head  # NOT advanced
    assert mp.exists()                                                   # manifest preserved
    # the local promotion commit is PRESERVED (HEAD advanced once; never reset)
    assert git(fx["canonical"], "rev-parse", "HEAD").strip() == res["commit"]


def test_p1_failure_recovery_exact_push(fx, monkeypatch):
    """P1-13 recovery tool: verify local commit parent == manifest_main_sha and
    artifact hashes == manifest, then retry the EXACT push. No reset."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    real_run = ops_git.run_git
    calls = {"n": 0}

    def fake_run(cwd, *args, **kw):
        if args and args[0] == "push" and "origin" in args and calls["n"] == 0:
            calls["n"] += 1
            raise ops_git.OpsGitError("simulated network push failure")
        return real_run(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", fake_run)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res.get("pending_state") == "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
    rec = promote_batch.recover_local_promotion(mp, str(fx["canonical"]), str(fx["ops"]))
    assert rec["ok"] is True
    assert rec["commit"] == res["commit"]
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == rec["commit"]
    assert ops_config.load_state()["last_promoted_ops_sha"] == m["manifest_ops_head_sha"]
    assert "promotion_pending_manifest_id" not in ops_config.load_state()
    assert not mp.exists()


def test_p1g_success_remote_verified_then_state_advances(fx):
    """P1-4 order: real P1 success = remote verified FIRST, THEN last_promoted
    advances, THEN lock cleared + residue removed. Lock is SET during promotion."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    _pending_lock("p1-g")
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is True
    assert res["remote_verified"] is True
    assert git(fx["canonical"], "rev-parse", "origin/main").strip() == res["commit"]
    assert ops_config.load_state()["last_promoted_ops_sha"] == m["manifest_ops_head_sha"]
    assert "promotion_pending_manifest_id" not in ops_config.load_state()  # lock cleared
    assert not mp.exists()                                                  # residue removed


def test_m9_production_manifest_uses_canonical_refs(fx):
    """P1-4/M9: production manifest derives the range MECHANICALLY from
    origin/main -> origin/ops/automation — no caller-selected refs."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    repo = str(fx["canonical"])
    _refresh_ops_ref(fx)
    m = generate_promotion_manifest.generate_manifest(repo, fetch=False)
    assert m["manifest_main_sha"] == git(repo, "rev-parse", "origin/main").strip()
    assert m["manifest_ops_head_sha"] == git(repo, "rev-parse", "origin/ops/automation").strip()
    assert m["batch_base_sha"] == m["manifest_main_sha"]
    a = m["artifacts"][0]
    assert a["path"] == RADAR23 and a["source_commit"] == head


def test_m10_caller_range_must_equal_canonical(fx):
    """M10: caller-supplied refs MUST equal the mechanically derived canonical refs."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    repo = str(fx["canonical"])
    _refresh_ops_ref(fx)
    with pytest.raises(ValueError, match="origin/main"):
        generate_promotion_manifest.generate_manifest(repo, manifest_main_sha=head, fetch=False)


def test_m11_ops_head_outside_lineage_holds(fx):
    """M11: manifest ops head no longer in canonical origin/ops lineage -> HOLD."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    # sever the lineage: force-push canonical main (init) over ops/automation
    git(fx["canonical"], "push", "--force", "origin", "main:refs/heads/ops/automation")
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "frozen_lineage"


def test_m12_source_commit_outside_batch_holds(fx):
    """M12: source_commit outside the frozen batch (base commit, not in main..head)
    -> HOLD at promotion."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["artifacts"][0]["source_commit"] = git(fx["canonical"], "rev-parse", "HEAD").strip()  # init/base
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "source"


def test_m13_stale_source_commit_holds(fx):
    """M13: source_commit is not the LATEST path-touch in the frozen range -> HOLD."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    write(fx["ops"], RADAR23, "v1"); git(fx["ops"], "add", "--", RADAR23)
    git(fx["ops"], "commit", "-m", "r1"); git(fx["ops"], "push", "origin", "ops/automation")
    r1 = git(fx["ops"], "rev-parse", "HEAD").strip()
    write(fx["ops"], RADAR23, "v2"); git(fx["ops"], "add", "--", RADAR23)
    git(fx["ops"], "commit", "-m", "r2"); git(fx["ops"], "push", "origin", "ops/automation")
    r2 = git(fx["ops"], "rev-parse", "HEAD").strip()
    m = _manifest_for(fx, WEEKLY, r2, base)          # generator says latest touch = r2
    assert m["artifacts"][0]["source_commit"] == r2
    m["artifacts"][0]["source_commit"] = r1          # stale claim
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "source"


def test_m14_manifest_subset_omission_holds(fx):
    """M14: manifest artifact set must EQUAL the canonical batch delta — dropping
    one artifact (Founder approval = the exact deterministic batch) -> HOLD."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    r = _make_artifact_commit(fx, RADAR23, base)
    h = _make_artifact_commit(fx, AM_REL, r)
    repo = str(fx["canonical"]); _refresh_ops_ref(fx)
    m = generate_promotion_manifest.generate_manifest(repo, base, h,
                                                      expected_jobs=[WEEKLY, AM], fetch=False)
    m["artifacts"] = [a for a in m["artifacts"] if a["job_id"] != AM]   # omitted artifact
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "delta"


def test_m15_manifest_adds_foreign_artifact_holds(fx):
    """M15: manifest adds an artifact NOT in the canonical delta -> HOLD."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["artifacts"].append({"path": RADAR24, "job_id": WEEKLY,
                           "source_commit": head, "sha256": "0" * 64})
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"], do_push=False)
    assert res["ok"] is False and res["stage"] == "delta"


def test_m16_governance_between_batches_delta_only_unpromoted(fx):
    """M16: a governed main commit between batches + main->ops sync must NOT fail;
    the new canonical delta contains ONLY currently-unpromoted ops artifacts."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    _make_artifact_commit(fx, RADAR23, base)             # batch-1 ops artifact
    # governed main commit arrives between batches
    write(fx["canonical"], "docs/gov.md", "x"); git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "governed docs commit")
    git(fx["canonical"], "push", "origin", "main")
    # main -> ops sync (S3 clean merge in the ops worktree, exactly the sync helper)
    git(fx["ops"], "fetch", "origin", "main:refs/remotes/origin/main")
    git(fx["ops"], "merge", "origin/main", "-m", "sync main into ops")
    git(fx["ops"], "push", "origin", "ops/automation")
    repo = str(fx["canonical"]); git(repo, "fetch", "origin")
    m = generate_promotion_manifest.generate_manifest(repo, fetch=False)   # MECHANICAL
    assert m["manifest_main_sha"] == git(repo, "rev-parse", "origin/main").strip()
    assert m["batch_base_sha"] == m["manifest_main_sha"]
    assert [a["path"] for a in m["artifacts"]] == [RADAR23]  # ONLY the unpromoted artifact


def test_m17_promotion_pending_blocks_preflight(fx):
    """M17: promotion_pending_manifest_id set -> G0 preflight refuses new jobs
    (FAIL CLOSED; mechanical, not merely procedural)."""
    _pending_lock("p1-x")
    res = g0_check.g0_check(fx["ops"], fx["canonical"])
    assert res["ok"] is False and res["case"] == "PENDING"


def test_m18_successful_p1_clears_promotion_pending(fx):
    """M18: a successful verified REAL P1 clears promotion_pending_manifest_id."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    mp = _write_manifest(fx, m)
    _pending_lock("p1-m18")
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is True
    assert "promotion_pending_manifest_id" not in ops_config.load_state()


# footer: 2026-09-24 13:30 UTC+7 (R0.2 P1-execution-hardening RED diagnostics)

