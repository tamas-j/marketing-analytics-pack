---
description: Analyse overlap between audiences, customer segments, channels, lists, or campaigns and recommend targeting or measurement actions.
argument-hint: "<audiences/lists/segments, IDs available, sizes, overlap counts, activation goal>"
---

# Audience Overlap

Use this command when the user needs to understand overlap between customer audiences, marketing lists, channels, campaigns, or segments.

Use skill: "audience-overlap-visualiser"
Use skill: "data-visualization"

## Workflow

1. Restate the audiences and the decision the overlap analysis should support.
2. Confirm the ID used to match audiences.
3. Ask for audience sizes, overlap counts, or membership fields.
4. Calculate or specify overlap rates:
   - intersection size
   - overlap as percent of each audience
   - unique reach
   - duplicate reach
5. Interpret whether overlap is useful, wasteful, or expected.
6. Recommend targeting, suppression, budget, or test design actions.
7. Suggest a simple visual: overlap matrix, ranked bar chart, or Venn-style summary.

## Output Format

Return:

1. Audience summary
2. Overlap table
3. Interpretation
4. Recommended action
5. Measurement caveats
6. Visual recommendation

## Guardrails

- Do not compare audiences without a shared stable ID.
- Be clear whether overlap is symmetric or viewed from one audience's base.
- Do not treat overlap as bad by default; it may indicate useful reinforcement.
- Flag privacy, consent, and activation constraints where relevant.
