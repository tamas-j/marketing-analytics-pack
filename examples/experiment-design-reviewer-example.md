# Experiment Design Reviewer Example

## Prompt

```text
/experiment-design-reviewer We want to test a 10% discount email against no discount for lapsed ecommerce customers. Goal is more purchases. Audience is 80,000 lapsed customers. We can randomise by customer_id and measure purchases over 14 days.
```

## Example Output

## Experiment Design Review

### Test Summary

The test compares a 10% discount email against a no-discount control for lapsed customers, randomised by `customer_id`, with purchases measured over 14 days.

### Readiness Verdict

Ready with fixes. The randomisation unit is appropriate, but the design needs a clearer primary metric, margin guardrail, and eligibility definition.

### Design Review

| Area | Assessment | Risk | Fix |
|---|---|---|---|
| Hypothesis | discount will increase lapsed customer purchases | purchase lift may be unprofitable | define margin-adjusted success |
| Control | no discount | good counterfactual if control receives no equivalent promo | ensure control is suppressed from other offers |
| Randomisation | customer_id | appropriate for email | log assignment before send |
| Audience | lapsed customers | lapsed definition unclear | define days since last purchase |
| Measurement window | 14 days | may miss delayed purchases | check historical response lag |

### Metrics

Primary metric: incremental purchases per assigned customer.

Guardrails:
- net revenue per assigned customer
- gross margin after discount
- unsubscribe rate
- repeat purchase after discount

### Data and Instrumentation Needs

- assignment flag
- send timestamp
- customer_id
- purchase timestamp
- net revenue
- discount amount
- unsubscribe event

### Decision Rule

Launch the discount only if it increases purchases and improves margin-adjusted net revenue per assigned customer without materially increasing unsubscribes.
