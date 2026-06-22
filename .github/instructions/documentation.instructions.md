---
description: "Documentation standards for all Markdown: English, factual integrity, structure, and references."
applyTo: "**/*.md"
---

# Documentation Standards

Applies to every Markdown file in the workspace (READMEs, `CONTEXT.md`, `.github` content, notes).

## Language and voice

- Write in **English**. (App UI copy is trilingual; this rule is about documentation.)
- Be concise and direct. Prefer short sentences and scannable structure.
- Write "GitHub Copilot", never "Copilot" alone.
- No em dashes; use commas, parentheses, or restructure.

## Factual integrity

- **Never fabricate** metrics, KPIs, ROI, market data, statistics, or research findings.
- Every data claim must cite a credible source with a link: the client's audited workbooks and `CONTEXT.md`, official vendor docs (Microsoft Learn, GitHub Docs), or named analyst firms (Gartner, Forrester, IDC, McKinsey).
- If no source exists, state the value as an explicit assumption or omit it.
- Documents that present data must end with a **References** section listing the cited sources.

## Structure

- Start with a single H1 title and a one-paragraph summary of purpose.
- For folder READMEs, include: purpose, a contents table, status, how to run (if applicable), and references.
- Use tables for file/contents listings and relative links for cross-references.
- Use fenced code blocks for commands.

## Links

- Use workspace-relative links (for example `../gh-btg/README.md`).
- Keep links current when files move or are renamed.
