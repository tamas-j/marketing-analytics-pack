---
name: measurement-triangulation
description: Use when blending MMM, incrementality tests, and attribution into a single measurement framework, including triangulation cadence, reconciliation of disagreements, governance of which model wins which decision, and stakeholder communication.
---

# Measurement Triangulation

This skill designs and runs a **blended measurement framework** — the practical answer to "which of MTA, MMM, and incrementality should we use?" The answer for any mature marketing team is "all three, for three different questions, with a governance rule for when they disagree."

The skill exists because the individual measurement selectors (`/attribution-model-selector`, `/mmm-readiness`, `/incrementality-test-designer`) each answer "should I use this method?" — but the bigger question is "how do I run them together so my CMO can make budget decisions next quarter without re-litigating the methodology every time?"

The most common mistake this skill prevents is **picking one truth source and ignoring the others.** Teams that only use MMM make slow budget decisions on stale data. Teams that only use attribution chase ghost ROI on platform-tracked conversions. Teams that only use experiments answer narrow questions and never see the whole portfolio. Triangulation is not a compromise — it's the design.

## Required Inputs

Ask only for what is missing. Inputs are listed in priority order: the first three drive the framework design.

1. **Decisions the framework will support.** Quarterly budget allocation, weekly optimisation, campaign go/no-go, executive narrative — the cadence and stakes of each decision shape the framework.
2. **Currently used measurement methods.** What's in place: platform attribution, MMM (vendor or in-house), incrementality testing, geo testing, none.
3. **Stakeholders and their decision authority.** CMO, paid media leads, lifecycle marketing, finance — who needs which answer, and who arbitrates when models disagree.
4. Budget scale per channel.
5. Operational capacity: can the team run experiments, refresh MMM quarterly, instrument geo tests?
6. Data assets: in-platform attribution, server-side tracking, MMM-ready time-series, ID coverage.
7. Tolerance for "we cannot fully prove this" framing in executive readouts.

## The Three Layers

The framework's strength comes from each method answering a different question at its right cadence. Treat them as layers, not alternatives.

| Layer | Question it answers | Cadence | Decision authority | When it's right |
|---|---|---|---|---|
| **MMM** | What is each channel worth at the budget level? | Quarterly / semi-annual | Channel-level budget allocation, CMO-level decisions | History + variation + controls present (see `/mmm-readiness`) |
| **Incrementality** | Is the MMM right where it matters most? | On the biggest planned changes + 1–2 always-on channels per quarter | Calibrates MMM, validates large shifts before committing | Operationally feasible holdout, geo, or switchback design |
| **Attribution (DDA / rules)** | How are we performing inside each channel day-to-day? | Daily / weekly | In-channel bidding, audience, creative optimisation | Sufficient tracking inside the channel |

The three layers must be **synchronised on a calendar** — quarterly MMM read → incrementality tests on the disputed channels → in-channel optimisation continues on attribution — and **governed by a disagreement rule** decided before the disagreement appears.

## Triangulation Calendar

The default cadence for a mature team running all three layers:

```
Q1: MMM refresh (full year of data through Q4)
    → Identify the 2-3 channels with the largest CI on marginal ROI
    → Plan incrementality tests for those channels (run in Q2)
    → Plan one validation incrementality on the largest planned budget shift

Q2: Run incrementality tests planned in Q1
    → Continue attribution-based in-channel optimisation week-by-week
    → Use Q1 MMM read as the budget anchor

Q3: MMM mid-year refresh (incremental, lighter)
    → Reconcile Q2 incrementality results vs Q1 MMM estimates
    → If material gap, recalibrate MMM priors for Q4 run
    → Plan Q4 incrementality on next-quarter's biggest changes

Q4: Run Q3-planned incrementality
    → Continue attribution-based optimisation
    → Prep Q1 MMM with full-year data
```

Smaller teams without MMM operational capacity can still run a meaningful framework with **incrementality + attribution only**: pick the 2–3 channels that matter most by budget share, test each one's true lift annually or semi-annually, then trust attribution for within-channel decisions.

## Disagreement Governance

The three layers will disagree. They are designed to disagree — they answer different questions with different methods. The framework's value depends on **pre-committing which one wins which kind of disagreement**, before the disagreement appears.

