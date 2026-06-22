# Contributing

This repository is Frontier Cockpit Team's central hub for GitHub Copilot agents, skills, prompts, instructions, validation scripts, and reusable content assets.

## Contribution Principles

1. Follow the repository guidance in [copilot-instructions.md](copilot-instructions.md).
2. Keep documentation in English.
3. Write "GitHub Copilot" in full.
4. Do not fabricate metrics, prices, benchmarks, or client data.
5. Keep generated documents in the correct type folder.
6. Validate changes before considering them complete.

## Primitive Changes

| Primitive | Required location | Validation |
| --- | --- | --- |
| Agent | `.github/agents/*.agent.md` | `bash .github/scripts/audit-primitives.sh` |
| Skill | `.github/skills/<name>/SKILL.md` | `bash .github/scripts/audit-skills.sh` |
| Prompt | `.github/prompts/*.prompt.md` | `bash .github/scripts/audit-primitives.sh` |
| Instruction | `.github/instructions/*.instructions.md` | `bash .github/scripts/audit-primitives.sh` |

## External Imports

When importing or adapting content from `github/awesome-copilot` or another external source, add source metadata to the frontmatter when the target format supports it:

```yaml
source: "github/awesome-copilot"
source_url: "https://github.com/github/awesome-copilot/..."
license: "MIT"
imported_date: "2026-06-17"
last_sync: "2026-06-17"
```

External content must be reviewed for:

- License compatibility.
- Hardcoded secrets or credentials.
- Absolute paths and platform-specific assumptions.
- Shell injection or unsafe workflow patterns.
- Tool dependencies that are not documented.
- Bare "Copilot" usage where "GitHub Copilot" is required.
- Em dashes in repository-authored Markdown or UI copy.

## Validation

Run the full local validation set:

```bash
bash .github/scripts/audit-primitives.sh
bash .github/scripts/audit-skills.sh
bash .github/scripts/audit-external-content.sh
bash .github/scripts/validate-deliverables.sh
bash .github/scripts/generate-llms-txt.sh --check
```

## References

- [Root README](../README.md)
- [Document organization rules](instructions/document-organization.instructions.md)
- [Documentation standards](instructions/documentation.instructions.md)
- [Skill authoring conventions](instructions/skills-authoring.instructions.md)
