# Graph Report - workspace  (2026-10-20)

## Corpus Check
- 71 files · ~44,443 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 861 nodes · 2038 edges · 59 communities (41 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 92 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Exogenous Control ETL
- SLSQP Allocator Core
- Media QA Gate
- Calibration ROI Prior
- Budget CLI Parser
- Meridian Spike MCMC
- Allocation Teaching Plots
- Path-C Data Generator
- Brief API Key Lock
- Geometric Adstock Tests
- Meridian Input Adapter
- Agent Repo Conventions
- Brief Schema Models
- Claude Brief Renderer
- Fact Pack Numbers
- C-Suite Brief CLI
- Story Teaching Scripts
- Adstock Validation Plots
- Open Gap Registry
- Dashboard Percent Bounds
- Media Transform Library
- Sprint Data Lineage
- Streamlit Dashboard App
- Dashboard View Math
- Meridian Spike Learnings
- Sprint 3 Brief
- Dashboard View Tests
- Hill Saturation Tests
- Path-C Panel Docs
- Transform Speed Gate
- Calibration Gate Docs
- Graphify Archify Index
- Dashboard How To Test
- README Product Stories
- Client Filesystem Wall
- Pathc Posterior Chart
- Reports Posterior Chart
- Synced Slider Controls
- Pathc Recovery Note
- Reports Recovery Note
- Project Skill Notes
- Graphify Scope Files
- Notebook Pointer
- Secret Directory
- Allocation vs Baseline Figure
- Fixture Response Curves
- Story 301 Response Curves
- Toy Diminishing Returns
- Budget Shift Figure
- KPI Lift Figure
- Saturation Figure
- Date-Level Control Figure

## God Nodes (most connected - your core abstractions)
1. `MetricsJsonCurveProvider` - 46 edges
2. `load_client()` - 35 edges
3. `build_dashboard()` - 27 edges
4. `build_fact_pack()` - 27 edges
5. `optimize_budget()` - 26 edges
6. `resolve_client_path()` - 25 edges
7. `build_controls()` - 23 edges
8. `generate()` - 21 edges
9. `render_offline()` - 21 edges
10. `weibull_adstock()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `GAP-501-API` --references--> `build_controls()`  [INFERRED]
  docs/learnings/open-gaps.md → src/data/controls.py
- `pathc models parameter recovery note` --semantically_similar_to--> `reports parameter recovery note`  [INFERRED] [semantically similar]
  data/clients/pathc/models/parameter_recovery.md → reports/parameter_recovery.md
- `main()` --uses--> `TenantError`  [INFERRED]
  app/streamlit_app.py → src/data/tenants.py
- `_kpi()` --uses--> `MetricsJsonCurveProvider`  [INFERRED]
  scripts/plot_story_302_concepts.py → src/optimize/curves.py
- `test_path_inside_other_client_raises()` --uses--> `TenantError`  [INFERRED]
  tests/test_calibration.py → src/data/tenants.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Secret Hygiene Across Project Docs** — _cursor_skills_secret_hygiene_skill_secret_hygiene, _cursor_skills_mmt_mmm_skill_secret_folder [INFERRED 0.85]
- **Sprint 3 workstreams** — docs_sprints_sprint_3_sprint_3_exogenous_controls_multi_tenant_architecture_mmt_calibration, docs_sprints_sprint_3_story_501, docs_sprints_sprint_3_story_502, docs_sprints_sprint_3_story_503 [EXTRACTED 1.00]
- **Calibration gate before sample_prior** — docs_sprints_sprint_3_story_503, scripts_02_model_spike, readme_sample_prior, readme_roi_m, readme_prior_distribution [EXTRACTED 1.00]
- **STORY-501 control ingestion and open model gaps** — docs_sprints_sprint_3_story_501, agents_src_data_etl, readme_exogenous_controls_parquet, docs_learnings_open_gaps_gap_501_api, docs_learnings_open_gaps_gap_501_model [EXTRACTED 1.00]
- **Labeled series on the Meridian posterior predictive chart** — data_clients_pathc_models_posterior_predictive_actual_kpi, data_clients_pathc_models_posterior_predictive_posterior_expected_mean, data_clients_pathc_models_posterior_predictive_ci_90 [EXTRACTED 1.00]

## Communities (59 total, 18 thin omitted)

### Community 0 - "Exogenous Control ETL"
Cohesion: 0.06
Nodes (39): build_figure(), main(), _assert_matches_panel(), build_controls(), _count_col(), _counts(), _dated(), _flag() (+31 more)

### Community 1 - "SLSQP Allocator Core"
Cohesion: 0.06
Nodes (35): _bounds_dict(), _bounds_gate(), _constraints(), _curve_max_spends(), _fail_result(), _feasible_start(), _maximize(), objective() (+27 more)

### Community 2 - "Media QA Gate"
Cohesion: 0.09
Nodes (27): detect_anomalies(), load_panel(), main(), _prior_activity(), repair_panel(), _row_index(), run_qa(), sort_panel_by_channel() (+19 more)

### Community 3 - "Calibration ROI Prior"
Cohesion: 0.08
Nodes (27): build_report(), central_bounds(), default_roi_params(), gate_reasons(), _inside(), load_experiments(), loc_scale(), matched_experiments() (+19 more)

### Community 4 - "Budget CLI Parser"
Cohesion: 0.10
Nodes (23): build_parser(), main(), _parse_spend_arg(), run_allocate(), _check_id(), _inside(), list_processed(), _load_all() (+15 more)

### Community 5 - "Meridian Spike MCMC"
Cohesion: 0.10
Nodes (19): _analyzer(), _build_mmm(), _core_rhat_rows(), _jsonable(), main(), _mcmc_cfg(), _parameter_recovery(), _parse_args() (+11 more)

### Community 6 - "Allocation Teaching Plots"
Cohesion: 0.11
Nodes (16): _bar_frame(), build_curves_figure(), build_parser(), _curve_frame(), _equal_room_baseline(), main(), write_allocation_bars(), main() (+8 more)

### Community 7 - "Path-C Data Generator"
Cohesion: 0.11
Nodes (20): ground_truth.json, assert_valid(), _baseline_sales(), coerce_integer_columns(), generate(), _impressions_clicks(), main(), planted_ground_truth() (+12 more)

### Community 8 - "Brief API Key Lock"
Cohesion: 0.14
Nodes (19): load_api_key(), numbers_match(), _allocation(), _cli(), _fake_client(), _matching_payload(), _run(), test_cli_failed_allocation_exits_nonzero() (+11 more)

### Community 9 - "Geometric Adstock Tests"
Cohesion: 0.11
Nodes (17): geometric_adstock(), long_pulse(), pulse(), test_2d_channels_by_time(), test_length_preserved(), test_matches_recursive_definition(), test_nonnegative_when_x_nonnegative(), test_pulse_decay_theta_half() (+9 more)

### Community 10 - "Meridian Input Adapter"
Cohesion: 0.16
Nodes (10): load_clean_panel(), load_meridian_input(), panel_to_national_wide(), wide_to_input_data(), _mini_panel(), test_load_clean_panel_missing_columns(), test_load_meridian_input_from_committed_parquet(), test_panel_to_national_wide_daily_kpi_not_summed_across_channels() (+2 more)

### Community 11 - "Agent Repo Conventions"
Cohesion: 0.09
Nodes (20): archify, data/raw/, github remote, martech-mmm-ai-allocator, mmt-mmm conda env, origin remote, sprint-1-core-data-engine, STORY-101 (+12 more)

### Community 12 - "Brief Schema Models"
Cohesion: 0.16
Nodes (11): ChannelFact, ChannelShift, CsuiteBrief, FactPack, _brief_from(), _load(), test_brief_round_trip_and_drift_fails_lock(), test_equal_room_baseline_and_alpha_ceiling() (+3 more)

### Community 13 - "Claude Brief Renderer"
Cohesion: 0.19
Nodes (11): build_messages(), _field(), _fmt(), _headline(), _lift_bullet(), render_live(), render_offline(), _saturation_bullet() (+3 more)

### Community 14 - "Fact Pack Numbers"
Cohesion: 0.18
Nodes (10): _allowed_numbers(), _bound(), build_fact_pack(), _concentration_note(), _equal_room(), first_mismatch(), _first_prose_mismatch(), _same() (+2 more)

### Community 15 - "C-Suite Brief CLI"
Cohesion: 0.17
Nodes (7): _update_insights(), build_parser(), _fail(), main(), _redact(), format_brief(), MissingApiKey

### Community 16 - "Story Teaching Scripts"
Cohesion: 0.17
Nodes (5): _equal_room_baseline(), _kpi(), _long_frame(), main(), _write()

### Community 17 - "Adstock Validation Plots"
Cohesion: 0.19
Nodes (7): reports/figures/, STORY-102, build_geometric_figure(), build_hill_figure(), build_weibull_figure(), main(), _pulse_frame()

### Community 18 - "Open Gap Registry"
Cohesion: 0.17
Nodes (15): src.data.controls, Dockerfile, .dockerignore, Closed / not listed, GAP-402-DOCKERIGNORE, GAP-402-LOOM, GAP-402-RENAME, GAP-402-VISIBILITY (+7 more)

### Community 19 - "Dashboard Percent Bounds"
Cohesion: 0.14
Nodes (7): clamp_percent(), clamp_percents(), default_curves_path(), slider_bounds(), _slider_step(), test_default_curves_path_prefers_metrics(), test_slider_defaults_are_feasible()

### Community 20 - "Media Transform Library"
Cohesion: 0.16
Nodes (6): weibull_adstock(), _weibull_n_lags(), _weibull_pdf_weights(), test_weibull_2d_channels_by_time(), test_weibull_normalize_unit_mass_on_constant(), test_weibull_rejects_bad_params()

### Community 21 - "Sprint Data Lineage"
Cohesion: 0.26
Nodes (13): src.data.etl, src.models.meridian_data, pathc models parameter recovery note, clean_spend.parquet, DATA_CARD, Path-C synthetic panel, STORY-104 media QA gate, GAP-501-MODEL (+5 more)

### Community 22 - "Streamlit Dashboard App"
Cohesion: 0.23
Nodes (8): _client_id(), _commentary(), main(), _clamp_max(), _clamp_min(), _redact(), clamp_max_percent(), clamp_min_percent()

### Community 23 - "Dashboard View Math"
Cohesion: 0.36
Nodes (7): build_dashboard(), _failed(), _kpi_move_figure(), _response_figure(), _saturation_figure(), _show_units(), _spend_move_figure()

### Community 24 - "Meridian Spike Learnings"
Cohesion: 0.17
Nodes (12): How to run, Likely investigation axes (post-POC), Meridian is a local pip library, National weekly adapter, Open issue — rank recovery vs Path-C is inconsistent, R-hat, Related docs, Smoke vs full (+4 more)

### Community 25 - "Sprint 3 Brief"
Cohesion: 0.17
Nodes (12): 1. Exogenous Controls, 2. Multi-Tenant Architecture, 3. MMT Calibration, How this builds on Sprint 1–2, Open gaps Sprint 3 may or may not touch, Remotes, Sprint 3 — Exogenous Controls, Multi-Tenant Architecture & MMT Calibration, Stories (from local sprint file) (+4 more)

### Community 26 - "Dashboard View Tests"
Cohesion: 0.32
Nodes (6): format_units(), partner_investments(), _forbid_claude(), test_infeasible_maxes_show_allocator_error(), test_optimizer_respects_min_max_spends(), test_second_min_clamps_so_mins_cannot_pass_100()

### Community 27 - "Hill Saturation Tests"
Cohesion: 0.17
Nodes (8): hill_saturation(), test_hill_bounds_in_unit_interval(), test_hill_clips_negative_x(), test_hill_half_saturation_at_K(), test_hill_larger_S_steeper_around_K(), test_hill_monotonic_in_x(), test_hill_rejects_bad_params(), test_hill_shape_preserved()

### Community 28 - "Path-C Panel Docs"
Cohesion: 0.31
Nodes (9): Path-C synthetic multi-channel DGP, geometric_adstock, hill_saturation, Channel-day grain, Path-C synthetic multi-channel marketing panel, meta google tiktok tv channels, transformations perf gate <1s, synthetic_ad_spend.csv (+1 more)

### Community 29 - "Transform Speed Gate"
Cohesion: 0.31
Nodes (3): _panel(), _run_transforms(), test_transforms_two_years_daily_under_one_second()

### Community 30 - "Calibration Gate Docs"
Cohesion: 0.29
Nodes (8): src.models.calibration, geo_experiment.json, graphify and archify artifact index, STORY-503 MMT Geo-Experiment Calibration Gate, calibration_delta.json, PriorDistribution, roi_m prior, sample_prior

### Community 31 - "Graphify Archify Index"
Cohesion: 0.32
Nodes (3): archify, graphify, graphify + archify artifacts

### Community 32 - "Dashboard How To Test"
Cohesion: 0.25
Nodes (7): 1. What you are testing, 2. Install once, 3. Automated test, 4. Dashboard test, no API key, 5. Optional live test, 6. What a good result is not, How to test this marketing mix modeling tool

### Community 33 - "README Product Stories"
Cohesion: 0.43
Nodes (6): How to test the dashboard, GAP-201-RANK, GAP-COMM-KPI, STORY-301 SLSQP allocator, STORY-302 C-suite brief, STORY-401 Streamlit dashboard

### Community 34 - "Client Filesystem Wall"
Cohesion: 0.53
Nodes (5): --client_id, src.data.tenants, pathc, wellness, STORY-502 Multi-Tenant Client Wall

### Community 35 - "Pathc Posterior Chart"
Cohesion: 0.40
Nodes (6): actual KPI, Meridian posterior predictive chart (national, weekly): KPI (units) versus time index, 90% CI, KPI (units), posterior expected (mean), Actual KPI rises and falls repeatedly across time index 0-100, while the posterior expected mean levels off after an early rise and the 90% CI becomes a narrow band around that mean; later actual peaks and troughs leave the band, and one actual peak crosses above the 400000 KPI (units) gridline

### Community 36 - "Reports Posterior Chart"
Cohesion: 0.53
Nodes (6): Meridian posterior predictive (national, weekly), actual KPI, 90% CI, KPI (units), national weekly, posterior expected (mean), Actual KPI is cyclical and leaves the 90% CI for long stretches; the posterior mean rises early then stays near the 360000 gridline

### Community 37 - "Synced Slider Controls"
Cohesion: 0.60
Nodes (4): _synced_number(), _from_number(), _from_slider(), _store()

### Community 38 - "Pathc Recovery Note"
Cohesion: 0.40
Nodes (4): Estimated iROAS (posterior mean, units per $), Parameter recovery note (STORY-201), Path-C planted signals, Rank comparison

### Community 39 - "Reports Recovery Note"
Cohesion: 0.40
Nodes (4): Estimated iROAS (posterior mean, units per $), Parameter recovery note (STORY-201), Path-C planted signals, Rank comparison

### Community 40 - "Project Skill Notes"
Cohesion: 0.67
Nodes (4): archify Skill, MMT&MMM Project Conventions, Secret/ Local-Only Path, Secret Hygiene

## Ambiguous Edges - Review These
- `GAP-201-RANK` → `STORY-503 MMT Geo-Experiment Calibration Gate`  [AMBIGUOUS]
  docs/sprints/sprint-3.md · relation: might_inform

## Knowledge Gaps
- **34 isolated node(s):** `archify Skill`, `src.data.tenants`, `src.models.calibration`, `roi_m prior`, `PriorDistribution` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 305 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `STORY-503 MMT Geo-Experiment Calibration Gate` connect `Calibration Gate Docs` to `README Product Stories`, `Meridian Spike MCMC`, `Open Gap Registry`, `Sprint Data Lineage`, `Sprint 3 Brief`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `MetricsJsonCurveProvider` (e.g. with `_bar_frame()` and `build_curves_figure()`) actually correct?**
  _`MetricsJsonCurveProvider` has 24 INFERRED edges - model-reasoned connections that need verification._
- **What connects `archify Skill`, `src.data.tenants`, `src.models.calibration` to the rest of the system?**
  _34 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Exogenous Control ETL` be split into smaller, more focused modules?**
  _Cohesion score 0.06199285946121389 - nodes in this community are weakly interconnected._
- **Why does `STORY-201 Meridian spike` connect `Sprint Data Lineage` to `README Product Stories`, `Open Gap Registry`, `Meridian Spike MCMC`, `Calibration Gate Docs`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Should `SLSQP Allocator Core` be split into smaller, more focused modules?**
  _Cohesion score 0.06241519674355495 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `GAP-201-RANK` and `STORY-503 MMT Geo-Experiment Calibration Gate`?**
  _Edge tagged AMBIGUOUS (relation: might_inform) - confidence is low._