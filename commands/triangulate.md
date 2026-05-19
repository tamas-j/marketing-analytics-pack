---
description: Design a blended marketing measurement framework that triangulates MMM, incrementality tests, and attribution with a governance rule for disagreements.
argument-hint: "<decisions the framework must support, current measurement state, budget scale>"
---

# Triangulate Measurement

Use this command when the user is past picking a single measurement method and needs a framework that runs MMM, incrementality, and attribution together — with a clear rule for what happens when they disagree.

Use skill: "measurement-triangulation"
Use skill: "data-visualization"

## When to Use This Command vs the Single-Method Selectors

- Use `/triangulate` when the user is asking "how do we measure marketing overall?" or planning a quarterly cadence across multiple methods.
- Use `/attribution-model-selector` when the user is picking one attribution approach.
- Use `/mmm-readiness` when the user is scoping a specific MMM run.
- Use `/incrementality-test-designer` when the user is designing one specific test.

`/triangulate` is the wrapper that decides which of the others get used when, by whom, with what governance.

## Workflow

1. Restate the marketing decisions the framework must support, with cadence and approximate dollar stake.
2. Inventory what measurement is already in place — platform attribution, MMM (vendor or in-house), incrementality programme.
3. Identify the stakeholders and who arbitrates when measurement results disagree.
4. Apply the three-layer model: MMM for budget allocation, incrementality for calibration of the highest-stakes decisions, attribution for in-channel optimisation. Map each layer to the specific decisions it supports.
5. Identify gaps: which layer is missing for which decision?
6. Plan a triangulation calendar (quarterly is the default cadence).
7. Pre-commit a governance rule: when MMM and incrementality disagree by more than X on the same channel, what happens? When attribution and MMM disagree on cross-channel reallocation, who wins?
8. If a layer is missing or being built, name the bridge measurement that fills the gap in the meantime.
9. Set out the first 90 days of concrete moves to stand the framework up.

## Output Format

Return the `Measurement Framework Design` template from the skill, including:

1. Decisions the framework supports, with cadence and dollar stake.
2. Layer status: what's in place, what's recommended, what's next.
3. Triangulation calendar.
4. Governance rule (one page; reads cleanly out of context).
5. Stakeholder communication plan.
6. Bridge measurement, if any.
7. First 90 days of moves.
8. Honest caveats.

## Tips

- The governance rule is the most-skipped, highest-value part of the framework. Always pre-commit it.
- When the team is too small for full MMM, design a credible framework with incrementality + attribution and revisit MMM in 6–12 months. Don't recommend a stripped-down MMM as a substitute.
- The calendar matters as much as the methods. A team that runs MMM quarterly and reads it daily is mis-using it.
- "We just use platform attribution" is a clear anti-pattern for any team making budget decisions worth >$1M annually. Push back with the framework as the alternative.

## Guardrails

- Do not recommend averaging outputs across layers — layer them, with each layer authoritative for its own question.
- Do not recommend a single-method framework for a team making decisions at multiple cadences.
- Do not propose attribution as authoritative for budget reallocation.
- Always pre-commit the governance rule for disagreements; the rule turns "which model is right?" into "which decision is this?"
- If readiness for any layer is unclear, route to `/mmm-readiness`, `/incrementality-test-designer`, or `/attribution-model-selector` for that layer before finalising the framework.
