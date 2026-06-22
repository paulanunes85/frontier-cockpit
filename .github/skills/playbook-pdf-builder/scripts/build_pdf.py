#!/usr/bin/env python3
"""
playbook-pdf-builder — bundled generator script
------------------------------------------------
Converts multiple Markdown files into a single polished PDF:
  - Dark cover page with gradient accent bar + chapter preview blocks
  - Table of Contents with colored dots
  - Per-chapter colored banner headers
  - Continuous page numbers (cover + TOC excluded)
  - Embedded images
  - References always on ONE final page: auto-scales font + column count
    to fit all references regardless of quantity

Usage:
    python3 build_pdf.py --config /tmp/playbook_config.json --output /path/to/output.pdf

Config JSON schema: see SKILL.md Step 3.
"""

import argparse
import json
import os
import re
import sys

try:
    import markdown
    from weasyprint import HTML
except ImportError:
    print("ERROR: Missing dependencies. Run:")
    print("  pip install weasyprint markdown pypdf --break-system-packages")
    sys.exit(1)

# ─── CSS template (references section is injected dynamically) ─────────────────

CSS_BASE = """
@page {
    size: A4;
    margin: 20mm 16mm 24mm 16mm;
    @bottom-right {
        content: counter(page);
        font-size: 8.5pt;
        color: #888780;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    }
}
@page cover { margin: 0; @bottom-right { content: none; } }
@page toc   { @bottom-right { content: none; } }
@page refs  { margin: 14mm 14mm 18mm 14mm; @bottom-right { content: none; } }

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.6;
    color: #2C2C2A;
}

/* ── Orphan / widow control ── */
p { orphans: 3; widows: 3; }
h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid; orphans: 3; widows: 3; }
h2 + p, h2 + ul, h2 + ol, h2 + table, h2 + pre, h2 + blockquote { page-break-before: avoid; break-before: avoid; }
h3 + p, h3 + ul, h3 + ol, h3 + table, h3 + pre, h3 + blockquote { page-break-before: avoid; break-before: avoid; }

/* ── Cover ── */
.cover-page {
    page: cover;
    page-break-after: always;
    width: 210mm;
    height: 297mm;
    background: #0F0F0E;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    overflow: hidden;
}
.cover-accent-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 6mm;
    background: linear-gradient(90deg, #F25022 0%, #FFB900 25%, #7FBA00 50%, #0078D4 75%, #8661C5 100%);
}
.cover-blocks {
    position: absolute;
    top: 18mm; right: 16mm;
    display: flex;
    flex-direction: column;
    gap: 2.5mm;
    align-items: flex-end;
}
.cover-block {
    padding: 3mm 7mm;
    border-radius: 2mm;
    font-size: 8pt;
    font-weight: 600;
    letter-spacing: 0.5pt;
    text-transform: uppercase;
    color: white;
    opacity: 0.85;
}
.cover-content { padding: 0 20mm 18mm 20mm; }
.cover-eyebrow {
    font-size: 9pt;
    letter-spacing: 2pt;
    text-transform: uppercase;
    color: #888780;
    margin-bottom: 6mm;
}
.cover-title {
    font-size: 32pt;
    font-weight: 800;
    line-height: 1.1;
    color: #FFFFFF;
    margin-bottom: 4mm;
}
.cover-subtitle {
    font-size: 13pt;
    color: #C8C6BE;
    line-height: 1.4;
    margin-bottom: 10mm;
    max-width: 140mm;
}
.cover-divider {
    width: 40mm;
    height: 0.5mm;
    background: #444;
    margin-bottom: 8mm;
}
.cover-author      { font-size: 11pt; color: #FFFFFF; font-weight: 600; margin-bottom: 2mm; }
.cover-author-role { font-size: 9pt;  color: #888780; margin-bottom: 1mm; }
.cover-date        { font-size: 9pt;  color: #888780; }

/* ── TOC ── */
.toc-page {
    page: toc;
    page-break-after: always;
    padding: 16mm 0 10mm 0;
}
.toc-title {
    font-size: 18pt;
    font-weight: 700;
    color: #5B2D8E;
    margin-bottom: 10mm;
    padding-bottom: 3mm;
    border-bottom: 1.5pt solid #D6C8E8;
}
.toc-entry {
    display: flex;
    align-items: flex-start;
    margin-bottom: 5mm;
    gap: 3mm;
}
.toc-dot {
    width: 8mm;
    height: 8mm;
    min-width: 8mm;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 7.5pt;
    font-weight: 700;
    color: white;
    margin-right: 3mm;
    margin-top: 1mm;
}
.toc-label { font-size: 11pt; font-weight: 600; color: #2C2C2A; }
.toc-desc  { font-size: 9pt;  color: #888780; margin-top: 1mm; }

/* ── Chapter banner ── */
.chapter-header {
    page-break-before: always;
    margin: -20mm -16mm 10mm -16mm;
    padding: 10mm 16mm 8mm 16mm;
    color: white;
    position: relative;
}
.chapter-eyebrow {
    font-size: 8pt;
    letter-spacing: 2pt;
    text-transform: uppercase;
    opacity: 0.75;
    margin-bottom: 3mm;
}
.chapter-title {
    font-size: 20pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 2mm;
}
.chapter-desc {
    font-size: 10pt;
    opacity: 0.8;
    line-height: 1.4;
    max-width: 145mm;
}

/* ── Body typography — editorial purple/blue palette ── */
h1 {
    font-size: 19pt; font-weight: 700; line-height: 1.2;
    color: #5B2D8E; margin-top: 14pt; margin-bottom: 10pt;
    display: none;
}
h2 {
    font-size: 13pt; font-weight: 700; color: #5B2D8E;
    border-bottom: 1.5pt solid #D6C8E8; padding-bottom: 4pt;
    margin-top: 20pt; margin-bottom: 8pt;
}
h3 {
    font-size: 10.5pt; font-weight: 600; color: #0058A3;
    margin-top: 14pt; margin-bottom: 6pt;
}
h4 {
    font-size: 9.5pt; font-weight: 600; color: #5B2D8E;
    margin-top: 12pt; margin-bottom: 5pt;
}
p   { margin-bottom: 7pt; }
em  { font-style: italic; }
strong { font-weight: 700; }
hr  { border: none; border-top: 1pt solid #D6C8E8; margin: 14pt 0; }

/* Opening italic — purple accent */
p em:only-child {
    color: #5B2D8E;
    border-left: 3pt solid #8661C5;
    padding-left: 10pt;
    display: block;
}

blockquote {
    border-left: 3pt solid #8661C5;
    background: #F6F2FA;
    padding: 8pt 14pt;
    margin: 10pt 0;
    border-radius: 0 4pt 4pt 0;
}
blockquote p { margin: 0; }

code {
    font-family: 'Consolas', 'SF Mono', 'Monaco', 'Courier New', monospace;
    font-size: 7.5pt; background: #EBF3FD; color: #0058A3;
    padding: 1pt 3pt; border-radius: 2pt;
}
pre {
    background: #1A1A2E; color: #D4D4D4;
    font-family: 'Consolas', 'SF Mono', 'Monaco', 'Courier New', monospace;
    font-size: 7.5pt; padding: 10pt 14pt; border-radius: 4pt;
    border-left: 3pt solid #0058A3;
    margin: 10pt 0; page-break-inside: avoid;
    white-space: pre-wrap; word-wrap: break-word;
}
pre code { background: none; color: inherit; padding: 0; font-size: 7.5pt; }

table {
    font-size: 8pt; width: 100%;
    border-collapse: collapse; margin: 10pt 0;
    page-break-inside: avoid;
}
th {
    background: #5B2D8E; color: white;
    font-weight: 600; padding: 5pt 8pt;
    text-align: left; font-size: 7.5pt;
}
td {
    padding: 4pt 8pt; border-bottom: 0.5pt solid #E8E6DF;
    font-size: 8pt; vertical-align: top;
}
tr:nth-child(even) td { background: #F8F5FC; }

img {
    max-width: 75%; max-height: 180mm; display: block;
    margin: 10pt auto; border-radius: 3pt;
    border: 0.5pt solid #E0E0E0;
}
ul, ol { margin-top: 0; margin-bottom: 8pt; padding-left: 18pt; }
li { margin-bottom: 3pt; }

/* ── References — injected dynamically below ── */
"""

