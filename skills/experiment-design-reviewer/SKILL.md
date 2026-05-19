---
name: experiment-design-reviewer
description: Use when reviewing A/B test or experiment designs for hypothesis, control, randomisation unit, metrics, guardrails, sample, duration, power, SRM, variance reduction, peeking, network effects, and bias risks.
---

# Experiment Design Reviewer

This skill reviews experiment designs before launch and flags the failure modes that make tests inconclusive, biased, or unactionable. The goal is to surface issues while they are still cheap to fix — once a test is live, most design problems can only be re-run, not fixed.

The skill is opinionated about three things most reviews miss: **power**, **SRM / pre-experiment health**, and **peeking**. A test with the right hypothesis but the wrong power, or with sample-ratio mismatch, or read mid-flight, is worse than no test.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first four drive most of the review.

1. **Hypothesis.** Specific, falsifiable, and tied to a decision the team will make based on the result.
2. **Randomisation unit and primary metric.** User, session, account, geo, or device, and what the test is measuring.
3. **Expected effect size (MDE) and traffic / sample size.** Without these, power is impossible to assess.
4. **Measurement window and analysis plan.** Duration, when the test will be read, and what the decision rule is.
5. Treatment and control definition.
6. Eligibility / exposure / assignment events.
7. Guardrail metrics.
8. Instrumentation and data source for assignment and outcome.
9. Known external events during the window (launches, holidays, competitor moves).

## Review Checklist

The Output Template's "Design Review" table should cover every row below.

| Area | Check |
|---|---|
| Hypothesis | Specific, falsifiable, tied to a decision; predicts direction and rough size |
| Control | Represents the right counterfactual; not contaminated by other tests or rollouts |
| Randomisation unit | Matches the decision; prevents interference (user-level if effects can leak across sessions) |
| Eligibility | Defined **before** assignment; filters applied symmetrically to treatment and control |
| Assignment & exposure | Logged for every unit; exposure-based analysis available if treatment is gated |
| Primary metric | Tied to the decision; matures inside the test window; computable from logged data |
| Guardrail metrics | Protect customer experience, margin, churn, fatigue, quality, latency |
| Sample size & MDE | Power ≥80% at the MDE the team cares about; effect-size assumption is defended |
| Duration | At least one full weekly cycle for behavioural metrics; aligned to business cycles |
| Pre-experiment health | AA-test passed or SRM check planned; baseline metrics stable |
| Variance reduction | CUPED or stratification considered if pre-period data is rich and effect size is small |
| Peeking & stopping | Either fixed-horizon with no peeking, or sequential / Bayesian with proper correction |
| Network effects | Spillover identified; randomisation unit chosen to contain it (geo / time switchback if needed) |
| Analysis plan | Pre-registered; cuts and segments listed; multiple-comparison correction planned |
| External events | Window does not span a major event likely to confound; sensitivity analysis planned if it does |

## Power and MDE

The single most common gap in experiment reviews is silent under-powering. The conversation usually goes "we'll run for two weeks and see." Force the math.

For a two-sample test of proportions with significance α = 0.05 and power 1−β = 0.80, the rough per-arm sample size is:

`n_per_arm ≈ 16 × p × (1 − p) / MDE²`

where `p` is the baseline conversion rate and `MDE` is the absolute (not relative) detectable effect. The factor 16 comes from `(z_{α/2} + z_β)² ≈ 7.85` rounded up for safety.

Worked example: baseline conversion 4%, the team wants to detect a 10% relative lift (absolute MDE = 0.004). `n ≈ 16 × 0.04 × 0.96 / 0.004² ≈ 38,400 per arm`. If the test ships with 30,000 users per arm over two weeks, it is under-powered for that MDE — recommend extending or reframing the expectation.

For continuous metrics, sample size scales with variance: `n ≈ 16 × σ² / MDE²`. Get the standard deviation from the pre-period.

Recommend the team compute power **before** scoping the duration, not after. The output of this skill should always include an explicit MDE check.

## SRM and AA-Test

Sample-ratio mismatch (SRM) is the leading indicator that a test is broken. If treatment and control receive 50/50 traffic by design but actual exposure is 50.4 / 49.6, the test infrastructure has a bug — even tiny SRM invalidates the result.

Recommend the team:

