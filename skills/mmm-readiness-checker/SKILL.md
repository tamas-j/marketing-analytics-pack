---
name: mmm-readiness-checker
description: Use when checking whether marketing time-series data is suitable for media mix modelling, including outcome quality, spend/exposure fields, controls, history, variation, granularity, and risks.
---

# MMM Readiness Checker

This skill checks whether a dataset and business question are ready for media mix modelling. The pack's preferred MMM library is Google Meridian, but this readiness check is model-agnostic — the readiness gates apply to any MMM (Meridian, PyMC-Marketing, Robyn, classic stats, vendor).

MMM is expensive in calendar time, analyst time, and stakeholder patience. The single most common failure mode is running an MMM on data that can't credibly answer the budget question, and then arguing about the answer for a quarter. This skill exists to stop that.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive most of the readiness verdict.

1. **Business question.** What budget or contribution decision will the MMM inform? "Channel-level reallocation" is a different model from "what is connected TV worth?"
2. **Outcome metric and date grain.** What is the KPI, at what frequency? Weekly is the typical sweet spot; daily is noisy; monthly is too coarse for most decisions.
3. **History length and seasonal coverage.** How many periods, and do they cover at least two full annual seasonal cycles?
4. Media channels — paid search, paid social, display, video, CTV, audio, OOH, affiliate, partnerships, etc. — and whether spend OR impressions are available for each.
5. Controls — promotions, pricing, holidays, weather, macro, distribution, stock.
6. Geography or product / segment splits.
7. Known tracking changes, pricing changes, repositioning events, or COVID-era distortions.
8. Channels that are "always on" (no off-periods in the data).

## Readiness Thresholds

These are the hard thresholds. A `Blocked` verdict on any of the first four means the user is not ready.

| Check | Ready | Usable with caveats | Blocked |
|---|---|---|---|
| History length | ≥2 full seasonal cycles + the modelling window (≥104 weeks for weekly, ≥36 months for monthly) | 1 full cycle (52 weeks / 12 months) | <1 cycle |
| Outcome quality | Business KPI (orders, revenue, signups) with stable definition | Same KPI but with one definition change | Platform-attributed conversions only; or KPI definition changed mid-period |
| Variation in media | Each major channel has periods of high, low, and zero spend OR substantial week-to-week variation | Variation exists but always-on channels dominate | One or more major channels never varies; or all channels move in lockstep |
| Major control coverage | Holidays, promos, pricing, stock all available | Holidays + promos available; pricing missing | None of the major controls available |
| Channel granularity | Spend / impressions per channel, no omitted major channels | Spend grouped at category level (digital / TV / print) | Material channels not in dataset (e.g., affiliate ignored) |
| Geographic variation | Multiple geos with independent variation | National only, but rich time variation | National only + always-on channels (identification crisis) |
| Tracking stability | No major tracking change in the window | One tracking change documented | Multiple changes; pre/post inconsistent |

Any one `Blocked` row produces a `Blocked` overall verdict regardless of the rest.

## Readiness Verdicts

- **Ready** — enough history, variation, controls, and outcome quality to scope an MMM with confidence. Route to `/mmm-runner`.
- **Usable with caveats** — possible, but limitations must be documented in the model spec and stakeholder readout. State the caveats up front, not in the appendix.
- **Needs fixes** — core structure exists but specific fields, history, or controls need work before MMM can begin. List the fixes; do not start the runner.
- **Blocked** — not enough time series, variation, outcome quality, or channel data. Recommend an alternative measurement approach (incrementality tests, channel-level reporting) and re-check in 6–12 months.

## Decision Tree

Work through these in order. Stop at the first `Blocked` outcome.

1. **Is the business question a budget reallocation worth more than ~3 months of analyst + tooling cost?**
   → If no, MMM is the wrong tool. Recommend `/attribution-model-selector` or `/incrementality-test-designer` for cheaper answers.
2. **Is the outcome a business KPI (orders, revenue, signups), not a platform-attributed conversion?**
   → If no, **Blocked**. Platform-attributed outcomes turn MMM into "model the tracking," not "model demand."
3. **Is there ≥2 full seasonal cycles of history plus the modelling window?**
   → If less than 1 full cycle, **Blocked**. If 1 cycle, **Usable with caveats** — be plain that year-over-year seasonality is one observation.
4. **Does every major channel show meaningful variation (high / low / zero, or week-to-week variance ≥ ~30%)?**
   → If a major channel is always-on with no variation, **Blocked** for channel-level claims on that channel. Either run a flighting experiment first, or scope the MMM to exclude that channel's coefficient claims.
5. **Are the major confounders (holidays, promos, pricing, stock, distribution) in the dataset?**
   → If none, **Needs fixes**. MMM without these will give credit to media for non-media effects. Holidays and promos at minimum.
6. **Is there geographic variation, or is this national-only?**
   → National-only is workable if time variation is strong. If both national-only AND always-on channels, **Blocked** for the channel in question.
7. **Are there material tracking, pricing, or business-model changes in the window?**
   → If multiple, **Usable with caveats** at best; scope the model to a stable sub-window if possible.

## Input Priority

If the user can only fix two things before the MMM, fix in this order:

1. **Add missing controls.** Holidays and promos are non-negotiable. Pricing and distribution if material.
2. **Get channel variation.** Flighting (turning channels off in some weeks or geos) is the single biggest unlock. A flighting experiment for 6–12 weeks before MMM scoping is often worth more than another quarter of history.
3. Lengthen history if <2 cycles.
4. Add geographic variation if national-only.

