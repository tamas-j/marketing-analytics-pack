---
description: Prepare a Prophet forecast runner spec with input schema, assumptions, validation, outputs, and interpretation guardrails.
argument-hint: "<prepared time series, target metric, date field, horizon, seasonality, holidays, regressors>"
---

# Forecast Runner

Use this command to prepare or specify a Prophet forecast. In v1 this is an advanced-runner planning workflow; automated Prophet execution is deferred until the heavy dependency runner is added.

Use skill: "forecast-runner"
Use skill: "forecast-method-selector"
Use skill: "data-visualization"

## Workflow

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

## Output Format

Return:

1. Forecast scope
2. Input schema
3. Assumptions
4. Execution checklist
5. Validation plan
6. Expected outputs
7. Caveats

## Guardrails

- Do not pretend the forecast has run unless actual outputs are provided.
- Keep this as a runner spec until the Prophet advanced runner exists.
- Include a baseline comparison.
- Do not include future-unknown regressors without scenario assumptions.
