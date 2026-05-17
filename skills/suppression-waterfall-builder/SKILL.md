---
name: suppression-waterfall-builder
description: Use when creating an audience suppression waterfall with eligibility, consent, contactability, business rules, fatigue, removals, remaining counts, and optimisation recommendations.
---

# Suppression Waterfall Builder

This skill explains how a starting audience becomes a final reachable campaign audience. It is useful for campaign planning, CRM operations, lifecycle marketing, and stakeholder explanations.

## Required Inputs

Ask only for what is missing:

- Starting audience definition and count.
- Channel or campaign.
- Suppression rules.
- Counts removed by each rule, or fields needed to calculate them.
- Whether counts are sequential or independent.
- Consent, compliance, and eligibility constraints.

## Suppression Rule Order

Use this default order unless the user gives a known operations sequence:

1. Starting population
2. Product or campaign eligibility
3. Legal basis, consent, and privacy exclusions
4. Contactability and deliverability
5. Business rules, such as VIP exclusions, recent support issue, credit risk, or employee/test account
6. Recent conversion or purchase exclusions
7. Frequency cap or fatigue rules
8. Channel-specific exclusions
9. Final reachable audience

## Output Template

```markdown
## Suppression Waterfall

### Audience Summary
<starting audience, channel, and goal>

### Waterfall Table
| Step | Rule | Removed | Remaining | Removal rate | Notes |
|---|---|---:|---:|---:|---|
| 0 | Starting audience | - | <count> | - | <note> |

### Biggest Loss Points
- <rule and interpretation>

### Data Quality Checks
- <check>

### Recommended Fixes or Decisions
- <recommendation>

### Visual Recommendation
<waterfall chart or ranked removal bar chart>
```

## Interpretation Guide

- Large consent/contactability losses are often data capture or preference-centre issues.
- Large recent-purchase suppressions may be intentional journey control.
- Large frequency suppressions can indicate over-contacting or poor campaign prioritisation.
- Overlapping rules need sequential logic or unique suppressed IDs to avoid double counting.

## Guardrails

- Never suggest weakening consent or compliance exclusions.
- Do not add independent suppression counts together as if they are sequential.
- Do not optimise for audience size alone; quality and customer experience matter.
- Always separate reachable audience from eligible audience.
