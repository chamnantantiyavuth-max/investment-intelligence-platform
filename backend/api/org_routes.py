"""Org-workflow API routes (FD #55, UI-0) — read-only operational tracking.

Serves kanban cards, holds, and the research-artifact registry from committed
repo files. Operational tracking ONLY — never domain state (KANBAN-CONTRACT
§1). No writes; git is the single writer and audit trail.

Endpoints:
  GET /org-queue                — kanban columns + cards (+ holds join)
  GET /org-holds                — hold records (active + cleared)
  GET /research-artifacts       — artifact registry
  GET /research-artifacts/{id}  — single artifact (markdown content)

Provenance is explicit per surface (data_source field). Auth-protected like
every /api/* route except the allowlist (FD #46/47).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from backend import auth, org_store

router = APIRouter(prefix="/api", tags=["org-workflow"], dependencies=[Depends(auth.require_auth)])


@router.get("/org-queue")
async def get_org_queue():
    cards = org_store.list_cards()
    return {
        "data_source": "org_workflow_kanban",
        "columns": org_store.COLUMNS,
        "cards": cards,
        "holds": org_store.list_holds(),
    }


@router.get("/org-holds")
async def get_org_holds():
    return {
        "data_source": "org_workflow_holds",
        "holds": org_store.list_holds(),
    }


@router.get("/research-artifacts")
async def get_research_artifacts():
    return {
        "data_source": "research_artifact_registry",
        "artifacts": org_store.list_artifacts(),
    }


@router.get("/research-artifacts/{artifact_id:path}")
async def get_research_artifact(artifact_id: str):
    artifact = org_store.get_artifact(artifact_id)
    if artifact is None:
        raise HTTPException(status_code=404, detail="artifact not found")
    return {"data_source": "research_artifact_registry", "artifact": artifact}
