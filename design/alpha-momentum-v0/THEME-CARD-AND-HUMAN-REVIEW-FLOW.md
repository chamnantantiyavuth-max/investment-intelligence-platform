# Theme Card and Human Review Flow — Gate C

Status: Approved — Gate C Complete (Founder Review 22 Jul 2026)
Version: 1.0
Owner: Founder
Authority: Gate C artifact subordinate to the Constitution, Founder's Decisions, Approved Domain Specifications, and Approved Stable Design Plan v0.1
Derived from: Constitution v0.3, Project Definition v0.1 (THEME-MODEL §7, CANDIDATE-AND-QUEUE-MODEL §3-4, HUMAN-REVIEW-AND-LEARNING-MODEL §2, EVIDENCE-MODEL §7, ALPHA-MOMENTUM-V0-SPEC §5)
Draft Authorization: Founder Decision #19 (Gate C Authorization)
Prerequisite: CONTROLLED-THEME-SET.md v1.0 (Gate B Complete)

---

## 1. Purpose

This document defines the human-facing presentation and interaction contracts for Alpha Momentum V0. It covers:

1. **Theme Card** — what a human reviewer sees when viewing a Theme
2. **Research Queue View** — how Candidates are presented in a Theme-first queue
3. **Human Review Flow** — how the Founder moves through review, override, and decision
4. **Override Visibility** — how machine dissent is preserved when the Founder overrides
5. **Research State Transitions** — how a Candidate moves through Watchlist → Priority → Selected → Archived

This document defines **presentation contracts** — what must be visible and how interactions are structured. It does **not** define:
- Investment rules, thresholds, weights, or formulas (deferred)
- UI technology, layout pixels, colors, or rendering framework (implementation)
- Database schema or persistence (implementation)
- Computation logic for scores or rankings (Gate A)

---

## 2. Theme Card

### 2.1 Required Fields

Every Theme Card in V0 must present the following information. Fields marked [D] are derived from deterministic computation; fields marked [E] are evidence-based; fields marked [G] are governance state.

| # | Field | Source | Type | Display Rule |
|---|---|---|---|---|
| 1 | **Theme Name** | CONTROLLED-THEME-SET.md (TH-xxx) | [G] | Always visible |
| 2 | **Industry** | Finviz Industry classification | [D] | Always visible |
| 3 | **Sector** | Finviz Sector classification | [D] | Always visible |
| 4 | **Lifecycle Stage** | Theme entity lifecycle axis | [G] | Always visible; color-coded (Expansion=green, Emerging=yellow, Formation=blue, Crowded=orange, Deterioration=red) |
| 5 | **Approval Status** | Theme entity approval axis | [G] | Always visible |
| 6 | **Monitoring Status** | Theme entity monitoring axis | [G] | Always visible |
| 7 | **Stocks in Industry** | Finviz count | [D] | Always visible |
| 8 | **Key Tickers** | CONTROLLED-THEME-SET.md (6 representative) | [D] | Always visible |
| 9 | **Why-Now Case** | CONTROLLED-THEME-SET.md §6 evidence | [E] | Always visible; paragraph text |
| 10 | **Supporting Evidence** | Evidence records (Constitution §8 types 1-6) | [E] | Always visible; bullet list with source links |
| 11 | **Contradicting Evidence** | Evidence records (Constitution §8 types 1-6) | [E] | Always visible; bullet list with source links; **must not be hidden or collapsed by default** |
| 12 | **Missing Evidence** | Explicitly marked gaps | [E] | Always visible; bullet list with markers |
| 13 | **Alternative Explanations** | Theme entity | [E] | Visible when present; section hidden when empty |
| 14 | **Confidence Assessment** | Theme entity confidence axis | [G] | Always visible |
| 15 | **Candidate Summary** | Candidate–Theme relationships | [D] | Always visible; counts by role + leadership state |

### 2.2 Candidate Summary Table

Beneath the Theme-level information, each Theme Card presents its Candidates in a table:

