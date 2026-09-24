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


class StateError(RuntimeError):
    """ops-state is corrupt/unreadable — FAIL CLOSED (R0.3 §6). An existing
    malformed/truncated/unreadable state is NEVER interpreted as 'no lock';
    callers must HOLD (G0 -> STATE_CORRUPT, manifest generation HOLD, real P1
    HOLD, recovery HOLD unless a safe path reads valid state)."""


def load_state() -> dict:
    """Fail-closed ops-state read (R0.3 §6).

    Missing file -> fresh {} (bootstrap explicitly allowed: the first write
    creates authoritative state). Existing file that is malformed JSON,
    truncated, unreadable, a wrong top-level type, or structurally malformed
    raises StateError — the caller must fail closed, never silently continue
    with {}. Covers: promotion_pending_manifest_id, last_promoted_ops_sha,
    approval receipt, recovery state.
    """
    p = state_dir() / "ops-state.json"
    if not p.exists():
        return {}
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as e:
        raise StateError(f"ops-state unreadable: {e}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise StateError(f"ops-state malformed JSON: {e}")
    if not isinstance(data, dict):
        raise StateError(f"ops-state wrong top-level type: {type(data).__name__}")
    for key in ("ops_sync_base_sha", "last_promoted_ops_sha",
                "promotion_pending_manifest_id", "approved_manifest_id",
                "approved_manifest_sha256", "pending_p1_manifest_id",
                "pending_p1_manifest_sha256", "pending_p1_local_commit_sha"):
        if key in data and not isinstance(data[key], str):
            raise StateError(
                f"ops-state key {key!r} is not a string: {type(data[key]).__name__}")
    return data


def save_state(state: dict) -> None:
    """ATOMIC ops-state persistence (R0.3 §7): deterministic same-directory
    temp file -> flush -> fsync -> atomic os.replace. The previous valid state
    survives until replacement succeeds; an interrupted write never leaves
    partial/truncated authoritative state."""
    p = state_dir() / "ops-state.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(f"ops-state.json.tmp.{os.getpid()}")
    data = json.dumps(state, indent=2, sort_keys=True).encode("utf-8")
    fd = os.open(str(tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, p)


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


# ---- Founder approval receipt (R0.3 §3) -------------------------------------
def approval_receipt() -> tuple[str, str] | None:
    """(approved_manifest_id, approved_manifest_sha256) — the external receipt
    binding Founder approval to ONE exact deterministic batch. A mutable
    'disposition = APPROVED' string inside the manifest is never sufficient."""
    st = load_state()
    mid, dig = st.get("approved_manifest_id"), st.get("approved_manifest_sha256")
    return (mid, dig) if mid and dig else None


def set_approval_receipt(manifest_id: str, digest: str) -> None:
    st = load_state()
    st["approved_manifest_id"] = manifest_id
    st["approved_manifest_sha256"] = digest
    save_state(st)


def clear_approval_receipt() -> None:
    st = load_state()
    st.pop("approved_manifest_id", None)
    st.pop("approved_manifest_sha256", None)
    save_state(st)


# ---- pending-P1 recovery identity (R0.3 §9) ---------------------------------
_PENDING_P1_KEYS = ("pending_p1_manifest_id", "pending_p1_manifest_sha256",
                    "pending_p1_local_commit_sha")


def pending_p1_record() -> dict:
    """Recorded recovery identity written on push failure: manifest id + immutable
    digest + exact local promotion commit. Recovery requires all three exact
    matches — identity is never inferred from current HEAD alone."""
    st = load_state()
    return {k: st[k] for k in _PENDING_P1_KEYS if k in st}


def set_pending_p1_record(manifest_id: str, digest: str, local_commit: str) -> None:
    st = load_state()
    st.update({"pending_p1_manifest_id": manifest_id,
               "pending_p1_manifest_sha256": digest,
               "pending_p1_local_commit_sha": local_commit})
    save_state(st)


def clear_pending_p1_record() -> None:
    st = load_state()
    for k in _PENDING_P1_KEYS:
        st.pop(k, None)
    save_state(st)


# footer: 2026-09-24 15:30 UTC+7 (R0.3 fail-closed state + atomic persistence + approval receipt + recovery identity)