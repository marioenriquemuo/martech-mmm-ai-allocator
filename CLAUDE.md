# CLAUDE.md — MMT&MMM

Working brief for Claude/Cursor on **martech-mmm-ai-allocator** (Origin: `mario-mu-oz-dev/MMT-MMM`).

## Quick facts

| Item | Value |
| --- | --- |
| Product | Enterprise measurement + budget allocation (Bayesian MMM + touchpoint calibration) |
| Local path | `/home/mario/dev/MMT&MMM` |
| Language | Python 3.12 |
| Env | Conda env `mmt-mmm` from `environment.yml` (Miniconda at `~/miniconda3`) |
| Core libs | numpy, pandas, scipy, scikit-learn, pymc, arviz, matplotlib, jupyter, plotly, pyyaml, pydantic, pandera, pyarrow, pytest, streamlit |
| Secrets | `Secret/` gitignored — never read into commits or paste into PRs |
| Docker | `Dockerfile` (micromamba + `environment.yml`) for the dashboard and allocator on port 8501. Full Meridian MCMC is a conda/CPU job. The first image build is heavy. |
| Working branch | `sprint-3-exogenous-multitenant-mmt` (Sprint 3 — Exogenous Controls, Multi-Tenant Architecture & MMT Calibration); Sprint 2 archived on `sprint-2-mvp-optimization-agentic-ui` @ tag `sprint-2-mvp`; Sprint 1 on `main` + `sprint-1-core-data-engine` @ tag `sprint-1-milestone-1` |
| Remotes | `origin` (Origin `mario-mu-oz-dev/MMT-MMM`), `github` (`marioenriquemuo/martech-mmm-ai-allocator`, public) |
| Status | Sprint 1–2 MVP on `main` / tag `sprint-2-mvp`; Sprint 3 active on `sprint-3-exogenous-multitenant-mmt` — brief `docs/sprints/sprint-3.md`; Meridian rank caveat still open — `docs/learnings/open-gaps.md` |

## What we build

1. **Top-down Bayesian MMM** — decay, saturation, incremental lift; continuous updates from new performance data
2. **Bottom-up calibration** — touchpoint / funnel signals that keep the MMM honest vs platform attribution windows
3. **Allocator layer** — optimization scripts that turn posteriors into budget recommendations
4. **Agentic explain layer** — orchestrates scripts and narrates statistical outputs for C-suite (LLMs do not replace the Bayesian math)

## Layout (current)

