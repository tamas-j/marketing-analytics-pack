# RFM Segment Example

## Prompt

```text
/rfm-segment We have ecommerce orders with customer_id, order_id, order_date, order_status, net_revenue, discount_code, and refund_amount. We want lifecycle segments for email.
```

## Example Output

## RFM Segmentation

### Readiness Verdict

Ready with caveats. The core RFM fields are present, but cancelled, test, duplicate, and fully refunded orders must be excluded before scoring.

### RFM Definitions

| Component | Definition | Field needed |
|---|---|---|
| Recency | days since most recent completed non-refunded order | `order_date`, `order_status`, `refund_amount` |
| Frequency | count of completed non-refunded orders in the last 12 months | `order_id`, `order_status`, `order_date` |
| Monetary | total net revenue from completed non-refunded orders in the last 12 months | `net_revenue`, `refund_amount` |

### Scoring Approach

Use quintiles if the customer base is large enough. Score recency so the most recent customers receive the highest score. Score frequency and monetary so higher values receive higher scores.

### Segment Map

| Segment | Rule | Meaning | Recommended action |
|---|---|---|---|
| Champions | R 4-5, F 4-5, M 4-5 | best current customers | loyalty, referrals, early access |
| New customers | R 5, F 1-2 | recent first-time buyers | onboarding and second purchase |
| Loyal | R 4-5, F 4-5, M 1-3 | frequent but not highest value | cross-sell and basket growth |
| Big spenders | M 5, F 1-3 | high-value but less frequent | premium product journeys |
| At risk | R 1-2, F 4-5 or M 4-5 | valuable customers going quiet | winback and save offers |
| Hibernating | R 1-2, F 1-2, M 1-2 | low recent and historical value | low-cost reactivation or suppression |

### QA Checks

- Confirm each `order_id` belongs to one `customer_id`.
- Exclude cancelled and fully refunded orders.
- Use a fixed analysis date for recency.
- Check segment sizes before activation.
- Compare email eligibility by segment.

### Caveats

- RFM is descriptive, not predictive.
- Discount-heavy customers may look valuable on revenue while being weaker on margin.
- Customers acquired recently have not had the same chance to build frequency.

---

## Execution Mode Example (v0.2.0)

### Prompt

```text
/rfm-segment Run RFM on examples/data/orders.csv. customer_id, order_date, order_value columns. Use quantile-based named segments.
```

### Command

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

### Real Output (smoke-tested 2026-05-18)

#### `summary.md`

```markdown
# RFM segmentation summary

- Input: `examples/data/orders.csv`
- Customers: 116
- Analysis date (recency anchor): 2025-12-31
- Method: `quantile`

## Segment profiles

| Segment       | Customers | Avg recency (days) | Avg frequency | Avg monetary | Total monetary |
|---------------|----------:|-------------------:|--------------:|-------------:|---------------:|
| Champions     |        17 |               21.9 |           6.1 |          803 |         13,658 |
| Big spenders  |        17 |              100.0 |           4.4 |          614 |         10,446 |
| New customers |        20 |               24.9 |           2.4 |          304 |          6,085 |
| Hibernating   |        25 |              195.8 |           1.8 |          221 |          5,516 |
| Loyal         |         7 |               60.4 |           5.9 |          679 |          4,755 |
| At risk       |        11 |              158.2 |           3.2 |          419 |          4,606 |
| Promising     |        11 |               54.6 |           3.4 |          404 |          4,442 |
| Other         |         8 |               66.8 |           1.9 |          206 |          1,645 |

Top segment by total revenue: **Champions** (17 customers, 13,658 total).
```

#### Files written

| File | Contents |
|---|---|
| `rfm_scores.csv` | 116 rows: customer_id, R, F, M, r_score, f_score, m_score, segment |
| `segment_profiles.csv` | 8 rows: segment, customers, R/F/M means, total monetary |
| `segment_sizes.png` | Horizontal bar chart of customers per segment |
| `rf_scatter.png` | Recency vs Frequency scatter, segments coloured, bubble size = monetary |
| `summary.md` | The narrative above |

### How to read this

- 17 Champions drive 14k of the 51k total revenue — 33% of revenue from 15% of customers. Standard concentration; flag for VIP / referral programs.
- Hibernating is the largest segment by count (25), but smallest in unit value. Cheap reactivation or suppression rather than expensive winback.
- "At risk" + "Big spenders" combined are ~25% of customers and ~30% of revenue. These deserve targeted retention messaging before they hibernate.
- For k-means clusters (`--method kmeans --n-clusters 4`), labels come out as `Cluster 1`, `Cluster 2`, etc., ranked by total monetary descending. Translate to business names before activation.
