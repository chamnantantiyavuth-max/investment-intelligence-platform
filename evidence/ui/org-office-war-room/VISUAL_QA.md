# Visual QA — Org Office / Virtual Office (`/org-office`)

- **Task:** Org Office War Room → **Virtual Office (Maple-Story-style chibi sprites)** — role-centric org monitor; Founder picked the sprite direction (reference: Close System `agent-sprites` style), 2026-08-07
- **Commits:** War Room v1 `118b51a`; sprite rebuild (this commit) — see git log
- **Approved objective (Founder):** monitor that work is actually divided across roles — "who is working on what, where each item stands" — read-only, real data only, presentation layer. **Visual direction:** high-quality chibi anime fantasy sprites (Maple Story style), NOT flat SVG/pixel — generated via `image_generate` (gpt-image-2-medium, 11 roles, chroma-keyed to transparent PNG cutouts via PIL — same pipeline as Close System Product Radar `agent-sprites`).
- **Pages/states reviewed:** `/org-office` populated (desktop 1440): 11 sprite desks + pulse strip + holds; empty/standby desks (Options, Quant, CoS) verified in same view; radar desk shows PRODUCED + all radar-produced cards (0006–0013); error/loading via existing Skeleton + scoped Retry pattern.
- **Viewports:** desktop 1440 browser-verified. Mobile 390 = code-level audit only (browser viewport lock): grid `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`, pulse `grid-cols-2 md:grid-cols-6`, flex-wrap meta — single-column collapse, no horizontal overflow introduced.
- **Data contract (all real, read-only):** `GET /org-queue` (cards + columns + holds), `GET /research-artifacts` (card→artifact links), `GET /reports` (published notes per role via author match). No backend/API/schema change; git stays single writer (KANBAN-CONTRACT §6).
- **Sprite pipeline:** 11 roles generated (batch, same style prompt family + role archetype + chroma green bg) → PIL chroma key + despill + bbox trim → `frontend/src/assets/agents/<role>.png` (RGBA). Role→archetype: CoS royal steward, IC Secretary court scribe, Commodity alchemist-merchant, Macro oracle, Equity battle tactician, Options card-mage, CRO gate guardian, Quant rune mage, Data Steward star scholar, Auditor inquisitor, Radar Scout scout. 0 emoji (vector/PNG art).
- **IC Secretary author match:** anchored `^IC Secretary` (reports authored "… — IC Secretary synthesis" stay with their analyst desks).
- **Radar Scout desk:** cards owned = 0 (radar hands cards to analysts); desk shows PRODUCED + radar-produced cards (cards carrying `radar_observation`) under Recent output.

## Functional verification (browser, 2026-08-07)

- Login → `/org-office`: masthead nav has **Org Office**; 11 sprite desks; pulse strip (Cards in flight 6 · Awaiting you 1 · Published notes 18 · Active holds 0 · Desks active 7/11 · Org pulse Healthy); holds "No active holds".
- Card→artifact links + published-report links render per desk; radar desk lists ORG-2026-0006..0013 (round-2 cards 0012/0013 appear automatically from live `/org-queue`).
- Console: **0 errors / 0 warnings** on the route.
- `npm run build` exit 0 (tsc -b + vite) · `npm run lint` 0 errors (7 pre-existing warnings).

## Border & containment audit

- Full-perimeter bordered content surfaces per viewport: **0** (target 0, budget ≤2). Hairline grid separators (desk grid `border-r`/`border-b`/`border-l`/`border-t`), pulse hairline `border-l`, section `border-b` — no ring/box wraps/shadows. Tonal status chips + card-count badge (semantic, excluded from budget). Sprite floor shadow = soft ellipse under character (grounding, not a border).
- Justification: scanning/state communication only; no decorative outlines.

## Browser-first refinement passes (≥1 required — done)

1. War Room v1 → sprite rebuild per Founder direction (SVG chibi mockup `org-office-maple.html` approved direction → real generated sprites).
2. Added soft floor shadow under each sprite (vision feedback: characters "floating") — characters now grounded.
3. Monitor tile shows card count per role (kept from War Room).
4. Removed unused vars on rebuild; build/lint clean.

## Remaining deviations / notes

- **Known data drift (pre-existing, not introduced):** cards ORG-2026-0006..0013 carry `workflow_column: Published`, NOT in `org_store.COLUMNS` (11 canonical) — the existing `/kanban` board does not render published cards; this page renders cards by their own `workflow_column` (published cards appear correctly). Flagged for org-workflow (CoS/IC Secretary).
- Pilot cards (0001–0005) remain in In Research/Cross-Review/Triage/Founder Review per card YAML (board.md mirror drift 2026-08-05) — page shows card truth.
- Mobile 390 = **EXTERNAL_NOT_TESTED** (browser viewport lock); code-level audit passed.
- No new locked tests: presentation-layer page over existing read-only endpoints (same class as /kanban FD #59 — non-material, no backend change).
- Sprite assets ~1.2–1.8 MB each (1024² source, transparent PNG) — acceptable for a private app; not optimized (out of scope).

## Screenshot inventory

| File | State | Viewport |
|---|---|---|
| `03-final-desktop.png` | populated — 11 sprite desks + pulse + holds | 1440 |

## Evidence tags

`BROWSER_VERIFIED` · `SCREENSHOT_VERIFIED` · `FUNCTION_TEST_VERIFIED` · `ACCESSIBILITY_STATIC_CHECK` · `EXTERNAL_NOT_TESTED` (mobile viewport)

## Verdict

**PASS** — renders with real org data, role-centric monitoring objective met, Maple-Story sprite direction per Founder pick, borderless 0, console clean, build/lint green. Presentation-layer only; no backend/schema/API change.

<!-- 2026-08-07 15:10 UTC+7 -->
