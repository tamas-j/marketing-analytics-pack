---
description: Choose or customize the shared visual style used by Marketing Analytics Pack outputs.
argument-hint: "<default|executive|custom|brand primary color/logo/font>"
---

# Style

Use this command to set the visual style for charts and analytical outputs across the pack.

Use skill: "style-picker"
Use skill: "data-visualization"

## Workflow

1. Ask whether the user wants `default`, `executive`, or a custom branded style.
2. If they choose `default` or `executive`, explain that future runner and report commands should pass `--style <style-name>`.
3. If they choose custom, gather only the fields they know:
   - primary brand color as a hex code
   - logo path, if available
   - preferred font family, if available
   - whether the tone should be everyday or executive
4. For custom styles, run `python skills/style-picker/scripts/set_style.py` with the chosen base and supplied brand fields. Add `--preview <path>` if the user wants a sample chart.
5. Confirm the active style name and remind future commands to pass `--style custom`.

## Non-Technical Prompt

If the user is unsure, say:

> Pick `default` for clear everyday charts, `executive` for board-style outputs, or `custom` if you have a brand color you want reflected in the charts.

## Guardrails

- Do not redesign charts inside this command.
- Do not add dependencies.
- Keep `custom.yaml` valid YAML.
- Use hex colors in the form `#2563eb`.
- Leave `logo_path` blank unless the user provides a usable local or project-relative path.
- Do not edit `default.yaml` or `executive.yaml`; only `custom.yaml` should be modified.
