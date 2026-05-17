# Build conventions

Rules of the road for the Marketing Analytics Pack codebase. Future turns: follow these unless URB-182 explicitly overrides.

## Skill structure
- One folder per skill under `skills/{kebab-name}/`.
- Each folder has a `SKILL.md`. Optional `assets/` and `references/` subfolders.
- `SKILL.md` must include a **"Required inputs"** section written for a non-technical reader — name the file shape, the columns, and what to do if you don't have them.
- Lowercase, hyphenated folder/file names (`kpi-tree-generator`, `mmm-readiness-checker`).

## Dependencies
- **Core skills** assume only the standard pack runtime (which includes matplotlib). Do **not** import pandas, scikit, Prophet, Meridian, etc. in a core skill.
- **Advanced runners** (RFM, Forecast, MMM) declare their extra deps explicitly and pip-install on first use. Never assume those libraries are pre-installed.

## Visual output
- Anything that draws **must** go through `lib/visualize.py` and pull style from `lib/styles/*.yaml`.
- Skills must not hand-roll matplotlib rcParams. Custom skill-specific tweaks are fine, but they extend the shared style rather than replacing it.
- Three bundled styles: `default`, `executive`, `custom`. The Style picker skill is the canonical UI for choosing/customising; other skills read the active style and just render.
- Output is meant to be screenshot-worthy and copy-pasteable into a deck without further work.

## Data input (v1)
- Files only — CSV, Excel, pasted data.
- Database access is deferred. README documents the warehouse MCP workaround for users who already have one connected.

## Versioning
- Semver. 0.x = pre-stable. 1.0.0 = full 25-skill pack shipped and polished.
- `plugin.json` `version` and `CHANGELOG.md` must move together — divergence is a common marketplace rejection cause.

## Distribution prep
- Every release: update `CHANGELOG.md`, bump `plugin.json` version, tag the commit `v{version}`.
- Screenshots for the README + marketplace submission come from real skill runs, not mockups.
- Marketplace submission lives on the critical path — leave time for review cycles.

## Sub-tickets
- Each of the 7 clusters can spawn its own Linear sub-ticket under URB-182 if the build runs long. Default: track via the checklist in URB-182.
