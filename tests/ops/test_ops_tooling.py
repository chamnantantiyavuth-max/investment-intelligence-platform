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
    monkeypatch.setenv("OPS_STATE_DIR", str(tmp_path / "state"))   # per-test state isolation
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


def _manifest_for(fx, job, head=None, base=None):
    repo, ops = str(fx["canonical"]), fx["ops"]
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    # R0.2 §8: batch range is MECHANICAL (origin/main -> origin/ops/automation);
    # in the fixtures the caller's base/head equal the derived refs.
    m = generate_promotion_manifest.generate_manifest(repo, expected_jobs=[job], fetch=False)
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
    # single manifest over the canonical A..M batch covering BOTH artifact classes
    manifest = generate_promotion_manifest.generate_manifest(repo, fetch=False)
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
    manifest = generate_promotion_manifest.generate_manifest(repo, fetch=False)
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
    manifest = generate_promotion_manifest.generate_manifest(repo, fetch=False)
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
        generate_promotion_manifest.generate_manifest(repo, fetch=False)


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
        generate_promotion_manifest.generate_manifest(repo, fetch=False)


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
        generate_promotion_manifest.generate_manifest(repo, fetch=False)


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
        generate_promotion_manifest.generate_manifest(repo, fetch=False)


def test_m8_manifest_frozen_despite_newer_ops_commits(fx):
    """Newer ops commits AFTER the frozen manifest head: the FROZEN manifest stays
    exactly as generated (freeze point, R0.2 §10); a later generation is a NEW
    batch over the newer canonical delta."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head1 = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m1 = generate_promotion_manifest.generate_manifest(repo, fetch=False)  # frozen at head1
    assert m1["manifest_ops_head_sha"] == head1
    frozen_artifacts = m1["artifacts"]
    # newer ops commit AFTER the freeze
    _make_artifact_commit(fx, "evidence/radar/digests/2026-09-24-radar-digest.md", head1)
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    # the frozen manifest object is stable — never mutated by newer ops
    assert m1["manifest_ops_head_sha"] == head1
    assert m1["artifacts"] == frozen_artifacts
    assert m1["artifacts"][0]["source_commit"] == head1
    # a NEW generation is a NEW batch over the newer canonical delta
    m2 = generate_promotion_manifest.generate_manifest(repo, fetch=False)
    assert m2["manifest_ops_head_sha"] != head1
    assert {a["path"] for a in m2["artifacts"]} == {
        "evidence/radar/digests/2026-09-23-radar-digest.md",
        "evidence/radar/digests/2026-09-24-radar-digest.md"}


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
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))   # R0.3 §2/§3: APPROVED + digest receipt
    mp = _write_manifest(fx, m)
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
    assert res["ok"] is False and res["stage"] == "owner_mismatch"  # R0.3 §8: unique owner re-derived


def test_promotion_uses_real_source_commit_blob(fx):
    """Promotion verifies the blob at the artifact's REAL source commit (R0.1 §8/§12),
    not the batch head — for a range A->R(radar)->M(am), the radar blob is read at R."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    r = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m = _make_artifact_commit(fx, AM_REL, r)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    manifest = generate_promotion_manifest.generate_manifest(repo, fetch=False)
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
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))   # R0.3: approval binding
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
    # R0.3 §9: the push failure RECORDS the exact recovery identity — id + digest
    # + local commit — so recovery never infers identity from HEAD alone
    st = ops_config.load_state()
    assert st.get("pending_p1_manifest_id") == m["manifest_id"]
    assert st.get("pending_p1_manifest_sha256") == _manifest_digest(m)
    assert st.get("pending_p1_local_commit_sha") == res["commit"]


def test_p1_failure_recovery_exact_push(fx, monkeypatch):
    """P1-13 recovery tool: verify local commit parent == manifest_main_sha and
    artifact hashes == manifest, then retry the EXACT push. No reset."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))   # R0.3: approval binding
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
    st = ops_config.load_state()
    assert "promotion_pending_manifest_id" not in st
    assert "approved_manifest_id" not in st
    assert "pending_p1_local_commit_sha" not in st
    assert not mp.exists()


def test_p1g_success_remote_verified_then_state_advances(fx):
    """P1-4 order: real P1 success = remote verified FIRST, THEN last_promoted
    advances, THEN lock cleared + residue removed. Lock is SET during promotion."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))   # R0.3: approval binding
    mp = _write_manifest(fx, m)
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
    m = generate_promotion_manifest.generate_manifest(repo, expected_jobs=[WEEKLY, AM], fetch=False)
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
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))   # R0.3: approval binding
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is True
    st = ops_config.load_state()
    assert "promotion_pending_manifest_id" not in st
    assert "approved_manifest_id" not in st          # exact receipt also cleared
    assert "pending_p1_local_commit_sha" not in st


