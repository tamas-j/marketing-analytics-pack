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
- Use the active style palette in order; reserve positive, negative, and warning colors for status meaning.
- Add value labels when there are 12 or fewer marks.
- Include a short source note when data provenance is available.
- Export charts as PNG with `bbox_inches="tight"` unless the command explicitly needs another format.
