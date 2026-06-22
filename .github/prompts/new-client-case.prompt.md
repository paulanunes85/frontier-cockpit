---
description: "Scaffold a new GitHub Copilot UBB client case from the Contoso template, following the BTG reference structure."
agent: agent
argument-hint: "client name, target folder, case type, and audited data source"
---

# New Client Case

Scaffold a new GitHub Copilot Usage-Based Billing (UBB) client case in this workspace.

## Inputs

Ask for any that are missing:

- **Client name** and the target folder (convention: `gh-<client>/`).
- Whether the case needs a **control center app** (port from `gh-btg/`), a **deliverables package** (from `gh-contoso-template/`), or both.
- The **audited data source** for the client (workbook or numbers). If none is available yet, scaffold structure only and mark numbers as `TODO (pending audit)`, do not invent values.

## Steps

1. Read [../../gh-btg/README.md](../../gh-btg/README.md) and [../../gh-contoso-template/README.md](../../gh-contoso-template/README.md) to mirror the reference structure.
2. Create the client folder with a `README.md` (purpose, contents, status, how to run, references) in English.
3. If a deliverables package is requested, copy the relevant Contoso template files and replace branding and placeholder numbers with the client's audited data.
4. If an app is requested, port the BTG app parametrized by the client id; reuse the engine, `useDB` hook, grid, i18n, and design system. Do not rewrite them.
5. Add a `CONTEXT.md` capturing decisions and canonical numbers, with a References section.
6. Update the root [../../README.md](../../README.md) inventory table: set the client's status.

## Rules

- Never fabricate metrics. Use only audited data and cite the source.
- Keep `gh-contoso-template/` anonymized; never copy real client numbers into it.
- Documentation in English; app UI copy trilingual EN / PT-BR / ES.
- Write "GitHub Copilot"; no em dashes in UI copy.

## Done when

- The client folder exists with a complete English `README.md`.
- Any copied deliverables and/or ported app build and render without errors.
- The root README inventory reflects the new case.

## Output

Output concisely: return only the created artifact path(s), validation status, and any critical findings or blockers. Do not narrate the process steps.
