# IIP Hermes AI Organization — Operating Directory

**Status:** PROPOSED OPERATIONAL STANDARD — approved for implementation by FD #54 (2026-08-05, org-workflow scope)
**Version:** 0.1

This directory implements the approved IIP Hermes AI Workforce Runtime Model (FD #54, 2026-08-05; Q1 approved as proposed, Q2 Holds org-workflow-only, Q3 Option C zero-profile pilot). It is **subordinate to the IIP Constitution** and Founder's Decisions. Nothing here is canonical product/domain content; nothing here has constitutional standing.

## Authority hierarchy

1. IIP Constitution + approved amendments
2. Founder's Decisions (`operational/FOUNDERS-DECISIONS.md`, incl. FD #54)
3. Approved Project Definitions (incl. `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md`, `EVIDENCE-MODEL.md`, `THEME-MODEL.md`, `CANDIDATE-AND-QUEUE-MODEL.md`, CIW contracts)
4. Approved ADRs + implementation plans
5. **This directory (operational standard + role contracts)**
6. AI-generated proposals

## Contents

| File | Purpose |
|---|---|
| `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md` | Operating rules (renamed + corrected from the proposed pack constitution; F-01/F-02/F-05) |
| `AUTHORITY-MATRIX-v0.1.md` | Role/activity authority table incl. FD #54 grants (Holds, IC gate) |
| `DAILY-WEEKLY-WORKFLOW-v0.1.md` | Cadence; no cron without named authorization |
| `KANBAN-CONTRACT-v0.1.md` | Repo-based single board contract; canonical state fields |
| `ROLE-REGISTRY-v0.1.md` | 10 roles → profile mapping |
| `ROLE-MAPPING-v0.1.md` | Role → approved logical responsibility mapping (analysis) |
| `TEMPLATE-DISPOSITION-v0.1.md` | Template disposition (analysis) |
| `INTEGRATION-PLAN-v0.1.md` | Staged integration plan (analysis) |
| `roles/01..10/` | Principal + Assistant contracts (thin; canonical content in repo) |
| `templates/` | 13 mapped org forms (no duplicates of canonical artifacts) |
| `installation/` | Hermes profile mapping, startup contract, runtime verification checklist |
| `kanban/` | Repo-based board, cards, holds |

## Key boundaries (FD #54)

- **Portfolio-blind:** no role/Assistant receives holdings, positions, cost basis, transactions, or Capital Command data (Constitution §23.8.1).
- **State canonical-only:** Theme governance = two axes (Approval × Monitoring); no parallel state machines.
- **CIW remains paused:** bounded consumption of published results only; no CIW-path research/automation without a separate named FD.
- **Holds:** org-workflow scope only (FD #54 Q2) — never canonical state.
- **Assistants:** bounded delegated subagents, not profiles.
- **No cron** is authorized by this standard.

## Status

PROPOSED/IMPLEMENTED-ON-BRANCH `org-pack-v0.1` — pending Founder acceptance of the pre-merge review (diff + verification evidence + pilot). Nothing here is merged to `main`.
<!-- 2026-08-05 14:45 UTC+7 -->
