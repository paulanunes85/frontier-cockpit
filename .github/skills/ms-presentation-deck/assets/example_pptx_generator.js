const pptxgen = require("pptxgenjs");
const fs = require("fs");

const data = JSON.parse(fs.readFileSync("./output/deck_data_pt.json", "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Frontier Cockpit Team";
pres.company = "Microsoft";
pres.title = "Gestão de tokens e design de agentes";

const C = {
  red: "F25022", redLight: "FCE9E3", red700: "C13E1A",
  green: "7FBA00", greenLight: "F1F8E3", green700: "5A8500",
  yellow: "FFB900", yellowLight: "FFF7E0", yellow700: "B88500",
  blue: "00A4EF", blueLight: "DDF3FD", blue700: "0076AC",
  ink: "1A1A19", ink2: "5C5A52", ink3: "82807A",
  paper: "F8F7F2", rule: "E8E5DC", bg: "FFFFFF",
  darkBg: "0F0F0E", darkInk: "F0F0EB", darkInk2: "B8B6AE", darkInk3: "82807A",
};

const FONT_SANS = "Inter";
const FONT_MONO = "JetBrains Mono";

function addBrandHeader(slide, theme = "light") {
  const inkColor = theme === "dark" ? C.darkInk2 : C.ink2;
  const sx = 0.5, sy = 0.32, s = 0.13, gap = 0.02;
  slide.addShape(pres.shapes.RECTANGLE, { x: sx, y: sy, w: s, h: s, fill: { color: C.red }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy, w: s, h: s, fill: { color: C.green }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx, y: sy + s + gap, w: s, h: s, fill: { color: C.blue }, line: { type: "none" } });
  slide.addShape(pres.shapes.RECTANGLE, { x: sx + s + gap, y: sy + s + gap, w: s, h: s, fill: { color: C.yellow }, line: { type: "none" } });
  slide.addText("PAULA SILVA  |  SOFTWARE GLOBAL BLACK BELT", {
    x: 0.9, y: 0.32, w: 6, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: inkColor,
    charSpacing: 2, valign: "middle",
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 13.333, h: 0.06,
    fill: { color: C.blue }, line: { type: "none" },
  });
}

function addPageNumber(slide, current, total, theme = "light") {
  const inkColor = theme === "dark" ? C.darkInk3 : C.ink3;
  slide.addText(String(current).padStart(2, "0") + " / " + total, {
    x: 12.0, y: 7.1, w: 1.0, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: inkColor,
    align: "right", charSpacing: 2, valign: "middle",
  });
}

function addEyebrow(slide, text, color, opts) {
  opts = opts || {};
  slide.addText(text.toUpperCase(), {
    x: opts.x || 0.5, y: opts.y || 1.0, w: opts.w || 12, h: 0.3,
    fontFace: FONT_MONO, fontSize: 10, bold: true, color: color || C.blue,
    charSpacing: 4, valign: "middle", margin: 0,
  });
}

function addTitle(slide, text, opts) {
  opts = opts || {};
  slide.addText(text, {
    x: opts.x || 0.5, y: opts.y || 1.45, w: opts.w || 12.3, h: opts.h || 1.5,
    fontFace: FONT_SANS, fontSize: opts.size || 36, bold: false, color: opts.color || C.ink,
    valign: "top", margin: 0,
  });
}

function plainNote(text) {
  if (!text) return "";
  return text.replace(/\*\*/g, "").replace(/\*/g, "").trim();
}

function slide1() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.cover.eyebrow, C.blue, { x: 0.5, y: 1.6 });
  const lines = [data.cover.part1, data.cover.keyword1];
  s.addText([
    { text: lines[0] + "\n", options: { color: C.ink } },
    { text: lines[1] || "", options: { color: C.blue } },
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
  s.addText([
    { text: "Autor\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: "Frontier Cockpit Team\nSoftware Global Black Belt", options: { color: C.ink, fontSize: 12 } },
  ], { x: 0.5, y: 6.2, w: 3, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });
  s.addText([
    { text: "Publicado\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: "2026-05-28", options: { color: C.ink, fontSize: 12 } },
  ], { x: 5.0, y: 6.2, w: 2.5, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });
  s.addText([
    { text: "Audiência\n", options: { color: C.ink3, fontSize: 9, charSpacing: 2, bold: true } },
    { text: "Líderes de engenharia, FinOps, plataforma", options: { color: C.ink, fontSize: 12 } },
  ], { x: 8.0, y: 6.2, w: 5, h: 0.8, fontFace: FONT_MONO, valign: "top", margin: 0 });
  const lineY = 7.0, segW = 0.6, segH = 0.05;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: lineY, w: segW, h: segH, fill: { color: C.red }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW, y: lineY, w: segW, h: segH, fill: { color: C.green }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW * 2, y: lineY, w: segW, h: segH, fill: { color: C.yellow }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW * 3, y: lineY, w: segW, h: segH, fill: { color: C.blue }, line: { type: "none" } });
  addPageNumber(s, 1, 20);
  s.addNotes(plainNote(data.notes.s1));
}

function slide2() {
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
    s.addText(labels[i], {
      x: 0.5, y: y, w: 1.5, h: rowH,
      fontFace: FONT_MONO, fontSize: 11, bold: true, color: C.ink3,
      charSpacing: 3, valign: "middle", margin: 0,
    });
    s.addText(item, {
      x: 2.2, y: y, w: 10.5, h: rowH,
      fontFace: FONT_SANS, fontSize: 18, color: C.ink,
      valign: "middle", margin: 0,
    });
    if (i < items.length - 1) {
      s.addShape(pres.shapes.LINE, {
        x: 0.5, y: y + rowH, w: 12.3, h: 0,
        line: { color: C.rule, width: 0.5 },
      });
    }
    y += rowH;
  });
  addPageNumber(s, 2, 20);
  s.addNotes(plainNote(data.notes.s2));
}