# =====================================================================
# R0.3 RED diagnostics — bounded P1 governance/atomicity hardening
# (POST-M5.3 O3 R0.3, FD #142 conformance, NO new FD)
#
# The real P1 path must: enforce Founder approval BOUND TO THE EXACT
# manifest digest (R0.3 §2/§3), validate the ENTIRE batch with zero
# primary mutation before writing anything (§4/§5 two-phase), fail
# closed on corrupt ops state (§6), persist state atomically (§7),
# re-derive the unique owner at consumption (§8), verify the exact
# preserved-commit delta before recovery push (§9), verify the new
# commit's exactness before push (§10), reject duplicate manifest
# paths (§11), verify batch_base_sha == manifest_main_sha (§12), and
# require the pending/approval identity to match EXACTLY (§13).
# =====================================================================


def _manifest_digest(m):
    """Deterministic immutable payload digest (R0.3 §3): manifest identity +
    batch range + exact ordered artifact entries + changed_jobs. Mutable
    review fields (disposition/approval/review notes) are EXCLUDED."""
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


def _approve(fx, m):
    """Founder-approval binding (R0.3 §2/§3): disposition APPROVED + pending
    lock == manifest_id + digest-bound receipt in ops-state. Mechanical —
    approval applies to ONE exact deterministic batch."""
    m["disposition"] = "APPROVED"
    _pending_lock(m["manifest_id"])
    ops_config.save_state({**ops_config.load_state(),
                           "approved_manifest_id": m["manifest_id"],
                           "approved_manifest_sha256": _manifest_digest(m)})
    return m


def _assert_main_pristine(fx, manifest):
    repo = str(fx["canonical"])
    assert git(repo, "status", "--porcelain") == ""
    assert git(repo, "diff", "--cached", "--name-only") == ""
    assert git(repo, "rev-parse", "HEAD").strip() == manifest["manifest_main_sha"]
    assert git(repo, "rev-parse", "origin/main").strip() == manifest["manifest_main_sha"]
    for a in manifest["artifacts"]:
        assert not (fx["canonical"] / a["path"]).exists()


def test_r3a_awaiting_approval_refuses(fx):
    """R3-A: disposition AWAITING_FOUNDER_APPROVAL -> REAL P1 FAILS 'approval'
    BEFORE any mutation (R0.3 §2) — main pristine."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    assert m["disposition"] == "AWAITING_FOUNDER_APPROVAL"
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "approval"
    _assert_main_pristine(fx, m)


def test_r3b_rejected_manifest_refuses(fx):
    """R3-B: disposition REJECTED -> REAL P1 FAILS 'approval' (R0.3 §2)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["disposition"] = "REJECTED"
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "approval"
    _assert_main_pristine(fx, m)


def test_r3c_approved_string_without_receipt_refuses(fx):
    """R3-C: disposition=APPROVED but NO matching external approval receipt in
    ops-state -> real P1 FAILS 'approval' (R0.3 §3 — mutable string alone is
    never sufficient)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["disposition"] = "APPROVED"
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "approval"
    _assert_main_pristine(fx, m)


def test_r3d_receipt_digest_mismatch_refuses(fx):
    """R3-D: external receipt exists but approved_manifest_sha256 != recomputed
    immutable digest -> real P1 FAILS 'approval' (R0.3 §3 — digest-bound)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["disposition"] = "APPROVED"
    _pending_lock(m["manifest_id"])
    ops_config.save_state({**ops_config.load_state(),
                           "approved_manifest_id": m["manifest_id"],
                           "approved_manifest_sha256": "0" * 64})
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "approval"
    _assert_main_pristine(fx, m)


