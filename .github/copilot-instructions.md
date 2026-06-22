# GitHub Copilot Instructions

Repository-wide guidance for GitHub Copilot in the **GitHub Copilot UBB Transition Workspace**. Keep responses aligned with these conventions. Path-scoped rules live in [instructions/](instructions/), reusable prompts in [prompts/](prompts/), custom agents in [agents/](agents/), and skills in [skills/](skills/).

## Document organization (always)

This repository stores rendered and authored documents by file type (`html/`, `pdf/`, `xlsx/`, `pptx/`, `docx/`, `md/`). Whenever you generate, save, or update a document:

- Place it in the folder matching its extension; never leave it loose at the repository root.
- Exception for deck derivatives: PDF and PPTX files generated from `html/decks/*.html` stay with the deck family under `html/decks/pdf/<DeckBase>/` and `html/decks/pptx/<DeckBase>/`. Deck previews stay under `html/decks/previews/`, and deck-only support images stay under `html/decks/assets/`.
- Keep only the latest version in the folder root; move any previous version or duplicate download into that folder's `archive/`.
- Validate it in place, and update the document map in [../README.md](../README.md) when you add a new logical document.

The full rule is auto-applied by [instructions/document-organization.instructions.md](instructions/document-organization.instructions.md); the document map and "how it works" are in [../README.md](../README.md).

## What this repository is

A workspace for planning, packaging, and presenting **GitHub Copilot Usage-Based Billing (UBB)** transitions for enterprise clients. It holds:

- **Client cases**: per-client packages (control center apps and/or deliverables). The reference, fully built case is `gh-btg/`. Other client folders (`gh-bb`, `gh-bradesco`, `gh-caixa`, `gh-petrobras`, `gh-serpro`) are planned placeholders.
- **Template**: `gh-contoso-template/`, the brand-safe (anonymized "Contoso") deliverables used to seed new client cases.
- **Learning experiences**: `gh-ubb-learning-site/` (React + TypeScript + Tailwind), `gh-ubb-simple-learning-site/` (static HTML tools), `gh-ubb-ebook/` (PT-BR Markdown ebook with SVG diagrams), and `gh-ubb-token-optimization-workshop/` (English Markdown workshop).
- **Tools**: `gh-agentic-roi-calculator/` (static HTML agent ROI calculator).
- **Decks and documents**: `gh-ms-customers-decks/` (client-facing decks) and `gh-ubb-oficial-documents/` (official reference documents). Planned (empty) packages.
- **Platform spec**: the build prompt for the future multi-client `ubb-platform/` lives at [prompts/build-ubb-platform.prompt.md](prompts/build-ubb-platform.prompt.md). The platform is the single main site that indexes and hosts every workspace folder as a mini-app.
- **AI context index**: [../llms.txt](../llms.txt) is the machine-readable map of this hub for AI-native tools. Regenerate it with `bash .github/scripts/generate-llms-txt.sh` after adding or removing primitives.

The strategic direction: instead of duplicating one site per client, treat **each client as a data record** inside a single platform; the BTG case is the validated template.

## Golden rules

1. **Never fabricate metrics.** Financial, billing, usage, and ROI numbers are audited per client. Do not invent, estimate, or alter canonical values. When a number is needed, pull it from the client's audited source (for BTG, see `gh-btg/btg-gh-ubb-mini-site/CONTEXT.md`). Cite the source.
2. **Always write "GitHub Copilot"**, never "Copilot" alone, in user-facing copy.
3. **English for documentation.** All `.md` documentation, READMEs, and everything under `.github/` is written in English. App UI copy is trilingual (EN / PT-BR / ES).
4. **No em dashes in UI copy.** Use commas, parentheses, or restructure the sentence.
5. **Reuse, do not rewrite.** The BTG app contains battle-tested code (engine formulas, the `useDB` persistence hook, the editable grid, i18n, the design system). Port and parametrize it; do not reimplement from scratch.
6. **Do not alter built deliverables.** Treat files under any client's deliverables package (for BTG, `btg-gh-ubb-mini-site/`) as audited outputs. Update `CONTEXT.md` if context changes, but never silently rewrite numbers.
7. **Curate external primitives.** Do not bulk-import from `github/awesome-copilot` or any external catalog. Use the local `suggest-awesome-github-copilot-*` skills and [prompts/compare-with-awesome.prompt.md](prompts/compare-with-awesome.prompt.md), then classify each candidate as adopt, adapt, defer, or reject.

## Tech stack and conventions

- **Frontend:** React 18 with Vite. Prefer **TypeScript** for new apps. Hash routing so single-file builds open from `file://`.
- **Design system (ms-identity):** Microsoft 4-color palette `#F25022` / `#7FBA00` / `#00A4EF` / `#FFB900` with 50/500/700 ramps; **Inter** for body text, **JetBrains Mono** for data; light and dark themes; sticky header with the 4-square logo; cards with colored top accents; editorial tables.
- **Charts:** hand-rolled SVG in the design-system style. No external chart libraries.
- **Assets:** use **SVG** for icons, favicons, and logos (inline data-URI favicon is preferred).
- **Persistence:** client edits live in `localStorage` with export/import and File System Access save, following the existing `useDB` hook. No backend today (Azure Static Web Apps is the future path for shared persistence).
- **i18n:** trilingual EN / PT-BR / ES via the existing `t()` pattern; persist the locale; never let one language leak into another.