function slideDivider(num, romanNum, title, sub, color, slideNum) {
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
  addPageNumber(s, slideNum, 20, "dark");
  s.addNotes(plainNote(data.notes["s" + slideNum]));
}

function slide3() {
  slideDivider(1, "I", data.part1.title || "O fato",
    data.part1.sub || "O que muda em 1 de junho de 2026, e por que isso importa", C.red, 3);
}

function slide4() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.june.eyebrow, C.red);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 3.0, y: 0.97, w: 2.2, h: 0.35,
    fill: { color: C.redLight }, line: { type: "none" }, rectRadius: 0.15,
  });
  s.addText("● T-MINUS COUNTDOWN", {
    x: 3.0, y: 0.97, w: 2.2, h: 0.35,
    fontFace: FONT_MONO, fontSize: 9, bold: true, color: C.red,
    charSpacing: 3, align: "center", valign: "middle", margin: 0,
  });
  s.addText("2026-06-01", {
    x: 0.5, y: 1.6, w: 12.3, h: 2.2,
    fontFace: FONT_MONO, fontSize: 110, bold: false, color: C.red,
    valign: "top", margin: 0,
  });
  addTitle(s, data.june.title, { y: 3.9, size: 28, h: 1.2 });
  s.addText(data.june.body, {
    x: 0.5, y: 5.1, w: 11.5, h: 1.4,
    fontFace: FONT_SANS, fontSize: 13, color: C.ink2,
    valign: "top", margin: 0,
  });
  s.addShape(pres.shapes.LINE, {
    x: 0.5, y: 6.7, w: 6, h: 0,
    line: { color: C.rule, width: 0.5 },
  });
  s.addText([
    { text: "UNIDADE ANTIGA\n", options: { fontSize: 8, charSpacing: 3, bold: true, color: C.ink3 } },
    { text: "1 PRU", options: { fontSize: 12, color: C.ink } },
  ], { x: 0.5, y: 6.85, w: 1.5, h: 0.5, fontFace: FONT_MONO, valign: "top", margin: 0 });
  s.addText("→", {
    x: 1.8, y: 6.95, w: 0.3, h: 0.4,
    fontFace: FONT_MONO, fontSize: 14, color: C.ink3,
    valign: "middle", align: "center", margin: 0,
  });
  s.addText([
    { text: "UNIDADE NOVA\n", options: { fontSize: 8, charSpacing: 3, bold: true, color: C.red } },
    { text: "1 credit = US$ 0,01", options: { fontSize: 12, color: C.ink } },
  ], { x: 2.3, y: 6.85, w: 3, h: 0.5, fontFace: FONT_MONO, valign: "top", margin: 0 });
  addPageNumber(s, 4, 20);
  s.addNotes(plainNote(data.notes.s4));
}

function slide5() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.pruvs.eyebrow, C.yellow);
  addTitle(s, data.pruvs.title);
  const colY = 3.5, colH = 3.0, colW = 5.8;
  // LEFT
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: colY, w: 0.05, h: colH, fill: { color: C.yellow }, line: { type: "none" } });
  s.addText(data.pruvs.left.label.toUpperCase(), {
    x: 0.8, y: colY + 0.1, w: colW, h: 0.3,
    fontFace: FONT_MONO, fontSize: 10, bold: true, color: C.yellow,
    charSpacing: 4, valign: "top", margin: 0,
  });
  s.addText(data.pruvs.left.title, {
    x: 0.8, y: colY + 0.5, w: colW, h: 0.7,
    fontFace: FONT_SANS, fontSize: 22, bold: true, color: C.ink,
    valign: "top", margin: 0,
  });
  s.addText(data.pruvs.left.body, {
    x: 0.8, y: colY + 1.3, w: colW, h: 1.6,
    fontFace: FONT_SANS, fontSize: 14, color: C.ink2,
    valign: "top", margin: 0,
  });
  // RIGHT
  const rightX = 7.0;
  s.addShape(pres.shapes.RECTANGLE, { x: rightX, y: colY, w: 0.05, h: colH, fill: { color: C.blue }, line: { type: "none" } });
  s.addText(data.pruvs.right.label.toUpperCase(), {
    x: rightX + 0.3, y: colY + 0.1, w: colW, h: 0.3,
    fontFace: FONT_MONO, fontSize: 10, bold: true, color: C.blue,
    charSpacing: 4, valign: "top", margin: 0,
  });
  s.addText(data.pruvs.right.title, {
    x: rightX + 0.3, y: colY + 0.5, w: colW, h: 0.7,
    fontFace: FONT_SANS, fontSize: 22, bold: true, color: C.ink,
    valign: "top", margin: 0,
  });
  s.addText(data.pruvs.right.body, {
    x: rightX + 0.3, y: colY + 1.3, w: colW, h: 1.6,
    fontFace: FONT_SANS, fontSize: 14, color: C.ink2,
    valign: "top", margin: 0,
  });
  addPageNumber(s, 5, 20);
  s.addNotes(plainNote(data.notes.s5));
}

