# Radar Cards — Round 2 Triage Verification (ORG-2026-0009/0010/0011, Scoped state)

**Type:** ad-hoc verification (no canonical test suite exists for kanban YAML data)
**Date:** 2026-08-07 02:15 UTC+7 · **Method:** tempfile script (`hermes-verify-` prefix, created/run/cleaned) + PyYAML round-trip

**Result:** PASS (exit 0) — first script run sliced the board segment at 100 chars, truncating 'RESEARCH INTAKE' in the long card titles (script bug, board was correct); slice widened to 150, re-run PASS.

- 3/3 YAML valid; 28/28 mandatory fields present each (KANBAN-CONTRACT §3); 6 canonical nulls
- workflow_column = Scoped (triage complete); artifact_state = Draft (research pending); next_action contains 'TRIAGED (Founder A, 7 Aug)'
- materiality M2/M2/M1; decision_user = Founder
- board.md cross-refs OK: 0009 + 0010 = RESEARCH INTAKE; 0011 = FOLDED INTO 0010

Script output: `PASS — ORG-2026-0009/0010/0011: 3/3 YAML valid; 28/28 fields; workflow_column=Scoped; next_action=TRIAGED (Founder A); board cross-refs OK (0009/0010 RESEARCH INTAKE, 0011 FOLDED INTO 0010)`

Context: RADAR round 2 triage (Founder A) committed e8879f5 → post-edit verification commit (this evidence). 0009 research in progress (analyst note deleg_f0e66ec6); 0010 next (Services GM verification with 0011 folded).

<!-- 2026-08-07 02:15 UTC+7 -->
