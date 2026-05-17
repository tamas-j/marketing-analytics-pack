# Segmentation Method Example

## Prompt

```text
/segmentation-method We run an ecommerce skincare brand and want customer segments for lifecycle email. We have customer_id, order dates, net revenue, product category, discount code, and email engagement.
```

## Example Output

## Segmentation Method Recommendation

### Goal

Create actionable lifecycle email segments for ecommerce customers.

### Recommended Method

Start with a hybrid lifecycle + RFM segmentation.

### Why This Fits

Lifecycle email needs segments that are easy to explain and activate. RFM captures value and purchase timing, while lifecycle rules make the segments usable for journeys such as onboarding, second purchase, retention, and winback.

### Required Data

- `customer_id`
- `order_date`
- `net_revenue`
- `order_status`
- `product_category`
- `discount_code`
- email engagement fields

### Segment Output Shape

| Segment | Rule or definition | Use case |
|---|---|---|
| New customers | first purchase in last 30 days | onboarding and second purchase |
| Champions | recent, frequent, high value | loyalty and referrals |
| At risk | previously frequent or high value, not recent | winback |
| Discount-led | high discount use, moderate value | margin-aware offers |

### Caveats and Guardrails

- RFM should exclude cancelled and fully refunded orders.
- Email eligibility and consent must be checked before activation.
- Discount-led segments need margin guardrails.

### Next Step

Run `/rfm-segment` to define scoring rules, then use `/persona-to-segment` if qualitative personas need to be layered in.
