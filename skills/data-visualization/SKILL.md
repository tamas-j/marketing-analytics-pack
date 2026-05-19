---
name: data-visualization
description: Use when a Marketing Analytics Pack command needs to create matplotlib charts with consistent palette, typography, annotations, and export settings.
user-invocable: false
---

# Data Visualization Reference

Use this reference skill whenever a command creates a chart. Do not invent chart styling locally. Load style tokens from `lib/visualize.py`, then copy the relevant chart pattern below into the generated Python.

## Required Inputs

- The chart purpose in plain language.
- The fields or values to plot.
- The active style name: `default`, `executive`, or `custom`. If the user has not chosen one, use `default`.
- Any source note or caveat that should appear below the chart.

## Style Loading Pattern

```python
from pathlib import Path
import sys

ROOT = Path.cwd()
if str(ROOT / "lib") not in sys.path:
    sys.path.insert(0, str(ROOT / "lib"))

from visualize import load_style, palette, chart_tokens, typography, layout, matplotlib_rc_params

style = load_style("default")
colors = palette(style)
chart = chart_tokens(style)
type_tokens = typography(style)
layout_tokens = layout(style)
```

## Matplotlib Setup Pattern

```python
import matplotlib.pyplot as plt

plt.rcParams.update(matplotlib_rc_params(style))

fig, ax = plt.subplots(
    figsize=(layout_tokens.get("figure_width", 9), layout_tokens.get("figure_height", 5)),
    dpi=layout_tokens.get("dpi", 160),
)
ax.grid(axis="y", linewidth=0.8, alpha=0.8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

## Bar Chart Pattern

Use for KPI comparisons, channel rankings, segment sizes, waterfall stages, and categorical diagnostics.

```python
labels = ["Paid search", "Email", "Organic", "Paid social"]
values = [1240, 920, 760, 680]

bars = ax.bar(labels, values, color=colors[: len(labels)])
ax.set_title("Conversions by channel", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_ylabel("Conversions")
ax.tick_params(axis="x", rotation=0)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=type_tokens.get("note_size", 8),
        color=chart.get("muted", "#6b7280"),
    )

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Line Chart Pattern

Use for trends, forecasts, time series diagnostics, and before/after comparisons.

```python
x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
y = [100, 112, 108, 129, 141, 155]

ax.plot(x, y, color=colors[0], linewidth=2.4, marker="o", markersize=4)
ax.set_title("Monthly revenue trend", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_ylabel("Revenue index")
ax.grid(axis="y", linewidth=0.8, alpha=0.8)

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Horizontal Bar Pattern

Use when labels are long, especially marketing channels, campaign names, personas, or root-cause factors.

```python
labels = ["Lifecycle email", "Paid search brand", "Organic social", "Display retargeting"]
values = [42, 37, 21, 18]

positions = range(len(labels))
ax.barh(positions, values, color=colors[: len(labels)])
ax.set_yticks(positions)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_title("Incremental lift by tactic", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_xlabel("Lift")

for index, value in enumerate(values):
    ax.text(value, index, f" {value:,.0f}", va="center", fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))

fig.tight_layout()
fig.savefig("chart.png", bbox_inches="tight")
```

## Scatter Pattern

Use for two-variable distributions where one or both axes are continuous: RFM Recency vs Frequency, CAC vs LTV, spend vs ROI, lead score vs conversion. Use the optional `sizes` argument when a third numeric variable (e.g. monetary value, deal size) is worth encoding as bubble area.

```python
groups = {
    "Champions":    {"x": [12, 18,  9, 22],   "y": [8, 7, 9, 6],  "m": [800, 920, 760, 1010]},
    "Loyal":        {"x": [40, 55, 48, 62],   "y": [5, 6, 4, 5],  "m": [520, 610, 480, 540]},
    "At risk":      {"x": [160, 190, 175],    "y": [3, 4, 3],     "m": [410, 480, 360]},
    "Hibernating":  {"x": [240, 280, 310],    "y": [1, 2, 1],     "m": [180, 210, 150]},
}

max_m = max(max(g["m"]) for g in groups.values()) or 1

for index, (label, g) in enumerate(groups.items()):
    sizes = [20 + 80 * (m / max_m) for m in g["m"]]
    ax.scatter(
        g["x"], g["y"],
        s=sizes,
        color=colors[index % len(colors)],
        alpha=0.75,
        edgecolors="none",
        label=label,
    )

