# Front Door Example

## Prompt

```text
/plan-analysis We want to know whether our spring paid social campaign actually helped acquire profitable subscribers. We have campaign spend by day, signups by day, plan type, discount code, and cancellations.
```

## Example Output

### Question Understood

You want to know whether the spring paid social campaign created profitable subscriber growth, not just whether signups increased.

### Best Next Step

Start with `/check-data`, then move to an incrementality or campaign post-mortem workflow once the data grain is confirmed.

### Why This Fits

The question is partly a campaign effectiveness question and partly a profitability question. Before judging impact, the dataset needs enough structure to connect spend, signup timing, subscriber value, discounting, and churn. A basic campaign trend may be possible, but a true incrementality read needs a control, holdout, geo split, pre/post design, or another credible comparison.

### What I Need From You

- The campaign dates.
- Whether there was a holdout, test region, or untreated comparison group.
- Whether subscriber value or margin is available by plan.
- A sample of the columns in each file.

### Data Readiness

Partial. The listed fields are useful, but incrementality is blocked unless there is a credible comparison group or pre/post design.

### Suggested Sequence

1. Run `/check-data` on the spend, signup, and cancellation files.
2. Build a KPI tree for profitable subscriber acquisition if the success metric is not settled.
3. Choose an incrementality or post-mortem workflow based on whether a comparison group exists.
