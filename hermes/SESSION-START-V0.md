# Session Start Prompt — Alpha Momentum V0.5

You are resuming work on the Investment Intelligence Platform. Read AGENTS.md first, then pick up where we left off.

## Current State

```
✅ Foundation v0.4 (Constitution + AI Operating Constitution §23)
✅ Project Definition v0.1 (7 domain specs)
✅ Operating Model v0.1 (Dual Intelligence paths)
✅ Founder Decisions #1-24
✅ Gate A — 35/35 DS slots approved
✅ Gate B — 143 themes (DR-005)
✅ Gate C — 7 HC slots + 20 acceptance scenarios
✅ Gate D — Independent audit passed
✅ Phase 3 — V0 Implementation (10/10 ACs)
✅ Phase 4 — Real EOD Data via yfinance (V0.5)
```

## Key Commands

```bash
cd alpha-momentum-v0
python run.py          # Synthetic fixtures (V0)
python run_real.py     # Real EOD data (V0.5)
```

## Pipeline (V0.5)

- 5 themes, 5 candidates, 1 empty theme
- NVDA in 2 themes (multi-role demo)
- Real prices via yfinance (24h JSON cache)
- Claude-inspired UI (warm beige palette: #fbfaf7, terracotta #cc5a37)

## Architecture

```
source_adapter.py → data/cache/*.json → run_real.py → pipeline.py → display.py → output/*.html
```

- `source_adapter.py`: run with system Python 3.14 (venv is 3.11, numpy incompat)
- `fixtures.py`: 5 themes, 5 entities, 5 candidates, 13 evidence, 1 override
- `pipeline.py`: 6 stages (S1 Universe → S6 Queue), deterministic
- `display.py`: Jinja2 templates (base, macros, queue, theme_card)
- `templates/`: Claude warm minimalism + Playfair Display + Plus Jakarta Sans

## Pending

- Phase 5: Theme Intelligence V1 (Weak Signal Inbox, Experimental Themes)
- Phase 6: Learning Loop (postmortems, lessons)
- Phase 7: Close System Definition
- Phase 8: Fundamental & Opportunity Intelligence (V1+)

## Key Files

- `AGENTS.md` — authority + phase + restrictions
- `02-PROJECT-CONSTITUTION.md` — constitution v0.4
- `operational/FOUNDERS-DECISIONS.md` — decisions #1-24
- `project-definition/INVESTMENT-INTELLIGENCE-OPERATING-MODEL.md` — dual paths
- `alpha-momentum-v0/` — all code

## Communication

Founder = Chamnan (Jarvis). Thai-first, English for technical terms. Investor/trader, not software engineer. Report before acting. Explore-only until green light.
