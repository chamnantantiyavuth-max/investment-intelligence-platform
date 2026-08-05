# Hermes Profile Mapping (Installation)

**Status:** PROPOSED OPERATIONAL STANDARD — FD #54 (2026-08-05)
**Version:** 0.1
**Runtime facts verified 2026-08-05:** profiles live under `C:\Users\Admin\AppData\Local\hermes\profiles\` (NOT `~/.hermes/profiles/`); profile = flat copy of canonical `shared\SOUL.md` + spliced `shared\project-context\<profile>.md` (composed by `sync-governance.py`); skills dir is a junction to `skills-shared`; per-profile `memories\{MEMORY,USER}.md`; `config.yaml` per profile (iip's used as base); `profile.yaml` optional (description only). No inheritance/includes/symlinks beyond the skills junction.

## Installed Principal Profiles (10 — thin; FD #54 Q1)

| Role | Profile dir | project-context file |
|---|---|---|
| Founder Chief of Staff | `org-cos` | `shared/project-context/org-cos.md` |
| Investment Committee Secretary | `org-ic-secretary` | `shared/project-context/org-ic-secretary.md` |
| Commodity Product Analyst | `org-commodity-analyst` | `shared/project-context/org-commodity-analyst.md` |
| Global Macro Strategist | `org-macro-strategist` | `shared/project-context/org-macro-strategist.md` |
| Equity Alpha Analyst | `org-equity-analyst` | `shared/project-context/org-equity-analyst.md` |
| Options Strategist | `org-options-strategist` | `shared/project-context/org-options-strategist.md` |
| Chief Risk Officer | `org-cro` | `shared/project-context/org-cro.md` |
| Quant & Model Validator | `org-quant-validator` | `shared/project-context/org-quant-validator.md` |
| Data Steward | `org-data-steward` | `shared/project-context/org-data-steward.md` |
| Internal Auditor / Red Team | `org-auditor` | `shared/project-context/org-auditor.md` |

**Not installed:** 10 Assistant profiles (approved topology = bounded delegated subagents under Principals — FD #54 Q1/Q3). `iip` remains the project bootstrap/control profile (unchanged).

## Per-Profile Contents (thin)

1. `SOUL.md` — composed canonical shared SOUL + role context splice (BEGIN/END markers; same mechanism as all profiles).
2. `memories/USER.md` — Founder identity (shared user.md content).
3. `memories/MEMORY.md` — empty at install; operational notes only, NEVER domain truth (DNA-018).
4. `config.yaml` — copy of `iip/config.yaml` (identical model routing/toolsets; role profiles behave like iip).
5. `user.md` — Founder profile doc (copy of `iip/user.md`).
6. `skills` — junction to `C:\Users\Admin\AppData\Local\hermes\skills-shared` (shared skill library).
7. `.no-bundled-skills` — marker (consistent with existing profiles).
8. NO `.env`, NO `auth.json`, NO profile-specific credentials. Role profiles have zero secret material.

## Sync Extension (with backup — see Rollback)

- `sync-governance.py`: `PROFILES` list extended with the 10 `org-*` names (canonical SOUL + context compose keeps them current on future sync runs).
- `cross-profile-sync-watchdog.py`: `PROFILES` list extended with the same 10 (SOUL-core hash coverage).
- Backup of both scripts + `shared/` + sample configs taken at install: `C:\Users\Admin\Desktop\Antigravity\_staging\hermes-backup-20260805\`.

## Boot Verification (run at install)

1. `hermes profile list` → all 18 profiles present (8 existing + 10 org-*).
2. `sync-governance.py` re-run → idempotent, no drift report for existing profiles.
3. Existing 8 profiles' `SOUL.md` content-hash unchanged vs pre-install snapshot.
4. Sample profile config read: `hermes --profile org-cos config get model.default` → `deepseek-v4-flash`.
5. New profile SOUL contains role context between BEGIN/END markers; canonical core matches shared SOUL.

## Rollback (profile layer)

Restore from `_staging\hermes-backup-20260805\`: revert `sync-governance.py` + `cross-profile-sync-watchdog.py`, re-run sync (recomposes existing profiles to canonical), delete the 10 `org-*` profile dirs + 10 project-context files. Existing profiles are unaffected (they are never written by org-profile content).
<!-- 2026-08-05 14:55 UTC+7 -->