## Worked Examples

### Example 1: DTC ecommerce, 3 years weekly, well-controlled

Question: reallocate $5M annual paid budget across 6 channels. Data: 156 weeks of revenue, weekly spend per channel, weekly promo flags, holiday calendar, weekly average price, weekly stock-status flag. Channels have all flighted at some point in the 3 years. National only.

Verdict: **Ready.** All thresholds met; national-only is fine given strong time variation. Route to `/mmm-runner` with Meridian. Scope: 6 channels, 156 weeks, controls = promo + price + stock + holiday. Plan one incrementality test on the largest planned reallocation as triangulation.

### Example 2: B2B SaaS, 18 months monthly, no controls, always-on paid

Question: justify paid search investment to the CFO. Data: 18 months of monthly signups, monthly spend per channel, no promo / pricing / launch flags. Paid search and paid social always-on. National only.

Verdict: **Blocked.** Three issues stack: <2 cycles of history, no controls, two channels always-on. MMM here would produce a confident-sounding number that's actually noise. Recommend: (a) build the missing controls inventory over the next quarter; (b) flight paid search down 30% in selected weeks or markets; (c) re-check at 24+ months of history. Bridge measurement: an incrementality test on paid search alone (`/incrementality-test-designer`).

### Example 3: Retail, 4 years weekly, 12 markets, one major repositioning event

Question: regional budget reallocation. Data: 208 weeks of revenue per market per channel; promos, prices, holidays, stock present; a major brand repositioning landed 14 months ago.

Verdict: **Usable with caveats.** Two options: (a) scope the model to the 60 weeks since repositioning (less history but a stable regime); (b) include a repositioning indicator and scope claims to "post-repositioning effect." Recommend (b) for richer history and explicit regime modelling. Document the repositioning as a known confound in the readout. Route to `/mmm-runner` with explicit caveats; budget 2x the usual analyst time for sensitivity analysis.

## Anti-Patterns

- **MMM on platform-attributed conversions.** The model ends up modelling the platform's attribution, not demand. Always use a business KPI.
- **MMM on always-on channels with no flighting.** Coefficients become identified only by trend, not by media variation. Results look confident but are essentially priors.
- **Running MMM to "settle" a stakeholder argument.** If stakeholders are at war over channel ROI, MMM is unlikely to resolve it — both sides will dispute the priors and the controls. Recommend incrementality on the disputed channel first.
- **Ignoring repositioning, COVID, pricing changes.** These are structural breaks. Either scope the window around them or model them explicitly.
- **MMM on monthly data with a 12-month history.** 12 observations is not a time series.
- **Modelling 12 channels when 4 actually matter.** Multi-collinearity explodes; coefficients destabilise. Aggregate small channels into "other."
- **Treating the readout as a precise allocation table.** MMM produces credible intervals, not point estimates. Stakeholders will round to the point estimate; the readout needs to fight that.
- **Skipping the readiness check because "we have a vendor doing it."** Vendor MMM runs on whatever data you give it; readiness is the customer's responsibility, not the vendor's.

## Output Template

```markdown
## MMM Readiness Check

### MMM Question
<budget or contribution question, with the specific decision the MMM will support>

### Readiness Verdict
<Ready / Usable with caveats / Needs fixes / Blocked>

### Threshold Scorecard
| Check | Status | Notes |
|---|---|---|
| History length | <Ready / Caveats / Blocked> | <numbers> |
| Outcome quality | <status> | <KPI and definition stability> |
| Variation in media | <status> | <which channels lack variation> |
| Control coverage | <status> | <which controls are present / missing> |
| Channel granularity | <status> | <gaps> |
| Geographic variation | <status> | <markets / national> |
| Tracking stability | <status> | <known changes> |

### Gaps and Risks
- <risk tied to a threshold>

### Required Fixes (if Needs fixes or Blocked)
1. <fix in priority order from Input Priority section>
2. <fix>

### Recommended Modelling Scope (if Ready or Caveats)
- Channels: <list>
- Controls: <list>
- Window: <date range>
- Caveats to surface in readout: <list>

### Bridge Measurement (if Blocked)
<what to use instead until MMM is ready — usually incrementality + channel reporting>

### Next Step
<command — usually /mmm-runner, /incrementality-test-designer, or a data-collection plan>
```

## Quality Rubric

- `Strong`: every threshold scored explicitly, fixes ranked by impact, caveats named for the readout (not just the design), bridge measurement recommended if blocked.
- `Usable`: verdict given with rationale but threshold scorecard is incomplete or fix priority is implicit.
- `Needs revision`: "Ready" verdict on data without 2 cycles of history; MMM recommended on platform-attributed outcomes; always-on channels accepted without flagging the identification problem.

## Guardrails

- Do not overpromise channel-level precision.
- Do not ignore non-media controls.
- Do not recommend a heavy MMM runner before readiness is clear.
- Do not use MMM to answer creative, audience, or short-campaign questions better suited to experiments.
- Do not accept "we'll just run it and see" — readiness gates exist because a bad MMM is worse than no MMM.
- When channels are always-on, recommend a flighting experiment via `/incrementality-test-designer` before MMM scoping.
- When the question is feature- or creative-level, this is not an MMM question — route to `/experiment-design-reviewer`.
- When the question is "did this specific campaign work," route to `/incrementality-test-designer`.
- After a Ready verdict, route to `/mmm-runner` for scoping and execution.
