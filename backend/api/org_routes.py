"""Org-workflow API routes (FD #55, UI-0 + Stage 7.5, FD #106) — read-only.

Serves kanban cards, holds, and the research-artifact registry. Since Stage 7.5
cutover the ONE authoritative organizational work-state source is the Hermes
Capital Intelligence board (`hermes_kanban_store`); legacy repo-board YAML is
FROZEN (Stage 7.1) and no longer read for live work-state. Operational tracking
ONLY — never domain state (KANBAN-CONTRACT §1). No writes; read-only UI.

Endpoints:
  GET /org-queue                — Hermes board columns + tasks
  GET /org-holds                — hold records (empty on Hermes board; legacy holds frozen)
  GET /research-artifacts       — artifact registry (unchanged — repo artifacts)
  GET /research-artifacts/{id}  — single artifact (markdown content)

Provenance is explicit per surface (data_source field). Auth-protected like
every /api/* route except the allowlist (FD #46/47).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from backend import auth, hermes_kanban_store, org_store

router = APIRouter(prefix="/api", tags=["org-workflow"], dependencies=[Depends(auth.require_auth)])


@router.get("/org-queue")
async def get_org_queue():
    try:
        cards = hermes_kanban_store.list_tasks()
        meta = hermes_kanban_store.board_meta()
        columns = hermes_kanban_store.COLUMNS
        holds = hermes_kanban_store.list_holds()
        data_source = meta.get("data_source", "hermes_kanban_board")
    except FileNotFoundError:
        # Hard-fail closed: do NOT silently fall back to the frozen legacy board
        # as live work-state (Stage 7.1 freeze). Surface the error honestly.
        raise HTTPException(status_code=503, detail="Hermes kanban board unavailable (frozen legacy board is not live work-state)")
    return {
        "data_source": data_source,
        "columns": columns,
        "cards": cards,
        "holds": holds,
        "board": {"slug": meta.get("slug"), "name": meta.get("name")},
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
