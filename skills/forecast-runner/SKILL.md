---
name: forecast-runner
description: Use when scoping or preparing an advanced Prophet forecast run, including input schema, horizon, seasonality, holidays, regressors, validation, expected outputs, and caveats.
---

# Forecast Runner

This skill prepares a Prophet forecast run. In v1 it is a specification workflow, not an automated execution runner. A future advanced runner can install and run Prophet once the plugin adds heavy dependency support.

## Required Inputs

Ask only for what is missing:

- Prepared time series or schema.
- Date field.
- Target metric.
- Forecast horizon.
- Date grain.
- Holiday, promotion, or event fields.
- Regressors and whether future values are known.
- Validation period.

## Prophet Input Shape

Prophet expects:

- `ds`: date column
- `y`: target value

Optional:

- holidays dataframe
- additional regressors with future values
- caps/floors for logistic growth, if justified

## Output Template

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

## Guardrails

- Do not use Prophet as a substitute for causal measurement.
- Do not include regressors whose future values are unknown unless they are scenarios.
- Do not ignore outliers, stockouts, promos, tracking changes, or missing periods.
- Always compare the model against naive or seasonal naive baselines.
