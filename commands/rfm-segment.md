---
description: Design or interpret RFM segmentation from recency, frequency, and monetary value fields, with scoring rules and action guidance.
argument-hint: "<customer_id, order date, order value fields, scoring approach, activation goal>"
---

# RFM Segment

Use this command when the user wants a recency-frequency-monetary segmentation for ecommerce, retail, donation, or repeat purchase data.

Use skill: "rfm-segment-generator"
Use skill: "data-readiness-checker"

## Workflow

1. Confirm the business goal and customer unit.
2. Check required fields:
   - customer ID
   - order or transaction date
   - order or transaction value
   - order status or eligibility filters
3. Define recency, frequency, and monetary calculations.
4. Recommend scoring approach: quintiles, tertiles, rules, or custom thresholds.
5. Map RFM scores into named segments.
6. Explain activation use cases and guardrails.
7. Note that this v1 command designs and interprets RFM; a heavier pandas runner can be added later.

## Output Format

Return:

1. RFM readiness verdict
2. RFM definitions
3. Scoring approach
4. Segment map
5. Activation recommendations
6. Caveats and QA checks

## Guardrails

- Do not use RFM if purchases are one-off or frequency has little meaning.
- Do not compare customers with incomplete observation windows without caveats.
- Exclude cancelled, test, duplicate, and fully refunded transactions where relevant.
- Use monetary value only after clarifying gross revenue, net revenue, or margin.
- Do not treat RFM as a predictive model.
