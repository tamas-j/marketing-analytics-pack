---
name: mmm-readiness-checker
description: Use when checking whether marketing time-series data is suitable for media mix modelling, including outcome quality, spend/exposure fields, controls, history, variation, granularity, and risks.
---

# MMM Readiness Checker

This skill checks whether a dataset and business question are ready for media mix modelling. The pack's preferred MMM library is Google Meridian, but this readiness check is model-agnostic.

## Required Inputs

Ask only for what is missing:

- Business question or budget decision.
- Outcome metric and date grain.
- History length.
- Media channels and spend or exposure fields.
- Controls and external factors.
- Geography, product, or market splits.
- Known tracking, pricing, stock, or promotion issues.

## Readiness Verdicts

- `Ready`: enough history, variation, controls, and outcome quality to scope an MMM.
- `Usable with caveats`: possible, but limitations must be documented.
- `Needs fixes`: core structure exists but fields/history/controls need work.
- `Blocked`: not enough time series, variation, outcome quality, or channel data.

## Readiness Checks

| Area | What to check | Risk if weak |
|---|---|---|
| Outcome | stable business KPI, not platform-attributed | model explains tracking, not demand |
| Time grain | regular daily/weekly data | missing periods and noise |
| History | enough observations and seasonal coverage | unstable estimates |
| Media inputs | spend/exposure by channel | omitted channel bias |
| Variation | channels change over time | always-on channels hard to estimate |
| Controls | promo, price, holidays, stock, macro | media gets credit for non-media effects |
| Collinearity | channels move together | hard to separate effects |
| Geography | market variation if available | weak identification without variation |

## Output Template

```markdown
## MMM Readiness Check

### MMM Question
<budget or contribution question>

### Readiness Verdict
<Ready / Usable with caveats / Needs fixes / Blocked>

### Data Inventory
| Data area | Available? | Notes |
|---|---|---|
| <area> | <yes/no/partial> | <notes> |

### Gaps and Risks
- <risk>

### Required Fixes
- <fix>

### Recommended Modelling Scope
<scope>

### Next Step
<next action>
```

## Guardrails

- Do not overpromise channel-level precision.
- Do not ignore non-media controls.
- Do not recommend a heavy MMM runner before readiness is clear.
- Do not use MMM to answer creative, audience, or short-campaign questions better suited to experiments.
