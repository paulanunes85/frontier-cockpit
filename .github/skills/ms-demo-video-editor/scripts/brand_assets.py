#!/usr/bin/env python3
"""Assets ms-identity para video: logo oficial, capa, encerramento, moldura, lower-thirds.

Uso:
  pip install cairosvg --break-system-packages -q
  python brand_assets.py --kicker "PROJ // CONTEXTO" --title "Titulo" \
      [--title2 "linha 2"] --subtitle "stack · contexto" [--subtitle2 "..."] \
      --end-line1 "Frase." --end-line2 "Fechamento." \
      --lt m1 BLU "01 · SECAO" "Fato concreto · numero" \
      --lt m2 GRN "02 · SECAO" "Outro fato"

Cores de accent: RED GRN BLU YEL. Saidas: cover.png endcard.png framebg.png lt_*.png
"""
import argparse, io, os, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
COLORS = {'RED': '#F25022', 'GRN': '#7FBA00', 'BLU': '#00A4EF', 'YEL': '#FFB900'}
MS = [COLORS[c] for c in ('RED', 'GRN', 'BLU', 'YEL')]
INK, PAPER = '#1A1A1A', '#FFFFFF'
BYLINE = 'PAULA SILVA | SOFTWARE GLOBAL BLACK BELT'

# Logo </.> oficial - paths do ms-identity/references/identity.md. NAO alterar geometria.
LOGO_SVG = '''<svg viewBox="0 0 1914 1062" xmlns="http://www.w3.org/2000/svg">
<path fill="#F25022" d="M532 131 L36 462 L13 497 L13 560 L23 582 L48 604 L521 923 L539 926 L539 699 L547 680 L314 530 L527 395 L551 371 L558 347 L558 155 L547 135 Z"/>
<path fill="#7FBA00" d="M551 681 L542 693 L540 700 L540 917 L546 930 L558 940 L571 943 L778 943 L788 941 L798 935 L809 910 L809 702 L807 694 L799 682 L784 674 L566 674 Z"/>
<path fill="#FFB900" d="M1390 16 L1208 13 L1184 23 L1171 38 L768 1009 L768 1026 L778 1038 L957 1042 L975 1037 L995 1017 L1346 179 L1349 145 L1367 129 L1401 47 L1402 31 Z"/>
<path fill="#00A4EF" d="M1369 131 L1350 149 L1349 355 L1354 369 L1385 399 L1592 528 L1373 667 L1354 688 L1349 703 L1349 907 L1361 924 L1377 926 L1871 595 L1893 563 L1894 501 L1885 477 L1863 456 L1398 142 Z"/>
</svg>'''

FONTS = {
    'Inter.ttf': 'https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf',
    'JBMono.ttf': 'https://github.com/google/fonts/raw/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf',
}


def ensure_fonts():
    for name, url in FONTS.items():
        if not os.path.exists(name):
            urllib.request.urlretrieve(url, name)


def ensure_logo():
    if not os.path.exists('logo.png'):
        import cairosvg
        cairosvg.svg2png(bytestring=LOGO_SVG.encode(), write_to='logo.png', output_width=1200)
    return Image.open('logo.png')


def F(p, s, *ax):
    f = ImageFont.truetype(p, s); f.set_variation_by_axes(list(ax)); return f


ixb = lambda s: F('Inter.ttf', s, 28, 800)
isb = lambda s: F('Inter.ttf', s, 20, 600)
mono = lambda s: F('JBMono.ttf', s, 600)


def grad_bar(d, x, y, w, h):
    hx = lambda c: tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
    st = [hx(c) for c in MS]
    for i in range(w):
        p = i/(w-1)*3; a = st[min(int(p), 2)]; b = st[min(int(p)+1, 3)]; f = p-int(p)
        d.line([x+i, y, x+i, y+h], fill=tuple(round(a[j]+(b[j]-a[j])*f) for j in range(3)))


def dark_base():
    im = Image.new('RGB', (W, H), '#141519')
    v = Image.new('L', (W, H), 0)
    ImageDraw.Draw(v).ellipse([-500, -420, W+500, H+420], fill=26)
    return Image.composite(Image.new('RGB', (W, H), '#1B1D23'), im,
                           v.filter(ImageFilter.GaussianBlur(180)))