# References CSS — injected with computed font-size and column-count
REFS_CSS_TEMPLATE = """
.references-section {{
    page: refs;
    page-break-before: always;
    page-break-after: always;
    column-count: {col_count};
    column-gap: 10pt;
    font-size: {font_size}pt;
    line-height: 1.45;
    color: #444;
}}
.references-section h2 {{
    column-span: all;
    font-size: {heading_size}pt;
    font-weight: 700;
    border-bottom: 1.5pt solid #D6C8E8;
    padding-bottom: 4pt;
    margin-bottom: 8pt;
    margin-top: 0;
    color: #5B2D8E;
}}
.references-section ul {{
    margin: 0; padding-left: 0; list-style: none;
}}
.references-section li {{
    margin-bottom: {li_spacing}pt;
    word-break: break-word;
    font-size: {font_size}pt;
    padding-left: 0;
    line-height: 1.4;
}}
"""

# ─── Reference font sizing logic ─────────────────────────────────────────────
#
# A4 usable height with 14mm top/bottom margins ≈ 269mm.
# We reserve ~14mm for the heading. So usable column height ≈ 255mm.
# At 1pt = 0.353mm, each line of text height ≈ font_size * line_height * 0.353mm
# Each ref item typically wraps to ~2 lines on average.
# We compute estimated lines per item and pick font+columns to fit.

