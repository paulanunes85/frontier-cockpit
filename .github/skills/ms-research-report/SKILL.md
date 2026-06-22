---
name: ms-research-report
description: Research-to-deliverable engine for Frontier Cockpit Team (Software Global Black Belt). Conducts industry analyst, account, technical, competitive intel, or general research, produces polished outputs in Markdown, HTML, PDF, XLSX, DOCX, PPTX. Also generates multi-chapter workshop/playbook content (one .md per chapter, basic to advanced) with derived consolidated PDF, PPTX, HTML deck. ALWAYS use for "research and report on", "analyst report", "industry analysis", "market landscape", "account dossier", "competitive intel brief", "workshop content", "playbook content", "material de estudo", "training material", "do basico ao avancado", or multi-chapter educational content. Trigger on "vendor landscape", "Magic Quadrant", "Forrester Wave", "benchmark analysis", "workshop", "curriculum", "playbook", or attached prompt library, RFP, transcript. Skip ONLY for pure formatting with no research (route to ms-docx-creator, ms-gartner-deck, markdown-writer), or three-language Medium articles (paula-article-writer).
---

# MS Research Report

Research-to-deliverable engine for Frontier Cockpit Team's Software Global Black Belt work. End-to-end, standalone: this skill handles intake, research, structuring, drafting, formatting, and exporting without delegating to other format-specific skills. Identity tokens, format recipes, and deliverable structures are bundled in the references directory.

## What this skill is for

The user needs both research AND a polished deliverable. Examples:

- "Research the GenAI coding assistant market and build me an analyst report with a quadrant chart, an Excel capability matrix, and an exec deck."
- "Build a dossier on Banco do Brasil: tech stack, GitHub/Microsoft footprint, recent news, opportunity map. PDF and DOCX."
- "Competitive intel on GitHub Copilot vs Cursor vs Cody. HTML one-pager plus Excel feature comparison."
- "Investigate platform engineering maturity models, write it up." (Single research write-up, MD + HTML default.)

If the user only wants formatting of pre-existing content with no research step, route to the dedicated format skill instead.

## Workflow (4 phases)

### Phase 1: Intake

Resolve five questions before researching anything:

1. **Deliverable type** (pick one): industry analyst report, account dossier, technical research paper, competitive intel brief, general write-up, or **workshop / educational content**. If ambiguous, ask the user with one short clarifying question.
2. **Research scope**: web search, uploaded documents, attached prompt library, or a mix. Note which sources are in play.
3. **Prompt library detection**: check `input/` for any file matching `Industry_Analyst_Prompt_Library_v*.md`, AND check `assets/templates/industry-analyst-prompt-library.md` for the bundled copy. If either is present, the **library-active mode** turns on; load `references/library-anti-patterns.md` and follow the Role + Domain + Output Format workflow there, which OVERRIDES the default `deliverable-types.md` structure for output sections.
4. **Requested formats**: subset of {md, html, pdf, xlsx, docx, pptx}. If user says "all formats", produce all six. If user says nothing, apply the defaults in the format-selection table below.
5. **Identity**: this skill assumes ms-identity (Software Global Black Belt). If the user wants the personal @your-org identity, stop and tell them to use a different skill.

**Additional intake for workshop / educational content (deliverable type 6)**:
- **Topic**: specific subject and the scope boundary (e.g., "Token Optimization in VS Code and GitHub", "covering economics, observability, and governance")
- **Target audience**: who the learners are (developers, platform engineers, eng managers, mixed)
- **Depth scope**: foundations only, full basic-to-advanced, or advanced-only
- **Expected chapter count**: a target range or "as many as needed for completeness" (no hard cap)
- **Derived formats requested**: any subset of {consolidated PDF playbook, PPTX deck, HTML deck}. Chapter MDs and the master index are always produced.

State the answers back to the user in one tight paragraph before researching. This is the contract.

### Phase 2: Research

Pick research methods per scope. See `references/research-methods.md` for the full playbook (when to use web search, how to triangulate sources, how to handle uploaded RFPs and transcripts, source quality tiers, how to apply an attached prompt library).

