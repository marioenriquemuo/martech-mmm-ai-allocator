# Sprint 3 — Exogenous Controls, Multi-Tenant Architecture & MMT Calibration

| Item | Value |
| --- | --- |
| Working branch | `sprint-3-exogenous-multitenant-mmt` |
| Goal | Upgrade the data ingestion pipeline to handle organic traffic, holidays, quincenas, and inventory gaps, establish multi-tenant client isolation, and integrate MMT geo-experiment calibration anchors. |
| Builds on | Sprint 1–2 MVP on `main` / `sprint-2-mvp-optimization-agentic-ui` (tag `sprint-2-mvp`) |
| Duration (local sprint file) | 1 week (Days 15–21) |
| Story points (local sprint file) | 18 |
| Source of story IDs | Local sprint file under `Secret/` (gitignored) — titles/DoD summarized here; never commit that file |

## How this builds on Sprint 1–2

Sprint 1–2 delivered a single-tenant measurement → allocation → explain path:

1. **Path-C synthetic DGP** + shared adstock/saturation transforms → ETL/QA → `clean_spend.parquet`, plus STORY-501 date-level `exogenous_controls.parquet` (not in the Meridian fit yet)
2. **Meridian national weekly** MMM spike (`scripts/02_model_spike.py`) → response curves
3. **SLSQP allocator** (`src/optimize/`) → `reports/allocation.json`
4. **Fact pack + Claude brief** (`src/report/`, `scripts/04_csuite_brief.py`)
5. **Streamlit dashboard** (`app/streamlit_app.py`) with bounds + offline/live insights

Sprint 3 hardens that stack for enterprise use: control for non-media confounders, isolate clients, and anchor the national ROI prior with geo-experiment bounds — without inventing a new allocator/UI MVP.

## Workstreams

### 1. Exogenous Controls

**Plain language:** Media alone is not the whole world. Holidays, paydays, organic search, promos, price, and stockouts move the KPI. If the MMM ignores them, paid channels get credit (or blame) they do not deserve.

**Technical intent:** Extend the ingestion / alignment layer so non-media regressors land on the same time index as spend and conversions, then condition the measurement model on those controls.

**Today:** `python -m src.data.etl` writes `clean_spend.parquet` (date × channel) and `exogenous_controls.parquet` (one row per date) from CSV or in-memory frames, not a live API. Quincena is day 15 or the last calendar day of the month. Do not sum controls across channels. `baseline_sales` stays on the spend panel. Brand search can be a mediator. Inventory can be a result of demand. Meridian still fits the post-QA spend panel only.

**Architecture “done” (likely):** Aux inputs aligned without null holes; control columns available as regression conditioning for Meridian (or the agreed Bayesian stack); tests prove date alignment with spend/KPI. Detailed DoD lives with STORY-501 below.

### 2. Multi-Tenant Architecture

**Plain language:** One codebase, many clients — without mixing their data, configs, or model runs.

**Technical intent:** Partition raw/processed data, model artifacts, and reports by `client_id`; scripts take an explicit tenant flag; config maps currency, channels, and geography per client.

**Today:** `config/clients.yaml` lists `pathc` and `wellness` (currency, channels, one region label). `--client_id` defaults to `pathc` on ETL, QA, the spike, the allocator, the brief, calibration, and Streamlit. `pathc` keeps `data/raw`, `data/processed`, and `reports`; models are `data/clients/pathc/models`. `wellness` is only `data/clients/wellness/` (`raw`, `processed`, `models`, `reports`). `src/data/tenants.py` raises `TenantError` when a path lands in another client. Industry separation is this filesystem wall, not a second model. Regions are labels.

**Landed:** Client config, `--client_id`, and a fail-closed path check. Other clients stay under `data/clients/{client_id}/`. Detailed behavior is STORY-502 below.

### 3. MMT Calibration

**Plain language:** Top-down MMM should be checked against bottom-up truth — geo lift tests / MMT — so platform attribution windows do not quietly warp channel strength.

**Technical intent:** Ingest structured experiment lift bounds and use them as informative priors / anchors in Meridian; emit a before/after calibration delta report.

