# User & Decision Map — Investment Intelligence Platform

> **Phase D — ui-dashboard-workflow v4.0.0 · 2026-08-04 · FD #51 (A — Research Desk)**

## Primary user

**Chamnan (Founder, solo operator).** Frequency: daily–weekly review sessions. Context: momentum-first opportunity discovery; portfolio-blind; advisory only. Secondary user: none in V0 (single-user auth, FD #46).

## Page decision map

| Page | Primary question | Primary decision | Primary action | Prevented mistakes | Frequency |
|---|---|---|---|---|---|
| Login | Am I the authorized user? | Enter session | Authenticate | Unauthorized access (single-user, FD #46) | Session start |
| Dashboard | What deserves my attention NOW? | Which theme/candidate to open next | Open Theme Card / AM Queue | Acting on synthetic as real (CS banner); stale data; API-failure misread as "nothing to see" (C5) | Every session |
| AM Queue | What is the queue ordering and why? | Which candidate/theme to investigate | Open Theme Card | Composite-score confusion (4 dims separate); overclaiming override/history capability (A-01) | Every session |
| Theme Card | Does this thesis still hold? | Continue / escalate / challenge | Read falsification + evidence | False evidence associations (C2); hidden falsification; provenance mislabel | When a theme is being judged |
| AM Screener | Which candidates pass approved criteria? | Shortlist for the queue | Read matrix rows | Invented criteria; hidden methodology; summed composite (never) | When re-screening |
| CS Radar | What product should I watch? | Which radar product to monitor | Open product view | Misreading SYNTHETIC DEMO as live (FD #46) | Weekly |
| FO Queue | Which companies deserve fundamental research? | Open package / detail | Open FO package | Unapproved derived scores surfacing (C-02) | Weekly |
| FO Detail | What is the moat / earnings-quality / trap story? | Thesis validity judgment | Read classification panels | Trap misclassification; invented moat scores (C-02) | When a company is judged |
| Cheap & Quality | Cheap & quality — or trap? | Which candidates are genuinely cheap-quality | Read verdict rows | Value-trap mapping drift (C-02) | Weekly |
| Institutional | What are large holders doing? | Conviction / action read | Read 13F signal rows | Invented score_signal (C-02); stale 13F read (120d bound) | Monthly-ish |
| Weak Signal | What is unexplained? | Which anomaly/hypothesis to promote | Promote to research | Experimental ≠ official conflation (FD #27) | Occasionally |

## Page-state contract (per page)

```markdown
Primary user: Chamnan
Primary question: <above>
Primary decision: <above>
Primary action: <above>
Secondary questions: methodology, provenance, falsification
Not the purpose of this page: execution, allocation, portfolio views
Critical mistakes this page must prevent: <above>
```

## Overview-page rule (Dashboard)

Answers: (1) current state? (2) anything outside approved boundaries? (3) what changed? (4) what requires attention/decision? (5) where next? — NOT every detail simultaneously. AM request failure → scoped degraded state, never coerced to zero (C5).
<!-- 2026-08-04 17:20 UTC+7 -->