Hard rules:

- Cite every empirical claim with a source the user can verify.
- Surface methodology assumptions explicitly. Do not bury them.
- When sources conflict, present both and label the conflict.
- For market sizing, always show the math and the inputs, never just the output number.
- Never fabricate vendor positions, customer counts, or revenue figures. If unknown, say "not disclosed" or "estimate not available".

### Phase 3: Structure and draft

**For deliverable types 1 to 5 (single-document outputs)**:

Build the outline using the structure for the chosen deliverable type. See `references/deliverable-types.md` for the full structure of each type. Draft sections in Markdown first. Markdown is the canonical source; all other formats render from it. This keeps multi-format outputs consistent and lets the user audit a single source of truth.

Apply editorial rules during drafting (see "Editorial rules" below). Do not retrofit them at the end.

**For deliverable type 6 (workshop / educational content), use the 3-step iterative pattern**:

- **Phase 3a: Master index + chapter outlines (single turn)**: Generate `00-index.md` (scope, audience, prereqs, learning outcomes, chapter map, delivery formats, glossary) PLUS one-page outline for every chapter (title, level, estimated duration, learning outcomes, brief topical bullets). Do NOT write chapter bodies yet.

- **Phase 3b: Approval checkpoint (mandatory)**: Present the index and chapter outline list back to the user with a tight summary ("Workshop will have N chapters: X foundations, Y intermediate, Z advanced. Estimated total ~K words, ~M hours of facilitator delivery."). Wait for user approval, edits, additions, or removals. Do NOT proceed to Phase 3c without explicit approval. This checkpoint exists because workshop content is high-token-cost; generating 50K+ words on a wrong structure burns budget.

- **Phase 3c: Chapter generation in batches (multi-turn)**: After approval, generate chapters in batches of 2 to 3 per turn (each chapter typically 3K to 7K words). For each chapter, produce a complete file at `NN-{slug}.md` with full frontmatter and all required sections (see `references/deliverable-types.md` workshop structure). Apply library anti-patterns (no fabricated data, no vendor bias, time horizons on recommendations when applicable, hedge language on projections) throughout.

Apply editorial rules during drafting in all phases. Do not retrofit them at the end.

### Phase 3.5: Validation gate (mandatory, before rendering)

Validate the canonical Markdown before producing any other format. This is where rework is prevented: an unsourced number or an em dash caught here is fixed once; caught after rendering it has to be fixed in the PDF, the PPTX, and the DOCX too. The gate exits non-zero on any error, so do not render until it passes.

```bash
python .github/skills/ms-research-report/scripts/validate_report.py <file.md>
# or validate a whole workshop chapter set:
python .github/skills/ms-research-report/scripts/validate_report.py output/
```

It fails on: em dashes, bare "Copilot" without "GitHub Copilot" (official SKU names are allowed), a missing References or Sources section, and unfilled placeholders. It warns on: empirical claims (percentages, currency, counts, growth) with no citation on the line, projection language with no Methodology or Caveats block, regional framing when the report is territory neutral, and corporate filler. Treat every warning as a claim to source or soften; run with `--strict` to make warnings blocking for client-facing work. Fix everything and rerun until it passes, then proceed to Phase 4.

Then walk `references/first-run-checklist.md` end to end. It is the final gate for intake completeness, source integrity, canonical Markdown, workshop approval checkpoints, and derivative rendering.

### Phase 4: Produce formats

**For deliverable types 1 to 5**: Render each requested format from the canonical Markdown using the recipes in `references/format-recipes.md`. Apply identity tokens from `references/identity-tokens.md` per format.

**For deliverable type 6 (workshop)**: After all chapter MDs are generated, render derived formats from the full chapter set:
- **Consolidated PDF playbook**: cover + auto-TOC from chapter frontmatter + each chapter starting on a new page with rotating 4-color banner + final references + closing card
- **PPTX facilitator deck**: cover + TOC slide + section divider per chapter + 5 to 8 content slides per chapter (1 outline slide + 3 to 6 concept slides + 1 practice/summary slide) + references slide + closing card. Speaker notes filled on every slide.
- **HTML deck**: self-contained file with the full chapter set. Two style options: scroll-style (long-form readable) or slide-style (reveal.js-like navigation). Sticky header, collapsible TOC.

