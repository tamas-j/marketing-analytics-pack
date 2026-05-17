# Forecast Runner Example

## Prompt

```text
/forecast-runner Prepare a Prophet runner spec for weekly ecommerce revenue with week_start, revenue, promo_flag, holiday_flag, stockout_flag, and planned_paid_spend. Horizon is 12 weeks.
```

## Example Output

## Prophet Forecast Runner Spec

### Forecast Scope

Forecast weekly ecommerce revenue for the next 12 weeks to support trading and marketing planning.

### Input Schema

| Field | Prophet role | Notes |
|---|---|---|
| `week_start` | `ds` | weekly date |
| `revenue` | `y` | target metric |
| `holiday_flag` | holiday/control | known future calendar |
| `promo_flag` | regressor/scenario | use only if future promo plan is known |
| `stockout_flag` | outlier/control | review before modelling future |
| `planned_paid_spend` | regressor/scenario | use as scenario input, not known truth |

### Assumptions

- Weekly seasonality is less important than yearly seasonality at weekly grain.
- Promo weeks may lift revenue and should be handled explicitly.
- Stockout weeks may need adjustment or flags to avoid under-forecasting demand.
- Paid spend should be modelled only if future plans are available or scenario-based.

### Execution Checklist

1. Rename `week_start` to `ds` and `revenue` to `y`.
2. Confirm no missing weeks.
3. Flag or adjust stockout outliers.
4. Define holidays and promo regressors.
5. Fit Prophet and seasonal naive baseline.
6. Backtest on the most recent 12 weeks.
7. Export forecast table and interval chart.

### Validation Plan

- Compare Prophet MAE/MAPE against seasonal naive.
- Inspect errors around promo, holiday, and stockout weeks.
- Check whether forecast intervals are credible for planning.

### Expected Outputs

- 12-week forecast table.
- Upper and lower intervals.
- Forecast chart.
- Baseline comparison.
- Trend/seasonality component readout.

### Caveats

- This is a runner spec, not an executed forecast.
- Future campaign and promo assumptions should be versioned as scenarios.
- Forecast accuracy may degrade if product availability or pricing changes.
