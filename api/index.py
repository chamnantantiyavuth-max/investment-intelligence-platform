"""Vercel Python serverless entry — re-exports the FastAPI app.

Vercel deploys this file as the single /api/* function. The repo root is
added to sys.path so `backend` (and its reports/ data) resolves inside the
function bundle. Requirements live at api/requirements.txt (Vercel reads the
requirements file next to the entrypoint).
"""
import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# serverless filesystem is ephemeral: point SQLite + artifacts at /tmp
# (lineage survives only within an instance lifetime — documented limitation)
os.environ.setdefault("IIP_DB_PATH", "/tmp/iip.db")
os.environ.setdefault("IIP_ARTIFACT_BASE", "/tmp/artifacts")

# CORS: allow the deployed frontend origin (same-origin /api rewrites are the
# primary path; this covers cross-origin tooling)
os.environ.setdefault("IIP_ALLOWED_ORIGIN", "")

from backend.main import app  # noqa: E402

__all__ = ["app"]
