---
name: measurement-pitfalls
description: Use when a Marketing Analytics Pack skill or command needs the canonical reference for common measurement pitfalls — cohort comparability, denominator errors, attribution vs causality, regression to the mean, survivorship, selection bias, Simpson's paradox, multiple testing, base rates, spillover, and others. Model-only reference; load and quote from this when surfacing or explaining a pitfall in another skill.
user-invocable: false
---

# Measurement Pitfalls Reference

This reference skill is the shared catalogue of common measurement pitfalls that other skills point at instead of repeating thin one-liners.

Other skills' guardrails sections often include lines like "don't compare immature cohorts to mature cohorts" or "don't infer causality from segment cuts alone." This file is where those lines are explained properly — with the mechanism, the symptom, the fix, and one or two worked illustrations. When a skill needs to surface a pitfall, it should load this skill and quote the relevant section, not re-explain it.

The pitfalls below are ordered roughly by how often they appear in marketing analytics specifically. Sections are self-contained and can be quoted in isolation.

## Required Inputs

This is a reference skill, not invoked directly. Calling skills supply:

- The pitfall area they need to surface or check.
- The specific analysis context (e.g., "comparing churn rates across cohorts of different tenures").

## How to Use This Reference

When another skill needs to flag a pitfall:

1. Identify which section(s) below apply.
2. Quote the relevant section's `Mechanism`, `Symptom`, and `Fix` lines, adapted to the user's situation.
3. Link to the related skill or command for the fix (e.g., `/check-data`, `/incrementality-test-designer`).

When in doubt, prefer linking to the section than rewriting it.

---

## Cohort Comparability

**Mechanism.** Cohorts at different tenures have had different amounts of time to experience the outcome. Comparing them at a fixed calendar moment systematically misrepresents the metric.

**Symptom.** "Customers acquired in Q1 have 18% retention; Q3 customers have 22% — Q3 is the better cohort." Q3 customers have had less time to churn.

**Fix.** Always compare cohorts at **equal tenure**. If you want a 90-day retention comparison, every cohort must have at least 90 days of observation, and you compare each cohort's 90-day retention specifically.

**Example.** A subscription business looking at "customers active today" mixes mature customers who have survived multiple churn opportunities with new customers who haven't yet had any. Active-base composition shifts trick the team into seeing a "retention improvement" that is actually a mix shift toward newer cohorts.

**Related fixes:** report cohort curves with tenure on the x-axis, not calendar dates; quote retention at fixed tenures (30d, 90d, 12m); flag any "improvement" that depends on cohort age.

## Denominator Errors

**Mechanism.** Rate-metric calculations require numerator and denominator to share the same filtering, time window, and grain. Subtle inconsistencies — different eligibility filters, different time windows, different units — produce ratios that don't mean what the label says.

**Symptom.** "Conversion rate fell" but the denominator definition silently changed (e.g., bot filtering tightened) and the numerator didn't.

**Fix.** State the formula explicitly: numerator definition, denominator definition, filters that apply to both. Trace each filter through both sides; mismatched filters are the most common cause of bad rate metrics.

**Example.** "Email click-through rate" computed as `clicks / sends` is different from `clicks / deliveries` is different from `unique clickers / unique recipients`. A 30% gap between metrics often turns out to be one of these distinctions.

**Related fixes:** `/metric-spec-card` produces precise formulas; require formula + filters for any rate metric in a brief.

## Attribution vs Causality

**Mechanism.** Attribution assigns credit over observed conversion paths. It cannot answer "what would have happened without this marketing." Two channels can each be the "last touch" before different conversions and still not be causally responsible for those conversions.

**Symptom.** "Channel X has high attributed ROI, so increasing channel X budget will yield ROI X." Often it won't — the channel was credited for conversions that would have happened anyway.

**Fix.** Use attribution for in-channel optimisation and reporting. Use incrementality and MMM for causal claims. Always label attribution numbers as "attributed" not "incremental" or "caused by."

**Example.** Branded paid-search shows ROI of 15× in platform attribution. Pause it for two weeks in a holdout — half the conversions still happen organically. The true incremental ROI is closer to 7×. The platform isn't lying; it's just not measuring causality.

**Related fixes:** `/attribution-model-selector`, `/incrementality-test-designer`, `/triangulate`.

