---
name: main-analysis-planner
description: Use when a user has a marketing analytics question but needs help choosing the right workflow, command, data check, or sequence of analysis steps.
---

# Main Analysis Planner

This skill is the front door for the pack. It turns an ambiguous marketing or analytics request into a small, practical plan and routes the user to the right command.

## Required Inputs

Ask only for missing essentials:

- Business question or decision to support.
- Business model or product context.
- Target outcome or metric, if known.
- Available data, file names, or pasted column names.
- Time period, audience, channel, campaign, or market in scope.

If the user gives a vague request, infer the likely intent and state assumptions.

## Intent Classifier

| Intent | User language | Best route |
|---|---|---|
| Metric design | "What should we measure?", "define KPIs", "build a framework" | `/kpi-tree` |
| Data readiness | "Can this file support...", "is my data enough?", "check columns" | `/check-data` |
| Root cause diagnosis | "Why did X drop?", "what caused the change?" | `/root-cause-tree` |
| Analysis brief | "Plan the analysis", "what cuts should I run?" | `/analysis-brief` |
| Segmentation | "Group customers", "find audiences", "who should we target?" | `/segmentation-method` |
| RFM | "Recency frequency monetary", "best customers", "lapsed buyers" | `/rfm-segment` |
| Experimentation | "A/B test", "holdout", "incrementality", "did it work?" | `/experiment-design-reviewer` or `/incrementality-test-designer` |
| Attribution/MMM | "channel contribution", "media mix", "budget allocation" | `/attribution-model-selector` or `/mmm-readiness` |
| Forecasting | "forecast", "predict next month", "seasonality" | `/forecast-method` |
| Marketing operations | "taxonomy", "suppression", "frequency cap", "NBA" | `/marketing-taxonomy-auditor`, `/suppression-waterfall`, `/frequency-cap-fatigue`, or `/nba-logic` |
| Narrative | "explain the result", "post-mortem", "exec summary" | `/analysis-brief` or `/campaign-post-mortem` |

## Question Type Classifier

Use this before routing when the user's request is fuzzy:

| Question type | User is really asking | Best first move |
|---|---|---|
| Framework | "What should we measure?" | `/kpi-tree` or `/customer-journey-measurement` |
| Descriptive | "What happened?" | `/analysis-brief` after `/check-data` if data is involved |
| Diagnostic | "Why did it happen?" | `/root-cause-tree` |
| Causal | "Did this cause lift?" | `/incrementality-test-designer` or `/experiment-design-reviewer` |
| Predictive | "What will happen next?" | `/forecast-method` |
| Packaging | "Can I share this?" | `/report` |

## Routing Examples

- If the user has a broad goal but no metric definition, start with `/kpi-tree`, then `/metric-spec-card` for the most important KPI.
- If the user has a file and asks whether an analysis is possible, start with `/check-data`, then route based on the verdict.
- If the user asks whether a campaign "worked" but has no control or holdout, use `/campaign-post-mortem` for descriptive readout and `/incrementality-test-designer` for the next causal test.
- If the user has model outputs or charts and needs stakeholder-ready material, use `/report`.

## Planning Method

1. Translate the request into one business decision.
2. Identify whether the user needs a framework, a data check, an analysis, a model, or a narrative.
3. Check whether the dataset exists and whether readiness matters before analysis.
4. Pick the smallest useful next step.
5. Name the command to run and explain why.
6. Give a short sequence, usually no more than three steps.

## Output Template

```markdown
## Analysis Plan

### Question Understood
<one sentence>

### Best Next Step
<command or workflow>

### Why This Fits
<2-4 sentences>

### What I Need From You
- <input>

### Data Readiness
<Ready / Partial / Blocked / Not applicable, with a short reason>

### Suggested Sequence
1. <step>
2. <step>
3. <step>
```

## Guardrails

- Do not send the user into complex modeling when their goal is still a measurement design problem.
- Do not recommend MMM, forecasting, RFM, or experimentation until data grain and fields are plausible.
- If the best command is not built yet, say so plainly and offer the closest available route.
- Prefer one strong recommendation over a menu of options.
- Keep the plan actionable for a marketing or analytics practitioner — name the command, name the fields, name the next concrete step.
