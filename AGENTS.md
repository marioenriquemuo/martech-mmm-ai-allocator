# AGENTS.md — MMT&MMM

Working guide for AI agents in this Origin repo (`mario-mu-oz-dev/MMT-MMM`).
Read `CLAUDE.md` and `README.md` before changing layout, env, or measurement code.

## What this repo is

**martech-mmm-ai-allocator** — Bayesian Marketing Mix Modeling fused with touchpoint calibration and an agentic layer that turns statistical outputs into budget allocation strategies.

Not a trading lab. Do not import forex-research lab protocol, DSR gates, or BacktestEngine conventions here.

## Golden rules

1. **Accuracy over agreement.** Challenge weak lift / ROI claims; cite data windows and model assumptions.
2. **No leakage.** Features, media, and outcomes must be point-in-time; never use future spend or conversions to fit today’s effect.
3. **Stats do the math.** LLMs orchestrate and explain; PyMC (or agreed Bayesian stack) estimates effects.
4. **Lean env.** Change `environment.yml` only when code needs a package; never pollute conda `base`.
5. **Secrets.** `Secret/` is local-only and **gitignored** — never commit, never paste into PRs or docs beyond “gitignored, never commit”.
6. **Small diffs.** Prefer surgical PRs; update these docs when paths or setup change.

## Layout agents should know

| Path | Role |
| --- | --- |
| `/home/mario/dev/MMT&MMM` | Canonical local checkout (quote the `&`) |
| `environment.yml` | Conda env `mmt-mmm` (Python 3.12 + Bayesian MMM + plotly + pandera + pyarrow + pytest + streamlit) |
| `README.md` | Human overview + Miniconda setup + STORY-101–401 how-to |
| `docs/how-to-test.md` | Dashboard click-through, no statistics background |
| `Dockerfile` | Micromamba image for the dashboard and allocator. Full Meridian MCMC is a conda/CPU job. First build is heavy. |
| `requirements.txt` | Direct deps only; `environment.yml` stays the supported install |
| `LICENSE` | MIT, Mario Muñoz, 2026 |
| `CLAUDE.md` | Project brief / conventions / sprint status |
| `AGENTS.md` | This file — agent entrypoint |
| `docs/learnings/` | Story learnings + [`open-gaps.md`](docs/learnings/open-gaps.md) registry |
| `docs/learnings/story-201-meridian.md` | STORY-201 Meridian learnings + open rank-recovery issue |
| `src/data/generator.py` | STORY-101 Path-C synthetic multi-channel DGP |
| `src/data/etl.py` | STORY-103 spend panel; STORY-501 `main` also writes controls |
| `src/data/controls.py` | STORY-501 date-level exogenous controls (CSV or frames) |
| `src/data/tenants.py` | STORY-502 client filesystem wall (`--client_id`, default `pathc`) |
| `src/models/calibration.py` | STORY-503 geo-experiment ROI prior (`roi_m` only; no posterior). Spike `--calibration` exits 1 before sampling when the gate fails |
| `src/data/qa.py` | STORY-104 media detect / repair / hard-fail gate |
| `src/models/transformations.py` | STORY-102 geometric / Weibull adstock + Hill saturation |
| `src/models/meridian_data.py` | STORY-201 clean parquet → Meridian national `InputData` |
| `src/optimize/curves.py` | STORY-301 offline response-curve provider |
| `src/optimize/allocator.py` | STORY-301 SLSQP budget optimizer (bounds + target KPI) |
| `src/report/facts.py` | STORY-302 fact pack from an allocation plan |
| `src/report/schema.py` | STORY-302 pydantic brief + JSON schema |
| `src/report/brief.py` | STORY-302 offline + live brief from the fact pack |
| `src/dashboard/view.py` | STORY-401 allocator + Plotly figures + offline brief (no Claude) |
| `app/streamlit_app.py` | STORY-401 Streamlit layout (`streamlit run app/streamlit_app.py`) |
| `notebooks/README.md` | Plotly scripts under `scripts/` and `reports/figures/`; no `.ipynb` |
| `scripts/plot_adstock_validation.py` | Plotly Express validation figures (not Jupyter) |
| `scripts/02_model_spike.py` | STORY-201 Meridian smoke / fuller MCMC spike |
| `scripts/03_allocate_budget.py` | STORY-301 CLI → `reports/allocation.json` |
| `scripts/plot_allocation_teaching.py` | STORY-301 Plotly teaching figures |
| `scripts/plot_story_302_concepts.py` | STORY-302 Plotly teaching figures (shift, saturation, lift) |
| `scripts/04_csuite_brief.py` | STORY-302 brief → `reports/csuite_brief.json` (`--offline` or live) |
| `tests/` | Generator, transforms, ETL, controls, QA, Meridian, curves, allocator, `<1s` perf |
| `config/clients.yaml` | `pathc` and `wellness`: currency, channels, regions |
| `data/raw/` | Path-C corpus: CSV + ground truth + `DATA_CARD.md` + `controls/` |
| `data/clients/` | `pathc/models`; `wellness/{raw,processed,models,reports}` |
| `data/processed/` | `clean_spend.parquet`, `exogenous_controls.parquet` (+ optional `qa_repair_log.csv`) |
| `reports/` | `metrics.json`, `allocation.json`, `csuite_brief.json` |
| `reports/figures/` | Plotly HTML + Meridian PPC + `story_301_*.html` + `story_302_*.html` |
| `docs/graphify-archify.md` | Index of graphify + archify artifacts |
| `graphify-out/` | Knowledge graph outputs |
| `.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html` | Current project architecture diagram |
| `.cursor/skills/` | Repo-only skills: `mmt-mmm`, `secret-hygiene`, `archify` |
| `.cursor/rules/` | Repo-only rules: `graphify`, `secret-hygiene` |
| `Secret/` | Local-only; **gitignored** — never commit |

