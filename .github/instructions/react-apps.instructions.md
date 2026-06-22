---
description: "Conventions for the React/Vite client apps and learning sites (engine, persistence, design system, i18n)."
applyTo: "gh-btg/**,gh-ubb-learning-site/**,ubb-platform/**"
---

# React / Vite App Conventions

These rules apply to the React applications in this workspace (the BTG control center, the learning site, and any future `ubb-platform/` or calculator app).

## Stack

- **React 18 + Vite.** Use **TypeScript** for new code; the BTG app is JS and should be ported rather than rewritten when reused.
- **Hash routing** so single-file builds open from `file://`. For an Azure Static Web Apps target, switch to history routing with an SPA fallback (`staticwebapp.config.json`) and `base: '/'`.
- **Single-file build** via `vite-plugin-singlefile` when the artifact must open from the file system.

## Reuse, do not rewrite

The BTG app contains validated building blocks. Port and parametrize them by `clientId`; do not reimplement:

- **Engine** (UBB formulas: pools, overage, FY27 curve, leverage, budgets, maturity, ROI), keep as pure functions; cover with a node assertion script against canonical outputs.
- **`useDB` hook**: `localStorage` persistence + export/import + File System Access save. Namespace keys per client (for example `ubb-${clientId}-${dbName}`).
- **Editable Grid** + toolbar, **i18n** dictionaries and `t()` helper, and the **design system** stylesheet.

## Design system (ms-identity)

- Palette: `#F25022` / `#7FBA00` / `#00A4EF` / `#FFB900` with 50/500/700 ramps; light and dark themes.
- Fonts: **Inter** for text, **JetBrains Mono** for data.
- Sticky header with the 4-square logo; cards with colored top accents; editorial tables.
- **Charts are hand-rolled SVG.** Do not add chart libraries.
- Favicon and icons are **SVG** (inline data-URI favicon preferred).

## i18n

- Trilingual **EN / PT-BR / ES** through the existing `t()` pattern; persist the chosen locale.
- Never let one language leak into another. Sweep all three languages on sampled routes before considering work done.

## Data

- Render audited numbers exactly; never invent or alter canonical values.
- Keep the documented note explaining the small difference between the live FY27 formula and the canonical hand-rounded curve.

## Verification before done

1. `npm run build` succeeds.
2. Every route renders with **zero** console/page errors (check the single-file `dist` from `file://` when applicable).
3. Editing a grid cell recomputes derived values and toggles the dirty badge; reset restores canonical data.
4. All three languages and dark mode work on sampled routes.
