---
name: ms-gartner-deck
description: Generate Gartner-style strategic and technical client proposal decks in three synchronized formats (HTML source, fully native and editable PPTX with no flattened images, and vector PDF). Microsoft 4-color identity, white background, one anchor color rotating per section, 30 slide archetypes including 4 selectable cover variants. Use whenever Frontier Cockpit Team needs a client-facing briefing deck, an analyst-style proposal, a strategic-plus-technical deck, a "Gartner-style" presentation, an editable PowerPoint deck, or a deck that must work as both HTML and PPTX. Trigger on "Gartner deck", "client proposal deck", "strategic brief deck", "editable PPTX deck", "native PowerPoint deck", "deck Gartner", "proposta de cliente", "deck editavel", or any structured multi-section advisory deck under the Microsoft Software Global Black Belt identity. This is the specialization for the Gartner deck format and the native-PPTX generator; it inherits all visual tokens, identity strings, and editorial rules from ms-identity.
---

# ms-gartner-deck Skill (v1.0.0)

Generates Gartner-style strategic + technical proposal decks for Frontier Cockpit Team,
Software Global Black Belt. One deck definition produces three synchronized
outputs: an HTML source deck, a **fully native and editable PPTX**, and a
vector PDF.

This skill is a **specialization of `ms-identity`**. It does not redefine
the design system. It adds one thing: the Gartner deck format and a
native-PowerPoint generator that carries no flattened images, so every word,
color, table, and shape stays editable after the file is opened.

## Relationship to ms-identity

Load `ms-identity` first. This skill inherits from it:

- Microsoft 4-color palette and the neutral structural spine
- Identity strings (`Frontier Cockpit Team`, `Software Global Black Belt`,
  `frontier-cockpit@example.com`, single-channel contact)
- Editorial rules (no em dashes, full product names, sentence case, ISO dates)
- The `</>` logo geometry and forbidden personal-identity patterns

What this skill adds:

- A 53-slide reference deck in the Gartner format (HTML)
- 30 slide archetypes, including a `cover` archetype with 4 selectable variants
- A native PPTX generator (`build_pptx.py`): autoshapes, native tables, text
  frames, connectors, and speaker notes; **never** images or screenshots
- A vector PDF path that mirrors the HTML one-to-one

## When to use which size

| Deck size | When |
|---|---|
| ~16 slides | The standard client briefing. One section per act, a handful of supporting slides each. This is the default. |
| ~25 slides | A fuller briefing. Room for section intros and more data slides per section. |
| ~53 slides | The reference deck length, every archetype represented once. A reasonable ceiling for a single briefing. |
| 53+ slides | Technically supported, not editorially recommended. See below. |

The generators have **no hard slide limit**. `build_html.py`, `build_pptx.py`,
and `deck_data.py` produce however many slides the `DECK` list contains;
`_TOTAL`, page numbering, and the HTML contents index all adjust dynamically.
The 53-slide reference deck is a design choice, not a code constraint.

So a large project *can* exceed 53 slides when it genuinely needs to. But
before doing that, check the format is still right:

- The Gartner format's strength is the tight six-act spine. Past ~30 slides
  an audience starts losing the thread, and past ~53 the deck is usually
  carrying content that wants to be a document, not a presentation.
- For genuinely large, dense material, a multi-page playbook (see the
  `ms-identity` playbook pattern) or a consolidated PDF
  (`playbook-pdf-builder`) handles volume better than slides do.
- If the project still wants a deck at that length, split it: a core briefing
  deck plus a separate appendix deck, rather than one 80-slide file.

Do not pad a deck to fill a target. The reference deck is 53 because it
demonstrates all 30 archetypes; a real client deck is usually 16 to 25.

## The three formats

All three come from one deck definition. Never hand-build one format.

| Format | Script | Output | Editable? |
|---|---|---|---|
| HTML (source) | `scripts/build_html.py` | one `.html`, vertical-stacked 16:9 slides, print-CSS = 1 page/slide | yes, it is the source |
| PPTX (native) | `scripts/build_pptx.py` + `scripts/deck_data.py` | one `.pptx`, every element a native shape, with speaker notes | yes, fully (text, tables, shapes, colors, notes) |
| PDF (vector) | `scripts/build_pdf.py` | one `.pdf`, one page per slide, vector not raster | no, it is a render |

