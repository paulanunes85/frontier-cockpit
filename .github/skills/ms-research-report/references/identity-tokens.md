# Identity tokens (ms-identity)

Source of truth: the `ms-identity` skill. This file replicates the tokens needed by `ms-research-report` so the skill stays standalone. If `ms-identity` changes, re-sync this file.

## Author and contact

- **Author line (full)**: Frontier Cockpit Team, Software Global Black Belt, Microsoft
- **Author line (short)**: Frontier Cockpit Team · Software Global Black Belt
- **Role string**: Software Global Black Belt
- **Contact**: frontier-cockpit@example.com
- **Single email only**. Do NOT include @your-org, @your-handle, or any social handle. Those belong to personal-identity deliverables only.

## Header (every doc/deck/page)

`Software Global Black Belt`

- Right-aligned in document headers
- Small caps when the format supports it (DOCX, HTML, PDF)
- Plain caps when it doesn't (PPTX speaker notes, plain MD)

## Closing card

Every multi-page deliverable ends with a closing card:

```
Frontier Cockpit Team
Software Global Black Belt, Microsoft
frontier-cockpit@example.com
```

Single email. No socials, no LinkedIn URL.

## Microsoft 4-color palette

| Token | Hex | Role |
|---|---|---|
| `--ms-red` | #F25022 | Anchor 1 |
| `--ms-green` | #7FBA00 | Anchor 2 |
| `--ms-yellow` | #FFB900 | Anchor 3 |
| `--ms-blue` | #00A4EF | Anchor 4 (default for first section) |

## Neutrals

| Token | Hex | Role |
|---|---|---|
| `--ink` | #1A1A1A | Primary text |
| `--ink-mid` | #4A4A4A | Secondary text, captions |
| `--rule` | #E5E5E5 | Borders, table grid |
| `--surface` | #F7F7F7 | Card backgrounds (used sparingly) |
| `--bg` | #FFFFFF | Page background |

## Anchor color rotation

For multi-section deliverables, rotate the anchor color per section in this order: **blue, green, yellow, red, blue, green, ...**

Apply to:
- HTML: H2 left border, section divider rules
- PDF: chapter banner background
- DOCX: H1 color
- PPTX: section divider full-bleed
- XLSX: sheet tab color when there's a 1:1 sheet-to-section mapping

## Typography

| Format | Primary | Fallback | Notes |
|---|---|---|---|
| Markdown | n/a | n/a | renderer chooses |
| HTML | Segoe UI | Inter, system-ui, sans-serif | font-display: swap |
| PDF (HTML-rendered) | Segoe UI | Inter, sans-serif | embed if needed |
| DOCX | Segoe UI | Calibri | applied via styles |
| PPTX | Segoe UI | Calibri | applied per shape |
| XLSX | Arial | n/a | Arial 10 body, Arial 11 bold header |

## Logo (ms-identity shape, Microsoft 4-color squares)

Four squares in a 2x2 grid, one per Microsoft color, with the ms-identity shape outline. Use in cover pages and closing cards. SVG and PNG variants live in `assets/templates/` (placeholder; if not present, render the 2x2 color block directly in the format).

Inline SVG fallback if no asset file is available:

```svg
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <rect x="0"  y="0"  width="22" height="22" fill="#F25022"/>
  <rect x="26" y="0"  width="22" height="22" fill="#7FBA00"/>
  <rect x="0"  y="26" width="22" height="22" fill="#00A4EF"/>
  <rect x="26" y="26" width="22" height="22" fill="#FFB900"/>
</svg>
```

## Cover patterns per format

**HTML**: top band 100% width, 96px tall, anchor color, white title and author line on top.

**PDF**: top third anchor color block, title in white centered, author/date in white bottom-left of the block.

**DOCX**: full-width image or shape block on the first page using anchor color; title in white, then a thin 4-color stripe (one square of each color, ~6pt tall).

**PPTX**: cover slide with anchor color block taking left third or top third; title and author in the remaining area; 4-color stripe along the bottom edge.

**XLSX**: row 1 banner merged across used columns, anchor color fill, white bold title; row 2 sub-banner with author + date.

## Closing card patterns per format

**HTML**: centered card at end of body, neutral surface background, 4-color stripe across the top, author block centered.

**PDF**: dedicated final page, centered, 4-color stripe near top, author block centered, single email last.

**DOCX**: dedicated final page (page break before), centered, 4-color stripe, author block.

**PPTX**: final slide, white background, 4-color stripe across top, author block centered, single email centered.

**XLSX**: final sheet named `About`, with the author block in the first few rows and stripe in row 1.

## Editorial tokens (cross-format)

- No em dashes (`—`). Use commas, periods, semicolons, parentheses, or colons.
- "GitHub Copilot" always in full.
- Territory-neutral by default. No LATAM/Brazil/regional framing unless explicitly requested.
- Direct, structured, casual-professional tone.

## Version

This identity spec mirrors ms-identity as of the date this skill was authored. If ms-identity changes, update this file.
