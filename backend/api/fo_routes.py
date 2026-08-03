"""Fundamental & Opportunity Intelligence API routes — real artifact-backed (FD #46, arch v0.4 §6)."""
from fastapi import APIRouter, Depends

from backend import adapters
from backend.auth import require_auth
from backend.schemas.responses import ResearchPackageDetail, ResearchPackageSummary

router = APIRouter(prefix="/api", tags=["fundamental-opportunity"], dependencies=[Depends(require_auth)])


@router.get("/fo-queue", response_model=list[ResearchPackageSummary])
async def get_fo_queue():
    return adapters.fo_queue()


@router.get("/fo-package/{company_id}", response_model=ResearchPackageDetail)
async def get_fo_package(company_id: str):
    return adapters.fo_package(company_id)


@router.get("/fo-cheap-quality", response_model=list[ResearchPackageSummary])
async def get_fo_cheap_quality():
    return adapters.fo_cheap_quality()
