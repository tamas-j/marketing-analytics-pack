---
name: segmentation-method-selector
description: Use when choosing a customer, audience, lead, or account segmentation method based on business goal, data availability, activation needs, and interpretability.
---

# Segmentation Method Selector

This skill selects a practical segmentation approach. It helps the user avoid over-complicated clustering when a simpler lifecycle, value, needs, or rules-based segmentation would be more useful — and it pushes back when a propensity model would do the job better than another round of clustering.

The most common mistake this skill prevents is **method-led segmentation**: a team learns about k-means or a tool offers RFM-out-of-the-box, builds segments, and then asks what to do with them. Segmentation should start from the activation decision and work backwards.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive the recommendation.

1. **Activation use.** Targeting, lifecycle messaging, sales prioritisation, product strategy, budget allocation, research, reporting. The activation determines the right method more than the data does.
2. **Business goal.** What decision improves if the segmentation is good?
3. **Unit to segment.** Customer, lead, account, visitor, subscriber, audience, product buyer, campaign recipient.
4. Available fields and event data.
5. Need for explainability (regulators, sales, exec stakeholders) vs automation.
6. Refresh cadence — daily, weekly, ad-hoc.
7. Channel where the segment will be activated (some methods produce segments that cannot be reached in the target channel).

## Method Guide

| Method | Best for | Required data | Strength | Watch-out |
|---|---|---|---|---|
| Lifecycle stage | journey orchestration and reporting | dates, status, activity | easy to explain and activate | can be too broad |
| Value tiers | prioritising profitable customers | revenue, margin, orders | directly commercial | may ignore future potential |
| RFM | ecommerce / customer value quick read | customer_id, order_date, order value | fast and interpretable | weak for non-purchase businesses |
| Behavioural rules | lifecycle and product usage | events, engagement, frequency | actionable | needs clean event definitions |
| Needs / persona translation | connecting research to data | persona traits plus measurable proxies | bridges qual and quant | proxies can be weak |
| Propensity model | prediction and ranking | labelled outcome, history, features | optimises targeting | less transparent, needs validation |
| Clustering (k-means / GMM / hierarchical) | exploratory patterns | rich numeric features | discovers hidden groups | can be hard to activate |
| Audience overlap | channel / list planning | audience membership flags | reduces duplication | needs consistent IDs |

## Decision Tree

Work through these in order. Stop at the first match.

1. **Is the activation channel-level reporting or list dedup?**
   → Recommend `/audience-overlap`. Don't build segments at all.
2. **Is the activation lifecycle messaging or journey orchestration?**
   → Recommend **lifecycle stage** plus **behavioural rules** for in-stage triggers. Avoid clustering.
3. **Is the activation "rank customers by who is most likely to do X (convert / churn / upgrade)"?**
   → Recommend a **propensity model**. Most teams reach for RFM here; propensity outperforms RFM whenever a labelled outcome exists.
4. **Is the activation "where should we spend marketing budget"?**
   → Recommend **value tiers** with **channel-of-acquisition cuts**. Pair with `/clv-scenario` for forward-looking value.
5. **Is the activation "translate this persona / ICP into something measurable"?**
   → Recommend `/persona-to-segment`. Do not let the persona owners hand-roll rules.
6. **Is the goal exploratory, with no fixed activation yet?**
   → Recommend **clustering** with strict guardrails: pre-defined activation criteria, interpretability check, size floor. Otherwise the segments become a deck nobody uses.
7. **Is this an ecommerce / transactional business with a quick-look customer review?**
   → Recommend **RFM**, route to `/rfm-segment` for execution.
8. **Default**: lifecycle stage + value tier, kept boring. Most teams overinvest in segmentation method.

## Method Choice by Activation

| Activation use | Default method | Often better than | Notes |
|---|---|---|---|
| Lifecycle journeys | Lifecycle stage + behavioural rules | RFM | RFM bins lag the actual lifecycle event |
| Win-back targeting | Propensity (churned + likely-to-return) | RFM "At risk" | If labels exist, propensity beats heuristic |
| Acquisition prioritisation (B2B) | Account scoring (rules or ML) | Clustering | Sales needs ranked accounts, not groups |
| Email frequency tiering | Engagement tier rules | RFM | Direct mapping from behaviour to frequency |
| Channel budget allocation | Value tiers × channel of acquisition | RFM | Decision is channel-level, not customer-level |
| Product strategy research | Clustering or needs-based | RFM | Looking for patterns, not actioning lists |
| Personalisation testing | Behavioural rules + experiment | Persona-based | Personas often unactivatable in channel |

## Worked Examples

### Example 1: DTC skincare, lifecycle marketing wants to launch a win-back programme

Activation: messaging to customers who haven't purchased in 120+ days. Data: 18 months of orders, customer_id, channel of acquisition, plan/subscription flag.

