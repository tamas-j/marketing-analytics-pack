---
description: Design a practical incrementality test for campaigns, channels, offers, CRM journeys, or media using holdouts, geo tests, matched markets, or switchbacks.
argument-hint: "<campaign/channel, goal, audience, geography, budget, constraints, available data>"
---

# Incrementality Test Designer

Use this command when the user needs to know whether marketing activity caused additional outcomes, not just attributed outcomes.

Use skill: "incrementality-test-designer"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the causal question.
2. Identify the intervention, outcome, population, and decision.
3. Ask for the minimum missing context:
   - whether random holdout is possible
   - geography or audience structure
   - campaign dates and budget
   - outcome metric and expected lag
   - contamination risks
   - historical data available
4. Recommend a design:
   - user-level holdout
   - geo holdout or matched market
   - switchback
   - PSA/control creative
   - difference-in-differences
5. Define assignment, measurement window, guardrails, and analysis readout.
6. Flag limitations and operational requirements.

## Output Format

Return:

1. Incrementality question
2. Recommended design
3. Test setup
4. Data requirements
5. Analysis plan
6. Risks and mitigations
7. Decision rule

## Guardrails

- Do not claim incrementality from platform attribution alone.
- Recommend the simplest credible design.
- Flag contamination and spillover risks.
- Include customer experience, revenue quality, and margin guardrails.
- If a true test is not feasible, explain the strongest available quasi-experimental fallback.
