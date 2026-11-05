"""Gera a identidade visual fictícia do Hospital Mandalore (MM) para o Chatwoot.

Uso: python3 generate.py  ->  arquivos em ./public (copiados para /app/public no container)

Marca e cores podem ser trocadas por variáveis de ambiente (BRAND_NAME, BRAND_SHORT,
BRAND_LOGO_TOP, BRAND_LOGO_MAIN, BRAND_COLOR_TOP, BRAND_COLOR_BOTTOM, BRAND_COLOR_BADGE).
"""
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


NAME = os.environ.get("BRAND_NAME", "Hospital Mandalore")
SHORT = os.environ.get("BRAND_SHORT", "MM")
LOGO_TOP = os.environ.get("BRAND_LOGO_TOP", "HOSPITAL")
LOGO_MAIN = os.environ.get("BRAND_LOGO_MAIN", "Mandalore")
TOP = rgb(os.environ.get("BRAND_COLOR_TOP", "#12A4A8"))
BOTTOM = rgb(os.environ.get("BRAND_COLOR_BOTTOM", "#0B5C7A"))
BADGE = rgb(os.environ.get("BRAND_COLOR_BADGE", "#E53935"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

OUT = Path(__file__).parent / "public"
ASSETS = OUT / "brand-assets"
BASE = 1024


def hexcolor(rgb):
    return "#%02X%02X%02X" % rgb


def draw_icon(with_text=True, badge=False):
    s = BASE
    grad = Image.new("RGB", (s, s))
    gd = ImageDraw.Draw(grad)
    for y in range(s):
        t = y / (s - 1)
        gd.line([(0, y), (s, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(TOP, BOTTOM)))

    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.22), fill=255)
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    u = s / 512
    r = int(36 * u)
    d.rounded_rectangle([166 * u, 72 * u, 346 * u, 440 * u], radius=r, fill="white")
    d.rounded_rectangle([72 * u, 166 * u, 440 * u, 346 * u], radius=r, fill="white")

    if with_text:
        font = ImageFont.truetype(FONT, int(82 * u))
        d.text((s / 2, s / 2), SHORT, font=font, fill=BOTTOM, anchor="mm")

    if badge:
        cx, cy, br = 410 * u, 102 * u, 96 * u
        d.ellipse([cx - br - 16 * u, cy - br - 16 * u, cx + br + 16 * u, cy + br + 16 * u], fill="white")
        d.ellipse([cx - br, cy - br, cx + br, cy + br], fill=BADGE)
    return img


def save_png(img, name, size):
    img.resize((size, size), Image.LANCZOS).save(OUT / name, optimize=True)


def icon_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="mm-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{hexcolor(TOP)}"/>
      <stop offset="1" stop-color="{hexcolor(BOTTOM)}"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="112" fill="url(#mm-bg)"/>
  <rect x="166" y="72" width="180" height="368" rx="36" fill="#FFFFFF"/>
  <rect x="72" y="166" width="368" height="180" rx="36" fill="#FFFFFF"/>
  <text x="256" y="256" dy="0.35em" text-anchor="middle" fill="{hexcolor(BOTTOM)}"
        font-family="DejaVu Sans, Verdana, Arial, sans-serif" font-weight="700" font-size="82">{SHORT}</text>
</svg>
"""


def logo_svg(text_color, sub_color):
    inner = icon_svg().split("\n", 1)[1].rsplit("</svg>", 1)[0]
    top = (f"""  <text x="580" y="200" fill="{sub_color}" font-family="DejaVu Sans, Verdana, Arial, sans-serif"
        font-weight="700" font-size="104" letter-spacing="18">{LOGO_TOP}</text>
""" if LOGO_TOP else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1820" height="512" viewBox="0 0 1820 512">
  <g>{inner}  </g>
{top}  <text x="572" y="{main_y()}" fill="{text_color}" font-family="DejaVu Sans, Verdana, Arial, sans-serif"
        font-weight="700" font-size="196">{LOGO_MAIN}</text>
</svg>
"""


def main_y():
    return 400 if LOGO_TOP else 326


def logo_preview(text_color, sub_color, bg):
    h = 512
    img = Image.new("RGBA", (1820, h), bg)
    img.paste(draw_icon().resize((h, h), Image.LANCZOS), (0, 0), draw_icon().resize((h, h), Image.LANCZOS))
    d = ImageDraw.Draw(img)
    if LOGO_TOP:
        d.text((580, 200), " ".join(LOGO_TOP), font=ImageFont.truetype(FONT, 96), fill=sub_color, anchor="ls")
    d.text((572, main_y()), LOGO_MAIN, font=ImageFont.truetype(FONT, 196), fill=text_color, anchor="ls")
    return img


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)

    full = draw_icon(with_text=True)
    small = draw_icon(with_text=False)
    badge_small = draw_icon(with_text=False, badge=True)
    badge_full = draw_icon(with_text=True, badge=True)

    for size in (16, 32):
        save_png(small, f"favicon-{size}x{size}.png", size)
        save_png(badge_small, f"favicon-badge-{size}x{size}.png", size)
    save_png(full, "favicon-96x96.png", 96)
    save_png(badge_full, "favicon-badge-96x96.png", 96)
    save_png(full, "favicon-512x512.png", 512)

    for size in (57, 60, 72, 76, 114, 120, 144, 152, 180):
        save_png(full, f"apple-icon-{size}x{size}.png", size)
    for name in ("apple-icon.png", "apple-icon-precomposed.png",
                 "apple-touch-icon.png", "apple-touch-icon-precomposed.png"):
        save_png(full, name, 192)
    for size in (36, 48, 72, 96, 144, 192):
        save_png(full if size >= 48 else small, f"android-icon-{size}x{size}.png", size)
    for size in (70, 144, 150, 310):
        save_png(full, f"ms-icon-{size}x{size}.png", size)

    (ASSETS / "logo_thumbnail.svg").write_text(icon_svg(), encoding="utf-8")
    (ASSETS / "logo.svg").write_text(logo_svg(hexcolor(BOTTOM), hexcolor(TOP)), encoding="utf-8")
    (ASSETS / "logo_dark.svg").write_text(logo_svg("#FFFFFF", "#7FD8DB"), encoding="utf-8")

    densities = {36: "0.75", 48: "1.0", 72: "1.5", 96: "2.0", 144: "3.0", 192: "4.0"}
    manifest = {
        "name": NAME,
        "short_name": SHORT,
        "icons": [{"src": f"/android-icon-{s}x{s}.png", "sizes": f"{s}x{s}",
                   "type": "image/png", "density": d} for s, d in densities.items()],
        "start_url": "/",
        "display": "standalone",
        "background_color": hexcolor(BOTTOM),
        "theme_color": hexcolor(BOTTOM),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    preview = Path(__file__).parent / "preview"
    preview.mkdir(exist_ok=True)
    full.resize((256, 256), Image.LANCZOS).save(preview / "icon.png")
    logo_preview(BOTTOM, TOP, "white").save(preview / "logo.png")
    logo_preview("white", (127, 216, 219), (17, 24, 39)).save(preview / "logo_dark.png")
    strip = Image.new("RGBA", (16 + 32 + 96 + 32 * 4, 96 + 16), "white")
    x = 16
    for img, size in ((small, 16), (small, 32), (badge_small, 32), (full, 96)):
        strip.paste(img.resize((size, size), Image.LANCZOS), (x, 8), img.resize((size, size), Image.LANCZOS))
        x += size + 32
    strip.save(preview / "favicons.png")
    print("ok ->", OUT)


if __name__ == "__main__":
    main()
