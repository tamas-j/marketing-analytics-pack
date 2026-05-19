---
name: attribution-model-selector
description: Use when choosing or critiquing marketing attribution approaches, including rules-based attribution, data-driven attribution, MMM, incrementality tests, and blended measurement frameworks.
---

# Attribution Model Selector

This skill helps users choose an attribution approach that fits the decision and the data. It is deliberately careful about the difference between attribution (credit-assignment over observed paths) and incrementality (causal impact of marketing).

The single most common mistake this skill exists to prevent is using path-based attribution to make budget reallocation decisions. Path-based attribution can be useful for reporting and platform optimisation, but it cannot answer "what would have happened without this marketing?" — and that is usually the question the user actually has.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive the recommendation, the rest refine it.

1. **Decision to support.** Reporting, platform optimisation, budget reallocation, incremental ROI, channel investment case, or executive narrative.
2. **Tracking and ID coverage.** Logged-in vs anonymous mix, cross-device, consent loss, walled gardens, offline conversions.
3. **Channel mix and journey length.** Number of touchpoints, online + offline, paid + owned + earned, buying-cycle length.
4. Conversion event and lag.
5. Operational constraints: ability to run holdouts, geo splits, suppression.
6. History available (relevant for MMM).
7. Stakeholder appetite for "we cannot fully prove this" framing.

If the user gives only the decision, infer the rest with stated assumptions and route to a readiness check (`/mmm-readiness`, `/check-data`) before recommending a heavy approach.

## Method Guide

| Approach | Best for | Data needed | Main limitation | Causal? |
|---|---|---|---|---|
| Last touch | simple reporting and ops | conversion path or source | overcredits lower funnel | No |
| First touch | acquisition source reporting | first touch ID | ignores nurture and conversion | No |
| Position-based | simple journey credit | ordered touchpoints | arbitrary weights | No |
| Rules-based custom | stakeholder-aligned reporting | touchpoint data | not causal | No |
| Data-driven attribution (DDA) | platform optimisation | rich path data | black box, biased by tracking gaps | No |
| Incrementality testing | causal campaign impact | holdout / geo / control design | operational complexity, slow | Yes |
| MMM | budget allocation across channels | time-series spend / outcome data | needs history and assumptions | Causal at channel level |
| Blended framework | mature measurement | multiple sources | governance needed | Best available |

## Decision Tree

Work through these in order. Stop at the first node where the answer is "yes."

1. **Is the decision a budget reallocation across channels worth more than the cost of being wrong?**
   → Recommend **MMM** as the primary tool. Use attribution only as an optimisation layer underneath. Run incrementality on the largest planned shifts to triangulate.
