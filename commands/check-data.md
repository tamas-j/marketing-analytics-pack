---
description: Check whether a CSV, Excel file, pasted table, or described dataset is ready for a marketing analytics workflow.
argument-hint: "<file path, pasted columns, dataset summary, and intended analysis>"
---

# Check Data

Use this command before analysis when the user has a dataset, table description, or pasted columns and wants to know whether it can support a marketing analytics task.

Use skill: "data-readiness-checker"

## Workflow

1. Identify the intended analysis or decision.
2. Identify the dataset grain: one row per customer, order, session, campaign, email send, day, product, or another unit.
3. Check required fields for the intended workflow.
4. Check basic quality risks:
   - missing key identifiers
   - missing dates
   - duplicate rows at the stated grain
   - inconsistent categories
   - unclear metric definitions
   - insufficient time coverage
   - leakage risks for prediction or forecasting
5. If the user provided a CSV path and the environment can read files, run:
   `python skills/data-readiness-checker/scripts/profile_data.py <file>`.
   Add `--grain-key <column>` for the expected grain when the key is known.
6. Classify readiness as `Ready`, `Usable with caveats`, `Needs fixes`, or `Blocked`.
7. Recommend the next command or analysis route.

## Output Format

Return:

1. `Readiness verdict`
2. `Dataset grain`
3. `What looks usable`
4. `Risks or missing fields`
5. `Fixes to make before analysis`
6. `Best next command`
7. `Can proceed now?`

## Guardrails

- Do not over-audit the file. Focus on whether it can support the user's intended analysis.
- Be specific about missing columns and why they matter.
- If the user only pasted column names, clearly label the check as a schema-level review.
- Do not require perfect data for exploratory work.
- Flag when a metric cannot be interpreted because its definition is unclear.
- For files, prefer a quick profile before making claims about data quality.
