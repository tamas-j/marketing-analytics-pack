# Root Cause Tree Example

## Prompt

```text
/root-cause-tree Revenue dropped 18% last week for our ecommerce store. We have sessions, orders, order value, product category, channel, device, discount code, and refunds.
```

## Example Output

## Root Cause Investigation: Weekly Revenue Down 18%

### Movement Summary

Revenue fell 18% last week versus the prior week. Because ecommerce revenue is driven by traffic, conversion, and order value, the first step is to decompose the drop into volume, rate, value, and mix components before assuming a channel or campaign caused it.

### Root Cause Tree

| Branch | Hypothesis | What to check | Evidence that supports it | Priority |
|---|---|---|---|---|
| Traffic volume | Fewer qualified visits reduced orders | Sessions and product page views by channel and day | Sessions fell in the same channels/days as revenue | High |
| Conversion rate | Visitors arrived but purchased at a lower rate | Orders / sessions by channel, device, landing page | Sessions stable but conversion fell | High |
| Average order value | Customers bought lower-value baskets | AOV, units per order, category mix, discount rate | Orders stable but AOV fell | High |
| Channel mix | More traffic came from lower-converting channels | Revenue, sessions, conversion by channel | Total sessions stable but mix shifted to weaker channels | Medium |
| Product/category issue | A major category lost demand or availability | Revenue and conversion by product category | Drop concentrated in one category | Medium |
| Promo/discount issue | Offer changed, expired, or over-discounted | Discount code use, conversion, net revenue | Conversion or AOV changed around discount activity | Medium |
| Refund/returns | Reported net revenue fell because refunds rose | Refund amount and refund count by day/category | Gross orders stable but net revenue fell | Medium |
| Tracking or data issue | Revenue tracking changed or failed | Order counts vs trusted platform totals | Analytics revenue diverges from order system | High if sudden |

### First Cuts to Run

1. Decompose revenue into `sessions x conversion rate x average order value` by day.
2. Compare sessions, conversion, AOV, and revenue by channel.
3. Split the same metrics by device and product category.
4. Check refund amount and discount code usage by day.
5. Reconcile order count and revenue against the ecommerce platform.

### Data Needed

- Date
- Sessions
- Orders
- Revenue or net revenue
- Product category
- Channel
- Device
- Discount code
- Refund amount
- Trusted platform totals for reconciliation

### Likely Explanations to Validate

- Paid traffic volume or quality changed.
- Mobile conversion fell because of checkout friction.
- Product mix shifted toward lower-value categories.
- Refunds or discounting reduced net revenue.
- Tracking or order ingestion changed.

### Watch-outs

- A channel-level drop does not prove the channel caused the decline; it may reflect budget, audience, stock, promo, or tracking changes.
- If revenue is net of refunds, a refund spike can look like a demand drop.
- Compare the same weekdays where possible, because ecommerce revenue often has weekday patterns.
