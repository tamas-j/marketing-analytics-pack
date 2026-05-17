---
description: Choose the right segmentation approach for a marketing question, audience, dataset, and activation goal.
argument-hint: "<business goal, customer/audience context, available fields, activation need>"
---

# Segmentation Method

Use this command when the user wants to segment customers, leads, audiences, or accounts but is unsure which method fits the goal and data.

Use skill: "segmentation-method-selector"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the segmentation goal and intended use.
2. Ask for the minimum missing context:
   - business model
   - customer or audience unit
   - activation channel or decision
   - available behavioral, value, lifecycle, demographic, or campaign fields
   - whether the user needs explainability, actionability, or predictive lift
3. Check whether the dataset grain supports segmentation.
4. Recommend the best method and one fallback method.
5. Explain data needs, outputs, caveats, and activation risks.
6. Recommend the next command or analysis step.

## Output Format

Return:

1. Segmentation goal
2. Recommended method
3. Why it fits
4. Required data
5. Segment output shape
6. Caveats and guardrails
7. Next step

## Guardrails

- Do not recommend clustering just because the user says "segments".
- Prefer interpretable rules when the goal is activation or stakeholder alignment.
- Recommend RFM only when recency, frequency, and monetary fields exist.
- Separate descriptive segments from predictive propensity models.
- Flag when segments cannot be activated in the user's channels.
