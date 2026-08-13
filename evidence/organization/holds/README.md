# Holds Register

Hold semantics (FD #54 Q2 — org-workflow scope only): a Hold pauses org-workflow promotion/canonical publication within the org pipeline; it never changes canonical domain state, never erases work, never rejects the underlying idea. Only the issuing role clears its Hold; Founder override per Constitution §21 with recorded rationale + accepted residual risk.

Record format (one YAML file per Hold):

```yaml
hold_id:
type: DATA HOLD | VALIDATION HOLD | RISK HOLD | GOVERNANCE HOLD
issuer:
artifact/card:
scope:                # what is paused (org-workflow promotion/publication only)
triggering_condition:
evidence:
remediation_required:
owner:
review_condition:
partial_work_allowed: true/false
status: OPEN | CLEARED | OVERRIDDEN
clear_record:
  cleared_by:
  date:
  basis:
override_record:      # Founder only
  fd_reference:
  rationale:
  accepted_residual_risk:
```
<!-- 2026-08-05 14:55 UTC+7 -->
