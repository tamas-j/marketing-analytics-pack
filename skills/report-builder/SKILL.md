---
name: report-builder
description: Use when packaging a Marketing Analytics Pack skill output (markdown summary, charts, CSV exports) into a single shareable file — HTML by default, plus DOCX, PPTX, or PDF on request.
---

# Report Builder

This skill turns whatever a Marketing Analytics Pack command just produced into a file the user can share with a stakeholder. Most of the pack produces markdown in the chat window (KPI tree tables, post-mortem scorecards, RFM segment maps, etc.) and the advanced runners produce a folder of CSVs + PNG charts + `summary.md`. This skill is the packaging layer that turns either into a single shareable artifact.

## Required Inputs

Ask only for what is missing:

- **Source** — one of:
  - the most recent skill output in the conversation (extract from chat history), or
  - a runner output folder (e.g. `examples/rfm-segment/output/`), or
  - a markdown file path the user points to.
- **Format** — `html` (default), `docx`, `pptx`, or `pdf`.
- **Title** — short report title; defaults to the source command or a sensible inferred title.
- **Audience** — optional (analyst, marketer, executive, product owner); shapes tone and which sections get emphasised.
- **Report type** — optional for HTML artifacts: `executive-summary`, `kpi-tree`, `metric-spec`, `clv-scenario`, `journey-framework`, `forecast`, `mmm`, `rfm`, `post-mortem`, or `generic`.
- **Data source / previous report** — optional labels for recurring analysis or stakeholder traceability.
- **Output path** — defaults to `report-out/<slug>-<timestamp>.<ext>`.

If the user runs `/report` without arguments, default to HTML packaging of the most recent skill output in the conversation.

## Format Selection Guide

| Format | Best for | Why |
|---|---|---|
| `html` | Default; anything; quick share via link or attachment | Single self-contained file, embeds images as base64, opens in any browser, brand-styled, no install needed on the recipient side |
| `docx` | Narrative-heavy outputs — analysis briefs, churn-driver narratives, campaign post-mortems, MMM result interpretations | Stakeholder reads text + tables; comments / track changes; pastes into longer reports |
| `pptx` | Stakeholder presentations — KPI tree reviews, segmentation overviews, MMM scorecards, forecast walkthroughs | One headline per slide, chart + commentary, lands in exec meetings |
| `pdf` | Formal handoff, locked content, archive | Recipient can't edit; print-friendly |

If the user has no preference and the output is narrative (no charts), prefer `docx`. If it includes charts, prefer `html` first (then offer pptx/pdf). Never produce all four by default — pick one and offer the others.

## Workflow

1. **Identify the source.** If the user pointed to a folder, use it. Otherwise:
   - Look for the most recent skill output in the conversation.
   - For runner output, that means a `summary.md` plus PNGs in an output dir.
   - For prompt-only skills, that means the markdown the previous command produced in chat — capture it as a temp file.
2. **Confirm the format.** Honour the user's choice; otherwise pick from the Format Selection Guide and tell them why.
3. **Build the report.**
   - **HTML:** run `scripts/build_html_report.py` (see below). Prefer a report type when the source workflow is known so the artifact gets the right metadata label and highlight cards.
   - **DOCX:** use the runtime `docx` skill — pass the markdown source and any image paths.
   - **PPTX:** use the runtime `pptx` skill — one slide per top-level heading is a good default.
   - **PDF:** use the runtime `pdf` skill — convert the HTML if one already exists, otherwise build directly from markdown.
4. **Confirm the output path.** Tell the user where the file landed and how to share it (open the file, attach to email, drop into Slack, etc.).
5. **Offer a follow-up.** If they picked HTML, offer DOCX/PPTX/PDF as a one-step conversion. Many users want both ("file for myself, deck for the meeting").

## HTML Helper

For HTML, prefer the bundled helper over hand-rolling the HTML:

