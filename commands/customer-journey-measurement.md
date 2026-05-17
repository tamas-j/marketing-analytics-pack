---
description: Build a customer journey measurement framework across lifecycle stages, KPIs, data needs, diagnostics, and guardrails.
argument-hint: "<business model, journey stages, goal, channels, available data>"
---

# Customer Journey Measurement

Use this command when the user wants to measure a customer journey from awareness through acquisition, activation, conversion, retention, reactivation, and advocacy.

Use skill: "customer-journey-measurement-framework"
Use skill: "metric-spec-card-generator"

## Workflow

1. Restate the journey and business goal in plain language.
2. Ask for the minimum missing context:
   - business model or product
   - journey stages in scope
   - key channels or touchpoints
   - target customer or audience
   - available files, fields, or systems
3. Map the journey stages and define the desired customer behavior at each stage.
4. Select 1-3 meaningful KPIs per stage.
5. Classify each KPI as outcome, driver, input, quality, or guardrail.
6. Add required fields, useful dimensions, and common diagnostic cuts.
7. Flag measurement gaps, attribution risks, and handoff issues between stages.
8. Recommend the first analysis or instrumentation fix.

## Output Format

Return:

1. Journey summary
2. Stage-by-stage measurement table
3. Key guardrails
4. Data requirements and gaps
5. Diagnostic questions
6. Recommended first analysis

## Guardrails

- Do not treat the journey as a generic funnel if the business model needs lifecycle or retention stages.
- Keep each stage focused on behavior the business can observe or influence.
- Prefer a small set of useful metrics over a dashboard wish list.
- Separate customer behavior from marketing activity.
- Include guardrails for over-optimizing one stage at the expense of another.
- If attribution is uncertain, state the limitation and recommend a practical proxy or test.