def test_r3e_pending_id_mismatch_refuses(fx):
    """R3-E: promotion_pending_manifest_id != supplied manifest id -> real P1
    FAILS 'pending' (R0.3 §13 — one manifest can never promote/clear another)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["disposition"] = "APPROVED"
    _pending_lock("p1-OTHER-MANIFEST")
    ops_config.save_state({**ops_config.load_state(),
                           "approved_manifest_id": m["manifest_id"],
                           "approved_manifest_sha256": _manifest_digest(m)})
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "pending"
    _assert_main_pristine(fx, m)


def test_a1_late_bad_hash_zero_mutation(fx):
    """A1: artifact 1 valid + artifact 2 bad hash -> FAIL with ZERO primary
    mutation: main worktree clean, artifact 1 NOT written, HEAD/index/origin
    unchanged (R0.3 §4/§5 two-phase)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    h1 = _make_artifact_commit(fx, AM_REL, base)
    _make_artifact_commit(fx, RADAR23, h1)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m = generate_promotion_manifest.generate_manifest(
        repo, expected_jobs=[WEEKLY, AM], fetch=False)
    m["artifacts"][1]["sha256"] = "0" * 64                # late bad hash
    _approve(fx, m)                                       # approval binds the EXACT file
    a0 = m["artifacts"][0]                                # AM first (sorted) — the valid one
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False  # stage: hash (or earlier) — zero mutation either way
    _assert_main_pristine(fx, m)
    assert a0["path"] not in git(repo, "ls-tree", "-r", "--name-only", "main").splitlines()


def test_a2_late_invalid_owner_zero_mutation(fx):
    """A2: artifact 1 valid + artifact 2 invalid owner -> zero primary mutation
    (R0.3 §4/§5)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    h1 = _make_artifact_commit(fx, AM_REL, base)
    _make_artifact_commit(fx, RADAR23, h1)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m = generate_promotion_manifest.generate_manifest(
        repo, expected_jobs=[WEEKLY, AM], fetch=False)
    m["artifacts"][1]["job_id"] = "1f5f03f9236d"          # observer job: owns nothing
    _approve(fx, m)
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False
    _assert_main_pristine(fx, m)


def test_a3_late_invalid_source_zero_mutation(fx):
    """A3: artifact 1 valid + artifact 2 invalid source_commit -> zero primary
    mutation (R0.3 §4/§5)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    h1 = _make_artifact_commit(fx, AM_REL, base)
    _make_artifact_commit(fx, RADAR23, h1)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m = generate_promotion_manifest.generate_manifest(
        repo, expected_jobs=[WEEKLY, AM], fetch=False)
    m["artifacts"][1]["source_commit"] = base            # outside the frozen batch
    _approve(fx, m)
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False
    _assert_main_pristine(fx, m)