2. **Is the decision platform-level bidding, audience, or creative optimisation?**
   → Recommend **DDA** (or the platform's native attribution) for optimisation, with a quarterly **incrementality test** as the calibration layer.
3. **Is the decision "did this specific campaign work?"**
   → Recommend **incrementality** (geo, user holdout, or PSA). Attribution is descriptive only here — see `/campaign-post-mortem` for the narrative readout.
4. **Is the decision reporting / dashboards / stakeholder communication?**
   → Recommend a **rules-based** model (position-based for journey nuance, last-non-direct for simplicity). Be explicit it is reporting, not causal.
5. **Is tracking and ID coverage so fragmented that path-based methods can't credibly run?**
   → Recommend **MMM + incrementality** as the only credible options; attribution becomes commentary.
6. **Is the team mature enough to triangulate three sources?**
   → Recommend a **blended framework** — MMM for channel-level budget, incrementality for calibration and large changes, DDA / rules-based for optimisation and reporting. See the **Blended Framework** section below.

## Blended Framework

A blended approach uses three layers for three different questions. It is not "average the three numbers."

| Layer | Question it answers | Cadence | Decision authority |
|---|---|---|---|
| MMM | What is each channel worth at the budget level? | Quarterly / semi-annual | Channel-level budget allocation |
| Incrementality | Is the MMM right where it matters most? | On the biggest changes and 1–2 always-on channels per quarter | Calibrates MMM, validates large shifts |
| Attribution (DDA / rules-based) | How are we performing inside each channel day-to-day? | Daily / weekly | In-channel optimisation, reporting |

The blended framework's governance matters more than its math. Decide in advance: when MMM and DDA disagree on channel ROI by more than X%, MMM wins for budget; DDA wins for in-channel optimisation. Document the rule before the disagreement, not after.

## Worked Examples

### Example 1: DTC ecommerce, CMO wants to reallocate paid budget

Decision: shift $2M annually between paid search, paid social, affiliate, and connected TV. Data: 18 months of weekly channel spend, conversions, promo flags. Strong in-platform tracking on search and social, weak on connected TV and affiliate, consent loss ~30%.

Recommendation: **MMM** as primary (decision tree node 1). Run incrementality lifts on the proposed connected-TV expansion before scaling. Keep DDA for in-platform bidding. Anchor stakeholder reporting on weekly DDA, anchor the annual reallocation on MMM.

Why this fits: the decision size justifies MMM cost; history and variation are present; ID-level path-based methods would systematically undercredit connected TV.

### Example 2: B2B SaaS marketing, attributing pipeline

Decision: how much pipeline does each marketing program deserve credit for? Data: HubSpot / Salesforce with first-touch + last-touch + UTM tags; 8-month sales cycle; ~3,000 closed-won opportunities per year.

Recommendation: **W-shaped or position-based** rules-based model as the primary reporting view. Layer in a quarterly **incrementality test** on one major program (e.g., webinar pause in a matched-region holdout) to calibrate. MMM is not yet credible at this volume — see `/mmm-readiness`.

Why this fits: decision is reporting + program prioritisation, not budget reallocation across paid channels; conversion volume is too low and journey too long for MMM; DDA black-box models are noisy at this sample size.

### Example 3: Lifecycle marketer asking "does email get credit?"

Decision: a lifecycle team wants to defend email's contribution to revenue against a paid-team argument that email is "free" and uncredited.

Recommendation: do **not** answer with attribution. Run a **user-level holdout** on the next major email campaign (`/incrementality-test-designer`) and report incremental revenue per email recipient. Use that as the credit number. Attribution is the wrong tool here because email overlaps with every other channel and any attribution model can be argued either way.

Why this fits: the underlying question is causal, the answer needs to be defensible in a budget conversation, and holdouts on owned channels are operationally cheap.

## Anti-Patterns

These are the most common misroutes this skill exists to prevent.

- **Using MTA / DDA for budget reallocation.** Path-based attribution is optimisation-grade, not budget-grade. Symptom: stakeholders argue about which model to use. Fix: route to `/mmm-readiness`.
- **Treating DDA as proof of channel impact.** DDA optimises against tracked conversions; it cannot see channels it doesn't track and over-credits channels with rich path data. Symptom: paid social ROI looks "obviously better" than connected TV.
- **Using MMM for short or single-campaign questions.** MMM has poor signal below quarterly cadence. Symptom: someone asks "did the May campaign work?" and the team runs MMM. Fix: incrementality test.
- **Last-click for budget decisions.** Includes its sibling "last-non-direct." Defensible as a reporting view, indefensible as the basis for reallocation.
- **Comparing channel ROI across platforms using their own attribution.** Meta, Google, and TikTok each claim the same conversion. Symptom: paid-channel ROI sum exceeds total revenue.
- **Promising "attribution will be solved" by adopting a new tool.** No vendor solves attribution — they pick a model. Symptom: RFP language like "true multi-touch."
- **Skipping the incrementality calibration layer in a blended framework.** Without calibration, MMM and DDA disagree forever and the team picks whichever supports the meeting agenda.

## Output Template

```markdown
## Attribution Approach Recommendation

### Attribution Question
<decision the user actually needs to make>

### Recommended Approach
<approach, with explicit "primary" and "supporting" if blended>

### Why This Fits
<rationale grounded in decision + data + constraints, 2-4 sentences>

### Data Requirements
- <field or source>

### Limitations
- <limitation tied to the recommendation>

### If You Need Incrementality
<experiment / MMM recommendation; route to /incrementality-test-designer or /mmm-readiness>

### Governance Note
<if blended: when models disagree, which one wins which decision>

### Next Step
<practical next action — usually a readiness check, a test design, or a reporting spec>
```

## Quality Rubric

- `Strong`: the recommendation names a primary approach matched to the decision size, names supporting methods where triangulation matters, sets out limitations honestly, and ends with a concrete next command.
- `Usable`: a single approach is recommended with clear rationale, but supporting methods or governance are absent.
- `Needs revision`: the recommendation hedges across all eight options, or recommends MTA/DDA for budget allocation, or proposes MMM without checking readiness.

## Guardrails

- Attribution assigns credit; it does not prove what would have happened without marketing.
- Platform attribution can be useful for optimisation but may overstate business impact.
- Do not recommend user-level attribution if IDs are fragmented or consent limits tracking.
- Do not use attribution alone for major budget shifts when experiments or MMM are feasible.
- Do not present a blended framework without naming the governance rule for disagreements.
- When recommending MMM, always route to `/mmm-readiness` before scoping the runner.
- When recommending incrementality, always route to `/incrementality-test-designer`.
