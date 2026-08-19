"""Locked acceptance tests — Audit API (FD #86, WS-3 — UI-4 Decision Register / Audit Center).

Charter:
  1. Route inventory  — /api/decisions, /api/audit/git-log, /api/audit/model-registry
                        return 401 without a session cookie (FD #46 auth boundary)
  2. /api/decisions   — 200 with auth; data_source = founders_decisions_register;
                        register is contiguous 1..N (currently 102 items); every
                        item has num/title/preview; latest items carry a 2026 date
  3. /api/audit/git-log — 200; data_source = git_history; commits non-empty with
                        hash/date/subject; corrections list non-empty (repo has
                        committed CORRECTIONS-RECORD.md files, §23.9)
  4. /api/audit/model-registry — 200; data_source = adapter_registry;
                        current_version == ADAPTER_VERSION (v5); versions dict
                        non-empty (v1..v5)
  5. Provenance       — data_source truthfulness per surface; audit endpoints
                        never claim domain state (shape contract only)

Environment isolation follows tests/locked/test_real_data_api.py: env vars
set BEFORE importing the app. Do NOT modify expected values without a Bible
quote or FD (Acceptance Lock Rule, FD-108).
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

# ── Environment isolation (MUST precede app import) ──────────────────────────
TEST_ROOT = Path(tempfile.mkdtemp(prefix="iip-fd86-audit-"))
os.environ["IIP_DB_PATH"] = str(TEST_ROOT / "iip.db")
os.environ["IIP_ARTIFACT_BASE"] = str(TEST_ROOT / "artifacts")
os.environ["IIP_AUTH_USER"] = "founder"
os.environ["IIP_AUTH_PASSWORD"] = "test-password-123"
os.environ["IIP_AUTH_SECRET"] = "y" * 40  # >=32 chars

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)


def _auth_headers() -> dict[str, str]:
    r = client.post("/api/auth/login", json={"username": "founder", "password": "test-password-123"})
    assert r.status_code == 200
    return {}


def test_audit_routes_require_auth():
    for path in ["/api/decisions", "/api/audit/git-log", "/api/audit/model-registry"]:
        r = client.get(path)
        assert r.status_code == 401, f"{path} must require auth (FD #46)"


def test_decisions_register_contiguous_and_parsed():
    _auth_headers()
    r = client.get("/api/decisions")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "founders_decisions_register"
    decisions = body["decisions"]
    # Contiguous register 1..N (currently 102 items — FD #86 register append)
    nums = [d["num"] for d in decisions]
    assert nums == list(range(1, len(nums) + 1)), "register must be contiguous 1..N"
    assert len(decisions) >= 100, "register must carry the full decision history"
    for d in decisions:
        assert d["num"] >= 1
        assert isinstance(d["title"], str) and d["title"].strip()
        assert isinstance(d["preview"], str) and d["preview"].strip()
    # Latest decisions carry a dated stamp (FD #131, 19 Aug 2026)
    latest = decisions[-1]
    assert latest["date"] == "19 Aug 2026", f"latest decision date {latest['date']!r}"


def test_git_log_and_corrections():
    _auth_headers()
    r = client.get("/api/audit/git-log")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "git_history"
    commits = body["commits"]
    assert len(commits) > 0, "repo has commit history"
    for c in commits:
        assert c["hash"] and c["date"] and c["subject"]
    # Repo carries committed §23.9 correction records (Apple, Silver, JNJ…)
    corrections = body["corrections"]
    assert len(corrections) > 0, "repo has committed CORRECTIONS-RECORD.md files"
    for c in corrections:
        assert c["path"].endswith("CORRECTIONS-RECORD.md")
        assert c["modified"] > 0


def test_model_registry_matches_adapter_version():
    _auth_headers()
    r = client.get("/api/audit/model-registry")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "adapter_registry"
    # Current version must match the live adapters module (v5 as of FD #57)
    from backend import adapters  # noqa: PLC0415

    assert body["current_version"] == adapters.ADAPTER_VERSION
    assert body["current_version"] == "v5"
    assert set(body["versions"].keys()) >= {"v1", "v2", "v3", "v4", "v5"}
    for v, h in body["versions"].items():
        assert len(h) == 64, f"registry {v} must store a sha-256 code hash"
