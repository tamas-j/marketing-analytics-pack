---
name: results-skeptic
description: Use when red-teaming an analytical output before sharing — forecast, MMM, RFM, experiment readout, attribution analysis, KPI tree, post-mortem, or any chart-and-narrative result — to surface methodological gaps, hidden assumptions, sanity-check failures, and likely stakeholder objections.
---

# Results Skeptic

This skill takes any analytical output and performs a structured red-team pass against it before the user shares with stakeholders. It is the "what would a smart, skeptical colleague ask?" function — surfacing methodological gaps, hidden assumptions, sanity-check failures, and the questions that will land in the meeting if they aren't addressed in the deck.

The skill is intentionally adversarial in tone. Most analyses survive most reviews; the failure mode this skill targets is the analysis that ships with a quietly broken assumption nobody noticed because everyone was friendly. Better to surface the problem now than in front of the CMO.

It is also intentionally generic across analytical outputs. Specific runners and selectors have their own quality rubrics; this skill is the second pass that any output can go through, regardless of which method produced it.

## Required Inputs

Ask only for what is missing.

1. **The output to review.** Markdown summary, chart pack, runner output folder, draft slide, written brief, or pasted analysis text.
2. **What the output is meant to support.** A decision, a stakeholder conversation, a published report, an internal debrief.
3. **The intended audience.** CMO, paid leads, finance, board, internal analyst team.
4. **The analytical method used.** Forecast (Prophet / ETS / scenario), MMM, incrementality test, A/B test, RFM, attribution model, KPI tree, root-cause analysis, post-mortem narrative.
5. Any known caveats the analyst is already aware of.

## Skepticism Framework

Run the output through five lenses in order. Stop reviewing if any earlier lens raises a blocking issue — fixing it usually invalidates later checks.

### 1. Definition and Scope

The analysis must clearly state what it is measuring and what it is not.

- Is the primary metric defined precisely (with formula and grain)?
- Is the population, audience, or unit of analysis explicit?
- Does the time window match the decision the result will support?
- Does the analysis make a causal claim ("X drove Y") or a correlational one ("X moved with Y")?
- Is the comparison defined? "Up 12%" versus what — last week, last year, plan, control?

### 2. Data and Method

- Is the data source documented? Is the freshness named (last-extract date)?
- Are there known data-quality issues — missing periods, definition changes, tracking shifts, instrumentation changes — that fall inside the window?
- Is the chosen method appropriate for the data shape? (Selectors exist for this — `/forecast-method`, `/attribution-model-selector`, etc.)
- Are baselines and benchmarks named? A forecast without a naive baseline is suspect; an experiment without a power check is suspect.
- Are denominators consistent? Most rate-metric errors are denominator errors (different filters in numerator and denominator).

### 3. Bias and Confounding

- Does the analysis acknowledge bias risks specific to the method?
- Selection bias: was the sample chosen in a way that correlates with the outcome?
- Survivorship bias: are units that "dropped out" omitted from the result?
- Cohort comparability: are cohorts being compared at the same tenure / same point in their lifecycle?
- Regression to the mean: is "improvement" measured from an unusual baseline?
- Simpson's paradox: does the aggregate result reverse when cut by an important dimension?
- Confounding: is there a third variable that explains both the input and the outcome?
- Spillover: is the control group actually unaffected by the treatment?

### 4. Uncertainty and Honesty

- Are uncertainty intervals, confidence intervals, or scenarios reported alongside point estimates?
- Where are the assumptions, and how sensitive is the result to each one?
- What would change the conclusion? Is the magnitude of the result robust to the obvious robustness checks?
- Are negative or null findings reported as such, or have they been re-framed?
- Is precision honest — e.g., "$1,247,392 attributed revenue" implies false precision when the underlying interval is ±30%.
- Does the result claim more than the method can support? (Attribution claiming causality is the most common case.)

### 5. Decision Relevance

- Does the output actually answer the decision the user named?
- If the result is positive, what's the recommended action? If negative, what's recommended? If null, what's recommended?
- Is the result actionable at the cadence and authority of the stakeholder?
- Are guardrail / counter-metrics present (margin, churn, customer experience), or has the analysis optimised one number in isolation?
- Has the user pre-committed to a decision rule, or are they fitting the rule to the result?

## Skepticism by Method

Some methods have characteristic failure modes. Run the relevant section if the method is named.

### Forecast (Prophet / ETS / regression / scenario)

