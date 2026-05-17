# MMM Runner Example

## Prompt

```text
/mmm-runner Prepare a Google Meridian MMM spec for weekly ecommerce revenue with paid search, paid social, TV, affiliates, promotions, price index, stockout flag, and holiday controls.
```

## Example Output

## Google Meridian MMM Runner Spec

### Model Scope

Weekly national-level MMM for ecommerce revenue, using Google Meridian as the implementation target. The model should estimate paid media contribution while controlling for promotions, price, stockouts, and holidays.

### Input Schema

| Field | Role | Grain | Notes |
|---|---|---|---|
| `week_start` | time index | weekly | regular weekly series |
| `revenue` | outcome | weekly | business revenue, not platform-attributed |
| `paid_search_spend` | media | weekly | spend |
| `paid_social_spend` | media | weekly | spend |
| `tv_spend` | media | weekly | spend |
| `affiliate_spend` | media | weekly | spend |
| `promo_flag` | control | weekly | major promotional weeks |
| `price_index` | control | weekly | pricing changes |
| `stockout_flag` | control | weekly | availability issue |
| `holiday_flag` | control | weekly | calendar effect |

### Assumptions and Priors

- TV likely has longer lag than paid search.
- Paid search may include demand capture and should be interpreted carefully.
- Promotions and stockouts need controls to avoid media over-credit.
- Channel correlations should be reviewed before modelling.

### Execution Checklist

1. Confirm weekly table has no missing dates.
2. Reconcile revenue to finance or ecommerce reporting.
3. Check spend variation and channel correlations.
4. Fit baseline model in Meridian.
5. Review diagnostics, uncertainty, and response curves.
6. Interpret results with `/mmm-result-interpreter`.

### Expected Outputs

- contribution by channel
- ROI and marginal ROI
- response curves
- uncertainty intervals
- fit diagnostics
- budget scenario recommendations

### Validation Checks

- Holdout or validation period fit.
- Residual spikes around stockouts and promo periods.
- Plausible channel lag and saturation.
- Contribution estimates aligned with known experiments where available.

### Caveats

- This is a runner spec, not a completed model run.
- Budget recommendations should wait for diagnostics and uncertainty review.