| Column | Source | Display Rule |
|---|---|---|
| **Ticker + Name** | Entity/Asset identity | Always visible |
| **Theme Relationship Role** | Candidate–Theme relationship | Always visible; primary role bolded; secondary roles listed |
| **Leadership State** | Candidate–Theme relationship | Always visible |
| **Candidate Quality** | Four quality dimensions assessment | Displayed as separate dimension labels (not one number) |
| **Entry Readiness** | Four quality dimensions assessment | Displayed as separate dimension labels (not one number) |
| **Data Confidence** | Data Confidence assessment | Displayed as separate dimension label |
| **Research State** | Candidate–Strategy–Workflow context | Always visible |

### 2.3 Empty Theme Card

When a Theme has zero qualified Candidates (Approach C, §6 of CONTROLLED-THEME-SET.md):

- The Theme Card still renders with all Theme-level information (fields 1-14)
- The Candidate Summary section shows: **"No qualified candidates — theme is monitored but no actionable setups at this time."**
- This is an **Honest Empty State** (DNA-016) — the system must not fabricate or pad candidates

---

## 3. Research Queue View

### 3.1 Queue Structure

The Research Queue is presented **Theme-first** (Constitution §14). The view has three levels:

```
Queue Level 1: Theme Cards (sorted by Theme priority)
  └── Queue Level 2: Candidates within Theme (sorted by Candidate priority)
        └── Queue Level 3: Candidate Detail (expanded view)
```

### 3.2 Queue-Level Theme Card (Condensed)

At the queue level, each Theme shows a condensed card:

| Field | Display |
|---|---|
| Theme Name | Always |
| Lifecycle | Color-coded indicator |
| Candidate Count | "12 candidates" / "0 candidates" |
| Top 3 Candidates | Ticker + Role + Leadership State |
| Expand Action | "View Full Theme Card" |

### 3.3 Queue Ordering

Theme ordering in the queue is determined by strategy-owned prioritization (CANDIDATE-AND-QUEUE-MODEL §4.3). Candidate ordering within each Theme is determined by strategy-owned prioritization.

**V0 simplification:** The queue presents Themes in a fixed order (by sector, then by industry within sector) and Candidates ordered by lifecycle-prioritized grouping (Expansion first, then Emerging Leadership, then Formation, then Crowded/Late, then Deterioration). This is a **V0 presentation default**, not an approved permanent ordering rule.

**Exact prioritization formulas, weights, and ranking rules remain deferred.**

### 3.4 Empty Queue

