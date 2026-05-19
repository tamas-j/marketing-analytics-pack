---
description: Package the most recent Marketing Analytics Pack output into a shareable file (HTML, DOCX, PPTX, or PDF).
argument-hint: "<format (html|docx|pptx|pdf) and/or source folder/file, optional title>"
---

# Report

Use this command when the user has just run another Marketing Analytics Pack command and wants the output as a file they can send to a stakeholder.

Use skill: "report-builder"

## Workflow

1. **Identify the source** the user wants to package:
   - If they pointed to a folder (e.g. an advanced-runner output dir) or a markdown file, use it.
   - Otherwise look at the most recent skill output in the conversation. Capture chat output into a temp markdown file if you need to.
   - If there is nothing to package, say so and recommend running `/plan-analysis` first.
2. **Pick the format.** If the user named one, honour it. Otherwise:
   - Default to `html` (single self-contained file, opens in any browser).
   - Prefer `docx` for narrative-heavy outputs (analysis brief, churn-driver narrative, campaign post-mortem, MMM result interpretation).
   - Prefer `pptx` when the user mentions a meeting, exec review, presentation, or share-out.
   - Use `pdf` for formal handoff.
3. **Build the report:**
   - For `html`: run `python skills/report-builder/scripts/build_html_report.py --input <md> --images <dir> --output <path> --title "<title>" --style <style> --report-type <type>`. Pass `--auto-install` on first use if deps aren't installed.
   - For `docx`, `pptx`, `pdf`: use the runtime skill of the same name to convert the markdown + images into the requested format.
4. **Confirm the file.** Tell the user the exact output path, file size, and a one-liner on how to share (open, attach, drop into Slack).
5. **Offer a follow-up format** — many users want both an HTML for themselves and a DOCX or PPTX for the meeting.

## Output Format

Return:

1. `Source` — which skill output was packaged.
2. `Format` — html / docx / pptx / pdf.
3. `File` — absolute path to the file.
4. `How to share` — one-line action.
5. `Want this in another format?` — single offered alternative.

## Examples

- `/report` → packages the most recent skill output as HTML at `report-out/<slug>-<timestamp>.html`.
- `/report pptx` → packages the most recent output as a slide deck for a meeting.
- `/report html --source examples/rfm-segment/output --title "Q4 RFM review"` → packages a runner output folder as a titled HTML report.
- `/report docx` after running `/campaign-post-mortem` → narrative Word document ready for the comms team.

## Guardrails

- Never invent content. The report only contains what the source skill produced.
- Preserve every chart and table the source produced; if an image referenced in the markdown is missing from the images directory, flag it rather than silently dropping it.
- Never bake credentials, PII, or raw customer rows into a public-shareable file without an explicit go-ahead.
- For HTML, always pass `--style` so the report visually matches the chart outputs the user has seen earlier.
- For HTML, pass `--report-type` when the source workflow is known (`kpi-tree`, `metric-spec`, `clv-scenario`, `journey-framework`, `forecast`, `mmm`, `rfm`, `post-mortem`). Use `auto` only when unsure.
- Do not produce all four formats by default — pick one, offer one alternative.
