---
description: Select an attribution approach for a marketing question and explain fit, data needs, limitations, and alternatives.
argument-hint: "<marketing question, channels, touchpoints, conversion path, data available, decision>"
---

# Attribution Model Selector

Use this command when the user needs to choose or critique an attribution approach for channels, campaigns, journeys, or conversion paths.

Use skill: "attribution-model-selector"
Use skill: "incrementality-test-designer"

## Workflow

1. Restate the decision attribution is meant to support.
2. Ask for the minimum missing context:
   - channels and touchpoints
   - conversion event
   - journey length
   - ID and tracking coverage
   - offline or cross-device gaps
   - whether incrementality is needed
3. Recommend an attribution approach.
4. Explain what it can and cannot answer.
5. List data requirements and caveats.
6. Recommend next measurement step.

## Output Format

Return:

1. Attribution question
2. Recommended approach
3. Why it fits
4. Data requirements
5. Limitations
6. Better alternatives if the goal is incrementality
7. Next step

## Guardrails

- Do not claim attribution equals incrementality.
- Do not recommend complex models when tracking is weak.
- Flag cross-device, cookie, offline, and platform walled-garden limitations.
- Recommend experiments or MMM when the decision requires causal budget allocation.
