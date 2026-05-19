---
description: Build a marketing KPI tree that connects a business goal to measurable drivers, diagnostic questions, and next data checks.
argument-hint: "<business goal, product/channel context, target audience, optional data columns>"
---

# KPI Tree

Use this command when the user wants to turn a broad business goal into a practical measurement framework.

Use skill: "kpi-tree-generator"
Use skill: "data-visualization"

## Workflow

1. Restate the user's goal in one sentence.
2. If the goal is vague, ask for the minimum missing context:
   - the business model or product
   - the target outcome, such as revenue, retention, acquisition, conversion, or engagement
   - the main channel, journey, or audience in scope
   - whether they already have a dataset or are still planning measurement
3. Build the KPI tree from top to bottom:
   - North-star outcome
   - level 1 drivers
   - level 2 levers
   - measurable KPIs
   - formulas or measurement definitions
   - data needed
4. Flag which metrics are leading indicators, lagging indicators, input metrics, or guardrails.
5. Add diagnostic questions that help the user decide where to investigate first.
6. Add a short "next data check" section that tells the user what columns or cuts they need before analysis.
7. Produce a compact visual summary using the `data-visualization` style loading pattern. Use `default` unless the user has selected another style.

## Output Format

Return:

1. A short executive summary.
2. A KPI tree table with columns:
   - Level
   - Metric or driver
   - Why it matters
   - Formula or definition
   - Data needed
   - Metric type
3. A visual KPI tree or ranked driver chart.
4. Diagnostic questions.
5. Recommended first analysis.

## Guardrails

- Keep the framework practical for a marketing or analytics practitioner — analyst, marketer, growth/lifecycle owner, or product owner — not just a data engineer.
- Do not treat every available metric as important. Prefer 6-12 meaningful metrics.
- Separate business outcomes from activity metrics.
- Include guardrails where optimizing the main KPI could create bad behavior.
- Avoid claiming causality unless the user has experiment or incrementality evidence.
- If no data is available yet, design the tree anyway and mark data requirements clearly.
