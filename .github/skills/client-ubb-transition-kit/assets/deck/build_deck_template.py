# -*- coding: utf-8 -*-
"""Executive deck generator, client UBB transition kit, deliverable 4 of 4.

15 slides, trilingual (PT-BR/EN/ES), speaker notes (N) and presenter view (F),
ms-presentation-deck v2 pattern with the </.> personal logo.

How to use for a NEW client:
1. Copy this script to a work dir together with content_i18n.py and
   notes_i18n.py (start from the BTG masters in examples/, swap the data) and
   the golden deck examples/golden_BTG_*.html renamed to golden_deck_multi.html
   (it is the engine donor: its chrome and JS are reused, all sections and the
   I18N object are replaced).
2. Edit content_i18n.py: client name, the three scenarios, the September jump
   hero (moment.hero), the FY redemption hero (redeem.hero), deliverables,
   roadmap, levers stay as the R1-R7 standard, tracks, roles, closing dates.
3. Edit notes_i18n.py: s1..s15 per locale, [ABERTURA]/[NÚCLEO]/[GANCHO
   PROVOCATIVO]/[TRANSIÇÃO]/[TIMING] structure, the actual words to be spoken.
4. Run: DECK_OUT_NAME=Client_Deck_v1_0_0_<date>_multi.html python build_deck_template.py
5. Validate with Playwright (reduced_motion='no-preference'): 15 slides, i18n
   complete in 3 locales, 15/15 notes, zero JS errors, zero em dashes.

NON-NEGOTIABLE narrative rules (see references/deck-structure.md):
- 4-part structure: the moment / the work so far / the six-month program /
  two parallel tracks.
- The partnership is SIX MONTHS, June to December. September is the mid-program
  checkpoint (promo expiry), NEVER the end of the engagement.
- The commercial track is ALWAYS presented as an open set of options (extend
  the promotional credit, additional discount for the remaining months, and if
  it fits, Pre-Purchase Plan or ACD terms). Nothing predetermined: "o caminho
  certo sai da conversa". Never name internal desks.
- Levers: two slides with the official runbook bands (R1 40-70% of output,
  R2 40-70% of the bill, R4 40-80% of input, R5 30-50% of input, then R6
  compound, R3 BYOK zero-credit routine, R7 budgets guardrail). Always a
  sourced range, never a promise.
"""
import re, json
from content_i18n import PT, EN, ES
from notes_i18n import NOTES_PT, NOTES_EN, NOTES_ES

PT['notes'] = NOTES_PT; EN['notes'] = NOTES_EN; ES['notes'] = NOTES_ES
I18N = {"en": EN, "pt-BR": PT, "es": ES}

import os
# ENGINE_SOURCE: any previous ms-identity multi.html (its chrome/JS engine is reused;
# all 15 sections and the I18N object are replaced). Default: the BTG golden master.
ENGINE_SOURCE = os.environ.get('DECK_ENGINE_SOURCE', 'golden_deck_multi.html')
OUT_NAME = os.environ.get('DECK_OUT_NAME', 'Client_Deck_v1_0_0_multi.html')
h = open(ENGINE_SOURCE, encoding='utf-8').read()

ACC = {"red":"var(--ps-color-ms-red-500)","green":"var(--ps-color-ms-green-500)",
       "blue":"var(--ps-color-ms-blue-500)","yellow":"var(--ps-color-ms-yellow-500)"}

def divider(key, accent, num):
    return f'''<section class="slide slide--dark" style="--accent: {ACC[accent]};">
  <div class="eyebrow" data-i18n="{key}.eyebrow">Part</div>
  <div class="section-number">{num}</div>
  <h1 class="section-title" data-i18n="{key}.title">.</h1>
  <p class="subtitle" data-i18n="{key}.sub">.</p>
</section>'''

card = lambda key,n,accent: f'''<div style="padding: 26px; background: var(--ps-color-bg); border-top: 3px solid {ACC[accent]}; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);">
      <div style="font-family: var(--ps-font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: {ACC[accent]}; margin-bottom: 14px;" data-i18n="{key}.c{n}Label">.</div>
      <h3 style="font-size: 21px; font-weight: 600; line-height: 1.25; color: var(--ps-color-ink); margin-bottom: 10px;" data-i18n="{key}.c{n}Title">.</h3>
      <p style="font-size: 14px; line-height: 1.55; color: var(--ps-color-ink-2);" data-i18n="{key}.c{n}Body">.</p>
    </div>'''

