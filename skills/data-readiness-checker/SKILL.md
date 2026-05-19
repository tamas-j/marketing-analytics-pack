---
name: data-readiness-checker
description: Use when checking whether a marketing dataset, file, schema, or pasted column list can support a requested analysis workflow.
---

# Data Readiness Checker

This skill checks whether a dataset is fit for the user's intended marketing analytics task. It is not a full data quality audit; it is a practical readiness check that tells the user whether they can proceed.

## Required Inputs

Ask only for missing essentials:

- Intended analysis or decision.
- Dataset grain, if known.
- File path, pasted sample, or column list.
- Time period covered.
- Key entities, such as customer, order, campaign, channel, product, session, or email send.

If the user has only column names, perform a schema-level review and say that row-level checks still need the file.

## Readiness Verdicts

- `Ready`: the dataset appears to contain the grain and fields needed for the analysis.
- `Usable with caveats`: the analysis can proceed, but interpretation needs warnings.
- `Needs fixes`: useful structure exists, but the user should repair fields, definitions, or missing values first.
- `Blocked`: core grain, identifiers, dates, or outcome fields are missing.

## Universal Checks

1. Grain: can we say what one row represents?
2. Entity keys: are key identifiers present and stable?
3. Dates: are there usable date fields for the analysis period?
4. Outcome: is the metric or event to explain present?
5. Drivers: are there plausible dimensions or inputs to compare?
6. Coverage: is the time window long enough?
7. Duplicates: could duplicated rows inflate counts or revenue?
8. Missingness: are important fields often blank?
9. Definitions: are derived fields clearly defined?
10. Leakage: for prediction or forecasting, are future-known fields excluded?

## Quick File Profile

When the user provides a CSV path and file access is available, run the bundled profiler before making row-level claims:

```bash
python skills/data-readiness-checker/scripts/profile_data.py <csv-path>
```

If the expected grain key is known, include it:

```bash
python skills/data-readiness-checker/scripts/profile_data.py <csv-path> --grain-key customer_id
```

Use the profile to report row count, column names, missingness, date-like columns, and duplicate keys. If only column names are pasted, do not claim missingness, duplicates, or date gaps.

## Common Field Aliases

Map likely aliases before deciding something is missing:

| Concept | Common aliases |
|---|---|
| Customer key | `customer_id`, `user_id`, `client_id`, `account_id`, `subscriber_id` |
| Order key | `order_id`, `transaction_id`, `purchase_id`, `booking_id` |
| Date | `date`, `order_date`, `event_date`, `week_start`, `created_at`, `signup_date` |
| Revenue | `revenue`, `net_revenue`, `sales`, `amount`, `order_value`, `mrr` |
| Channel | `channel`, `source`, `medium`, `utm_source`, `utm_medium`, `acquisition_channel` |
| Campaign | `campaign`, `campaign_id`, `utm_campaign`, `campaign_name` |
| Treatment | `treatment`, `variant`, `holdout_flag`, `control_flag`, `exposed_flag` |

## Task-Specific Field Guide

### KPI Tree or Metric Design

Useful fields:

- outcome metric or proxy
- date
- entity key
- channel, campaign, audience, product, region, or journey stage
- numerator and denominator fields for rates

### Root Cause Diagnosis

Useful fields:

- metric value
- date or period
- dimensions to cut by
- comparable prior period or benchmark
- volume and rate components

### Segmentation

Useful fields:

- customer or account key
- behavior measures
- value measures
- recency or tenure dates
- consent or eligibility flags when relevant

### Experimentation or Incrementality

Useful fields:

- treatment or exposure flag
- control or holdout flag
- assignment date
- outcome date
- pre-period baseline
- unit of randomization

### Forecasting

Useful fields:

- date
- target metric
- regular time interval
- enough history for seasonality
- known calendar events or campaign inputs, if available

Typical thresholds:

- `Ready`: at least 2 seasonal cycles, regular time grain, target has few missing periods.
- `Usable with caveats`: 1-2 seasonal cycles or limited known future inputs.
- `Blocked`: no date field, no target metric, or irregular periods that cannot be repaired.

### MMM or Attribution

Useful fields:

- date at a regular interval
- outcome metric
- spend or exposure by channel
- price, promo, seasonality, and external controls where possible
- enough history to estimate lagged effects

Typical thresholds:

- `Ready`: 104+ weekly rows or 24+ monthly rows, stable KPI, media inputs by channel, and useful controls.
- `Usable with caveats`: 52-103 weekly rows, few controls, or some channels with weak variation.
- `Blocked`: no regular time series, no media inputs, or only platform-attributed conversions as the KPI.

### RFM Segmentation

Useful fields:

- customer key
- order or transaction key
- transaction date
- order value or revenue

Typical thresholds:

- `Ready`: stable customer key, transaction date, monetary value, and enough repeat behavior to rank customers.
- `Usable with caveats`: customer/date/value exist but repeat behavior is sparse.
- `Blocked`: no customer key or no transaction date.

### CLV Scenario

Useful fields:

- customer or cohort key
- revenue or ARPU
- margin or contribution margin
- retention, churn, repeat purchase, or lifetime proxy
- acquisition cost or media cost

Typical thresholds:

- `Ready`: enough observed cohort behavior to replace at least retention/frequency and margin assumptions.
- `Usable with caveats`: directional assumptions available but cohorts are immature.
- `Blocked`: no value, margin, or retention/frequency assumption.

## Output Template

```markdown
## Data Readiness Check

### Verdict
<Ready / Usable with caveats / Needs fixes / Blocked>

### Dataset Grain
<one row per ...>

### What Looks Usable
- <field or structure>

### Risks or Missing Fields
- <issue and why it matters>

### Fixes Before Analysis
- <specific fix>

### Best Next Command
<command or workflow>

### Can Proceed Now?
<yes / yes with caveats / no, with one sentence>
```

## Guardrails

- Do not make row-level claims from column names alone.
- Do not block exploratory work because the dataset is imperfect.
- Do block analysis when the grain is unclear and counts or rates would be misleading.
- Separate "missing for this analysis" from "generally nice to have".
- Explain problems in user language, not database jargon.
