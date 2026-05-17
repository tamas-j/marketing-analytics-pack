---
description: Turn a marketing analytics question into a clear analysis brief with objective, hypotheses, data needs, cuts, outputs, and decision criteria.
argument-hint: "<business question, decision, audience, data available, deadline>"
---

# Analysis Brief

Use this command when the user needs to plan an analysis before running cuts, modelling, or narrative work.

Use skill: "analysis-brief-generator"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the business decision the analysis should support.
2. Ask for the minimum missing context:
   - audience or stakeholder
   - decision deadline
   - metric or outcome
   - data available
   - constraints or known caveats
3. Define the analysis objective and scope.
4. Write testable hypotheses.
5. Specify data requirements, grain, filters, and dimensions.
6. Recommend analysis steps and outputs.
7. Define what evidence would change the decision.
8. List risks, caveats, and open questions.

## Output Format

Return:

1. Business question
2. Decision to support
3. Scope
4. Hypotheses
5. Data requirements
6. Analysis plan
7. Expected outputs
8. Decision criteria
9. Risks and caveats

## Guardrails

- Do not turn every brief into a modelling project.
- Keep the first analysis small enough to complete.
- Separate "nice to know" from "needed for the decision".
- Make hypotheses testable with the available data.
- State when the data can support correlation but not causality.
