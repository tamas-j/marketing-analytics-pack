# Changelog

All notable changes to **Marketing Analytics Pack for Claude** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-05-19

### Added
- **Three cross-cutting new skills (Batch 2 of skills audit).** The audit identified three structural gaps: no skill for blended measurement (MMM + incrementality + attribution together), no shared adversarial-review skill for any analytical output, and no canonical reference for measurement pitfalls — so the same warnings were repeated thinly across many skills. All three are added.
  - **`measurement-triangulation` skill + `/triangulate` command** (~200 lines). Designs a blended measurement framework using all three layers (MMM for budget allocation, incrementality for calibration of the largest decisions, attribution for in-channel optimisation). Covers the triangulation calendar, the disagreement governance rule that pre-commits which layer wins which decision, three worked examples (DTC mature, B2B no-MMM, marketplace switchback-led), and stakeholder communication patterns. Addresses the audit's #2 priority gap ("missing measurement triangulation skill — senior signal lives here").
  - **`results-skeptic` skill + `/skeptic` command** (~200 lines). Adversarial second-pass review for any analytical output — forecast, MMM, experiment readout, RFM, attribution, post-mortem, brief. Runs five lenses (definition / data and method / bias and confounding / uncertainty / decision relevance), method-specific checks per analysis type, the three pre-share questions, and a Share / Caveat / Fix / Do-not-share verdict. Severity-tagged findings. Addresses the audit's #3 priority gap ("no results-skeptic / red-team skill").
  - **`measurement-pitfalls` reference skill** (~200 lines, `user-invocable: false`). Shared catalogue of common measurement pitfalls — cohort comparability, denominator errors, attribution vs causality, regression to the mean, selection / survivorship bias, Simpson's paradox, multiple testing, base rates, spillover / SUTVA violations, peeking, confounding by time, Goodhart's law, precision theatre, lurking variables, wrong counterfactual. Each section has mechanism / symptom / fix / worked example. Cross-skill wiring notes at the end map each pitfall to the skills that should link to it instead of repeating one-liners. Addresses the audit's #7 priority gap ("no shared pitfalls / glossary reference").
- **Planner routing updated.** `main-analysis-planner` and `/plan-analysis` now route to `/triangulate` for blended-measurement questions and to `/skeptic` for pre-share review. The Question-Type Classifier added Framework and Review rows.

### Changed
- Bumped plugin manifest version to `0.4.0`.

## [0.3.0] - 2026-05-19

### Changed
- **Selector tier deepened (Batch 1 of skills audit).** The seven thinnest selector / reviewer skills were rewritten to match the depth of `kpi-tree-generator`, `clv-scenario-modeller`, and `root-cause-investigation-tree`. Each now includes a decision tree, 2–3 worked examples, anti-patterns, ranked inputs, a quality rubric, and explicit cross-skill routing. Audit-driven; addresses the "selectors are too thin" finding.
  - `attribution-model-selector` (67 → ~180 lines): adds the decision tree for picking between path-based attribution, MMM, incrementality, and blended frameworks; develops the blended-framework governance pattern (which model wins which decision); three worked examples (DTC reallocation, B2B pipeline attribution, lifecycle email defence).
  - `forecast-method-selector` (66 → ~180 lines): adds the seven-step method decision tree, an error-metric guide (MAPE / sMAPE / WAPE / MAE / RMSE / Pinball), three worked examples (DTC weekly revenue, B2B short-history pipeline, lifecycle daily sends), and explicit treatment of intermittent / hierarchical / regime-change cases.
  - `segmentation-method-selector` (68 → ~210 lines): adds the activation-first decision tree (RFM is *not* the default), an activation-feasibility check by channel, method-choice-by-activation matrix, three worked examples (DTC win-back, B2B account scoring, subscription research clustering), and anti-patterns including "method-led segmentation."
  - `experiment-design-reviewer` (70 → ~210 lines): adds explicit treatment of power / MDE (with the `n ≈ 16pq/MDE²` rule), SRM and AA-test discipline, variance reduction (CUPED / stratification), peeking and sequential testing, network-effects mitigation table, three worked examples (under-powered button test, eligibility-after-assignment email test, marketplace spillover).
  - `incrementality-test-designer` (74 → ~210 lines): adds design selection decision tree, geo-test power rules of thumb (markets, not impressions), spillover mitigation table, parallel-trends and placebo-test pre-period checks, three worked examples (CRM reactivation, paid social geo test, marketplace switchback).
  - `mmm-readiness-checker` (76 → ~190 lines): adds explicit Ready / Caveats / Blocked thresholds per check, decision tree, input priority for fixes, three worked verdict examples (Ready, Blocked, Caveats), bridge-measurement guidance for the Blocked case.
  - `mmm-result-interpreter` (68 → ~200 lines): adds diagnostic-threshold scorecard (R-hat / ESS / holdout / residuals / decomposition), explicit separation of contribution / average ROI / marginal ROI with worked stories, credible-interval discipline (overlapping intervals = not different), response-curve / saturation interpretation, three worked readouts (healthy, caveat-heavy, counter-intuitive).

