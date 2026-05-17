---
name: attribution-model-selector
description: Use when choosing or critiquing marketing attribution approaches, including rules-based attribution, data-driven attribution, MMM, incrementality tests, and blended measurement frameworks.
---

# Attribution Model Selector

This skill helps users choose an attribution approach that fits the decision and data. It is deliberately careful about the difference between attribution and incrementality.

## Required Inputs

Ask only for what is missing:

- Decision to support.
- Channels and touchpoints.
- Conversion event.
- Journey length and buying cycle.
- Tracking and ID coverage.
- Offline, cross-device, or walled-garden constraints.
- Whether the user needs reporting, optimisation, or causal budget allocation.

## Method Guide

| Approach | Best for | Data needed | Main limitation |
|---|---|---|---|
| Last touch | simple reporting and ops | conversion path or source | overcredits lower funnel |
| First touch | acquisition source reporting | first touch ID | ignores nurture and conversion |
| Position-based | simple journey credit | ordered touchpoints | arbitrary weights |
| Rules-based custom | stakeholder-aligned reporting | touchpoint data | not causal |
| Data-driven attribution | platform optimisation | rich path data | black box, biased by tracking |
| Incrementality testing | causal campaign impact | holdout/geo/control design | operational complexity |
| MMM | budget allocation across channels | time series spend/outcome data | needs history and assumptions |
| Blended framework | mature measurement | multiple sources | governance needed |

## Output Template

```markdown
## Attribution Approach Recommendation

### Attribution Question
<decision>

### Recommended Approach
<approach>

### Why This Fits
<rationale>

### Data Requirements
- <field or source>

### Limitations
- <limitation>

### If You Need Incrementality
<experiment/MMM recommendation>

### Next Step
<practical next action>
```

## Guardrails

- Attribution assigns credit; it does not prove what would have happened without marketing.
- Platform attribution can be useful for optimisation but may overstate business impact.
- Do not recommend user-level attribution if IDs are fragmented or consent limits tracking.
- Do not use attribution alone for major budget shifts when experiments or MMM are feasible.