def compute_refs_style(n_items: int) -> dict:
    """
    Given the number of reference items, return CSS parameters that
    guarantee all items fit on a single A4 page (with 14mm margins).

    Returns dict: col_count, font_size, li_spacing, heading_size
    """
    # A4 usable content height in mm with 14mm top+bottom margins
    PAGE_H_MM = 297 - 14 - 18   # 265mm
    HEADING_H_MM = 12            # reserved for "References" heading + rule
    COL_H_MM = PAGE_H_MM - HEADING_H_MM  # 253mm per column

    # Try progressively more columns and smaller fonts until it fits
    # Each ref item: ~1.7 lines average at full column width / 2 cols
    # line height in mm = font_pt * line_height_factor * 0.3528
    LINE_HEIGHT = 1.42
    MM_PER_PT   = 0.3528

    candidates = [
        # (col_count, font_size_pt, li_spacing_pt)
        (2, 7.5,  3.5),
        (2, 7.0,  3.0),
        (2, 6.5,  2.5),
        (3, 7.5,  3.5),
        (3, 7.0,  3.0),
        (3, 6.5,  2.5),
        (3, 6.0,  2.0),
        (4, 7.0,  2.5),
        (4, 6.5,  2.0),
        (4, 6.0,  2.0),
        (4, 5.5,  1.5),
    ]

    for col_count, font_pt, li_spacing in candidates:
        # chars per line at this font size and column width
        # A4 content width = 210 - 14*2 = 182mm, minus gaps
        col_gap_mm   = 10 * (col_count - 1) * 0.3528  # gap in mm
        col_w_mm     = (182 - col_gap_mm) / col_count
        chars_per_mm = 1.7 / font_pt          # empirical: ~1.7 chars/mm at any size
        chars_per_line = col_w_mm * chars_per_mm

        # estimate lines per item: ref items average ~120 chars
        avg_chars = 120
        lines_per_item = max(1.0, avg_chars / chars_per_line)

        line_h_mm = font_pt * LINE_HEIGHT * MM_PER_PT
        item_h_mm = lines_per_item * line_h_mm + li_spacing * MM_PER_PT
        items_per_col = COL_H_MM / item_h_mm

        total_capacity = items_per_col * col_count
        if total_capacity >= n_items:
            return {
                'col_count':    col_count,
                'font_size':    font_pt,
                'li_spacing':   li_spacing,
                'heading_size': min(13.0, font_pt * 1.7),
            }

    # Absolute fallback: 4 cols, 5pt — should fit even 200+ refs
    return {'col_count': 4, 'font_size': 5.5, 'li_spacing': 1.5, 'heading_size': 10.0}


