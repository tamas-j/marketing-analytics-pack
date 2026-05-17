# Changelog

All notable changes to **Marketing Analytics Pack for Claude** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Shared visual style system (`lib/visualize.py`, `lib/styles/*.yaml`)
- Front-door skills: Style picker, Main analysis planner, Data readiness checker
- KPI tree generator (first proof-of-pattern skill)
- Remaining 24 skills across Metrics, Diagnosis, Segmentation, Experimentation, Forecasting, and Marketing operations clusters
- Advanced runners: RFM (pandas/scikit), Forecast (Prophet), MMM (Google Meridian)
- Sample datasets + screenshot gallery for README and marketplace submission

## [0.1.0] - 2026-05-17

### Added
- Initial plugin scaffold and repository structure (`/skills`, `/lib`, `/docs`, `/examples`).
- `plugin.json` manifest (name `marketing-analytics-pack`, version `0.1.0`, MIT license).
- MIT `LICENSE`.
- README skeleton with pitch, install path, and planned skill clusters.
- `.gitignore` for Python and common editor / OS artefacts.
- `CLAUDE.md` working memory capturing locked decisions, architecture, conventions, and visual style approach.

[Unreleased]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tamas-j/marketing-analytics-pack/releases/tag/v0.1.0
