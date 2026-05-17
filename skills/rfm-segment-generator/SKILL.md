---
name: rfm-segment-generator
description: Use when designing, reviewing, or interpreting RFM segmentation from customer transaction data with recency, frequency, monetary value, scoring rules, segments, caveats, and activation guidance.
---

# RFM Segment Generator

This skill designs an RFM segmentation. In v1 it is a prompt-first workflow that specifies the logic and interpretation. A future advanced runner can calculate scores directly from files with pandas.

## Required Inputs

Ask only for what is missing:

- Customer identifier.
- Transaction or order date.
- Transaction or order value.
- Order status or eligibility filters.
- Analysis date or period end.
- Business goal and activation channel.

## RFM Definitions

- `Recency`: days since most recent eligible purchase. Lower is better.
- `Frequency`: count of eligible purchases in the observation window. Higher is better.
- `Monetary`: total, average, or margin-adjusted value in the observation window. Higher is usually better.

## Scoring Options

| Approach | Best for | Notes |
|---|---|---|
| Quintiles 1-5 | medium/large customer bases | common, easy to explain |
| Tertiles 1-3 | smaller datasets | less granular, more stable |
| Business thresholds | known lifecycle windows | easiest to activate |
| Hybrid rules | marketing journeys | combines score and domain logic |

## Segment Map Starter

| Segment | Typical rule | Use case |
|---|---|---|
| Champions | high R, high F, high M | loyalty, referrals, early access |
| Loyal | high R, high F | retention and cross-sell |
| Big spenders | high M, medium F | premium offers and care |
| New customers | high R, low F | onboarding and second purchase |
| At risk | low R, historically high F/M | winback and save journeys |
| Hibernating | low R, low F/M | low-cost reactivation or suppression |
| Price-sensitive | high discount use plus medium value | margin-aware targeting |

## Output Template

```markdown
## RFM Segmentation

### Readiness Verdict
<Ready / Usable with caveats / Needs fixes / Blocked>

### RFM Definitions
| Component | Definition | Field needed |
|---|---|---|
| Recency | <definition> | <field> |
| Frequency | <definition> | <field> |
| Monetary | <definition> | <field> |

### Scoring Approach
<quintiles/tertiles/thresholds/hybrid>

### Segment Map
| Segment | Rule | Meaning | Recommended action |
|---|---|---|---|
| <segment> | <rule> | <meaning> | <action> |

### QA Checks
- <check>

### Caveats
- <caveat>
```

## Guardrails

- RFM works best where repeat purchase behavior is meaningful.
- Use a fixed analysis date so recency is consistent.
- Avoid monetary fields that include tax, shipping, refunds, or discounts unless intentionally included.
- Do not over-message at-risk customers without fatigue and margin guardrails.
- Treat RFM as descriptive segmentation, not proof of future behavior.
