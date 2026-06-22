# Industry Analyst Prompt Library application workflow

This file is the operational guide for applying the Industry Analyst Prompt Library (v1.2.0 or later) when it is attached by the user or bundled in `assets/templates/`. The library itself lives at `assets/templates/industry-analyst-prompt-library.md`.

## When this guide activates

Activate this workflow whenever any of these are true:
1. The user attaches a file matching `Industry_Analyst_Prompt_Library_v*.md`.
2. The user explicitly references "the analyst prompt library", "Paula's prompt library", "the IDC/Gartner/Forrester library", or similar.
3. The user says "apply the library" or "use my analyst frames".
4. The bundled `assets/templates/industry-analyst-prompt-library.md` exists and the user has not opted out for this request.

When activated, this workflow REPLACES the default deliverable-type structure from `deliverable-types.md` with the library's selection model.

## The Role + Domain + Output Format selection model

The library is structured as a configuration tool, not a template. For every request, pick one option from each axis and combine them. The skill must walk this selection before drafting.

### Axis 1: Role variant (library Section 4)

Pick the role that matches the analytical posture the user needs:

| Role | When to pick |
|---|---|
| 4.1 Market Assessment & Vendor Evaluation | User compares vendors or assesses a category landscape |
| 4.2 Business Case & ROI Analysis | User builds investment justification or quantifies ROI |
| 4.3 Risk & Compliance Advisory | User assesses regulatory, security, or operational risk |
| 4.4 Technology Maturity & Innovation Scouting | User evaluates how mature a technology or category is |
| 4.5 Agentic AI Specialist | User asks about autonomous agents, agentic platforms |
| 4.6 Digital Transformation & Operational Metrics | User asks about productivity or transformation outcomes |
| 4.7 Strategic Planning & Board Communication | User needs executive or board-ready framing |
| 4.8 Knowledge Management & AI Maturity | User assesses organizational AI readiness |
| 4.9 Innovation Ecosystem & Startup Assessment | User evaluates startups or innovation pipelines |

If the request spans multiple roles, pick the dominant one and note the secondary in the methodology block. Do not stack roles; the role is a posture, not a checklist.

### Axis 2: Domain-specific prompt (library Section 5)

Pick the closest domain match, or fall back to the Master Analyst Prompt (Section 3) if no Section 5 prompt is a clean fit:

| Section | Use for |
|---|---|
| 5.1 Agentic AI Enterprise Readiness | Readiness assessments, autonomy levels, use case suitability |
| 5.2 AI Business Case Construction | ROI, cost-benefit, board-defensible business case |
| 5.3 AI Agent Platform Comparison | Comparing platforms used to build agents |
| 5.4 Workforce Impact & Headcount Planning | Job impact, productivity, reskilling |
| 5.5 Outcome-Driven Metrics Design | KPIs, dashboards, value-realization metrics |
| 5.6 Emerging Risk Assessment: AI Agents | Risk inventory for agentic deployments |
| 5.7 Startup Scoring & KPI Frameworks | Evaluating startups across a vertical |
| 5.8 AI-Native Development Tooling | SDD, Spec-Kit, Kiro, GitHub Spec Kit comparisons |

If no Section 5 prompt fits the topic (e.g., the topic is GenAI coding assistants generally, which spans editor-native plus agent-native and is not a clean Section 5.x match), use the Section 3 Master Analyst Prompt as the analytical base.

### Axis 3: Output format (library Section 6)

Pick the output format that matches the deliverable scope, NOT the topic:

| Section | Use for | Key required elements |
|---|---|---|
| 6.1 Executive Briefing | 1 to 2 page brief for time-constrained reader | Strategic Summary, Key Takeaways, Recommended Next Steps |
| 6.2 Deep-Dive Research Note | Multi-section research report | Strategic Summary, Market Context, Detailed Analysis, Comparative Analysis, **Recommendations by Horizon table (mandatory)**, Risks and Mitigations, References |
| 6.3 Vendor Comparison Matrix | Comparison-first deliverable | Evaluation Summary, Methodology, Vendor Profiles, **Weighted Comparison Matrix with canonical weights (Capability 30%, Enterprise 25%, Integration 20%, TCO 15%, Roadmap 10%)**, Trade-Off Analysis, Recommendation |
| 6.4 Quick Assessment Card | Single-card snapshot | Tight summary, three findings, one recommendation |

For analyst reports involving vendor comparison, default to **6.2 with 6.3 embedded** in the Comparative Analysis section. This is the highest-information output and matches the "industry analyst report" deliverable type when the library is active.

## Format selection table (library-active mode)

When the library is active, use this mapping instead of the default in `SKILL.md`:

| User-requested deliverable | Library output format | Embedded substructure |
|---|---|---|
| Industry analyst report | 6.2 Deep-Dive Research Note | 6.3 Weighted Matrix inside Comparative Analysis |
| Competitive intel brief | 6.3 Vendor Comparison Matrix | Standalone |
| Account dossier | 6.2 Deep-Dive Research Note | None |
| Technical research paper | 6.2 Deep-Dive Research Note | None |
| Executive briefing | 6.1 Executive Briefing | None |
| Quick scan | 6.4 Quick Assessment Card | None |

## Anti-Patterns (library Section 8), enforced as editorial rules when library is active

These are non-negotiable when the library is active. They layer on top of the skill's existing editorial rules.

### 8.1 No fabricated data

