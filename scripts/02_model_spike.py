#!/usr/bin/env python3
"""STORY-201 Meridian national MMM spike (smoke + fuller MCMC).

Examples::

    conda activate mmt-mmm
    python -m src.data.etl && python -m src.data.qa
    python scripts/02_model_spike.py --mode smoke
    python scripts/02_model_spike.py --mode smoke --fail-on-rhat
    python scripts/02_model_spike.py --mode smoke --calibration data/raw/calibration/geo_experiment.json
    python scripts/02_model_spike.py --mode full

Fuller mode writes the posterior predictive plot and the parameter-recovery
note under that client's ``models/``. It writes ``metrics.json`` only when
max core R-hat is under 1.05. A miss exits 1 and leaves that curve file
untouched. Smoke mode prints ``SMOKE_RHAT_WARN`` when R-hat is high but
still exits 0 unless ``--fail-on-rhat``. Parameter-recovery Spearman is
recorded in metrics / DoD flags only — never a hard fail for this spike.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data.tenants import load_client, resolve_client_path  # noqa: E402
from src.models.meridian_data import load_meridian_input  # noqa: E402

GROUND_TRUTH = REPO_ROOT / "data" / "raw" / "ground_truth.json"


def _jsonable(obj):
    """Recursively convert numpy / JAX leftovers for strict JSON."""
    if obj is None or isinstance(obj, (str, bool)):
        return obj
    if isinstance(obj, float):
        if np.isnan(obj) or np.isinf(obj):
            return None
        return obj
    if isinstance(obj, int) and not isinstance(obj, bool):
        return obj
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return _jsonable(obj.tolist())
    if isinstance(obj, np.generic):
        return _jsonable(obj.item())
    if obj is pd.NA:
        return None
    tolist = getattr(obj, "tolist", None)
    if callable(tolist) and not isinstance(obj, (str, bytes)):
        try:
            return _jsonable(tolist())
        except Exception:
            pass
    item = getattr(obj, "item", None)
    if callable(item):
        try:
            return _jsonable(item())
        except Exception:
            pass
    return str(obj)


# Smallest configs that still exercise Meridian MCMC on CPU.
SMOKE = dict(n_chains=2, n_adapt=50, n_burnin=20, n_keep=20, n_prior=50)
# Lean fuller: aim R-hat < 1.05 without multi-hour runtime on laptop CPU.
FULL = dict(n_chains=4, n_adapt=500, n_burnin=200, n_keep=400, n_prior=200)

CORE_RHAT_PREFIXES = (
    "media_channel",
    "roi_m",
    "alpha_m",
    "ec_m",
    "slope_m",
    "beta_m",
    "beta_gm",
    "mu_t",
    "knot",
    "tau_g",
    "gamma",
    "sigma",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--mode",
        choices=("smoke", "full"),
        default="smoke",
        help="smoke = short chains; full = DoD MCMC + artifacts",
    )
    p.add_argument("--client_id", default="pathc")
    p.add_argument(
        "--calibration",
        type=Path,
        default=None,
        help="Geo-experiment JSON. Omit to keep PriorDistribution()",
    )
    p.add_argument(
        "--parquet",
        type=Path,
        default=None,
        help="Processed panel. Default: this client's clean_spend.parquet",
    )
    p.add_argument(
        "--freq",
        choices=("W", "D"),
        default="W",
        help="time grain for Meridian InputData (default weekly)",
    )
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--rhat-threshold",
        type=float,
        default=1.05,
        help="full mode fails if max core R-hat ≥ this (default 1.05)",
    )
    p.add_argument(
        "--fail-on-rhat",
        action="store_true",
        help="smoke mode: exit 1 when max core R-hat ≥ threshold "
        "(default: warn only, exit 0)",
    )
    p.add_argument("--n-chains", type=int, default=None)
    p.add_argument("--n-adapt", type=int, default=None)
    p.add_argument("--n-burnin", type=int, default=None)
    p.add_argument("--n-keep", type=int, default=None)
    return p.parse_args()


def _mcmc_cfg(args: argparse.Namespace) -> dict:
    base = dict(SMOKE if args.mode == "smoke" else FULL)
    for key, attr in (
        ("n_chains", "n_chains"),
        ("n_adapt", "n_adapt"),
        ("n_burnin", "n_burnin"),
        ("n_keep", "n_keep"),
    ):
        val = getattr(args, attr)
        if val is not None:
            base[key] = val
    return base


def _analyzer(mmm):
    from meridian.analysis import analyzer

    return analyzer.Analyzer(mmm)


def _build_mmm(input_data, *, max_lag: int = 8, spec_override=None):
    from meridian.model import model, prior_distribution, spec

    if spec_override is None:
        spec_override = spec.ModelSpec(
            prior=prior_distribution.PriorDistribution(),
            media_effects_dist="log_normal",
            hill_before_adstock=False,
            max_lag=max_lag,
            unique_sigma_for_each_geo=False,
            media_prior_type="roi",
            adstock_decay_spec="geometric",
            enable_aks=False,
        )
    return model.Meridian(input_data=input_data, model_spec=spec_override)


def _core_rhat_rows(rhat_df: pd.DataFrame) -> pd.DataFrame:
    if rhat_df is None or rhat_df.empty:
        return pd.DataFrame()
    name_col = "parameter" if "parameter" in rhat_df.columns else rhat_df.columns[0]
    mask = rhat_df[name_col].astype(str).apply(
        lambda n: any(n.startswith(p) or p in n for p in CORE_RHAT_PREFIXES)
    )
    return rhat_df.loc[mask].copy()


def _rhat_peek(mmm, threshold: float) -> dict:
    an = _analyzer(mmm)
    summary = an.rhat_summary(bad_rhat_threshold=threshold)
    core = _core_rhat_rows(summary)
    max_col = "max_r_hat" if "max_r_hat" in summary.columns else summary.columns[-1]
    max_all = float(summary[max_col].max()) if len(summary) else float("nan")
    max_core = float(core[max_col].max()) if len(core) else max_all
    print("\n=== R-hat summary (peek) ===")
    print(summary.to_string(index=False))
    print(f"max R-hat (all)={max_all:.4f}  max R-hat (core)={max_core:.4f}")
    return {
        "rhat_summary": _jsonable(summary.to_dict(orient="records")),
        "max_rhat_all": max_all,
        "max_rhat_core": max_core,
        "rhat_pass": bool(max_core < threshold),
        "rhat_threshold": threshold,
    }


def _roi_by_channel(mmm) -> dict[str, float]:
    an = _analyzer(mmm)
    channels = list(mmm.input_data.media.coords["media_channel"].values)
    # use_kpi=True → incremental units / spend (iROAS-like for non_revenue KPI)
    roi = np.asarray(an.roi(use_posterior=True, use_kpi=True))
    # Expected shape: (n_chains, n_draws, n_channels) or similar — take mean.
    while roi.ndim > 1:
        roi = roi.mean(axis=0)
    return {ch: float(v) for ch, v in zip(channels, roi)}


def response_curve_means(curves) -> dict:
    """Per-channel mean / ci_lo / ci_hi vs spend_multiplier (plot-ready).

    Expects Meridian ``Analyzer.response_curves`` xarray Dataset with
    ``incremental_outcome`` dims (spend_multiplier, channel, metric).
    """
    means: dict = {}
    if curves is None or "incremental_outcome" not in getattr(curves, "data_vars", {}):
        return means

    outcome = curves["incremental_outcome"]
    channels = [str(c) for c in curves.coords["channel"].values]
    multipliers = [float(x) for x in curves.coords["spend_multiplier"].values]
    spend = curves["spend"] if "spend" in curves.data_vars else None

    for ch in channels:
        ch_out = outcome.sel(channel=ch)
        entry = {
            "spend_multiplier": multipliers,
            "mean": [float(x) for x in np.asarray(ch_out.sel(metric="mean")).reshape(-1)],
            "ci_lo": [float(x) for x in np.asarray(ch_out.sel(metric="ci_lo")).reshape(-1)],
            "ci_hi": [float(x) for x in np.asarray(ch_out.sel(metric="ci_hi")).reshape(-1)],
        }
        if spend is not None:
            entry["spend"] = [
                float(x) for x in np.asarray(spend.sel(channel=ch)).reshape(-1)
            ]
        means[ch] = entry
    return means


def _response_curve_summary(mmm) -> dict:
    an = _analyzer(mmm)
    curves = an.response_curves(use_posterior=True, use_kpi=True)
    out: dict = {"coords": {}, "means": response_curve_means(curves)}
    for name, coord in curves.coords.items():
        out["coords"][name] = [str(x) for x in coord.values]
    # Store mean incremental outcome across posterior for each spend multiplier.
    data_vars = {}
    for var in curves.data_vars:
        arr = np.asarray(curves[var])
        data_vars[var] = {
            "shape": list(arr.shape),
            "mean": float(np.nanmean(arr)),
            "std": float(np.nanstd(arr)),
        }
    out["data_vars"] = data_vars
    return out


def _posterior_summaries(mmm) -> dict:
    an = _analyzer(mmm)
    try:
        sm = an.summary_metrics(use_kpi=True, aggregate_geos=True, aggregate_times=True)
        summary = {}
        for var in sm.data_vars:
            arr = np.asarray(sm[var])
            summary[var] = {
                "mean": float(np.nanmean(arr)),
                "std": float(np.nanstd(arr)),
                "shape": list(arr.shape),
            }
        return summary
    except Exception as exc:  # pragma: no cover - defensive for Meridian API drift
        return {"error": str(exc)}


def _write_ppc(mmm, path: Path) -> None:
    an = _analyzer(mmm)
    eva = an.expected_vs_actual_data(
        aggregate_geos=True, aggregate_times=False, use_kpi=True
    )
    actual = np.asarray(eva["actual"]).reshape(-1)
    # Meridian returns expected as (time, metric) with mean / ci_lo / ci_hi.
    exp = eva["expected"]
    if "metric" in getattr(exp, "dims", ()):
        expected = np.asarray(exp.sel(metric="mean")).reshape(-1)
        ci_lo = np.asarray(exp.sel(metric="ci_lo")).reshape(-1)
        ci_hi = np.asarray(exp.sel(metric="ci_hi")).reshape(-1)
    else:
        expected = np.asarray(exp).reshape(-1)
        ci_lo = ci_hi = None

    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(actual))
    ax.plot(x, actual, label="actual KPI", color="#333333", linewidth=1.2)
    ax.plot(x, expected, label="posterior expected (mean)", color="#1f77b4", linewidth=1.2)
    if ci_lo is not None and ci_hi is not None:
        ax.fill_between(x, ci_lo, ci_hi, color="#1f77b4", alpha=0.2, label="90% CI")
    ax.set_title("Meridian posterior predictive (national, weekly)")
    ax.set_xlabel("time index")
    ax.set_ylabel("KPI (units)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print(f"wrote {path}")


def recovery_rank_stats(
    iroas: dict[str, float],
    contrib: dict[str, float],
) -> dict:
    """Spearman of iROAS rank vs contribution rank; directional if Spearman > 0.

    Not a hard DoD gate for STORY-201 — status only.
    """
    est_rank = sorted(iroas, key=iroas.get, reverse=True)
    truth_rank = sorted(contrib, key=contrib.get, reverse=True) if contrib else []
    spearman = None
    common = [c for c in truth_rank if c in est_rank]
    if len(common) >= 2:
        t_ranks = {c: i for i, c in enumerate(truth_rank)}
        e_ranks = {c: i for i, c in enumerate(est_rank)}
        n = len(common)
        d2 = sum((t_ranks[c] - e_ranks[c]) ** 2 for c in common)
        spearman = round(1 - 6 * d2 / (n * (n * n - 1)), 6)
    directional = bool(spearman is not None and spearman > 0)
    return {
        "est_rank": est_rank,
        "truth_rank": truth_rank,
        "recovery_spearman": spearman,
        "directional_recovery": directional,
    }


def _parameter_recovery(
    iroas: dict[str, float],
    ground_truth: Path = GROUND_TRUTH,
) -> tuple[str, dict]:
    truth = json.loads(ground_truth.read_text()) if ground_truth.is_file() else {}
    contrib = truth.get("sales_meta", {}).get("channel_contribution_means", {})
    beta = truth.get("media_beta", {})
    decay = truth.get("adstock_decay", {})
    stats = recovery_rank_stats(iroas, contrib)

    lines = [
        "# Parameter recovery note (STORY-201)",
        "",
        "Directional check only — Meridian ROI / Hill parameterization ≠ Path-C",
        "`media_beta` × geometric adstock × Hill saturation. Compare ranks, not",
        "point estimates.",
        "",
        "**Not a hard fail for this spike.** `dod.directional_recovery` /",
        "`recovery_spearman` in `metrics.json` record status only; a mismatch",
        "does not exit non-zero.",
        "",
        "## Estimated iROAS (posterior mean, units per $)",
        "",
    ]
    for ch, v in sorted(iroas.items(), key=lambda kv: -kv[1]):
        lines.append(f"- `{ch}`: {v:.4f}")
    lines.extend(["", "## Path-C planted signals", ""])
    if contrib:
        lines.append("Channel contribution means (units):")
        for ch, v in sorted(contrib.items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{ch}`: {v:.2f}")
    if beta:
        lines.append("")
        lines.append("media_beta (DGP scale):")
        for ch, v in sorted(beta.items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{ch}`: {v}")
    if decay:
        lines.append("")
        lines.append("adstock_decay (higher = longer memory):")
        for ch, v in sorted(decay.items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{ch}`: {v}")

    lines.extend(
        [
            "",
            "## Rank comparison",
            "",
            f"- Meridian iROAS rank: {stats['est_rank']}",
            f"- Path-C contribution rank: {stats['truth_rank']}",
        ]
    )
    spearman = stats["recovery_spearman"]
    if spearman is not None:
        lines.append(
            f"- Spearman rank correlation (iROAS vs contribution): {spearman:.3f}"
        )
        if stats["directional_recovery"]:
            lines.append(
                "- Verdict: **directional match** (positive rank correlation)."
            )
        else:
            lines.append(
                "- Verdict: **directional mismatch** — investigate media scaling / "
                "priors. (Status only; spike script does not hard-fail.)"
            )
    lines.append("")
    return "\n".join(lines), stats


# --- Curve file gate (STORY-505) ---


def publish_full_metrics(
    metrics_path: Path,
    metrics: dict,
    *,
    rhat_pass: bool,
    max_rhat_core: float,
    threshold: float,
) -> int:
    """Write ``metrics.json`` only when core R-hat passes.

    The allocator and the dashboard treat this file as the current curves
    and do not read ``dod.rhat_lt_1_05``. A failed full fit leaves an
    existing file byte-for-byte and does not create a missing one.
    Returns 0 after a write, or 1 when the curve file was not replaced.
    """
    if not rhat_pass:
        print(f"curve file not replaced: {metrics_path}", file=sys.stderr)
        print(
            f"FAIL: max core R-hat {max_rhat_core:.4f} "
            f">= {threshold}",
            file=sys.stderr,
        )
        return 1
    metrics_path.write_text(json.dumps(_jsonable(metrics), indent=2) + "\n")
    print(f"wrote {metrics_path}")
    print("full DoD: R-hat PASS (recovery status recorded; not a hard fail)")
    return 0


def main() -> int:
    args = _parse_args()
    client = load_client(args.client_id)
    parquet = resolve_client_path(
        args.client_id,
        args.parquet or client["roots"]["processed"] / "clean_spend.parquet",
    )
    models = client["roots"]["models"]
    metrics_path = resolve_client_path(args.client_id, models / "metrics.json")
    ppc_path = resolve_client_path(args.client_id, models / "posterior_predictive.png")
    recovery_path = resolve_client_path(args.client_id, models / "parameter_recovery.md")
    ground_truth = resolve_client_path(
        args.client_id,
        client["roots"]["raw"] / "ground_truth.json",
    )
    calibration_path = None
    if args.calibration is not None:
        calibration_path = resolve_client_path(args.client_id, args.calibration)
        if not calibration_path.is_file():
            print(f"missing {calibration_path}", file=sys.stderr)
            return 2
    args.parquet = parquet
    cfg = _mcmc_cfg(args)
    print(f"mode={args.mode} freq={args.freq} parquet={args.parquet}")
    print(f"mcmc={cfg}")

    if not args.parquet.is_file():
        print(
            f"missing {args.parquet}; run: python -m src.data.etl && python -m src.data.qa",
            file=sys.stderr,
        )
        return 2

    input_data = load_meridian_input(args.parquet, freq=args.freq)
    channels = [str(c) for c in input_data.media.coords["media_channel"].values]
    print(f"InputData: times={input_data.kpi.shape[1]} channels={channels}")

    max_lag = 8 if args.freq == "W" else 28
    spec_override = None
    if calibration_path is not None:
        from src.models.calibration import (
            build_report,
            gate_reasons,
            load_experiments,
            model_spec,
        )

        rows = load_experiments(calibration_path)
        report, ok = build_report(client, rows)
        if not ok:
            for reason in gate_reasons(report):
                print(reason, file=sys.stderr)
            return 1
        spec_override = model_spec(
            channels,
            rows,
            max_lag=max_lag,
            region=report["region"],
        )
    mmm = _build_mmm(input_data, max_lag=max_lag, spec_override=spec_override)
    mmm.sample_prior(cfg["n_prior"], seed=args.seed)
    print("sampling posterior…")
    mmm.sample_posterior(
        n_chains=cfg["n_chains"],
        n_adapt=cfg["n_adapt"],
        n_burnin=cfg["n_burnin"],
        n_keep=cfg["n_keep"],
        seed=args.seed,
    )

    rhat_info = _rhat_peek(mmm, args.rhat_threshold)

    if args.mode == "smoke":
        if not rhat_info["rhat_pass"]:
            extra = "" if args.fail_on_rhat else "; pass --fail-on-rhat to exit 1"
            print(
                f"SMOKE_RHAT_WARN: max core R-hat {rhat_info['max_rhat_core']:.4f} "
                f">= {args.rhat_threshold} "
                f"(smoke chains are short; use --mode full for DoD gate{extra})",
                file=sys.stderr,
            )
            if args.fail_on_rhat:
                return 1
        else:
            print("smoke OK — R-hat peek printed above")
        return 0

    # --- Fuller DoD artifacts ---
    models.mkdir(parents=True, exist_ok=True)

    iroas = _roi_by_channel(mmm)
    print("iROAS (posterior mean):", iroas)
    response = _response_curve_summary(mmm)
    post_sum = _posterior_summaries(mmm)
    _write_ppc(mmm, ppc_path)

    recovery_md, recovery_stats = _parameter_recovery(iroas, ground_truth)
    recovery_path.write_text(recovery_md)
    print(f"wrote {recovery_path}")

    metrics = {
        "story": "STORY-201",
        "mode": args.mode,
        "freq": args.freq,
        "mcmc": cfg,
        "seed": args.seed,
        "n_times": int(input_data.kpi.shape[1]),
        "channels": [str(c) for c in input_data.media.coords["media_channel"].values],
        "rhat": rhat_info,
        "iroas_units_per_dollar": iroas,
        "recovery_spearman": recovery_stats["recovery_spearman"],
        "posterior_summaries": post_sum,
        "response_curves": response,
        "artifacts": {
            "metrics": str(metrics_path.relative_to(REPO_ROOT)),
            "posterior_predictive": str(ppc_path.relative_to(REPO_ROOT)),
            "parameter_recovery": str(recovery_path.relative_to(REPO_ROOT)),
        },
        "dod": {
            "rhat_lt_1_05": rhat_info["rhat_pass"],
            "metrics_json": True,
            "ppc_png": ppc_path.is_file(),
            "parameter_recovery": recovery_path.is_file(),
            # Status only — mismatch must not be read as a silent green recovery.
            "directional_recovery": recovery_stats["directional_recovery"],
        },
    }
    # metrics.json is the current curves. Write it only when R-hat passes.
    return publish_full_metrics(
        metrics_path,
        metrics,
        rhat_pass=bool(rhat_info["rhat_pass"]),
        max_rhat_core=float(rhat_info["max_rhat_core"]),
        threshold=float(args.rhat_threshold),
    )


if __name__ == "__main__":
    raise SystemExit(main())
