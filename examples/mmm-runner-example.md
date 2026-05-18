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

---

## Execution Mode Example (v0.2.0)

### Prompt

```text
/mmm-runner Run a Google Meridian MMM on examples/data/mmm-weekly.csv. KPI is revenue, weekly grain. Media channels are paid_search_spend and paid_social_spend, controls are promo_active and holiday.
```

### Command

```bash
# One-time setup (use a venv so TensorFlow / tfp-nightly install cleanly)
python3 -m venv .venv
source .venv/bin/activate
pip install -r skills/mmm-runner/scripts/requirements.txt

# Run
python skills/mmm-runner/scripts/run_mmm.py \
  --input examples/data/mmm-weekly.csv \
  --time-col week_start \
  --kpi-col revenue \
  --kpi-type revenue \
  --media-cols paid_search_spend,paid_social_spend \
  --media-channels paid_search,paid_social \
  --controls promo_active,holiday \
  --n-chains 2 --n-adapt 200 --n-burnin 200 --n-keep 400 \
  --output-dir examples/mmm-runner/output \
  --style default
```

### Example Output Shape

#### `summary.md`

```markdown
# MMM summary

- Input: `examples/data/mmm-weekly.csv`
- KPI: `revenue` (revenue, 96 historical periods)
- Time column: `week_start`
- Media channels: `paid_search`, `paid_social`
- Controls: `promo_active`, `holiday`
- MCMC: chains=2, adapt=200, burnin=200, keep=400

## ROI per channel

| Channel      | ROI (mean) |   P5 |   P95 |
|--------------|-----------:|-----:|------:|
| paid_search  |       2.4  |  1.6 |   3.3 |
| paid_social  |       1.8  |  1.1 |   2.6 |

Highest mean ROI: **paid_search** (2.40).
```

Exact ROI values depend on MCMC sampling and the seed — quote credible intervals (P5–P95), never just the mean.

#### Files written

| File | Contents |
|---|---|
| `roi_per_channel.csv` | One row per channel: mean ROI, P5, P95 |
| `channel_contribution.csv` | Posterior contribution share per channel |
| `response_curves.csv` | Long-format spend multiplier → incremental outcome |
| `roi_per_channel.png` | Horizontal bar chart with credible interval error bars, styled via `lib/visualize.py` |
| `response_curves.png` | Multi-line saturation curves per channel |
| `summary.md` | The narrative above |

### How to read this

- Quote ROI as **mean (P5–P95)**, never as a point estimate. A "1.8 ROI" with a P5 of 0.4 is structurally different from one with a P5 of 1.6.
- Channels whose P5 dips below 1.0 are not statistically clear winners — flag them as inconclusive rather than recommending reallocation.
- Response curves let you spot saturation: where the slope flattens, more spend stops returning incremental revenue.
- Small MCMC settings (`--n-keep 400`) are fine for exploration. Production runs need `--n-keep 1000+` and convergence checks.
- Meridian fits Bayesian models with MCMC, so each run takes minutes-to-tens-of-minutes depending on data size + MCMC budget. Plan accordingly.
- MMM is **correlational, not causal.** Calibrate channel ROI against geo or holdout incrementality tests where possible.
