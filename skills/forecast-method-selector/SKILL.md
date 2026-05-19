---
name: forecast-method-selector
description: Use when selecting a forecasting method for marketing, revenue, demand, traffic, conversion, retention, or campaign metrics based on horizon, history, seasonality, drivers, and decision needs.
---

# Forecast Method Selector

This skill picks a practical forecasting method. It favours simple baselines unless the user's data and decision justify a more complex model. The default assumption is that a naive or seasonal-naive baseline is good enough; the burden of proof sits with anything fancier.

The skill is also opinionated about a second decision the user usually skips: which **error metric** to use. The right method depends on the right metric, and most "Prophet was bad" complaints turn out to be MAPE-on-near-zero series.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive the recommendation.

1. **History length and grain.** How many observations, at what frequency (daily / weekly / monthly)? More than two full seasonal cycles is the rough threshold for trusting seasonal estimates.
2. **Forecast horizon and decision.** How far ahead, and what decision does the forecast support? Budget planning, capacity, hiring, executive expectation-setting, and trading look very different.
3. **Series shape.** Smooth and growing, seasonal, intermittent (lots of zeros), highly campaign-driven, or a mix?
4. Known events: promotions, holidays, launches, stockouts, pricing changes, tracking changes.
5. External drivers: spend, weather, macro, search trends — and whether their future values are known.
6. Hierarchy: are you forecasting total only, or total + channels / regions / products that must reconcile?
7. Tolerance for uncertainty intervals vs single-number commitments.

## Method Guide

| Method | Best for | Requirements | Watch-out |
|---|---|---|---|
| Naive baseline | quick benchmark; very short horizon | recent observed values | weak with trend / seasonality |
| Moving average | noisy stable series | enough recent history | lags trend changes |
| Seasonal naive | strong repeated seasonality | at least one full seasonal cycle | fails after structural breaks |
| Exponential smoothing (ETS) | smooth series with trend + seasonality | regular series, ~2 cycles | brittle with regime changes |
| Prophet | trend + seasonality + holidays | regular time series, ~2 cycles, enough history | not magic; validate against baselines |
| ARIMA / SARIMA | stationary series, technical user | clean regular data | overfitting; brittle |
| Regression with drivers | forecast depends on known future inputs | future-known drivers | driver scenarios can dominate result |
| Hierarchical reconciliation | total + sub-totals must add up | per-level forecasts | tooling: `hts`, `MinT` reconciliation |
| Intermittent demand (Croston / TSB) | sparse series with many zeros | event log | many marketing series are not actually intermittent |
| Scenario forecast | planning under uncertainty | assumptions | not a statistical prediction |

## Decision Tree

Work through these in order. Stop at the first match.

1. **Is the series intermittent (more than ~30% of periods are zero)?**
   → Recommend **Croston / TSB** or roll up to a less granular grain. Prophet and ETS perform badly here.
2. **Is the horizon ≤ 1 period and the user just needs a number for tomorrow / next week?**
   → Recommend a **naive or seasonal-naive baseline**. Anything more is over-engineering for that horizon.
3. **Do you have less than two full seasonal cycles?**
   → Recommend **seasonal naive + a scenario forecast**. Do not promise a statistical model on this data.
4. **Are the drivers known into the future (e.g., planned spend, scheduled promos)?**
   → Recommend **regression with drivers** as primary, Prophet as a baseline. Scenario the drivers if they're decisions, not data.
5. **Is the series smooth-ish with clear trend and seasonality, no major regime change, ≥2 cycles?**
   → Recommend **Prophet** or **ETS**. Prophet wins when there are explicit holiday effects; ETS is fine otherwise. Always compare against seasonal naive.
6. **Do channels / regions / products need to roll up to a total that reconciles?**
   → Recommend a **hierarchical reconciliation** approach on top of per-level Prophet / ETS forecasts.
7. **Is the decision "what range should we plan for?" rather than "what's the number?"**
   → Recommend a **scenario forecast** (Cautious / Base / Optimistic) backed by the simplest statistical model available. Do not present a single-number forecast.

## Error Metric Guide

Pick the metric before picking the model. The wrong metric makes the wrong model look right.