## [0.2.1] - 2026-05-19

### Added
- `.claude-plugin/marketplace.json` so the repository can be added directly as a Claude plugin marketplace.
- `style-picker` skill and `skills/style-picker/scripts/set_style.py` helper for safe custom style updates and optional preview charts.
- `skills/data-readiness-checker/scripts/profile_data.py`, a stdlib CSV profiler for row count, missingness, date-like fields, and duplicate grain keys.
- HTML report artifacts now support report types, audience/source/data metadata, previous-report labels for recurring readouts, and key-section highlight cards extracted from the source markdown.
- **Sharing layer — `/report` command + `report-builder` skill.** Packages whatever the most recent skill produced (markdown summary, chart PNGs, runner output folder, or chat output captured to a temp file) into a single shareable file. Defaults to **HTML** — `skills/report-builder/scripts/build_html_report.py` renders the markdown, embeds every PNG / JPG / SVG from the images dir as a base64 data URI, and applies brand palette + typography from `lib/styles/` so the report visually matches the chart visuals. If the source markdown doesn't reference some discovered images, they're auto-appended under a "Charts" section so runner outputs always surface their visuals. **DOCX / PPTX / PDF** are produced by composing with the runtime `docx` / `pptx` / `pdf` skills — narrative for DOCX, one-slide-per-heading for PPTX, locked handoff for PDF. Smoke-tested end-to-end against the RFM runner output: 217 KB HTML file, 2 charts embedded, brand-styled. Deps for the HTML helper: `markdown` + `pyyaml` (PEP 668-aware `--auto-install`).
- Five new chart patterns in the `data-visualization` reference skill: **Scatter** (RFM, CAC vs LTV, spend vs ROI), **Multi-Line** (MMM response curves, cohort retention), **Line With Interval / Fan** (forecasts and any line with an uncertainty band), **Waterfall** (suppression decomposition, list eligibility losses, revenue bridges), and **Overlap Matrix** (audience overlap heatmap, persona × channel reach). All five copy-paste cleanly, follow the existing token-loading idiom, and were smoke-tested locally. Added a "Pattern Selection Guide" table so Claude picks the right shape per situation.
- `examples/check-data-example.md` — worked `/check-data` flow against `examples/data/mmm-weekly.csv`, closing the previous data-readiness example gap.
- `examples/report-example.md` — worked `/report` flow packaging an RFM run as HTML, with variations for PPTX (exec deck) and DOCX (narrative for comms).

### Changed
- Bumped plugin manifest version to `0.2.1` so Claude Code update checks see this release.
- **Audience framing widened.** README, CLAUDE.md, memory files, and the relevant skill / command bodies now describe the audience as "analysts, marketers, growth / lifecycle owners, product owners, founders — anyone who works with marketing data" rather than "non-technical marketing/analytics person." The bar is "understands the question, has or can get the data, would rather not hand-roll the analysis or chart code." Skill bodies still avoid assuming SQL / Python fluency.
- README now reflects the current 28-command package, the `/report` sharing layer, and the direct marketplace manifest.
- `main-analysis-planner` routes ambiguous user intents to concrete slash commands instead of prose skill names.
- Front-door and Metrics skills now include stronger routing, profiling, implementation, scenario, and instrumentation guidance.
- Bundled chart styles now use `DejaVu Sans` instead of `Arial` to avoid noisy matplotlib font fallback warnings on Linux.

### Removed
- Stale `docs/CONTRIBUTING.md` duplicate. The current contributor guide lives at the repo root (`CONTRIBUTING.md`).
- Stale `.gitkeep` files from `docs/` and `scripts/`.

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

[Unreleased]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/tamas-j/marketing-analytics-pack/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/tamas-j/marketing-analytics-pack/releases/tag/v0.1.0
