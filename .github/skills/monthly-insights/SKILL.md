---
name: monthly-insights
description: "Create consolidated Monthly Insights reports for Microsoft field and GBB work. Use for monthly insights, monthly reports, account updates, field observations, workshop analysis, quarterly FY reports, Brazil and LATAM account dashboards, survey analysis, consolidated HTML reporting, or combining account data with workshop data into one executive report."
---

# Monthly Insights

Use this skill to create a consolidated Monthly Insights report that combines account updates, field observations, and optional workshop or survey data into one executive HTML deliverable under the `ms-identity` identity.

## First Step

Ask only for missing inputs:

- Reporting period, for example `Q3 FY26` or a month range.
- Account update source files or pasted notes.
- Workshop, survey, or event data when applicable.
- Target audience and language.
- Whether the user wants HTML only or derived PDF as well.

If the user provides files, inspect them before asking follow-up questions.

## Report Structure

Accounts come first, workshop data second.

1. **Header and navigation**: title, period, author, sticky nav.
2. **Introduction**: period, number of accounts, countries, verticals, and strategic focus.
3. **Account portfolio overview**: account, country, industry, segment, key themes, risk.
4. **Account updates**: one card per account with all source details preserved.
5. **Additional accounts**: compact grid for accounts without deep updates.
6. **Field observations**: critical, warning, info, and recommended-action callouts.
7. **Workshop or survey data**: KPI row, role distribution, utilization, misuse analysis, agent knowledge, and comparison tables when data exists.
8. **Focus and priorities**: FY timeline, top priorities, and competitive landscape.

## Design System

- Apply `ms-identity`: Microsoft 4-color palette, Inter or Segoe UI, JetBrains Mono for data, white background, concise editorial cards.
- Use the author identity `Frontier Cockpit Team, Software Global Black Belt` and Microsoft email only.
- Write `GitHub Copilot` in full.
- Use self-contained HTML by default. Prefer inline SVG charts or static SVG generated from data.
- Do not use external chart libraries unless the user explicitly asks for an interactive dashboard and accepts external dependencies.
- Keep no duplicate data points: each metric should appear once in the primary narrative and once in the source appendix only if needed.

## Account Data Rules

- Never summarize away source account details. Preserve the full signal, then organize it.
- Always include country, industry, segment, and risk level for every account.
- Risk level is evidence-based: High, Medium, or Low.
- Tag competitive threats and engagement types consistently.
- Do not invent account metrics, survey counts, or workshop findings.

## Workshop and Survey Rules

Include workshop sections only when data exists. For each workshop or survey, capture:

- Total audience and respondent count.
- Response rate and dominant profile.
- Effective utilization or equivalent primary signal.
- Role distribution and key observed misuse patterns.
- Agent knowledge or readiness metrics when available.

## Workflow

1. Inventory inputs and identify account, observation, and workshop data.
2. Normalize account metadata and risk tags.
3. Build the report using the structure above.
4. Add chart data from verified sources only.
5. Validate identity, copy rules, data coherence, and render quality.
6. Save outputs under the repository's document organization rules.

## Reference

- Read [references/template-structure.md](references/template-structure.md) for the full HTML component map.

## Validation

- Check every number against the provided source.
- Ensure all account details from source material are represented.
- Confirm no personal social handles or non-Microsoft identity strings are present.
- Confirm no en dashes or em dashes are present.
- Open the HTML and verify no console errors if JavaScript is used.
- If PDF is requested, render and visually inspect cover, tables, charts, and final page.

## Fiscal Year Reference

Microsoft's fiscal year runs July through June:

- Q1: July through September.
- Q2: October through December.
- Q3: January through March.
- Q4: April through June.

Example: `Q3 FY26` means January through March 2026.