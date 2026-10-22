# Kit de diseño

Genera piezas gráficas de marca (PNG) desde plantillas HTML. Sin dependencias: Python 3 + un navegador (Chrome, Chromium, Edge o Brave).

```bash
# 1. Copia y edita la marca (colores, tipografías, logo)
cp brand.example.json brand.json

# 2. Una pieza
python3 make_piece.py --brand brand.json --format post --layout bold \
  --headline "Pan de masa madre" --subhead "Horneado esta mañana" --cta "Pide ahora" --out out/post.png

# 3. Un lote (ver pieces.example.json)
python3 make_piece.py --brand brand.json --spec pieces.json --outdir out/
```

| Formato | Tamaño | | Layout | Uso |
|---|---|---|---|---|
| `post` | 1080×1350 | | `bold` | Texto grande sobre el color de la marca, con barra de acento |
| `square` | 1080×1080 | | `photo` | Imagen a sangre con degradado (pasa `--image`); sin imagen usa un degradado de marca |
| `story` | 1080×1920 | | `center` | Anuncio o cita centrada |
| `banner` | 1200×628 | | | |
| `landscape` | 1920×1080 | | | |

- Avisa si el contraste texto/fondo o botón no llega a 4.5:1 (AA).
- Ajusta el tamaño del titular según su largo.
- Si tu navegador está en una ruta rara: `CHROME_PATH=/ruta/al/navegador`.
- Tipografías web: pon la URL de Google Fonts en `font_css_url` del `brand.json` (necesita internet al generar).

**Límite:** compone texto, color e imágenes que tú aportes. No crea fotos ni ilustraciones.

Ejemplos generados con `brand.example.json` y `pieces.example.json`: carpeta `examples/`.
