#!/usr/bin/env python3
"""Validate a research deliverable (Markdown, the canonical source) for the
ms-research-report skill.

Hard gate. Exits non-zero on any error so a report cannot ship while it breaks
the editorial rules or the data-integrity rule. Run it on every .md the skill
produces before rendering to other formats.

Errors (fail the gate):
  1. Em dashes anywhere.
  2. Bare "Copilot" without "GitHub Copilot" (official SKU names are allowed).
  3. No References or Sources section.
  4. Unfilled placeholders (TODO, TBD, [source], [citation needed], XX%).

Warnings (review, or fail with --strict):
  5. Empirical claims (percentages, currency, "N customers", growth rates) on a
     line with no citation marker. This is the data-integrity check: numbers
     must be sourced.
  6. Projection or forecast language with no Methodology/Caveats/Assumptions block.
  7. Regional framing (LATAM, Brazil, ...) when the report is meant to be
     territory neutral.
  8. Corporate filler openers.

Usage:
    python validate_report.py <file.md | dir> [--strict]

See ../SKILL.md (Editorial rules) and references/research-methods.md.
"""

import argparse
import os
import re
import sys

# Official GitHub Copilot SKU and product names that keep a bare "Copilot".
COPILOT_ALLOWED = [
    "GitHub Copilot", "Microsoft Copilot", "Copilot Studio", "Copilot Pro+",
    "Copilot Pro", "Copilot Business", "Copilot Enterprise", "Copilot Free",
    "Copilot Chat",
]

CITATION_MARKERS = re.compile(
    r"\[\d+\]|\[[^\]]*\d{4}[^\]]*\]|\(([^)]*\b(?:20\d\d|source|gartner|forrester|idc|"
    r"mckinsey|microsoft|github)\b[^)]*)\)|https?://|according to|per\s+\w+|source:",
    re.I,
)

# Empirical-claim signals: percentages, currency, multipliers, "N customers".
EMPIRICAL = re.compile(
    r"\b\d+(?:\.\d+)?\s?%|\b(?:US\$|\$|R\$|EUR|USD)\s?\d|\b\d+(?:\.\d+)?x\b|"
    r"\b\d[\d,\.]*\s+(?:customers|clients|seats|users|deployments|enterprises|"
    r"developers|organizations)\b|\bgrew?\s+\d|\bgrowth of\s+\d",
    re.I,
)

PROJECTION = re.compile(
    r"\b(?:forecast|projected|projection|by 20\d\d|will reach|expected to|"
    r"estimate[ds]?|CAGR|through 20\d\d)\b", re.I)

REGIONAL = re.compile(
    r"\b(?:LATAM|Latin America|Brazil|Brazilian|Spanish-speaking)\b", re.I)

FILLER = re.compile(
    r"in today's (?:fast-paced|digital|modern) world|it is important to note that|"
    r"in the ever-(?:changing|evolving)|in conclusion,|at the end of the day",
    re.I)

PLACEHOLDERS = re.compile(
    r"\bTODO\b|\bTBD\b|\[source\]|\[citation needed\]|\bXX%|\bNN\b|\blorem ipsum\b",
    re.I)


def find_bare_copilot(text):
    hits = []
    for m in re.finditer(r"\bCopilot\b", text):
        s = m.start()
        window = text[max(0, s - 12):s + 20]
        if any(a in text[max(0, s - 12):s + 18] for a in COPILOT_ALLOWED):
            continue
        # Allowed if directly preceded by "GitHub " or "Microsoft ".
        before = text[max(0, s - 10):s]
        if before.endswith(("GitHub ", "Microsoft ")):
            continue
        hits.append(window.strip())
    return hits


def validate(path, strict):
    errors, warnings = [], []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        return [f"cannot read file: {exc}"], []

    lines = text.split("\n")

    # 1. Em dashes.
    em_lines = [i + 1 for i, ln in enumerate(lines) if "\u2014" in ln]
    if em_lines:
        errors.append(f"em dash on line(s) {em_lines[:10]} (forbidden)")

    # 2. Bare Copilot.
    bare = find_bare_copilot(text)
    if bare:
        errors.append(f"bare 'Copilot' without 'GitHub Copilot': e.g. \"{bare[0]}\"")

    # 3. References section.
    if not re.search(r"(?mi)^#{1,4}\s+(references|sources|bibliography)\b", text):
        errors.append("no References or Sources section")

    # 4. Placeholders.
    ph = sorted({m.group(0) for m in PLACEHOLDERS.finditer(text)})
    if ph:
        errors.append(f"unfilled placeholders: {ph}")

    # 5. Empirical claims without a citation on the same line.
    uncited = []
    in_code = False
    for i, ln in enumerate(lines):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or ln.strip().startswith(("#", ">", "|")):
            continue
        if EMPIRICAL.search(ln) and not CITATION_MARKERS.search(ln):
            uncited.append(i + 1)
    if uncited:
        warnings.append(
            f"empirical claim with no citation on line(s) {uncited[:10]}"
            + (" ..." if len(uncited) > 10 else "")
        )

    # 6. Projections without a caveats block.
    if PROJECTION.search(text) and not re.search(
            r"(?mi)^#{1,4}.*\b(methodology|assumptions|caveats|limitations)\b", text):
        warnings.append("projection/forecast language but no Methodology/Caveats block")

    # 7. Regional framing.
    reg = sorted({m.group(0) for m in REGIONAL.finditer(text)})
    if reg:
        warnings.append(f"regional framing found (territory-neutral by default): {reg}")

    # 8. Filler.
    if FILLER.search(text):
        warnings.append("corporate filler phrase found")

    if strict:
        errors.extend(warnings)
        warnings = []
    return errors, warnings


def iter_files(target):
    if os.path.isdir(target):
        for root, _, files in os.walk(target):
            for f in sorted(files):
                if f.endswith(".md"):
                    yield os.path.join(root, f)
    else:
        yield target


def main(argv):
    ap = argparse.ArgumentParser(description="Validate a research deliverable (Markdown).")
    ap.add_argument("target", help="A .md file or a directory of .md files")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = ap.parse_args(argv[1:])

    total_err = 0
    any_file = False
    for path in iter_files(args.target):
        any_file = True
        errs, warns = validate(path, args.strict)
        for w in warns:
            print(f"WARN  {path}: {w}")
        if errs:
            total_err += len(errs)
            print(f"FAIL  {path}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK    {path}")

    if not any_file:
        print(f"no .md files found at {args.target}")
        return 2
    if total_err:
        print(f"\n{total_err} error(s). Fix before rendering other formats; do not ship unsourced numbers.")
        return 1
    print("\nResearch deliverable passes the validation gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