S = []
# 1 cover
S.append('''<section class="slide slide--light" data-active="true" style="--accent: var(--ps-color-ms-blue-500);">
  <div class="eyebrow" data-i18n="cover.eyebrow">.</div>
  <h1 class="title">
    <span data-i18n="cover.part1">.</span>
    <span class="accent-blue" data-i18n="cover.keyword1">.</span>
  </h1>
  <p class="subtitle" data-i18n="cover.subtitle">.</p>
  <div class="meta-grid">
    <div class="meta-item"><span class="meta-label" data-i18n="labels.author">Autora</span><span class="meta-value">Frontier Cockpit Team</span></div>
    <div class="meta-item"><span class="meta-label" data-i18n="labels.role">Função</span><span class="meta-value">Software Global Black Belt</span></div>
    <div class="meta-item"><span class="meta-label" data-i18n="labels.duration">Cliente</span><span class="meta-value" data-i18n="cover.duration">.</span></div>
    <div class="meta-item"><span class="meta-label" data-i18n="labels.date">Data</span><span class="meta-value">2026-06-12</span></div>
  </div>
</section>''')
# 2 agenda (4 items)
S.append('''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-blue-500);" data-i18n="agenda.eyebrow">Agenda</div>
  <h2 class="title title--medium" data-i18n="agenda.title">.</h2>
  <div class="list-numbered stagger">
    <div class="list-numbered__item"><span class="list-numbered__num">01</span><span class="list-numbered__text" data-i18n="agenda.item1">.</span></div>
    <div class="list-numbered__item"><span class="list-numbered__num">02</span><span class="list-numbered__text" data-i18n="agenda.item2">.</span></div>
    <div class="list-numbered__item"><span class="list-numbered__num">03</span><span class="list-numbered__text" data-i18n="agenda.item3">.</span></div>
    <div class="list-numbered__item"><span class="list-numbered__num">04</span><span class="list-numbered__text" data-i18n="agenda.item4">.</span></div>
  </div>
</section>''')
# 3 divider parte 1
S.append(divider('p1','red','01'))
# 4 moment: big jump number + 3-scenario strip
S.append('''<section class="slide slide--light" style="--accent: var(--ps-color-ms-red-500);">
  <div class="eyebrow" data-i18n="moment.eyebrow">.</div>
  <div style="display:flex;flex-direction:column;gap:22px;margin-top:26px;">
    <div style="font-family: var(--ps-font-mono); font-size: 150px; font-weight: 600; line-height: 0.95; color: var(--ps-color-ms-red-500); letter-spacing: -0.02em;" data-i18n="moment.hero">+US$ 94k</div>
    <h2 class="title title--medium" data-i18n="moment.title" style="max-width:1100px;">.</h2>
    <p class="body-large" data-i18n="moment.body" style="max-width:1050px;">.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;padding-top:16px;border-top:1px solid var(--ps-color-rule);">
      <div><div style="font-family:var(--ps-font-mono);font-size:10px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-ms-blue-500);margin-bottom:6px;" data-i18n="moment.s1Label">.</div><div style="font-family:var(--ps-font-mono);font-size:19px;color:var(--ps-color-ink);" data-i18n="moment.s1">.</div></div>
      <div><div style="font-family:var(--ps-font-mono);font-size:10px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-ms-green-500);margin-bottom:6px;" data-i18n="moment.s2Label">.</div><div style="font-family:var(--ps-font-mono);font-size:19px;color:var(--ps-color-ink);" data-i18n="moment.s2">.</div></div>
      <div><div style="font-family:var(--ps-font-mono);font-size:10px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-ms-red-500);margin-bottom:6px;" data-i18n="moment.s3Label">.</div><div style="font-family:var(--ps-font-mono);font-size:19px;color:var(--ps-color-ink);" data-i18n="moment.s3">.</div></div>
    </div>
  </div>
</section>''')
# 5 divider parte 2
S.append(divider('p2','blue','02'))
# 6 deliverables 3-card
S.append(f'''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-blue-500);" data-i18n="deliver.eyebrow">.</div>
  <h2 class="title title--medium" data-i18n="deliver.title">.</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px;margin-top:36px;" class="stagger">
    {card('deliver',1,'blue')}
    {card('deliver',2,'green')}
    {card('deliver',3,'yellow')}
  </div>
</section>''')
# 7 divider parte 3
S.append(divider('p3','green','03'))
# 8 roadmap 3 phases
ph = lambda n,accent: f'''<div style="display:grid;grid-template-columns:170px 1fr;gap:22px;padding:20px 0;border-bottom:1px solid var(--ps-color-rule);align-items:start;">
      <div style="font-family:var(--ps-font-mono);font-size:12px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:{ACC[accent]};padding-top:3px;" data-i18n="program.ph{n}Label">.</div>
      <div><h3 style="font-size:20px;font-weight:600;color:var(--ps-color-ink);margin-bottom:6px;" data-i18n="program.ph{n}Title">.</h3>
      <p style="font-size:14px;line-height:1.55;color:var(--ps-color-ink-2);max-width:900px;" data-i18n="program.ph{n}Body">.</p></div>
    </div>'''