Recommendation: do **not** use the RFM "At risk / Hibernating" buckets as the audience. Build a **propensity-to-return** model labelled on "purchased within 30 days of being inactive 120+ days" using the last 6 months. Activate the top-decile by propensity into the win-back journey. Use RFM only as the reporting cut, not the targeting list.

Why this fits: propensity beats RFM whenever a labelled outcome exists, and a win-back outcome is easy to label. RFM groups are useful for reporting but they're a coarse target list.

### Example 2: B2B SaaS, marketing wants to prioritise account outreach

Activation: prioritise ~5,000 accounts for SDR outreach. Data: firmographics, intent signals, prior engagement, free-tier usage.

Recommendation: **account scoring** (rules-based first, ML when a labelled "became opportunity" history exists). Pair with `/persona-to-segment` to turn the ICP description into account-level rules. Do not cluster — sales needs a ranked list, not personas.

Why this fits: the activation is a ranked list, not groups. Clustering produces deck-friendly outputs that don't help an SDR pick the next call.

### Example 3: Subscription product, comms team wants "customer types" for the next quarterly

Activation: stakeholder narrative + research. Data: rich usage data, NPS, support contacts, tenure.

Recommendation: **clustering**, with explicit guardrails — at most 5 clusters, each ≥10% of base, interpretability check by domain experts before publishing. Pair with `/persona-to-segment` to translate the clusters into activatable rules afterwards if anyone wants to use them in channel.

Why this fits: the activation is research-grade, not operational. Clustering's exploratory strength matches the use case. Anti-patterns appear when clusters move to channel without being translated to rules.

## Activation Feasibility Check

Before recommending any method, confirm the segments can actually be **reached** in the activation channel. A method that produces segments that can't be activated is a method failure regardless of statistical elegance.

| Channel | Reachable segment shapes | Will not work |
|---|---|---|
| Email / SMS | Customer ID lists; behavioural rules; lifecycle | Anonymous traffic clusters |
| Paid social (custom audiences) | Hashed customer ID lists | Daily-refresh ML scores without API plumbing |
| Onsite personalisation | Logged-in user lists; session-level rules | Long-form personas with no proxy fields |
| Sales outreach | Account-level lists; ranked accounts | Customer-level clusters where no contact exists |
| In-product messaging | User ID lists; behavioural rules | Audiences defined on external systems only |

## Anti-Patterns

- **Method-led segmentation.** Building segments before defining the activation. Symptom: the deck lands and the team can't operationalise it.
- **Using RFM for a problem with a labelled outcome.** Propensity will beat RFM whenever you can label "did X happen." RFM is a great reporting cut; it's a weak targeting list once you have outcome data.
- **Clustering without an activation plan.** K-means produces "interesting" clusters that nobody can target in channel.
- **Persona → segment without proxies.** Marketing produces "the busy parent" segment, analytics has no field that proxies it, the segment is unactivatable.
- **Segmenting on data that won't be available at decision time.** Building rules on data joined retrospectively that isn't in the activation channel's data plane.
- **Too many segments.** More than ~7 segments in a single framework usually means lifecycle + persona + value got mashed together. Pick one dimension primary.
- **Stale segments.** Segmentation built once and never refreshed; customers move through lifecycle but stay flagged as "New" forever.
- **Using a model where rules would do.** A linear scoring rule a sales lead can explain often beats a propensity model nobody trusts.

## Output Template

```markdown
## Segmentation Method Recommendation

### Goal
<goal — what decision improves if the segmentation is good>

### Activation Use
<lifecycle / targeting / sales prioritisation / research / reporting>

### Recommended Method
<method>

### Why This Fits
<2-4 sentences anchored on activation and data>

### Required Data
- <field>

### Segment Output Shape
| Segment | Rule or definition | Use case | Reachable in channel? |
|---|---|---|---|
| <segment> | <definition> | <use> | <yes / no / partial> |

### Activation Feasibility
<can these segments actually be reached in the target channel?>

### Caveats and Guardrails
- <risk>

### Refresh Cadence
<how often the segmentation should be rebuilt>

### Next Step
<command or analysis — usually /persona-to-segment, /rfm-segment, /audience-overlap, or an analysis brief>
```

## Quality Rubric

- `Strong`: method matches the activation, segments are reachable in channel, refresh cadence is named, and either an alternative method is acknowledged or a clear reason given to dismiss it.
- `Usable`: method is sensible but activation feasibility or refresh cadence is left implicit.
- `Needs revision`: clustering recommended without an activation plan; persona segments with no proxy fields; RFM recommended when a labelled outcome exists and propensity would be stronger.

## Guardrails

- Do not recommend a method that cannot be activated or explained to the intended user.
- Do not build segments from fields that would not be available at targeting time.
- Do not compare segment performance without considering size and eligibility.
- Do not call a persona a segment until it has measurable rules or proxies.
- When the activation is "rank by likelihood of X" and labels exist, recommend propensity over RFM.
- When the activation is lifecycle messaging, recommend lifecycle stage + rules over clustering.
- When the activation is exploratory, set guardrails for cluster count and size before agreeing to cluster.
