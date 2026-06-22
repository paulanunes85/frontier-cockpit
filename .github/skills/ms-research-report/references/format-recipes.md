# Format recipes

Per-format production recipes. Markdown is always the canonical source; render the other five from it.

## Table of contents

1. [Markdown (.md)](#markdown-md)
2. [HTML (.html)](#html-html)
3. [PDF (.pdf)](#pdf-pdf)
4. [Excel (.xlsx)](#excel-xlsx)
5. [Word (.docx)](#word-docx)
6. [PowerPoint (.pptx)](#powerpoint-pptx)
7. [Workshop multi-chapter formats](#workshop-multi-chapter-formats)

---

## Markdown (.md)

YAML frontmatter at the top:

```yaml
---
title: "Document title"
author: "Frontier Cockpit Team, Software Global Black Belt, Microsoft"
contact: "frontier-cockpit@example.com"
date: "YYYY-MM-DD"
version: "1.0"
status: "draft" | "review" | "final"
deliverable_type: "industry_analyst_report" | "account_dossier" | "technical_paper" | "competitive_intel" | "general" | "workshop"
---
```

Then:
- H1 for the title (matches frontmatter title)
- H2 for top-level sections
- H3 for subsections
- Fenced code blocks with language tags
- Markdown tables for structured comparisons
- Footnote-style citations (`[^id]`) collected at the bottom
- **Every footnote MUST resolve to a hyperlinked reference**, never a bare URL or plain source name. Format: `[^id]: [Source title and date](https://url)`.
- The References section at the bottom groups footnotes by source tier (A/B/C/D) when the deliverable type warrants it.

Output path: `output/<slug>.md`

---

## HTML (.html)

Single self-contained file. No external CSS files, no external JS files except CDN. Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {
      --ms-red: #F25022;
      --ms-green: #7FBA00;
      --ms-yellow: #FFB900;
      --ms-blue: #00A4EF;
      --ink: #1A1A1A;
      --ink-mid: #4A4A4A;
      --rule: #E5E5E5;
      --bg: #FFFFFF;
    }
    body { font-family: 'Segoe UI', Inter, system-ui, sans-serif; color: var(--ink); background: var(--bg); margin: 0; }
    .container { max-width: 960px; margin: 0 auto; padding: 32px 24px; }
    .header { position: sticky; top: 0; background: var(--bg); border-bottom: 1px solid var(--rule); padding: 12px 24px; }
    /* anchor color rotates per section */
    h2 { border-left: 4px solid var(--ms-blue); padding-left: 12px; }
    /* ... */
  </style>
</head>
<body>
  <header class="header">Software Global Black Belt · Frontier Cockpit Team</header>
  <main class="container">
    <!-- content -->
  </main>
  <footer>frontier-cockpit@example.com</footer>
</body>
</html>
```

Rotate the H2 left-border color across sections in the order: blue, green, yellow, red, blue, green...

If producing a JSX/React artifact, also produce a standalone HTML version using React CDN + Babel standalone + Tailwind CDN. Both functionally identical.

Output path: `output/<slug>.html`

---

## PDF (.pdf)

Use the `reportlab` Python library OR convert from HTML using `weasyprint` OR convert from DOCX using `docx2pdf`. Preferred approach by deliverable type:

- Industry analyst report → weasyprint from HTML (richest formatting)
- Account dossier → docx2pdf from DOCX (Word features carry over)
- Technical research paper → weasyprint from HTML
- Competitive intel brief → weasyprint from HTML
- General write-up → weasyprint from HTML

Required pages:
1. Cover (Microsoft 4-color block accent, title, author line, date, version)
2. Table of contents (auto-generated)
3. Body sections with chapter banner (rotating anchor color per chapter)
4. References page
5. Closing card (single-email contact)

Continuous page numbers, footer with "Software Global Black Belt · frontier-cockpit@example.com".

Output path: `output/<slug>.pdf`

---

## Excel (.xlsx)

Use `openpyxl`. Always:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
# remove default sheet, build sheets explicitly
```

Per-sheet rules:
- Font: Arial 10 for data, Arial 11 bold for headers
- Header row: white text on Microsoft blue (#00A4EF) fill
- Freeze panes at A2 (or wherever the header ends)
- Auto-filter on full data range
- Column widths sized to content (don't leave default)
- SUM formulas with explicit cell ranges, not hard-coded numbers
- No merged cells inside data ranges (banner row at top can merge)

Standard sheet set for an industry analyst report XLSX:
1. `Cover`: title, author, date, version, color block
2. `Capability Matrix`: primary deliverable
3. `Vendor Scores`: weighted scoring with SUM totals and validation
4. `Sizing`: TAM/SAM/SOM math if applicable
5. `Sources`: [ID, Claim, Source, URL, Date, Tier]

Standard sheet set for a competitive intel XLSX:
1. `Cover`
2. `Feature Comparison`: rows = features, cols = vendors
3. `Scorecard`: weighted scores
4. `Sources`

Output path: `output/<slug>.xlsx`

---

## Word (.docx)

Use `python-docx`. Apply identity tokens via styles, not inline formatting (so the user can tweak via Word's Styles pane).

Required structure:
1. Cover page (4-color accent block, title, author line, date, version)
2. Document properties filled: title, author = "Frontier Cockpit Team", subject = deliverable_type, company = "Microsoft"
3. Header: "Software Global Black Belt" (right-aligned, small caps)
4. Footer: page number center, "frontier-cockpit@example.com" right
5. Table of contents (auto-generated if 4+ sections)
6. Body with H1/H2/H3 styles using Microsoft 4-color anchors
7. Closing page with single-email contact card

Style names to define and apply:
- `MS Title`: Segoe UI 28 bold, blue
- `MS H1`: Segoe UI 18 bold, anchor color per chapter
- `MS H2`: Segoe UI 14 bold, ink
- `MS Body`: Segoe UI 11, ink
- `MS Caption`: Segoe UI 9 italic, ink-mid

Output path: `output/<slug>.docx`

---

## PowerPoint (.pptx)

Use `python-pptx`. White background standard. Slide types:

1. **Cover**: Microsoft 4-color block (pick one anchor for this deck), title, author, date
2. **Section divider**: full-bleed anchor color, section title in white
3. **Content slide**: title, body, optional sidebar; anchor color as a thin top accent bar
4. **Comparison/quadrant**: chart or 2x2 with anchor color callouts
5. **Capability heatmap**: table with conditional color fill
6. **References**: single slide listing sources
7. **Closing card**: Frontier Cockpit Team, Software Global Black Belt, frontier-cockpit@example.com

Anchor color rotates per section (not per slide). Speaker notes filled on every slide (key talking points, 2 to 4 bullets per slide). No em dashes in speaker notes either.

Slide size: 16:9 widescreen (13.333" x 7.5").

Output path: `output/<slug>.pptx`

---

## Common gotchas

- Em dashes sneak into Python string literals copied from web sources. Grep your draft for `—` and replace with `, ` or `: ` before rendering.
- `python-docx` doesn't fully support custom theme colors; set RGB explicitly per run.
- `openpyxl` SUM with non-numeric cells produces `#VALUE!`; coerce to numeric or skip.
- `weasyprint` doesn't render `position: sticky`; use it for HTML, drop it for PDF rendering.
- Speaker notes in `python-pptx` are added via `slide.notes_slide.notes_text_frame.text`, not via a regular text frame.
- For HTML, set `print:` CSS rules to ensure PDF conversion looks right.

---

## Workshop multi-chapter formats

For deliverable type 6 (workshop / educational content). Inputs are the full set of chapter MDs plus the master index plus the references file. Outputs are derived formats that aggregate the chapter set into a single deliverable.

### Multi-chapter MD pattern

Save each chapter to `output/workshop-{slug}/NN-{chapter-slug}.md`. The workshop slug is derived from the topic (e.g., "Token Optimization in VS Code and GitHub" → `token-optimization-vscode-github`). Chapter slugs use kebab-case and concise (3 to 6 words).

Naming convention:
- `00-index.md`: master index (always)
- `01-{slug}.md` through `NN-{slug}.md`: substantive chapters in reading order
- `99-references.md`: consolidated bibliography (always)

The 2-digit zero-padded prefixes ensure chapters sort correctly in directory listings and in PDF/PPTX assembly. Use prefixes 01 through 98 for substantive chapters. Reserve 99 for references.

### Consolidated PDF playbook

Single PDF assembled from the full chapter set. Use weasyprint via an HTML intermediary, same engine as the single-doc PDF recipe above.

Required pages in order:

1. **Cover** (1 page): workshop title, subtitle, author block, version, date. Microsoft 4-color stripe top or left edge. Same cover pattern as single-doc PDF.
2. **Table of contents** (1 to 2 pages, auto-generated): list every chapter with its level badge, estimated duration, and page number where the chapter starts.
3. **Workshop scope page** (1 page): pulled from `00-index.md`. Includes audience, prereqs, total duration, workshop-level learning outcomes.
4. **Chapter pages** (multi-page per chapter): each chapter starts on a new page with a banner header carrying the chapter number, title, and level badge. Banner background rotates through the Microsoft 4 colors (blue, green, yellow, red, blue, ...) per chapter. Full chapter content inline.
5. **Consolidated references page** (1 to 3 pages): merged citations from all chapters, grouped by source tier (A/B/C/D) per library anti-pattern, sorted alphabetically within tier.
6. **Closing card** (1 page): ms-identity closing pattern.

Page numbering is continuous across the playbook (excludes cover). Footer shows `Software Global Black Belt · frontier-cockpit@example.com` left and `Page N of M` right. Each chapter banner also shows chapter-level info (e.g., "Chapter 4 · Token economics no GitHub Copilot · Intermediate · 45 min").

Output path: `output/workshop-{slug}/workshop-{slug}.pdf`

### PPTX facilitator deck

Use `python-pptx`. Slide size 16:9 (13.333" x 7.5"). White background. Each chapter gets a section divider + 5 to 8 content slides.

Required slide order:

1. **Cover slide**: workshop title, author block, date. One anchor color (default blue) as a corner block.
2. **TOC slide**: chapter list with level badges. One slide, not split.
3. **Scope and audience slide**: pulled from `00-index.md`.
4. **Per chapter** (5 to 8 slides):
   a. **Section divider** (1 slide): full-bleed anchor color (rotating per chapter), chapter number and title in white. Level badge (Foundations / Intermediate / Advanced) bottom-left.
   b. **Chapter outline slide** (1 slide): learning outcomes, prereqs, duration. Top accent bar in anchor color.
   c. **Concept slides** (3 to 6 slides): one core idea per slide. Top accent bar in anchor color. Body uses bullets sparingly; favor diagrams, tables, and worked-example snippets.
   d. **Practice / summary slide** (1 slide): exercises or key takeaways. Anchor color used in summary box.
5. **Consolidated references slide** (1 slide; if references exceed one slide, split as needed)
6. **Closing card slide**: ms-identity closing pattern. White background, 4-color stripe top, author block centered.

Speaker notes filled on every slide: 2 to 4 bullets, 40 to 80 words, written for spoken delivery, no em dashes. Anchor color for each chapter persists across all that chapter's content slides; it changes only at the next section divider.

Output path: `output/workshop-{slug}/workshop-{slug}.pptx`

### HTML deck (web)

Self-contained single HTML file. Two style modes, default picked by audience:

- **scroll-style** (default for self-study audiences): long-form readable, all chapters in one scrollable page, sticky header, collapsible TOC sidebar. Best for reading and reference.
- **slide-style** (default for instructor-led delivery): reveal.js-like horizontal navigation, one chapter per "row", with vertical slides within each row for the chapter's content slides. Keyboard nav (arrow keys, Space).

Both modes:
- Microsoft 4-color identity: anchor color rotates per chapter
- Sticky header: workshop title + chapter indicator + "Software Global Black Belt"
- TOC always reachable: sidebar in scroll-style, "T" key in slide-style
- Code blocks rendered with light syntax highlighting
- Closing footer with single email contact

Output path: `output/workshop-{slug}/workshop-{slug}.html`

If JSX/React is used, ALSO produce a standalone HTML version with React CDN + Babel standalone + Tailwind CDN. Both versions functionally identical.

### 99-references.md (consolidated bibliography)

Always produced for workshop deliverables. Aggregates every reference cited across the chapter set. Format:

- Top YAML frontmatter (title "References", author, version matching the workshop)
- H1 "References"
- Brief intro paragraph (1 to 2 sentences) explaining the source-tier scheme
- One H2 per tier in this order: "Tier A: Primary sources", "Tier B: Industry coverage and analyst sources", "Tier C: Vendor self-positioning", "Tier D: Sentiment sources (not cited as fact)". Skip tiers with zero entries.
- Each entry is a hyperlinked Markdown reference: `- [Source title and date](https://url): one-line description of what claim it supports`
- Within each tier, sort alphabetically by source title
- Final H2 "Academic papers" if any peer-reviewed or arXiv sources are cited, listing them separately with formal-ish citation (authors, year, title-as-hyperlink, venue or arXiv id)

Every URL in this file is a clickable hyperlink. Bare URLs and plain-text source names are forbidden anywhere in this file.

### Build script pattern

For workshops with 10+ chapters, write a build driver (`build_workshop.py`) that reads the entire `workshop-{slug}/` directory, parses chapter frontmatter, and renders all three derived formats. Keeps logic in one place and lets the user re-render after editing any chapter MD.

Skeleton:

```python
from pathlib import Path
import yaml

WORKSHOP_DIR = Path("output/workshop-{slug}")
chapters = sorted(WORKSHOP_DIR.glob("[0-9][0-9]-*.md"))
index = WORKSHOP_DIR / "00-index.md"
references = WORKSHOP_DIR / "99-references.md"

# Parse each chapter: frontmatter + body
# Aggregate into PDF (weasyprint via HTML), PPTX (python-pptx), HTML (single file)
```

### Workshop output delivery

After all formats are produced, present the files to the user in this order:
1. Consolidated PDF playbook (the headline artifact)
2. PPTX facilitator deck
3. HTML deck (if produced)
4. Master index MD (so user can edit scope and re-render)
5. All chapter MDs as a group

Summary paragraph identifies the audience for each format: "PDF playbook for printing or as the authoritative reference, PPTX for live facilitator delivery, HTML for self-study or async distribution, chapter MDs for editing and version control."