S.append(f'''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-green-500);" data-i18n="program.eyebrow">.</div>
  <h2 class="title title--medium" data-i18n="program.title">.</h2>
  <div style="margin-top:28px;" class="stagger">
    {ph(1,'blue')}
    {ph(2,'red')}
    {ph(3,'green')}
  </div>
</section>''')
# 9 redemption big number
S.append('''<section class="slide slide--light" style="--accent: var(--ps-color-ms-green-500);">
  <div class="eyebrow" data-i18n="redeem.eyebrow">.</div>
  <div style="display:flex;flex-direction:column;gap:22px;margin-top:24px;">
    <div style="font-family: var(--ps-font-mono); font-size: 150px; font-weight: 600; line-height: 0.95; color: var(--ps-color-ms-green-500); letter-spacing: -0.02em;" data-i18n="redeem.hero">US$ 495k</div>
    <h2 class="title title--medium" data-i18n="redeem.title" style="max-width:1100px;">.</h2>
    <p class="body-large" data-i18n="redeem.body" style="max-width:1050px;">.</p>
    <div style="display:flex;gap:14px;align-items:baseline;padding-top:14px;border-top:1px solid var(--ps-color-rule);">
      <span style="font-family:var(--ps-font-mono);font-size:10px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-ink-3);" data-i18n="redeem.kLabel">.</span>
      <span style="font-size:15px;color:var(--ps-color-ink-2);" data-i18n="redeem.kValue">.</span>
    </div>
  </div>
</section>''')
# 10 + 11 levers, two slides of compact rows with impact band on the label
lv = lambda n,accent: f'''<div style="display:grid;grid-template-columns:230px 1fr;gap:22px;padding:14px 0;border-bottom:1px solid var(--ps-color-rule);align-items:start;">
      <div style="padding-top:2px;"><div style="font-family:var(--ps-font-mono);font-size:12px;font-weight:700;letter-spacing:0.06em;color:{ACC[accent]};" data-i18n="levers.r{n}Label">.</div></div>
      <div><h3 style="font-size:17px;font-weight:600;color:var(--ps-color-ink);margin-bottom:4px;" data-i18n="levers.r{n}Title">.</h3>
      <p style="font-size:13px;line-height:1.48;color:var(--ps-color-ink-2);max-width:1000px;" data-i18n="levers.r{n}Body">.</p></div>
    </div>'''