function slide6() {
  slideDivider(2, "II", data.part2.title || "Fundamentos",
    data.part2.sub || "A linguagem que precisamos compartilhar", C.green, 6);
}

function slide7() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.token.eyebrow, C.blue);
  addTitle(s, data.token.title, { size: 32 });
  const pillars = [data.token.p1, data.token.p2, data.token.p3];
  const colors = [C.blue, C.green, C.yellow];
  const cy = 4.2, cw = 3.9, ch = 2.5, gap = 0.3;
  const totalW = cw * 3 + gap * 2;
  const startX = (13.333 - totalW) / 2;
  pillars.forEach((p, i) => {
    const x = startX + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.paper }, line: { color: C.rule, width: 0.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: 0.06, fill: { color: colors[i] }, line: { type: "none" } });
    s.addText("0" + (i + 1), {
      x: x + 0.3, y: cy + 0.25, w: 1, h: 0.35,
      fontFace: FONT_MONO, fontSize: 10, bold: true, color: colors[i],
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(p.title, {
      x: x + 0.3, y: cy + 0.6, w: cw - 0.6, h: 0.7,
      fontFace: FONT_SANS, fontSize: 18, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(p.body, {
      x: x + 0.3, y: cy + 1.4, w: cw - 0.6, h: 1.0,
      fontFace: FONT_SANS, fontSize: 12, color: C.ink2,
      valign: "top", margin: 0,
    });
  });
  addPageNumber(s, 7, 20);
  s.addNotes(plainNote(data.notes.s7));
}

function slide8() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.ioc.eyebrow, C.blue);
  addTitle(s, data.ioc.title, { size: 32 });
  // Donut chart
  s.addChart(pres.charts.DOUGHNUT, [{
    name: "Token cost mix",
    labels: [data.ioc.chartL2 || "Output", data.ioc.chartL1 || "Input", data.ioc.chartL3 || "Cached"],
    values: [65, 30, 5],
  }], {
    x: 0.7, y: 3.4, w: 3.5, h: 3.5,
    chartColors: [C.red, C.blue, C.green],
    showLegend: true, legendPos: "b",
    legendFontFace: FONT_MONO, legendFontSize: 9, legendColor: C.ink2,
    holeSize: 60,
    showValue: false,
  });
  s.addText(data.ioc.chartCaption || "Mix típico em sessão agêntica", {
    x: 0.7, y: 3.1, w: 3.5, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: C.ink3,
    align: "center", charSpacing: 2, valign: "middle", margin: 0,
  });
  const layers = [
    { name: data.ioc.l1.name, desc: data.ioc.l1.desc, label: "CLASSE 1", color: C.blue },
    { name: data.ioc.l2.name, desc: data.ioc.l2.desc, label: "CLASSE 2", color: C.red },
    { name: data.ioc.l3.name, desc: data.ioc.l3.desc, label: "CLASSE 3", color: C.green },
  ];
  const rowH = 1.05, rx = 5.0, rw = 7.8;
  let ry = 3.5;
  layers.forEach((l) => {
    s.addShape(pres.shapes.RECTANGLE, { x: rx, y: ry, w: rw, h: rowH, fill: { color: C.paper }, line: { type: "none" } });
    s.addShape(pres.shapes.RECTANGLE, { x: rx, y: ry, w: 0.05, h: rowH, fill: { color: l.color }, line: { type: "none" } });
    s.addText(l.label, {
      x: rx + 0.25, y: ry + 0.15, w: 1.5, h: 0.25,
      fontFace: FONT_MONO, fontSize: 9, bold: true, color: l.color,
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(l.name, {
      x: rx + 0.25, y: ry + 0.4, w: 1.7, h: 0.4,
      fontFace: FONT_SANS, fontSize: 14, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(l.desc, {
      x: rx + 2.0, y: ry + 0.15, w: rw - 2.2, h: rowH - 0.3,
      fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
      valign: "middle", margin: 0,
    });
    ry += rowH + 0.08;
  });
  addPageNumber(s, 8, 20);
  s.addNotes(plainNote(data.notes.s8));
}

function slide9() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.ctxe.eyebrow, C.green);
  addTitle(s, data.ctxe.title, { size: 30 });
  const disciplines = [
    { layer: data.ctxe.p1.layer, title: data.ctxe.p1.title, body: data.ctxe.p1.body, color: C.green },
    { layer: data.ctxe.p2.layer, title: data.ctxe.p2.title, body: data.ctxe.p2.body, color: C.blue },
    { layer: data.ctxe.p3.layer, title: data.ctxe.p3.title, body: data.ctxe.p3.body, color: C.yellow },
  ];
  const cy = 4.2, cw = 3.95, ch = 2.6, gap = 0.25;
  const totalW = cw * 3 + gap * 2;
  const startX = (13.333 - totalW) / 2;
  disciplines.forEach((d, i) => {
    const x = startX + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.paper }, line: { color: C.rule, width: 0.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: 0.08, fill: { color: d.color }, line: { type: "none" } });
    s.addText(d.layer, {
      x: x + 0.3, y: cy + 0.3, w: cw - 0.6, h: 0.3,
      fontFace: FONT_MONO, fontSize: 9, bold: true, color: d.color,
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(d.title, {
      x: x + 0.3, y: cy + 0.7, w: cw - 0.6, h: 0.8,
      fontFace: FONT_SANS, fontSize: 17, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(d.body, {
      x: x + 0.3, y: cy + 1.6, w: cw - 0.6, h: 0.95,
      fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
      valign: "top", margin: 0,
    });
  });
  addPageNumber(s, 9, 20);
  s.addNotes(plainNote(data.notes.s9));
}

function slide10() {
  slideDivider(3, "III", data.part3.title || "O custo real",
    data.part3.sub || "Onde o dinheiro de fato flui", C.yellow, 10);
}

function slide11() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.gap.eyebrow, C.blue);
  s.addText([
    { text: "100", options: { fontSize: 130, color: C.blue, bold: true } },
    { text: "x", options: { fontSize: 50, color: C.blue, italic: true, superscript: true } },
  ], {
    x: 0.5, y: 1.8, w: 6, h: 2.2,
    fontFace: FONT_SANS,
    valign: "top", margin: 0,
  });
  s.addText(data.gap.title, {
    x: 0.5, y: 4.1, w: 5.8, h: 1.8,
    fontFace: FONT_SANS, fontSize: 19, color: C.ink,
    valign: "top", margin: 0,
  });
  s.addText(data.gap.body, {
    x: 0.5, y: 6.1, w: 5.8, h: 1.0,
    fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
    valign: "top", margin: 0,
  });
  // Terminal
  const tx = 6.8, ty = 2.0, tw = 6.0, th = 4.5;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: tx, y: ty, w: tw, h: th,
    fill: { color: C.darkBg }, line: { color: "1A1A1A", width: 0.5 }, rectRadius: 0.08,
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: tx, y: ty, w: tw, h: 0.35,
    fill: { color: "1A1A1A" }, line: { type: "none" },
  });
  s.addShape(pres.shapes.OVAL, { x: tx + 0.15, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: C.red }, line: { type: "none" } });
  s.addShape(pres.shapes.OVAL, { x: tx + 0.33, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: C.yellow }, line: { type: "none" } });
  s.addShape(pres.shapes.OVAL, { x: tx + 0.51, y: ty + 0.11, w: 0.13, h: 0.13, fill: { color: C.green }, line: { type: "none" } });
  s.addText("agent-session.log", {
    x: tx, y: ty, w: tw, h: 0.35,
    fontFace: FONT_MONO, fontSize: 9, color: "B8B6AE",
    align: "center", valign: "middle", margin: 0,
  });
  let ly = ty + 0.5;
  s.addText([
    { text: "$ ", options: { color: C.green, bold: true } },
    { text: "refatorar user-service em 50 arquivos", options: { color: C.darkInk } },
  ], { x: tx + 0.25, y: ly, w: tw - 0.5, h: 0.3, fontFace: FONT_MONO, fontSize: 11, valign: "top", margin: 0 });
  ly += 0.4;
  const turnLines = [
    ["turno 01", "input: 12,400", "output: 8,200", "cached: 0"],
    ["turno 02", "input: 18,900", "output: 12,500", "cached: 11,200"],
    ["turno 03", "input: 24,100", "output: 19,800", "cached: 17,400"],
    ["…", "", "", ""],
    ["turno 87", "input: 31,200", "output: 28,400", "cached: 28,900"],
  ];
  turnLines.forEach(([turno, inp, out, cch]) => {
    const parts = [{ text: "  " + turno, options: { color: C.darkInk2 } }];
    if (inp) parts.push({ text: " · ", options: { color: C.darkInk3 } }, { text: inp, options: { color: C.blue } });
    if (out) parts.push({ text: " · ", options: { color: C.darkInk3 } }, { text: out, options: { color: C.red } });
    if (cch) parts.push({ text: " · ", options: { color: C.darkInk3 } }, { text: cch, options: { color: C.green } });
    s.addText(parts, { x: tx + 0.25, y: ly, w: tw - 0.5, h: 0.3, fontFace: FONT_MONO, fontSize: 10, valign: "top", margin: 0 });
    ly += 0.32;
  });
  ly += 0.15;
  s.addText([
    { text: "total: ", options: { color: C.yellow, bold: true } },
    { text: "4.2M input ", options: { color: C.blue } },
    { text: "· ", options: { color: C.darkInk3 } },
    { text: "2.8M output ", options: { color: C.red } },
    { text: "· ", options: { color: C.darkInk3 } },
    { text: "2.1M cached", options: { color: C.green } },
  ], { x: tx + 0.25, y: ly, w: tw - 0.5, h: 0.3, fontFace: FONT_MONO, fontSize: 11, valign: "top", margin: 0 });
  ly += 0.32;
  s.addText([
    { text: "custo: ", options: { color: C.yellow, bold: true } },
    { text: "~12,400 credits ≈ US$ 124.00", options: { color: C.darkInk } },
  ], { x: tx + 0.25, y: ly, w: tw - 0.5, h: 0.3, fontFace: FONT_MONO, fontSize: 11, valign: "top", margin: 0 });
  addPageNumber(s, 11, 20);
  s.addNotes(plainNote(data.notes.s11));
}

