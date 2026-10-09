"""Maakt de app iconen: voorkant van een moderne SUV bij nacht,
met een lichtbalk over de volle breedte en smalle koplampen eronder.
Gebruik: python3 extra/make_icons.py icons   (vereist Pillow)
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

out = sys.argv[1] if len(sys.argv) > 1 else "icons"

BG_TOP = (14, 20, 30)
BG_BOT = (4, 6, 10)
BODY = (34, 42, 54)
BODY_EDGE = (70, 84, 102)
LIGHT = (236, 246, 255)
GLOW = (130, 185, 255)


def gradient(s):
    img = Image.new("RGB", (s, s))
    d = ImageDraw.Draw(img)
    for y in range(s):
        t = y / s
        c = tuple(int(BG_TOP[i] * (1 - t) + BG_BOT[i] * t) for i in range(3))
        d.line([(0, y), (s, y)], fill=c)
    return img.convert("RGBA")


def draw(size, full_bleed=False):
    s = size * 4
    img = gradient(s)
    k = 0.86 if full_bleed else 1.0          # maskable: alles binnen de veilige zone
    cx, cy = s / 2, s * 0.52
    W = s * 0.86 * k                           # breedte van de neus
    H = s * 0.40 * k

    # carrosserie: afgeronde neus met motorkaplijn
    body = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    x0, x1 = cx - W / 2, cx + W / 2
    top, bot = cy - H * 0.45, cy + H * 0.55
    # voorruit en dak: trapezium boven de neus
    ws_top = top - H * 0.62
    bd.polygon([(x0 + W * 0.16, top + H * 0.05), (x1 - W * 0.16, top + H * 0.05),
                (x1 - W * 0.27, ws_top), (x0 + W * 0.27, ws_top)], fill=(26, 33, 44))
    bd.line([(x0 + W * 0.27, ws_top), (x1 - W * 0.27, ws_top)], fill=BODY_EDGE, width=max(2, int(s * 0.008)))
    # spiegels
    for side in (-1, 1):
        mx = cx + side * W * 0.44
        bd.ellipse([mx - W * 0.06, top - H * 0.16, mx + W * 0.06, top + H * 0.04], fill=BODY)
    bd.rounded_rectangle([x0, top, x1, bot], radius=int(H * 0.45), fill=BODY)
    # motorkaplijn: subtiele lichtere rand bovenaan de neus
    bd.arc([x0 + W * 0.02, top, x1 - W * 0.02, top + H * 0.9], 195, 345,
           fill=BODY_EDGE, width=max(2, int(s * 0.008)))
    # onderste luchtinlaat
    bd.rounded_rectangle([cx - W * 0.30, bot - H * 0.30, cx + W * 0.30, bot - H * 0.14],
                         radius=int(H * 0.08), fill=(20, 25, 33))
    img = Image.alpha_composite(img, body)

    # lichten: lichtbalk over de volle breedte + twee smalle koplampen
    lights = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lights)
    bar_y = cy - H * 0.16
    bar_h = max(3, s * 0.016)
    ld.rounded_rectangle([x0 + W * 0.07, bar_y - bar_h / 2, x1 - W * 0.07, bar_y + bar_h / 2],
                         radius=int(bar_h / 2), fill=LIGHT)
    hl_y = cy + H * 0.06
    hl_h = s * 0.034
    for side in (-1, 1):
        a = cx + side * W * 0.40
        b = cx + side * W * 0.22
        xa, xb = min(a, b), max(a, b)
        ld.rounded_rectangle([xa, hl_y - hl_h / 2, xb, hl_y + hl_h / 2], radius=int(hl_h / 2), fill=LIGHT)

    glow = lights.copy()
    tint = Image.new("RGBA", (s, s), GLOW + (0,))
    tint.putalpha(glow.split()[3])
    halo_big = tint.filter(ImageFilter.GaussianBlur(s * 0.05))
    halo_small = tint.filter(ImageFilter.GaussianBlur(s * 0.015))
    img = Image.alpha_composite(img, halo_big)
    img = Image.alpha_composite(img, halo_big)
    img = Image.alpha_composite(img, halo_small)
    img = Image.alpha_composite(img, lights)

    # lichtschijnsel op de grond
    floor = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    fd = ImageDraw.Draw(floor)
    fd.ellipse([cx - W * 0.55, bot + H * 0.05, cx + W * 0.55, bot + H * 0.35], fill=GLOW + (70,))
    img = Image.alpha_composite(img, floor.filter(ImageFilter.GaussianBlur(s * 0.04)))

    img = img.resize((size, size), Image.LANCZOS)
    if not full_bleed:
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
        img.putalpha(mask)
    return img


draw(192).save(f"{out}/icon-192.png")
draw(512).save(f"{out}/icon-512.png")
draw(512, full_bleed=True).save(f"{out}/icon-maskable-512.png")
draw(180, full_bleed=True).convert("RGB").save(f"{out}/apple-touch-icon.png")  # iPhone rondt zelf af
print("ok")
