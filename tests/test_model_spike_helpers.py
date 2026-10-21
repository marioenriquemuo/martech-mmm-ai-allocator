"""Unit tests for STORY-201 spike helpers (no Meridian MCMC)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
import xarray as xr

REPO_ROOT = Path(__file__).resolve().parents[1]
SPIKE_PATH = REPO_ROOT / "scripts" / "02_model_spike.py"


def _load_spike():
    """Import scripts/02_model_spike.py without running main (no Meridian import)."""
    name = "model_spike_helpers_under_test"
    spec = importlib.util.spec_from_file_location(name, SPIKE_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def spike():
    return _load_spike()


def test_response_curve_means_structure(spike):
    channels = ["meta", "google"]
    multipliers = [0.0, 1.0, 2.0]
    # (spend_multiplier, channel, metric=mean/ci_lo/ci_hi)
    outcome = np.zeros((3, 2, 3), dtype=float)
    outcome[:, 0, 0] = [0.0, 10.0, 18.0]  # meta mean
    outcome[:, 0, 1] = [0.0, 8.0, 14.0]
    outcome[:, 0, 2] = [0.0, 12.0, 22.0]
    outcome[:, 1, 0] = [0.0, 5.0, 9.0]  # google mean
    outcome[:, 1, 1] = [0.0, 4.0, 7.0]
    outcome[:, 1, 2] = [0.0, 6.0, 11.0]
    spend = np.array([[0.0, 0.0], [100.0, 50.0], [200.0, 100.0]])
    curves = xr.Dataset(
        data_vars={
            "incremental_outcome": (("spend_multiplier", "channel", "metric"), outcome),
            "spend": (("spend_multiplier", "channel"), spend),
        },
        coords={
            "channel": channels,
            "metric": ["mean", "ci_lo", "ci_hi"],
            "spend_multiplier": multipliers,
        },
    )
    means = spike.response_curve_means(curves)
    assert set(means) == {"meta", "google"}
    assert means["meta"]["spend_multiplier"] == multipliers
    assert means["meta"]["mean"] == [0.0, 10.0, 18.0]
    assert means["meta"]["ci_lo"] == [0.0, 8.0, 14.0]
    assert means["meta"]["ci_hi"] == [0.0, 12.0, 22.0]
    assert means["meta"]["spend"] == [0.0, 100.0, 200.0]
    assert means["google"]["mean"] == [0.0, 5.0, 9.0]


def test_response_curve_means_empty_without_outcome(spike):
    assert spike.response_curve_means(None) == {}
    empty = xr.Dataset(data_vars={"spend": (("x",), [1.0])})
    assert spike.response_curve_means(empty) == {}


def test_recovery_rank_stats_directional_false(spike):
    # Opposite ranks → negative Spearman → not directional recovery.
    iroas = {"meta": 1.0, "google": 0.8, "tiktok": 0.6, "tv": 0.4}
    contrib = {"tv": 4.0, "google": 3.0, "meta": 2.0, "tiktok": 1.0}
    stats = spike.recovery_rank_stats(iroas, contrib)
    assert stats["recovery_spearman"] is not None
    assert stats["recovery_spearman"] < 0
    assert stats["directional_recovery"] is False


def test_recovery_rank_stats_directional_true(spike):
    iroas = {"tv": 1.0, "google": 0.8, "meta": 0.6, "tiktok": 0.4}
    contrib = {"tv": 4.0, "google": 3.0, "meta": 2.0, "tiktok": 1.0}
    stats = spike.recovery_rank_stats(iroas, contrib)
    assert stats["recovery_spearman"] == pytest.approx(1.0)
    assert stats["directional_recovery"] is True


class _Mmm:
    """Stand-in for Meridian. Records the posterior call; does not run MCMC."""

    def __init__(self) -> None:
        self.posterior_calls = 0

    def sample_prior(self, *_args, **_kwargs) -> None:
        return None

    def sample_posterior(self, *_args, **_kwargs) -> None:
        self.posterior_calls += 1


class _Input:
    def __init__(self) -> None:
        self.media = type("Media", (), {})()
        self.media.coords = {"media_channel": type("Coord", (), {"values": ["meta"]})()}
        self.kpi = np.zeros((1, 4))


def _arm_smoke(spike, monkeypatch, tmp_path: Path, *, rhat_pass: bool) -> tuple[Path, _Mmm]:
    """Point smoke at tmp curves and stub Meridian so main() never samples."""
    processed = tmp_path / "processed"
    models = tmp_path / "models"
    raw = tmp_path / "raw"
    processed.mkdir()
    models.mkdir()
    raw.mkdir()
    (processed / "clean_spend.parquet").write_bytes(b"unused")
    client = {
        "client_id": "pathc",
        "roots": {"processed": processed, "models": models, "raw": raw},
    }
    mmm = _Mmm()
    monkeypatch.setattr(spike, "load_client", lambda *_args, **_kwargs: client)
    monkeypatch.setattr(spike, "load_meridian_input", lambda *_args, **_kwargs: _Input())
    monkeypatch.setattr(spike, "_build_mmm", lambda *_args, **_kwargs: mmm)
    monkeypatch.setattr(
        spike,
        "_rhat_peek",
        lambda *_args, **_kwargs: {
            "rhat_pass": rhat_pass,
            "max_rhat_core": 1.01 if rhat_pass else 2.39,
        },
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["02_model_spike.py", "--mode", "smoke", "--client_id", "pathc"],
    )
    return models / "metrics.json", mmm


def test_smoke_does_not_overwrite_metrics(spike, tmp_path, monkeypatch, capsys):
    metrics, mmm = _arm_smoke(spike, monkeypatch, tmp_path, rhat_pass=False)
    original = '{"keep": true}\n'
    metrics.write_text(original, encoding="utf-8")

    assert spike.main() == 0

    assert metrics.read_text(encoding="utf-8") == original
    assert mmm.posterior_calls == 1
    out = capsys.readouterr().out
    expected = spike.smoke_curves_notice(metrics.resolve())
    assert expected == f"existing metrics: {metrics.resolve()}\ncurves were not replaced"
    assert expected in out
    assert "no curve file yet" not in out


def test_smoke_says_when_curve_file_is_missing(spike, tmp_path, monkeypatch, capsys):
    metrics, mmm = _arm_smoke(spike, monkeypatch, tmp_path, rhat_pass=True)

    assert spike.main() == 0

    assert not metrics.exists()
    assert mmm.posterior_calls == 1
    out = capsys.readouterr().out
    expected = spike.smoke_curves_notice(metrics.resolve())
    assert expected == f"no curve file yet: {metrics.resolve()}\ncurves were not replaced"
    assert expected in out
    assert "existing metrics:" not in out
