---
description: "How every generated or saved document must be placed, versioned, archived, and validated in this repository: one folder per file type, latest version in the folder root, old and duplicate versions in that folder's archive/."
applyTo: "html/**,pdf/**,xlsx/**,pptx/**,docx/**,md/**,README.md"
---

# Document Organization

These rules apply whenever GitHub Copilot generates, saves, updates, or reorganizes a document in this repository. The repository is a document store organized by file type. The full document map and "how it works" live in [../../README.md](../../README.md).

## Placement (always)

- **One folder per file type.** Save each file under the folder matching its extension:
  - `.html` to `html/`
  - `.pdf` / `.PDF` to `pdf/`
  - `.xlsx` to `xlsx/`
  - `.pptx` / `.PPTX` to `pptx/`
  - `.docx` to `docx/`
  - `.md` to `md/` (the root `README.md` is the only Markdown file that stays at the root)
- **Deck derivative exception.** Files derived directly from a deck HTML under `html/decks/` stay with the deck family:
  - deck `.pdf` files to `html/decks/pdf/<DeckBase>/`
  - deck `.pptx` files to `html/decks/pptx/<DeckBase>/`
  - deck preview images to `html/decks/previews/`
  - deck-only screenshots and simulation images to `html/decks/assets/`
- **Never leave a new document loose at the repository root.** The root holds only `README.md`, the type folders, `.github/`, and `agentic-roi-calculator/`.
- The `agentic-roi-calculator/` app is self-contained; do not move its files into the type folders.

## Versioning and archive (always)

- **Keep only the latest version of a document in its type folder root.**
- When a newer version arrives, move the previous version into that folder's `archive/` (create `archive/` if it does not exist).
- Treat duplicate downloads as old versions and move them to `archive/` too: `name (1).pdf`, `name_4.html`, `name copy.pptx`, and similar suffixes.
- "Latest" is decided by the version and date in the filename (`Name_vMAJOR_MINOR_PATCH_YYYY-MM-DD_lang.ext`). If two files are the same logical document, the higher version or later date wins and the other goes to `archive/`.
- Two files that are genuinely different documents (for example `..._Architecture_1.html` and `..._Architecture_2.html` being distinct diagrams) both stay in the folder root. When unsure whether something is a new version or a separate document, ask before archiving.

## Naming

- For authored deliverables, follow `Name_vMAJOR_MINOR_PATCH_YYYY-MM-DD_lang.ext` (for example `BTG_BusinessCase_UBB_v2_0_0_2026-06-05_pt-BR.html`).
- Keep the original names of external source files (vendor PDFs, arXiv papers).

## Validate in place (before considering done)

1. The new file is in the correct type folder, not at the root.
2. Any previous version of the same document is in that folder's `archive/`, and only the latest version remains in the folder root.
3. For HTML deliverables, the file opens and renders with no console errors.
4. If a new logical document was added (not just a new version), the document map in [../../README.md](../../README.md) is updated to list it.

## Copy rules

- Documentation is written in English. Write "GitHub Copilot", never "Copilot" alone. No em dashes.
- Never fabricate metrics. BTG financial, billing, usage, and ROI numbers are audited; pull them from the audited workbooks under `xlsx/` and cite the source.
