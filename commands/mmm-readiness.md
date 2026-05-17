---
description: Check whether marketing data is ready for media mix modelling and identify gaps, risks, and next fixes.
argument-hint: "<outcome, spend/exposure channels, date grain, history length, controls, business question>"
---

# MMM Readiness

Use this command when the user wants to know whether their marketing data can support media mix modelling.

Use skill: "mmm-readiness-checker"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the MMM decision or budget question.
2. Ask for the minimum missing context:
   - outcome metric
   - date grain and history length
   - media channels and spend/exposure fields
   - controls such as price, promotions, seasonality, holidays, stock, competitor or macro factors
   - geography/product splits if relevant
3. Check MMM readiness:
   - consistent time series
   - enough history and variation
   - media coverage
   - outcome quality
   - control variables
   - spend/outcome timing
   - channel collinearity risk
4. Classify readiness and recommend fixes.

## Output Format

Return:

1. MMM question
2. Readiness verdict
3. Data inventory
4. Gaps and risks
5. Required fixes
6. Recommended modelling scope
7. Next step

## Guardrails

- Do not recommend MMM when history, variation, or outcome quality is insufficient.
- Do not treat platform-attributed conversions as the dependent variable without caveats.
- Flag highly correlated channels and always-on spend.
- Keep Google Meridian as the preferred MMM library for this pack.
