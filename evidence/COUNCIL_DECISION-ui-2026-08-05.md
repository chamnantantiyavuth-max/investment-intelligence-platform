# COUNCIL DECISION

## Gate
Visual Council — Research Workflow UI (UI-1 + UI-2, FD #55/#56) — rounds 1→3, 2026-08-05

## Verdict
**PASS** (round 3 — final focused retest, HEAD-bound at `d9e0abd`)

## Rounds History

| Round | Verdict | Findings | Disposition |
|---|---|---|---|
| 1 | RETEST | 7 material findings: Briefing provenance labels; client-clock as-of; annotated expected_artifact link break; Material Changes unpaired + false-empty; hidden Founder transition; Validation/Data Quality generic empty; 404 conflated with API failure | All 7 remediated + browser re-verified (VISUAL_QA.md remediation table) |
| 2 | RETEST | 2 findings: stamps lacked as-of on 3 of 4 Briefing sections; /org-queue + founder-record failures silently degraded | All 2 remediated: admitted as-of on every stamp (Holds = "as-of unavailable", no timestamp field in hold YAML); queueDown + recordsQ failed[] scoped errors with Retry |
| 3 | PASS | None | — |

## Round 3 Decision (verbatim from Sol Medium, 2026-08-05)

### Material Findings
1. None. The four Briefing stamps render correctly and honestly in `01-briefing-desktop.png`: Decisions and Throughput use the admitted latest card update (`as-of 2026-08-05`); Material Changes uses the latest registry modification (`as-of 2026-08-05T15:00:13`); Holds reports `2 recorded · as-of unavailable`, correctly reflecting the absence of hold timestamps. Source wiring is confirmed in `DashboardPage.tsx:148-151,201,215,258,292`.
2. The scoped failure remediations are present and correctly wired in `ResearchArtifactDetailPage.tsx`: `queue.isError` drives affected-section error messages and `queue.refetch()` actions in Validation and Data Quality (`82-83,230-266`); founder-record fetches preserve failed IDs and Decision History renders a scoped warning plus `recordsQ.refetch()` (`56-75,302-318`).
3. No new material regression was found in the four committed screenshots. Research Desk retains admitted freshness and the `OPEN →` action; artifact detail retains identity/state and correctly scoped related artifacts; Decision History retains the Founder publication transition. Production build passed, lint completed with 0 errors and 7 pre-existing Fast Refresh warnings.
4. HEAD-bound evidence is sufficient: HEAD remained `d9e0abd`, `git status --short` was empty before and after verification, and all reviewed screenshots, source files, and `VISUAL_QA.md` matched their HEAD blob identities.

### Required Changes
1. None.

### Evidence Gaps
- None

### Founder Decisions Required
- None

### Minority Warning
- None

### Scope Expansion Check
- No scope expansion detected — the review remained bounded to the two round-2 remediations and regression/evidence-integrity checks. No files were created or modified.

---

*Council run: 3 rounds via llm-council (delegate_task → gpt-5.6-sol, openai-codex). Evidence: `evidence/ui/research-workflow/` (screenshots 01–04 + VISUAL_QA.md) at HEAD `d9e0abd`. Parent re-verify: backend suite 309/309, `npm run build` exit 0, lint 0 errors, console 0 JS errors, ad-hoc hermes-verify 12/12 (R1) + 11/11 (R2).*
<!-- 2026-08-05 17:05 UTC+7 -->
