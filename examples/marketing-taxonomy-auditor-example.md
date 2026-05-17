# Marketing Taxonomy Auditor Example

## Prompt

```text
/marketing-taxonomy-auditor Audit these UTM values for paid social reporting: facebook / paid_social / spring_sale, fb / social-paid / SpringSale, meta / paid-social / spring-sale-uk, instagram / paid_social / spring_sale_uk.
```

## Example Output

## Marketing Taxonomy Audit

### Taxonomy Summary

The taxonomy should support paid social reporting by platform, channel, campaign, and market. The sample values show inconsistent platform names, medium values, delimiters, and market encoding.

### Audit Findings

| Issue | Example | Reporting risk | Fix |
|---|---|---|---|
| Source aliases | `facebook`, `fb`, `meta`, `instagram` | paid social platform reporting fragments | define approved source values |
| Medium inconsistency | `paid_social`, `social-paid`, `paid-social` | channel grouping breaks | standardise to `paid_social` |
| Campaign delimiter inconsistency | `spring_sale`, `SpringSale`, `spring-sale-uk` | parsing and grouping fail | use lowercase snake case |
| Market sometimes embedded | `spring-sale-uk`, `spring_sale_uk` | UK market may be missed | add explicit `market` field or suffix rule |

### Recommended Naming Schema

`source / medium / campaign_market`

Example:

`meta / paid_social / spring_sale_uk`

### Cleanup Rules

- Map `facebook`, `fb`, and `meta` to a chosen reporting source.
- Map all paid social medium variants to `paid_social`.
- Convert campaign names to lowercase snake case.
- Extract market suffix where present.

### QA Checks

- No blank source, medium, or campaign values.
- Medium maps to a known channel group.
- Campaign values are parseable with the agreed delimiter.

### Governance Notes

- Future campaign briefs should include approved source, medium, campaign, market, objective, and owner fields before launch.
