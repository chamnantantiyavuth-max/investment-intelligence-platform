"""Alpha Momentum API routes."""
from fastapi import APIRouter, HTTPException
from backend.schemas.responses import AMQueueResponse, ThemeSummary

router = APIRouter(prefix="/api", tags=["alpha-momentum"])

# DEMO DATA — static demonstration themes, NOT live pipeline output.
# data_source field on every response marks this provenance (Constitution §8/§23.4).
_MOCK_THEMES = [
    ThemeSummary(
        id="theme-ai-infra", name="AI Infrastructure", approval_status="approved",
        lifecycle="formation", driver_count=3, candidate_count=4,
        evidence_supporting=23, evidence_contradicting=4, evidence_missing=2,
        theme_quality=4.2, candidate_quality=4.0, entry_readiness=3.1, data_confidence=4.3,
    ),
    ThemeSummary(
        id="theme-glp1", name="GLP-1 Weight Loss", approval_status="approved",
        lifecycle="expansion", driver_count=5, candidate_count=6,
        evidence_supporting=31, evidence_contradicting=3, evidence_missing=1,
        theme_quality=4.5, candidate_quality=4.1, entry_readiness=3.8, data_confidence=4.6,
    ),
    ThemeSummary(
        id="theme-semicon", name="Semiconductor Cycle", approval_status="approved",
        lifecycle="expansion", driver_count=4, candidate_count=7,
        evidence_supporting=28, evidence_contradicting=5, evidence_missing=3,
        theme_quality=4.0, candidate_quality=4.3, entry_readiness=3.5, data_confidence=4.1,
    ),
    ThemeSummary(
        id="theme-defense", name="Defense Spending", approval_status="experimental",
        lifecycle="formation", driver_count=2, candidate_count=3,
        evidence_supporting=12, evidence_contradicting=6, evidence_missing=4,
        theme_quality=3.5, candidate_quality=3.2, entry_readiness=2.5, data_confidence=3.8,
    ),
    ThemeSummary(
        id="theme-grid", name="Grid Modernization", approval_status="experimental",
        lifecycle="weak_signal", driver_count=3, candidate_count=5,
        evidence_supporting=8, evidence_contradicting=2, evidence_missing=7,
        theme_quality=3.0, candidate_quality=3.5, entry_readiness=2.0, data_confidence=2.8,
    ),
]


@router.get("/am-queue", response_model=AMQueueResponse)
async def get_am_queue():
    return AMQueueResponse(themes=_MOCK_THEMES)


@router.get("/am-theme/{theme_id}", response_model=ThemeSummary)
async def get_am_theme(theme_id: str):
    for t in _MOCK_THEMES:
        if t.id == theme_id:
            return t
    raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")
