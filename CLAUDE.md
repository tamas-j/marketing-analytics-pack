# Memory — Marketing Analytics Pack

Working memory for the `marketing-analytics-pack` plugin build. Future turns: read this first; deeper context lives in `memory/`.

## Project
**Marketing Analytics Pack for Claude** (`marketing-analytics-pack`), v0.2.0, MIT.
A coherent skills pack (27 slash commands + 1 `data-visualization` reference skill, across 7 clusters) for non-technical marketing/analytics users. Three advanced runners (Prophet, Google Meridian, pandas/scikit RFM) ship with real execution from v0.2.0 onwards. Tracked in Linear as **URB-182** (parent: URB-181, project: Experiments, team: Urbsai).

## Locked decisions
| Decision | Value |
|----------|-------|
| GitHub handle | `tamas-j` |
| Repo | https://github.com/tamas-j/marketing-analytics-pack (live, v0.1.0 tagged; v0.1.1 manifest fix; v0.2.0 with real advanced runners) |
| Plugin name | `marketing-analytics-pack` (`-pack` suffix — `marketing-analytics` taken on claudepluginhub) |
| Display name | "Marketing Analytics Pack for Claude" (README only — not a manifest field) |
| License | MIT |
| Manifest path | `.claude-plugin/plugin.json` — *not* `plugin.json` at the repo root (Anthropic convention) |
| Manifest schema | Exactly 4 fields: `name`, `version`, `description`, `author`. Nothing else (no `displayName`, `keywords`, `categories`, `repository`, `skills`, etc.) |
| Name regex | `^[a-z0-9][a-z0-9-]{1,63}$`, no hidden Unicode (marketplace invariants I10/I11) |
| Initial version | 0.1.0 → 0.1.1 (manifest-path fix) → 0.2.0 (real Prophet / Meridian / RFM execution; see CHANGELOG) |
| MMM library | **Google Meridian** (chosen over PyMC-Marketing) |
| Forecast library | **Prophet** |
| Data input scope (v1) | Files only — CSV / Excel / paste. DB access deferred, documented in README. |
| Distribution | GitHub primary → Anthropic official marketplace → 1–2 third-party marketplaces |

## Architecture (the spine)
- **Tiered skills.** Most are **core skills** (prompt + matplotlib, install in seconds): planner, readiness checker, style picker, all selectors / generators / interpreters / framework builders. Three are **advanced runners** with heavier deps declared and pip-installed on first use: RFM (pandas/scikit), Forecast (Prophet), MMM (Google Meridian).
- **Commands vs skills — separate peer directories (financial-services pattern).** Two flavours, two folders:
  - **`commands/<name>.md`** — slash commands the user invokes (`/kpi-tree`, `/check-data`, `/style`, `/forecast`). Frontmatter: `description` + `argument-hint`. **No `name:` field — filename is the command name.** All 27 user-invocable entries live here.
  - **`skills/<name>/SKILL.md`** — composable knowledge units commands pull in via `Use skill: "<name>"`. Frontmatter: `description` (with "Use when…" trigger), optional `user-invocable: false` for pure model-only. The `data-visualization` reference skill is the canonical example. Skills can have `references/` (static support files) and `scripts/` (Python the skill runs) subdirs.
  - Commands **compose** skills. One command can pull in several skills (e.g. `/forecast` pulls in `skills/forecast-methods/` and `skills/data-visualization/`).
  - Cross-plugin invocation uses `/<plugin-name>:<command>` namespacing — `/marketing-analytics-pack:kpi-tree` when called from outside the plugin; bare `/kpi-tree` from inside the user's loaded session.
- **Shared visual style system (revised in v0.1.1).** Three layers:
  1. **Chart code patterns** live in a `data-visualization` *reference skill* (`skills/data-visualization/SKILL.md`). Skills don't import code — Claude copies the patterns into generated Python at runtime. Matches Anthropic's `knowledge-work-plugins/data` pattern.
  2. **Brand / palette / typography config** lives in `lib/styles/*.yaml` (`default`, `executive`, `custom`). Each YAML carries optional `brand: { primary_hex, logo_path, font_family }` slots.
  3. **A thin `lib/visualize.py` helper** reads the active style YAML and exposes a small palette/typography API. Not an import target for chart drawing — just a config reader.
  - Front-door **Style picker** skill walks the user through choices and writes `lib/styles/custom.yaml`. Visual consistency is **core infrastructure, not decoration** — mirrors Tamas's CV line at RAPP ("Established data visualisation standards adopted by a 5-person BI team").
