---
description: Review an A/B test or experiment design for hypothesis clarity, randomisation, metrics, sample, bias, and decision rules.
argument-hint: "<test idea, audience, unit, variants, metric, duration, sample size, constraints>"
---

# Experiment Design Reviewer

Use this command when the user wants to sanity-check an experiment before launch or diagnose weaknesses in a proposed A/B test.

Use skill: "experiment-design-reviewer"
Use skill: "metric-spec-card-generator"

## Workflow

1. Restate the test hypothesis and decision.
2. Ask for the minimum missing design details:
   - treatment and control
   - randomisation unit
   - target audience
   - primary metric and guardrails
   - expected duration
   - sample size or traffic
   - exposure and measurement windows
3. Review design risks:
   - unclear hypothesis
   - weak control
   - wrong randomisation unit
   - contamination or spillover
   - insufficient sample
   - metric mismatch
   - peeking or early stopping
   - instrumentation gaps
4. Recommend fixes and a launch-readiness verdict.

## Output Format

Return:

1. Test summary
2. Readiness verdict
3. Design review table
4. Metric and guardrail review
5. Data and instrumentation needs
6. Risks and fixes
7. Decision rule

## Guardrails

- Do not approve a test without a measurable primary metric.
- Do not ignore randomisation unit or contamination risks.
- Do not recommend many primary metrics.
- Flag when the test is really an incrementality or geo/holdout problem rather than a simple A/B test.
