# Metric Spec Card Example

## Prompt

```text
/metric-spec-card Define repeat purchase rate for our ecommerce retention dashboard. We have customer_id, order_id, order_date, order_status, refund_amount, discount_code, and net_revenue.
```

## Example Output

## Metric Spec Card: Repeat Purchase Rate

### Purpose

Measure whether customers come back after their first order. Use this as a retention driver metric for lifecycle marketing, customer quality, and cohort health.

### Metric Type

Driver

### Definition

The share of new customers in a cohort who place at least one additional completed order within the chosen retention window.

### Formula

`repeat purchase rate = customers with 2+ completed orders within window / new customers in cohort`

Numerator: customers whose first completed order is in the cohort period and who have at least one later completed order within the retention window.

Denominator: customers whose first completed order is in the cohort period.

Time window: define explicitly, such as 30, 60, 90, or 180 days after first order.

### Grain

Customer cohort. Calculate at `customer_id` level, then aggregate by first order cohort period.

### Required Fields

| Field | Why it is needed | Example |
|---|---|---|
| `customer_id` | Identify repeat behavior by customer | `C12345` |
| `order_id` | Count distinct orders | `O98765` |
| `order_date` | Identify first order and repeat window | `2026-03-14` |
| `order_status` | Exclude cancelled or failed orders | `completed` |
| `refund_amount` | Optional guardrail for poor-quality repeats | `0.00` |
| `net_revenue` | Optional value-weighted retention view | `42.50` |

### Filters and Exclusions

- Include completed orders only.
- Exclude cancelled, failed, test, and fully refunded orders.
- Count distinct `order_id` values.
- Treat the first completed order as the cohort-start event.

### Useful Dimensions

- First order month
- Acquisition channel
- Discount code usage
- Product category
- Region
- First order value band

### Interpretation Notes

- Rising repeat purchase rate usually indicates stronger customer quality, onboarding, product fit, or lifecycle activity.
- Falling repeat purchase rate can reflect weaker acquisition quality, product issues, discount-led one-time buyers, or delayed repeat cycles.
- Compare cohorts only after each cohort has had the same amount of time to repeat.

### Caveats and Guardrails

- A 30-day repeat window may understate repeat behavior for products with long replenishment cycles.
- Discount-heavy repeat purchases may improve the rate while hurting margin.
- If guest checkout creates duplicate customer records, repeat purchase rate will be understated.

### QA Checks

- Confirm every `customer_id` can have multiple `order_id` values.
- Check that cancelled and failed orders are excluded.
- Confirm fully refunded orders are not counted as successful repeats.
- Verify that each cohort has aged long enough for the chosen repeat window.
- Reconcile total completed orders against a trusted order report.

### Example Calculation

If 10,000 customers placed their first completed order in January and 2,400 placed at least one additional completed order within 90 days, the 90-day repeat purchase rate is `2,400 / 10,000 = 24%`.
