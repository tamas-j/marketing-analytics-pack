---
description: Explain likely churn drivers from retention, cohort, engagement, customer quality, and cancellation evidence.
argument-hint: "<churn movement, business model, cohorts, fields, segments, cancellation or engagement data>"
---

# Churn Driver Narrative

Use this command when the user needs a clear narrative explaining why churn or retention changed.

Use skill: "churn-driver-narrative-generator"
Use skill: "root-cause-investigation-tree"

## Workflow

1. Restate the churn or retention movement.
2. Confirm the churn definition: logo, revenue, activity, voluntary, involuntary, or cancellation rate.
3. Ask for the minimum missing context:
   - baseline and comparison periods
   - customer cohorts
   - acquisition channels
   - plan, product, or segment dimensions
   - engagement, support, cancellation, billing, or usage signals
4. Decompose churn into cohort quality, engagement, value, operational, billing, and measurement drivers.
5. Build a ranked narrative of likely drivers.
6. Explain evidence needed to validate or rule out each driver.
7. Recommend first retention analysis and next actions.

## Output Format

Return:

1. Churn movement summary
2. Driver narrative
3. Evidence table
4. Customer segments to inspect
5. Data gaps
6. Recommended first analysis
7. Actions to consider after validation

## Guardrails

- Do not treat churn as one thing; distinguish voluntary, involuntary, activity, logo, and revenue churn.
- Do not compare cohorts before they have had enough time to churn.
- Do not blame lifecycle marketing before checking acquisition quality, product value, billing, and operations.
- Avoid causal language unless supported by experiment or strong design.
