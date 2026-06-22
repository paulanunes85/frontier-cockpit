# Layout patterns

Thirteen reusable slide layouts. Each one has been visually validated in HTML and in PPTX. Mix and match across a deck. Most decks should use 6 to 8 of these patterns total.

## Table of contents

1. **Cover** — opening slide with title in 2 lines, eyebrow, meta block
2. **Agenda** — 5 numbered parts with thin separators
3. **Section divider** — dark theme, `PARTE` label, giant Roman numeral, section title and subtitle
4. **Big number** — single dominant statistic, supporting context below
5. **Before/After (2-column)** — comparison with accent bars
6. **Three pillars (3-card)** — three equal cards with accent tops
7. **Four-card spectrum** — 4 cards horizontal with cost bars below
8. **Stat-pair extremes** — two big numbers with ratio in between
9. **Donut + classes** — pie chart left, 3 detailed rows right
10. **Terminal mockup** — code/log on dark background with colored tokens
11. **FinOps layers (4-row)** — numbered rows with accent bars (full-width layout)
12. **Roadmap (3-phase)** — 3 phase rows with duration label on right
13. **Closing slide** — dark theme, contact + next step + code block

## Common elements across all patterns

### Brand header (top-left, every slide)

```javascript
// PPTX
function addBrandHeader(slide, theme = "light") {
  const inkColor = theme === "dark" ? "B8B6AE" : "5C5A52";
  const sx = 0.5, sy = 0.32, s = 0.13, gap = 0.02;
  slide.addShape(pres.shapes.RECTANGLE, { x: sx,         y: sy,         w: s, h: s, fill: { color: "F25022" }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy,       w: s, h: s, fill: { color: "7FBA00" }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx,         y: sy + s + gap, w: s, h: s, fill: { color: "00A4EF" }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy + s + gap, w: s, h: s, fill: { color: "FFB900" }, line: { type: "none" } });
  slide.addText("PAULA SILVA  |  SOFTWARE GLOBAL BLACK BELT", {
    x: 0.9, y: 0.32, w: 6, h: 0.3,
    fontFace: "JetBrains Mono", fontSize: 9, color: inkColor,
    charSpacing: 2, valign: "middle"
  });
  // Thin blue progress bar at very top
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.333, h: 0.06,
    fill: { color: "00A4EF" }, line: { type: "none" }
  });
}
```

### Page number (bottom-right, every slide)

```javascript
function addPageNumber(slide, current, total, theme = "light") {
  const inkColor = theme === "dark" ? "82807A" : "82807A";
  slide.addText(`${String(current).padStart(2, "0")} / ${total}`, {
    x: 12.0, y: 7.1, w: 1.0, h: 0.3,
    fontFace: "JetBrains Mono", fontSize: 9, color: inkColor,
    align: "right", charSpacing: 2, valign: "middle"
  });
}
```

### Eyebrow (small uppercase mono text above title)

```javascript
function addEyebrow(slide, text, color, opts = {}) {
  slide.addText(text.toUpperCase(), {
    x: opts.x || 0.5, y: opts.y || 1.0, w: opts.w || 12, h: 0.3,
    fontFace: "JetBrains Mono", fontSize: 10, bold: true, color: color || "00A4EF",
    charSpacing: 4, valign: "middle", margin: 0
  });
}
```

### Standard title (36pt, top of content area)

```javascript
function addTitle(slide, text, opts = {}) {
  slide.addText(text, {
    x: opts.x || 0.5, y: opts.y || 1.45, w: opts.w || 12.3, h: opts.h || 1.5,
    fontFace: "Inter", fontSize: opts.size || 36, bold: false, color: opts.color || "1A1A19",
    valign: "top", margin: 0
  });
}
```

## Pattern 1: Cover

Two-line title with one color shift, eyebrow, subtitle, meta block (Author/Published/Audience), decorative 4-color line at bottom.

**Critical:** title fontSize is **44pt, not 54pt**. At 54pt the title wraps and overlaps the subtitle in PPTX.

