# Speaker notes structure

The speaker notes for Paula's decks are not bullet-point reminders. They are **the actual words she will say**, structured for delivery, in three languages.

## Why this matters

The notes get rendered in three places:

1. **Inline notes panel** in the presenter deck (toggled with N), at the bottom of each slide. Markdown lite is rendered as styled HTML (bold yellow, italic blue, markers as green badges, pause markers in red).
2. **Presenter window** (toggled with F or P) on a second screen, full-size, dark theme. Same formatting.
3. **PPTX speaker notes** (plain text, the formatting stripped). Paula sees these in PowerPoint's notes panel during a presentation.

Because Paula reads these aloud, they need to be **complete sentences in her speaking voice**, not bullets like "talk about the 100x gap".

## Structure (every note follows this)

```
**[ABERTURA]** (or [OPENING] or [APERTURA] depending on locale)
First spoken sentence. Sets the room. Often a question to the audience or a callback to the previous slide.

**[NÚCLEO]** (or [CORE] or [NÚCLEO])
The substantive content. 2-4 paragraphs. This is the bulk of what she says. Specific numbers, named examples, concrete situations. Pauses marked with [pausa] or [pause].

**[GANCHO PROVOCATIVO]** (or [PROVOCATIVE HOOK] or [GANCHO PROVOCATIVO])
One sharp observation that reframes the content. Sometimes a question, sometimes a claim. The "thing they'll remember" if they remember only one moment.

**[TRANSIÇÃO, para slide N, <topic>]** (or [TRANSITION, to slide N, <topic>])
One sentence handing off to the next slide. Names the next idea.

**[TIMING]** ~N min
```

Note the markers use commas inside the brackets (NOT em dashes — em dashes are forbidden in this deck). So `[TRANSIÇÃO, para slide 6]`, not `[TRANSIÇÃO — para slide 6]`.

## Word count target

- Content slides: **180-220 words per note** (60-90 seconds of speech).
- Section dividers (slides 3, 6, 10, 14, 17): **70-100 words** (30 seconds, just to set up the section).
- Cover and closing (slides 1, 20): **200-230 words** (more presence at opening and closing).

Across the whole deck (20 slides), aim for **3500-4000 words per locale**.

## Markdown lite

Three patterns are recognized and styled:

