# Company Intelligence Workbench — Research Lifecycle

**Status:** Approved v0.2 — FD-CIW-008 (Founder batch approval, 2 Aug 2026)
**Version:** 0.2
**Owner:** Founder
**Authority:** Draft CIW specification subordinate to the Constitution and Founder's Decisions
**Derived from:** `docs/CIW-INTEGRATION-AMENDMENT-MAP.md` §7; `evidence/COUNCIL_DECISION-bible-2026-08-02.md` Required Changes #4, #5, #8; `project-definition/CANDIDATE-AND-QUEUE-MODEL.md` §3.3–§3.3.3; proposal §10.4, §13.2 (mapped, not duplicated)
**Approval:** FD-CIW-008 — Founder batch approval, 2 Aug 2026

---

## 1. Principle: Reuse Approved States, Do Not Create a Parallel Machine

Required Change #4: all CIW research, thesis, and artifact states **reuse or explicitly map to approved domain states** in `CANDIDATE-AND-QUEUE-MODEL.md` §3.3–§3.3.3 and the Founder Decision Gate (Operating Model §9). CIW introduces **no competing official state machine**.

The proposal's terms ("Thesis Broken", "Published", "Current Authoritative", "Investable Candidate") are mapped below to approved states with explicit actor, transition, evidence, and approval rules.

## 2. CIW Research Statuses → Approved Candidate Research States

CIW research statuses are **workflow-level states** scoped to a Candidate within the CIW workflow context (per Candidate Research State semantics: one current Research State per Strategy–Workflow context, not a global Candidate property).

| CIW Research Status | Meaning | Maps to Approved Candidate Research State | Transition Authority |
|---|---|---|---|
| **Proposed for Research** | Research request drafted; not yet approved | `Priority Research` (workflow-level intent) | AI may propose; only Founder approves promotion |
| **Approved for Research** | Founder approved the Research Request | `Selected for Deep Research` | Founder (Research Gate — see REQUEST-CONTRACT §Research Gate) |
| **Researching** | Bounded initial research in progress (Source Map → draft) | `Selected for Deep Research` | AI executes within approved scope |
| **Draft** | Research draft complete; not yet independently reviewed | `Selected for Deep Research` | AI produces; status is draft, never authoritative |
| **Independent Review** | Under independent challenge/review | `Selected for Deep Research` | Reviewer (separate from executor — QUALITY-GATES); publication blocked until pass |
| **Founder Review** | Awaiting Founder decision on publication | `Selected for Deep Research` | Founder only |
| **Published** | Founder approved; artifact is Current Authoritative | `Selected for Deep Research` (research state) — **does not change Investment Status** | Founder only (PUBLICATION-STANDARD) |
| **Monitoring** | Published case under active monitoring; re-underwriting/review triggers allowed | `Watchlist` (monitoring semantics) — **monitoring ≠ investment approval** | Founder + approved Class A observation (FD-CIW-005) |
| **Archived** | Case removed from active workflow; history fully preserved | `Archived` | Founder; reactivation requires new material evidence + explicit Founder approval |

**Constraints:**