- Never fabricate market sizes, growth rates, customer counts, revenue figures, or ROI numbers.
- If specific data is not available in cited sources or training data, say "specific data not available" and provide qualitative directional guidance.
- Apply hedge language: "evidence suggests", "early indicators show", "directional rather than definitive", "specific data should be verified against [authoritative source]".
- For projected numbers, label as projection and identify the source's confidence level when stated.

### 8.2 No vendor bias

- Never advocate for a specific vendor unless the user explicitly asks for a recommendation.
- When comparison is asked, the weighted matrix is the neutral instrument; the recommendation derives from the matrix plus user-stated priorities, not from analyst preference.
- For Microsoft and GitHub products specifically: even though this skill is authored under the Microsoft GBB identity, vendor neutrality in analysis is the editorial standard. Identity tokens (logo, header, contact) do NOT extend to vendor advocacy.

### 8.3 No generic recommendations

Every recommendation must be concrete and operational. Required fields per recommendation:
- **Action**: one verb-led specific instruction
- **Owner**: a named role (CIO, VP of Engineering, BU Engineering Lead, etc.), not "the team" or "the organization"
- **Investment**: a quantitative range or "no new spend" / "internal effort only"
- **Expected outcome**: a measurable result or decision artifact

Reject any recommendation phrased as "the organization should develop an AI strategy" or similar.

### 8.4 Time horizons mandatory

Every recommendation table or list MUST anchor to time horizons:
- Immediate (0-30 days)
- Short-term (1-6 months), combined as **0-6m** in library 6.2 table
- Medium-term (6-18 months)
- Long-term (18-36 months)

Use the 0-6m / 6-18m / 18-36m grouping in tables to match library 6.2 schema. Recommendations without a horizon get rejected and require a horizon assignment before drafting completes.

### 8.5 Search project knowledge first (web analog, strengthened)

When operating without an attached knowledge base, the analog is:
- Cite sources inline for every empirical claim
- **Format every citation as a hyperlinked Markdown reference** (`[Title with date](https://url)`), never a bare URL or plain text source name
- Triangulate quantitative claims across at least 3 sources
- Label source tiers (A/B/C/D per `research-methods.md`)
- When sources conflict, present both and label the conflict
- **Always search for the most recent updates** on the topic before drafting (see Recency discipline in `research-methods.md`); never rely on training data alone for vendor pricing, features, or roadmaps
- **Include preview, beta, Insider, and Canary channel info** where relevant (VS Code Insiders, GitHub Copilot Preview features, Azure preview features)
- **Search for academic papers** when the topic has active research footprint (arXiv, ACL Anthology, ACM, Semantic Scholar, Google Scholar); at least 1 to 2 paper citations per long-form chapter when literature exists

## Microsoft AI governance products awareness

When a deliverable touches AI governance, observability, compliance, model selection at organizational scale, or FinOps for AI, **always evaluate whether Azure AI Foundry is a relevant tool to mention or cover**. Foundry provides org-level model catalog, agent governance, hub management, cost tracking, audit logs, and content safety policies that complement GitHub Copilot at the team and enterprise level.

The skill should not push Foundry where it is not relevant (anti-pattern 8.2 vendor bias still applies), but should not omit it when governance, observability, or multi-workload AI cost attribution are in scope. Specifically:
- For workshop content covering GitHub Copilot governance: include Foundry as a discrete topic, not a footnote
- For account dossiers where the company has multi-workload AI: include Foundry footprint assessment
- For competitive intel where Foundry competes (Bedrock, Vertex AI), include it in the vendor set

## Mandatory methodology block additions

When the library is active, the methodology block at the end of the deliverable MUST include:

1. The library name and version applied (e.g., "Industry Analyst Prompt Library v1.2.0 (2026-03-19)")
2. The Role variant applied (e.g., "Role 4.1 Market Assessment & Vendor Evaluation")
3. The Output Format applied (e.g., "Output Format 6.2 Deep-Dive Research Note with embedded 6.3 Weighted Comparison Matrix")
4. A compliance check listing each anti-pattern from Section 8 with how it was applied in this deliverable
5. Any library weights or schemas applied without modification (e.g., "Library 6.3 weights applied without modification: Capability 30%, Enterprise 25%, Integration 20%, TCO 15%, Roadmap 10%")

## Master Analyst Prompt constraints (always layered)

When the library is active, also apply these constraints from the library's Section 3 Master Analyst Prompt:

- Ground all analysis in data, frameworks, and recognized methodologies
- Use consultative language, not commercial or promotional
- Present trade-offs and risks alongside benefits
- Distinguish between what is proven vs. what is projected
- Use hedge language appropriately

## What to do when library and skill conflict

| Domain | Wins |
|---|---|
| Output structure (section names, order, mandatory tables) | Library |
| Analytical method (frames, scoring schemas, weights) | Library |
| Identity tokens (palette, fonts, header, contact, logo) | Skill |
| Editorial rules (no em dashes, "GitHub Copilot" in full, territory-neutral default) | Skill |
| Format-specific recipes (XLSX banded rows, PDF cover layout, DOCX styles) | Skill |
| Methodology block requirements | **Both layer**: skill requires methodology block; library adds mandatory contents to it |
| Recommendations format | Library (Horizon-anchored table from 6.2) |
| Source citation pattern | **Both layer**: skill defines citation tiers, library mandates inline citation and anti-pattern 8.1 hedge |

When in doubt: identity and editorial = skill; analytical structure and output organization = library.
