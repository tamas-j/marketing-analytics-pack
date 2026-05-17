# RFM Segment Example

## Prompt

```text
/rfm-segment We have ecommerce orders with customer_id, order_id, order_date, order_status, net_revenue, discount_code, and refund_amount. We want lifecycle segments for email.
```

## Example Output

## RFM Segmentation

### Readiness Verdict

Ready with caveats. The core RFM fields are present, but cancelled, test, duplicate, and fully refunded orders must be excluded before scoring.

### RFM Definitions

| Component | Definition | Field needed |
|---|---|---|
| Recency | days since most recent completed non-refunded order | `order_date`, `order_status`, `refund_amount` |
| Frequency | count of completed non-refunded orders in the last 12 months | `order_id`, `order_status`, `order_date` |
| Monetary | total net revenue from completed non-refunded orders in the last 12 months | `net_revenue`, `refund_amount` |

### Scoring Approach

Use quintiles if the customer base is large enough. Score recency so the most recent customers receive the highest score. Score frequency and monetary so higher values receive higher scores.

### Segment Map

| Segment | Rule | Meaning | Recommended action |
|---|---|---|---|
| Champions | R 4-5, F 4-5, M 4-5 | best current customers | loyalty, referrals, early access |
| New customers | R 5, F 1-2 | recent first-time buyers | onboarding and second purchase |
| Loyal | R 4-5, F 4-5, M 1-3 | frequent but not highest value | cross-sell and basket growth |
| Big spenders | M 5, F 1-3 | high-value but less frequent | premium product journeys |
| At risk | R 1-2, F 4-5 or M 4-5 | valuable customers going quiet | winback and save offers |
| Hibernating | R 1-2, F 1-2, M 1-2 | low recent and historical value | low-cost reactivation or suppression |

### QA Checks

- Confirm each `order_id` belongs to one `customer_id`.
- Exclude cancelled and fully refunded orders.
- Use a fixed analysis date for recency.
- Check segment sizes before activation.
- Compare email eligibility by segment.

### Caveats

- RFM is descriptive, not predictive.
- Discount-heavy customers may look valuable on revenue while being weaker on margin.
- Customers acquired recently have not had the same chance to build frequency.
