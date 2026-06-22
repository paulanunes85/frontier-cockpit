/**
 * make_pptx.js: base template for generating PPTX from deck data JSON
 *
 * USAGE:
 *   This file is a TEMPLATE, not a runnable generator. Each deck has its own slide functions
 *   tailored to its content. Copy this file, customize the slide functions to match the deck
 *   structure, set CUSTOMIZED = true, then run with:
 *
 *     NODE_PATH=$(npm root -g) node make_pptx.js
 *
 * STRUCTURE:
 *   1. Setup (palette, fonts, slide layout)
 *   2. Helpers (addBrandHeader, addPageNumber, addEyebrow, addTitle, plainNote, richText)
 *   3. Pattern functions for each slide layout (cover, divider, 3-card, 4-card, etc.)
 *   4. slideN() functions, one per slide in the deck, calling the pattern functions
 *   5. Set CUSTOMIZED = true, execute all slideN(), and write the file
 *
 * DEPENDENCIES:
 *   npm install pptxgenjs        (local)
 *   npm install -g pptxgenjs     (global)
 *
 * SEE ALSO:
 *   references/pptx-mapping.md: full font size cheat sheet and pitfalls
 *   references/patterns.md: code snippets for each pattern
 */

let pptxgen;
try {
  pptxgen = require("pptxgenjs");
} catch {
  console.error("ERROR: pptxgenjs is not installed.");
  console.error("  npm install pptxgenjs        (local)");
  console.error("  npm install -g pptxgenjs     (global)");
  console.error("  then run: NODE_PATH=$(npm root -g) node make_pptx.js");
  process.exit(2);
}
const fs = require("fs");

// =============================================================================
// CONFIG
// =============================================================================
const DATA_PATH = "./deck_data.json";
const OUTPUT_PATH = "./output_deck.pptx";

// Set to true ONLY after you have customized the EXECUTE block below for THIS deck.
// The bare template must never produce an empty PPTX.
const CUSTOMIZED = false;

if (!fs.existsSync(DATA_PATH)) {
  console.error(`ERROR: data file not found: ${DATA_PATH}`);
  console.error("  Export the deck I18N to JSON first (see references/pptx-mapping.md).");
  process.exit(2);
}

const data = JSON.parse(fs.readFileSync(DATA_PATH, "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333" × 7.5"
pres.author = "Frontier Cockpit Team";
pres.company = "Microsoft";
pres.title = data.cover?.part1 || "Deck title";

// =============================================================================
// PALETTE
// =============================================================================
const C = {
  red: "F25022",   redLight: "FCE9E3",
  green: "7FBA00", greenLight: "F1F8E3",
  yellow: "FFB900", yellowLight: "FFF7E0",
  blue: "00A4EF",   blueLight: "DDF3FD",
  ink: "1A1A19", ink2: "5C5A52", ink3: "82807A",
  paper: "F8F7F2", rule: "E8E5DC", bg: "FFFFFF",
  darkBg: "0F0F0E", darkInk: "F0F0EB", darkInk2: "B8B6AE", darkInk3: "82807A",
};

const FONT_SANS = "Inter";
const FONT_MONO = "JetBrains Mono";

// =============================================================================
// HELPERS
// =============================================================================
function addBrandHeader(slide, theme = "light") {
  const inkColor = theme === "dark" ? C.darkInk2 : C.ink2;
  const sx = 0.5, sy = 0.32, s = 0.13, gap = 0.02;
  slide.addShape(pres.shapes.RECTANGLE, { x: sx,         y: sy,         w: s, h: s, fill: { color: C.red },    line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy,       w: s, h: s, fill: { color: C.green },  line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx,         y: sy + s + gap, w: s, h: s, fill: { color: C.blue },   line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy + s + gap, w: s, h: s, fill: { color: C.yellow }, line: { type: "none" } });
  slide.addText("PAULA SILVA  |  SOFTWARE GLOBAL BLACK BELT", {
    x: 0.9, y: 0.32, w: 6, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: inkColor,
    charSpacing: 2, valign: "middle",
  });
  // Thin blue progress bar at very top
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.333, h: 0.06,
    fill: { color: C.blue }, line: { type: "none" },
  });
}

