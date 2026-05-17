# Analysis Brief Example

## Prompt

```text
/analysis-brief We need to understand why repeat purchases fell in Q1 for our ecommerce skincare brand and what lifecycle team should do next. We have orders, customer IDs, product category, discounts, email engagement, and refund data.
```

## Example Output

## Analysis Brief: Q1 Repeat Purchase Decline

### Business Question

Why did repeat purchases fall in Q1, and what should the lifecycle team do next?

### Decision to Support

Decide whether the lifecycle team should prioritise replenishment timing, discount strategy, product category journeys, or customer quality interventions.

### Scope

In scope:
- Repeat purchase behavior for Q1 cohorts and comparable prior cohorts.
- Customer cuts by first product category, discount use, acquisition channel, and email engagement.
- Refund and product mix checks.

Out of scope:
- Full incrementality read of lifecycle campaigns.
- Long-term CLV modelling beyond repeat purchase indicators.

### Hypotheses

| Hypothesis | How to test | Evidence that supports it |
|---|---|---|
| Discount-acquired customers repeated less | Compare repeat rate by first-order discount use | Discount cohorts have lower 60/90-day repeat rate |
| Product mix shifted to lower-repeat categories | Compare first product category mix and repeat rate | More customers entered through low-repeat categories |
| Lifecycle engagement weakened | Compare email click/open before second purchase | Lower engagement among customers who failed to repeat |
| Refund or product issues reduced repeat | Compare refund rate by cohort/category | High refund categories show weaker repeat |

### Data Requirements

| Data | Grain | Required fields | Notes |
|---|---|---|---|
| Orders | order | customer_id, order_id, order_date, product_category, discount_code, net_revenue | Needed to define first and repeat orders |
| Email engagement | send or customer | customer_id, campaign_date, open, click | Needed to inspect lifecycle engagement |
| Refunds | order | order_id, refund_amount, refund_date | Needed as guardrail |

### Analysis Plan

1. Build first-order cohorts by month and measure 60/90-day repeat purchase rate.
2. Split repeat rate by first product category, discount use, and acquisition channel.
3. Compare email engagement before expected repeat windows.
4. Check refund rate and net revenue by cohort.

### Expected Outputs

- Cohort repeat purchase table.
- Driver cuts by category, discount, acquisition channel, and email engagement.
- Short recommendation on which lifecycle lever to test first.

### Decision Criteria

- Prioritise a lever if it explains a material share of the repeat purchase decline and is actionable by lifecycle marketing.

### Risks and Caveats

- Q1 cohorts must have enough time to repeat before comparison.
- Email engagement may correlate with repeat behavior without causing it.
- Missing acquisition channel data would limit customer quality diagnosis.