function slide12() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.rates.eyebrow, C.yellow);
  addTitle(s, data.rates.title, { size: 26, h: 0.9 });
  const spY = 2.7;
  s.addText("MODELO DEFAULT · OUTPUT", {
    x: 0.5, y: spY, w: 4, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, bold: true, color: C.ink3,
    charSpacing: 3, valign: "top", margin: 0,
  });
  s.addText([
    { text: "0", options: { fontSize: 90, color: C.green, bold: false } },
    { text: " cr", options: { fontSize: 28, color: C.green, italic: true } },
  ], { x: 0.5, y: spY + 0.3, w: 4, h: 1.5, fontFace: FONT_SANS, valign: "top", margin: 0 });
  s.addText("GPT-5 mini, incluído no plano base", {
    x: 0.5, y: spY + 2.0, w: 4, h: 0.5,
    fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
    valign: "top", margin: 0,
  });
  s.addText("RAZÃO DE CUSTO", {
    x: 4.7, y: spY + 0.5, w: 3, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, bold: true, color: C.ink3,
    charSpacing: 3, align: "center", valign: "top", margin: 0,
  });
  s.addText("7,500x", {
    x: 4.7, y: spY + 0.85, w: 3, h: 1.0,
    fontFace: FONT_SANS, fontSize: 48, color: C.red,
    align: "center", valign: "top", margin: 0,
  });
  s.addText("por milhão de tokens de output", {
    x: 4.7, y: spY + 1.85, w: 3, h: 0.4,
    fontFace: FONT_MONO, fontSize: 9, color: C.ink3,
    align: "center", charSpacing: 2, valign: "top", margin: 0,
  });
  s.addText("MODELO RESERVADO · OUTPUT", {
    x: 8.0, y: spY, w: 4.5, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, bold: true, color: C.ink3,
    charSpacing: 3, valign: "top", margin: 0,
  });
  s.addText([
    { text: "7,500", options: { fontSize: 70, color: C.red, bold: false } },
    { text: " cr", options: { fontSize: 24, color: C.red, italic: true } },
  ], { x: 8.0, y: spY + 0.3, w: 5.0, h: 1.5, fontFace: FONT_SANS, valign: "top", margin: 0 });
  s.addText("Claude Opus 4.7, uso reservado", {
    x: 8.0, y: spY + 2.0, w: 4.8, h: 0.5,
    fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
    valign: "top", margin: 0,
  });
  const tableData = [
    [
      { text: "MODELO", options: { bold: true, color: C.ink3, fontSize: 9, charSpacing: 2, fontFace: FONT_MONO } },
      { text: "INPUT", options: { bold: true, color: C.ink3, fontSize: 9, charSpacing: 2, fontFace: FONT_MONO } },
      { text: "OUTPUT", options: { bold: true, color: C.ink3, fontSize: 9, charSpacing: 2, fontFace: FONT_MONO } },
      { text: "MELHOR USO", options: { bold: true, color: C.ink3, fontSize: 9, charSpacing: 2, fontFace: FONT_MONO } },
    ],
    [
      { text: "GPT-5 mini", options: { fontSize: 11, fontFace: FONT_SANS, bold: true } },
      { text: "incluído", options: { fontSize: 11, fontFace: FONT_MONO, color: C.green } },
      { text: "incluído", options: { fontSize: 11, fontFace: FONT_MONO, color: C.green } },
      { text: "Chat diário, completions rotineiras", options: { fontSize: 11, fontFace: FONT_SANS, color: C.ink2 } },
    ],
    [
      { text: "GPT-5", options: { fontSize: 11, fontFace: FONT_SANS } },
      { text: "125 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.ink } },
      { text: "1,000 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.ink } },
      { text: "Raciocínio e código de média complexidade", options: { fontSize: 11, fontFace: FONT_SANS, color: C.ink2 } },
    ],
    [
      { text: "Claude Sonnet 4.6", options: { fontSize: 11, fontFace: FONT_SANS } },
      { text: "300 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.ink } },
      { text: "1,500 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.ink } },
      { text: "Contexto longo, trabalho sustentado", options: { fontSize: 11, fontFace: FONT_SANS, color: C.ink2 } },
    ],
    [
      { text: "Claude Opus 4.7", options: { fontSize: 11, fontFace: FONT_SANS, bold: true } },
      { text: "1,500 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.red } },
      { text: "7,500 cr", options: { fontSize: 11, fontFace: FONT_MONO, color: C.red, bold: true } },
      { text: "Tarefas agênticas difíceis, uso reservado", options: { fontSize: 11, fontFace: FONT_SANS, color: C.ink2 } },
    ],
  ];
  s.addTable(tableData, {
    x: 0.5, y: 5.4, w: 12.3, h: 1.6,
    rowH: 0.32,
    colW: [2.4, 1.8, 1.8, 6.3],
    border: { type: "solid", pt: 0.5, color: C.rule },
    fontFace: FONT_SANS,
    color: C.ink,
    valign: "middle",
  });
  s.addText(data.rates.note || "Taxas ilustrativas. Sempre valide contra a documentação oficial de billing do GitHub Copilot.", {
    x: 0.5, y: 7.1, w: 11.5, h: 0.3,
    fontFace: FONT_SANS, fontSize: 9, color: C.ink3, italic: true,
    valign: "middle", margin: 0,
  });
  addPageNumber(s, 12, 20);
  s.addNotes(plainNote(data.notes.s12));
}

function slide13() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.promo.eyebrow, C.green);
  addTitle(s, data.promo.title);
  const phases = [
    { phase: data.promo.r1.phase, action: data.promo.r1.text, when: data.promo.r1.duration || "Até 31 de maio", color: C.yellow },
    { phase: data.promo.r2.phase, action: data.promo.r2.text, when: data.promo.r2.duration || "1 jun a 1 set", color: C.green },
    { phase: data.promo.r3.phase, action: data.promo.r3.text, when: data.promo.r3.duration || "A partir de 1 set", color: C.blue },
  ];
  let y = 3.6;
  const rowH = 1.05;
  phases.forEach((p) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 0.05, h: rowH, fill: { color: p.color }, line: { type: "none" } });
    s.addText(p.phase, {
      x: 0.75, y: y + 0.15, w: 2.3, h: 0.7,
      fontFace: FONT_MONO, fontSize: 10, bold: true, color: p.color,
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(p.action, {
      x: 3.2, y: y + 0.2, w: 8.0, h: rowH - 0.3,
      fontFace: FONT_SANS, fontSize: 13, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(p.when, {
      x: 11.2, y: y + 0.2, w: 1.8, h: 0.4,
      fontFace: FONT_MONO, fontSize: 10, color: C.ink3,
      align: "right", valign: "top", margin: 0,
    });
    y += rowH + 0.1;
  });
  addPageNumber(s, 13, 20);
  s.addNotes(plainNote(data.notes.s13));
}

function slide14() {
  slideDivider(4, "IV", data.part4.title || "Design de agentes",
    data.part4.sub || "Quando agent vale o custo", C.blue, 14);
}

function slide15() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.aw.eyebrow, C.green);
  addTitle(s, data.aw.title, { size: 26, h: 1.0 });
  const cards = [
    { label: data.aw.spec.c1Label, title: data.aw.spec.c1Title, body: data.aw.spec.c1Body, ex: data.aw.spec.c1Ex, color: C.blue, costSegs: 1, costSym: "$" },
    { label: data.aw.spec.c2Label, title: data.aw.spec.c2Title, body: data.aw.spec.c2Body, ex: data.aw.spec.c2Ex, color: C.yellow, costSegs: 2, costSym: "$$" },
    { label: data.aw.spec.c3Label, title: data.aw.spec.c3Title, body: data.aw.spec.c3Body, ex: data.aw.spec.c3Ex, color: C.green, costSegs: 3, costSym: "$$$" },
    { label: data.aw.spec.c4Label, title: data.aw.spec.c4Title, body: data.aw.spec.c4Body, ex: data.aw.spec.c4Ex, color: C.red, costSegs: 4, costSym: "$$$$" },
  ];
  const cy = 3.4, cw = 2.95, ch = 2.5, gap = 0.18;
  const totalW = cw * 4 + gap * 3;
  const startX = (13.333 - totalW) / 2;
  cards.forEach((card, i) => {
    const x = startX + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.paper }, line: { color: C.rule, width: 0.5 } });
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: 0.08, fill: { color: card.color }, line: { type: "none" } });
    s.addText(card.label.toUpperCase(), {
      x: x + 0.2, y: cy + 0.3, w: cw - 0.4, h: 0.3,
      fontFace: FONT_MONO, fontSize: 9, bold: true, color: card.color,
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(card.title, {
      x: x + 0.2, y: cy + 0.65, w: cw - 0.4, h: 0.8,
      fontFace: FONT_SANS, fontSize: 14, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(card.body, {
      x: x + 0.2, y: cy + 1.45, w: cw - 0.4, h: 0.7,
      fontFace: FONT_SANS, fontSize: 10, color: C.ink2,
      valign: "top", margin: 0,
    });
    s.addShape(pres.shapes.LINE, { x: x + 0.2, y: cy + ch - 0.4, w: cw - 0.4, h: 0, line: { color: C.rule, width: 0.5 } });
    s.addText(card.ex, {
      x: x + 0.2, y: cy + ch - 0.35, w: cw - 0.4, h: 0.3,
      fontFace: FONT_MONO, fontSize: 8, color: C.ink3,
      charSpacing: 2, valign: "top", margin: 0,
    });
  });
  // cost bars
  const barY = cy + ch + 0.2, barH = 0.25;
  cards.forEach((card, i) => {
    const x = startX + i * (cw + gap);
    const segW = (cw - 0.4 - 3 * 0.05) / 4;
    for (let k = 0; k < 4; k++) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x + 0.2 + k * (segW + 0.05), y: barY, w: segW, h: barH,
        fill: { color: k < card.costSegs ? card.color : C.rule }, line: { type: "none" },
      });
    }
    s.addText(card.costSym, {
      x: x + 0.2, y: barY + barH + 0.05, w: cw - 0.4, h: 0.3,
      fontFace: FONT_MONO, fontSize: 11, bold: true, color: card.color,
      valign: "top", margin: 0,
    });
  });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 6.95, w: 12.3, h: 0, line: { color: C.rule, width: 0.5 } });
  s.addText("← " + (data.aw.spec.leftMsg || "onde vive 90% do AI em produção"), {
    x: 0.5, y: 7.05, w: 6, h: 0.3,
    fontFace: FONT_SANS, fontSize: 11, italic: true, color: C.ink2,
    valign: "middle", margin: 0,
  });
  s.addText((data.aw.spec.rightMsg || "só quando nada mais resolve") + " →", {
    x: 6.5, y: 7.05, w: 6.3, h: 0.3,
    fontFace: FONT_SANS, fontSize: 11, italic: true, color: C.ink2,
    align: "right", valign: "middle", margin: 0,
  });
  addPageNumber(s, 15, 20);
  s.addNotes(plainNote(data.notes.s15));
}

