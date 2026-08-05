"""Locked acceptance tests — Org-Workflow Read-Only API (FD #55, UI-0).

Charter:
  1. Route inventory  — the 4 new /api/org-* + /api/research-artifacts* routes
                        return 401 without a session cookie (FD #46 auth boundary)
  2. /org-queue       — 200 with auth; data_source = org_workflow_kanban;
                        canonical 11 columns (KANBAN-CONTRACT §2); all 5 pilot
                        cards present with the mandatory card fields; holds join
                        (cleared holds attached, never in active_holds)
  3. /org-holds       — 200; HOLD-DATA-001 + HOLD-RISK-001 with issuer, reason,
                        remediation, clear_record (status CLEARED, honest)
  4. /research-artifacts — 200; registry contains the REAL CIW artifacts
                        (research-result.md v1, research-result-2.md v2) with
                        identity fields parsed from the artifact's own table
                        (research_id CRR-2026-0001/0002), plus challenge-review
                        and pilot artifacts; no invented fields
  5. Detail           — /research-artifacts/{id} returns markdown content;
                        unknown id -> 404; traversal guard blocks ".." paths
  6. Provenance       — data_source truthfulness per surface; org endpoints
                        never claim domain state (shape contract only)

Environment isolation follows tests/locked/test_real_data_api.py: env vars
set BEFORE importing the app. Org endpoints read committed repo files (not
IIP_ARTIFACT_BASE) — they are stable because the artifacts are committed.

Do NOT modify expected values without a Bible quote or FD (Acceptance Lock
Rule, FD-108).
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

# ── Environment isolation (MUST precede app import) ──────────────────────────
TEST_ROOT = Path(tempfile.mkdtemp(prefix="iip-fd55-test-"))
os.environ["IIP_DB_PATH"] = str(TEST_ROOT / "iip.db")
os.environ["IIP_ARTIFACT_BASE"] = str(TEST_ROOT / "artifacts")
os.environ["IIP_AUTH_USER"] = "founder"
os.environ["IIP_AUTH_PASSWORD"] = "test-password-123"
os.environ["IIP_AUTH_SECRET"] = "y" * 40  # >=32 chars

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)

ORG_ENDPOINTS = [
    "/api/org-queue",
    "/api/org-holds",
    "/api/research-artifacts",
    "/api/research-artifacts/ciw-pilot-msft/research-result.md",
]


def _login() -> None:
    r = client.post("/api/auth/login", json={"username": "founder", "password": "test-password-123"})
    assert r.status_code == 200, r.text


# ── 1. Auth boundary ─────────────────────────────────────────────────────────

def test_org_endpoints_require_auth():
    for ep in ORG_ENDPOINTS:
        r = client.get(ep)
        assert r.status_code == 401, f"{ep} -> {r.status_code} (auth boundary, FD #46)"


# ── 2. /org-queue ────────────────────────────────────────────────────────────

def test_org_queue_shape_and_provenance():
    _login()
    r = client.get("/api/org-queue")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "org_workflow_kanban"  # provenance truthfulness
    assert body["columns"] == [
        "Inbox", "Triage", "Scoped", "Data Ready", "In Research",
        "Cross-Review", "Validation", "Founder Review", "Monitoring",
        "Blocked", "Closed",
    ]  # KANBAN-CONTRACT §2
    assert len(body["cards"]) >= 5  # ORG-2026-0001..0005 pilot cards
    ids = [c["card_id"] for c in body["cards"]]
    assert "ORG-2026-0004" in ids and "ORG-2026-0001" in ids


def test_org_queue_card_fields():
    _login()
    cards = client.get("/api/org-queue").json()["cards"]
    c4 = next(c for c in cards if c["card_id"] == "ORG-2026-0004")
    # Mandatory card fields (KANBAN-CONTRACT §3) surfaced for the UI row
    assert c4["workflow_column"] == "Founder Review"
    assert c4["approval_status"] is None          # canonical state untouched
    assert c4["artifact_state"] == "Draft"
    assert c4["domain"] == "GOVERNANCE"
    assert c4["principal_owner"] == "IC Secretary (simulated)"
    assert c4["priority"] == "P1" and c4["materiality"] == "M2"
    assert c4["data_status"] == "DATA READY WITH LIMITATIONS"
    assert c4["validation_status"] == "PENDING"
    assert c4["risk_status"] == "REVIEWED WITH OPEN RISKS"
    assert c4["next_action"]  # non-empty next required action
    assert "created_at" in c4 and "last_updated" in c4


def test_org_queue_holds_join():
    _login()
    body = client.get("/api/org-queue").json()
    holds = body["holds"]
    assert {h["hold_id"] for h in holds} == {"HOLD-DATA-001", "HOLD-RISK-001"}
    # Both pilot holds are CLEARED -> attached but never "active"
    c2 = next(c for c in body["cards"] if c["card_id"] == "ORG-2026-0002")
    assert any(h["hold_id"] == "HOLD-DATA-001" for h in c2["holds"])
    assert c2["active_holds"] == []  # cleared hold is not an active hold


# ── 3. /org-holds ────────────────────────────────────────────────────────────

def test_org_holds_shape():
    _login()
    body = client.get("/api/org-holds").json()
    assert body["data_source"] == "org_workflow_holds"
    by_id = {h["hold_id"]: h for h in body["holds"]}
    assert set(by_id) == {"HOLD-DATA-001", "HOLD-RISK-001"}
    h = by_id["HOLD-DATA-001"]
    assert h["type"] == "DATA HOLD"
    assert h["issuer"] == "Data Steward (simulated)"
    assert h["remediation_required"]
    assert h["status"] == "CLEARED"
    assert h["clear_record"]["cleared_by"]  # clearance trail present
    assert h["owner"] == "Data Steward"


# ── 4. /research-artifacts registry ──────────────────────────────────────────

def test_research_artifact_registry_contains_real_ciw_artifacts():
    _login()
    body = client.get("/api/research-artifacts").json()
    assert body["data_source"] == "research_artifact_registry"
    by_id = {a["artifact_id"]: a for a in body["artifacts"]}
    # REAL published CIW results must be registered
    r1 = by_id["ciw-pilot-msft/research-result.md"]
    assert r1["artifact_type"] == "research-result"
    assert r1["research_id"] == "CRR-2026-0001"       # from artifact's own table
    assert "research_status" in r1                    # Founder Review / Published
    assert r1["path"] == "docs/ciw-pilot-msft/research-result.md"
    r2 = by_id["ciw-pilot-msft/research-result-2.md"]
    assert r2["research_id"] == "CRR-2026-0002"       # second slice (FD-CIW-016)
    # challenge-review files + pilot artifacts registered by convention
    assert any("challenge-review" in a["artifact_id"] for a in body["artifacts"])
    assert any(a["artifact_id"].startswith("org-pilot/") for a in body["artifacts"])


def test_research_artifact_detail():
    _login()
    r = client.get("/api/research-artifacts/ciw-pilot-msft/research-result.md")
    assert r.status_code == 200
    a = r.json()["artifact"]
    assert a["research_id"] == "CRR-2026-0001"
    assert "Microsoft" in a["content"]      # real markdown body served
    assert "content" in a and len(a["content"]) > 1000


def test_research_artifact_404_and_traversal_guard():
    _login()
    assert client.get("/api/research-artifacts/nope.md").status_code == 404
    assert client.get("/api/research-artifacts/ciw-pilot-msft/../org_store.py").status_code == 404
    assert client.get("/api/research-artifacts/..%2F..%2FREADME.md").status_code == 404
    assert client.get("/api/research-artifacts/ciw-pilot-msft/").status_code == 404
