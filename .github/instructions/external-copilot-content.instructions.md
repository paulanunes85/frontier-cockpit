---
description: "Rules for importing or adapting external GitHub Copilot agents, skills, prompts, and instructions: provenance metadata, license checks, safe adaptation, and validation gates."
applyTo: ".github/agents/**,.github/skills/**,.github/prompts/**,.github/instructions/**"
---

# External GitHub Copilot Content

Use these rules whenever adding or updating GitHub Copilot primitives from an external source such as `github/awesome-copilot`.

## Import Rules

- Prefer adaptation over blind copying.
- Keep the HQ conventions as the source of truth.
- Add provenance metadata when the file format supports YAML frontmatter: `source`, `source_url`, `license`, `imported_date`, and `last_sync`.
- Do not import content with incompatible licenses unless the repository owner approves it.
- Do not import unreviewed scripts that install packages, invoke network commands, or modify user-level configuration.
- Do not install, overwrite, or delete primitives automatically from a recommendation workflow.

## Quality Rules

- Documentation is in English.
- Write "GitHub Copilot" in full.
- Do not use em dashes.
- Never fabricate metrics, prices, benchmarks, or research claims.
- Remove sandbox paths, hardcoded personal paths, and platform-specific assumptions.
- Document required tools and external services.

## Validation

Run these checks after importing or adapting external content:

```bash
bash .github/scripts/audit-primitives.sh
bash .github/scripts/audit-skills.sh
bash .github/scripts/audit-external-content.sh
bash .github/scripts/generate-llms-txt.sh --check
```
