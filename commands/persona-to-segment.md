---
description: Translate qualitative personas or ICPs into measurable audience segment rules, proxy fields, and validation checks.
argument-hint: "<persona description, business model, available fields, activation channel>"
---

# Persona To Segment

Use this command when the user has qualitative personas, ICPs, or audience descriptions and needs measurable segment definitions.

Use skill: "persona-to-segment-translator"
Use skill: "metric-spec-card-generator"

## Workflow

1. Restate each persona in plain language.
2. Identify the business decision or activation channel.
3. Convert persona traits into observable proxies.
4. Define inclusion and exclusion rules.
5. List data fields needed and likely gaps.
6. Add validation checks to test whether the segment behaves differently.
7. Recommend activation, messaging, or analysis use cases.

## Output Format

Return:

1. Persona summary
2. Measurable segment definition
3. Proxy field map
4. Inclusion/exclusion rules
5. Validation checks
6. Activation notes
7. Caveats

## Guardrails

- Do not pretend a qualitative persona is measurable without proxy fields.
- Flag weak or biased proxies.
- Keep segment rules simple enough to implement.
- Separate research language from activation logic.
- Include a way to validate whether the segment is useful.
