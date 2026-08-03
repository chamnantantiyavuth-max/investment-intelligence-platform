"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import am_routes, cs_routes, fo_routes
from backend.schemas.responses import DashboardSummary

app = FastAPI(title="IIP API", version="0.1.0")

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


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    # Derive CS counts from the single source of truth (cs_routes mock) so the
    # dashboard KPI can never disagree with /api/cs-radar (audit SOL-003 fix).
    cs_assets = cs_routes._MOCK_ASSETS
    return DashboardSummary(
        cs_radar_items=len(cs_assets),
        cs_qc_met=sum(1 for a in cs_assets if a["q_conditions_met"] == a["q_conditions_total"]),
    )
