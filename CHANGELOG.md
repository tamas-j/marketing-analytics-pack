# Changelog

All notable changes to **Marketing Analytics Pack for Claude** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Shared visual style system: `lib/styles/*.yaml` (runtime config) + thin `lib/visualize.py` (style reader / palette helper) + `skills/data-visualization/` reference skill with chart code patterns.
- Front-door skills: Style picker, Main analysis planner, Data readiness checker
- KPI tree generator (first proof-of-pattern skill)
- Remaining 24 skills across Metrics, Diagnosis, Segmentation, Experimentation, Forecasting, and Marketing operations clusters
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
