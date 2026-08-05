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
    """Startup guard: app refuses to boot without IIP_AUTH_PASSWORD (real subprocess proof)."""
    code = (
        "import os; os.environ.pop('IIP_AUTH_PASSWORD', None); os.environ['IIP_AUTH_SECRET']='x'*40; "
        "import backend.auth"
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30,
                       cwd=str(Path(__file__).resolve().parents[2]))
    assert r.returncode != 0, "backend.auth must refuse to import without IIP_AUTH_PASSWORD"
    assert "IIP_AUTH_PASSWORD" in r.stderr


def test_weak_secret_blocks_startup():
    """Startup guard: secret <32 chars must refuse to boot (real subprocess proof)."""
    code = (
        "import os; os.environ['IIP_AUTH_PASSWORD']='pw'; os.environ['IIP_AUTH_SECRET']='short'; "
        "import backend.auth"
    )
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=30,
                       cwd=str(Path(__file__).resolve().parents[2]))
    assert r.returncode != 0, "backend.auth must refuse weak IIP_AUTH_SECRET"
    assert "IIP_AUTH_SECRET" in r.stderr


def test_expired_session_rejected_server_side():
    """F6/F8: a token past its expires_at must be rejected even if the cookie is presented."""
    from backend import auth as auth_mod
    _login()
    # craft a token signed with the test secret but already expired
    import time as _time
    nonce = "expired-nonce"
    payload = json.dumps({"nonce": nonce, "issued_at": int(_time.time()) - 7200,
                          "expires_at": int(_time.time()) - 3600}, separators=(",", ":"))
    expired_token = f"{payload}.{auth_mod._sign(payload)}"
    fresh = TestClient(app)
    fresh.cookies.set(auth_mod.SESSION_COOKIE, expired_token)
    assert fresh.get("/api/am-queue").status_code == 401


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


def test_am_theme_falsification_fields_passthrough():
    """Falsification read-only extension (mini-FD, 4 Aug 2026, Constitution §11):
    alternative_explanations / evidence register / unresolved_counter_evidence
    map straight from the artifact — never invented, additive DTO fields only."""
    art = _real_am_artifact()
    _login()
    r = client.get("/api/am-queue")
    body = r.json()
    themes = body["themes"]
    # field presence — additive contract on every theme
    for t in themes:
        tt = t["theme"]
        assert "alternative_explanations" in tt
        assert "evidence" in tt
        assert "unresolved_counter_evidence" in tt
    # per-theme alternatives match the artifact (TH-004 carries a real one)
    t004 = next(t["theme"] for t in themes if t["theme"]["id"] == "TH-004")
    assert t004["alternative_explanations"] and "TH-004" in t004["alternative_explanations"]
    # evidence register entries carry id/type/content
    if t004["evidence"]:
        ev = t004["evidence"][0]
        assert {"id", "type", "content"}.issubset(ev.keys())
    # counter-evidence normalized to a list when present
    for t in themes:
        uce = t["theme"]["unresolved_counter_evidence"]
        if uce:
            assert isinstance(uce, list) and all(isinstance(x, str) for x in uce)


def test_am_counter_evidence_scoped_per_theme():
    """Audit C2 fix: unresolved counter-evidence attaches ONLY to the theme whose
    candidate owns the override (OVR-001 → CAND-002 → TH-004). Unrelated themes
    (e.g. TH-014 Medical Devices) must NOT receive the INTC/semiconductor record."""
    art = _real_am_artifact()
    host = next(
        tid for tid, pl in art["queue"]
        if any(c.get("id") == "CAND-002" for c in pl.get("candidates", []))
    )
    _login()
    body = client.get("/api/am-queue").json()
    assert body["themes"], "queue must not be empty"
    for t in body["themes"]:
        uce = t["theme"]["unresolved_counter_evidence"]
        if t["theme"]["id"] == host:
            assert uce, f"host theme {host} must carry OVR-001 counter-evidence"
            assert any("EV-003" in x for x in uce)
        else:
            assert not uce, f"unrelated theme {t['theme']['id']} must not carry OVR-001 counter-evidence"


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
_FO_SEQ = [0]


