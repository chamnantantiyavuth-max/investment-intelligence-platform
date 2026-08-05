"""Read-only store for IIP org-workflow tracking data (FD #55, UI-0).

Serves operational tracking ONLY — kanban card/hold state and the research
artifact registry. Never domain state (KANBAN-CONTRACT §1: "card state never
equals domain state"). Read-only: git remains the single writer and audit
trail. No schema, no migration, no writes.

Data sources (all committed repo files, verified 2026-08-05):
  - operational/hermes-organization/kanban/cards/*.yaml   (card schema §3)
  - operational/hermes-organization/kanban/holds/*.yaml   (hold schema §10)
  - docs/ciw-pilot-msft/**/*.md        (CIW research artifacts — REAL)
  - evidence/organization/pilot/*.md   (org dry-run pilot — simulated)

Design notes:
  - Deliberately does NOT touch backend/adapters.py: this is a new read-only
    file adapter, so the F3 ADAPTER_VERSION ceremony does not apply.
  - PyYAML is used for the flat card/hold YAML (verified present 6.0.3 in
    both `python` and `python3`; NOT added to requirements.txt).
  - Provenance is explicit per surface: org_workflow_kanban /
    org_workflow_holds / research_artifact_registry. The registry never
    invents fields: identity values are parsed from the artifact's own
    "Identity and State" table when present, else null (honest absence).
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

KANBAN_DIR = REPO_ROOT / "operational" / "hermes-organization" / "kanban"
CARDS_DIR = KANBAN_DIR / "cards"
HOLDS_DIR = KANBAN_DIR / "holds"

# Canonical column order — KANBAN-CONTRACT §2 (single source).
COLUMNS = [
    "Inbox", "Triage", "Scoped", "Data Ready", "In Research",
    "Cross-Review", "Validation", "Founder Review", "Monitoring",
    "Blocked", "Closed",
]

# Artifact roots for the registry: (registry key, repo-relative dir).
ARTIFACT_ROOTS = [
    ("ciw-pilot-msft", REPO_ROOT / "docs" / "ciw-pilot-msft"),
    ("org-pilot", REPO_ROOT / "evidence" / "organization" / "pilot"),
]

# Filename → artifact-type mapping (convention, not AI-invented).
_ARTIFACT_TYPE_PATTERNS = [
    (re.compile(r"^CRR-.*-request\.md$"), "research-request"),
    (re.compile(r"^research-result.*\.md$"), "research-result"),
    (re.compile(r"^research-draft.*\.md$"), "research-draft"),
    (re.compile(r"^source-map.*\.md$"), "source-map"),
    (re.compile(r"^challenge-review.*\.md$"), "challenge-review"),
    (re.compile(r"^founder-review-record.*\.md$"), "founder-review-record"),
    (re.compile(r"^monitoring.*\.md$"), "monitoring"),
    (re.compile(r"^IC-DECISION-PACK\.md$"), "ic-decision-pack"),
    (re.compile(r"^DATA-QUALITY-REPORT\.md$"), "data-quality-report"),
    (re.compile(r"^RISK-CHALLENGE-MEMO\.md$"), "risk-challenge-memo"),
    (re.compile(r"^EQUITY-RESEARCH-BRIEF.*\.md$"), "equity-research-brief"),
    (re.compile(r"^WORKLOG-.*\.md$"), "assistant-worklog"),
    (re.compile(r"^PILOT-REPORT\.md$"), "pilot-report"),
]

# Identity-and-State table row:  | `research_id` | CRR-2026-0001 |
_IDENTITY_ROW = re.compile(r"^\|\s*`?([a-z_]+)`?\s*\|\s*([^|]+?)\s*\|")
_HEADING = re.compile(r"^#\s+(.+)$")
_CARD_REF = re.compile(r"card\s+(ORG-\d{4}-\d{4})")


def _parse_flat_yaml(path: Path) -> dict:
    """Load a flat card/hold YAML file; missing/empty file -> {}."""
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh.read())
        return data if isinstance(data, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def _mtime_iso(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
    except OSError:
        return ""


# ── Kanban cards ─────────────────────────────────────────────────────────────

def list_cards() -> list[dict]:
    """All kanban cards sorted by card_id, each joined with its holds."""
    holds = list_holds()
    cards = []
    for path in sorted(CARDS_DIR.glob("ORG-*.yaml")):
        data = _parse_flat_yaml(path)
        if not data:
            continue
        card_id = data.get("card_id") or path.stem
        data["active_holds"] = [h for h in holds if _hold_attaches_to(h, card_id) and not _hold_cleared(h)]
        data["holds"] = [h for h in holds if _hold_attaches_to(h, card_id)]
        data["_path"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        cards.append(data)
    return cards


def _hold_attaches_to(hold: dict, card_id: str) -> bool:
    refs = set()
    for field in ("artifact", "scope"):
        refs.update(_CARD_REF.findall(str(hold.get(field) or "")))
    return card_id in refs


def _hold_cleared(hold: dict) -> bool:
    return str(hold.get("status") or "").upper() == "CLEARED"


# ── Holds ────────────────────────────────────────────────────────────────────

def list_holds() -> list[dict]:
    holds = []
    for path in sorted(HOLDS_DIR.glob("HOLD-*.yaml")):
        data = _parse_flat_yaml(path)
        if not data:
            continue
        data.setdefault("hold_id", path.stem)
        data["_path"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        holds.append(data)
    return holds


# ── Research artifact registry ───────────────────────────────────────────────

def _artifact_type(name: str) -> str:
    for pattern, atype in _ARTIFACT_TYPE_PATTERNS:
        if pattern.match(name):
            return atype
    return "document"


def _parse_identity_table(text: str) -> dict:
    """Extract the artifact's own Identity-and-State fields (CIW result contract).

    Honest absence: returns {} when the artifact has no such table. Never
    invents values — only `research_id`, `research_version`,
    `research_status` are surfaced.
    """
    out: dict = {}
    for line in text.splitlines():
        m = _IDENTITY_ROW.match(line.strip())
        if m and m.group(1) in ("research_id", "research_version", "research_status"):
            out[m.group(1)] = m.group(2).strip()
    return out


def list_artifacts() -> list[dict]:
    artifacts = []
    for key, root in ARTIFACT_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.md")):
            rel = path.relative_to(root)
            artifact_id = f"{key}/{rel.as_posix()}"
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            heading = _HEADING.search(text)
            identity = _parse_identity_table(text)
            artifacts.append({
                "artifact_id": artifact_id,
                "title": heading.group(1).strip() if heading else path.stem,
                "artifact_type": _artifact_type(path.name),
                "path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "modified": _mtime_iso(path),
                **identity,  # research_id / research_version / research_status
            })
    return sorted(artifacts, key=lambda a: a["artifact_id"])


def get_artifact(artifact_id: str) -> dict | None:
    """Resolve artifact_id (e.g. "ciw-pilot-msft/research-result.md").

    Traversal guard: resolves against the allowed roots and requires the
    final path to stay inside one of them (no writes, read-only).
    """
    if not artifact_id or ".." in artifact_id:
        return None
    for key, root in ARTIFACT_ROOTS:
        rel = Path(artifact_id)
        if artifact_id.startswith(key + "/"):
            rel = Path(artifact_id[len(key) + 1:])
            full = (root / rel).resolve()
            try:
                full.relative_to(root.resolve())
            except ValueError:
                return None
            if not full.is_file() or full.suffix != ".md":
                return None
            try:
                text = full.read_text(encoding="utf-8", errors="replace")
            except OSError:
                return None
            heading = _HEADING.search(text)
            identity = _parse_identity_table(text)
            return {
                "artifact_id": artifact_id,
                "title": heading.group(1).strip() if heading else full.stem,
                "artifact_type": _artifact_type(full.name),
                "path": str(full.relative_to(REPO_ROOT)).replace("\\", "/"),
                "modified": _mtime_iso(full),
                **identity,
                "content": text,
            }
    return None
