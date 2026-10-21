"""Pydantic schema for a future ``emit_brief`` tool (STORY-302 Step 1).

The model is the contract the narrator must fill. ``emit_brief_json_schema``
is the JSON Schema a tool definition can publish. No model client lives here.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# --- Brief the narrator emits ---


class ChannelShift(BaseModel):
    """One channel move from the equal-room baseline to the recommended spend."""

    channel: str
    baseline_spend: float
    recommended_spend: float
    spend_delta: float
    saturation_flag: Literal["near_ceiling", "at_floor", "ok"]


class CsuiteBrief(BaseModel):
    """Numbers in a brief must match the fact pack (see ``numbers_match``)."""

    headline: str = Field(min_length=1)
    bullets: list[str] = Field(min_length=3, max_length=6)
    shifts: list[ChannelShift]
    predicted_incremental_kpi: float
    incremental_kpi_delta_vs_baseline: float | None
    caveats: list[str]


class ChannelFact(BaseModel):
    recommended_spend: float
    baseline_spend: float
    spend_delta: float
    share_of_budget: float
    saturation_flag: Literal["near_ceiling", "at_floor", "ok"]


class FactPack(BaseModel):
    """Validated shape of ``build_fact_pack`` (not the narrator output)."""

    channels: dict[str, ChannelFact]
    concentration_note: str | None
    expected_incremental_kpi: float | None
    incremental_kpi_delta_vs_baseline: float | None
    mode: str | None = None


# --- Tool schema ---


def emit_brief_json_schema() -> dict:
    """JSON Schema for a future ``emit_brief`` tool."""
    return CsuiteBrief.model_json_schema()
