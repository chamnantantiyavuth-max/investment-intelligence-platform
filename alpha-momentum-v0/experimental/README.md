# ✅ ACTIVE — Phase 5 Theme Intelligence V1

**Status:** ACTIVE (T0 Architecture Re-design complete, 24 July 2026)
**Authorization:** FD #27 (23 July 2026)
**Previous status:** QUARANTINED per WF-Phase 2R Architecture Review (23 July 2026) — RESOLVED

## Architecture

The experimental pipeline is **constitutionally separate** from the approved Alpha Momentum V0 pipeline. It does NOT reuse approved stage functions.

### Pipeline Stages (E1–E4 vs S1–S6)

| | Approved Pipeline | Experimental Pipeline |
|---|---|---|
| **Purpose** | Screen candidates against existing themes | Discover NEW themes from market signals |
| **Stages** | S1–S6 (Universe→Theme→CQ→ER→DC→Queue) | E1–E4 (Anomaly→Classify→Hypothesize→Review) |
| **Determinism** | Deterministic (same input→same output) | Non-deterministic (statistical detection + AI generation) |
| **Output** | `output/queue.html` + `output/pipeline_result.json` | `output/experimental/radar.html` + `output/experimental/experimental_pipeline_result.json` |

### E1: Anomaly Detection (→ T2 anomaly.py)
- Statistical deviation from market data baselines
- NOT hand-written fixtures (FD #27 §2)
- Types: Sector Divergence, Single-Stock Outlier, Volume Anomaly, Missing Correlation

### E2: Anomaly Classification (→ T2 anomaly.py)
- Classify by type, enforce cooldown, deduplicate
- Circular feedback guard: 30-day cooldown (FD #27 §4)

### E3: Hypothesis Generation (→ T3 hypothesis.py)
- AI-generated Theme Hypotheses from anomaly patterns
- Epistemic metadata MANDATORY (§23.4): provenance, confidence, version, source_refs

### E4: Founder Review Queue (→ T4 radar.py)
- Surface hypotheses + experimental themes for Founder review
- Theme approval remains Founder-only (FD #27 §5)

## Hard Guards (FD #27)

| # | Guard | Status |
|---|---|---|
| 1 | ZERO imports from approved `pipeline.py` stage functions | ✅ Enforced |
| 2 | Experimental output NEVER contaminates `pipeline_result.json` | ✅ Separate output dir |
| 3 | Experimental themes NEVER alter official filters/rankings/scores | ✅ Read-only access to approved data |
| 4 | Circular feedback cooldown (anomaly→hypothesis→theme→anomaly) | ✅ 30-day cooldown in E2 |
| 5 | Epistemic metadata mandatory for AI-generated hypotheses | ✅ _epistemic field on all hypotheses |

## Files

| File | Purpose | Status |
|---|---|---|
| `pipeline.py` | Experimental 4-stage pipeline (E1–E4) | ✅ T0 re-architected |
| `display.py` | Inbox + Radar rendering (standalone) | ✅ T0 re-architected |
| `inbox.py` | Weak Signal Inbox data model + API | ⏳ T1 |
| `anomaly.py` | Statistical anomaly detection engine | ⏳ T2 |
| `hypothesis.py` | AI hypothesis generation pipeline | ⏳ T3 |
| `radar.py` | Experimental Theme Radar dashboard | ⏳ T4 |

## Test Coverage

- `tests/locked/test_experimental_separation.py` — ✅ T0 (Parent-written, RO for subagents)
- `tests/locked/test_inbox_*.py` — ⏳ T1
- `tests/locked/test_anomaly_*.py` — ⏳ T2
- `tests/locked/test_hypothesis_*.py` — ⏳ T3
- `tests/locked/test_radar_*.py` — ⏳ T4
