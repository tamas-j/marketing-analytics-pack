---
name: kpi-tree-generator
description: Use when turning a marketing or commercial goal into a KPI tree with measurable drivers, formulas, guardrails, diagnostic questions, and recommended first analysis.
---

# KPI Tree Generator

This skill turns a broad goal into a clear KPI tree. It is designed for non-technical marketing and analytics users who need to know what to measure, why it matters, and what data they need next.

## Required Inputs

Ask only for what is missing:

- Business goal, such as "increase retention", "grow paid acquisition profitably", or "improve checkout conversion".
- Business model or context, such as ecommerce, subscription, marketplace, B2B SaaS, media, or lead generation.
- Audience, journey stage, channel, product line, or region in scope.
- Time horizon, if relevant.
- Available data columns, if the user has a dataset.

If the user gives only a vague goal, proceed with sensible assumptions and mark them clearly.

## Method

1. Define the north-star outcome in business language.
2. Split the outcome into level 1 drivers that are as close to mutually exclusive as practical.
3. Split each driver into level 2 levers that a marketing or analytics team can influence or diagnose.
4. Convert each lever into measurable KPIs with formulas.
5. Classify each metric:
   - `Outcome`: lagging business result
   - `Driver`: direct component of the outcome
   - `Input`: controllable activity or volume
   - `Quality`: measure of traffic, audience, or customer quality
   - `Guardrail`: metric that prevents harmful optimization
6. Add data requirements and useful dimensions for cuts.
7. Recommend the first analysis based on likely leverage and data availability.

## KPI Tree Principles

- A KPI tree should explain how the business outcome moves, not list every dashboard metric.
- Prefer formulas that reveal trade-offs, such as `Revenue = Sessions x Conversion rate x Average order value`.
- Put vanity metrics below the line unless they directly explain the outcome.
- Guardrails matter. For example, improving conversion by over-discounting can hurt margin and customer quality.
- Leading indicators should help the user act earlier than the final outcome metric.
- If a driver cannot be measured with current data, include it anyway and mark the missing data.

## Common Marketing KPI Trees

### Ecommerce Revenue

North-star: `Revenue`

- Traffic volume
  - Sessions
  - Qualified sessions
  - New vs returning visitors
- Conversion efficiency
  - Product page view rate
  - Add-to-cart rate
  - Checkout completion rate
- Order value
  - Average order value
  - Units per transaction
  - Discount rate
- Customer quality
  - Repeat purchase rate
  - Gross margin
  - Return rate

### Subscription Retention

North-star: `Retained recurring revenue`

- Active customer base
  - Paying subscribers
  - Activation rate
  - Re-activation rate
- Churn
  - Logo churn
  - Revenue churn
  - Involuntary churn
- Expansion
  - Upgrade rate
  - Add-on attach rate
  - Seat expansion
- Engagement quality
  - Core action completion
  - Frequency of use
  - Support issue rate

### Paid Acquisition Efficiency

North-star: `Incremental profitable customers`

- Spend
  - Budget by channel
  - Impression volume
  - Reach and frequency
- Traffic quality
  - Click-through rate
  - Landing page engagement
  - Qualified visit rate
- Conversion
  - Lead or purchase conversion rate
  - Cost per acquisition
  - Sales acceptance rate
- Value and incrementality
  - Customer lifetime value
  - Payback period
  - Incremental lift
  - Margin after media cost

## Output Template

```markdown
## KPI Tree: <goal>

### Executive Summary
<2-4 sentences on the measurement logic and likely first place to investigate.>

### KPI Tree
| Level | Metric or driver | Why it matters | Formula or definition | Data needed | Metric type |
|---|---|---|---|---|---|
| 0 | <north-star> | <reason> | <formula> | <columns> | Outcome |

### Diagnostic Questions
- <question>

### Next Data Check
- <column or dimension needed>

### Recommended First Analysis
<one focused analysis that would most quickly validate the tree.>
```

## Visual Output Guidance

Use the `data-visualization` skill for chart styling. If rendering a tree diagram, keep it simple: one title, 3-5 level 1 drivers, and short labels. If a tree would be too dense, render a horizontal bar chart ranking the level 1 drivers by estimated importance, confidence, or current performance gap.

## Quality Checklist

- The north-star outcome is a business result, not an activity metric.
- Every level 1 driver has a clear relationship to the north-star outcome.
- Every metric has either a formula or a plain-English definition.
- Data requirements are specific enough for the user to check a CSV or warehouse table.
- Guardrails are included where optimization could create bad behavior.
- The recommended first analysis is one concrete next step, not a broad research agenda.