- **Entry point = Main analysis planner.** It diagnoses the user's need and routes them to the right skill. **Data readiness checker** validates input before any work starts. These two plus Style picker are the "front door."
- **Files-only input** for v1. README documents the workaround for warehouse users: "connect your warehouse MCP and describe the table to Claude" (works today, just not built in). v2 will add `.mcp.json` for direct warehouse connectors.

## Target user
Non-technical marketing/analytics person who wants to do real analytical work but doesn't know how to start. SKILL.md "Required inputs" sections must be written for non-technical readers.

## Repo structure
```
marketing-analytics-pack/
├── .claude-plugin/
│   └── plugin.json      # manifest (4 fields: name, version, description, author)
├── README.md
├── LICENSE              # MIT
├── CHANGELOG.md         # Keep a Changelog
├── .gitignore
├── CLAUDE.md            # ← this file (developer memory)
├── commands/            # slash commands — one .md per command (no name field, filename = command name)
├── skills/              # composable knowledge — one folder per skill, SKILL.md + optional references/ + scripts/
├── lib/                 # brand/style config + thin reader (no chart code)
│   └── styles/          # default.yaml / executive.yaml / custom.yaml
├── scripts/             # validate.py (manifest + YAML lint), other repo tooling
├── docs/                # design notes, conventions, contribution guide
├── examples/            # sample datasets + worked example flows
└── memory/              # deep memory (people, projects, context)
```

## Conventions
- **Commands (`commands/*.md`):** frontmatter is `description` + `argument-hint`. No `name:` field — the filename is the command name. Body is the workflow: numbered steps, "Use skill: \"<name>\"" calls to pull in shared knowledge, examples, tips. Reference: `plugins/vertical-plugins/financial-analysis/commands/dcf.md` in the financial-services audit.
- **Skills (`skills/<name>/SKILL.md`):** required-inputs section for a non-technical reader. Optional `references/` (static support files — templates, examples, dialect notes — the `data-context-extractor` pattern) and `scripts/` (Python the skill runs — the `data-context-extractor` + advanced-runner pattern) subdirs.
- **Frontmatter:**
  - Commands: `description`, `argument-hint`. No `name:`.
  - Model-invoked skills: `description` ("Use when…" pattern). Add `user-invocable: false` for pure model-only.
  - Multi-mode skills: `description: >` block scalar with "MODE A Triggers: …" / "MODE B Triggers: …" sections (the `data-context-extractor` pattern).
  - `description` is 10–2000 chars, no leading/trailing whitespace, no hidden Unicode.
- **Visual output.** Skills copy chart patterns from the `data-visualization` reference skill into the Python they generate. They read style config via the thin `lib/visualize.py` helper (palette, typography, brand fields). Skills must not hand-roll style; pull from the active style YAML.
- **Dependencies.** Core skills assume only the standard pack runtime (matplotlib included). Advanced runners declare their extra deps explicitly and pip-install on first invocation; never assume Prophet / Meridian / scikit is present in a core skill.
- **CHANGELOG.md** must stay in lockstep with `.claude-plugin/plugin.json` `version` — common marketplace rejection cause.
- **Semver** for releases. 0.x = pre-stable; bumping to 1.0.0 when the full 25-skill pack ships.
- **File naming:** lowercase, hyphens (`kpi-tree-generator`, `mmm-readiness-checker`). Skill directory name **must** match the `name` field in its SKILL.md frontmatter — slash commands in prose are dead if they don't.
- **Validation before push:** run `scripts/validate.py` — JSON loads manifest, YAML loads every style file, frontmatter has required fields, names match invariants I1–I11.
- **Each cluster could spawn a sub-ticket** if the build runs long; otherwise tracked via the checklist in URB-182.

