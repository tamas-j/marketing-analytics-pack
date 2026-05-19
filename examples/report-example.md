# Report Example

## Prompt

```text
/report Package the RFM run I just did as HTML I can email to my VP.
```

## Example Output

## Report packaged

### Source

`examples/rfm-segment/output/summary.md` plus the two PNG charts from the same folder (`segment_sizes.png`, `rf_scatter.png`). Pulled from the `/rfm-segment` execution run earlier in the conversation.

### Format

`html` — single self-contained file. Both charts are embedded as base64 data URIs, so the file opens correctly even after you've emailed it.

### File

`report-out/rfm-segmentation-2026-05-19.html`  ·  216 KB

### How to share

Open in any browser to preview, then drag-and-drop into Gmail / Outlook / Slack as an attachment, or upload to your team's Drive / SharePoint. Recipients don't need anything installed.

### Want this in another format?

Say `/report pptx` if you want a slide deck for the VP meeting itself — one slide per segment-profile insight, charts as the visual. The HTML is the artifact you send; the deck is the artifact you present.

---

## Command (under the hood)

```bash
python skills/report-builder/scripts/build_html_report.py \
  --input examples/rfm-segment/output/summary.md \
  --images examples/rfm-segment/output \
  --output report-out/rfm-segmentation-2026-05-19.html \
  --title "RFM segmentation — Q4 review" \
  --style default \
  --auto-install
```

## What the HTML looks like

- Header with the title in brand primary, today's date, and a "Built with Marketing Analytics Pack" footer.
- The `summary.md` narrative rendered: segment-profile table, "Top segment by total revenue" callout, caveats.
- A "Charts" section at the bottom with both PNGs as captioned figures (auto-appended because the `summary.md` lists them in the Outputs table but doesn't use `<img>` tags — the script surfaces them anyway).
- All colours / typography pulled from `lib/styles/default.yaml`, so the report matches the chart visuals.

## Variations

### Stakeholder deck instead of an HTML

```text
/report pptx --title "Q4 lifecycle segmentation — exec review"
```

Claude routes to the runtime `pptx` skill, takes the same `summary.md` + chart PNGs, and lays out one slide per top-level heading (Segment profiles, Top segment, Caveats, Charts).

### Narrative Word doc for the comms team

```text
/report docx
```

(Common after `/campaign-post-mortem` or `/churn-driver-narrative`.) Claude routes to the runtime `docx` skill so the comms team gets a Word doc they can edit, with charts inline and tables preserved.

### Brand-styled HTML for an external partner

If the user has previously run `/style` and set `custom.yaml` with their brand primary colour, logo, and font:

```text
/report html --style custom --title "Partner readout: lifecycle program review"
```

The HTML adopts those brand tokens for the header rule, headings, table header tint, and link colour — same brand the charts already use.

## Guardrails reminder

- The report only contains content the source skill produced. No new analysis is invented.
- Every chart from the source folder is preserved; if a referenced chart is missing, the script warns rather than silently drops it.
- Don't pipe raw customer rows from sample data into an externally-shared report without explicit go-ahead.
