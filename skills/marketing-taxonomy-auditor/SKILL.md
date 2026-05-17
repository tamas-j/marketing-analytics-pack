---
name: marketing-taxonomy-auditor
description: Use when auditing campaign naming, UTM, channel, lifecycle, audience, or marketing taxonomy fields for consistency, reporting reliability, cleanup, and governance.
---

# Marketing Taxonomy Auditor

This skill audits marketing naming and taxonomy. It helps users find inconsistent values, missing fields, weak conventions, and reporting risks before analysis or dashboarding.

## Required Inputs

Ask only for what is missing:

- Fields being audited, such as source, medium, campaign, content, term, channel, objective, market, product, audience, or lifecycle stage.
- Current naming rules, if any.
- Sample values or a file.
- Platforms involved.
- Reporting dimensions the taxonomy must support.

## Audit Dimensions

- Completeness: blanks, nulls, unknowns, missing required parts.
- Consistency: spelling, case, delimiters, abbreviations, ordering.
- Parseability: can values be split reliably into reporting fields?
- Channel alignment: source, medium, channel, and platform agree.
- Business usefulness: fields support objective, audience, product, market, creative, and lifecycle reporting.
- Governance: rules are clear enough for future campaign creation.

## Output Template

```markdown
## Marketing Taxonomy Audit

### Taxonomy Summary
<fields and reporting goal>

### Audit Findings
| Issue | Example | Reporting risk | Fix |
|---|---|---|---|
| <issue> | <value> | <risk> | <fix> |

### Recommended Naming Schema
<schema>

### Cleanup Rules
- <rule>

### QA Checks
- <check>

### Governance Notes
- <note>
```

## Common Checks

- `utm_source` and platform names are normalised.
- `utm_medium` maps cleanly to channel grouping.
- Campaign name includes objective, audience, market, product, or date only if those are needed.
- Delimiters are consistent.
- Paid, organic, lifecycle, affiliate, and referral traffic are not mixed.
- Test campaigns and internal traffic are identifiable.

## Guardrails

- Do not over-engineer taxonomy with fields no one reports on.
- Do not erase historical meaning during cleanup.
- Do not merge channels unless reporting owners agree.
- Do not assume UTM values are trustworthy without source/platform checks.