```bash
python skills/report-builder/scripts/build_html_report.py \
  --input <markdown file or - for stdin> \
  --images <directory containing PNGs to embed> \
  --output <output html path> \
  [--title "<report title>"] \
  [--style default|executive|custom] \
  [--report-type auto|executive-summary|kpi-tree|metric-spec|clv-scenario|journey-framework|forecast|mmm|rfm|post-mortem|generic] \
  [--audience "<intended reader>"] \
  [--source-label "<analysis source>"] \
  [--data-source "<dataset or system>"] \
  [--previous-report "<prior report path or label>"] \
  [--auto-install]
```

The helper:

- Reads the markdown with the `markdown` library (auto-installed on first use if missing).
- Embeds every PNG / JPG / SVG it finds in `--images` as a base64 data URI inline in the HTML.
- Applies brand palette / typography from `lib/styles/<style>.yaml` (same source as the chart styles).
- Adds a static artifact header with report type, audience, source, data source, style, chart count, and optional previous-report label.
- Extracts up to four key-section cards from the source markdown based on report type. It does not invent new claims; it only lifts short snippets from existing sections.
- Produces a single self-contained `.html` file the user can open in any browser, attach to email, or drop into a Slack DM.

## HTML Artifact Types

| Report type | Use for | Highlight sections |
|---|---|---|
| `kpi-tree` | KPI tree outputs | Executive Summary, KPI Tree, Diagnostic Questions, Recommended First Analysis |
| `metric-spec` | Metric definition cards | Purpose, Definition, Formula, Caveats and Guardrails, QA Checks |
| `clv-scenario` | CLV planning scenarios | Decision Summary, Scenario Results, Sensitivity Notes, Guardrails and Caveats |
| `journey-framework` | Lifecycle or journey measurement | Journey Summary, Measurement Framework, Measurement Gaps, Recommended First Analysis |
| `forecast` | Forecast runner outputs | Forecast Summary, Baseline Comparison, Caveats, Recommended Next Step |
| `mmm` | MMM readouts | Executive Summary, ROI, Contribution, Response Curves, Caveats |
| `rfm` | RFM runner outputs | Segment Profiles, Top Segment, Activation Recommendations, Caveats |
| `post-mortem` | Campaign or performance reviews | Executive Summary, What Happened, Root Causes, Actions |

Use `auto` if unsure; the helper detects common titles and section names. Use `generic` for one-off markdown that does not match a known workflow.

## DOCX / PPTX / PDF Composition

When the user wants `docx`, `pptx`, or `pdf`:

1. First, make sure you have the markdown + images on disk (run the source-identification step above and save anything that's only in chat to a temp markdown file).
2. Use the runtime `docx` / `pptx` / `pdf` skill in the same Claude session — those skills know how to take markdown + images and produce a clean file.
3. For `pptx`: a good default is one slide per top-level heading (`##`), with the heading as the slide title, the immediate prose as speaker notes, any tables as a slide table, and the first relevant image as the slide visual. Don't try to fit a whole post-mortem on one slide.
4. For `pdf`: if you already produced an HTML version, use the runtime `pdf` skill to convert HTML → PDF. Otherwise build directly from markdown.

## Output Template (what to tell the user)

```markdown
## Report packaged

### Source
<which skill output was packaged>

### Format
<html / docx / pptx / pdf>

### File
<absolute path>

### How to share
- <one-liner: open in browser / attach to email / drop into Slack>

### Want this in another format?
<offer of one alternative format>

### Artifact metadata
- Report type: <type>
- Audience: <audience>
- Data source: <source>
- Previous report: <optional>
```

## Guardrails

- Never invent content. The report only contains what the source skill produced; you may rewrite headings for the format, but do not add new analysis or numbers.
- Preserve every chart and table from the source. If a chart is referenced in the markdown but missing from the images directory, flag it rather than silently dropping it.
- Keep stakeholder-shareable formats brand-consistent. The HTML helper enforces this via `lib/styles/`; for DOCX/PPTX, the runtime skill controls visual style and the report just needs to be honest about which charts came from which run.
- Do not embed credentials, PII, or raw customer rows from a sample dataset into a public-shareable file unless the user has explicitly cleared it.
- If the source is empty, ambiguous, or the user has not produced any skill output yet, say so plainly and offer to run one of the front-door commands (`/plan-analysis`, `/kpi-tree`) first.
- Always tell the user the exact file path and how to open / share it. A report nobody can find isn't shareable.
