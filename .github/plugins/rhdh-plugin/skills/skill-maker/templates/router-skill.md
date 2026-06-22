---
name: SKILL_NAME
description: |
  What the skill does broadly. Use when [trigger phrases for any sub-command].
  Also use when [edge phrasings, related terms].
---

# SKILL_TITLE

Brief statement of the skill's domain and purpose.

## Essential Principles

Rules that apply to ALL commands. Keep this section short — it's always loaded.

- Principle with reasoning
- Another principle — explain why

## Commands

| Command | Description | Reference |
|---|---|---|
| `command-a [args]` | What it does | [references/command-a.md](references/command-a.md) |
| `command-b [args]` | What it does | [references/command-b.md](references/command-b.md) |

## Routing Rules

1. **No argument**: Show the command table. Ask what the user wants to do.
2. **First word matches a command**: Load its reference file and follow it.
3. **First word doesn't match**: Treat the full input as context for the most likely command. State which command you chose and why.

## Setup (if applicable)

| Gate | Required check | If fail |
|---|---|---|
| Context | Project config loaded | Run the loader first |
| Command | Sub-command reference is loaded | Load the reference |

## References

- `references/command-a.md` — loaded when running command-a
- `references/command-b.md` — loaded when running command-b
- `references/shared-patterns.md` — loaded when [specific condition]