- `**bold**` — rendered as yellow (Microsoft yellow #FFB900). Use for the **key term** of a paragraph, the thing she wants to emphasize when speaking.
- `*italic*` — rendered as blue (Microsoft blue #00A4EF). Use for terms or concepts she's introducing or contrasting.
- `[ALL CAPS]` — rendered as a green badge. Used for the section markers above.
- `[pause]` or `[pausa]` — rendered as a red mono inline. The literal word "pause" / "pausa" — she sees this and knows to actually pause.

DON'T use any other markdown (no `~~strike~~`, no `# heading`, no links). The renderer doesn't handle them.

## Voice and tone

Paula's notes should sound like:

- An **authoritative consultant** who has seen this at multiple enterprise clients ("Rodei Preview Your Usage em quatro clientes nos últimos dois meses. Sem exceção, a liderança ficou surpresa...").
- **Didactic** — defines jargon before using it ("Um token não é uma palavra. É um fragmento de palavra.").
- **Provocative in a productive way** — challenges the room ("Quem no seu time está tomando uma decisão de budget toda vez que escolhe um modelo, sem saber?").
- **Vivid** — uses specific numbers, named examples, situations ("Uma sessão real, oitenta e sete turnos, quatro horas, refatorando cinquenta arquivos, custo de cento e vinte e quatro dólares.").
- **Casual but professional** — uses contractions, second person ("vocês"), some humor, but never slang or filler.
- **No corporate jargon** — avoid "synergize", "actionable", "leverage", "best in class". Say what they mean.

## What NOT to do

- Don't write bullets: "- Explain the 100x gap / - Reference the chart". Write the sentences.
- Don't write meta-instructions: "Now pivot to the agent design discussion". Just write the transition sentence.
- Don't repeat slide content verbatim. The slide is the visual; the notes are what fills in around it.
- Don't write generic statements ("This is important because..."). Say WHY specifically.
- Don't use em dashes. Use commas or periods.

## Three-locale parity

Every note exists in three locales (`en`, `pt-BR`, `es`) with parallel structure. The markers translate:

| EN              | PT-BR                  | ES                   |
|-----------------|------------------------|----------------------|
| [OPENING]       | [ABERTURA]             | [APERTURA]           |
| [CORE]          | [NÚCLEO]               | [NÚCLEO]             |
| [PROVOCATIVE HOOK] | [GANCHO PROVOCATIVO] | [GANCHO PROVOCATIVO] |
| [TRANSITION, to slide N] | [TRANSIÇÃO, para slide N] | [TRANSICIÓN, para slide N] |
| [pause]         | [pausa]                | [pausa]              |
| [TIMING]        | [TIMING]               | [TIMING]             |

The notes are NOT machine translations of each other. Each locale is written natively — same arguments, same vivid examples, but phrased the way someone speaking that language would actually say it. Portuguese tends to use "vocês" (plural you), Spanish "ustedes", English "you all" or just "you".

## Format in the I18N JSON

Speaker notes go under `notes` in each locale:

```json
{
  "pt-BR": {
    "cover": { ... },
    "agenda": { ... },
    "notes": {
      "s1": "**[ABERTURA]**\nBom dia. Antes de começar, uma pergunta...\n\n**[NÚCLEO]**\n...\n\n**[GANCHO PROVOCATIVO]**\n...\n\n**[TRANSIÇÃO, para slide 2, agenda]**\n...\n\n**[TIMING]** ~2 min",
      "s2": "...",
      "s3": "...",
      ...
      "s20": "..."
    }
  }
}
```

The keys are `s1` through `s20` (or however many slides). Use this convention consistently.

## Writing a new set of notes

When the deck is new (no existing notes), write them in this order:

1. **Pick the strongest slide** (usually the big-number slide or the most-controversial claim). Write its notes first, fully, in one locale. This sets the voice.
2. **Pair-test the voice with the user.** Show one note in one locale. Get feedback on tone, length, vivid examples, pace. Iterate.
3. **Write the cover and closing notes** next. These bracket the entire experience.
4. **Write the dividers** (slides 3, 6, 10, 14, 17). Short, setup-only.
5. **Write the rest in order**, ensuring each note's transition matches the opening of the next note.
6. **Audit the timing**: sum all `[TIMING]` estimates and check it lands in the target window (e.g., 60-90 min for a long briefing, 25-35 min for a short one).
7. **Translate to the other two locales** by re-writing (not by Google Translate). Use the same examples and pacing.
8. **Run the em dash audit** before delivering. Count of `—` should be 0 in the notes JSON.

## Inserting notes into the HTML deck

After writing all 60 notes (20 slides × 3 locales), merge them into the I18N JSON inside the multi.html:

```python
# Extract the existing I18N block, replace just the notes section, write back
content = open('deck.html').read()
i18n_start = content.find('const I18N = {')
# parse JSON, set i18n['en']['notes'] = ..., i18n['pt-BR']['notes'] = ..., i18n['es']['notes'] = ...
# serialize and write back
```

The `make_pptx.js` script reads from a single locale's notes (via the data JSON it's given) and embeds them as plain text in `slide.addNotes()`. The markdown markers stay visible in the PPTX (no rendering), so the apresentadora still sees `[ABERTURA]`, `[NÚCLEO]`, etc. as text in the PowerPoint notes panel.

## Example: a well-formed note

```
**[ABERTURA, vindo do slide 4]**
Esqueçam a data. Fiquem com uma palavra: **custo**. O que muda em primeiro de junho não é preço. É a *definição* daquilo pelo que vocês pagam. Esse é o slide mais importante da manhã.

**[NÚCLEO]**
Lado esquerdo. Premium Request Units. Uma pergunta de chat contava como uma request. Uma sessão agêntica de quatro horas refatorando cinquenta arquivos contava como uma request, com multiplicador, mas a mesma unidade. [pausa] Era ficção útil, porque deixava budgets previsíveis. O custo: ninguém na engenharia sabia o que de fato estava consumindo.

Lado direito. AI Credits. A unidade mudou de intenção para trabalho. Input, output, cached, cada um na taxa da API do modelo. Um credit, um centavo.

O que está escondido: isso é uma **mudança de visibilidade gerencial**. Pela primeira vez, o líder de engenharia de vocês vê, na linha, quais tipos de trabalho são caros. Rodei Preview Your Usage em quatro clientes enterprise nos últimos dois meses. Sem exceção, a liderança ficou surpresa pelo lugar onde o custo de fato estava.

**[GANCHO PROVOCATIVO]**
Levem isso: *quem no seu time está tomando uma decisão de budget toda vez que escolhe um modelo, sem saber?* Todo dev é, silenciosamente, um comprador.

**[TRANSIÇÃO, para Parte II]**
Para responder, precisamos de linguagem compartilhada. O que é um token, onde o custo mora, o que é context engineering. Parte II.

**[TIMING]** ~2 min
```

**Word count**: 194. Has all 5 sections. Specific (Premium Request Units, AI Credits, quatro clientes). Vivid (a sessão agêntica de quatro horas, cinquenta arquivos). Provocative (every dev is silently a buyer). Transition names the next part. No em dashes.