### Build commands

Install generator dependencies before producing PDF or PPTX:

```bash
pip install -r scripts/requirements.txt
python -m playwright install chromium   # required only for PDF export
```

```bash
# 1. HTML deck (CSS source-of-truth is assets/deck-template.html)
python3 scripts/build_html.py --out deck.html

# 2. Native editable PPTX (reads the 53-slide spec from deck_data.py)
python3 scripts/build_pptx.py --out deck.pptx
#    build a subset for QA:
python3 scripts/build_pptx.py --out sample.pptx --only cover_meeting,data_table,quadrant

# 3. Vector PDF from the HTML deck
python3 scripts/build_pdf.py --input deck.html --output deck.pdf
```

`build_pptx.py` imports `deck_data.py` from the same `scripts/` folder; keep
them together.

Before presenting any output, walk `references/first-run-checklist.md`. It is the final gate for source synchronization, identity, dependency readiness, HTML/PPTX/PDF output validation, and delivery.

## The data model

The deck is **not** built by parsing HTML. Both generators carry their own
content:

- `scripts/build_html.py` holds `build_50()`, 53 builder calls, each with
  inline content, that assemble the HTML deck.
- `scripts/deck_data.py` holds `DECK`, a list of 53 plain-dict slide specs,
  each with a `type` that maps to one PPTX renderer.

These two are kept in sync by hand. **To change deck content**, edit both: the
builder call in `build_html.py` and the matching dict in `deck_data.py`. They
are deliberately separate so each generator stays simple and debuggable.

For a new client deck, the usual path is: copy `deck_data.py`, trim it to the
16 to 25 slides you need, edit the content, and mirror the same cuts and edits
in `build_html.py`'s `build_50()`.

## The 30 archetypes

Each archetype is one renderer in `build_pptx.py` and one builder in
`build_html.py`. Anchor color rotates by section.

### Structural (front matter, dividers, transitions)

| Archetype | Purpose |
|---|---|
| `cover` (4 variants) | Slide 1. Fixed left panel (brand, title, subtitle, chips, byline), swappable right panel. See "Cover variants" below. |
| `divider` | Full-bleed section divider. Big act number, section title, the questions that act answers. Anchor color fills the right panel. |
| `section_intro` | Lighter than a divider. Frames a sub-topic inside a long section, or closes a section by pointing forward. |
| `agenda` | The six-section running order as a card grid. |
| `appendix_divider` | Dark full-bleed divider marking the start of back matter. |
| `contact` | Closing slide. Split panel: the next step on an anchor-color field, the ask and signature on white. |

### Narrative content

| Archetype | Purpose |
|---|---|
| `exec_summary` | Three columns, each a claim plus evidence plus a "so what". The one slide the room reads if it reads nothing else. |
| `big_number` | One dark metric card plus three supporting stat cards. For a single dominant figure. |
| `quote` | Full-bleed pull quote with attribution. A breather between dense sections. |
| `pillar_grid` | Three vertical pillars. For "three causes", "three principles", "three moves". |
| `flow` | Horizontal four-stage process with arrows. For a path or pipeline. |
| `before_after` | Two columns plus a stat row. For expectation-vs-reality, current-vs-target. |
| `case_study` | Dark hero panel (client, headline outcome) plus three labeled steps (problem, approach, result). |

### Data and analysis

| Archetype | Purpose |
|---|---|
| `data_table` | Dense native table with tag pills and an optional pull-quote. Row heights auto-computed from content. |
| `quadrant` | 2x2 matrix with positioned dots and a legend. For "where teams sit". |
| `metrics_dashboard` | One featured dark tile plus a 2x2 grid of metric tiles. |
| `risks_table` | Risk / likelihood / impact / mitigation table with colored tag pills. |
| `vendor_compare` | Feature matrix across options, recommended column highlighted, check / partial / dash glyphs. |
| `decision_matrix` | Weighted scoring table with a highlighted total row. Shows the reasoning, not just the verdict. |
| `stakeholder_map` | 2x2 influence-vs-interest map with chips in each quadrant. |

### Architecture

