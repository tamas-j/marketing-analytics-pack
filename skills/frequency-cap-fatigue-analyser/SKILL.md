---
name: frequency-cap-fatigue-analyser
description: Use when analysing marketing contact frequency, fatigue, saturation, over-contact, frequency caps, engagement decay, opt-outs, complaints, conversions, and customer pressure.
---

# Frequency Cap Fatigue Analyser

This skill diagnoses contact pressure and fatigue risk. It helps users decide whether they should cap sends, impressions, contacts, or campaign eligibility.

## Required Inputs

Ask only for what is missing:

- Channel and time window.
- Customer/user identifier.
- Contact events with timestamps.
- Engagement and conversion events.
- Negative signals, such as unsubscribes, complaints, opt-outs, churn, refunds, or support contacts.
- Segment or lifecycle fields, if available.

## Method

1. Define contact pressure: contacts per user per time window.
2. Create frequency bands.
3. Compare engagement, conversion, and negative signals by band.
4. Inspect customer mix by band.
5. Identify point of diminishing returns or risk.
6. Recommend caps, priority rules, and testing.

## Output Template

```markdown
## Frequency Cap and Fatigue Analysis

### Question
<channel, audience, time window>

### Frequency Bands
| Band | Definition | Audience share | Engagement | Conversion | Negative signal | Readout |
|---|---|---:|---:|---:|---:|---|
| <band> | <definition> | <pct> | <metric> | <metric> | <metric> | <readout> |

### Recommended Rule
<cap or prioritisation rule>

### Segment Notes
- <segment-specific readout>

### Test Plan
- <test>

### Caveats
- <caveat>
```

## Interpretation Guide

- Fatigue often appears as flat or falling conversion plus rising opt-outs, complaints, or ignores.
- High-value customers may tolerate higher frequency if messages are relevant.
- New customers may need onboarding frequency but should not receive conflicting campaigns.
- Channel-level caps can miss total pressure across email, SMS, push, paid, and onsite.

## Guardrails

- Do not set caps without considering campaign priority.
- Do not suppress important service or transactional messages.
- Do not assume frequency causes fatigue without considering customer intent and lifecycle stage.
- Do not ignore silent fatigue: non-opens, non-clicks, lower conversion, or churn risk.
