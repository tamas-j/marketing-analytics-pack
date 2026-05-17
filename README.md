# Marketing Analytics Pack for Claude

A coherent skills pack that helps non-technical marketing and analytics people do real analytical work in Claude — guided by a main planner, validated by a data readiness checker, and rendered through a shared visual style system.

> **Status:** 0.1.1 — scaffold plus shared visual style system, front-door workflows (`/style`, `/plan-analysis`, `/check-data`), and the Metrics command set (`/kpi-tree`, `/metric-spec-card`, `/customer-journey-measurement`, `/clv-scenario`). Track progress in [CHANGELOG.md](./CHANGELOG.md).

## Why this exists

Most analytics tooling assumes you already know what to do. This pack assumes you don't. You bring a question and a CSV; the pack figures out what type of analysis you need, checks that your data can support it, and produces output that's screenshot-worthy without you touching a chart library.

## Who it's for

A non-technical marketing or analytics person who wants to do real analytical work but doesn't know how to start. The plugin's entry point is the **Main analysis planner**, which diagnoses your need and routes you to the right skill. The **Data readiness checker** validates your data before any work begins.

## Install

```
claude plugins add tamas-j/marketing-analytics-pack
```

Also planned for distribution via the official Anthropic plugin marketplace and 1–2 third-party Claude marketplaces.

## What's in the pack

25 skills across 7 clusters. The full checklist lives in the [URB-182 ticket](https://linear.app/urbsai/issue/URB-182/marketing-analytics-plugin-skills-pack-v1); high level:

- **Front door** — Style picker, Main analysis planner, Data readiness checker
- **Metrics** — KPI tree generator, Metric spec card generator, CLV scenario modeller, Customer journey measurement framework
- **Diagnosis** — Root cause investigation tree, Analysis brief generator, Churn driver narrative generator, Campaign post-mortem generator
- **Segmentation** — Segmentation method selector, RFM segment generator *(advanced runner)*, Persona-to-segment translator, Audience overlap visualiser
- **Experimentation** — Experiment design reviewer, Incrementality test designer, Attribution model selector, MMM readiness checker, MMM runner — Google Meridian *(advanced runner)*, MMM result interpreter
- **Forecasting** — Forecast method selector, Forecast runner — Prophet *(advanced runner)*
- **Marketing operations** — Suppression waterfall, Marketing taxonomy auditor, Frequency cap / fatigue analyser, NBA logic generator

## Architecture

Skills are tiered by install weight. Most are **core skills** — prompt + matplotlib, install in seconds. A handful are **advanced runners** (RFM, Forecast/Prophet, MMM/Meridian) that declare heavier dependencies and pip-install them on first use.

Every skill that produces visuals follows a **shared style system**: chart code patterns live in a `data-visualization` reference skill (Claude copies them into generated code at runtime), brand and palette settings live in `lib/styles/*.yaml` (read at runtime by a thin helper), and a front-door **Style picker** skill lets you select or customise a style. Three bundled styles — `default`, `executive`, `custom` — plus optional brand mode (logo, primary colour, font). The point is that output across the whole pack is cohesive, screenshot-worthy, and copy-pasteable.

## Data input (v1)

Files only — CSV, Excel, or pasted data. Database access is deferred to a later version. If you already have a warehouse MCP connected in Claude, point it at your table and describe the schema; the skills will work against that today, just not bundled.

## Repository layout

```
marketing-analytics-pack/
├── .claude-plugin/
│   └── plugin.json      # plugin manifest (name, version, description, author)
├── commands/            # slash commands users invoke (e.g. /kpi-tree, /style, /forecast)
├── skills/              # composable knowledge units commands pull in (chart patterns, method comparisons, etc.)
├── lib/                 # shared brand/style config + a thin reader
│   └── styles/          # default / executive / custom YAML
├── docs/                # design notes, conventions, contribution guide
└── examples/            # sample datasets + worked example flows
```

## Screenshots

_Coming with the first published skill — README will be updated with a gallery before marketplace submission._

## Example flow

See [examples/front-door-example.md](./examples/front-door-example.md), [examples/kpi-tree-example.md](./examples/kpi-tree-example.md), [examples/metric-spec-card-example.md](./examples/metric-spec-card-example.md), [examples/customer-journey-measurement-example.md](./examples/customer-journey-measurement-example.md), and [examples/clv-scenario-example.md](./examples/clv-scenario-example.md) for the first worked examples.

## Roadmap

See [URB-182](https://linear.app/urbsai/issue/URB-182/marketing-analytics-plugin-skills-pack-v1) for the full build order. In short: scaffold → style system + front door → KPI tree generator → lightweight clusters → experimentation → segmentation + forecasting → advanced runners → polish → publish.

## License

MIT — see [LICENSE](./LICENSE).
