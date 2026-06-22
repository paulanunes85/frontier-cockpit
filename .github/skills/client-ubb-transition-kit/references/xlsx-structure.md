# XLSX Transition Kit, 18-tab structure (BTG v11 master)

Language: ENGLISH. Font: Segoe UI. Conventions: yellow fill = editable input, blue font = hardcoded input, black = formula.

## Tabs in order

1. **Cover**: 4-color bar, title, client + TPID + plan, author block, companion-document list, workbook map (INPUT / ENGINE / BUSINESS CASE / EXECUTION / GOVERNANCE blocks).
2. **How to Use**: 5-step flow + color conventions.
3. **Dashboard**: 6 KPI cards row 1 (today, no action, with promo, September jump, mature saving/yr, FY program savings); 6 ops cards row 2 (consumption/included ratio, pool coverage, top family share, top-2 share, actions done x/y via COUNTIF, blocked items). 4 native charts: scenarios bar (Engine C23:C25), FY27 overage line (Forecast cols D,E with headers row 7), model mix top-8 horizontal bar, FY26 ACR line.
4. **Client Intake**: the ONLY input tab. Fields: client, TPID, plan (dropdown Business/Enterprise), CB seats, CE seats, price per credit, monthly token consumption, current PRU overage, promo months covered, ACD band, Azure sub, growth, cost centers.
5. **Engine**: plan table (Business 1900/3000/19; Enterprise 3900/7000/39); derived: license cost, std pool, promo pool, std overage, promo overage, ratio, coverage; three scenarios with monthly/annual/delta columns; September jump; annual exposure.
6. **Consumption FY26**: monthly actuals pasted from db.json uso_mensal (blue font), MoM % and index formulas, computed signals block.
7. **Model Mix**: rows from db.json modelos_tokens for the client (blue font), share formula per row, cache-read share = H/(F+G+H+J) including cache creation column J, totals via SUMPRODUCT, family share via SUMIF wildcard, top-2 share via LARGE.
8. **Simulator**: 7 levers R1-R7, editable reductions; combined = explicit product `=1-(1-C8)*(1-C9)*(1-C10)*(1-C11)*(1-C12)*(1-C13)*(1-C14)` (NEVER `1-PRODUCT(1-range)`, that is an array formula and returns #VALUE!); mature overage `=MAX(0, consumption*(1-combined) - std_pool)`; run-rate saving; link to Forecast FY savings.
9. **Forecast FY27**: 12 months, editable ramp column; no-action overage `=IF(month_index<promo_months, promo_overage, std_overage)`; with-program `=MAX(0, consumption*(1-ramp*combined) - applicable_pool)` with the same promo/std pool switch; saving, cumulative, scenario cost columns; totals row.
10. **ROI Scenarios**: editable P3 published % and above-table %; ladder A (no action) / B (promo + published) / C (promo + above-table) / D (above-table + program); decomposition of D into discount component (on optimized overage) + redemption component.
11. **Action Plan R1-R7**: 10 actions with ID, lever, action, owner, due, effort, impact, status dropdown, notes; traffic-light conditional formatting.
12. **90-Day Plan**: 12 weeks, phase / KPI / action / target / status dropdown.
13. **Monthly Checkpoints**: 6 months, September row highlighted as the lock.
14. **KPI Tracker**: targets + 8 weekly actual columns (yellow), Latest via `=IFERROR(LOOKUP(2,1/(E:L<>""),E:L),"")`, variance with ColorScale.
15. **Governance**: caps per user and cost center from the engine, alert margin input, 3-layer metrics model.
16. **Maturity**: 5 dimensions 1-5 (yellow), total, stage IF formula with conditional colors.
17. **Glossary**: UBB, credit, pools, overage, pooling, PRU, P3, ACD, R1-R7, ramp, cache read, frontier.
18. **Sources**: origin of every number, engine-vs-report reconciliation note, editable assumptions list.

## Engine physics (the part people get wrong)

- Reducing consumption reduces overage dollar-for-dollar while consumption > pool. Never model program impact as a scalar on overage.
- Lever composition is multiplicative. Additive lever sums above 100% are a known historical bug; never reproduce it.
- Promo months use the promo pool in BOTH the no-action and with-program columns.

## Known pitfalls

- openpyxl chart series: take titles from the header row (titles_from_data=True with min_row at the header).
- Always run scripts/recalc.py (copy the office/ helper dir too) until zero errors. If LibreOffice wedges, kill soffice and retry with a fresh -env:UserInstallation profile; never deliver unverified formulas silently.
- Strip U+2013/U+2014 from all strings post-build, then recalc again if strings changed.
