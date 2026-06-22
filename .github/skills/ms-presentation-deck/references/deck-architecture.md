# Deck architecture

The HTML deck is a single-file, self-contained presentation. No build step, no external dependencies (other than CDN fonts). Open it directly in a browser and it works.

## File structure

A multi.html (the master source of truth) contains, in order:

1. `<head>` with meta, title, and a single `<link>` to Google Fonts (Inter + JetBrains Mono).
2. `<style>` with all CSS. Uses CSS custom properties for the palette.
3. `<body>` with:
   - `.deck-controls` (top right): EN/PT/ES locale switcher
   - 20 `.slide` elements positioned absolutely, only one visible at a time
   - `.notes-panel` at the bottom (toggled with N)
   - `.kbd-hint` overlay (auto-hides after 4 seconds)
   - `.lang-switcher` at the bottom right (← → arrows + slide counter)
   - `.overview-grid` (toggled with O) showing all slides as thumbnails
4. A single `<script>` containing all the deck logic.

## Viewport and units

- The "stage" is **1280 × 720 px** (16:9 widescreen).
- All slide content is scaled to fit this viewport using `transform: scale()`.
- The CSS uses **px** (not em or rem) for the stage, so coordinates translate predictably to PPTX inches (1 inch = 96 px, slide is 13.333 in × 7.5 in).

## Palette (CSS variables)

```css
:root {
  --ps-color-ms-red-500: #F25022;
  --ps-color-ms-green-500: #7FBA00;
  --ps-color-ms-yellow-500: #FFB900;
  --ps-color-ms-blue-500: #00A4EF;
  --ps-color-ink: #1A1A19;
  --ps-color-ink-2: #5C5A52;
  --ps-color-ink-3: #82807A;
  --ps-color-paper: #F8F7F2;
  --ps-color-rule: #E8E5DC;
  --ps-color-bg: #FFFFFF;
  --ps-color-dark-bg: #0F0F0E;
  --ps-color-dark-ink: #F0F0EB;
  --ps-color-dark-ink-2: #B8B6AE;
  --ps-color-dark-ink-3: #82807A;
  --ps-font-sans: 'Inter', system-ui, sans-serif;
  --ps-font-mono: 'JetBrains Mono', 'Consolas', monospace;
}
```

## Slide structure

Each slide is:

```html
<div class="slide" data-active="false" data-theme="light">
  <div class="brand-header">
    <div class="brand-squares"><span></span><span></span><span></span><span></span></div>
    <span class="brand-text">PAULA SILVA  |  SOFTWARE GLOBAL BLACK BELT</span>
  </div>
  <div class="slide-content">
    <!-- pattern-specific content with data-i18n attributes -->
  </div>
  <div class="page-number" data-i18n="labels.pageOf">01 / 20</div>
</div>
```

Themes: `data-theme="light"` (default) or `data-theme="dark"` (for dividers and closing slide).

## I18N

Three locales in a global `I18N` object:

```javascript
const I18N = {
  "en": { /* all keys */ },
  "pt-BR": { /* all keys */ },
  "es": { /* all keys */ }
};
```

Keys use **dot notation, max 2 levels, camelCase last segment**:

```javascript
{
  "cover": {
    "eyebrow": "Token Economics",
    "part1": "Token management and agent design",
    "keyword1": "for the GitHub Copilot AI Credits era",
    "subtitle": "..."
  },
  "agenda": {
    "title": "Five parts, one frame.",
    "item1": "...", "item2": "...", "item3": "...", "item4": "...", "item5": "..."
  }
}
```

**DON'T DO THIS**: `"cover.title.line1"` as a leaf key — the resolver breaks. Use `"cover.line1"` instead.

The resolver:

```javascript
function resolveKey(obj, dotPath) {
  return dotPath.split('.').reduce((o, k) => o?.[k], obj);
}
```

Applied to every element with `data-i18n="key.path"`. Lists use `data-i18n-list="key.path"` and the resolver expects an array.

## Locale switching

```javascript
function setLocale(loc) {
  currentLocale = loc;
  document.documentElement.setAttribute('lang', loc);
  localStorage.setItem('ps-locale', loc);
  // Update all [data-i18n] and [data-i18n-list] elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = resolveKey(I18N[loc], el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-list]').forEach(el => {
    const list = resolveKey(I18N[loc], el.dataset.i18nList);
    if (Array.isArray(list)) el.innerHTML = list.map(item => `<li>${item}</li>`).join('');
  });
  // Update the kbd-hint via uiBundles
  // Update notes via renderNotes()
  // Notify presenter via broadcastState()
}
```

## Locale default

```javascript
const saved = (() => { try { return localStorage.getItem('ps-locale'); } catch { return null; }})();
const browser = navigator.language?.startsWith('pt') ? 'pt-BR'
              : navigator.language?.startsWith('es') ? 'es'
              : 'en';
setLocale(saved || browser);
```

For the public version (which is single-locale), replace this with a hardcoded `setLocale('pt-BR')` (or whatever target).

## Navigation

```javascript
function goToSlide(i) {
  if (i < 0 || i >= total) return;
  slides.forEach(s => s.setAttribute('data-active', 'false'));
  slides[i].setAttribute('data-active', 'true');
  currentSlide = i;
  syncSlideTheme(i);  // Sets body data-slide-theme for chrome adaptation
  if (typeof renderNotes === 'function') renderNotes();
  if (typeof broadcastState === 'function') broadcastState();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft') goToSlide(currentSlide - 1);
  if (e.key === 'ArrowRight') goToSlide(currentSlide + 1);
  if (e.key === 'n' || e.key === 'N') toggleNotes();
  if (e.key === 'o' || e.key === 'O' || e.key === 'Escape') toggleOverview();
  if (e.key === 'f' || e.key === 'F') toggleFullscreenAndPresenter();
  if (e.key === 'p' || e.key === 'P') openPresenterView();
});
```

