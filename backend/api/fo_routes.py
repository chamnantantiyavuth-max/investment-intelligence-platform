"""Fundamental & Opportunity Intelligence API routes (Phase 8)."""
from fastapi import APIRouter, HTTPException
from backend.schemas.responses import ResearchPackageSummary, ResearchPackageDetail

# ── Pipeline import (same pattern as test_locked imports) ──
import sys
import os

_FO_DIR = os.path.join(os.path.dirname(__file__), "../../fundamental-opportunity-v0")
sys.path.insert(0, os.path.abspath(_FO_DIR))

from pipeline import run_pipeline, build_research_package

router = APIRouter(prefix="/api", tags=["fundamental-opportunity"])


def _pkg_to_summary(pkg: dict) -> ResearchPackageSummary:
    """Convert a full pipeline package dict into a lightweight summary."""
    ia = pkg.get("industry_assessment", {})
    ca = pkg.get("company_assessment", {})
    moat = ca.get("moat", {})
    et = pkg.get("earnings_trajectory", {})
    vt = pkg.get("valuation_context", {}).get("value_trap", {})

    return ResearchPackageSummary(
        id=pkg.get("id", "UNKNOWN"),
        name=pkg.get("name", "Unknown"),
        sector=ia.get("sector", "Unknown"),
        industry=ia.get("industry", "Unknown"),
        moat_width=moat.get("width", "None"),
        moat_depth=moat.get("depth", "Shallow"),
        moat_trend=moat.get("trend", "Stable"),
        earnings_quality=et.get("rating", "UNKNOWN"),
        conviction=pkg.get("conviction", {}).get("level", "Unknown"),
        value_trap_verdict=vt.get("verdict", "NOT_TRIGGERED"),
    )


def _pkg_to_detail(pkg: dict) -> ResearchPackageDetail:
    """Convert a full pipeline package dict into a ResearchPackageDetail."""
    ia = pkg.get("industry_assessment", {})
    ca = pkg.get("company_assessment", {})
    moat = ca.get("moat", {})
    et = pkg.get("earnings_trajectory", {})
    vt = pkg.get("valuation_context", {}).get("value_trap", {})

    return ResearchPackageDetail(
        id=pkg.get("id", "UNKNOWN"),
        name=pkg.get("name", "Unknown"),
        sector=ia.get("sector", "Unknown"),
        industry=ia.get("industry", "Unknown"),
        moat_width=moat.get("width", "None"),
        moat_depth=moat.get("depth", "Shallow"),
        moat_trend=moat.get("trend", "Stable"),
        earnings_quality=et.get("rating", "UNKNOWN"),
        conviction=pkg.get("conviction", {}),
        value_trap_verdict=vt.get("verdict", "NOT_TRIGGERED"),
        generated_at=pkg.get("generated_at", ""),
        spec_ref=pkg.get("spec_ref", ""),
        thesis_summary=pkg.get("thesis_summary", ""),
        thesis_lifecycle=pkg.get("thesis_lifecycle", ""),
        macro_context=pkg.get("macro_context", {}),
        industry_assessment=pkg.get("industry_assessment", {}),
        company_assessment=pkg.get("company_assessment", {}),
        earnings_trajectory=pkg.get("earnings_trajectory", {}),
        valuation_context=pkg.get("valuation_context", {}),
        key_risks=pkg.get("key_risks", []),
        independent_challenge=pkg.get("independent_challenge", []),
        supporting_evidence=pkg.get("supporting_evidence", []),
        contradicting_evidence=pkg.get("contradicting_evidence", []),
        open_questions=pkg.get("open_questions", []),
    )


@router.get("/fo-queue", response_model=list[ResearchPackageSummary])
async def get_fo_queue():
    """Run the full FO pipeline and return 8 summary items."""
    packages = run_pipeline()
    return [_pkg_to_summary(pkg) for pkg in packages]


@router.get("/fo-package/{company_id}", response_model=ResearchPackageDetail)
async def get_fo_package(company_id: str):
    """Return the full research package for a single company."""
    packages = run_pipeline()
    company_upper = company_id.upper()
    for pkg in packages:
        if pkg.get("id", "").upper() == company_upper:
            return _pkg_to_detail(pkg)
    raise HTTPException(status_code=404, detail=f"Company '{company_id}' not found")


@router.get("/fo-cheap-quality", response_model=list[ResearchPackageSummary])
async def get_fo_cheap_quality():
    """Filter pipeline results to companies with value_trap_verdict == NOT_A_TRAP."""
    packages = run_pipeline()
    results = []
    for pkg in packages:
        vt = pkg.get("valuation_context", {}).get("value_trap", {}).get("verdict", "")
        if vt == "NOT_A_TRAP":
            results.append(_pkg_to_summary(pkg))
    return results
