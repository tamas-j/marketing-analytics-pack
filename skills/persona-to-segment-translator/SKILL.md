---
name: persona-to-segment-translator
description: Use when translating qualitative personas, ICPs, or audience descriptions into measurable segment rules, proxy fields, validation checks, and activation guidance.
---

# Persona To Segment Translator

This skill bridges qualitative persona work and measurable segmentation. It turns persona descriptions into proxy fields, rules, caveats, and validation checks.

## Required Inputs

Ask only for what is missing:

- Persona or ICP description.
- Business model and product.
- Activation use case.
- Available fields or systems.
- Channel where the segment will be used.

## Translation Method

1. Extract persona traits:
   - needs
   - motivations
   - barriers
   - behaviors
   - value potential
   - lifecycle stage
   - channel preference
2. Convert each trait into observable proxies.
3. Rate proxy strength as strong, medium, or weak.
4. Build simple segment rules.
5. Define validation checks.
6. Flag missing data and bias risks.

## Output Template

```markdown
## Persona-To-Segment Translation

### Persona Summary
<persona>

### Segment Definition
<plain-English definition>

### Proxy Field Map
| Persona trait | Measurable proxy | Field needed | Proxy strength |
|---|---|---|---|
| <trait> | <proxy> | <field> | <Strong/Medium/Weak> |

### Segment Rules
Include:
- <rule>

Exclude:
- <rule>

### Validation Checks
- <check>

### Activation Notes
- <channel/use>

### Caveats
- <risk>
```

## Guardrails

- Do not use protected or sensitive traits unless the user has a legitimate, compliant use case.
- Do not assume intent from a single weak proxy.
- Do not make segments so narrow they are unusable.
- Do not recommend activation unless the segment can be reached in the channel.
