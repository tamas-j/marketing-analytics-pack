# CLV Scenario Example

## Prompt

```text
/clv-scenario We run a subscription coffee brand. Monthly subscription revenue is 28 GBP, gross margin is about 55%, monthly churn is around 8%, CAC is 42 GBP, and first month discount costs about 8 GBP. Can we afford to scale paid social?
```

## Example Output

## CLV Scenario Model

### Decision Summary

This model estimates whether paid social acquisition is economically viable at a 42 GBP CAC. The key question is whether retained gross margin over the customer lifetime is comfortably above CAC and first-month incentive cost.

### Formula Used

Subscription CLV:

`gross CLV = monthly ARPU x gross margin / monthly churn rate`

`net CLV = gross CLV - CAC - incentive cost`

This fits because the business has recurring monthly revenue and a churn assumption.

### Assumptions

| Assumption | Cautious | Base | Optimistic | Notes |
|---|---:|---:|---:|---|
| Monthly ARPU | 28 GBP | 28 GBP | 28 GBP | Subscription price |
| Gross margin | 50% | 55% | 58% | Needs validation after shipping and discounts |
| Monthly churn | 10% | 8% | 6% | Biggest sensitivity |
| CAC | 48 GBP | 42 GBP | 36 GBP | Paid social acquisition cost |
| First-month discount cost | 8 GBP | 8 GBP | 6 GBP | Incentive cost |

### Scenario Results

| Scenario | Gross CLV | Acquisition cost | Net CLV | CLV:CAC | Payback | Readout |
|---|---:|---:|---:|---:|---:|---|
| Cautious | 140 GBP | 48 GBP | 84 GBP | 2.9x | 3.4 months | Viable but not much room for worse churn |
| Base | 193 GBP | 42 GBP | 143 GBP | 4.6x | 2.7 months | Paid social looks scalable if churn is stable |
| Optimistic | 271 GBP | 36 GBP | 229 GBP | 7.5x | 2.2 months | Strong economics if retention improves |

### Sensitivity Notes

- Monthly churn is the biggest driver. Moving from 8% to 10% cuts gross CLV from about 193 GBP to 140 GBP.
- CAC matters, but the model is more sensitive to retention because churn affects every future month.
- Gross margin should include shipping, coffee cost, fulfilment, and typical discounts.

### Guardrails and Caveats

- This is a planning model, not proof that paid social is incremental.
- Paid social cohorts may churn faster than blended customers.
- Discount-acquired customers may have lower retention or lower second-month margin.
- Refunds, failed payments, and support costs are not included.

### Data Needed Next

- Cohort churn by acquisition channel.
- Gross margin by subscription plan.
- Discount usage by first-month cohort.
- Failed payment and cancellation reason rates.
- Paid social CAC by campaign and creative.

### Recommended First Analysis

Compare 90-day retention and gross margin for paid social subscribers versus organic and email-acquired subscribers. If paid social customers have meaningfully worse churn, use channel-specific CLV before scaling spend.
