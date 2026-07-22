# Learning and Knowledge Loop

Evidence  
→ Hypothesis  
→ Theme  
→ Candidate  
→ Research  
→ Human Decision  
→ Outcome  
→ Postmortem  
→ AI Lesson Draft  
→ Human Review  
→ Approved Lesson  
→ Rule, Skill, or Playbook Proposal

## Self-Reflection Log (Per-Run Learning)

After every material pipeline run, assessment cycle, or investment decision, the AI shall produce a self-reflection log — a structured markdown record capturing what was learned, what changed, and what remains uncertain.

### Purpose

The self-reflection log enables compound learning across runs. Instead of starting from zero each cycle, the AI reviews its own prior assessments, identifies what was confirmed or contradicted, and surfaces lessons for the Founder.

### Required Sections

Every self-reflection log shall include:

| Section | Content |
|---|---|
| **Run Context** | Timestamp, pipeline version, data vintage, themes evaluated, candidates assessed |
| **Thesis Status Changes** | Which theses were Confirmed, Weakened, or Invalidated by new evidence since the last run. Include specific evidence references. |
| **Surprises** | What the AI or Founder did not expect. What contradicted prior assumptions. What was overlooked in previous assessments. |
| **Mistakes Identified** | What prior assessments were wrong. Why they were wrong (reasoning error, missing evidence, changed conditions). What should have been done differently. |
| **Lessons** | What should be remembered for future runs. What pattern or principle emerged. What the AI now understands that it did not understand before. |
| **Open Questions** | What remains uncertain. What evidence is still missing. What the system is waiting to learn. |
| **Blind Spots** | What themes, candidates, or risks the Founder may have overlooked. What is present in the evidence but absent from the Watchlist. |

### Rules

- Self-reflection logs are AI-generated drafts — they are not official knowledge until Founder reviews and approves specific lessons.
- Logs are cumulative: each run's log references prior logs so the learning chain is traceable.
- Logs are versioned and never silently overwritten.
- Approved lessons extracted from self-reflection logs are promoted to the formal Lesson entity in the Learning Loop.
- Self-reflection logs are part of the AI Intelligence Layer — they do not modify deterministic rules, scores, or thresholds without separate Founder approval.

## Knowledge Layers

### Application
Structured source of truth.

### Obsidian / NotebookLM
Narrative case studies, playbooks, patterns, and reflection.

### Self-Reflection Archive
Cumulative AI self-reflection logs, organized by run date and pipeline version, serving as the AI's experiential memory.