See the workshop-specific recipes in `references/format-recipes.md`.

After all formats are produced:

1. Save all outputs to `output/`.
2. Present the files to the user, most polished or most-requested format first, then the rest. For workshop deliveries, present the consolidated PDF playbook first, then the PPTX, then the HTML deck, then the chapter MDs as a group.
3. Write one tight paragraph summarizing what was produced and which format is for which audience.

## Format selection defaults

User-stated formats override these. If the user does not state formats, apply by deliverable type:

| Deliverable type | Default formats |
|---|---|
| Industry analyst report | md, html, pdf, xlsx, pptx |
| Account dossier | md, docx, pptx |
| Technical research paper | md, pdf |
| Competitive intel brief | md, html, pdf, xlsx |
| General research write-up | md, html |
| **Workshop / Educational content** | **chapter MDs + 00-index.md + 99-references.md (always); consolidated PDF playbook + PPTX deck (default on); HTML deck (on request)** |

If the user says "all formats" or asks for the full set, produce all six regardless of deliverable type. For workshop deliveries, "all formats" means chapter MDs + PDF playbook + PPTX deck + HTML deck.

## Deliverable types (one-line summary, details in references)

1. **Industry analyst report** (target 8 to 25 PDF pages): vendor landscape, market sizing, MQ-style quadrant or Wave-style placement, capability matrix, adoption curves, recommendations.
2. **Account dossier** (target 4 to 12 PDF pages): company profile, tech stack, Microsoft/GitHub footprint, stakeholder map, news radar, opportunity map, next plays.
3. **Technical research paper** (target 6 to 20 PDF pages): architecture comparisons, benchmark analysis, design tradeoff studies, references, reproducibility notes.
4. **Competitive intel brief** (target 3 to 8 PDF pages): vendor-vs-vendor scorecards, feature matrix, positioning quote bank, threat assessment, win/loss themes.
5. **General research write-up** (target 2 to 10 PDF pages): flexible structure for topics that do not fit the four above; adapts headings to the question.
6. **Workshop / Educational content** (no hard cap; typical 5 to 25 chapters, 30K to 150K words total): multi-chapter learning content from basic to advanced. One .md per chapter. Derived consolidated PDF playbook, PPTX facilitator deck, HTML deck. Mandatory outline checkpoint before chapter content generation.

Length targets are guidelines, not ceilings. If the user requests a specific length, honor it.

Full templates: `references/deliverable-types.md`. **When the library is active, output structure comes from `references/library-anti-patterns.md` (Section 6 of the library), not from this file.**

## Identity (always ms-identity)

Software Global Black Belt deliverable. Key tokens:

- **Author line**: Frontier Cockpit Team, Software Global Black Belt, Microsoft
- **Contact**: frontier-cockpit@example.com (single email, NO @your-org, NO @your-handle: those are for personal-identity deliverables only)
- **Header on every doc/deck**: "Software Global Black Belt"
- **Palette (Microsoft 4-color)**: #F25022 red, #7FBA00 green, #FFB900 yellow, #00A4EF blue, plus neutrals (#1A1A1A, #4A4A4A, #E5E5E5, #FFFFFF)
- **Fonts**: Segoe UI (primary, docs/web/decks), Inter (web fallback), Arial (Excel only)
- **Logo**: ms-identity shape with Microsoft 4-color squares

Full token specification (hex values, font stacks, per-format application, cover/closing patterns): `references/identity-tokens.md`.

## Editorial rules (non-negotiable, apply during drafting)

