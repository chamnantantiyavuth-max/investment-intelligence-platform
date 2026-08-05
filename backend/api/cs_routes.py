"""Close System API routes — v0.1 pipeline artifact surface (FD #57).

The static demo mock (q_conditions/dimensions — no spec/pipeline basis) is
retired; /cs-radar and /cs-radar/{product_id} serve the ACTUAL v0.1 CS
pipeline artifact via backend.adapters (fixture_category SYNTHETIC, labeled).
"""
from fastapi import APIRouter, Depends, HTTPException

from backend import adapters, auth

router = APIRouter(prefix="/api", tags=["close-system"], dependencies=[Depends(auth.require_auth)])


@router.get("/cs-radar")
async def get_cs_radar():
    return {"data_source": "synthetic_demo", "assets": adapters.cs_radar()}


@router.get("/cs-radar/{product_id}")
async def get_cs_product(product_id: str):
    asset = adapters.cs_product(product_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="product not found")
    return {"data_source": "synthetic_demo", "asset": asset}
