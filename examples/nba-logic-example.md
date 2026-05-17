# NBA Logic Example

## Prompt

```text
/nba-logic We need next-best-action logic for subscription coffee customers. Actions are onboarding, skip-prevention, upgrade, winback, referral, and pause support. We have tenure, plan type, skipped deliveries, email engagement, churn risk, payment failure, and referral status.
```

## Example Output

## Next-Best-Action Logic

### Objective

Choose the most relevant lifecycle action for each subscription customer while protecting retention, margin, and customer experience.

### Action Catalogue

| Action | Intended customer | Success metric | Guardrail |
|---|---|---|---|
| Onboarding | new customers in first 30 days | activation, second shipment | unsubscribe rate |
| Skip prevention | customers with recent skipped delivery | retained shipments | complaint rate |
| Upgrade | engaged customers on low-tier plans | upgrade rate | churn after upgrade |
| Winback | lapsed or churn-risk customers | saved subscriptions | margin after incentive |
| Referral | loyal active customers | referral conversions | low-quality referrals |
| Pause support | customers showing friction | reduced cancellations | support burden |

### Eligibility Rules

- Customer must have marketing consent for promotional actions.
- Payment failure customers receive billing support before promotional actions.
- Customers with open support issues are excluded from upgrade and referral actions.
- Churned customers are eligible only for winback or pause/support flows.

### Prioritisation Logic

1. Payment failure or billing issue: billing support.
2. Open support issue or recent complaint: pause support.
3. New customer under 30 days: onboarding.
4. Recent skipped delivery plus churn risk: skip prevention.
5. High engagement and loyal tenure: referral.
6. High engagement on low-tier plan: upgrade.
7. Lapsed or high churn risk: winback.

### Suppression and Guardrails

- Suppress promotional actions after recent cancellation.
- Limit to one lifecycle action per customer per week.
- Do not show upgrade offers to customers with unresolved service issues.
- Track margin after incentive for winback.

### Fallback Logic

- If no action qualifies, send no marketing action or place customer in a low-pressure nurture pool.
- If data is missing, default to lower-risk education content rather than promotion.

### Measurement Plan

- Use a holdout for each high-volume action.
- Track action-specific conversion, churn, unsubscribe, complaint, and margin.
