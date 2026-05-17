---
description: Choose or customize the shared visual style used by Marketing Analytics Pack outputs.
argument-hint: "<default|executive|custom|brand primary color/logo/font>"
---

# Style

Use this command to set the visual style for charts and analytical outputs across the pack.

Use skill: "data-visualization"

## Workflow

1. Ask whether the user wants `default`, `executive`, or a custom branded style.
2. If they choose `default` or `executive`, explain that future chart code should call `load_style("<style-name>")`.
3. If they choose custom, gather only the fields they know:
   - primary brand color as a hex code
   - logo path, if available
   - preferred font family, if available
   - whether the tone should be everyday or executive
4. Update `lib/styles/custom.yaml` by copying the closest bundled style and changing only the supplied brand fields.
5. Confirm the active style name and remind future commands to use `load_style("custom")`.

## Non-Technical Prompt

If the user is unsure, say:

> Pick `default` for clear everyday charts, `executive` for board-style outputs, or `custom` if you have a brand color you want reflected in the charts.

## Guardrails

- Do not redesign charts inside this command.
- Do not add dependencies.
- Keep `custom.yaml` valid YAML.
- Use hex colors in the form `#2563eb`.
- Leave `logo_path` blank unless the user provides a usable local or project-relative path.
