"""Read-only UNH canonical case slice.

GET reports the case rebuilt from the committed cache.
POST rejects a FOUNDER_READY write while precondition stages are incomplete.
It does not publish the draft and it does not create a Founder decision.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend import auth
from research.qad_pilot.unh.case_slice import (
    CASE_ID,
    FounderReadyRejected,
    case_view,
    case_view_for_slug,
    recover_case,
    request_case_transition,
)

router = APIRouter(prefix="/api", tags=["qad-case"], dependencies=[Depends(auth.require_auth)])


class CaseStateAttempt(BaseModel):
    case_state: str | None = None
    publication_state: str | None = None


def _rejected(exc: FounderReadyRejected, requested: str) -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={
            "rejected": True,
            "requested": requested,
            "reason": exc.reason,
            "blocking_stages": exc.blocking_stages,
        },
    )


@router.get("/qad/cases/by-report/{slug}")
async def get_case_by_report(slug: str):
    try:
        return case_view_for_slug(slug)
    except KeyError:
        raise HTTPException(status_code=404, detail="no canonical case for this report") from None


@router.get("/qad/cases/{case_id}")
async def get_case(case_id: str):
    if case_id != CASE_ID:
        raise HTTPException(status_code=404, detail="case not found")
    return case_view(recover_case(case_id))


@router.post("/qad/cases/{case_id}/state")
async def attempt_case_state(case_id: str, body: CaseStateAttempt):
    if case_id != CASE_ID:
        raise HTTPException(status_code=404, detail="case not found")
    bundle = recover_case(case_id)
    requested = body.case_state or body.publication_state or ""
    try:
        request_case_transition(
            bundle,
            case_state=body.case_state,
            publication_state=body.publication_state,
        )
    except FounderReadyRejected as exc:
        raise _rejected(exc, requested) from exc
    raise HTTPException(status_code=409, detail={"rejected": True, "requested": requested})
