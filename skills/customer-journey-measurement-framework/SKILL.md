---
name: customer-journey-measurement-framework
description: Use when mapping a customer journey into lifecycle stages, KPIs, data requirements, diagnostics, and guardrails for marketing measurement.
---

# Customer Journey Measurement Framework

This skill turns a customer journey into a practical measurement framework. It helps the user understand which customer behaviors matter at each stage, how to measure them, and what data is needed before analysis.

## Required Inputs

Ask only for what is missing:

- Business model, such as ecommerce, subscription, marketplace, B2B SaaS, lead generation, or media.
- Journey stages in scope.
- Target customer or audience.
- Main channels or touchpoints.
- Business goal, such as growth, conversion, retention, reactivation, or profitability.
- Available fields, files, or systems.

If the user has no formal journey map, create a standard lifecycle and mark it as a draft.

## Standard Journey Stages

Use only the stages that fit the business:

1. `Awareness`: the customer becomes reachable or aware.
2. `Acquisition`: the customer visits, signs up, becomes a lead, or enters the funnel.
3. `Activation`: the customer completes the first meaningful action.
4. `Conversion`: the customer purchases, subscribes, books, or becomes qualified.
5. `Retention`: the customer repeats, renews, stays active, or continues value-generating behavior.
6. `Expansion`: the customer increases value through upsell, cross-sell, basket growth, seats, or usage.
7. `Reactivation`: the customer returns after lapse, churn, or inactivity.
8. `Advocacy`: the customer refers, reviews, shares, or creates positive word of mouth.

## Method

1. Define the journey in terms of customer behaviors, not internal team activities.
2. Choose the stages that matter for the user's business model.
3. For each stage, define:
   - desired customer behavior
   - primary KPI
   - supporting drivers
   - guardrails
   - required data
   - useful dimensions
   - diagnostic questions
4. Identify handoff points where customers commonly drop, stall, or become unmeasurable.
5. Flag data gaps that prevent stage-to-stage measurement.
6. Recommend one first analysis that would improve decision-making fastest.

## Stage Metric Guide

### Awareness

- Primary metrics: reach, qualified reach, brand search demand, direct traffic, share of search.
- Drivers: impressions, frequency, audience quality, channel mix.
- Guardrails: wasted reach, frequency saturation, brand safety.

### Acquisition

- Primary metrics: visits, leads, signups, new customers, cost per acquired customer.
- Drivers: click-through rate, landing page conversion, form completion, traffic quality.
- Guardrails: acquisition quality, fraud, duplicate leads, margin after acquisition cost.

### Activation

- Primary metrics: activation rate, first value action rate, onboarding completion.
- Drivers: time to first action, onboarding step completion, product or content engagement.
- Guardrails: support burden, drop-off after activation, low-quality activation events.

### Conversion

- Primary metrics: purchase conversion rate, sales accepted lead rate, subscription conversion.
- Drivers: product page engagement, add-to-cart rate, checkout completion, sales contact rate.
- Guardrails: discount rate, refund rate, cancelled orders, poor-fit customers.

### Retention

- Primary metrics: repeat purchase rate, renewal rate, retained revenue, churn rate.
- Drivers: engagement frequency, product usage, lifecycle contact, satisfaction, delivery quality.
- Guardrails: margin, complaint rate, unsubscribe rate, customer support cost.

### Expansion

- Primary metrics: average order value, upsell rate, cross-sell rate, revenue expansion.
- Drivers: recommendations, bundles, plan upgrades, add-on attach rate.
- Guardrails: downgrade rate, returns, discount dependency, churn after upsell.

### Reactivation

- Primary metrics: reactivated customers, winback rate, revenue from lapsed customers.
- Drivers: winback offer engagement, lapse duration, reason for churn, channel reachability.
- Guardrails: margin after incentives, unsubscribe rate, complaint rate.

### Advocacy

- Primary metrics: referrals, reviews, earned sharing, referral conversion rate.
- Drivers: satisfaction, incentive structure, review prompts, referral journey completion.
- Guardrails: incentive abuse, low-quality referrals, review policy risk.

## Output Template

```markdown
## Customer Journey Measurement Framework

### Journey Summary
<business model, goal, audience, and stages in scope>

### Measurement Framework
| Stage | Desired customer behavior | Primary KPI | Supporting drivers | Guardrails | Data needed | Diagnostic cuts |
|---|---|---|---|---|---|---|
| <stage> | <behavior> | <metric> | <drivers> | <guardrails> | <fields> | <dimensions> |

### Measurement Gaps
- <gap and why it matters>

### Diagnostic Questions
- <question>

### Recommended First Analysis
<one focused next step>
```

## Quality Checklist

- The journey stages match the business model.
- Every stage describes customer behavior, not only marketing activity.
- Each stage has a primary KPI and at least one guardrail where needed.
- Metrics are not duplicated across stages unless the interpretation changes.
- Required data is specific enough for a file or schema check.
- The recommended first analysis is feasible with likely available data.

## Guardrails

- Do not overfit the framework to every possible touchpoint.
- Do not present attribution as solved if customer interactions cross channels or devices.
- Do not optimize acquisition metrics without quality or retention guardrails.
- Do not use retention metrics before cohorts have had enough time to mature.
- Keep recommendations practical for a marketing or analytics practitioner — concrete metrics, named fields, and decision-relevant cuts.
