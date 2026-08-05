# Runtime Verification Checklist

**Status:** PROPOSED OPERATIONAL STANDARD — FD #54 (2026-08-05)
**Version:** 0.1
**Usage:** run per stage; record results in `evidence/organization/RUNTIME-VERIFICATION-2026-08-05.md`.

## Stage 1 — Docs (standard/matrix/workflow/kanban/registry)

- [ ] No "Organization Constitution" title anywhere under `operational/hermes-organization/` (renamed — F-01)
- [ ] No flat `governance_state` field; `approval_status` + `monitoring_status` both present (two axes — F-02)
- [ ] No pack "Research Lifecycle State" values (Observation/Hypothesis/Draft/Reviewed/Validated/…) as a state model (F-05)
- [ ] Constitution §21 referenced by the standard's amendment rule (§15)
- [ ] Hold semantics state "org-workflow scope only, FD #54 Q2"
- [ ] No template `04-DEEP-DIVE-RESEARCH-PAPER`, no `05-THEME-HYPOTHESIS-CARD` (rejected — F-06/F-07)
- [ ] CIW boundary clause present in Equity role (F-09)
- [ ] Sol Medium routing present in Internal Auditor role (F-11)

## Stage 2 — Roles and Templates

- [ ] Every `roles/*/PRINCIPAL.md` has: authority boundary, permitted evidence, prohibited actions, input/output contract, deterministic dependencies, provenance, failure behavior, escalation, review requirements (Constitution §23.5)
- [ ] Every `roles/*/ASSISTANT.md` carries the label contract + prohibition envelope
- [ ] Every template maps to a canonical source (templates/README.md)
- [ ] Zero "portfolio" / "holdings" / "cost basis" / "position size" data grants anywhere in role contracts
- [ ] `iip` profile untouched (bootstrap/control preserved)

## Stage 3 — Installation Docs

- [ ] HERMES-PROFILE-MAPPING paths match the real runtime (AppData\Local\hermes\profiles)
- [ ] PROFILE-STARTUP-CONTRACT present
- [ ] Kanban bootstrap (board/cards/holds) present

## Stage 4 — Profiles (runtime)

- [ ] `hermes profile list` shows 10 org-* profiles (18 total)
- [ ] `sync-governance.py` re-run idempotent; no drift for existing profiles
- [ ] Existing 8 profiles' SOUL.md content-hash unchanged vs pre-install
- [ ] Sample profile loads config: `hermes --profile org-cos config get model.default` = deepseek-v4-flash
- [ ] New profile SOUL = canonical core + role context splice (BEGIN/END intact)
- [ ] No `.env`/auth material in any org-* profile

## Stage 5 — Dry-Run Pilot (Option C, zero profiles)

- [ ] 5-role simulation on `docs/ciw-pilot-msft/research-result.md` v1 (published, hash 34a1f324…)
- [ ] 5/5 handoffs named owner + inputs + outputs + next state
- [ ] 3/3 memos trace claims to the published result's source map (no fabricated references)
- [ ] 2/2 Holds recorded + cleared by issuing role only
- [ ] Dissent preserved after simulated Founder approval
- [ ] Packet failed once as ADMINISTRATIVELY INCOMPLETE, re-passed after defect fix
- [ ] Zero canonical state changes; zero CIW-path work; zero cron; portfolio-blind verified

## Evidence Tags

TEST_VERIFIED (commands executed) · STATIC_OBSERVATION (docs inspection) · INFERENCE (mapping claims) — per Verification Doctrine closeout.
<!-- 2026-08-05 14:55 UTC+7 -->
