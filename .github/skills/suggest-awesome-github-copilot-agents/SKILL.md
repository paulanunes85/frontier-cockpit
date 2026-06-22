---
name: suggest-awesome-github-copilot-agents
description: "Suggest relevant GitHub Copilot custom agents from github/awesome-copilot for this repository. Use when comparing HQ agents with the Awesome GitHub Copilot catalog, identifying missing agent personas, avoiding duplicate imports, or reviewing whether a local agent should be refreshed from upstream. Produces recommendations only and never installs automatically."
argument-hint: "the target area to compare, for example security, testing, or onboarding agents"
source: "github/awesome-copilot"
source_url: "https://github.com/github/awesome-copilot/tree/main/skills/suggest-awesome-github-copilot-agents"
license: "MIT"
imported_date: "2026-06-17"
last_sync: "2026-06-17"
---

# Suggest Awesome GitHub Copilot Agents

Use this skill to compare the HQ repository's local custom agents with the public Awesome GitHub Copilot agent catalog and produce a curated recommendation set.

## When To Use

Use this skill when the user asks to:

- Compare local agents with Awesome GitHub Copilot.
- Find missing agent personas for the HQ repository.
- Identify agent overlap or duplication.
- Decide whether to adopt, adapt, defer, or reject an external agent.
- Refresh an agent from upstream without losing HQ-specific conventions.

## Workflow

1. Inventory local agents in `.github/agents/*.agent.md`.
2. Read the public catalog from `https://awesome-copilot.github.com/llms.txt` or the Awesome GitHub Copilot repository when web access is available.
3. Compare by purpose, not only by filename.
4. Group recommendations as `adopt`, `adapt`, `defer`, or `reject`.
5. Prefer adapting agents to the HQ pattern: lean agent, rich companion skill, clear first step, validation gates, and no duplicated domain knowledge.
6. Do not install, copy, overwrite, or delete anything unless the user explicitly asks for implementation.

## Recommendation Criteria

| Decision | Meaning |
| --- | --- |
| `adopt` | The agent fills a clear HQ gap and can be added with minimal adaptation. |
| `adapt` | The concept is useful, but it must be rewritten to fit HQ conventions. |
| `defer` | Useful later, but no current HQ workflow needs it. |
| `reject` | Duplicates existing HQ capability, conflicts with policy, or creates avoidable complexity. |

## HQ Priority Areas

Prioritize agents for security review, DevOps and CI, QA, accessibility, prompt and primitive authoring, onboarding, AI readiness, and repository governance.

## Output

Return a concise table with: candidate, source URL, decision, rationale, overlap with local agents, expected files, and validation gates.
