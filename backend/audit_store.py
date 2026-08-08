"""Audit store — read-only decision/audit/model-registry data for UI-4 (FD #86, WS-3).

Sources (all committed repo files, no DB):
  1. FOUNDERS-DECISIONS.md          — the Founder decision register (items 1..N)
  2. git log                        — commit history (via subprocess, bounded)
  3. research/**/CORRECTIONS-RECORD.md — Constitution §23.9 correction records
  4. backend/adapter_registry.json  — adapter version -> committed code hash

Operational/audit tracking ONLY — never domain state (KANBAN-CONTRACT §1).
No writes; git is the single writer and audit trail.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DECISIONS_PATH = REPO_ROOT / "operational" / "FOUNDERS-DECISIONS.md"
ADAPTER_REGISTRY_PATH = Path(__file__).with_name("adapter_registry.json")
CORRECTIONS_GLOB = "research/**/CORRECTIONS-RECORD.md"

_ITEM_RE = re.compile(r"^(\d+)\.\s+(.*)$")
_DATE_RE = re.compile(r"\b(\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) 2026)\b")


def _parse_decisions() -> list[dict]:
    """Parse FOUNDERS-DECISIONS.md into ordered decision items.

    Handles three first-line shapes: plain statements (items 1–44),
    FD-CIW-xxx (45–52), and FD #N (53+). Continuation lines are appended
    to the item body; title = first segment before ' — ' or ':'.
    """
    text = DECISIONS_PATH.read_text(encoding="utf-8")
    items: list[dict] = []
    cur: dict | None = None
    for ln in text.splitlines():
        m = _ITEM_RE.match(ln)
        if m:
            if cur is not None:
                items.append(cur)
            first = m.group(2).strip()
            cur = {"num": int(m.group(1)), "first": first, "body": ""}
        elif cur is not None and ln.strip():
            cur["body"] += ln.strip() + " "
    if cur is not None:
        items.append(cur)

    out = []
    for it in items:
        combined = (it["first"] + " " + it["body"]).strip()
        title = it["first"].split(" — ")[0].split(": ")[0].strip()
        dm = _DATE_RE.search(combined)
        out.append(
            {
                "num": it["num"],
                "title": title,
                "preview": (combined[:180] + ("…" if len(combined) > 180 else "")),
                "date": dm.group(1) if dm else "",
            }
        )
    return out


def list_decisions() -> list[dict]:
    return _parse_decisions()


def _git_log(limit: int = 40) -> list[dict]:
    """Recent commit history (bounded). Runs git in the repo root."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", f"-{limit}", "--pretty=format:%h|%ad|%s", "--date=short"],
            capture_output=True, text=True, timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return []
    commits = []
    for ln in proc.stdout.splitlines():
        if "|" not in ln:
            continue
        h, d, s = ln.split("|", 2)
        commits.append({"hash": h, "date": d, "subject": s.strip()})
    return commits


def list_corrections() -> list[dict]:
    records = []
    for p in sorted(REPO_ROOT.glob(CORRECTIONS_GLOB)):
        records.append(
            {
                "path": str(p.relative_to(REPO_ROOT)).replace("\\", "/"),
                "modified": p.stat().st_mtime,
            }
        )
    return records


def model_registry() -> dict:
    """Adapter registry (immutable version -> committed code hash) + current version."""
    try:
        versions = json.loads(ADAPTER_REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        versions = {}
    try:
        from backend import adapters  # noqa: PLC0415

        current = getattr(adapters, "ADAPTER_VERSION", "")
    except Exception:  # pragma: no cover — import-guard only
        current = ""
    return {"current_version": current, "versions": versions}
