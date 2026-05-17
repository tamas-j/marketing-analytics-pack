---
description: Create a marketing campaign post-mortem covering goal, performance, drivers, learnings, caveats, and next actions.
argument-hint: "<campaign, goal, dates, channels, budget, results, available data>"
---

# Campaign Post-Mortem

Use this command when the user needs to explain what happened in a completed campaign and what to do next.

Use skill: "campaign-post-mortem-generator"
Use skill: "root-cause-investigation-tree"

## Workflow

1. Restate the campaign goal, audience, dates, and channels.
2. Ask for the minimum missing context:
   - budget or spend
   - target KPI
   - actual results
   - comparison period, target, forecast, or holdout
   - major changes, issues, or external context
3. Compare results against the right baseline.
4. Decompose performance into delivery, engagement, conversion, value, quality, and measurement factors.
5. Separate what is known from what is plausible.
6. Summarise learnings, caveats, and follow-up analyses.
7. Recommend next actions for creative, audience, budget, measurement, and testing.

## Output Format

Return:

1. Executive summary
2. Campaign context
3. Performance scorecard
4. Driver analysis
5. What worked
6. What did not work
7. Caveats and measurement limits
8. Recommendations
9. Next test or analysis

## Guardrails

- Do not claim incrementality without a credible comparison.
- Separate platform-reported performance from business outcomes.
- Include quality and profitability guardrails, not just volume.
- Do not over-generalise from one campaign.
- Make recommendations specific enough to brief the next campaign.
