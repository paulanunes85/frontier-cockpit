# Deliverable types

Full structure for each of the 6 deliverable types. Pick one per request based on Phase 1 intake.

## Table of contents

1. [Industry analyst report](#1-industry-analyst-report)
2. [Account dossier](#2-account-dossier)
3. [Technical research paper](#3-technical-research-paper)
4. [Competitive intel brief](#4-competitive-intel-brief)
5. [General research write-up](#5-general-research-write-up)
6. [Workshop / Educational content](#6-workshop--educational-content)

---

## 1. Industry analyst report

**Use when**: user asks for vendor landscape, market sizing, Magic Quadrant style, Forrester Wave style, Hype Cycle, capability matrix, market overview.

**Section structure**:

1. Executive summary (1 page max, 4 to 6 bullets, a single recommendation line)
2. Market definition and scope
   - What's in scope, what's not
   - Segment boundaries and adjacent markets
3. Market sizing and growth
   - TAM, SAM, SOM if applicable (show the math)
   - 3-year and 5-year growth projections with source ranges
4. Demand drivers and inhibitors
5. Vendor landscape
   - Vendor profiles (1 page each): description, target customer, key capabilities, GTM motion, recent moves, strengths, weaknesses
   - Quadrant or Wave chart placing each vendor (if prompt library specifies a frame, use it)
6. Capability matrix
   - Rows = vendors, columns = capabilities, cells = score or check
   - Always reproduce as XLSX with one row per vendor and one column per capability dimension
7. Adoption signals
   - Customer wins (publicly disclosed only)
   - Hiring trends, GitHub activity, conference presence
8. Recommendations
   - For buyers, for vendors, for the field team if Microsoft-relevant
9. Methodology and assumptions
10. References (grouped by tier)

**XLSX companion**: capability matrix as the primary sheet, vendor-by-criterion scores, weighted total column, source sheet at the end.

**PPTX companion**: 8 to 12 slide executive readout. Cover, scope, sizing, quadrant chart, top 3 vendors, capability heatmap, recommendations, methodology, references, closing card.

---

## 2. Account dossier

**Use when**: user names a specific company and asks for research about them as a customer, prospect, or partner.

**Section structure**:

1. Company snapshot
   - Legal name, HQ, employee count, revenue band, industry, ownership (public/private/PE-backed)
   - Recent 12-month news headlines (3 to 5 bullets)
2. Business context
   - Strategy and priorities (from earnings calls, investor decks, public statements)
   - Recent organizational changes
3. Technology footprint
   - Cloud presence (AWS, Azure, GCP, multi-cloud signals)
   - Developer tooling (GitHub presence, GitLab, Azure DevOps, Atlassian, etc.)
   - AI initiatives (announced or inferred)
   - Data platform (Databricks, Snowflake, native cloud, etc.)
4. Stakeholder map
   - Key roles relevant to the engagement (CIO, CTO, VP Eng, Head of Platform, etc.)
   - Public LinkedIn or press references only; never speculate on internal politics
5. Opportunity map
   - Pain hypotheses tied to public signals
   - Microsoft/GitHub plays that fit (GitHub Enterprise, GitHub Copilot, Azure AI Foundry, Copilot Studio, Microsoft Agent Framework)
   - Plays explicitly ranked by fit and ease, not by deal size
6. Competitive context
   - Incumbent vendors and recent vendor changes
7. Engagement plan
   - Suggested next 3 plays in sequence (week 1, weeks 2 to 4, quarter)
   - Required artifacts to produce
8. Sources

**DOCX companion**: full dossier as a Word document with cover, TOC, sections, closing card.
**PPTX companion**: 6 to 10 slide readout for an internal team meeting.

---

## 3. Technical research paper

**Use when**: user asks for architecture comparisons, benchmark analysis, design tradeoff studies, "how does X actually work" deep dives, evaluation of an approach.

**Section structure**:

1. Abstract (150 words)
2. Problem statement
3. Background and prior art
4. Methods
   - What was compared, against what criteria, using what data
5. Results
   - Tables, charts, key numbers
6. Analysis
   - Why the results look the way they do
   - Tradeoffs surfaced
7. Limitations
8. Recommendations and applicability
9. References

**No PPTX by default** for this type. If requested, produce a 6-slide technical readout: problem, methods, key chart, key finding, limitations, references.

---

## 4. Competitive intel brief

**Use when**: user asks for vendor-vs-vendor comparison, feature scorecard, positioning analysis, threat assessment.

**Section structure**:

1. TL;DR (3 bullets)
2. Vendors in scope
3. Feature comparison
   - Comparison table (rows = features, columns = vendors)
   - Always also produced as XLSX
4. Positioning
   - How each vendor describes itself (their own words)
   - Independent positioning (analyst and press framings)
5. Pricing and packaging (when public)
6. Win/loss themes
   - Where vendor A wins, where vendor B wins, where the buyer should look closer
7. Threat assessment (only when scoped to a Microsoft/GitHub product)
   - Where the competitor is gaining
   - Where the competitor is exposed
   - Microsoft/GitHub response options
8. Recommendations for the field
9. Sources

**HTML companion**: single-page scorecard with sticky header and a printable view.

---

## 5. General research write-up

**Use when**: the topic doesn't fit the four above (e.g., "investigate platform engineering maturity models", "explain the state of WebAssembly adoption in 2026", "summarize what changed in agentic frameworks last quarter").

**Section structure** (adapt to the question):

1. Question being answered (one sentence)
2. TL;DR (3 to 5 bullets)
3. Body (3 to 7 sections, named for what they cover, not for generic labels)
4. So what (implications for the reader)
5. Sources

This is the most flexible type. Default to a clear question-driven structure rather than forcing a template.

---

## 6. Workshop / Educational content

**Use when**: user asks for workshop content, training material, study material, course content, playbook content, curriculum, "do basico ao avancado" / "basic to advanced" content, or any multi-chapter educational deliverable. Common phrasings: "create complete content on X", "build me a workshop on X from basic to advanced", "I need study material on X", "create chapters about X for a playbook".

**File structure** (auto-generated):

```
workshop-{slug}/
├── 00-index.md                Master index
├── 01-{chapter-slug}.md       Chapter 1 (foundations)
├── 02-{chapter-slug}.md       Chapter 2
├── ...
├── NN-{chapter-slug}.md       Final substantive chapter
├── 99-references.md           Consolidated bibliography
└── (derived outputs in output/)
    ├── workshop-{slug}.pdf
    ├── workshop-{slug}.pptx
    └── workshop-{slug}.html
```

Chapter files use 2-digit zero-padded prefixes (`01-`, `02-`, ..., `99-`) so sort order matches reading order. The `99-references.md` is always the consolidated bibliography across all chapters.

**Master index (`00-index.md`) frontmatter**:

```yaml
---
title: "Workshop title"
author: "Frontier Cockpit Team, Software Global Black Belt, Microsoft"
contact: "frontier-cockpit@example.com"
date: "YYYY-MM-DD"
version: "1.0"
status: "draft"
deliverable_type: "workshop"
target_audience: "developers | platform engineers | engineering managers | mixed"
depth_scope: "foundations | basic_to_advanced | advanced_only"
chapter_count: 15
total_word_count_estimate: 75000
total_duration_hours: 12
---
```

**Master index sections**:

1. Title and metadata banner
2. Scope and out-of-scope (explicit boundaries)
3. Target audience and prerequisites
4. Total duration and delivery formats (self-study, instructor-led, async)
5. Workshop-level learning outcomes (5 to 10 outcomes covering the full curriculum)
6. Chapter map (table: chapter number, title, level, estimated duration, key concepts)
7. Tools and environment setup
8. How to use this material (different paths for different audiences)
9. Glossary (key terms used across chapters)
10. Methodology (research approach, source mix, library version if applied)

**Per-chapter file (`NN-{chapter-slug}.md`) frontmatter**:

```yaml
---
chapter: 04
title: "Chapter title"
slug: "chapter-slug"
level: "foundations | intermediate | advanced | reference"
estimated_duration_min: 45
prereqs: ["chapter-02", "chapter-03"]
learning_outcomes:
  - "Learner will be able to do X"
  - "Learner will be able to explain Y"
key_concepts:
  - "Concept A"
  - "Concept B"
---
```

**Per-chapter sections** (in order):

1. **Why this chapter matters** (motivation, 1 to 3 paragraphs, anchored to a real problem)
2. **Learning outcomes** (explicit list mirroring frontmatter, written learner-side)
3. **Core concept(s)** (the main pedagogical content, with diagrams or tables when helpful)
4. **Hands-on / examples** (concrete code, screenshots, walkthroughs, demos)
5. **Practice** (exercises the learner can do; optional for reference chapters)
6. **Common pitfalls and anti-patterns** (what goes wrong, why, how to avoid)
7. **Sources and further reading** (mandatory; every empirical claim in the chapter cited inline with footnote markers, and the Sources section at the bottom lists each citation as a hyperlinked Markdown reference). Must include at minimum: 1 to 3 Tier A primary sources (vendor docs, official blog, GitHub Docs, Microsoft Learn) AND, when the topic has an active academic literature, 1 to 2 papers from arXiv, ACL Anthology, ACM Digital Library, or equivalent. Every reference is a clickable hyperlink in the format `[Title with date](https://url)`, never a bare URL or plain text source name.
8. **What's next** (link to the next chapter and what it builds toward)

**Chapter level conventions**:

- **foundations**: assume no prior knowledge of the topic. Define every term. Use real-world analogies. Worked examples are simple but complete.
- **intermediate**: assume foundations chapters done. Move at normal pace. Examples are realistic but bounded.
- **advanced**: assume foundations and intermediate. Real-world complexity. Multi-system examples. Discussion of tradeoffs the foundations chapter glossed over.
- **reference**: not progressive; lookup-style content (glossary, pitfalls, references).

**Chapter sequencing rules**:

1. Foundations chapters come first, no exceptions.
2. Each intermediate chapter declares its foundations prereqs in frontmatter.
3. Advanced chapters can reference any earlier chapter as prereq.
4. Reference chapters (99-references.md, optional pitfalls index) come last.
5. Total chapter count is set by topic completeness, not by an artificial cap. If the topic genuinely needs 22 chapters, generate 22. If 6 suffices, generate 6.

**Editorial voice for workshop content**:

- Voice shifts from analyst-neutral to **expert instructor**. Still neutral on vendors and tools (library anti-pattern 8.2 still applies), but more pedagogical.
- Use the second person ("you") when addressing the learner directly. Avoid "we" except in explanations of collective practice.
- Worked examples must be complete and runnable. No "and so on" hand-waves on code.
- Diagrams as Mermaid or ASCII when possible (so they render in MD without external files). For complex visuals, generate inline SVG.
- Every empirical claim still cited per library anti-pattern 8.1.

**Workshop-level research**:

Run the same Gartner-style research pass that single-doc deliverables use, but applied across the topic's full surface. Triangulate quantitative claims. Apply library anti-patterns. Cite sources per chapter AND consolidate in `99-references.md`.

**Derived formats**: see workshop format recipes in `format-recipes.md` for the consolidated PDF playbook, PPTX facilitator deck, and HTML deck patterns.

---

## Choosing between types when ambiguous

- User names a market or category and multiple vendors → industry analyst report
- User names a single company as a customer/prospect → account dossier
- User names 2 to 4 vendors and asks to compare them → competitive intel brief
- User asks "how does X work" or "is approach A better than approach B" → technical research paper
- User asks for workshop, training, course, study material, playbook content, "do basico ao avancado", multi-chapter educational content, or anything that implies a learner audience and progressive depth → workshop / educational content (type 6)
- Anything else → general research write-up

When in doubt, ask one clarifying question rather than guessing.
