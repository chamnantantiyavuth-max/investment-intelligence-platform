"""Single authority for C+ ops/automation configuration: allowlists, denylist, paths, state.

All patterns are ANCHORED (fullmatch) against POSIX-relative paths from the ops worktree
root. A malformed or unknown path FAILS CLOSED — patterns are never widened to make a
run pass (FD #142, POST-M5.3 O3 Final Ruling, allowlist section).
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

OPS_BRANCH = "ops/automation"

DEFAULT_OPS_WORKTREE = r"C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform-ops"
DEFAULT_REPO = r"C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform"
DEFAULT_MANIFEST_DIR = "ops/manifests"

# Job -> anchored artifact allowlist (fullmatch). Learning Loop = observer only -> EMPTY.
JOB_ALLOWLISTS: dict[str, list[str]] = {
    "8ba233e88015": [  # IIP Weekly Radar Scan (FD #78)
        r"^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-digest\.md$",
    ],
    "cda817d17236": [  # IIP Radar Mid-Week Watch (FD #80)
        r"^evidence/radar/digests/\d{4}-\d{2}-\d{2}-radar-midweek\.md$",
    ],
    "8b1cd19aba7d": [  # ciw-msft-class-a-monitor
        r"^docs/ciw-pilot-msft/monitoring/\d{4}-\d{2}-\d{2}-monitoring-draft\.md$",
    ],
    "73e611584447": [  # Nick-Weekly AM pipeline (Self-Reflection Log)
        r"^operational/self-reflection-logs/\d{4}-\d{2}-\d{2}-run-AM-V0-\d{8}-\d{6}\.md$",
    ],
    "1f5f03f9236d": [],  # Learning Loop: OBSERVER ONLY — NO REPOSITORY OUTPUT
}

JOB_NAMES = {
    "8ba233e88015": "IIP Weekly Radar Scan",
    "cda817d17236": "IIP Radar Mid-Week Watch",
    "8b1cd19aba7d": "ciw-msft-class-a-monitor",
    "73e611584447": "Nick-Weekly AM Pipeline",
    "1f5f03f9236d": "IIP Daily Learning Loop",
}

# Absolute denylist (fullmatch, prefix rules). A denylist hit FAILS CLOSED and an
# allowlist PASS never overrides it (FD #142 §8).
DENYLIST_PATTERNS: list[str] = [
    r"^PROJECT_STATE\.md$",
    r"^SESSION_CLOSEOUT\.md$",
    r"^AGENTS\.md$",
    r"^README\.md$",
    r"^operational/FOUNDERS-DECISIONS\.md$",
    r"^operational/hermes-organization/",
    r"^project-definition/",
    r"^design/",
    r"^reports/",
    r"^qad/",
    r"^tests/",
    r"^frontend/",
    r"^backend/",
    r"^\.github/",
    r"^package.*\.json$",
    r"^contract/",
    r"^model-routing",
    r"^docs/.*\.env",
    r".*\.env$",
    r".*\.pem$",
    r".*\.key$",
    r".*id_rsa.*",
    r"^ops/manifests/",  # manifests are interactive-only (P1 review), never cron writes
]

_COMPILED_ALLOW: dict[str, list[re.Pattern]] = {
    jid: [re.compile(p) for p in pats] for jid, pats in JOB_ALLOWLISTS.items()
}
_COMPILED_DENY: list[re.Pattern] = [re.compile(p) for p in DENYLIST_PATTERNS]


def normalize_rel(path: str) -> str:
    """POSIX-relative path from worktree root; reject absolute/outside escapes."""
    p = path.replace("\\", "/")
    p = p.lstrip("./")
    if p.startswith("/") or p == ".." or p.startswith("../") or ":" in p.split("/")[0]:
        raise ValueError(f"path escapes worktree root: {path!r}")
    return p


def is_denied(rel: str) -> bool:
    rel = normalize_rel(rel)
    return any(p.fullmatch(rel) for p in _COMPILED_DENY)


def allowed_for(job_id: str, rel: str) -> bool:
    """Allowlist fullmatch; empty allowlist = nothing is allowed (fail closed)."""
    rel = normalize_rel(rel)
    pats = _COMPILED_ALLOW.get(job_id)
    if pats is None:
        raise KeyError(f"unknown job id {job_id!r}")
    if not pats:
        return False
    return any(p.fullmatch(rel) for p in pats)


def owning_jobs(rel: str) -> list[str]:
    """ALL job ids whose anchored allowlist fullmatches rel, in config order.

    Mechanical path-authority derivation for multi-job P1 manifests (R0.1 87):
    exactly one match = the owning job; zero = unknown (FAIL CLOSED); more than
    one = ambiguous ownership (FAIL CLOSED).
    """
    rel = normalize_rel(rel)
    return [jid for jid in JOB_ALLOWLISTS if allowed_for(jid, rel)]


def job_exists(job_id: str) -> bool:
    return job_id in JOB_ALLOWLISTS


# ---- state (outside the worktree; never part of the repo) -------------------
def state_dir() -> Path:
    env = os.environ.get("OPS_STATE_DIR")
    if env:
        return Path(env)
    home = os.environ.get("HERMES_HOME") or str(Path.home() / "AppData/Local/hermes/profiles/iip")
    return Path(home) / "ops-state"


def load_state() -> dict:
    p = state_dir() / "ops-state.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_state(state: dict) -> None:
    p = state_dir() / "ops-state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


# ---- promotion-pending lock (R0.2 §14) --------------------------------------
def promotion_pending() -> str | None:
    """promotion_pending_manifest_id — external operational flag (NOT a repo
    governance write). When set, artifact-cron preflight / G0 FAILS CLOSED until
    a verified REAL P1 promotion clears it or the manifest is explicitly
    cancelled/disposed. Makes 'jobs are paused during Founder P1 review'
    mechanical rather than merely procedural."""
    return load_state().get("promotion_pending_manifest_id")


def set_promotion_pending(manifest_id: str | None) -> None:
    state = load_state()
    if manifest_id is None:
        state.pop("promotion_pending_manifest_id", None)
    else:
        state["promotion_pending_manifest_id"] = manifest_id
    save_state(state)


# footer: 2026-09-24 13:45 UTC+7 (R0.2 promotion-pending lock helpers)