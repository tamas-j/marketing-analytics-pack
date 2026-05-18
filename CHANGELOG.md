# Changelog

All notable changes to **Marketing Analytics Pack for Claude** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-05-18

### Added
- **Advanced runner — RFM segmentation execution.** `skills/rfm-segment-generator/scripts/run_rfm.py` computes Recency-Frequency-Monetary from a transactions CSV, assigns named segments (quantile rules by default — Champions, Loyal, Big spenders, New customers, Promising, At risk, Hibernating — or k-means clusters when `--method kmeans` is passed), and writes `rfm_scores.csv`, `segment_profiles.csv`, styled `segment_sizes.png` + `rf_scatter.png`, and `summary.md`. Deps declared in `scripts/requirements.txt` (`pandas`, `matplotlib`, `pyyaml`, `scikit-learn`); much lighter than the Prophet / Meridian runners. End-to-end smoke-tested against `examples/data/orders.csv` (116 customers → 8 named segments; Champions drive 33% of revenue from 15% of customers). SKILL.md and `/rfm-segment` command updated with execution-mode workflow and surface-availability table; worked example extended with the v0.2.0 execution run.
- **Advanced runner — Google Meridian MMM execution.** `skills/mmm-runner/scripts/run_mmm.py` fits a Bayesian MMM on a CSV with KPI + media spend + optional controls, computes posterior ROI / contribution / response curves, and emits styled `roi_per_channel.png` and `response_curves.png` plus `roi_per_channel.csv`, `channel_contribution.csv`, `response_curves.csv`, and `summary.md`. Deps declared in `scripts/requirements.txt` (`google-meridian`, `pandas`, `matplotlib`, `pyyaml`); written against the verified Meridian 1.6 API surface (`DataFrameInputDataBuilder` + `Meridian.sample_posterior` + `Analyzer.roi/response_curves/incremental_outcome`). SKILL.md and `/mmm-runner` command updated with execution-mode workflow and surface-availability table; worked example extended to show the v0.2.0 execution path against `examples/data/mmm-weekly.csv`. Use a venv — Meridian pulls TensorFlow + tfp-nightly (~600 MB).
- **Advanced runner — Prophet forecast execution.** `skills/forecast-runner/scripts/run_forecast.py` fits Prophet on a CSV time series, supports holidays + extra regressors, backtests against naive and seasonal-naive baselines, and writes styled forecast / components charts plus `forecast.csv`, `baselines.csv`, and `summary.md`. Deps declared in `scripts/requirements.txt` (`prophet`, `pandas`, `matplotlib`, `pyyaml`); install up-front or pass `--auto-install`. SKILL.md and `/forecast-runner` command updated with execution-mode workflow; worked example extended to show execution against `examples/data/mmm-weekly.csv` (Prophet beats both baselines on the sample data: 7.7% MAPE vs 13.8% seasonal naive vs 17.6% naive).
- **Shippability guardrails for advanced runners:** PEP 668-aware `_install_deps()` in both runners (try plain pip, fall back to `--user`, then a clear venv-setup message); README "Advanced runners — environment setup" section calling out venv usage and which Claude surfaces support execution mode; "Execution Mode Availability" surface-compatibility table in each runner's SKILL.md so Claude knows to fall back to spec mode when Bash isn't available.
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
- Experimentation batch 1: `/experiment-design-reviewer`, `/incrementality-test-designer`, and `/attribution-model-selector`.
- Worked Experimentation examples for A/B test review, geo incrementality design, and attribution approach selection.
- MMM workflows: `/mmm-readiness`, `/mmm-runner`, and `/mmm-result-interpreter` with Google Meridian as the runner target.
- Worked MMM examples for readiness, runner specification, and result interpretation.
- Forecasting command set: `/forecast-method` and `/forecast-runner` with Prophet as the runner target.
- Worked Forecasting examples for method selection and runner specification.

### Planned
- Metrics cluster examples and screenshots for README polish
- Diagnosis cluster examples and screenshots for README polish
- Segmentation cluster examples and screenshots for README polish
- Marketing operations cluster examples and screenshots for README polish
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

[Unreleased]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/tamas-j/marketing-analytics-pack/releases/tag/v0.1.0
