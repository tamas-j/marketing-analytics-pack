# Audience Overlap Example

## Prompt

```text
/audience-overlap Compare our VIP customers list, lapsed customers list, and paid social retargeting audience. We can match by hashed email. VIP size is 12,000, lapsed is 35,000, retargeting is 48,000. VIP x retargeting overlap is 4,800; lapsed x retargeting is 18,000; VIP x lapsed is 1,200.
```

## Example Output

## Audience Overlap Analysis

### Audience Summary

The goal is to understand whether retargeting overlaps with VIP and lapsed customer audiences, using hashed email as the shared ID.

### Overlap Table

| Pair | Audience A size | Audience B size | Overlap | % of A | % of B | Readout |
|---|---:|---:|---:|---:|---:|---|
| VIP x retargeting | 12,000 | 48,000 | 4,800 | 40% | 10% | meaningful VIP exposure in retargeting |
| Lapsed x retargeting | 35,000 | 48,000 | 18,000 | 51% | 38% | retargeting is heavily reaching lapsed customers |
| VIP x lapsed | 12,000 | 35,000 | 1,200 | 10% | 3% | small but important group to define carefully |

### Interpretation

- Retargeting appears to contain a large lapsed customer component.
- VIP overlap is smaller as a share of retargeting, but high as a share of VIPs.
- VIP x lapsed needs a clear business rule: former VIPs may deserve a different winback treatment.

### Recommended Action

- Split retargeting into current VIP, lapsed, former VIP/lapsed, and prospect groups.
- Suppress current VIPs from generic winback creative.
- Give former VIP/lapsed customers a higher-touch reactivation message.

### Measurement Caveats

- Hashed email match rate may understate overlap if some audiences use different identifiers.
- Consent and platform eligibility must be checked before activation.

### Visual Recommendation

Use an overlap matrix for the three audiences; use a horizontal bar chart if presenting top duplicate-reach opportunities.
