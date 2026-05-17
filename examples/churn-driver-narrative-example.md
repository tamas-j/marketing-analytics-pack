# Churn Driver Narrative Example

## Prompt

```text
/churn-driver-narrative Monthly churn rose from 6% to 9% for our subscription coffee brand. We have plan type, signup channel, discount code, skipped deliveries, cancellation reason, payment failures, and email engagement.
```

## Example Output

## Churn Driver Narrative

### Movement Summary

Monthly churn rose from 6% to 9%. The first read should separate voluntary cancellations from payment failures, then inspect whether the increase is concentrated in newer cohorts, discount-acquired customers, specific plan types, or customers showing lower engagement before cancellation.

### Likely Driver Narrative

The most plausible drivers are acquisition quality and early lifecycle friction. If discount-acquired customers or newer paid social cohorts account for most of the increase, the issue is likely lower-fit acquisition rather than a broad product problem. If churn follows skipped deliveries or payment failures, operational and billing fixes may be higher leverage than more lifecycle messaging.

### Evidence Table

| Driver | Evidence to check | Pattern that supports it | Priority |
|---|---|---|---|
| Acquisition quality | Churn by signup channel and discount code | Churn concentrated in paid or discount cohorts | High |
| Early tenure onboarding | Churn by months since signup | Increase concentrated in first 30-90 days | High |
| Delivery friction | Churn after skipped deliveries | Customers churn soon after skips | Medium |
| Involuntary churn | Payment failure rate and recovered payments | Failed payments rise with churn | High |
| Engagement decay | Email clicks before cancellation | Engagement drops before churn | Medium |
| Plan fit | Churn by plan type | One plan drives most churn increase | Medium |

### Segments to Inspect

- New customers from paid social.
- Customers acquired with first-month discounts.
- Customers with skipped deliveries.
- Customers with payment failures.
- Plan types with high cancellation reasons tied to value or frequency.

### Data Gaps

- Cancellation reasons may be incomplete or biased.
- Gross margin is needed before recommending discount-led save offers.
- Support contacts would help identify service issues.

### Recommended First Analysis

Build churn by signup month, channel, discount use, plan type, skipped delivery flag, and payment failure flag. Split voluntary and involuntary churn before making lifecycle recommendations.

### Actions After Validation

- If paid discount cohorts drive churn, tighten acquisition targeting or revise first-month offer.
- If payment failures drive churn, improve dunning and card update journeys.
- If skipped deliveries predict churn, test proactive delivery support or frequency controls.
