---
name: playbook-pdf-builder
description: >
  Generates a professional consolidated PDF from multiple Markdown files — playbooks,
  runbooks, frameworks, or any multi-chapter document. Produces: dark cover page with
  gradient accent bar and chapter preview blocks, auto-generated TOC with colored dots,
  per-chapter colored banner headers, continuous page numbers, embedded images, dark-mode
  code blocks, striped tables, and a 2-column references section on its own final page.
  Use when the user says: "criar PDF do playbook", "gerar PDF consolidado", "juntar
  capítulos em PDF", "consolidate chapters into PDF", "make a runbook PDF", "PDF único
  de vários markdowns", "playbook completo em PDF", "assemble playbook", "build PDF
  from markdown files", or wants a single polished deliverable from multiple .md files.
---

# Playbook PDF Builder

This skill produces a single, polished PDF from multiple Markdown source files.
The visual pattern is fixed and production-ready — dark cover, colored chapter banners,
auto TOC, page numbers, images embedded, 2-column references. All you provide is the
content; the skill handles the design.

## What it produces

```
Page 1  — Cover (no page number): dark background, gradient accent bar,
           chapter preview blocks top-right, title + subtitle + author + date
Page 2  — Table of Contents (no page number): colored dots per chapter, descriptions
Pages 3+ — Chapters in order: colored banner header + body content
           Continuous page numbers bottom-right
Last    — References: page-break-before, 2-column, 7.5pt
```

## Step 1 — Gather inputs from the user

Ask (or infer from context) the following. Most have sensible defaults.

| Input | Required | Default |
|-------|----------|---------|
| List of `.md` files in order | Yes | — |
| Images folder path | No | same folder as .md files |
| Document title (cover) | Yes | infer from first chapter title |
| Document subtitle (cover, 1–2 sentences) | No | infer from chapter descriptions |
| Author name | No | `Frontier Cockpit Team` |
| Author title/org | No | `AI-Native Software Engineer · @your-org` |
| Document date + version | No | today's date + `v1.0` |
| Output PDF path | No | auto-generated — see naming convention below |
| Chapter colors (one per chapter) | No | use default palette (see below) |
| Chapter descriptions (for TOC + banner) | No | extract from frontmatter `description` field or first paragraph |
| Type label (cover eyebrow) | No | `Complete Playbook` |

**Default color palette** (cycles if more chapters than colors):
```
#0078D4  (blue)
#7FBA00  (green)
#FFB900  (yellow/amber)
#F25022  (red/orange)
#8661C5  (purple)
#00B294  (teal)
#E3008C  (magenta)
#2C2C2A  (dark, for intro/overview chapters)
```

## Step 2 — Confirm chapter list with the user

Before generating, show the user a summary:

```
I'll generate a PDF with these chapters:
  Cover: [Title] — [Subtitle]
  00 ● [color] — [Chapter Label]   (filename.md)
  01 ● [color] — [Chapter Label]   (filename.md)
  ...
Output: [output_path.pdf]
```

Adjust based on feedback. Then proceed.

## Step 3 — Run the generator script

Use the bundled script at `scripts/build_pdf.py`. Call it as:

```bash
python3 <skill_dir>/scripts/build_pdf.py \
  --config /tmp/playbook_config.json \
  --output /path/to/output.pdf
```

Before calling the script, write a JSON config file to `/tmp/playbook_config.json`
with this structure:

```json
{
  "title": "Document Title",
  "title_break": "Document\nTitle",
  "subtitle": "One or two sentence description of the document.",
  "eyebrow": "Complete Playbook",
  "author": "Frontier Cockpit Team",
  "author_title": "AI-Native Software Engineer · @your-org",
  "date": "April 2026 · v1.1.0",
  "images_dir": "/absolute/path/to/images/folder",
  "chapters": [
    {
      "num": 0,
      "label": "Introduction",
      "description": "Short description shown in TOC and banner (1–2 sentences)",
      "color": "#2C2C2A",
      "file": "/absolute/path/to/00_intro.md"
    },
    {
      "num": 1,
      "label": "Chapter One Title",
      "description": "Short description for TOC and banner",
      "color": "#0078D4",
      "file": "/absolute/path/to/01_chapter.md"
    }
  ]
}
```

**`title_break`**: use `\n` to control where the title breaks across lines on the cover.
If omitted, defaults to `title`.

**`description` in chapters**: keep to 1–2 sentences max; shown below the chapter title
in both the TOC entry and the colored banner header. If not provided, extract from the
markdown file's YAML frontmatter `description` field, or use the first sentence of the
first paragraph.

## Step 4 — Verify output

After the script runs, confirm:
- File exists and is non-zero size
- Check page count: `python3 -c "from pypdf import PdfReader; r=PdfReader('output.pdf'); print(len(r.pages), 'pages')"`
- Present the file link to the user

---

## Design system (do not modify)

