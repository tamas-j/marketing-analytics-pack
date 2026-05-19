# Check Data Example

## Prompt

```text
/check-data I want to run an MMM on examples/data/mmm-weekly.csv. Columns: week_start, revenue, paid_search_spend, paid_social_spend, email_sends, tv_grps, promo_active, holiday. ~96 weeks. Is it ready?
```

## Example Output

The command first profiles the file:

```bash
python skills/data-readiness-checker/scripts/profile_data.py examples/data/mmm-weekly.csv --grain-key week_start
```

## Data Readiness Check

### Verdict

**Usable with caveats.** The file has the right shape for a small Bayesian MMM (one row per week, revenue as KPI, three paid-media spend columns, email volume, TV GRPs, and two control flags), but the history is short for separating channels and the lack of a separate exposure series for TV / email means you'll have to lean on spend (or sends / GRPs) as the exposure proxy.

### Dataset Grain

One row per `week_start` — 96 weekly observations (2024-01-01 → 2025-10-27), no obvious gaps in the date column.

### What Looks Usable

- **Outcome:** `revenue` is a stable business KPI, not a platform-attributed one. Right metric for MMM.
- **Time grain:** weekly is the standard MMM grain.
- **Media inputs:** three paid channels with spend (`paid_search_spend`, `paid_social_spend`, `tv_grps`) plus an owned channel (`email_sends`). Mixing spend with non-spend exposure is fine as long as you're explicit about it in the runner.
- **Controls:** `promo_active` and `holiday` are present as 0/1 flags — covers two of the most common confounders.
- **Variation:** spend columns vary across weeks (eyeball check on the first / last rows confirms paid search ranged ~6.6k–11.4k); not always-on at a flat budget, which is what MMM needs.

### Risks or Missing Fields

- **History length is on the short side.** 96 weeks is just under two years; you have one full seasonal cycle plus part of a second, which is the floor for picking up annual seasonality + holiday effects. Estimates will be wider than they'd be with three years.
- **No separate exposure for TV or email.** `tv_grps` is a delivery measure (fine), but `email_sends` is volume, not engagement. If most sends go to inactive users, the channel's coefficient will look weaker than its real impact.
- **No price or promotion depth.** `promo_active` is binary — captures *whether* there was a promo, not how big the discount was. MMM may credit media for promo-driven lifts unless you add a `promo_depth` column.
- **No external controls.** No macro index, competitor spend, weather, or category demand proxy. Often fine for an internal directional MMM; flag it before promising channel-level precision.
- **Geo / market split absent.** This is national-only data. Geo splits would give Meridian more identification; without them you're relying on time variation alone.

### Fixes Before Analysis

- Add a `promo_depth` numeric column (avg discount %) alongside `promo_active`, if available.
- Confirm `paid_search_spend` and `paid_social_spend` exclude agency fees / production costs you wouldn't expect to drive incremental sales — or call it out in the spec so the ROI readout doesn't mislead.
- Sanity-check `email_sends` against a deliverability or open-volume proxy if one exists. If not, plan to interpret the email coefficient as "send volume effect", not "engagement effect".
- Keep the first 8–13 weeks aside as a holdout for backtesting; the runner's `--validate` flag will do this automatically.

### Best Next Command

`/mmm-readiness` for the full MMM-specific checklist (saturation priors, MCMC settings, identifiability risks), then `/mmm-runner` once you've decided on channel labels and controls. Given the short history, plan to **calibrate against a small geo or holdout incrementality test** before shifting real budget — `/incrementality-test-designer` for that.

## How to read this

- "Usable with caveats" is the most common readiness verdict for MMM. Don't read it as "fail" — it means proceed but document the limitations in the writeup.
- The "no separate exposure for TV / email" caveat matters less than it sounds: spend is a fine MMM input in practice as long as media costs haven't shifted dramatically across the window.
- Short history is the most-cited reason for wide credible intervals in the result. If the user has another year of data sitting elsewhere, this is the cheapest single thing they can do to improve precision.
