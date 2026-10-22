#!/usr/bin/env python3
"""Genera piezas gráficas (PNG) de marca desde plantillas HTML + un archivo de marca.

Una pieza:
  make_piece.py --brand brand.json --format post --layout bold \\
      --headline "Pan de masa madre" --subhead "Horneado esta mañana" --cta "Pide ahora" --out out/post.png

Varias piezas (lote):
  make_piece.py --brand brand.json --spec piezas.json --outdir out/

Formatos: post (1080x1350) · square (1080x1080) · story (1080x1920) · banner (1200x628) · landscape (1920x1080)
Layouts:  bold (texto sobre color de marca) · photo (imagen a sangre; usa --image) · center (anuncio centrado)
Solo usa la librería estándar de Python 3 y un navegador (ver render.py).
"""
import argparse
import html
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render  # noqa: E402

HERE = Path(__file__).resolve().parent
FORMATS = {
    "post": (1080, 1350),
    "square": (1080, 1080),
    "story": (1080, 1920),
    "banner": (1200, 628),
    "landscape": (1920, 1080),
}
LAYOUTS = ("bold", "photo", "center")
DEFAULT_BRAND = {
    "name": "Marca",
    "bg": "#101820",
    "fg": "#FFFFFF",
    "accent": "#F2A900",
    "accent_fg": "#101820",
    "font_heading": "'Helvetica Neue', Arial, sans-serif",
    "font_body": "'Helvetica Neue', Arial, sans-serif",
    "font_css_url": "",
    "logo": "",
    "lang": "es",
}


def _lum(hexcolor):
    m = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", hexcolor.strip())
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    chan = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        chan.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2]


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    if la is None or lb is None:
        return None
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(brand, layout):
    pairs = [("texto sobre fondo", brand["fg"], brand["bg"]), ("texto del botón", brand["accent_fg"], brand["accent"])]
    if layout != "photo":
        pairs.append(("kicker (acento) sobre fondo", brand["accent"], brand["bg"]))
    for label, a, b in pairs:
        c = contrast(a, b)
        if c is not None and c < 4.5:
            print(f"AVISO contraste: {label} = {c:.2f}:1 (mínimo AA 4.5:1). Ajusta la paleta.", file=sys.stderr)


def esc(text):
    return html.escape(text or "", quote=True).replace("\n", "<br>")


def fit_factor(headline, w, h):
    n = len((headline or "").replace("\n", " "))
    f = 1.0 if n <= 24 else 0.85 if n <= 40 else 0.72 if n <= 60 else 0.6
    if w > h * 1.5:  # formatos apaisados tienen menos alto útil
        f *= 0.9
    return f


def build_html(brand, piece, fmt, layout):
    w, h = FORMATS[fmt]
    tpl = (HERE / "templates" / "piece.html").read_text(encoding="utf-8")
    css = (HERE / "templates" / "base.css").read_text(encoding="utf-8")

    logo = brand.get("logo", "")
    if logo and Path(logo).expanduser().exists():
        logo_html = f'<img class="logo-img" alt="{esc(brand["name"])}" src="{Path(logo).expanduser().resolve().as_uri()}">'
    else:
        logo_html = f'<span class="logo-text">{esc(brand["name"])}</span>'

    image = piece.get("image", "")
    has_image = ""
    image_css = "none"
    if image:
        p = Path(image).expanduser()
        if p.exists():
            image_css = f'url("{p.resolve().as_uri()}")'
        elif image.startswith(("http://", "https://")):
            image_css = f'url("{image}")'
        else:
            sys.exit(f"No existe la imagen: {image}")
        has_image = "has-image"

    cta = piece.get("cta", "")
    font_link = f'<link rel="stylesheet" href="{brand["font_css_url"]}">' if brand.get("font_css_url") else ""
    values = {
        "lang": brand["lang"], "font_link": font_link, "bg": brand["bg"], "fg": brand["fg"],
        "accent": brand["accent"], "accent_fg": brand["accent_fg"],
        "font_heading": brand["font_heading"], "font_body": brand["font_body"],
        "u": f"{min(w, h) / 100:.3f}", "fit": f"{fit_factor(piece.get('headline'), w, h):.2f}",
        "image_css": image_css, "w": str(w), "h": str(h), "layout": layout, "has_image": has_image,
        "logo_html": logo_html, "kicker": esc(piece.get("kicker")), "headline": esc(piece.get("headline")),
        "subhead": esc(piece.get("subhead")), "cta_html": f'<span class="cta">{esc(cta)}</span>' if cta else "",
    }
    out = tpl.replace("{{base_css}}", css)
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    return out, w, h


def make(brand, piece, out_path):
    fmt = piece.get("format", "post")
    layout = piece.get("layout", "bold")
    if fmt not in FORMATS:
        sys.exit(f"Formato inválido '{fmt}'. Opciones: {', '.join(FORMATS)}")
    if layout not in LAYOUTS:
        sys.exit(f"Layout inválido '{layout}'. Opciones: {', '.join(LAYOUTS)}")
    if layout == "photo" and not piece.get("image"):
        print("AVISO: layout 'photo' sin --image; se usa un degradado de la marca.", file=sys.stderr)
    check_contrast(brand, layout)
    doc, w, h = build_html(brand, piece, fmt, layout)
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "piece.html"
        src.write_text(doc, encoding="utf-8")
        path, size = render(src, out_path, w, h)
    print(f"OK {path} ({size[0]}x{size[1]})")
    return path


def load_brand(path):
    brand = dict(DEFAULT_BRAND)
    if path:
        brand.update(json.loads(Path(path).read_text(encoding="utf-8")))
    return brand


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brand", help="brand.json con colores, tipografías y logo")
    ap.add_argument("--spec", help="JSON con una lista de piezas (modo lote)")
    ap.add_argument("--outdir", default="out", help="carpeta de salida en modo lote")
    ap.add_argument("--out", help="archivo PNG de salida (una pieza)")
    ap.add_argument("--format", default="post", choices=list(FORMATS))
    ap.add_argument("--layout", default="bold", choices=list(LAYOUTS))
    ap.add_argument("--headline", default="")
    ap.add_argument("--subhead", default="")
    ap.add_argument("--kicker", default="")
    ap.add_argument("--cta", default="")
    ap.add_argument("--image", default="")
    a = ap.parse_args()
    brand = load_brand(a.brand)

    if a.spec:
        pieces = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        outdir = Path(a.outdir)
        for i, piece in enumerate(pieces, 1):
            name = piece.get("out") or f"{i:02d}_{piece.get('format', 'post')}_{piece.get('layout', 'bold')}.png"
            make(brand, piece, outdir / name)
        return
    if not a.out or not a.headline:
        ap.error("una pieza necesita --out y --headline (o usa --spec)")
    make(brand, {k: getattr(a, k) for k in ("format", "layout", "headline", "subhead", "kicker", "cta", "image")}, a.out)


if __name__ == "__main__":
    main()
