---
description: "Build the UBB Platform: one React app that is the main site indexing and hosting every workspace folder as a mini-app (client control centers, learning experiences, tools, document packages, and decks), with a central dashboard, client admin, and a GitHub Copilot agent cost calculator. BTG is the first client and the reusable template."
agent: agent
argument-hint: "the phase or platform feature to build, for example Phase 0 scaffold"
---

# Build the UBB Platform

Build `ubb-platform/` at the repository root: a complete React application (Vite, requires a build) that is the **main site** (the single hub) indexing and hosting **every other folder in this workspace as a mini-app or mini-site**. Client control centers are the primary category (BTG is the first client and the reusable template), alongside learning experiences, tools, document packages, and decks.

Before writing any feature code, **map the whole workspace** (see "Workspace map" below and Phase 0): every `gh-*` folder is a mini-app the platform must catalog, surface in navigation, and link to or embed. Treat the platform as the index of indexes.

Follow the repository conventions in [../copilot-instructions.md](../copilot-instructions.md), the React app rules in [../instructions/react-apps.instructions.md](../instructions/react-apps.instructions.md), the client-case rules in [../instructions/client-cases.instructions.md](../instructions/client-cases.instructions.md), and the documentation rules in [../instructions/documentation.instructions.md](../instructions/documentation.instructions.md).

## First step, always

Load the `ms-identity` skill before planning, scaffolding, generating, or editing the platform. Apply its Microsoft-identity design system (the 4-square logo, the Microsoft 4-color palette with 50/500/700 ramps, Inter for body and JetBrains Mono for data, light and dark themes, cards with colored top accents, editorial tables) to the entire platform shell and every page. Author identity is Frontier Cockpit Team, Software Global Black Belt; never use personal social handles.

## Role

You are a senior full-stack engineer. The platform manages GitHub Copilot Usage-Based Billing (UBB) transitions for multiple enterprise clients.

## Context

A complete single-client React app already exists and is validated at [../../gh-btg/](../../gh-btg/) (Vite + React 18, hash routing, single-file build, trilingual EN/PT-BR/ES, dark mode). It contains battle-tested code you must **reuse, not rewrite**:

- `src/engine.js`: UBB formulas
- `src/db.js`: the `useDB` hook (localStorage + export/import + File System Access API)
- `src/components/Grid.jsx`: editable grid
- `src/i18n.js`, `src/content.js`
- `src/styles.css`: the ms-identity design system
- `src/data/db/*.json`: the five per-sheet databases for client BTG

The BTG document package lives at [../../gh-btg/btg-gh-ubb-mini-site/](../../gh-btg/btg-gh-ubb-mini-site/) (deck HTML, business case PDF, kit workbook, audited analysis, consolidated data source, raw billing report, and `CONTEXT.md` with canonical numbers and decisions). **Read `CONTEXT.md` first.**

Why this project exists: the BTG case becomes the template for many clients. Instead of duplicating one site per client, build **one** platform where each client is a data record with its own JSON databases, its own full control center, and a central index that aggregates every client for leadership: cross-client dashboard, comparisons, automations, and a GitHub Copilot agent cost calculator. Beyond clients, the same main site also catalogs and surfaces every other workspace asset (learning experiences, tools, documents, decks), so the platform is the single front door to all of it.

## Workspace map

Every folder at the repository root is a mini-app or mini-site the platform must catalog. Scan the root at build time and reconcile against this reference (folders may be added, so the catalog must be data-driven, not hardcoded):

| Folder | Category | Type | Status |
| --- | --- | --- | --- |
| [../../gh-btg/](../../gh-btg/) | client | React control center + deliverables package | built (reference template) |
| [../../gh-bb/](../../gh-bb/) | client | placeholder | planned |
| [../../gh-bradesco/](../../gh-bradesco/) | client | placeholder | planned |
| [../../gh-caixa/](../../gh-caixa/) | client | placeholder | planned |
| [../../gh-petrobras/](../../gh-petrobras/) | client | placeholder | planned |
| [../../gh-serpro/](../../gh-serpro/) | client | placeholder | planned |
| [../../gh-contoso-template/](../../gh-contoso-template/) | template | brand-safe deliverables template | built |
| [../../gh-ubb-learning-site/](../../gh-ubb-learning-site/) | learning | React + TypeScript + Tailwind site | built |
| [../../gh-ubb-simple-learning-site/](../../gh-ubb-simple-learning-site/) | learning | static HTML tools | built |
| [../../gh-ubb-ebook/](../../gh-ubb-ebook/) | learning | Markdown ebook (PT-BR) with SVG | built |
| [../../gh-ubb-token-optimization-workshop/](../../gh-ubb-token-optimization-workshop/) | learning | Markdown workshop (EN) | built |
| [../../gh-agentic-roi-calculator/](../../gh-agentic-roi-calculator/) | tool | static HTML calculator | built |
| [../../gh-ms-customers-decks/](../../gh-ms-customers-decks/) | decks | client-facing decks package | planned (empty) |
| [../../gh-ubb-oficial-documents/](../../gh-ubb-oficial-documents/) | documents | official documents package | planned (empty) |

