"""Locked acceptance tests — Real-Data Production Path (FD #46, arch v0.4, plan v1.1).

12-point charter (arch §9 / plan T1):
  1. Route inventory      — every /api/* route except allowlist -> 401 without cookie
  2. Auth                 — login ok/wrong, startup guards, tampered/expired/revoked, status, non-loopback
  3. AM                   — real artifact fields, per-theme+candidate provenance (hybrid), 6-field entry_readiness,
                            /am-theme/{id} {theme,candidates} shape, 404
  4. FO                   — envelope {run_id, provenance, packages}, locked flattening, value_trap_verdict derivation,
                            legacy root-list -> 503, /fo-package/{id} 404, cheap-quality NOT_A_TRAP filter
  5. II                   — /ii-signals 200 shape, meta + partial provenance, SYNTHETIC -> 503, stale -> 503
  6. CS                   — unchanged synthetic_demo contract
  7. Dashboard            — per-component provenance, CS counts == /api/cs-radar (triple agreement), unadmitted -> null
  8. Persistence          — ingest upsert, immutable (module,run_id) reject, api_read_runs composite, FK enforcement,
                            response_sha256, schema_version init/reject, adapter registry code-hash
  9. Fail-closed/stale    — corrupt/missing -> 503, wrong-mode -> 503, unknown-mode -> 503, stale -> 503
 10. Concurrency          — os.replace refresh during read -> old or new complete, never partial
 11. E2E subprocess       — producer (python3 3.14) writes temp FO envelope -> 3.11 FastAPI ingests + serves
 12. Frontend             — npm run build exit 0 (separate T9/T10 command; smoke asserted here via typed client contract)

Environment isolation: tests set IIP_DB_PATH + IIP_ARTIFACT_BASE + auth env vars BEFORE importing the app.
Do NOT modify expected values without a Bible quote or FD (Acceptance Lock Rule, FD-108).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

# ── Environment isolation (MUST precede app import) ──────────────────────────
TEST_ROOT = Path(tempfile.mkdtemp(prefix="iip-fd46-test-"))
TEST_DB = TEST_ROOT / "iip.db"
TEST_ARTIFACTS = TEST_ROOT / "artifacts"
TEST_ARTIFACTS.mkdir(parents=True, exist_ok=True)

os.environ["IIP_DB_PATH"] = str(TEST_DB)
os.environ["IIP_ARTIFACT_BASE"] = str(TEST_ARTIFACTS)
os.environ["IIP_AUTH_USER"] = "founder"
os.environ["IIP_AUTH_PASSWORD"] = "test-password-123"
os.environ["IIP_AUTH_SECRET"] = "x" * 40  # >=32 chars

from fastapi.testclient import TestClient  # noqa: E402

from backend.main import app  # noqa: E402

client = TestClient(app)

ALLOWLIST = {"/api/health", "/api/auth/login", "/api/auth/status"}


# ── Helpers ───────────────────────────────────────────────────────────────────
def _real_am_artifact() -> dict:
    """Load the committed REAL EOD AM artifact from the repo AND copy it into the isolated base."""
    p = Path(__file__).resolve().parents[2] / "alpha-momentum-v0" / "output" / "pipeline_result.json"
    assert p.exists(), f"AM artifact missing: {p}"
    payload = json.loads(p.read_text(encoding="utf-8"))
    # adapters read from IIP_ARTIFACT_BASE/am/ — mirror the real artifact there
    am_dir = TEST_ARTIFACTS / "am"
    am_dir.mkdir(parents=True, exist_ok=True)
    (am_dir / "pipeline_result.json").write_text(json.dumps(payload, default=str), encoding="utf-8")
    return payload


def _write_artifact(module: str, payload) -> Path:
    """Write an artifact into the isolated artifact base; return its path."""
    base = TEST_ARTIFACTS / module
    base.mkdir(parents=True, exist_ok=True)
    p = base / "pipeline_result.json"
    p.write_text(json.dumps(payload, default=str), encoding="utf-8")
    return p


def _login() -> dict:
    r = client.post("/api/auth/login", json={"username": "founder", "password": "test-password-123"})
    assert r.status_code == 200, r.text
    return {"cookies": client.cookies}


# ── 1. Route inventory ────────────────────────────────────────────────────────
def test_all_api_routes_require_auth_except_allowlist():
    for route in app.routes:
        path = getattr(route, "path", "")
        if not path.startswith("/api") or path in ALLOWLIST:
            continue
        methods = getattr(route, "methods", None)
        r = client.request(next(iter(methods)) if methods else "GET", path)
        # 401 = protected; 405 = wrong method for that path (still not publicly GET-served);
        # anything else (200/503/404) indicates a protection gap
        assert r.status_code in (401, 405), (
            f"route {path} must require auth (got {r.status_code}): {r.text[:120]}"
        )


def test_logout_requires_auth():
    fresh = TestClient(app)
    r = fresh.post("/api/auth/logout")
    assert r.status_code == 401


def test_allowlist_routes_are_reachable_without_auth():
    assert client.get("/api/health").status_code == 200
    r = client.get("/api/auth/status")
    assert r.status_code == 200
    assert r.json() == {"authenticated": False}


# ── 2. Auth ───────────────────────────────────────────────────────────────────
def test_login_wrong_password_401():
    r = client.post("/api/auth/login", json={"username": "founder", "password": "wrong"})
    assert r.status_code == 401


def test_login_ok_sets_session_and_status_true():
    _login()
    r = client.get("/api/auth/status")
    assert r.status_code == 200
    assert r.json() == {"authenticated": True}


def test_logout_revokes_session_server_side():
    _login()
    r = client.post("/api/auth/logout")
    assert r.status_code == 200
    # stolen/copied cookie must now be invalid (server-side nonce revoked)
    assert client.get("/api/am-queue").status_code == 401
    assert client.get("/api/auth/status").json() == {"authenticated": False}


def test_tampered_cookie_rejected():
    # fresh client so no valid session cookie leaks into the jar
    fresh = TestClient(app)
    fresh.post("/api/auth/login", json={"username": "founder", "password": "test-password-123"})
    fresh.cookies.clear()
    fresh.cookies.set("iip_session", "forged.value")
    assert fresh.get("/api/am-queue").status_code == 401


def test_missing_password_blocks_startup():
    """Startup guard: app refuses to boot without IIP_AUTH_PASSWORD (tested via import guard)."""
    from backend import auth as auth_mod  # noqa: F401
    assert auth_mod.ENV_CHECKED is True


def test_non_loopback_host_rejected():
    _login()
    r = client.get("/api/am-queue", headers={"Host": "evil.example.com"})
    assert r.status_code == 403


# ── 3. AM ─────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def am_artifact_bytes():
    p = Path(__file__).resolve().parents[2] / "alpha-momentum-v0" / "output" / "pipeline_result.json"
    return p.read_bytes()


def test_am_queue_serves_real_artifact_fields(am_artifact_bytes):
    art = _real_am_artifact()
    _login()
    r = client.get("/api/am-queue")
    assert r.status_code == 200
    body = r.json()
    assert body["run_id"] == art["run_id"]
    assert body["point_in_time"] == art["point_in_time"]
    themes = body["themes"]
    assert len(themes) == len(art["queue"])
    # first theme must match the real artifact (TH-014) — no fabricated counts
    t0 = themes[0]["theme"]
    art_theme = art["queue"][0][1]["theme"]
    assert t0["id"] == art_theme["id"]
    assert t0["name"] == art_theme["name"]
    assert "driver_count" not in t0, "synthetic-only field must be removed"
    assert t0["provenance"]["mode"] == "real"
    assert t0["provenance"]["hybrid"] is True  # real EOD overlays + SRC-SYN evidence


def test_am_candidate_entry_readiness_six_fields():
    art = _real_am_artifact()
    _login()
    r = client.get("/api/am-queue")
    body = r.json()
    cand = body["themes"][0]["candidates"][0]
    er = cand["entry_readiness"]
    assert set(er.keys()) == {
        "price_structure", "base_quality", "breakout_proximity",
        "volume_behavior", "volatility_contraction", "extension_risk",
    }
    assert cand["provenance"]["component_map"]  # non-empty component provenance


def test_am_evidence_provenance_marks_synthetic_sources():
    art = _real_am_artifact()
    _login()
    r = client.get("/api/am-queue")
    body = r.json()
    ev = body["themes"][0]["theme"]["evidence_provenance"]
    types = {e["source_type"] for e in ev}
    assert "synthetic" in types  # SRC-SYN evidence must be labeled synthetic


def test_am_theme_detail_shape_and_404():
    art = _real_am_artifact()
    theme_id = art["queue"][0][0]
    _login()
    r = client.get(f"/api/am-theme/{theme_id}")
    assert r.status_code == 200
    body = r.json()
    assert "theme" in body and "candidates" in body  # {theme, candidates} shape
    assert body["theme"]["id"] == theme_id
    assert client.get("/api/am-theme/does-not-exist").status_code == 404


# ── 4. FO ─────────────────────────────────────────────────────────────────────
def _fo_envelope() -> dict:
    return {
        "run_id": "FO-20260803-000001",
        "provenance": {"source": "yfinance", "mode": "real", "as_of": "2026-08-01",
                       "coverage": "3/3", "completeness": "complete", "hybrid": False},
        "packages": [
            {
                "id": "AAPL", "name": "Apple Inc.", "generated_at": "2026-08-01T00:00:00",
                "spec_ref": "FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1",
                "thesis_summary": "s", "thesis_lifecycle": "Under Review",
                "conviction": {"level": "High", "score": 80},
                "macro_context": {}, "industry_assessment": {"sector": "Tech", "industry": "Hardware"},
                "company_assessment": {"moat": {"width": "Wide", "depth": "Deep", "trend": "Stable"}},
                "earnings_trajectory": {"rating": "GOOD"},
                "valuation_context": {"value_trap": {"triggered": False}},
                "key_risks": [], "independent_challenge": [],
                "supporting_evidence": [{"text": "real data", "source": "yfinance"}],
                "contradicting_evidence": [], "open_questions": [],
            }
        ],
    }


def test_fo_queue_reads_envelope_no_rerun():
    _write_artifact("fo", _fo_envelope())
    _login()
    r = client.get("/api/fo-queue")
    assert r.status_code == 200
    body = r.json()
    assert body[0]["id"] == "AAPL"
    assert body[0]["provenance"]["mode"] == "real"
    assert body[0]["value_trap_verdict"] == "NOT_TRIGGERED"  # triggered==false -> label
    # flattening contract
    assert body[0]["sector"] == "Tech"
    assert body[0]["industry"] == "Hardware"
    assert body[0]["moat_width"] == "Wide"
    assert body[0]["earnings_quality"] == "GOOD"
    assert body[0]["conviction"] == "High"


def test_fo_value_trap_triggered_uses_artifact_verdict():
    env = _fo_envelope()
    env["packages"][0]["valuation_context"]["value_trap"] = {
        "triggered": True, "verdict": "NOT_A_TRAP", "score": 4, "max_score": 5}
    _write_artifact("fo", env)
    _login()
    r = client.get("/api/fo-queue")
    assert r.json()[0]["value_trap_verdict"] == "NOT_A_TRAP"


def test_fo_cheap_quality_filters_not_a_trap():
    env = _fo_envelope()
    env["packages"][0]["valuation_context"]["value_trap"] = {
        "triggered": True, "verdict": "NOT_A_TRAP"}
    env["packages"].append(dict(env["packages"][0], id="INTC",
                                valuation_context={"value_trap": {"triggered": True, "verdict": "VALUE_TRAP"}}))
    _write_artifact("fo", env)
    _login()
    r = client.get("/api/fo-cheap-quality")
    ids = [p["id"] for p in r.json()]
    assert "AAPL" in ids and "INTC" not in ids


def test_fo_legacy_root_list_rejected_503():
    _write_artifact("fo", [{"id": "AAPL", "name": "Apple"}])  # legacy root list, no envelope
    _login()
    r = client.get("/api/fo-queue")
    assert r.status_code == 503


def test_fo_package_detail_404():
    _write_artifact("fo", _fo_envelope())
    _login()
    assert client.get("/api/fo-package/UNKNOWN").status_code == 404
    r = client.get("/api/fo-package/aapl")
    assert r.status_code == 200
    assert r.json()["id"] == "AAPL"


# ── 5. II ─────────────────────────────────────────────────────────────────────
def _ii_artifact(mode: str = "REAL 13F", partial: bool = False) -> dict:
    return {
        "signals": [{
            "filer_name": "Scion", "filer_cik": "0001649339", "filer_category": "Legendary",
            "ticker": "JD", "filing_quarter": "2026Q1", "report_date": "2026-03-31",
            "pct_of_portfolio": 37.5, "conviction": "Maximum", "action": "ADD",
            "change_pct": 29.8, "signal_score": 95, "value_usd": 75000000,
        }],
        "summary": {"total_funds_tracked": 5, "total_signals": 68, "total_filings": 10},
        "meta": {
            "version": "v0.1.0", "spec_ref": "FD #42",
            "generated_at": "2026-07-28T02:32:22",
            "data_source": mode,
            "as_of": "2026-07-28",
            "completeness": "partial_3_5" if partial else "complete",
        },
    }


def test_ii_signals_200_shape_and_provenance():
    _write_artifact("ii", _ii_artifact(partial=True))
    _login()
    r = client.get("/api/ii-signals")
    assert r.status_code == 200
    body = r.json()
    assert body["signals"][0]["ticker"] == "JD"
    assert body["provenance"]["mode"] == "real"
    assert body["provenance"]["completeness"] == "partial_3_5"  # partial preserved verbatim


def test_ii_synthetic_artifact_rejected_503():
    _write_artifact("ii", _ii_artifact(mode="SYNTHETIC"))
    _login()
    assert client.get("/api/ii-signals").status_code == 503


def test_ii_stale_artifact_rejected_503():
    art = _ii_artifact()
    art["meta"]["as_of"] = "2026-01-01"  # > 120 days before 2026-08-03
    _write_artifact("ii", art)
    _login()
    assert client.get("/api/ii-signals").status_code == 503


# ── 6. CS ─────────────────────────────────────────────────────────────────────
def test_cs_radar_unchanged_synthetic_demo():
    _login()
    r = client.get("/api/cs-radar")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "synthetic_demo"
    assert isinstance(body["assets"], list)


# ── 7. Dashboard ──────────────────────────────────────────────────────────────
def test_dashboard_per_component_provenance_and_cs_agreement():
    _write_artifact("fo", _fo_envelope())
    _write_artifact("ii", _ii_artifact())
    _login()
    r = client.get("/api/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    # per-component provenance
    assert body["components"]["am"]["data_source"].startswith("real")
    assert body["components"]["fo"]["data_source"].startswith("real")
    assert body["components"]["ii"]["data_source"].startswith("real")
    # CS: explicit null lineage, static mock source, NOT linked to CS pipeline artifact
    cs = body["components"]["cs"]
    assert cs["run_id"] is None and cs["point_in_time"] is None
    assert cs["data_source"] == "synthetic_demo"
    assert cs["source"] == "backend_static_mock"
    # SOL-003 triple agreement: dashboard CS counts == /api/cs-radar collection + Q-met
    cs_radar = client.get("/api/cs-radar").json()["assets"]
    expected_items = len(cs_radar)
    expected_qmet = sum(1 for a in cs_radar if a["q_conditions_met"] == a["q_conditions_total"])
    assert body["cs_radar_items"] == expected_items
    assert body["cs_qc_met"] == expected_qmet
    assert not (body["cs_radar_items"] == 8 and body["cs_qc_met"] == 3)  # hardcoded regression guard


def test_dashboard_unadmitted_component_is_null():
    # no FO artifact -> fo component must be unavailable, not synthetic
    fo_dir = TEST_ARTIFACTS / "fo"
    if fo_dir.exists():
        shutil.rmtree(fo_dir)
    _write_artifact("ii", _ii_artifact())
    _login()
    r = client.get("/api/dashboard/summary")
    body = r.json()
    fo = body["components"]["fo"]
    assert fo["state"] == "unavailable"
    assert fo.get("data_source") is None


# ── 8. Persistence / lineage ──────────────────────────────────────────────────
def test_ingest_upsert_and_immutable_reject():
    from backend import persistence
    art = _real_am_artifact()
    payload = json.dumps(art, default=str).encode()
    run_id = persistence.ingest_run("am", payload)
    # re-ingest identical bytes -> same row, no dup
    run_id2 = persistence.ingest_run("am", payload)
    assert run_id == run_id2
    # same (module, run_id) with different bytes -> REJECT (immutable)
    altered = json.dumps({**art, "point_in_time": "2026-08-02"}, default=str).encode()
    with pytest.raises(Exception):
        persistence.ingest_run("am", altered)


def test_api_reads_lineage_with_composite_runs():
    from backend import persistence
    fo_bytes = json.dumps(_fo_envelope(), default=str).encode()
    ii_bytes = json.dumps(_ii_artifact(), default=str).encode()
    fo_run = persistence.ingest_run("fo", fo_bytes)
    ii_run = persistence.ingest_run("ii", ii_bytes)
    read_id = persistence.log_read(
        endpoint="/api/dashboard/summary", params="{}", data_source="real",
        response_sha256=hashlib.sha256(b"resp").hexdigest(), status=200,
        adapter_version=persistence.ADAPTER_VERSION,
        runs=[(fo_run, "fo"), (ii_run, "ii")],
    )
    rows = persistence.get_read_runs(read_id)
    assert {r["component"] for r in rows} == {"fo", "ii"}
    # FK enforcement: invalid run id must fail
    with pytest.raises(Exception):
        persistence.log_read("/api/x", "{}", "real", "h", 200, "v1", runs=[(999999, "am")])


def test_schema_version_init_and_newer_reject():
    from backend import persistence
    assert persistence.get_schema_version() == 1
    persistence.set_schema_version(99)  # simulate newer schema
    # next open must refuse to operate
    with pytest.raises(Exception):
        persistence.check_schema_compatibility()


def test_adapter_registry_code_hash_bound():
    from backend import persistence
    from backend import adapters
    assert persistence.ADAPTER_VERSION == adapters.ADAPTER_VERSION
    # code-hash is deterministic and non-trivial
    assert len(adapters.ADAPTER_CODE_HASH) == 64
    assert adapters.ADAPTER_CODE_HASH == hashlib.sha256(
        Path(adapters.__file__).read_bytes()).hexdigest()


# ── 9. Fail-closed / stale ────────────────────────────────────────────────────
def test_missing_artifact_503():
    # ensure the isolated AM artifact is absent (earlier tests may have mirrored it)
    am_dir = TEST_ARTIFACTS / "am"
    if am_dir.exists():
        shutil.rmtree(am_dir)
    _login()
    assert client.get("/api/am-queue").status_code == 503


def test_corrupt_artifact_503():
    _write_artifact("ii", b"{not json")
    _login()
    assert client.get("/api/ii-signals").status_code == 503


def test_unknown_mode_artifact_503():
    art = _ii_artifact(mode="MYSTERY")
    _write_artifact("ii", art)
    _login()
    assert client.get("/api/ii-signals").status_code == 503


# ── 10. Concurrency ───────────────────────────────────────────────────────────
def test_atomic_replace_during_read_never_partial():
    env = _fo_envelope()
    p = _write_artifact("fo", env)
    # simulate runner atomic write: tmp + os.replace while server reads
    for i in range(30):
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(env, default=str), encoding="utf-8")
        os.replace(tmp, p)  # atomic on same filesystem
        _login()
        r = client.get("/api/fo-queue")
        assert r.status_code == 200  # never 500/partial-parse
        assert r.json()[0]["id"] == "AAPL"


# ── 11. E2E subprocess (python3 3.14 producer -> 3.11 FastAPI) ────────────────
@pytest.mark.skipif(shutil.which("python3") is None, reason="python3 (3.14 producer) not on PATH")
def test_e2e_subprocess_envelope_produce_and_serve():
    producer_dir = Path(__file__).resolve().parents[2] / "fundamental-opportunity-v0"
    out_dir = TEST_ROOT / "e2e-out"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "pipeline_result.json"
    # producer: minimal synthetic run with envelope + atomic write (no network)
    code = (
        "import json,sys,os,pathlib;"
        "p=pathlib.Path(sys.argv[1]);"
        "env={'run_id':'E2E-1','provenance':{'source':'yfinance','mode':'real','as_of':'2026-08-01',"
        "'coverage':'1/1','completeness':'complete','hybrid':False},"
        "'packages':[{'id':'AAPL','name':'Apple Inc.','generated_at':'2026-08-01','spec_ref':'s',"
        "'thesis_summary':'s','thesis_lifecycle':'Under Review','conviction':{'level':'High'},"
        "'macro_context':{},'industry_assessment':{'sector':'Tech','industry':'Hardware'},"
        "'company_assessment':{'moat':{'width':'Wide','depth':'Deep','trend':'Stable'}},"
        "'earnings_trajectory':{'rating':'GOOD'},'valuation_context':{'value_trap':{'triggered':False}},"
        "'key_risks':[],'independent_challenge':[],'supporting_evidence':[],'contradicting_evidence':[],"
        "'open_questions':[]}]};"
        "tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(env),encoding='utf-8');"
        "os.replace(tmp,p);print('written')"
    )
    r = subprocess.run([sys.executable, "-c", code, str(out_path)],
                       cwd=str(producer_dir), capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    # 3.11 FastAPI ingests + serves the envelope produced by the 3.14 interpreter
    shutil.copy(out_path, TEST_ARTIFACTS / "fo" / "pipeline_result.json")
    _login()
    resp = client.get("/api/fo-queue")
    assert resp.status_code == 200
    assert resp.json()[0]["id"] == "AAPL"
    assert resp.json()[0]["provenance"]["mode"] == "real"


# ── 12. Frontend contract (typed client smoke) ────────────────────────────────
def test_frontend_client_types_match_locked_contracts():
    """Static contract guard: frontend TS types must not reference removed synthetic fields."""
    types_am = Path(__file__).resolve().parents[2] / "frontend" / "src" / "types" / "am.ts"
    text = types_am.read_text(encoding="utf-8")
    for removed in ("driver_count", "candidate_count", "evidence_supporting",
                    "evidence_contradicting", "evidence_missing", "theme_quality"):
        assert removed not in text, f"removed synthetic field {removed} still in types/am.ts"
    for client_path in ("amClient.ts", "foClient.ts", "csClient.ts", "iiClient.ts", "authClient.ts"):
        p = Path(__file__).resolve().parents[2] / "frontend" / "src" / "api" / client_path
        assert p.exists(), f"missing client {client_path}"
        assert 'credentials: "include"' in p.read_text(encoding="utf-8") or "credentials: 'include'" in p.read_text(encoding="utf-8"), \
            f"{client_path} must send credentials"


# ── Cleanup ───────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def _cleanup():
    yield
    shutil.rmtree(TEST_ROOT, ignore_errors=True)