# ─── Helpers ──────────────────────────────────────────────────────────────────

REF_HEADINGS = ['<h2>References</h2>', '<h2>Referências</h2>', '<h2>Referencias</h2>']

CHANGELOG_PATTERN = re.compile(
    r'\n##\s+(Changelog|Change Log|CHANGELOG|Histórico de Versões|Version History)\b[^\n]*\n'
    r'(?:(?!\n##\s).*\n)*',
    re.IGNORECASE
)

def preprocess_md(text, images_dir):
    """Strip frontmatter, changelogs, fix image paths."""
    text = re.sub(r'^---\n.*?---\n', '', text, flags=re.DOTALL)
    text = CHANGELOG_PATTERN.sub('', text)
    def fix_img(m):
        alt, fname = m.group(1), m.group(2)
        abs_path = os.path.join(images_dir, fname)
        if os.path.exists(abs_path):
            return f'![{alt}](file://{abs_path})'
        return m.group(0)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg|webp))\)', fix_img, text)
    return text

def md_to_html(text):
    exts = ['tables', 'fenced_code', 'attr_list', 'nl2br']
    return markdown.markdown(text, extensions=exts)

def split_at_references(html):
    for pat in REF_HEADINGS:
        idx = html.find(pat)
        if idx != -1:
            return html[:idx], html[idx:]
    return html, ''

# ─── HTML builders ────────────────────────────────────────────────────────────

def build_cover(cfg):
    blocks = []
    for ch in reversed(cfg['chapters']):
        num_str = 'Intro' if ch['num'] == 0 else f"{ch['num']:02d}"
        blocks.append(
            f'<div class="cover-block" style="background:{ch["color"]};">'
            f'{num_str} — {ch["label"]}</div>'
        )
    title_html = cfg.get('title_break', cfg['title']).replace('\n', '<br>')
    return f"""
<div class="cover-page">
  <div class="cover-accent-bar"></div>
  <div class="cover-blocks">{''.join(blocks)}</div>
  <div class="cover-content">
    <div class="cover-eyebrow">{cfg.get('eyebrow', 'Complete Playbook')}</div>
    <div class="cover-title">{title_html}</div>
    <div class="cover-subtitle">{cfg.get('subtitle', '')}</div>
    <div class="cover-divider"></div>
    <div class="cover-author">{cfg.get('author', '')}</div>
    <div class="cover-author-role">{cfg.get('author_title', '')}</div>
    <div class="cover-date">{cfg.get('date', '')}</div>
  </div>
</div>
"""

def build_toc(cfg):
    entries = []
    for ch in cfg['chapters']:
        num_str = '00' if ch['num'] == 0 else f"{ch['num']:02d}"
        desc = ch.get('description', '')
        entries.append(f"""
<div class="toc-entry">
  <div class="toc-dot" style="background:{ch['color']};">{num_str}</div>
  <div>
    <div class="toc-label">{ch['label']}</div>
    <div class="toc-desc">{desc}</div>
  </div>
</div>""")
    return f"""
<div class="toc-page">
  <div class="toc-title">Contents</div>
  {''.join(entries)}
</div>
"""