ax.set_title("Recency vs Frequency by segment", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_xlabel("Recency (days since last order — lower is better)")
ax.set_ylabel("Frequency (orders in window)")
ax.grid(linewidth=0.8, alpha=0.6)
ax.legend(frameon=False, loc="best", fontsize=type_tokens.get("note_size", 8))

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Multi-Line Pattern

Use for several time series or response curves on the same axes: MMM saturation curves per channel, channel ROI over weeks, cohort retention curves. Keep to 6 or fewer lines — drop or facet beyond that.

```python
x = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]

series = {
    "Paid search":  [0,  82, 152, 210, 258, 296, 326, 348, 366],
    "Paid social":  [0,  60, 112, 158, 198, 232, 260, 282, 298],
    "Email":        [0,  42,  76, 104, 126, 142, 154, 162, 168],
    "TV":           [0,  20,  38,  54,  68,  80,  90,  98, 104],
}

for index, (label, values) in enumerate(series.items()):
    ax.plot(
        x, values,
        color=colors[index % len(colors)],
        linewidth=2.2,
        marker="o", markersize=3,
        label=label,
    )

ax.set_title("Response curves by channel", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_xlabel("Spend multiplier (1.0 = current)")
ax.set_ylabel("Incremental outcome")
ax.grid(axis="y", linewidth=0.8, alpha=0.8)
ax.legend(frameon=False, loc="best", fontsize=type_tokens.get("note_size", 8))

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Line With Interval (Fan) Pattern

Use for forecasts, predictions, or any line that carries an uncertainty band: Prophet forecasts, MMM contribution over time with credible interval, A/B uplift with confidence interval. The shaded band shows the interval; the solid line shows the central estimate; an optional history line shows actuals before the forecast horizon.

```python
history_x = ["W-12", "W-11", "W-10", "W-9", "W-8", "W-7", "W-6", "W-5", "W-4", "W-3", "W-2", "W-1"]
history_y = [100, 104, 108, 106, 112, 118, 122, 119, 124, 130, 128, 134]

forecast_x   = ["W+1", "W+2", "W+3", "W+4", "W+5", "W+6"]
forecast_y   = [138, 142, 145, 148, 151, 154]
forecast_lo  = [128, 130, 131, 132, 133, 134]
forecast_hi  = [148, 154, 159, 164, 169, 174]

ax.plot(history_x, history_y, color=chart.get("muted", "#6b7280"), linewidth=1.8, label="Actuals")
ax.plot(forecast_x, forecast_y, color=colors[0], linewidth=2.4, marker="o", markersize=4, label="Forecast")
ax.fill_between(forecast_x, forecast_lo, forecast_hi, color=colors[0], alpha=0.18, linewidth=0, label="80% interval")

ax.set_title("Weekly revenue — actuals and forecast", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_ylabel("Revenue")
ax.grid(axis="y", linewidth=0.8, alpha=0.8)
ax.tick_params(axis="x", rotation=0)
ax.legend(frameon=False, loc="upper left", fontsize=type_tokens.get("note_size", 8))

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Waterfall Pattern

Use when explaining how a starting count decomposes into losses (and optional gains) before arriving at a remaining total: suppression waterfalls, list eligibility losses, budget allocation, revenue bridges. Negative deltas use the chart `negative` colour; positive deltas use `positive`; totals use the primary palette colour.

```python
labels  = ["Starting list", "Ineligible", "No consent", "Bounces", "Recent buyers", "Frequency cap", "Final reachable"]
deltas  = [200_000, -45_000, -28_000, -7_000, -12_000, -18_000, None]   # None marks a total bar
is_total = [True, False, False, False, False, False, True]

running = 0
bases   = []
heights = []
bar_colors = []

for delta, total in zip(deltas, is_total):
    if total:
        bases.append(0)
        heights.append(running if delta is None else delta)
        running = heights[-1]
        bar_colors.append(colors[0])
    else:
        # Place the bar so it visually connects from the running total.
        height = abs(delta)
        if delta < 0:
            bases.append(running + delta)   # bar grows downward from current total
            running += delta
        else:
            bases.append(running)
            running += delta
        heights.append(height)
        bar_colors.append(chart.get("negative", "#dc2626") if delta < 0 else chart.get("positive", "#16a34a"))

positions = list(range(len(labels)))
ax.bar(positions, heights, bottom=bases, color=bar_colors, width=0.7)

# Connector lines between consecutive bar tops/bottoms.
tops = [b + h for b, h in zip(bases, heights)]
for i in range(len(positions) - 1):
    y = tops[i] if not is_total[i + 1] else (bases[i] + heights[i])
    ax.plot([positions[i] + 0.35, positions[i + 1] - 0.35], [y, y],
            color=chart.get("muted", "#6b7280"), linewidth=0.8, linestyle=":")

ax.set_xticks(positions)
ax.set_xticklabels(labels, rotation=20, ha="right")
ax.set_title("Suppression waterfall — campaign reach", pad=layout_tokens.get("title_pad", 14), loc="left")
ax.set_ylabel("Customers")
ax.grid(axis="y", linewidth=0.8, alpha=0.8)
ax.set_axisbelow(True)

for position, delta, base, height, total in zip(positions, deltas, bases, heights, is_total):
    if total:
        ax.text(position, base + height, f"{height:,.0f}", ha="center", va="bottom",
                fontsize=type_tokens.get("note_size", 8), color=chart.get("foreground", "#111827"))
    else:
        ax.text(position, base + height, f"{delta:+,.0f}", ha="center", va="bottom",
                fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Overlap Matrix Pattern

Use for pairwise audience overlap, channel cannibalisation, segment cross-membership, or any square comparison where each cell is a percentage / count: audience overlap heatmaps, persona x channel reach, A/B variant cross-conversion.

```python
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

audiences = ["Email file", "Paid social", "Display", "VIP list"]
# Cell [i, j] = overlap of audience i with audience j as a percentage of i.
overlap = np.array([
    [100, 38, 22,  8],
    [ 41, 100, 28, 12],
    [ 19, 22, 100,  5],
    [ 64, 47, 22, 100],
])

# Build a brand-aware colormap from the sequential palette.
sequential = palette(style, kind="sequential") or colors
cmap = LinearSegmentedColormap.from_list("seq", sequential, N=256)

ax.grid(False)
heatmap = ax.imshow(overlap, cmap=cmap, vmin=0, vmax=100, aspect="auto")

ax.set_xticks(range(len(audiences)))
ax.set_xticklabels(audiences, rotation=20, ha="right")
ax.set_yticks(range(len(audiences)))
ax.set_yticklabels(audiences)
ax.set_title("Audience overlap (% of row in column)", pad=layout_tokens.get("title_pad", 14), loc="left")

# Annotate each cell.
for i in range(overlap.shape[0]):
    for j in range(overlap.shape[1]):
        value = overlap[i, j]
        text_color = chart.get("background", "#ffffff") if value >= 55 else chart.get("foreground", "#111827")
        ax.text(j, i, f"{value:.0f}%", ha="center", va="center",
                fontsize=type_tokens.get("note_size", 8), color=text_color)

cbar = fig.colorbar(heatmap, ax=ax, shrink=0.85)
cbar.ax.tick_params(labelsize=type_tokens.get("tick_size", 9))

fig.text(0.01, 0.01, layout_tokens.get("source_note", ""), fontsize=type_tokens.get("note_size", 8), color=chart.get("muted", "#6b7280"))
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig("chart.png", bbox_inches="tight")
```

## Number Formatting Helpers

```python
def fmt_number(value):
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def fmt_percent(value):
    return f"{value:.1%}"
```

## Output Rules

- Prefer horizontal bars when category labels are long.
- Use the active style palette in order; reserve `positive`, `negative`, and `warning` chart-token colors for status meaning (waterfall losses, guardrail breaches, etc.) — not for ordinary categories.
- Add value labels when there are 12 or fewer marks.
- Include a short source note when data provenance is available.
- Export charts as PNG with `bbox_inches="tight"` unless the command explicitly needs another format.

## Pattern Selection Guide

| Situation | Pattern |
|---|---|
| Ranked categories (channels, segments, tactics, campaigns) | Bar / Horizontal Bar |
| A single time series or trend | Line |
| Several time series or response curves on the same axes | Multi-Line |
| Time series with an uncertainty band (forecasts, model fits, A/B uplift) | Line With Interval (Fan) |
| Two continuous variables, optionally with a third encoded as size | Scatter |
| Sequential decomposition (start → losses → remaining) | Waterfall |
| Pairwise comparison across the same set on both axes | Overlap Matrix |