function addPageNumber(slide, current, total, theme = "light") {
  const inkColor = theme === "dark" ? C.darkInk3 : C.ink3;
  slide.addText(`${String(current).padStart(2, "0")} / ${total}`, {
    x: 12.0, y: 7.1, w: 1.0, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: inkColor,
    align: "right", charSpacing: 2, valign: "middle",
  });
}

function addEyebrow(slide, text, color, opts = {}) {
  slide.addText(text.toUpperCase(), {
    x: opts.x || 0.5, y: opts.y || 1.0, w: opts.w || 12, h: 0.3,
    fontFace: FONT_MONO, fontSize: 10, bold: true, color: color || C.blue,
    charSpacing: 4, valign: "middle", margin: 0,
  });
}

function addTitle(slide, text, opts = {}) {
  slide.addText(text, {
    x: opts.x || 0.5, y: opts.y || 1.45, w: opts.w || 12.3, h: opts.h || 1.5,
    fontFace: FONT_SANS, fontSize: opts.size || 36, bold: false, color: opts.color || C.ink,
    valign: "top", margin: 0,
  });
}

/**
 * Strips markdown lite (**bold**, *italic*) from speaker notes for plain-text PPTX notes.
 * Keeps markers like [ABERTURA] and [pausa] visible.
 */
function plainNote(text) {
  if (!text) return "";
  return text.replace(/\*\*/g, "").replace(/\*/g, "").trim();
}

// =============================================================================
// PATTERN: SECTION DIVIDER (slides 3, 6, 10, 14, 17 typically)
// CRITICAL: use Roman numerals (I, II, III) for section dividers, matching the HTML source
// =============================================================================
function slideDivider(romanNum, title, sub, color, slideNum, total) {
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  addBrandHeader(s, "dark");
  s.addText("PARTE", {
    x: 0.5, y: 2.5, w: 4, h: 0.5,
    fontFace: FONT_MONO, fontSize: 14, bold: true, color: color,
    charSpacing: 6, valign: "middle", margin: 0,
  });
  s.addText(romanNum, {
    x: 0.5, y: 2.9, w: 5, h: 3.0,
    fontFace: FONT_SANS, fontSize: 140, bold: true, color: color,
    valign: "top", margin: 0,
  });
  s.addText(title, {
    x: 6.0, y: 3.5, w: 7, h: 1.0,
    fontFace: FONT_SANS, fontSize: 50, color: C.darkInk,
    valign: "top", margin: 0,
  });
  s.addText(sub, {
    x: 6.0, y: 4.7, w: 7, h: 1.5,
    fontFace: FONT_SANS, fontSize: 15, color: C.darkInk2,
    valign: "top", margin: 0,
  });
  addPageNumber(s, slideNum, total, "dark");
  s.addNotes(plainNote(data.notes[`s${slideNum}`]));
}