## Sprint status

Working branch: **`sprint-3-exogenous-multitenant-mmt`** — Sprint 3 — Exogenous Controls, Multi-Tenant Architecture & MMT Calibration. Brief: `docs/sprints/sprint-3.md`.

**Sprint 3 goal:** Upgrade the data ingestion pipeline to handle organic traffic, holidays, quincenas, and inventory gaps, establish multi-tenant client isolation, and integrate MMT geo-experiment calibration anchors.

Sprint 1 is complete on `main` (tag `sprint-1-milestone-1`); branch `sprint-1-core-data-engine` kept. Sprint 2 MVP archived on `sprint-2-mvp-optimization-agentic-ui` (tag `sprint-2-mvp`).

- **STORY-101 done** — Path-C generator, integer counts, `DATA_CARD.md`
- **STORY-102 done** — shared transforms; generator imports them; Plotly figures (Jupyter DoD adapted away); perf gate
- **STORY-103 done** — Pandera schema; date×channel align; zero-fill media / ffill KPI; `clean_spend.parquet`
- **STORY-104 done** — media QA detect/repair + audit; overwrite parquet; hard-fail if unrepaired
- **STORY-501 done (feature tip)** — `python -m src.data.etl` writes `clean_spend.parquet` (date × channel) and `exogenous_controls.parquet` (one row per date: organic, brand search, CRM, holiday, quincena, price drop, stockout). Do not sum controls across channels. `baseline_sales` stays on the spend panel. Quincena is day 15 or the last calendar day of the month. Brand search can be a mediator; inventory can be a result of demand. CSV or in-memory frames, not a live API. Controls are not in the Meridian fit. `GAP-201-RANK` stays open. New open items: `GAP-501-API`, `GAP-501-MODEL`.
- **STORY-502 done (feature tip)** — Default client `pathc`. Four directories per client: raw, processed, models, reports. `pathc` keeps `data/raw`, `data/processed`, and `reports` (`models` at `data/clients/pathc/models`). `wellness` uses only `data/clients/wellness/`. `--client_id` defaults to `pathc`. Industry separation is this filesystem wall, not a second model. Regions are labels.
- **STORY-503 done (feature tip)** — `python -m src.models.calibration` turns national geo-experiment ROI bounds into a log-normal `roi_m` prior and writes `reports/calibration_delta.json`. A `bogota` row is ignored. No posterior sample. `GAP-201-RANK` stays open. `scripts/02_model_spike.py --calibration` runs that gate before `sample_prior`. A miss (interval outside the experiment, or scale not tighter than the default prior) exits 1 and does not build Meridian. Omitting `--calibration` keeps `PriorDistribution()`.
- **STORY-504** (not done) — smoke must not look like a new curve file. Brief: `docs/sprints/sprint-4.md`.
- **STORY-201 spike done** — Meridian national weekly (`google-meridian`, adapter, `scripts/02_model_spike.py`, DoD artifacts under `reports/`); learnings in `docs/learnings/story-201-meridian.md` (**open:** rank recovery vs Path-C, Spearman ≈ −0.6)
- **STORY-301 done (feature tip)** — offline response curves → SLSQP allocator (`src/optimize/`, `scripts/03_allocate_budget.py`); teaching figures under `reports/figures/story_301_*.html`; on solver failure `channels` is `{}` (no partial plan). **Caveat:** allocations follow Meridian/fixture curves, not Path-C ground truth.
- **STORY-302 done (feature tip, step 0–4)** — teaching figures `scripts/plot_story_302_concepts.py` (`reports/figures/story_302_*.html`); fact pack, schema, and brief in `src/report/`; CLI `scripts/04_csuite_brief.py` (`--offline` or live, model `claude-sonnet-4-5`). Structured fields stay exact; headline and bullets may round a fact (lift 0.12). Key: `ANTHROPIC_API_KEY` or gitignored `Secret/anthropic_api_key` (never commit). **Caveat:** incremental KPI, not revenue; Meridian ≠ Path-C. Not merged.
- **STORY-401 done (feature tip)** — `conda activate mmt-mmm` then `streamlit run app/streamlit_app.py`. Total budget and each partner’s min % and max % have a slider and a number box (0–100). Mins cannot sum past 100 and a min cannot pass its max; those percents are spend bounds. `optimize_budget` chooses the spend. Charts compare the equal-room baseline with that recommendation. Infeasible bounds show the allocator error and do not call Claude. **Update insights** is the only Claude call (`render_live`); before that click, commentary is the offline brief. Changing a control clears the live brief. Key filename: `Secret/anthropic_api_key` (or `ANTHROPIC_API_KEY`). **Caveat:** incremental KPI, not revenue; Meridian ≠ Path-C. Not merged.