| Archetype | Purpose |
|---|---|
| `layer_stack` | Horizontal layered bands, colored tag plus body. For a reference stack or a runtime layer. |
| `architecture_detail` | Annotated component diagram: tiers of nodes on a canvas, design-decision notes alongside. |

### Plan and investment

| Archetype | Purpose |
|---|---|
| `roadmap` | Four phase cards, colored headers, exit criteria pinned to each footer. |
| `gantt` | Week-by-week timeline with colored bars, overlaps shown honestly. |
| `team` | Role cards with avatar circles. Who owns what. |
| `raci` | Responsible / accountable / consulted / informed matrix with colored badges and a legend. |
| `pricing` | Three engagement-size tiers, the recommended one featured. |
| `recommendation` | Three stacked pillars plus a dark "ask" card and a next-step pull. The closing argument. |
| `org_chart` | A lead node with a connector rail to report nodes. |

## Cover variants

The `cover` archetype has a fixed left panel and four swappable right panels.
The reference deck uses `cover_meeting` as slide 1 and parks the other three
in the appendix (slides 50 to 52) as a variant reference.

| Variant | Right panel | Use when |
|---|---|---|
| `cover_meeting` | Client, date, session type, attendees, outcome | A proposal tied to a specific meeting. The default. |
| `cover_stat` | One big number plus a claim, with a three-act agenda strip | Opening on a striking statistic. |
| `cover_thesis` | The central thesis statement plus supporting text | Opening on the core argument. |
| `cover_pillars` | Three horizon cards | Opening on the three-move structure of the brief. |

To pick a variant for slide 1: set the first `DECK` entry's `type` to the
chosen `cover_*` and use the matching builder in `build_html.py`. The left
panel never changes.

## Deck structure

The reference deck follows a fixed six-act spine. Anchor color rotates so the
audience always knows which act they are in.

| Slides | Section | Anchor |
|---|---|---|
| 1 to 4 | Front matter (cover, agenda, exec summary, quote) | blue |
| 5 to 13 | Section 1, Context | blue |
| 14 to 22 | Section 2, The problem | green |
| 23 to 31 | Section 3, The solution | yellow |
| 32 to 39 | Section 4, Architecture | red |
| 40 to 45 | Section 5, The plan | blue |
| 46 to 48 | Section 6, Investment | green |
| 49 to 53 | Back matter (appendix divider, 3 cover variants, contact) | red |

A 16-slide deck collapses this: one divider plus two or three content slides
per section, front and back matter trimmed to cover plus contact.

## Design tokens

Inherited from `ms-identity`. Two font pairings, one per format:

| Context | Sans | Mono | Why |
|---|---|---|---|
| HTML, PDF | Inter | JetBrains Mono | Matches the ms-identity web system |
| PPTX | Segoe UI | Consolas | PowerPoint-portable, present on every Office install |

PPTX canvas is 16:9 at 13.333 by 7.5 inches. Margins and content box are
defined at the top of `build_pptx.py` (`MARGIN_X`, `CONTENT_TOP`,
`CONTENT_BOT`). Do not hardcode geometry in renderers; use those constants.

## Why the PPTX is built shape-by-shape

The PPTX must be **editable**, not a picture of a deck. So `build_pptx.py`
never rasterizes. Every element is a native PowerPoint object:

- Text is native text frames with styled runs
- Tables are `add_table` native tables, default banding stripped, row heights
  computed from estimated content wrap
- Boxes, cards, chips, badges are autoshapes (rectangles, rounded rectangles,
  ovals)
- Rules and connectors are native line shapes
- The Microsoft logo is four native rectangles, not an image

The cost of this is that PowerPoint has no automatic layout. A text box does
not push the box below it; a table cell grows unpredictably. The generator
compensates with estimation helpers; read the next section before editing a
renderer.

## Editing renderers safely

The renderer-robustness rules, learned the hard way:

1. **The renderer environment runs fonts wider and larger than a naive
   estimate.** LibreOffice and PowerPoint render Segoe UI roughly 18 percent
   wider than a plain character count predicts. Every size and height in the
   renderers is calibrated to that. If you shrink a box, shrink conservatively.