## Regression to the Mean

**Mechanism.** Units selected because they are extreme on a measurement will, on average, be less extreme on the next measurement — regardless of any intervention. The improvement is partly real and partly statistical.

**Symptom.** "We targeted our 10% lowest-engagement customers with a re-engagement campaign; their engagement is up 40%." Some of that 40% would have happened without the campaign because the lowest-engagement customers were measured at their worst moment.

**Fix.** Use a control group selected the same way as the treatment group. The control's regression-to-the-mean improvement is what you subtract from the treatment's apparent improvement to find the true lift.

**Example.** Schools targeted because they were the worst-performing in the district. The next year their scores improved more than the district average. Some of this is genuine; much of it is regression to the mean. Without a comparable control, you can't separate the two.

**Related fixes:** `/incrementality-test-designer` for control design; always include a comparable control group when targeting on an extreme value.

## Selection Bias

**Mechanism.** The sample you analyse was filtered by a process correlated with the outcome you're measuring. Conclusions from the sample do not generalise to the population.

**Symptom.** "Our newsletter subscribers have 2× the LTV of non-subscribers." Yes — but subscribers self-selected because they were already engaged.

**Fix.** Either randomise into the treatment, or use a comparable control that didn't self-select. If neither is possible, frame the result as descriptive: "newsletter subscribers are a high-LTV segment," not "newsletter subscription causes high LTV."

**Example.** Loyalty programme members have higher repeat rates than non-members. This may be the loyalty programme causing repeat purchases, or it may be the kind of customer who joins a loyalty programme buying more anyway. Without random assignment to membership, you cannot separate the two.

**Related fixes:** `/experiment-design-reviewer`, `/incrementality-test-designer`; flag the bias in the readout if neither is feasible.

## Survivorship Bias

**Mechanism.** Units that "drop out" before the analysis window are omitted from the result. The survivors are systematically different from the dropouts. Conclusions from survivors describe survivors, not the original population.

**Symptom.** "Customers in our loyalty programme have 30% higher LTV." Yes — because the customers with low LTV churned out of the programme.

**Fix.** Anchor the analysis on the original population at a fixed start point. Track outcomes for everyone who started, including those who dropped out. Cohort analysis with tenure-anchored measurement avoids the trap.

**Example.** "Our top-tier customers retain at 95%." That's true today, but "top-tier" is a status customers earn over time — the comparison silently excludes everyone who never made it to top tier.

**Related fixes:** anchor on acquisition or activation cohort; report drop-out explicitly.

## Simpson's Paradox

**Mechanism.** A relationship that holds in aggregate reverses when the data is split by an important dimension. Usually caused by a confounding variable correlated with both the input and the outcome.

**Symptom.** Conversion rate increased month-over-month overall — but conversion rate decreased in every channel individually. Channel mix shifted toward a higher-converting channel.

**Fix.** Cut the aggregate by the dimensions most likely to confound it (channel, audience, product, region, period). If aggregate and segment cuts disagree, the segment cuts usually tell the truer story — unless the segments themselves are not comparable.

**Example.** A new landing page "improved conversion rate" in aggregate. Split by traffic source: every source's conversion rate fell. Traffic mix had shifted toward a high-converting source (branded paid search up; cold display down). The landing page wasn't responsible for either move.

**Related fixes:** require segment cuts on any aggregate movement; route to `/root-cause-tree`.

## Multiple Testing

**Mechanism.** Running many statistical tests on the same dataset inflates the false-positive rate. With 20 independent tests at α=0.05, one or two will appear "significant" by chance alone.

**Symptom.** An A/B test deck reports "the primary metric was flat, but conversion rate among new mobile users in California from organic search was +18% (p=0.04) — let's ship it."

**Fix.** Pre-register the primary metric and the small list of pre-specified segments. Apply a multiple-testing correction (Bonferroni, Benjamini-Hochberg) when many segments are explored. Treat post-hoc segment findings as hypotheses for the next test, not conclusions from this one.

**Example.** A homepage redesign A/B test reads flat on the primary metric. The analyst slices by 12 segments and finds one with p=0.03. Probability of at least one false positive across 12 tests is roughly 46% — the segment finding has the same odds as a coin flip.

