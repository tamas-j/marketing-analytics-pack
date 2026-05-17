---
description: Audit marketing campaign, channel, UTM, naming, or taxonomy fields for consistency, coverage, and reporting reliability.
argument-hint: "<taxonomy fields, naming rules, sample values, platforms, reporting goal>"
---

# Marketing Taxonomy Auditor

Use this command when the user needs to review campaign naming, UTMs, channel taxonomy, lifecycle tags, or reporting dimensions.

Use skill: "marketing-taxonomy-auditor"
Use skill: "data-readiness-checker"

## Workflow

1. Restate the taxonomy and reporting goal.
2. Ask for naming rules, sample values, platforms, and required reporting cuts.
3. Audit consistency:
   - required fields present
   - naming pattern followed
   - channel/source/medium alignment
   - campaign objective or funnel stage consistency
   - date, market, product, audience, and creative conventions
   - unknown, blank, or miscellaneous values
4. Flag reporting risks and suggested standardisation.
5. Recommend a cleaned taxonomy schema and QA checks.

## Output Format

Return:

1. Taxonomy summary
2. Audit findings
3. Reporting risks
4. Recommended naming schema
5. Cleanup rules
6. QA checks

## Guardrails

- Do not invent naming rules that conflict with the user's existing platform constraints.
- Separate historical cleanup from future governance.
- Keep taxonomy fields useful for reporting, not decorative.
- Flag values that will break joins or attribution.
