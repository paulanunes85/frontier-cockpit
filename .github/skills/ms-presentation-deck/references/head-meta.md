# Head, favicon, and social preview (mandatory)

Every deck HTML (the multilingual presenter file, the public file, and any per-locale export) must ship a self-contained `<head>` with the Microsoft favicon and the social preview meta. Self-contained means no external file references, so the deck keeps its identity when shared or moved.

## 1. Favicon (inline Microsoft 4-square mark, always)

Inline the Microsoft 4-square logo as an SVG data URI. Never reference an external `favicon.svg` (it breaks when the deck is moved).

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20viewBox%3D%270%200%2032%2032%27%20xmlns%3D%27http%3A//www.w3.org/2000/svg%27%3E%3Crect%20x%3D%272%27%20y%3D%272%27%20width%3D%2713%27%20height%3D%2713%27%20fill%3D%27%23F25022%27/%3E%3Crect%20x%3D%2717%27%20y%3D%272%27%20width%3D%2713%27%20height%3D%2713%27%20fill%3D%27%237FBA00%27/%3E%3Crect%20x%3D%272%27%20y%3D%2717%27%20width%3D%2713%27%20height%3D%2713%27%20fill%3D%27%2300A4EF%27/%3E%3Crect%20x%3D%2717%27%20y%3D%2717%27%20width%3D%2713%27%20height%3D%2713%27%20fill%3D%27%23FFB900%27/%3E%3C/svg%3E">
```

The four fills are the Microsoft palette only: `#F25022`, `#7FBA00`, `#00A4EF`, `#FFB900`. Never use the personal palette in the favicon.

## 2. Social preview meta (Open Graph and Twitter)

Add a 1200x630 preview so a shared deck link renders a card. Keep the title and description in the deck locale, write "GitHub Copilot" in full, and use no em dashes.

```html
<meta property="og:type" content="website" />
<meta property="og:title" content="<localized deck title>" />
<meta property="og:description" content="<localized one-line summary>" />
<meta property="og:image" content="preview-en.png" />
<meta property="og:url" content="<canonical url or filename>" />
<meta property="og:locale" content="en_US" />
<meta property="og:locale:alternate" content="pt_BR" />
<meta property="og:locale:alternate" content="es_ES" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="<localized deck title>" />
<meta name="twitter:description" content="<localized one-line summary>" />
<meta name="twitter:image" content="preview-en.png" />
```

Locale codes: English `en_US`, Portuguese `pt_BR`, Spanish `es_ES`.

## 3. Preview image per language

Social scrapers do not run JavaScript, so the language a card shows is fixed at share time. Produce one preview per locale, matched to how the deck is shared:

- The multilingual presenter file (`*_multi.html`) and the public file (`*_public.html`) switch language client-side. Set `og:locale` to the default locale you are sharing, add `og:locale:alternate` for the other two, and localize `og:title` and `og:description` to that default. Reference `preview-<locale>.png`.
- Per-locale exports: when you export one deck per locale (alongside the per-locale PDF and PPTX), each exported HTML carries its own `og:locale`, its own localized title and description, and its own `preview-<locale>.png`.

Generate each preview by rendering slide 1 (the cover) in that locale at 1200x630 and saving `assets/preview-en.png`, `assets/preview-pt.png`, `assets/preview-es.png`. The cover already carries the Microsoft logo and "PAULA SILVA | SOFTWARE GLOBAL BLACK BELT", so the card stays on identity. Point `og:image` and `twitter:image` at the file that matches the page locale.

## Checklist before a deck is done

1. Inline Microsoft favicon present in every deck HTML (no external `favicon.svg`).
2. Open Graph and Twitter meta present, title and description localized to the deck.
3. `og:locale` set, with `og:locale:alternate` for the other two languages.
4. A 1200x630 `preview-<locale>.png` exists and is referenced.
5. Favicon is the Microsoft 4-square logo, uses only the Microsoft palette, and passes `audit.py`.
