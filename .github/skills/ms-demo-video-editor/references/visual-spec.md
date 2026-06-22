# Visual Spec, ms-identity Video

This reference derives from the `ms-identity` identity system. If there is a conflict, the `ms-identity` skill is the source of truth.

## Tokens

```text
RED #F25022, GRN #7FBA00, BLU #00A4EF, YEL #FFB900
INK #1A1A1A, PAPER #FFFFFF, BG-frame #F7F7F5, BG-dark #141519 to #1B1D23
Fonts: Inter variable and JetBrains Mono variable from Google Fonts
Weights: title Inter 800, subtitle Inter 600, body 450 to 500, mono JetBrains Mono 600
```

## Logo `</.>`

Official SVG paths are embedded in `scripts/brand_assets.py` with `viewBox="0 0 1914 1062"`. Use only the Microsoft 4-color palette. Render with `cairosvg`. The old personal palette is forbidden.

## Cover, Dark 1920x1080

- Background `#141519` with soft radial vignette to `#1B1D23`.
- Logo at 300 px, positioned around `(160,150)`.
- Kicker in JetBrains Mono 34, uppercase, theme color, format `PROJETO // CONTEXTO`.
- Title in Inter ExtraBold 118 to 150, paper color, one or two lines.
- Four-color gradient bar under the title.
- Subtitle in Inter Semibold 34 to 40, `#C9CCD4` or `#8A8F99`.
- Byline in mono 26, `#8A8F99`: `PAULA SILVA | SOFTWARE GLOBAL BLACK BELT`.
- Optional slow `zoompan` from 1 to 1.05 across the card.

## End Card, Dark

- Centered logo around y=240.
- Closing thesis in Inter ExtraBold 76, centered, one or two lines.
- Four-color gradient bar below thesis.
- Mono byline and `Microsoft · GitHub` co-brand.
- Closing phrase should state the presentation thesis, for example: `Mesmos dados. Mesmas regras. Novo sistema.`

## Content Frame, Light

- Background `#F7F7F5`.
- White content rectangle around `1764x952` at `(78,46)` with baked shadow.
- Footer has mono byline at left, logo at right, and four-color hairline at bottom.
- Video sits inside the white frame with padding appropriate to aspect ratio.

## Lower Thirds

- White pill, rounded 14, with soft shadow.
- Accent bar at left, 8 px wide.
- Kicker in JetBrains Mono 24, uppercase, accent color, format `NN · SEÇÃO`.
- Title in Inter Semibold 34, one line, concrete and factual.
- Position around `(110,848)` over the framed video.
- Fade in around 0.35 s and fade out around 0.45 to 0.5 s.
- Rotate accent colors in Microsoft order: blue, green, yellow, red, blue.

## Highlights

Use a double `drawbox`: fill `#FFB900@0.15` and stroke `#FFB900@0.95`, with short verified windows. Keep highlights centered on verified frames.

## Canonical Strings

```text
Frontier Cockpit Team | Software Global Black Belt
Microsoft · GitHub
```

Use `Software Global Black Belt`, never abbreviated role labels. If contact appears, use only `frontier-cockpit@example.com`.
