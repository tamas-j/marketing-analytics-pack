# Contributing to Marketing Analytics Pack

Thanks for the interest. This pack is opinionated about shape — commands, skills, and runners follow conventions that the validator enforces. The fastest path in is to copy an existing example.

## Dev setup

```bash
git clone https://github.com/tamas-j/marketing-analytics-pack
cd marketing-analytics-pack

# Optional: virtual environment (required for the advanced runners if your
# Python is PEP 668-managed — Ubuntu 23+ / Debian 12+).
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
.venv\Scripts\activate             # Windows PowerShell
```

No build step — the pack is markdown + Python scripts. Most contributions only need a text editor.

## Before every push

```bash
python scripts/validate.py
```

The validator enforces:

- `.claude-plugin/plugin.json` loads as JSON and contains exactly 4 fields (`name`, `version`, `description`, `author`).
- Every `commands/*.md` has `description` + `argument-hint` in its frontmatter and **no** `name:` field (filename is the command name).
- Every `skills/<dir>/SKILL.md` has `name` matching the directory, a `description` that starts with "Use when…" trigger language, and a `Required Inputs` section in the body.
- All names match `^[a-z0-9][a-z0-9-]{1,63}$` (marketplace invariant I11).
- No hidden Unicode in any name or description (I10).
- All `description` fields are 10–2000 chars with no leading / trailing whitespace (I3).
- Every `lib/styles/*.yaml` parses and has the required top-level keys.

CI runs the same script on every PR; failures block merge.

## Adding a new command + skill pair

Most additions are a slash command backed by a skill. The convention:

1. **Skill** — `skills/<kebab-name>/SKILL.md`:
   ```yaml
   ---
   name: kebab-name
   description: Use when <trigger language describing the situation>.
   ---
   ```
   Folder name **must** match the `name:` field. Body should have:
   - A `## Required Inputs` section (the validator warns if it's missing).
   - The method / framework / output template the command pulls in.
   - A `## Guardrails` section listing things Claude should refuse to do.

2. **Command** — `commands/<kebab-name>.md`:
   ```yaml
   ---
   description: <One-line task description.>
   argument-hint: "<what the user types after the command>"
   ---
   ```
   No `name:` field — the filename **is** the command name. Body should:
   - Open with `Use skill: "<skill-name>"` lines (one per skill the command pulls in).
   - Walk through the workflow as a numbered list.
   - Show output format and an example.
   - Close with `## Guardrails`.

3. **Worked example** — `examples/<command-name>-example.md`:
   - A real prompt and expected output.
   - References sample data from `examples/data/` where applicable.

4. **Validate + smoke** — run `python scripts/validate.py`, then load the plugin in Claude Code or Cowork and test the command end-to-end.

## Adding a new advanced runner

Advanced runners ship an executable Python script that Claude invokes via Bash. The pattern (see `skills/forecast-runner/`, `skills/mmm-runner/`, `skills/rfm-segment-generator/` for working examples):

1. **`skills/<name>/scripts/requirements.txt`** — pinned dependencies.
2. **`skills/<name>/scripts/run_<name>.py`** — CLI entry point. Must include:
   - PEP 668-aware `_install_deps()` that tries plain pip → falls back to `--user` → bails with a `python3 -m venv` message.
   - `--auto-install` flag so the script can install its own deps on first use.
   - Style loading from `lib/visualize.py` so output matches the pack's brand.
   - Outputs in a `--output-dir` (CSV + PNG + `summary.md`).
3. **SKILL.md** — add an `## Execution Mode Availability` table noting which Claude surfaces support the runner (Claude Code + Cowork yes; pure web chat no, fall back to spec mode).
4. **Command** — add an Execution workflow alongside the existing Spec workflow.
5. **Smoke test** against sample data in `examples/data/` and capture the output for the README.

## Style system

Don't hand-roll chart styling. Three layers:

- **Chart code patterns** in `skills/data-visualization/SKILL.md` — copy these into generated Python at runtime.
- **Brand / palette / typography** in `lib/styles/{default,executive,custom}.yaml`.
- **Reader** in `lib/visualize.py` — exposes `load_style`, `palette`, `chart_tokens`, `typography`, `layout`, `matplotlib_rc_params`.

Bundled styles are `default` (clean, balanced) and `executive` (restrained, boardroom). User-customised brand goes in `custom.yaml`, written by the `/style` front-door command.

## Conventions

- **Names** — lowercase, hyphens. No underscores, no camelCase.
- **Markdown** — backticks for inline code, fenced blocks for examples.
- **Descriptions** — start with "Use when…" for skills; one-line task descriptions for commands.
- **Sample data** — small, synthetic, fixed-seed. Keep `examples/data/` files under a few hundred rows so they load instantly.
- **Versioning** — semver. Patch for fixes, minor for new commands or runners, major for breaking conventions changes.
- **CHANGELOG** — keep [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format. CHANGELOG entries must land in the same PR as the change (the validator doesn't enforce this, but reviewers will).

## Pull requests

- Open against `main`.
- Run `python scripts/validate.py` locally before pushing.
- Include a CHANGELOG entry under `[Unreleased]`.
- Reference any related issue or ticket in the PR description.

Questions or stuck on something? Open an issue rather than guessing — the conventions are stricter than they look, and a quick clarification saves a round-trip.
