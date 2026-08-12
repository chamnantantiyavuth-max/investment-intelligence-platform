# Model-Routing Migration Sweep — Sol→Luna→Flash (2026-08-13, Stage 6.5/6.6)

Full worked example of a **two-phase model-routing migration across ALL profile configs** (22 configs: global + 21 profiles) plus the **architectural corrections the Founder demanded afterward**. Extends the 2026-08-02 delegation-model sweep with the block-scoped edit technique and the "selective premium reviewer" cost doctrine.

## Phase 1 — Sol→Luna (Stage 6.5, FD #104)

Goal: `delegation.model` `gpt-5.6-sol/openai-codex` → `openai/gpt-5.6-luna/openrouter` in every config.

**Technique — BLOCK-SCOPED regex, never a blind global replace.** A naive `t.replace("provider: openai-codex", "provider: openrouter")` across the whole file ALSO rewrites:
- `image_gen.provider` (gpt-image-2-medium rides openai-codex) → image generation breaks silently,
- `moa.reference_models[].provider` (gpt-5.5 via openai-codex is a design choice, not delegation).

Both must be restored from backup afterward (hit live: 20/20 image_gen + 20/20 MoA blocks clobbered, restored from `.bak-2026-08-13-stage65`).

Correct pattern: anchor on the block header, consume its own indented body only:
```python
t2 = re.sub(r"(delegation:\n(?:  .*\n)*?  model: )openai/gpt-5\.6-luna", r"\1deepseek-v4-flash", t, count=1)
```
Validate YAML after EVERY write; on parse error restore that file from backup immediately (don't let a broken config sit).

**Multi-line regex trap:** a `fallback_providers:` block regex with a trailing `\n?)+` can eat the next top-level key (`agent:`) into the same line → YAML parse error. Use exact 4-line block patterns with `^` anchors and `re.M`, and ALWAYS `yaml.safe_load` after write.

**Restore-after-edit ordering trap (hit live):** restoring a config from `.bak` to fix one mistake resurrects the PRE-fix state of OTHER edits made earlier in the same migration (e.g. global delegation back to the old model). After any restore, re-run the full intended edit sequence for that file and re-verify ALL of delegation / fallback / image_gen / MoA — then re-grep the retired string (expect exactly the files you intended, nothing more).

## Phase 2 — Founder corrections (Stage 6.6, FD #105): "selective" made real

The Founder rejected the Phase-1 result on 3 architectural grounds — each is a durable rule:

1. **R1 — `delegation.model` must NOT be the premium model.** `delegate_task` reads ONE `delegation.model` with NO per-task override (docs `delegation.md` L171: "the pin is global"). A global Luna delegation silently routes every routine `delegate_task` to the premium reviewer = the cost leak. **Final: `delegation.model = deepseek-v4-flash / deepseek` in ALL configs.** Premium reviews run as **Kanban tasks with per-task model override**: `hermes kanban create --model openai/gpt-5.6-luna --provider openrouter` (proven: premium audit + material engineering review → Luna; routine worker → Flash).

2. **R2 — `fallback_providers` must not auto-fallback routine work to the paid model.** If DeepSeek goes down, Radar/Data/workers would silently flood Luna. **Final: `fallback_providers: []`** (routine failure → queue/fail safely; premium tasks retry Luna explicitly per their own contract). NOTE: some profiles write this block with `- provider:` (no indent) vs `  - provider:` — handle BOTH indent variants in the regex.

3. **R3 — SOUL/USER must NOT carry model names.** Stage 6.5 had put 28 model-routing refs × 18 SOULs — the exact config-drift regression the architecture avoids. **Final: SOUL carries one generic pointer** ("Use the currently approved model-routing policy — load the `model-routing` skill") and zero model/provider names; routing lives in config + superseding FD + `model-routing` skill. Model changes must never require 18-profile SOUL edits again.

## Premium-review execution-path doctrine (P1, FD #105)

`delegate_task` has NO per-task model parameter. Therefore every "premium reviewer" procedure MUST be written as:
- **routine bounded helper** → `delegate_task` → Flash (global delegation.model),
- **premium independent review** → **Kanban review task with per-task override** (`--model openai/gpt-5.6-luna --provider openrouter`) → Luna.

Skills that say "delegate to Luna High via delegate_task" are silently wrong post-R1 — audit them (hit: llm-council L84, prelaunch-close-beta-audit split-lane, governance-proposal-review). Fix = replace with the Kanban-override path.

## Verification sweep checklist (run at migration end)

```
grep -rln "<old-model>" config.yaml profiles/*/config.yaml          # expect 0 (exclude .bak)
grep -rln "<old-model>" profiles/*/SOUL.md profiles/*/user.md        # R3: expect 0 model names anywhere
hermes config get delegation.model  → deepseek-v4-flash             # R1
hermes config get fallback_providers → []                           # R2
kanban create --model openai/gpt-5.6-luna --provider openrouter      # premium path proves Luna
kanban create (no override)                                          # routine path proves Flash
```
Backups: `config.yaml.bak-2026-08-13-stage65/66` per file — rollback = copy back (verified restorable).
