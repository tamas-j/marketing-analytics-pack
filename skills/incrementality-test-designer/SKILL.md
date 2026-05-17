---
name: incrementality-test-designer
description: Use when designing incrementality tests for marketing campaigns, channels, CRM journeys, offers, or media using holdouts, geo tests, matched markets, switchbacks, or quasi-experimental fallbacks.
---

# Incrementality Test Designer

This skill designs practical incrementality tests. It helps users answer "what happened because of this marketing activity?" rather than "what did the platform attribute?"

## Required Inputs

Ask only for what is missing:

- Intervention: campaign, channel, journey, offer, budget change, or treatment.
- Outcome metric.
- Population or market.
- Whether random holdout is possible.
- Geography or audience structure.
- Campaign timing.
- Historical data.
- Operational constraints.

## Design Options

| Design | Best for | Requirements | Watch-out |
|---|---|---|---|
| User-level holdout | CRM, lifecycle, owned channels | stable IDs and ability to suppress | contamination across channels |
| Geo holdout | paid media, offline, broad campaigns | enough comparable geos | market differences |
| Matched markets | campaigns where random geo split is not possible | historical geo data | weaker than randomisation |
| Switchback | time-based operations or auctions | repeated on/off periods | seasonality and carryover |
| PSA/control creative | media platforms | control creative accepted by platform | control may still have effects |
| Difference-in-differences | quasi-experimental fallback | pre/post and comparison group | parallel trend assumption |

## Output Template

```markdown
## Incrementality Test Design

### Question
<causal question>

### Recommended Design
<design and why>

### Test Setup
| Element | Recommendation |
|---|---|
| Population | <population> |
| Treatment | <treatment> |
| Control | <control> |
| Outcome | <metric> |
| Window | <window> |

### Data Requirements
- <field>

### Analysis Plan
1. <step>
2. <step>
3. <step>

### Risks and Mitigations
- <risk and mitigation>

### Decision Rule
<what result would change the decision>
```

## Guardrails

- Do not present attribution, matched markets, or before/after as equivalent to randomised holdout.
- Do not ignore spillover between treatment and control.
- Do not use a control group that can still receive the same treatment elsewhere.
- Do not use outcomes that mature after the measurement window without caveats.
