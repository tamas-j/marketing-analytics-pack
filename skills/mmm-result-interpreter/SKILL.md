---
name: mmm-result-interpreter
description: Use when interpreting media mix model outputs, including contribution, ROI, marginal ROI, response curves, uncertainty, diagnostics, caveats, budget implications, and validation steps.
---

# MMM Result Interpreter

This skill translates MMM outputs into practical business interpretation. It is opinionated about three things stakeholders routinely conflate: **contribution vs ROI vs marginal ROI**, **uncertainty vs ranking**, and **diagnostics before recommendations**.

The most common mistake this skill exists to prevent is reading the point estimate of channel ROI as a precise number and immediately reallocating budget. MMM produces posterior distributions; treating them as point estimates is the largest single source of MMM regret.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive most of the interpretation.

1. **Model diagnostics.** Convergence (R-hat / ESS), holdout / backtest performance, residual patterns, in-sample fit. Without these, channel claims aren't yet earned.
2. **Channel contribution, ROI, and marginal ROI with credible intervals.** All three. Each answers a different question.
3. **Response curves / saturation outputs.** Where does each channel sit on its curve?
4. Known caveats: excluded variables, structural breaks, channels with poor variation.
5. Current budget allocation and decision context.
6. Triangulating evidence: incrementality tests, geo lifts, prior MMM runs.
7. Stakeholder audience for the readout.

## Interpretation Order

Do not jump to the budget recommendation. Work through these in order.

1. **Check diagnostics and scope.** Did the model converge? Does it fit the holdout? Are residuals patterned (auto-correlated, heteroscedastic)?
2. **Summarise what the model can and cannot answer.** Be explicit. Channels with poor variation get caveats up front, not in the appendix.
3. **Interpret contribution.** What share of the outcome do paid channels collectively explain, vs baseline + controls?
4. **Interpret ROI and marginal ROI separately.** Average ROI tells you what each historical dollar returned. Marginal ROI tells you what the next dollar would return. Budget decisions need marginal ROI.
5. **Inspect saturation and response curves.** Which channels are near saturation? Which have headroom?
6. **Highlight uncertainty.** Where credible intervals overlap, channels are not statistically different — don't rank them.
7. **Translate into recommendations.** Pre-commit thresholds: "shift budget only where marginal ROI gap exceeds X and intervals don't overlap."
8. **Recommend validation experiments.** The MMM's most uncertain claims should be the first incrementality tests.

## Diagnostic Thresholds

Recommend not proceeding to interpretation until these pass. If the runner output doesn't include them, request them.

| Diagnostic | Healthy threshold | Concerning | Action if failed |
|---|---|---|---|
| R-hat (Gelman-Rubin) | <1.01 across all parameters | 1.01–1.05 | Re-run with more chains / iterations |
| Effective sample size (ESS) | >1000 per parameter | 400–1000 | More samples; suspect funnel geometry |
| Posterior predictive check | Holdout MAPE close to in-sample | Holdout error >2× in-sample | Likely overfit; simplify priors |
| Residual autocorrelation | No significant lags | Lag-1 or lag-52 autocorrelation | Missing seasonality / trend / unmodelled control |
| Coefficient stability | Stable across leave-one-out runs | Coefficients flip sign with one window dropped | Channel coefficient is not identified |
| Decomposition reasonableness | Baseline + media sum to outcome with sensible split (typically 20–60% media for paid-heavy brands) | Baseline <10% or >90% | Often a prior / scaling issue |

## Contribution vs ROI vs Marginal ROI

These are three different questions. Every readout needs all three, and most readouts collapse them.

| Output | Question it answers | Use for | Common misuse |
|---|---|---|---|
| **Contribution (incremental units / revenue)** | "How much of the outcome did each channel cause?" | Allocating credit; communicating channel size; comparing vs prior period | Treating contribution share as budget share |
| **Average ROI** | "What did historical spend return on average?" | Performance reporting; trend analysis | Using avg ROI to decide marginal allocation |
| **Marginal ROI (mROI)** | "What would the next dollar return at current spend?" | Budget reallocation | Reporting only average ROI |

