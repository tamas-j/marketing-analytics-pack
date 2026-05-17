---
name: experiment-design-reviewer
description: Use when reviewing A/B test or experiment designs for hypothesis, control, randomisation unit, metrics, guardrails, sample, duration, instrumentation, and bias risks.
---

# Experiment Design Reviewer

This skill reviews experiment designs before launch. It helps users catch common issues that make tests inconclusive or misleading.

## Required Inputs

Ask only for what is missing:

- Hypothesis.
- Treatment and control.
- Randomisation unit.
- Audience and eligibility.
- Primary metric.
- Guardrail metrics.
- Expected sample size or traffic.
- Duration or measurement window.
- Instrumentation and data source.

## Review Checklist

- Hypothesis is specific and falsifiable.
- Control represents the right counterfactual.
- Randomisation unit matches the decision and prevents interference.
- Eligibility is defined before assignment.
- Primary metric is tied to the decision.
- Guardrail metrics protect customer experience, margin, churn, fatigue, or quality.
- Measurement window is long enough for the expected effect.
- Sample size and minimum detectable effect are plausible.
- Tracking is available for assignment, exposure, and outcome.
- Analysis plan avoids peeking, cherry-picking, and post-hoc segmentation.

## Output Template

```markdown
## Experiment Design Review

### Test Summary
<hypothesis, treatment, control, audience>

### Readiness Verdict
<Ready / Needs fixes / Blocked>

### Design Review
| Area | Assessment | Risk | Fix |
|---|---|---|---|
| <area> | <assessment> | <risk> | <fix> |

### Metrics
Primary metric: <metric>
Guardrails:
- <metric>

### Data and Instrumentation Needs
- <field or event>

### Decision Rule
<how the result will be interpreted>
```

## Guardrails

- Do not treat observational before/after comparisons as randomised tests.
- Do not approve tests where treatment assignment is not logged.
- Do not use downstream metrics as primary if they will not mature during the test.
- Do not recommend sample-size precision without enough inputs; give directional guidance instead.
