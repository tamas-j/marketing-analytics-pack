---
name: metric-spec-card-generator
description: Use when defining a marketing metric precisely with formula, grain, required fields, exclusions, interpretation notes, caveats, and QA checks.
---

# Metric Spec Card Generator

This skill converts a KPI, dashboard metric, or stakeholder metric request into a precise metric spec card. The goal is to remove ambiguity before analysis or dashboarding begins.

## Required Inputs

Ask only for what is missing:

- Metric name or rough metric idea.
- Business context and decision the metric will support.
- Current definition, if one already exists.
- Reporting cadence, such as daily, weekly, monthly, campaign-level, or cohort-level.
- Available fields, files, or tables.
- Intended owner or audience, if relevant.

If details are missing, create a sensible draft and mark assumptions clearly.

## Method

1. Identify the metric's job: outcome, driver, input, quality signal, or guardrail.
2. Define the metric in plain English before writing a formula.
3. Define the numerator, denominator, and time window.
4. Specify the grain at which the metric is calculated.
5. Define inclusions, exclusions, and filters.
6. List required fields and useful breakdown dimensions.
7. Add interpretation notes so users know what movement means.
8. Add caveats and failure modes.
9. Add QA checks that can catch common data issues.
10. Include an example calculation if the user gave enough numbers.

## Metric Types

- `Outcome`: final business result, such as revenue, retained revenue, profit, churn, or customer growth.
- `Driver`: component that directly moves an outcome, such as conversion rate, average order value, or repeat purchase rate.
- `Input`: controllable activity, such as spend, sends, impressions, calls, or discounts issued.
- `Quality`: signal of audience, traffic, customer, or lead quality.
- `Guardrail`: metric that prevents harmful optimization, such as margin, unsubscribe rate, refund rate, complaint rate, or delivery failure.

## Spec Card Template

```markdown
## Metric Spec Card: <metric name>

### Purpose
<what decision this metric supports>

### Metric Type
<Outcome / Driver / Input / Quality / Guardrail>

### Definition
<plain-English definition>

### Formula
<formula>

Numerator: <definition>
Denominator: <definition, if applicable>
Time window: <daily / weekly / monthly / campaign / cohort>

### Grain
<one row per ... / calculated at ...>

### Required Fields
| Field | Why it is needed | Example |
|---|---|---|
| <field> | <reason> | <value> |

### Filters and Exclusions
- <inclusion or exclusion>

### Useful Dimensions
- <dimension>

### Interpretation Notes
- <how to read movement in this metric>

### Caveats and Guardrails
- <risk or related guardrail>

### QA Checks
- <check>

### Example Calculation
<short calculation, if possible>
```

## Common Metric Specs

### Conversion Rate

- Formula: `converted users / eligible users`
- Clarify eligibility, conversion event, attribution window, duplicate handling, and whether the denominator is users, sessions, leads, or visitors.
- Common guardrails: conversion quality, average order value, refund rate, downstream retention.

### Customer Acquisition Cost

- Formula: `eligible acquisition spend / new customers acquired`
- Clarify included spend, time window, acquisition definition, attribution source, refunds, and whether customers are gross or net new.
- Common guardrails: customer lifetime value, margin, payback period, retention.

### Retention Rate

- Formula: `retained customers / customers eligible to retain`
- Clarify cohort start, retention event, retention window, reactivation handling, and whether it is logo, revenue, or activity retention.
- Common guardrails: revenue retained, discount rate, service cost, customer satisfaction.

### Email Click Rate

- Formula: `unique clickers / delivered emails`
- Clarify unique vs total clicks, bot filtering, delivered vs sent denominator, and attribution window.
- Common guardrails: unsubscribe rate, complaint rate, conversion rate, fatigue.

## QA Checklist

- Numerator and denominator can be reproduced from raw fields.
- Metric grain matches the intended reporting grain.
- Date filters are explicit and timezone handling is known.
- Test records, internal users, bots, and duplicates are excluded where relevant.
- Missing values cannot silently turn into zeros.
- Rate denominators cannot be zero.
- The metric reconciles to at least one trusted source or known total.
- A sudden change can be explained by components or data pipeline changes.

## Guardrails

- Never define a rate without naming the denominator.
- Never define a time-based metric without a time window.
- Do not mix user-level, session-level, and order-level grains without saying how they join.
- Do not imply causality from a descriptive metric.
- Keep the spec practical enough for someone to implement or request from a data team.