## Data integrity and sources

- Every document with data claims must include a **References** section linking to the source.
- Acceptable sources: the client's audited workbooks and `CONTEXT.md`, official vendor docs (Microsoft Learn, GitHub Docs), and named analyst firms with links.
- If no source exists, state the value as an explicit assumption or omit it.

## Verification

When building or changing an app, prefer rendering-based verification (build, then check routes render with zero console errors) over reading code alone. Most regressions in this project (i18n leaks, broken references, wrong totals) are caught by rendering, not by inspection.

## Customizations in this repository

- **Instructions** (auto-applied by path): [instructions/react-apps.instructions.md](instructions/react-apps.instructions.md), [instructions/client-cases.instructions.md](instructions/client-cases.instructions.md), [instructions/documentation.instructions.md](instructions/documentation.instructions.md), [instructions/skills-authoring.instructions.md](instructions/skills-authoring.instructions.md), [instructions/agentic-architecture.instructions.md](instructions/agentic-architecture.instructions.md).
- **Prompts** (run with `/`): [prompts/build-ubb-platform.prompt.md](prompts/build-ubb-platform.prompt.md), [prompts/new-client-case.prompt.md](prompts/new-client-case.prompt.md), [prompts/verify-app.prompt.md](prompts/verify-app.prompt.md), [prompts/research.prompt.md](prompts/research.prompt.md), [prompts/spec-feature.prompt.md](prompts/spec-feature.prompt.md), [prompts/audit-skills.prompt.md](prompts/audit-skills.prompt.md), [prompts/new-skill.prompt.md](prompts/new-skill.prompt.md), [prompts/design-agentic-system.prompt.md](prompts/design-agentic-system.prompt.md), [prompts/diagram-architecture.prompt.md](prompts/diagram-architecture.prompt.md), [prompts/review-agentic-architecture.prompt.md](prompts/review-agentic-architecture.prompt.md).
- **Agents** (select in chat): `UBB Engineer` ([agents/ubb-engineer.agent.md](agents/ubb-engineer.agent.md)) builds and extends the apps; `Data Auditor` ([agents/data-auditor.agent.md](agents/data-auditor.agent.md)), read-only, checks canonical-number integrity; `Deliverables Producer` ([agents/deliverables-producer.agent.md](agents/deliverables-producer.agent.md)) produces decks, reports, and PDFs under the Microsoft identity; `Spec Engineer` ([agents/spec-engineer.agent.md](agents/spec-engineer.agent.md)) writes spec-driven plans; `AI-Native Engineer` ([agents/ai-native-engineer.agent.md](agents/ai-native-engineer.agent.md)) designs agentic architectures on the GitHub platform and Azure AI Foundry and renders diagrams with official icons.
- **Skills** (loaded on demand): `ubb-engine` ([skills/ubb-engine/SKILL.md](skills/ubb-engine/SKILL.md)) holds the canonical formulas and a node script that asserts the audited outputs, plus the design and document skills (`ms-identity` family). The AI-native set covers `agentic-architecture-patterns`, `azure-managed-redis-cache`, `foundry-agent-blueprint`, `azure-api-center`, `apim-ai-gateway`, and `azure-architecture-diagrams` (which bundles a Python draw.io MCP server for diagrams with official Azure, Microsoft, and GitHub icons).
- **Validation** (the equivalent of hooks; GitHub Copilot has no hooks primitive): VS Code tasks in [../.vscode/tasks.json](../.vscode/tasks.json) (run "Validate workspace") and CI in [workflows/validate.yml](workflows/validate.yml) run on every push and pull request. The engine check verifies the canonical numbers; [scripts/audit-skills.sh](scripts/audit-skills.sh) audits the skills; [scripts/audit-primitives.sh](scripts/audit-primitives.sh) audits the agents, prompts, and instructions; [scripts/audit-external-content.sh](scripts/audit-external-content.sh) audits external provenance; [scripts/generate-llms-txt.sh](scripts/generate-llms-txt.sh) keeps [../llms.txt](../llms.txt) current. The skill output gates (deck, identity HTML, architecture, research) run together through [scripts/validate-deliverables.sh](scripts/validate-deliverables.sh): with no argument it is a regression guard over the committed example assets, and with a folder it validates real deliverables.
- **External content governance**: [instructions/external-copilot-content.instructions.md](instructions/external-copilot-content.instructions.md) applies to imported or adapted agents, skills, prompts, and instructions. External content must keep provenance metadata, pass [scripts/audit-external-content.sh](scripts/audit-external-content.sh), and avoid automatic installation or overwrites.

## Repository hygiene

- Do not commit build output (`dist/`, `build/`), `node_modules/`, Vite `*.timestamp-*.mjs` artifacts, or `.DS_Store`. These are covered by the root `.gitignore`.
- Each folder has a `README.md` describing its purpose, contents, status, and how to run it. Keep them current.

## Pointers

- Root overview: [../README.md](../README.md)
- Platform build prompt: [prompts/build-ubb-platform.prompt.md](prompts/build-ubb-platform.prompt.md)
- Reference case: [../gh-btg/README.md](../gh-btg/README.md)
- Canonical BTG numbers: [../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md](../gh-btg/btg-gh-ubb-mini-site/CONTEXT.md)
