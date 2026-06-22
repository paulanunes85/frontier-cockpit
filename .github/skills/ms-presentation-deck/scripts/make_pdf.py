#!/usr/bin/env python3
"""
make_pdf.py: generate a PDF from the public HTML deck via Playwright.

Strategy: navigate to each slide individually, wait for animations to settle, capture a PDF
of just that slide. Then concatenate all per-slide PDFs into one final PDF.

Why slide-by-slide instead of full_page=True? Slides are absolute-positioned in the HTML;
only one is visible (data-active="true") at a time. A full-page capture would only get one slide.

Critical Playwright settings:
- reduced_motion='no-preference' (NOT the default 'reduce') so stagger animations render correctly
- 1.5s wait after goToSlide() before capturing
- Inject CSS to hide chrome elements: deck-controls, kbd-hint, lang-switcher

Dependencies (see scripts/requirements.txt):
    pip install -r scripts/requirements.txt
    python -m playwright install chromium

Usage:
    python make_pdf.py <input_public.html> <output.pdf> [--total 20] [--locale pt-BR]
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path


# Widescreen 16:9, matching the HTML viewport at 96 DPI (1280x720 px)
W_IN, H_IN = 13.333, 7.5
W_PX, H_PX = int(W_IN * 96), int(H_IN * 96)


def _preflight():
    """Import heavy deps lazily and fail with actionable guidance if missing."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "ERROR: Playwright is not installed.\n"
            "  pip install -r scripts/requirements.txt\n"
            "  python -m playwright install chromium"
        )
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        sys.exit(
            "ERROR: pypdf is not installed.\n"
            "  pip install -r scripts/requirements.txt"
        )
    return sync_playwright, PdfReader, PdfWriter


def make_pdf(input_path: str, output_path: str, total_slides: int = 20, locale: str = "pt-BR") -> None:
    sync_playwright, PdfReader, PdfWriter = _preflight()
    input_abs = Path(input_path).absolute()
    if not input_abs.is_file():
        sys.exit(f"ERROR: input HTML not found: {input_abs}")
    out_dir = Path(tempfile.mkdtemp(prefix="pdf_slides_"))

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as exc:  # noqa: BLE001 - surface a friendly install hint
            sys.exit(
                "ERROR: could not launch Chromium. Install the browser binary:\n"
                "  python -m playwright install chromium\n"
                f"  (details: {exc})"
            )
        ctx = browser.new_context(
            viewport={"width": W_PX, "height": H_PX},
            device_scale_factor=2,
            reduced_motion="no-preference",
        )
        page = ctx.new_page()
        page.goto(f"file://{input_abs}")
        page.wait_for_load_state("networkidle")

        page.evaluate(f'setLocale("{locale}")')

        # Hide chrome elements via injected CSS
        page.add_style_tag(content="""
            .deck-controls { display: none !important; }
            .kbd-hint      { display: none !important; }
            .lang-switcher { display: none !important; }
            body           { overflow: hidden !important; }
        """)
        page.wait_for_timeout(300)

        for i in range(total_slides):
            page.evaluate(f"goToSlide({i})")
            page.wait_for_timeout(1500)  # wait for stagger animations
            pdf_path = out_dir / f"slide_{i + 1:02d}.pdf"
            page.pdf(
                path=str(pdf_path),
                width=f"{W_IN}in",
                height=f"{H_IN}in",
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                print_background=True,
                prefer_css_page_size=False,
            )
            print(f"  Slide {i + 1:02d}/{total_slides}: {pdf_path.stat().st_size} bytes")

        browser.close()

    # Concatenate all per-slide PDFs
    writer = PdfWriter()
    for i in range(1, total_slides + 1):
        writer.append(str(out_dir / f"slide_{i:02d}.pdf"))
    with open(output_path, "wb") as f:
        writer.write(f)

    # Validate the output before declaring success.
    if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
        sys.exit("ERROR: output PDF was not written or is empty")
    reader = PdfReader(output_path)
    pages = len(reader.pages)
    print(f"\nFinal PDF: {output_path}")
    print(f"Size: {os.path.getsize(output_path)} bytes, {pages} pages")
    if pages != total_slides:
        sys.exit(
            f"ERROR: page count {pages} does not match slide count {total_slides}; "
            "check --total and re-run"
        )
    print("  OK: page count matches slide count")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input public.html")
    parser.add_argument("output", help="Output PDF")
    parser.add_argument("--total", type=int, default=20, help="Total number of slides")
    parser.add_argument("--locale", default="pt-BR", choices=["pt-BR", "en", "es"])
    args = parser.parse_args()
    make_pdf(args.input, args.output, args.total, args.locale)


if __name__ == "__main__":
    main()
