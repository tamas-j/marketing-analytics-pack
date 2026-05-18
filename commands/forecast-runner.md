---
description: Run a Prophet forecast (spec mode for planning, execution mode via scripts/run_forecast.py for real outputs).
argument-hint: "<prepared time series, target metric, date field, horizon, seasonality, holidays, regressors>"
---

# Forecast Runner

Use this command for a Prophet forecast. It has two modes:

- **Spec mode** (default): plan the forecast — input schema, assumptions, validation plan, expected outputs, caveats.
- **Execution mode**: run `skills/forecast-runner/scripts/run_forecast.py` against a CSV and emit styled forecast / components charts plus baseline comparison.

Default to spec mode unless the user has a CSV ready and asks for outputs.

Use skill: "forecast-runner"
Use skill: "forecast-method-selector"
Use skill: "data-visualization"

## Spec Workflow

1. Confirm the forecast method and decision.
2. Define the input schema:
   - date field
   - target metric
   - date grain
   - optional holidays or regressors
3. Define forecast assumptions:
   - horizon
   - seasonality
   - outlier handling
   - known events
   - train/test split
4. Produce a Prophet runner checklist.
5. Define outputs:
   - forecast table
   - uncertainty intervals
   - baseline comparison
   - component plots
   - caveats and interpretation

### Spec Output Format

Return:

1. Forecast scope
2. Input schema
3. Assumptions
4. Execution checklist
5. Validation plan
6. Expected outputs
7. Caveats

## Execution Workflow

1. Confirm the CSV path, date column, target column, frequency, and horizon with the user.
2. Confirm any holidays column and extra regressors.
3. Confirm whether to backtest (`--validate`).
4. Run `python skills/forecast-runner/scripts/run_forecast.py` with the chosen flags. Pass `--auto-install` if Prophet is not yet installed in the user's environment.
5. Read `summary.md` from the output directory and present the headline forecast + baseline comparison to the user.
6. Show `forecast.png` and `components.png` inline if the surface supports it.

### Example

```bash
python skills/forecast-runner/scripts/run_forecast.py \
  --input examples/data/mmm-weekly.csv \
  --date-col week_start \
  --target-col revenue \
  --freq W \
  --horizon 13 \
  --holidays-col holiday \
  --regressors paid_search_spend,paid_social_spend \
  --validate \
  --output-dir examples/forecast-runner/output \
  --style default
```

## Guardrails

- In spec mode: do not pretend the forecast has run unless actual outputs are provided.
- In execution mode: always include `--validate` unless the user explicitly opts out — Prophet should be compared against a naive baseline before being trusted.
- Do not include future-unknown regressors without scenario assumptions.
- If `summary.md` shows the naive baseline beating Prophet, surface that prominently.
