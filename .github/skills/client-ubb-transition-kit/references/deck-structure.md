# Executive deck, structure spec (deliverable 4 of 4)

15 slides, trilingual PT-BR/EN/ES, speaker notes panel (N) and presenter view
(F), ms-presentation-deck v2 engine with the rounded `</.>` personal logo on
every slide header. The HTML multi file with notes is the deliverable and the
source of truth; public HTML, PDF and PPTX are derivatives generated only when
asked.

## The 15-slide map (4-part narrative)

| # | Pattern | Content |
|---|---------|---------|
| 1 | Cover | "O programa de seis meses." + "Eficiência, governança e parceria até dezembro." Meta: Autora / Função / Cliente / Data |
| 2 | Agenda | 4 parts: o momento / o trabalho até aqui / o programa de seis meses / duas trilhas em paralelo |
| 3 | Divider 01 (dark, red) | O momento |
| 4 | Big number + 3-strip | The September jump hero (moment.hero) + today / with promo / no action |
| 5 | Divider 02 (dark, blue) | O trabalho até aqui |
| 6 | 3-card | Deliverables: audited analysis / dynamic transition kit / executive proposal |
| 7 | Divider 03 (dark, green) | O programa de seis meses |
| 8 | Roadmap 3 phases | Months 1-2 foundation, month 3 September checkpoint (the lock), months 4-6 maturation |
| 9 | Big number | FY redemption hero (redeem.hero), conservative band, no discount required |
| 10 | 4-row levers | Highest impact: R1 (40-70% of output), R2 (40-70% of bill), R4 (40-80% of input), R5 (30-50% of input), with mechanisms |
| 11 | 3-row levers | Structural: R6 compound gain, R3 local models BYOK zero-credit routine, R7 budgets guardrail (ULB GA 2026-06-01) |
| 12 | Divider 04 (dark, yellow) | Duas trilhas em paralelo |
| 13 | 2-col | Commercial track (OPEN options) vs strategic GBB track (biweekly Jun-Dec) |
| 14 | 3-card | Who does what: client / Microsoft (GBB + account) / GitHub |
| 15 | Closing (dark) | "Kickoff em junho. Checkpoint em setembro. Parceria até dezembro." + contact |

## Non-negotiable narrative rules

1. **Six-month partnership, June to December.** September is the mid-program
   checkpoint where the promo expires and the real overage appears. It is the
   lock, never the end. The closing slide carries all three anchors.
2. **The commercial track is an OPEN set of options, never determined.**
   Always present as: extend the promotional credit, or an additional discount
   for the remaining months to soften the overage step, and, if it fits the
   client, a Pre-Purchase Plan or ACD-based terms. Phrase: "nada definido
   ainda, o caminho certo sai da conversa, com os números na mesa". The s12/s13
   notes open with "aqui nada está definido, isto é o início da abordagem".
   Never name internal desks ("Deal Desk" forbidden); say "condições acima da
   tabela, sujeitas a elegibilidade e aprovação".
3. **Levers always carry the official runbook band with source**, never a
   promise: R1 output 40-70% (output ~4-5x input; 400-600 → 30-50 tokens
   diff-restricted), R2 routing 40-70% (two orders of magnitude; Auto +10%
   chat), R4 context 40-80% of input (LLMLingua up to 20x), R5 cache 30-50% of
   input (cache read 0.1x Anthropic / 50% OpenAI; client cache-read share from
   the kit), R6 compound, R3 BYOK zero AI Credits (not completions, single
   digit to ~15%), R7 four budget levels, alert at 80%.
4. **Client numbers come from the kit golden contract**: the three scenarios,
   the September jump, the FY redemption, the top-2 model concentration, the
   cache-read share. The deck must reconcile with the XLSX, the PDF and db.json.
5. Hero numbers are i18n keys (`moment.hero`, `redeem.hero`), abbreviated as
   "+US$ 94k" style for the 150px stat.

## Build and validation

- Engine donor: any previous ms-identity multi.html (default
  `golden_deck_multi.html`, copy from examples/). The builder transplants 15
  new sections + the I18N object onto its chrome and JS.
- Notes: s1..s15 per locale inside `I18N[locale].notes`, structure
  [ABERTURA]/[NÚCLEO]/[GANCHO PROVOCATIVO]/[TRANSIÇÃO]/[TIMING], ~1,600-1,800
  words per locale. They are the words to be spoken, not bullets.
- Validate with Playwright using `reduced_motion='no-preference'` (the default
  'reduce' makes stagger slides capture blank) and wait ~1.3 s after
  goToSlide before screenshots.
- Identity audit: zero em dashes, `Software Global Black Belt`,
  `frontier-cockpit@example.com`, `GitHub Copilot` in full, `</.>` logo
  (aria-label="frontier-cockpit") and favicon present, forbidden strings absent.
- Full PT-BR/ES accents in client copy. Never bulk ASCII→accent replace.

## Known pitfalls

- The I18N resolver follows dot paths, max 2 levels, camelCase last. Never
  create `a.b.c` leaf keys.
- Slide total is computed from the DOM (`slides.length`); adding a slide only
  requires a matching `notes.sN` in each locale.
- When renumbering notes, never regex-shift keys across the three locale dicts
  in one pass; rebuild the dicts programmatically (s1..sN ordered) instead.
