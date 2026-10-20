# DATA_CARD — `synthetic_ad_spend.csv` (STORY-101)

Path-C synthetic multi-channel marketing panel for portfolio / recovery tests.

| Field | Value |
| --- | --- |
| Generator | `python -m src.data.generator` (`seed=42`) |
| Transforms | DGP calls `geometric_adstock` / `hill_saturation` from `src.models.transformations` (STORY-102) |
| Rows | 2,912 = 728 days × 4 channels |
| Grain | **Channel-day only** (`meta`, `google`, `tiktok`, `tv`) |
| Locked artifact | Committed CSV matches seed=42 **after** integer post-processing |

## Columns

| Column | Type | Meaning |
| --- | --- | --- |
| `date` | ISO date | Calendar day |
| `channel` | string | Channel ID |
| `spend` | float USD | Media spend (currency; may be fractional) |
| `impressions` | int ≥ 0 | Rounded delivery counts |
| `clicks` | int ≥ 0 | Rounded click counts |
| `baseline_sales` | int ≥ 0 | **Site-wide daily order/unit counts** (KPI) |

Integer columns are produced by continuous DGP → `round` → clip ≥ 0 → `int64`.

## Long-format rule for `baseline_sales`

`baseline_sales` is the **same site-wide daily KPI repeated on every channel row** for that date.

- Recover the series with `groupby("date")["baseline_sales"].first()` (or `.mean()`).
- **Do not sum across channels** — that would multiply the KPI by 4.

## Real-life mapping

| Synthetic column | Typical source |
| --- | --- |
| `spend`, `impressions`, `clicks` | Partner / ad-platform exports |
| `baseline_sales` | Site / CRM daily orders (units) |
| Join key | `date` (+ `channel` for media only) |

## KPI decision (locked for STORY-101)

- `baseline_sales` = **units / orders only** (integer counts).
- **No `revenue` column** in this story (keeps the STORY-101 column DoD).
- USD revenue can be the client KPI in a **later story / ETL mapping** without changing this schema.

## Out of scope (do not reopen STORY-101)

- Campaign / ad-set / creative grain
- Funnel stages (brand vs retargeting, prospecting, etc.)
- Multiple KPIs or revenue alongside units

Those are planned later; this file stays channel-level only.

## STORY-103 ETL → processed Parquet

| Item | Value |
| --- | --- |
| Module | `python -m src.data.etl` (`src/data/etl.py`) |
| Schema | Pandera `SpendPanelSchema` |
| Output | `data/processed/clean_spend.parquet` |
| Dirty practice fixture | `tests/fixtures/dirty_ad_spend.csv` (google omitted ~2 days; blank KPI one day) |

**Fill rules (locked):** after date×channel alignment, missing `spend` / `impressions` / `clicks` → **0** (pause / absent from export). Missing `baseline_sales` → **forward-fill** site-wide daily KPI. Raw `synthetic_ad_spend.csv` stays clean/locked.

## STORY-501 exogenous controls (date grain)

The same command also writes `data/processed/exogenous_controls.parquet`. Controls are **date-level** (one row per date, not per channel). A missing auxiliary day is **zero-filled**. `quincena_flag` is 1 on day 15 or the last calendar day of the month. `holiday_flag`, `price_drop_flag`, and `inventory_oos_flag` are one flag each from the CSVs under `data/raw/controls/`.

`baseline_sales` stays on the spend panel. Do not sum control columns across channels.

`brand_search_volume` can be a mediator (media can cause brand search). `inventory_oos_flag` can be a result of demand.

## STORY-502 client wall

Default client is `pathc`. These Path-C files stay in `data/raw` and `data/processed`; reports stay in `reports`. Models for `pathc` are `data/clients/pathc/models`. Client `wellness` is only `data/clients/wellness/` with `raw`, `processed`, `models`, and `reports`. Industry separation is that filesystem wall, not a second model. `regions` in `config/clients.yaml` is a label.

## STORY-503 geo-experiment prior

`data/raw/calibration/geo_experiment.json` holds synthetic national ROI bounds for `meta` and `google`, plus one `bogota` row that the national prior ignores. These numbers are not Path-C ground truth. `python -m src.models.calibration` writes `reports/calibration_delta.json` and does not sample a posterior. `scripts/02_model_spike.py --calibration` exits 1 before `sample_prior` when a calibrated channel misses the experiment interval or does not tighten scale. Omitting `--calibration` keeps `PriorDistribution()`. `GAP-201-RANK` stays open.

## STORY-104 media QA (post-ETL)

| Item | Value |
| --- | --- |
| Module | `python -m src.data.qa` (`src/data/qa.py`) |
| Input / output | Overwrites `data/processed/clean_spend.parquet` when clean or fully repaired |
| Audit log | `data/processed/qa_repair_log.csv` (written only when ≥1 repair) |
| Hard fail | Exit ≠ 0 if unrepaired anomalies remain → training parquet not overwritten |
| Immutable | `spend`, `baseline_sales` never changed |
| Fixture | `tests/fixtures/anomalous_spend.csv` (CTR collapse + IPS spike + insufficient-history case) |

**Rules (v1):** 14-day trailing activity window; ≥7 prior `spend > 0` days to repair. CTR collapse when impressions ≥ 1000 and clicks ≪ median CTR; IPS outlier when spend ≈ median but impressions/spend outside [0.5×, 2.0×] median IPS.

## STORY-201 Meridian grain (weekly)

Meridian national InputData defaults to **weekly** periods (`freq="W"`, week ending Sunday) via `src/models/meridian_data.py`. Spike learnings + **open rank-recovery issue**: [`docs/learnings/story-201-meridian.md`](../../docs/learnings/story-201-meridian.md).

| Series | Weekly aggregation |
| --- | --- |
| KPI (`baseline_sales` → national daily first, then week) | **Sum of daily units** (flow / count aggregation) |
| `spend`, `impressions` per channel | Sum |
| `revenue_per_kpi` | Mean (synthetic constant 1.0) |

Do **not** confuse with long-format channel stacking: daily KPI is still recovered with `groupby("date").first()` before the week sum.

**Open issue (post-POC):** Meridian iROAS channel order does not match Path-C contribution / `media_beta` order (Spearman ≈ −0.6). See the learning doc — not a silent pass.
