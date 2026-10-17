"""Fresh process reads the B1 finding back through the Case API.

The child process is a new interpreter. It recovers CASE-2026-001 by
replaying committed journals, which mints the S5/M6 receipt by fetching
the filing again. This is not a hosted database.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

EXPECTED_SHA256 = "6953bf0e9f2cbb3ccec3849321f14663012329d50a7c596c593956ced7a65ed7"
GAP_ID = "EG-2026-001-B1-01"
STATEMENT = (
    "Continued funding pressures have resulted in benefit and pricing actions, "
    "causing contraction in our Medicare Advantage membership in the first quarter, "
    "which we expect to continue throughout 2026."
)


def test_fresh_process_recovers_b1_receipt_and_blocks_founder_ready():
    script = """
import json, os
os.environ["IIP_AUTH_USER"] = "founder"
os.environ["IIP_AUTH_PASSWORD"] = "test-password-123"
os.environ["IIP_AUTH_SECRET"] = "y" * 40
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
login = client.post(
    "/api/auth/login",
    json={"username": "founder", "password": "test-password-123"},
)
assert login.status_code == 200, login.text
body = client.get("/api/qad/cases/CASE-2026-001").json()
blocked = client.post(
    "/api/qad/cases/CASE-2026-001/state",
    json={"case_state": "FOUNDER_READY"},
)
recovery = body["specialist_recovery"]
rows = [
    row for row in recovery["accepted_evidence"]
    if row.get("gap_id") == "EG-2026-001-B1-01"
]
stages = {row["stage_name"]: row["stage_state"] for row in body["stages"]}
print(json.dumps({
    "case_state": body["case_state"],
    "founder_ready_status": blocked.status_code,
    "founder_ready_rejected": blocked.json()["detail"]["rejected"],
    "stages": stages,
    "scuttlebutt_stage_state": recovery["scuttlebutt_stage_state"],
    "verified_fact_count": recovery["verified_fact_count"],
    "finding": rows[0] if rows else None,
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
    finding = payload["finding"]
    assert finding is not None
    assert finding["verification_status"] == "VERIFIED"
    assert finding["statement"] == STATEMENT
    assert finding["content_hash"] == EXPECTED_SHA256
    assert finding["source_id"]
    assert finding["retriever"] == "qad.m6.source_bridge"
    assert finding["retrieval_method"] == "M6 original-source verification receipt"
    assert finding["gap_id"] == GAP_ID
