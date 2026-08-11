---
description: "Rules for AI-native architecture documents (the {system}_AI_Architecture.md produced by the AI-Native Engineer agent): required decisions, sourced claims, official icons, and copy conventions."
applyTo: "**/*_AI_Architecture.md"
---

# AI-Native Architecture Document Conventions

These rules apply to architecture documents produced by the `AI-Native Engineer` agent and the `design-agentic-system` prompt. They complement the general documentation standards.

## Required content

An AI-native architecture document must resolve and record all seven agentic decisions (from the `agentic-architecture-patterns` skill), each with a rationale and a source:

1. Model routing (task classes and the model per class, with a fallback).
2. Caching (prompt caching on stable prefixes, semantic caching with scoped keys and a threshold).
3. Memory (short term thread state and long term durable memory, scoped by tenant and user).
4. Context curation (window budget, retrieval ranking, history compaction).
5. Tools and MCP (small, well-described tool surface; governance).
6. Identity and guardrails (agent identity, managed identity, Content Safety, Prompt Shields, approval gates, tenant isolation).
7. Evaluation, observability, and cost (eval set in CI, OpenTelemetry GenAI tracing, spend attribution).

The document must also include: an executive summary, a service mapping, the diagrams (context, component, deployment, and a sequence for the critical path), a phased path (MVP then target), a non-functional analysis, risks and mitigations, and a References section.

## Factual integrity

- Never fabricate model limits, prices, or benchmarks. Verify against Microsoft Learn and the model card, cite the source, or state the value as an explicit assumption.
- End the document with a References section listing the cited sources with links.

## Diagrams

- Use the official Azure, Microsoft, and GitHub (Octicons) icon sets through the `azure-architecture-diagrams` skill.
- Do not modify, distort, or re-color official product icons. Color the containers and connectors instead.
- Keep the editable `.drawio` sources under an `output/` folder and embed exported SVG.

## Copy rules

- Write in English. Write "GitHub Copilot", never "Copilot" alone.
- No em dashes; use commas, parentheses, or restructure.
- Prefer managed identity over keys, least privilege, and private networking where the requirement calls for it.
