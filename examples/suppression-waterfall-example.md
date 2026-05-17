# Suppression Waterfall Example

## Prompt

```text
/suppression-waterfall We start with 250,000 customers for an email campaign. Remove 30,000 ineligible product owners, 45,000 without email consent, 12,000 invalid emails, 18,000 recent purchasers, 20,000 over frequency cap, and 5,000 support exclusions.
```

## Example Output

## Suppression Waterfall

### Audience Summary

Starting audience is 250,000 customers for an email campaign. The goal is to explain how eligibility, consent, contactability, business, and fatigue rules reduce the final reachable audience.

### Waterfall Table

| Step | Rule | Removed | Remaining | Removal rate | Notes |
|---|---|---:|---:|---:|---|
| 0 | Starting audience | - | 250,000 | - | customer pool |
| 1 | Ineligible product owners | 30,000 | 220,000 | 12.0% | product eligibility |
| 2 | No email consent | 45,000 | 175,000 | 20.5% | compliance exclusion |
| 3 | Invalid email | 12,000 | 163,000 | 6.9% | contactability issue |
| 4 | Recent purchasers | 18,000 | 145,000 | 11.0% | journey control |
| 5 | Over frequency cap | 20,000 | 125,000 | 13.8% | fatigue control |
| 6 | Support exclusions | 5,000 | 120,000 | 4.0% | customer experience |

### Biggest Loss Points

- Consent removes the largest group and should be tracked separately from optimisation rules.
- Frequency cap removes 20,000 customers, which may indicate campaign pressure across the lifecycle calendar.

### Data Quality Checks

- Confirm counts are sequential, not independent.
- Check email consent freshness and source.
- Check whether invalid emails can be repaired.

### Recommended Fixes or Decisions

- Do not bypass consent exclusions.
- Review email capture and preference-centre flows.
- Inspect which campaign types are causing frequency cap pressure.

### Visual Recommendation

Use a waterfall chart for stakeholder reporting and a ranked removal bar chart for operational fixes.
