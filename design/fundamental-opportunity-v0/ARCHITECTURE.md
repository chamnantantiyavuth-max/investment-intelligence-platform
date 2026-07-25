# Phase 8 Architecture — Fundamental & Opportunity Intelligence V1

**Status:** Draft for Founder Review (WF-Phase 2R)
**Version:** 0.1
**Derived from:** FUNDAMENTAL-OPPORTUNITY-INTELLIGENCE.md v0.1 (FD #40)
**Spike validated:** e229b36 (28/28 checks)

---

## 1. Architecture Overview

**Pattern:** Hybrid — separate pipeline, shared modules (WF-Phase 0 Decision 2)

```
┌──────────────────────────────────────────────────────┐
│  Frontend (React + shadcn/ui)                        │
│  ┌────────────┐ ┌──────────────────┐ ┌─────────────┐ │
│  │ Dashboard  │ │ Fundamental Queue│ │Cheap&Quality │ │
│  │ (+FO card) │ │ (13-sect pkg)   │ │ (watchlist)  │ │
│  └─────┬──────┘ └────────┬─────────┘ └──────┬──────┘ │
└────────┼─────────────────┼──────────────────┼────────┘
         │                 │                  │
    ┌────▼─────────────────▼──────────────────▼────┐
    │  FastAPI Backend                              │
    │  /api/fo-queue  /api/fo-package/{id}         │
    │  /api/fo-cheap-quality                        │
    └────────────────────┬─────────────────────────┘
                         │
    ┌────────────────────▼─────────────────────────┐
    │  fundamental-opportunity-v0/                  │
    │  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
    │  │ fixtures │  │ pipeline │  │  display   │  │
    │  │  .py     │─▶│  6-stage │─▶│  HTML/JSON │  │
    │  └──────────┘  └──────────┘  └────────────┘  │
    │        │              │              │        │
    │   ┌────▼────┐   ┌─────▼──────┐  ┌───▼─────┐  │
    │   │  moat   │   │  earnings  │  │  value  │  │
    │   │  .py    │   │  _quality  │  │  _trap  │  │
    │   └─────────┘   └────────────┘  └─────────┘  │
    └──────────────────────────────────────────────┘
                         │
    ┌────────────────────▼─────────────────────────┐
    │  Shared Core (reused from V0)                 │
    │  shared/base.html  — IIP design tokens        │
    │  AM V0 patterns    — fixtures, display, run   │
    └──────────────────────────────────────────────┘
```

---

## 2. Directory Structure

```
fundamental-opportunity-v0/
├── __init__.py              # Package marker
├── fixtures.py              # 8-10 synthetic companies + macro regime
├── moat.py                  # §3.4.1 Moat Classification
├── earnings_quality.py      # §3.5.1 Earnings Quality Dimension
├── value_trap.py            # §3.6.2 Value Trap Detector
├── pipeline.py              # 6-stage pipeline (S1→S6) → Research Package
├── display.py               # HTML/JSON renderer
├── run.py                   # CLI entry point
├── test_locked/             # Locked acceptance tests (WF-Phase 4)
│   ├── test_moat.py
│   ├── test_earnings_quality.py
│   ├── test_value_trap.py
│   └── test_pipeline.py
└── output/                  # Generated artifacts
    ├── research_packages.html
    └── pipeline_result.json
```

**New Frontend:**
```
frontend/src/
├── pages/
│   ├── FundamentalQueuePage.tsx    # Research Packages table
│   ├── FundamentalDetailPage.tsx   # 13-section detail view
│   └── CheapQualityPage.tsx        # Cheap & Quality watchlist
├── api/
│   └── foClient.ts                 # /api/fo-* fetch wrappers
└── types/
    └── fo.ts                       # FundamentalOpportunity types
```

**New Backend:**
```
backend/api/
└── fo_routes.py              # /api/fo-queue, /api/fo-package/{id}, /api/fo-cheap-quality
```

---

## 3. Pipeline — 6 Stages

| Stage | Name | Input | Output | Module |
|---|---|---|---|---|
| S1 | Macro Analysis | MACRO_REGIME from fixtures | Regime + sector implications | pipeline.py |
| S2 | Industry Analysis | Company sector/industry + margins | Industry position (Leader/Strong/Challenged) | pipeline.py |
| S3 | Product Analysis | Company market_cap, sector | Product type, liquidity, exchange | pipeline.py |
| S4 | **Company Analysis** | Company financial data | Moat assessment + Financial quality + Management | moat.py |
| S5 | **Earnings & Change** | Company earnings data | Quality rating + Thesis impact | earnings_quality.py |
| S6 | **Valuation Context** | Company valuation data + Moat | Value Trap verdict + Cheap/Quality classification | value_trap.py |

### S4 Detail — Moat Classification

```
moat.classify_moat(company) → {
    types: [{type, strength, evidence}, ...],
    width: Wide | Narrow | None,
    depth: Deep | Moderate | Shallow,
    trend: Stable | Widening | Narrowing,
    active_count: int,
    types_summary: str
}

moat.moat_conviction_cap(moat) → Maximum | High | Moderate
moat.moat_strength_score(moat) → 0-100
moat.moat_narrative(moat) → str
```

### S5 Detail — Earnings Quality

```
earnings_quality.assess_earnings_quality(company) → {
    rating: HIGH | MEDIUM | LOW | COSMETIC,
    conviction_impact: str,
    surprise_direction: Beat | Meet | Miss,
    revenue_quality: str,
    margin_quality: str,
    fcf_conversion: float,
    narrative: str
}
```

### S6 Detail — Value Trap

```
value_trap.is_unusually_cheap(company) → bool  # P/E < 70% of 5Y avg

value_trap.run_value_trap_check(company, moat) → {
    triggered: bool,
    score: 0-5,
    verdict: NOT_A_TRAP | MIXED | SUSPECT | TRAP | DEFINITE_TRAP,
    action: str,
    questions: [{number, question, pass, detail, icon}, ...]
}
```

---

## 4. Module Contracts

### 4.1 Pipeline Contract

```python
def run_pipeline() -> list[dict]:
    """Returns list of Research Packages, one per company."""
    # Input: FIXTURES (list of company dicts)
    # Output: list of 13-section dicts
    # No side effects, deterministic
```

### 4.2 Display Contract

```python
def render_full_report(packages: list[dict], json_path: str = None) -> str:
    """Returns complete HTML page as string."""
    # Saves JSON to json_path if provided
    # Uses IIP design tokens (Inter, #f5f6f8, #0f1117)
    # SYNTHETIC FIXTURES watermark
```

### 4.3 API Contract (FastAPI)

```python
# GET /api/fo-queue → list[ResearchPackageSummary]
# GET /api/fo-package/{id} → ResearchPackage (full 13 sections)
# GET /api/fo-cheap-quality → list[CheapQualityItem]
```

### 4.4 Frontend Contract

| Route | Component | Data Source |
|---|---|---|
| `/fundamental` | FundamentalQueuePage | `GET /api/fo-queue` |
| `/fundamental/:id` | FundamentalDetailPage | `GET /api/fo-package/{id}` |
| `/cheap-quality` | CheapQualityPage | `GET /api/fo-cheap-quality` |

---

## 5. Shared Core Reuse

| Module | Source | Reused By |
|---|---|---|
| `shared/base.html` | IIP design tokens template | display.py (wraps content) |
| Fixtures pattern | `alpha-momentum-v0/fixtures.py` | fo fixtures.py (same shape concept) |
| Display pattern | `alpha-momentum-v0/display.py` | fo display.py (HTML structure) |
| Pipeline pattern | `alpha-momentum-v0/pipeline.py` | fo pipeline.py (stage structure) |
| Run pattern | `alpha-momentum-v0/run.py` | fo run.py (CLI entry) |
| Frontend components | MetricCard, Badge, Table, Tabs | Fundamental pages |
| Sidebar + Layout | AppSidebar.tsx, Layout.tsx | +3 nav items |

---

## 6. Deployment Boundary

| Layer | What | How |
|---|---|---|
| Python Pipeline | `fundamental-opportunity-v0/` | `python run.py` (CLI) or via FastAPI |
| FastAPI | `backend/api/fo_routes.py` | `GET` endpoints, JSON responses |
| Frontend | 3 new pages | React + TanStack Query |
| Output | `output/` dir | HTML + JSON, SYNTHETIC watermark |

**No new dependencies.** Phase 8 uses existing tech stack:
- Python 3.11+ (pandas not required for V1 fixtures)
- FastAPI (existing backend)
- React + shadcn/ui (existing frontend)

---

## 7. V1 vs V1.5+ Boundary

| Capability | V1 (Phase 8) | V1.5+ |
|---|---|---|
| Synthetic fixtures | ✅ 8-10 companies | → Real data |
| Moat classification | ✅ Deterministic rules | → May add AI assistance |
| Earnings quality | ✅ Deterministic rules | → Real filings/transcripts |
| Value trap detector | ✅ Deterministic rules | → Automated screening |
| HTML output | ✅ Static report | → Live API + React |
| Independent Challenge | ✅ Rule-based | → AI-generated challenges |
| Real data | ❌ | ✅ yfinance/API |
| Capital Command | ❌ External | → Integration deferred |

---

## 8. Risk & Constraints

| Risk | Mitigation |
|---|---|
| Moat classification is subjective | Width/Depth/Trend = explicit criteria, not AI judgment |
| Value Trap false positives | 5-question check with scoring (not binary); MIXED (3-4/5) = flag for research, not reject |
| Fixture scope too small | 8-10 companies across 5 sectors = same scope as AM V0 (10 candidates) |
| Frontend scope creep | 3 pages max (Queue, Detail, Cheap&Quality) — same pattern as AM Queue + Theme Card |
| Pipeline performance | Synthetic fixtures = instant; no real data overhead in V1 |
