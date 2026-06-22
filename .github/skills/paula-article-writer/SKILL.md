---
name: paula-article-writer
description: >
  Use this skill whenever the user wants to write, draft, or generate a technical article,
  Medium post, or long-form publication piece, especially on AI, software engineering, or
  agentic systems. Activate for requests in any language (English, Portuguese, Spanish) that
  ask to produce original written content for external audiences: "write an article",
  "escrever artigo", "publicar no Medium", "post técnico", "write a technical piece",
  "long-form", or any request for multiple language versions (EN + PT-BR + ES, "nas três
  línguas", "three languages"). Also activate for requests to write in Frontier Cockpit Team's voice
  or @your-org style. Always delivers three language versions by default.
  DO NOT USE FOR: internal docs, specs, READMEs, translations of existing content,
  summaries, or short social posts.
---

# Paula Article Writer Skill

This skill encodes Frontier Cockpit Team's empirical, practitioner-voice writing style for technical
articles, Medium posts, and long-form publications. Every article produced by this skill
must be output in **three language versions**: English (EN), Brazilian Portuguese (PT-BR),
and Latin American Spanish (ES).

---

## 0. GitHub Copilot execution mode

Use GitHub Copilot Chat or agent mode depending on the task shape.

| Task | GitHub Copilot mode | Notes |
|------|---------------------|-------|
| Writing full article (EN + PT-BR + ES) | Ask | Keep one canonical argument and produce three versions. |
| Translating existing EN article to PT-BR / ES | Ask | Preserve meaning, terminology, and citations. |
| Generating references section only | Ask | Verify every cited claim. |
| Researching sources before writing | Agent mode | Use when files or web/source collection must be created. |
| Quick summary or outline | Ask | Keep it short and clearly labelled as draft. |

Article writing has high ambiguity: voice consistency across 3 languages, empirical claim accuracy, and structural coherence. Spend effort on source integrity, outline quality, and language-specific nuance before drafting. Do not invent metrics or citations.

---

---

## 1. Identity and Voice

Every article is written from Paula's first-person practitioner perspective:

```
Frontier Cockpit Team
AI-Native Software Engineer · @your-org
~20 years in technology · Latin America enterprise focus
```

**Byline block** (always at the end of the introduction section, before the first `---`):

```markdown
**Frontier Cockpit Team** · [@your-org](https://github.com/your-org)
[Month YYYY]
```

### Tone Rules

- **Empirical, not hype.** Every claim is traceable to a paper, analyst report, or lived
  observation. No marketing language, no superlatives without evidence.
- **Practitioner voice.** Paula speaks from field work with enterprise teams in LATAM.
  Reference this context when grounding problems ("I kept seeing this in my day-to-day work").
- **Casual and personal.** Write in first person, like you are talking to a colleague over
  coffee. Use "I", "I've been", "what I found", "honestly", "the thing is". Not academic.
- **Direct.** Short declarative sentences. Active voice. No hedging qualifiers unless
  genuinely uncertain.
- **Paragraphs max 4 sentences.** Dense walls of text lose readers. One idea per paragraph.
- **No em-dashes (-) anywhere. This is a hard rule.** Paula's voice uses short, declarative
  sentences instead of interrupting clauses. If you find yourself typing "-", stop and rewrite.
  Break into two sentences, or use a comma, or use a colon. Never use "-" in any context.
  Examples of how to fix em-dash usage:
  - WRONG: `The model you use-along with the context you feed it-determines quality.`
  - RIGHT: `The model you use matters, but so does the context you feed it. Together they determine quality.`
  - WRONG: `Teams were failing-wasted inference, slow reviews, bad coordination.`
  - RIGHT: `Teams were failing: wasted inference, slow reviews, bad coordination.`
  - WRONG: `a three-tier system-hot memory, domain agents, cold docs-cuts context collapse.`
  - RIGHT: `a three-tier system (hot memory, domain agents, cold docs) cuts context collapse.`
- **No bullet dumps.** Lists only when items are genuinely enumerable. Prefer prose for
  connected ideas.
- **Bold for key terms on first introduction**, not for decoration.
- **No hype words**: revolutionary, game-changing, unprecedented, powerful, seamlessly,
  robust, leverage (as verb), unlock, unleash, harness.

---

## 2. Article Structure

### Standard Article Layout

```markdown
# [Title]: [Subtitle with evidence hook]

*[Single italic paragraph, the problem statement that earns the read.
  Max 3 sentences. Must contain a concrete empirical claim or field observation.]*

---

[Author introduction, 3 to 5 paragraphs of first-person field context.
 Explains WHY Paula wrote this. Names the specific problem she kept encountering.
 Ends with the byline block.]

**Frontier Cockpit Team** · [@your-org](https://github.com/your-org)
[Month YYYY]

---

## Introduction

[MANDATORY SECTION, every article must have a full Introduction section.
 This is NOT the opening italic block. It is a full standalone section that:

 1. DESCRIBES THE TOPIC in depth, what it is, how it works, why it matters now.
    Treat this as the "executive briefing" someone needs before reading the rest.
    Cover: definition, current state of the field, key tensions or open questions.

 2. EXPLAINS THE IMPORTANCE, why should the reader care? What changes if they
    understand this well vs. if they ignore it? Use concrete costs and stakes.

 3. SHARES PERSONAL MOTIVATION, why Paula is writing about this, in her own words.
    First person, casual tone. "I've been thinking about this a lot lately because..."
    "The honest reason I wrote this is..." "What triggered this was a conversation
    I kept having over and over with teams across LATAM."

 4. SETS UP THE ARTICLE, closes with what the reader will get from reading on.

 Length: 4 to 8 paragraphs. This is the longest single section. Earn the scroll.]

---

![Image alt text](png/filename.png)

---

## 1. [Section Title]

[Content]

---

## 2. [Section Title]

[Content]

---

## [N]. Key Takeaways

[Numbered list of actionable conclusions, each starting with bold claim + explanation.
 Max 10 items. Each item: **bold claim sentence.** Then 1-2 sentences of evidence.]

---

## References

[See References section spec below]
```

### Title Convention

- Pattern: `[Concrete Noun]: [Evidence-Based Claim Across the SDLC / In Production / etc.]`
- Good: `Right Model, Right Task: Evidence-Based LLM Routing Across the SDLC`
- Bad: `How AI Is Revolutionizing Developer Workflows`

### Opening Italic Block

The italic paragraph under the title is the article's contract with the reader. It must:
1. Name the specific cost of the problem (not just "this is hard")
2. Signal that evidence will be provided (not opinion)
3. Preview the scope (what phases, what tools, what decisions)

Example:
```markdown
*Choosing the wrong model for a given SDLC phase does not just waste money.
It actively degrades output quality. This guide maps empirical research findings
to practical routing decisions across every phase of software development,
including VS Code primitives, GitHub Copilot chat modes, agents, skills,
hooks, and extended thinking tradeoffs.*
```

---

## 3. Writing Patterns

### Field Grounding Pattern

Use this to open sections or the introduction. Ground the technical claim in a
real enterprise scenario Paula encounters. The tone should feel like a conversation,
not a report:

```
I kept running into the same situation over and over in my day to day work.
[Concrete scenario. What the client does. What goes wrong. What it costs them.]
I call it the [named pattern], and it is more common than people admit.
```

Variations that reinforce the casual, personal voice:
```
Honestly, I was surprised when I first saw the numbers.
The thing is, most teams I work with don't even notice this is happening.
I've had this conversation so many times now that I decided to write it down.
What made me dig into this was a client in [Brazil / LATAM / financial sector]
who was doing everything "right", and still running into the same wall.
```

### Empirical Claim Pattern

Every quantitative claim must be formatted as:

```
[Study description] found that [specific finding with numbers].
```

Inline citation format: `(arXiv:XXXXXXXXX)` or named author reference.

Examples:
- `A randomized controlled trial with 16 experienced open-source developers found that
  allowing AI tools increased completion time by 19%, despite developers estimating a
  20% speedup.`
- `An empirical study of 304,362 AI-authored commits across 6,275 GitHub repositories
  found that AI-generated code tends to introduce higher shares of requirement and test debt.`

### Named Problem Pattern

Paula names enterprise anti-patterns to make them discussable:

- **Agent cemetery problem**: agents created without strategy, abandoned within months
- **Cognitive surrender**: adopting AI outputs with minimal scrutiny
- **Intent debt**: goals and rationale never captured as artifacts
- **Triple Debt**: Technical + Cognitive + Intent debt accumulating in parallel

When introducing a named pattern, define it concisely:
```
I call it the [name], and [one sentence definition].
[One sentence on why it is more common/dangerous than people admit.]
```

### Blockquote Usage

Use blockquotes sparingly, only for direct findings from papers where the exact wording
matters (legal weight, precise technical claim, or memorable formulation):

```markdown
> A model that declared a puzzle impossible when confined to text-only generation,
> once given agentic tools, not only solved it but mastered variations of complexity
> far beyond the reasoning cliff it previously failed to surmount.
```

Never use blockquotes for Paula's own observations or paraphrased content.

---

## 4. Technical Terminology Rules

### Preserve in All Languages

These terms are NEVER translated. They appear identically in EN, PT-BR, and ES:

**Products and tools:**
VS Code, GitHub Copilot, GitHub Copilot Chat, GitHub Copilot CLI, GitHub Copilot coding agent,
GitHub Copilot cloud agent, GitHub Models, Azure AI Foundry, Microsoft Copilot, Copilot Studio

**Technical concepts:**
agent, agents, routing, model routing, LLM, LRM, SDLC, SDD, TDD, spec, specification,
prompt, prompt file, skill, SKILL.md, AGENTS.md, hook, hooks, preToolUse,
postToolUse, handoff, token, tokens, context window, frontmatter, workspace, codebase,
patch, pull request, commit, scaffold, scaffolding, CI/CD, YAML, JSON, markdown,
ask mode, plan mode, agent mode, chain-of-thought, reasoning model,
compound AI, multi-agent, subagent, in-context learning, instruction following,
intent debt, cognitive debt, technical debt, cognitive surrender, agent cemetery,
CONSTITUTION.md, SPECIFICATION.md, IMPLEMENTATION_PLAN.md, applyTo, lazy-loaded,
read-only, feedback loop, test runner, compiler, docstring, changelog, README,
benchmark, leaderboard, SWE-bench, FeatureBench, HumanEval, MBPP, RCT

**Siglas e formatos acadêmicos:**
arXiv IDs (arXiv:XXXXXXXXX), EARS, Given/When/Then, Pareto-efficient,
difficulty-aware routing, overthinking, Analysis Paralysis, Rogue Actions,
Premature Disengagement

---

## 5. References Section

The References section is a **critical design element** of every article.
It signals empirical rigor and enables readers to verify claims.

### Format Rules

```markdown
## References

- Author(s) (Year). *Title in italics*. Source. arXiv:XXXXXXXXX or URL
- *Title in italics* (no author on paper). Source. arXiv:XXXXXXXXX
```

### PDF Rendering

In PDF output, References always render as:
- **Separate final page** (`page-break-before: always`)
- **2-column layout** to fit more refs per page
- **Font size 7.5pt**, smaller than body text, visually distinct
- **Italic titles** in the list

### In-text Citation Style

Use parenthetical inline citations for specific claims:

```markdown
A model achieving 74.4% resolved rate on SWE-bench succeeds on only
**11.0% of tasks in FeatureBench** (arXiv:2509.16941).
```

Or named-author style:
```markdown
Storey (2026) defines three compounding debt types: Technical, Cognitive,
and Intent (arXiv:2603.22106).
```

---

## 6. Key Takeaways Section

The Key Takeaways section is mandatory for all articles. Format:

```markdown
## [N]. Key Takeaways

**1. Bold claim sentence.** Supporting evidence sentence. Actionable implication.

**2. Bold claim sentence.** Supporting evidence sentence. Actionable implication.
```

Rules:
- Maximum 10 items
- Each item starts with a number in bold claim
- Claim sentence is self-contained (reader can scan just the bold lines)
- Supporting sentence adds the evidence number or study reference
- Final sentence is a concrete action for the reader
- No sub-bullets inside takeaways

---

## 7. Three-Language Output Protocol

Every article produced by this skill MUST be delivered in three versions.
This is non-negotiable and applies by default, the user does not need to ask for it.

### Output Files

```
outputs/articles/
  {Slug}_EN_{YYYY-MM-DD}.md
  {Slug}_PTBR_{YYYY-MM-DD}.md
  {Slug}_ES_{YYYY-MM-DD}.md
```

### Translation Rules

**PT-BR version:**
- Full Brazilian Portuguese prose
- Preserve all technical terms from Section 4 in English
- Decimal separator: comma (1.234,56 not 1,234.56)
- Date format: DD de [month] de YYYY
- Byline: `Abril 2026` (month in Portuguese)

**ES version:**
- Full Latin American Spanish prose (not Spain Spanish)
- Preserve all technical terms from Section 4 in English
- Decimal separator: comma (1.234,56)
- Byline: `Abril 2026` (month in Spanish)
- Prefer LATAM phrasing: "computadora" not "ordenador",
  "celular" not "móvil", "recursos" not "prestaciones"

### What to Translate vs. Preserve

| Element | EN | PT-BR | ES |
|---------|----|----|-----|
| Prose paragraphs | ✓ | Translate | Translate |
| Section headings | ✓ | Translate | Translate |
| Table headers | ✓ | Translate | Translate |
| Table cell content (prose) | ✓ | Translate | Translate |
| Table cell content (technical) | ✓ | Preserve EN | Preserve EN |
| Code blocks | ✓ | Preserve EN | Preserve EN |
| Product names | EN | Preserve EN | Preserve EN |
| arXiv IDs | EN | Preserve EN | Preserve EN |
| Reference titles | Italics | Preserve EN | Preserve EN |
| Reference source names | EN | Preserve EN | Preserve EN |
| Byline name | Frontier Cockpit Team · @your-org | Frontier Cockpit Team · @your-org | Frontier Cockpit Team · @your-org |
| Byline GitHub | @your-org link | Preserve | Preserve |

---

## 8. PDF Generation

When producing PDF output, apply these settings:

```css
/* Page */
@page { size: A4; margin: 18mm 16mm 22mm 16mm; }
/* Body */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
font-size: 10.5pt; line-height: 1.65; color: #2C2C2A;
/* H1 */ font-size: 22pt; font-weight: 700;
/* H2 */ font-size: 14pt; border-bottom: 2pt solid #E8E6DF; page-break-after: avoid;
/* H3 */ font-size: 11.5pt; page-break-after: avoid;
/* Code blocks */ background: #1E1E1E; color: #D4D4D4; font-size: 8.5pt;
/* Tables */ font-size: 9pt; th background: #2C2C2A; color: white;
/* Blockquotes */ border-left: 3pt solid #0078D4; background: #F5F8FC;
/* References page */ page-break-before: always; column-count: 2; font-size: 7.5pt;
/* Images */ max-width: 100%; display: block; margin: 12pt auto; border-radius: 4pt;
/* Page numbers */ @bottom-center: counter(page); font-size: 9pt; color: #888780;
```

PDF filenames:
- EN: `{English_Title_Underscored}_Paula_Silva_{YYYY-MM-DD}.pdf`
- PT-BR: `{Titulo_PT_Underscored}_Paula_Silva_{YYYY-MM-DD}.pdf`
- ES: `{Titulo_ES_Underscored}_Paula_Silva_{YYYY-MM-DD}.pdf`

---

## 9. Images in Articles

When an article includes diagrams or data visualizations:

- Reference images as `![Alt text](png/filename.png)` in the markdown source
- For PDF and final deliverables, embed as base64 inline
- Alt text must describe the content and key finding:
  `![Triple Debt Model, Technical, Cognitive, and Intent Debt form a reinforcing cycle](png/01-triple-debt-model.png)`
- Place images immediately after the section heading that introduces them
- Separate from surrounding text with `---` dividers above and below

---

## 10. Quality Checklist

Before delivering any article, verify:

- [ ] Opening italic block: concrete claim + evidence signal + scope preview
- [ ] Byline block present before first `---`, uses `@your-org` format, NOT Microsoft title
- [ ] **Introduction section present** (mandatory, 4-8 paragraphs):
  - [ ] Describes the topic in depth (what it is, how it works, current state of field)
  - [ ] Explains the importance (concrete stakes, costs of not understanding it)
  - [ ] Personal motivation in first person, casual tone ("I've been thinking...", "The honest reason...")
  - [ ] Closes with what the reader will get from reading on
- [ ] First-person voice is casual throughout, "I", "I've been", "what I found"
- [ ] Every quantitative claim has inline citation (arXiv ID, named study, or analyst report)
- [ ] No hype words (revolutionary, game-changing, seamlessly, leverage, unlock)
- [ ] No em-dashes anywhere in the text
- [ ] Paragraphs max 4 sentences
- [ ] Key Takeaways section present, numbered, bold claims scannable
- [ ] References section present, italicized titles, arXiv IDs where applicable
- [ ] All technical terms from Section 4 preserved in English across all versions
- [ ] Three language versions produced: EN, PT-BR, ES
- [ ] PDF: references on separate page, 2-column, 7.5pt font
- [ ] PDF: page numbers, A4, correct margins
- [ ] No placeholder text (TODO, TBD, [fill in])

---

## 11. Paper Corpus: Where to Look

Paula's complete research corpus lives in the `papers/` folder in her workspace.
**Always consult this folder before writing any article.** Never invent citations.

### Folder Structure

```
papers/
├── paper-map.md                  ← PRIMARY INDEX, start here every time
├── research-papers/              ← ~100 PDFs (arXiv + industry reports)
├── analyst-reports/              ← ~164 reports (IDC, Gartner, Forrester, CNCF, etc.)
└── primitives/                   ← 6 AI-Native SDLC playbooks
    ├── 01-context-engineering.md
    ├── 02-model-routing.md
    ├── 03-sdd-spec-driven.md
    ├── 04-skills-slash-commands.md
    ├── 05-quality-gates-hooks.md
    └── 06-multi-agent-orchestration.md
```

### How to Use the Corpus

1. **Open `papers/paper-map.md` first.** It has a thematic index (ÍNDICE TEMÁTICO)
   organized by topic. Find the relevant theme section and note the arXiv IDs.
2. **Read the paper ficha** (entry) in paper-map.md for the specific numbers and findings.
3. **Use the Quick Reference table** at the bottom of paper-map.md for the most
   important metrics across all papers in one view.
4. Only open a PDF from `papers/research-papers/` if you need deeper detail beyond
   the ficha summary.

### Quick-Reference Lookup by Topic

Use these arXiv IDs to find the right paper for each topic.
All fichas with full findings are in `papers/paper-map.md`.

**Model Routing and Cost Optimization:**
`2505.01622` (Extended Thinking benchmark) · `2604.07502` (Semantic Density Principle)
`2601.14470` (Tokenomics in agentic systems) · `2602.16873` (AdaptOrch topology selection)
`2603.29919` (SkillReducer cost compression) · `2504.10903` (Illusion of Thinking)
`2507.17699` (Thinking Isn't Illusion) · `2506.18957` (Agentic Gap reframing)

**Spec-Driven Development and Requirements:**
`2601.03878` (CURRANTE: SDD empirical workflow) · `2602.00180` (SDD: Code to Contract)
`2602.02584` (Constitutional SDD: -73% security defects) · `2603.22106` (Triple Debt: Storey)
`2603.16975` (State of GenAI: planning phases have lowest adoption)
`2601.00477` (Security PRs: lower merge rate, higher scrutiny)

**Agents and Context Primitives:**
`2602.20478` (Codified Context Infrastructure: hot/warm/cold tiers)
`2603.05344` (OpenDev: 5 workload types) · `2601.20404` (AGENTS.md: -28.64% runtime)
`2602.12430` (Agent Skills SKILL.md: 3 paradigms, 4-tier governance)
`2603.29919` (SkillReducer: 26.4% without routing description)
`2506.05370` (Contextual Memory Intelligence) · `2603.09619` (Context Engineering pyramid)
`2510.04618` (ACE ICLR2026: +10.6% via evolving playbooks)
`2510.21413` (Context Engineering for AI Agents in OSS)
`2505.19443` (Vibe Coding vs Agentic Coding: 4 maturity dimensions)

**Multi-Agent Architecture and Orchestration:**
`2602.16873` (AdaptOrch: 4 topologies, 12-23% improvement)
`2601.12538` (Agentic Reasoning Survey: 3 layers)
`2601.17542` (Cognitive Platform Engineering: 4-plane architecture)
`2604.02547` (Behavioral Drivers: LLM > Framework; 9,374 trajectories)
`2504.11805` (Planner-Coder Gap: 75.3% MAS failures)
`2603.15911` (Human-AI Code Review Synergy: 29.6 vs 4.1 tokens/line)

**Testing and Code Review:**
`2602.07900` (Agent-Generated Tests: 74.4% writes tests, frontier reasoning model)
`2603.23448` (c-CRAB: 40% code review tasks solved)
`2604.03196` (CRA Reality: 45.20% merge vs 68.37% human)
`2603.23443` (LLM Test Under Evolution: 66% pass rate with semantic changes)
`2603.13724` (AI Test Generation: 16.4% commits)
`2601.13597` (AI IDEs Causal: +18% warnings, +39% cognitive complexity)
`2312.04687` (LLM4TDD: 5 best practices) · `2404.10100` (LLMTCG: +20% pass@1 with loop)
`2508.18771` (AI Code Review: 58.6% suggestions accepted; security 73%)
`2505.16339` (Hybrid review pipeline: +40% efficiency)

**Security and Vulnerabilities:**
`2504.21774` (MCP Protocol Security: 4 lifecycle phases, 16 threats)
`2604.04288` (LLM OSS Vulnerabilities: Supply Chain 44%)
`2601.00477` (Security PRs: 14.6% security-focused coding agent)
`2503.23278` (MCP Landscape: 31 threats catalogued)
`2502.01853` (Security in LLM-Generated Code: -45% vulns with security context)

**Productivity, Adoption, and Impact:**
`2601.18341` (Agent adoption GitHub: 22.20-28.66% by Feb 2026)
`2603.16975` (State of GenAI: 79% devs daily; 70% reduce boilerplate)
`2601.10258` (JetBrains Longitudinal: AI users write+delete more, fragment workflow)
`2602.03593` (Beyond the Commit: 6 productivity dimensions; SPACE/DORA insufficient)
`2601.20245` (Skill Formation: AI harms library skills -17% quiz)
`2509.20353` (Developer Productivity with GitHub Copilot: +26% PRs, -review quality)
`google-faros` (AI Productivity Paradox: +98% PRs, +91% review time, +9% bugs)
`2507.09089` (METR RCT: +19% time increase despite -20% perceived speedup)

**Platform Engineering and Cloud-Native:**
`cncf-agentic` (CNCF Autonomous Enterprise: 4 pillars)
`cncf-standards` (CNCF Cloud-Native Agentic Standards 2026)
`2601.17542` (Cognitive Platform Engineering reference architecture)

**Benchmarks and Agent Evaluation:**
`495_featurebench` (FeatureBench: frontier reasoning model 4.5 = 11.0% on real features)
`2509.16941` (SWE-bench Pro: long-horizon tasks)
`2512.12730` (NL2Repo-Bench: repository-level generation)
`2505.09027` (Tests as Prompt: TDD benchmark)
`2505.05283` (SDLC AI Perspective: 61% benchmarks = implementation only)

**SE 3.0 and Agentic Software Engineering:**
`2507.15003` (Rise of AI Teammates: SE 3.0 paradigm)
`2509.06216` (Agentic SE Foundational Pillars: 5 pillars, research agenda)
`2509.14745` (Agentic Coding PRs GitHub: 83.8% accepted, 54.9% unmodified)

### Most Important Numbers (Quick Reference)

These are the headline metrics to cite most frequently:

| Metric | Value | arXiv ID |
|--------|-------|----------|
| Extended thinking on iterative tasks | -30% quality, +43% cost | 2505.01622 |
| AGENTS.md human-curated | -28.64% runtime, -16.58% tokens | 2601.20404 |
| AGENTS.md LLM-generated | -3% worse than no file | 2601.20404 |
| Constitutional SDD security defects | -73% | 2602.02584 |
| Code review token spend | 59.42% of all agent tokens | 2601.14470 |
| applyTo scoping | -68% instruction tokens | Paula's guide |
| FeatureBench (frontier reasoning model 4.5) | 11.0% solve rate | 495_featurebench |
| Agent adoption on GitHub | 22–28% by Feb 2026 | 2601.18341 |
| CRA merge rate vs human | 45.20% vs 68.37% | 2604.03196 |
| Planner-coder gap | 75.3% of MAS failures | 2504.11805 |
| SkillReducer description compression | 48% smaller, +2.8% quality | 2603.29919 |
| Agent-generated code complexity | +39% cognitive complexity | 2601.13597 |
| LLM > Framework | Consistent across 9,374 trajectories | 2604.02547 |
| Supply chain in LLM OSS | 44% of vulnerability advisories | 2604.04288 |
| AI Productivity Paradox | +98% PRs, +91% review time, +9% bugs | google-faros |
| TDD interactive loop | +20% pass@1 | 2404.10100 |
| MCP security threats | 31 threats catalogued | 2503.23278 |
| GitHub Copilot throughput | +26% PRs (4–6 week ramp) | 2501.13282 |
| Security context in prompts | -45% vulnerabilities | 2502.01853 |
| METR RCT (16 devs) | +19% time despite -20% perceived speedup | 2507.09089 |

## 12. Reference Corpus: Analyst Reports

When an article requires empirical citations, draw from this verified corpus.
Never invent data. If a claim cannot be traced to a source below, omit it.

### Context Engineering and Intent Engineering

| arXiv | Authors / Year | Key finding to cite |
|-------|---------------|---------------------|
| 2603.09619 | Vishnyakova 2026 | 4-layer pyramid: prompt → context → intent → specification engineering. "Whoever controls the agent's context controls its behavior; whoever controls its intent controls its strategy." |
| 2510.04618 | Zhang et al. 2025, ACE | Agentic Context Engineering: treats contexts as evolutionary playbooks. +10.6% agent benchmarks, +8.6% financial analysis. Solves brevity bias and context collapse. |
| 2602.20478 | Vasilopoulos 2026, Codified Context | 108k lines C#, 283 dev sessions. 3-tier: Hot Memory (Constitution), Domain Specialists (19 agents), Cold Memory (34 spec docs). |
| 2601.11595 | Jayanti et al. 2026, CA-MCP | Shared Context Store (SCS): agents read/write shared context memory. Reduces LLM calls for complex tasks, fewer failures when conditions unmet. |
| 2602.14878 | 2026, MCP Tool Description Smells | Textual imperfections in MCP tool descriptions propagate as spec errors that affect agent behavior. Analogy to code smells. |

### MCP and Compound AI

| arXiv | Authors / Year | Key finding to cite |
|-------|---------------|---------------------|
| 2503.23278 | Hou et al. 2025, MCP Landscape (ACM TOSEM) | Security threats taxonomy, attack surface classification for MCP. |
| 2603.13417 | 2026, MCP Design Patterns | 10,000+ active MCP servers in production. 97 million monthly SDK downloads in early 2026. |
| 2506.04565 | Chen et al. 2025, Compound AI Survey | Survey of compound AI system architectures and patterns. |
| 2506.05370 | 2025, CMI: Contextual Memory Intelligence | Contextual memory patterns and retention strategies. |
| 2603.05344 | Becker et al. 2026, OpenDev | 5 workload categories: Action (fast execution), Thinking (reasoning, no tool distraction), Vision (multimodal), Compaction (cheap summarization), Subagent (parallel specialized). |

### Technical Debt and Productivity

| Source | Authors / Year | Key finding to cite |
|--------|---------------|---------------------|
| arXiv:2603.22106 | Storey 2026, Triple Debt | Three compounding debt types: Technical (code shortcuts), Cognitive (cognitive surrender, developers accept AI output without understanding), Intent (goals/rationale never captured as artifacts). |
| arXiv:2603.28592 | Liu et al. 2026, Debt Behind AI Boom | 304,362 AI-authored commits, 6,275 GitHub repos. AI-generated code introduces higher shares of requirement debt and test debt. Developers defer completion and validation. |
| arXiv:2507.09089 | Becker et al. 2025, METR RCT | 16 experienced open-source developers. AI tools increased completion time +19% despite developers estimating -20% (speedup). Perception and reality are inverted. |
| arXiv:2302.06590 | Peng et al. 2022, GitHub Copilot RCT | +55.8% faster on isolated synthetic task (controlled, one programming language, no context). |
| SSRN:4945566 | Cui, Demirer, Peng, Microsoft/Accenture RCT | +26% weekly task completion in real enterprise environment. |

### Reasoning Models and Agent Behavior

| arXiv | Authors / Year | Key finding to cite |
|-------|---------------|---------------------|
| 2506.06941 | Shojaee et al. (Apple) 2025, Illusion of Thinking | LRMs exhibit accuracy collapse on planning puzzles beyond certain complexity thresholds when tested without tools. |
| 2506.18957 | Khan et al. 2025, Agentic Gap | Collapse was experimental artifact of text-only evaluation. With agentic tools, LRMs not only solved previously impossible puzzles but mastered harder variations. |
| 2507.17699 | 2025, Thinking Isn't Illusion | With tool augmentation (Python interpreters, scratchpads), LRMs consistently outperform non-reasoning models across all complexity levels. |
| 2502.08235 | 2025, Danger of Overthinking | 4,018 trajectories on SWE-Bench Verified. Three pathological patterns: Analysis Paralysis, Rogue Actions, Premature Disengagement. Mitigating overthinking: +30% performance, -43% cost. |
| 2509.13758 | 2025, Thinking Patterns in LRMs | Models follow human-like workflow on complex specs: multi-perspective analysis, clarify ambiguities, compare solutions, implement, review. Lighter patterns for simpler tasks. |
| 2604.02547 | 2026, Behavioral Drivers | 9,374 trajectories, 19 agents, 8 frameworks, 14 LLMs. LLM is primary driver of both outcome and behavior. Agents sharing same LLM agree far more than agents sharing same framework. Framework choice is second-order. |

### Benchmarks, Cost, and SDD

| arXiv | Authors / Year | Key finding to cite |
|-------|---------------|---------------------|
| 2511.14136 | CLEAR Framework | 6 leading agents, 300 enterprise tasks. Accuracy-optimal configurations cost 4.4–10.8x more than Pareto-efficient alternatives. |
| 2509.11079 | 2025, Difficulty-Aware Orchestration | +11.21% accuracy improvement at 64% of inference cost vs uniform strong-model routing. |
| 2505.05283 | Wang et al. 2025, SDLC Benchmarks Survey | 61% of LLM benchmarks measure only implementation phase. Requirements engineering: 5% coverage. Software design: 3% coverage. |
| 2509.16941 | 2025, SWE-Bench Pro | 74.4% resolved rate on SWE-bench → 11.0% on FeatureBench (complete real feature development). Gap reveals benchmark measures localized patches, not feature development. |
| 2601.03878 | SANER'26, SDD + TDD Registered Report | Spec-Driven TDD workflow. Human-in-the-loop refinement of test cases matters more than model choice for TDD workflows. |
| 2602.00180 | 2026, SDD Paper | Spec-Driven Development: CONSTITUTION.md → SPECIFICATION.md → IMPLEMENTATION_PLAN.md artifact chain. Human gate between spec and implementation. |
| 2505.09027 | 2025, Tests as Prompt TDD | 19 frontier models, 1,000 TDD tasks. Bottleneck is instruction following and in-context learning, not reasoning depth. Instruction loss in long prompts is primary failure mode. |
| 2512.12730 | 2025, NL2Repo-Bench | 104 long-horizon repo generation tasks. Models with standard context windows: 27.6% success even with frequent planning tool use. Context size determines planning effectiveness. |

### AGENTS.md, Code Review, and Skills

| arXiv | Authors / Year | Key finding to cite |
|-------|---------------|---------------------|
| 2601.20404 | Lulla et al. 2026, AGENTS.md Impact (JAWs) | Human-curated AGENTS.md: -28.64% runtime, -16.58% token usage. LLM-generated AGENTS.md: performs 3% WORSE than sessions with no file. Human curation is mandatory. |
| 2602.11988 | ETH Zurich 2026, Evaluating AGENTS.md | Confirms human curation requirement. Analyzes structural properties of effective AGENTS.md files. |
| 2603.15911 | 2026, Human-AI Code Review Synergy | 278,790 conversations, 300 projects. AI agents excel at systematic coverage and consistency. Humans excel at contextual and architectural judgment. Complementary, not substitutable. |
| 2601.00477 | 2026, Security PRs Study | 33,000+ agentic PRs on GitHub. Security-related agent PRs have lower merge rates and longer review latency due to heightened human scrutiny. |
| 2603.29919 | 2026, SkillReducer | Token cost analysis of agent skills. Quantifies lazy-loading benefits of SKILL.md description-first architecture. |

---

Use these for enterprise adoption statistics, market sizing, and strategic trends.
All claims from analyst reports must be cited by source name and publication date.

| Source | Report / Date | Key finding to cite |
|--------|--------------|---------------------|
| Gartner | Newsroom, August 2025 | 40% of enterprise applications will feature task-specific AI agents by 2026, up from less than 5% in 2025. |
| Gartner | Strategic Trends in Platform Engineering, 2025 | 80% of large software engineering organizations will establish dedicated platform teams by 2026. |
| Gartner | Top Strategic Tech Trends, October 2025 | Agentic AI and autonomous enterprise as top strategic priorities for 2026. |
| CNCF | Kubernetes AI Conformance Program, March 2026 | 66% of organizations run AI workloads on Kubernetes. CNCF nearly doubled certified Kubernetes AI platforms, +70% certifications. |
| CNCF | Autonomous Enterprise Four Pillars, January 2026 | Four pillars of platform control: Golden Paths (intent-to-infrastructure), Guardrails (AI-driven prevention), Safety Nets (autonomous recovery), Manual Review Workflows (automated compliance evidence). |
| CNCF | Autonomous Infrastructure, October 2025 | Timeline: 2025 (early adopters, 95% automated provisioning) → 2026 (standard for leading tech companies) → 2027 (manual management becomes competitive disadvantage) → 2028 (fully autonomous is enterprise standard). |
| Futurum Research | MCP Dev Summit 2026 | AAIF (Agentic AI Foundation) under Linux Foundation. Fastest-growing LF foundation in history. 170+ member organizations. MCP scope explicitly defined: agent-to-resource only. |
| PlatformEngineering.org | 10 Predictions 2026 | Nearly 90% of companies already have internal developer platforms (exceeded Gartner 2026 forecast one year early). |
| PlatformEngineering.org | State of Platform Engineering 2025 | DORA 2025 confirms platform engineering adoption acceleration. |
| The New Stack | AI Merging with Platform Engineering, January 2026 | "Platform engineering emerged as the essential framework for harnessing AI's potential without unleashing chaos." Spotify: 1,500+ AI agent PRs merged, 60–90% time savings on migrations. |
| Roadie.io | Platform Engineering in 2026: Why DIY Is Dead | Backstage: 89% market share among IDP adopters. 270+ public adopters (LinkedIn, CVS Health, Vodafone). 4th most contributed CNCF project in 2024. |
| SiliconANGLE | KubeCon EU 2026, Platform Engineering and AI | "Agents amplify what is good in your ecosystem and amplify what is bad." Platform engineering as primary AI governance layer. |
| BVP | AI Infrastructure Roadmap 2026 | Five frontiers for AI infrastructure investment in 2026. |

---

