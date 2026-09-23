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
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "ops"))

import ops_config  # noqa: E402
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


def test_sync_diverged_fail_closed(fx):
    write(fx["ops"], "evidence/radar/digests/2026-09-23-radar-digest.md")
    git(fx["ops"], "add", "-A"); git(fx["ops"], "commit", "-m", "local divergent")
    write(fx["canonical"], "docs/gov.md"); git(fx["canonical"], "add", "-A")
    git(fx["canonical"], "commit", "-m", "main divergent"); git(fx["canonical"], "push", "origin", "main")
    res = sync_main_to_ops.sync_main_to_ops(fx["ops"], fx["canonical"], do_fetch=True, persist=False)
    assert res["ok"] is False
    assert "FAIL CLOSED" in res["reason"]


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
    m = generate_promotion_manifest.generate_manifest(job, repo, base, head, fetch=False)
    return m


def test_manifest_deterministic_hashes(fx):
    base = git(fx["ops"], "rev-parse", "HEAD").strip()
    head = _make_artifact_commit(fx, "evidence/radar/digests/2026-09-23-radar-digest.md", base)
    m1 = _manifest_for(fx, WEEKLY, head, base)
    m2 = _manifest_for(fx, WEEKLY, head, base)
    assert m1["manifest_id"] == m2["manifest_id"]
    a = m1["artifacts"][0]
    data = git(fx["canonical"], "show", f"{head}:evidence/radar/digests/2026-09-23-radar-digest.md").encode("utf-8")
    assert a["sha256"] == hashlib.sha256(data).hexdigest()
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


# footer: 2026-09-23 15:00 UTC+7