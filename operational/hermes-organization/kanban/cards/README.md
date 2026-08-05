# Kanban Cards

Card schema per KANBAN-CONTRACT §3 (canonical states only). One YAML file per card.

```yaml
card_id:
title:
research_question:
decision_user: Founder
workflow_column:          # operational only
approval_status:          # canonical
monitoring_status:        # canonical
thesis_status:            # canonical, if applicable
research_state:           # canonical, if applicable
artifact_state:           # canonical
domain:
principal_owner:
assistant_owner:
priority:
materiality:
created_at:
required_by:
expected_artifact:
evidence_standard:
data_status:
validation_status:
risk_status:
audit_status:
open_decision_slots: []
dependencies: []
blocked_reason:
next_action:
last_updated:
```

State rule: a card move never changes canonical state. Transitions require audit fields (prior/new state, reason, evidence refs, actor, timestamp, rule version).
<!-- 2026-08-05 14:55 UTC+7 -->
