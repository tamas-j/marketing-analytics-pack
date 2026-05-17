# Incrementality Test Designer Example

## Prompt

```text
/incrementality-test-designer We want to know if paid social prospecting drives incremental new subscribers. We can split by region, have 18 months of daily spend and signups, and can pause spend in some regions for four weeks.
```

## Example Output

## Incrementality Test Design

### Question

Does paid social prospecting create incremental new subscribers beyond what would have happened without spend?

### Recommended Design

Use a geo holdout or matched-market test. A user-level holdout is unlikely to be feasible for broad paid social prospecting, while the ability to pause spend in regions creates a practical causal test.

### Test Setup

| Element | Recommendation |
|---|---|
| Population | eligible regions with stable historical signup volume |
| Treatment | continue paid social prospecting |
| Control | pause or materially reduce prospecting spend |
| Outcome | new subscribers, plus subscriber quality guardrails |
| Window | four-week test plus agreed lag window |

### Data Requirements

- daily spend by region
- daily signups by region
- historical pre-period signups
- other channel spend by region
- seasonality or promotional calendar
- subscriber quality or early churn by region

### Analysis Plan

1. Match regions using pre-period signup trends and spend patterns.
2. Confirm treatment and control regions have similar pre-test trends.
3. Run the four-week holdout with minimal other regional changes.
4. Estimate incremental signups and cost per incremental subscriber.
5. Check early subscriber quality and churn guardrails.

### Risks and Mitigations

- Regional spillover: choose geographically distinct regions where possible.
- Other channel changes: freeze or log regional campaign changes.
- Short window: include a lag window and avoid overreading noisy regions.

### Decision Rule

Scale paid social only if cost per incremental subscriber is within target and early quality is not materially worse than baseline.
