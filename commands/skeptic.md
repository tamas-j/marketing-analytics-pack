---
description: Red-team an analytical output before sharing — forecast, MMM, experiment, RFM, attribution, post-mortem — to surface methodological gaps, hidden assumptions, sanity-check failures, and likely stakeholder objections.
argument-hint: "<the output to review (file path, pasted text, or runner output folder) and the decision it supports>"
---

# Results Skeptic

Use this command when an analysis is drafted and about to be shared. The command runs a structured adversarial review before stakeholders see it — surfacing methodological gaps, hidden assumptions, sanity-check failures, and the objections that will land in the meeting if they aren't addressed in the deck.

Use skill: "results-skeptic"
Use skill: "measurement-pitfalls"

## When to Use This Command

- After any runner produces output (`/forecast-runner`, `/mmm-runner`, `/rfm-segment`).
- After an experiment readout is drafted and before it goes to a leadership review.
- After an attribution or MMM result interpretation is written.
- Before a post-mortem or analysis brief goes to a CMO / CFO / board audience.
- When the user is uneasy about a result and wants a second pass.

The command does not redo the analysis. It reviews it.

## Workflow

1. Identify what's being reviewed: the analysis output, the method used, the decision it supports, the intended audience.
2. Run the five lenses from the skill: definition and scope, data and method, bias and confounding, uncertainty and honesty, decision relevance.
3. If the method is named (forecast / MMM / experiment / RFM / attribution / root cause / post-mortem), run the method-specific checks.
4. Tag each finding by severity: **blocker**, **caveat**, **improvement**.
5. Answer the three questions: what would have to be true for the conclusion to be wrong, what does the analysis NOT answer, what would change the recommendation.
6. Issue a headline verdict: Share / Share with caveats / Fix first / Do not share.
7. Return required fixes and likely stakeholder objections.

## Output Format

Return the `Results Skeptic Review` template from the skill:

1. What's being reviewed.
2. Headline verdict.
3. Findings across all five lenses, each tagged by severity.
4. Method-specific findings if the method is identified.
5. Answers to the three questions.
6. Required fixes (blockers) and nice-to-have improvements.
7. Likely stakeholder objections and how to pre-empt them.

## Tips

- The skeptic is adversarial by design. Do not soften findings to be polite — the user invoked this command specifically for hard challenge.
- A clean "Share" verdict is a valid outcome; don't invent findings to look thorough.
- When a blocker is found, lead with it. Improvements come after the blockers are acknowledged.
- After the review, route to the relevant fix command (`/check-data`, `/forecast-method`, `/experiment-design-reviewer`, etc.) so the user knows what to actually do.

## Guardrails

- Do not duplicate the analyst's own quality rubric — this is a second pass, not a re-run.
- Do not turn the review into a methodology lecture; tie every finding to a specific risk in this specific output.
- Do not give a `Share` verdict if any blocker is unaddressed.
- Do not give a `Do not share` verdict without naming the specific blocker and the specific fix.
- When the analysis is fundamentally the wrong method for the question, surface that as a blocker and route to the right selector (`/attribution-model-selector`, `/forecast-method`, etc.).
- When the analysis is sound but the recommendation is over-specified, the verdict is `Share with caveats` — the analysis stays, the framing changes.
