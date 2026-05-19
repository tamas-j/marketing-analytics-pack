---
description: Turn a marketing KPI or metric idea into a precise spec card with formula, grain, caveats, data requirements, and QA checks.
argument-hint: "<metric name, business context, intended use, available fields>"
---

# Metric Spec Card

Use this command when the user needs a single metric defined clearly enough for a dashboard, analysis brief, stakeholder review, or data request.

Use skill: "metric-spec-card-generator"

## Workflow

1. Restate the metric and what decision it supports.
2. Ask for the minimum missing context:
   - business model or product
   - metric purpose
   - intended audience or owner
   - available fields or current definition
   - reporting grain and cadence
3. Classify the metric as outcome, driver, input, quality, or guardrail.
4. Write a clear definition and formula.
5. Specify grain, filters, inclusions, exclusions, and dimensions.
6. List data requirements and likely source tables or files.
7. Add interpretation notes, caveats, and common failure modes.
8. Add QA checks the user can run before trusting the metric.

## Output Format

Return a metric spec card with:

1. Metric name
2. Purpose
3. Metric type
4. Plain-English definition
5. Formula
6. Grain
7. Required fields
8. Filters and exclusions
9. Useful dimensions
10. Interpretation notes
11. Caveats and guardrails
12. QA checks
13. Example calculation, if enough detail is available

## Guardrails

- Do not leave formulas ambiguous. Define numerator, denominator, and time window.
- Separate the metric definition from how it should be interpreted.
- Make exclusions explicit, especially refunds, cancellations, test records, bots, internal users, and duplicate events.
- If the current definition is flawed, preserve it as "current definition" and propose a cleaner version.
- Keep the card understandable for a marketing or analytics practitioner — definitions in plain language even when the underlying SQL is non-trivial.