- Plan a chi-square SRM check on day 1 of the experiment (and again at midpoint). A p-value below 0.001 means stop the test and investigate the assignment pipeline.
- Run a 24–48 hour AA-test (control vs control) on the assignment pipeline before any new launch.
- Confirm assignment is logged independently of exposure (you need both — assignment for ITT analysis, exposure for treatment-on-treated).
- Watch for sample-ratio drift over time, which often signals a downstream filter applied unequally.

## Variance Reduction

Recommend CUPED (Controlled-experiment Using Pre-Experiment Data) or stratification when:

- The metric has rich pre-period history per unit (e.g., per-user spend last 30 days).
- The expected effect is small (<5% relative) and sample is finite.
- The team has the engineering capacity to compute the adjustment.

CUPED reduces variance by regressing the outcome on a pre-period covariate. Typical variance reduction: 20–50%, which translates to a 10–30% reduction in required sample size. Stratified sampling on a strong pre-period covariate gets a similar effect.

When CUPED is not feasible, recommend stratified randomisation on the most important blocking variable (country, plan, platform).

## Peeking and Stopping Rules

If the team plans to read the test mid-flight at fixed-horizon significance thresholds, recommend:

- **Pre-commit a decision date** and don't read the test before it.
- If business pressure to read early is real, switch to **sequential testing** (e.g., always-valid p-values via Howard et al., or Bayesian posterior with a decision boundary).
- For Bayesian designs, pre-register the prior, the decision boundary (e.g., "ship if P(treatment > control) > 95%"), and the loss function.

Peeking with fixed-horizon p-values inflates false positive rates substantially — a "significant" result halfway through a planned 4-week test is roughly twice as likely to be spurious as the headline p-value suggests.

## Network Effects and Spillover