**Related fixes:** `/experiment-design-reviewer`; pre-register the analysis plan; correct for multiple comparisons.

## Base Rate Neglect

**Mechanism.** Conclusions drawn from rates without considering the underlying population can be misleading. A small absolute number becomes a "high percentage" when the denominator is small.

**Symptom.** "Our experimental cohort had a 50% conversion rate, double the baseline." The experimental cohort was 8 customers.

**Fix.** Always show the absolute counts alongside rates. Demand minimum-sample thresholds before reporting rate comparisons.

**Example.** "Region X has 3× the complaint rate of region Y." Region X has 12 customers and 3 complaints; region Y has 12,000 customers and 1,200 complaints. The "3×" is real arithmetically and uninformative practically.

**Related fixes:** require denominators on every rate; flag rate comparisons where either denominator is below a minimum (default ~100 for percentages).

## Peeking and Multiple Looks

**Mechanism.** Reading a fixed-horizon experiment before its planned end date and stopping at the first "significant" result inflates the false-positive rate substantially. The nominal p-value no longer reflects the true rate of false positives.

**Symptom.** "We were going to run for four weeks but we hit significance on day 9 so we stopped." The "significant" result is roughly twice as likely to be spurious as the headline p-value suggests.

**Fix.** Commit to the horizon and don't look. If business pressure to look mid-flight is real, adopt sequential testing (always-valid p-values, Bayesian decision boundaries with proper priors). Either way, the decision rule is pre-committed before launch.

**Example.** An e-commerce checkout test was planned for 28 days. Day 11 showed +4.2% (p=0.03). The team stopped and shipped. The final 28-day result, had they run it, would have been +1.1% (n.s.) — they shipped on early noise.

**Related fixes:** `/experiment-design-reviewer`; pre-register stopping rules.

## Spillover and SUTVA Violations

**Mechanism.** Treatment of one unit affects another (network effects, marketplace dynamics, auction systems, shared resources). The Stable Unit Treatment Value Assumption (SUTVA) underlying basic A/B test analysis is violated, biasing the result in unpredictable directions.

**Symptom.** "We tested a marketplace supplier-side incentive and saw +15% GMV in treatment suppliers." If buyers shift demand from control suppliers to treatment suppliers, the marketplace-level lift is much smaller than the treatment-vs-control difference suggests.

**Fix.** Choose a randomisation unit that contains the spillover (geo, cluster, time window). Switchback or cluster randomisation for marketplaces and social products. Disclose the assumption in the readout if mitigation is infeasible.

**Example.** A two-sided marketplace tested a search-ranking change at the user level. Power-users in treatment booked more from popular suppliers; supply shifted; control users found inventory thinner. The user-level treatment effect overstated the system-level effect by ~2×.

**Related fixes:** `/incrementality-test-designer`; geo or cluster randomisation; switchback designs for fast-cycle interventions.

## Confounding by Time and Seasonality

**Mechanism.** Before/after comparisons attribute change to an intervention when the change would have happened anyway due to seasonality, secular trends, or concurrent events.

**Symptom.** "Revenue is up 22% since we launched the new homepage in November." November is also Black Friday.

**Fix.** Use a control that's exposed to the same seasonality and trends but not to the intervention. Difference-in-differences, geo holdouts, and matched-period analyses all serve this purpose.

**Example.** A retailer launched a new loyalty programme in October. Q4 revenue rose 30%. Without a comparison group exposed to the same Q4 macro tailwinds, the programme's contribution is impossible to separate from the season.

**Related fixes:** `/incrementality-test-designer`; require a counterfactual for any before/after claim.

## Goodhart's Law

**Mechanism.** When a measure becomes a target, it ceases to be a good measure. Optimising for the proxy degrades the underlying outcome the proxy was meant to track.

**Symptom.** "Email opens are up 40% since we made open-tracking the team's goal." Subject lines are now misleading clickbait; long-term engagement is down; complaint rates rose.

**Fix.** Always pair an optimisation metric with a guardrail metric that catches the gaming. KPI trees should include guardrails for every level-1 driver.

**Example.** A customer-service team measured on call-handle-time started ending calls faster; first-call resolution dropped; repeat-contact rate rose; total cost went up.

**Related fixes:** `/kpi-tree`; require guardrail metrics on any single-metric optimisation goal.

