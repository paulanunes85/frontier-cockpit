# Research methods

How to actually conduct research for each scope.

## Scope decision tree

```
User attached an analyst prompt library (.md with prompts/frames)?
  YES → apply prompt library (see "Prompt library usage" below) + web triangulation
  NO  → continue

User attached source documents (RFP, transcript, report PDF, deck)?
  YES → synthesize attached docs first, then web for gap-filling
  NO  → continue

User's request mentions a public market, vendor, or technology?
  YES → web-first research
  NO  → ask the user where the source material lives
```

## Web research

Default capability: web search. Triangulation rules:

- Minimum 3 independent sources for any quantitative claim (market size, growth rate, customer count, revenue).
- Prefer primary sources: vendor 10-Ks and 10-Qs, official product pages, peer-reviewed papers, analyst firm public posts, regulatory filings.
- Secondary sources: tech press (TechCrunch, The Information, Stratechery), analyst blog summaries. Useful for context, weaker for numbers.
- Tertiary sources: forum posts, Reddit threads, blog aggregators. Use only for sentiment, never for facts.
- Always note publication date. Anything older than 18 months for a moving market gets a "stale" flag.

For competitive intel, search both the company's own materials AND independent reviews. Vendor self-positioning is a data point, not the truth.

## Document synthesis (uploaded files)

When the user attaches RFPs, transcripts, decks, or reports:

1. Read the full document before drafting any output.
2. Extract requirements (RFP), pain points (transcript), claims (deck), or findings (report).
3. Cluster extracted items into themes.
4. Map themes to the deliverable type's section structure.
5. Note what the document does NOT cover so you can flag gaps explicitly.

For transcripts: distinguish quoted speakers, attributed statements, and inferred meaning. Never put words in a real person's mouth.

For RFPs: produce a requirements traceability table as a default artifact. Every RFP requirement gets mapped to a proposed response section.

## Prompt library usage

When the user attaches an analyst prompt library (typically a markdown file with named prompts, frames, and rubrics):

1. Read the library end to end before researching.
2. **If the library is the Industry Analyst Prompt Library v1.x.x (bundled in `assets/templates/industry-analyst-prompt-library.md` or uploaded by the user), follow the structured workflow in `references/library-anti-patterns.md`.** That file specifies the Role + Domain + Output Format selection model and the mandatory anti-patterns from the library's Section 8.
3. For any other prompt library, infer its structure and apply the same general rule: the library wins on output structure and analytical method; this skill wins on identity tokens and editorial rules.
4. Cite the library version in the methodology block (e.g., "Industry Analyst Prompt Library v1.2.0, applied 2026-03-19, Role 4.1, Output Format 6.2").

### General library-recognition patterns

Common prompt library patterns to recognize across any library:
- Magic Quadrant frame (Ability to Execute vs Completeness of Vision, with Leaders/Challengers/Visionaries/Niche)
- Forrester Wave frame (Current Offering, Strategy, Market Presence)
- Hype Cycle frame (Innovation Trigger → Peak → Trough → Slope → Plateau)
- IDC MarketScape frame (Capabilities vs Strategies, with Leaders/Major Players/Contenders/Participants)
- Porter's Five Forces, SWOT, PESTLE for context analyses
- Role + Domain + Output Format selection model (see Industry Analyst Prompt Library for the canonical version)

## Source quality tiers (cite explicitly when relevant)

| Tier | Examples | Use for |
|---|---|---|
| A | SEC filings, official vendor documentation (docs.github.com, learn.microsoft.com, openai.com docs), GitHub Blog, official press releases, peer-reviewed papers, arXiv preprints from recognized labs | Quantitative claims, official positions, technical specifications |
| B | Major analyst firms (public posts), top-tier tech press (TechCrunch, The Verge, Bloomberg, Reuters), Microsoft Learn community blogs, recognized industry experts | Market context, trend signals, adoption signals |
| C | Vendor marketing pages, partner blog posts, sponsored content | Self-stated capabilities (label as "vendor claim") |
| D | Forums (GitHub Discussions, Stack Overflow), Reddit, anonymous reviews | Sentiment only, never quoted as fact |

In the final deliverable, the References section groups citations by tier when the deliverable type is "industry analyst report", "competitive intel brief", or "workshop / educational content".

## Recency discipline (mandatory)

