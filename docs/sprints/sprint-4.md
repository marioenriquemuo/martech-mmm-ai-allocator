# Sprint 4

This file is STORY-507 only.

## STORY-507 — The two measurement gaps stay open

**Plain language:** The tool already says two measurement problems are unfinished. This story writes that down. It does not fix them.

Meridian channel order still disagrees with Path-C (Spearman about −0.6). That is `GAP-201-RANK` in [`docs/learnings/open-gaps.md`](../learnings/open-gaps.md). The offline brief already prints that Meridian rank vs Path-C is open.

ETL writes `exogenous_controls.parquet`. Meridian still reads the spend panel only (`src/models/meridian_data.py`). That is `GAP-501-MODEL`. This story does not pass those controls into Meridian and does not change rank-recovery math.

Stories 504, 505, and 506 do not close `GAP-201-RANK` or `GAP-501-MODEL`. This story does not close them either. `GAP-501-API` stays open.

The same registry gains two leftover review rows, both open and low: `GAP-TARGET-BASELINE` (target-mode shift lines still read like a change from old spend; the lift stays empty) and `GAP-QA-TIMEDELTA` (the QA timedelta warning). This story does not fix those either.

**Definition of done:**

- `GAP-201-RANK` and `GAP-501-MODEL` are still `open`. A note says STORY-507 does not close them. `GAP-501-API` is still `open`.
- New open rows exist for `GAP-TARGET-BASELINE` and `GAP-QA-TIMEDELTA` only. Existing gap-row text is unchanged.
- [`docs/learnings/README.md`](../learnings/README.md) lists those two new gaps as unchecked. `GAP-201-RANK` and `GAP-501-MODEL` stay unchecked.
- The offline brief still prints both caveats: incremental KPI is not revenue, and Meridian rank vs Path-C is open. Caveat wording is unchanged.

This story is not a close of those gaps.
