# graphify + archify artifacts

Generated knowledge graph and the current project architecture diagram: Path-C panel → client wall (default `pathc`) → ETL spend panel and date-level `exogenous_controls.parquet` → media QA → Meridian on the spend panel only. Optional `--calibration` must pass the ROI-prior gate before `sample_prior`; a miss exits 1 and does not sample. Then response curves → SLSQP allocator → fact pack / number lock → offline or Claude brief and Streamlit dashboard.

Working branch for this refresh: `cursor/sprint-3-docs-graph-702b` (code tip `fc8a8bb`).

Spike learnings (incl. **open rank-recovery issue** that still applies to allocator inputs): [`docs/learnings/story-201-meridian.md`](learnings/story-201-meridian.md).

## graphify

Scoped via [`.graphifyignore`](../.graphifyignore) (excludes bulky `.cursor/skills/archify` package so the graph reflects the MMM POC).

| Artifact | Path |
| --- | --- |
| Interactive HTML | [`graphify-out/graph.html`](../graphify-out/graph.html) |
| Audit report | [`graphify-out/GRAPH_REPORT.md`](../graphify-out/GRAPH_REPORT.md) |
| Graph JSON | [`graphify-out/graph.json`](../graphify-out/graph.json) |
| Token benchmark | [`graphify-out/benchmark.txt`](../graphify-out/benchmark.txt) |

Regenerated with `graphify update .` after STORY-502 and STORY-503 (client wall, control parquet, calibration gate). Re-run `graphify update .` after code changes.

## archify

**Current:** [`.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html`](../.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html). Client wall (default `pathc`) → ETL (`clean_spend.parquet` and date-level `exogenous_controls.parquet`) → media QA → Meridian national weekly fit on the spend panel only. Controls are not in the fit. The calibration gate runs only with `--calibration`: a pass supplies the national `roi_m` prior; a fail exits 1 before `sample_prior`. Then response curves → SLSQP allocator → fact pack and number lock → offline or Claude brief, and the Streamlit dashboard. The client wall is the industry separation, not a second model.

| Artifact | Path |
| --- | --- |
| HTML diagram | [`.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html`](../.archify/architecture-mmt-sprint3-20261020-215729/architecture-mmt-sprint3.html) |
| Candidate JSON | [`.archify/architecture-mmt-sprint3-20261020-215729/candidate.json`](../.archify/architecture-mmt-sprint3-20261020-215729/candidate.json) |

Pinned revision for evidence: `fc8a8bb011d4441d886e81d642f0bff411e531aa` (STORY-503 calibration gate the diagram cites).

Prior runs kept for history:

- After STORY-501/502, before the calibration gate: [`.archify/architecture-mmt-project/`](../.archify/architecture-mmt-project/)
- Sprint 2 MVP picture: [`.archify/architecture-mmt-mvp-20261013-164444/`](../.archify/architecture-mmt-mvp-20261013-164444/)
- STORY-302 brief only: [`.archify/workflow-mmt-story302-20261013-161023/`](../.archify/workflow-mmt-story302-20261013-161023/)
- STORY-301: [`.archify/architecture-mmt-story301-20261012-120314/`](../.archify/architecture-mmt-story301-20261012-120314/)
- STORY-101→201: [`.archify/architecture-mmt-story101-201-20261009-171324/`](../.archify/architecture-mmt-story101-201-20261009-171324/)
- STORY-101→104: [`.archify/architecture-mmt-story101-104-20261009-151448/`](../.archify/architecture-mmt-story101-104-20261009-151448/)
- STORY-101→103: [`.archify/architecture-mmt-story101-103-20261008-165012/`](../.archify/architecture-mmt-story101-103-20261008-165012/)
- STORY-101+102: [`.archify/architecture-mmt-story101-102-20261008-153042/`](../.archify/architecture-mmt-story101-102-20261008-153042/)
- STORY-101-only: [`.archify/architecture-mmt-story101-20261008-161209/`](../.archify/architecture-mmt-story101-20261008-161209/)
