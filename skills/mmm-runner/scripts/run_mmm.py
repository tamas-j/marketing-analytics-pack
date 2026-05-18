#!/usr/bin/env python3
"""Google Meridian MMM runner for marketing-analytics-pack.

Reads weekly (or daily) marketing data from a CSV — KPI plus one or more paid
media channels with spend — fits a Bayesian MMM with Meridian, then writes a
folder of artefacts that match the plugin's visual style:

    roi_per_channel.csv       Channel ROI: mean, P5, P95
    channel_contribution.csv  Posterior contribution % per channel
    response_curves.csv       Long-format spend multiplier → incremental outcome
    roi_per_channel.png       Horizontal bar chart of ROI with credible intervals
    response_curves.png       Multi-line saturation curves per channel
    summary.md                Short human-readable narrative

Chart styling is loaded from `lib/visualize.py` so the output matches every
other chart the pack produces.

Run from the repo root, with the deps installed first (see
`skills/mmm-runner/scripts/requirements.txt`), or pass `--auto-install` to
let the script pip-install them on first use. Meridian needs TensorFlow +
tfp-nightly (the first install is ~600 MB) — use a venv if your Python is
PEP 668-managed (Ubuntu 23+ / Debian 12+).

Example
-------

    python skills/mmm-runner/scripts/run_mmm.py \\
        --input examples/data/mmm-weekly.csv \\
        --time-col week_start \\
        --kpi-col revenue \\
        --kpi-type revenue \\
        --media-cols paid_search_spend,paid_social_spend \\
        --media-channels paid_search,paid_social \\
        --controls promo_active,holiday \\
        --n-chains 2 --n-adapt 200 --n-burnin 200 --n-keep 400 \\
        --output-dir examples/mmm-runner/output \\
        --style default
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS = REPO_ROOT / "skills" / "mmm-runner" / "scripts" / "requirements.txt"
LIB_DIR = REPO_ROOT / "lib"


# --------------------------------------------------------------------------- #
# Dep handling (PEP 668-aware, mirrors forecast-runner)                       #
# --------------------------------------------------------------------------- #

REQUIRED_IMPORTS = {
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "meridian": "google-meridian",
    "yaml": "pyyaml",
}


def _missing_deps() -> list[str]:
    missing: list[str] = []
    for module, package in REQUIRED_IMPORTS.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    return missing


def _in_virtualenv() -> bool:
    return getattr(sys, "base_prefix", sys.prefix) != sys.prefix


def _pip_install(args: list[str]) -> int:
    cmd = [sys.executable, "-m", "pip", "install", *args]
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.call(cmd)


def _install_deps() -> None:
    print(f"Installing mmm-runner deps from {REQUIREMENTS} ...", flush=True)
    base_args = ["-r", str(REQUIREMENTS), "--prefer-binary"]

    code = _pip_install(base_args)
    if code == 0:
        return

    if not _in_virtualenv():
        print(
            "First install attempt failed (likely PEP 668-managed Python). "
            "Retrying with --user ...",
            flush=True,
        )
        code = _pip_install([*base_args, "--user"])
        if code == 0:
            return

    print(
        "\nmmm-runner could not install its dependencies automatically.\n"
        "Meridian pulls TensorFlow + tfp-nightly (~600 MB), which usually\n"
        "fails on a system Python. Create a virtual environment and retry:\n\n"
        "    python3 -m venv .venv\n"
        "    source .venv/bin/activate      # Linux / macOS\n"
        "    .venv\\Scripts\\activate       # Windows PowerShell\n"
        f"    pip install -r {REQUIREMENTS}\n",
        file=sys.stderr,
    )
    sys.exit(2)


def _ensure_deps(auto_install: bool) -> None:
    missing = _missing_deps()
    if not missing:
        return
    if not auto_install:
        print(
            "mmm-runner is missing required packages: "
            + ", ".join(missing)
            + "\nInstall them and retry:\n"
            f"    pip install -r {REQUIREMENTS}\n"
            "Or rerun with --auto-install to install them now.\n"
            "Tip: Meridian pulls TensorFlow + tfp-nightly; use a venv "
            "(`python3 -m venv .venv && source .venv/bin/activate`).",
            file=sys.stderr,
        )
        sys.exit(2)
    _install_deps()
    missing = _missing_deps()
    if missing:
        print(
            "Auto-install completed but these packages are still missing: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        sys.exit(2)


# --------------------------------------------------------------------------- #
# Argument parsing                                                            #
# --------------------------------------------------------------------------- #


@dataclass
class RunConfig:
    input_path: Path
    time_col: str
    kpi_col: str
    kpi_type: str
    media_cols: list[str]
    media_spend_cols: list[str]
    media_channels: list[str]
    controls: list[str]
    n_chains: int
    n_adapt: int
    n_burnin: int
    n_keep: int
    seed: int
    output_dir: Path
    style_name: str
    auto_install: bool


def parse_args(argv: Iterable[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Fit a Google Meridian MMM, write ROI + response curves with styled charts.",
    )
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--time-col", required=True, help="Time column (e.g. week_start)")
    parser.add_argument("--kpi-col", required=True, help="KPI column (e.g. revenue or conversions)")
    parser.add_argument(
        "--kpi-type",
        default="revenue",
        choices=["revenue", "non_revenue"],
        help="Meridian KPI type (default revenue)",
    )
    parser.add_argument(
        "--media-cols",
        required=True,
        help="Comma-separated media exposure columns (use spend columns if no separate exposure)",
    )
    parser.add_argument(
        "--media-spend-cols",
        default=None,
        help="Comma-separated media spend columns (defaults to --media-cols)",
    )
    parser.add_argument(
        "--media-channels",
        default=None,
        help="Comma-separated channel labels (defaults to --media-cols)",
    )
    parser.add_argument(
        "--controls",
        default="",
        help="Optional comma-separated control variable columns (e.g. promo flags)",
    )
    parser.add_argument("--n-chains", type=int, default=2, help="MCMC chains (default 2)")
    parser.add_argument("--n-adapt", type=int, default=200, help="MCMC adaptation draws (default 200)")
    parser.add_argument("--n-burnin", type=int, default=200, help="MCMC burn-in draws (default 200)")
    parser.add_argument("--n-keep", type=int, default=400, help="MCMC kept draws (default 400)")
    parser.add_argument("--seed", type=int, default=1, help="Random seed")
    parser.add_argument(
        "--output-dir",
        default="mmm_output",
        help="Where to write artefacts (default ./mmm_output)",
    )
    parser.add_argument(
        "--style",
        default="default",
        help="Style name from lib/styles (default, executive, custom)",
    )
    parser.add_argument(
        "--auto-install",
        action="store_true",
        help="pip install requirements.txt if any dep is missing",
    )

    args = parser.parse_args(list(argv) if argv is not None else None)

    media_cols = [c.strip() for c in args.media_cols.split(",") if c.strip()]
    spend_cols = (
        [c.strip() for c in args.media_spend_cols.split(",") if c.strip()]
        if args.media_spend_cols
        else list(media_cols)
    )
    channels = (
        [c.strip() for c in args.media_channels.split(",") if c.strip()]
        if args.media_channels
        else list(media_cols)
    )
    controls = [c.strip() for c in args.controls.split(",") if c.strip()]

    if not (len(media_cols) == len(spend_cols) == len(channels)):
        raise SystemExit(
            f"--media-cols ({len(media_cols)}), --media-spend-cols ({len(spend_cols)}), "
            f"and --media-channels ({len(channels)}) must all have the same length"
        )

    return RunConfig(
        input_path=Path(args.input).expanduser().resolve(),
        time_col=args.time_col,
        kpi_col=args.kpi_col,
        kpi_type=args.kpi_type,
        media_cols=media_cols,
        media_spend_cols=spend_cols,
        media_channels=channels,
        controls=controls,
        n_chains=args.n_chains,
        n_adapt=args.n_adapt,
        n_burnin=args.n_burnin,
        n_keep=args.n_keep,
        seed=args.seed,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        style_name=args.style,
        auto_install=args.auto_install,
    )


# --------------------------------------------------------------------------- #
# Data loading                                                                #
# --------------------------------------------------------------------------- #


def load_dataframe(config: RunConfig):
    import pandas as pd

    df = pd.read_csv(config.input_path)
    required = [config.time_col, config.kpi_col, *config.media_cols, *config.media_spend_cols, *config.controls]
    for col in required:
        if col not in df.columns:
            raise SystemExit(f"Column {col!r} not found in {config.input_path}")

    df = df.copy()
    df[config.time_col] = pd.to_datetime(df[config.time_col]).dt.strftime("%Y-%m-%d")
    df = df.sort_values(config.time_col).reset_index(drop=True)
    return df


def build_input_data(df, config: RunConfig):
    """Build Meridian InputData from a national (single-geo) DataFrame."""
    import pandas as pd
    from meridian.data.data_frame_input_data_builder import DataFrameInputDataBuilder

    builder = DataFrameInputDataBuilder(
        kpi_type=config.kpi_type,
        default_time_column=config.time_col,
    )
    builder = builder.with_kpi(df, kpi_col=config.kpi_col)
    builder = builder.with_media(
        df,
        media_cols=config.media_cols,
        media_spend_cols=config.media_spend_cols,
        media_channels=config.media_channels,
    )
    if config.controls:
        builder = builder.with_controls(df, control_cols=config.controls)

    # National model still needs a population entry — Meridian creates the
    # single 'national_geo' coordinate when no geo column is present, but it
    # expects a population value to scale the priors against.
    population_df = pd.DataFrame({"population": [1.0]})
    builder = builder.with_population(population_df, population_col="population")

    return builder.build()


# --------------------------------------------------------------------------- #
# Modeling                                                                    #
# --------------------------------------------------------------------------- #


def fit_meridian(input_data, config: RunConfig):
    from meridian.model.model import Meridian
    from meridian.model.spec import ModelSpec

    spec = ModelSpec()
    m = Meridian(input_data=input_data, model_spec=spec)

    print(
        f"Sampling Meridian posterior: chains={config.n_chains} "
        f"adapt={config.n_adapt} burnin={config.n_burnin} keep={config.n_keep}",
        flush=True,
    )
    m.sample_posterior(
        n_chains=config.n_chains,
        n_adapt=config.n_adapt,
        n_burnin=config.n_burnin,
        n_keep=config.n_keep,
        seed=config.seed,
    )
    return m


# --------------------------------------------------------------------------- #
# Analysis                                                                    #
# --------------------------------------------------------------------------- #


def summarize_roi(model, channels: list[str]):
    """Return a DataFrame with mean / p5 / p95 ROI per channel."""
    import numpy as np
    import pandas as pd
    from meridian.analysis.analyzer import Analyzer

    analyzer = Analyzer(model)
    roi_tensor = analyzer.roi(use_posterior=True)  # shape: (chains, draws, channels)
    arr = np.asarray(roi_tensor).reshape(-1, len(channels))

    summary = pd.DataFrame({
        "channel": channels,
        "roi_mean": arr.mean(axis=0),
        "roi_p5": np.percentile(arr, 5, axis=0),
        "roi_p95": np.percentile(arr, 95, axis=0),
    })
    return summary, arr


def summarize_response_curves(model, channels: list[str]):
    """Return a tidy DataFrame of incremental outcome at varying spend multipliers."""
    import numpy as np
    import pandas as pd
    from meridian.analysis.analyzer import Analyzer

    analyzer = Analyzer(model)
    multipliers = [round(m, 2) for m in np.linspace(0.0, 2.0, 11)]
    rc = analyzer.response_curves(spend_multipliers=multipliers, by_reach=False)
    df = rc.to_dataframe().reset_index()

    keep_cols = [c for c in ["channel", "spend_multiplier", "spend", "incremental_outcome"] if c in df.columns]
    if keep_cols:
        df = df[keep_cols]
    return df


# --------------------------------------------------------------------------- #
# Plotting                                                                    #
# --------------------------------------------------------------------------- #


def _load_style(name: str):
    if str(LIB_DIR) not in sys.path:
        sys.path.insert(0, str(LIB_DIR))
    from visualize import load_style, palette, chart_tokens, typography, layout, matplotlib_rc_params

    style = load_style(name)
    return {
        "style": style,
        "palette": palette(style),
        "chart": chart_tokens(style),
        "typography": typography(style),
        "layout": layout(style),
        "rc": matplotlib_rc_params(style),
    }


def plot_roi(summary_df, output_path: Path, tokens) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(tokens["rc"])
    fig, ax = plt.subplots(
        figsize=(tokens["layout"].get("figure_width", 9), tokens["layout"].get("figure_height", 5)),
        dpi=tokens["layout"].get("dpi", 160),
    )
    ax.grid(axis="x", linewidth=0.8, alpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    colors = tokens["palette"]
    chart = tokens["chart"]
    type_tokens = tokens["typography"]
    layout_tokens = tokens["layout"]

    positions = list(range(len(summary_df)))
    ax.barh(positions, summary_df["roi_mean"], color=colors[: len(summary_df)])
    err_lower = (summary_df["roi_mean"] - summary_df["roi_p5"]).clip(lower=0)
    err_upper = (summary_df["roi_p95"] - summary_df["roi_mean"]).clip(lower=0)
    ax.errorbar(
        summary_df["roi_mean"],
        positions,
        xerr=[err_lower, err_upper],
        fmt="none",
        ecolor=chart.get("muted", "#6b7280"),
        elinewidth=1.2,
        capsize=4,
    )
    ax.set_yticks(positions)
    ax.set_yticklabels(summary_df["channel"])
    ax.invert_yaxis()
    ax.set_title("ROI per channel (posterior mean with 5–95% interval)",
                 pad=layout_tokens.get("title_pad", 14), loc="left")
    ax.set_xlabel("ROI")
    for i, value in enumerate(summary_df["roi_mean"]):
        ax.text(value, i, f" {value:.2f}", va="center",
                fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))

    source_note = layout_tokens.get("source_note", "")
    if source_note:
        fig.text(0.01, 0.01, source_note,
                 fontsize=type_tokens.get("note_size", 8),
                 color=chart.get("muted", "#6b7280"))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_response_curves(curves_df, output_path: Path, tokens) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(tokens["rc"])
    fig, ax = plt.subplots(
        figsize=(tokens["layout"].get("figure_width", 9), tokens["layout"].get("figure_height", 5)),
        dpi=tokens["layout"].get("dpi", 160),
    )
    ax.grid(axis="y", linewidth=0.8, alpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    colors = tokens["palette"]
    chart = tokens["chart"]
    type_tokens = tokens["typography"]
    layout_tokens = tokens["layout"]

    x_col = "spend" if "spend" in curves_df.columns else "spend_multiplier"
    for idx, (channel, sub) in enumerate(curves_df.groupby("channel")):
        ax.plot(sub[x_col], sub["incremental_outcome"],
                color=colors[idx % len(colors)],
                linewidth=2.0, marker="o", markersize=4, label=channel)

    ax.set_title("Response curves — incremental outcome vs. spend",
                 pad=layout_tokens.get("title_pad", 14), loc="left")
    ax.set_xlabel("Spend" if x_col == "spend" else "Spend multiplier")
    ax.set_ylabel("Incremental outcome")
    ax.legend(frameon=False, loc="lower right")

    source_note = layout_tokens.get("source_note", "")
    if source_note:
        fig.text(0.01, 0.01, source_note,
                 fontsize=type_tokens.get("note_size", 8),
                 color=chart.get("muted", "#6b7280"))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Summary                                                                     #
# --------------------------------------------------------------------------- #


def write_summary(output_path: Path, config: RunConfig, history_rows: int, roi_df) -> None:
    lines: list[str] = []
    lines.append("# MMM summary")
    lines.append("")
    lines.append(f"- Input: `{config.input_path}`")
    lines.append(f"- KPI: `{config.kpi_col}` ({config.kpi_type}, {history_rows} historical periods)")
    lines.append(f"- Time column: `{config.time_col}`")
    lines.append(f"- Media channels: {', '.join(f'`{c}`' for c in config.media_channels)}")
    lines.append(f"- Controls: {', '.join(f'`{c}`' for c in config.controls) if config.controls else 'none'}")
    lines.append(
        f"- MCMC: chains={config.n_chains}, adapt={config.n_adapt}, "
        f"burnin={config.n_burnin}, keep={config.n_keep}"
    )
    lines.append("")
    lines.append("## ROI per channel")
    lines.append("")
    lines.append("| Channel | ROI (mean) | P5 | P95 |")
    lines.append("|---|---:|---:|---:|")
    for _, row in roi_df.iterrows():
        lines.append(
            f"| {row['channel']} | {row['roi_mean']:.2f} | {row['roi_p5']:.2f} | {row['roi_p95']:.2f} |"
        )
    lines.append("")
    best = roi_df.loc[roi_df["roi_mean"].idxmax()]
    lines.append(f"Highest mean ROI: **{best['channel']}** ({best['roi_mean']:.2f}).")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("- `roi_per_channel.csv` — mean / P5 / P95 ROI per channel")
    lines.append("- `channel_contribution.csv` — posterior contribution % per channel")
    lines.append("- `response_curves.csv` — long-format spend multiplier → incremental outcome")
    lines.append("- `roi_per_channel.png` — horizontal bar chart with credible intervals")
    lines.append("- `response_curves.png` — saturation curves per channel")
    lines.append("")
    lines.append("## Caveats")
    lines.append("")
    lines.append("- MMM is correlational, not causal — calibrate against geo or holdout incrementality tests where possible.")
    lines.append("- Small sample sizes and short MCMC settings produce wider intervals; use `--n-keep 1000+` for production runs.")
    lines.append("- Response curves assume the historical media mix and saturation shape generalize to the spend range plotted.")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #


def summarize_contribution(model, channels: list[str]):
    """Return a DataFrame with mean / p5 / p95 % contribution per channel."""
    import numpy as np
    import pandas as pd
    from meridian.analysis.analyzer import Analyzer

    analyzer = Analyzer(model)
    incremental = np.asarray(analyzer.incremental_outcome(use_posterior=True))
    # shape: (chains, draws, channels) — sum across channels for total, then divide.
    total = incremental.sum(axis=-1, keepdims=True)
    pct = np.where(total > 0, incremental / total, 0.0)
    arr = pct.reshape(-1, len(channels))

    return pd.DataFrame({
        "channel": channels,
        "contribution_mean_pct": arr.mean(axis=0) * 100,
        "contribution_p5_pct": np.percentile(arr, 5, axis=0) * 100,
        "contribution_p95_pct": np.percentile(arr, 95, axis=0) * 100,
    })


def run(config: RunConfig) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {config.input_path} ...", flush=True)
    df = load_dataframe(config)
    print(f"  {len(df)} rows, "
          f"channels={config.media_channels}, controls={config.controls or 'none'}",
          flush=True)

    print("Building Meridian InputData ...", flush=True)
    input_data = build_input_data(df, config)

    tokens = _load_style(config.style_name)
    model = fit_meridian(input_data, config)

    print("Computing ROI ...", flush=True)
    roi_df, _ = summarize_roi(model, config.media_channels)
    roi_path = config.output_dir / "roi_per_channel.csv"
    roi_df.to_csv(roi_path, index=False)
    print(f"Wrote {roi_path}", flush=True)

    print("Computing contribution shares ...", flush=True)
    contrib_df = summarize_contribution(model, config.media_channels)
    contrib_path = config.output_dir / "channel_contribution.csv"
    contrib_df.to_csv(contrib_path, index=False)
    print(f"Wrote {contrib_path}", flush=True)

    print("Computing response curves ...", flush=True)
    curves_df = summarize_response_curves(model, config.media_channels)
    curves_path = config.output_dir / "response_curves.csv"
    curves_df.to_csv(curves_path, index=False)
    print(f"Wrote {curves_path}", flush=True)

    roi_png = config.output_dir / "roi_per_channel.png"
    plot_roi(roi_df, roi_png, tokens)
    print(f"Wrote {roi_png}", flush=True)

    curves_png = config.output_dir / "response_curves.png"
    plot_response_curves(curves_df, curves_png, tokens)
    print(f"Wrote {curves_png}", flush=True)

    summary_path = config.output_dir / "summary.md"
    write_summary(summary_path, config, len(df), roi_df)
    print(f"Wrote {summary_path}", flush=True)

    print("Done.", flush=True)


def main(argv: Iterable[str] | None = None) -> int:
    config = parse_args(argv)
    _ensure_deps(config.auto_install)
    run(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
