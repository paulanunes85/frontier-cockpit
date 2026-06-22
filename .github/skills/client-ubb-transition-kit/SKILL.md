---
name: client-ubb-transition-kit
description: "Generate a complete client GitHub Copilot Usage-Based Billing package under client-ubb-transition-kits/: internal budget analysis HTML, internal XLSX transition kit, customer executive deck, customer proposal PDF, generic customer PDFs, and a per-client db.json snapshot. Use for UBB transition kits, audited client billing data, FY usage, model mix, transition scenarios, or six-month GitHub Copilot UBB action plans."
---

# Client UBB Transition Kit

Use this skill to produce the standard client folder package for a GitHub Copilot Usage-Based Billing engagement. Every generated package lives under `client-ubb-transition-kits/<ClientSlug>_<TPID>/` at the repository root. The validated BTG assets in `examples/` and the current reference package under `REFERENCES_gh-ubb-customers-kit/` are structural references, formula references, and visual QA references, not a source for new client numbers.

## Deliverables

Generate the full folder package every time:

1. **Internal budget analysis HTML**, trilingual PT-BR, EN, ES, account-team source of truth, placed under `INTERNAL_Budget_Impact_Analysis/`.
2. **Internal XLSX Transition Kit**, English workbook with simulator, charts, dashboard, and sources, placed under `INTERNAL_Transition_Kit/`.
3. **Customer executive deck**, trilingual HTML slides with speaker notes and presenter view, placed under `EXTERNAL_Customer_Ready_Documents/customer-deck/`.
4. **Customer executive action-proposal PDF**, client-language editorial document, PT-BR default for Brazil, placed under `EXTERNAL_Customer_Ready_Documents/customer-ready-playbooks/`.
5. **Generic customer-ready PDFs**, copied unchanged from the reference package into `EXTERNAL_Customer_Ready_Documents/customer-ready-playbooks/` for every client.
6. **Per-client `db.json` snapshot**, generated from the canonical source `db.json` and placed in the client package root.

The client-facing mini-site is outside the standard package. Generate it only when explicitly requested.

## Package Root

The repository root directory for generated packages is:

```text
client-ubb-transition-kits/
```

Each client package folder name is deterministic:

```text
client-ubb-transition-kits/<ClientSlug>_<TPID>/
```

`<ClientSlug>` is the audited `top_parent` from `db.json`, normalized for the file system. The package keeps the original audited client name inside its root `db.json` snapshot.

Before generating or validating a package, read [references/package-structure.md](references/package-structure.md).

## First Step

Ask only for missing audited inputs. If files or `db.json` are present, read them before asking.

Required inputs:

- Canonical source `db.json`, normally `REFERENCES_gh-ubb-customers-kit/db.json` unless the user provides a newer audited file.
- Client TPID or exact client name from `db.json`.
- Promo window months for the forecast year when not already captured in the engagement brief.
- ACD band, Azure subscription availability, cost centers, and named owners when they are not in `db.json`.
- Any client-approved language preference for the customer PDF.

Never ask the user to retype values that already exist in `db.json`. Derive client name, TPID, seats, current spend, standard scenario, promo scenario, model mix, monthly usage, billable-owner rows, and growth signal from the audited source.

## Data Integrity

- Never invent client financial, billing, usage, seat, or ROI numbers.
- The same audited values must reconcile across internal HTML, XLSX, customer PDF, customer deck, package `db.json`, and source `db.json`.
- If official report values and engine values differ by rounding, document the reconciliation in the XLSX Sources tab and PDF appendix.
- Use the BTG examples only as a structural and validation reference.
- If a client lacks required rows in `db.json`, block the package and report the missing section. Do not backfill from another client and do not estimate.

## Workflow

### 0. Prepare and validate the package folder

Use `assets/package_customer_kit.py` to create the deterministic folder, write the per-client `db.json` snapshot, and copy the generic PDFs:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py init-client \
  --db REFERENCES_gh-ubb-customers-kit/db.json \
  --reference-root REFERENCES_gh-ubb-customers-kit \
  --tpid <TPID>