## Build order (URB-182 §"Order of operations")
1. **Scaffold + style system + KPI tree generator** — proves end-to-end pattern.
2. Remaining front-door skills — Main analysis planner, Data readiness checker.
3. Metrics + Diagnosis + Marketing ops clusters (lightest skills, fastest wins, strongest CV signal).
4. Experimentation cluster (most senior signal, includes MMM stack).
5. Segmentation + Forecasting clusters.
6. Advanced runners — RFM, Forecast (Prophet), MMM (Meridian).
7. README polish + screenshots + sample data.
8. GitHub publish.
9. Marketplace submissions (Anthropic + 1–2 third-party).
10. Add GitHub URL to CV.

## 25-skill checklist (see URB-182 for live status)
- **Front door:** Style picker · Main analysis planner · Data readiness checker
- **Metrics:** KPI tree generator · Metric spec card generator · CLV scenario modeller · Customer journey measurement framework
- **Diagnosis:** Root cause investigation tree · Analysis brief generator · Churn driver narrative generator · Campaign post-mortem generator
- **Segmentation:** Segmentation method selector · RFM segment generator *(advanced)* · Persona-to-segment translator · Audience overlap visualiser
- **Experimentation:** Experiment design reviewer · Incrementality test designer · Attribution model selector · MMM readiness checker · MMM runner — Google Meridian *(advanced)* · MMM result interpreter
- **Forecasting:** Forecast method selector · Forecast runner — Prophet *(advanced)*
- **Marketing ops:** Suppression waterfall · Marketing taxonomy auditor · Frequency cap / fatigue analyser · NBA logic generator

## Success criteria (URB-182)
- 25 skills implemented with consistent visual style, each with non-technical-friendly SKILL.md
- Plugin installable end-to-end on a fresh Claude install
- Working example flow demonstrable on sample data
- Published to GitHub with polished README
- Submitted to Anthropic official marketplace
- Listed on at least 1 third-party marketplace
- GitHub URL added to CV
- *(Stretch)* First public install / star / external feedback

## Parallel housekeeping (URB-181 carryover)
- [ ] Unfork or private the existing forks (`jobs-data`, `lenny-skills`) on `tamas-j`
- [ ] Create profile README repo (`tamas-j/tamas-j`) — short pitch + link to the plugin, ship after first skill is live

## Status (live)
- ✅ **0.1.0 scaffold** pushed to GitHub: folder structure, manifest, LICENSE, CHANGELOG, README skeleton, .gitignore, CLAUDE.md.
- ✅ **0.1.1** — manifest moved to `.claude-plugin/plugin.json`, schema stripped to 4 fields, visual style architecture revised after auditing `claude-for-legal` + `knowledge-work-plugins/data`.
- ✅ **0.1.x build-out** — all 27 commands + 27 backing skills + style system + `scripts/validate.py` + 28 worked examples + 5 sample-data CSVs.
- ✅ **0.2.0 (this turn, 2026-05-18)** — real execution for all three advanced runners:
  - `skills/forecast-runner/scripts/run_forecast.py` (Prophet, ~370 lines) — fit + baselines + styled charts. Smoke-tested: Prophet beat naive 17.6% MAPE and seasonal naive 13.8% with 7.7% MAPE on `mmm-weekly.csv`.
  - `skills/mmm-runner/scripts/run_mmm.py` (Meridian, ~470 lines) — written against verified Meridian 1.6 API (`DataFrameInputDataBuilder` → `Meridian.sample_posterior` → `Analyzer.roi/response_curves/incremental_outcome`). CLI verified; full smoke test deferred to user machine because TensorFlow + tfp-nightly is too large for the sandbox install budget.
  - `skills/rfm-segment-generator/scripts/run_rfm.py` (pandas + optional scikit, ~430 lines) — Recency-Frequency-Monetary + named segments or k-means. Smoke-tested: 116 customers → 8 segments, Champions drive 33% of revenue from 15% of customers.
  - Shippability guardrails: PEP 668-aware `_install_deps()` (plain pip → `--user` → clear venv message), README "Advanced runners — environment setup" section, "Execution Mode Availability" table in each runner's SKILL.md so Claude knows to fall back to spec mode on web chat.
- ⏭ **Next:** screenshot gallery (real chart outputs already produced — capture them into the README); GitHub tag `v0.2.0`; marketplace submissions.

→ Deeper context: `memory/projects/marketing-analytics-pack.md`, `memory/context/build-conventions.md`, `memory/glossary.md`