| Disagreement type | Who wins | Why |
|---|---|---|
| MMM says channel A is more incremental than channel B; in-platform DDA says the reverse | **MMM** for budget-level decisions; **DDA** for in-channel optimisation | MMM sees outside-the-channel effects DDA can't; DDA sees inside-the-channel signal MMM can't |
| MMM says channel A has marginal ROI 1.4 (CI 0.9–2.1); incrementality test says lift = 0 (CI -0.1 to 0.3) | **Incrementality wins** | Direct causal measurement on a specific intervention beats inference at the channel level |
| Incrementality says creative B drives lift; MMM has no signal on creative | **Incrementality wins** within scope | MMM has no signal at creative level; it's the wrong tool |
| MMM contribution sum > 100% of revenue | **Something is broken** | Re-fit MMM with tighter priors; this is a model issue, not a triangulation issue |
| Platform-attributed conversions sum > total conversions | **Discount platform attribution** for budget decisions | The platforms are double-counting; use incrementality or MMM-derived contribution instead |
| Two MMM vendors disagree by >2× on a channel | **Run incrementality** | Stop arguing about priors; measure |

Write the governance rule into the framework charter and reference it when disagreements arise. The rule turns "which model is right?" into "the framework says X wins this decision," which is a much easier conversation.

## Worked Examples

### Example 1: DTC ecommerce, mature paid programme, $40M annual budget

Decisions: quarterly channel reallocation (CMO), weekly bidding (paid leads), campaign go/no-go (marketing lead). Existing: platform attribution everywhere, MMM run by vendor quarterly, no incrementality programme.

Recommended framework:

- **MMM (quarterly)** anchors annual budget allocation across 8 channels. Vendor refresh in Q1 and Q3.
- **Incrementality (rolling)** runs one test per quarter on the channel with the largest CI on marginal ROI in the most recent MMM. In Q1: planned test on connected TV (currently the widest CI). In Q2: lifecycle email holdout. Pre-committed: when an incrementality result and MMM mROI differ by >30% on the same channel, MMM priors get recalibrated.
- **Attribution (continuous)** drives in-platform bidding and creative rotation. Weekly performance reviews use DDA. Pre-committed: DDA never overrides MMM for cross-channel reallocation discussions.
- **Governance rule:** quarterly MMM read sets channel budgets. Mid-quarter shifts >10% of any channel's spend require an incrementality study at the new level before the shift becomes permanent. DDA never moves >5% of a channel's budget.

### Example 2: B2B SaaS, $5M annual marketing, 6-month sales cycle, no MMM

Decisions: annual budget across paid + content + events + ABM (CMO + CRO), quarterly programme prioritisation (demand gen lead), pipeline attribution to programmes (CFO ask).

Recommended framework:

- **MMM is not ready** here — see `/mmm-readiness`. History is short, paid is mostly always-on, pipeline volume is low. Don't run a vendor MMM.
- **Incrementality (semi-annual)** on the two largest programmes. Recommended: paused-webinars geo-or-region holdout, paused-content-promotion holdout. Each runs for 4–8 weeks with a 6-month post-period to allow pipeline to mature.
- **Attribution (continuous)** uses W-shaped rules-based credit (first-touch, opp-creation-touch, closed-won-touch). Used for programme prioritisation conversations only. Pre-committed: never used for absolute budget claims.
- **Governance rule:** annual budget set on the prior incrementality reads + judgement. Attribution is the conversation tool, not the decision tool. CFO ask answered with attribution + caveats explicit.

### Example 3: Marketplace, $20M annual budget, ad-hoc measurement today

Decisions: marketplace incentive programmes, supply-side acquisition spend, demand-side performance. Existing: platform attribution + ad-hoc switchback tests run by the analytics team.

Recommended framework:

- **MMM is in the medium-term roadmap.** Right now: scope an MMM readiness check after collecting one more cycle of data; meanwhile the framework runs without MMM.
- **Incrementality (rolling switchbacks)** is the workhorse. Each major incentive programme runs through a switchback or geo test. Marketplace structure means most paid tactics need spillover-aware designs (`/incrementality-test-designer`).
- **Attribution (continuous)** for in-channel optimisation only.
- **Governance rule:** every >$500K annualised programme requires a switchback or geo test before scaling. Attribution informs which programme to test next, not which to scale.

## Designing the Framework

When the user comes in fresh, structure the design conversation in this order:

1. **Decisions first.** List 3–5 marketing decisions the framework must support, with cadence and dollar stakes per decision.
2. **Map each decision to its right layer.** Annual budget → MMM (if ready) or pooled incrementality. Quarterly reallocation → MMM + validation incrementality. In-channel optimisation → attribution. Campaign go/no-go → incrementality.
3. **Identify gaps.** What layer is missing for which decision? Most teams have attribution everywhere and gaps on incrementality and MMM.
4. **Plan the calendar.** Set the quarterly cadence; commit dates for MMM refresh and incrementality launches.
5. **Write the governance rule.** Pre-commit who wins which disagreement. The rule should fit on one page.
6. **Identify the bridge.** While the framework is being built, what's the interim answer for each decision? Usually that's: attribution-based reporting + targeted incrementality + judgement, with explicit caveats.

