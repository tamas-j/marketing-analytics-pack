---
name: analysis-brief-generator
description: Use when creating a concise marketing analytics brief with objective, scope, hypotheses, data requirements, analysis steps, outputs, decision criteria, and caveats.
---

# Analysis Brief Generator

This skill turns a broad question into a practical analysis brief. It is useful before starting exploratory analysis, stakeholder reporting, experiment review, diagnosis, segmentation, forecasting, or campaign post-mortems.

## Required Inputs

Ask only for what is missing:

- Business question or decision.
- Stakeholder or audience.
- Metric or outcome.
- Time period.
- Data available.
- Deadline or level of depth required.
- Known constraints, such as missing fields, tracking issues, or no holdout.

If details are missing, draft the brief and mark assumptions.

## Method

1. Translate the request into one decision.
2. Define scope and out of scope.
3. Write 3-5 testable hypotheses.
4. Identify the minimum viable data needed.
5. Define analysis steps in sequence.
6. Specify outputs, such as tables, charts, summary, recommendations, or appendix.
7. Define decision criteria.
8. Add risks, caveats, and open questions.

## Output Template

```markdown
## Analysis Brief: <topic>

### Business Question
<question>

### Decision to Support
<decision>

### Scope
In scope:
- <item>

Out of scope:
- <item>

### Hypotheses
| Hypothesis | How to test | Evidence that supports it |
|---|---|---|
| <hypothesis> | <test> | <evidence> |

### Data Requirements
| Data | Grain | Required fields | Notes |
|---|---|---|---|
| <dataset> | <grain> | <fields> | <notes> |

### Analysis Plan
1. <step>
2. <step>
3. <step>

### Expected Outputs
- <output>

### Decision Criteria
- <criteria>

### Risks and Caveats
- <risk>
```

## Brief Quality Checklist

- The brief names the decision, not just the topic.
- Hypotheses can be tested with available or requested data.
- The plan starts with basic profiling and decomposition before deeper analysis.
- Data grain is explicit.
- Caveats are visible before recommendations are made.
- The output is sized to the decision deadline.

## Guardrails

- Do not promise causal answers without experiment, holdout, quasi-experimental design, or credible comparison.
- Do not ask for every possible field when a smaller analysis can answer the decision.
- Do not bury major data gaps in the caveats.
- Do not let the brief become a dashboard requirements document unless that is the user's stated need.
