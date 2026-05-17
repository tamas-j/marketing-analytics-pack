---
name: forecast-method-selector
description: Use when selecting a forecasting method for marketing, revenue, demand, traffic, conversion, retention, or campaign metrics based on horizon, history, seasonality, drivers, and decision needs.
---

# Forecast Method Selector

This skill chooses a practical forecasting method. It favours simple baselines unless the user's data and decision justify a more complex model.

## Required Inputs

Ask only for what is missing:

- Target metric.
- Forecast horizon.
- Date grain.
- History length.
- Known seasonality.
- Promotions, holidays, campaigns, stockouts, pricing, or other events.
- External drivers and whether future driver values are known.
- Decision the forecast will support.

## Method Guide

| Method | Best for | Requirements | Watch-out |
|---|---|---|---|
| Naive baseline | quick benchmark | recent observed values | weak with trend/seasonality |
| Moving average | noisy stable series | enough recent history | lags trend changes |
| Seasonal naive | strong repeated seasonality | at least one full seasonal cycle | fails after structural breaks |
| Prophet | trend + seasonality + holidays | regular time series and enough history | not magic; validate against baselines |
| Regression with drivers | forecast depends on known inputs | future-known drivers | driver scenarios can dominate result |
| Scenario forecast | planning under uncertainty | assumptions | not a statistical prediction |

## Output Template

```markdown
## Forecast Method Recommendation

### Forecast Question
<target, horizon, and decision>

### Recommended Method
<method>

### Why This Fits
<rationale>

### Data Requirements
- <field>

### Validation Plan
- <backtest or baseline comparison>

### Caveats
- <risk>

### Next Step
<runner or data fix>
```

## Guardrails

- Always compare against a simple baseline.
- Do not use future-unknown campaign or spend variables as if they are known.
- Do not forecast through a major business model change without scenario caveats.
- Do not overstate precision; provide ranges where possible.
