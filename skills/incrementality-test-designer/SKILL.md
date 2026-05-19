---
name: incrementality-test-designer
description: Use when designing incrementality tests for marketing campaigns, channels, CRM journeys, offers, or media using holdouts, geo tests, matched markets, switchbacks, or quasi-experimental fallbacks.
---

# Incrementality Test Designer

This skill designs practical incrementality tests. It helps users answer "what happened **because of** this marketing activity?" rather than "what did the platform attribute to it?"

The skill is opinionated about three things teams routinely get wrong: **spillover**, **parallel trends**, and **decision rules pre-committed before the test runs**. A test without a decision rule is a test that produces a debate.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first four drive the design choice.

1. **Intervention.** What is being turned on or off — campaign, channel, journey, offer, budget change, creative variant?
2. **Decision the result will inform.** Continue / stop / scale / reallocate. The decision dictates the required precision.
3. **Whether random user-level holdout is operationally possible.** If yes, that is almost always the best design.
4. **Geography or audience structure.** Number of markets, comparability, cross-market spillover risk.
5. Outcome metric and how quickly it matures.
6. Campaign timing and duration.
7. Historical data — how much pre-period exists per geo / cohort?
8. Operational constraints — can the team suppress in certain platforms, hold back creative, run a PSA?

## Design Options

| Design | Best for | Requirements | Watch-out | Causal strength |
|---|---|---|---|---|
| **User-level holdout** | CRM, lifecycle, owned channels, paid retargeting | Stable IDs and ability to suppress in the channel | Cross-channel contamination | Highest |
| **Geo holdout (RCT)** | Paid media, offline, broad campaigns | Many comparable geos, ability to turn off by geo | Cross-geo media spill | High |
| **Matched markets (synthetic control)** | Campaigns where random geo split is not possible | 18+ months of pre-period geo data | Weaker than randomisation; needs careful market matching | Medium |
| **Switchback (time-based)** | Auctions, dynamic pricing, time-based operations | Repeated on/off periods with cleanup gaps | Seasonality, carryover, day-of-week | Medium-high |
| **PSA / placebo creative** | Media platforms that won't allow a true holdout | Platform accepts a control creative | Control creative may still drive effects | Medium |
| **Difference-in-differences** | Quasi-experimental fallback | Pre/post + comparison group, parallel trends | Parallel-trend assumption is hard to verify | Medium-low |
| **Interrupted time series** | One-off launches with no comparison group | Stable pre-period | Cannot rule out concurrent events | Low |

## Decision Tree

Work through these in order. Stop at the first design that is feasible.

1. **Is the intervention an owned-channel campaign (email, push, in-product, CRM)?**
   → Recommend a **user-level holdout** (5–20% withheld). This is almost always operationally cheap and is the strongest design.
2. **Is the intervention a paid media campaign in a platform that supports holdouts (Meta, YouTube)?**
   → Recommend a **platform-level user holdout** (Meta Conversion Lift, YouTube Brand Lift) for headline metrics, plus a parallel **geo test** if budget allows triangulation.
3. **Is the intervention a multi-channel or always-on programme?**
   → Recommend a **geo holdout** (10–20 matched markets randomly assigned). Plan power based on the number of markets, not impressions — geo tests are noisy.
4. **Is geo random assignment infeasible (only 2–3 markets, or markets are very different)?**
   → Recommend **matched markets / synthetic control** with explicit pre-period fit metrics. Be honest about reduced causal strength.
5. **Is the intervention something that changes on a fast cadence (dynamic pricing, auction bidding)?**
   → Recommend a **switchback** with cleanup windows between switches.
6. **Is the platform unwilling to support a true holdout?**
   → Recommend a **PSA / control-creative** design. Pre-commit that PSA creative is documented as the control.
7. **None of the above feasible?**
   → Recommend a **difference-in-differences** or **interrupted time series** quasi-experimental analysis with explicit assumption checks. Be plain about the limitation in the readout.

## Power for Geo Tests

Geo tests are routinely under-powered because teams plan on impression count instead of market count. The unit of analysis is the **geo**, not the user. A test across 6 markets has 6 observations, not 6 million.

Rough rule of thumb for a 2-arm geo test with α=0.05, power=0.80:

- 8–10 matched market pairs → can detect ~10–15% relative lift on a well-matched series.
- 4–6 pairs → can only detect ~25–40% relative lift; null results are uninformative.
- <4 pairs → use synthetic control, not a t-test.

If the team has 4 markets and wants to see 5% lift, the design cannot answer the question. Surface that before launch.

## Spillover Mitigations

Spillover between treatment and control is the most common reason results don't match expectations. Treat it in the design, not the readout.

| Spillover source | Mitigation |
|---|---|
| Cross-channel (treated users see other channels too) | Choose a unit that contains the channel mix; report results per-channel-as-treated |
| Cross-geo media (Connected TV bleeds across DMA) | Use DMAs that are not adjacent; check media-buying rules |
| Social / referral | Cluster randomisation; geo if cluster is intractable |
| Auction effects (treatment bidder raises CPMs) | Switchback or platform-level lift study |
| Word-of-mouth | Longer post-period; accept the bias and disclose |

## Parallel Trends and Pre-Period Checks

Every design except true RCT user-level holdout depends on the assumption that treatment and control would have moved together absent the intervention. Pre-period checks should be part of the design, not an afterthought.

Required checks before approval:

- **Pre-period correlation:** treatment and control series correlated >0.85 over a comparable seasonal window.
- **Visual inspection:** plot treatment and control over the pre-period and confirm parallel motion.
- **Placebo test:** apply the analysis to a fake "treatment" date in the pre-period; if it shows a significant effect, the analysis is biased and needs rework.
- **Covariate balance:** key market-level covariates (population, baseline metric, seasonality) are balanced across arms.

