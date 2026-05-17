---
name: churn-driver-narrative-generator
description: Use when explaining likely drivers of churn, retention, renewal, repeat purchase, or customer lapse using cohort, engagement, acquisition, billing, operations, and cancellation evidence.
---

# Churn Driver Narrative Generator

This skill turns churn or retention evidence into a clear, defensible narrative. It helps the user move from "churn went up" to "these are the most likely drivers, what evidence supports them, and what to check next."

## Required Inputs

Ask only for what is missing:

- Churn or retention metric definition.
- Direction and size of movement.
- Baseline and comparison periods.
- Business model.
- Customer cohorts or tenure.
- Available dimensions, such as channel, plan, product, region, discount use, lifecycle segment, or customer value.
- Engagement, usage, support, cancellation, payment failure, delivery, or satisfaction signals.

If cancellation reasons or engagement data are unavailable, say how that limits the narrative.

## Driver Framework

Use these branches:

- `Acquisition quality`: weaker cohorts, lower-fit customers, discount-led acquisition, channel mix changes.
- `Activation or onboarding`: customers fail to reach first value.
- `Engagement decay`: usage, email, purchase, or product activity drops before churn.
- `Value perception`: price, offer, product fit, competitor alternatives, unmet expectations.
- `Operational friction`: delivery, support, stock, service, product availability, fulfilment.
- `Billing or involuntary churn`: failed payments, card expiry, dunning gaps.
- `Lifecycle contact`: poor timing, fatigue, irrelevant messages, missing save/winback journeys.
- `Measurement`: churn definition change, delayed status updates, duplicate customer records, reactivation handling.

## Output Template

```markdown
## Churn Driver Narrative

### Movement Summary
<metric, period, direction, and scale>

### Likely Driver Narrative
<plain-English synthesis>

### Evidence Table
| Driver | Evidence to check | Pattern that supports it | Priority |
|---|---|---|---|
| <driver> | <check> | <pattern> | <High/Medium/Low> |

### Segments to Inspect
- <segment>

### Data Gaps
- <missing field and why it matters>

### Recommended First Analysis
<one focused analysis>

### Actions After Validation
- <action>
```

## Common Patterns

- Churn concentrated in early tenure usually points to acquisition quality, onboarding, expectation-setting, or first-value delivery.
- Churn concentrated among discount-acquired customers often signals lower-quality acquisition or weak post-discount value perception.
- Rising involuntary churn points to billing, payment failure, dunning, or subscription operations.
- Churn after support, delivery, or product issues points to operational friction.
- Falling engagement before churn points to lifecycle, product usage, content relevance, or customer value.

## Guardrails

- Do not infer churn drivers from cancellation reason labels alone; they are often incomplete or biased.
- Do not compare cohorts until each has had the same chance to churn.
- Do not combine voluntary and involuntary churn without separating their drivers.
- Do not recommend retention actions before validating which customer segment is affected.