S.append(f'''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-yellow-500);" data-i18n="levers.eyebrow">.</div>
  <h2 class="title title--medium" data-i18n="levers.title">.</h2>
  <p style="font-size:14px;color:var(--ps-color-ink-3);margin-top:6px;" data-i18n="levers.lead1">.</p>
  <div style="margin-top:16px;" class="stagger">
    {lv(1,'red')}
    {lv(2,'blue')}
    {lv(3,'green')}
    {lv(4,'yellow')}
  </div>
</section>''')
S.append(f'''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-yellow-500);" data-i18n="levers.eyebrow2">.</div>
  <h2 class="title title--medium" data-i18n="levers.title2">.</h2>
  <p style="font-size:14px;color:var(--ps-color-ink-3);margin-top:6px;" data-i18n="levers.lead2">.</p>
  <div style="margin-top:16px;" class="stagger">
    {lv(5,'blue')}
    {lv(6,'green')}
    {lv(7,'red')}
  </div>
</section>''')
# 11 divider parte 4
S.append(divider('p4','yellow','04'))
# 12 two tracks 2-col
S.append('''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-yellow-500);" data-i18n="tracks.eyebrow">.</div>
  <h2 class="title title--medium" data-i18n="tracks.title">.</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 34px;" class="stagger">
    <div style="padding: 28px; background: var(--ps-color-bg); border-left: 3px solid var(--ps-color-ms-blue-500); border-radius: 4px;">
      <div style="font-family: var(--ps-font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ps-color-ms-blue-500); margin-bottom: 14px;" data-i18n="tracks.leftLabel">.</div>
      <h3 style="font-size: 22px; font-weight: 600; line-height: 1.25; color: var(--ps-color-ink); margin-bottom: 12px;" data-i18n="tracks.leftTitle">.</h3>
      <p style="font-size: 14.5px; line-height: 1.6; color: var(--ps-color-ink-2);" data-i18n="tracks.leftBody">.</p>
    </div>
    <div style="padding: 28px; background: var(--ps-color-bg); border-left: 3px solid var(--ps-color-ms-green-500); border-radius: 4px;">
      <div style="font-family: var(--ps-font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ps-color-ms-green-500); margin-bottom: 14px;" data-i18n="tracks.rightLabel">.</div>
      <h3 style="font-size: 22px; font-weight: 600; line-height: 1.25; color: var(--ps-color-ink); margin-bottom: 12px;" data-i18n="tracks.rightTitle">.</h3>
      <p style="font-size: 14.5px; line-height: 1.6; color: var(--ps-color-ink-2);" data-i18n="tracks.rightBody">.</p>
    </div>
  </div>
</section>''')
# 13 who 3-card
S.append(f'''<section class="slide slide--light">
  <div class="eyebrow" style="--accent: var(--ps-color-ms-blue-500);" data-i18n="who.eyebrow">.</div>
  <h2 class="title title--medium" data-i18n="who.title">.</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px;margin-top:36px;" class="stagger">
    {card('who',1,'yellow')}
    {card('who',2,'blue')}
    {card('who',3,'green')}
  </div>
</section>''')
# 14 closing dark
S.append('''<section class="slide slide--dark" style="--accent: var(--ps-color-ms-blue-500);">
  <div class="eyebrow" data-i18n="end.eyebrow">.</div>
  <h1 class="section-title" style="font-size:64px;" data-i18n="end.title">.</h1>
  <p class="subtitle" data-i18n="end.sub" style="max-width:980px;">.</p>
  <div style="display:grid;grid-template-columns:auto auto;gap:60px;margin-top:48px;align-items:start;justify-content:start;">
    <div>
      <div style="font-family:var(--ps-font-mono);font-size:10px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-dark-ink-3);margin-bottom:8px;" data-i18n="end.contactLabel">.</div>
      <div style="font-size:18px;color:var(--ps-color-dark-ink);">Frontier Cockpit Team</div>
      <div style="font-family:var(--ps-font-mono);font-size:14px;color:var(--ps-color-ms-blue-500);margin-top:4px;">frontier-cockpit@example.com</div>
      <div style="font-size:13px;color:var(--ps-color-dark-ink-2);margin-top:4px;">Software Global Black Belt</div>
    </div>
    <div>
      <div style="font-family:var(--ps-font-mono);font-size:10px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:var(--ps-color-dark-ink-3);margin-bottom:8px;" data-i18n="end.nextLabel">.</div>
      <div style="font-size:18px;color:var(--ps-color-dark-ink);max-width:520px;" data-i18n="end.next">.</div>
    </div>
  </div>
</section>''')

new_sections = "".join(S)

# splice: replace from first <section to last </section>
i0 = h.index('<section')
i1 = h.rindex('</section>') + len('</section>')
h2 = h[:i0] + new_sections + h[i1:]

# replace I18N object
def grab_span(s, name):
    i = s.index(f'const {name} = ') + len(f'const {name} = ')
    depth=0; j=i
    while True:
        c=s[j]
        if c=='{': depth+=1
        elif c=='}':
            depth-=1
            if depth==0: break
        j+=1
    return i, j+1
a,b = grab_span(h2, 'I18N')
h2 = h2[:a] + json.dumps(I18N, ensure_ascii=False, indent=1) + h2[b:]

# title + meta
h2 = re.sub(r'<title>[^<]*</title>', '<title>BTG Pactual, o programa de seis meses · GitHub Copilot UBB</title>', h2)

out=OUT_NAME
open(out,'w',encoding='utf-8').write(h2)
print('written', out, len(h2))
