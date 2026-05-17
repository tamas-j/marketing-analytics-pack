# Attribution Model Selector Example

## Prompt

```text
/attribution-model-selector We need to decide how to measure paid search, paid social, email, and affiliates for ecommerce budget allocation. We have GA4 paths, platform reports, spend by day, and orders, but cross-device tracking is patchy.
```

## Example Output

## Attribution Approach Recommendation

### Attribution Question

The decision is budget allocation across paid search, paid social, email, and affiliates for ecommerce growth.

### Recommended Approach

Use a blended measurement framework: rules-based attribution for operational reporting, incrementality tests for key channels, and MMM later if enough time-series history and spend variation are available.

### Why This Fits

GA4 path data and platform reports are useful for directional reporting, but patchy cross-device tracking makes user-level attribution unreliable for budget allocation. Because the decision is causal, paid social and affiliates should be tested with incrementality designs where possible. Paid search may need brand/non-brand separation before interpreting results.

### Data Requirements

- spend by day and channel
- orders and revenue by day
- campaign and channel taxonomy
- GA4 path and source/medium data
- experiment or geo holdout flags where available
- margin or refund guardrails

### Limitations

- Platform reports may over-credit their own channels.
- GA4 paths may miss cross-device journeys.
- Email can look strong in last-touch attribution because it is lower funnel.
- Affiliate incrementality can be weak if partners capture existing demand.

### If You Need Incrementality

Design channel-specific tests:

- paid social: geo holdout or conversion lift test
- affiliates: publisher holdout or voucher-code incrementality check
- email: user-level holdout
- paid search: brand/non-brand split and geo or budget switchback where feasible

### Next Step

Run `/incrementality-test-designer` for the highest-spend or most uncertain channel before making major budget shifts.
