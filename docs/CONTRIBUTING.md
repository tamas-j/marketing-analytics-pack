# Contributing

This is a personal portfolio project, but the build is set up so that
anyone (or future-me) can add a command + skill pair without breaking
the marketplace invariants.

## Before you start

Read these in order:

1. `README.md` — what the pack does and how it's installed.
2. `CLAUDE.md` — working memory: target user, architecture, current status.
3. `docs/conventions.md` — repo conventions, frontmatter rules, marketplace invariants.

Then run `python scripts/validate.py` from the repo root. It should
exit zero. If it doesn't, fix the existing findings before adding
anything new.

## Adding a new command + skill

A command is the user-facing slash command; the skill is the
composable knowledge unit it pulls in. Most additions need both.

1. Pick a `kebab-case` name. Same name for the command file and the
   skill folder — that's the convention.
2. Create `commands/<name>.md`. Frontmatter is exactly:
   - `description:` — 10–2000 chars, one sentence, no leading/trailing
     whitespace, no hidden Unicode.
   - `argument-hint: "<placeholder text>"` — the slash command's
     argument summary.
   - No `name:` field. The filename is the name.
3. Create `skills/<name>/SKILL.md`. Frontmatter is exactly:
   - `name: <name>` — must match the folder name.
   - `description:` — 10–2000 chars, starts with "Use when…" trigger
     language so the model picks it up.
   - `user-invocable: false` — only if the skill is purely model-only
     reference material (like `data-visualization`).
4. The skill body must include a `## Required Inputs` section written
   for a non-technical reader.
5. The command body should:
   - Pull in its primary skill via `Use skill: "<name>"`.
   - Pull in `data-readiness-checker` if data is involved.
   - Pull in `data-visualization` if it produces a chart.
6. Add a worked example to `examples/<name>-example.md` using the
   same template as the existing examples.
7. Run `python scripts/validate.py` before committing.

## Style and visual output

Don't hand-roll chart code. Copy the matplotlib patterns from
`skills/data-visualization/SKILL.md` into the Python the command
generates at runtime. Read brand / palette / typography from
`lib/styles/*.yaml` through `lib/visualize.py` — never inline colours
or fonts.

If you need a new chart pattern, add it to the `data-visualization`
SKILL.md rather than to the command that needs it.

## Advanced runners

Three skills are tiered as "advanced runners":
`rfm-segment-generator`, `forecast-runner`, `mmm-runner`. They
currently ship as specification workflows, not executable runners. If
you wire up real execution, place the runtime code under
`skills/<name>/scripts/`, declare the heavier dependencies in the
SKILL body, and update the cluster row in URB-182 to remove the
"spec only in v1" tag.

## Validation

`scripts/validate.py` checks:

- `.claude-plugin/plugin.json` is valid JSON with exactly four fields:
  `name`, `version`, `description`, `author`.
- Every command file has `description` + `argument-hint` and no `name:`.
- Every skill folder has a `SKILL.md` whose `name` matches the folder.
- Every name matches `^[a-z0-9][a-z0-9-]{1,63}$` (I11).
- Every description is 10–2000 chars (I3), no hidden Unicode (I10).
- Every skill body has a `## Required Inputs` section (warning only).
- Every `lib/styles/*.yaml` file loads and has the expected top-level
  keys.

## Pull requests

Open a PR with:

1. The new files.
2. Updated `CHANGELOG.md` under `[Unreleased] → Added`.
3. The `scripts/validate.py` output (should be `OK`).
4. A screenshot of the worked example output, if the command
   produces a chart.

That's it. Keep changes small.
