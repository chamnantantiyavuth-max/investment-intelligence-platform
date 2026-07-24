# Emergent Rule Proposals — 2024-07-24

**Authority:** Phase 6B (FD #28 deferred scope — now active per Founder direction)
**Source:** Patterns detected in Self-Reflection Log v0.2 + gap resolution session
**AI Intelligence Layer (§23) — Draft proposals, not constitutional until Founder-approved**

---

## ERP-001 (Revised): Sector Concentration Monitor

**Original (2024-07-23):** Flag when any sector exceeds 60% of candidates
**Revised (2024-07-24):** Deploy as monitoring rule (warn, not block) from Phase 8 onward

**Pattern detected:**
- V0 pre-gap: 80% Tech (4/5 themes)
- V0 post-gap: 90% Tech (9/10 queue entries)
- Healthcare: 10% (1/10)
- This is structurally expected — V0 was designed as Tech + Healthcare

**Proposed rule:**
```
WHEN any sector exceeds 70% of total candidates
AND pipeline phase >= Phase 8 (expanded universe)
THEN surface Sector Concentration Warning in pipeline output
BUT never block, filter, or re-rank candidates automatically
```

**Why not V0:** V0 is intentionally Tech-scoped. Concentration warning would be permanent noise. Activate when Fundamental & Opportunity themes (Phase 8) introduce new sectors.

**Evidence:** SRL v0.2 §3, §5-L3, §6-Q5

---

## ERP-002: Empty Theme Timer

**Pattern detected:**
- TH-030 (Cybersecurity) was approved + active monitoring with 0 candidates from 2024-07-01 to 2024-07-24 (23 days)
- Gap report detected it on day 0, but no escalation mechanism existed
- Founder manually reviewed and resolved

**Proposed rule:**
```
WHEN a theme has approval_status = "Approved"
AND monitoring_status = "Active Monitoring"
AND candidate_count = 0
AND days_since_last_candidate_change > 30
THEN auto-flag in Coverage Gap Report as "Aging Empty Theme" (severity: High)
AND include in pipeline_result.messages[]

BUT never auto-add, auto-archive, or auto-demote themes
```

**Rationale:** Prevents approved themes from drifting without coverage. 30-day window gives Founder time for natural review cycles. At 143 themes, multiple empty themes could accumulate silently.

**Evidence:** SRL v0.1 §7.1 (original blind spot), SRL v0.2 §3 (gap resolution latency), GAP-001 resolution

---

## ERP-003: Anomaly-to-Candidate Escalation Signal

**Pattern detected:**
- AN-003 (CRWD+PANW volume anomaly) → Founder added both as candidates (GAP-001)
- AN-002 (AVGO outlier) → Founder added as Priority Research candidate (GAP-003)
- 3/4 Phase 5 anomalies correctly predicted candidates that Founder later approved

**Proposed rule:**
```
WHEN 2+ anomalies reference the same ticker within a 90-day window
AND that ticker is NOT currently a Candidate
THEN surface as "Emergent Candidate Signal" in Coverage Gap Report (severity: Medium)
AND include anomaly IDs as evidence references

BUT never auto-promote to Candidate — Founder decision required per FD #6
```

**Differentiation from Gap Detection:** Gap detection finds gaps (missing coverage). This rule finds positive signals (converging anomalies pointing to the same name). It's the "signal" side of the "signal vs gap" coin.

**Evidence:** SRL v0.2 §3 (anomaly prediction accuracy), AN-002, AN-003

---

## ERP-004: Conviction-Research State Alignment

**Pattern detected:**
- High conviction → Priority Research: NVDA (High), AVGO (High) — 2/2 aligned
- Moderate conviction → Watchlist: CRWD, PANW, SMCI, MDT, AMD — 5/5 aligned
- Low conviction → Watchlist with waiting triggers: INTC (Low + Human Override), FSLR (Low) — 2/2 aligned
- System is 9/9 consistent with intuitive hierarchy but alignment is informal

**Proposed rule:**
```
WHEN a candidate's conviction_level is "High" AND thesis_status is "Confirmed"
THEN recommend research_state = "Priority Research" in pipeline output
AND surface as advisory (not automatic)
Founder may override per Human Override mechanism (FD #13)

WHEN conviction_level is "Low"
THEN candidate should have an explicit entry_trigger with measurable conditions
AND trigger_status should be "Waiting" (not "Watch")
```

**Rationale:** Codifies what is already working informally. Prevents future candidates from entering at mismatched conviction/research states. The Low conviction → Waiting trigger requirement ensures we don't Watchlist candidates that shouldn't be actively monitored.

**Evidence:** SRL v0.2 §5-L5, current pipeline state (9/9 aligned)

---

## ERP-005: Self-Reflection Log Trigger Criteria

**Pattern detected:**
- SRL v0.1 was a "per-Phase" log (covered entire Phase 5 implementation)
- SRL v0.2 is a "per-session" log (covers gap resolution session)
- The granularity question from SRL v0.1 §6-Q4 remains unanswered

**Proposed rule:**
```
Generate Self-Reflection Log when:
(1) Pipeline run changes candidate count (additions or removals)
(2) Pipeline run changes any thesis_status or conviction_level
(3) Founder review session occurs (regardless of code changes)
(4) Coverage gap is resolved (at least 1 gap addressed)

Do NOT generate for:
- Routine daily runs with zero changes
- Cosmetic/display-only edits
- Documentation-only changes without pipeline impact
```

**Rationale:** Prevents SRL spam (daily runs with no changes) while ensuring every material decision is captured. Condition (4) ensures gap resolution is always documented.

**Evidence:** SRL v0.2 §6-Q4

---

## Disposition

| Rule | Status | Action Required |
|------|--------|-----------------|
| ERP-001 | Monitoring rule, Phase 8+ | No V0 action — acknowledge |
| ERP-002 | New proposal | Founder: approve / revise / reject |
| ERP-003 | New proposal | Founder: approve / revise / reject |
| ERP-004 | New proposal | Founder: approve / revise / reject |
| ERP-005 | New proposal | Founder: approve / revise / reject |

---

*Proposed: 2024-07-24 15:40 ICT | AI Intelligence Layer (§23) | FD #14: AI may propose learning but may not enforce rule changes | FD #28: Phase 6B Emergent Rule Discovery authorized*
