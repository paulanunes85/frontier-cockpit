---
description: "Conventions for client case folders: structure, audited data integrity, and how to seed a new client from the template."
applyTo: "gh-btg/**,gh-bb/**,gh-bradesco/**,gh-caixa/**,gh-petrobras/**,gh-serpro/**,gh-contoso-template/**"
---

# Client Case Conventions

These rules apply to per-client transition packages and the Contoso template.

## Structure

A complete client case (model: `gh-btg/`) contains:

- A control center **app** (React/Vite) and/or
- A **deliverables package** (executive deck, business case, control center HTML, transition kit workbook, audited billing, consolidated data source) plus a `CONTEXT.md` capturing decisions and canonical numbers.
- A `README.md` describing the case, its status, and how to run any app.

Placeholder client folders contain only a `README.md` marked **Planned** until work begins.

## Data integrity (non-negotiable)

- All financial, billing, usage, seat, and ROI numbers are **audited**. Never invent, estimate, round differently, or alter canonical values.
- The single source of truth for a client's numbers is that client's `CONTEXT.md` and audited workbooks. Pull from there and cite it.
- If a number is not available, mark it as an explicit assumption or omit it. Do not fill gaps with guesses.
- Treat files in the deliverables package as audited outputs. Update `CONTEXT.md` when context changes, but do not silently rewrite figures.

## Seeding a new client

1. Start from the brand-safe deliverables in `gh-contoso-template/`.
2. Mirror the reference structure in `gh-btg/`.
3. Replace placeholder branding and numbers with the client's audited data.
4. Keep `gh-contoso-template/` anonymized; never copy real client numbers into it.

## Copy rules

- Write "GitHub Copilot", never "Copilot" alone.
- Documentation (`.md`, README, `CONTEXT.md`) is in English; app UI copy is trilingual EN / PT-BR / ES.
- No em dashes in user-facing copy.
