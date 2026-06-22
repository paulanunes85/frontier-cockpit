#!/usr/bin/env python3
"""
build_pdf.py: render the HTML deck to a vector PDF via Playwright print-CSS.

One page per slide, vector (not screenshots). The deck's print stylesheet
already sizes each .slide to one 16:9 page, so this just drives headless
Chromium through print emulation.

Usage:
    python3 build_pdf.py --input deck.html --output deck.pdf
"""

import argparse
import pathlib
import sys


def _preflight():
    """Import Playwright lazily and fail with install guidance if missing."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        sys.exit(
            f"ERROR: required dependency missing ({exc.name}).\n"
            "  pip install -r scripts/requirements.txt\n"
            "  python -m playwright install chromium"
        )
    return sync_playwright


def build_pdf(input_html, output_pdf):
    sync_playwright = _preflight()
    input_path = pathlib.Path(input_html).resolve()
    if not input_path.is_file():
        sys.exit(f"ERROR: input HTML not found: {input_path}")
    url = "file://" + str(pathlib.Path(input_html).resolve())
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:
            sys.exit(
                "ERROR: Chromium is not ready. Install it with:\n"
                "  python -m playwright install chromium\n"
                f"  details: {exc}"
            )
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(600)          # let fonts settle
        page.emulate_media(media="print")
        page.pdf(path=output_pdf, width="1280px", height="720px",
                 print_background=True, prefer_css_page_size=True)
        browser.close()
    output_path = pathlib.Path(output_pdf).resolve()
    if not output_path.is_file() or output_path.stat().st_size == 0:
        sys.exit(f"ERROR: PDF output is missing or empty: {output_path}")
    print(f"wrote {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Render the HTML deck to a vector PDF.")
    ap.add_argument("--input", default="ms-reference-deck.html",
                    help="input HTML deck (from build_html.py)")
    ap.add_argument("--output", default="ms-reference-deck.pdf",
                    help="output PDF path")
    args = ap.parse_args()
    build_pdf(args.input, args.output)
