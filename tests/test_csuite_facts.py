"""STORY-302 Step 1 — fact pack baseline, saturation flags, brief number lock."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.report.facts import build_fact_pack, numbers_match
from src.report.schema import CsuiteBrief, FactPack, emit_brief_json_schema

REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "tests" / "fixtures" / "story_302_allocation.json"


def _load(path: Path = FIXTURE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _brief_from(pack: dict) -> CsuiteBrief:
    shifts = [
        {
            "channel": ch,
            **{k: row[k] for k in (
                "baseline_spend",
                "recommended_spend",
                "spend_delta",
                "saturation_flag",
            )},
        }
        for ch, row in pack["channels"].items()
    ]
    return CsuiteBrief(
        headline="Shift budget toward alpha",
        bullets=[
            "Alpha moves onto the ceiling.",
            "Beta and gamma give spend back.",
            "Predicted lift is the KPI difference.",
        ],
        shifts=shifts,
        predicted_incremental_kpi=pack["expected_incremental_kpi"],
        incremental_kpi_delta_vs_baseline=pack["incremental_kpi_delta_vs_baseline"],
        caveats=["Fixture curves, not Path-C ground truth."],
    )


# --- Baseline + flags ---


def test_equal_room_baseline_and_alpha_ceiling():
    allocation = _load()
    pack = build_fact_pack(allocation)
    FactPack.model_validate(pack)

    assert pack["mode"] == allocation["constraints"]["mode"]
    assert pack["expected_incremental_kpi"] == allocation["expected_incremental_kpi"]
    assert (
        pack["incremental_kpi_delta_vs_baseline"]
        == allocation["incremental_kpi_delta_vs_baseline"]
    )
    assert pack["concentration_note"] is None

    alpha, beta, gamma = (pack["channels"][ch] for ch in ("alpha", "beta", "gamma"))
    assert alpha["baseline_spend"] == pytest.approx(20.0)
    assert beta["baseline_spend"] == pytest.approx(20.0)
    assert gamma["baseline_spend"] == pytest.approx(20.0)
    assert alpha["recommended_spend"] == pytest.approx(27.0)
    assert beta["recommended_spend"] == pytest.approx(18.0)
    assert gamma["recommended_spend"] == pytest.approx(15.0)
    assert alpha["spend_delta"] == pytest.approx(7.0)
    assert beta["spend_delta"] == pytest.approx(-2.0)
    assert gamma["spend_delta"] == pytest.approx(-5.0)
    assert alpha["share_of_budget"] == pytest.approx(27.0 / 60.0)
    assert beta["share_of_budget"] == pytest.approx(18.0 / 60.0)
    assert gamma["share_of_budget"] == pytest.approx(15.0 / 60.0)
    assert alpha["saturation_flag"] == "near_ceiling"
    assert beta["saturation_flag"] == "ok"
    assert gamma["saturation_flag"] == "ok"


def test_floor_flag_and_concentration_note():
    allocation = _load()
    allocation["channels"] = {"alpha": 80.0, "beta": 15.0, "gamma": 5.0}
    allocation["total_spend"] = 100.0
    allocation["constraints"]["total_budget"] = 100.0
    allocation["constraints"]["min_spend"] = {"alpha": 5.0, "beta": 5.0, "gamma": 5.0}
    allocation["constraints"]["max_spend"] = {"alpha": 100.0, "beta": 100.0, "gamma": 100.0}
    allocation["incremental_kpi_delta_vs_baseline"] = None

    pack = build_fact_pack(allocation)
    # equal-room: mins 5+5+5, leftover 85, room 95 each → 5 + 85/3
    each = 5.0 + 85.0 / 3.0
    for row in pack["channels"].values():
        assert row["baseline_spend"] == pytest.approx(each)
    assert pack["channels"]["gamma"]["saturation_flag"] == "at_floor"
    assert pack["channels"]["alpha"]["saturation_flag"] == "ok"
    assert pack["channels"]["alpha"]["share_of_budget"] == pytest.approx(0.80)
    assert pack["concentration_note"] == "alpha holds 80% of total spend"
    assert pack["incremental_kpi_delta_vs_baseline"] is None


def test_exact_floor_tolerance_is_at_floor():
    allocation = _load()
    allocation["channels"] = {"alpha": 30.0, "beta": 25.0 - 1e-6, "gamma": 5.0 + 1e-6}
    allocation["total_spend"] = 60.0
    pack = build_fact_pack(allocation)
    assert pack["channels"]["alpha"]["saturation_flag"] == "near_ceiling"
    assert pack["channels"]["gamma"]["saturation_flag"] == "at_floor"


# --- Refuse a failed plan ---


def test_refuses_failed_solver_and_empty_channels():
    failed = _load()
    failed["solver"] = {"success": False, "message": "infeasible"}
    failed["channels"] = {}
    with pytest.raises(ValueError, match="no fact pack"):
        build_fact_pack(failed)

    empty = _load()
    empty["channels"] = {}
    empty["solver"] = {"success": True, "message": "empty"}
    with pytest.raises(ValueError, match="no fact pack"):
        build_fact_pack(empty)


# --- Brief schema + number lock ---


def test_brief_round_trip_and_drift_fails_lock():
    pack = build_fact_pack(_load())
    brief = _brief_from(pack)
    again = CsuiteBrief.model_validate(brief.model_dump())
    assert again == brief
    assert numbers_match(pack, brief)
    assert numbers_match(pack, brief.model_dump())

    schema = emit_brief_json_schema()
    assert set(schema["required"]) >= {
        "headline",
        "bullets",
        "shifts",
        "predicted_incremental_kpi",
        "incremental_kpi_delta_vs_baseline",
        "caveats",
    }

    drifted = brief.model_copy(
        update={"predicted_incremental_kpi": brief.predicted_incremental_kpi + 0.01}
    )
    assert numbers_match(pack, drifted) is False

    with pytest.raises(ValidationError):
        CsuiteBrief.model_validate({**brief.model_dump(), "bullets": ["only", "two"]})