When the entire queue returns zero high-priority candidates (Founder Decision #9):

- The queue view displays: **"No candidates meet current quality thresholds across any monitored theme."**
- Below this message, show the count of themes being actively monitored (for context)
- This is an **Honest Empty State** (DNA-016)
- The system must not fabricate candidates or lower thresholds to fill the queue

### 3.5 Near-Miss Display

For transparency, the queue may optionally display a "Near Miss" section below the main queue:

- Candidates that passed most but not all quality thresholds
- Clearly labeled: **"Near Miss — Did Not Qualify"**
- Shows which threshold(s) were not met
- Separated visually from qualified candidates

This section is **optional in V0** and may be omitted. When present, it must not be confused with qualified candidates.

---

## 4. Human Review Flow

### 4.1 Review Sequence

The Founder's review follows this logical sequence:

```
1. Open Research Queue
     ↓
2. Browse Theme Cards (condensed view)
     ↓
3. Expand Theme Card (full view)
     ↓
4. Review Candidates within Theme
     ↓
5. Expand Candidate Detail
     ↓
6. Review Evidence + Assessments
     ↓
7. Take Action (Override, Change Research State, Approve, Reject)
     ↓
8. Action recorded with audit trail
```

### 4.2 Candidate Detail View

When a Candidate is expanded from the queue or Theme Card:

| Section | Content |
|---|---|
| **Candidate Identity** | Ticker, company name, industry, sector |
| **Theme Context** | Which Theme(s), role(s), leadership state(s) |
| **Candidate Quality** | Four dimensions displayed separately with labels |
| **Entry Readiness** | Four dimensions displayed separately with labels |
| **Data Confidence** | Freshness, completeness, conflicts, missing data |
| **Supporting Evidence** | Evidence linked to this Candidate–Theme pair |
| **Contradicting Evidence** | Contradictory evidence (never hidden) |
| **System Assessment Summary** | Machine-generated summary of what the system sees |
| **Research State** | Current state + transition history |
| **Actions** | Override, Change Research State, Add Note |

### 4.3 Actions Available to Founder

At each review stage, the Founder may:

| Action | Where Available | What It Does |
|---|---|---|
| **View Full Theme Card** | Queue, Condensed Card | Expands to full Theme Card |
| **View Candidate Detail** | Theme Card, Queue | Expands to Candidate Detail |
| **Record Human Override** | Candidate Detail | Records override with all 8 required fields (HUMAN-REVIEW-AND-LEARNING-MODEL §2) |
| **Change Research State** | Candidate Detail | Transitions Candidate to new Research State (see §5) |
| **Add Founder Note** | Any level | Free-text note preserved with timestamp and context |
| **Approve Theme** | Theme Card | Transitions Approval Status to Approved (requires explicit confirmation) |
| **Reject Theme** | Theme Card | Transitions Approval Status to Rejected with rationale |
| **Flag for Further Research** | Candidate Detail | Marks Candidate as needing additional evidence |

---

## 5. Human Override Visibility

### 5.1 Override Display Rules

When a Human Override is recorded (HUMAN-REVIEW-AND-LEARNING-MODEL §2), the display must preserve **both** the original system assessment and the override:

| Rule | Description |
|---|---|
| **O-1: Side-by-side** | The system assessment and Founder override are displayed together — not one replacing the other |
| **O-2: Machine dissent visible** | Any unresolved contradictions, alternative rankings, or warnings the system flagged remain visible after override |
| **O-3: Counter-evidence preserved** | Evidence that contradicted the Founder's decision remains listed under "Unresolved Counter-Evidence" |
| **O-4: Rationale displayed** | Founder's stated reason for the override is displayed prominently |
| **O-5: Timestamp + context** | When the override was made, by whom, in what context (which Theme, Candidate, Research State) |
| **O-6: Reassessment marker** | If a reassessment point was set, it is displayed with the override |
| **O-7: Override stacked, not merged** | Multiple overrides on the same Candidate are displayed chronologically, each with its own system state at that time |
| **O-8: Original never erased** | The system assessment at the time of override remains permanently visible — it is not deleted, hidden behind a toggle by default, or replaced |

### 5.2 Override Indicator

In queue and list views, any Candidate with an active override displays an **Override Indicator**:

- Visual marker (e.g., "⚠️ Override" badge)
- Does not replace the Candidate's quality assessment display
- Expanding the Candidate shows the full override context

### 5.3 Override History

A Candidate's audit history includes a chronological list of all overrides:

```
Override #1 — 15 July 2026
  System Assessment: [what the system said]
  Founder Override: [what the Founder decided]
  Rationale: [Founder's reasoning]
  Counter-Evidence: [evidence against the override]
  Reassessment: 15 October 2026
  Outcome: Pending
```

---

## 6. Unresolved Evidence Visibility

### 6.1 Contradicting Evidence

Contradicting evidence must be:

- **Visible by default** — not hidden behind a toggle, expand, or "show more"
- **Listed alongside supporting evidence** — same visual weight, same section prominence
- **Never averaged away** — no composite score may silently absorb contradictions (Constitution §10, EVIDENCE-MODEL §7)
- **Preserved in exports** — Theme Card exports, research reports, and decision-support packages include contradicting evidence

### 6.2 Missing Evidence

Missing evidence is displayed as:

- **Explicit markers** — "Missing: long-term safety data for GLP-1 (>10 year)"
- **Separated from supporting/contradicting** — its own section, not mixed with other evidence
- **Not treated as contradicting** — missing evidence is absence of information, not negative evidence

### 6.3 Data Confidence Integration

When Data Confidence is low due to missing or conflicting evidence:

- The low-confidence indicator is displayed **alongside** (not replacing) the Candidate Quality and Entry Readiness displays
- The specific reason for low confidence is shown: "Low confidence: 3 of 8 expected data fields missing"
- The Founder can see **what** is missing, not just **that** something is missing

---

## 7. Research State Transitions

### 7.1 State Definitions

Per CANDIDATE-AND-QUEUE-MODEL §3.3, Research State is scoped to Candidate–Strategy–Workflow context:

| State | Meaning | Display |
|---|---|---|
| **Watchlist** | Candidate is being monitored but not promoted for active research | Default state for all Candidates linked to monitored Themes |
| **Priority Research** | Candidate identified as deserving deeper investigation | Elevated in queue; highlighted in Theme Card |
| **Selected for Deep Research** | Candidate undergoing or queued for detailed research | Prominent display; "In Research" indicator |
| **Archived** | Removed from active consideration; history preserved | Hidden from active queue; visible in archive view |

### 7.2 Transition Rules

| From | To | Who | Required |
|---|---|---|---|
| Watchlist | Priority Research | Founder or system recommendation | Rationale required |
| Priority Research | Selected for Deep Research | Founder | Explicit Founder action + rationale |
| Priority Research | Watchlist | Founder | Rationale required (demotion) |
| Selected for Deep Research | Watchlist | Founder | Rationale required (research complete or abandoned) |
| Any active state | Archived | Founder | Rationale + confirmation |
| Archived | Watchlist | Founder | Rationale + confirmation (reactivation) |

### 7.3 Transition Audit

Every Research State transition records:

- Prior state → New state
- Actor (Founder or system)
- Timestamp
- Rationale (required for human transitions; optional for system recommendations)
- Trigger context (which queue view or review action initiated the transition)

### 7.4 System-Initiated vs Founder-Initiated

- **System may propose** a transition from Watchlist → Priority Research (based on quality threshold changes)
- **System may not** archive, demote, or move to Selected for Deep Research
- **All system proposals** are displayed as "Suggested" with a clear "Approve / Dismiss" action for the Founder
- **Founder may** transition to any valid state at any time

---

## 8. Presentation vs. Material Decisions

This document makes **presentation decisions** (what the Founder sees, how information is organized). The following are **material decisions** and remain governed by Gate A artifacts:

| Concern | Owner | Reference |
|---|---|---|
| What constitutes Candidate Quality | Gate A | RULE-PACK-AND-QUALITY-CONTRACTS.md |
| How scores are computed | Gate A (deferred) | Exact formulas deferred |
| What thresholds qualify a Candidate | Gate A (deferred) | Exact thresholds deferred |
| Queue ordering rules | Gate A | PIPELINE-AND-RESEARCH-QUEUE-DESIGN.md |
| What counts as independent evidence | Gate A | DATA-CONFIDENCE-AND-POINT-IN-TIME-CONTRACTS.md |
| Override semantics (what override preserves) | Approved Domain Spec | HUMAN-REVIEW-AND-LEARNING-MODEL.md §2 |
| Theme lifecycle semantics | Approved Domain Spec | THEME-MODEL.md §2-3 |

**If a presentation decision would change a material rule, it is out of Gate C scope and requires a material-change proposal.**

---

## 9. Open Decision Slots

The following presentation decisions are proposed for Gate C resolution:

| # | Slot | Question | Proposed Default |
|---|---|---|---|
| HC-01 | Queue-level Theme Ordering | ✅ Approved — V0 fixed order by sector → industry | 22 Jul 2026 |
| HC-02 | Candidate Ordering Within Theme | ✅ Approved — V0 lifecycle-prioritized grouping | 22 Jul 2026 |
| HC-03 | Near-Miss Display | ✅ Approved — Optional; if shown, clearly separated and labeled | 22 Jul 2026 |
| HC-04 | Empty-State Wording | ✅ Approved — As proposed in §2.3 and §3.4 | 22 Jul 2026 |
| HC-05 | Override Indicator Style | ✅ Approved — "⚠️ Override" text label | 22 Jul 2026 |
| HC-06 | Condensed vs. Full Theme Card Toggle | ✅ Approved — Single click/tap to expand and collapse | 22 Jul 2026 |
| HC-07 | Contradicting Evidence Default Visibility | ✅ Approved — Visible by default (not hidden behind toggle) | 22 Jul 2026 |

---

## 10. Decision Status

| Decision | Status |
|---|---|
| **Gate C — Theme Card and Human Review Flow** | ✅ **APPROVED** (Founder review 22 Jul 2026) |
| **HC-01 through HC-07** | All 7 Approved |
| **DR-006 — Canonical Theme-Role Ownership** | Approved (Gate A) — applied here via Candidate Summary Table §2.2 |

---

## Amendment History

| Date | Change | Authority |
|---|---|---|
| 22 July 2026 | v0.1 — Initial Gate C draft | Founder Decision #19 |
| 22 July 2026 | v1.0 — Founder review complete: all 7 HC slots approved. Gate C COMPLETE. | Founder Decision #19 |
