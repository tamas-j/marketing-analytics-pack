---
description: Choose the right forecasting approach for a marketing metric, business question, data history, seasonality, and available drivers.
argument-hint: "<metric, forecast horizon, date grain, history length, seasonality, drivers, decision>"
---

# Forecast Method

Use this command when the user needs to choose an appropriate forecasting method before building a forecast.

Use skill: "forecast-method-selector"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the forecasting decision and target metric.
2. Ask for the minimum missing context:
   - forecast horizon
   - date grain
   - history length
   - known seasonality
   - business events, promotions, campaigns, or holidays
   - available external drivers
3. Check forecast readiness:
   - regular time series
   - enough history
   - missing periods and outliers
   - seasonality and trend
   - future-known drivers
4. Recommend the simplest useful method:
   - naive baseline
   - moving average
   - seasonal naive
   - Prophet
   - regression with drivers
   - scenario forecast
5. Define validation and caveats.

## Output Format

Return:

1. Forecast question
2. Recommended method
3. Why it fits
4. Data requirements
5. Validation plan
6. Caveats
7. Next step

## Guardrails

- Do not recommend Prophet before checking whether a simpler baseline is enough.
- Do not forecast without a regular date grain.
- Do not include drivers unless their future values are known or can be scenarised.
- Treat campaign, pricing, and stockout changes as structural risks.
