---
name: style-picker
description: Use when selecting default, executive, or custom visual styling for Marketing Analytics Pack charts and reports, including brand color, logo path, font, and preview guidance.
---

# Style Picker

This skill sets the visual style that Marketing Analytics Pack outputs should use. It keeps brand customization small and predictable: choose a base style, update only the brand fields in `lib/styles/custom.yaml`, then tell future commands which style name to pass.

## Required Inputs

Ask only for what is missing:

- Base style: `default`, `executive`, or `custom`.
- Primary brand color as a hex code, if custom.
- Logo path, if the user wants a logo referenced in outputs.
- Font family, if the user has one.
- Tone: everyday analysis or executive stakeholder output.
- Whether to create a preview chart.

If the user is unsure, recommend:

- `default` for everyday analysis.
- `executive` for board-style or senior stakeholder outputs.
- `custom` when they have a brand color, logo, or font to reflect.

## Style Selection Method

1. Decide whether the user needs a bundled style or a custom style.
2. If bundled, tell them to pass `--style default` or `--style executive` to runner/report commands.
3. If custom, pick the nearest base:
   - everyday tone -> `default`
   - executive tone -> `executive`
4. Validate brand fields:
   - color must be `#` plus six hex characters
   - logo path can be blank, relative, or absolute
   - font can be any installed font name, but `DejaVu Sans` is the safe fallback
5. Use `scripts/set_style.py` to update `lib/styles/custom.yaml`.
6. If requested, generate a preview PNG so the user can inspect the result.
7. Confirm the active style and exact command flag to use next.

## Safe Update Command

Prefer the bundled helper over hand-editing YAML:

```bash
python skills/style-picker/scripts/set_style.py \
  --base executive \
  --primary "#c026d3" \
  --font "Inter" \
  --clear-logo \
  --preview docs/screenshots/custom-style-preview.png
```

For default/executive selection without customization, do not modify files. Just tell the user which style to pass:

```bash
--style executive
```

## Output Template

```markdown
## Style Selection

### Active Style
<default / executive / custom>

### Brand Settings
| Field | Value |
|---|---|
| Base style | <default / executive> |
| Primary color | <hex or inherited> |
| Logo path | <path or blank> |
| Font family | <font> |

### How To Use It
Pass `--style <style>` to runner and report commands.

### Preview
<path, if generated>
```

## Guardrails

- Do not redesign chart patterns inside this skill.
- Do not edit `default.yaml` or `executive.yaml`; only update `custom.yaml`.
- Do not accept short hex codes like `#fff`; normalize only six-character hex codes.
- Do not claim a font is installed unless a preview render succeeds.
- Keep `custom.yaml` structurally aligned with the bundled style files.
- Tell the user that style choice is explicit: advanced runners and `/report` need `--style custom` unless the command already says otherwise.