| Metric | Use when | Avoid when |
|---|---|---|
| MAPE | values are well above zero and roughly comparable across periods | series contains zeros or near-zeros (MAPE explodes); mixing very different scales |
| sMAPE | values can be small but not zero | values are zero |
| WAPE | aggregated forecasts across a mix of scales (e.g., portfolio of products) | you need per-period accuracy |
| MAE | absolute error matters in the same unit as the metric | comparing across series of different scales |
| RMSE | penalising large misses more than small ones is important | the metric is noisy and outliers dominate |
| Pinball loss | the forecast is a quantile / interval, not a point | you only have point forecasts |

Always report against **at least one baseline** (naive and seasonal naive). If the chosen method does not beat both baselines on the chosen metric, recommend falling back to the better baseline.

## Worked Examples

### Example 1: DTC ecommerce, weekly revenue, 12-month horizon

Data: 3 years of weekly revenue, clear annual seasonality (Black Friday + January dip), promos flagged. Decision: annual planning + capacity.

Recommendation: **Prophet with holiday effects and a promo regressor**, validated against seasonal naive on the last 26 weeks. Report MAPE for the trend, and additionally report a Cautious / Base / Optimistic scenario for Q4 because promo plans for next year are not yet finalised. Use **WAPE** if rolling up by product line.

### Example 2: B2B SaaS, monthly pipeline, 6-month horizon, 14 months of history

Data: 14 months of monthly pipeline. One full seasonal cycle barely, with structural growth and a major product launch six months ago.

Recommendation: **seasonal naive + scenario forecast**, not Prophet. The history is too short and the launch is a regime change. State plainly that a statistical model is not yet supportable. Reassess after another year.

### Example 3: Lifecycle email programme, daily sends and clicks, 30-day horizon

Data: 18 months of daily sends and clicks, with campaign-driven spikes (no sends on Sundays for most lists).

Recommendation: **regression with the planned send calendar as a driver**, because future sends are a decision, not a forecast input. Pair with seasonal naive at the weekly grain as a baseline. Do not use Prophet directly — the daily zero-pattern on Sundays will fight the weekly seasonality.

## Anti-Patterns

- **Forecasting through a regime change without scenarios.** Pricing change, repositioning, major launch, tracking switch — the model has no signal for the new regime.
- **Reporting MAPE on a series with zeros.** Each zero divides into a huge percentage error. Use WAPE or MAE instead.
- **Treating planned spend as a "predicted" input.** Spend is a decision; if you regress on planned spend, the forecast becomes a scenario, not a prediction. Label it accordingly.
- **Skipping the baseline comparison.** Prophet "looks reasonable" but loses to seasonal naive. Always run both. The runner enforces this (`--validate`).
- **Daily forecasting when the decision is weekly.** Aggregating up adds noise. Forecast at the grain of the decision.
- **Single-number forecasts for high-uncertainty decisions.** Range or scenario forecasts are more honest and more useful for planning.
- **Promising "we'll forecast and then test against actuals."** Without a baseline, beating actuals is meaningless; with a baseline, the comparison is informative.

## Output Template

```markdown
## Forecast Method Recommendation

### Forecast Question
<target, horizon, and decision>

### Recommended Method
<method, with baselines named>

### Why This Fits
<rationale tied to history length, series shape, and decision>

### Error Metric
<chosen metric and why; baselines to beat>

### Data Requirements
- <field>

### Validation Plan
- <backtest window>
- <baselines (always naive + seasonal naive when applicable)>

### Caveats
- <risk, including the regime / event risks specific to this series>

### Next Step
<runner, data fix, or scenario workshop>
```

## Quality Rubric

- `Strong`: method matches the decision and the data shape, baselines are named, the error metric is defended, caveats name the specific regime risks (not generic "uncertainty exists"), and the next step is concrete.
- `Usable`: a sensible method is chosen, but baselines or error metric are left implicit.
- `Needs revision`: Prophet recommended on <2 cycles of history; MAPE recommended on a zero-heavy series; single-number forecast for a decision that needs a range; no baseline comparison.

## Guardrails

- Always compare against a simple baseline. If the model loses, surface that prominently.
- Do not use future-unknown campaign or spend variables as if they are known.
- Do not forecast through a major business-model change without scenario caveats.
- Do not overstate precision; provide ranges where the decision warrants it.
- Do not pick MAPE without checking whether the series can be near zero.
- When the recommendation is Prophet, route to `/forecast-runner` for execution.
- When the decision is causal ("did this drive lift?"), this is not a forecasting question — route to `/incrementality-test-designer`.