def make_cover(logo, a):
    im = dark_base(); d = ImageDraw.Draw(im)
    lg = logo.resize((300, round(300*logo.height/logo.width))); im.paste(lg, (160, 150), lg)
    d.text((160, 388), a.kicker, font=mono(34), fill=COLORS[a.accent])
    size = 150 if not a.title2 else 118
    d.text((160, 452), a.title, font=ixb(size), fill=PAPER)
    y = 452 + size + 16
    if a.title2:
        d.text((160, y - 16), a.title2, font=ixb(size), fill=PAPER); y += size + 8
    grad_bar(d, 166, y, 560, 10); y += 48
    if a.subtitle:  d.text((160, y), a.subtitle,  font=isb(40), fill='#C9CCD4'); y += 60
    if a.subtitle2: d.text((160, y), a.subtitle2, font=isb(34), fill='#8A8F99')
    d.text((160, 950), BYLINE, font=mono(26), fill='#8A8F99')
    im.save('cover.png')


def make_end(logo, a):
    im = dark_base(); d = ImageDraw.Draw(im)
    lg = logo.resize((220, round(220*logo.height/logo.width))); im.paste(lg, ((W-220)//2, 240), lg)
    lines = [l for l in (a.end_line1, a.end_line2) if l]
    for i, t in enumerate(lines):
        w_ = d.textlength(t, font=ixb(76)); d.text(((W-w_)//2, 470+i*96), t, font=ixb(76), fill=PAPER)
    grad_bar(d, (W-460)//2, 680, 460, 8)
    w_ = d.textlength(BYLINE, font=mono(26)); d.text(((W-w_)//2, 760), BYLINE, font=mono(26), fill='#C9CCD4')
    c = 'Microsoft  ·  GitHub'
    w_ = d.textlength(c, font=isb(30)); d.text(((W-w_)//2, 816), c, font=isb(30), fill='#8A8F99')
    im.save('endcard.png')


def make_framebg(logo):
    VX, VY, VW, VH = 78, 46, 1764, 952
    bg = Image.new('RGB', (W, H), '#F7F7F5')
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([VX-2, VY+14, VX+VW+2, VY+VH+22], 18, fill=(20, 22, 28, 90))
    bg = Image.alpha_composite(bg.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(22))).convert('RGB')
    d = ImageDraw.Draw(bg)
    d.rectangle([VX-1, VY-1, VX+VW+1, VY+VH+1], fill='#FFFFFF')
    seg = W/4
    for i, c in enumerate(MS):
        d.rectangle([i*seg, H-8, (i+1)*seg, H], fill=c)
    d.text((VX, H-52), BYLINE, font=mono(20), fill='#737373')
    lg = logo.resize((64, round(64*logo.height/logo.width)))
    bg.paste(lg, (W-VX-64, H-58), lg)
    bg.save('framebg.png')


def make_lt(key, accent, kick, title):
    acc = COLORS.get(accent, accent)
    fk, ft = mono(24), isb(34)
    tmp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    w_ = int(max(tmp.textlength(kick, font=fk), tmp.textlength(title, font=ft))) + 76
    h_ = 104
    im = Image.new('RGBA', (w_+20, h_+20), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([10, 14, 10+w_, 14+h_], 14, fill=(20, 22, 28, 110))
    im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), im)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 10+w_, 10+h_], 14, fill=(255, 255, 255, 242))
    d.rounded_rectangle([10, 10, 18, 10+h_], 14, fill=acc); d.rectangle([14, 10, 18, 10+h_], fill=acc)
    d.text((40, 24), kick, font=fk, fill=acc)
    d.text((40, 56), title, font=ft, fill=INK)
    im.save(f'lt_{key}.png')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--kicker', default='SIFAP // DEMO')
    p.add_argument('--title', default='Demo')
    p.add_argument('--title2', default='')
    p.add_argument('--subtitle', default='')
    p.add_argument('--subtitle2', default='')
    p.add_argument('--accent', default='BLU', choices=list(COLORS))
    p.add_argument('--end-line1', default='')
    p.add_argument('--end-line2', default='')
    p.add_argument('--lt', nargs=4, action='append', metavar=('KEY', 'ACCENT', 'KICKER', 'TITLE'), default=[])
    p.add_argument('--no-cards', action='store_true', help='so lower-thirds')
    a = p.parse_args()
    ensure_fonts(); logo = ensure_logo()
    if not a.no_cards:
        make_cover(logo, a); make_end(logo, a); make_framebg(logo)
        print('cover.png endcard.png framebg.png ok')
    for key, acc, kick, title in a.lt:
        make_lt(key, acc, kick, title); print(f'lt_{key}.png ok')
