---
name: clv-scenario-modeller
description: Use when building lightweight customer lifetime value scenarios with revenue, margin, retention, churn, purchase frequency, CAC, payback, and sensitivity assumptions.
---

# CLV Scenario Modeller

This skill builds simple customer lifetime value scenarios for marketing planning. It is designed for directional decision-making, not financial reporting or a full predictive model.

## Required Inputs

Ask only for what is missing:

- Business model: ecommerce, subscription, marketplace, B2B SaaS, lead generation, or another model.
- Revenue input: average order value, average revenue per user, monthly recurring revenue, or average deal value.
- Margin input: gross margin percent or contribution margin percent.
- Retention input: repeat purchase rate, purchase frequency, retention rate, churn rate, or expected lifetime.
- Acquisition cost input: CAC, CPA, media cost per customer, or target acquisition cost.
- Time horizon: such as 90 days, 12 months, 24 months, or customer lifetime.
- Discount, incentive, refund, or service cost assumptions, if relevant.

If the user lacks some numbers, create clearly labelled placeholder scenarios and tell them which assumptions matter most.

## Formula Selection

Choose the simplest model that fits the business.

### Ecommerce Repeat Purchase CLV

Use when customers make discrete purchases.

`gross CLV = average order value x gross margin x expected orders per customer`

Optional:

`net CLV = gross CLV - acquisition cost - discount cost - expected return cost`

Expected orders can be a direct input, or estimated from first order plus repeat behavior:

`expected orders = 1 + repeat purchase rate x average repeat orders among repeaters`

### Subscription CLV

Use when customers pay recurring revenue.

`gross CLV = ARPU per period x gross margin / churn rate`

Optional:

`net CLV = gross CLV - acquisition cost - onboarding cost - incentive cost`

If using retention instead of churn:

`churn rate = 1 - retention rate`

### Cohort Horizon CLV

Use when the user wants a fixed horizon, such as 90-day or 12-month value.

`gross CLV over horizon = sum(period revenue x margin)`

If detailed period values are not available:

`gross CLV over horizon = average period revenue x gross margin x expected active periods`

### Lead Generation CLV

Use when marketing creates leads that convert later.

`expected customer value per lead = lead-to-customer rate x customer gross CLV`

`net value per lead = expected customer value per lead - cost per lead`

## Scenario Method

Create three scenarios:

- `Cautious`: lower retention or frequency, lower margin, higher acquisition cost.
- `Base`: user's best current assumption.
- `Optimistic`: better retention or frequency, better margin, lower acquisition cost.

For each scenario, show:

- revenue assumption
- margin assumption
- retention or frequency assumption
- acquisition cost
- gross CLV
- net CLV
- CLV:CAC ratio
- payback period, if possible

## Output Template

```markdown
## CLV Scenario Model

### Decision Summary
<what decision this model supports>

### Formula Used
<formula and why it fits>

### Assumptions
| Assumption | Cautious | Base | Optimistic | Notes |
|---|---:|---:|---:|---|
| <assumption> | <value> | <value> | <value> | <note> |

### Scenario Results
| Scenario | Gross CLV | Acquisition cost | Net CLV | CLV:CAC | Payback | Readout |
|---|---:|---:|---:|---:|---:|---|
| Cautious | <value> | <value> | <value> | <ratio> | <period> | <interpretation> |

### Sensitivity Notes
- <which assumptions move the result most>

### Guardrails and Caveats
- <risk>

### Data Needed Next
- <field or metric>

### Recommended First Analysis
<one focused analysis to replace assumptions with observed values>
```

## Sensitivity Guide

Most CLV scenarios are highly sensitive to:

- retention or churn rate
- repeat purchase frequency
- gross margin
- acquisition cost
- discount dependency
- refund or return rate
- customer quality by acquisition channel

Call out sensitivity plainly. A useful CLV model should tell the user which assumption to validate first.

## Guardrails

- Do not imply that a scenario model proves causal impact.
- Do not use revenue CLV when the decision depends on profitability.
- Do not compare channels on CAC alone; include quality, retention, and margin.
- Do not treat early cohorts as mature if the time horizon has not elapsed.
- Do not hide discount, refund, servicing, or onboarding costs when they materially affect value.
- Use sensible rounding and avoid fake precision.