// =============================================================================
// PATTERN: COVER (slide 1)
// CRITICAL: title fontSize is 44pt, NOT 54pt (54 wraps to 3 lines and overlaps subtitle)
// =============================================================================
function slideCover(slideNum, total) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);

  addEyebrow(s, data.cover.eyebrow, C.blue, { x: 0.5, y: 1.6 });

  // 2-line title (line 1 black, line 2 blue)
  s.addText([
    { text: data.cover.part1 + "\n", options: { color: C.ink } },
    { text: data.cover.keyword1 || "", options: { color: C.blue } },
  ], {
    x: 0.5, y: 2.0, w: 12.3, h: 3.5,
    fontFace: FONT_SANS, fontSize: 44, bold: false,
    valign: "top", margin: 0,
  });

  s.addText(data.cover.subtitle, {
    x: 0.5, y: 5.5, w: 11, h: 0.7,
    fontFace: FONT_SANS, fontSize: 15, color: C.ink2,
    valign: "top", margin: 0,
  });

  // Meta block (Author, Published, Audience)
  s.addText([
    { text: "Autor\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: "Frontier Cockpit Team\nSoftware Global Black Belt", options: { color: C.ink, fontSize: 12 } },
  ], { x: 0.5, y: 6.2, w: 3, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });

  s.addText([
    { text: "Publicado\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: data.meta?.date || "2026-XX-XX", options: { color: C.ink, fontSize: 12 } },
  ], { x: 5.0, y: 6.2, w: 2.5, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });

  s.addText([
    { text: "Audiência\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: data.meta?.audience || "", options: { color: C.ink, fontSize: 12 } },
  ], { x: 8.0, y: 6.2, w: 5, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });

  // Decorative 4-color line at bottom
  const lineY = 7.0, segW = 0.6, segH = 0.05;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5,           y: lineY, w: segW, h: segH, fill: { color: C.red },    line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW,    y: lineY, w: segW, h: segH, fill: { color: C.green },  line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW*2,  y: lineY, w: segW, h: segH, fill: { color: C.yellow }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW*3,  y: lineY, w: segW, h: segH, fill: { color: C.blue },   line: { type: "none" } });

  addPageNumber(s, slideNum, total);
  s.addNotes(plainNote(data.notes[`s${slideNum}`]));
}

// =============================================================================
// PATTERN: AGENDA (slide 2 typically)
// 5 items, mono labels on left, sans titles on right, thin separator lines
// =============================================================================
function slideAgenda(slideNum, total) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, "AGENDA", C.blue);
  addTitle(s, data.agenda.title);

  const items = [data.agenda.item1, data.agenda.item2, data.agenda.item3, data.agenda.item4, data.agenda.item5];
  const labels = ["PARTE I", "PARTE II", "PARTE III", "PARTE IV", "PARTE V"];
  let y = 3.4;
  const rowH = 0.7;
  items.forEach((item, i) => {
    s.addText(labels[i], { x: 0.5, y, w: 1.5, h: rowH, fontFace: FONT_MONO, fontSize: 11, bold: true, color: C.ink3, charSpacing: 3, valign: "middle", margin: 0 });
    s.addText(item, { x: 2.2, y, w: 10.5, h: rowH, fontFace: FONT_SANS, fontSize: 18, color: C.ink, valign: "middle", margin: 0 });
    if (i < items.length - 1) {
      s.addShape(pres.shapes.LINE, { x: 0.5, y: y + rowH, w: 12.3, h: 0, line: { color: C.rule, width: 0.5 } });
    }
    y += rowH;
  });

  addPageNumber(s, slideNum, total);
  s.addNotes(plainNote(data.notes[`s${slideNum}`]));
}

// =============================================================================
// EXECUTE
// =============================================================================
// Customize this block to match your deck. Reference patterns.md for each pattern's code.
// Common deck structure:
//   slide 1: slideCover
//   slide 2: slideAgenda
//   slides 3, 6, 10, 14, 17: slideDivider (Parts I-V)
//   other slides: custom functions using patterns from references/patterns.md
//
// Example:
//   slideCover(1, 20);
//   slideAgenda(2, 20);
//   slideDivider("I", data.part1.title, data.part1.sub, C.red, 3, 20);
//   slideBigNumber(...);  // slide 4
//   slideTwoColumn(...);  // slide 5
//   slideDivider("II", data.part2.title, data.part2.sub, C.green, 6, 20);
//   ...

console.log("Customize the execute block in make_pptx.js to call your slide functions.");
console.log("Then set CUSTOMIZED = true at the top of this file.");

if (!CUSTOMIZED) {
  console.error("ERROR: make_pptx.js is an uncustomized template; refusing to write an empty PPTX.");
  console.error("  1. Copy this file per deck.");
  console.error("  2. Add slideN() calls in the EXECUTE block to build every slide.");
  console.error("  3. Set CUSTOMIZED = true.");
  console.error("  See references/pptx-mapping.md and references/patterns.md.");
  process.exit(2);
}

pres.writeFile({ fileName: OUTPUT_PATH }).then(() => {
  console.log("Wrote: " + OUTPUT_PATH);
});