def build_chapter_header(ch):
    eyebrow = 'Introduction' if ch['num'] == 0 else f"Chapter {ch['num']}"
    return f"""
<div class="chapter-header" style="background:{ch['color']};">
  <div class="chapter-eyebrow">{eyebrow}</div>
  <div class="chapter-title">{ch['label']}</div>
  <div class="chapter-desc">{ch.get('description', '')}</div>
</div>
"""

def build_references_section(unique_items):
    """Build a single-page references div with auto-scaled font and columns."""
    n = len(unique_items)
    style = compute_refs_style(n)

    print(f"  References: {n} items → {style['col_count']} columns, {style['font_size']}pt")

    ref_css = REFS_CSS_TEMPLATE.format(
        col_count    = style['col_count'],
        font_size    = style['font_size'],
        li_spacing   = style['li_spacing'],
        heading_size = style['heading_size'],
    )

    items_html = ''.join(f'<li>{item}</li>' for item in unique_items)
    return ref_css, f'<div class="references-section"><h2>References</h2><ul>{items_html}</ul></div>'

# ─── Main assembly ────────────────────────────────────────────────────────────

def build_full_html(cfg):
    images_dir = cfg.get('images_dir', '')
    title      = cfg.get('title', 'Playbook')

    body_parts = []
    all_ref_items = []

    for ch in cfg['chapters']:
        fpath = ch['file']
        ch_images_dir = images_dir or os.path.dirname(fpath)

        print(f"  Processing: {os.path.basename(fpath)}")
        with open(fpath, 'r', encoding='utf-8') as f:
            raw = f.read()

        processed = preprocess_md(raw, ch_images_dir)

        # Fallback: also try chapter's own dir for images
        if ch_images_dir != images_dir:
            def fix_local(m, d=ch_images_dir):
                alt, fname = m.group(1), m.group(2)
                p = os.path.join(d, fname)
                return f'![{alt}](file://{p})' if os.path.exists(p) else m.group(0)
            processed = re.sub(
                r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg|webp))\)',
                fix_local, processed
            )

        body_html = md_to_html(processed)
        main_body, ref_html = split_at_references(body_html)

        if ref_html:
            items = re.findall(r'<li>(.*?)</li>', ref_html, re.DOTALL)
            all_ref_items.extend(items)

        body_parts.append(build_chapter_header(ch))
        body_parts.append(main_body)

    # Deduplicate references (preserve order)
    seen, unique_items = set(), []
    for item in all_ref_items:
        key = re.sub(r'\s+', ' ', item.strip())
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    # Build references section with auto-scaled CSS
    ref_css, ref_html = build_references_section(unique_items)

    full_css = CSS_BASE + ref_css

    html = (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8"/>'
        f'<title>{title}</title>'
        f'<style>{full_css}</style>'
        '</head><body>'
        + build_cover(cfg)
        + build_toc(cfg)
        + '\n'.join(body_parts)
        + ref_html
        + '</body></html>'
    )
    return html


def main():
    parser = argparse.ArgumentParser(description='Build consolidated playbook PDF')
    parser.add_argument('--config', required=True, help='Path to JSON config file')
    parser.add_argument('--output', required=True, help='Output PDF path')
    args = parser.parse_args()

    with open(args.config, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    if cfg.get('images_dir'):
        cfg['images_dir'] = os.path.abspath(cfg['images_dir'])

    print(f"Building: {cfg.get('title', 'Playbook')}")
    html = build_full_html(cfg)

    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Rendering PDF → {output_path}")
    base_url = cfg.get('images_dir') or os.path.dirname(cfg['chapters'][0]['file'])
    HTML(string=html, base_url=base_url).write_pdf(output_path)

    size_kb = os.path.getsize(output_path) // 1024
    print(f"Done: {output_path} ({size_kb} KB)")

    try:
        from pypdf import PdfReader
        r = PdfReader(output_path)
        print(f"Pages: {len(r.pages)}")
    except Exception:
        pass


if __name__ == '__main__':
    main()