**Today:** `src/models/calibration.py` reads that client's `raw/calibration/geo_experiment.json` and writes `reports/calibration_delta.json` (for `pathc`: `data/raw/calibration/geo_experiment.json` and `reports/calibration_delta.json`). National `roi` bounds become a log-normal `roi_m` prior. A `bogota` row is ignored. The calibration command does not sample a posterior. `scripts/02_model_spike.py --calibration` runs the gate before `sample_prior`: the central interval must sit inside the experiment bounds, and the scale must be tighter than the default prior. A miss prints the reason and exits 1. The spike does not build the model. Omitting `--calibration` keeps `PriorDistribution()`. The JSON is synthetic, not a live MMT feed and not Path-C ground truth. **GAP-201-RANK** stays open (Spearman ≈ −0.6).

**Landed:** Calibration module, delta report, and a spike gate that refuses a failing prior before sampling. No city model. Detailed behavior is STORY-503 below.

## Stories (from local sprint file)

Stories below are **not invented** — they come from the local Sprint 3 backlog file (gitignored). High-level titles and DoD only.

### STORY-501 — Exogenous Control Variables & Organic Traffic ETL Pipeline (5 pts)

- Done on `cursor/story-501-exogenous-etl-702b`. ETL `main` writes the date-level control matrix (`organic_seo_clicks`, `brand_search_volume`, `crm_email_volume`, `holiday_flag`, `quincena_flag`, `price_drop_flag`, `inventory_oos_flag`). Tests cover alignment with the spend panel and no nulls.
- Still open: `GAP-501-API` (no live Search Console or CRM API) and `GAP-501-MODEL` (controls are not passed into Meridian). `GAP-201-RANK` stays open.

### STORY-502 — Multi-Tenant Data & Model Isolation Directory Structure (5 pts)

- Done on this branch (`8a2eca3` through `8d52c32`). `config/clients.yaml` lists `pathc` and `wellness`. `--client_id` defaults to `pathc`.
- `pathc` keeps `data/raw`, `data/processed`, and `reports`. Models are `data/clients/pathc/models`. `wellness` is only `data/clients/wellness/` with `raw`, `processed`, `models`, and `reports`.
- `src/data/tenants.py` raises `TenantError` on a cross-client path. Tests: `tests/test_tenants.py`. Industry separation is this filesystem wall, not a second model. Regions are labels.
- Original DoD asked for raw/processed/weights/reports. Landed names are raw, processed, models, and reports.

### STORY-503 — MMT Geo-Experiment Prior Calibration Module (8 pts)

- Done on this branch (`58434b4` through `fc8a8bb`). `python -m src.models.calibration` writes `reports/calibration_delta.json` from that client's geo-experiment JSON.
- National `roi` bounds become a log-normal `roi_m` prior. A `bogota` row does not move it. The command does not sample a posterior.
- The spike gate: `scripts/02_model_spike.py --calibration` calls `build_report` before `sample_prior`. A calibrated channel fails when its central interval misses the experiment bounds or its scale is not tighter than the default prior. The process exits 1 and does not build Meridian. Omitting `--calibration` keeps `PriorDistribution()`.
- The checked-in JSON is synthetic. It is not a live MMT feed and not Path-C ground truth. There is no city model. `GAP-201-RANK` stays open.
- Original DoD asked for live experiment results and regional drift constrained by those outcomes. That part is not in this code.

## Open gaps Sprint 3 may or may not touch

From [`docs/learnings/open-gaps.md`](../learnings/open-gaps.md):

| Gap | Status | Sprint 3 relevance |
| --- | --- | --- |
| **GAP-201-RANK** | `open` | May be addressed indirectly via STORY-503 MMT priors / recovery work — only close when new evidence shows rank agreement or an accepted definitional mismatch. |
| **GAP-402-LOOM** | `open` | Portfolio DoD; not required for Sprint 3 workstreams. |
| **GAP-402-DOCKERIGNORE** | `open` | Optional housekeeping; not required for Sprint 3 workstreams. |
| **GAP-COMM-KPI** | `open` | Standing communication caveat (incremental KPI ≠ revenue); keep visible in copy/UI. |
| **GAP-501-API** | `open` | Controls load from CSV or frames. No live Search Console or CRM API. |
| **GAP-501-MODEL** | `open` | `exogenous_controls.parquet` is aligned and not passed into Meridian. |
| GAP-402-RENAME / GAP-402-VISIBILITY | `closed` | No Sprint 3 action. |

## Remotes

Push Sprint 3 commits to both `origin` and `github` on `sprint-3-exogenous-multitenant-mmt`. Do not force-push. Do not delete tags (`sprint-2-mvp`, `sprint-1-milestone-1`, …).
