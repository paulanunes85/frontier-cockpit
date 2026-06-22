---
description: "Verify a React/Vite app in this workspace by building it and checking that every route renders with zero console errors, plus i18n, dark mode, and grid recompute."
agent: agent
argument-hint: "app folder, for example gh-btg"
---

# Verify App

Verify the React/Vite app in `${input:appFolder:the app folder to verify, for example gh-btg}` against the repository's rendering-based verification standard.

Follow [../instructions/react-apps.instructions.md](../instructions/react-apps.instructions.md). Prefer rendering over reading code: most regressions in this project (i18n leaks, broken references, wrong totals) are caught by rendering.

## Steps

1. Install and build:
   - `cd ${input:appFolder}`
   - `npm install`
   - `npm run build`
   Confirm the build succeeds.
2. Open the build and check every route:
   - For single-file builds, open `dist/index.html` from `file://`; otherwise run `npm run preview`.
   - Visit each route and confirm zero console and page errors.
3. Check the canonical numbers render exactly. For BTG, cross-check against [../../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md](../../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md). Do not alter any audited value.
4. Editable grids: edit one cell, confirm derived values recompute and the dirty badge toggles, then reset and confirm canonical data returns.
5. i18n: switch EN, PT-BR, and ES on sampled routes; confirm no language leaks into another.
6. Dark mode: toggle and confirm styles hold.
7. If the app ports the UBB engine, run the engine check: `node .github/skills/ubb-engine/verify-engine.mjs`.

## Report

List each route with pass or fail, every console error found, and any number that does not match the canonical source. Fix what you can, then rerun the failing checks.

Output concisely: return only the route results, console errors, canonical-number mismatches, files changed, validation status, and any critical blockers. Do not narrate the process steps.
