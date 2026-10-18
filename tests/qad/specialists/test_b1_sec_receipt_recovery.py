"""Fresh process reads the B1 finding back through the Case API.

The child process is a new interpreter. It recovers CASE-2026-001 from
committed journals and the persisted M6 receipt. urlopen and
create_connection raise, so a read that fetches fails the test.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

EXPECTED_SHA256 = "6953bf0e9f2cbb3ccec3849321f14663012329d50a7c596c593956ced7a65ed7"
RECEIPT_SHA256 = "52fd7cb8572f32efc71f6dcceeb837decf91e801f055c88fb595810c6b43ea97"
NORMALIZED_SHA256 = "9f16515990aa8880e9e0b243192d7f8cafdd891e2ffe3fd8b56d34d07cf5d5d1"
GAP_ID = "EG-2026-001-B1-01"
STATEMENT = (
    "Continued funding pressures have resulted in benefit and pricing actions, "
    "causing contraction in our Medicare Advantage membership in the first quarter, "
    "which we expect to continue throughout 2026."
)


def test_fresh_process_recovers_b1_receipt_and_blocks_founder_ready():
    script = """
import json, os, socket, urllib.request
os.environ["IIP_AUTH_USER"] = "founder"
os.environ["IIP_AUTH_PASSWORD"] = "test-password-123"
os.environ["IIP_AUTH_SECRET"] = "y" * 40
from fastapi.testclient import TestClient
from backend.main import app

def _blocked(*args, **kwargs):
    raise RuntimeError("outbound HTTP is not allowed on a case or report read")

urllib.request.urlopen = _blocked
socket.create_connection = _blocked
client = TestClient(app)
login = client.post(
    "/api/auth/login",
    json={"username": "founder", "password": "test-password-123"},
)
assert login.status_code == 200, login.text
report = client.get("/api/reports/unh-b1-medicare-advantage-2026-10-18")
assert report.status_code == 200, report.text
article = report.json()["report"]
assert article["status"] == "draft"
assert "VERIFIED" in article["content"]
assert "UNVERIFIED" in article["content"]
assert "6953bf0e9f2cbb3ccec3849321f14663012329d50a7c596c593956ced7a65ed7" in article["content"]
assert "52fd7cb8572f32efc71f6dcceeb837decf91e801f055c88fb595810c6b43ea97" in article["content"]
assert "9f16515990aa8880e9e0b243192d7f8cafdd891e2ffe3fd8b56d34d07cf5d5d1" in article["content"]
body = client.get("/api/qad/cases/CASE-2026-001").json()
by_report = client.get("/api/qad/cases/by-report/unh-b1-medicare-advantage-2026-10-18")
assert by_report.status_code == 200, by_report.text
blocked = client.post(
    "/api/qad/cases/CASE-2026-001/state",
    json={"case_state": "FOUNDER_READY"},
)
recovery = body["specialist_recovery"]
rows = [
    row for row in recovery["accepted_evidence"]
    if row.get("gap_id") == "EG-2026-001-B1-01"
]
held = [
    row for row in recovery["quarantined"]
    if "Continued funding pressures have resulted" in str(row.get("statement") or "")
]
stages = {row["stage_name"]: row["stage_state"] for row in body["stages"]}
print(json.dumps({
    "case_state": body["case_state"],
    "report_status": article["status"],
    "by_report_status": by_report.status_code,
    "founder_ready_status": blocked.status_code,
    "founder_ready_rejected": blocked.json()["detail"]["rejected"],
    "stages": stages,
    "scuttlebutt_stage_state": recovery["scuttlebutt_stage_state"],
    "verified_fact_count": recovery["verified_fact_count"],
    "finding": rows[0] if rows else None,
    "quarantine": held[0] if held else None,
    "quarantined_count": len(recovery["quarantined"]),
}))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(Path(__file__).resolve().parents[3]),
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout.strip().splitlines()[-1])
    print(json.dumps(payload, indent=2))
    assert payload["case_state"] == "CASE_OPEN"
    assert payload["founder_ready_status"] == 409
    assert payload["founder_ready_rejected"] is True
    stages = payload["stages"]
    for name in ("SCUTTLEBUTT", "AUDIT", "UNDERWRITING", "FOUNDER_REVIEW", "VALUATION"):
        assert stages[name] != "COMPLETE"
    assert stages["SCUTTLEBUTT"] == "INCOMPLETE"
    assert stages["AUDIT"] == "NOT_STARTED"
    assert stages["UNDERWRITING"] == "NOT_STARTED"
    assert payload["verified_fact_count"] == 1
    assert payload["quarantine"] is None
    finding = payload["finding"]
    assert finding is not None
    assert finding["verification_status"] == "VERIFIED"
    assert finding["statement"] == STATEMENT
    assert finding["content_hash"] == RECEIPT_SHA256
    assert finding["normalized_sha256"] == NORMALIZED_SHA256
    assert finding["evidence_lead_raw_sha256"] == EXPECTED_SHA256
    assert finding["evidence_lead_normalized_sha256"] == NORMALIZED_SHA256
    assert finding["cross_retrieval_agreement"] == "normalized"
    assert finding["source_id"] == "01a14a2d-3880-7cf3-8376-90acd6428de7"
    assert finding["evidence_id"] == "01a14a2d-3880-7c04-b439-988da8c3b4d7"
    assert finding["fact_id"] == "01a14a2d-3880-744f-a52b-55ca8009751c"
    assert payload["quarantined_count"] == 42
    assert payload["report_status"] == "draft"
