#!/usr/bin/env python3
"""Build a single self-contained HTML report from a Marketing Analytics Pack skill output.

Takes a markdown source (file path or stdin), an optional directory of images,
and writes one .html file that:

- Renders the markdown with the `markdown` library (tables, fenced code, headings).
- Embeds every PNG / JPG / SVG in the images directory as a base64 data URI in
  the HTML, so the file is fully portable (no external assets, opens anywhere).
- Applies brand palette / typography from `lib/styles/<style>.yaml` so the look
  matches the chart visuals the pack produces.
- If the source markdown does not reference some images we discovered, appends
  them as a "Charts" section at the bottom so runner outputs (RFM, Prophet,
  Meridian) always surface their visuals.
- Adds an artifact header with report type, audience, source, data source,
  prior-report reference, and extracted key sections for quick stakeholder scan.

Run from the repo root, with deps installed first
(`pip install -r skills/report-builder/scripts/requirements.txt`), or pass
`--auto-install` to let the script install them on first use.

Example
-------

    python skills/report-builder/scripts/build_html_report.py \\
        --input examples/rfm-segment/output/summary.md \\
        --images examples/rfm-segment/output \\
        --output report-out/rfm-report.html \\
        --title "RFM segmentation - Q4 review" \\
        --style default \\
        --report-type rfm
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import mimetypes
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS = REPO_ROOT / "skills" / "report-builder" / "scripts" / "requirements.txt"
LIB_DIR = REPO_ROOT / "lib"

REQUIRED_IMPORTS = {
    "markdown": "markdown",
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
    print(f"Installing report-builder deps from {REQUIREMENTS} ...", flush=True)
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
        "\nreport-builder could not install its dependencies.\n"
        "Create a virtual environment and retry:\n\n"
        "    python3 -m venv .venv\n"
        "    source .venv/bin/activate\n"
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
            "report-builder is missing required packages: " + ", ".join(missing)
            + f"\nInstall: pip install -r {REQUIREMENTS}\n"
            "Or rerun with --auto-install.",
            file=sys.stderr,
        )
        sys.exit(2)
    _install_deps()
    missing = _missing_deps()
    if missing:
        print(
            "Auto-install completed but these are still missing: " + ", ".join(missing),
            file=sys.stderr,
        )
        sys.exit(2)


@dataclass
class RunConfig:
    input_path: Path | None
    images_dir: Path | None
    output_path: Path
    title: str | None
    style_name: str
    report_type: str
    audience: str | None
    source_label: str | None
    data_source: str | None
    previous_report: str | None
    auto_install: bool


def parse_args(argv: Iterable[str] | None = None) -> RunConfig:
    parser = argparse.ArgumentParser(
        description="Build a single self-contained HTML report from a markdown source.",
    )
    parser.add_argument("--input", required=True,
                        help="Path to markdown file, or '-' to read from stdin")
    parser.add_argument("--images", default=None,
                        help="Directory of images to embed inline (PNG/JPG/SVG)")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", default=None,
                        help="Report title (defaults to first markdown H1 or filename)")
    parser.add_argument("--style", default="default",
                        help="Style name from lib/styles (default, executive, custom)")
    parser.add_argument(
        "--report-type",
        default="auto",
        choices=[
            "auto",
            "executive-summary",
            "kpi-tree",
            "metric-spec",
            "clv-scenario",
            "journey-framework",
            "forecast",
            "mmm",
            "rfm",
            "post-mortem",
            "generic",
        ],
        help="HTML artifact template to use (default: auto)",
    )
    parser.add_argument("--audience", default=None,
                        help="Intended reader, e.g. executive, analyst, lifecycle team")
    parser.add_argument("--source-label", default=None,
                        help="Human-readable source label shown in the artifact header")
    parser.add_argument("--data-source", default=None,
                        help="Dataset, folder, or system name shown in the artifact header")
    parser.add_argument("--previous-report", default=None,
                        help="Optional path or label for the previous report in a recurring series")
    parser.add_argument("--auto-install", action="store_true",
                        help="pip install requirements.txt if any dep is missing")
    args = parser.parse_args(list(argv) if argv is not None else None)
    input_path = None if args.input == "-" else Path(args.input).expanduser().resolve()
    images_dir = Path(args.images).expanduser().resolve() if args.images else None
    return RunConfig(
        input_path=input_path,
        images_dir=images_dir,
        output_path=Path(args.output).expanduser().resolve(),
        title=args.title,
        style_name=args.style,
        report_type=args.report_type,
        audience=args.audience,
        source_label=args.source_label,
        data_source=args.data_source,
        previous_report=args.previous_report,
        auto_install=args.auto_install,
    )


def load_style_tokens(style_name: str) -> dict:
    if str(LIB_DIR) not in sys.path:
        sys.path.insert(0, str(LIB_DIR))
    from visualize import load_style, palette, chart_tokens, typography, layout, brand
    style = load_style(style_name)
    return {
        "palette": palette(style),
        "chart": chart_tokens(style),
        "typography": typography(style),
        "layout": layout(style),
        "brand": brand(style),
    }


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
IMG_SRC_RE = re.compile(r'<img([^>]*?)src="([^"]+)"', re.IGNORECASE)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)

REPORT_TYPE_LABELS = {
    "executive-summary": "Executive Summary",
    "kpi-tree": "KPI Tree",
    "metric-spec": "Metric Spec",
    "clv-scenario": "CLV Scenario",
    "journey-framework": "Journey Framework",
    "forecast": "Forecast",
    "mmm": "MMM Readout",
    "rfm": "RFM Segmentation",
    "post-mortem": "Post-Mortem",
    "generic": "Marketing Analysis",
}

REPORT_TYPE_KEY_SECTIONS = {
    "executive-summary": ["Executive Summary", "Recommended First Analysis", "Caveats", "Next Steps"],
    "kpi-tree": ["Executive Summary", "KPI Tree", "Diagnostic Questions", "Recommended First Analysis"],
    "metric-spec": ["Purpose", "Definition", "Formula", "Caveats and Guardrails", "QA Checks"],
    "clv-scenario": ["Decision Summary", "Scenario Results", "Sensitivity Notes", "Guardrails and Caveats"],
    "journey-framework": ["Journey Summary", "Measurement Framework", "Measurement Gaps", "Recommended First Analysis"],
    "forecast": ["Forecast Summary", "Baseline Comparison", "Caveats", "Recommended Next Step"],
    "mmm": ["Executive Summary", "ROI", "Contribution", "Response Curves", "Caveats"],
    "rfm": ["Segment Profiles", "Top Segment", "Activation Recommendations", "Caveats"],
    "post-mortem": ["Executive Summary", "What Happened", "Root Causes", "Actions"],
    "generic": ["Executive Summary", "Recommended First Analysis", "Caveats", "Next Steps"],
}


def discover_images(images_dir: Path | None) -> dict[str, str]:
    if not images_dir or not images_dir.is_dir():
        return {}
    mapping: dict[str, str] = {}
    for path in sorted(images_dir.iterdir()):
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        mime, _ = mimetypes.guess_type(str(path))
        if mime is None:
            mime = "image/png"
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        mapping[path.name] = f"data:{mime};base64,{encoded}"
    return mapping


def inline_images(html: str, image_map: dict[str, str]) -> tuple[str, list[str], set[str]]:
    missing: list[str] = []
    used: set[str] = set()

    def replacer(match: re.Match[str]) -> str:
        attrs = match.group(1)
        src = match.group(2)
        basename = Path(src).name
        if basename in image_map:
            used.add(basename)
            return f'<img{attrs}src="{image_map[basename]}"'
        if src.startswith("data:") or src.startswith(("http://", "https://")):
            return match.group(0)
        missing.append(src)
        return match.group(0)

    rewritten = IMG_SRC_RE.sub(replacer, html)
    return rewritten, missing, used


def append_unreferenced_images(html: str, image_map: dict[str, str], used: set[str]) -> str:
    leftover = [name for name in image_map if name not in used]
    if not leftover:
        return html
    cards: list[str] = []
    for name in leftover:
        caption = name.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
        cards.append(
            f'<figure class="chart">'
            f'<img alt="{_html_escape(caption)}" src="{image_map[name]}">'
            f'<figcaption>{_html_escape(caption)}</figcaption>'
            f'</figure>'
        )
    return html + (
        '<section class="auto-charts">'
        '<h2>Charts</h2>'
        + "".join(cards)
        + '</section>'
    )


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --primary: __PRIMARY__;
  --foreground: __FOREGROUND__;
  --muted: __MUTED__;
  --background: __BACKGROUND__;
  --grid: __GRID__;
  --positive: __POSITIVE__;
  --negative: __NEGATIVE__;
  --warning: __WARNING__;
  --font-family: __FONT_FAMILY__;
  --title-size: __TITLE_SIZE__px;
  --label-size: __LABEL_SIZE__px;
  --note-size: __NOTE_SIZE__px;
}
html, body {
  background: var(--background);
  color: var(--foreground);
  font-family: var(--font-family), system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 0;
  font-size: var(--label-size);
  line-height: 1.55;
}
.report {
  max-width: 1080px;
  margin: 0 auto;
  padding: 48px 32px 80px;
}
.report-header {
  border-bottom: 2px solid var(--primary);
  padding-bottom: 16px;
  margin-bottom: 28px;
}
.report-header h1 {
  font-size: var(--title-size);
  margin: 0 0 6px;
  color: var(--foreground);
  font-weight: 600;
  line-height: 1.2;
}
.report-header .meta {
  color: var(--muted);
  font-size: var(--note-size);
}
.artifact-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: var(--primary);
  font-size: var(--note-size);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.artifact-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
  gap: 22px;
  align-items: start;
  margin: 0 0 28px;
}
.artifact-panel,
.artifact-card {
  border: 1px solid var(--grid);
  border-radius: 8px;
  background: rgba(107, 114, 128, 0.035);
}
.artifact-panel {
  padding: 16px 18px;
}
.artifact-panel h2,
.artifact-card h3 {
  margin-top: 0;
}
.artifact-meta {
  display: grid;
  grid-template-columns: 120px minmax(0, 1fr);
  gap: 7px 12px;
  font-size: var(--note-size);
}
.artifact-meta dt {
  color: var(--muted);
}
.artifact-meta dd {
  margin: 0;
  color: var(--foreground);
  overflow-wrap: anywhere;
}
.artifact-highlights {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 28px;
}
.artifact-card {
  padding: 13px 14px;
}
.artifact-card h3 {
  font-size: calc(var(--title-size) * 0.48);
  color: var(--primary);
  margin-bottom: 6px;
}
.artifact-card p {
  color: var(--foreground);
  font-size: var(--note-size);
  margin: 0;
}
.share-note {
  color: var(--muted);
  font-size: var(--note-size);
}
.report h2 {
  font-size: calc(var(--title-size) * 0.78);
  color: var(--foreground);
  margin: 32px 0 8px;
  font-weight: 600;
}
.report h3 {
  font-size: calc(var(--title-size) * 0.62);
  color: var(--foreground);
  margin: 24px 0 6px;
  font-weight: 600;
}
.report h4 {
  font-size: calc(var(--title-size) * 0.55);
  color: var(--muted);
  margin: 18px 0 4px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.report p { margin: 8px 0; }
.report ul, .report ol { margin: 8px 0 12px; padding-left: 22px; }
.report li { margin: 4px 0; }
.report a { color: var(--primary); text-decoration: none; }
.report a:hover { text-decoration: underline; }
.report table {
  border-collapse: collapse;
  margin: 14px 0 18px;
  font-size: calc(var(--label-size) * 0.95);
  width: 100%;
}
.report th, .report td {
  border-bottom: 1px solid var(--grid);
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
}
.report th {
  background: rgba(37, 99, 235, 0.08);
  color: var(--foreground);
  font-weight: 600;
}
.report tr:hover td { background: rgba(37, 99, 235, 0.04); }
.report code {
  background: rgba(107, 114, 128, 0.12);
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 0.92em;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
}
.report pre {
  background: rgba(107, 114, 128, 0.08);
  padding: 12px 14px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: var(--note-size);
  line-height: 1.45;
}
.report pre code { background: transparent; padding: 0; }
.report blockquote {
  border-left: 3px solid var(--primary);
  margin: 12px 0;
  padding: 4px 14px;
  color: var(--muted);
  background: rgba(37, 99, 235, 0.04);
}
.report img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 18px auto;
  border-radius: 4px;
  border: 1px solid var(--grid);
}
.report .auto-charts {
  margin-top: 36px;
  padding-top: 12px;
  border-top: 1px solid var(--grid);
}
.report .auto-charts figure { margin: 0 0 22px; }
.report .auto-charts figcaption {
  text-align: center;
  font-size: var(--note-size);
  color: var(--muted);
  margin-top: 6px;
}
.missing-assets {
  border: 1px solid var(--warning);
  background: rgba(217, 119, 6, 0.08);
  border-radius: 8px;
  padding: 12px 14px;
  margin: 20px 0;
}
.missing-assets h2 {
  margin-top: 0;
}
.report-footer {
  margin-top: 48px;
  padding-top: 16px;
  border-top: 1px solid var(--grid);
  color: var(--muted);
  font-size: var(--note-size);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}
@media print {
  .report { max-width: none; padding: 24px; }
  .report img { break-inside: avoid; }
  .report table { break-inside: avoid; }
}
@media (max-width: 760px) {
  .artifact-grid,
  .artifact-highlights {
    grid-template-columns: 1fr;
  }
  .artifact-meta {
    grid-template-columns: 1fr;
  }
  .artifact-meta dt {
    font-weight: 700;
  }
}
</style>
</head>
<body>
<main class="report">
<header class="report-header">
<div class="artifact-label">__REPORT_TYPE__</div>
<h1>__TITLE__</h1>
<div class="meta">__META__</div>
</header>
__ARTIFACT_HEADER__
__HIGHLIGHTS__
__BODY__
<footer class="report-footer">
<span>__SOURCE_NOTE__</span>
<span>Built with Marketing Analytics Pack</span>
</footer>
</main>
</body>
</html>
"""