If pre-period correlation is below 0.85 or the placebo test fails, recommend matched markets with explicit weights or do not proceed.

## Worked Examples

### Example 1: CRM team wants to know if a re-engagement email drives incremental revenue

Intervention: a 3-email reactivation sequence to customers inactive 60+ days. Decision: continue / stop the journey. Data: 90 days of customer history, full email send / open / revenue logs.

Recommendation: **10% user-level holdout**, randomised at customer level, suppress from all reactivation comms for 30 days. Primary metric: revenue per customer over the 30-day window. Secondary: open rate (to confirm suppression worked), unsubscribe rate (guardrail). Decision rule: continue if incremental revenue per holdout customer exceeds the program's variable cost at 80% posterior probability.

Why this fits: owned channel, stable IDs, operationally cheap to suppress. User-level holdout is the strongest design.

### Example 2: Paid social budget decision, brand wants to know what their always-on Meta spend drives

Intervention: 15% of Meta budget. Decision: hold / cut / scale. Data: 12 months of weekly conversions and spend; offline conversions for 60% of sales.

Recommendation: **geo holdout in 10 matched DMA pairs** (turn off Meta spend in 10 DMAs for 6 weeks, hold spend in 10 paired DMAs). Synthetic control as a secondary analysis. Decision rule pre-committed: incremental ROI must exceed 1.2× to scale; below 0.8× to cut. Run a platform-level Conversion Lift study in parallel for triangulation.

Why this fits: paid media question, always-on programme, sufficient market count for a real geo test. Platform-level lift alone would not satisfy the "should we cut?" question.

### Example 3: Marketplace team wants to test a supplier-side promotional credit

Intervention: $50 credit to suppliers in a treatment cell. Decision: roll out / abandon. Data: marketplace event log, 14 markets.

Recommendation: **switchback or geo, not user-level**. Supplier-level randomisation creates demand spillover (buyers shift from control suppliers to treatment suppliers within the same market). Best design: switch the credit on / off in 4-week alternating windows across all suppliers, with a 1-week cleanup gap. If switching isn't operationally clean, fall back to geo with 7 matched market pairs and accept reduced power.

Why this fits: SUTVA is violated at the supplier level. Switchback contains the spillover within each window.

## Anti-Patterns

- **User holdout where cross-channel contamination is large.** Holding a user out of email but they still see paid; the "incremental revenue" attributed to email actually moved across channels.
- **Geo test with <6 markets and a t-test.** Insufficient power; null result is uninformative.
- **No decision rule pre-committed.** The result lands and the team debates whether it counts.
- **Reading geo tests at the impression level instead of the market level.** The unit of analysis is the geo; impression counts make a small-n test look big.
- **Skipping the pre-period parallel-trends check on a synthetic control.** Without it, the synthetic control is dressing up a difference-in-differences with poor balance.
- **PSA creative that's actually a strong message.** Picking a charity ad with strong emotional pull as "control" — it's still driving brand effects.
- **Calling a before/after comparison incrementality.** Without a control, before/after is just a time series.
- **Combining incrementality and attribution numbers in the same readout without flagging the difference.** Stakeholders read them as the same thing.

## Output Template

```markdown
## Incrementality Test Design

### Question
<causal question — what would happen without this marketing activity?>

### Recommended Design
<design and why; if a stronger design is infeasible, name it and explain why>

### Test Setup
| Element | Recommendation |
|---|---|
| Population | <population> |
| Treatment | <treatment> |
| Control | <control> |
| Randomisation unit | <unit and why> |
| Outcome | <metric> |
| Window | <duration with rationale> |
| Sample size / market count | <numbers> |

### Power Check
<for user-level: arm sizes and MDE. For geo: market pair count and detectable lift.>

### Pre-Period Checks (required before launch)
- [ ] Treatment / control pre-period correlation ≥ 0.85
- [ ] Placebo test on a fake pre-period date returns null
- [ ] Covariates balanced across arms
- [ ] Spillover sources identified and mitigated

### Data Requirements
- <field>

### Analysis Plan
1. <step — pre-registered>
2. <step>
3. <step>

### Decision Rule (pre-committed)
<exact rule the team will apply at read-out: "continue if lift ≥ X% at 80% posterior probability", or "scale if incremental ROI > 1.2×", etc.>

### Risks and Mitigations
- <risk and mitigation>

### Reporting Frame
<how the result will be communicated, including the distinction from platform-attributed numbers if both are reported>
```

## Quality Rubric

- `Strong`: design chosen explicitly because stronger options are infeasible; spillover addressed in the design; pre-period checks named; power calculated against the right unit (markets for geo, users for user holdout); decision rule pre-committed.
- `Usable`: sensible design with most safeguards in place but power or spillover mitigation is implicit.
- `Needs revision`: geo test with <6 markets and a t-test; no pre-period checks; no decision rule; PSA control that's actually a brand message; user-holdout where cross-channel contamination dominates.

## Guardrails

- Do not present attribution, matched markets, or before/after as equivalent to randomised holdout.
- Do not ignore spillover between treatment and control.
- Do not use a control group that can still receive the same treatment elsewhere.
- Do not use outcomes that mature after the measurement window without caveats.
- Do not approve a geo test without checking market count against required power.
- Always require a pre-period parallel-trends check for matched markets or DiD.
- Always require a pre-committed decision rule before launch.
- When the question is "what does my budget mix yield?" rather than "does this campaign work?", route to `/mmm-readiness`.
- When the question is feature-level rather than campaign-level, route to `/experiment-design-reviewer`.
