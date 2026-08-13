# C4 — Relocation of Formal Holds + Durable Non-Board History (13 Aug 2026)

> Correction pass C4 per Founder directive: nothing durable may depend on the
> old `kanban/` tree surviving Stage 8.

## Inventory + classification

| Item | Classification | Disposition |
|---|---|---|
| `kanban/holds/HOLD-DATA-001.yaml` | DURABLE GOVERNANCE HISTORY (status CLEARED 2026-08-05 — not an active hold) | → `evidence/organization/holds/HOLD-DATA-001.yaml` (git mv) |
| `kanban/holds/HOLD-RISK-001.yaml` | DURABLE GOVERNANCE HISTORY (status CLEARED 2026-08-05) | → `evidence/organization/holds/HOLD-RISK-001.yaml` (git mv) |
| `kanban/holds/README.md` | DURABLE GOVERNANCE HISTORY (hold schema doc) | → `evidence/organization/holds/README.md` (git mv) |
| `kanban/digests/2026-08-07-radar-digest.md` | DURABLE RESEARCH HISTORY | → `evidence/radar/digests/` (git mv) |
| `kanban/digests/2026-08-07-radar-midweek.md` | DURABLE RESEARCH HISTORY | → `evidence/radar/digests/` (git mv) |
| `kanban/digests/2026-08-10-radar-digest.md` | DURABLE RESEARCH HISTORY | → `evidence/radar/digests/` (git mv) |
| `kanban/digests/2026-08-13-radar-midweek.md` | DURABLE RESEARCH HISTORY | → `evidence/radar/digests/` (git mv) |
| `kanban/card-outcomes.md` | **ACTIVE GOVERNANCE** (FD #82 feedback-loop register — still consumed by the radar cron) | → `operational/hermes-organization/card-outcomes.md` (git mv — stays in the org pack, OUTSIDE the retired kanban tree) |
| `kanban/cards/ORG-2026-0001..0022.yaml` | OBSOLETE BOARD STATE (migration source, frozen) | stay in place until Stage 8 — semantic content preserved on the Hermes board tasks + git history |
| `kanban/board.md` | OBSOLETE BOARD STATE (frozen migration record) | stay until Stage 8; FROZEN note updated with C4 relocation record |

## Code / reference updates (no duplication of canonical evidence)

- `backend/org_store.py` — `HOLDS_DIR` → `evidence/organization/holds/`; docstring updated
  (hold records now HISTORICAL; legacy cards no longer read for live work-state);
  `CARDS_DIR` kept pointing at the frozen tree as read-only migration source
- `backend/api/org_routes.py` — endpoint docstring updated (`/org-holds` = historical
  records; Hermes board owns live work-state)
- `operational/hermes-organization/kanban/board.md` — FROZEN section records the C4
  relocation (nothing durable depends on this tree)
- Cron prompts (C3) + role 11 PRINCIPAL + STANDARD/AUTHORITY-MATRIX/ROLE-REGISTRY (C5)
  reference the new locations

## Active-hold check

Both HOLD-DATA-001 and HOLD-RISK-001 are **CLEARED** (2026-08-05, issuer-only
clearance + sign-off recorded) — no active hold needed a blocked-task linkage on
the Hermes board. If a future Hold is issued, the org-pack Hold semantics remain
(STANDARD §10) with records under `evidence/organization/holds/`.

## Verification

- `git mv` executed for all 8 files (tracked — history preserved)
- `ls evidence/radar/digests/` → 4 digests; `ls evidence/organization/holds/` →
  2 holds + README
- Old tree now contains ONLY: board.md + cards/ (22 YAML + README) — the migration
  source slated for Stage 8
- /org-holds still serves both holds (test_org_holds_shape passes — suite 206/206)

<!-- 2026-08-13 16:30 UTC+7 -->
