# C5 — Old Repo-Kanban Governance Supersession (M7B) (13 Aug 2026)

> Correction pass C5 per Founder directive. Final invariant:
> **ONE active work-state contract = Hermes Capital Intelligence board.**

## Superseded / updated artifacts

| Artifact | Action |
|---|---|
| `operational/hermes-organization/KANBAN-CONTRACT-v0.1.md` | ⛔ SUPERSEDED banner (FD #106 + C5) — HISTORY ONLY for field semantics / Hold concept / 11-column record. Write/commit instructions retired. |
| `operational/hermes-organization/AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md` | Status line updated — work-state mechanics superseded; holds path → `evidence/organization/holds/`; 11-column list marked LEGACY (Hermes native statuses listed) |
| `operational/hermes-organization/installation/PROFILE-STARTUP-CONTRACT.md` | Startup steps 3-4 updated — Holds (historical) path + Hermes board (`hermes kanban list/create`) |
| `operational/hermes-organization/AUTHORITY-MATRIX-v0.1.md` | Hold records path → `evidence/organization/holds/` (historical), active work-state = Hermes board |
| `operational/hermes-organization/ROLE-REGISTRY-v0.1.md` | Status banner — work-state = Hermes board; FD amendment rows marked historical records, not write-path instructions |
| `operational/hermes-organization/roles/11-radar-scout/PRINCIPAL.md` | **ACTIVE role contract updated** — cards = Hermes board tasks (`[RADAR][INBOX]`, `--triage`, date-keyed); digests → `evidence/radar/digests/`; ZERO writes to frozen repo-board tree |
| `backend/org_store.py` + `backend/api/org_routes.py` | Docstrings + HOLDS_DIR → `evidence/organization/holds/` (C4) |
| `operational/hermes-organization/kanban/board.md` | FROZEN note extended — C4 relocation record |
| `AGENTS.md` | No active old-board writer instruction (references are historical FD checkpoints — preserved as history) |
| Cron prompts `8ba233e88015` / `cda817d17236` | Rewritten (C3) — board tasks only, digest → `evidence/radar/digests/`, explicit frozen-tree boundary |

## Verified scan targets (per Master Integration Prompt v1.1 M7B list)

KANBAN-CONTRACT-v0.1.md ✅ · AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md ✅ ·
installation/PROFILE-STARTUP-CONTRACT.md ✅ · DAILY-WEEKLY-WORKFLOW-v0.1.md
(no board-write paths — Founder Review Pack concept retained as-is) ✅ ·
role contracts (11-radar-scout updated; others reference org governance only) ✅ ·
AGENTS.md (historical checkpoints only) ✅ · API/UI docs/tests (org_store/org_routes
updated; locked tests updated in C6) ✅

## Invariant

Remaining `kanban/digests` / `kanban/cards` / `kanban/holds` strings exist ONLY in
historical records (KANBAN-CONTRACT under its SUPERSEDED banner; ROLE-REGISTRY FD
amendment rows under the C5 banner; AGENTS.md checkpoints). No active instruction
teaches a reader to create repo-board cards/digests/holds or to treat the old
11-column state machine as live.

Historical meaning preserved through git history — no second active governance
contract created.

<!-- 2026-08-13 15:55 UTC+7 -->
