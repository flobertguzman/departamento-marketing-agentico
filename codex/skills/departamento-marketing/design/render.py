#!/usr/bin/env python3
"""Convierte un HTML en PNG usando Chrome/Chromium/Edge/Brave sin pantalla (headless).

Uso:  render.py pieza.html salida.png --width 1080 --height 1350
Sin dependencias: solo librería estándar de Python 3 y un navegador instalado.
"""
import argparse
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "microsoft-edge", "brave-browser"]


def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for n in NAMES:
        p = shutil.which(n)
        if p:
            return p
    sys.exit("No encontré Chrome, Chromium, Edge ni Brave. Instala uno o define CHROME_PATH=/ruta/al/navegador")


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def _shot(browser, html, out, w, h):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            browser, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--allow-file-access-from-files",
            f"--user-data-dir={profile}", f"--window-size={w},{h}",
            "--virtual-time-budget=5000", f"--screenshot={out}", Path(html).resolve().as_uri(),
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90, check=False)


def render(html, out, width, height):
    browser = find_browser()
    out = str(Path(out).resolve())
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    if Path(out).exists():
        Path(out).unlink()
    _shot(browser, html, out, width, height)
    size = png_size(out) if Path(out).exists() else None
    if size and size != (width, height):
        # Algunas versiones de Chrome restan alto/ancho de interfaz: compensa y repite una vez.
        dw, dh = width - size[0], height - size[1]
        Path(out).unlink()
        _shot(browser, html, out, width + dw, height + dh)
        size = png_size(out) if Path(out).exists() else None
    if not size:
        sys.exit(f"No se generó la imagen: {out}")
    if size != (width, height):
        print(f"AVISO: tamaño {size[0]}x{size[1]} (esperado {width}x{height})", file=sys.stderr)
    return out, size


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    a = ap.parse_args()
    path, (w, h) = render(a.html, a.out, a.width, a.height)
    print(f"OK {path} ({w}x{h})")
