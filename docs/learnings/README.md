# Learnings

Durable story learnings and the single registry of **open gaps** for future review and Sprint planning.

| File | Role |
| --- | --- |
| [`open-gaps.md`](open-gaps.md) | Registry of every current open gap (status, evidence, done criteria) |
| [`story-201-meridian.md`](story-201-meridian.md) | STORY-201 Meridian spike learnings + rank-recovery deep dive |

## Open gaps

Use [`open-gaps.md`](open-gaps.md) as the checklist. At tip `188e496` (pre-registry), the open set is:

- [ ] `GAP-201-RANK` — Meridian iROAS rank vs Path-C (Spearman ≈ −0.6)
- [ ] `GAP-402-LOOM` — README Loom walkthrough still a placeholder
- [x] `GAP-402-RENAME` — closed 2026-10-14; GitHub is `marioenriquemuo/martech-mmm-ai-allocator`
- [x] `GAP-402-VISIBILITY` — closed 2026-10-14; GitHub repo is public
- [ ] `GAP-402-DOCKERIGNORE` — `.dockerignore` omits `.pytest_cache` / `.cursor` (Low)
- [ ] `GAP-COMM-KPI` — standing communication caveat: incremental KPI ≠ revenue dollars
- [ ] `GAP-501-API` — control inputs are CSV or frames; no live Search Console or CRM API
- [ ] `GAP-501-MODEL` — exogenous controls are aligned and not passed into Meridian

Do not invent gaps here. Add a row only when README, CLAUDE/AGENTS, a learning doc, metrics, or a Bugbot review already evidences it.

## Sprint 3 themes vs open gaps

Working branch: `sprint-3-exogenous-multitenant-mmt` (tip `fc8a8bb`). Brief: [`docs/sprints/sprint-3.md`](../sprints/sprint-3.md). STORY-501 writes date-level `exogenous_controls.parquet` (not passed into Meridian). STORY-502 is the client filesystem wall (`config/clients.yaml`, `--client_id`, default `pathc`). STORY-503 is the national `roi_m` prior; the spike `--calibration` gate exits 1 before sampling when it fails. Gaps that may be touched by those themes (not auto-closed):

- `GAP-201-RANK` — calibration / recovery honesty (MMT anchors could inform a later fix; not assumed)
- `GAP-COMM-KPI` — still applies to any new lift / calibration narrative

STORY-501 added [`GAP-501-API`](open-gaps.md) and [`GAP-501-MODEL`](open-gaps.md). Month-end quincena and the synthetic holiday list are decided, not gaps. Multi-tenant isolation still has no row — add one only when evidenced.