## Communicating to Stakeholders

The framework's biggest threat is stakeholders treating each layer as a competing claim. Three communication patterns help.

- **One readout, three sections.** Quarterly business review presents MMM (channel-level budget view), incrementality (validation), attribution (operational performance) as three sections of one readout, not three separate decks competing for shelf space.
- **Name the question at the top of each chart.** A chart showing channel ROI should headline "Q3 MMM — what would each channel return at current spend?" not "Channel ROI." The question framing prevents the chart being misused for the wrong decision.
- **Always show ranges, not points.** Every channel-level number — MMM ROI, incrementality lift, attributed conversions — gets a credible interval or confidence interval. Stakeholders learn the precision the data supports.
- **Distinguish "model says" from "we recommend."** The framework outputs are inputs to a decision, not the decision itself. Recommendations layer judgement on top of model output and should be labelled as such.

## Anti-Patterns

- **Picking one truth source.** "We just use MMM" or "we just use platform attribution." Each method has known blind spots; ignoring them produces predictable mistakes.
- **No governance rule.** Models disagree; the team picks whichever supports the meeting agenda; trust in measurement erodes.
- **Calendar mismatch.** Running MMM every two years and reading it monthly. Running incrementality once and citing it for two years.
- **Treating attribution like it scales to budget decisions.** Platform attribution is optimisation-grade; using it for budget reallocation is the most common framework failure.
- **Skipping the incrementality calibration layer.** Without it, MMM and DDA will disagree forever and the team picks favourites.
- **Vendor MMM as the framework.** A vendor MMM is one layer, not a framework. If the vendor's number is the only number, the team has outsourced measurement, not built a framework.
- **Triangulating the average.** "MMM says 2.4, DDA says 1.8, incrementality says 1.5 — let's call it 1.9." Don't average; layer.
- **No bridge measurement during MMM build-out.** Teams spend 6 months building MMM and have no answer for the budget conversation in the meantime. Always design the interim.

## Output Template

```markdown
## Measurement Framework Design

### Decisions This Framework Supports
| Decision | Cadence | Dollar stake | Right layer |
|---|---|---|---|
| <decision> | <cadence> | <$> | <MMM / Incrementality / Attribution> |

### Layer Status
| Layer | Currently in place? | Recommended state | Next move |
|---|---|---|---|
| MMM | <yes/no/partial> | <state> | <next step or "/mmm-readiness"> |
| Incrementality | <yes/no/partial> | <state> | <next step or "/incrementality-test-designer"> |
| Attribution | <yes/no/partial> | <state> | <next step or "/attribution-model-selector"> |

### Triangulation Calendar
- Q1: <activity>
- Q2: <activity>
- Q3: <activity>
- Q4: <activity>

### Governance Rule
<one-page rule covering: which layer wins which decision; when results disagree by more than X, what triggers recalibration; what counts as override vs noise>

### Stakeholder Communication
<who sees which layer; how disagreements are framed; the "one readout, three sections" plan>

### Bridge Measurement (if a layer is being built)
<interim answer for each decision while the missing layer is under construction>

### First 90 Days
1. <concrete step>
2. <concrete step>
3. <concrete step>

### Caveats
- <honest limitations of the framework as designed>
```

## Quality Rubric

- `Strong`: framework names a layer per decision; calendar is concrete; governance rule pre-commits who wins which disagreement; bridge measurement is named for any layer not yet in place; first 90 days are specific.
- `Usable`: framework is sensible but governance rule is vague ("we'll figure it out") or bridge is missing.
- `Needs revision`: framework picks one layer as the truth; no calendar; no governance; recommends averaging across layers; vendor MMM treated as the whole framework.

## Guardrails

- Do not recommend a single-method framework for a team making decisions at multiple cadences.
- Do not propose triangulation that averages outputs across layers; layer them.
- Do not propose MMM as the only layer without a calibrating incrementality plan.
- Do not propose attribution as authoritative for budget reallocation; route to MMM or pooled incrementality.
- Always pre-commit the governance rule for disagreements.
- Always design the bridge measurement when a layer is missing.
- When the team isn't ready for any layer, recommend the simplest version of incrementality + attribution and revisit MMM in 6–12 months.
- When the user is choosing one method (not designing a framework), route to `/attribution-model-selector`, `/mmm-readiness`, or `/incrementality-test-designer` instead.