The visual language is fixed. Do not change colors, fonts, margins, or layout
unless the user explicitly asks. The design was battle-tested across multiple
enterprise playbooks and the proportions are deliberate.

### Cover
- Background: `#0F0F0E` (near-black)
- Accent bar: 6mm gradient `#F25022 → #FFB900 → #7FBA00 → #0078D4 → #8661C5`
- Chapter preview blocks: top-right, colored pills, white text, uppercase, 8pt
- Title: 32pt, weight 800, white, line-height 1.1
- Subtitle: 13pt, `#C8C6BE`, max-width 140mm
- Author block: divider line + name (11pt white bold) + title (9pt `#888780`) + date

### TOC
- Colored circle dot (8mm diameter) per chapter
- Chapter label: 11pt bold
- Chapter description: 9pt `#888780`
- No page numbers in TOC (intentional — WeasyPrint cross-reference links are unreliable)

### Chapter banner
- Full-bleed (bleeds into margins), colored background per chapter
- Eyebrow: chapter number label, 8pt, uppercase, letter-spacing 2pt, 75% opacity
- Title: 20pt bold white
- Description: 10pt, 80% opacity

### Body typography (editorial purple/blue palette)
- Font: system sans-serif stack (renders as Segoe UI on Windows, SF Pro on Mac, Helvetica elsewhere)
- Body: 9.5pt, line-height 1.6, `#2C2C2A`
- H2: 13pt, color `#5B2D8E` (purple), border-bottom `#D6C8E8` (lavender), page-break-after avoid
- H3: 10.5pt, color `#0058A3` (blue), page-break-after avoid
- Orphan/widow control: `orphans: 3; widows: 3;` on all paragraphs and headings;
  `page-break-before: avoid` on elements immediately following h2/h3 (prevents topics starting at page bottom)
- Code (inline): `#EBF3FD` background, `#0058A3` text, 7.5pt — blue tint for .md file references
- Code blocks (pre): dark `#1A1A2E` background, `#D4D4D4` text, 7.5pt, blue left border `#0058A3`
- Blockquotes: purple left border `#8661C5`, lavender background `#F6F2FA`
- Tables: 8pt, purple header `#5B2D8E`, alternating row tint `#F8F5FC`
- Images: max-width 75%, max-height 180mm, centered, light border `#E0E0E0`
- HR: 1pt `#D6C8E8`

### References
- Triggered by `## References`, `## Referências`, or `## Referencias` heading
- Combined from **all chapters** into a single deduplicated final page
- **Always fits on exactly ONE page** — the script auto-computes font size and
  column count based on the total number of reference items:
  - ≤ ~60 items: 2 columns, 7.5pt
  - ~60–90 items: 2 columns, 7.0–6.5pt
  - ~90–130 items: 3 columns, 7.5–6.5pt
  - 130+ items: 3–4 columns, 6.5–5.5pt
- Page uses tighter margins (14mm all sides) to maximize usable space
- No page number on references page (intentional — it's an appendix)

### Page numbers
- Bottom-right, 8.5pt, `#888780`
- Cover and TOC pages: no page number
- Body pages: start at 1

---

## Handling frontmatter and images

The script automatically:
- **Strips YAML frontmatter** (any `--- ... ---` block at the top of each file)
- **Strips changelog sections** — any `## Changelog`, `## Change Log`, `## CHANGELOG`,
  or `## Histórico de Versões` heading and all content after it within the same file
  is removed before rendering
- **Resolves image paths** — `![alt](filename.png)` → `file:///absolute/path/filename.png`
  using the `images_dir` from config. If an image is not found, it is skipped gracefully.

---

## Dependencies

The script uses these Python packages. Install if missing:

```bash
pip install weasyprint markdown pypdf --break-system-packages
```

WeasyPrint renders HTML → PDF via CSS Paged Media. It handles `@page`, `page-break-*`,
and `column-count` correctly. Do not substitute with other PDF libraries (reportlab,
fpdf, pdfkit) — they do not support the CSS features used here.

---

## Troubleshooting

**Images missing in PDF**: Check `images_dir` is the correct absolute path.
The script uses `file://` URIs; relative paths won't work.

**Cover background renders white**: WeasyPrint needs `background: #0F0F0E` on `.cover-page`
plus the `page: cover` named page rule. Both are in the bundled CSS. Do not remove either.

**Chapter banners don't bleed**: The negative margins (`margin: -20mm -16mm 10mm -16mm`)
on `.chapter-header` must match the page content margins (20mm top, 16mm sides).
If you change page margins, update these values accordingly.

**Tables overflow the page**: The table CSS uses `page-break-inside: avoid`. Very large
tables may overflow; split the markdown table into smaller sections.

**References not appearing on separate page**: The heading must be exactly `## References`,
`## Referências`, or `## Referencias`. Other spellings are not detected.

**References overflowing onto a second page**: Should not happen — the script auto-scales
font and columns. If it does, individual reference items are extremely long (>300 chars).
Shorten long entries in the source markdown.