```javascript
// PPTX
s.addText([
  { text: data.cover.part1 + "\n", options: { color: "1A1A19" } },
  { text: data.cover.keyword1,    options: { color: "00A4EF" } }
], {
  x: 0.5, y: 2.0, w: 12.3, h: 3.5,
  fontFace: "Inter", fontSize: 44, bold: false,
  valign: "top", margin: 0
});

// Subtitle at y: 5.5 (not 5.0) to give room for the 2-line title
s.addText(data.cover.subtitle, {
  x: 0.5, y: 5.5, w: 11, h: 0.7,
  fontFace: "Inter", fontSize: 15, color: "5C5A52",
  valign: "top", margin: 0
});

// Meta block: 3 columns
// Autor (x: 0.5), Publicado (x: 5.0), Audiência (x: 8.0)
// Each: small charSpacing label + value

// Decorative 4-color line at y: 7.0
// 4 segments of 0.6" wide, height 0.05"
```

## Pattern 2: Agenda

Five numbered items with thin separator lines.

```javascript
const items = [data.agenda.item1, ..., data.agenda.item5];
const labels = ["PARTE I", "PARTE II", "PARTE III", "PARTE IV", "PARTE V"];
let y = 3.4;
const rowH = 0.7;
items.forEach((item, i) => {
  s.addText(labels[i], {
    x: 0.5, y, w: 1.5, h: rowH,
    fontFace: "JetBrains Mono", fontSize: 11, bold: true, color: "82807A",
    charSpacing: 3, valign: "middle", margin: 0
  });
  s.addText(item, {
    x: 2.2, y, w: 10.5, h: rowH,
    fontFace: "Inter", fontSize: 18, color: "1A1A19",
    valign: "middle", margin: 0
  });
  if (i < items.length - 1) {
    s.addShape(pres.shapes.LINE, {
      x: 0.5, y: y + rowH, w: 12.3, h: 0,
      line: { color: "E8E5DC", width: 0.5 }
    });
  }
  y += rowH;
});
```

## Pattern 3: Section divider

Dark background, `PARTE`/`PART` label, giant Roman numeral on the left, section title and subtitle underneath. This is the standard shown in the reference screenshots: four-square Microsoft mark in the top-left brand header, then `PARTE`, then `I`, `II`, `III`, etc. in the section accent color.

**Critical:** use Roman numerals (`I`, `II`, `III`, `IV`, `V`) for section dividers. Do not use `01`, `02`, etc. in HTML dividers. The label carries only the word (`PART` in EN, `PARTE` in PT-BR/ES); the numeral below carries the section number.

```javascript
function slideDivider(romanNum, title, sub, color, slideNum) {
  const s = pres.addSlide();
  s.background = { color: "0F0F0E" };  // dark
  addBrandHeader(s, "dark");

  s.addText("PARTE", {
    x: 0.5, y: 2.5, w: 4, h: 0.5,
    fontFace: "JetBrains Mono", fontSize: 14, bold: true, color: color,
    charSpacing: 6, valign: "middle", margin: 0
  });
  s.addText(romanNum, {  // "I", "II", ...
    x: 0.5, y: 2.9, w: 5, h: 3.0,
    fontFace: "Inter", fontSize: 140, bold: false, color: color,
    valign: "top", margin: 0
  });
  s.addText(title, {
    x: 6.0, y: 3.5, w: 7, h: 1.0,
    fontFace: "Inter", fontSize: 50, color: "F0F0EB",
    valign: "top", margin: 0
  });
  s.addText(sub, {
    x: 6.0, y: 4.7, w: 7, h: 1.5,
    fontFace: "Inter", fontSize: 15, color: "B8B6AE",
    valign: "top", margin: 0
  });
  addPageNumber(s, slideNum, 20, "dark");
}
```

Section colors cycle: red → green → yellow → blue → red.

## Pattern 4: Big number

Single dominant statistic (a date, a number, a percentage). Eyebrow above, title and body below.