Network effects break the SUTVA assumption (treatment of one unit doesn't affect another). Common cases:

| Pattern | Example | Mitigation |
|---|---|---|
| Marketplace two-sided | Test improves supplier visibility — diverts demand from control suppliers | Geo or cluster randomisation |
| Social product | Test changes user behaviour — affects friends in control | Cluster randomisation on social graph |
| Marketing channel | Email test changes user behaviour — affects paid attribution | Holdout at the user level across channels |
| Auction systems | Test raises bid — affects auction prices seen by control | Time-based switchback |

If spillover is plausible, recommend escalating to geo or cluster randomisation rather than treating it as a one-line caveat.

## Worked Examples

### Example 1: Ecommerce checkout button test, well-scoped

Hypothesis: changing the "Place order" button colour from green to orange increases checkout completion by ≥2% relative. Randomisation: user. Primary metric: checkout completion rate per assigned user. MDE: 2% relative on a 14% baseline = 0.0028 absolute. Traffic: 200K users / week.

Review: power check — `n ≈ 16 × 0.14 × 0.86 / 0.0028² ≈ 245,000 per arm`. With 100K per arm per week, a 2-week test is under-powered. Recommend extending to 5 weeks or accepting a higher MDE (5% relative would shrink the required `n` ~6×). Otherwise, design looks clean: clear hypothesis, sensible unit, exposure logging in place.

Verdict: **Needs fixes** — extend duration or revise MDE. AA-test recommended on day 1 to confirm assignment is balanced.

### Example 2: Email send-frequency test with sample-ratio risk

Hypothesis: increasing weekly email frequency from 2 to 3 lifts 28-day revenue per recipient. Randomisation: customer. Eligibility filter: "active in last 90 days" applied post-assignment.

Review: post-assignment eligibility filtering is the killer here. If "active in last 90 days" is recomputed at exposure time, treatment customers who receive an extra email may stay "active" while equivalent control customers tip into inactive — biasing the comparison. Recommend computing eligibility once at assignment and freezing it. Also recommend SRM check at day 1 and weekly thereafter; email send infrastructure is a common SRM source.

Verdict: **Needs fixes** — freeze eligibility at assignment, plan SRM monitoring, add unsubscribe / complaint as guardrail metrics.

### Example 3: Marketplace promo test with spillover risk

Hypothesis: a 10% supplier-side promo lifts marketplace gross merchandise value (GMV) by ≥3%. Randomisation: supplier.

Review: supplier-level randomisation in a marketplace with shared demand creates spillover — buyers shifting from control suppliers to treatment suppliers will inflate the measured lift without growing the market. Recommend switching to **geo randomisation** (10–20 matched markets) or **time-based switchback** if geo doesn't apply. SUTVA does not hold at the supplier level here.

Verdict: **Blocked** until randomisation unit is changed. Route to `/incrementality-test-designer` for a geo design.

## Anti-Patterns

- **No MDE.** "We'll run two weeks and look." The test ships under-powered and produces a null result that doesn't update anyone's beliefs.
- **Eligibility filtered after assignment.** Any filter computed post-assignment risks differential attrition. Lock eligibility at assignment.
- **Peeking with fixed-horizon p-values.** Reading the test on Friday because the meeting is Monday. Use sequential or commit to the horizon.
- **Multiple comparisons without correction.** Three primary metrics × five segments = 15 tests; one or two will be "significant" by chance.
- **Treating attribution as the primary metric.** "Did this campaign drive +X conversions per platform attribution?" is not a test result.
- **Network effects ignored as a one-line caveat.** Spillover invalidates SUTVA; mitigate it in the design or accept the test doesn't answer the causal question.
- **No pre-experiment AA / SRM check.** Half of "broken test" investigations turn out to be assignment pipeline bugs that an AA-test would have caught.
- **Underspecified treatment.** "Some users will see a new homepage" — which users, when, on what device, in which session?
- **Reporting relative lift as absolute.** "+12%" with no baseline is meaningless. Always report both.

## Output Template

```markdown
## Experiment Design Review

### Test Summary
<hypothesis, treatment, control, audience, randomisation unit>

### Readiness Verdict
<Ready / Needs fixes / Blocked>

### Design Review
| Area | Assessment | Risk | Fix |
|---|---|---|---|
| Hypothesis | <assessment> | <risk> | <fix> |
| Control | <assessment> | <risk> | <fix> |
| Randomisation unit | <assessment> | <risk> | <fix> |
| Eligibility | <assessment> | <risk> | <fix> |
| Primary metric | <assessment> | <risk> | <fix> |
| Guardrails | <assessment> | <risk> | <fix> |
| Sample / MDE / Power | <assessment with explicit n vs required n> | <risk> | <fix> |
| Duration | <assessment> | <risk> | <fix> |
| Pre-experiment health | <SRM / AA-test plan> | <risk> | <fix> |
| Variance reduction | <CUPED / stratification considered?> | <risk> | <fix> |
| Peeking / stopping | <fixed-horizon vs sequential> | <risk> | <fix> |
| Network effects | <spillover risk> | <risk> | <fix> |
| Analysis plan | <pre-registration / cuts / corrections> | <risk> | <fix> |
| External events | <window vs known events> | <risk> | <fix> |

### Metrics
Primary metric: <metric>
Guardrails:
- <metric>

### Power Check
- Baseline: <p or σ>
- MDE: <absolute>
- Required n per arm: <calculation>
- Planned n per arm: <number>
- Verdict: <powered / under-powered>

### Decision Rule
<exact rule the team will apply at read-out: ship / no-ship / iterate, including effect size and significance threshold>

### Pre-Launch Checklist
- [ ] AA-test or SRM monitoring plan in place
- [ ] Eligibility frozen at assignment
- [ ] Exposure logged independently of assignment
- [ ] Analysis plan written before launch
- [ ] Stop date pre-committed (or sequential design adopted)
```

## Quality Rubric

- `Strong`: hypothesis is decision-tied; power is calculated and adequate; SRM/AA plan is in place; randomisation unit handles spillover; analysis plan is pre-registered; decision rule is explicit.
- `Usable`: design is sound but power, SRM, or peeking discipline is implicit rather than explicit.
- `Needs revision`: power is undefined; eligibility computed post-assignment; planned peeking with fixed-horizon p-values; spillover dismissed without mitigation; primary metric is a platform-attributed conversion.

## Guardrails

- Do not treat observational before/after comparisons as randomised tests.
- Do not approve tests where treatment assignment is not logged independently of exposure.
- Do not use downstream metrics as primary if they will not mature during the test.
- Do not recommend sample-size precision without enough inputs; give directional guidance and demand the inputs before sign-off.
- Do not approve tests with planned peeking unless a sequential or Bayesian framework is adopted.
- Do not dismiss spillover with a guardrail line; redesign the randomisation unit.
- When spillover or interference is plausible at user level, route to `/incrementality-test-designer` for a geo or cluster design.
- When the question is causal at the channel or budget level rather than feature level, this is not an A/B test — route to `/incrementality-test-designer` or `/mmm-readiness`.
