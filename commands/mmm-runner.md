---
description: Scope and prepare a Google Meridian media mix model run, including inputs, assumptions, outputs, and execution checklist.
argument-hint: "<prepared MMM dataset, outcome, media channels, controls, priors/assumptions, geo/time grain>"
---

# MMM Runner

Use this command to prepare or specify a Google Meridian MMM run. In v1 this is an advanced-runner planning workflow; automated model execution is deferred until the heavy dependency runner is added.

Use skill: "mmm-runner"
Use skill: "mmm-readiness-checker"
Use skill: "data-visualization"

## Workflow

1. Confirm the readiness verdict and modelling scope.
2. Define the model inputs:
   - outcome
   - time index
   - media spend/exposure
   - controls
   - geo/product hierarchy if used
3. Define assumptions:
   - lag/adstock expectations
   - saturation expectations
   - priors or constraints where available
   - train/validation windows
4. Produce an execution checklist for Google Meridian.
5. Define expected outputs and interpretation guardrails.

## Output Format

Return:

1. Model scope
2. Input schema
3. Assumptions and priors
4. Execution checklist
5. Expected outputs
6. Validation checks
7. Caveats

## Guardrails

- Do not pretend the model has run unless actual outputs are provided.
- Keep this as a runner spec until the advanced Google Meridian implementation exists.
- Do not recommend MMM if readiness is blocked.
- Include validation and sanity checks before business recommendations.
