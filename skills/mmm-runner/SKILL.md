---
name: mmm-runner
description: Use when scoping or preparing an advanced Google Meridian media mix model run, including input schema, assumptions, priors, validation, outputs, and execution checklist.
---

# MMM Runner

This skill prepares a Google Meridian media mix model run. In v1 it is a specification workflow, not an automated execution runner. A future advanced runner can install and run Meridian once the plugin adds heavy dependency support.

## Required Inputs

Ask only for what is missing:

- Prepared MMM dataset or schema.
- Outcome metric.
- Time grain and date field.
- Media channels and spend/exposure fields.
- Controls.
- Geo or market structure, if any.
- Train and validation windows.
- Business question.

## Runner Scope

The runner spec should define:

- input schema
- model scope
- transformations
- lag/adstock assumptions
- saturation expectations
- controls
- validation plan
- expected outputs
- interpretation guardrails

## Output Template

```markdown
## Google Meridian MMM Runner Spec

### Model Scope
<scope>

### Input Schema
| Field | Role | Grain | Notes |
|---|---|---|---|
| <field> | <role> | <grain> | <notes> |

### Assumptions and Priors
- <assumption>

### Execution Checklist
1. <step>
2. <step>
3. <step>

### Expected Outputs
- contribution by channel
- ROI or marginal ROI
- response curves
- uncertainty intervals
- fit diagnostics
- budget scenario recommendations

### Validation Checks
- <check>

### Caveats
- <caveat>
```

## Guardrails

- Do not create fake model results.
- Do not hide uncertainty or identifiability issues.
- Do not model channels that lack meaningful variation without caveats.
- Do not recommend budget moves before diagnostics and result interpretation.
- Keep Google Meridian as the named implementation target for this pack.
