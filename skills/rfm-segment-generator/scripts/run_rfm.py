#!/usr/bin/env python3
"""RFM segmentation runner for marketing-analytics-pack.

Reads a transactions CSV with customer / date / value columns, computes
Recency-Frequency-Monetary scores per customer, assigns named segments
(quantile rules by default, optional k-means), and writes:

    rfm_scores.csv         per-customer R, F, M, scores, and segment
    segment_profiles.csv   per-segment customer count, R/F/M means, total value
    segment_sizes.png      bar chart of customers per segment, styled
    rf_scatter.png         Recency vs Frequency scatter, coloured by segment
    summary.md             short narrative

Chart styling is loaded from `lib/visualize.py`.

Run from the repo root, with deps installed first
(`pip install -r skills/rfm-segment-generator/scripts/requirements.txt`), or
pass `--auto-install` to let the script install them on first use.

Example
-------

    python skills/rfm-segment-generator/scripts/run_rfm.py \\
        --input examples/data/orders.csv \\
        --customer-col customer_id \\
        --date-col order_date \\
        --value-col order_value \\
        --method quantile \\
        --output-dir examples/rfm-segment/output \\
        --style default
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS = REPO_ROOT / "skills" / "rfm-segment-generator" / "scripts" / "requirements.txt"
LIB_DIR = REPO_ROOT / "lib"


# --------------------------------------------------------------------------- #
# Dep handling (PEP 668-aware, mirrors forecast-runner / mmm-runner)          #
# --------------------------------------------------------------------------- #

REQUIRED_IMPORTS = {
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "yaml": "pyyaml",
}
KMEANS_IMPORTS = {"sklearn": "scikit-learn"}


def _missing_deps(extra: dict[str, str] | None = None) -> list[str]:
    missing: list[str] = []
    targets = dict(REQUIRED_IMPORTS)
    if extra:
        targets.update(extra)
    for module, package in targets.items():
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
    print(f"Installing rfm-segment deps from {REQUIREMENTS} ...", flush=True)
    base_args = ["-r", str(REQUIREMENTS), "--prefer-binary"]
    code = _pip_install(base_args)
    if code == 0:
        return
    if not _in_virtualenv():
        print("Retrying with --user (PEP 668 fallback) ...", flush=True)
        code = _pip_install([*base_args, "--user"])
        if code == 0:
            return
    print(
        "\nrfm-segment-generator could not install its dependencies.\n"
        "Create a virtual environment and retry:\n\n"
        "    python3 -m venv .venv\n"
        "    source .venv/bin/activate      # Linux / macOS\n"
        "    .venv\\Scripts\\activate       # Windows PowerShell\n"
        f"    pip install -r {REQUIREMENTS}\n",
        file=sys.stderr,
    )
    sys.exit(2)


def _ensure_deps(auto_install: bool, need_kmeans: bool) -> None:
    extra = KMEANS_IMPORTS if need_kmeans else None
    missing = _missing_deps(extra)
    if not missing:
        return
    if not auto_install:
        print(
            "rfm-segment-generator is missing required packages: "
            + ", ".join(missing)
            + f"\nInstall them: pip install -r {REQUIREMENTS}\n"
            "Or rerun with --auto-install.",
            file=sys.stderr,
        )
        sys.exit(2)
    _install_deps()
    missing = _missing_deps(extra)
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
    customer_col: str
    date_col: str
    value_col: str
    status_col: str | None
    valid_statuses: list[str]
    analysis_date: str | None
    method: str
    n_clusters: int
    output_dir: Path
    style_name: str
    auto_install: bool


def parse_args(argv: Iterable[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Compute RFM segmentation from transactions and write styled outputs.",
    )
    parser.add_argument("--input", required=True, help="Path to transactions CSV")
    parser.add_argument("--customer-col", required=True, help="Customer ID column")
    parser.add_argument("--date-col", required=True, help="Order date column")
    parser.add_argument("--value-col", required=True, help="Order value column")
    parser.add_argument("--status-col", default=None,
                        help="Optional order status column (filter to valid statuses)")
    parser.add_argument("--valid-statuses", default="",
                        help="Comma-separated list of order statuses to keep (only used with --status-col)")
    parser.add_argument("--analysis-date", default=None,
                        help="ISO date used as the recency anchor (default: max date in the file)")
    parser.add_argument("--method", default="quantile", choices=["quantile", "kmeans"],
                        help="Segmentation method (default quantile rules; kmeans uses scikit-learn)")
    parser.add_argument("--n-clusters", type=int, default=5,
                        help="Number of clusters when --method kmeans (default 5)")
    parser.add_argument("--output-dir", default="rfm_output",
                        help="Where to write artefacts (default ./rfm_output)")
    parser.add_argument("--style", default="default",
                        help="Style name from lib/styles (default, executive, custom)")
    parser.add_argument("--auto-install", action="store_true",
                        help="pip install requirements.txt if any dep is missing")

    args = parser.parse_args(list(argv) if argv is not None else None)

    valid_statuses = [s.strip() for s in args.valid_statuses.split(",") if s.strip()]

    return RunConfig(
        input_path=Path(args.input).expanduser().resolve(),
        customer_col=args.customer_col,
        date_col=args.date_col,
        value_col=args.value_col,
        status_col=args.status_col,
        valid_statuses=valid_statuses,
        analysis_date=args.analysis_date,
        method=args.method,
        n_clusters=args.n_clusters,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        style_name=args.style,
        auto_install=args.auto_install,
    )


# --------------------------------------------------------------------------- #
# RFM computation                                                             #
# --------------------------------------------------------------------------- #


def load_transactions(config: RunConfig):
    import pandas as pd

    df = pd.read_csv(config.input_path)
    for col in [config.customer_col, config.date_col, config.value_col]:
        if col not in df.columns:
            raise SystemExit(f"Column {col!r} not found in {config.input_path}")

    if config.status_col:
        if config.status_col not in df.columns:
            raise SystemExit(f"Status column {config.status_col!r} not found")
        if config.valid_statuses:
            df = df[df[config.status_col].isin(config.valid_statuses)]

    df = df.copy()
    df[config.date_col] = pd.to_datetime(df[config.date_col])
    df = df.dropna(subset=[config.customer_col, config.date_col, config.value_col])
    return df


def compute_rfm(df, config: RunConfig):
    import pandas as pd

    anchor = (
        pd.to_datetime(config.analysis_date) if config.analysis_date else df[config.date_col].max()
    )

    rfm = (
        df.groupby(config.customer_col)
        .agg(
            recency=(config.date_col, lambda s: (anchor - s.max()).days),
            frequency=(config.date_col, "count"),
            monetary=(config.value_col, "sum"),
        )
        .reset_index()
    )
    rfm = rfm.rename(columns={config.customer_col: "customer_id"})
    return rfm, anchor


# --------------------------------------------------------------------------- #
# Segmentation                                                                #
# --------------------------------------------------------------------------- #


SEGMENT_RULES = [
    # (segment label, predicate over (r_score, f_score, m_score))
    ("Champions",       lambda r, f, m: r >= 4 and f >= 4 and m >= 4),
    ("Loyal",           lambda r, f, m: r >= 3 and f >= 4),
    ("Big spenders",    lambda r, f, m: m >= 4 and f >= 3),
    ("New customers",   lambda r, f, m: r >= 4 and f <= 2),
    ("Promising",       lambda r, f, m: r >= 3 and f >= 2 and m >= 2),
    ("At risk",         lambda r, f, m: r <= 2 and (f >= 3 or m >= 3)),
    ("Hibernating",     lambda r, f, m: r <= 2 and f <= 2 and m <= 2),
]


def _score_quantile(series, ascending: bool):
    """Return integer scores 1..5 via quintile binning.

    `ascending=True` means higher raw values get higher scores (good for F/M).
    For Recency (`ascending=False`) we invert because lower recency = better.
    """
    import pandas as pd

    if series.nunique() < 2:
        return pd.Series([3] * len(series), index=series.index)

    # qcut with duplicates='drop' handles ties; pad to 5 buckets when possible.
    try:
        bucketed = pd.qcut(series, q=5, labels=False, duplicates="drop") + 1
    except ValueError:
        bucketed = pd.qcut(series.rank(method="first"), q=5, labels=False) + 1

    if not ascending:
        bucketed = (5 + 1) - bucketed
    return bucketed.astype(int)


def segment_quantile(rfm):
    rfm = rfm.copy()
    rfm["r_score"] = _score_quantile(rfm["recency"], ascending=False)
    rfm["f_score"] = _score_quantile(rfm["frequency"], ascending=True)
    rfm["m_score"] = _score_quantile(rfm["monetary"], ascending=True)

    def assign(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        for label, predicate in SEGMENT_RULES:
            if predicate(r, f, m):
                return label
        return "Other"

    rfm["segment"] = rfm.apply(assign, axis=1)
    return rfm


def segment_kmeans(rfm, n_clusters: int):
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler

    rfm = rfm.copy()
    rfm["r_score"] = _score_quantile(rfm["recency"], ascending=False)
    rfm["f_score"] = _score_quantile(rfm["frequency"], ascending=True)
    rfm["m_score"] = _score_quantile(rfm["monetary"], ascending=True)

    features = rfm[["recency", "frequency", "monetary"]].astype(float).values
    scaled = StandardScaler().fit_transform(features)
    km = KMeans(n_clusters=n_clusters, n_init=10, random_state=1)
    labels = km.fit_predict(scaled)

    # Rank clusters by total monetary descending so labels are stable + intuitive.
    rfm["_cluster"] = labels
    order = (
        rfm.groupby("_cluster")["monetary"].sum().sort_values(ascending=False).index.tolist()
    )
    label_map = {cluster: f"Cluster {idx + 1}" for idx, cluster in enumerate(order)}
    rfm["segment"] = rfm["_cluster"].map(label_map)
    rfm = rfm.drop(columns=["_cluster"])
    return rfm


# --------------------------------------------------------------------------- #
# Profiling                                                                   #
# --------------------------------------------------------------------------- #


def segment_profiles(rfm):
    import pandas as pd

    grouped = rfm.groupby("segment").agg(
        customers=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_monetary=("monetary", "sum"),
    ).reset_index()
    grouped = grouped.sort_values("total_monetary", ascending=False).reset_index(drop=True)
    return grouped


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


def plot_segment_sizes(profiles, output_path: Path, tokens) -> None:
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

    positions = list(range(len(profiles)))
    ax.barh(positions, profiles["customers"], color=colors[: len(profiles)])
    ax.set_yticks(positions)
    ax.set_yticklabels(profiles["segment"])
    ax.invert_yaxis()
    ax.set_title("Customers per RFM segment", pad=layout_tokens.get("title_pad", 14), loc="left")
    ax.set_xlabel("Customers")
    for i, value in enumerate(profiles["customers"]):
        ax.text(value, i, f" {value:,.0f}", va="center",
                fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))

    source_note = layout_tokens.get("source_note", "")
    if source_note:
        fig.text(0.01, 0.01, source_note,
                 fontsize=type_tokens.get("note_size", 8),
                 color=chart.get("muted", "#6b7280"))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def plot_rf_scatter(rfm, output_path: Path, tokens) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(tokens["rc"])
    fig, ax = plt.subplots(
        figsize=(tokens["layout"].get("figure_width", 9), tokens["layout"].get("figure_height", 5)),
        dpi=tokens["layout"].get("dpi", 160),
    )
    ax.grid(linewidth=0.8, alpha=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    colors = tokens["palette"]
    chart = tokens["chart"]
    type_tokens = tokens["typography"]
    layout_tokens = tokens["layout"]

    for idx, (segment, sub) in enumerate(rfm.groupby("segment")):
        ax.scatter(sub["recency"], sub["frequency"],
                   color=colors[idx % len(colors)], alpha=0.7,
                   s=20 + sub["monetary"] / max(rfm["monetary"].max(), 1) * 80,
                   label=segment, edgecolors="none")

    ax.set_title("Recency vs Frequency, coloured by segment",
                 pad=layout_tokens.get("title_pad", 14), loc="left")
    ax.set_xlabel("Recency (days since last order — lower is better)")
    ax.set_ylabel("Frequency (orders in window)")
    ax.legend(frameon=False, loc="best", fontsize=type_tokens.get("note_size", 8))

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


def write_summary(output_path: Path, config: RunConfig, anchor, n_customers: int, profiles) -> None:
    lines: list[str] = []
    lines.append("# RFM segmentation summary")
    lines.append("")
    lines.append(f"- Input: `{config.input_path}`")
    lines.append(f"- Customers: {n_customers}")
    lines.append(f"- Analysis date (recency anchor): {anchor.date() if hasattr(anchor, 'date') else anchor}")
    lines.append(f"- Method: `{config.method}`"
                 + (f" (k={config.n_clusters})" if config.method == "kmeans" else ""))
    lines.append("")
    lines.append("## Segment profiles")
    lines.append("")
    lines.append("| Segment | Customers | Avg recency (days) | Avg frequency | Avg monetary | Total monetary |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for _, row in profiles.iterrows():
        lines.append(
            f"| {row['segment']} | {row['customers']:,} | "
            f"{row['avg_recency']:.1f} | {row['avg_frequency']:.1f} | "
            f"{row['avg_monetary']:,.0f} | {row['total_monetary']:,.0f} |"
        )
    lines.append("")
    if not profiles.empty:
        top = profiles.iloc[0]
        lines.append(f"Top segment by total revenue: **{top['segment']}** "
                     f"({top['customers']:,} customers, {top['total_monetary']:,.0f} total).")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    lines.append("- `rfm_scores.csv` — one row per customer with R/F/M, scores, and segment")
    lines.append("- `segment_profiles.csv` — segment-level customer count and R/F/M means")
    lines.append("- `segment_sizes.png` — bar chart of customers per segment")
    lines.append("- `rf_scatter.png` — Recency vs Frequency scatter, coloured by segment")
    lines.append("")
    lines.append("## Caveats")
    lines.append("")
    lines.append("- RFM is descriptive, not predictive — treat segments as activation buckets, not forecasts.")
    lines.append("- Monetary excludes nothing unless you filtered the input — refunds, tax, shipping, and discounts are all in `monetary` as-is.")
    lines.append("- Recency anchor matters: changing `--analysis-date` shifts every customer's R score.")
    lines.append("- Don't over-message At-risk / Hibernating without fatigue and margin guardrails.")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Orchestration                                                               #
# --------------------------------------------------------------------------- #


def run(config: RunConfig) -> None:
    config.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading {config.input_path} ...", flush=True)
    df = load_transactions(config)
    print(f"  {len(df):,} transactions, "
          f"{df[config.customer_col].nunique():,} customers", flush=True)

    rfm, anchor = compute_rfm(df, config)
    print(f"Computed RFM for {len(rfm):,} customers; recency anchor = {anchor.date()}", flush=True)

    if config.method == "kmeans":
        rfm = segment_kmeans(rfm, config.n_clusters)
    else:
        rfm = segment_quantile(rfm)
    profiles = segment_profiles(rfm)

    rfm_path = config.output_dir / "rfm_scores.csv"
    rfm.to_csv(rfm_path, index=False)
    print(f"Wrote {rfm_path}", flush=True)

    profiles_path = config.output_dir / "segment_profiles.csv"
    profiles.to_csv(profiles_path, index=False)
    print(f"Wrote {profiles_path}", flush=True)

    tokens = _load_style(config.style_name)

    sizes_png = config.output_dir / "segment_sizes.png"
    plot_segment_sizes(profiles, sizes_png, tokens)
    print(f"Wrote {sizes_png}", flush=True)

    scatter_png = config.output_dir / "rf_scatter.png"
    plot_rf_scatter(rfm, scatter_png, tokens)
    print(f"Wrote {scatter_png}", flush=True)

    summary_path = config.output_dir / "summary.md"
    write_summary(summary_path, config, anchor, len(rfm), profiles)
    print(f"Wrote {summary_path}", flush=True)

    print("Done.", flush=True)


def main(argv: Iterable[str] | None = None) -> int:
    config = parse_args(argv)
    _ensure_deps(config.auto_install, need_kmeans=(config.method == "kmeans"))
    run(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