- Research completion is **not** investment approval (proposal §10.4, retained).
- Every transition records audit fields: prior state, new state, actor, reason, evidence reference, timestamp, workflow version.
- AI and Cron **cannot** create authoritative states (Required Change #5 verification; FD-CIW-005): every transition into Published or any state change of an official artifact requires a human actor (Founder) or a Founder-approved deterministic rule.

## 3. Thesis Status Mapping (Required Change #4)

CIW uses the **approved Thesis Lifecycle** (`CANDIDATE-AND-QUEUE-MODEL.md` §3.3.2): `Proposed → Under Review → Confirmed / Weakened / Invalidated / Waiting`. The proposal's parallel terms map as follows:

| Proposal term | Approved Thesis Status | Rule |
|---|---|---|
| "Thesis Strengthened" | `Confirmed` | New evidence strengthens/supports the thesis |
| "Thesis Weakened" | `Weakened` | New evidence contradicts/undermines without full invalidation |
| "Thesis Under Review" | `Under Review` | Evidence triggers active re-evaluation |
| "Thesis Broken" | `Invalidated` | Requires a **predeclared invalidation condition** or an **explicit Founder decision** (Required Change #8). It is never an AI-only determination |
| — (waiting for event) | `Waiting` | Must specify the awaited information event (earnings, regulatory decision, product launch) |

**Minimum evidence to change an official thesis** (Required Change #8): any relevant evidence may *open review*, but an official thesis change requires:

1. a source-grounded update package (see PUBLICATION-STANDARD §4);
2. rerun deterministic calculations where applicable;
3. visible counterevidence (contradictions preserved, never averaged away);
4. independent review;
5. Founder approval.

## 4. Investment Status Remains Separate and Founder-Decided (Required Change #5)

- "Investable Candidate" and "Attractive Below Price" are **advisory, Founder-decided judgments** — never mechanical states derived from CIW output.
- CIW research status (`Published`) does **not** change Investment Status. Investment Status changes require the Founder Decision Gate (Operating Model §9).
- Valuation scenarios (Modules N–Q) cannot promote, reject, or reclassify a Candidate (see CONCEPT §5).

## 5. Artifact Authority States (mapped from proposal §13.2)

The proposal's artifact states are adopted as **artifact-level** states (they describe documents, not Candidates):

| Artifact State | Meaning | Transition Authority |
|---|---|---|
| **Draft** | Work in progress; not reviewable as authoritative | AI/executor |
| **Reviewed Draft** | Passed independent review; awaiting Founder | Reviewer (approves review pass only) |
| **Founder-Reviewed** | Founder reviewed; decision pending publication | Founder |
| **Current Authoritative** | Published; the canonical version of this artifact | Founder only |
| **Superseded** | Replaced by a newer approved version; history preserved (append-first) | Founder only |
| **Archived** | Removed from active use; fully retrievable | Founder |
| **Rejected** | Founder rejected; rejection rationale recorded | Founder |

**Rules:**

- A **presentation is never the canonical source of analytical truth** (proposal §13.3). The Master Research Paper is canonical narrative; the presentation is a decision interface that summarizes, never replaces, evidence.
- Prior versions remain retrievable (append-first rule, proposal §17.5).
- "Current Authoritative" exists for **one version per artifact at a time**; supersession is explicit and Founder-approved.

## 6. Lifecycle Flow (First Slice — Required Change #9)

```
Approved Research Request
  → Source Map
  → Bounded Initial Research (Draft)
  → Independent Challenge (Independent Review)
  → Founder Review
  → Structured Research Result (published artifact; Current Authoritative)
```

Deferred to later slices (NOT in first slice): earnings detection, update packages, re-underwriting automation, Obsidian sync, recurring scheduling. The lifecycle above is the **complete** first slice.

## 7. Transition Matrix Summary

| From | To | Actor | Requires |
|---|---|---|---|
| Proposed for Research | Approved for Research | Founder | Approved Research Request (REQUEST-CONTRACT) |
| Approved for Research | Researching | AI | Approved scope + Source Map |
| Researching | Draft | AI | Source-coverage report; framework modules per REQUEST-CONTRACT |
| Draft | Independent Review | Reviewer | Executor/reviewer separation (QUALITY-GATES) |
| Independent Review | Founder Review | Reviewer | Passed quality gates + review artifact |
| Founder Review | Published | Founder | Explicit approval (PUBLICATION-STANDARD) |
| Published | Monitoring | Founder | Approval of monitoring spec |
| Any | Archived | Founder | Reason + evidence reference; history preserved |

**Prohibited transitions:** AI → Published; Cron → any authoritative state change; Reviewer → Published (reviewer approves pass, Founder publishes); any transition without audit fields.

---

*Approved v0.2 (FD-CIW-008). Source: Council verdict Required Changes #4, #5, #8; Amendment Map §7; CANDIDATE-AND-QUEUE-MODEL §3.3–§3.3.3; proposal §10.4/§13.2 mapped.*
<!-- 2026-08-02 23:48 UTC+7 -->
