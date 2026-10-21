# Sprint 4

This file records STORY-504 only.

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
