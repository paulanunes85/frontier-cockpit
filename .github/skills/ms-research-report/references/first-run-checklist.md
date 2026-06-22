# First-run checklist

Use this gate before rendering or delivering any ms-research-report output. The canonical source is Markdown. If this checklist or `validate_report.py` fails, fix the Markdown first, then render derivative formats again.

## Intake contract

- [ ] Deliverable type is explicit: industry analyst report, account dossier, technical research paper, competitive intel brief, general write-up, or workshop / educational content.
- [ ] Research scope is explicit: web, uploaded files, prompt library, or mixed.
- [ ] Requested formats are explicit, or the SKILL.md default format table was applied.
- [ ] Identity is ms-identity: Frontier Cockpit Team, Software Global Black Belt, Microsoft, single contact `frontier-cockpit@example.com`.

## Source integrity

- [ ] Every empirical claim has a citation the user can verify.
- [ ] Every metric, price, market size, benchmark, vendor position, and quote is sourced or marked as an explicit assumption.
- [ ] Conflicting sources are labelled as conflicts, not reconciled by guessing.
- [ ] Market sizing shows the inputs and math.
- [ ] No fabricated customer counts, revenue figures, analyst rankings, or internal Microsoft data.

## Canonical Markdown gate

- [ ] Markdown is the single source of truth for all derivative formats.
- [ ] A References, Sources, or Bibliography section exists.
- [ ] No placeholders remain (`TODO`, `TBD`, `[source]`, `[citation needed]`, `XX%`, `NN`).
- [ ] No em dashes anywhere.
- [ ] "GitHub Copilot" is written in full except for official SKU names like `Copilot Business`.
- [ ] Run `python3 scripts/validate_report.py <file-or-folder>` and fix all errors.
- [ ] For client-facing work, run `python3 scripts/validate_report.py <file-or-folder> --strict` and address every warning.

## Workshop-specific gate

- [ ] The master index and all chapter outlines were approved before chapter generation.
- [ ] Chapters were generated in batches, not all at once before approval.
- [ ] `00-index.md` and `99-references.md` exist.
- [ ] Every chapter has frontmatter, learning outcomes, sources, and a references trail.

## Rendering gate

- [ ] Formats are rendered from the canonical Markdown only.
- [ ] PDF, PPTX, DOCX, XLSX, and HTML inherit the same sourced claims and references.
- [ ] Final files are saved under `output/`.
- [ ] The most polished or most requested format is presented first, with the remaining formats grouped clearly.