## Notes panel (inline, toggled with N)

A fixed panel at the bottom that shows the current slide's speaker notes inline. The notes go through `formatNote()` which converts markdown lite to styled HTML:

```javascript
function formatNote(text) {
  if (!text) return '';
  let s = text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  s = s.replace(/\*\*([^\*]+?)\*\*/g, '<strong>$1</strong>');   // **bold** -> yellow
  s = s.replace(/\*([^\*\n]+?)\*/g, '<em>$1</em>');             // *italic* -> blue
  s = s.replace(/\[([A-Z][^\]]*?)\]/g, '<span class="note-marker">[$1]</span>');  // [ABERTURA] -> green badge
  s = s.replace(/\[(pause|pausa)\]/gi, '<span class="note-pause">[$1]</span>');  // [pause] -> red
  s = s.replace(/\n\n+/g, '</p><p>').replace(/\n/g, '<br>');
  return '<p>' + s + '</p>';
}
```

CSS for these:

```css
.notes-panel__body p { margin-bottom: 14px; }
.notes-panel__body strong { color: var(--ps-color-ms-yellow-500); font-weight: 600; }
.notes-panel__body em { color: var(--ps-color-ms-blue-500); font-style: normal; font-weight: 500; }
.note-marker {
  display: inline-block;
  font-family: var(--ps-font-mono);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--ps-color-ms-green-500);
  padding: 2px 6px;
  background: rgba(127, 186, 0, 0.10);
  border-radius: 3px;
  margin-right: 6px;
  text-transform: uppercase;
}
.note-pause {
  font-family: var(--ps-font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--ps-color-ms-red-500);
  letter-spacing: 0.10em;
}
```

## Presenter view (separate window, opened with F or P)

A second-window full presenter view, synced via BroadcastChannel.

Architecture:

- Main deck has `const presenterChannel = new BroadcastChannel('ps-deck')`.
- Pressing F or P does `window.open('about:blank', 'presenter', '...')` then writes `PRESENTER_HTML` into it. F also requests fullscreen on the main window.
- Main deck `broadcastState()` posts `{ type: 'state', slideIdx, total, locale, currentTitle, currentEyebrow, nextTitle, nextEyebrow }` whenever locale or slide changes.
- Presenter window listens for these messages, updates its UI.
- Presenter window has its own `formatNote()` (duplicated, since it's a separate document).
- Presenter window has its own controls (← Prev / Next →, ESC to close).
- Heartbeat: every 2.5s the presenter checks `lastStateReceived`. If > 3s, it sends `{ type: 'request-state' }` and marks indicator as "reconnecting". If > 6s, "disconnected".
- Main deck listens for `request-state` and responds with `broadcastState()`.

Refresh button: a visible "↻ REFRESH" button in the presenter header that forces an immediate `request-state` send. This is the user's escape hatch for when the deck has been reloaded but the presenter window is stuck on stale data.

Connection indicator: a `<span class="pv-conn">` near the brand showing "connected" / "reconnecting" / "disconnected" with a pulsing dot, color-coded green/yellow/red. Label is localized.

The presenter window CSS uses a dark theme by default for low ambient light during presentation, regardless of slide theme.

## Overview mode (toggled with O)

A grid of all slides as scaled-down thumbnails. Click on one to jump to it. Escape closes overview.

## kbd-hint

A small overlay shown at startup that fades out after 4 seconds. Shows:

```
Use ← → para navegar · O visão geral · N notas · F apresentador
```

(localized via `uiBundles` in the JS, not via the I18N JSON, because it needs to render fast at load time)

For the public version, the kbd-hint is reduced to just:

```
Use ← → para navegar · O visão geral
```

**Two places to update**: the inline HTML in `<div class="kbd-hint">` AND the `uiBundles` block inside `setLocale()`. The inline HTML is shown initially; `uiBundles` overwrites it after locale switch. If you only fix one, the hint changes when the user clicks a locale switcher.

## Animations

Slides use `data-active="true"` to become visible. Inside an active slide, child elements with `data-stagger="N"` animate in with a `delay: N * 80ms` after the slide becomes active.

Implementation:

```css
.slide[data-active="true"] [data-stagger] {
  opacity: 0;
  transform: translateY(8px);
  animation: stagger-in 0.5s forwards;
}
.slide[data-active="true"] [data-stagger="1"] { animation-delay: 0.08s; }
.slide[data-active="true"] [data-stagger="2"] { animation-delay: 0.16s; }
/* ... up to 8 */
@keyframes stagger-in {
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .slide [data-stagger] { opacity: 1; transform: none; animation: none; }
}
```

**Playwright trap**: the default `reduced_motion` for Playwright contexts is `reduce`. This makes all stagger animations skip, which is fine — but if you're capturing during a transition, some elements may render unstyled. Always pass `reduced_motion='no-preference'` and wait 1.2–1.5 seconds after `goToSlide` before capturing.

## Persistent storage

The deck uses `localStorage.setItem('ps-locale', ...)` to remember the user's preferred locale. This is fine for the multi version. For the public version, the locale is forced, so this can be removed (but leaving it doesn't hurt).
