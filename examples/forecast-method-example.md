# Forecast Method Example

## Prompt

```text
/forecast-method We want to forecast weekly ecommerce revenue for the next 12 weeks. We have three years of weekly revenue, promo flags, holidays, stockout flags, and marketing spend plans.
```

## Example Output

## Forecast Method Recommendation

### Forecast Question

Forecast weekly ecommerce revenue for the next 12 weeks to support trading and marketing planning.

### Recommended Method

Use Prophet with holiday/promotion controls, compared against a seasonal naive baseline.

### Why This Fits

The series has three years of weekly history, so annual seasonality and trend can be estimated. The 12-week horizon is long enough that a moving average may miss seasonal effects, and the available promotion/holiday flags are relevant. Marketing spend plans can be used only if future values are known or treated as scenarios.

### Data Requirements

- week start date
- weekly revenue
- promo flag or promo intensity
- holiday flag
- stockout flag
- planned marketing spend by week, if used as scenario input

### Validation Plan

- Backtest on the most recent 12-week period.
- Compare Prophet against seasonal naive forecast.
- Inspect error by promo and non-promo weeks.

### Caveats

- Stockout weeks can suppress revenue and distort seasonality.
- Future promotions and spend plans must be known or scenarised.
- Forecast is not causal; it should not be used to infer marketing incrementality.

### Next Step

Prepare a Prophet runner spec with `/forecast-runner`.
