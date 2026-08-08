"""Audit API routes (FD #86, WS-3 — UI-4 Decision Register / Audit Center).

Read-only operational/audit tracking. No writes; git is the single writer
and audit trail (KANBAN-CONTRACT §1).

Endpoints:
  GET /api/decisions          — Founder decision register (FOUNDERS-DECISIONS.md)
  GET /api/audit/git-log      — recent commits + §23.9 correction records
  GET /api/audit/model-registry — adapter version registry

Auth-protected like every /api/* route except the allowlist (FD #46/47).
"""
from __future__ import annotations

from fastapi import APIRouter, Depends

from backend import audit_store, auth

router = APIRouter(prefix="/api", tags=["audit"], dependencies=[Depends(auth.require_auth)])


@router.get("/decisions")
async def get_decisions():
    return {"data_source": "founders_decisions_register", "decisions": audit_store.list_decisions()}


@router.get("/audit/git-log")
async def get_git_log():
    return {
        "data_source": "git_history",
        "commits": audit_store._git_log(),
        "corrections": audit_store.list_corrections(),
    }


@router.get("/audit/model-registry")
async def get_model_registry():
    return {"data_source": "adapter_registry", **audit_store.model_registry()}
