# First-run checklist

Use this gate before presenting any Gartner-style deck. One deck definition must produce all requested formats. If a check fails, fix the source scripts and regenerate every derivative.

## Source of truth

- [ ] HTML and PPTX definitions are in sync: matching slide order, titles, sections, and trimmed subset.
- [ ] `build_html.py` and `deck_data.py` were edited together.
- [ ] The deck is the right size for the audience. Default is 16 to 25 slides; the 53-slide reference deck is a ceiling, not a target.
- [ ] No padding slides were added just to fill a number.

## Identity and copy

- [ ] Frontier Cockpit Team, Software Global Black Belt, Microsoft identity is used throughout.
- [ ] Single contact is `frontier-cockpit@example.com`.
- [ ] Microsoft 4-color palette only.
- [ ] No em dashes anywhere in visible text, comments copied into speaker notes, or generated strings.
- [ ] "GitHub Copilot" is written in full when referring to GitHub Copilot.
- [ ] No personal identity strings or personal social handles.
- [ ] Any customer, price, metric, analyst claim, or benchmark is sourced or marked as illustrative.

## Build prerequisites

- [ ] For PPTX/PDF paths, install dependencies with `pip install -r scripts/requirements.txt`.
- [ ] For PDF, install Chromium with `python -m playwright install chromium`.
- [ ] `python3 -m py_compile scripts/*.py` passes.

## HTML build

- [ ] `python3 scripts/build_html.py --out deck.html` exits 0.
- [ ] The output HTML exists, is non-empty, and contains the expected slide count.
- [ ] The HTML opens in a browser with no console errors.

## PPTX build

- [ ] `python3 scripts/build_pptx.py --out deck.pptx` exits 0.
- [ ] The generated PPTX can be reopened by python-pptx.
- [ ] Slide count matches the selected deck subset.
- [ ] Every slide has speaker notes with `[OPENING]`, `[CORE]`, `[TRANSITION]`, and `[TIMING]` markers.
- [ ] Key slides were opened in PowerPoint or LibreOffice to confirm native editability and no overlap.

## PDF build

- [ ] `python3 scripts/build_pdf.py --input deck.html --output deck.pdf` exits 0.
- [ ] The generated PDF exists and is non-empty.
- [ ] The PDF opens and shows one page per slide.

## Delivery

- [ ] Requested formats are delivered together and labelled: HTML source, native editable PPTX, vector PDF.
- [ ] If only one format was requested, mention that the others can be generated from the same deck definition.
