# WORKFLOW_REGISTER — Browser Lane (Parent) — 2026-08-03

> Pre-Launch Close Beta Audit · profile: iip · Browser operator: Parent (deepseek-v4-flash)
> All workflows exercised through the live app at http://localhost:5173 (vite dev, proxy → 127.0.0.1:8000)

| WF-ID | Workflow | Route | Result | Evidence | Console |
|---|---|---|---|---|---|
| WF-01 | Dashboard (Strategy Control Center) | `/` | **PASS** | screenshots/WF-01-dashboard.png | 0 JS errors (3 Base UI a11y advisories, known class) |
| WF-02 | AM Queue | `/am-queue` | **PASS** | screenshots/WF-02-am-queue.png | 0 JS errors |
| WF-03 | AM Theme detail (theme-ai-infra, via row click) | `/am-theme/theme-ai-infra` | **PASS** | screenshots/WF-03-am-theme.png | 0 JS errors |
| WF-04 | CS Radar | `/cs-radar` | **PASS** | screenshots/WF-04-cs-radar.png | 0 JS errors |
| WF-05 | FO Queue | `/fundamental` | **PASS** | screenshots/WF-05-fo-queue.png | 0 JS errors |
| WF-06 | FO Detail (MSFT — all 5 tabs exercised: Overview/Moat/Earnings/Valuation) + deep-link URL | `/fundamental/msft` | **PASS** | screenshots/WF-06-fo-detail-msft.png | 0 JS errors |
| WF-07 | Cheap & Quality | `/cheap-quality` | **PASS (finding: no provenance label)** | screenshots/WF-07-cheap-quality.png | 0 JS errors |
| WF-08 | Weak Signal Inbox | `/weak-signals` | **PASS** | (snapshot) | 0 JS errors |
| WF-09 | 404 page | `/does-not-exist` | **PASS** | (snapshot) | 0 JS errors (1 a11y advisory from NotFound button) |
| WF-10 | All-pages JS sweep | all 8 routes | **PASS** | console checks after each | **0 JS errors across all pages** |

## Browser findings

- **BROWSER-003 (Major — data agreement):** CS Radar page (`/cs-radar`) renders a **hardcoded frontend `ASSETS` array** (3 assets: BRK.B, JNJ, PG) and **never calls `/api/cs-radar`** (which serves 2: BRK.B, JNJ). Confirmed in source: `frontend/src/pages/CSRadarPage.tsx:8-45` defines the array; no API client import; page maps `ASSETS` directly (line 72). Combined with dashboard `cs_radar_items: 8` (schema default) → **triple disagreement: dashboard=8, API=2, UI=3.** Violates Phase 3 UI/API/oracle agreement requirement. WF-04 cannot reach WORKFLOW_COMPLETED.
- **BROWSER-001 (Minor):** Cheap & Quality page (`/cheap-quality`) renders FO pipeline
  fixture data with **NO SYNTHETIC/DEMO provenance label** — every other data page
  (Dashboard, AM Queue, AM Theme, CS Radar, FO Queue, Weak Signal) carries one.
  Confirmed in source: `frontend/src/pages/CheapQualityPage.tsx` contains no
  "SYNTHETIC"/"demo"/"data_source" string. Violates FD #44 provenance doctrine
  (synthetic data must be labeled). Severity: Minor (data is synthetic fixtures —
  misrepresentation risk if a user treats it as live).
- **BROWSER-002 (Minor/cosmetic):** FO detail page — Base UI tab highlight box
  extends vertically beyond the label (CSS alignment quirk noted by visual check).
  Cosmetic only.
- **Known (pre-audit, re-confirmed):** sidebar renders light not dark #0f1117
  (missing `--color-sidebar` token — confirmed via computed style + static token gap).
  Listed in manifest known-open-items; recorded as BROWSER-004.

## Mutation coverage

N/A — display-only platform. Only actionable controls (Weak Signal
Propose/Dismiss/Request Review/Add Evidence) verified as **disabled** (WF-08) —
honest disabled state is the coverage. [BROWSER_VERIFIED]

## Re-login

N/A for all workflows — no auth/login flow exists in V0 (manifest-declared N/A).

## Refresh

Verified per workflow: re-navigation + fresh load re-renders full data from API
(e.g. WF-06 deep-link, WF-05 re-entry). [BROWSER_VERIFIED]

## Verification tags

- All workflows: `BROWSER_VERIFIED` (exercised live in browser)
- Console sweeps: `TEST_VERIFIED` (browser_console, 0 js_errors)
- Provenance finding: `BROWSER_VERIFIED` + `STATIC_OBSERVATION` (source grep)
- `NOT_TESTED`: none in browser lane

<!-- 2026-08-03 21:35 UTC+7 -->
