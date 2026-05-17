---
name: segmentation-method-selector
description: Use when choosing a customer, audience, lead, or account segmentation method based on business goal, data availability, activation needs, and interpretability.
---

# Segmentation Method Selector

This skill selects a practical segmentation approach. It helps the user avoid over-complicated clustering when a simpler lifecycle, value, needs, or rules-based segmentation would be more useful.

## Required Inputs

Ask only for what is missing:

- Business goal.
- Unit to segment: customer, lead, account, visitor, subscriber, audience, product buyer, or campaign recipient.
- Activation use: targeting, reporting, lifecycle messaging, sales prioritisation, product strategy, budget allocation, or research.
- Available fields.
- Need for explainability or automation.
- Refresh cadence, if relevant.

## Method Guide

| Method | Best for | Required data | Strength | Watch-out |
|---|---|---|---|---|
| Lifecycle stage | Journey orchestration and reporting | dates, status, activity | easy to explain and activate | can be too broad |
| Value tiers | prioritising profitable customers | revenue, margin, orders | directly commercial | may ignore future potential |
| RFM | ecommerce/customer value quick read | customer_id, order_date, order value | fast and interpretable | weak for non-purchase businesses |
| Behavioral rules | lifecycle and product usage | events, engagement, frequency | actionable | needs clean event definitions |
| Needs/persona translation | connecting research to data | persona traits plus measurable proxies | bridges qual and quant | proxies can be weak |
| Propensity model | prediction and ranking | labelled outcome, history, features | optimises targeting | less transparent, needs validation |
| Clustering | exploratory patterns | rich numeric features | discovers hidden groups | can be hard to activate |
| Audience overlap | channel/list planning | audience membership flags | reduces duplication | needs consistent IDs |

## Output Template

```markdown
## Segmentation Method Recommendation

### Goal
<goal>

### Recommended Method
<method>

### Why This Fits
<2-4 sentences>

### Required Data
- <field>

### Segment Output Shape
| Segment | Rule or definition | Use case |
|---|---|---|
| <segment> | <definition> | <use> |

### Caveats and Guardrails
- <risk>

### Next Step
<command or analysis>
```

## Guardrails

- Do not recommend a method that cannot be activated or explained to the intended user.
- Do not build segments from fields that would not be available at targeting time.
- Do not compare segment performance without considering size and eligibility.
- Do not call a persona a segment until it has measurable rules or proxies.
