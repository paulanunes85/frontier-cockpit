#!/usr/bin/env python3
"""Mapeia um video: probe, contact sheets, transicoes, frame com grade.

Uso:
  python map_video.py SRC [--fps-frac 5] [--out map_out]     # contact sheets
  python map_video.py SRC --transitions [--thresh 3.0]       # detector de cortes
  python map_video.py SRC --grid 48.4 [--scaled-from FILE]   # frame com grade 100px
"""
import argparse, glob, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw


def sh(cmd):
    subprocess.run(cmd, shell=True, check=True)


def probe(src):
    r = subprocess.run(
        f"ffprobe -v error -show_entries format=duration,size "
        f"-show_entries stream=codec_type,width,height,r_frame_rate -of default=nw=1 \"{src}\"",
        shell=True, capture_output=True, text=True)
    print(r.stdout)
    has_audio = 'codec_type=audio' in r.stdout
    print(f"AUDIO: {'sim' if has_audio else 'NAO (Quick Cut descartado, gotchas §10)'}")
    return r.stdout


def sheets(src, frac, out):
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    sh(f"ffmpeg -y -v error -i \"{src}\" -vf fps=1/{frac},scale=560:-1 {out}/f%03d.png")
    files = sorted(glob.glob(f"{out}/f*.png"))
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size
    for g in range(0, len(ims), 12):
        chunk = ims[g:g+12]
        rows = (len(chunk)+3)//4
        s = Image.new('RGB', (w*4, h*rows), 'black')
        for i, im in enumerate(chunk):
            d = ImageDraw.Draw(im)
            d.text((6, 4), f"t={(g+i)*frac}s", fill='red')
            s.paste(im, ((i % 4)*w, (i//4)*h))
        s.save(f"{out}/grid{g//12}.png")
    print(f"{len(ims)} frames (1/{frac}s) -> {out}/grid*.png - VEJA TODAS as grades.")


def transitions(src, thresh):
    tmp = '_scan_tmp'
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    sh(f"ffmpeg -y -v error -i \"{src}\" -vf fps=2,scale=160:-1 {tmp}/s%05d.png")
    prev = None
    for i, f in enumerate(sorted(glob.glob(f"{tmp}/s*.png"))):
        a = np.asarray(Image.open(f).convert('L'), dtype=np.int16)
        if prev is not None:
            d = (np.abs(a - prev) > 25).mean()*100
            if d > thresh:
                print(f"t={i/2:7.1f}s  diff={d:5.1f}%")
        prev = a
    shutil.rmtree(tmp)
    print("(diff alto = troca de tela; rajada = scroll; silencio = tela parada -> bom p/ corte)")


def grid_frame(src, t):
    sh(f"ffmpeg -y -v error -ss {t} -i \"{src}\" -frames:v 1 _grid.png")
    im = Image.open('_grid.png'); d = ImageDraw.Draw(im)
    W, H = im.size
    for x in range(0, W, 100):
        d.line([x, 0, x, H], fill='#FF00FF' if x % 500 == 0 else '#FFA0FF', width=2 if x % 500 == 0 else 1)
        d.text((x+4, 4), str(x), fill='#FF00FF')
    for y in range(0, H, 100):
        d.line([0, y, W, y], fill='#FF00FF' if y % 500 == 0 else '#FFA0FF', width=2 if y % 500 == 0 else 1)
        d.text((4, y+4), str(y), fill='#FF00FF')
    out = f"grid_{t}.png"; im.save(out)
    print(f"-> {out} (coordenadas no espaco {W}x{H})")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('src')
    p.add_argument('--fps-frac', type=int, default=5)
    p.add_argument('--out', default='map_out')
    p.add_argument('--transitions', action='store_true')
    p.add_argument('--thresh', type=float, default=3.0)
    p.add_argument('--grid', type=float, default=None)
    a = p.parse_args()
    probe(a.src)
    if a.transitions:
        transitions(a.src, a.thresh)
    elif a.grid is not None:
        grid_frame(a.src, a.grid)
    else:
        sheets(a.src, a.fps_frac, a.out)