Avg ROI of paid social at 3.2× and marginal ROI at 0.9× tells two completely different stories. Avg ROI says "this has been a good channel"; marginal ROI says "the next dollar is below break-even." Both are right. The budget decision rests on marginal ROI.

## Uncertainty and Ranking

Posterior credible intervals matter more than the point estimate. Two rules to apply:

1. **Overlapping intervals = not different.** If channel A's 80% CI for ROI is [1.4, 2.8] and channel B's is [1.6, 3.2], they overlap heavily — do not rank them or shift budget between them based on point estimates.
2. **Report the spread, not just the centre.** "Paid search ROI is 2.4 (80% CI 1.6–3.2)" is honest. "Paid search ROI is 2.4" implies precision that isn't there.

For a typical MMM, credible intervals on marginal ROI are often ±30–50% of the centre. That width is not a flaw of the model; it's the truth about the data. The readout should reflect it.

## Response Curves and Saturation

Each channel has a response curve. The same channel may be high-ROI when underspent and zero-ROI when saturated. Three patterns to flag:

- **Saturated channel (high contribution, low marginal ROI):** marginal ROI well below average ROI. Recommendation: hold or cut, not scale.
- **Underspent channel (low contribution, high marginal ROI):** above break-even at current spend. Recommendation: test scaling with an incrementality study at the new level before committing.
- **Linear-looking channel (flat curve):** poorly identified, often always-on. Recommendation: treat coefficients as uncertain; the curve isn't credible without flighting variation.

When a recommendation involves scaling a channel materially beyond historical spend, flag that the model is extrapolating outside its support — response curves are most credible inside the spend range observed in the data.

## Worked Examples

### Example 1: Healthy readout, clear recommendation

Diagnostics: R-hat 1.005, holdout MAPE 8.2% (in-sample 7.1%), no residual autocorrelation. Decomposition: 38% media, 62% baseline + controls. Channels: paid search avg ROI 2.8 (CI 2.1–3.5), mROI 1.9 (CI 1.4–2.6). Paid social avg ROI 1.6 (CI 1.0–2.3), mROI 0.7 (CI 0.3–1.2). Connected TV avg ROI 0.9 (CI 0.4–1.6), mROI 1.4 (CI 0.8–2.3). Curves: paid social near saturation, CTV in headroom.

Interpretation: paid social is saturated — its average ROI of 1.6 is real but the next dollar yields 0.7. Recommend cutting paid social by ~15% and reinvesting in CTV, where marginal ROI of 1.4 exceeds paid social's marginal ROI of 0.7 with non-overlapping intervals. Validate the shift with a six-month CTV scale-up tracked by geo lift. Hold paid search.

### Example 2: Caveat-heavy readout, recommendation hedged

Diagnostics: R-hat 1.02 on two channel coefficients, holdout MAPE 14% (in-sample 9%). Decomposition: 22% media, 78% baseline. Paid search and paid social both always-on for entire window; their coefficients have wide intervals.

Interpretation: this model is not yet decision-grade for paid search vs paid social. The diagnostics flag convergence issues, and both channels lack variation needed to identify their coefficients. Marginal ROI estimates exist but credible intervals overlap heavily. Recommendation: do **not** reallocate between paid search and paid social based on this output. Validate with an incrementality test on the channel with the higher point estimate. The model can support directional claims about TV and OOH where variation is richer.

### Example 3: Counter-intuitive result, validate before acting

Model says affiliate marketing has marginal ROI of 4.1 (CI 2.8–5.8) — well above any other channel. Stakeholders want to triple affiliate budget tomorrow.

