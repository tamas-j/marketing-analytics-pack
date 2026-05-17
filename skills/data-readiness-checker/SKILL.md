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

### MMM or Attribution

Useful fields:

- date at a regular interval
- outcome metric
- spend or exposure by channel
- price, promo, seasonality, and external controls where possible
- enough history to estimate lagged effects

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
```

## Guardrails

- Do not make row-level claims from column names alone.
- Do not block exploratory work because the dataset is imperfect.
- Do block analysis when the grain is unclear and counts or rates would be misleading.
- Separate "missing for this analysis" from "generally nice to have".
- Explain problems in user language, not database jargon.
