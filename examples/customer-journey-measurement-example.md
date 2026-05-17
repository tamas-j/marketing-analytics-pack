# Customer Journey Measurement Example

## Prompt

```text
/customer-journey-measurement We are an ecommerce skincare brand. We want to improve lifecycle performance from first site visit through repeat purchase. Channels include paid social, email, SMS, and organic search. We have sessions, orders, customer IDs, email engagement, discount codes, and product category.
```

## Example Output

## Customer Journey Measurement Framework

### Journey Summary

The journey should focus on turning qualified visitors into first-time buyers, then moving those buyers into repeat purchase without over-relying on discounts. The most important handoff is from first purchase to second purchase, because that is where lifecycle marketing can influence retention and customer quality.

### Measurement Framework

| Stage | Desired customer behavior | Primary KPI | Supporting drivers | Guardrails | Data needed | Diagnostic cuts |
|---|---|---|---|---|---|---|
| Acquisition | Reach the site with purchase intent | Qualified sessions | Sessions, channel mix, product page view rate | Bounce rate, low-quality traffic | session_id, customer_id or visitor_id, channel, landing_page, session_date | channel, campaign, landing page, device |
| Activation | Engage with skincare products or education | Product engagement rate | Product page views, quiz starts, email signup rate | Email signup quality, duplicate leads | session_id, product_page_view, quiz_start, email_signup | product category, traffic source, new vs returning |
| Conversion | Complete first purchase | First purchase conversion rate | Add-to-cart rate, checkout completion, discount usage | Refund rate, discount rate, gross margin | customer_id, order_id, order_date, order_status, discount_code, net_revenue | channel, campaign, product category, discount code |
| Retention | Return for a second purchase | 90-day repeat purchase rate | Email click rate, replenishment timing, product category mix | Unsubscribe rate, refund rate, margin after discount | customer_id, order_date, email_click, product_category, refund_amount | first product category, first discount, lifecycle segment |
| Expansion | Increase basket or category breadth | Repeat order value | Cross-sell rate, bundle take-up, units per order | Return rate, discount dependency | order_id, customer_id, product_category, units, net_revenue | category, cohort month, prior purchase count |
| Reactivation | Bring lapsed customers back | Winback rate | Winback email engagement, lapse duration, offer usage | Complaint rate, margin after incentive | customer_id, last_order_date, campaign_id, email_click, order_date | lapse band, offer, category, prior value |

### Measurement Gaps

- Visitor-to-customer stitching may be incomplete if anonymous sessions cannot connect to later orders.
- Gross margin is not listed, so discount-led repeat purchases may look better than they are.
- SMS engagement is mentioned as a channel but not listed in the available data.

### Diagnostic Questions

- Which acquisition channels produce the highest 90-day repeat purchase rate?
- Do discount-acquired customers repeat without another discount?
- Which first product categories have the strongest second-purchase behavior?
- Does email engagement drop before customers lapse?
- Are repeat purchases happening on a natural replenishment cycle?

### Recommended First Analysis

Build a cohort table for first-time buyers by acquisition channel, first product category, and discount usage, then measure 90-day repeat purchase rate and repeat order value. This will show whether the lifecycle issue is traffic quality, first-product fit, offer dependency, or post-purchase engagement.
