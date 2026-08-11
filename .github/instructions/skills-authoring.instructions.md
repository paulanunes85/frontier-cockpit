---
description: "Authoring conventions for GitHub Copilot agent skills in this repository: frontmatter, structure, portability, and progressive disclosure."
applyTo: ".github/skills/**"
---

# Skill Authoring Conventions

These rules apply to every skill under `.github/skills/`. They encode the defects found in past audits so they do not recur.

## Folder and file layout

- One folder per skill: `.github/skills/<name>/`. The folder name must equal the `name` in `SKILL.md` frontmatter (lowercase, hyphenated).
- Every skill has a `SKILL.md` at its root.
- Bundle supporting material in subfolders: `references/` (Markdown the agent reads on demand), `assets/` (templates, HTML, images), `scripts/` (runnable helpers).

## Frontmatter (required)

- `SKILL.md` must start with YAML frontmatter on **line 1**. No blank line, BOM, or stray token before the opening `---`. (A leading line breaks loading silently.)
- Required keys: `name` (matches the folder) and `description`.
- `description` is the discovery surface. State **what** the skill does and **when** to use it, with concrete trigger keywords. Keep it within 1024 characters.
- Do not use platform-specific frontmatter keys such as `allowed-tools`. Optional supported keys include `argument-hint`, `license`, `user-invocable`, `disable-model-invocation`.

## Portability (no platform leaks)

- No sandbox paths: never reference hardcoded agent home folders, mounted skill folders, or mounted user-data folders. Use workspace-relative paths such as `output/` and `input/`.
- No platform-specific product framing as a hard dependency. Describe the portable artifact instead (for example "self-contained HTML file").
- Use portable tooling in examples (for example `soffice` for LibreOffice conversions), not internal wrapper scripts.
- AI model names and cited benchmarks are legitimate content and may stay; this rule targets platform mechanics, not factual references.

## Progressive disclosure

- Keep `SKILL.md` focused: an overview, when-to-use, the core workflow, and pointers. Push depth into `references/` files.
- Every file path referenced in `SKILL.md` must exist in the skill. No dangling references.
- Helper scripts must run with the interpreters available in the environment and should be self-contained (prefer standard library).

## Content rules

- Documentation is in English. Write "GitHub Copilot", never "Copilot" alone.
- No em dashes; use commas, parentheses, or restructure.
- Never fabricate metrics, benchmarks, or prices. Cite a source or mark the value as an assumption.

## Before considering a skill done

1. Frontmatter parses and the skill appears in the available-skills list.
2. The folder name matches `name`.
3. No sandbox paths or hard platform dependencies remain.
4. Every referenced file exists; every bundled script runs.
