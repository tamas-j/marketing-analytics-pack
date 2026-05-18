---
name: forecast-runner
description: Use when scoping or executing a Prophet forecast — input schema, horizon, seasonality, holidays, regressors, validation, baselines, and styled outputs.
---

# Forecast Runner

This skill has two modes:

- **Spec mode** (always available): walk through input schema, assumptions, validation plan, expected outputs, and caveats for a Prophet forecast, without running anything.
- **Execution mode** (advanced runner, from v0.2.0): run `scripts/run_forecast.py` to actually fit Prophet, compare against naive baselines, and emit styled forecast / components charts.

Choose the mode based on whether the user is *planning* a forecast or *running* one. Default to spec mode unless the user has a prepared CSV and asks for outputs.

## Required Inputs

Ask only for what is missing:

- Prepared time series (CSV with one date column + one target column).
- Date field.
- Target metric.
- Forecast horizon (number of periods).
- Frequency: `D` (daily), `W` (weekly), `M` (monthly), `Q`, `Y`.
- Holiday / promotion / event fields (optional binary 0/1 column).
- Regressors and whether future values are known (optional comma-separated list).
- Validation period (defaults to last 20% of the series when validation is requested).

## Prophet Input Shape

Prophet expects:

- `ds`: date column
- `y`: target value

Optional:

- holidays dataframe (built automatically from a 0/1 column)
- additional regressors (future values default to the trailing 4-period mean)
- caps/floors for logistic growth, if justified

## Spec Mode Output Template

```markdown
## Prophet Forecast Runner Spec

### Forecast Scope
<metric, horizon, grain, and decision>

### Input Schema
| Field | Prophet role | Notes |
|---|---|---|
| <field> | <role> | <notes> |

### Assumptions
- <assumption>

### Execution Checklist
1. <step>
2. <step>
3. <step>

### Validation Plan
- <baseline and backtest>

### Expected Outputs
- forecast table
- upper/lower intervals
- baseline comparison
- trend/seasonality components
- caveat summary

### Caveats
- <caveat>
```

## Execution Mode Availability

| Surface | Spec mode | Execution mode |
|---|---|---|
| Claude Code | ✅ | ✅ — Claude can run the script via Bash |
| Cowork | ✅ | ✅ — Claude can run the script via Bash |
| Claude.ai web chat | ✅ | ❌ — no shell access; fall back to spec mode |

If you're not sure whether the active surface supports Bash, ask the user before assuming execution mode. The spec-mode output is always a valid fallback.

## Execution Mode

Run from the repo root:

```bash
python skills/forecast-runner/scripts/run_forecast.py \
  --input <csv path> \
  --date-col <date column> \
  --target-col <target column> \
  --freq <D|W|M|Q|Y> \
  --horizon <int> \
  [--holidays-col <0/1 column>] \
  [--regressors col1,col2] \
  [--validate] \
  [--validation-fraction 0.2] \
  [--seasonality-mode additive|multiplicative] \
  [--output-dir <path>] \
  [--style default|executive|custom] \
  [--auto-install]
```

Dependencies are declared in `scripts/requirements.txt`. Install them first with `pip install -r skills/forecast-runner/scripts/requirements.txt`, or pass `--auto-install` to let the script install them on first use. Prophet pulls cmdstanpy and downloads a CmdStan toolchain on first import, so the initial install takes a few minutes.

### Outputs

| File | Contents |
|---|---|
| `forecast.csv` | `ds, yhat, yhat_lower, yhat_upper` for the horizon |
| `forecast.png` | Actuals + forecast line + 80% confidence interval, styled via `lib/visualize.py` |
| `components.png` | Prophet trend / weekly / yearly decomposition |
| `baselines.csv` | MAPE / MAE / RMSE for Prophet vs naive vs seasonal-naive (when `--validate` is set) |
| `summary.md` | Short human-readable narrative |

## Guardrails

- Do not use Prophet as a substitute for causal measurement.
- Do not include regressors whose future values are unknown unless they are scenarios.
- Do not ignore outliers, stockouts, promos, tracking changes, or missing periods.
- Always compare the model against naive and seasonal-naive baselines (`--validate`).
- If Prophet beats neither baseline, surface that prominently rather than burying it.