For dates and 10-digit numbers, max font size is **110pt in mono** (anything bigger wraps to 2 lines).

For "100x" style numbers, see Pattern 8 (stat-pair) which handles superscript x.

```javascript
// PPTX (the 2026-06-01 date)
s.addText("2026-06-01", {
  x: 0.5, y: 1.6, w: 12.3, h: 2.2,
  fontFace: "JetBrains Mono", fontSize: 110, bold: false, color: "F25022",
  valign: "top", margin: 0
});
// Title at fontSize 28, h 1.2
// Body at fontSize 13
// Old-vs-new comparison row at bottom
```

## Pattern 5: Before/After (2-column)

Two equal columns with accent bars on the left of each. Label (mono uppercase), title (sans bold), body (sans).

```javascript
const colY = 3.5, colH = 3.0, colW = 5.8;

// LEFT
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: colY, w: 0.05, h: colH, fill: { color: "FFB900" }, line: { type: "none" } });
s.addText(left.label.toUpperCase(), {
  x: 0.8, y: colY + 0.1, w: colW, h: 0.3,
  fontFace: "JetBrains Mono", fontSize: 10, bold: true, color: "FFB900",
  charSpacing: 4, valign: "top", margin: 0
});
s.addText(left.title, {
  x: 0.8, y: colY + 0.5, w: colW, h: 0.7,
  fontFace: "Inter", fontSize: 22, bold: true, color: "1A1A19",
  valign: "top", margin: 0
});
s.addText(left.body, {
  x: 0.8, y: colY + 1.3, w: colW, h: 1.6,
  fontFace: "Inter", fontSize: 14, color: "5C5A52",
  valign: "top", margin: 0
});

// RIGHT (x: 7.0, accent bar color: "00A4EF")
// Same structure
```

## Pattern 6: Three pillars (3-card)

Three equal cards horizontally, each with a top accent bar (different color per card).

```javascript
const pillars = [p1, p2, p3];
const colors = ["00A4EF", "7FBA00", "FFB900"];
const cy = 4.2, cw = 3.9, ch = 2.5, gap = 0.3;
const totalW = cw * 3 + gap * 2;
const startX = (13.333 - totalW) / 2;

pillars.forEach((p, i) => {
  const x = startX + i * (cw + gap);
  s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: "F8F7F2" }, line: { color: "E8E5DC", width: 0.5 } });
  s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: 0.06, fill: { color: colors[i] }, line: { type: "none" } });
  s.addText(`0${i + 1}`, {
    x: x + 0.3, y: cy + 0.25, w: 1, h: 0.35,
    fontFace: "JetBrains Mono", fontSize: 10, bold: true, color: colors[i],
    charSpacing: 3, valign: "top", margin: 0
  });
  s.addText(p.title, { x: x + 0.3, y: cy + 0.6, w: cw - 0.6, h: 0.7, fontFace: "Inter", fontSize: 18, bold: true, color: "1A1A19", valign: "top", margin: 0 });
  s.addText(p.body,  { x: x + 0.3, y: cy + 1.4, w: cw - 0.6, h: 1.0, fontFace: "Inter", fontSize: 12, color: "5C5A52", valign: "top", margin: 0 });
});
```

## Pattern 7: Four-card spectrum (Agent autonomy spectrum)

Four cards horizontal showing a spectrum (e.g., Workflow → Augmented → Agent → Autonomous), with cost bars below each card and `$/$$/$$$/$$$$` indicators.