function slide16() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.patterns.eyebrow, C.blue);
  addTitle(s, data.patterns.title, { size: 30 });
  const patterns = [
    { num: "01", topic: "MCP", title: data.patterns.p1.title, body: data.patterns.p1.body, color: C.blue },
    { num: "02", topic: "RAG", title: data.patterns.p2.title, body: data.patterns.p2.body, color: C.yellow },
    { num: "03", topic: "SUBAGENTES", title: data.patterns.p3.title, body: data.patterns.p3.body, color: C.green },
  ];
  const cy = 4.0, cw = 4.0, ch = 2.8, gap = 0.25;
  const totalW = cw * 3 + gap * 2;
  const startX = (13.333 - totalW) / 2;
  patterns.forEach((p, i) => {
    const x = startX + i * (cw + gap);
    s.addShape(pres.shapes.RECTANGLE, { x, y: cy, w: cw, h: ch, fill: { color: C.paper }, line: { color: C.rule, width: 0.5 } });
    s.addText(p.num + " · " + p.topic, {
      x: x + 0.3, y: cy + 0.25, w: cw - 0.6, h: 0.3,
      fontFace: FONT_MONO, fontSize: 10, bold: true, color: p.color,
      charSpacing: 4, valign: "top", margin: 0,
    });
    s.addText(p.title, {
      x: x + 0.3, y: cy + 0.65, w: cw - 0.6, h: 0.7,
      fontFace: FONT_SANS, fontSize: 17, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(p.body, {
      x: x + 0.3, y: cy + 1.5, w: cw - 0.6, h: 1.25,
      fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
      valign: "top", margin: 0,
    });
  });
  addPageNumber(s, 16, 20);
  s.addNotes(plainNote(data.notes.s16));
}

function slide17() {
  slideDivider(5, "V", data.part5.title || "Operação",
    data.part5.sub || "FinOps stack e o roteiro de 90 dias", C.red, 17);
}

function slide18() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.finops.eyebrow, C.blue);
  addTitle(s, data.finops.title, { size: 30 });
  const layers = [
    { num: "04", label: data.finops.l4Sub, title: data.finops.l4.name, body: data.finops.l4.desc, color: C.red },
    { num: "03", label: data.finops.l3Sub, title: data.finops.l3.name, body: data.finops.l3.desc, color: C.yellow },
    { num: "02", label: data.finops.l2Sub, title: data.finops.l2.name, body: data.finops.l2.desc, color: C.green },
    { num: "01", label: data.finops.l1Sub, title: data.finops.l1.name, body: data.finops.l1.desc, color: C.blue },
  ];
  let y = 3.5;
  const rowH = 0.85;
  layers.forEach((l) => {
    s.addText(l.num, {
      x: 0.5, y: y + 0.05, w: 0.8, h: rowH - 0.1,
      fontFace: FONT_MONO, fontSize: 28, color: l.color,
      valign: "middle", margin: 0,
    });
    s.addShape(pres.shapes.RECTANGLE, { x: 1.5, y: y, w: 0.05, h: rowH, fill: { color: l.color }, line: { type: "none" } });
    s.addText(l.label, {
      x: 1.75, y: y + 0.1, w: 3.4, h: 0.4,
      fontFace: FONT_MONO, fontSize: 9, bold: true, color: l.color,
      charSpacing: 2, valign: "top", margin: 0,
    });
    s.addText(l.title, {
      x: 1.75, y: y + 0.48, w: 3.4, h: 0.35,
      fontFace: FONT_SANS, fontSize: 14, bold: true, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(l.body, {
      x: 5.4, y: y + 0.1, w: 7.5, h: rowH - 0.2,
      fontFace: FONT_SANS, fontSize: 11, color: C.ink2,
      valign: "middle", margin: 0,
    });
    y += rowH + 0.1;
  });
  addPageNumber(s, 18, 20);
  s.addNotes(plainNote(data.notes.s18));
}

function slide19() {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  addBrandHeader(s);
  addEyebrow(s, data.r90.eyebrow, C.blue);
  addTitle(s, data.r90.title);
  const phases = [
    { phase: data.r90.r1.phase, action: data.r90.r1.text, color: C.red, days: "30 dias" },
    { phase: data.r90.r2.phase, action: data.r90.r2.text, color: C.yellow, days: "30 dias" },
    { phase: data.r90.r3.phase, action: data.r90.r3.text, color: C.green, days: "30 dias" },
  ];
  let y = 3.7;
  const rowH = 1.05;
  phases.forEach((p) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y, w: 0.05, h: rowH, fill: { color: p.color }, line: { type: "none" } });
    s.addText(p.phase, {
      x: 0.75, y: y + 0.15, w: 2.5, h: 0.8,
      fontFace: FONT_MONO, fontSize: 10, bold: true, color: p.color,
      charSpacing: 3, valign: "top", margin: 0,
    });
    s.addText(p.action, {
      x: 3.4, y: y + 0.2, w: 7.8, h: rowH - 0.3,
      fontFace: FONT_SANS, fontSize: 13, color: C.ink,
      valign: "top", margin: 0,
    });
    s.addText(p.days, {
      x: 11.4, y: y + 0.2, w: 1.5, h: 0.4,
      fontFace: FONT_MONO, fontSize: 10, color: C.ink3,
      align: "right", valign: "top", margin: 0,
    });
    y += rowH + 0.1;
  });
  addPageNumber(s, 19, 20);
  s.addNotes(plainNote(data.notes.s19));
}

