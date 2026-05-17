# Changelog

All notable changes to **Marketing Analytics Pack for Claude** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Shared visual style system: `lib/styles/default.yaml`, `lib/styles/executive.yaml`, `lib/styles/custom.yaml`, and thin `lib/visualize.py` style reader.
- `skills/data-visualization/` reference skill with reusable matplotlib chart patterns.
- `/style` command workflow for selecting or customising the active chart style.
- `/kpi-tree` command and `kpi-tree-generator` skill for the first proof-of-pattern marketing analytics workflow.
- Worked KPI tree example for a subscription retention use case.
- `/plan-analysis` and `/check-data` front-door commands, backed by `main-analysis-planner` and `data-readiness-checker` skills.
- Front-door example showing how the planner routes a campaign effectiveness question.
- `/metric-spec-card` command and `metric-spec-card-generator` skill for precise metric definitions.
- Worked metric spec example for ecommerce repeat purchase rate.
- `/customer-journey-measurement` command and framework skill for lifecycle-stage measurement design.
- Worked customer journey measurement example for an ecommerce skincare brand.
- `/clv-scenario` command and `clv-scenario-modeller` skill for lightweight CLV scenario planning.
- Worked CLV scenario example for subscription acquisition economics.
- `/root-cause-tree` command and `root-cause-investigation-tree` skill for structured metric movement diagnosis.
- Worked root cause example for an ecommerce revenue drop.
- `/analysis-brief`, `/churn-driver-narrative`, and `/campaign-post-mortem` commands with backing Diagnosis skills.
- Worked Diagnosis examples for repeat purchase analysis planning, subscription churn, and campaign review.
- Segmentation command set: `/segmentation-method`, `/persona-to-segment`, `/audience-overlap`, and `/rfm-segment`.
- Worked Segmentation examples for method selection, persona translation, audience overlap, and RFM.
- Marketing operations command set: `/suppression-waterfall`, `/marketing-taxonomy-auditor`, `/frequency-cap-fatigue`, and `/nba-logic`.
- Worked Marketing operations examples for audience suppression, taxonomy audit, fatigue, and next-best-action logic.

### Planned
- Metrics cluster examples and screenshots for README polish
- Diagnosis cluster examples and screenshots for README polish
- Segmentation cluster examples and screenshots for README polish
- Marketing operations cluster examples and screenshots for README polish
- Remaining skills across Experimentation and Forecasting clusters
- Advanced runners: RFM (pandas/scikit), Forecast (Prophet), MMM (Google Meridian)
- Sample datasets + screenshot gallery for README and marketplace submission
- `scripts/validate.py` for JSON / YAML / manifest sanity checks before push

## [0.1.1] - 2026-05-17

### Changed
- **BREAKING (manifest path):** Moved `plugin.json` → `.claude-plugin/plugin.json` to match the official Claude plugin convention. The marketplace validator (`claude plugin validate`) expects the manifest at that path; ours would have been rejected.
- **Manifest schema simplified** to the official 4-field shape — `name`, `version`, `description`, `author`. Removed `displayName`, `keywords`, `categories`, `homepage`, `repository`, `bugs`, `license`, `skills` (none of these are part of the official schema). License is conveyed via the top-level `LICENSE` file.
- **Visual style architecture revised** (locked decision update): instead of a heavyweight `lib/visualize.py` that skills import, the style system is `lib/styles/*.yaml` (runtime brand/style config) plus a thin Python helper for reading those YAMLs. Chart code patterns live in a `data-visualization` reference SKILL.md and are copied into generated code by Claude at runtime. Matches Anthropic's `knowledge-work-plugins/data` pattern.
- **Commands vs skills separated into peer directories** (locked decision update, financial-services pattern): `commands/<name>.md` for slash commands the user invokes (frontmatter: `description` + `argument-hint`, filename is the command name), `skills/<name>/SKILL.md` for composable knowledge units commands pull in. Commands compose skills via `Use skill: "<name>"`. Most of the 25 planned entries are commands; a smaller set of shared-knowledge skills (chart patterns, statistical methods, forecast / segmentation / attribution method comparisons) sit under `skills/`.

### Added
- `commands/` directory scaffold (peer to `skills/`).

### Notes
- Followed audits of `claude-for-legal`, `knowledge-work-plugins/data`, and `claude-for-financial-services` to align with marketplace conventions before building the first real command.

## [0.1.0] - 2026-05-17

### Added
- Initial plugin scaffold and repository structure (`/skills`, `/lib`, `/docs`, `/examples`).
- `plugin.json` manifest (name `marketing-analytics-pack`, version `0.1.0`, MIT license). *(Path corrected in 0.1.1.)*
- MIT `LICENSE`.
- README skeleton with pitch, install path, and planned skill clusters.
- `.gitignore` for Python and common editor / OS artefacts.
- `CLAUDE.md` working memory capturing locked decisions, architecture, conventions, and visual style approach.

[Unreleased]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/tamas-j/marketing-analytics-pack/releases/tag/v0.1.0
