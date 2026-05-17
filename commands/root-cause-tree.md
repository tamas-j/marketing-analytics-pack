---
description: Diagnose why a marketing or business metric changed by building a structured root cause investigation tree.
argument-hint: "<metric, change observed, time period, segments/channels/data available>"
---

# Root Cause Tree

Use this command when a metric moved and the user needs a structured investigation plan.

Use skill: "root-cause-investigation-tree"
Use skill: "data-readiness-checker"
Use skill: "data-visualization"

## Workflow

1. Restate the metric movement and time period.
2. Ask for the minimum missing context:
   - metric definition
   - baseline period and comparison period
   - business model or journey stage
   - available dimensions, such as channel, campaign, product, region, audience, device, or cohort
   - any known events, launches, outages, tracking changes, or campaigns
3. Decompose the metric into component drivers.
4. Build a root cause tree with likely branches:
   - mix shift
   - volume change
   - rate change
   - value change
   - audience or customer quality
   - seasonality or external factors
   - operational or product changes
   - measurement or tracking changes
5. Prioritise the branches by likely impact and ease of validation.
6. Recommend the first cuts, tables, or charts to run.
7. Include caveats about causality and measurement limits.

## Output Format

Return:

1. Metric movement summary
2. Root cause tree
3. Prioritised investigation plan
4. Data needed
5. First cuts to run
6. Likely explanations to validate
7. Watch-outs and caveats

## Guardrails

- Do not jump to one explanation without decomposing the metric.
- Separate real performance changes from tracking or definition changes.
- Prefer component checks before complex modelling.
- Do not imply causality from descriptive cuts.
- Make the first investigation step small enough to run quickly.
