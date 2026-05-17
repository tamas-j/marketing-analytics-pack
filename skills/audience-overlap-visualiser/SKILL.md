---
name: audience-overlap-visualiser
description: Use when assessing overlap between audiences, lists, segments, campaigns, or channels and recommending targeting, suppression, budget, or measurement actions.
---

# Audience Overlap Visualiser

This skill helps users understand how audiences overlap and what to do about it. It is useful for suppression planning, channel duplication, list quality, retargeting, and audience strategy.

## Required Inputs

Ask only for what is missing:

- Audience names.
- Audience sizes.
- Shared ID used to match audiences.
- Overlap counts or membership flags.
- Activation or measurement decision.
- Consent or eligibility constraints, if relevant.

## Core Metrics

- `intersection`: count of IDs in both audiences.
- `overlap as % of A`: intersection / audience A size.
- `overlap as % of B`: intersection / audience B size.
- `unique reach`: count of IDs in either audience.
- `duplicate reach`: sum of audience sizes - unique reach.
- `Jaccard index`: intersection / union.

## Output Template

```markdown
## Audience Overlap Analysis

### Audience Summary
<audiences, ID, and goal>

### Overlap Table
| Pair | Audience A size | Audience B size | Overlap | % of A | % of B | Readout |
|---|---:|---:|---:|---:|---:|---|
| <A x B> | <n> | <n> | <n> | <pct> | <pct> | <readout> |

### Interpretation
- <meaning>

### Recommended Action
- <action>

### Measurement Caveats
- <caveat>

### Visual Recommendation
<matrix/bar/Venn-style summary>
```

## Interpretation Guide

- High overlap can indicate wasted reach, strong intent, list duplication, retargeting concentration, or expected lifecycle progression.
- Low overlap can indicate distinct audiences, poor matching, fragmented IDs, or channel isolation.
- Asymmetric overlap matters. A small VIP list may overlap heavily with a large email list, while the email list barely overlaps with VIPs.
- Suppression decisions should consider value, consent, and campaign objective.

## Guardrails

- Do not calculate overlap without consistent ID logic.
- Do not merge audiences without checking consent and channel eligibility.
- Do not infer incrementality from overlap alone.
- Do not hide match-rate limitations.
