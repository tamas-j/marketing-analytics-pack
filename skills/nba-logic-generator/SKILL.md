---
name: nba-logic-generator
description: Use when designing next-best-action, next-best-offer, journey prioritisation, eligibility, suppression, fallback, guardrail, and measurement logic.
---

# NBA Logic Generator

This skill designs practical next-best-action logic. It is intended for rules-first decisioning that marketing teams can understand, implement, test, and govern.

## Required Inputs

Ask only for what is missing:

- Business objective.
- Action or offer catalogue.
- Customer data fields.
- Channel and cadence.
- Eligibility and compliance constraints.
- Prioritisation goal.
- Measurement approach or test design.

## Logic Layers

1. `Eligibility`: can the customer receive this action?
2. `Relevance`: does the customer match the action intent?
3. `Priority`: which eligible action should win?
4. `Suppression`: should we hold back because of consent, fatigue, recent conversion, service issue, or risk?
5. `Fallback`: what happens when no action qualifies or data is missing?
6. `Measurement`: how will we know the logic helped?

## Output Template

```markdown
## Next-Best-Action Logic

### Objective
<goal>

### Action Catalogue
| Action | Intended customer | Success metric | Guardrail |
|---|---|---|---|
| <action> | <customer> | <metric> | <guardrail> |

### Eligibility Rules
- <rule>

### Prioritisation Logic
1. <rule>
2. <rule>
3. <rule>

### Suppression and Guardrails
- <rule>

### Fallback Logic
- <fallback>

### Measurement Plan
- <test or KPI>
```

## Common Prioritisation Patterns

- Value first: prioritise actions with highest expected margin or retained value.
- Need first: prioritise urgent customer need, such as onboarding, payment failure, service issue, or churn risk.
- Journey first: prioritise the next logical lifecycle step.
- Risk first: prioritise actions that reduce churn, complaint, refund, or service risk.
- Simplicity first: choose a small rule set that can be audited.

## Guardrails

- Do not let promotional offers override service or compliance needs.
- Do not optimise short-term conversion at the expense of margin or churn.
- Do not use fields unavailable at decision time.
- Do not create conflicting actions across channels.
- Always define a control or holdout when impact matters.