```javascript
const cards = [
  { label: "Workflow",  color: "00A4EF", costSegs: 1, costSym: "$" },
  { label: "Augmentado", color: "FFB900", costSegs: 2, costSym: "$$" },
  { label: "Agente",     color: "7FBA00", costSegs: 3, costSym: "$$$" },
  { label: "Autônomo",   color: "F25022", costSegs: 4, costSym: "$$$$" }
];
const cy = 3.4, cw = 2.95, ch = 2.5, gap = 0.18;
const totalW = cw * 4 + gap * 3;
const startX = (13.333 - totalW) / 2;

cards.forEach((card, i) => {
  const x = startX + i * (cw + gap);
  // ... card with top accent, label, title, body, example footer
});

// Cost bars below cards: 4 segments per card, fill segments 1..costSegs
const barY = cy + ch + 0.2, barH = 0.25;
cards.forEach((card, i) => {
  const x = startX + i * (cw + gap);
  const segW = (cw - 0.4 - 3 * 0.05) / 4;
  for (let k = 0; k < 4; k++) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.2 + k * (segW + 0.05), y: barY, w: segW, h: barH,
      fill: { color: k < card.costSegs ? card.color : "E8E5DC" }, line: { type: "none" }
    });
  }
  s.addText(card.costSym, { x: x + 0.2, y: barY + barH + 0.05, w: cw - 0.4, h: 0.3, fontFace: "JetBrains Mono", fontSize: 11, bold: true, color: card.color, valign: "top", margin: 0 });
});

// Footer: left/right arrow messages
```

## Pattern 8: Stat-pair extremes

Two extreme stats with a ratio in the middle. Common variant: "100x" with x as superscript.

```javascript
// For the "100x" inline (huge number + superscript x)
s.addText([
  { text: "100", options: { fontSize: 130, color: "00A4EF", bold: true } },
  { text: "x",   options: { fontSize: 50,  color: "00A4EF", italic: true, superscript: true } }
], {
  x: 0.5, y: 1.8, w: 6, h: 2.2,
  fontFace: "Inter",
  valign: "top", margin: 0
});

// For the GPT-5 mini "0 cr" vs Opus "7,500 cr" pair:
// Left value (90pt + 28pt cr inline)
s.addText([
  { text: "0",  options: { fontSize: 90, color: "7FBA00", bold: false } },
  { text: " cr", options: { fontSize: 28, color: "7FBA00", italic: true } }
], { x: 0.5, y: 3.0, w: 4, h: 1.5, fontFace: "Inter", valign: "top", margin: 0 });

// Ratio in middle (48pt, centered)
s.addText("7,500x", {
  x: 4.7, y: 3.55, w: 3, h: 1.0,
  fontFace: "Inter", fontSize: 48, color: "F25022",
  align: "center", valign: "top", margin: 0
});

// Right value (70pt, smaller than left because "7,500" is wider than "0")
s.addText([
  { text: "7,500", options: { fontSize: 70, color: "F25022", bold: false } },
  { text: " cr",    options: { fontSize: 24, color: "F25022", italic: true } }
], { x: 8.0, y: 3.0, w: 5.0, h: 1.5, fontFace: "Inter", valign: "top", margin: 0 });
```

**Key insight:** the bigger the digit count, the smaller the font, so both stats visually fit their column.

## Pattern 9: Donut + 3 classes

Native PowerPoint donut chart on the left, 3 detailed rows on the right. The donut is **fully editable** in PPTX.

```javascript
s.addChart(pres.charts.DOUGHNUT, [{
  name: "Token cost mix",
  labels: ["Output", "Input", "Cached"],
  values: [65, 30, 5]
}], {
  x: 0.7, y: 3.4, w: 3.5, h: 3.5,
  chartColors: ["F25022", "00A4EF", "7FBA00"],
  showLegend: true, legendPos: "b",
  legendFontFace: "JetBrains Mono", legendFontSize: 9, legendColor: "5C5A52",
  holeSize: 60,
  showValue: false
});

// 3 layer rows on right
const layers = [
  { name: "Tokens de input",  desc: "...", label: "CLASSE 1", color: "00A4EF" },
  { name: "Tokens de output", desc: "...", label: "CLASSE 2", color: "F25022" },
  { name: "Tokens cached",    desc: "...", label: "CLASSE 3", color: "7FBA00" }
];
const rowH = 1.05, rx = 5.0, rw = 7.8;
let ry = 3.5;
layers.forEach((l) => {
  // bg, accent bar, label, name, desc
});
```

## Pattern 10: Terminal mockup

