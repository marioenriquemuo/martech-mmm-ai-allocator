# Sprint 4 — STORY-506

STORY-506 only. No points. No dates. This story is not done.

## STORY-506 — Name the question in the offline brief

**Plain language:** Target mode finds the cheapest spend that reaches a KPI. Maximize mode splits a fixed total budget. Both opened with the same sentence, `Move {channel} up…`. Readers treated them as one recommendation.

**Where it lives:** `constraints.mode` is `target` or `maximize` on the allocation (`src/optimize/allocator.py`). `build_fact_pack` copies that field (`src/report/facts.py`). `render_offline` names the question in the opening line (`src/report/brief.py`). The dashboard prints that same offline brief. There is one brief, not a second template.

- `target`: cheapest spend that reaches the KPI target.
- `maximize`: how to split this fixed total budget.

Structured spend, KPI, and saturation flags stay exact. Headline and bullets keep the existing rounding rules.

This story does not close `GAP-201-RANK`, `GAP-501-MODEL`, `GAP-504-SMOKE`, or `GAP-505-RHAT`. `GAP-506-MODE` stays open.
