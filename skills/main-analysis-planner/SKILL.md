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
| Root cause diagnosis | "Why did X drop?", "what caused the change?" | Root cause investigation tree |
| Analysis brief | "Plan the analysis", "what cuts should I run?" | Analysis brief generator |
| Segmentation | "Group customers", "find audiences", "who should we target?" | Segmentation method selector |
| RFM | "Recency frequency monetary", "best customers", "lapsed buyers" | RFM segment generator |
| Experimentation | "A/B test", "holdout", "incrementality", "did it work?" | Experiment design reviewer or incrementality test designer |
| Attribution/MMM | "channel contribution", "media mix", "budget allocation" | Attribution model selector or MMM readiness checker |
| Forecasting | "forecast", "predict next month", "seasonality" | Forecast method selector |
| Marketing operations | "taxonomy", "suppression", "frequency cap", "NBA" | Relevant marketing ops command |
| Narrative | "explain the result", "post-mortem", "exec summary" | Analysis brief or campaign post-mortem generator |

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