Topics in this skill's scope (developer tools, AI platforms, cloud services, AI governance) move fast. Stale information is a credibility failure.

Rules:
- **Always search for the latest** on every empirical claim. Do not rely on training data alone for any vendor product, pricing, feature, or roadmap item.
- **Date every empirical claim**. Inline cites must include the publication date of the source.
- **Anything older than 12 months for a fast-moving topic gets a "may be stale" flag** in the prose or in the methodology block.
- **Search for the most recent updates explicitly** when the topic touches: pricing, billing models, model availability, feature releases, preview/beta features, governance policies, enterprise SKUs.
- **Consider preview, beta, Insider, and Canary channels**: when documenting a developer tool (VS Code, Visual Studio, GitHub Copilot, Azure AI Foundry, Microsoft Agent Framework), also search for what is currently in:
  - VS Code Insiders builds
  - GitHub Copilot Preview / experimental features
  - Azure preview features (microsoft.com/azure/preview-portal entries, "in preview" docs labels)
  - Microsoft Build / GitHub Universe announcements from the most recent event cycle
- **Cross-check vendor roadmap disclosures** against actual release notes and changelogs when the topic involves a "what's coming" statement.

When preview/Insider features are relevant, clearly label them ("Preview as of YYYY-MM-DD", "VS Code Insiders only", "Public preview in Azure AI Foundry") rather than presenting them as generally available.

## Academic papers (when topic-relevant)

For topics that have an active academic research footprint, search for and cite peer-reviewed or preprint papers. This applies especially to:

- Tokenization, attention mechanisms, KV-cache management
- Prompt compression, context distillation, long-context evaluation
- Agentic systems, autonomous coding agents, tool use
- Cost optimization, inference economics
- AI governance, model evaluation, benchmark methodologies
- Software engineering productivity metrics under AI tooling

Search venues to check:
- [arXiv](https://arxiv.org/) (cs.CL, cs.LG, cs.SE categories)
- [ACL Anthology](https://aclanthology.org/)
- [Google Scholar](https://scholar.google.com/)
- [ACM Digital Library](https://dl.acm.org/)
- [Semantic Scholar](https://www.semanticscholar.org/)
- Major lab publication pages (OpenAI, DeepMind, Microsoft Research, Google Research)

When a relevant paper exists, cite it (Tier A) in the Sources section. Even for educational content (workshop deliverable type), one or two well-chosen academic citations per chapter elevate credibility above vendor-doc-only content.

If no academic literature directly addresses the topic, say so explicitly in the methodology block ("No peer-reviewed literature was found that directly addresses [X]; the strongest available evidence is [Y]").

## Citation pattern

**All references in deliverables MUST be formatted as inline Markdown hyperlinks**, never as bare URLs and never as plain-text source names. The hyperlink target is the canonical URL of the source.

In Markdown source, prefer footnote-style for inline citations and full hyperlink format in the References section:
```
... GitHub Copilot reached 4.7M paid seats by Q3 2025 [^gh-q3-2025].

[^gh-q3-2025]: [Microsoft Q3 FY25 earnings call transcript, 30 Apr 2025](https://www.microsoft.com/en-us/Investor/earnings/FY-2025-Q3/press-release-webcast).
```

In HTML: numbered superscripts linking to a References section at the bottom; each entry is a clickable hyperlink.
In PDF: same as HTML, plus a dedicated final References page; weasyprint preserves the hyperlinks as clickable in the PDF.
In PPTX: a "Sources" slide as the penultimate slide; each entry is a hyperlink runnable in presentation mode.
In XLSX: a "Sources" sheet as the final tab with columns [ID, Claim, Source title, URL (hyperlinked), Date, Tier]. Use openpyxl `Hyperlink` on the URL cell.
In DOCX: footnotes via Word's native footnote system; hyperlink the URL within each footnote.

**Never leave a bare URL or a plain source name without a hyperlink anywhere in a deliverable.** This applies to the inline cites, the References section, and any in-line "see also" mentions.

## Methodology block (always include)

Every deliverable ends with a clearly labeled methodology block covering:

- Research scope (what was in scope, what was not)
- Source mix (counts by tier, date ranges)
- Assumptions made (numbered list)
- Known gaps and caveats
- Prompt library version applied, if any

This is non-negotiable. It is what separates a research deliverable from an opinion piece.