A code/log block on a dark background, with macOS-style traffic lights (red/yellow/green dots) and colored tokens for input/output/cached etc.

```javascript
const tx = 6.8, ty = 2.0, tw = 6.0, th = 4.5;
// Rounded dark background
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: tx, y: ty, w: tw, h: th,
  fill: { color: "0F0F0E" }, line: { color: "1A1A1A", width: 0.5 }, rectRadius: 0.08
});
// Title bar
s.addShape(pres.shapes.RECTANGLE, { x: tx, y: ty, w: tw, h: 0.35, fill: { color: "1A1A1A" }, line: { type: "none" } });
// 3 traffic light dots
s.addShape(pres.shapes.OVAL, { x: tx + 0.15, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: "F25022" }, line: { type: "none" } });
s.addShape(pres.shapes.OVAL, { x: tx + 0.33, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: "FFB900" }, line: { type: "none" } });
s.addShape(pres.shapes.OVAL, { x: tx + 0.51, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: "7FBA00" }, line: { type: "none" } });
// Title text
s.addText("agent-session.log", { x: tx, y: ty, w: tw, h: 0.35, fontFace: "JetBrains Mono", fontSize: 9, color: "B8B6AE", align: "center", valign: "middle", margin: 0 });

// Log lines with colored tokens: $ in green, input: in blue, output: in red, cached: in green
let ly = ty + 0.5;
s.addText([
  { text: "$ ", options: { color: "7FBA00", bold: true } },
  { text: "refatorar user-service em 50 arquivos", options: { color: "F0F0EB" } }
], { x: tx + 0.25, y: ly, w: tw - 0.5, h: 0.3, fontFace: "JetBrains Mono", fontSize: 11, valign: "top", margin: 0 });
```

## Pattern 11: FinOps layers (4-row, full-width)

Numbered rows (04, 03, 02, 01 from top to bottom — like a stack), each with an accent bar, a multi-line label (mono uppercase, with line break), a title (sans bold), and a body to the right.

```javascript
const layers = [
  { num: "04", label: "Camada 4 · governança e limites",  title: "Política",      body: "...", color: "F25022" },
  { num: "03", label: "Camada 3 · dashboards e alertas",  title: "Visibilidade", body: "...", color: "FFB900" },
  { num: "02", label: "Camada 2 · práticas de engenharia", title: "Disciplina",   body: "...", color: "7FBA00" },
  { num: "01", label: "Camada 1 · plataforma e identidade", title: "Fundação",   body: "...", color: "00A4EF" }
];
let y = 3.5;
const rowH = 0.85;
layers.forEach((l) => {
  // Number (big mono, left)
  s.addText(l.num, { x: 0.5, y: y + 0.05, w: 0.8, h: rowH - 0.1, fontFace: "JetBrains Mono", fontSize: 28, color: l.color, valign: "middle", margin: 0 });
  // Accent bar
  s.addShape(pres.shapes.RECTANGLE, { x: 1.5, y, w: 0.05, h: rowH, fill: { color: l.color }, line: { type: "none" } });
  // Label (mono uppercase) — fontSize: 9, charSpacing: 2 (NOT 10/3 — that overflows)
  s.addText(l.label, { x: 1.75, y: y + 0.1, w: 3.4, h: 0.4, fontFace: "JetBrains Mono", fontSize: 9, bold: true, color: l.color, charSpacing: 2, valign: "top", margin: 0 });
  // Title — at y + 0.48 (NOT y + 0.42 — needs space for 2-line label)
  s.addText(l.title, { x: 1.75, y: y + 0.48, w: 3.4, h: 0.35, fontFace: "Inter", fontSize: 14, bold: true, color: "1A1A19", valign: "top", margin: 0 });
  // Body
  s.addText(l.body, { x: 5.4, y: y + 0.1, w: 7.5, h: rowH - 0.2, fontFace: "Inter", fontSize: 11, color: "5C5A52", valign: "middle", margin: 0 });
  y += rowH + 0.1;
});
```

## Pattern 12: Roadmap (3-phase)

