#!/usr/bin/env python3
"""Monta o filme a partir de um plan.json. Ver references/plan-example.json.

Modos:
  beats      - fatias emolduradas + LT por beat, unidas por xfade
  continuous - video inteiro na moldura + lower-thirds cronometrados

Sempre: capa/encerramento animados (-framerate 30!), offsets de xfade por
duracao MEDIDA, re-encode final unico (QuickTime-safe), QA sheet + decode test.
"""
import json, subprocess, sys, os, glob, shutil


def sh(cmd, show=False):
    if show: print('>>', cmd[:150])
    subprocess.run(cmd, shell=True, check=True)


def dur_of(f):
    r = subprocess.run(f"ffprobe -v error -show_entries format=duration -of csv=p=0 \"{f}\"",
                       shell=True, capture_output=True, text=True)
    return float(r.stdout.strip())


FIT = {  # rect da moldura: 1764x952 em (78,46)
    'tall': 'scale=-2:952:flags=lanczos,pad=1764:952:(1764-iw)/2:0:color=white',
    'wide': 'scale=1764:-2:flags=lanczos,pad=1764:952:0:(952-ih)/2:color=white',
}


def fx_segment(b, out):
    """Extrai a 1440p da fonte ORIGINAL e aplica drawbox + zoompan (gotchas §5-§7).
    boxes em coords 1080 (x,y,w,h,enable) - escala 4/3 p/ 1440. zoom: cx,cy (1080), z."""
    hi = '_hi_tmp.mp4'
    crop = b.get('src_crop', '')          # ex.: "crop=3466:1950:0:120," p/ tirar menubar
    sh(f"ffmpeg -y -v error -ss {b['ss']} -to {b['ss']+b['dur']} -i \"{b['fx_src']}\" "
       f"-vf \"{crop}scale=2560:1440,fps=30\" -c:v libx264 -preset veryfast -crf 15 -an {hi}")
    S = 4/3; vf = []
    for (x, y, w, h, en) in b.get('boxes', []):
        x, y, w, h = [round(v*S) for v in (x, y, w, h)]
        vf.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0xFFB900@0.15:t=fill:enable='{en}'")
        vf.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0xFFB900@0.95:t=7:enable='{en}'")
    z = b.get('zoom')
    if z:
        N = int(b['dur']*30); cx, cy = round(z['cx']*S), round(z['cy']*S)
        vf.append(f"zoompan=z='1+({z['z']}-1)*on/{N}'"
                  f":x='max(0,min(iw-iw/zoom,{cx}-iw/zoom/2))'"
                  f":y='max(0,min(ih-ih/zoom,{cy}-ih/zoom/2))':d=1:fps=30:s=1920x1080")
    else:
        vf.append('scale=1920:1080:flags=lanczos')
    vf.append('format=yuv420p')
    sh(f"ffmpeg -y -v error -i {hi} -vf \"{','.join(vf)}\" -c:v libx264 -preset veryfast -crf 16 -an {out}")
    os.remove(hi)


def beat(b, framebg, out):
    """Compoe um beat: fonte (ou fx pre-renderizado) na moldura + LT com fade."""
    if b.get('fx_src'):
        inner = f"_fx_{b['key']}.mp4"; fx_segment(b, inner); ss = 0
    else:
        inner, ss = b['src'], b.get('ss', 0)
    dur = b['dur']; fit = FIT[b.get('fit', 'tall')]
    ltout = max(dur-1.3, 1.0)
    lt_in = f"-loop 1 -t {dur} -i \"{b['lt']}\"" if b.get('lt') else ''
    fc = [f"[1:v]{fit}[v]", "[0:v][v]overlay=78:46[base]"]
    if b.get('lt'):
        fc.append(f"[2:v]format=rgba,fade=t=in:st=0.5:d=0.35:alpha=1,"
                  f"fade=t=out:st={ltout:.2f}:d=0.5:alpha=1[lt]")
        fc.append("[base][lt]overlay=110:848,fps=30,format=yuv420p[out]")
    else:
        fc.append("[base]fps=30,format=yuv420p[out]")
    sh(f"ffmpeg -y -v error -framerate 30 -loop 1 -t {dur} -i {framebg} "
       f"-ss {ss} -t {dur} -i \"{inner}\" {lt_in} "
       f"-filter_complex \"{';'.join(fc)}\" -map '[out]' -t {dur} "
       f"-c:v libx264 -preset veryfast -crf 16 -an {out}")


