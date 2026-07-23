# ⚠️ QUARANTINED — Phase 5 Preview Code

**Status:** QUARANTINED per Architecture Review Gate (Phase 2R, 23 July 2026)
**Reason:** Phase 5 code (Experimental Themes, Weak Signal Inbox, Theme Hypotheses) was implemented in V0 without authorization — violating ALPHA-MOMENTUM-V0-SPEC.md §7 (V0 Non-Scope) and AGENTS.md "no new pipeline stages without explicit authorization."

**Original source:** Nick Intelligence Integration (FD #25, 22 July 2026) — experimental fixtures were added as data model preview, but the pipeline integration and display rendering exceeded scope.

**Action required before un-quarantine:**
1. Phase 5 authorization via formal Founder Decision
2. Re-architecture: experimental pipeline must NOT reuse identical deterministic logic as approved pipeline (Constitution §23.3)
3. Add epistemic status contracts to AI hypotheses (§23.4)
4. Add cooldown/staleness mechanism to prevent anomaly↔hypothesis circular feedback

**Contents:**
- `fixtures.py` — Experimental themes, candidates, anomalies, inbox hypotheses (preview data)
- `pipeline.py` — `run_experimental_pipeline()` (separated from main)
- `display.py` — `render_inbox()` and experimental theme card rendering (separated from main)
