# Style Picker Example

## Prompt

```text
/style custom brand primary #c026d3, font Inter, no logo, executive tone
```

## Example Output

### Style Selection

You picked the **custom** style, branded from the executive template.

### Brand Settings Applied

| Field | Value |
|---|---|
| `primary_hex` | `#c026d3` |
| `logo_path` | *(left blank)* |
| `font_family` | `Inter` |

### What Changed

`lib/styles/custom.yaml` now carries your brand block. The rest of the file
remains structurally aligned with `default.yaml` so `lib/visualize.py`
continues to read it cleanly.

### Active Style

`custom` (cloned from `executive`).

### How To Use It

Future chart code in the pack will call:

```python
from visualize import load_style, palette, matplotlib_rc_params

style = load_style("custom")
colors = palette(style)
plt.rcParams.update(matplotlib_rc_params(style))
```

That returns a palette led by your `#c026d3` primary, Inter typography,
and the executive base tones for everything else (slate foreground,
restrained grid, deep teal sequential ramp).

### Reminder

- Re-run `/style` any time you want to switch base style or change brand fields.
- Hand-edits to `custom.yaml` are fine, but keep the top-level keys
  (`name`, `description`, `brand`, `chart`, `palette`, `typography`, `layout`)
  intact so the reader doesn't break.
- `default.yaml` and `executive.yaml` are read-only templates; only
  `custom.yaml` should be modified.
