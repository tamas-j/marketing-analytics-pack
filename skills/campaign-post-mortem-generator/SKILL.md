---
name: campaign-post-mortem-generator
description: Use when summarising completed marketing campaign performance, drivers, learnings, caveats, and recommendations for the next campaign or analysis.
---

# Campaign Post-Mortem Generator

This skill creates a practical post-mortem for completed campaigns. It is designed to help marketing teams learn what happened, what evidence supports the interpretation, and what should change next.

## Required Inputs

Ask only for what is missing:

- Campaign name, dates, channels, audience, and objective.
- Target KPI and success threshold.
- Spend, delivery, and result metrics.
- Baseline, target, forecast, prior period, or holdout.
- Conversion, revenue, margin, retention, or quality metrics where available.
- Known issues, changes, launches, promotions, competitor events, or tracking caveats.

If there is no credible comparison group, frame the output as observed performance rather than incremental impact.

## Method

1. Define the goal and success metric.
2. Compare results against target, prior period, forecast, or holdout.
3. Decompose performance:
   - delivery: spend, impressions, reach, frequency
   - engagement: CTR, visits, landing page behavior
   - conversion: leads, purchases, signups, funnel rates
   - value: revenue, AOV, margin, LTV proxy
   - quality: retention, refunds, lead acceptance, repeat behavior
   - measurement: tracking, attribution, windows, data completeness
4. Identify what worked and what did not.
5. Separate evidence from interpretation.
6. Recommend next actions and follow-up tests.

## Output Template

```markdown
## Campaign Post-Mortem: <campaign>

### Executive Summary
<3-5 sentences>

### Campaign Context
| Item | Detail |
|---|---|
| Objective | <objective> |
| Dates | <dates> |
| Channels | <channels> |
| Audience | <audience> |
| Budget | <budget> |

### Performance Scorecard
| Metric | Target/Baseline | Actual | Readout |
|---|---:|---:|---|
| <metric> | <target> | <actual> | <readout> |

### Driver Analysis
| Driver | What happened | Evidence | Confidence |
|---|---|---|---|
| <driver> | <summary> | <evidence> | <High/Medium/Low> |

### What Worked
- <learning>

### What Did Not Work
- <learning>

### Caveats and Measurement Limits
- <caveat>

### Recommendations
- <recommendation>

### Next Test or Analysis
<one focused next step>
```

## Common Post-Mortem Patterns

- Strong platform metrics but weak business outcomes usually point to traffic quality, landing page fit, attribution, or funnel friction.
- Good conversion but weak margin often points to discounting, product mix, or fulfillment/refund costs.
- Strong new customer volume but weak retention points to acquisition quality or expectation mismatch.
- Spend under-delivery can make performance look efficient while failing the business goal.
- Creative fatigue often appears as rising frequency, falling CTR, and rising CPA.

## Guardrails

- Do not equate attributed conversions with incremental conversions.
- Do not ignore audience quality or downstream value.
- Do not compare against a misleading baseline if seasonality, promo, or tracking changed.
- Do not present caveats as afterthoughts; put major measurement limits near the scorecard.
- Keep recommendations tied to evidence.