def test_a4_late_denylisted_zero_mutation(fx, monkeypatch):
    """A4: artifact 1 valid + artifact 2 denied by CURRENT denylist config at
    promotion time (config changed after generation) -> zero primary mutation
    (R0.3 §4/§5)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    h1 = _make_artifact_commit(fx, AM_REL, base)
    _make_artifact_commit(fx, RADAR23, h1)
    repo = str(fx["canonical"])
    git(repo, "fetch", "origin", "ops/automation:refs/remotes/origin/ops/automation")
    m = _approve(fx, generate_promotion_manifest.generate_manifest(
        repo, expected_jobs=[WEEKLY, AM], fetch=False))
    mp = _write_manifest(fx, m)
    # denylist gains the radar-digest path AFTER generation (exact fullmatch —
    # ops_config deny semantics are anchored fullmatch, not prefixes)
    extra = r"^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-digest\.md$"
    monkeypatch.setattr(ops_config, "DENYLIST_PATTERNS",
                        ops_config.DENYLIST_PATTERNS + [extra])
    monkeypatch.setattr(ops_config, "_COMPILED_DENY",
                        [re.compile(p) for p in ops_config.DENYLIST_PATTERNS + [extra]])
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False
    _assert_main_pristine(fx, m)


def test_r3h_corrupt_state_fails_closed(fx):
    """R3-H: corrupt ops-state JSON -> G0 FAIL CLOSED (STATE_CORRUPT), manifest
    generation HOLD, real P1 HOLD. NEVER interpret corrupt state as 'no lock'."""
    st = ops_config.state_dir() / "ops-state.json"
    st.parent.mkdir(parents=True, exist_ok=True)
    orig = ops_config.load_state()
    try:
        # approval binding recorded while state is VALID (generation needs a
        # readable state), THEN the state file is corrupted
        base = git(fx["ops"], "rev-parse", "HEAD").strip()
        head = _make_artifact_commit(fx, RADAR23, base)
        m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
        mp = _write_manifest(fx, m)
        repo = str(fx["canonical"])
        st.write_text("{not valid json", encoding="utf-8")
        # G0 preflight FAILS CLOSED
        res = g0_check.g0_check(fx["ops"], fx["canonical"])
        assert res["ok"] is False and res["case"] == "STATE_CORRUPT"
        # manifest generation HOLDS
        with pytest.raises(ValueError, match="HOLD"):
            generate_promotion_manifest.generate_manifest(repo, fetch=False)
        # real P1 HOLDS before any mutation
        res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
        assert res["ok"] is False and res["stage"] == "state_corrupt"
        _assert_main_pristine(fx, m)
    finally:
        ops_config.save_state(orig)


def test_r3i_state_write_interrupted_preserves_previous(fx, monkeypatch):
    """R3-I: state write interrupted at the atomic-replace step -> previous
    valid state preserved and readable; never partial/truncated authoritative
    state (R0.3 §7)."""
    ops_config.save_state({"promotion_pending_manifest_id": "p1-old",
                           "last_promoted_ops_sha": "a" * 40})
    def boom(src, dst):
        raise OSError("simulated replace failure")
    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError):
        ops_config.save_state({"promotion_pending_manifest_id": "p1-new"})
    st = ops_config.load_state()
    assert st.get("promotion_pending_manifest_id") == "p1-old"
    assert st.get("last_promoted_ops_sha") == "a" * 40


def test_r3j_owner_ambiguity_derived_at_consumption(fx, monkeypatch):
    """R3-J: owner re-derived MECHANICALLY at promotion time (R0.3 §8): path
    becomes ambiguous AFTER manifest generation -> HOLD, main pristine; unique
    owner changes -> owner_mismatch; owner removed -> owner."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    # path becomes ambiguous: MIDWEEK now also owns the digest path
    monkeypatch.setattr(
        ops_config, "JOB_ALLOWLISTS",
        {**ops_config.JOB_ALLOWLISTS,
         MIDWEEK: [r"^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-digest\.md$"]})
    monkeypatch.setattr(ops_config, "_COMPILED_ALLOW",
                        {jid: [re.compile(p) for p in pats]
                         for jid, pats in ops_config.JOB_ALLOWLISTS.items()})
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "owner_ambiguous"
    _assert_main_pristine(fx, m)


def test_r3k_recovery_rejects_extra_path(fx, monkeypatch):
    """R3-K: recovery must refuse when the preserved local promote commit delta
    contains an extra file (exact path-set + hashes verified BEFORE exact push,
    R0.3 §9) — no push, origin/main unchanged."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    repo, real = str(fx["canonical"]), ops_git.run_git
    calls = {"n": 0}
    def fail_once(cwd, *args, **kw):
        if args and args[0] == "push":
            calls["n"] += 1
            if calls["n"] == 1:
                raise ops_git.OpsGitError("push refused (simulated)")
        return real(cwd, *args, **kw)
    monkeypatch.setattr(ops_git, "run_git", fail_once)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)   # restore runner ONLY — never
    # monkeypatch.undo(), which would also revert the fx fixture's OPS_STATE_DIR/HOME
    assert res["ok"] is False
    assert res["pending_state"] == "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
    # someone amends an EXTRA file into the preserved promotion commit
    write(fx["canonical"], "docs/extra-recovery.md", "x")
    git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "--amend", "--no-edit")
    r2 = promote_batch.recover_local_promotion(mp, str(fx["canonical"]), str(fx["ops"]))
    assert r2["ok"] is False
    assert git(repo, "rev-parse", "origin/main").strip() == m["manifest_main_sha"]


def test_r3l_exact_recovery_succeeds(fx, monkeypatch):
    """R3-L: recovery succeeds ONLY when the recorded pending identity matches
    (id + digest + local commit) AND the preserved commit delta is EXACT
    (path set + hashes) (R0.3 §9) — advances last_promoted, clears locks,
    removes residue."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    repo, real = str(fx["canonical"]), ops_git.run_git
    calls = {"n": 0}
    def fail_once(cwd, *args, **kw):
        if args and args[0] == "push":
            calls["n"] += 1
            if calls["n"] == 1:
                raise ops_git.OpsGitError("push refused (simulated)")
        return real(cwd, *args, **kw)
    monkeypatch.setattr(ops_git, "run_git", fail_once)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)   # scoped restore — NEVER full undo
    assert res["ok"] is False and res["commit"]
    # recorded recovery identity (R0.3 §9) — written by the corrected impl on
    # push failure; set explicitly here so the test pins the exact contract
    ops_config.save_state({**ops_config.load_state(),
                           "pending_p1_manifest_id": m["manifest_id"],
                           "pending_p1_manifest_sha256": _manifest_digest(m),
                           "pending_p1_local_commit_sha": res["commit"]})
    r2 = promote_batch.recover_local_promotion(mp, str(fx["canonical"]), str(fx["ops"]))
    assert r2["ok"] is True and r2["remote_verified"] is True
    assert r2["last_promoted_ops_sha"] == m["manifest_ops_head_sha"]
    st = ops_config.load_state()
    assert st.get("last_promoted_ops_sha") == m["manifest_ops_head_sha"]
    assert "promotion_pending_manifest_id" not in st
    assert "approved_manifest_id" not in st
    assert "pending_p1_local_commit_sha" not in st
    assert not mp.exists()          # residue removed
    assert git(repo, "rev-parse", "origin/main").strip() == res["commit"]