## Skills

User skills in `~/.cursor/skills/` apply here. Do not vendor them into `.cursor/skills/`.

- Global: `ponytail`, `ponytail-*`, `graphify`, `eli5-teacher`, `skill-author`, `text-review-documentation`, `ai-workstation-advisor`
- Repo only: `mmt-mmm`, `secret-hygiene`, `archify`

## Rules

Prefer `~/.cursor/rules/*.mdc` (simplicity, terse comms, get-shit-done, Karpathy, text review). Do not copy those into this repo.

Repo-only `.cursor/rules/`: `graphify.mdc` (this `graphify-out/`), `secret-hygiene.mdc` (this `Secret/`).

Cursor User Rules (Customize → Rules) also apply. Cloud agents do not load `~/.cursor/rules`.

## Remotes and PR conventions

| Remote | URL |
| --- | --- |
| `origin` | `https://origin.cursor.com/mario-mu-oz-dev/MMT-MMM.git` |
| `github` | `https://github.com/marioenriquemuo/martech-mmm-ai-allocator.git` |

- Sprint integration work lands on `sprint-3-exogenous-multitenant-mmt`; push both remotes when asked
- Feature branches: `cursor/<short-topic>-…` when opening separate PRs
- One concern per PR when practical (env, docs, model code)
- Do not commit `Secret/`, `.conda/`, `*.egg-info/`, or notebook checkpoints

## Local env

```bash
cd "/home/mario/dev/MMT&MMM"
conda env create -f environment.yml   # once
conda activate mmt-mmm
python -c "import numpy, pandas, scipy, sklearn, pymc, arviz, matplotlib, plotly, yaml, pydantic, pandera, pyarrow; print('ok', pymc.__version__)"
python -c "import meridian; print('meridian', meridian.__version__)"
python -m pytest tests/ -q
python -m src.data.etl   # clean_spend.parquet and exogenous_controls.parquet
python -m src.data.qa
# Fuller Meridian spike (slow on CPU): python scripts/02_model_spike.py --mode full
# Budget allocate (synthetic fixture): python scripts/03_allocate_budget.py --curves tests/fixtures/synthetic_response_curves.json --budget 60 --min-spend 5 --max-spend 30
# Dashboard: streamlit run app/streamlit_app.py -- --client_id pathc
# Docker (dashboard + allocator; first build is heavy). Full Meridian MCMC stays conda/CPU:
# docker build -t mmt-mmm .
```

## Definition of done (agent tasks)

- [ ] Edited Python compiles / smoke imports pass in `mmt-mmm`
- [ ] No secrets or conda env trees committed
- [ ] `README.md` / `CLAUDE.md` / `AGENTS.md` updated if layout or setup changed
- [ ] Leakage / assumption risks called out when touching measurement code
- [ ] Teaching / validation plots stay Plotly scripts under `scripts/` / `reports/figures/` unless a story explicitly requires notebooks
