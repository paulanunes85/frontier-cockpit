---
name: suggest-awesome-github-copilot-instructions
description: "Suggest relevant GitHub Copilot instruction files from github/awesome-copilot for this repository. Use when comparing HQ path-scoped instructions with the Awesome GitHub Copilot catalog, identifying missing coding standards, avoiding duplicate instructions, or planning an adapted instruction import. Produces recommendations only and never installs automatically."
argument-hint: "the instruction area to compare, for example security, accessibility, Playwright, or GitHub Actions"
source: "github/awesome-copilot"
source_url: "https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-instructions"
license: "MIT"
imported_date: "2026-06-17"
last_sync: "2026-06-17"
---

# Suggest Awesome GitHub Copilot Instructions

Use this skill to compare the HQ repository's local path-scoped instructions with the public Awesome GitHub Copilot instructions catalog.

## When To Use

Use this skill when the user asks to:

- Compare local instructions with Awesome GitHub Copilot.
- Find missing path-scoped coding standards.
- Identify instruction overlap or duplication.
- Plan a safe adapted instruction import.
- Refresh an instruction while preserving HQ conventions.

## Workflow

1. Inventory local instructions in `.github/instructions/*.instructions.md`.
2. Read the public catalog from `https://awesome-copilot.github.com/llms.txt` or the Awesome GitHub Copilot repository when web access is available.
3. Compare by `applyTo`, domain, quality rule, and likely file ownership.
4. Group recommendations as `adopt`, `adapt`, `defer`, or `reject`.
5. Prioritize instructions for security, accessibility, performance, GitHub Actions, Playwright, MCP security, shell scripting, and external import governance.
6. Do not install, copy, overwrite, or delete anything unless the user explicitly asks for implementation.

## Recommendation Criteria

| Decision | Meaning |
| --- | --- |
| `adopt` | The instruction fills a clear gap and can be added with minimal rewriting. |
| `adapt` | The instruction should be rewritten to fit HQ naming, applyTo, and copy rules. |
| `defer` | The instruction is not needed for current HQ work. |
| `reject` | The instruction duplicates an existing rule or conflicts with HQ policy. |

## HQ Rules

Every instruction must have frontmatter on line 1, `description`, `applyTo`, English documentation, no em dashes, and full "GitHub Copilot" product naming.

## Output

Return a concise table with: candidate, source URL, decision, rationale, local overlap, proposed `applyTo`, and validation gates.
