# Frequency Cap Fatigue Example

## Prompt

```text
/frequency-cap-fatigue We send lifecycle email. Last 30 days: customers with 1-2 sends had 18% click rate and 0.2% unsubscribe, 3-5 sends had 14% click and 0.5% unsubscribe, 6-8 sends had 9% click and 1.1% unsubscribe, 9+ sends had 5% click and 2.4% unsubscribe.
```

## Example Output

## Frequency Cap and Fatigue Analysis

### Question

Assess email fatigue over the last 30 days and recommend a practical frequency rule.

### Frequency Bands

| Band | Definition | Audience share | Engagement | Conversion | Negative signal | Readout |
|---|---|---:|---:|---:|---:|---|
| Low | 1-2 sends | unknown | 18% click | not supplied | 0.2% unsubscribe | healthy engagement |
| Medium | 3-5 sends | unknown | 14% click | not supplied | 0.5% unsubscribe | acceptable pressure |
| High | 6-8 sends | unknown | 9% click | not supplied | 1.1% unsubscribe | fatigue risk |
| Very high | 9+ sends | unknown | 5% click | not supplied | 2.4% unsubscribe | likely over-contact |

### Recommended Rule

Use a default cap of 5 lifecycle marketing emails per customer per 30 days, with exceptions only for high-priority service, transactional, or triggered onboarding messages.

### Segment Notes

- Check whether VIP, new customer, and at-risk segments behave differently before applying one universal cap.
- Customers in the 9+ band should be reviewed for campaign conflict and journey collisions.

### Test Plan

- Hold out a subset of customers currently receiving 6+ sends and cap them at 5 for 30 days.
- Compare conversion, unsubscribe, complaint, and downstream purchase behavior.

### Caveats

- Conversion data is missing, so the recommendation is based on engagement and unsubscribe risk.
- Total customer pressure across SMS, push, paid, and onsite is not included.
