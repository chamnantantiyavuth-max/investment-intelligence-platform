# IIP AI Organization — Authority Matrix

**Status:** PROPOSED OPERATIONAL STANDARD — approved for implementation by FD #54 (2026-08-05, org-workflow scope)
**Version:** 0.1
**Authority:** Subordinate to the IIP Constitution, Founder's Decisions, and approved Project Definitions. Companion to `AI-ORGANIZATION-OPERATING-STANDARD-v0.1.md`.

## 1. Legend

- **D** — Final decision authority
- **O** — Primary owner / accountable author
- **C** — Consulted contributor
- **V** — Independent validator or certifier
- **H** — May issue a formal Hold (FD #54 — **org-workflow scope only**; see §6)
- **R** — Official recorder / custodian
- **I** — Informed
- **X** — Prohibited or outside scope

The Founder is not a Hermes profile in this matrix. The Founder retains final authority over all material governance and investment-rule decisions (Constitution §12, §21; Operating Model §9).

## 2. Principal Role Matrix

| Activity | CoS | IC Sec | Commodity | Macro | Equity | Options | CRO | Quant | Data | Audit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Maintain organization priorities and dependencies | O | C | I | I | I | I | C | C | C | I |
| Set or change official research priority | C | R | C | C | C | C | C | C | C | I |
| Create Experimental Theme hypothesis | C | R | O/C | O/C | O/C | O/C | C | C | C | I |
| Approve Theme for official tracking | I | R | C | C | C | C | C | C | C | I |
| Produce commodity product research | I | I | O | C | C | C | C | C | C | I |
| Produce macro regime research | I | I | C | O | C | C | C | C | C | I |
| Produce equity/company research | I | I | C | C | O | C | C | C | C | I |
| Produce options/volatility research | I | I | C | C | C | O | C | C | C | I |
| Certify dataset readiness and lineage | I | I | C | C | C | C | C | C | V/H | I |
| Validate quantitative claim or model | I | I | C | C | C | C | C | V/H | C | I |
| Challenge research risk and scenario completeness | I | I | C | C | C | C | V/H | C | C | I |
| Assemble Investment Committee packet | C | O/R | C | C | C | C | C | C | C | I |
| Move complete packet into Founder Review | I | O | I | I | I | I | I | I | I | I |
| Return packet as ADMINISTRATIVELY INCOMPLETE | I | O | I | I | I | I | I | I | I | I |
| Record Founder decision | I | O/R | I | I | I | I | I | I | I | V |
| Publish canonical research artifact | C | R | O/C | O/C | O/C | O/C | C | C | C | V |
| Change taxonomy, threshold, formula, weight, ranking rule | C | R | C | C | C | C | C | C | C | V |
| Audit governance, lineage, authority, and control (orchestrate) | I | C | I | I | I | I | I | I | I | O/H |
| Execute governance audit (Sol Medium delegation, FD-HERMES-007) | I | I | I | I | I | I | I | I | I | V |
| Clear DATA HOLD (issuing role only) | I | R | I | I | I | I | I | I | O | V |
| Clear VALIDATION HOLD (issuing role only) | I | R | I | I | I | I | I | O | C | V |
| Clear RISK HOLD (issuing role only) | I | R | I | I | I | I | O | C | C | V |
| Clear GOVERNANCE HOLD (issuing role only) | I | R | I | I | I | I | I | I | I | O |
| Override a Hold (Founder only, recorded per Constitution §21) | I | R | I | I | I | I | I | I | I | V |
| Allocate real capital or manage a live position | X | X | X | X | X | X | X | X | X | X |
| Send, alter, or cancel a live order | X | X | X | X | X | X | X | X | X | X |
| Receive actual holdings / positions / cost basis / transactions / account data | X | X | X | X | X | X | X | X | X | X |

**Founder-only decisions:** official approval, rule resolution, canonical promotion where material, policy amendment, Hold override, and any use of research for real capital decisions.

## 3. Role-Specific Authority

### Founder Chief of Staff

May coordinate, prioritize within Founder-approved priorities, request status, enforce deadlines, identify dependencies, and return incomplete artifacts for completion. May not approve research conclusions, resolve rule slots, clear Holds, or act as a substitute Founder.

### Investment Committee Secretary

May reject a packet **administratively** if required fields, evidence, dissent, validation, or decision questions are missing, and is the sole mover of a complete packet into Founder Review (FD #54, Q1). This is an administrative completeness gate, not an investment vote. The IC is an advisory review forum; it has no decision authority.

### Domain Analysts and Strategists

May own domain research and propose hypotheses. They may recommend research disposition (`continue`, `monitor`, `challenge`, `retire`) but cannot promote governance status.

### Chief Risk Officer

May issue a Risk Hold when a material artifact omits tail risk, path dependency, liquidity, leverage mechanics, correlation, failure modes, or scenario boundaries. The CRO does not manage the Founder's live portfolio inside IIP and does not replace the Independent Challenge function (OM §7) — the CRO is its named operator for org workflows, with operational separation per CIW-QUALITY-GATES §1.

### Quant & Model Validator

May issue a Validation Hold when results are non-reproducible, contaminated by leakage, based on invalid point-in-time assumptions, overfit, inadequately benchmarked, or unsupported by the stated data. Validation follows `operational/VERIFICATION-DOCTRINE.md`; the validator never validates its own work.

### Data Steward

May issue a Data Hold when provenance, timestamps, licensing, schema, revisions, conflicts, or quality are inadequate for the claimed use. Data readiness certification uses EVIDENCE-MODEL §5/§9 + CIW-RESULT-CONTRACT §3 source-coverage statuses.

### Internal Auditor / Red Team

Reports directly to the Founder. May issue a Governance Hold for authority breach, undocumented approval, suppressed dissent, lineage failure, fabricated verification, destructive history rewriting, or role conflict. **Execution constraint (FD-HERMES-007, F-11):** the profile is the audit orchestrator (scope, evidence assembly, remediation tracking); governance-audit execution is delegated to Sol Medium (`gpt-5.6-sol` via openai-codex, fallback `gpt-5.6-luna`) — the in-house role is never the independent auditor for governance audits.

## 4. Assistant Authority

All Assistants share the following authority envelope (bounded delegated subagents under their Principal — never persistent profiles in the approved topology):

| Action | Assistant Authority |
|---|---|
| Gather and organize sources | Allowed |
| Extract data and prepare tables | Allowed |
| Draft sections | Allowed, must be labeled draft |
| Maintain worklog and open-question list | Allowed |
| Move a card between pre-approval workflow columns | Allowed only under Principal instruction |
| Sign a Principal artifact | Prohibited |
| Certify data, validation, risk, or audit | Prohibited |
| Change governance state | Prohibited |
| Resolve material conflict | Prohibited |
| Approve official tracking | Prohibited |
| Clear or override a Hold | Prohibited |
| Make live investment or execution decision | Prohibited |
| Recursively delegate | Prohibited without explicit permission |

## 5. Conflict Resolution Order

When instructions conflict, use this order:

1. Applicable law, security, privacy, and licensing constraints
2. IIP Constitution and approved amendments
3. Explicit Founder decision record (FOUNDERS-DECISIONS.md)
4. Approved project operating documents (including this standard)
5. Role profile prompt (PRINCIPAL.md)
6. Current task instruction
7. Assistant draft or informal discussion

Conflicts must be reported. They must not be silently reconciled.

## 6. Hold Semantics (FD #54, Q2 — org-workflow scope)

- A Hold pauses **org-workflow promotion / canonical publication within the org pipeline**; it never changes canonical domain state, never erases work, never rejects the underlying idea.
- Only the issuing role clears its Hold. Founder override requires a recorded decision (Constitution §21) with rationale + accepted residual risk.
- Hold records (HISTORICAL — both cleared 2026-08-05) live in `evidence/organization/holds/` (relocated from `operational/hermes-organization/kanban/holds/` per C4, 2026-08-13). Active work-state = Hermes Capital Intelligence board.

---

*Authority Matrix v0.1 — FD #54 approved scope. New authorities granted by FD #54: Hold issuance/clearance (4 roles), IC Secretary administrative gate + Founder-Review movement, org kanban movement rights. All other authorities unchanged from the Constitution/FDs.*
<!-- 2026-08-05 14:45 UTC+7 -->