def test_r3m_post_commit_extra_path_refuses_push(fx, monkeypatch):
    """R3-M: unexpected commit delta (hook/index mutation between staged-set
    check and commit) adds an extra path -> normal real P1 refuses BEFORE push
    (R0.3 §10); local commit preserved, origin/main unchanged."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    repo, real = str(fx["canonical"]), ops_git.run_git
    def inject(cwd, *args, **kw):
        if args and args[0] == "commit":
            extra = Path(cwd) / "docs/injected.md"
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text("hook injected", encoding="utf-8")
            real(cwd, "add", "--", "docs/injected.md")
        return real(cwd, *args, **kw)
    monkeypatch.setattr(ops_git, "run_git", inject)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)   # scoped restore — NEVER full undo
    assert res["ok"] is False and res["stage"] == "post_commit"
    assert git(repo, "rev-parse", "origin/main").strip() == m["manifest_main_sha"]
    assert res["commit"] and git(repo, "rev-parse", "HEAD").strip() == res["commit"]


def test_r3n_duplicate_path_fails(fx):
    """R3-N: duplicate artifact path entries -> FAIL CLOSED 'manifest'
    (len(list) != len(set)); duplicates must never collapse silently (R0.3 §11)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["artifacts"].append(dict(m["artifacts"][0]))
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"],
                                      do_push=False)
    assert res["ok"] is False and res["stage"] == "manifest"
    assert mp.exists()          # interactive review manifest never deleted by a canary


def test_r3o_batch_base_mismatch_fails(fx):
    """R3-O: batch_base_sha != manifest_main_sha -> FAIL CLOSED 'manifest'
    (internally contradictory provenance fields not retained, R0.3 §12)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    m["batch_base_sha"] = "0" * 40
    mp = _write_manifest(fx, m)
    res = promote_batch.promote_batch(mp, "wip/canary", fx["canonical"], fx["ops"],
                                      do_push=False)
    assert res["ok"] is False and res["stage"] == "manifest"
    assert mp.exists()


# =====================================================================
# R0.4 RED diagnostics — final bounded P1 crash-consistency/disposition
# (POST-M5.3 O3 R0.4, FD #142 conformance, NO new FD)
#
# R0.3 RETAINED. R0.4 covers ONLY: (1) mandatory pending identity,
# (2) approved-manifest cancellation, (3) short-write-safe state persistence,
# (4) remote-success/acknowledgement-loss reconciliation, (5) single atomic
# promotion-state transition. All must demonstrate RED on canonical 2d44d7e.
# =====================================================================

def test_r4a_missing_pending_refuses(fx):
    """R4-A: valid APPROVED manifest + matching receipt but NO pending lock ->
    real P1 FAILS 'pending', zero primary mutation. There is NO valid real-P1
    state with an absent pending lock (R0.4 §2)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    # remove the whole pending tuple (id + digest) — approval receipt stays
    st = ops_config.load_state()
    st.pop("promotion_pending_manifest_id", None)
    st.pop("promotion_pending_manifest_sha256", None)
    ops_config.save_state(st)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    assert res["ok"] is False and res["stage"] == "pending"
    _assert_main_pristine(fx, m)


