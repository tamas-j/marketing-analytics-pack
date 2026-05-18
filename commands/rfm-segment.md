---
description: Compute or design RFM segmentation (spec mode for design, execution mode via scripts/run_rfm.py for real per-customer scores + segments).
argument-hint: "<customer_id, order date, order value fields, scoring approach, activation goal>"
---

# RFM Segment

Use this command for RFM segmentation on customer transactions. It has two modes:

- **Spec mode** (default): design the segmentation — RFM definitions, scoring approach, segment map, activation guidance.
- **Execution mode**: run `skills/rfm-segment-generator/scripts/run_rfm.py` against a transactions CSV and emit per-customer R/F/M, named segments, and styled charts.

Default to spec mode unless the user has a CSV ready and asks for outputs.

Use skill: "rfm-segment-generator"
Use skill: "data-readiness-checker"

## Spec Workflow

1. Confirm the business goal and customer unit.
2. Check required fields:
   - customer ID
   - order or transaction date
   - order or transaction value
   - order status or eligibility filters
3. Define recency, frequency, and monetary calculations.
4. Recommend scoring approach: quintiles (interpretable), tertiles (small data), thresholds (known lifecycle), or k-means (data-driven).
5. Map RFM scores into named segments.
6. Explain activation use cases and guardrails.

### Spec Output Format

Return:

1. RFM readiness verdict
2. RFM definitions
3. Scoring approach
4. Segment map
5. Activation recommendations
6. Caveats and QA checks

## Execution Workflow

1. Confirm the CSV path, customer / date / value columns with the user.
2. Confirm any status filter (e.g. only `completed` and `fulfilled`) and the recency anchor date.
3. Confirm method: `quantile` (default, named segments) or `kmeans` (clusters).
4. Run `python skills/rfm-segment-generator/scripts/run_rfm.py` with the chosen flags. Pass `--auto-install` if scikit-learn isn't installed yet.
5. Read `summary.md` and present the top segments by total revenue.
6. Show `segment_sizes.png` and `rf_scatter.png` inline if the surface supports it.

### Example

```bash
python skills/rfm-segment-generator/scripts/run_rfm.py \
  --input examples/data/orders.csv \
  --customer-col customer_id \
  --date-col order_date \
  --value-col order_value \
  --method quantile \
  --output-dir examples/rfm-segment/output \
  --style default
```

## Guardrails

- In spec mode: do not pretend the segmentation has run unless actual outputs are provided.
- In execution mode: always quote segment sizes alongside revenue share — a tiny "Champions" segment driving 40% of revenue is a very different story from a large one.
- Do not use RFM if purchases are one-off or frequency has little meaning.
- Do not compare customers with incomplete observation windows without caveats.
- Exclude cancelled, test, duplicate, and fully refunded transactions where relevant.
- Use monetary value only after clarifying gross revenue, net revenue, or margin.
- Do not treat RFM as a predictive model.