- Was the forecast validated against a naive and seasonal-naive baseline? If it loses to either, is that surfaced?
- Is the error metric appropriate (no MAPE on series with zeros)?
- Are regressors that are actually decisions (planned spend, planned promos) treated as scenarios, not predictions?
- Does the forecast extrapolate through a regime change (launch, repositioning, pricing) without explicit scenario caveat?
- Are uncertainty intervals shown alongside the point forecast?

### MMM

- Were diagnostics (R-hat, ESS, holdout fit, residual patterns) checked before interpretation?
- Are credible intervals reported alongside point estimates?
- Is the recommendation based on marginal ROI (right for budget) rather than average ROI (right for performance reporting)?
- Are channels with poor variation (always-on with no flighting) flagged as poorly identified?
- Does the recommended budget shift extrapolate outside the observed spend support?
- Was an incrementality test recommended for the biggest planned shifts?

### Incrementality / Experiment

- Was the test powered for the MDE that matters? (Geo tests: by markets, not impressions.)
- Was SRM checked? Was an AA-test run on the pipeline?
- Was eligibility frozen at assignment, or computed post-assignment?
- Is the decision rule pre-committed or fitted to the result?
- Is spillover or interference plausible? If so, was it mitigated in the design or hand-waved in the readout?
- Are network effects, parallel-trends assumptions, and placebo tests addressed for geo / matched-market designs?

### Attribution

