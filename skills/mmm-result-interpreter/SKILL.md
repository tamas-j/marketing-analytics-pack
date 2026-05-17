---
name: mmm-result-interpreter
description: Use when interpreting media mix model outputs, including contribution, ROI, marginal ROI, response curves, uncertainty, diagnostics, caveats, budget implications, and validation steps.
---

# MMM Result Interpreter

This skill translates MMM outputs into practical business interpretation. It starts with diagnostics and uncertainty before budget recommendations.

## Required Inputs

Ask only for what is missing:

- Model question.
- Channel contribution estimates.
- ROI or marginal ROI.
- Response curves or saturation outputs.
- Uncertainty intervals.
- Model fit diagnostics.
- Known caveats or excluded variables.
- Current budget or decision context.

## Interpretation Order

1. Check diagnostics and scope.
2. Summarise what the model can and cannot answer.
3. Interpret contribution.
4. Interpret ROI and marginal ROI separately.
5. Inspect saturation and response curves.
6. Highlight uncertainty.
7. Translate into recommendations.
8. Recommend validation experiments or data improvements.

## Output Template

```markdown
## MMM Result Interpretation

### Executive Readout
<plain-English summary>

### Diagnostics Check
| Diagnostic | Readout | Implication |
|---|---|---|
| <diagnostic> | <readout> | <implication> |

### Channel Interpretation
| Channel | Contribution | ROI/mROI | Uncertainty | Interpretation |
|---|---:|---:|---|---|
| <channel> | <value> | <value> | <range> | <readout> |

### Budget Implications
- <recommendation>

### Caveats and Uncertainty
- <caveat>

### Follow-Up Tests or Data Improvements
- <next step>
```

## Guardrails

- Do not interpret contribution or ROI before checking diagnostics.
- Do not treat wide uncertainty intervals as precise ranking.
- Do not shift budget from average ROI alone when marginal ROI is available.
- Do not compare channels without considering spend scale and saturation.
- Recommend experiments where model uncertainty is decision-critical.
