# KPI Tree Example

## Prompt

```text
/kpi-tree We run a subscription coffee brand and want to improve retention. We have customer signup date, plan type, order dates, skipped deliveries, cancellation reason, discount code, and email engagement.
```

## Example Output

### Executive Summary

The north-star metric should be retained recurring revenue, because it captures both subscriber volume and customer value. The first investigation should compare churn and skip behavior by plan type, tenure, discount usage, and email engagement to find the highest-leverage retention drivers.

### KPI Tree

| Level | Metric or driver | Why it matters | Formula or definition | Data needed | Metric type |
|---|---|---|---|---|---|
| 0 | Retained recurring revenue | Captures the revenue that remains after churn and plan changes | Opening recurring revenue - churned recurring revenue + expansion recurring revenue | customer_id, plan_price, subscription_status, order_date | Outcome |
| 1 | Active subscriber base | Sets the pool of customers who can renew | Active paying subscribers at period start | customer_id, signup_date, subscription_status | Driver |
| 1 | Churn rate | Directly reduces retained revenue | Cancelled subscribers / active subscribers at period start | cancellation_date, subscription_status | Driver |
| 1 | Skip rate | Early warning signal before cancellation | Skipped deliveries / scheduled deliveries | skipped_delivery_flag, order_date | Input |
| 1 | Plan value | Explains revenue retained per subscriber | Average plan value among retained subscribers | plan_type, plan_price | Driver |
| 1 | Engagement quality | Signals whether subscribers are still responsive | Email opens or clicks per active subscriber | email_open, email_click, campaign_date | Quality |
| 2 | Discount-acquired retention | Checks whether promotion-led customers are lower quality | Retention rate by discount code cohort | discount_code, signup_date, cancellation_date | Quality |
| 2 | Cancellation reason mix | Shows which churn causes are addressable | Share of cancellations by reason | cancellation_reason | Driver |
| 2 | Tenure-based churn | Separates onboarding issues from mature customer fatigue | Churn rate by months since signup | signup_date, cancellation_date | Driver |
| 2 | Delivery friction | Detects operational drivers of churn | Churn after skip or missed delivery events | skipped_delivery_flag, order_date, cancellation_date | Guardrail |

### Diagnostic Questions

- Is churn concentrated in the first 30, 60, or 90 days?
- Do discount-acquired customers churn faster than full-price customers?
- Are skipped deliveries a warning sign before cancellation?
- Which cancellation reasons are growing fastest?
- Does email engagement drop before skip or cancellation events?

### Next Data Check

- Confirm whether each order row can be tied to a stable `customer_id`.
- Confirm whether cancelled customers retain their plan price and cancellation date.
- Add gross margin by plan if retention work might increase discounting or shipping cost.
- Add campaign exposure if the team wants to measure lifecycle email impact.

### Recommended First Analysis

Build a churn cohort table by signup month, plan type, discount usage, and first skip event. This will show whether the retention problem is primarily onboarding quality, plan-product fit, promotional acquisition quality, or delivery friction.
