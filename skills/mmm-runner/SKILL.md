---
name: mmm-runner
description: Use when scoping or executing a Google Meridian media mix model — input schema, priors, MCMC settings, validation, ROI, response curves, and styled outputs.
---

# MMM Runner

This skill has two modes:

- **Spec mode** (always available): walk through model scope, input schema, priors, assumptions, validation plan, expected outputs, and interpretation guardrails for a Google Meridian MMM, without running anything.
- **Execution mode** (advanced runner, from v0.2.0): run `scripts/run_mmm.py` to actually fit Meridian (Bayesian MCMC), compute ROI + contribution + response curves, and emit styled charts.

Choose the mode based on whether the user is *planning* an MMM or *running* one. Default to spec mode unless the user has a prepared CSV and asks for outputs.

## Required Inputs

Ask only for what is missing:

- Prepared MMM dataset (CSV) at weekly or daily grain.
- Time column.
- KPI column (revenue or conversions).
- KPI type (`revenue` or `non_revenue`).
- Media exposure columns (use spend columns if no separate exposure proxy is available).
- Media spend columns (defaults to media exposure columns).
- Channel labels (defaults to the media column names).
- Optional control columns (promo flags, holiday flags, seasonality).
- Geo or market structure (current version is national / single-geo).
- MCMC settings (chains / adapt / burnin / keep — defaults are conservative).

## Execution Mode Availability

| Surface | Spec mode | Execution mode |
|---|---|---|
| Claude Code | ✅ | ✅ — Claude can run the script via Bash |
| Cowork | ✅ | ✅ — Claude can run the script via Bash |
| Claude.ai web chat | ✅ | ❌ — no shell access; fall back to spec mode |

If you're not sure whether the active surface supports Bash, ask the user before assuming execution mode. The spec-mode output is always a valid fallback.

## Spec Mode Output Template

```markdown
## Google Meridian MMM Runner Spec

### Model Scope
<scope>

### Input Schema
| Field | Role | Grain | Notes |
|---|---|---|---|
| <field> | <role> | <grain> | <notes> |

### Assumptions and Priors
- <assumption>

### Execution Checklist
1. <step>
2. <step>
3. <step>

### Expected Outputs
- contribution by channel
- ROI or marginal ROI
- response curves
- uncertainty intervals
- fit diagnostics
- budget scenario recommendations

### Validation Checks
- <check>

### Caveats
- <caveat>
```

## Execution Mode

Run from the repo root:

```bash
python skills/mmm-runner/scripts/run_mmm.py \
  --input <csv path> \
  --time-col <time column> \
  --kpi-col <kpi column> \
  --kpi-type revenue|non_revenue \
  --media-cols col1,col2 \
  [--media-spend-cols col1,col2] \
  [--media-channels label1,label2] \
  [--controls col1,col2] \
  [--n-chains 2 --n-adapt 200 --n-burnin 200 --n-keep 400] \
  [--seed 1] \
  [--output-dir <path>] \
  [--style default|executive|custom] \
  [--auto-install]
```

Dependencies are declared in `scripts/requirements.txt` (`google-meridian`, `pandas`, `matplotlib`, `pyyaml`). Meridian pulls TensorFlow + tfp-nightly on first install (~600 MB); always use a virtual environment, especially on PEP 668-managed systems (Ubuntu 23+ / Debian 12+).

### Outputs

| File | Contents |
|---|---|
| `roi_per_channel.csv` | Posterior ROI per channel: mean, P5, P95 |
| `channel_contribution.csv` | Posterior contribution % per channel |
| `response_curves.csv` | Long-format spend multiplier → incremental outcome |
| `roi_per_channel.png` | Horizontal bar chart of ROI with credible intervals, styled via `lib/visualize.py` |
| `response_curves.png` | Multi-line saturation curves per channel |
| `summary.md` | Short human-readable narrative |

## Guardrails

- Do not create fake model results — only quote numbers that come out of an actual run.
- Do not hide uncertainty or identifiability issues. Always present credible intervals alongside the mean.
- Do not model channels that lack meaningful variation without caveats.
- Do not recommend budget moves from a single MMM run without diagnostics, result interpretation, and ideally external incrementality calibration.
- Small MCMC settings (chains=2, keep=400) are fine for demos and exploratory runs; bump `--n-keep` to 1000+ for production interpretation.
- MMM is correlational, not causal — calibrate against geo or holdout incrementality tests where possible.
- Keep Google Meridian as the named implementation target for this pack.
