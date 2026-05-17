---
description: Build a suppression waterfall that explains how a marketing audience is reduced by eligibility, consent, contactability, frequency, and business rules.
argument-hint: "<starting audience, suppression rules, counts, channel, campaign goal>"
---

# Suppression Waterfall

Use this command when the user needs to explain why an audience, campaign list, or eligible customer pool shrinks before activation.

Use skill: "suppression-waterfall-builder"
Use skill: "data-visualization"

## Workflow

1. Restate the starting audience and campaign/channel goal.
2. Ask for the suppression rules and counts, or the fields needed to calculate them.
3. Order rules in a defensible sequence:
   - starting population
   - eligibility
   - consent and legal exclusions
   - contactability
   - business exclusions
   - frequency or fatigue
   - recent purchase or conversion
   - channel-specific exclusions
   - final reachable audience
4. Calculate removed count, remaining count, and removal rate for each step.
5. Flag unusually large losses, overlapping rules, and unclear definitions.
6. Recommend a waterfall chart or step table using the shared visual style.

## Output Format

Return:

1. Audience summary
2. Suppression waterfall table
3. Biggest loss points
4. Data quality checks
5. Recommended fixes or decisions
6. Visual recommendation

## Guardrails

- Do not treat suppression loss as bad by default; many exclusions protect users and performance.
- Separate legal/consent exclusions from business optimisation rules.
- Flag rule overlap if counts are not applied sequentially.
- Do not recommend bypassing consent, compliance, or safety exclusions.
