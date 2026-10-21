# Sprint 4

Follow-up to the Sprint 3 walkthrough. This file is STORY-505 only.

### STORY-505 — A failed R-hat full fit must not become the current curves

**Plain language:** A full Meridian fit can miss the R-hat check and still be saved as the model the allocator and the dashboard use. Those readers open `metrics.json` and never look at `dod.rhat_lt_1_05`. If a failed fit replaces that file, the next budget plan uses the failed curves.

**Where the code does it:** `scripts/02_model_spike.py` `--mode full` still writes the posterior predictive PNG and the parameter-recovery note under that client's `models/`. `publish_full_metrics` writes `models/metrics.json` only when max core R-hat is under the threshold (default 1.05). On a miss it prints `curve file not replaced: <path>` and exits 1. The file on disk is left as it was, and a missing file is not created. `--mode smoke` still returns before any of those writes. `src/optimize/curves.py` and the dashboard still do not read `dod.rhat_lt_1_05`.

**Done when:** A failed full fit does not replace `models/metrics.json`. A passing full fit writes `metrics.json` the same way as before. `tests/test_model_spike_helpers.py` locks the failed-fit bytes (existing file unchanged, missing file not created) without running MCMC.

This story does not close `GAP-201-RANK` or `GAP-501-MODEL`.
