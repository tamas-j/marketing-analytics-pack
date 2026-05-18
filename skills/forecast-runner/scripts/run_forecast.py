#!/usr/bin/env python3
"""Prophet forecast runner for marketing-analytics-pack.

Reads a time series from CSV, fits a Prophet model with optional holidays and
extra regressors, predicts forward `--horizon` periods, compares against naive
and seasonal-naive baselines, and writes a folder of artefacts that match the
plugin's visual style:

    forecast.csv         ds, yhat, yhat_lower, yhat_upper for the horizon
    forecast.png         actuals + forecast line + confidence interval
    components.png       Prophet trend / weekly / yearly decomposition
    baselines.csv        MAPE / MAE / RMSE for Prophet vs naive baselines
                         (only when --validate is set)
    summary.md           short human-readable narrative

The chart styling is loaded from lib/visualize.py so the output looks the same
as every other chart the pack produces.

Run from the repo root, with the deps installed first (see
skills/forecast-runner/scripts/requirements.txt), or pass --auto-install to
let the script pip-install them on first use.

Example
-------

    python skills/forecast-runner/scripts/run_forecast.py \\
        --input examples/data/mmm-weekly.csv \\
        --date-col week_start \\
        --target-col revenue \\
        --freq W \\
        --horizon 13 \\
        --holidays-col holiday \\
        --regressors paid_search_spend,paid_social_spend \\
        --validate \\
        --output-dir examples/forecast-runner/output \\
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
REQUIREMENTS = REPO_ROOT / "skills" / "forecast-runner" / "scripts" / "requirements.txt"
LIB_DIR = REPO_ROOT / "lib"


# --------------------------------------------------------------------------- #
# Dep handling                                                                #
# --------------------------------------------------------------------------- #

REQUIRED_IMPORTS = {
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "prophet": "prophet",
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
    """Detect whether the current interpreter is inside a venv / virtualenv."""
    return getattr(sys, "base_prefix", sys.prefix) != sys.prefix


def _pip_install(args: list[str]) -> int:
    """Run pip install with the given extra args. Returns the exit code."""
    cmd = [sys.executable, "-m", "pip", "install", *args]
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.call(cmd)


def _install_deps() -> None:
    """Install runner deps with a PEP 668-aware strategy.

    Order of attempts:
    1. Plain `pip install -r requirements.txt` — works inside a venv or on
       systems that don't mark their Python as externally managed.
    2. `--user` — falls back to a per-user install for system Pythons that
       block global writes (Ubuntu 23+ / Debian 12+ enforce PEP 668).
    3. Bail with a clear message asking the user to create a venv.
    """
    print(f"Installing forecast-runner deps from {REQUIREMENTS} ...", flush=True)
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
        "\nforecast-runner could not install its dependencies automatically.\n"
        "This usually means the Python on your PATH is managed by the OS.\n"
        "Create a virtual environment and retry:\n\n"
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
            "forecast-runner is missing required packages: "
            + ", ".join(missing)
            + "\nInstall them and retry:\n"
            f"    pip install -r {REQUIREMENTS}\n"
            "Or rerun with --auto-install to install them now.\n"
            "Tip: on Ubuntu 23+/Debian 12+ create a venv first "
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
    date_col: str
    target_col: str
    freq: str
    horizon: int
    holidays_col: str | None
    regressors: list[str]
    validate: bool
    validation_fraction: float
    seasonality_mode: str
    output_dir: Path
    style_name: str
    auto_install: bool


PROPHET_FREQ_MAP = {
    "D": "D",
    "W": "W",
    "M": "MS",  # Prophet expects month-start
    "Q": "QS",
    "Y": "YS",
}


def parse_args(argv: Iterable[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Fit a Prophet forecast, compare to baselines, write styled charts.",
    )
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--date-col", required=True, help="Date column in the CSV")
    parser.add_argument("--target-col", required=True, help="Target value column")
    parser.add_argument(
        "--freq",
        default="W",
        choices=sorted(PROPHET_FREQ_MAP.keys()),
        help="Series frequency: D, W, M, Q, Y (default W)",
    )
    parser.add_argument(
        "--horizon", type=int, required=True, help="Number of future periods to forecast"
    )
    parser.add_argument(
        "--holidays-col",
        default=None,
        help="Optional 0/1 column flagging holidays in the input rows",
    )
    parser.add_argument(
        "--regressors",
        default="",
        help="Comma-separated extra regressor columns (future values are filled with the trailing mean)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Backtest the last --validation-fraction of the data and compare against baselines",
    )
    parser.add_argument(
        "--validation-fraction",
        type=float,
        default=0.2,
        help="Fraction of the series to hold out when --validate is set (default 0.2)",
    )
    parser.add_argument(
        "--seasonality-mode",
        default="additive",
        choices=["additive", "multiplicative"],
        help="Prophet seasonality mode (default additive)",
    )
    parser.add_argument(
        "--output-dir",
        default="forecast_output",
        help="Where to write artefacts (default ./forecast_output)",
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

    regressors = [r.strip() for r in args.regressors.split(",") if r.strip()]

    return RunConfig(
        input_path=Path(args.input).expanduser().resolve(),
        date_col=args.date_col,
        target_col=args.target_col,
        freq=args.freq,
        horizon=args.horizon,
        holidays_col=args.holidays_col,
        regressors=regressors,
        validate=args.validate,
        validation_fraction=args.validation_fraction,
        seasonality_mode=args.seasonality_mode,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        style_name=args.style,
        auto_install=args.auto_install,
    )


# --------------------------------------------------------------------------- #
# Data loading                                                                #
# --------------------------------------------------------------------------- #


def load_series(config: "RunConfig"):
    import pandas as pd

    df = pd.read_csv(config.input_path)

    for col in [config.date_col, config.target_col]:
        if col not in df.columns:
            raise SystemExit(f"Column {col!r} not found in {config.input_path}")
    for col in config.regressors:
        if col not in df.columns:
            raise SystemExit(f"Regressor column {col!r} not found in {config.input_path}")
    if config.holidays_col and config.holidays_col not in df.columns:
        raise SystemExit(
            f"Holidays column {config.holidays_col!r} not found in {config.input_path}"
        )

    df = df.copy()
    df[config.date_col] = pd.to_datetime(df[config.date_col])
    df = df.sort_values(config.date_col).reset_index(drop=True)

    keep_cols = [config.date_col, config.target_col, *config.regressors]
    if config.holidays_col:
        keep_cols.append(config.holidays_col)
    df = df[keep_cols].rename(columns={config.date_col: "ds", config.target_col: "y"})

    if df["y"].isna().any():
        raise SystemExit("Target column contains NaN — clean the input series first")
    return df


def build_holidays_frame(df, holidays_col: str | None):
    if not holidays_col:
        return None
    import pandas as pd

    flagged = df.loc[df[holidays_col].astype(int) == 1, "ds"]
    if flagged.empty:
        return None
    return pd.DataFrame({"holiday": "flagged", "ds": flagged.values, "lower_window": 0, "upper_window": 0})


# --------------------------------------------------------------------------- #
# Prophet wiring                                                              #
# --------------------------------------------------------------------------- #


def fit_prophet(train_df, config: "RunConfig", holidays_frame):
    from prophet import Prophet

    model = Prophet(
        seasonality_mode=config.seasonality_mode,
        holidays=holidays_frame,
        interval_width=0.8,
    )
    for regressor in config.regressors:
        model.add_regressor(regressor)
    fit_cols = ["ds", "y", *config.regressors]
    model.fit(train_df[fit_cols])
    return model


def build_future_frame(history_df, config: "RunConfig"):
    """Build the future frame Prophet predicts over, including regressor fills."""
    import pandas as pd

    freq = PROPHET_FREQ_MAP[config.freq]
    future_index = pd.date_range(
        start=history_df["ds"].iloc[-1],
        periods=config.horizon + 1,
        freq=freq,
    )[1:]
    future = pd.DataFrame({"ds": list(history_df["ds"]) + list(future_index)})

    for regressor in config.regressors:
        tail_mean = history_df[regressor].tail(min(len(history_df), 4)).mean()
        fill_value = tail_mean if not math.isnan(tail_mean) else 0.0
        history_values = list(history_df[regressor].values)
        future_values = [float(fill_value)] * config.horizon
        future[regressor] = history_values + future_values

    return future


# --------------------------------------------------------------------------- #
# Baselines                                                                   #
# --------------------------------------------------------------------------- #


def seasonal_period(freq: str) -> int:
    return {"D": 7, "W": 52, "M": 12, "Q": 4, "Y": 1}.get(freq, 1)


def naive_forecast(train, horizon: int):
    return [float(train["y"].iloc[-1])] * horizon


def seasonal_naive_forecast(train, horizon: int, period: int) -> list[float]:
    if len(train) < period:
        return naive_forecast(train, horizon)
    seasonal_slice = train["y"].iloc[-period:].tolist()
    return [seasonal_slice[i % period] for i in range(horizon)]


def score(actual: list[float], predicted: list[float]) -> dict[str, float]:
    n = len(actual)
    if n == 0 or len(predicted) != n:
        return {"mape": float("nan"), "mae": float("nan"), "rmse": float("nan")}
    errors = [a - p for a, p in zip(actual, predicted)]
    abs_pct = [abs(e) / a for a, e in zip(actual, errors) if a != 0]
    mape = sum(abs_pct) / len(abs_pct) if abs_pct else float("nan")
    mae = sum(abs(e) for e in errors) / n
    rmse = math.sqrt(sum(e * e for e in errors) / n)
    return {"mape": mape, "mae": mae, "rmse": rmse}


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


def plot_forecast(history, forecast, output_path: Path, tokens, title: str) -> None:
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
    chart_colors = tokens["chart"]

    ax.plot(history["ds"], history["y"], color=chart_colors.get("foreground", "#111827"),
            linewidth=1.6, label="Actuals")
    ax.plot(forecast["ds"], forecast["yhat"], color=colors[0], linewidth=2.0, label="Forecast")
    ax.fill_between(
        forecast["ds"],
        forecast["yhat_lower"],
        forecast["yhat_upper"],
        color=colors[0],
        alpha=0.18,
        label="80% interval",
    )
    ax.set_title(title, pad=tokens["layout"].get("title_pad", 14), loc="left")
    ax.legend(frameon=False, loc="upper left")

    source_note = tokens["layout"].get("source_note", "")
    if source_note:
        fig.text(0.01, 0.01, source_note,
                 fontsize=tokens["typography"].get("note_size", 8),
                 color=chart_colors.get("muted", "#6b7280"))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_components(model, forecast, output_path: Path, tokens) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(tokens["rc"])
    fig = model.plot_components(forecast)
    fig.set_dpi(tokens["layout"].get("dpi", 160))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Summary writer                                                              #
# --------------------------------------------------------------------------- #


def write_summary(
    output_path: Path,
    config: "RunConfig",
    history_rows: int,
    forecast,
    baselines: dict[str, dict[str, float]] | None,
) -> None:
    lines: list[str] = []
    lines.append("# Forecast summary")
    lines.append("")
    lines.append(f"- Input: `{config.input_path}`")
    lines.append(f"- Target: `{config.target_col}` ({history_rows} historical rows)")
    lines.append(f"- Frequency: `{config.freq}` — horizon: {config.horizon} periods")
    lines.append(f"- Holidays: `{config.holidays_col or 'none'}`")
    lines.append(
        f"- Regressors: {', '.join(f'`{r}`' for r in config.regressors) if config.regressors else 'none'}"
    )
    lines.append(f"- Seasonality mode: `{config.seasonality_mode}`")
    lines.append("")

    last = forecast.tail(1).iloc[0]
    lines.append(f"## Headline forecast")
    lines.append("")
    lines.append(
        f"Last horizon point ({last['ds'].date()}): **{last['yhat']:,.0f}** "
        f"(80% interval {last['yhat_lower']:,.0f} – {last['yhat_upper']:,.0f})"
    )
    lines.append("")

    if baselines:
        lines.append("## Backtest scores (lower is better)")
        lines.append("")
        lines.append("| Model | MAPE | MAE | RMSE |")
        lines.append("|---|---:|---:|---:|")
        for label, metrics in baselines.items():
            mape = "n/a" if math.isnan(metrics["mape"]) else f"{metrics['mape']:.1%}"
            lines.append(
                f"| {label} | {mape} | {metrics['mae']:,.1f} | {metrics['rmse']:,.1f} |"
            )
        lines.append("")
        best = min(baselines.items(), key=lambda kv: kv[1]["rmse"])
        lines.append(f"Lowest RMSE on the holdout: **{best[0]}**.")
        lines.append("")

    lines.append("## Outputs")
    lines.append("")
    lines.append("- `forecast.csv` — `ds, yhat, yhat_lower, yhat_upper` for the horizon")
    lines.append("- `forecast.png` — actuals + forecast line + 80% confidence interval")
    lines.append("- `components.png` — Prophet trend / seasonality decomposition")
    if baselines:
        lines.append("- `baselines.csv` — Prophet vs naive vs seasonal-naive scores on the holdout")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #


def run(config: RunConfig) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {config.input_path} ...", flush=True)
    df = load_series(config)
    holidays_frame = build_holidays_frame(df, config.holidays_col)
    history_rows = len(df)
    print(f"  {history_rows} rows, "
          f"{df['ds'].iloc[0].date()} → {df['ds'].iloc[-1].date()}", flush=True)

    tokens = _load_style(config.style_name)

    baselines: dict[str, dict[str, float]] | None = None

    if config.validate:
        split_idx = max(1, int(history_rows * (1 - config.validation_fraction)))
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()
        print(f"Backtest split: train={len(train_df)}  test={len(test_df)}", flush=True)

        backtest_holidays = build_holidays_frame(train_df, config.holidays_col)
        model_bt = fit_prophet(train_df, config, backtest_holidays)
        future_bt = build_future_frame(train_df, _replace(config, horizon=len(test_df)))
        forecast_bt = model_bt.predict(future_bt)
        prophet_pred = (
            forecast_bt.tail(len(test_df))["yhat"].tolist()
        )

        period = seasonal_period(config.freq)
        baselines = {
            "Prophet": score(test_df["y"].tolist(), prophet_pred),
            "Naive (last value)": score(test_df["y"].tolist(), naive_forecast(train_df, len(test_df))),
            "Seasonal naive": score(
                test_df["y"].tolist(),
                seasonal_naive_forecast(train_df, len(test_df), period),
            ),
        }

        import pandas as pd
        baselines_df = pd.DataFrame(baselines).T.reset_index().rename(columns={"index": "model"})
        baselines_path = config.output_dir / "baselines.csv"
        baselines_df.to_csv(baselines_path, index=False)
        print(f"Wrote {baselines_path}", flush=True)

    print("Fitting Prophet on full history ...", flush=True)
    model = fit_prophet(df, config, holidays_frame)
    future = build_future_frame(df, config)
    print(f"Predicting {config.horizon} {config.freq} periods ahead ...", flush=True)
    forecast = model.predict(future)
    horizon_forecast = forecast.tail(config.horizon)

    forecast_path = config.output_dir / "forecast.csv"
    horizon_forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(forecast_path, index=False)
    print(f"Wrote {forecast_path}", flush=True)

    chart_path = config.output_dir / "forecast.png"
    plot_forecast(
        history=df,
        forecast=forecast,
        output_path=chart_path,
        tokens=tokens,
        title=f"{config.target_col} — actuals and {config.horizon}-period forecast",
    )
    print(f"Wrote {chart_path}", flush=True)

    components_path = config.output_dir / "components.png"
    plot_components(model, forecast, components_path, tokens)
    print(f"Wrote {components_path}", flush=True)

    summary_path = config.output_dir / "summary.md"
    write_summary(summary_path, config, history_rows, horizon_forecast, baselines)
    print(f"Wrote {summary_path}", flush=True)

    print("Done.", flush=True)


def _replace(config: RunConfig, **overrides) -> RunConfig:
    from dataclasses import replace as dc_replace
    return dc_replace(config, **overrides)


def main(argv: Iterable[str] | None = None) -> int:
    config = parse_args(argv)
    _ensure_deps(config.auto_install)
    run(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