2. **`title_block()` is the key robustness fix.** It estimates how many lines
   the title will wrap to (weighting bold runs 1.18x), sizes the title block
   accordingly, pushes the descriptor down, and returns a safe content-start
   Y. Any renderer with a content area must call `content_frame()` and use the
   returned `ctop`, never a hardcoded `CONTENT_TOP`.

3. **Tables compute row heights from content.** `_est_lines()` estimates wrap
   per cell; the renderer sums real row heights and positions tag pills and
   pull-quotes from the cumulative total, not from a fixed row height.

4. **Tag pills and badges are overlay shapes**, positioned after the table is
   drawn, using the same cumulative-height math. Native table cells cannot
   hold a styled pill.

5. **Vertical axis labels use `_vlabel()`**, a real 270-degree rotation via
   shape XML. Never try to fake a vertical label with a narrow text box; it
   stacks letter by letter.

When you change a renderer, regenerate and visually QA. Do one fix-and-verify
cycle per defect. Do not chase pixels.

## QA loop

```bash
# generate
python3 scripts/build_pptx.py --out deck.pptx
# convert to images
soffice --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 110 deck.pdf page
# then view page-*.jpg and look for overflow, overlap, clipping
```

The most common defect is a large font in a narrow panel wrapping to more
lines than its box reserved. The fix is always the same family: shrink the
font a step, grow the box, or both.

## Editorial rules

All inherited from `ms-identity`, and they apply to every slide in every
format:

- No em dashes. Use commas, semicolons, or periods.
- Full product names: `GitHub Copilot`, `Azure AI Foundry`, `Azure Kubernetes
  Service`. Never the short form.
- Sentence case for headings.
- ISO dates: `2026-05-20`.
- Microsoft 4-color palette only. Never the personal your-org palette.
- Sign as `Software Global Black Belt`, never the personal role.
- For a reference template or any external-audience deck, content is
  territory-neutral and explicitly illustrative. Mark placeholder figures as
  placeholders; never invent client names or Microsoft-internal data.

## File naming

Follow the `ms-identity` convention:

```
{Title}_Deck_v{M_M_M}_{YYYY-MM-DD}_{locale}.{ext}
```

Example: `AI_Platform_Modernization_Deck_v1_0_0_2026-05-20_en.html` and the
matching `.pptx` and `.pdf`.

## Assets

| File | Purpose |
|---|---|
| `assets/deck-template.html` | The CSS source-of-truth. Holds every archetype's styling plus all 4 cover variants. `build_html.py` splices generated slides into this. Edit here to change HTML styling. |
| `assets/reference-deck.html` | The full 53-slide reference deck, rendered. Open in a browser as the visual spec. |
| `assets/reference-deck.pptx` | The full 53-slide deck as native PPTX. Open in PowerPoint to confirm everything is editable, or as the starting file to cut down from. |

## Scripts

| File | Purpose |
|---|---|
| `scripts/build_html.py` | Builds the HTML deck. Holds `build_50()` with all 53 builder calls and every archetype builder function. |
| `scripts/build_pptx.py` | Builds the native PPTX. Holds the 30 renderers, the shape helpers, `title_block()`, `_est_lines()`, `_vlabel()`, and the `RENDERERS` registry. |
| `scripts/deck_data.py` | The 53-slide `DECK` spec consumed by `build_pptx.py`. Plain dicts, one per slide. |
| `scripts/build_pdf.py` | Renders the HTML deck to vector PDF via Playwright print-CSS. |

## Anti-patterns

- Rasterizing anything into the PPTX. The whole point is that it stays
  editable. No screenshots, no flattened SVG, no picture-of-a-table.
- Hand-building one format. All three come from the deck definition. If they
  drift, regenerate.
- Hardcoding `CONTENT_TOP` in a renderer instead of using the `ctop` returned
  by `content_frame()`. Long titles will collide with the content.
- Padding a client deck to hit a slide count. 53 is the reference template
  length, not a target; most client decks are 16 to 25. Going past ~53 is
  technically fine but usually a sign the content wants a playbook or a PDF,
  not a deck.
- Editing `build_html.py` content without mirroring it in `deck_data.py`, or
  the reverse. The two formats will silently diverge.
- Faking a vertical axis label with a narrow text box. Use `_vlabel()`.
- Using the personal your-org palette or the personal role string. This
  is Microsoft-identity output, start to finish.
