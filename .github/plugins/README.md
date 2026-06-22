# GitHub Copilot Plugin Source Packages

This folder stores source packages that were originally authored as agent skill or source plugin distributions. GitHub Copilot does not load `.source-plugin/` manifests directly. In this repository, the runtime surface for GitHub Copilot is the native primitive set under `.github/`.

## Runtime Mapping

| Source package element | GitHub Copilot primitive |
| --- | --- |
| `.source-plugin/plugin.json` | Provenance only. Not loaded by GitHub Copilot. |
| `skills/<name>/SKILL.md` | `.github/skills/<name>/SKILL.md` |
| `agents/*.md` | `.github/agents/*.agent.md` |
| `commands/*.md` | `.github/prompts/*.prompt.md` |
| Agent-specific bootstrap files | `.github/copilot-instructions.md` or `.github/instructions/*.instructions.md` |
| Workspace permission examples | Path-scoped instructions and explicit prompt rules. |

## Current Conversions

| Source package | GitHub Copilot-native output |
| --- | --- |
| `rhdh-plugin/skills/*` | `rhdh`, `rhdh-local`, `rhdh-jira`, `create-plugin`, and `overlay` skills under `.github/skills/` |
| `code-modernization-plugin/agents/*` | Five modernization agents under `.github/agents/` |
| `code-modernization-plugin/commands/*` | Seven `/modernize-*` prompts under `.github/prompts/` |
| `code-modernization-plugin` folder rules | `.github/instructions/code-modernization.instructions.md` |

## Conversion Rules

- Treat this folder as import source, not as the GitHub Copilot runtime surface.
- Keep converted primitives under `.github/agents/`, `.github/prompts/`, `.github/skills/`, and `.github/instructions/`.
- Add provenance metadata to adapted primitives when content came from an external package.
- Remove plugins source-only metadata such as `tool allow-list metadata`, plugin source tool names, `plugin installation command`, and `source workspace settings` permissions.
- Replace permission examples with explicit GitHub Copilot instructions, for example `legacy/**` is read-only unless the user explicitly asks to edit it.
- Run repository validation after conversion.

## Validation

```bash
bash .github/scripts/audit-primitives.sh
bash .github/scripts/audit-skills.sh
bash .github/scripts/audit-external-content.sh
bash .github/scripts/generate-llms-txt.sh --check
```

For new prompts, agents, skills, or instructions, also check that the relevant `.gitignore` exception exists so the file is versioned.