- Is the chosen model appropriate for the decision (reporting vs optimisation vs budget reallocation)?
- Does the readout distinguish "attribution credit" from "incremental contribution"?
- If platform DDA is the source, is its scope (one platform's view) named?
- Is the sum-of-attributed-conversions sanity-checked against total conversions?

### RFM / Segmentation

- Was the segmentation method matched to the activation? (RFM is a reporting cut, often a weak targeting list.)
- Are segments reachable in the activation channel?
- Was a labelled-outcome alternative (propensity) considered if labels exist?
- Are segment sizes large enough to be operationally useful?
- Has the segmentation been validated against any business outcome, or is the validation only internal (silhouette / cohesion)?

### Root-cause / Post-mortem narrative

- Does the narrative distinguish causes from correlates?
- Are alternative explanations addressed and ruled out, or only the favoured one presented?
- Does the narrative match the data, or is it telling the story stakeholders wanted to hear?
- Are component decompositions reconciled (do the parts sum to the whole)?

## The Three Questions to Ask Before Sharing

If time is short, these three questions catch most failures:

1. **What would have to be true for this conclusion to be wrong?** Force a list. If the list is empty, the analysis is over-confident. If any item is "an obvious data issue we haven't checked," go check.
2. **What does this analysis NOT answer?** A clear scope statement prevents the result being misused for an adjacent decision.
3. **What would change the recommendation?** If the answer is "nothing within plausible variation," the analysis is brittle or the recommendation is over-specified.

## Worked Examples

### Example 1: Weekly forecast handed to finance

Output: Prophet forecast of weekly revenue for next 13 weeks, point estimates only, no baseline comparison.

Red-team output:

- Definition: window and metric are clear; **decision** is "next-quarter revenue plan" — this is OK for that.
- Method: **no baseline comparison shown** — this is a blocker. Re-run with `--validate` (forecast-runner) and report Prophet vs naive vs seasonal-naive. If Prophet loses, surface that.
- Bias: a major launch occurred 8 weeks ago. **Regime change** — Prophet's trend will under-fit the new level. Recommend a launch-effect regressor or a shortened training window.
- Uncertainty: **no intervals shown**. Add 80% prediction intervals. The point estimate plus interval is the honest forecast.
- Decision relevance: finance will round the point estimate. Lead with the range, follow with the centre. Pre-commit a re-forecast cadence.

Verdict: **Do not share** as-is. Fix the baseline, intervals, and regime caveat before circulating.

### Example 2: A/B test readout claiming +3.2% conversion lift

Output: a fixed-horizon two-week test, "treatment converted 3.2% better, p=0.04, ship it." No SRM check, no baseline-conversion stated, no MDE check.

Red-team output:

- Definition: "+3.2%" — relative or absolute? Of what baseline? **Clarify before reading the result.**
- Method: **no MDE / power check.** If the MDE the team cared about was 5% relative, this test was under-powered and the +3.2% may be a fluke. If MDE was 1%, it was over-powered and the +3.2% is genuine.
- Bias: **no SRM check.** Run a chi-square on assignment counts. Half of "broken test" investigations turn out to be assignment-pipeline bugs.
- Uncertainty: p=0.04 with no peeking discipline is suspect. **Was the test read mid-flight?** If yes, the effective alpha is much higher than 0.05.
- Decision relevance: a 3.2% relative lift on a 4% baseline is 0.13 percentage points absolute. Across the business, that's possibly large; possibly noise. Pre-commit the ship/no-ship rule.

Verdict: **Do not ship** until SRM passes and the MDE-vs-detected-effect frame is clear. The p-value alone is insufficient.

### Example 3: MMM readout recommending 3x scale-up of affiliate

Output: MMM marginal ROI for affiliate = 4.1, recommendation = triple affiliate budget next year.

Red-team output:

- Definition: marginal ROI at **current** spend is 4.1. The recommendation asks for that to hold at **3× current spend** — that's an extrapolation, not the model's claim.
- Method: response curve at 3× spend is outside the observed support. The model's number there is essentially the prior.
- Bias: affiliate often gets credit for traffic that would have converted anyway; **MMM rarely separates affiliate from organic intent**. Recommend a known-affiliate-pause test.
- Uncertainty: was the credible interval on affiliate ROI shown? An interval of [1.2, 7.0] reads differently from [3.6, 4.7].
- Decision relevance: 3× is a big bet. Recommendation should be a 30% scale, an incrementality test at the new spend, and a re-fit.

Verdict: **Materially overstated.** Recommend a phased scale with incrementality calibration.

## Anti-Patterns the Skeptic Catches

- **Confident point estimates with no intervals.** "Revenue will be $4.2M next quarter." Always demand the range.
- **Causal claims from non-causal methods.** Attribution analysis labelled as "the impact of channel X."
- **Aggregate hides the result.** Headline is positive, but the result reverses on every meaningful cut. Demand the segment cuts.
- **Decision rule fitted after the result.** "We were going to ship if lift was >2%, but +1.6% directionally counts, so let's ship."
- **Cherry-picked baseline.** "Up 30% versus 2020" — measured against a pandemic trough.
- **Survivorship.** "Customers in our loyalty programme have higher LTV." Yes, because the low-LTV ones churned out of it.
- **One-way sensitivity.** Author varied one assumption at a time; the answer would change if two co-varied.
- **Precision theatre.** "$1,247,392 attributed revenue" when the underlying CI is ±30%.
- **Ghost peer review.** "We reviewed this internally" — by whom, with what challenge function?
- **Method picked to fit the conclusion.** The team ran three measurement methods; the one that gave the desired answer is the one in the deck.

## Output Template

```markdown
## Results Skeptic Review

### What's Being Reviewed
<analysis name, method, intended decision, audience>

### Headline Verdict
<Share / Share with caveats / Fix first / Do not share>

### Lens 1: Definition and Scope
- <finding>

### Lens 2: Data and Method
- <finding>

### Lens 3: Bias and Confounding
- <finding>

### Lens 4: Uncertainty and Honesty
- <finding>

### Lens 5: Decision Relevance
- <finding>

### Method-Specific Checks (if applicable)
- <method> — <finding>

### The Three Questions
- What would have to be true for this conclusion to be wrong? <list>
- What does this analysis NOT answer? <list>
- What would change the recommendation? <list>

### Required Fixes Before Sharing
1. <fix>
2. <fix>

### Nice-to-Have Improvements
- <improvement>

### Likely Stakeholder Objections
- <objection and how to address it in the readout>
```

## Severity Ratings

When listing findings, tag each as:

- **Blocker:** the result is materially misleading without a fix; do not share.
- **Caveat:** the finding does not invalidate the conclusion but must be surfaced in the readout.
- **Improvement:** nice-to-have; not a blocker.

A `Do not share` verdict requires at least one blocker. `Share with caveats` requires at least one caveat. `Share` means no blockers and no major caveats.

## Quality Rubric

- `Strong`: every lens applied; method-specific checks run; findings tagged by severity; specific fixes named; the three questions are answered substantively.
- `Usable`: most lenses applied; severity unclear; fixes named.
- `Needs revision`: a generic "looks fine" pass with no concrete findings; flattery instead of red-team; method-specific checks skipped.

## Guardrails

- Do not soften findings to be polite — the user invoked this skill specifically for adversarial review.
- Do not pretend findings exist if the analysis is genuinely clean — surface that too; a "Share" verdict is a valid outcome.
- Do not duplicate the analyst's own quality rubric; this is a second pass, not a re-run.
- When a blocker is found, do not list improvements until the blocker is acknowledged.
- When the method is named, run the method-specific checks; do not skip them.
- After review, route to the relevant fix-skill — `/check-data` for data issues, `/forecast-method` to revisit method choice, `/experiment-design-reviewer` for design problems, etc.
- This skill reviews outputs that already exist. To design an analysis from scratch, route to `/plan-analysis`.