def continuous(c, framebg, out):
    dur = c['dur']; fit = FIT[c.get('fit', 'tall')]
    fc = [f"[1:v]{fit}[v]", "[0:v][v]overlay=78:46[b0]"]
    prev = 'b0'
    for i, (png, s, e) in enumerate(c['lts']):
        idx = i+2
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st={s}:d=0.35:alpha=1,"
                  f"fade=t=out:st={e}:d=0.45:alpha=1[lt{i}]")
        fc.append(f"[{prev}][lt{i}]overlay=110:848:enable='between(t,{s-0.1},{e+0.6})'[b{i+1}]")
        prev = f'b{i+1}'
    fc.append(f"[{prev}]fps=30,format=yuv420p[out]")
    lt_inputs = ' '.join(f"-loop 1 -t {dur} -i \"{p}\"" for p, _, _ in c['lts'])
    sh(f"ffmpeg -y -v error -framerate 30 -loop 1 -t {dur} -i {framebg} -i \"{c['src']}\" {lt_inputs} "
       f"-filter_complex \"{';'.join(fc)}\" -map '[out]' -t {dur} "
       f"-c:v libx264 -preset veryfast -crf 16 -an {out}")


def card(png, dur, out):
    n = int(dur*30)
    sh(f"ffmpeg -y -v error -framerate 30 -loop 1 -t {dur} -i \"{png}\" -vf "
       f"\"zoompan=z='1+0.05*on/{n}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps=30:s=1920x1080,"
       f"format=yuv420p\" -c:v libx264 -preset veryfast -crf 16 {out}")


def assemble(parts, out, fd=0.4):
    durs = [dur_of(p) for p in parts]                  # MEDIDAS, nao nominais (gotchas §4)
    fc, prev, cum = [], '[0:v]', durs[0]
    for i in range(1, len(parts)):
        fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={fd}:offset={cum-fd:.4f}[v{i}]")
        prev = f'[v{i}]'; cum = cum - fd + durs[i]
    fc.append(f"{prev}fade=t=in:st=0:d=0.6,fade=t=out:st={cum-0.8:.2f}:d=0.8,format=yuv420p[out]")
    open('_fc.txt', 'w').write(';'.join(fc))
    inputs = ' '.join(f"-i \"{p}\"" for p in parts)
    sh(f"ffmpeg -y -v error {inputs} -filter_complex_script _fc.txt -map '[out]' "
       f"-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart \"{out}\"", show=True)
    print(f'total: {cum:.2f}s')


def qa(final):
    shutil.rmtree('_qa', ignore_errors=True); os.makedirs('_qa')
    d = dur_of(final); step = max(round(d/14, 1), 2)
    sh(f"ffmpeg -y -v error -i \"{final}\" -vf fps=1/{step},scale=560:-1 _qa/q%02d.png")
    from PIL import Image, ImageDraw
    files = sorted(glob.glob('_qa/q*.png')); ims = []
    for i, f in enumerate(files):
        im = Image.open(f); ImageDraw.Draw(im).text((6, 4), f"t={i*step:.0f}s", fill='red'); ims.append(im)
    w, h = ims[0].size; cols = 4; rows = (len(ims)+3)//4
    s = Image.new('RGB', (w*cols, h*rows), '#111')
    for i, im in enumerate(ims):
        s.paste(im, ((i % cols)*w, (i//cols)*h))
    s.save('_qa/sheet.png')
    sh(f"ffmpeg -v error -i \"{final}\" -f null -")
    print('decode OK · VEJA _qa/sheet.png antes de entregar (gotchas §11)')


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1]))
    fb = plan.get('framebg', 'framebg.png')
    parts = []
    if plan.get('cover'):
        card(plan['cover']['png'], plan['cover'].get('dur', 4.5), '_p_cover.mp4'); parts.append('_p_cover.mp4')
    if plan.get('mode', 'beats') == 'continuous':
        continuous(plan['continuous'], fb, '_p_main.mp4'); parts.append('_p_main.mp4')
    else:
        for b in plan['beats']:
            o = f"_p_{b['key']}.mp4"; beat(b, fb, o); parts.append(o)
    if plan.get('end'):
        card(plan['end']['png'], plan['end'].get('dur', 5.0), '_p_end.mp4'); parts.append('_p_end.mp4')
    assemble(parts, plan['out'], plan.get('fade', 0.4))
    qa(plan['out'])