Categories the platform navigation must expose: **Clients** (data-record control centers), **Learning** (sites, ebook, workshop), **Tools** (calculators), **Documents** (official document packages), **Decks** (client and analyst decks), and **Template** (the Contoso seed). Each catalog entry records how to reach the mini-app: a route inside the platform (ported or embedded) for things the platform renders itself, or an external link (with a note about the relative path) for standalone HTML, Markdown, or document packages.

## Canonical data (audited, do not invent or alter)

These BTG numbers must render exactly:

- Monthly token consumption US$ 231,704; seat revenue / standard entitlements US$ 127,249.
- Promo entitlements US$ 221,450 (1,693 CB seats x $30 + 2,438 CE seats x $70).
- Standard overage US$ 104,455/mo; promo overage US$ 10,375/mo (per-owner sum; account-level formula gives 10,254, both documented).
- PRU today US$ 130,948; with promo US$ 137,624; standard total US$ 231,704.
- Seats 4,131 (1,693 Business + 2,438 Enterprise); cache read 83.5% of tokens; claude opus 4.6 = 43.4% of spend.
- Growth +267.5% GHCP ACR (US$ 26,002.67 jul/25 to US$ 95,549.53 apr/26); Enterprise seats 157 to 2,145.87.
- Mature overage target US$ 35k (-66.5%); FY27 canonical curve savings US$ 485,550 (live formula yields ~487k, difference documented in-app).
- Scenario D total US$ 599k = US$ 209k discount (P3 20%) + US$ 390k net rescue.
- ROI ladder A 2.592 / B 2.435 / C 2.383 / D 1.993 (US$ mi).
- Model classes mini 0.60 / standard 6.00 / premium 12.00 / frontier 75.00 US$ per 1M tokens (125x spread).

## Engine formulas

Already implemented in `gh-btg/src/engine.js`; port as a shared module:

- `poolStd = (cbSeats x planBusiness.stdCredits + ceSeats x planEnterprise.stdCredits) x creditUSD`
- `poolPromo` = same with promo credits (Business 1,900/3,000 cr; Enterprise 3,900/7,000 cr; $19/$39 per seat)
- `overage = max(0, monthlyConsumption - pool)`; `ratio = consumption / poolStd`
- FY27 curve, month `m`: pool for promo months (jul, aug) uses `poolPromo`, otherwise `poolStd`; `withoutRescue = max(0, consumption - pool)` exact; `withRescue = round1k(max(0, consumption x (1 - ramp[m] x totalLeverReduction) - pool))`
- Leverage insight: cutting consumption X% cuts overage approximately 2.21X% (fixed entitlement pool)
- Budgets: `perUser = matureOverage / seats`; `perCostCenter = matureOverage / costCenters`; alert at 80%
- Maturity: 5 dimensions scored 1-5; stage initial <=10, evolving 11-18, mature 19-25
- ROI: `A = poolStd x 12 + sum(withoutRescue)`; `discount = P3% x sum(withoutRescue)`; `rescueNet = curveSavings x (1 - P3%)`; `C = A - discount`; `D = A - discount - rescueNet`

## Architecture

```text
ubb-platform/
  package.json (react, react-dom, vite, @vitejs/plugin-react, vite-plugin-singlefile)
  vite.config.js (base './', singlefile plugin so dist/index.html opens from file://)
  index.html (favicon: inline SVG data-URI Microsoft 4-square logo; OG/Twitter meta)
  src/
    main.jsx, App.jsx (hash router), styles.css (port ms-identity DS)
    i18n.js (EN/PT-BR/ES dictionaries; t(obj, loc) helper; persist locale)
    db.js (port useDB; namespace localStorage keys per client: ubb-${clientId}-${dbName})
    engine/ubb.js (port computeKit/computeAnalise; pure functions)
    engine/agentCalc.js (new, see Agent calculator)
    components/ (Grid.jsx editable grid + DBToolbar, Chrome nav, KpiCard, CurveChart,
      RoiLadder, ClientPicker, charts as hand-rolled SVG in DS style, no chart libs)
    data/
      registry.json (client list: id, name, tpid, segment, status, docsPath, colors)
      catalog.json (every workspace mini-app: id, title, category, type, path, entry,
        serve method, status, colors; drives the Catalog and category pages)
      clients/btg/{meta,billing,growth,kit,analise,acr}.json (copy from existing site)
    pages/
      central/Dashboard.jsx   (route #/)
      central/Catalog.jsx     (route #/catalog, all mini-apps grouped by category)
      central/Clients.jsx     (route #/clients)
      central/Calculator.jsx  (route #/calc)
      central/Automations.jsx (route #/auto)
      client/                 (routes #/c/:id/...)
        Overview, Documents, Data, Sheets (hub + kit/billing/growth/analise/acr
        editable mini-apps), Simulator, Plan, Glossary
  dist/ (single-file build + db/ JSON copies + preview PNG)
```

