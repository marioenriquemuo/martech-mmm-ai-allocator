# Open gaps registry

Single list of **current open gaps** for Sprint planning and future review.
Only items evidenced in-repo or in Project-store Bugbot/DoD notes. Status values: `open` | `closed`.

Baseline tip when this registry was first filled: `188e496` (Merge STORY-402 public-ready packaging).
Index: [`README.md`](README.md).

---

## GAP-201-RANK

| Field | Value |
| --- | --- |
| Story | STORY-201 |
| Status | `open` |
| Severity | High (measurement correctness vs Path-C ground truth) |
| Description | Meridian posterior iROAS channel order disagrees with Path-C contribution / `media_beta` order. Speaks to whether posteriors (and downstream allocator curves) recover planted channel strength. |
| Evidence | Deep dive: [`story-201-meridian.md`](story-201-meridian.md). Metrics at tip `188e496`: `reports/metrics.json` → `recovery_spearman: -0.6`, `dod.directional_recovery: false`. Also `reports/parameter_recovery.md`, README / CLAUDE / AGENTS / `data/raw/DATA_CARD.md` open-issue callouts. STORY-503 tightens the national `roi_m` prior from geo-experiment bounds and does not sample a posterior. The spike refuses a failing calibration before `sample_prior`. Neither step refits channel rank, so this gap stays open. |
| Done when | A later recovery/calibration story produces documented channel-rank agreement (or an explicit accepted definitional mismatch with updated DoD), and this gap is closed with a citation to the new evidence. |

---

## GAP-402-LOOM

| Field | Value |
| --- | --- |
| Story | STORY-402 |
| Status | `open` |
| Severity | Medium (portfolio DoD gap; intentional) |
| Description | README still has a placeholder instead of a real 2-minute Loom walkthrough URL. |
| Evidence | `README.md` line: `Walkthrough: add a 2-minute Loom URL here.` Bugbot: Project store `docs/story-402-bugbot.md` (reviewed tip `188e496`) — DoD #2 PASS with gap. |
| Done when | Placeholder replaced with a working Loom (or equivalent) URL that demos the dashboard in ~2 minutes. |

---

## GAP-402-RENAME

| Field | Value |
| --- | --- |
| Story | STORY-402 |
| Status | `closed` (2026-10-14) |
| Severity | Medium (portfolio DoD gap; intentional) |
| Description | Product name in prose is `martech-mmm-ai-allocator`; GitHub remote was `marioenriquemuo/MMT-MMM`. Mario renamed the public GitHub repo and updated the local `github` remote URL. Origin stays `mario-mu-oz-dev/MMT-MMM`. |
| Evidence | GitHub public API `GET https://api.github.com/repos/marioenriquemuo/martech-mmm-ai-allocator` → `"private": false`, `full_name: marioenriquemuo/martech-mmm-ai-allocator`. Local `git remote -v` → `github` = `https://github.com/marioenriquemuo/martech-mmm-ai-allocator.git`. README / AGENTS remotes updated. Prior gap: Bugbot `docs/story-402-bugbot.md` DoD #4 at tip `188e496`. |
| Done when | GitHub repository exists as `marioenriquemuo/martech-mmm-ai-allocator` (or remotes/docs updated to the chosen canonical name) without breaking dual-remote push. **Met** 2026-10-14. |

---

## GAP-402-VISIBILITY

| Field | Value |
| --- | --- |
| Story | STORY-402 |
| Status | `closed` (2026-10-14) |
| Severity | Medium (portfolio DoD gap; intentional) |
| Description | GitHub mirror was private; STORY-402 DoD asked for a public-ready publish path. Mario confirmed publish — repo is public (now at `marioenriquemuo/martech-mmm-ai-allocator` after rename). |
| Evidence | GitHub public API → `"private": false` for `marioenriquemuo/martech-mmm-ai-allocator` (and the prior `MMT-MMM` name before rename). README Local workspace table lists GitHub as public. Prior: Bugbot `docs/story-402-bugbot.md` intentional gap #3 at tip `188e496`. |
| Done when | Mario explicitly publishes (or documents a permanent private decision) and README/AGENTS visibility wording matches reality. **Met** 2026-10-14. |

---

## GAP-402-DOCKERIGNORE

