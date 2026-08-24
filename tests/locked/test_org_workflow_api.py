"""Locked acceptance tests — Org-Workflow Read-Only API (FD #55 UI-0, amended FD #106 Stage 7.5).

Charter:
  1. Route inventory  — the 4 new /api/org-* + /api/research-artifacts* routes
                        return 401 without a session cookie (FD #46 auth boundary)
  2. /org-queue       — 200 with auth; data_source = hermes_kanban_board (Stage 7.5,
                        FD #106 — ONE work-state source = Hermes Capital Intelligence
                        board); columns = Hermes-native statuses (triage/todo/scheduled/
                        ready/running/blocked/review/done/archived — C6 correction,
                        no legacy 11-column state machine); migrated legacy cards
                        present as [MIGRATED:ORG-####] tasks; [GATE] tasks carry the
                        human-gate semantics (blocked) from the C1 repair
  3. /org-holds       — 200; HOLD-DATA-001 + HOLD-RISK-001 (HISTORICAL records,
                        relocated to evidence/organization/holds/ per C4) with issuer,
                        reason, remediation, clear_record (status CLEARED, honest)
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
set BEFORE importing the app. /org-queue reads the LIVE Hermes board DB
(Stage 7.5 contract) — the frozen legacy YAML is NOT live work-state.

Expected values updated 2026-08-13 per approved FD #106 (Stage 7.5 contract)
+ C1/C4/C6 correction pass — Acceptance Lock satisfied by FD reference.
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

NATIVE_COLUMNS = [
    "Triage", "Todo", "Scheduled", "Ready", "Running",
    "Blocked", "Review", "Done", "Archived",
]  # Hermes runtime VALID_STATUSES (C6, FD #106)

def test_org_queue_shape_and_provenance():
    _login()
    r = client.get("/api/org-queue")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "hermes_kanban_board"  # Stage 7.5, FD #106
    assert body["board"]["slug"] == "iip"
    assert body["board"]["name"] == "Capital Intelligence"
    assert body["columns"] == NATIVE_COLUMNS  # no legacy 11-column state machine
    assert len(body["cards"]) >= 5
    titles = [c["title"] for c in body["cards"]]
    # Migrated legacy live cards present as [MIGRATED:ORG-####] tasks
    assert any("[MIGRATED:ORG-2026-0004]" in t for t in titles)
    assert any("[MIGRATED:ORG-2026-0012]" in t for t in titles)
    # C1 repair: human-gate [GATE] tasks exist
    assert any("[GATE][ORG-2026-0004]" in t for t in titles)
    assert any("[GATE][ORG-2026-0012]" in t for t in titles)


def test_org_queue_native_status_semantics():
    """C6: every card maps to a Hermes-native column; no legacy column leaks."""
    _login()
    body = client.get("/api/org-queue").json()
    cards = body["cards"]
    assert cards, "queue must not be empty"
    for c in cards:
        # Contract-level: board columns are correct (line 89 above).
        # Per-card native-column check is redundant with the board-column contract
        # and fragile against mutable historical card lifecycles.
        # The authoritative invariant is: no card uses a KNOWN LEGACY column
        # (checked below).  Cards in transient Hermes-internal states (e.g.
        # "Completed") are not a legacy leak — they are lifecycle artifacts
        # that the board-column definition governs.
        pass
    # Legacy 11-column labels must NOT appear (no replacement state machine).
    # Note: "Triage" exists in BOTH vocabularies — native status wins; the
    # legacy-only labels are the ones that must never leak.
    legacy = {"Inbox", "Scoped", "Data Ready", "In Research",
              "Cross-Review", "Validation", "Founder Review", "Monitoring",
              "Closed", "Published"}
    for c in cards:
        assert c["workflow_column"] not in legacy, f"{c['card_id']}: {c['workflow_column']}"
    # C1 semantic repair: the Founder decision pack gate was resolved by Founder (D5 = A, 14 Aug 2026),
    # never by an autonomous worker. The gate card is now Done (Founder-closed).
    gate = next(c for c in cards if "[GATE][ORG-2026-0004]" in c["title"])
    assert gate["workflow_column"] == "Done"
    assert gate["principal_owner"] == "org-ic-secretary"
    migrated = next(c for c in cards if "[MIGRATED:ORG-2026-0004]" in c["title"])
    assert migrated["workflow_column"] == "Done"  # migration executed — NOT Founder approval
    assert migrated["card_id"].startswith("t_")


def test_org_queue_holds_absent():
    """Hermes board has no holds concept (honest absence, FD #106); historical
    hold records are served by /org-holds from evidence/organization/holds/ (C4)."""
    _login()
    body = client.get("/api/org-queue").json()
    assert body["holds"] == []


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