Client registry resolution: load all clients via Vite glob import (`import.meta.glob('./data/clients/*/meta.json', { eager: true })`), so adding a client folder automatically appears in the platform after a rebuild. Clients created at runtime via the Admin UI live in localStorage and merge with built-in ones.

Workspace catalog resolution: `catalog.json` is generated in Phase 0 by scanning the repository root, and drives the Catalog and category pages. Adding a `gh-*` folder must surface in the catalog after regenerating it, so keep the catalog data-driven (never hardcode the list in a component).

## Central pages

1. **Dashboard (`#/`):** aggregated KPIs across selected clients (total consumption, total standard overage, total FY27 savings potential, seats); client selector (multi-select chips); comparison table (client, seats, consumption, overage, ratio, mature target, savings); SVG bar comparison chart; per-client status badges (phase: baseline / instrument / optimize / scale, from kit data); cards linking to each client workspace.
2. **Catalog (`#/catalog`):** the index of every workspace mini-app from `catalog.json`, grouped by category (Clients, Learning, Tools, Documents, Decks, Template). Each card shows the title, category, type, status badge, and the way to open it (an internal route for things the platform renders, or an external link with a path note for standalone HTML, Markdown, or document packages). This is the main-site front door to all folders.
3. **Clients admin (`#/clients`):** list with meta editing; "New client" wizard: pick template (BTG), fill name/tpid/seats/consumption, the platform generates the six JSON databases from the template with the new parameters and recalculates; import per-sheet JSON files; export full client pack (sequential JSON downloads are acceptable, no zip); delete runtime clients (built-in clients cannot be deleted, only reset).
4. **Agent calculator (`#/calc`):** see the next section.
5. **Automations (`#/auto`):** batch actions across selected clients: recalculate all engines and show drift versus stored values; export all databases; reset to canonical; snapshot summary (one JSON with every client's KPIs) for leadership reporting.

## Agent calculator

A GitHub Copilot agent cost calculator (the planning tool for agent fleets).

- **Inputs (sliders/fields):** developers, agent sessions per developer per day, working days per month, average input tokens per session, average output tokens, cache read share %, model mix % (mini/standard/premium/frontier, must sum to 100), price per 1M tokens per class (defaults 0.60/6/12/75, editable), cache read price factor (default 0.1), plan (Business/Enterprise) and seats for entitlement comparison.
- **Outputs (live):** tokens per month by type; blended cost per session; monthly cost total and per developer; AI Credits equivalent (US$ 0.01/credit); entitlement pool for the chosen plan/seats; projected overage; sensitivity hint ("moving 10% of premium traffic to mini saves US$ X/mo"); mini-first recommendation note.
- Persist scenarios via `useDB` (`'calc'`), allow named scenarios, export/import.

## Client workspace

Routes `#/c/:id/{overview,docs,data,sheets,sheets/kit,sheets/billing,sheets/growth,sheets/analise,sheets/acr,sim,plan,glossary}`. Port **all** existing BTG pages from [../../gh-btg/](../../gh-btg/) parametrized by `clientId` (engine + editable grids + persistence per client). The Documents page reads `docsPath` from client meta; show a note that links require the documents folder to sit at the configured path. Keep the curve note explaining the approximately US$ 1.5k difference between the live formula and the canonical hand-rounded curve.

## i18n and design

Everything trilingual EN/PT-BR/ES with the existing `t()` pattern; port and extend the existing dictionaries; language switcher EN | PT | ES in the header; persist the choice. ms-identity design system: Microsoft palette #F25022 / #7FBA00 / #00A4EF / #FFB900 with 50/500/700 ramps, Inter for body and JetBrains Mono for data, light and dark themes, sticky header with the 4-square logo, cards with colored top accents, editorial tables. Always write "GitHub Copilot", never "Copilot" alone. No em dashes anywhere in UI copy.

## Execution plan

Work in phases and commit per phase (conventional commits).

- **Phase 0, scaffold and map:** package.json, vite config, index.html, styles port (load and apply the `ms-identity` skill), db.js port with client namespacing, engine port plus a unit-test script (a node script asserting canonical outputs: poolStd 127249, overageStd 104455, curve total savings approximately 485-487k, ROI A 2.59). Also **scan the repository root and generate `src/data/catalog.json`** cataloging every `gh-*` folder per the Workspace map (id, title, category, type, path, entry, serve method, status, colors). This catalog is the first data artifact and drives navigation.
- **Phase 1, data:** registry.json plus clients/btg/* from existing site data; meta schema `{id,name,tpid,segment,currency,fiscalMonth,docsPath,builtIn:true}`.
- **Phase 2, central pages:** Dashboard, Catalog (all mini-apps from `catalog.json`), Clients admin, Automations.
- **Phase 2, client workspace:** port all pages parametrized by `:id`.
- **Phase 2, agent calculator:** engine plus page.
- **Phase 3, integration:** router, nav (with the category sections Clients, Learning, Tools, Documents, Decks, Template surfaced from the catalog), cross-links, i18n completeness sweep (no PT leaking into EN/ES), favicon/OG, preview image.
- **Phase 4, verification (mandatory):** `npm run build`; then run a headless browser against `dist/index.html` over `file://`: zero page errors; every route renders (5 central including Catalog + 12 client for BTG); the Catalog lists every `gh-*` folder from `catalog.json` grouped by category, with each link or route resolving; dashboard aggregates equal the BTG canonical numbers; create a test client via the Admin wizard and verify it appears on the Dashboard, the Catalog, and its engine recalculates; edit a cell in each editable grid and verify recalc + dirty badge + reset; switch all three languages on five sampled routes; toggle dark mode; screenshot key pages. Fix everything found, then rerun.
- **Phase 5, docs:** README.md (usage, add-client flow, persistence model, build); update [../../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md](../../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md) to point to the platform as the new central; keep [../../gh-btg/](../../gh-btg/) untouched as the legacy reference.

## Constraints

- Reuse existing validated code instead of rewriting.
- Never modify files under the BTG deliverables package except `CONTEXT.md`; never alter canonical numbers.
- Client edits live in localStorage with export/import and File System Access save, exactly like the existing `useDB`.
- The final `dist/index.html` must open directly from `file://` with zero console errors.
- No external chart libraries; no backend (note in the README that Azure Static Web Apps plus an API is the future path for shared multi-user persistence).

## Done when

- The build succeeds and all Phase 4 checks pass with evidence (screenshots plus console output).
- The Catalog renders every workspace folder as a mini-app card grouped by category, and each one opens (internal route or external link with a path note).
- BTG renders its full control center inside the platform with numbers matching the canonical data.
- A new client can be created from the BTG template entirely through the UI.
- The agent calculator produces coherent costs at defaults (sanity check: 1,000 developers, 4 sessions/day, 22 days, 30k in / 3k out tokens, mix 40/40/15/5 should land in the low hundreds of thousands US$/mo before cache effects).
- The README documents everything.

## Output

Output concisely: return only the artifact path(s), build and rendering validation status, screenshots or preview path(s), and any critical findings or blockers. Do not narrate the process steps.

## Notes

- One platform with clients-as-data beats N copied sites: zero code duplication, automatic aggregation, one build.
- The platform is the single main site: it does not just list clients, it catalogs every workspace folder as a mini-app (clients, learning, tools, documents, decks, template). Keep `catalog.json` data-driven so a newly added `gh-*` folder appears after regenerating it.
- Vite glob import gives "drop a folder, get a client" for curated clients; the Admin wizard covers runtime creation without a rebuild.
- Phase 4 makes rendering-based verification mandatory because every regression caught in this project (i18n leaks, broken references, wrong totals) was found by rendering, not by reading code.

### Variations

- For Azure Static Web Apps hosting: remove vite-plugin-singlefile, set `base: '/'`, add `staticwebapp.config.json` with an SPA fallback.
- To include the BTG documents inside `dist` for portability: add a copy step for the deliverables folder into `dist/docs/btg` and set `docsPath` to `./docs/btg/`.
- To embed a static mini-app (a learning tool, a calculator, a deck) inside the platform rather than linking out, copy its built files into `dist/mini/<id>/` and point the catalog entry at that path; otherwise keep an external link with a note about the relative path.
