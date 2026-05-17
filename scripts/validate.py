#!/usr/bin/env python3
"""Manifest + frontmatter + style-YAML linter for marketing-analytics-pack.

Checks the marketplace invariants the pack commits to:

* I3  — every `description` is 10–2000 chars, no leading/trailing whitespace
* I10 — no hidden Unicode (zero-width, bidi) in any name or description
* I11 — every name matches ^[a-z0-9][a-z0-9-]{1,63}$
* Plus pack-specific rules:
  - .claude-plugin/plugin.json loads as JSON with exactly the 4 allowed fields
  - commands/*.md have description + argument-hint, NO `name:` field, command
    name = filename
  - skills/<dir>/SKILL.md has name = directory name, description with
    "Use when" trigger language, optional user-invocable boolean
  - lib/styles/*.yaml load and contain expected top-level keys

Run from the repo root:

    python scripts/validate.py

Exit code is 0 on success, 1 on any failure. Findings are printed as
`path:line: severity: message`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_MANIFEST_FIELDS = {"name", "version", "description", "author"}
ALLOWED_SKILL_FIELDS = {"name", "description", "user-invocable"}
ALLOWED_COMMAND_FIELDS = {"description", "argument-hint"}
ALLOWED_STYLE_KEYS = {"name", "description", "brand", "chart", "palette", "typography", "layout"}

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
HIDDEN_UNICODE_RE = re.compile(
    "["  # zero-width and bidi controls that frequently sneak into copied descriptions
    "​-‏"
    "‪-‮"
    "⁠-⁤"
    "﻿"
    "]"
)

EXIT_FAIL = 1


class Findings:
    def __init__(self) -> None:
        self.items: list[tuple[Path, int, str, str]] = []

    def error(self, path: Path, message: str, line: int = 0) -> None:
        self.items.append((path, line, "error", message))

    def warn(self, path: Path, message: str, line: int = 0) -> None:
        self.items.append((path, line, "warning", message))

    def print(self) -> None:
        for path, line, sev, msg in self.items:
            rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
            loc = f"{rel}:{line}" if line else str(rel)
            print(f"{loc}: {sev}: {msg}")

    @property
    def has_errors(self) -> bool:
        return any(sev == "error" for _, _, sev, _ in self.items)


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, int]:
    """Return (frontmatter_dict, body_start_line) or (None, 0) if absent."""
    if not text.startswith("---"):
        return None, 0
    end = text.find("\n---", 4)
    if end == -1:
        return None, 0
    block = text[4:end]
    data: dict[str, str] = {}
    current: str | None = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]*:", line):
            key, _, value = line.partition(":")
            value = value.strip().strip('"').strip("'")
            data[key.strip()] = value
            current = key.strip()
        elif current and line.startswith(" "):
            data[current] = (data[current] + " " + line.strip()).strip()
    body_line = text[: end + 4].count("\n") + 2
    return data, body_line


def check_description(value: str, path: Path, findings: Findings) -> None:
    if value != value.strip():
        findings.error(path, "description has leading/trailing whitespace (I3)")
    if len(value) < 10 or len(value) > 2000:
        findings.error(path, f"description length {len(value)} outside 10-2000 (I3)")
    if HIDDEN_UNICODE_RE.search(value):
        findings.error(path, "description contains hidden Unicode (I10)")


def check_name(name: str, path: Path, findings: Findings) -> None:
    if not NAME_RE.match(name):
        findings.error(path, f"name {name!r} fails ^[a-z0-9][a-z0-9-]{{1,63}}$ (I11)")
    if HIDDEN_UNICODE_RE.search(name):
        findings.error(path, "name contains hidden Unicode (I10)")


def lint_manifest(findings: Findings) -> None:
    path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not path.exists():
        findings.error(path, "manifest missing")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.error(path, f"invalid JSON: {exc}")
        return
    if not isinstance(data, dict):
        findings.error(path, "manifest must be a JSON object")
        return
    extra = set(data) - ALLOWED_MANIFEST_FIELDS
    missing = ALLOWED_MANIFEST_FIELDS - set(data)
    for field in sorted(extra):
        findings.error(path, f"unexpected manifest field {field!r}")
    for field in sorted(missing):
        findings.error(path, f"missing manifest field {field!r}")
    if isinstance(data.get("name"), str):
        check_name(data["name"], path, findings)
    if isinstance(data.get("description"), str):
        check_description(data["description"], path, findings)


def lint_commands(findings: Findings) -> None:
    cmd_dir = REPO_ROOT / "commands"
    for f in sorted(cmd_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if fm is None:
            findings.error(f, "missing frontmatter")
            continue
        keys = set(fm)
        if "name" in keys:
            findings.error(f, "commands must not declare a `name:` field (filename is the name)")
        for required in ("description", "argument-hint"):
            if required not in keys:
                findings.error(f, f"missing required frontmatter field {required!r}")
        extra = keys - ALLOWED_COMMAND_FIELDS - {"name"}
        for field in sorted(extra):
            findings.warn(f, f"unexpected command frontmatter field {field!r}")
        if "description" in fm:
            check_description(fm["description"], f, findings)
        check_name(f.stem, f, findings)


def lint_skills(findings: Findings) -> None:
    skills_dir = REPO_ROOT / "skills"
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        sf = d / "SKILL.md"
        if not sf.exists():
            findings.error(d, "skill folder missing SKILL.md")
            continue
        text = sf.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(text)
        if fm is None:
            findings.error(sf, "missing frontmatter")
            continue
        keys = set(fm)
        for required in ("name", "description"):
            if required not in keys:
                findings.error(sf, f"missing required frontmatter field {required!r}")
        extra = keys - ALLOWED_SKILL_FIELDS
        for field in sorted(extra):
            findings.warn(sf, f"unexpected skill frontmatter field {field!r}")
        if fm.get("name") and fm["name"] != d.name:
            findings.error(
                sf, f"frontmatter name {fm['name']!r} != directory name {d.name!r}"
            )
        if "description" in fm:
            check_description(fm["description"], sf, findings)
            if not fm["description"].lower().startswith("use when"):
                findings.warn(
                    sf,
                    "skill description should start with 'Use when' trigger language",
                )
        check_name(d.name, sf, findings)
        if "user-invocable" in fm and fm["user-invocable"].lower() not in {"true", "false"}:
            findings.error(sf, "user-invocable must be true or false")
        # Required-inputs section
        body = text.split("---", 2)[-1]
        if not re.search(r"(?im)^#+\s*required\s+inputs", body):
            findings.warn(sf, "skill body missing 'Required Inputs' section")


def lint_styles(findings: Findings) -> None:
    style_dir = REPO_ROOT / "lib" / "styles"
    for f in sorted(style_dir.glob("*.yaml")):
        try:
            data = _load_yaml(f)
        except Exception as exc:
            findings.error(f, f"YAML failed to parse: {exc}")
            continue
        if not isinstance(data, dict):
            findings.error(f, "style file must be a YAML mapping at the top level")
            continue
        unknown = set(data) - ALLOWED_STYLE_KEYS
        for key in sorted(unknown):
            findings.warn(f, f"unexpected style key {key!r}")
        for required in ("name", "chart", "palette", "typography", "layout"):
            if required not in data:
                findings.error(f, f"missing required style key {required!r}")


def _load_yaml(path: Path) -> Any:
    """Use PyYAML if present, else fall back to a small literal-friendly parser."""
    try:
        import yaml  # type: ignore

        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except ModuleNotFoundError:
        return _load_simple_yaml(path.read_text(encoding="utf-8"))


def _load_simple_yaml(text: str) -> Any:
    # Tiny parser sufficient for our flat configs; matches lib/visualize.py.
    root: dict[str, Any] = {}
    current_key: str | None = None
    nested_key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0:
            key, _, value = line.partition(":")
            current_key = key.strip()
            nested_key = None
            root[current_key] = {} if not value.strip() else _scalar(value.strip())
        else:
            if current_key is None:
                raise ValueError("nested value before top-level key")
            container = root.setdefault(current_key, {})
            if not isinstance(container, dict):
                raise ValueError(f"can't nest under scalar key {current_key}")
            if line.startswith("- "):
                if nested_key is None:
                    raise ValueError("list item before list key")
                target = container.setdefault(nested_key, [])
                target.append(_scalar(line[2:].strip()))
            else:
                key, _, value = line.partition(":")
                key = key.strip()
                if not value.strip():
                    container[key] = []
                    nested_key = key
                else:
                    container[key] = _scalar(value.strip())
                    nested_key = key
    return root


def _scalar(value: str) -> Any:
    value = value.strip()
    if value in {"''", '""'}:
        return ""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def main(argv: Iterable[str]) -> int:
    findings = Findings()
    lint_manifest(findings)
    lint_commands(findings)
    lint_skills(findings)
    lint_styles(findings)
    findings.print()
    if findings.has_errors:
        print(f"\nvalidate.py: {sum(1 for _, _, s, _ in findings.items if s == 'error')} error(s)")
        return EXIT_FAIL
    warnings = sum(1 for _, _, s, _ in findings.items if s == "warning")
    if warnings:
        print(f"\nvalidate.py: {warnings} warning(s); no errors")
    else:
        print("\nvalidate.py: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
