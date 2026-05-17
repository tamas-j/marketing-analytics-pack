# Build conventions

Rules of the road for the Marketing Analytics Pack codebase. Future turns: follow these unless URB-182 explicitly overrides.

## Commands vs skills — separate peer directories
Following the financial-services pattern (`plugins/vertical-plugins/financial-analysis/`):

- **`commands/<name>.md`** — slash commands the user explicitly invokes (`/kpi-tree`, `/style`, `/forecast`). One markdown file per command. **No subdirectory.** Frontmatter has `description` + `argument-hint`. **No `name:` field — the filename is the command name.** Most of our 25 entries live here.
- **`skills/<name>/SKILL.md`** — composable knowledge units. One folder per skill. Optional `references/` (static support files — templates, examples, dialect notes — the `data-context-extractor` pattern) and `scripts/` (Python the skill runs — the advanced-runner pattern) subfolders.
- **Commands compose skills.** A command's workflow calls `Use skill: "<name>"` to pull in shared knowledge (chart patterns, statistical methods, forecast comparisons, etc.). One command can pull in several skills.
- **Cross-plugin invocation:** `/<plugin-name>:<command>` — so `/marketing-analytics-pack:kpi-tree` when called from outside the plugin. Bare `/kpi-tree` works from inside the user's loaded session.
- **Naming:** lowercase, hyphenated (`kpi-tree.md`, `mmm-readiness.md`, `forecast-methods/`). For skills, the directory name must match the `name` field in `SKILL.md` frontmatter. For commands, the filename IS the name.

## Frontmatter
- **Commands** (`commands/<name>.md`): `description` + `argument-hint`. No `name`.
- **Model-invoked skills** (`skills/<name>/SKILL.md`): `description` with "Use when…" trigger language. Add `user-invocable: false` for pure model-only.
- **Multi-mode skills**: `description: >` block scalar with explicit "MODE A Triggers: …" / "MODE B Triggers: …" sections (the `data-context-extractor` pattern).
- `description` is 10–2000 chars, no leading/trailing whitespace, no hidden Unicode (marketplace invariants I3, I10).
- Names match `^[a-z0-9][a-z0-9-]{1,63}$` (invariant I11).

## Manifest
- Path: `.claude-plugin/plugin.json`. **Not** `plugin.json` at the repo root.
- Schema: exactly 4 fields — `name`, `version`, `description`, `author`. Don't add `keywords`, `categories`, `homepage`, `repository`, `bugs`, `license`, or a `skills` array. License is conveyed via the top-level `LICENSE` file; the rest aren't part of the schema and `claude plugin validate` may complain.

## Dependencies
- **Core skills** assume only the standard pack runtime (which includes matplotlib). Do **not** import pandas, scikit, Prophet, Meridian, etc. in a core skill.
- **Advanced runners** (RFM, Forecast, MMM) declare their extra deps explicitly and pip-install on first use. Never assume those libraries are pre-installed.

## Visual output
- Three-layer model (revised v0.1.1, after auditing Anthropic's `knowledge-work-plugins/data`):
  1. **Chart code patterns** live in the `data-visualization` reference skill (`skills/data-visualization/SKILL.md`). Skills don't `import` — Claude copies these patterns into generated Python at runtime. Patterns include line, bar, histogram, heatmap, small multiples, plus number-formatting helpers. The skill is `user-invocable: false`.
  2. **Brand / palette / typography config** lives in `lib/styles/*.yaml`. Three bundled styles: `default`, `executive`, `custom`. Each carries optional `brand: { primary_hex, logo_path, font_family }` slots.
  3. **A thin `lib/visualize.py` helper** reads the active style YAML and exposes a small palette/typography API. Not an import target for chart code — just a config reader.
- Skills must not hand-roll style or invent rcParams. Pull from the active YAML; copy patterns from the reference skill.
- The Style picker skill is the canonical UI for choosing/customising; writes `lib/styles/custom.yaml`.
- Output is meant to be screenshot-worthy and copy-pasteable into a deck without further work.

## Data input (v1)
- Files only — CSV, Excel, pasted data.
- Database access is deferred. README documents the warehouse MCP workaround for users who already have one connected.

## Versioning
- Semver. 0.x = pre-stable. 1.0.0 = full 25-skill pack shipped and polished.
- `.claude-plugin/plugin.json` `version` and `CHANGELOG.md` must move together — divergence is a common marketplace rejection cause.

## Validation before push
- Run `scripts/validate.py` (when it exists): JSON-loads the manifest, YAML-loads every `lib/styles/*.yaml`, walks every `SKILL.md` to confirm frontmatter has required fields and `description` is within 10–2000 chars with no leading/trailing whitespace or hidden Unicode.
- If `claude` CLI is installed: `claude plugin validate .` as the canonical check.

## Distribution prep
- Every release: update `CHANGELOG.md`, bump `.claude-plugin/plugin.json` version, tag the commit `v{version}`.
- Screenshots for the README + marketplace submission come from real skill runs, not mockups.
- Marketplace submission lives on the critical path — leave time for review cycles.

## Sub-tickets
- Each of the 7 clusters can spawn its own Linear sub-ticket under URB-182 if the build runs long. Default: track via the checklist in URB-182.
