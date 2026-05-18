---
description: Run a Google Meridian MMM (spec mode for planning, execution mode via scripts/run_mmm.py for real ROI + response curves).
argument-hint: "<prepared MMM dataset, KPI, media channels, controls, priors/assumptions, geo/time grain>"
---

# MMM Runner

Use this command for a Google Meridian MMM run. It has two modes:

- **Spec mode** (default): plan the model — input schema, priors, assumptions, validation plan, expected outputs, caveats.
- **Execution mode**: run `skills/mmm-runner/scripts/run_mmm.py` against a CSV and emit ROI per channel, contribution shares, response curves, and styled charts.

Default to spec mode unless the user has a CSV ready and asks for outputs.

Use skill: "mmm-runner"
Use skill: "mmm-readiness-checker"
Use skill: "data-visualization"

## Spec Workflow

1. Confirm the readiness verdict and modelling scope.
2. Define the model inputs:
   - KPI (and `kpi_type`: revenue or non_revenue)
   - time index
   - media spend / exposure columns
   - controls
   - geo / product hierarchy if used (national for v1)
3. Define assumptions:
   - lag / adstock expectations
   - saturation expectations
   - priors or constraints where available
   - train / validation windows
4. Produce an execution checklist for Google Meridian.
5. Define expected outputs and interpretation guardrails.

### Spec Output Format

Return:

1. Model scope
2. Input schema
3. Assumptions and priors
4. Execution checklist
5. Expected outputs
6. Validation checks
7. Caveats

## Execution Workflow

1. Confirm the CSV path, time column, KPI column, KPI type, media columns, channel labels, and controls with the user.
2. Confirm MCMC settings — defaults are fine for exploratory runs, bump `--n-keep` to 1000+ for production interpretation.
3. Run `python skills/mmm-runner/scripts/run_mmm.py` with the chosen flags. Pass `--auto-install` if Meridian is not yet installed. Strongly recommend a virtual environment because Meridian pulls TensorFlow + tfp-nightly (~600 MB).
4. Read `summary.md` from the output directory and present ROI + best channel + caveats.
5. Show `roi_per_channel.png` and `response_curves.png` inline if the surface supports it.

### Example

```bash
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

## Guardrails

- In spec mode: do not pretend the model has run unless actual outputs are provided.
- In execution mode: always quote the posterior interval alongside the mean ROI; never quote a point estimate alone.
- Do not recommend MMM if readiness is blocked.
- Do not recommend budget moves from a single MMM run without diagnostics and ideally external incrementality calibration.
- Small MCMC settings (`--n-keep 400`) are fine for exploration; production runs need 1000+.
