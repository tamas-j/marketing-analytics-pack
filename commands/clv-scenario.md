---
description: Model simple customer lifetime value scenarios from revenue, margin, retention, purchase frequency, acquisition cost, and discount assumptions.
argument-hint: "<business model, AOV/ARPU, margin, purchase frequency or churn, CAC, scenario assumptions>"
---

# CLV Scenario

Use this command when the user wants a lightweight customer lifetime value model for planning, prioritisation, or stakeholder discussion.

Use skill: "clv-scenario-modeller"
Use skill: "metric-spec-card-generator"

## Workflow

1. Restate the business question and decision the CLV model should support.
2. Ask for the minimum missing assumptions:
   - business model
   - average order value or ARPU
   - gross margin
   - purchase frequency, retention rate, or churn rate
   - acquisition cost
   - discount or incentive assumptions
   - time horizon
3. Choose the simplest appropriate CLV formula for the business model.
4. Build base, optimistic, and cautious scenarios.
5. Show the assumptions, calculation, CLV, CAC payback, and CLV:CAC ratio.
6. Flag the assumptions with the biggest impact.
7. Add guardrails and data needed to replace assumptions with observed values.

## Output Format

Return:

1. Decision summary
2. Formula used
3. Assumption table
4. Scenario table
5. Sensitivity notes
6. Guardrails and caveats
7. Data needed next
8. Recommended first analysis

## Guardrails

- Keep this as a planning model, not a claim of precise customer value.
- Do not hide the assumptions. Show them before the output values.
- Use gross margin, not revenue, when estimating economic CLV.
- Include acquisition cost and payback where possible.
- Flag when retention, churn, or repeat purchase assumptions are too immature to trust.
- Avoid false precision; round outputs sensibly.