```

To initialize every client that already has the required source sections in `db.json`, use:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py init-all-clients \
  --db REFERENCES_gh-ubb-customers-kit/db.json \
  --reference-root REFERENCES_gh-ubb-customers-kit \
  --output-root client-ubb-transition-kits
```

The all-client initializer skips clients with missing audited source data and reports them as source gaps. It does not generate incomplete packages unless `--allow-source-gaps` is explicitly used for diagnostics.

To recreate packages from the audited existing materials in `00-Customers_Transition_Plan`, use:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py import-transition-plan \
  --db REFERENCES_gh-ubb-customers-kit/db.json \
  --reference-root REFERENCES_gh-ubb-customers-kit \
  --source REFERENCES_gh-ubb-customers-kit/00-Customers_Transition_Plan \
  --output-root client-ubb-transition-kits
```

The import copies the four audited custom materials for each transition-plan client, generates a fresh per-client `db.json`, copies the generic PDFs, and writes `package-manifest.json` with SHA-256 checksums. It copies files, never moves them, so the reference folder stays intact.

Run the source-data check before generating deliverables:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py validate-db \
  --db REFERENCES_gh-ubb-customers-kit/db.json
```

If the command reports a missing source section for a client, that client is not generation-ready.

### 1. XLSX Transition Kit

Use `assets/build_kit_template.py` with `client_monthly.csv` and `client_models.csv` beside it. The BTG CSV files in `examples/` define the column contract.

Run recalculation until there are zero formula errors and zero uncalculated cells:

```bash
python3 assets/recalc_portable.py <workbook.xlsx>
```

Read [references/xlsx-structure.md](references/xlsx-structure.md) before changing workbook structure.

Place the final workbook in:

```text
client-ubb-transition-kits/<ClientSlug>_<TPID>/INTERNAL_Transition_Kit/
```

Non-negotiables:

- `Client Intake` is the single input source.
- Simulator combines R1 to R7 multiplicatively with an explicit product formula.
- Forecast uses promo pool during promo months, standard pool after.
- Dashboard includes native openpyxl charts and live status cards.
- Inputs use yellow fill, hardcodes use blue font, formulas use black font.

### 2. Executive Proposal PDF

Use `assets/build_proposal_template.py` and the bundled editorial components. Read [references/pdf-structure.md](references/pdf-structure.md) before changing chapter flow.

Place the final PDF in:

```text
client-ubb-transition-kits/<ClientSlug>_<TPID>/EXTERNAL_Customer_Ready_Documents/customer-ready-playbooks/
```

Non-negotiables:

- Client-facing copy avoids internal jargon.
- PT-BR copy keeps full Portuguese accents.
- Zero en dashes and zero em dashes.
- Cover top says `Confidencial · {Client}`.
- Commercial conditions are positioned as options subject to eligibility and approval.

### 3. Internal Analysis HTML

Use the BTG internal HTML as the structure master. Preserve trilingual behavior, the `ms-identity` identity, localStorage language handling, and the 26-section internal analysis spine.

Place the final internal HTML in:

```text
client-ubb-transition-kits/<ClientSlug>_<TPID>/INTERNAL_Budget_Impact_Analysis/
```

Validate with browser rendering when available.

### 4. Executive Deck

Use the deck generator and BTG golden deck as the engine donor. Read [references/deck-structure.md](references/deck-structure.md) before changing the narrative.

Place the final customer deck in:

```text
client-ubb-transition-kits/<ClientSlug>_<TPID>/EXTERNAL_Customer_Ready_Documents/customer-deck/
```

Non-negotiables:

- 15 slides.
- Trilingual copy and speaker notes in PT-BR, EN, ES.
- Six-month partnership story through December.
- September is the mid-program checkpoint.
- Commercial track stays an open set of options, never a decided concession.