function slide20() {
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  addBrandHeader(s, "dark");
  addEyebrow(s, data.end.eyebrow, C.blue, { x: 0.5, y: 1.4 });
  s.addText(data.end.title1 + " " + data.end.title2, {
    x: 0.5, y: 2.0, w: 8.5, h: 2.5,
    fontFace: FONT_SANS, fontSize: 52, color: C.darkInk,
    valign: "top", margin: 0,
  });
  s.addText(data.end.tagline, {
    x: 0.5, y: 4.6, w: 8.5, h: 0.6,
    fontFace: FONT_SANS, fontSize: 16, italic: true, color: C.darkInk2,
    valign: "top", margin: 0,
  });
  s.addText([
    { text: "CONTATO\n", options: { fontSize: 9, charSpacing: 3, bold: true, color: C.darkInk3 } },
    { text: "Frontier Cockpit Team\n", options: { fontSize: 16, bold: true, color: C.darkInk } },
    { text: "Software Global Black Belt\n", options: { fontSize: 12, color: C.darkInk2 } },
    { text: "frontier-cockpit@example.com", options: { fontSize: 12, color: C.blue } },
  ], { x: 0.5, y: 5.6, w: 4, h: 1.6, fontFace: FONT_SANS, valign: "top", margin: 0 });
  s.addText([
    { text: "PRÓXIMO PASSO\n", options: { fontSize: 9, charSpacing: 3, bold: true, color: C.darkInk3 } },
    { text: "Diagnóstico de 90 dias\n", options: { fontSize: 16, bold: true, color: C.darkInk } },
    { text: "Grátis para clientes enterprise\n", options: { fontSize: 12, color: C.darkInk2 } },
    { text: "Publicado 2026-05-28", options: { fontSize: 11, color: C.darkInk3 } },
  ], { x: 4.7, y: 5.6, w: 4, h: 1.6, fontFace: FONT_SANS, valign: "top", margin: 0 });
  // Code block
  const cx = 9.0, cy = 1.8, cw = 4.0, ch = 4.5;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: cx, y: cy, w: cw, h: ch,
    fill: { color: "1A1A1A" }, line: { color: "2A2A2A", width: 0.5 }, rectRadius: 0.05,
  });
  s.addText(".github/copilot-instructions.md", {
    x: cx + 0.2, y: cy + 0.15, w: cw - 0.4, h: 0.3,
    fontFace: FONT_MONO, fontSize: 9, color: C.darkInk3,
    charSpacing: 2, valign: "top", margin: 0,
  });
  s.addText([
    { text: "# Model policy\n", options: { color: C.green, italic: true } },
    { text: "Default model: GPT-5 mini (included)\n", options: { color: C.darkInk } },
    { text: "Premium models: only for hard tasks\n\n", options: { color: C.darkInk } },
    { text: "# Context discipline\n", options: { color: C.green, italic: true } },
    { text: "Reference files with #file:path explicitly\n", options: { color: C.darkInk } },
    { text: "Use @workspace only when search-wide is needed\n\n", options: { color: C.darkInk } },
    { text: "# Caching\n", options: { color: C.green, italic: true } },
    { text: "System prompts cached after first turn\n", options: { color: C.darkInk } },
    { text: "Long reference docs always cached", options: { color: C.darkInk } },
  ], { x: cx + 0.2, y: cy + 0.55, w: cw - 0.4, h: ch - 0.7, fontFace: FONT_MONO, fontSize: 9, valign: "top", margin: 0 });
  // Linha decorativa colorida
  const lineY = 7.0, segW = 0.6, segH = 0.05;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: lineY, w: segW, h: segH, fill: { color: C.red }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW, y: lineY, w: segW, h: segH, fill: { color: C.green }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW * 2, y: lineY, w: segW, h: segH, fill: { color: C.yellow }, line: { type: "none" } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5 + segW * 3, y: lineY, w: segW, h: segH, fill: { color: C.blue }, line: { type: "none" } });
  addPageNumber(s, 20, 20, "dark");
  s.addNotes(plainNote(data.notes.s20));
}