- **No em dashes anywhere**. Use commas, periods, semicolons, parentheses, or colons. This rule applies to every format including code comments in xlsx and speaker notes in pptx.
- **"GitHub Copilot" always in full**. Never "Copilot" alone when referring to GitHub Copilot. "Microsoft Copilot" and "Copilot Studio" are different products and use their own full names. **Exception**: official product SKU names like "Copilot Pro", "Copilot Pro+", "Copilot Business", "Copilot Enterprise", "Copilot Free" are retained verbatim because they are the vendor's official tier labels; the rule applies to generic product references, not to SKU names.
- **Territory-neutral by default**. No LATAM, Brazil, Spanish-speaking-market, or any regional framing unless the user explicitly requests regional content. Drop "in Latin America", "for LATAM clients", and similar phrases by default.
- **Cite empirical claims**. Numbers, market positions, customer counts, growth rates, and quotes all need a source.
- **Flag assumptions explicitly**. Use a clearly labeled "Methodology assumptions" or "Caveats" block rather than hiding them mid-paragraph.
- **Avoid corporate filler**. Direct, structured, systematic. No "in today's fast-paced world" openers, no "it is important to note that" hedging.

## Format-specific rules

**Excel (.xlsx)**:
- Arial font throughout
- SUM formulas (and equivalents) with explicit validation on totals
- Freeze panes on header row
- Auto-filter enabled on all data tables
- One logical view per sheet (e.g., "Vendor Matrix", "Capability Scores", "Sources")
- No merged cells inside data ranges (merging in a banner row is fine)
- Sources sheet always included as the last tab

**HTML/JSX**:
- If producing a JSX artifact, ALWAYS also produce a standalone HTML version with React CDN + Babel standalone + Tailwind CDN
- Both versions functionally identical
- Light background, white or near-white card surfaces, Microsoft 4-color accents
- Sticky header with "Software Global Black Belt" identity line

**PDF**:
- Cover page → table of contents → body → references page
- Continuous page numbers
- Chapter banner uses one of the 4 logo colors, rotated per chapter
- Single email in footer (frontier-cockpit@example.com)

**DOCX**:
- Cover page with 4-color accent
- Document properties filled (title, author, subject)
- Table of contents for any doc with 4+ sections
- Closing page with single email contact

**PPTX**:
- White background standard; color blocks come from the 4-color palette
- Cover slide uses one of the 4 anchor colors
- One color anchor per section, rotated
- Speaker notes filled for every slide
- Final slide is the closing card with single email contact

**Markdown**:
- YAML frontmatter with title, author, date, version, status
- Heading hierarchy starts at H1 for doc title, H2 for sections
- Use fenced code blocks with language tags
- Tables for structured comparisons, lists for sequential content

## References (load on demand)

Load these only when you need the detail. Each is scoped to one concern.

- `references/research-methods.md`: research methods, source quality, prompt library detection, citation patterns
- `references/deliverable-types.md`: full outline and section list for each of the 5 deliverable types
- `references/format-recipes.md`: per-format production recipe with concrete code/structure patterns
- `references/identity-tokens.md`: full ms-identity token spec, per-format application, cover and closing patterns
- `references/library-anti-patterns.md`: **load whenever the Industry Analyst Prompt Library is attached or bundled**. Specifies the Role + Domain + Output Format selection model, mandatory anti-patterns (no fabricated data, no vendor bias, no generic recs, time horizons, citation discipline), and the library compliance checks for the methodology block.
- `references/first-run-checklist.md`: final gate before rendering or delivery. Covers intake contract, source integrity, Markdown validation, workshop checkpoints, and derivative rendering consistency.

## Bundled assets

- `assets/templates/industry-analyst-prompt-library.md`: bundled copy of the Industry Analyst Prompt Library v1.2.0. Available even when the user does not re-upload it. Re-sync if the library version changes upstream.

## Skill boundaries (what NOT to do)

- Do not call `paula-article-writer`, `ms-docx-creator`, `ms-docx-colorful`, `ms-gartner-deck`, `ms-gamma-presenter`, `markdown-writer`, or `playbook-pdf-builder`. This skill is standalone and produces all formats itself.
- Do not use the @your-org personal identity. If the user wants that, redirect.
- Do not produce three-language versions automatically. If the user explicitly asks for PT-BR or ES, produce that single language; for three-language content route to `paula-article-writer`.
- Do not skip the intake contract paragraph. The user should always see the four resolved questions before research begins.