def _fo_envelope() -> dict:
    _FO_SEQ[0] += 1  # unique run_id per test — immutable guard rejects reused ids with different bytes
    return {
        "run_id": f"FO-20260803-{_FO_SEQ[0]:06d}",
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
            "change_pct": 29.8, "value_usd": 75000000,
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


def test_ii_pagination_limit_offset():
    """II pagination (FD #46, 3 Aug post-release): limit/offset slice, total always full count."""
    art = _ii_artifact(partial=True)
    extra = []
    for i, tk in enumerate(("AAPL", "MSFT", "NVDA", "AMZN")):
        s = dict(art["signals"][0], ticker=tk, value_usd=1000 * (i + 1))
        extra.append(s)
    art["signals"] = extra
    _write_artifact("ii", art)
    _login()
    r = client.get("/api/ii-signals?limit=2&offset=0")
    assert r.status_code == 200
    b1 = r.json()
    assert len(b1["signals"]) == 2
    assert b1["total"] == 4
    r2 = client.get("/api/ii-signals?limit=2&offset=2")
    b2 = r2.json()
    assert len(b2["signals"]) == 2
    # no overlap between page 1 and page 2
    ids1 = {s["ticker"] for s in b1["signals"]}
    ids2 = {s["ticker"] for s in b2["signals"]}
    assert not (ids1 & ids2), "pagination pages must not overlap"
    assert ids1 | ids2 == {"AAPL", "MSFT", "NVDA", "AMZN"}
    # provenance preserved on paginated response
    assert b1["provenance"]["mode"] == "real"
    assert b1["provenance"]["completeness"] == "partial_3_5"


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


# ── 6. CS — v0.1 pipeline artifact surface (FD #57: mock replaced) ───────────
def test_cs_radar_pipeline_synthetic_demo():
    _login()
    r = client.get("/api/cs-radar")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "synthetic_demo"
    assets = body["assets"]
    assert isinstance(assets, list)
    tickers = [a["ticker"] for a in assets]
    # eligible radar products from the committed v0.1 pipeline artifact, conviction-priority order
    # (Maximum SLV first per spec §5.1)
    assert tickers == ["SLV", "TLT", "GDX", "XLE"], tickers
    # admitted pipeline fields (FD #57)
    slv = next(a for a in assets if a["ticker"] == "SLV")
    assert slv["p1_pass"] is True and slv["p2_pass"] is True and slv["p3_pass"] is True
    assert slv["layers_aligned"] == 5 and slv["layers_contradicting"] == 0
    # conviction reconciled with the recommendation rationale (council F2): 5/5 aligned +
    # hidden corroboration + confirmed discount = Maximum per spec §5.1
    assert slv["conviction"] == "Maximum" and slv["recommendation"] == "Present to Founder"
    assert "L1_macro" in slv["layers"] and "L5_hidden" in slv["layers"]
    assert slv["layers"]["L1_macro"]["signal"] in ("supporting", "neutral", "contradicting")
    assert slv["discount_detail"] and slv["demand_detail"] and slv["key_risks"]
    # mock-only fields removed — no spec/pipeline basis (FD #57; Q-conditions belong to AM)
    for key in ("q_conditions_met", "q_conditions_total", "q_details",
                "dimensions", "rule_pack", "instrument", "liquidity", "capital_lockup"):
        assert key not in slv, key


def test_cs_product_detail_and_404():
    _login()
    r = client.get("/api/cs-radar/SLV")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"] == "synthetic_demo"
    assert body["asset"]["ticker"] == "SLV"
    assert body["asset"]["discount_detail"]["signal"]
    assert body["asset"]["demand_detail"]  # product-specific breakdown (solar/electronics/supply for SLV)
    assert client.get("/api/cs-radar/NOPE").status_code == 404


# ── 7. Dashboard ──────────────────────────────────────────────────────────────
def test_dashboard_per_component_provenance_and_cs_agreement():
    _real_am_artifact()  # mirror real AM artifact — this test is self-sufficient (no order dependency)
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
    # CS: pipeline-linked synthetic surface (FD #57) — run_id/point_in_time from the artifact
    cs = body["components"]["cs"]
    assert cs["run_id"] == "CS-V0-20260805-180430"
    assert cs["point_in_time"] == "2026-08-05T18:04:30.174454"
    assert cs["data_source"] == "synthetic_demo"
    assert cs["source"] == "close_system_pipeline"
    # SOL-003 triple agreement preserved: dashboard CS counts == /api/cs-radar via the adapter;
    # cs_qc_met = display derivation, count of products with full 5-layer alignment (FD #57)
    cs_radar = client.get("/api/cs-radar").json()["assets"]
    expected_items = len(cs_radar)
    expected_aligned = sum(1 for a in cs_radar if a["layers_aligned"] == 5)
    assert body["cs_radar_items"] == expected_items == 4
    assert body["cs_qc_met"] == expected_aligned == 1


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
    # same (module, run_id) with different bytes -> REJECT (immutable, case a)
    altered = json.dumps({**art, "point_in_time": "2026-08-02"}, default=str).encode()
    with pytest.raises(Exception):
        persistence.ingest_run("am", altered)


def test_ingest_no_embedded_run_id_content_addressed():
    """Plan T1/C7 case b: bytes without an embedded run_id get a hash-derived id;
    changed bytes -> NEW id (never collapses)."""
    from backend import persistence
    p1 = {"packages": [{"id": "A"}]}
    p2 = {"packages": [{"id": "B"}]}
    r1 = persistence.ingest_run("noembed", json.dumps(p1).encode())
    r2 = persistence.ingest_run("noembed", json.dumps(p2).encode())
    assert r1 != r2, "different bytes must produce different content-addressed run ids"
    # re-ingest identical bytes -> same id (idempotent)
    r1b = persistence.ingest_run("noembed", json.dumps(p1).encode())
    assert r1b == r1


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


def test_endpoint_to_db_lineage_wired():
    """Council F1: a real AM/FO/II read must register pipeline_runs + api_reads + api_read_runs."""
    from backend import persistence
    from backend import adapters
    _write_artifact("fo", _fo_envelope())
    _write_artifact("ii", _ii_artifact())
    _real_am_artifact()  # mirror real AM artifact into isolated base
    _login()
    # real API reads (dashboard touches am+fo+ii -> composite lineage)
    r = client.get("/api/dashboard/summary")
    assert r.status_code == 200
    body = r.json()
    # dashboard run_ids must be NON-NULL now (F1 proof)
    for comp in ("am", "fo", "ii"):
        assert body["components"][comp]["run_id"], f"{comp} run_id must be registered"
    # pipeline_runs rows exist for all three modules
    for mod in ("am", "fo", "ii"):
        assert persistence.latest_run(mod) is not None
    # api_reads row recorded with real status + hash for the dashboard call
    conn = persistence._connect()
    try:
        row = conn.execute(
            "SELECT endpoint, status, response_sha256, adapter_version FROM api_reads "
            "WHERE endpoint='/api/dashboard/summary' ORDER BY id DESC LIMIT 1").fetchone()
        assert row is not None
        assert row["status"] == 200
        assert len(row["response_sha256"]) == 64
        assert row["adapter_version"] == persistence.ADAPTER_VERSION
        # composite lineage: dashboard read has 3 component runs
        n = conn.execute(
            "SELECT COUNT(*) c FROM api_read_runs ar JOIN api_reads a ON a.id=ar.api_read_id "
            "WHERE a.endpoint='/api/dashboard/summary'").fetchone()["c"]
        assert n >= 3, f"expected >=3 api_read_runs rows, got {n}"
    finally:
        conn.close()


def test_schema_version_init_and_newer_reject():
    from backend import persistence
    assert persistence.get_schema_version() == 1
    persistence.set_schema_version(99)  # simulate newer schema
    # next open must refuse to operate
    with pytest.raises(Exception):
        persistence.check_schema_compatibility()
    persistence.set_schema_version(1)  # restore — avoids polluting later tests (test order)


def test_api_reads_lineage_records_real_status_and_hash():
    """Council F1/F8: middleware-recorded api_reads carries the REAL status + response SHA."""
    from backend import persistence
    _write_artifact("fo", _fo_envelope())
    _login()
    r = client.get("/api/fo-queue")
    assert r.status_code == 200
    expected_sha = hashlib.sha256(r.content).hexdigest()
    conn = persistence._connect()
    try:
        row = conn.execute(
            "SELECT status, response_sha256, adapter_version FROM api_reads "
            "WHERE endpoint='/api/fo-queue' ORDER BY id DESC LIMIT 1").fetchone()
        assert row is not None
        assert row["status"] == 200
        assert row["response_sha256"] == expected_sha, "recorded hash must match actual served bytes"
        assert row["adapter_version"] == persistence.ADAPTER_VERSION
    finally:
        conn.close()


def test_adapter_registry_code_hash_bound():
    from backend import persistence
    from backend import adapters
    assert persistence.ADAPTER_VERSION == adapters.ADAPTER_VERSION
    # code-hash is deterministic and non-trivial
    assert len(adapters.ADAPTER_CODE_HASH) == 64
    # F3: current file hash MUST match the registered immutable hash — else registry contract broken
    assert adapters.ADAPTER_CODE_HASH == adapters.ADAPTER_REGISTRY[adapters.ADAPTER_VERSION]
    # F3: changing the code without bumping the version must FAIL verification with the
    # registry guard error (NOT any exception — a NameError would have masked the guard)
    original_hash = adapters.ADAPTER_CODE_HASH
    adapters.ADAPTER_CODE_HASH = "0" * 64  # simulate a source change without a version bump
    try:
        with pytest.raises(RuntimeError, match="adapter code hash"):
            adapters.verify_adapter_registry()
    finally:
        adapters.ADAPTER_CODE_HASH = original_hash


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
    r = subprocess.run([shutil.which("python3"), "-c", code, str(out_path)],
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
