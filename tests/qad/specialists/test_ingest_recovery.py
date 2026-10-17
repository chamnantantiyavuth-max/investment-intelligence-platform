"""Fresh Case API read recovers a specialist ingest from the committed journal."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

os.environ.setdefault("IIP_AUTH_USER", "founder")
os.environ.setdefault("IIP_AUTH_PASSWORD", "test-password-123")
os.environ.setdefault("IIP_AUTH_SECRET", "y" * 40)

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402
from qad.specialists.ingest import main as ingest_main  # noqa: E402

CASE = "CASE-2026-001"
GAP = "01a14a2d-3880-7792-80f6-34b43bab1141"
SOURCE = Path("research/qad-cases") / CASE
URL = "https://www.cms.gov/newsroom/fact-sheets/2027-medicare-advantage-part-d-rate-announcement"
GENUINE = "expected net 2.48 percent"
FABRICATED = "expected net 99.99 percent and an invented special dividend"


def _login(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"username": "founder", "password": "test-password-123"},
    )
    assert response.status_code == 200, response.text


def _write_result(path: Path) -> None:
    payload = {
        "contract": "qad.specialists.result.v1",
        "case_id": CASE,
        "gap_id": GAP,
        "investigator_charter_id": "01a14a2d-3880-7726-82dd-4d412bed3502",
        "specialist_id": "industry_economics_capital_cycle",
        "actor_id": "recovery-fixture-actor",
        "canonical_role": "Business & Industry Analyst",
        "desk_research_only": True,
        "disposition": "PARTIALLY_ANSWERED",
        "falsifiable_question": "Fixture question for the recovery test.",
        "stop_rule_triggered": "EVIDENCE_SUFFICIENT",
        "usage": {"tool_calls": 1, "sources": 1, "minutes": 5},
        "sampling_limitations": "Fixture snapshot only. No network.",
        "findings": ["fixture"],
        "claims": [
            {
                "statement": "The snapshot contains the genuine rate sentence.",
                "evidence_type": "FACT",
                "source": {
                    "url": URL,
                    "retrieval_timestamp": "2026-10-17T14:30:16Z",
                    "source_date": "2026-04-06",
                    "publisher": "CMS",
                    "source_tier": "L3",
                    "source_type": "GOVERNMENT_DATA",
                    "title": "Fixture snapshot",
                    "quotation": GENUINE,
                },
            },
            {
                "statement": "The snapshot contains an invented dividend.",
                "evidence_type": "FACT",
                "source": {
                    "url": URL,
                    "retrieval_timestamp": "2026-10-17T14:30:16Z",
                    "source_date": "2026-04-06",
                    "publisher": "CMS",
                    "source_tier": "L3",
                    "source_type": "GOVERNMENT_DATA",
                    "title": "Fixture snapshot",
                    "quotation": FABRICATED,
                },
            },
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_fresh_case_api_recovers_accepted_and_quarantined_evidence(tmp_path, monkeypatch):
    root = tmp_path / "cases"
    dest = root / CASE
    shutil.copytree(SOURCE, dest)
    for path in (dest / "ingest").glob("*.json"):
        path.unlink()
    (dest / "charters" / "reported-gaps.json").write_text("[]\n", encoding="utf-8")
    (dest / "charters" / "actor-ledger.json").write_text("[]\n", encoding="utf-8")
    snap = dest / "snapshots"
    snap.mkdir()
    (snap / "cms.bin").write_bytes(
        f"CMS fixture document.\n{GENUINE}\nEnd of snapshot.\n".encode("utf-8")
    )
    (snap / "cms.url").write_text(URL + "\n", encoding="utf-8")
    result_path = dest / "results" / f"{GAP}.json"
    _write_result(result_path)
    monkeypatch.setenv("QAD_CASE_ROOT", str(root))

    code = ingest_main(
        ["--case", CASE, "--result", str(result_path), "--charters", str(dest / "charters")]
    )
    assert code == 0
    journal = json.loads((dest / "ingest" / f"{GAP}.json").read_text(encoding="utf-8"))
    assert journal["verified_fact_count"] == 1
    assert journal["quarantined_count"] == 1
    assert journal["founder_ready"] is False
    assert journal["stage_state"] == "IN_PROGRESS"
    assert journal["case_state"] == "CASE_OPEN"

    first = TestClient(app)
    _login(first)
    body = first.get(f"/api/qad/cases/{CASE}").json()
    second = TestClient(app)
    _login(second)
    again = second.get(f"/api/qad/cases/{CASE}").json()

    assert body["case_state"] == "CASE_OPEN"
    assert body["case_state"] != "FOUNDER_READY"
    recovery = body["specialist_recovery"]
    assert recovery == again["specialist_recovery"]
    assert recovery["verified_fact_count"] == 1
    assert recovery["scuttlebutt_stage_state"] == "IN_PROGRESS"
    assert len(recovery["accepted_evidence"]) == 1
    assert recovery["accepted_evidence"][0]["verification_status"] == "VERIFIED"
    assert recovery["accepted_evidence"][0]["statement"] == (
        "The snapshot contains the genuine rate sentence."
    )
    quote_hash = hashlib.sha256(GENUINE.encode("utf-8")).hexdigest()
    assert recovery["accepted_evidence"][0]["content_hash"] != quote_hash
    assert len(recovery["quarantined"]) == 1
    assert recovery["quarantined"][0]["verification_status"] == "UNVERIFIED"
    assert "independently loaded" in recovery["quarantined"][0]["reason"]
    assert recovery["investigations"]
    assert recovery["investigations"][0]["disposition"] == "PARTIALLY_ANSWERED"
    stages = {row["stage_name"]: row["stage_state"] for row in body["stages"]}
    assert stages["SCUTTLEBUTT"] == "IN_PROGRESS"
    assert stages["SCUTTLEBUTT"] != "COMPLETE"
    for name in ("VALUATION", "UNDERWRITING", "AUDIT", "FOUNDER_REVIEW"):
        assert stages[name] == "NOT_STARTED"

    blocked = second.post(
        f"/api/qad/cases/{CASE}/state",
        json={"case_state": "FOUNDER_READY"},
    )
    assert blocked.status_code == 409
    assert blocked.json()["detail"]["rejected"] is True