| Field | Value |
| --- | --- |
| Story | STORY-402 |
| Status | `open` |
| Severity | Low (optional housekeeping; not DoD-blocking) |
| Description | `.dockerignore` excludes `Secret/`, `.git`, `.env`, `__pycache__`, `.conda`, but not `.pytest_cache` or `.cursor`. `Dockerfile` `COPY .` can still ship those into the image (noise/size only; not a secret leak). |
| Evidence | `.dockerignore` contents at tip `188e496`. Bugbot `docs/story-402-bugbot.md` optional Low finding. |
| Done when | `.dockerignore` lists `.pytest_cache` and `.cursor` (or equivalent), and a rebuild confirms they are absent from the image context. |

---

## GAP-COMM-KPI

| Field | Value |
| --- | --- |
| Story | Cross-cutting (STORY-301 / 302 / 401 / 402 communication) |
| Status | `open` |
| Severity | Standing caveat (measurement communication, not a code bug) |
| Description | Dashboard, briefs, and README figures are **incremental KPI**, not currency and not client revenue. Easy to misread as ROI dollars. Kept open so Sprint 3+ copy and UI keep the disclaimer visible until product language deliberately changes. |
| Evidence | README intro + STORY-301/302/401 caveats; CLAUDE Sprint 2 note (“Numbers are incremental KPI, not revenue”); AGENTS story caveats; Bugbot packaging review did not close this. |
| Done when | Either (a) product surfaces consistently prevent revenue/$ misreads and the caveat is retired as “handled,” or (b) a later story deliberately redefines output units and updates all user-facing copy. |

---

## GAP-501-API

| Field | Value |
| --- | --- |
| Story | STORY-501 |
| Status | `open` |
| Severity | Medium (ingestion scope) |
| Description | Auxiliary controls load from CSV or in-memory frames. There is no live Search Console or CRM API. |
| Evidence | `src/data/controls.py` `build_controls` (path or DataFrame). `data/raw/controls/`. README STORY-501. No network client in the ETL command. |
| Done when | A story adds a real client without putting keys in git. |

---

## GAP-501-MODEL

| Field | Value |
| --- | --- |
| Story | STORY-501 |
| Status | `open` |
| Severity | High (measurement use) |
| Description | `exogenous_controls.parquet` is aligned to the spend-panel dates and is not passed into Meridian. |
| Evidence | `src/data/etl.py` `main` writes the parquet. `src/models/meridian_data.py` reads `clean_spend.parquet` only. README STORY-501. |
| Done when | A later fit conditions on an explicit, parsimonious subset and records priors plus a holdout. |

---

## GAP-505-RHAT

| Field | Value |
| --- | --- |
| Story | STORY-505 |
| Status | `open` |
| Severity | High (a failed fit must not become the current curves) |
| Description | On `--mode full`, a core R-hat at or above 1.05 must not replace `models/metrics.json`. The allocator and the dashboard read that file and never check `dod.rhat_lt_1_05`, so a failed fit that lands there becomes the current model. |
| Evidence | `scripts/02_model_spike.py` `publish_full_metrics` is the write gate. Default curves for the allocator: `data/clients/pathc/models/metrics.json` (`scripts/03_allocate_budget.py`). Readers that do not check the flag: `src/optimize/curves.py` `MetricsJsonCurveProvider`, `src/dashboard/view.py`, `app/streamlit_app.py`. Smoke mode returns before the write. |
| Done when | A failed full fit leaves an existing `metrics.json` byte-for-byte and does not create it when missing. `tests/test_model_spike_helpers.py` locks that without MCMC. Closing this row does not close `GAP-201-RANK` or `GAP-501-MODEL`. |

---

## Closed / not listed

- `GAP-402-RENAME` — closed 2026-10-14; GitHub is `marioenriquemuo/martech-mmm-ai-allocator` (public). Local `github` remote updated. Origin unchanged.
- `GAP-402-VISIBILITY` — closed 2026-10-14; GitHub mirror is public (`"private": false` via public API). See entry above.
- STORY-402 packaging paths (`app/streamlit_app.py`, `Dockerfile`, `LICENSE`, `requirements.txt`, `.env.example`, `docs/how-to-test.md`) — Bugbot PASS at `188e496`.
- Secret hygiene — Bugbot scanned clean; not an open gap.
- STORY-501 left `GAP-201-RANK` open. New open items are `GAP-501-API` and `GAP-501-MODEL` only. Month-end quincena and the synthetic holiday list are decided.
- STORY-503 prior tightening does not close `GAP-201-RANK`.