def test_r4b1_approved_exact_cancellation_succeeds(fx):
    """R4-B1: approved receipt exists + disposition CANCELLED + exact id/digest
    -> cancellation succeeds; ONE atomic transition clears ONLY the pending pair
    and the approval pair (R0.4 §3/§7)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    m["disposition"] = "CANCELLED"
    mp = _write_manifest(fx, m)
    res = generate_promotion_manifest.cancel_manifest(mp)
    assert res["ok"] is True, res
    st = ops_config.load_state()
    assert "promotion_pending_manifest_id" not in st
    assert "promotion_pending_manifest_sha256" not in st
    assert "approved_manifest_id" not in st
    assert "approved_manifest_sha256" not in st
    assert "pending_p1_local_commit_sha" not in st


def test_r4b2_cancellation_digest_mismatch_refuses(fx):
    """R4-B2: same manifest id but ALTERED immutable digest -> cancellation
    refuses; pending + approval state untouched (R0.4 §3)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    m["disposition"] = "CANCELLED"
    m["artifacts"][0]["sha256"] = "0" * 64           # tamper -> different digest
    mp = _write_manifest(fx, m)
    res = generate_promotion_manifest.cancel_manifest(mp)
    assert res["ok"] is False and res["stage"] == "pending"
    st = ops_config.load_state()
    assert st.get("promotion_pending_manifest_id") == m["manifest_id"]
    assert st.get("approved_manifest_id") == m["manifest_id"]


def test_r4b3_foreign_pending_cancellation_refuses(fx):
    """R4-B3: pending lock belongs to a DIFFERENT manifest -> cancellation
    refuses (one manifest never cancels another) (R0.4 §3)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    h1 = _make_artifact_commit(fx, RADAR23, base)
    m1 = _approve(fx, _manifest_for(fx, WEEKLY, h1, base))     # pending = m1
    h2 = _make_artifact_commit(fx, AM_REL, h1)
    m2 = _manifest_for(fx, AM, h2, h1)                          # unapproved foreign
    mp2 = _write_manifest(fx, m2)
    res = generate_promotion_manifest.cancel_manifest(mp2)
    assert res["ok"] is False and res["stage"] == "pending"
    assert ops_config.promotion_pending() == m1["manifest_id"]  # unchanged


def test_r4b4_pending_recovery_cancellation_refuses(fx):
    """R4-B4: pending recovery record exists for the same manifest/digest ->
    ordinary cancellation REFUSES (must not destroy the preserved local P1
    commit); Founder recovery-disposition required (R0.4 §3)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    m["disposition"] = "CANCELLED"
    mp = _write_manifest(fx, m)
    st = ops_config.load_state()
    st.update({"pending_p1_manifest_id": m["manifest_id"],
               "pending_p1_manifest_sha256": _manifest_digest(m),
               "pending_p1_local_commit_sha": "1" * 40})
    ops_config.save_state(st)
    res = generate_promotion_manifest.cancel_manifest(mp)
    assert res["ok"] is False and res["stage"] == "recovery"
    st = ops_config.load_state()
    assert st.get("pending_p1_local_commit_sha") == "1" * 40    # commit NOT destroyed


