"""Alpha Momentum API routes — real artifact-backed (FD #46, arch v0.4 §6)."""
from fastapi import APIRouter, Depends

from backend import adapters
from backend.auth import require_auth
from backend.schemas.responses import AMQueueResponse, ThemeWithCandidates

router = APIRouter(prefix="/api", tags=["alpha-momentum"], dependencies=[Depends(require_auth)])


@router.get("/am-queue", response_model=AMQueueResponse)
async def get_am_queue():
    return adapters.am_queue()


@router.get("/am-theme/{theme_id}", response_model=ThemeWithCandidates)
async def get_am_theme(theme_id: str):
    return adapters.am_theme(theme_id)
