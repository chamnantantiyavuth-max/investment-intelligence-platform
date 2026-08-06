# Council Artifact — Plan (Lite) — 2026-08-06

- **Gate:** Plan Council (Lite — 3 review roles: governance/process, domain/architecture, portfolio/simulation risk)
- **Subject:** `docs/RECONSTITUTION-PLAN-v0.1.md` (IIP AI-Native Research Organization + Independent Portfolio Manager reconstitution)
- **Reviewed against:** `ChatGPT/IIP_AI_Native_Research_and_Independent_PM_Direction_v0.1.md`
- **Council:** gpt-5.6-sol (openai-codex), one independent subagent via `delegate_task` (deleg_c291e43b), 2026-08-06 13:57–14:02 UTC+7
- **Disposition:** Verdict **PASS WITH FIXES** — 3 material findings; all fixes applied by Parent to plan **v0.2** (new §3.6 Governance Authority Map, §3.4 spec-authority disposition, §6.1 Minimum Simulated-Ledger Contract, expanded D-3/D-5/D-6, §11 verification additions). Founder decisions D-1..D-10 presented for approval one at a time.

---

# COUNCIL DECISION

## Gate
Plan (Lite)

## Verdict
PASS WITH FIXES

## Material Findings
1. **The plan does not identify the higher-authority amendments required by the reconstitution.** Plan §3.2 proposes keeping the Constitution and Project DNA unchanged or only lightly touched, while plan §9 D-6 addresses only the Blind Portfolio Rule, no-live-trading, and no-AI-invented-rules. The new direction conflicts materially with Constitution §§1–3, 17–18, 20, and 23.2; Project DNA DNA-001, DNA-004, DNA-018, and DNA-020; and the current AGENTS.md prohibitions on portfolio allocation. In particular, direction §§11–17 authorize an AI Portfolio Manager to make simulated allocation and transaction decisions, whereas the current governing documents prohibit AI from autonomously deciding what to buy, sell, or allocate. Without an explicit scoped amendment under Constitution §21, approval of plan D-5/D-6 would leave the IPM unauthorized and the repository governed by contradictory current-purpose and source-of-truth rules.
2. **The proposed retirement of checklist-driven requirements is not authoritative enough to displace the existing approved specifications.** Plan §3.3 says the nine domain specifications remain textually unchanged as references and QA checklists, while §3.4 says their mandatory-field requirements will be retired from the active research path. Under AGENTS.md's authority hierarchy, approved domain specifications outrank an implementation plan; an operational statement cannot demote their mandatory requirements. This conflicts with direction §§2, 5–6, and 19 and could allow the old pipeline/checklist structure to remain binding on research essays.
3. **The USD 200,000 simulated-ledger design does not yet explain how the ledger will be maintained.** Plan §6 states only that the ledger is the source of truth and distinguishes idea, eligibility, simulated order, and simulated fill. It does not define the opening balance, append-only transaction/correction record, cash and position reconciliation, simulated-fill basis, valuation treatment, fees/FX/multipliers, or tracking of reserves and committed obligations required by direction §§13.4, 14, 17, and 19. Without a minimum accounting contract, the Founder cannot verify that the simulated office remains within USD 200,000, that portfolio letters agree with holdings and cash, or that derivatives and multi-currency exposures are represented consistently.

## Required Changes
1. **Correct the governance classification and expand D-6:** identify the Constitution, Project DNA, AGENTS.md, and approved-decision clauses that must be retained for frozen legacy scope, amended for the research organization, or given a narrowly bounded simulated-IPM exception. Preserve the prohibitions on live orders, real-account access, and autonomous use of real capital. **Verification:** a clause-level authority map shows every affected clause as Retained, Legacy-Scope Only, Amended, or Superseded, with an explicit Constitution §21 Founder decision and no unresolved contradiction between the IPM mandate and higher-authority documents.
2. **Give the research-path demotion of mandatory fields explicit authority:** state that approved platform/domain specifications continue governing frozen legacy modules but are non-binding analytical lenses or QA references for the new research workflow; identify the active role prompts, templates, and report contracts from which checklist-shaped output mandates will be retired. Do not rewrite the specifications into a new checklist. **Verification:** the amended plan assigns one authority status to each affected artifact class, and the implementation verification confirms that no active research contract requires fixed analytical sections, scores, pass/fail conclusions, or all-role participation.
3. **Add a minimal simulated-ledger contract to plan §6 and its Founder decision:** specify USD 200,000 opening cash; append-only simulated transactions and corrections; deterministic derivation and reconciliation of cash, positions, realized/unrealized results, reserves, and committed obligations; required instrument/IBKR-verification, currency, multiplier, expiry, quantity, simulated-fill, fee, FX, timestamp, and decision-letter references; and a fail-closed rule forbidding ledger entry when eligibility evidence is missing. Explicitly exclude broker credentials, live-account data, and live-order connectivity. **Verification:** a no-trade opening ledger reconciles to USD 200,000, and one representative multi-currency or derivative simulation reconciles journal, cash, position, obligations, and letter references without any live-order path.

## Evidence Gaps
- None

## Founder Decisions Required
1. Expand D-6 into an explicit scoped constitutional/DNA amendment or exception for autonomous decisions inside the simulated office only, while retaining the prohibition on live trading and real-capital authority.
2. Approve the authority disposition of existing approved domain specifications for the new research path: binding for frozen legacy modules, non-binding research lenses/QA references for free-form research outputs.
3. Expand D-5 to approve the minimum simulated-ledger accounting, valuation, reconciliation, and simulated-fill policy.

## Minority Warning
- None

## Scope Expansion Check
- none

<!-- 2026-08-06 17:55 UTC+7 -->