def test_r4c_partial_write_cannot_corrupt_state(fx):
    """R4-C: OS short-write cannot replace authoritative state with partial
    JSON — the implementation must loop until the FULL payload is written, or
    fail BEFORE os.replace; the previous valid state stays authoritative."""
    real_write = os.write

    def short_write(fd, data):
        n = max(1, len(data) // 4)
        return real_write(fd, data[:n])

    monkeypatch.setattr(os, "write", short_write)
    ops_config.save_state({"promotion_pending_manifest_id": "p1-full",
                           "promotion_pending_manifest_sha256": "0" * 64})
    st = ops_config.load_state()          # must decode the FULL payload
    assert st.get("promotion_pending_manifest_id") == "p1-full"
    assert len(st.get("promotion_pending_manifest_sha256", "")) == 64


def test_r4d1_remote_accepted_push_reports_failure_reconciles(fx):
    """R4-D1: push ACTUALLY reaches remote P, then the client reports failure ->
    recovery detects origin/main == P, performs NO second push, and finalizes
    state exactly once (reconciled_remote_success) (R0.4 §5 CASE B)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    real = ops_git.run_git
    pushes = {"n": 0}

    def fail_after_accept(cwd, *args, **kw):
        if args and args[0] == "push":
            real(cwd, *args, **kw)        # remote accepts P
            pushes["n"] += 1
            raise ops_git.OpsGitError("push reported failure after remote accepted")
        return real(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", fail_after_accept)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)
    assert res["ok"] is False
    assert res["pending_state"] == "P1_LOCAL_COMMIT_PENDING_REMOTE_RECOVERY"
    assert res["commit"]
    rec = ops_config.pending_p1_record()
    assert rec["pending_p1_manifest_id"] == m["manifest_id"]
    assert rec["pending_p1_local_commit_sha"] == res["commit"]
    r2 = promote_batch.recover_local_promotion(mp, str(fx["canonical"]), str(fx["ops"]))
    assert r2["ok"] is True and r2.get("reconciled_remote_success") is True, r2
    assert pushes["n"] == 1               # NO second push during reconciliation
    st = ops_config.load_state()
    assert st.get("last_promoted_ops_sha") == m["manifest_ops_head_sha"]
    for k in ("promotion_pending_manifest_id", "promotion_pending_manifest_sha256",
              "approved_manifest_id", "approved_manifest_sha256",
              "pending_p1_manifest_id", "pending_p1_manifest_sha256",
              "pending_p1_local_commit_sha"):
        assert k not in st
    assert not mp.exists()


def test_r4d2_post_push_fetch_failure_reconciles(fx):
    """R4-D2: push succeeds but the post-push fetch fails -> later reconciliation
    detects origin/main == P and finalizes exactly once (R0.4 §5 CASE B)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    real = ops_git.run_git
    calls = {"fetch": 0, "push": 0}

    def flaky_fetch(cwd, *args, **kw):
        if args and args[0] == "fetch":
            if calls["fetch"] >= 1:
                raise ops_git.OpsGitError("post-push fetch failed")
            calls["fetch"] += 1
        if args and args[0] == "push":
            calls["push"] += 1
        return real(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", flaky_fetch)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)
    assert res["ok"] is False and res["commit"]
    assert calls["push"] == 1
    r2 = promote_batch.recover_local_promotion(mp, str(fx["canonical"]), str(fx["ops"]))
    assert r2["ok"] is True and r2.get("reconciled_remote_success") is True, r2
    assert calls["push"] == 1             # finalization only, NO duplicate push
    assert ops_config.load_state().get("last_promoted_ops_sha") == m["manifest_ops_head_sha"]
    assert not mp.exists()


def test_r4d3_remote_unrelated_sha_fails_closed(fx):
    """R4-D3: origin/main holds an arbitrary third SHA -> recovery FAILS CLOSED
    'main_moved'; no state clearing (R0.4 §5 CASE C)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    real = ops_git.run_git
    pushes = {"n": 0}

    def fail_before_send(cwd, *args, **kw):
        if args and args[0] == "push":
            pushes["n"] += 1
            raise ops_git.OpsGitError("push refused")
        return real(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", fail_before_send)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)
    assert res["ok"] is False and res["commit"]
    # origin/main moves to an UNRELATED SHA (neither base B nor promotion P)
    repo = str(fx["canonical"])
    write(repo, "docs/unrelated-r4d3.md", "x")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "unrelated main commit")
    git(repo, "push", "origin", "main")
    r2 = promote_batch.recover_local_promotion(mp, repo, str(fx["ops"]))
    assert r2["ok"] is False and r2["stage"] == "main_moved"
    st = ops_config.load_state()
    assert st.get("promotion_pending_manifest_id") == m["manifest_id"]
    assert st.get("approved_manifest_id") == m["manifest_id"]
    assert st.get("pending_p1_local_commit_sha") == res["commit"]  # nothing cleared


def test_r4e_recovery_identity_before_push(fx):
    """R4-E: the pending-P1 recovery identity is persisted BEFORE the real push
    is invoked (ack-loss safety) (R0.4 §6)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    real = ops_git.run_git
    seen = {}

    def snap_at_push(cwd, *args, **kw):
        if args and args[0] == "push":
            seen.update(ops_config.load_state())
        return real(cwd, *args, **kw)

    monkeypatch.setattr(ops_git, "run_git", snap_at_push)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_git, "run_git", real)
    assert res["ok"] is True, res
    assert seen.get("promotion_pending_manifest_id") == m["manifest_id"]
    assert seen.get("promotion_pending_manifest_sha256") == _manifest_digest(m)
    assert seen.get("approved_manifest_id") == m["manifest_id"]
    assert seen.get("pending_p1_manifest_id") == m["manifest_id"]
    assert seen.get("pending_p1_manifest_sha256") == _manifest_digest(m)
    assert seen.get("pending_p1_local_commit_sha") == res["commit"]


def test_r4f_single_atomic_final_transition(fx):
    """R4-F: the promotion final state transition is ONE atomic save carrying
    last_promoted_ops_sha AND the removal of ALL seven promotion-state keys in
    the SAME payload (R0.4 §7)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _approve(fx, _manifest_for(fx, WEEKLY, head, base))
    mp = _write_manifest(fx, m)
    saves = []
    real_save = ops_config.save_state

    def spy(state):
        saves.append(dict(state))
        return real_save(state)

    monkeypatch.setattr(ops_config, "save_state", spy)
    res = promote_batch.promote_batch(**_real_p1_args(mp, fx))
    monkeypatch.setattr(ops_config, "save_state", real_save)
    assert res["ok"] is True, res
    finals = [s for s in saves if "last_promoted_ops_sha" in s]
    assert len(finals) == 1
    st = finals[0]
    assert st["last_promoted_ops_sha"] == m["manifest_ops_head_sha"]
    for k in ("promotion_pending_manifest_id", "promotion_pending_manifest_sha256",
              "approved_manifest_id", "approved_manifest_sha256",
              "pending_p1_manifest_id", "pending_p1_manifest_sha256",
              "pending_p1_local_commit_sha"):
        assert k not in st


def test_r4g_partial_approval_tuple_fails_closed(fx):
    """R4-G: approved_manifest_id without approved_manifest_sha256 -> StateError /
    G0 STATE_CORRUPT (never treated as 'not approved') (R0.4 §8)."""
    st = ops_config.state_dir() / "ops-state.json"
    st.parent.mkdir(parents=True, exist_ok=True)
    st.write_text('{"approved_manifest_id": "p1-x"}', encoding="utf-8")
    with pytest.raises(ops_config.StateError):
        ops_config.load_state()
    res = g0_check.g0_check(fx["ops"], fx["canonical"])
    assert res["ok"] is False and res["case"] == "STATE_CORRUPT"


def test_r4h_partial_recovery_tuple_fails_closed(fx):
    """R4-H: pending_p1 partial tuple (id + commit, missing digest) -> StateError
    (R0.4 §8)."""
    st = ops_config.state_dir() / "ops-state.json"
    st.parent.mkdir(parents=True, exist_ok=True)
    st.write_text('{"pending_p1_manifest_id": "p1-x", '
                  '"pending_p1_local_commit_sha": "' + "1" * 40 + '"}',
                  encoding="utf-8")
    with pytest.raises(ops_config.StateError):
        ops_config.load_state()


def test_r4i_partial_pending_tuple_fails_closed(fx):
    """R4-I: promotion_pending_manifest_id without the pending digest ->
    StateError (R0.4 §8)."""
    st = ops_config.state_dir() / "ops-state.json"
    st.parent.mkdir(parents=True, exist_ok=True)
    st.write_text('{"promotion_pending_manifest_id": "p1-x"}', encoding="utf-8")
    with pytest.raises(ops_config.StateError):
        ops_config.load_state()


def test_r4j_manifest_write_failure_keeps_pending_lock(fx):
    """R4-J: a manifest-write failure can NEVER produce a review manifest
    without a conservative pending lock — the lock is persisted FIRST (R0.4 §9)."""
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, RADAR23, base)
    m = _manifest_for(fx, WEEKLY, head, base)
    # sabotage the manifests directory: a FILE in the way of the dir
    blocked = Path(fx["ops"]) / "ops" / "manifests"
    blocked.parent.mkdir(parents=True, exist_ok=True)
    blocked.write_text("not a directory", encoding="utf-8")
    with pytest.raises((OSError, FileExistsError)):
        generate_promotion_manifest.write_manifest(
            m, str(fx["canonical"]), str(fx["ops"]))
    # conservative lock MUST be set even though the manifest file could not be written
    assert ops_config.promotion_pending() == m["manifest_id"]
    assert ops_config.promotion_pending_digest() == _manifest_digest(m)


# footer: 2026-09-24 16:00 UTC+7 (R0.4 crash-consistency/disposition RED diagnostics)

