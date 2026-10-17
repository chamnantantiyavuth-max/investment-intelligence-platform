"""Research blog API routes (FD #62) — read-only report library.

  GET /api/reports        — report index (metadata only, newest first)
  GET /api/reports/{slug} — single report (frontmatter meta + markdown body)

Auth-protected like every /api/* route (single-user session). Read-only:
git remains the single writer and audit trail.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from backend import auth, report_store

router = APIRouter(prefix="/api", tags=["research-blog"], dependencies=[Depends(auth.require_auth)])


@router.get("/reports")
async def get_reports(status: str | None = Query(default=None)):
    """Report index. Default is every status, including drafts.

    The library page hides drafts unless the reader opens `?preview=draft`.
    `?status=draft` is the explicit API filter for that same preview.
    """
    reports = report_store.list_reports()
    if status:
        reports = [r for r in reports if r["status"] == status]
    return {"data_source": "research_blog_reports", "reports": reports}


@router.get("/reports/{slug}")
async def get_report(slug: str):
    report = report_store.get_report(slug)
    if report is None:
        raise HTTPException(status_code=404, detail="report not found")
    return {"data_source": "research_blog_reports", "report": report}
