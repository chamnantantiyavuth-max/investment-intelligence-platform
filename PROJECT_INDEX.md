# Project Index — Investment Intelligence Platform

> Thin Project Bootstrap entrypoint. Read this file and `PROJECT_STATE.md` before opening the full repository.

## Bootstrap contract

- Read: `PROJECT_STATE.md`, this file, `AGENTS.md`, and `PROJECT_BIBLE.md`.
- `PROJECT_BIBLE.md` is an alias to `01-PROJECT-DNA.md`; do not read the authoritative Bible in full during bootstrap.
- Delegate Gate 0 as a read-only fresh-eyes audit. The child may read full governance documents in its isolated context.
- Do not implement, run broad tests, repair stale docs, or generate a full plan from `เริ่ม IIP` alone.

## Authority map

1. `02-PROJECT-CONSTITUTION.md` and approved amendments
2. `operational/FOUNDERS-DECISIONS.md`
3. `01-PROJECT-DNA.md` and approved domain specifications
4. Approved ADRs and implementation plans
5. AI suggestions

## Targeted navigation

| Need | Read only these first |
|---|---|
| Current phase and restrictions | `PROJECT_STATE.md`, `AGENTS.md` |
| Product DNA and constitutional rules | `PROJECT_BIBLE.md` → `01-PROJECT-DNA.md`, `02-PROJECT-CONSTITUTION.md` |
| Founder decisions | `operational/FOUNDERS-DECISIONS.md` |
| Domain entities and rules | `DOMAIN_MODEL.md`, `project-definition/` |
| Acceptance and verification | `ACCEPTANCE_EXAMPLES.md`, `operational/VERIFICATION-DOCTRINE.md` |
| Phase-specific work | Relevant phase document named by `PROJECT_STATE.md` |

## Repository

- Root: `C:/Users/Admin/Desktop/Antigravity/investment-intelligence-platform/`
- Vault notes: `C:/Users/Admin/AppData/Local/hermes/vault/09-Agent/project-notes/investment-intelligence-platform/`

## Lifecycle maintenance

- No-op session with no verified change, new FD, or phase transition: leave both files untouched.
- Session close: update `PROJECT_STATE.md` with verified outcome, evidence, blockers, latest FD, next action, and `last_verified`.
- Phase close: update `PROJECT_STATE.md` with gate/evidence/risks; update this index only if canonical authority or targeted navigation changed.
- Use shared skill `project-state-sync`; keep both files under 5,000 characters.