### 5. Final package validation

Validate the completed client package:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py validate-package \
  --db REFERENCES_gh-ubb-customers-kit/db.json \
  --reference-root REFERENCES_gh-ubb-customers-kit \
  --package client-ubb-transition-kits/<ClientSlug>_<TPID>
```

This validation checks the folder tree, per-client `db.json` snapshot, generic PDFs, custom deliverables, latest-version rule, `package-manifest.json` checksums, and reconciliation with source `db.json`.

### 6. Deck PDF and PPTX derivatives

When the user explicitly asks for PDF or PowerPoint versions of the six-month customer decks, use `assets/package_customer_kit.py` to call the `ms-presentation-deck` derivative scripts for every package:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py generate-deck-derivatives \
  --output-root client-ubb-transition-kits
```

This produces one PT-BR PDF and three native editable PPTX files (`pt-BR`, `en`, `es`) for each customer deck. The files are copied into each client package under `EXTERNAL_Customer_Ready_Documents/customer-deck/pdf/` and `EXTERNAL_Customer_Ready_Documents/customer-deck/pptx/`, and the package manifest is updated with checksums.

Run `validate-packages` again after derivative generation.

### 7. Visual QA for deck derivatives

After generating deck derivatives, create visual QA contact sheets and machine-readable reports:

```bash
python3 .github/skills/client-ubb-transition-kit/assets/package_customer_kit.py visual-qa-deck-derivatives \
  --output-root client-ubb-transition-kits
```

This renders each deck PDF into page images, checks page count, text extraction, blank pages, and creates a PDF contact sheet. It also inspects every PPTX for slide count, editable text, speaker notes, and full-slide screenshot flattening, then creates a structural contact sheet. If LibreOffice is not available, PPTX visual rendering is reported as unavailable and the PPTX QA remains structural.

## Required Audits

- Identity: Frontier Cockpit Team, Software Global Black Belt, `frontier-cockpit@example.com`, Microsoft 4-color palette, Inter plus JetBrains Mono for web/PDF, Segoe UI for XLSX.
- Forbidden strings: personal usernames, personal social handles, LinkedIn URLs, non-Microsoft identity labels, and non-identity fonts such as Fraunces.
- Zero en dashes and zero em dashes.
- XLSX recalculation passes with zero formula and uncalculated-cell errors.
- PDF raster review covers cover, charts, appendix, and close page.
- Cross-document scenario, September curve, FY savings, and model-mix numbers match.
- The completed package passes `assets/package_customer_kit.py validate-package`.

## First-Run Self-Validation

Before producing a new client kit, run the generators with the BTG example inputs and compare against [examples/expected_values_BTG.md](examples/expected_values_BTG.md). Any divergence on BTG inputs means the structure or engine broke.

## References

| File | Use when |
| --- | --- |
| [references/package-structure.md](references/package-structure.md) | Root output directory, client folder tree, generic PDFs, latest-version rules, and package validation. |
| [references/xlsx-structure.md](references/xlsx-structure.md) | Workbook structure, formulas, and known pitfalls. |
| [references/pdf-structure.md](references/pdf-structure.md) | Executive proposal chapter map and language rules. |
| [references/deck-structure.md](references/deck-structure.md) | Executive deck narrative, slide map, and validation rules. |
| [examples/expected_values_BTG.md](examples/expected_values_BTG.md) | Golden numeric contract. |

## Scripts and Assets

- `assets/build_kit_template.py`, parametrized XLSX generator.
- `assets/build_proposal_template.py`, parametrized PDF generator.
- `assets/package_customer_kit.py`, deterministic package initializer, transition-plan importer, deck derivative generator, visual QA reporter, manifest writer, and validator.
- `assets/recalc_portable.py`, LibreOffice recalculation and strict scan.
- `examples/client_monthly_BTG.csv` and `examples/client_models_BTG.csv`, input-contract examples.
- `examples/golden_*`, validated visual and numeric reference outputs.