```
MMT&MMM/
├── environment.yml           # conda env mmt-mmm (+ plotly, pandera, pyarrow, pytest, streamlit, google-meridian)
├── requirements.txt          # direct deps only; conda is the supported install
├── Dockerfile                # micromamba image: dashboard + allocator (first build is heavy)
├── .dockerignore             # excludes Secret/, .git, .env, __pycache__, .conda
├── .env.example              # ANTHROPIC_API_KEY= (offline path needs no key)
├── LICENSE                   # MIT, Mario Muñoz, 2026
├── README.md                 # setup + STORY-101–401 how-to
├── app/streamlit_app.py      # STORY-401 layout (`streamlit run app/streamlit_app.py -- --client_id pathc`)
├── notebooks/README.md       # points at scripts/ and reports/figures/; no .ipynb
├── CLAUDE.md                 # this file
├── AGENTS.md                 # agent entrypoint
├── .python-version           # 3.12
├── .gitignore                # Secret/, conda/python junk, graphify cache
├── .graphifyignore           # scope graphify away from archify package
├── Secret/                   # local-only (gitignored)
├── src/
│   ├── data/generator.py     # STORY-101 Path-C synthetic DGP
│   ├── data/etl.py           # STORY-103 spend panel; STORY-501 main also writes controls
│   ├── data/controls.py      # STORY-501 date-level exogenous controls
│   ├── data/tenants.py       # STORY-502 client filesystem wall
│   ├── data/qa.py            # STORY-104 media detect/repair + hard-fail gate
│   ├── models/transformations.py  # STORY-102 geometric/Weibull/Hill
│   ├── models/meridian_data.py    # STORY-201 parquet → Meridian InputData
│   ├── models/calibration.py      # STORY-503 geo-experiment ROI prior
│   ├── optimize/             # STORY-301 curves + SLSQP allocator
│   │   ├── curves.py         # offline response-curve provider
│   │   └── allocator.py      # maximize KPI / hit target under bounds
│   ├── report/               # STORY-302 fact pack, schema, brief
│   │   ├── facts.py
│   │   ├── schema.py
│   │   └── brief.py
│   └── dashboard/            # STORY-401 view math (no Streamlit)
│       └── view.py
├── scripts/plot_adstock_validation.py  # Plotly Express figures (not Jupyter)
├── scripts/02_model_spike.py           # STORY-201 Meridian smoke/full MCMC
├── scripts/03_allocate_budget.py       # STORY-301 CLI → allocation.json
├── scripts/plot_allocation_teaching.py # STORY-301 Plotly teaching figures
├── scripts/plot_story_302_concepts.py  # STORY-302 Plotly teaching figures
├── scripts/04_csuite_brief.py          # STORY-302 brief CLI (--offline or live)
├── tests/                    # + curves / allocator bounds tests
├── config/clients.yaml       # pathc + wellness (currency, channels, regions)
├── data/raw/                 # pathc corpus: synthetic_ad_spend.csv, ground_truth.json, DATA_CARD, controls/
├── data/clients/             # pathc/models; wellness raw/processed/models/reports
├── data/processed/           # clean_spend.parquet, exogenous_controls.parquet (+ optional qa_repair_log.csv)
├── reports/                  # metrics.json, allocation.json, csuite_brief.json
├── reports/figures/          # Plotly HTML + Meridian PPC + story_301_*.html + story_302_*.html
├── docs/how-to-test.md       # dashboard click-through, no statistics background
├── docs/graphify-archify.md  # index of graphify + archify artifacts
├── docs/learnings/           # story learnings + open-gaps.md registry (Sprint planning)
├── graphify-out/             # knowledge graph (HTML/JSON/report)
├── .archify/                 # architecture diagram runs
└── .cursor/                  # skills + rules
```

## Sprint 1 progress (complete on `main`)

| Story | Status | Notes |
| --- | --- | --- |
| STORY-101 | Done | Path-C generator → `data/raw/`; integer KPI; `DATA_CARD.md` |
| STORY-102 | Done | Shared transforms; DGP imports them; Plotly figures (no notebook); `<1s` perf gate |
| STORY-103 | Done | Pandera schema; date×channel align; zero-fill media / ffill KPI; `clean_spend.parquet` |
| STORY-104 | Done | Media QA detect/repair + audit log; overwrite parquet; hard-fail if unrepaired |
| STORY-201 | Done (spike) | `google-meridian` national weekly; R-hat &lt; 1.05; metrics + PPC + recovery note |

Path-C DGP calls `geometric_adstock` / `hill_saturation` from `src.models.transformations` (single source of truth). Validation plots are Plotly Express HTML under `reports/figures/` — Jupyter notebooks are not required for Sprint 1 DoD.

**STORY-201 open issue:** channel rank recovery vs Path-C is inconsistent (Spearman ≈ −0.6). Details: [`docs/learnings/story-201-meridian.md`](docs/learnings/story-201-meridian.md). All open gaps: [`docs/learnings/open-gaps.md`](docs/learnings/open-gaps.md).

## Sprint 2 progress (archived @ tag `sprint-2-mvp`)

