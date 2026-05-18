---
name: rfm-segment-generator
description: Use when designing, executing, or interpreting RFM segmentation from customer transactions — scoring rules, named segments, activation guidance, and styled outputs.
---

# RFM Segment Generator

This skill has two modes:

- **Spec mode** (always available): walk through RFM definitions, scoring approach, segment map, QA checks, and activation guidance, without running anything.
- **Execution mode** (advanced runner, from v0.2.0): run `scripts/run_rfm.py` to actually compute R/F/M from a transactions CSV, assign segments (quantile or k-means), and emit styled charts.

Choose the mode based on whether the user is *designing* the segmentation or *running* it. Default to spec mode unless the user has a transactions CSV ready and asks for outputs.

## Required Inputs

Ask only for what is missing:

- Customer identifier column.
- Transaction or order date column.
- Transaction or order value column.
- Order status column + valid-statuses filter (optional, to drop cancelled/refunded).
- Analysis date — the recency anchor (defaults to the latest date in the file).
- Business goal and activation channel.
- Segmentation method: quantile rules (default, interpretable) or k-means (data-driven).

## Execution Mode Availability

| Surface | Spec mode | Execution mode |
|---|---|---|
| Claude Code | ✅ | ✅ — Claude can run the script via Bash |
| Cowork | ✅ | ✅ — Claude can run the script via Bash |
| Claude.ai web chat | ✅ | ❌ — no shell access; fall back to spec mode |

If you're not sure whether the active surface supports Bash, ask the user before assuming execution mode. The spec-mode output is always a valid fallback.

## RFM Definitions

- `Recency`: days since most recent eligible purchase. Lower is better.
- `Frequency`: count of eligible purchases in the observation window. Higher is better.
- `Monetary`: total value in the observation window. Higher is usually better.

## Scoring Options

| Approach | Best for | Notes |
|---|---|---|
| Quintiles 1-5 | medium/large customer bases | common, easy to explain |
| Tertiles 1-3 | smaller datasets | less granular, more stable |
| Business thresholds | known lifecycle windows | easiest to activate |
| K-means clusters | exploratory / data-driven | needs scikit-learn; less interpretable labels |

## Segment Map (used by quantile method)

| Segment | Typical rule | Use case |
|---|---|---|
| Champions | high R, high F, high M | loyalty, referrals, early access |
| Loyal | high R, high F | retention and cross-sell |
| Big spenders | high M, medium F | premium offers and care |
| New customers | high R, low F | onboarding and second purchase |
| Promising | medium R, F, M | gentle nurture |
| At risk | low R, historically high F/M | winback and save journeys |
| Hibernating | low R, low F/M | low-cost reactivation or suppression |

## Spec Mode Output Template

```markdown
## RFM Segmentation

### Readiness Verdict
<Ready / Usable with caveats / Needs fixes / Blocked>

### RFM Definitions
| Component | Definition | Field needed |
|---|---|---|
| Recency | <definition> | <field> |
| Frequency | <definition> | <field> |
| Monetary | <definition> | <field> |

### Scoring Approach
<quintiles/tertiles/thresholds/kmeans>

### Segment Map
| Segment | Rule | Meaning | Recommended action |
|---|---|---|---|
| <segment> | <rule> | <meaning> | <action> |

### QA Checks
- <check>

### Caveats
- <caveat>
```

## Execution Mode

Run from the repo root:

```bash
python skills/rfm-segment-generator/scripts/run_rfm.py \
  --input <csv path> \
  --customer-col <customer id column> \
  --date-col <order date column> \
  --value-col <order value column> \
  [--status-col <status column> --valid-statuses completed,fulfilled] \
  [--analysis-date YYYY-MM-DD] \
  [--method quantile|kmeans] \
  [--n-clusters 5] \
  [--output-dir <path>] \
  [--style default|executive|custom] \
  [--auto-install]
```

Dependencies are declared in `scripts/requirements.txt` (`pandas`, `matplotlib`, `pyyaml`, `scikit-learn`). Lighter than the Prophet / Meridian runners — installs in seconds, even without a venv.

### Outputs

| File | Contents |
|---|---|
| `rfm_scores.csv` | One row per customer with R, F, M, scores, and segment |
| `segment_profiles.csv` | Per-segment customer count, R/F/M means, total monetary |
| `segment_sizes.png` | Horizontal bar chart of customers per segment, styled via `lib/visualize.py` |
| `rf_scatter.png` | Recency vs Frequency scatter, coloured by segment, bubble size encodes Monetary |
| `summary.md` | Short human-readable narrative |

## Guardrails

- RFM works best where repeat purchase behaviour is meaningful — flag one-off purchase data as a poor fit.
- Use a fixed analysis date (`--analysis-date`) when comparing runs across time.
- Avoid monetary fields that include tax, shipping, refunds, or discounts unless intentionally included.
- Do not over-message at-risk customers without fatigue and margin guardrails.
- Treat RFM as descriptive segmentation, not proof of future behaviour.
- K-means labels (`Cluster 1`, `Cluster 2`, ...) are ranked by total monetary descending — translate them to business-meaningful names before activation.
