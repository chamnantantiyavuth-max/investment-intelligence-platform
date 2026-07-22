# Session Start Prompt — Alpha Momentum V0

You are resuming work on the Investment Intelligence Platform. Read the current state below and pick up where we left off.

## Current State

```
✅ Foundation v0.3
✅ Project Definition v0.1
✅ Gate A — 35/35 DS slots approved
✅ Gate B — 143 themes (DR-005)
✅ Gate C — 7 HC slots + 20 acceptance scenarios
✅ Gate D — Independent audit passed (4 findings resolved)
✅ Phase 3 — V0 implementation complete (end-to-end vertical slice)
```

## Phase 3 Implementation (Built)

- `alpha-momentum-v0/run.py` — CLI entry: `python run.py`
- `alpha-momentum-v0/fixtures.py` — 3 themes, 5 entities, 5 candidates, 13 evidence, 1 override
- `alpha-momentum-v0/pipeline.py` — 6 stages (S1 Universe → S6 Queue)
- `alpha-momentum-v0/display.py` — HTML rendering (Jinja2)
- `alpha-momentum-v0/templates/theme_card.html` — Full Theme Card template
- Output: `output/queue.html` + 3 Theme Cards + `pipeline_result.json`

Stack: Python + pandas + Jinja2 (provisional V0 — not final)

## Pending Items

1. **UI polish** — Founder noted aesthetics need refinement (fonts, layout, colors). Currently functional but basic.
2. **Proposed amendments** (in `proposed-amendments/`) — ChatGPT-authored AI Operating Constitution v0.2 + Dual Intelligence Operating Model v0.1 — assessed but not yet approved/trimmed.
3. **Gate D Phase 3 transition** — Founder Decision #22 already recorded. Implementation authorized.
4. **Next phase** — expand fixtures, add real data pipeline (V0.5), or proceed to Close System design (Phase 7).

## Key Files to Read First

- `AGENTS.md` — current phase + restrictions
- `operational/FOUNDERS-DECISIONS.md` — decisions #1-22
- `design/alpha-momentum-v0/DESIGN-PLAN.md` — gate structure
- `alpha-momentum-v0/run.py` — entry point (run to see V0 output)

## Communication

Founder = Jarvis (Chamnan). Thai-first, technical terms in English. Founder is an investor/trader, not a software engineer. Prefers end-to-end workflow pictures before implementation. Report before acting — explore-only until given green light.
