# MMM Readiness Example

## Prompt

```text
/mmm-readiness We want to understand channel contribution for ecommerce revenue. We have 30 months of weekly revenue, spend by paid search, paid social, TV, affiliates, email sends, promotions, price index, stockout flag, and holidays.
```

## Example Output

## MMM Readiness Check

### MMM Question

Estimate marketing channel contribution and inform budget allocation for ecommerce revenue.

### Readiness Verdict

Ready with caveats. The dataset has enough weekly history and key channel/control fields, but channel collinearity, email measurement, and stockout handling need review before modelling.

### Data Inventory

| Data area | Available? | Notes |
|---|---|---|
| Outcome | yes | weekly ecommerce revenue |
| Media spend | yes | paid search, paid social, TV, affiliates |
| Owned media | partial | email sends are available, but email is not spend |
| Controls | yes | promotions, price, holidays, stockout |
| History | yes | 30 months weekly |
| Variation | unknown | check whether channels vary independently |

### Gaps and Risks

- Paid search and paid social may move together during campaigns.
- Email sends may reflect demand or lifecycle triggers rather than paid media pressure.
- Stockout weeks may distort revenue and channel contribution.

### Required Fixes

- Check missing weeks and outliers.
- Create a clean weekly modelling table.
- Inspect channel correlation and spend variation.
- Decide whether email is a control, channel, or separate lifecycle input.

### Recommended Modelling Scope

Start with weekly national-level MMM using revenue as outcome, paid channel spend as media inputs, and promotion, price, holiday, and stockout controls.

### Next Step

Prepare a Google Meridian runner spec with `/mmm-runner`.
