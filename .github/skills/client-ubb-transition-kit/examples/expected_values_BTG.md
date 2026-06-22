# Golden values, BTG Pactual master (validation contract)

Run the generators with the BTG example inputs (examples/client_monthly_BTG.csv,
examples/client_models_BTG.csv, CLIENT dict defaults) and the outputs MUST
reproduce these values. Any divergence means the structure broke; fix before
generating for a new client.

## XLSX (after recalculation, data_only read)

| Cell | Meaning | Expected |
|---|---|---|
| Engine!C13 | License cost / month | 127,249 |
| Engine!C14 | Standard pool | 127,249 |
| Engine!C15 | Promo pool | 221,450 |
| Engine!C16 | Standard overage | 104,455 |
| Engine!C17 | Promo overage | 10,254 |
| Engine!C18 | Consumption/included ratio | 1.82x |
| Engine!C23 | Scenario Today | 130,948 |
| Engine!C24 | Scenario No action | 231,704 |
| Engine!C25 | Scenario With promo | 137,503 (official report: 137,624; gap is seat-split rounding, documented in Sources) |
| Engine!C26 | September jump | 94,201 |
| Simulator!C18 | Combined reduction (lean defaults) | 0.305 |
| Simulator!C19 | Mature overage | 33,896 |
| Forecast FY27!E12 | September with-program overage | 93,871 |
| Forecast FY27!F22 | FY27 program savings | 494,617 |
| ROI!C12 to C15 | Ladder A/B/C/D | 2,592,046 / 2,432,287 / 2,379,034 / 1,983,341 |
| ROI!C20 | Scenario D total savings | 608,705 |
| Model Mix total | Token cost sum | 231,703 (rounding of 231,704) |
| Model Mix cache-read share | All-token denominator | 0.835 |

## PDF (text scan)

- 12 pages; contains: 130.948, 137.624, 231.704, 94 mil, 495 mil, 83,5%
- Zero hits for: em dash, en dash, "Deal Desk", ASCII Portuguese (acao, promocao, cenario, credito, grafico, licencas)
- Cover top reads "Confidencial" and the client name, never "Internal"

## Cross-document coherence

Today / No action / Promo / Jump / FY savings must match between the XLSX,
the PDF, the internal HTML and db.json (BTG tpid 5336866).

## Deck (HTML, after rebuild from BTG content modules)

- 15 slides; i18n complete in pt-BR, en, es (no element left as "." or undefined)
- 15/15 speaker notes per locale (I18N[locale].notes.s1..s15)
- Zero em dashes; logo aria-label="frontier-cockpit" and favicon present
- Cover keyword: partnership "até dezembro"; closing title carries the three anchors (kickoff June, checkpoint September, partnership December)
- Slide 4 hero: +US$ 94k; slide 9 hero: US$ 495k; scenario strip 130.948 / 137.624 / 231.704
- Slide 13 commercial track: open options wording ("nada definido ainda"), never a determined path, never internal desk names
- Lever slides carry the official bands: R1 40-70% output, R2 40-70% bill, R4 40-80% input, R5 30-50% input, R6 compound, R3 BYOK, R7 budgets
