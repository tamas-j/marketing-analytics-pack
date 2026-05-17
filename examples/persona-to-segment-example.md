# Persona To Segment Example

## Prompt

```text
/persona-to-segment Persona: "Ingredient researchers" are skincare customers who read educational content, compare product ingredients, buy slowly, and respond to expert proof rather than discounts. We have content views, product category, order history, email clicks, and discount code usage.
```

## Example Output

## Persona-To-Segment Translation

### Persona Summary

Ingredient researchers are high-consideration customers who show education-led behavior before buying and may respond better to proof, content, and expert guidance than price-led offers.

### Segment Definition

Customers or visitors with repeated educational content engagement, ingredient-focused product browsing, slower purchase cycles, and low discount dependency.

### Proxy Field Map

| Persona trait | Measurable proxy | Field needed | Proxy strength |
|---|---|---|---|
| Reads educational content | 2+ educational content views in 30 days | content_type, content_view_date | Strong |
| Compares ingredients | visits ingredient or product detail pages | page_category, product_category | Medium |
| Buys slowly | longer time from first visit/email click to order | first_touch_date, order_date | Medium |
| Not discount-led | no or low discount code usage | discount_code | Medium |
| Responds to expert proof | clicks expert/education emails | email_click, campaign_type | Medium |

### Segment Rules

Include:
- 2+ educational content views in the last 30 days.
- At least one product or ingredient page view.
- Email eligible or reachable in the intended channel.

Exclude:
- Customers whose only recent engagement is discount campaign clicks.
- Customers without consent for lifecycle email.

### Validation Checks

- Compare conversion rate and AOV against other engaged visitors.
- Compare response to education-led campaigns versus discount-led campaigns.
- Check whether the segment is large enough for activation.

### Activation Notes

- Use expert proof, ingredient explainers, routines, and product comparison content.
- Avoid defaulting to discounts unless the customer shows cart or purchase intent.

### Caveats

- Content views are a proxy for research intent, not proof of motivation.
- Anonymous browsing may be hard to connect to later purchase without stable IDs.
