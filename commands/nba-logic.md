---
description: Design next-best-action logic with eligibility rules, prioritisation, guardrails, fallback actions, and measurement.
argument-hint: "<business goal, actions/offers, customer data, channel, constraints>"
---

# NBA Logic

Use this command when the user wants next-best-action, next-best-offer, journey prioritisation, or customer decisioning logic.

Use skill: "nba-logic-generator"
Use skill: "segmentation-method-selector"

## Workflow

1. Restate the customer decision and business goal.
2. Ask for the minimum missing context:
   - available actions or offers
   - customer data and eligibility fields
   - channel and cadence
   - business constraints
   - guardrails, such as consent, margin, fatigue, service, or risk
3. Define action eligibility.
4. Define prioritisation rules.
5. Add suppression, frequency, and conflict rules.
6. Add fallback actions for missing data or no eligible action.
7. Define measurement and test approach.

## Output Format

Return:

1. NBA objective
2. Action catalogue
3. Eligibility rules
4. Prioritisation logic
5. Suppression and guardrails
6. Fallback logic
7. Measurement plan

## Guardrails

- Do not recommend an action a user cannot receive or is not eligible for.
- Separate eligibility from prioritisation.
- Include fallback logic for missing data.
- Include customer experience and margin guardrails.
- Avoid black-box decisioning unless the user has validation and governance.
