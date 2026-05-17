---
description: Diagnose marketing contact frequency, fatigue risk, channel pressure, and practical frequency cap recommendations.
argument-hint: "<channel, sends/impressions, customer IDs, engagement, opt-outs, conversions, time window>"
---

# Frequency Cap Fatigue

Use this command when the user wants to understand over-contact, fatigue, saturation, or frequency cap rules.

Use skill: "frequency-cap-fatigue-analyser"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the channel, audience, and time window.
2. Ask for the minimum missing data:
   - customer or user ID
   - send/impression/contact timestamps
   - channel or campaign
   - opens/clicks/conversions
   - unsubscribes, complaints, opt-outs, or negative events
3. Define contact frequency bands.
4. Compare engagement, conversion, and negative signals by frequency band.
5. Flag saturation, fatigue, and vulnerable segments.
6. Recommend frequency caps, priority rules, and test design.

## Output Format

Return:

1. Fatigue question
2. Data readiness
3. Frequency bands
4. Readout by band
5. Recommended cap or rule
6. Guardrails and test plan

## Guardrails

- Do not recommend a cap from engagement alone; include negative signals and conversion quality where possible.
- Separate campaign frequency from total customer contact pressure.
- Account for lifecycle stage and customer value.
- Avoid making universal caps when segments behave differently.
