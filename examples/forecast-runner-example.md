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

---

## Execution Mode Example (v0.2.0)

### Prompt

```text
/forecast-runner Run a Prophet forecast on examples/data/mmm-weekly.csv. Target is revenue, date column is week_start, horizon 13 weeks. Use holiday as a holiday column and paid_search_spend + paid_social_spend as regressors. Backtest the last 20%.
```

### Command

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

### Example Output

#### `summary.md`

```markdown
# Forecast summary

- Input: `examples/data/mmm-weekly.csv`
- Target: `revenue` (96 historical rows)
- Frequency: `W` — horizon: 13 periods
- Holidays: `holiday`
- Regressors: `paid_search_spend`, `paid_social_spend`
- Seasonality mode: `additive`

## Headline forecast

Last horizon point (2026-02-01): **84,964** (80% interval 75,115 – 95,678)

## Backtest scores (lower is better)

| Model              |  MAPE |       MAE |      RMSE |
|--------------------|------:|----------:|----------:|
| Prophet            |  7.7% |   6,890.3 |   9,239.5 |
| Naive (last value) | 17.6% |  14,455.6 |  16,057.8 |
| Seasonal naive     | 13.8% |  12,184.4 |  15,610.7 |

Lowest RMSE on the holdout: **Prophet**.
```

#### Files written

| File | Contents |
|---|---|
| `forecast.csv` | 13 rows of `ds, yhat, yhat_lower, yhat_upper` |
| `forecast.png` | Actuals + forecast line + 80% interval, styled via `lib/visualize.py` |
| `components.png` | Prophet trend / weekly / yearly decomposition |
| `baselines.csv` | Prophet vs naive vs seasonal-naive metrics on the holdout |
| `summary.md` | The narrative above |

### How to read this

- Prophet beat both baselines on every metric (MAPE 7.7% vs 13.8% seasonal naive vs 17.6% naive). Trust the forecast more than a flat trend, but still inspect `components.png` before planning around it.
- Holiday weeks are explicitly modelled via the `holiday` column. Promo or stockout weeks should be added the same way for production use.
- Future regressor values (paid search, paid social) are filled with the trailing 4-week mean. For a scenario forecast (e.g. "what if we cut paid search 30%?"), edit the regressor column in the CSV before running, or extend the script to take a scenario file.
- Run with `--auto-install` the first time. Prophet pulls cmdstanpy and downloads CmdStan on first import; expect a few minutes.