3 phase rows with phase name on left, action description in middle, duration on right.

```javascript
const phases = [
  { phase: "Dias 1 a 30, baseline",   text: "...", color: "F25022", days: "30 dias" },
  { phase: "Dias 31 a 60, instrumente", text: "...", color: "FFB900", days: "30 dias" },
  { phase: "Dias 61 a 90, escala",      text: "...", color: "7FBA00", days: "30 dias" }
];
let y = 3.7;
const rowH = 1.05;
phases.forEach((p) => {
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 0.05, h: rowH, fill: { color: p.color }, line: { type: "none" } });
  s.addText(p.phase, { x: 0.75, y: y + 0.15, w: 2.5, h: 0.8, fontFace: "JetBrains Mono", fontSize: 10, bold: true, color: p.color, charSpacing: 3, valign: "top", margin: 0 });
  s.addText(p.text, { x: 3.4, y: y + 0.2, w: 7.8, h: rowH - 0.3, fontFace: "Inter", fontSize: 13, color: "1A1A19", valign: "top", margin: 0 });
  s.addText(p.days, { x: 11.4, y: y + 0.2, w: 1.5, h: 0.4, fontFace: "JetBrains Mono", fontSize: 10, color: "82807A", align: "right", valign: "top", margin: 0 });
  y += rowH + 0.1;
});
```

## Pattern 13: Closing slide

Dark theme, title spanning left half, contact + next step blocks at bottom-left, code block on the right, 4-color decorative line at footer.

```javascript
// Title (52pt)
s.addText("Tokens recompensam disciplina de engenharia.", {
  x: 0.5, y: 2.0, w: 8.5, h: 2.5,
  fontFace: "Inter", fontSize: 52, color: "F0F0EB",
  valign: "top", margin: 0
});

// Tagline (16pt italic)
s.addText("Building the future of software development with AI and Agentic DevOps.", {
  x: 0.5, y: 4.6, w: 8.5, h: 0.6,
  fontFace: "Inter", fontSize: 16, italic: true, color: "B8B6AE",
  valign: "top", margin: 0
});

// Contact block (bottom left)
s.addText([
  { text: "CONTATO\n",                    options: { fontSize: 9,  charSpacing: 3, bold: true, color: "82807A" } },
  { text: "Frontier Cockpit Team\n",                options: { fontSize: 16, bold: true,                   color: "F0F0EB" } },
  { text: "Software Global Black Belt\n", options: { fontSize: 12,                                color: "B8B6AE" } },
  { text: "frontier-cockpit@example.com",     options: { fontSize: 12,                                color: "00A4EF" } }
], { x: 0.5, y: 5.6, w: 4, h: 1.6, fontFace: "Inter", valign: "top", margin: 0 });

// Next step block (middle bottom)
// at x: 4.7

// Code block on right (x: 9.0, y: 1.8, w: 4.0, h: 4.5)
// Rounded dark background + filename + multi-line code with green comments
```

## Anti-patterns to avoid

- **Don't repeat the same layout twice in a row.** Alternate between 2-column, 3-card, big number, terminal, etc. The deck flow needs visual rhythm.
- **Don't use accent lines under titles.** These are a hallmark of AI-generated slides.
- **Don't use rounded rectangles with rectangular accent bars.** The accent won't cover the rounded corners. Use RECTANGLE for the card and a separate RECTANGLE for the accent.
- **Don't share option objects between addShape calls.** PptxGenJS mutates them in place. Use inline objects or factory functions for shadows.
- **Don't center long body text.** Center only titles and big numbers; left-align body text.
- **Use Roman numerals for HTML dividers.** Keep them visually close to the reference: large, simple, left aligned, in the section accent color. Avoid oversized 220pt+ Roman numerals in native PPTX exports if they render poorly in PowerPoint or LibreOffice; use the same Roman value at a tested size instead of switching the HTML source to Arabic numerals.
- **Don't ship a slide where the same text appears twice.** This happens when the I18N resolver fails silently — verify all keys resolve.
