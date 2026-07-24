"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import am_routes, cs_routes
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


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    return DashboardSummary()
