---
name: suggest-awesome-github-copilot-prompts
description: "Suggest relevant GitHub Copilot prompt files from github/awesome-copilot for this repository. Use when comparing HQ prompt files with the Awesome GitHub Copilot catalog, identifying missing slash-command workflows, avoiding duplicate prompts, or planning a curated prompt import. Produces recommendations only and never installs automatically."
argument-hint: "the prompt workflow to compare, for example import governance, issue planning, or app verification"
source: "github/awesome-copilot"
source_url: "https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-prompts"
license: "MIT"
imported_date: "2026-06-17"
last_sync: "2026-06-17"
---

# Suggest Awesome GitHub Copilot Prompts

Use this skill to compare the HQ repository's local prompt files with the public Awesome GitHub Copilot prompt catalog and produce a curated recommendation set.

## When To Use

Use this skill when the user asks to:

- Compare local prompts with Awesome GitHub Copilot.
- Find missing repeatable workflows for the HQ repository.
- Identify prompt overlap or duplication.
- Plan a safe adapted prompt import.
- Refresh a prompt while preserving HQ conventions.

## Workflow

1. Inventory local prompts in `.github/prompts/*.prompt.md`.
2. Read the public catalog from `https://awesome-copilot.github.com/llms.txt` or the Awesome GitHub Copilot repository when web access is available.
3. Compare prompts by trigger, workflow, output contract, required skills, and validation gates.
4. Group recommendations as `adopt`, `adapt`, `defer`, or `reject`.
5. Favor prompts that support HQ governance, primitive audits, external intake, `llms.txt`, rendering verification, and metrics analysis.
6. Do not install, copy, overwrite, or delete anything unless the user explicitly asks for implementation.

## Recommendation Criteria

| Decision | Meaning |
| --- | --- |
| `adopt` | The prompt fills a clear HQ gap and can be added with minimal rewriting. |
| `adapt` | The workflow is useful, but it must be rewritten to match HQ prompt conventions. |
| `defer` | The prompt may be useful later, but it is not needed now. |
| `reject` | The prompt duplicates a stronger HQ prompt or conflicts with policy. |

## HQ Prompt Rules

Every prompt must include `agent`, `argument-hint`, a clear `Output concisely:` contract, and `## First step, always` when it loads a skill.

## Output

Return a concise table with: candidate, source URL, decision, rationale, local overlap, expected files, and validation gates.
