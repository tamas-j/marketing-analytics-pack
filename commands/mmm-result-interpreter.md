---
description: Interpret media mix model outputs into business implications, caveats, budget recommendations, and next validation steps.
argument-hint: "<MMM outputs, channel contributions, ROI/mROI, uncertainty, diagnostics, business question>"
---

# MMM Result Interpreter

Use this command when the user has MMM outputs and needs to explain what they mean for marketing decisions.

Use skill: "mmm-result-interpreter"
Use skill: "data-visualization"

## Workflow

1. Restate the model question and outputs available.
2. Check the diagnostics and caveats before interpreting contribution or ROI.
3. Interpret:
   - channel contribution
   - ROI or marginal ROI
   - response curves and saturation
   - lagged effects
   - uncertainty intervals
   - model fit and residual issues
4. Translate results into budget or measurement recommendations.
5. Flag where experiments or additional data are needed.

## Output Format

Return:

1. Executive readout
2. Diagnostics check
3. Channel interpretation
4. Budget implications
5. Caveats and uncertainty
6. Follow-up tests or data improvements

## Guardrails

- Do not recommend budget shifts from weak diagnostics.
- Do not overstate precision when uncertainty is wide.
- Distinguish ROI from marginal ROI.
- Treat MMM results as decision support, not absolute truth.
