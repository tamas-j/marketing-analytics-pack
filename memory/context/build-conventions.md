# Build conventions

Rules of the road for the Marketing Analytics Pack codebase. Future
turns: follow these unless URB-182 explicitly overrides.

## Commands vs skills — separate peer directories

Following the financial-services pattern
(`plugins/vertical-plugins/financial-analysis/`):

- **`commands/<name>.md`** — slash commands the user explicitly invokes
  (`/kpi-tree`, `/style`, `/forecast`). One markdown file per command.
  No subdirectory. Frontmatter has `description` + `argument-hint`.
  No `name:` field — the filename is the command name. All 27
  user-invocable entries live here.
- **`skills/<name>/SKILL.md`** — composable knowledge units. One folder
  per skill. Optional `references/` (static support files — templates,
  examples, dialect notes — the `data-context-extractor` pattern) and
  `scripts/` (Python the skill runs — the advanced-runner pattern)
  subfolders.
- **Commands compose skills.** A command's workflow calls
  `Use skill: "<name>"` to pull in shared knowledge (chart patterns,
  statistical methods, forecast comparisons, etc.). One command can
  pull in several skills.
- **Cross-plugin invocation:** `/<plugin-name>:<command>` — so
  `/marketing-analytics-pack:kpi-tree` when called from outside the
  plugin. Bare `/kpi-tree` works from inside the user's loaded session.
- **Naming:** lowercase, hyphenated (`kpi-tree.md`, `mmm-readiness.md`,
  `forecast-method-selector/`). For skills, the directory name must
  match the `name` field in `SKILL.md` frontmatter. For commands, the
  filename IS the name.

## Frontmatter

- **Commands** (`commands/<name>.md`): `description` + `argument-hint`.
  No `name` field.
- **Model-invoked skills** (`skills/<name>/SKILL.md`): `description`
  with "Use when…" trigger language. Add `user-invocable: false` for
  pure model-only reference skills.
- **Multi-mode skills**: `description: >` block scalar with explicit
  "MODE A Triggers: … / MODE B Triggers: …" sections (the
  `data-context-extractor` pattern).
- `description` is 10–2000 chars, no leading/trailing whitespace, no
  hidden Unicode (marketplace invariants I3, I10).
- Names match `^[a-z0-9][a-z0-9-]{1,63}$` (invariant I11).

## Manifest

- Path: `.claude-plugin/plugin.json`. **Not** `plugin.json` at the repo
  root.
- Schema: exactly 4 fields — `name`, `version`, `description`,
  `author`. No `displayName`, `keywords`, `categories`, `repository`,
  `skills`, etc. Common rejection cause if extras leak in.
- `name` matches `^[a-z0-9][a-z0-9-]{1,63}$` (I11).
- `description` is 10–2000 chars, no hidden Unicode (I3, I10).

## Skill body requirements

- A "Required Inputs" section written plainly for a marketing / analytics practitioner (precise about fields, never assuming SQL or Python fluency).
- Method, Output Template, and Guardrails sections are conventional
  but optional.
- Advanced runners explicitly note their dependency expectations and
  whether they execute or just specify. v1 ships them as
  specification-only stubs; treat that as the current floor, not the
  ceiling.

## Visual output

- Skills don't import chart code. Claude copies the matplotlib
  patterns from `skills/data-visualization/SKILL.md` into the Python
  it generates at runtime.
- Brand, palette, and typography come from `lib/styles/*.yaml`, read
  at runtime through `lib/visualize.py`. Never inline colours or fonts
  inside a skill.
- Three bundled styles: `default`, `executive`, `custom`. The `/style`
  command writes only to `custom.yaml`, only in the `brand` block.
- `default.yaml` and `executive.yaml` are read-only templates.

## Dependencies

- Core skills assume the standard pack runtime (matplotlib included).
- Advanced runners (RFM, Forecast/Prophet, MMM/Meridian) declare extra
  dependencies explicitly and pip-install them on first invocation.
  Never assume Prophet / Meridian / scikit-learn / pandas is available
  in a core skill.

## Validation

- Run `python scripts/validate.py` from the repo root before every
  commit and before any release.
- The script enforces invariants I3, I10, I11; the 4-field manifest
  schema; skill dir == name field; command frontmatter shape; style
  YAML structure. PyYAML is optional — a small inline parser is the
  fallback.
- `CHANGELOG.md` must stay in lockstep with `.claude-plugin/plugin.json`
  `version`.

## Releases

- Semver. 0.x = pre-stable.
- Bump to 1.0.0 when the full 27-command pack ships with screenshots,
  sample data, validated marketplace listing, and the advanced runners
  decision resolved.
- Each cluster could spawn a sub-ticket if the build runs long;
  otherwise tracked via the URB-182 checklist.

## File layout reference

```
marketing-analytics-pack/
├── .claude-plugin/plugin.json     # 4-field manifest
├── README.md
├── LICENSE                         # MIT
├── CHANGELOG.md                    # Keep a Changelog
├── CLAUDE.md                       # working memory
├── CONNECTORS.md                   # v2 placeholder
├── commands/                       # slash commands
├── skills/                         # composable knowledge
│   └── <name>/SKILL.md
├── lib/                            # brand/style config + thin reader
│   ├── visualize.py
│   └── styles/                     # default / executive / custom yaml
├── scripts/                        # validate.py and other repo tooling
├── docs/                           # design notes, conventions, contribution guide
├── examples/                       # worked example flows + sample data
└── memory/                         # deep memory (people, projects, context)
```

→ User-facing version of these conventions lives at `docs/conventions.md`.
