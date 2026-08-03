"""Institutional Intelligence API routes — NEW surface (FD #46, arch v0.4 §6)."""
from fastapi import APIRouter, Depends

from backend import adapters
from backend.auth import require_auth
from backend.schemas.responses import IISignalsResponse

router = APIRouter(prefix="/api", tags=["institutional-intelligence"], dependencies=[Depends(require_auth)])


@router.get("/ii-signals", response_model=IISignalsResponse)
async def get_ii_signals(limit: int = 0, offset: int = 0):
    """II signals with optional server-side pagination (FD #46; limit=0 = full list, backward-compatible)."""
    return adapters.ii_signals(limit=limit, offset=offset)
