# Domain Docs

How the engineering skills should consume this repo's domain documentation.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — domain language for the RHDH skill project
- **`docs/adr/`** — read ADRs that touch the area you're about to work in

If any of these files don't exist, proceed silently. Don't flag their absence.

## File structure

Single-context repo:

```
/
├── CONTEXT.md
└── docs/adr/
    ├── 0001-agent-assisted-workflows-over-ci-automation.md
    ├── 0002-stdlib-only-python-clis.md
    ├── 0003-orchestrator-plus-sub-skills.md
    └── 0004-agent-skills-open-standard.md
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill-with-docs`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0002 (stdlib-only Python CLIs) — but worth reopening because…_