console.log("Gerando 20 slides...");
slide1(); console.log("  v Slide 1, cover");
slide2(); console.log("  v Slide 2, agenda");
slide3(); console.log("  v Slide 3, Part I divider");
slide4(); console.log("  v Slide 4, June 1");
slide5(); console.log("  v Slide 5, PRU vs AI Credits");
slide6(); console.log("  v Slide 6, Part II divider");
slide7(); console.log("  v Slide 7, token concepts");
slide8(); console.log("  v Slide 8, donut + classes");
slide9(); console.log("  v Slide 9, context engineering");
slide10(); console.log("  v Slide 10, Part III divider");
slide11(); console.log("  v Slide 11, 100x + terminal");
slide12(); console.log("  v Slide 12, model pricing");
slide13(); console.log("  v Slide 13, promo window");
slide14(); console.log("  v Slide 14, Part IV divider");
slide15(); console.log("  v Slide 15, spectrum");
slide16(); console.log("  v Slide 16, patterns");
slide17(); console.log("  v Slide 17, Part V divider");
slide18(); console.log("  v Slide 18, FinOps stack");
slide19(); console.log("  v Slide 19, 90-day roadmap");
slide20(); console.log("  v Slide 20, closing");

const outputPath = "./output/Token_Management_Agent_Design_Deck_v2_0_0_2026-05-28_ptBR.pptx";
pres.writeFile({ fileName: outputPath }).then(() => {
  console.log("\nPPTX gerado: " + outputPath);
});
