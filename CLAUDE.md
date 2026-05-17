# Memory — Marketing Analytics Pack

Working memory for the `marketing-analytics-pack` plugin build. Future turns: read this first; deeper context lives in `memory/`.

## Project
**Marketing Analytics Pack for Claude** (`marketing-analytics-pack`), v0.1.0, MIT.
A coherent skills pack (25 skills, 7 clusters) for non-technical marketing/analytics users. Tracked in Linear as **URB-182** (parent: URB-181, project: Experiments, team: Urbsai).

## Locked decisions
| Decision | Value |
|----------|-------|
| GitHub handle | `tamas-j` |
| Repo | https://github.com/tamas-j/marketing-analytics-pack (not yet pushed) |
| Plugin name | `marketing-analytics-pack` (`-pack` suffix — `marketing-analytics` taken on claudepluginhub) |
| Display name | "Marketing Analytics Pack for Claude" |
| License | MIT |
| Initial version | 0.1.0 (semver) |
| MMM library | **Google Meridian** (chosen over PyMC-Marketing) |
| Forecast library | **Prophet** |
| Data input scope (v1) | Files only — CSV / Excel / paste. DB access deferred, documented in README. |
| Distribution | GitHub primary → Anthropic official marketplace → 1–2 third-party marketplaces |

## Architecture (the spine)
- **Tiered skills.** Most are **core skills** (prompt + matplotlib, install in seconds): planner, readiness checker, style picker, all selectors / generators / interpreters / framework builders. Three are **advanced runners** with heavier deps declared and pip-installed on first use: RFM (pandas/scikit), Forecast (Prophet), MMM (Google Meridian).
- **Shared visual style system.** Every skill that produces visuals imports `/lib/visualize.py` and reads from `/lib/styles/*.yaml`. Bundled styles: `default`, `executive`, `custom`. A front-door **Style picker** skill lets the user select or customise. Visual consistency is **core infrastructure, not decoration** — mirrors Tamas's CV line at RAPP ("Established data visualisation standards adopted by a 5-person BI team").
- **Entry point = Main analysis planner.** It diagnoses the user's need and routes them to the right skill. **Data readiness checker** validates input before any work starts. These two plus Style picker are the "front door."
- **Files-only input** for v1. README documents the workaround for warehouse users: "connect your warehouse MCP and describe the table to Claude" (works today, just not built in).

## Target user
Non-technical marketing/analytics person who wants to do real analytical work but doesn't know how to start. SKILL.md "Required inputs" sections must be written for non-technical readers.

## Repo structure
```
marketing-analytics-pack/
├── plugin.json          # manifest
├── README.md
├── LICENSE              # MIT
├── CHANGELOG.md         # Keep a Changelog, starts at 0.1.0
├── .gitignore
├── CLAUDE.md            # ← this file
├── skills/              # one folder per skill (SKILL.md + assets)
├── lib/                 # shared visual style + helpers
│   └── styles/          # default.yaml / executive.yaml / custom.yaml
├── docs/                # design notes, conventions, contribution guide
├── examples/            # sample datasets + worked example flows
└── memory/              # deep memory (people, projects, context)
```

## Conventions
- **SKILL.md** for every skill. Required-inputs section written for non-technical users. Bundled `assets/` and `references/` as needed.
- **Visual output** always goes through `lib/visualize.py`. Skills must not hand-roll matplotlib styles — pull from the shared style config.
- **Dependencies.** Core skills assume only the standard pack runtime (matplotlib included). Advanced runners declare their extra deps explicitly and pip-install on first invocation; never assume Prophet / Meridian / scikit is present in a core skill.
- **CHANGELOG.md** must stay in lockstep with `plugin.json` version — common marketplace rejection cause.
- **Semver** for releases. 0.x = pre-stable; bumping to 1.0.0 when the full 25-skill pack ships.
- **File naming:** lowercase, hyphens (`kpi-tree-generator`, `mmm-readiness-checker`).
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
- ✅ **0.1.0 scaffold** — folder structure, `plugin.json`, MIT `LICENSE`, `CHANGELOG.md`, README skeleton, `.gitignore`, this `CLAUDE.md`.
- ⏭ **Next:** Task #2 — shared visual style system (`lib/visualize.py` + `lib/styles/*.yaml` + Style picker skill).
- ⏭ **After that:** Task #3 — KPI tree generator (proof-of-pattern first skill).

→ Deeper context: `memory/projects/marketing-analytics-pack.md`, `memory/context/build-conventions.md`, `memory/glossary.md`