Working branch at close: `sprint-2-mvp-optimization-agentic-ui`. Feature tips: `cursor/story-301-budget-opt-702b` (PR #9), `cursor/story-302-csuite-brief-702b` (PR #10), `cursor/story-401-streamlit-dash-702b`.

| Story | Status | Notes |
| --- | --- | --- |
| STORY-301 | Done (feature tip) | Offline curves → SLSQP allocator; CLI + `reports/allocation.json`; Plotly teaching figures; fail clears `channels` to `{}` |
| STORY-302 | Done (feature tip, step 0–4) | Plots; fact pack; `scripts/04_csuite_brief.py` (`--offline` or live `emit_brief`, `claude-sonnet-4-5`). Structured fields exact; headline/bullets may round (lift 0.12). Not merged |
| STORY-401 | Done (feature tip) | `streamlit run app/streamlit_app.py`. Budget plus each partner’s min/max % (slider + number, 0–100). Optimizer chooses the spend inside those bounds. **Update insights** calls Claude. Key file: `Secret/anthropic_api_key`. Not merged |

Allocator trusts Meridian (or fixture) response curves — same Meridian≠Path-C caveat as above; do not treat allocations as Path-C ground truth. The dashboard shows those same curves. Numbers are incremental KPI, not revenue.

## Sprint 3 progress

| Item | Value |
| --- | --- |
| Name | Sprint 3 — Exogenous Controls, Multi-Tenant Architecture & MMT Calibration |
| Working branch | `sprint-3-exogenous-multitenant-mmt` |
| Goal | Upgrade the data ingestion pipeline to handle organic traffic, holidays, quincenas, and inventory gaps, establish multi-tenant client isolation, and integrate MMT geo-experiment calibration anchors. |
| Brief | [`docs/sprints/sprint-3.md`](docs/sprints/sprint-3.md) |
| Architecture | [`.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html`](.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html) |

| Story | Status | Notes |
| --- | --- | --- |
| STORY-501 | Done (feature tip) | `python -m src.data.etl` writes `clean_spend.parquet` (date × channel) and `exogenous_controls.parquet` (one row per date). Quincena is day 15 or the last calendar day. CSV or in-memory frames, not a live API. Not in the Meridian fit. Open: `GAP-501-API`, `GAP-501-MODEL`. |
| STORY-502 | Done (feature tip) | Default client `pathc` keeps today's raw/processed/reports. `wellness` is only `data/clients/wellness/`. Four dirs: raw, processed, models, reports. `--client_id` (default `pathc`). The wall is the separation, not a second model. |
| STORY-503 | Done (feature tip) | National `roi_m` prior from geo-experiment bounds (`src/models/calibration.py`). Writes `reports/calibration_delta.json`. Does not sample a posterior. Spike `--calibration` exits 1 before `sample_prior` when the gate fails. Omit the flag to keep `PriorDistribution()`. `GAP-201-RANK` stays open. |

Stories sourced from local sprint backlog under `Secret/` (gitignored). Open gaps that may overlap: `GAP-201-RANK` (see `docs/learnings/open-gaps.md`).

STORY-507 is not marked done. Brief: [`docs/sprints/sprint-4.md`](docs/sprints/sprint-4.md). It does not close `GAP-201-RANK` or `GAP-501-MODEL`.

## Key conventions

- Prefer Miniconda env `mmt-mmm`; do not install project packages into conda `base`
- Keep `environment.yml` lean — add deps when code needs them, not “just in case”
- Prefer Plotly Express scripts over Jupyter for Sprint 1 teaching/validation plots
- No look-ahead / leakage in measurement: features and targets must be point-in-time honest
- Flag assumptions that inflate incremental lift or ROI
- Secrets stay in `Secret/`; document only that the folder is gitignored
- Small PRs; update `README.md` / `CLAUDE.md` / `AGENTS.md` when layout or env changes
- Dual remotes: push intentional sprint work to both `origin` and `github`

## Activate and smoke-test

```bash
cd "/home/mario/dev/MMT&MMM"
conda activate mmt-mmm
python -c "import numpy, pandas, scipy, sklearn, pymc, arviz, matplotlib, plotly, yaml, pydantic, pandera, pyarrow; print('ok', pymc.__version__)"
python -c "import meridian; print('meridian', meridian.__version__)"
python -m pytest tests/ -q
python -m src.data.etl   # clean_spend.parquet and exogenous_controls.parquet
python -m src.data.qa
# Dashboard (sliders are local; Update insights calls Claude):
streamlit run app/streamlit_app.py -- --client_id pathc
```

See `AGENTS.md` for agent golden rules and the skills/rules index.