## Precision Theatre

**Mechanism.** Reporting a result with more significant digits than the underlying uncertainty supports. The number looks precise; the actual interval is wide.

**Symptom.** "Attributed revenue: $1,247,392." The underlying interval is ±$300K.

**Fix.** Round to a precision consistent with the credible / confidence interval. Report the interval alongside the point estimate.

**Example.** An MMM produces a credible interval of [$0.9M, $1.7M] for connected TV contribution. The deck reads "Connected TV contribution: $1.293M." Drop to one decimal at most; report the range.

**Related fixes:** require ranges on any MMM, forecast, or experiment readout; sense-check rounding against the interval.

## Lurking Variables and Omitted Confounders

**Mechanism.** An unobserved variable correlates with both the input and the outcome, making the observed relationship look causal when it isn't.

**Symptom.** "Customers who opt into SMS have higher LTV." Customers who opt into SMS are also more engaged generally — channel preference is the proxy, not the cause.

**Fix.** In experiments, randomisation handles this for the observed unit. In observational analyses, identify the most plausible confounders and either control for them or acknowledge the analysis as descriptive rather than causal.

**Example.** "Customers who attend our webinars convert 3× faster." The kind of customer who attends a webinar is closer to a buying decision already — the webinar didn't necessarily cause the speedup.

**Related fixes:** `/incrementality-test-designer`; explicit list of unobserved confounders in any observational result.

## Anchoring to the Wrong Counterfactual

**Mechanism.** Comparing the observed outcome to a counterfactual that wasn't actually counterfactual. Often the "control" still receives part of the treatment, or the "before" period was abnormal.

**Symptom.** "We held out 10% of users from email — they bought just as much." If the held-out users still see paid, push, and onsite messages from the same brand, the "no email" condition isn't actually no marketing.

**Fix.** Specify the counterfactual concretely. For owned channels, suppress across the full marketing stack for the holdout if the question is "what is email worth." For paid, design the holdout at the level that contains the channel.

**Example.** A "geo holdout" turned off TV in test DMAs but left digital running. The result is a TV-incremental-to-digital test, not a marketing-incremental-to-nothing test. Useful for a TV-specific decision; misleading if framed as overall marketing lift.

**Related fixes:** `/incrementality-test-designer`; name the counterfactual explicitly in any causal claim.

---

## Cross-Skill Wiring Notes

Other skills should link to this reference rather than re-explain. Suggested wiring:

- `/forecast-method` guardrails → link to **Anchoring to the Wrong Counterfactual** and **Confounding by Time**.
- `/experiment-design-reviewer` → link to **Multiple Testing**, **Peeking**, **Spillover and SUTVA**, **Regression to the Mean**.
- `/incrementality-test-designer` → link to **Spillover and SUTVA**, **Anchoring to the Wrong Counterfactual**, **Confounding by Time**.
- `/attribution-model-selector` → link to **Attribution vs Causality**, **Lurking Variables**.
- `/mmm-result-interpreter` → link to **Precision Theatre**, **Anchoring to the Wrong Counterfactual**.
- `/segmentation-method` → link to **Selection Bias**, **Survivorship Bias**.
- `/rfm-segment` and `/persona-to-segment` → link to **Selection Bias**, **Base Rate Neglect**.
- `/kpi-tree` → link to **Goodhart's Law**, **Denominator Errors**.
- `/check-data` → link to **Denominator Errors**, **Cohort Comparability**.
- `/root-cause-tree` → link to **Simpson's Paradox**, **Confounding by Time**, **Cohort Comparability**.
- `/clv-scenario` → link to **Cohort Comparability**, **Survivorship Bias**.
- `/campaign-post-mortem` and `/analysis-brief` → link to **Anchoring to the Wrong Counterfactual**, **Attribution vs Causality**.
- `/skeptic` → can quote any section as needed.

## Guardrails

- This skill is the canonical reference; do not duplicate full pitfall explanations in other skills' bodies. Other skills should link here and quote the relevant section.
- Keep sections self-contained so they can be quoted in isolation without context.
- When a new pitfall appears repeatedly across skill guardrails, add it here rather than repeating it; update the cross-skill wiring notes.
- This skill is `user-invocable: false` — it is loaded by other skills, not called directly by a slash command.