Interpretation: a marginal ROI 2–3× higher than other channels usually indicates one of four things: (a) the channel really is undervalued and underspent; (b) attribution leakage — affiliate gets credit for traffic that would have converted anyway; (c) a control variable correlated with affiliate spend is missing; (d) the channel is on the steep part of a curve and "tripling" would extrapolate far outside the data. Recommendation: scale by 30% as a test, run an incrementality study at the new spend level, re-run MMM with the additional data. Do not 3× a channel on a single MMM result, no matter how attractive.

## Anti-Patterns

- **Reading point estimates.** Treating posterior medians as precise numbers and reallocating accordingly.
- **Skipping diagnostics.** Going straight to channel ROI without checking convergence or holdout fit.
- **Using average ROI for budget decisions.** Average answers "was this channel good historically?" Marginal answers "should I add a dollar?" Most reallocation arguments use the wrong one.
- **Ranking channels with overlapping credible intervals.** Producing an ordered list when the intervals say "not different."
- **Ignoring response-curve position.** Recommending a 50% scale-up on a channel near saturation.
- **Extrapolating outside the spend support.** Recommending a 3× scale-up of a channel that has never been spent at that level.
- **Using MMM to settle a feature or creative argument.** MMM has no signal at that level. Route to experiments.
- **Hiding caveats in the appendix.** Always-on channels, structural breaks, and missing controls belong on slide 2, not slide 22.
- **Pretending the MMM has converged when R-hat says it hasn't.** Either re-run or downgrade the claims.

## Output Template

```markdown
## MMM Result Interpretation

### Executive Readout
<3-5 sentences: what the model says, what the recommendation is, what the biggest caveat is>

### Diagnostics Check
| Diagnostic | Readout | Healthy? | Implication |
|---|---|---|---|
| R-hat | <value> | <yes / no> | <implication> |
| ESS | <value> | <yes / no> | <implication> |
| Holdout fit | <metric> | <yes / no> | <implication> |
| Residual pattern | <description> | <yes / no> | <implication> |
| Decomposition | <% baseline / media split> | <yes / no> | <implication> |

### Channel Interpretation
| Channel | Contribution | Avg ROI (CI) | Marginal ROI (CI) | Curve position | Interpretation |
|---|---:|---|---|---|---|
| <channel> | <%> | <value (CI)> | <value (CI)> | <under / linear / saturated> | <readout> |

### Budget Implications
| Channel | Current spend | Recommended action | Confidence | Validation needed before scaling |
|---|---:|---|---|---|
| <channel> | <$> | <hold / scale +X% / cut -X%> | <high / medium / low> | <test recommendation> |

### Caveats and Uncertainty
- <caveat — surfaced up front, not hidden>

### Follow-Up Tests or Data Improvements
- <next test, prioritised by where MMM is least certain>

### What This Model Cannot Answer
- <feature-level / creative-level / short-campaign questions belong elsewhere>
```

## Quality Rubric

- `Strong`: diagnostics scored first; contribution / avg ROI / mROI separated explicitly; credible intervals reported with point estimates; channel ranking respects interval overlap; recommendations are conditional on validation; caveats are surfaced in the executive readout.
- `Usable`: interpretation is sound but uses point estimates without intervals, or ranks channels with overlapping CIs.
- `Needs revision`: budget recommendation based on avg ROI; channels with non-converged coefficients treated as decision-grade; saturated channel recommended for scaling; counter-intuitive results actioned without an incrementality test.

## Guardrails

- Do not interpret contribution or ROI before checking diagnostics.
- Do not treat wide uncertainty intervals as precise ranking.
- Do not shift budget from average ROI alone when marginal ROI is available.
- Do not compare channels without considering spend scale and saturation.
- Do not extrapolate response curves far beyond the spend range observed.
- Always recommend an incrementality test before any large reallocation (≥20% shift in a channel).
- Always report credible intervals alongside point estimates.
- When the recommendation depends on a poorly converged or always-on channel coefficient, downgrade confidence and recommend `/incrementality-test-designer`.
- When stakeholders treat the readout as a precise allocation table, push back explicitly — MMM produces ranges, not points.
