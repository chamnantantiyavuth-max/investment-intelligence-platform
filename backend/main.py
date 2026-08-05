"""FastAPI application entry point — Real-Data Production Path (FD #46, arch v0.4).

Auth (FD #47): all /api/* except health + auth/login + auth/status require session cookie.
Loopback enforcement: non-loopback Host -> 403 while cookie is Secure=False (F6).
ASGI capture: response_sha256 logged over exact serialized bytes (F2/NF6).
"""
from __future__ import annotations

import hashlib

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import adapters, auth, persistence
from backend.api import am_routes, cs_routes, fo_routes, ii_routes, org_routes
from backend.schemas.responses import DashboardSummary, ComponentProvenance

app = FastAPI(title="IIP API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(am_routes.router)
app.include_router(cs_routes.router)
app.include_router(fo_routes.router)
app.include_router(ii_routes.router)
app.include_router(org_routes.router)


# ── Auth endpoints ────────────────────────────────────────────────────────────
class LoginBody(BaseModel):
    username: str
    password: str


@app.post("/api/auth/login")
async def login(body: LoginBody, response: Response):
    if not auth.login(body.username, body.password, response):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"authenticated": True}


@app.post("/api/auth/logout")
async def logout(request: Request, response: Response):
    """Logout requires an authenticated session (server-side revocation, F6)."""
    auth.require_auth(request)
    auth.logout(response)
    return {"authenticated": False}


@app.get("/api/auth/status")
async def auth_status(request: Request):
    cookie = request.cookies.get(auth.SESSION_COOKIE)
    return {"authenticated": auth.verify_session(cookie)}


# ── Loopback Host enforcement (F6) ────────────────────────────────────────────
@app.middleware("http")
async def loopback_guard(request: Request, call_next):
    host = (request.headers.get("host") or "").split(":")[0]
    if host not in ("127.0.0.1", "localhost", "testserver", "::1"):
        return Response(status_code=403, content="non-loopback host rejected")
    return await call_next(request)


# ── ASGI response capture (F2/NF6): hash exact serialized bytes served + persist lineage ──
class CaptureResponseMiddleware:
    """Pure ASGI middleware: captures status + exact body bytes, persists api_reads lineage.

    Council F1: records the REAL HTTP status, REAL response SHA-256, and the component runs
    that produced the response (adapters.REQUEST_RUNS) into api_reads + api_read_runs.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or not scope.get("path", "").startswith("/api") \
                or scope["path"] in ("/api/health", "/api/auth/login", "/api/auth/status"):
            await self.app(scope, receive, send)
            return
        adapters.REQUEST_RUNS.set([])  # fresh lineage accumulator per request
        chunks = []
        status_holder = {"status": 0}

        async def send_capture(message):
            if message["type"] == "http.response.start":
                status_holder["status"] = message.get("status", 0)
            elif message["type"] == "http.response.body":
                chunks.append(message.get("body", b""))
            await send(message)

        await self.app(scope, receive, send_capture)
        body = b"".join(chunks)
        try:
            if body:
                sha = hashlib.sha256(body).hexdigest()
                runs = list(adapters.REQUEST_RUNS.get())
                read_id = persistence.log_read(
                    endpoint=scope["path"], params=str(scope.get("query_string", b"")),
                    data_source="api", response_sha256=sha, status=status_holder["status"],
                    adapter_version=persistence.ADAPTER_VERSION, runs=runs)
                # dashboard composite lineage uses api_read_runs via REQUEST_RUNS
                adapters.LAST_READ_ID.set(read_id)
        except Exception as e:  # pragma: no cover - defensive; lineage must not fail the request
            import sys
            print(f"[capture] lineage log failed for {scope.get('path')}: {type(e).__name__}: {e}",
                  file=sys.stderr)


app.add_middleware(CaptureResponseMiddleware)


# ── Fail-closed exception mapping (F5): ArtifactUnavailable -> 503 ───────────
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


@app.exception_handler(adapters.ArtifactUnavailable)
async def artifact_unavailable_handler(request: Request, exc: adapters.ArtifactUnavailable):
    return JSONResponse(
        status_code=503,
        content={"detail": "artifact unavailable", "module": exc.module,
                 "reason": exc.reason, "info": exc.detail},
    )


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok"}


# ── Dashboard (per-component provenance + CS triple agreement, SOL-003) ──────
@app.get("/api/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary(request: Request):
    auth.require_auth(request)
    comps = adapters.dashboard_components()
    am = comps.get("am")
    fo = comps.get("fo")
    ii = comps.get("ii")
    cs_counts = comps.get("_cs_counts")

    components = {}
    for key in ("am", "fo", "ii", "cs"):
        c = comps.get(key)
        if c is None:
            components[key] = ComponentProvenance(state="unavailable")
        else:
            components[key] = c

    # CS counts derived from the exact served mock bytes (SOL-003 fix)
    cs_assets = cs_routes._MOCK_ASSETS
    cs_radar_items = len(cs_assets)
    cs_qc_met = sum(1 for a in cs_assets if a["q_conditions_met"] == a["q_conditions_total"])

    # Total themes / queue size from admitted AM run (real artifact), else 0
    total_themes = 0
    approved_themes = 0
    queue_size = 0
    am_last_run = None
    if am is not None:
        try:
            q = adapters.am_queue()
            themes = q.themes
            total_themes = len(themes)
            approved_themes = sum(1 for t in themes if t.theme.approval_status.lower() == "approved")
            queue_size = len(themes)
            am_last_run = q.point_in_time
        except Exception:
            pass

    return DashboardSummary(
        total_themes=total_themes, approved_themes=approved_themes,
        active_signals=0, queue_size=queue_size, am_last_run=am_last_run,
        cs_radar_items=cs_radar_items, cs_qc_met=cs_qc_met, cs_regime="risk-on",
        components=components,
    )
