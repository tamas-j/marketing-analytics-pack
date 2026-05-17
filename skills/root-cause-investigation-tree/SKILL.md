---
name: root-cause-investigation-tree
description: Use when diagnosing why a marketing, product, revenue, conversion, retention, or engagement metric changed and the user needs a structured investigation plan.
---

# Root Cause Investigation Tree

This skill turns a metric movement into a structured diagnosis. It helps the user decompose the change, identify plausible branches, prioritise checks, and avoid premature conclusions.

## Required Inputs

Ask only for what is missing:

- Metric that changed.
- Direction and size of movement, if known.
- Baseline period and comparison period.
- Metric definition or formula.
- Business model or journey stage.
- Available dimensions, such as channel, campaign, product, segment, device, region, cohort, or lifecycle stage.
- Known changes, such as campaigns, launches, promotions, outages, tracking changes, pricing changes, seasonality, or competitor events.

If the user has only a vague movement, proceed with a draft tree and mark assumptions.

## Method

1. Define the metric and comparison period.
2. Decompose the metric into its mathematical or behavioral components.
3. Split likely causes into branches that can be checked with data.
4. Separate performance causes from measurement causes.
5. Prioritise branches by expected impact, plausibility, ease of validation, and decision relevance.
6. Recommend the first cuts or charts to run.
7. State what evidence would support or rule out each branch.

## Common Decompositions

### Revenue

`Revenue = traffic or customers x conversion rate x average order value`

Useful branches:

- volume: sessions, leads, active customers, orders
- conversion: visit-to-purchase, lead-to-sale, checkout completion
- value: average order value, units per order, price, discount rate
- mix: channel, product, region, new vs returning customers
- quality: customer value, lead quality, repeat behavior
- measurement: tracking, order status, refunds, attribution

### Conversion Rate

`Conversion rate = conversions / eligible population`

Useful branches:

- numerator change: fewer conversions, delayed conversions, event tracking
- denominator change: more low-quality traffic or broader eligibility
- funnel step change: product view, add-to-cart, checkout, payment
- mix shift: channel, device, landing page, campaign, audience
- friction: page speed, stock, form issues, price, shipping, promo validity
- measurement: duplicate sessions, event firing, bot filtering

### Retention or Churn

Useful branches:

- cohort quality: acquisition channel, discount use, first product, plan
- lifecycle engagement: email/SMS engagement, product usage, onboarding
- service or operational issues: delivery, support, billing, payment failure
- pricing or value perception
- seasonality or customer lifecycle timing
- measurement: churn definition, reactivation handling, tenure mix

### Campaign Performance

Useful branches:

- spend and delivery
- audience quality
- creative fatigue
- landing page conversion
- attribution window or tracking
- offer strength
- competitor or seasonality effects
- incrementality vs observed conversions

## Output Template

```markdown
## Root Cause Investigation: <metric movement>

### Movement Summary
<metric, period, comparison, size, and why it matters>

### Root Cause Tree
| Branch | Hypothesis | What to check | Evidence that supports it | Priority |
|---|---|---|---|---|
| <branch> | <hypothesis> | <cut/check> | <evidence> | <High/Medium/Low> |

### First Cuts to Run
1. <cut>
2. <cut>
3. <cut>

### Data Needed
- <field or table>

### Likely Explanations to Validate
- <hypothesis>

### Watch-outs
- <measurement or causality caveat>
```

## Prioritisation Heuristics

- Start with metric definition and tracking checks if the movement is sudden, extreme, or coincides with release or instrumentation changes.
- Start with component decomposition if the metric is a rate or revenue figure.
- Start with mix checks if total volume is stable but performance changed.
- Start with cohort or channel quality if new customers look worse than existing customers.
- Start with external or seasonal checks only after obvious internal component shifts are ruled out.

## Guardrails

- Do not make causal claims from segment cuts alone.
- Do not ignore the denominator of a rate.
- Do not compare immature cohorts with mature cohorts.
- Do not mix order, user, session, and event grains without noting the join risk.
- Do not overfit to one anecdote when a component check can be run.
- Keep the recommended first investigation practical and fast.
