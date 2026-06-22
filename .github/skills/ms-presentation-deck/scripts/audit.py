#!/usr/bin/env python3
"""
audit.py — identity and quality audit for a multi.html deck.

Checks:
1. Em dashes (—) — should be 0 anywhere in the file (forbidden in Paula's style)
2. Identity strings — required presence of "Software Global Black Belt", "frontier-cockpit@example.com", "GitHub Copilot"
3. Forbidden strings — absence of "@your-org", "your-handle", "Microsoft Americas", "Frontier Cockpit", "Microsoft Global Black Belt"
4. Colors — usage of the Microsoft 4-color palette (F25022, 7FBA00, FFB900, 00A4EF); flags non-MS reds/greens/yellows/blues that look brand-adjacent
5. Notes completeness — counts characters/words per locale per slide
6. JS validity — pipes the script content through node --check
7. Favicon — required inline Microsoft 4-square SVG favicon (no external favicon.svg reference)
8. Social preview — required Open Graph and Twitter meta with og:locale
9. Section dividers — dark dividers must use Roman numerals, not 01/02 style numbers

Usage:
    python audit.py <deck.html> [--max-em-dashes 0] [--locales en pt-BR es]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile


REQUIRED_STRINGS = [
    "Software Global Black Belt",
    "frontier-cockpit@example.com",
    "GitHub Copilot",
]

FORBIDDEN_STRINGS = [
    "@your-org",
    "your-handle",
    "Microsoft Americas",
    "Frontier Cockpit",
    "Microsoft Global Black Belt",
    "AI-Native Software Engineer",
]

MS_COLORS = {
    "F25022": "Microsoft red",
    "7FBA00": "Microsoft green",
    "FFB900": "Microsoft yellow",
    "00A4EF": "Microsoft blue",
}

# Common look-alike colors that signal "someone used the wrong palette"
SUSPICIOUS_COLORS = {
    "FF3133": "red (use Microsoft red F25022 instead)",
    "7ED956": "green (use Microsoft green 7FBA00 instead)",
    "FFDE59": "yellow (use Microsoft yellow FFB900 instead)",
    "39B8FF": "blue (use Microsoft blue 00A4EF instead)",
    "1976D2": "blue (use Microsoft blue 00A4EF instead)",
}


def extract_i18n(content: str):
    """Parse the I18N object out of the deck JS."""
    start = content.find("const I18N = {")
    if start < 0:
        return None
    i = start + len("const I18N = ")
    depth = 0
    in_str = False
    str_ch = None
    esc = False
    end = -1
    while i < len(content):
        c = content[i]
        if esc:
            esc = False
        elif in_str:
            if c == "\\":
                esc = True
            elif c == str_ch:
                in_str = False
        else:
            if c in ('"', "'"):
                in_str = True
                str_ch = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    if end < 0:
        return None
    try:
        return json.loads(content[start + len("const I18N = ") : end])
    except json.JSONDecodeError:
        return None


def check_js(content: str) -> tuple[bool, str]:
    m = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
    if not m:
        return False, "No <script> block found"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
        f.write(m.group(1))
        path = f.name
    result = subprocess.run(["node", "--check", path], capture_output=True, text=True)
    return result.returncode == 0, result.stderr.strip() if result.returncode != 0 else "OK"


def audit(deck_path: str, max_em_dashes: int = 0, locales: list[str] = None, check_assets: bool = False) -> int:
    if locales is None:
        locales = ["en", "pt-BR", "es"]

    content = open(deck_path).read()
    errors = 0
    warnings = 0

    print(f"=== Audit: {deck_path} ({len(content)} bytes) ===\n")

    # 1. Em dashes
    em_count = content.count("—")
    if em_count > max_em_dashes:
        print(f"  FAIL: em dashes found: {em_count} (max allowed: {max_em_dashes})")
        errors += 1
    else:
        print(f"  OK: em dashes: {em_count}")

    # 2. Required strings
    for s in REQUIRED_STRINGS:
        count = content.count(s)
        if count == 0:
            print(f"  FAIL: required string missing: '{s}'")
            errors += 1
        else:
            print(f"  OK: '{s}': {count} occurrences")

    # 3. Forbidden strings
    for s in FORBIDDEN_STRINGS:
        count = content.count(s)
        if count > 0:
            print(f"  FAIL: forbidden string found: '{s}' ({count} occurrences)")
            errors += 1
    print(f"  OK: no forbidden strings" if all(content.count(s) == 0 for s in FORBIDDEN_STRINGS) else "")

    # 4. Suspicious colors
    for hex_color, msg in SUSPICIOUS_COLORS.items():
        count = content.count(f"#{hex_color}") + content.count(hex_color.lower())
        if count > 0:
            print(f"  WARN: suspicious color #{hex_color} ({msg}) found {count} times")
            warnings += 1

    # 5. Check "GitHub Copilot" never abbreviated to just "Copilot"
    bare_copilot = len(re.findall(r"(?<!GitHub )Copilot(?! Studio)", content))
    if bare_copilot > 0:
        print(f"  WARN: 'Copilot' without 'GitHub' prefix: {bare_copilot} occurrences (may be in code blocks or notes; check manually)")
        warnings += 1

    # 6. JS validity
    js_ok, js_msg = check_js(content)
    if js_ok:
        print(f"  OK: JS valid")
    else:
        print(f"  FAIL: JS invalid: {js_msg[:300]}")
        errors += 1

    # 7. Favicon: inline Microsoft 4-square SVG data URI, no external reference
    has_inline_favicon = bool(
        re.search(r'rel="icon"[^>]*href="data:image/svg\+xml,', content)
    )
    if has_inline_favicon:
        print("  OK: inline Microsoft favicon present")
    else:
        print("  FAIL: inline Microsoft favicon missing (see references/head-meta.md)")
        errors += 1
    if 'images-logo/favicon.svg' in content or re.search(r'href="[^"]*\.\./[^"]*favicon\.svg"', content):
        print("  FAIL: external favicon reference found (must inline the data URI)")
        errors += 1
    # Favicon must use the Microsoft 4-square mark and palette.
    fav_match = re.search(r'rel="icon"[^>]*href="(data:image/svg\+xml,[^"]*)"', content)
    if fav_match and not all(c in fav_match.group(1) for c in ("F25022", "7FBA00", "FFB900", "00A4EF")):
        print("  FAIL: favicon does not use the Microsoft 4-color palette")
        errors += 1
    if fav_match:
        favicon_uri = fav_match.group(1)
        has_square_viewbox = "viewBox%3D%270%200%2032%2032%27" in favicon_uri or "viewBox%3D%220%200%2032%2032%22" in favicon_uri
        has_square_rects = all(fragment in favicon_uri for fragment in ("x%3D%272%27", "x%3D%2717%27", "y%3D%272%27", "y%3D%2717%27"))
        if not (has_square_viewbox and has_square_rects):
            print("  FAIL: favicon must be the Microsoft 4-square logo (see references/head-meta.md)")
            errors += 1

    # 8. Social preview: Open Graph and Twitter meta with locale
    og_required = ["og:title", "og:description", "og:image", "og:locale", "twitter:card", "twitter:image"]
    missing_og = [m for m in og_required if m not in content]
    if missing_og:
        print(f"  FAIL: social preview meta missing: {missing_og} (see references/head-meta.md)")
        errors += 1
    else:
        print("  OK: social preview meta present (Open Graph and Twitter)")

    # 8b. Asset existence (opt-in): referenced preview images must exist on disk.
    if check_assets:
        deck_dir = os.path.dirname(os.path.abspath(deck_path))
        img_refs = re.findall(
            r'<meta[^>]*(?:property|name)="(?:og:image|twitter:image)"[^>]*content="([^"]+)"',
            content,
        )
        img_refs += re.findall(
            r'<meta[^>]*content="([^"]+)"[^>]*(?:property|name)="(?:og:image|twitter:image)"',
            content,
        )
        local_refs = sorted(
            {
                ref
                for ref in img_refs
                if not ref.startswith(("http://", "https://", "data:"))
            }
        )
        if not local_refs:
            print("  OK: no local preview images to verify (remote or data URIs)")
        for ref in local_refs:
            asset_path = os.path.normpath(os.path.join(deck_dir, ref))
            if os.path.isfile(asset_path):
                print(f"  OK: preview asset exists: {ref}")
            else:
                print(f"  FAIL: preview asset missing: {ref} (generate it before publishing)")
                errors += 1

    # 9. Section dividers: the approved standard uses Roman numerals (I, II, III...).
    numeric_dividers = re.findall(r'class="section-number">\s*(\d+)\s*<', content)
    if numeric_dividers:
        print(f"  FAIL: section dividers must use Roman numerals, found numeric values: {numeric_dividers}")
        errors += 1
    elif 'class="section-number"' in content:
        print("  OK: section dividers use Roman numerals")
    numbered_eyebrows = re.findall(r'<div\s+class="eyebrow"[^>]*>\s*((?:Part|PART|Parte|PARTE)\s+(?:[IVXLC]+|\d+))\s*</div>', content)
    if numbered_eyebrows:
        print(f"  FAIL: section divider label must be PART/PARTE without a number, found: {numbered_eyebrows}")
        errors += 1
    if 'class="section-number"' in content:
        has_reference_divider_css = (
            "clamp(180px, 26vw, 400px)" in content
            and ("font-weight: 300" in content or "font-weight:300" in content)
        )
        if not has_reference_divider_css:
            print("  FAIL: section divider CSS must match the reference Roman numeral style")
            errors += 1

    # 10. Notes completeness
    i18n = extract_i18n(content)
    if i18n is None:
        print("  WARN: could not parse I18N block")
        warnings += 1
    else:
        for loc in locales:
            if loc not in i18n:
                print(f"  WARN: locale '{loc}' not in I18N")
                warnings += 1
                continue
            notes = i18n[loc].get("notes")
            if not notes:
                print(f"  WARN: no notes for locale '{loc}'")
                warnings += 1
                continue
            total_words = sum(len(n.split()) for n in notes.values())
            avg_words = total_words / len(notes) if notes else 0
            short = [k for k, v in notes.items() if len(v.split()) < 50]
            print(f"  Notes {loc}: {len(notes)} slides, avg {avg_words:.0f} words/slide")
            if short:
                print(f"    short notes (<50 words): {short}")
                warnings += 1

    print(f"\n=== Result: {errors} errors, {warnings} warnings ===")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("deck", help="Path to the multi.html deck")
    parser.add_argument("--max-em-dashes", type=int, default=0)
    parser.add_argument("--locales", nargs="+", default=["en", "pt-BR", "es"])
    parser.add_argument(
        "--check-assets",
        action="store_true",
        help="Verify referenced preview images (og:image, twitter:image) exist on disk",
    )
    args = parser.parse_args()
    sys.exit(audit(args.deck, args.max_em_dashes, args.locales, args.check_assets))


if __name__ == "__main__":
    main()
