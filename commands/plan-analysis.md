---
description: Diagnose a marketing analytics question and route the user to the right Marketing Analytics Pack workflow.
argument-hint: "<business question, goal, dataset summary, or decision to support>"
---

# Plan Analysis

Use this command as the main front door when the user is unsure what analysis they need.

Use skill: "main-analysis-planner"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the user's decision or business question in plain language.
2. Identify the likely analysis intent:
   - metric design
   - data readiness
   - root cause diagnosis
   - segmentation
   - experimentation or incrementality
   - forecasting
   - marketing operations
   - executive narrative or post-mortem
3. Ask for only the minimum missing context needed to route them.
4. Recommend one primary next command and, where helpful, one secondary command.
5. Explain why that route fits in 2-4 sentences.
6. If data is involved, run the readiness checklist from `data-readiness-checker` before recommending deeper analysis.
7. Return a short action plan the user can follow immediately.

## Routing Map

| User need | Primary route | Notes |
|---|---|---|
| "I don't know what to measure" | `/kpi-tree` | Build the measurement framework first. |
| "Can my file support this analysis?" | `/check-data` | Validate grain, columns, missingness, and time coverage. |
| "Why did this metric move?" | Root cause investigation tree | Planned diagnosis command. |
| "Which customers should we target?" | `/segmentation-method` | Choose the right segmentation approach first. |
| "Did this campaign work?" | `/campaign-post-mortem` or `/incrementality-test-designer` | Use post-mortem for observed performance; incrementality for causal impact. |
| "Can we trust this A/B test?" | `/experiment-design-reviewer` | Review hypothesis, control, randomisation, metrics, and risks. |
| "Which attribution model should we use?" | `/attribution-model-selector` | Choose the measurement approach and caveats. |
| "Are we ready for MMM?" | `/mmm-readiness` | Check time-series, media, controls, variation, and risks. |
| "Can you prepare an MMM run?" | `/mmm-runner` | Scope a Google Meridian runner spec. |
| "What do these MMM results mean?" | `/mmm-result-interpreter` | Interpret contribution, ROI, uncertainty, and caveats. |
| "What will happen next month?" | Forecast method selector | Planned forecasting command. |
| "How should I explain this result?" | `/analysis-brief` or `/campaign-post-mortem` | Plan or summarise the analysis. |
| "Why is my campaign list so small?" | `/suppression-waterfall` | Explain eligibility, consent, contactability, and business-rule losses. |
| "Are our UTMs/names clean enough?" | `/marketing-taxonomy-auditor` | Audit taxonomy consistency and reporting risk. |
| "Are we over-contacting customers?" | `/frequency-cap-fatigue` | Diagnose fatigue and recommend caps. |
| "Which action should each customer get?" | `/nba-logic` | Design next-best-action rules and guardrails. |

## Output Format

Return:

1. `Question understood`: one sentence.
2. `Best next step`: the command or workflow to use.
3. `Why this fits`: short rationale.
4. `What I need from you`: only essential inputs.
5. `Data readiness`: pass, partial, blocked, or not applicable.
6. `Suggested sequence`: 1-3 steps.

## Guardrails

- Be decisive once there is enough context.
- Do not recommend an advanced runner before checking whether the user has the right data.
- Prefer a lightweight diagnostic or KPI tree when the question is still vague.
- If a planned command does not exist yet, name it as planned and offer the closest available workflow.
- Keep language non-technical unless the user is clearly technical.