def extract_title_from_markdown(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and len(stripped) > 2:
            return stripped[2:].strip()
    return None


def detect_report_type(source: str, title: str, requested: str) -> str:
    if requested != "auto":
        return requested
    haystack = f"{title}\n{source[:3000]}".lower()
    if "kpi tree" in haystack:
        return "kpi-tree"
    if "metric spec" in haystack:
        return "metric-spec"
    if "clv" in haystack or "customer lifetime value" in haystack:
        return "clv-scenario"
    if "journey measurement" in haystack or "measurement framework" in haystack:
        return "journey-framework"
    if "forecast" in haystack or "baseline comparison" in haystack:
        return "forecast"
    if "mmm" in haystack or "media mix" in haystack:
        return "mmm"
    if "rfm" in haystack or "segment profiles" in haystack:
        return "rfm"
    if "post-mortem" in haystack or "what happened" in haystack:
        return "post-mortem"
    if "executive summary" in haystack:
        return "executive-summary"
    return "generic"


def extract_sections(source: str) -> dict[str, str]:
    matches = list(HEADING_RE.finditer(source))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = _clean_markdown_inline(match.group(2))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        body = source[start:end].strip()
        if body:
            sections[title.lower()] = body
    return sections


def build_highlights(source: str, report_type: str) -> str:
    sections = extract_sections(source)
    wanted = REPORT_TYPE_KEY_SECTIONS.get(report_type, REPORT_TYPE_KEY_SECTIONS["generic"])
    cards: list[str] = []
    for name in wanted:
        body = _find_section(sections, name)
        if not body:
            continue
        snippet = _summarize_markdown(body)
        if not snippet:
            continue
        cards.append(
            '<article class="artifact-card">'
            f'<h3>{_html_escape(name)}</h3>'
            f'<p>{_html_escape(snippet)}</p>'
            '</article>'
        )
    if not cards:
        return ""
    return '<section class="artifact-highlights" aria-label="Key sections">' + "".join(cards[:4]) + "</section>"


def _find_section(sections: dict[str, str], wanted: str) -> str | None:
    key = wanted.lower()
    if key in sections:
        return sections[key]
    for section_key, body in sections.items():
        if key in section_key or section_key in key:
            return body
    return None


def _summarize_markdown(value: str, max_chars: int = 260) -> str:
    lines = []
    for raw in value.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("|") or stripped.startswith("```"):
            continue
        if stripped.startswith(("-", "*")):
            stripped = stripped[1:].strip()
        lines.append(_clean_markdown_inline(stripped))
        if sum(len(line) for line in lines) > max_chars:
            break
    text = " ".join(lines).strip()
    if len(text) > max_chars:
        text = text[: max_chars - 1].rstrip() + "..."
    return text


def _clean_markdown_inline(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip("# ").strip()


def build_artifact_header(config: RunConfig, report_type: str, source_name: str, image_count: int) -> str:
    rows = [
        ("Report type", REPORT_TYPE_LABELS.get(report_type, "Marketing Analysis")),
        ("Audience", config.audience or "General stakeholder"),
        ("Source", config.source_label or source_name),
        ("Data source", config.data_source or "See report body"),
        ("Style", config.style_name),
        ("Charts", f"{image_count} embedded"),
    ]
    if config.previous_report:
        rows.append(("Previous", config.previous_report))
    rows.append(("Created", dt.date.today().isoformat()))
    meta = "".join(
        f"<dt>{_html_escape(label)}</dt><dd>{_html_escape(value)}</dd>"
        for label, value in rows
    )
    return (
        '<section class="artifact-grid">'
        '<div class="artifact-panel">'
        '<h2>Shareable HTML Artifact</h2>'
        '<p>This static report packages the analysis narrative, tables, charts, and caveats into a single browser-openable file. No backend or portal is required.</p>'
        '<p class="share-note">Share by attaching the HTML file, uploading it to Drive or SharePoint, or exporting it to PDF from the browser.</p>'
        '</div>'
        '<aside class="artifact-panel">'
        '<h2>Report Metadata</h2>'
        f'<dl class="artifact-meta">{meta}</dl>'
        '</aside>'
        '</section>'
    )


def build_missing_assets_warning(missing: list[str]) -> str:
    if not missing:
        return ""
    items = "".join(f"<li>{_html_escape(src)}</li>" for src in missing)
    return (
        '<section class="missing-assets">'
        '<h2>Missing Referenced Assets</h2>'
        '<p>The report references image paths that were not found in the image directory. The rest of the artifact was still built.</p>'
        f'<ul>{items}</ul>'
        '</section>'
    )


def _html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_report(config: RunConfig) -> int:
    import markdown as md

    if config.input_path is None:
        source = sys.stdin.read()
        source_name = "stdin"
    else:
        if not config.input_path.exists():
            print(f"Input file not found: {config.input_path}", file=sys.stderr)
            return 2
        source = config.input_path.read_text(encoding="utf-8")
        source_name = config.input_path.name

    title = (
        config.title
        or extract_title_from_markdown(source)
        or Path(source_name).stem.replace("-", " ").replace("_", " ").title()
    )
    report_type = detect_report_type(source, title, config.report_type)

    tokens = load_style_tokens(config.style_name)
    palette_list = tokens["palette"] or ["#2563eb"]
    primary = tokens["brand"].get("primary_hex") or palette_list[0]
    font_family = tokens["brand"].get("font_family") or "DejaVu Sans"

    body_html = md.markdown(
        source,
        extensions=["tables", "fenced_code", "sane_lists", "toc"],
        output_format="html5",
    )

    image_map = discover_images(config.images_dir)
    body_html, missing, used = inline_images(body_html, image_map)
    body_html = append_unreferenced_images(body_html, image_map, used)
    body_html = build_missing_assets_warning(missing) + body_html

    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    meta_bits = [
        dt.date.today().isoformat(),
        REPORT_TYPE_LABELS.get(report_type, "Marketing Analysis"),
        f"style: {config.style_name}",
    ]
    if config.images_dir:
        meta_bits.append(f"images: {len(image_map)} embedded")
    meta = "  |  ".join(meta_bits)
    artifact_header = build_artifact_header(config, report_type, source_name, len(image_map))
    highlights = build_highlights(source, report_type)

    replacements = {
        "__TITLE__": _html_escape(title),
        "__META__": _html_escape(meta),
        "__REPORT_TYPE__": _html_escape(REPORT_TYPE_LABELS.get(report_type, "Marketing Analysis")),
        "__ARTIFACT_HEADER__": artifact_header,
        "__HIGHLIGHTS__": highlights,
        "__BODY__": body_html,
        "__PRIMARY__": primary,
        "__FOREGROUND__": tokens["chart"].get("foreground", "#111827"),
        "__MUTED__": tokens["chart"].get("muted", "#6b7280"),
        "__BACKGROUND__": tokens["chart"].get("background", "#ffffff"),
        "__GRID__": tokens["chart"].get("grid", "#e5e7eb"),
        "__POSITIVE__": tokens["chart"].get("positive", "#16a34a"),
        "__NEGATIVE__": tokens["chart"].get("negative", "#dc2626"),
        "__WARNING__": tokens["chart"].get("warning", "#d97706"),
        "__FONT_FAMILY__": font_family,
        "__TITLE_SIZE__": str(int(tokens["typography"].get("title_size", 16) * 2)),
        "__LABEL_SIZE__": str(tokens["typography"].get("label_size", 10) * 1.5),
        "__NOTE_SIZE__": str(max(int(tokens["typography"].get("note_size", 8) * 1.4), 12)),
        "__SOURCE_NOTE__": _html_escape(
            tokens["layout"].get("source_note", "Source: analysis generated in Claude")
        ),
    }

    html = HTML_TEMPLATE
    for key, value in replacements.items():
        html = html.replace(key, str(value))
    config.output_path.write_text(html, encoding="utf-8")

    print(f"Wrote {config.output_path} ({len(html):,} bytes, {len(image_map)} images embedded)")
    if missing:
        print(
            f"\nWarning: {len(missing)} <img> src(s) could not be resolved:",
            file=sys.stderr,
        )
        for src in missing:
            print(f"  - {src}", file=sys.stderr)
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    config = parse_args(argv)
    _ensure_deps(config.auto_install)
    return build_report(config)


if __name__ == "__main__":
    sys.exit(main())
