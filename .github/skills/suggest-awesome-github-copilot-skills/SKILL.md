---
name: suggest-awesome-github-copilot-skills
description: "Suggest relevant GitHub Copilot skills from github/awesome-copilot for this repository. Use when comparing HQ skills with the Awesome GitHub Copilot catalog, finding reusable workflows, avoiding duplicate skills, checking upstream drift, or planning a curated import. Produces recommendations only and never installs automatically."
argument-hint: "the capability area to compare, for example governance, testing, llms.txt, or Playwright"
source: "github/awesome-copilot"
source_url: "https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-skills"
license: "MIT"
imported_date: "2026-06-17"
last_sync: "2026-06-17"
---

# Suggest Awesome GitHub Copilot Skills

Use this skill to compare the HQ repository's local skill library with the public Awesome GitHub Copilot skills catalog and produce a curated intake plan.

## When To Use

Use this skill when the user asks to:

- Compare local skills with Awesome GitHub Copilot.
- Find reusable skill workflows for the HQ repository.
- Identify skill overlap or duplication.
- Review upstream drift for an adapted skill.
- Plan a small, governed import from the public catalog.

## Workflow

1. Inventory local skills under `.github/skills/*/SKILL.md`.
2. Read the public catalog from `https://awesome-copilot.github.com/llms.txt` or the Awesome GitHub Copilot repository when web access is available.
3. Compare skills by trigger, workflow, bundled assets, validation logic, and maintenance burden.
4. Group recommendations as `adopt`, `adapt`, `defer`, or `reject`.
5. Favor skills that improve HQ governance, validation, onboarding, security, AI readiness, metrics, and rendering checks.
6. Do not install, copy, overwrite, or delete anything unless the user explicitly asks for implementation.

## Recommendation Criteria

| Decision | Meaning |
| --- | --- |
| `adopt` | The skill fills a clear HQ gap and can be added with limited rewriting. |
| `adapt` | The skill idea is valuable, but local rewriting is required for HQ conventions. |
| `defer` | The skill may be useful later, but there is no immediate HQ workflow. |
| `reject` | The skill duplicates an HQ skill, conflicts with policy, or adds avoidable bloat. |

## External Import Rules

Imported or adapted skills must keep provenance metadata, pass `audit-skills.sh`, pass `audit-external-content.sh`, and avoid hardcoded sandbox paths or undeclared tool dependencies.

## Output

Return a concise table with: candidate, source URL, decision, rationale, overlap with local skills, expected files, and validation gates.
