# Sprint 4

Follow-up to the Sprint 3 walkthrough. These stories are not done. Each one leaves `GAP-201-RANK` and `GAP-501-MODEL` open.

## STORY-504 — Smoke must not look like a new curve file

**Status:** not done.

### Plain language

A smoke run fits a short Meridian chain, prints R-hat, and stops. It does not replace the curve file. The allocator (`scripts/03_allocate_budget.py`) and the dashboard (`app/streamlit_app.py`) still read `data/clients/pathc/models/metrics.json` for pathc. Exit code 0 means the smoke check finished. It does not mean those curves were refreshed.

This story does not close `GAP-201-RANK` or `GAP-501-MODEL`.

### Where the code does it

`scripts/02_model_spike.py`, `--mode smoke`, after the R-hat peek and before the function returns. `--mode full` still writes `metrics.json`. Smoke does not.

When that file is already on disk, smoke prints:

```
existing metrics: <path>
curves were not replaced
```

When it is missing, smoke prints:

```
no curve file yet: <path>
curves were not replaced
```

`<path>` is that client's resolved `models/metrics.json`. For pathc that is `data/clients/pathc/models/metrics.json`.

### Definition of done

- A smoke run prints the lines above and does not overwrite `metrics.json`.
- `tests/test_model_spike_helpers.py` locks the unchanged file and the missing-file line. Meridian sampling is mocked. The test does not run a real MCMC.
- `GAP-201-RANK` and `GAP-501-MODEL` stay open.

Open gap for this story: `GAP-504-SMOKE` in [`docs/learnings/open-gaps.md`](../learnings/open-gaps.md).

## STORY-505 — A failed R-hat full fit must not become the current curves

**Plain language:** A full Meridian fit can miss the R-hat check and still be saved as the model the allocator and the dashboard use. Those readers open `metrics.json` and never look at `dod.rhat_lt_1_05`. If a failed fit replaces that file, the next budget plan uses the failed curves.

**Where the code does it:** `scripts/02_model_spike.py` `--mode full` still writes the posterior predictive PNG and the parameter-recovery note under that client's `models/`. `publish_full_metrics` writes `models/metrics.json` only when max core R-hat is under the threshold (default 1.05). On a miss it prints `curve file not replaced: <path>` and exits 1. The file on disk is left as it was, and a missing file is not created. `--mode smoke` still returns before any of those writes. `src/optimize/curves.py` and the dashboard still do not read `dod.rhat_lt_1_05`.

**Done when:** A failed full fit does not replace `models/metrics.json`. A passing full fit writes `metrics.json` the same way as before. `tests/test_model_spike_helpers.py` locks the failed-fit bytes (existing file unchanged, missing file not created) without running MCMC.

This story does not close `GAP-201-RANK` or `GAP-501-MODEL`.

## STORY-506 — Name the question in the offline brief

No points. No dates. This story is not done.

**Plain language:** Target mode finds the cheapest spend that reaches a KPI. Maximize mode splits a fixed total budget. Both opened with the same sentence, `Move {channel} up…`. Readers treated them as one recommendation.

**Where it lives:** `constraints.mode` is `target` or `maximize` on the allocation (`src/optimize/allocator.py`). `build_fact_pack` copies that field (`src/report/facts.py`). `render_offline` names the question in the opening line (`src/report/brief.py`). The dashboard prints that same offline brief. There is one brief, not a second template.

- `target`: cheapest spend that reaches the KPI target.
- `maximize`: how to split this fixed total budget.

Structured spend, KPI, and saturation flags stay exact. Headline and bullets keep the existing rounding rules.

This story does not close `GAP-201-RANK`, `GAP-501-MODEL`, `GAP-504-SMOKE`, or `GAP-505-RHAT`. `GAP-506-MODE` stays open.

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
