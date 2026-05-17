"""Thin style reader for Marketing Analytics Pack chart outputs.

Chart code lives in the data-visualization reference skill. This module only
loads style YAML and exposes small helpers for palettes, typography, and brand
fields.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


STYLE_ENV_VAR = "MARKETING_ANALYTICS_STYLE"
DEFAULT_STYLE = "default"
STYLE_DIR = Path(__file__).resolve().parent / "styles"


def load_style(name: str | None = None, style_dir: str | Path | None = None) -> dict[str, Any]:
    """Load a bundled style by name.

    The active style can be supplied directly or through MARKETING_ANALYTICS_STYLE.
    Missing styles fall back to the default style.
    """

    selected = _safe_style_name(name or os.getenv(STYLE_ENV_VAR) or DEFAULT_STYLE)
    styles_path = Path(style_dir) if style_dir else STYLE_DIR
    path = styles_path / f"{selected}.yaml"

    if not path.exists() and selected != DEFAULT_STYLE:
        path = styles_path / f"{DEFAULT_STYLE}.yaml"

    if not path.exists():
        raise FileNotFoundError(f"No style YAML found at {path}")

    return _parse_style_yaml(path)


def palette(style: dict[str, Any] | None = None, kind: str = "categorical") -> list[str]:
    """Return a color palette, defaulting to the categorical set."""

    style_data = style or load_style()
    values = style_data.get("palette", {}).get(kind, [])
    if not values:
        values = style_data.get("palette", {}).get("categorical", [])
    return list(values)


def brand(style: dict[str, Any] | None = None) -> dict[str, str]:
    """Return brand settings such as primary color, logo path, and font family."""

    style_data = style or load_style()
    return dict(style_data.get("brand", {}))


def typography(style: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return typography settings."""

    style_data = style or load_style()
    return dict(style_data.get("typography", {}))


def chart_tokens(style: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return chart-level tokens such as background, foreground, grid, and status colors."""

    style_data = style or load_style()
    return dict(style_data.get("chart", {}))


def layout(style: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return layout settings such as figure size, DPI, and source note."""

    style_data = style or load_style()
    return dict(style_data.get("layout", {}))


def matplotlib_rc_params(style: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a minimal rcParams dict for matplotlib outputs."""

    style_data = style or load_style()
    chart = chart_tokens(style_data)
    type_tokens = typography(style_data)
    brand_tokens = brand(style_data)

    return {
        "figure.facecolor": chart.get("background", "#ffffff"),
        "axes.facecolor": chart.get("background", "#ffffff"),
        "axes.edgecolor": chart.get("grid", "#e5e7eb"),
        "axes.labelcolor": chart.get("foreground", "#111827"),
        "axes.titlecolor": chart.get("foreground", "#111827"),
        "xtick.color": chart.get("muted", "#6b7280"),
        "ytick.color": chart.get("muted", "#6b7280"),
        "grid.color": chart.get("grid", "#e5e7eb"),
        "text.color": chart.get("foreground", "#111827"),
        "font.family": brand_tokens.get("font_family", "Arial"),
        "axes.titlesize": type_tokens.get("title_size", 16),
        "axes.labelsize": type_tokens.get("label_size", 10),
        "xtick.labelsize": type_tokens.get("tick_size", 9),
        "ytick.labelsize": type_tokens.get("tick_size", 9),
    }


def _safe_style_name(name: str) -> str:
    cleaned = name.strip().lower()
    if not cleaned:
        return DEFAULT_STYLE
    if not all(char.isalnum() or char == "-" for char in cleaned):
        raise ValueError(f"Invalid style name: {name!r}")
    return cleaned


def _parse_style_yaml(path: Path) -> dict[str, Any]:
    """Parse the small YAML subset used by lib/styles without extra dependencies."""

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Style file must contain a mapping: {path}")
        return data
    except ModuleNotFoundError:
        return _parse_simple_yaml(path.read_text(encoding="utf-8"))


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current_key: str | None = None
    current_nested_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            key, value = _split_key_value(line)
            current_key = key
            current_nested_key = None
            root[key] = {} if value is None else _parse_scalar(value)
            continue

        if current_key is None:
            raise ValueError("Nested value found before a top-level key")

        container = root.setdefault(current_key, {})
        if not isinstance(container, dict):
            raise ValueError(f"Cannot nest under scalar key: {current_key}")

        if line.startswith("- "):
            if current_nested_key is None:
                raise ValueError("List item found before a list key")
            target = container.setdefault(current_nested_key, [])
            if not isinstance(target, list):
                raise ValueError(f"Cannot append to non-list key: {current_nested_key}")
            target.append(_parse_scalar(line[2:].strip()))
            continue

        key, value = _split_key_value(line)
        if value is None:
            container[key] = []
            current_nested_key = key
        else:
            container[key] = _parse_scalar(value)
            current_nested_key = key

    return root


def _split_key_value(line: str) -> tuple[str, str | None]:
    if ":" not in line:
        raise ValueError(f"Expected key: value line, got {line!r}")
    key, value = line.split(":", 1)
    value = value.strip()
    return key.strip(), value if value else None


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"''", '""'}:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value
