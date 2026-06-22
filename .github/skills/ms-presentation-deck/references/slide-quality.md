# Slide Quality System

Use this reference after `patterns.md` and before writing the HTML. Its purpose is to prevent decks from becoming a sequence of similar cards, tables, and text blocks.

## Quality Bar

Every slide must have one clear job. Before writing markup, assign each slide:

- **Role**: hook, map, evidence, mechanism, comparison, demo, decision, recap, transition, close.
- **Pattern**: cover, agenda, divider, big number, split, stat pair, three cards, four-card spectrum, table, terminal, diagram, roadmap, closing.
- **Density**: low, medium, or high.
- **Anchor**: the one phrase, number, diagram, or interface detail the audience should remember.
- **Next move**: what the slide makes possible in the next slide.

A slide is not ready if its role is only "explain topic". It needs a sharper job.

## Rhythm Rules

1. Do not use the same layout twice in a row unless the two slides are an intentional pair.
2. Do not place more than two dense slides back to back. Follow high density with a divider, big number, stat pair, demo, or recap.
3. Every section needs a dark divider using the approved style: top-left Microsoft 4-square mark, `PART` or `PARTE`, large Roman numeral, title, and subtitle.
4. Every 4 to 6 slides should include one visual reset: big number, terminal mockup, diagram, screenshot-style simulation, or stat pair.
5. Prefer a diagram, simulation, or comparison over a card grid when the content is a flow, decision, or operating model.
6. Use cards for categories, not paragraphs. If a card has more than 35 words, change the pattern.
7. Use titles as conclusions, not labels. Prefer "The bill moved from intent to work" over "Billing model".
8. Speaker notes must carry the full narrative. Slide text should be sparse enough to scan from the back of the room.

## Section Arc

Each section should follow a small story arc:

1. **Divider**: creates expectation and names the tension.
2. **Hook**: a strong claim, date, number, or contrast.
3. **Evidence**: table, source-backed facts, metric cards, or an example.
4. **Mechanism**: diagram, terminal, flow, architecture, or step-by-step view.
5. **Decision**: what the audience should do differently.
6. **Recap or bridge**: one slide that prepares the next section.

Short sections may combine steps, but must still have hook, evidence, and decision.

## Content To Pattern Map

| Content type | Preferred pattern | Avoid |
| --- | --- | --- |
| Single important date or number | Big number | Three cards |
| Before and after | Split comparison | Bullet list |
| Decision criteria | Matrix, decision tree, or two-column tradeoff | Paragraph cards |
| Process or lifecycle | Sequence diagram, roadmap, or terminal trace | Static list |
| Architecture or stack | Layer diagram or layer pyramid | Dense table first |
| Cost or usage mix | Donut plus classes, stat cards, or table | Decorative chart without labels |
| Code or command workflow | Terminal mockup or VS Code simulation | Plain paragraph |
| Product surface or UX | Browser, VS Code, or GitHub Copilot simulation | Abstract cards |
| Risk, gap, or contrast | Stat pair or red/green split | Neutral cards |
| Section opening | Dark divider | Light chapter cover |
| Closing | Dark closing with contact and next step | Thank-you-only slide |

## Use The Showcase

Before building the deck, open `assets/showcase.html` and choose the visual vocabulary deliberately. Treat it as a menu, not decoration.

Minimum selection for a normal 15 to 25 slide deck:

- 1 cover.
- 1 agenda.
- 3 to 6 section dividers.
- 2 evidence slides using tables, stats, or sourced metric cards.
- 2 mechanism slides using diagrams, terminal, or UI simulations.
- 1 decision or roadmap slide.
- 1 closing slide.

For a long workshop deck, add more section dividers and more visual resets. Do not simply repeat card grids.

## Slide Plan Template

Create this plan before writing HTML:

```text
Slide | Role | Pattern | Density | Anchor | Why this pattern
01    | hook | cover | low | <main promise> | cover sets identity and topic
02    | map | agenda | medium | <section map> | gives audience navigation
03    | transition | divider | low | I | opens the first act
04    | evidence | big number | low | <number/date> | creates a memorable fact
05    | mechanism | diagram | medium | <flow> | shows how it works
```

If more than two adjacent rows have the same pattern, revise the plan.

## Copy Rules For Quality

- Put the claim in the title.
- Keep body copy to 1 or 2 short sentences on normal slides.
- Use the notes for nuance, caveats, and transitions.
- Do not add a visible instruction telling the audience how to read the slide.
- Avoid generic labels such as "Overview", "Benefits", "Architecture" unless the subtitle carries the real claim.
- Never invent metrics. If the slide needs a number, cite it in the notes or in the visible source line.

## Pre-Delivery Quality Gate

Before delivering the HTML, verify:

1. No repeated layout appears three times in a row.
2. Every section has a dark divider in the approved Roman-numeral style.
3. The deck includes at least one evidence slide and one mechanism slide.
4. Speaker notes exist for every slide and every required locale.
5. Every slide has one memorable anchor.
6. The final deck passes `scripts/audit.py` with zero errors and, for normal multilingual decks, zero warnings.
